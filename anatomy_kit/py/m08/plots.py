"""Module 8 plots (group `plots`): joint power (#8), cost of transport (#9) and the K1-K10 computed plots.

Every plotted number is computed here from the formula or the lab code module08.html states:
  #8   the joint-power template (a stated, drawn template: three Gaussian sums whose read-offs are the
       caption's 3.0 / -1.2 / 1.0 W/kg) and Lab 3's computed ankle power, overlaid as the caption's check;
  #9   CoT(v) = cs/v + cf v, calibrated from v* = 1.3 m/s, CoT* = 2.2 J/(kg m) (caption);
  K1   F_y = M cos(th) (g cos(th) - v(th)^2/ell), v^2 = v_mid^2 + 2 g ell (1 - cos th); stance time by
       integrating dt = ell dth / v; the measured double hump is Lab 3's assumed F_y shape;
  K2   Fr = v^2/(g ell); K3, K7 the section 7 cost proxy (Lab 2); K4 the exact simplest-walker cost;
  K5   Lab 3 verbatim; K6 the K6 recipe (seed 0 per rate, np.gradient twice); K8 H = 2 m d u;
  K9   E(n+1) = cos^2(2 alpha) E(n) + M g L sin(gamma); K10 the Prop 10.1 margin at the Lab 4 point.
The printed solution numbers are asserted.
"""
import html
import math

import numpy as np

import house as H
from m05 import plots_main as PM
from m05.plots_prob import Plot, label, legend, text_w, hov, svg, sub

O, I, SER = H.OVERLAY, H.INK, H.SERIES
GRID = "#e6e6e6"
BOX = "#f7f4ef"
W = 400                                     # problem figures: viewBox width = rendered width

# ---------------------------------------------------------------- reference gait (section 7, Lab 2)
G, M, ELL, V = 9.81, 70.0, 0.95, 1.3
KAPPA = 0.09
L_STAR = 0.6847                             # Lab 2's grid optimum, used by Labs 1 and 3
T_STRIDE = 2 * L_STAR / V


def cost(L, v=V, kappa=KAPPA):
    """Section 7 proxy C(v, L): transition + swing (J per step)."""
    a = np.arcsin(L / (2 * ELL))
    return 0.5 * M * v * v * np.sin(2 * a) ** 2 + kappa * M * (v / L) ** 2


def l_opt(v=V, kappa=KAPPA):
    """Interior minimum of the proxy on a fine grid over the feasible L < 2 ell sin 45 deg."""
    L = np.linspace(0.35, 1.3, 95001)
    c = cost(L, v, kappa)
    i = int(np.argmin(c))
    return float(L[i]), float(c[i])


def lab3():
    """Lab 3, verbatim: stance fraction s, time t, F_y, ankle moment, power."""
    Wt, T = M * G, 2 * L_STAR / V
    T_st = 0.62 * T
    s = np.linspace(0, 1, 601)
    t = s * T_st
    shape = np.sin(np.pi * s) ** 0.40 * (1 - 0.245 * np.cos(4 * np.pi * (s - 0.5)))
    Fy = shape * (Wt * T / 2) / np.trapezoid(shape, t)
    x_cop = -0.06 + 0.25 * s
    tau = Fy * x_cop
    omega = 2.3 * np.exp(-((s - 0.80) / 0.10) ** 2)
    return s, t, Fy, tau, tau * omega, T_st


def band_swatch(s, x, y, txt, col=BOX, op=1.0):
    return (f'<rect x="{x:.2f}" y="{y - 10:.2f}" width="20" height="11" fill="{col}" opacity="{op}" '
            f'stroke="{I["rule"]}" stroke-width="{s(0.6):.2f}"/>' + label(s, x + 25, y, txt, "label2", I["secondary"]))


def hollow(s, x, y, col):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(H.PX["dot"]):.2f}" fill="#fff" stroke="{col}" '
            f'stroke-width="{s(1.8):.2f}"/>')


def fdot(s, x, y, col, r=None):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r or H.PX["dot"]):.2f}" fill="{col}" stroke="#fff" '
            f'stroke-width="{s(1.5):.2f}"/>')


def mn(v, f="{:.2f}", plus=False):
    return PM.mn(v, f, plus)


# ================================================================ svg #8: joint power template + Lab 3 check
TEMPLATE = {                                # (amplitude W/kg, centre %, width %) of exp(-((p - c)/w)^2)
    "ankle": ((-0.5, 10, 5.0), (3.0, 50, 5.5)),
    "knee": ((-1.2, 16, 6.0), (0.5, 42, 9.0), (-0.9, 70, 8.0)),
    "hip": ((1.0, 14, 10.0), (-0.6, 46, 10.0), (0.7, 86, 10.0)),
}


def template(name, p):
    return sum(a * np.exp(-((p - c) / w) ** 2) for a, c, w in TEMPLATE[name])


def fig8():
    VB = (0, 0, 760, 428)
    s = H.Scale(VB[2], VB[3])
    ax = PM.Ax((84, 92, 650, 362), (0, 100), (-2.0, 3.5))
    p = np.linspace(0, 100, 101)
    cur = {k: template(k, p) for k in TEMPLATE}
    ia, ik, ih = int(cur["ankle"].argmax()), int(cur["knee"].argmin()), int(cur["hip"].argmax())
    pk = {"ankle": (p[ia], cur["ankle"][ia]), "knee": (p[ik], cur["knee"][ik]), "hip": (p[ih], cur["hip"][ih])}
    assert [round(v[1], 1) for v in pk.values()] == [3.0, -1.2, 1.0] and [round(v[0]) for v in pk.values()] == [50, 16, 14]
    s3, _, _, _, P3, _ = lab3()
    p3, w3 = 62 * s3, P3 / M                                     # stance = 0-62 % of the cycle (Lab 3)
    i3 = int(w3.argmax())
    assert round(w3[i3], 2) == 3.06 and round(p3[i3]) == 49
    o = [f'<rect x="{ax.X(40):.2f}" y="{ax.top:.2f}" width="{ax.X(62) - ax.X(40):.2f}" height="{ax.y0 - ax.top:.2f}" fill="{BOX}"/>']
    o += PM.axes(s, ax, [(v, f"{v}") for v in range(0, 101, 10)],
                 [(v, PM.mn(v, "{:.0f}")) for v in (-2, -1, 0, 1, 2, 3)], "gait cycle (% from heel strike)",
                 "joint power (W kg⁻¹)", ylab_x=30)
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["rule"], "ref"))
    # gait phases above the plot: stance 0-62 %, swing 62-100 %
    yb = 64
    for a, b, txt in ((0, 62, "stance (0–62 %)"), (62, 100, "swing")):
        o.append(f'<rect x="{ax.X(a):.2f}" y="{yb - 12:.2f}" width="{ax.X(b) - ax.X(a):.2f}" height="16" fill="#fff" '
                 f'stroke="{I["rule"]}" stroke-width="{s(1):.2f}"/>')
        o.append(label(s, ax.X((a + b) / 2), yb + 1, txt, "label2", I["secondary"], "middle"))
    o.append(label(s, ax.X(51), ax.Y(-1.05), "A2 push-off burst", "label2", I["primary"], "middle"))
    o.append(label(s, ax.X(51), ax.Y(-1.05) + 16, "40–62 %", "label2", I["secondary"], "middle"))
    for k, name in enumerate(("hip", "knee", "ankle")):
        o.append(PM.curve(s, ax, p, cur[name], SER[("ankle", "knee", "hip").index(name)], "curve_multi"))
    o.append(PM.curve(s, ax, p3[::6], w3[::6], I["primary"], "curve_multi", PM.DASH_SER))
    for name, (x, y) in pk.items():
        o.append(fdot(s, ax.X(x), ax.Y(y), SER[("ankle", "knee", "hip").index(name)]))
    o.append(label(s, ax.X(53.5), ax.Y(2.9), f"ankle {pk['ankle'][1]:.1f} at {pk['ankle'][0]:.0f} %", "label2"))
    o.append(label(s, ax.X(53.5), ax.Y(2.9) + 16, f"Lab 3: {w3[i3]:.2f} at {p3[i3]:.0f} %", "label2", I["secondary"]))
    o.append(label(s, ax.X(pk["knee"][0]), ax.Y(pk["knee"][1]) + 24, f"knee {mn(pk['knee'][1], '{:.1f}')} at {pk['knee'][0]:.0f} %",
                   "label2", I["primary"], "middle"))
    o.append(label(s, ax.X(pk["hip"][0]), ax.Y(pk["hip"][1]) - 12, f"hip {pk['hip'][1]:.1f} at {pk['hip'][0]:.0f} %",
                   "label2", I["primary"], "middle"))
    o.append(label(s, ax.x1 + 8, ax.Y(0) - 8, "generates", "label2", I["secondary"]))
    o.append(label(s, ax.x1 + 8, ax.Y(0) + 18, "absorbs", "label2", I["secondary"]))
    o += PM.legend(s, 84, 26, [(SER[0], None, "ankle"), (SER[1], None, "knee"), (SER[2], None, "hip"),
                               (I["primary"], PM.DASH_SER, "ankle, Lab 3 (computed)")])
    aria = ("Joint power in watts per kilogram against percent of the gait cycle for ankle, knee and hip, a drawn "
            "template. The ankle absorbs slightly in early stance and peaks at 3.0 at 50 percent inside the shaded A2 "
            "push-off band, 40 to 62 percent. The knee absorbs most at minus 1.2 at 16 percent and again in late swing; "
            "the hip peaks at 1.0 at 14 percent. A dashed curve, Lab 3's computed ankle power, peaks at 3.06 at 49 "
            "percent. A bar above the plot marks stance, 0 to 62 percent, and swing.")
    pts = []
    for i in range(len(p)):
        y3 = float(np.interp(p[i], p3, w3)) if p[i] <= 62 else 0.0
        pts.append([ax.X(p[i]), [ax.Y(cur["ankle"][i]), ax.Y(cur["knee"][i]), ax.Y(cur["hip"][i])],
                    f"{p[i]:.0f} %: ankle {mn(cur['ankle'][i])}, knee {mn(cur['knee'][i])}, hip {mn(cur['hip'][i])}, "
                    f"Lab 3 ankle {mn(y3)} W/kg"])
    return PM.svg(VB, aria, s, o, H.hover_attr(ax.box, pts))


# ================================================================ svg #9: cost of transport
def fig9():
    VB = (0, 0, 760, 404)
    s = H.Scale(VB[2], VB[3])
    v_s, cot_s = 1.3, 2.2                                        # assumed (caption)
    cs, cf = v_s * cot_s / 2, cot_s / (2 * v_s)
    assert (round(cs, 2), round(cf, 2)) == (1.43, 0.85)
    ax = PM.Ax((84, 56, 730, 324), (0.4, 2.2), (0, 4.0))
    v = np.linspace(0.4, 2.2, 109)
    slow, fast = cs / v, cf * v
    tot = slow + fast
    i = int(np.argmin(tot))
    assert abs(v[i] - 1.3) < 0.008 and round(tot[i], 2) == 2.2
    o = PM.axes(s, ax, [(x, f"{x:.1f}") for x in (0.5, 1.0, 1.3, 1.5, 2.0)],
                [(y, f"{y:.0f}") for y in (0, 1, 2, 3, 4)], "walking speed v (m s⁻¹)",
                "cost of transport (J kg⁻¹ m⁻¹)", ylab_x=30)
    o.append(H.line(s, ax.X(1.3), ax.y0, ax.X(1.3), ax.Y(cot_s), I["rule"], "ref", H.DASH_REF))
    o.append(H.line(s, ax.x0, ax.Y(cot_s), ax.X(1.3), ax.Y(cot_s), I["rule"], "ref", H.DASH_REF))
    o.append(PM.curve(s, ax, v, slow, SER[1], "curve_multi", PM.DASH_SER))
    o.append(PM.curve(s, ax, v, fast, SER[2], "curve_multi", PM.DASH_SER))
    o.append(PM.curve(s, ax, v, tot, SER[0]))
    o.append(fdot(s, ax.X(1.3), ax.Y(cs / 1.3), I["secondary"], 3.2))
    o.append(fdot(s, ax.X(1.3), ax.Y(cot_s), SER[0]))
    o.append(label(s, ax.X(1.3), ax.Y(2.62), "minimum: v* = 1.3 m s⁻¹, CoT* = 2.2 J kg⁻¹ m⁻¹", "label2", I["primary"], "middle"))
    o.append(label(s, ax.X(1.36), ax.Y(0.3), f"at v* the two terms are equal, {cs / 1.3:.2f} each",
                   "label2", I["secondary"]))
    o.append(label(s, ax.X(2.18), ax.Y(3.85), f"CoT = c{sub('s', s, 'label2')}/v + c{sub('f', s, 'label2')} v",
                   "label2", I["primary"], "end"))
    o.append(label(s, ax.X(0.95), ax.Y(1.72), f"support-time c{sub('s', s, 'label2')}/v", "label2",
                   I["primary"], "start"))
    o.append(label(s, ax.X(2.18), ax.Y(1.1), f"transition-and-swing term c{sub('f', s, 'label2')} v",
                   "label2", I["primary"], "end"))
    o.append(label(s, ax.X(2.18), ax.Y(3.85) + 18, f"c{sub('s', s, 'label2')} = {cs:.2f} J kg⁻¹ s⁻¹", "label2",
                   I["secondary"], "end"))
    o.append(label(s, ax.X(2.18), ax.Y(3.85) + 35, f"c{sub('f', s, 'label2')} = {cf:.2f} J s kg⁻¹ m⁻²", "label2",
                   I["secondary"], "end"))
    o += PM.legend(s, 84, 30, [(SER[0], None, "total CoT(v)"), (SER[1], PM.DASH_SER, "support-time term"),
                               (SER[2], PM.DASH_SER, "transition-and-swing term")])
    aria = ("Cost of transport against walking speed from 0.4 to 2.2 metres per second: the total, a U-shaped curve, "
            "is the sum of a falling support-time term cs over v and a rising transition-and-swing term cf times v, both "
            "drawn dashed. The minimum is marked at 1.3 metres per second and 2.2 joules per kilogram per metre, where "
            f"the two terms are equal at {cs / 1.3:.2f} each; cs = {cs:.2f} and cf = {cf:.2f}.")
    hv = [[ax.X(v[k]), [ax.Y(tot[k]), ax.Y(slow[k]), ax.Y(fast[k])],
           f"v = {v[k]:.2f} m/s: CoT {tot[k]:.2f} = {slow[k]:.2f} + {fast[k]:.2f} J/(kg m)"] for k in range(len(v))]
    return PM.svg(VB, aria, s, o, H.hover_attr(ax.box, hv))


# ================================================================ svg #37 K1: rigid-vault vertical GRF
def vault(alpha_deg, v_mid=V, n=801):
    a = math.radians(alpha_deg)
    th = np.linspace(-a, a, n)
    v2 = v_mid ** 2 + 2 * G * ELL * (1 - np.cos(th))
    fy = np.cos(th) * (np.cos(th) - v2 / (G * ELL))            # F_y / W
    rate = np.sqrt(v2) / ELL                                  # d theta / dt
    t = np.concatenate([[0], np.cumsum(0.5 * (1 / rate[1:] + 1 / rate[:-1]) * np.diff(th))])
    return 100 * t / t[-1], fy


def fig37():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (56, 66, 330, 248), (0, 100), (0, 1.25))
    curves = {a: vault(a) for a in (12, 16, 20)}
    edge = {a: float(c[1][0]) for a, c in curves.items()}
    assert [round(edge[a], 3) for a in (12, 16, 20)] == [0.737, 0.675, 0.599]
    assert round(float(vault(21.1)[1][0]), 3) == 0.576 and round(float(curves[12][1][400]), 3) == 0.819
    s3, _, Fy, _, _, _ = lab3()
    fw = Fy / (M * G)
    ip = int(fw[:300].argmax())
    assert (round(fw[ip], 2), round(100 * s3[ip]), round(fw[300], 2)) == (1.10, 28, 0.75)
    o = [P.axes([(x, f"{x}") for x in (0, 25, 50, 75, 100)], [(y, f"{y:g}") for y in (0, 0.25, 0.5, 0.75, 1.0, 1.25)],
                "percent of stance (time)", f"vertical GRF F{sub('y', s)}/W", grid=(0.25, 0.5, 0.75, 1.25), ytx=14)]
    o.append(H.line(s, P.x0, P.Y(1), P.x1, P.Y(1), I["rule"], "ref", H.DASH_REF))
    o.append(label(s, P.X(50), P.Y(1) - 6, "body weight", "label2", I["muted"], "middle"))
    o.append(P.curve(100 * s3, fw, I["primary"], multi=True, dash=PM.DASH_SER))
    for k, a in enumerate((12, 16, 20)):
        o.append(P.curve(*curves[a], SER[k], multi=True))
    o.append(P.dot(50, 1 - V * V / (G * ELL), I["primary"]))
    o.append(label(s, P.X(50), P.Y(0.819) + 22, "vault peak 1 − Fr = 0.819", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(50), P.Y(0.819) + 38, "measured trough 0.75", "label2", I["secondary"], "middle"))
    o.append(label(s, P.X(28), P.Y(1.10) - 8, "measured 1.10", "label2", I["secondary"], "middle"))
    for (a, yy) in ((12, edge[12] + 0.035), (16, edge[16]), (20, edge[20] - 0.035)):
        y = P.Y(yy) + 4.5
        o.append(H.line(s, P.x1 + 1, P.Y(edge[a]), P.x1 + 6, y - 4.5, SER[(12, 16, 20).index(a)], "leader"))
        o.append(label(s, P.x1 + 8, y, f"{a}°: {edge[a]:.3f}", "label2", I["primary"]))
    o.append(legend(s, 56, 18, [(SER[0], "vault α = 12°", None), (SER[1], "16°", None), (SER[2], "20°", None)]))
    o.append(legend(s, 56, 38, [(I["primary"], "measured double hump (Lab 3)", PM.DASH_SER)]))
    aria = ("Problem K1 plot: vertical ground reaction over body weight against percent of stance time. The rigid "
            "vault gives a single hump for step half-angles 12, 16 and 20 degrees, each peaking at 1 minus Fr = 0.819 "
            "at midstance and falling to 0.737, 0.675 and 0.599 at the step edges. The dashed measured double hump of "
            "Lab 3 peaks at 1.10 at 28 and 72 percent with a 0.75 trough at midstance: the opposite shape, and above "
            "body weight where the vault never goes.")
    xs = np.linspace(0, 100, 201)
    ys = [np.interp(xs, *curves[a]) for a in (12, 16, 20)] + [np.interp(xs, 100 * s3, fw)]
    hv = hov(P, xs, ys, lambda i: f"{xs[i]:.1f} % of stance: vault {ys[0][i]:.3f}, {ys[1][i]:.3f}, {ys[2][i]:.3f}; "
                                  f"measured {ys[3][i]:.3f} W")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #38 K2: Froude number read both ways
def fig38():
    VB = (0, 0, W, 296)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (56, 62, 322, 244), (0.6, 2.4), (0, 0.9))
    v = np.linspace(0.6, 2.4, 181)
    ells = (0.80, 0.95, 1.10)
    fr = {l: v ** 2 / (G * l) for l in ells}
    assert [round(1.3 ** 2 / (G * l), 3) for l in ells] == [0.215, 0.181, 0.157]
    assert [round(math.sqrt(0.5 * G * l), 2) for l in ells] == [1.98, 2.16, 2.32]
    l1, l2 = 2.1 ** 2 / (0.5 * G), 1.9 ** 2 / (0.5 * G)
    lo, hi = 2.1 ** 2 / (0.6 * G), 2.1 ** 2 / (0.4 * G)
    assert (round(l1, 3), round(l2, 3), round(lo, 3), round(hi, 3)) == (0.899, 0.736, 0.749, 1.124)
    o = [f'<rect x="{P.x0:.2f}" y="{P.Y(0.6):.2f}" width="{P.x1 - P.x0:.2f}" height="{P.Y(0.4) - P.Y(0.6):.2f}" fill="{BOX}"/>']
    o.append(P.axes([(x, f"{x:.1f}") for x in (0.6, 1.0, 1.4, 1.8, 2.2)], [(y, f"{y:.1f}") for y in (0, 0.2, 0.4, 0.6, 0.8)],
                    "walking speed v (m s⁻¹)", "Froude number Fr = v²/(gℓ)", grid=(0.2, 0.4, 0.6, 0.8), ytx=14))
    o.append(H.line(s, P.x0, P.Y(0.5), P.x1, P.Y(0.5), I["primary"], "ref", H.DASH_REF))
    for k, l in enumerate(ells):
        o.append(P.curve(v, fr[l], SER[k], multi=True))
    o.append(H.line(s, P.X(2.1), P.Y(0.4), P.X(2.1), P.Y(0.6), O["geometry"], "geom"))
    for f in (0.4, 0.6):
        o.append(H.line(s, P.X(2.1) - 4, P.Y(f), P.X(2.1) + 4, P.Y(f), O["geometry"], "geom"))
    o.append(hollow(s, P.X(2.1), P.Y(0.5), I["primary"]))
    o.append(label(s, P.X(0.66), P.Y(0.85), "transition at 2.1 m s⁻¹, Fr* = 0.5:", "label2"))
    o.append(label(s, P.X(0.66), P.Y(0.85) + 16, f"ℓ = v²/(Fr* g) = {l1:.3f} m", "label2"))
    o.append(label(s, P.X(0.66), P.Y(0.85) + 32, f"Fr* = 0.6 to 0.4: ℓ = {lo:.3f} to {hi:.3f} m", "label2",
                   I["secondary"]))
    o.append(label(s, P.X(1.0), P.Y(0.5) - 7, "Fr* = 0.5", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(0.66), P.Y(0.4) - 4, "walk–run band", "label2", I["muted"]))
    for k, l in enumerate(ells):
        o.append(label(s, P.x1 + 6, P.Y(fr[l][-1]) + 4.5, f"ℓ = {l:.2f} m", "label2"))
    o.append(legend(s, 56, 20, [(SER[0], "ℓ = 0.80 m", None), (SER[1], "0.95 m", None), (SER[2], "1.10 m", None)]))
    o.append(band_swatch(s, 56, 40, "walk–run band, Fr 0.4–0.6"))
    aria = ("Problem K2 plot: Froude number v squared over g ell against walking speed from 0.6 to 2.4 metres per "
            "second for leg lengths 0.80, 0.95 and 1.10 metres. A shaded band from Fr 0.4 to 0.6 is the walk-run range "
            "with a dashed line at Fr* = 0.5. A ring at 2.1 metres per second on that line inverts to ell = 0.899 metres; "
            "a bar across the band shows that Fr* from 0.6 to 0.4 moves it from 0.749 to 1.124 metres.")
    hv = hov(P, v, [fr[l] for l in ells], lambda i: f"v = {v[i]:.2f} m/s: Fr = {fr[0.8][i]:.3f}, {fr[0.95][i]:.3f}, "
                                                    f"{fr[1.1][i]:.3f} (ℓ = 0.80, 0.95, 1.10 m)")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svgs #39 K3 and #43 K7: the cost proxy
def proxy_fig(kind):
    VB = (0, 0, W, 296)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (56, 64, 388, 236), (0.42, 1.05), (0, 120))
    L = np.linspace(0.42, 1.05, 316)
    if kind == "K3":
        cases = [(V, k) for k in (0.05, 0.09, 0.15)]
        names = ["κ = 0.05 m²", "0.09 m² (reference)", "0.15 m²"]
    else:
        cases = [(v, KAPPA) for v in (1.0, 1.3, 1.6)]
        names = ["v = 1.0 m s⁻¹", "1.3 m s⁻¹", "1.6 m s⁻¹"]
    opt = [l_opt(v, k) for v, k in cases]
    if kind == "K3":
        assert [round(x[0], 3) for x in opt] == [0.577, 0.684, 0.807]
    else:
        assert [round(x[0], 3) for x in opt] == [0.684] * 3
        assert [round(v / x[0], 2) for (v, _), x in zip(cases, opt)] == [1.46, 1.90, 2.34]
    c09 = cost(np.array([0.6844]))[0]
    assert round(c09, 1) == 49.4
    o = [P.axes([(x, f"{x:.1f}") for x in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)], [(y, f"{y}") for y in (0, 30, 60, 90, 120)],
                "step length L (m)" + ("" if kind == "K3" else ", cadence c = v/L"),
                "cost proxy C per step (J)", grid=(30, 60, 90, 120), ytx=14)]
    if kind == "K7":
        o.append(H.line(s, P.X(opt[0][0]), P.y0, P.X(opt[0][0]), P.Y(112), I["rule"], "ref", H.DASH_REF))
        o.append(label(s, P.X(opt[0][0]) + 5, P.Y(112) + 4, "all three minima at", "label2"))
        o.append(label(s, P.X(opt[0][0]) + 5, P.Y(112) + 20, f"L* = {opt[0][0]:.3f} m", "label2"))
    ys = [cost(L, v, k) for v, k in cases]
    for k in range(3):
        o.append(P.curve(L, ys[k], SER[k], multi=True))
    for k in range(3):
        o.append(P.dot(opt[k][0], opt[k][1], SER[k]))
    if kind == "K3":
        o.append(label(s, P.X(0.43), P.Y(8), "L* =", "label2", I["secondary"]))
        for k, (lx, cx) in enumerate(opt):
            o.append(H.line(s, P.X(lx), P.Y(cx) + 5, P.X(lx), P.Y(16), SER[k], "leader"))
            o.append(label(s, P.X(lx), P.Y(8), f"{lx:.3f} m", "label2", I["primary"], "middle"))
        o.append(label(s, P.X(1.04), P.Y(108), "dots: interior minimum", "label2", I["secondary"], "end"))
    else:
        for k, ((v, _), (lx, cx)) in enumerate(zip(cases, opt)):
            o.append(label(s, P.X(lx) + 8, P.Y(cx) + 17, f"c* = {v / lx:.2f} steps s⁻¹", "label2"))
        o.append(label(s, P.X(opt[0][0]) + 5, P.Y(112) + 36, "(Mv² divides out, D8)", "label2", I["secondary"]))
    o.append(legend(s, 56, 18, [(SER[0], names[0], None), (SER[1], names[1], None)]))
    o.append(legend(s, 56, 38, [(SER[2], names[2], None)]))
    o.append(label(s, 388, 38, "v = 1.3 m s⁻¹" if kind == "K3" else "κ = 0.09 m²", "label2", I["secondary"], "end"))
    if kind == "K3":
        aria = ("Problem K3 plot: the per-step cost proxy against step length at 1.3 metres per second for swing "
                "coefficients kappa 0.05, 0.09 and 0.15 square metres, each curve marked at its interior minimum. The "
                "optimum moves from 0.577 to 0.684 to 0.807 metres: tripling kappa moves it by 40 percent, the fourth-root "
                "scaling of D8.")
        fmt = lambda i: (f"L = {L[i]:.3f} m: C = {ys[0][i]:.1f}, {ys[1][i]:.1f}, {ys[2][i]:.1f} J "  # noqa: E731
                         f"(κ = 0.05, 0.09, 0.15)")
    else:
        aria = ("Problem K7 plot: the per-step cost proxy against step length at 1.0, 1.3 and 1.6 metres per second, "
                "with cadence fixed by c = v over L, each curve marked at its minimum. All three minima fall at the same "
                "0.684 metre step length, on one dashed line, so the model carries the whole speed change on cadence: "
                "1.46, 1.90 and 2.34 steps per second.")
        fmt = lambda i: (f"L = {L[i]:.3f} m: C = {ys[0][i]:.1f}, {ys[1][i]:.1f}, {ys[2][i]:.1f} J "  # noqa: E731
                         f"(v = 1.0, 1.3, 1.6)")
    hv = hov(P, L, ys, fmt)
    return svg(VB, aria, s, "".join(o), (P.box, hv))


def fig39():
    return proxy_fig("K3")


def fig43():
    return proxy_fig("K7")


# ================================================================ svg #40 K4: push-off fraction
def fig40():
    VB = (0, 0, W, 290)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (56, 62, 388, 238), (0, 1.0), (0, 30))
    two_a = 2 * math.asin(L_STAR / (2 * ELL))                # Lab 2's reference step, 2 alpha = 42.25 deg
    e0 = 0.5 * M * V * V

    def exact(f):
        return e0 * np.sin((1 - f) * two_a) ** 2 / np.cos(two_a * f) ** 2

    f = np.linspace(0, 1, 201)
    ex, sa = exact(f), exact(0.0) * (1 - f) ** 2                # small-angle law: 1/n^2 = (1 - f)^2
    base = float(exact(0.0))
    near = lambda a, b, tol: all(abs(p - q) <= tol for p, q in zip(a, b))   # noqa: E731
    # K4's printed values: 26.73, 16.88, 8.83, 2.74 J; ratios 1.000, 0.330, 0.169, 0.103 (4th-digit rounding)
    assert round(e0, 2) == 59.15 and near([base] + [float(exact(x)) for x in (0.25, 0.5, 0.75)], [26.73, 16.88, 8.83, 2.74], 0.011)
    ns = (1, 2, 3, 4)
    fn = [1 - 1 / n for n in ns]
    assert near([float(exact(x)) / base for x in fn], [1.0, 0.330, 0.169, 0.103], 0.0006)
    assert round(base / 4, 2) == 6.68
    o = [P.axes([(x, f"{x:g}") for x in (0, 0.25, 0.5, 0.75, 1)], [(y, f"{y}") for y in (0, 10, 20, 30)],
                "push-off fraction f of the redirection", "energy supplied per step (J)", grid=(10, 20, 30), ytx=14)]
    o.append(P.curve(f, sa, SER[1], multi=True, dash=PM.DASH_SER))
    o.append(P.curve(f, ex, SER[0], multi=True))
    for n, x in zip(ns, fn):
        o.append(P.dot(x, float(exact(x)), SER[0]))
        if n > 1:
            o.append(hollow(s, P.X(x), P.Y(base / n ** 2), SER[1]))
    for n, x, dx, dy in ((1, 0.0, 10, 4), (2, 0.5, 2, -10), (3, 2 / 3, 0, -10), (4, 0.75, 6, -10)):
        o.append(label(s, P.X(x) + dx, P.Y(float(exact(x))) + dy, f"n = {n}" if n < 3 else f"{n}", "label2",
                       I["primary"], "start" if n == 1 else "middle"))
    o.append(label(s, P.X(0.47), P.Y(25), "n = 2 (f = 0.5): exact 8.83 J,", "label2"))
    o.append(label(s, P.X(0.47), P.Y(25) + 16, "small-angle 6.68 J", "label2"))
    o.append(label(s, P.X(0.47), P.Y(25) + 32, "ratio 0.330, not 0.250", "label2", I["secondary"]))
    o.append(legend(s, 56, 18, [(SER[0], "exact simplest walker", None)]))
    o.append(legend(s, 56, 38, [(SER[1], "small-angle 1/n², n = 1/(1−f)", PM.DASH_SER)]))
    aria = ("Problem K4 plot: energy supplied per step against the fraction f of the step-to-step redirection done by "
            "push-off, for the reference gait. The exact simplest-walker cost falls from 26.73 joules at f = 0 through "
            "16.88 at 0.25, 8.83 at 0.5 and 2.74 at 0.75. The dashed small-angle law 26.73 times (1 minus f) squared, "
            "with its 1 over n squared points at n = 2, 3, 4, lies below it everywhere: 6.68 joules against the exact "
            "8.83 at n = 2.")
    hv = hov(P, f[:200], [ex[:200], sa[:200]], lambda i: f"f = {f[i]:.3f}: exact {ex[i]:.2f} J, small-angle {sa[i]:.2f} J")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #41 K5: Lab 3's ankle power
def fig41():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (60, 40, 388, 228), (0, 100), (0, 240))
    sx, t, _, _, Pw, T_st = lab3()
    wpos = float(np.trapezoid(np.maximum(Pw, 0), t))
    i = int(Pw.argmax())
    loss = 0.5 * M * V * V * math.sin(2 * math.asin(L_STAR / (2 * ELL))) ** 2
    hm = sx[Pw > Pw.max() / 2]
    dur = (hm.max() - hm.min()) * T_st
    assert (round(wpos, 1), round(Pw[i]), round(100 * sx[i]), round(loss, 1), round(100 * wpos / loss)) == (22.5, 214, 79, 26.7, 84)
    pc = 100 * sx
    pos = np.maximum(Pw, 0)
    area = " ".join(f"{P.X(pc[k]):.1f},{P.Y(pos[k]):.1f}" for k in range(0, len(pc), 3))
    o = [f'<polygon points="{P.X(0):.1f},{P.Y(0):.1f} {area} {P.X(100):.1f},{P.Y(0):.1f}" fill="{SER[0]}" opacity="0.16"/>']
    o.append(P.axes([(x, f"{x}") for x in (0, 25, 50, 75, 100)], [(y, f"{y}") for y in (0, 80, 160, 240)],
                    f"percent of stance (stance = {T_st:.3f} s)", "ankle power P = τω (W)", grid=(80, 160, 240), ytx=14))
    o.append(P.curve(pc, Pw, SER[0]))
    o.append(P.dot(pc[i], Pw[i], SER[0]))
    o.append(label(s, P.X(72), P.Y(222), f"peak {Pw[i]:.0f} W ({Pw[i] / M:.2f} W kg⁻¹)", "label2", I["primary"], "end"))
    o.append(label(s, P.X(72), P.Y(222) + 16, f"at {pc[i]:.0f} % of stance", "label2", I["secondary"], "end"))
    o.append(H.line(s, P.X(72) + 2, P.Y(222) - 4, P.X(pc[i]) - 5, P.Y(Pw[i]), I["rule"], "leader"))
    y = P.Y(110)
    o.append(H.line(s, P.X(hm.min() * 100), y, P.X(hm.max() * 100), y, O["dim"], "ref"))
    for xx in (hm.min(), hm.max()):
        o.append(H.line(s, P.X(xx * 100), y - 4, P.X(xx * 100), y + 4, O["dim"], "ref"))
    o.append(label(s, P.X(hm.min() * 100) - 5, y + 4, f"half max: {dur:.3f} s", "label2", I["secondary"], "end"))
    # the energy books: positive ankle work against the transition loss of the same step
    bx, by, bw = P.X(3), 172, 120
    o.append(label(s, bx, by - 6, f"ankle positive work {wpos:.1f} J", "label2"))
    o.append(f'<rect x="{bx:.2f}" y="{by:.2f}" width="{bw * wpos / loss:.2f}" height="10" fill="{SER[0]}" opacity="0.55"/>')
    o.append(label(s, bx + bw * wpos / loss + 6, by + 9.5, f"= {100 * wpos / loss:.0f} %", "label2", I["secondary"]))
    o.append(label(s, bx, by + 30, f"transition loss {loss:.1f} J", "label2"))
    o.append(f'<rect x="{bx:.2f}" y="{by + 36:.2f}" width="{bw:.2f}" height="10" fill="{I["rule"]}"/>')
    aria = ("Problem K5 plot: Lab 3's ankle power over stance, negligible until about 60 percent of stance and then a "
            f"single late burst peaking at {Pw[i]:.0f} watts, {Pw[i] / M:.2f} watts per kilogram, at {pc[i]:.0f} percent. "
            f"The shaded positive area is {wpos:.1f} joules and the burst is {dur:.3f} seconds wide at half maximum. Two "
            f"bars compare it with the {loss:.1f} joule transition loss of the same step: {100 * wpos / loss:.0f} percent.")
    k = np.arange(0, len(pc), 3)
    hv = [[P.X(pc[j]), P.Y(Pw[j]), f"{pc[j]:.1f} % of stance (t = {t[j]:.3f} s): P = {Pw[j]:.1f} W"] for j in k]
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #42 K6: noise gain of double differentiation
def k6_rms(fs, sig=0.002, I6=0.035):
    rng = np.random.default_rng(0)
    t = np.arange(0, 1, 1 / fs)
    th = 0.35 * np.sin(2 * np.pi * t)
    dt = 1 / fs
    acc_n = np.gradient(np.gradient(th + rng.normal(0, sig, t.size), dt), dt)
    acc_c = np.gradient(np.gradient(th, dt), dt)
    return float(np.sqrt(np.mean((I6 * (acc_n - acc_c)) ** 2)))


def fig42():
    VB = (0, 0, W, 290)
    s = H.Scale(W, VB[3], display_w=400)
    I6, sig = 0.035, 0.002
    rates = (60, 120, 240)
    rms = [k6_rms(f) for f in rates]
    assert [round(r, 3) for r in rms] == [0.137, 0.556, 2.468]
    ana = lambda f: I6 * sig * math.sqrt(6) * f ** 2 / 4       # noqa: E731
    assert [round(ana(f), 3) for f in rates] == [0.154, 0.617, 2.469]
    true = I6 * 0.35 * (2 * math.pi) ** 2
    assert round(true, 3) == 0.484
    fx = math.sqrt(true / ana(1.0))
    lx = math.log10
    P = Plot(s, (60, 54, 388, 238), (lx(40), lx(320)), (lx(0.05), lx(5)))
    o = [P.axes([(lx(f), f"{f}") for f in (60, 120, 240)], [(lx(y), f"{y:g}") for y in (0.05, 0.1, 0.5, 1, 5)],
                "sample rate fₛ (Hz), log scale", "RMS torque error (N m), log", grid=(lx(0.1), lx(1)), ytx=14)]
    o.append(H.line(s, P.x0, P.Y(lx(true)), P.x1, P.Y(lx(true)), I["primary"], "ref", H.DASH_REF))
    fr = np.geomspace(40, 320, 121)
    o.append(P.curve(np.log10(fr), np.log10(ana(fr)), SER[1], multi=True, dash=PM.DASH_SER))
    o.append(P.curve([lx(f) for f in rates], [lx(r) for r in rms], SER[0], multi=True))
    for f, r in zip(rates, rms):
        o.append(P.dot(lx(f), lx(r), SER[0]))
    o.append(hollow(s, P.X(lx(fx)), P.Y(lx(true)), I["primary"]))
    o.append(label(s, P.X(lx(fx)) - 8, P.Y(lx(true)) - 8, f"crossing ≈ {fx:.0f} Hz", "label2", I["primary"], "end"))
    o.append(label(s, P.x1 - 2, P.Y(lx(true)) + 16, f"true torque {true:.3f} N m", "label2", I["primary"], "end"))
    o.append(label(s, P.X(lx(150)), P.Y(lx(0.13)), "slope 2: error ∝ fₛ²", "label2", I["secondary"]))
    o.append(legend(s, 60, 16, [(SER[0], "sampled, seed 0: " + ", ".join(f"{r:.3f}" for r in rms) + " N m", None)]))
    o.append(legend(s, 60, 34, [(SER[1], "analytic Iσ√6 fₛ²/4", PM.DASH_SER), (I["primary"], "true torque", H.DASH_REF)]))
    aria = ("Problem K6 plot on logarithmic axes: RMS inverse-dynamics torque error against sample rate. The sampled "
            "errors are 0.137, 0.556 and 2.468 newton metres at 60, 120 and 240 hertz; the dashed analytic line I sigma "
            "root 6 fs squared over 4 has slope 2. Both cross the true segment torque of 0.484 newton metres, a dashed "
            f"horizontal line, between 60 and 120 hertz; the analytic crossing is at {fx:.0f} hertz.")
    hv = [[P.X(float(np.log10(f))), [P.Y(float(np.log10(ana(f))))],
           f"fₛ = {f:.0f} Hz: analytic {ana(f):.3f} N m" + "".join(f"; sampled {r:.3f}" for q, r in zip(rates, rms) if abs(q - f) < 1.2)]
          for f in fr]
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #44 K8: yaw angular momentum
def fig44():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    m_leg, m_arm = 0.161 * M, 0.050 * M
    h_leg, h_arm = 2 * m_leg * 0.09 * 1.3, 2 * m_arm * 0.20 * 0.6
    res = h_leg - h_arm
    T2 = T_STRIDE / 2
    tq0, tq1 = 2 * h_leg / T2, 2 * res / T2
    assert (round(h_leg, 3), round(h_arm, 3), round(res, 3), round(100 * h_arm / h_leg, 1)) == (2.637, 0.840, 1.797, 31.9)
    assert (round(tq0, 1), round(tq1, 1), round(100 * (1 - (tq1 / tq0) ** 2))) == (10.0, 6.8, 54)
    P = Plot(s, (56, 62, 388, 232), (0, T_STRIDE), (-3, 3))
    t = np.linspace(0, T_STRIDE, 241)
    ph = np.sin(2 * np.pi * t / T_STRIDE)
    legs, arms, net = h_leg * ph, -h_arm * ph, res * ph
    o = [P.axes([(x, f"{x:.2f}") for x in (0, 0.25, 0.5, 0.75, 1.0)],
                [(y, mn(y, "{:.0f}")) for y in (-3, -2, -1, 0, 1, 2, 3)], f"time within one stride (s), T = {T_STRIDE:.3f} s",
                f"yaw momentum H{sub('z', s)} (kg m² s⁻¹)", grid=(-2, -1, 1, 2, 3), ytx=14)]
    up = " ".join(f"{P.X(a):.1f},{P.Y(b):.1f}" for a, b in zip(t, net))
    o.insert(0, f'<polygon points="{P.X(0):.1f},{P.Y(0):.1f} {up} {P.X(T_STRIDE):.1f},{P.Y(0):.1f}" fill="{SER[2]}" opacity="0.18"/>')
    o.append(H.line(s, P.x0, P.Y(0), P.x1, P.Y(0), I["rule"], "ref"))
    o.append(P.curve(t, legs, SER[0], multi=True))
    o.append(P.curve(t, arms, SER[1], multi=True))
    o.append(P.curve(t, net, SER[2]))
    tp = T_STRIDE / 4
    o.append(label(s, P.X(tp), P.Y(h_leg) - 8, f"legs, peak {h_leg:.3f}", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(3 * tp), P.Y(-0.8), f"residual {res:.3f}", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(tp), P.Y(-h_arm) + 18, f"arms, peak {h_arm:.3f}, antiphase", "label2", I["primary"], "middle"))
    xr = P.X(0.53 * T_STRIDE)
    o.append(label(s, xr, P.Y(2.7), f"arms cancel {100 * h_arm / h_leg:.1f} %", "label2"))
    o.append(label(s, xr, P.Y(2.7) + 16, "trunk torque, mean over T/2:", "label2", I["secondary"]))
    o.append(label(s, xr, P.Y(2.7) + 32, f"{tq0:.1f} N m still, {tq1:.1f} swinging", "label2", I["secondary"]))
    o.append(legend(s, 56, 20, [(SER[0], "legs", None), (SER[1], "arms", None), (SER[2], "residual (trunk absorbs)", None)]))
    aria = ("Problem K8 plot: vertical-axis angular momentum over one stride of 1.053 seconds. The legs' momentum "
            "peaks at 2.637 kilogram metre squared per second, the arms' runs in antiphase with peak 0.840, and their "
            "sum, the shaded residual of peak 1.797 that the trunk must absorb, is 68.1 percent of the legs'. The arms "
            "cancel 31.9 percent; the mean trunk yaw torque over a half stride is 10.0 newton metres with the arms "
            "still and 6.8 with them swinging.")
    hv = hov(P, t, [legs, arms, net], lambda i: f"t = {t[i]:.3f} s: legs {mn(legs[i], '{:.3f}')}, arms "
                                                f"{mn(arms[i], '{:.3f}')}, residual {mn(net[i], '{:.3f}')}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #45 K9: energy stride map and cobweb
def fig45():
    VB = (0, 0, W, 316)
    s = H.Scale(W, VB[3], display_w=400)
    alpha, gam = 0.30, 0.05
    a = math.cos(2 * alpha) ** 2
    Ls = 2 * ELL * math.sin(alpha)
    b = M * G * Ls * math.sin(gam)
    es = b / (1 - a)
    vs = math.sqrt(2 * es / M)
    E = [5.0]
    for _ in range(8):
        E.append(a * E[-1] + b)
    assert (round(Ls, 4), round(a, 4), round(b, 2), round(es, 2), round(vs, 3), round(E[-1], 1)) == \
        (0.5615, 0.6812, 19.27, 60.44, 1.314, 57.9)
    assert round(math.sqrt(G * ELL * math.sin(gam) / alpha), 3) == 1.246
    P = Plot(s, (60, 56, 380, 266), (0, 70), (0, 70))
    o = [P.axes([(x, f"{x}") for x in (0, 10, 20, 30, 40, 50, 60, 70)], [(y, f"{y}") for y in (0, 20, 40, 60)],
                f"energy before heel strike E{sub('n', s)} (J)", f"E{sub('n+1', s)} (J)", grid=(20, 40, 60), ytx=16)]
    o.append(P.curve([0, 70], [0, 70], I["rule"], multi=True, dash=H.DASH_REF))
    xs = np.linspace(0, 70, 71)
    o.append(P.curve(xs, a * xs + b, SER[0]))
    stair = [(E[0], 0.0)]
    for k in range(8):
        stair += [(E[k], E[k + 1]), (E[k + 1], E[k + 1])]
    o.append(P.curve([p[0] for p in stair], [p[1] for p in stair], SER[1], multi=True))
    o.append(P.dot(E[0], 0, SER[1]))
    o.append(fdot(s, P.X(es), P.Y(es), O["flag"]))
    o.append(label(s, P.X(es) - 8, P.Y(64.5), f"E* = {es:.2f} J, v* = {vs:.3f} m s⁻¹", "label2",
                   I["primary"], "end"))
    o.append(label(s, P.X(9.5), P.Y(2.5), f"release E{sub('0', s, 'label2')} = 5 J", "label2"))
    o.append(label(s, P.X(69), P.Y(22), f"after 8 steps: {E[-1]:.1f} J", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(69), P.Y(22) + 16, f"slope cos²2α = {a:.3f} < 1", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(44), P.Y(36), f"diagonal E{sub('n+1', s, 'label2')} = E{sub('n', s, 'label2')}", "label2",
                   I["secondary"]))
    o.append(legend(s, 60, 16, [(SER[0], f"stride map E{sub('n+1', s, 'label2')} = {a:.3f} E{sub('n', s, 'label2')} + {b:.2f} J", None)]))
    o.append(legend(s, 60, 36, [(SER[1], "cobweb from E₀ = 5 J", None), (I["rule"], "diagonal", H.DASH_REF)]))
    aria = ("Problem K9 cobweb plot of the passive walker's energy stride map: the line E next = 0.681 E plus 19.27 "
            "joules crosses the dashed diagonal at the fixed point 60.44 joules, a speed of 1.314 metres per second. "
            "The staircase from a 5 joule release climbs toward it and reaches 57.9 joules after eight steps, because "
            "the slope cos squared 2 alpha is 0.681, below one.")
    hv = hov(P, xs, [a * xs + b, xs], lambda i: f"Eₙ = {xs[i]:.0f} J: map {a * xs[i] + b:.2f} J, diagonal {xs[i]:.0f} J")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ svg #46 K10: elasticities of margin and capture point
def fig46():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    x, v, dl, xs = 0.03, 0.45, 0.20, (0.28 + 0.55) / 2
    w0 = math.sqrt(G / ELL)
    xi = x + v * dl + v / w0
    m = xs - xi
    em = [-(dl + 1 / w0) * v / m, -v * dl / m, xs / m]
    ec = [(dl + 1 / w0) * v / xi, v * dl / xi, 0.0]
    assert (round(w0, 2), round(xs, 3), round(xi, 3), round(m, 3)) == (3.21, 0.415, 0.260, 0.155)
    assert [round(e, 2) for e in em] == [-1.48, -0.58, 2.68] and [round(e, 2) for e in ec] == [0.88, 0.35, 0.0]
    panels = [(56, 214, em, "margin m"), (234, 392, ec, "capture point ξ")]
    yr = (-2, 3)
    y0, y1 = 236, 70
    Y = lambda e: y0 - (e - yr[0]) / (yr[1] - yr[0]) * (y0 - y1)   # noqa: E731
    names = ("COM speed", "delay Δ", "step reach")
    o = []
    for e in (-2, -1, 1, 2, 3):
        o.append(H.line(s, panels[0][0], Y(e), panels[1][1], Y(e), GRID, "leader"))
    o.append(H.line(s, panels[0][0], y0, panels[0][0], y1, I["axis"], "axis"))
    for e in (-2, -1, 0, 1, 2, 3):
        o.append(H.line(s, panels[0][0] - 5, Y(e), panels[0][0], Y(e), I["axis"], "leader"))
        o.append(label(s, panels[0][0] - 8, Y(e) + 4.5, mn(e, "{:.0f}"), "tick", I["secondary"], "end"))
    yc = (y0 + y1) / 2
    o.append(label(s, 14, yc, "elasticity ∂ln(·)/∂ln(variable)", "label", I["primary"], "middle",
                   f'transform="rotate(-90 14 {yc:.2f})"'))
    hv_panels = []
    for xa, xb, el, title in panels:
        o.append(H.line(s, xa, Y(0), xb, Y(0), I["axis"], "axis"))
        o.append(label(s, (xa + xb) / 2, y1 - 8, f"of the {title}", "label2", I["primary"], "middle"))
        pts = []
        bw = (xb - xa) / 3
        for k, (e, nm) in enumerate(zip(el, names)):
            xc = xa + bw * (k + 0.5)
            top, bot = min(Y(e), Y(0)), max(Y(e), Y(0))
            if abs(e) > 1e-9:
                o.append(f'<rect x="{xc - bw * 0.32:.2f}" y="{top:.2f}" width="{bw * 0.64:.2f}" height="{bot - top:.2f}" '
                         f'fill="{SER[k]}"/>')
            o.append(label(s, xc, Y(e) - 6 if e >= 0 else Y(e) + 16, mn(e, "{:.2f}", plus=True), "label2", I["primary"],
                           "middle"))
            o.append(label(s, xc, y0 + 18, nm.split(" ")[0], "tick", I["secondary"], "middle"))
            o.append(label(s, xc, y0 + 33, nm.split(" ")[1], "tick", I["secondary"], "middle"))
            pts.append([xc, Y(e), f"{title}: {nm} {mn(e, '{:.2f}', plus=True)}"])
        hv_panels.append(([xa, y1, xb, y0], pts))
    o.append(label(s, panels[1][0] + (panels[1][1] - panels[1][0]) * 5 / 6, Y(0) + 34, "reach does", "label2",
                   I["secondary"], "middle"))
    o.append(label(s, panels[1][0] + (panels[1][1] - panels[1][0]) * 5 / 6, Y(0) + 50, "not enter ξ", "label2",
                   I["secondary"], "middle"))
    o.append(H.line(s, panels[1][0] - 10, y1 - 4, panels[1][0] - 10, y0 + 36, I["rule"], "leader"))
    o.append("".join(f'<rect x="{xx:.2f}" y="{yy - 10:.2f}" width="11" height="11" fill="{SER[k]}"/>'
                     + label(s, xx + 16, yy, nm, "label2", I["secondary"])
                     for k, (nm, xx, yy) in enumerate(zip(names, (56, 160, 250), (24, 24, 24)))))
    o.append(label(s, 56, 44, f"Lab 4 point: ξ = {xi:.3f} m, m = {m:.3f} m, reach {xs:.3f} m", "label2", I["secondary"]))
    aria = ("Problem K10 bar chart: signed elasticities at the Lab 4 reference point. Of the fall margin: minus 1.48 to "
            "COM speed, minus 0.58 to reaction delay and plus 2.68 to step reach, the largest. Of the capture point: "
            "plus 0.88 to speed, plus 0.35 to delay and exactly 0 to step reach, which does not enter it.")
    return H.svg_open(VB, html.escape(aria), s, extra=H.hover_attr(hv_panels)) + "".join(o) + "</svg>"


FIGS = {
    8: ("Joint power plot for ankle, knee, and hip over gait percent ", fig8),
    9: ("Cost of transport against walking speed: a U-shaped curve wi", fig9),
    37: ("K1: vertical ground reaction of the rigid inverted-pendulum ", fig37),
    38: ("K2: Froude number against walking speed for leg lengths 0.80", fig38),
    39: ("K3: the per-step cost proxy against step length for three va", fig39),
    40: ("K4: energy supplied per step against the fraction of the ste", fig40),
    41: ("K5: Lab 3's ankle power over stance, negligible until midsta", fig41),
    42: ("K6: RMS inverse-dynamics torque error against sample rate on", fig42),
    43: ("K7: the per-step cost proxy against step length at three wal", fig43),
    44: ("K8: vertical-axis angular momentum of the legs and of the ar", fig44),
    45: ("K9: cobweb plot of the passive walker's energy stride map, t", fig45),
    46: ("K10: signed elasticities of the fall margin and of the captu", fig46),
}
