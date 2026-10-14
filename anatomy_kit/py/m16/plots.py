"""Module 16 main-text and lab plots in the house style (group `plots`; svg #5 8 9 10 11 14 16 18).

Every plotted number is computed here from the module's own formulas and code (module16.html):
  #5   Def. 3.1 / Prop. 3.1: sigma = E eps, W = 1/2 sigma eps; transverse strain -nu eps (nu = 0.3, cortical bone, table line 208)
  #8   Section 5 listing (lines 270-290): E 17 GPa, L 0.10 m, P 2 kN, A0 2e-4 m^2, taper A0 -> A0/2, 8 elements
  #9   Section 6 (line 311, K6 lines 683-685): E(theta) = E_mat + E_f cos^4 theta, E_mat 0.12, E_f 1.38 GPa
  #10  Section 7 and Lab B: neo-Hookean mu (lam^2 - 1/lam form for Lab B, nominal mu (lam - lam^-2) here), fibre 0.6 (e^{48 eps} - 1)
  #11  Def. 8.1 (G(t) = G_inf + (G0 - G_inf) e^{-t/tau}) and Prop. 8.1 (Terzaghi series F(T), line 357)
  #14  Lab A listing (lines 446-467), #16 Lab B listing (lines 477-490), #18 Lab C listing (lines 497-527)
This file does NOT expose SHARED_DEFS (the Lynch body kit is exposed by m16/body_main.py).
One user unit is one rendered px (760-unit viewBoxes), so sizes pass through H.Scale.
"""
import html
import math

import numpy as np

import house as H
from m05.plots_main import Ax, axes, curve, dot, poly, pts_str, tw

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
GRID = "#e6e6e6"
RED, BLUE, ORANGE = SER[0], SER[1], SER[2]


# ---------------------------------------------------------------- small local helpers
def sup(t, s, size="tick"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def tag(s, x, y, col, text, size="label2", dashed=False, dot_=False):
    """Direct label: a short coloured mark, then ink text (text is never the series colour)."""
    da = f' stroke-dasharray="{s(5):.2f} {s(3):.2f}"' if dashed else ""
    return [f'<line x1="{x:.2f}" y1="{y - 4:.2f}" x2="{x + 20:.2f}" y2="{y - 4:.2f}" stroke="{col}" '
            f'stroke-width="{s(H.PX["curve_multi"]):.2f}"{da}/>',
            H.label(s, x + 25, y, text, size, I["primary"])]


def hover_pts(ax, xs, ys, texts):
    """ys: list of series (each a list), one tooltip per x."""
    out = []
    for k, x in enumerate(xs):
        yy = [round(ax.Y(ser[k]), 2) for ser in ys]
        out.append([round(ax.X(x), 2), yy if len(yy) > 1 else yy[0], texts[k]])
    return out


def mn(v, f="{:.2f}"):
    t = f.format(v)
    return "−" + t[1:] if t.startswith("-") else t


def finish(vb, aria, s, body, hv=None):
    return H.svg_open(vb, html.escape(aria), s, extra=hv or "") + "".join(body) + "</svg>"


def sci(v):
    m, e = f"{v:.1e}".split("e")
    sup_ = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    return f"{m}×10{str(int(e)).translate(sup_)}"


def tick_pow(e, s):
    return "1" if e == 0 else "10" + sup(f"−{-e}" if e < 0 else str(e), s)


def poly1(xy, col, s, w="curve", dash=None, extra=""):
    """Polyline with one-decimal coordinates (long series: keeps the page small)."""
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    p = " ".join(f"{a:.1f},{b:.1f}" for a, b in xy)
    return (f'<polyline points="{p}" fill="none" stroke="{col}" stroke-width="{s(H.PX[w]):.2f}" '
            f'stroke-linejoin="round"{da} {extra}/>')


def band(x0, y0, x1, y1, col, op):
    return f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}" fill="{col}" opacity="{op}"/>'


# ================================================================ svg #5: linear law, energy, Poisson contraction
def block(s, cx, cy, w, h, nx, ny, op=1.0):
    """A bone-coloured specimen with a printed grid, so the stretch of every cell is visible."""
    x0, y0 = cx - w / 2, cy - h / 2
    o = [f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{T["bone"][0]}" stroke="{T["bone"][1]}" '
         f'stroke-width="{s(1.4):.2f}"/>']
    for k in range(1, ny):
        y = y0 + h * k / ny
        o.append(H.line(s, x0, y, x0 + w, y, T["bone_shade"][1], "art_line", extra='opacity="0.8"'))
    for k in range(1, nx):
        x = x0 + w * k / nx
        o.append(H.line(s, x, y0, x, y0 + h, T["bone_shade"][1], "art_line", extra='opacity="0.8"'))
    return "".join(o)


def fig5():
    VB = (0, 0, 760, 335)
    s = H.Scale(VB[2], VB[3])
    p = "m16f5_"
    ModE, e1 = 1.1, 0.80                # drawn slope (arbitrary units) and the strain marked
    s1 = ModE * e1
    W = 0.5 * s1 * e1
    A = Ax((84, 46, 350, 270), (0, 1), (0, 1))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, A, [], [], "strain ε", "stress σ", ylab_x=28, xlab_dy=36)
    tri = [(A.X(0), A.Y(0)), (A.X(e1), A.Y(s1)), (A.X(e1), A.Y(0))]
    o.append(f'<polygon points="{pts_str(tri)}" fill="{RED}" opacity="0.14"/>')
    o.append(curve(s, A, [0, e1], [0, s1], RED))
    o.append(H.line(s, A.X(0), A.Y(s1), A.X(e1), A.Y(s1), O["dim"], "ref", dash=H.DASH_REF))
    o.append(dot(s, A.X(e1), A.Y(s1), I["primary"]))
    o.append(H.label(s, A.X(0) - 9, A.Y(s1) + 5, "σ", "label", I["primary"], "end"))
    o.append(H.label(s, A.X(e1), A.y0 + 20, "ε", "label", I["primary"], "middle"))
    # slope triangle: E = d sigma / d eps
    a, b = 0.22, 0.52
    o.append(H.line(s, A.X(a), A.Y(ModE * a), A.X(b), A.Y(ModE * a), O["geometry"], "geom"))
    o.append(H.line(s, A.X(b), A.Y(ModE * a), A.X(b), A.Y(ModE * b), O["geometry"], "geom"))
    o.append(H.label(s, A.X((a + b) / 2), A.Y(ModE * a) + 19, "Δε", "label2", I["primary"], "middle"))
    o.append(H.label(s, A.X(b) + 9, A.Y(ModE * (a + b) / 2) + 4, "Δσ", "label2", I["primary"]))
    o.append(H.label(s, A.X(0.03), A.Y(0.955), "slope E = Δσ/Δε", "label", I["primary"]))
    o.append(H.label(s, A.X(0.665), A.Y(0.20), "W = ½σε", "label", I["primary"], "middle"))
    o.append(H.label(s, A.X(0.03), A.Y(0.79), "shaded area = stored energy", "label2", I["secondary"]))
    # right: the specimen, unloaded and loaded (strain exaggerated), nu = 0.3
    nu, eps_d = 0.3, 0.5
    w0, h0 = 56.0, 96.0
    cy = 170.0
    cb, ca = 470.0, 640.0
    wa, ha = w0 * (1 - nu * eps_d), h0 * (1 + eps_d)
    o.append(block(s, cb, cy, w0, h0, 3, 5))
    o.append(H.label(s, cb, cy + h0 / 2 + 24, "unloaded", "label2", I["primary"], "middle"))
    o.append(f'<rect x="{ca - w0 / 2:.2f}" y="{cy - h0 / 2:.2f}" width="{w0:.2f}" height="{h0:.2f}" fill="none" '
             f'stroke="{O["dim"]}" stroke-width="{s(H.PX["ref"]):.2f}" stroke-dasharray="{s(6):.2f} {s(4):.2f}"/>')
    o.append(block(s, ca, cy, wa, ha, 3, 5))
    o.append(H.label(s, ca, cy + ha / 2 + 56, "pulled by σ", "label2", I["primary"], "middle"))
    o.append(H.label(s, ca, cy + ha / 2 + 74, "(strain exaggerated)", "label2", I["secondary"], "middle"))
    ytop, ybot = cy - ha / 2, cy + ha / 2
    o.append(H.arrow(s, p, ca, ytop, ca, ytop - 46, "force"))
    o.append(H.arrow(s, p, ca, ybot, ca, ybot + 46, "force"))
    o.append(H.label(s, ca + 9, ytop - 28, "σ", "label", I["primary"]))
    o.append(H.label(s, ca + 9, ybot + 36, "σ", "label", I["primary"]))
    yc = cy
    xl, xr = ca - wa / 2, ca + wa / 2
    o.append(H.arrow(s, p, xl - 34, yc, xl - 1.5, yc, "geometry"))
    o.append(H.arrow(s, p, xr + 34, yc, xr + 1.5, yc, "geometry"))
    o.append(H.label(s, xl - 38, yc + 5, "−νε", "label", I["primary"], "end"))
    # elongation dimension on the right: dashed reference lines at the old ends
    xd = ca + w0 / 2 + 46
    for y_old, y_new in ((cy - h0 / 2, ytop), (cy + h0 / 2, ybot)):
        o.append(H.line(s, ca + w0 / 2, y_old, xd + 10, y_old, O["dim"], "ref", dash=H.DASH_REF))
        o.append(H.arrow(s, p, xd, y_old, xd, y_new, "geometry"))
    o.append(H.label(s, xd + 8, ytop + 2, "ΔL/2", "label2", I["primary"]))
    o.append(H.label(s, xd + 8, ybot + 8, "ΔL/2", "label2", I["primary"]))
    o.append(H.label(s, cb, cy + h0 / 2 + 44, f"ν = {nu} (cortical bone)", "label2", I["secondary"], "middle"))
    o.append(H.label(s, cb, cy + h0 / 2 + 62, "ε = ΔL/L", "label2", I["secondary"], "middle"))
    es = np.linspace(0, e1, 41)
    hv = H.hover_attr(A.box, hover_pts(A, es, [ModE * es],
                      [f"ε = {e:.2f}, σ = Eε = {ModE * e:.3f}, W = ½σε = {0.5 * ModE * e * e:.3f} (arbitrary units, E = {ModE})" for e in es]))
    aria = ("Left: a straight stress-strain line of slope Young's modulus E from the origin, with the slope triangle of run Δε "
            "and rise Δσ, and the triangle under the line up to a marked strain shaded as the stored strain energy W = ½σε. "
            "Right: a bone-coloured specimen with a printed grid, unloaded, and the same specimen pulled by σ at both ends, "
            "longer by ΔL/2 at each end and narrower by the lateral strain −νε, with the unloaded outline dashed behind it.")
    return finish(VB, aria, s, o, hv)


# ================================================================ svg #8: the tapered bar and its finite-element stress
E_, L_, P_, A0_, NEL = 17e9, 0.10, 2000.0, 2e-4, 8


def fe_bar(nel):
    xn = np.linspace(0, L_, nel + 1)
    Ael = A0_ * (1 - 0.5 * (xn[:-1] + xn[1:]) / 2 / L_)
    K = np.zeros((nel + 1, nel + 1))
    for e in range(nel):
        k = E_ * Ael[e] / (xn[e + 1] - xn[e])
        K[e:e + 2, e:e + 2] += k * np.array([[1, -1], [-1, 1]])
    f = np.zeros(nel + 1)
    f[-1] = P_
    free = np.arange(1, nel + 1)
    u = np.zeros(nel + 1)
    u[free] = np.linalg.solve(K[np.ix_(free, free)], f[free])
    sig = np.array([E_ * (u[e + 1] - u[e]) / (xn[e + 1] - xn[e]) for e in range(nel)])
    return xn, u, sig


def area(x):
    return A0_ * (1 - x / (2 * L_))


def fig8():
    VB = (0, 0, 760, 390)
    s = H.Scale(VB[2], VB[3])
    xn, u, sig = fe_bar(NEL)
    ex = P_ / area(np.linspace(0, L_, 201)) / 1e6
    # text checks (lines 291, 293): 10 -> 20 MPa exact, 10 -> 19 MPa elements, tip 0.082 mm
    assert abs(ex[0] - 10) < 1e-9 and abs(ex[-1] - 20) < 1e-9
    assert round(sig[0] / 1e6) == 10 and round(sig[-1] / 1e6) == 19, sig / 1e6
    assert abs(u[-1] * 1e3 - 0.0815) < 0.0001, u[-1] * 1e3
    ax = Ax((92, 160, 690, 335), (0, L_), (0, 22))
    o = axes(s, ax, [(0, "0.00"), (0.05, "0.05"), (0.10, "0.10")], [(0, "0"), (10, "10"), (20, "20")],
             "position along the bar x (m)", "axial stress σ (MPa)", ylab_x=34, xlab_dy=44)
    # the bar, to the same x scale as the plot (section area drawn as height: 2 cm² -> 1 cm²)
    yc, h0 = 74.0, 46.0
    xs = np.linspace(0, L_, 41)
    top = [(ax.X(x), yc - h0 / 2 * area(x) / A0_) for x in xs]
    bot = [(ax.X(x), yc + h0 / 2 * area(x) / A0_) for x in xs][::-1]
    o.append(f'<polygon points="{pts_str(top + bot)}" fill="{T["bone"][0]}" stroke="{T["bone"][1]}" stroke-width="{s(1.4):.2f}"/>')
    for k, xv in enumerate(xn):
        hh = h0 / 2 * area(xv) / A0_
        if 0 < k < NEL:
            o.append(H.line(s, ax.X(xv), yc - hh, ax.X(xv), yc + hh, T["bone"][1], "art_line"))
        o.append(dot(s, ax.X(xv), yc, I["primary"], r=2.6))
    wall = ax.x0
    o.append(f'<rect x="{wall - 12:.2f}" y="{yc - h0 / 2 - 8:.2f}" width="12" height="{h0 + 16:.2f}" fill="#d9d9d9" stroke="{I["axis"]}" '
             f'stroke-width="{s(1.2):.2f}"/>')
    for k in range(7):
        yy = yc - h0 / 2 - 8 + k * (h0 + 16) / 6
        o.append(H.line(s, wall - 12, yy + 7, wall, yy - 1, I["axis"], "leader"))
    o.append(f"<defs>{H.markers('m16f8_', s)}</defs>")
    o.append(H.arrow(s, "m16f8_", ax.X(L_), yc, ax.X(L_) + 46, yc, "force"))
    o.append(H.label(s, ax.X(L_) + 6, yc - 12, "P = 2 kN", "label2", I["primary"]))
    o.append(H.label(s, ax.x0 - 18, yc + 5, "fixed", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(L_ / 2), yc + h0 / 2 + 20, "8 bar elements, section area 2 cm² narrowing to 1 cm²", "label2", I["secondary"], "middle"))
    # stress plot
    for k in range(NEL):
        yv = sig[k] / 1e6
        o.append(H.line(s, ax.X(xn[k]), ax.Y(yv), ax.X(xn[k + 1]), ax.Y(yv), BLUE, "curve"))
    o.append(curve(s, ax, np.linspace(0, L_, 201)[::2], ex[::2], RED))
    o += tag(s, ax.x0 + 16, ax.top + 18, RED, "exact σ(x) = P/A(x)")
    o += tag(s, ax.x0 + 16, ax.top + 40, BLUE, "finite elements: one constant stress each")
    o.append(H.label(s, ax.X(0.0) + 8, ax.Y(10) + 24, f"first element {sig[0] / 1e6:.1f} MPa", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.0985), ax.Y(13.4), f"last element {sig[-1] / 1e6:.1f} MPa", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(L_) - 8, ax.Y(20) - 10, "exact 20 MPa at the thin end", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(0.0) + 12, ax.Y(0) - 12, f"tip displacement of the 8-element solution {u[-1] * 1e3:.4f} mm", "label2", I["secondary"]))
    pts = []
    xx = np.linspace(0, L_, 100)
    for x in xx:
        k = min(int(x / (L_ / NEL)), NEL - 1)
        pts.append([ax.X(x), [ax.Y(P_ / area(x) / 1e6), ax.Y(sig[k] / 1e6)],
                    f"x = {x:.3f} m: exact {P_ / area(x) / 1e6:.2f} MPa, element {sig[k] / 1e6:.2f} MPa"])
    hv = H.hover_attr(ax.box, pts)
    aria = ("A tapered bone-coloured bar, 2 square centimetres narrowing to 1, divided into eight elements, fixed to a wall at its wide "
            "end and pulled by 2 kilonewtons at the thin end, drawn above a stress plot with the same position axis. The red curve is the "
            "exact stress P over A of x, rising from 10 to 20 megapascals; the blue staircase is the eight-element solution, 10.3 "
            "megapascals in the first element to 18.8 in the last, each step constant and tracking the curve.")
    return finish(VB, aria, s, o, hv)


# ================================================================ svg #9: directional stiffness of a tendon
EMAT, EF = 0.12, 1.38


def e_theta(th_deg):
    return EMAT + EF * np.cos(np.radians(th_deg)) ** 4


def strip(s, cx, cy, hw, hh):
    """A tendon strip: rounded body in tendon tones, collagen fibres as long staggered bundles along the axis."""
    o = [f'<rect x="{cx - hw:.2f}" y="{cy - hh:.2f}" width="{2 * hw:.2f}" height="{2 * hh:.2f}" rx="{hh * 0.28:.2f}" '
         f'fill="{T["tendon"][0]}" stroke="{T["tendon"][1]}" stroke-width="{s(1.4):.2f}"/>']
    n = 8
    for k in range(n):
        y = cy - hh + hh * 2 * (k + 0.5) / n
        off = (k % 3 - 1) * hw * 0.10
        x0, x1 = cx - hw + 6 + max(0, off), cx + hw - 6 + min(0, off)
        o.append(f'<line x1="{x0:.2f}" y1="{y:.2f}" x2="{x1:.2f}" y2="{y:.2f}" stroke="{T["tendon"][1]}" '
                 f'stroke-width="{s(2.2):.2f}" stroke-linecap="round" opacity="0.75"/>')
        o.append(f'<line x1="{x0 + 10:.2f}" y1="{y + 2:.2f}" x2="{x1 - 14:.2f}" y2="{y + 2:.2f}" stroke="#fff" '
                 f'stroke-width="{s(0.7):.2f}" opacity="0.7"/>')
    return "".join(o)


def fig9():
    VB = (0, 0, 760, 345)
    s = H.Scale(VB[2], VB[3])
    p = "m16f9_"
    thetas = list(range(0, 91, 5))
    default = thetas.index(35)
    # text checks (line 311 and K6 lines 685): 1.50, 0.12, ratio 12.5, sweep, half at 34.7 degrees
    assert abs(e_theta(0) - 1.5) < 1e-9 and abs(e_theta(90) - 0.12) < 1e-9 and abs(e_theta(0) / e_theta(90) - 12.5) < 1e-9
    assert [round(float(e_theta(a)), 3) for a in (0, 15, 30, 45, 60, 90)] == [1.5, 1.321, 0.896, 0.465, 0.206, 0.12]
    th = np.linspace(0, 90, 400)
    assert abs(th[np.argmin(np.abs(e_theta(th) - 0.75))] - 34.7) < 0.2
    cx, cy, hw, hh = 200.0, 190.0, 105.0, 46.0
    ax = Ax((500, 60, 735, 270), (0, 90), (0, 1.6))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o.append(strip(s, cx, cy, hw, hh))
    o.append(H.arrow(s, p, cx - 80, cy + hh + 18, cx - 10, cy + hh + 18, "geometry"))
    o.append(H.label(s, cx - 45, cy + hh + 38, "fibre axis a", "label2", I["primary"], "middle"))
    o.append(H.line(s, cx, cy, cx + 80, cy, O["dim"], "ref", dash=H.DASH_REF))
    o += axes(s, ax, [(0, "0°"), (30, "30°"), (60, "60°"), (90, "90°")], [(0, "0"), (0.5, "0.5"), (1.0, "1.0"), (1.5, "1.5")],
              "angle θ between the load and the fibres", "directional stiffness E(θ) (GPa)", ylab_x=438, xlab_dy=44)
    thc = np.linspace(0, 90, 91)
    o.append(curve(s, ax, thc, e_theta(thc), RED))
    o.append(H.line(s, ax.x0, ax.Y(0.75), ax.x1, ax.Y(0.75), O["dim"], "ref", dash=H.DASH_REF))
    o.append(H.label(s, ax.x1 - 4, ax.Y(0.75) + 20, "half of 1.50: 34.7°", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(4), ax.Y(1.5) - 10, "along the fibres: 1.50 GPa", "label2", I["primary"]))
    o.append(H.label(s, ax.X(90), ax.Y(0.12) - 40, "across: 0.12 GPa", "label2", I["primary"], "end"))
    frames = []
    for k, a in enumerate(thetas):
        r = math.radians(a)
        ux, uy = math.cos(r), -math.sin(r)
        g = [H.arrow(s, p, cx + 22 * ux, cy + 22 * uy, cx + 128 * ux, cy + 128 * uy, "force"),
             H.arrow(s, p, cx - 22 * ux, cy - 22 * uy, cx - 128 * ux, cy - 128 * uy, "force")]
        g.append(H.label(s, cx + 138 * ux + (6 if ux > 0.3 else -4 if ux < 0.3 else 0), cy + 138 * uy - (4 if a > 60 else -4),
                         "load", "label2", I["primary"], "start" if ux > 0.3 else "middle"))
        if a > 0:
            rr = 62.0
            ex_, ey_ = cx + rr * ux, cy + rr * uy
            g.append(f'<path d="M{cx + rr:.2f},{cy:.2f} A{rr:.2f},{rr:.2f} 0 0 0 {ex_:.2f},{ey_:.2f}" fill="none" '
                     f'stroke="{O["geometry"]}" stroke-width="{s(H.PX["geom"]):.2f}"/>')
            rm = math.radians(a / 2)
            if a >= 12:
                g.append(H.label(s, cx + (rr + 14) * math.cos(rm), cy - (rr + 14) * math.sin(rm) + 5, "θ", "label", I["primary"], "middle"))
        e = float(e_theta(a))
        g.append(H.line(s, ax.x0, ax.Y(e), ax.X(a), ax.Y(e), O["dim"], "ref", dash=H.DASH_REF))
        g.append(H.line(s, ax.X(a), ax.Y(e), ax.X(a), ax.y0, O["dim"], "ref", dash=H.DASH_REF))
        g.append(dot(s, ax.X(a), ax.Y(e), I["primary"]))
        g.append(H.label(s, 24, 44, f"θ = {a}°,  E(θ) = {e:.3f} GPa", "label", I["primary"]))
        frames.append(H.frame(k, default, "".join(g)))
    o += frames
    pts = [[ax.X(a), ax.Y(float(e_theta(a))), f"θ = {a}°: E = {float(e_theta(a)):.3f} GPa"] for a in range(0, 91, 1)]
    hv = H.hover_attr(ax.box, pts)
    aria = ("Left: a tendon strip of aligned collagen fibres along a horizontal fibre axis a, pulled by a red load arrow pair at an "
            "angle θ to the fibres. Right: the directional stiffness E of θ equals 0.12 plus 1.38 cosine to the fourth power of θ, "
            "in gigapascals; it is 1.50 along the fibres, halves to 0.75 at 34.7 degrees and is 0.12 across them. A slider moves "
            "the load angle and the marked point on the curve; the still figure shows 35 degrees.")
    return finish(VB, aria, s, o, hv + " " + H.frames_attr("θ", [f"{a}°" for a in thetas], default))


# ================================================================ svg #10: three stress-stretch laws
MU, K_FIB, A_FIB = 200.0, 48.0, 0.6        # MPa, -, MPa ; linear law E = 3 mu = 600 MPa


def lin(lam):
    return 3 * MU * (lam - 1)


def neo_nom(lam):
    return MU * (lam - lam ** -2)           # incompressible neo-Hookean, nominal stress (uniaxial)


def fib(lam):
    return A_FIB * (np.exp(K_FIB * (lam - 1)) - 1)


def fig10():
    VB = (0, 0, 760, 420)
    s = H.Scale(VB[2], VB[3])
    lam = np.linspace(1.0, 1.10, 201)
    lc = lam[::2]
    ax = Ax((92, 70, 735, 340), (1.0, 1.10), (0, 80))
    lo, hi = 1.05, 1.10
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if fib(mid) > lin(mid) else (mid, hi)
    cross = (lo + hi) / 2
    assert abs(lin(1.1) - 60) < 1e-9 and abs(fib(1.1) - 72.3) < 0.1 and abs(cross - 1.097) < 0.002
    o = axes(s, ax, [(1.0, "1.00"), (1.05, "1.05"), (1.10, "1.10")], [(0, "0"), (20, "20"), (40, "40"), (60, "60"), (80, "80")],
             "stretch λ", "nominal stress P (MPa)", ylab_x=34, xlab_dy=46)
    o.append(curve(s, ax, lc, lin(lc), BLUE, "curve_multi", dash=H.DASH_REF if False else (7, 4)))
    o.append(curve(s, ax, lc, neo_nom(lc), ORANGE, "curve_multi"))
    o.append(curve(s, ax, lc, fib(lc), RED))
    xc, yc = ax.X(cross), ax.Y(lin(cross))
    o.append(dot(s, xc, yc, I["primary"], hollow=True))
    o.append(H.label(s, xc - 12, yc - 14, f"fibre law crosses the linear law at λ = {cross:.3f}", "label2", I["primary"], "end"))
    o += tag(s, ax.x0, 40, BLUE, "linear law, 600 MPa slope", dashed=True)
    o += tag(s, ax.x0 + 245, 40, ORANGE, "neo-Hookean, μ = 200 MPa")
    o += tag(s, ax.x0 + 470, 40, RED, "fibre-reinforced")
    # toe annotation: the flat start of the red curve
    o.append(H.label(s, ax.X(1.028), ax.Y(6.5), "toe: nearly flat", "label2", I["primary"]))
    o.append(H.label(s, ax.X(1.0715), ax.Y(neo_nom(1.0715)) - 14, "neo-Hookean", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(1.0485), ax.Y(lin(1.0485)) - 10, "linear", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(1.1) - 12, ax.Y(fib(1.1)) - 10, f"fibre law {fib(1.1):.0f} MPa at λ = 1.10", "label2", I["primary"], "end"))
    pts = [[ax.X(l), [ax.Y(lin(l)), ax.Y(neo_nom(l)), ax.Y(fib(l))],
            f"λ = {l:.3f}: linear {lin(l):.1f}, neo-Hookean {neo_nom(l):.1f}, fibre {fib(l):.1f} MPa"] for l in lam]
    hv = H.hover_attr(ax.box, pts)
    aria = ("Nominal stress against stretch from 1.00 to 1.10 for three laws. A blue dashed straight line, the linear law with a 600 megapascal "
            "slope, reaches 60 megapascals; the orange neo-Hookean curve with shear modulus 200 megapascals bends slightly below it, "
            "to 55; the red fibre-reinforced exponential law is nearly flat at first, the toe, then rises steeply, crosses the linear "
            "line near stretch 1.095 and reaches 72 megapascals.")
    return finish(VB, aria, s, o, hv)


# ================================================================ svg #11: relaxation and load partition
GINF = 0.4          # illustrative G_inf / G_0 (the module states none)


def terzaghi(Tv, n=80):
    Tv = np.asarray(Tv, dtype=float)
    return sum(8 / ((2 * k + 1) ** 2 * math.pi ** 2) * np.exp(-((2 * k + 1) * math.pi / 2) ** 2 * Tv) for k in range(n))


def fig11():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    A = Ax((80, 110, 340, 305), (0, 5), (0, 1.0))
    B = Ax((470, 110, 735, 305), (0, 1), (0, 1.0))
    tt = np.linspace(0, 5, 151)
    g = GINF + (1 - GINF) * np.exp(-tt)
    TT = np.linspace(0, 1, 151)
    F = terzaghi(TT)
    TT[0] = 0.0
    assert abs(F[0] - 1.0) < 0.02 and abs(float(terzaghi(0.5)) - 0.2360) < 0.0005          # line 357 / Lab C line 527
    o = axes(s, A, [(k, str(k)) for k in range(6)], [(0, "0"), (0.5, "0.5"), (1, "1")], "time t / τ after the step", "stress σ(t) / σ(0⁺)", ylab_x=24, xlab_dy=44)
    o += axes(s, B, [(0, "0"), (0.5, "0.5"), (1, "1")], [(0, "0"), (0.5, "0.5"), (1, "1")], "dimensionless time T = c" + H.sub("v", s) + "t/L²",
              "share of the load", ylab_x=414, xlab_dy=44)
    # left
    o.append(H.line(s, A.x0, A.Y(GINF), A.x1, A.Y(GINF), O["dim"], "ref", dash=H.DASH_REF))
    o.append(curve(s, A, tt[::2], g[::2], RED))
    o.append(dot(s, A.X(0), A.Y(1.0), I["primary"]))
    o.append(dot(s, A.X(1), A.Y(GINF + (1 - GINF) / math.e), I["primary"], hollow=True))
    o.append(H.label(s, A.X(0) + 12, A.Y(1.0) - 4, "instantaneous peak σ(0⁺) = G" + H.sub("0", s) + "ε", "label2", I["primary"]))
    o.append(H.label(s, A.X(5) - 4, A.Y(GINF) + 22, "equilibrium σ" + H.sub("∞", s) + " = G" + H.sub("∞", s) + "ε", "label2", I["primary"], "end"))
    o.append(H.label(s, A.X(1) + 12, A.Y(GINF + (1 - GINF) / math.e) - 12, "t = τ: excess down to 1/e", "label2", I["primary"]))
    o.append(H.label(s, A.x0, 36, "viscoelastic tissue under a step strain", "label", I["primary"]))
    o.append(H.label(s, A.x0, 58, f"illustrative G" + H.sub("∞", s) + f"/G" + H.sub("0", s) + f" = {GINF}", "label2", I["secondary"]))
    # right
    poly_f = [(B.X(x), B.Y(y)) for x, y in zip(TT[::2], F[::2])]
    fl = poly_f + [(B.X(1), B.Y(0)), (B.X(0), B.Y(0))]
    ml = [(B.X(0), B.Y(1))] + [(B.X(1), B.Y(1))] + poly_f[::-1]
    o.append(f'<polygon points="{pts_str(fl)}" fill="{T["fluid"][0]}" opacity="0.55"/>')
    o.append(f'<polygon points="{pts_str(ml)}" fill="{RED}" opacity="0.10"/>')
    o.append(curve(s, B, TT[::2], F[::2], BLUE))
    o.append(curve(s, B, TT[::2], 1 - F[::2], RED, "curve_multi"))
    o.append(H.label(s, B.x0, 36, "biphasic tissue under a step load", "label", I["primary"]))
    o += tag(s, B.x0, 62, BLUE, "fluid share F(T)")
    o += tag(s, B.x0, 82, RED, "matrix share 1 − F(T)")
    o.append(H.label(s, B.X(0.04), B.Y(0.065), "the load first", "label2", I["primary"]))
    o.append(H.label(s, B.X(0.04), B.Y(0.065) - 17, "fluid pressure carries", "label2", I["primary"]))
    o.append(H.label(s, B.X(0.12), B.Y(0.90), "solid matrix", "label2", I["primary"]))
    ptsA = [[A.X(t), A.Y(v), f"t/τ = {t:.2f}: σ/σ(0⁺) = {v:.3f}"] for t, v in zip(tt, g)]
    ptsB = [[B.X(t), [B.Y(f_), B.Y(1 - f_)], f"T = {t:.3f}: fluid {f_:.3f}, matrix {1 - f_:.3f}"] for t, f_ in zip(TT, F)]
    hv = H.hover_attr([(A.box, ptsA), (B.box, ptsB)])
    aria = ("Left: stress relaxation after a step strain, the red stress falling from an instantaneous peak toward a dashed equilibrium "
            "level over a few relaxation times τ. Right: a biphasic tissue under a step load; the blue fluid share starts near one and falls, "
            "the red matrix share rises, and the two cross at a dimensionless time near 0.2.")
    return finish(VB, aria, s, o, hv)


# ================================================================ svg #14: Lab A, convergence
def fig14():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    u_exact = 2 * P_ * L_ / (E_ * A0_) * math.log(2)
    ns = [2, 4, 8, 16, 32, 64]
    err = [abs(fe_bar(n)[1][-1] - u_exact) / u_exact for n in ns]
    slope = np.polyfit(np.log2(ns), np.log2(err), 1)[0]
    assert abs(err[0] - 1.1e-2) < 0.05e-2 and abs(err[-1] - 1.1e-5) < 0.05e-5 and -2.1 < slope < -1.9, (err, slope)  # line 472
    ax = Ax((96, 60, 735, 310), (2, 64), (1e-6, 1e-1), xlog=True, ylog=True)
    xt = [(n, str(n)) for n in ns]
    yt = [(10.0 ** e, tick_pow(e, s)) for e in range(-6, 0)]
    o = axes(s, ax, xt, yt, "number of elements N", "relative tip-displacement error", ylab_x=30, xlab_dy=46)
    ref = [4.0 * err[0] * (2 / n) ** 2 for n in (2, 64)]
    o.append(curve(s, ax, [2, 64], ref, O["dim"], "curve_multi", dash=(7, 4)))
    o.append(curve(s, ax, ns, err, RED))
    for n, e in zip(ns, err):
        o.append(dot(s, ax.X(n), ax.Y(e), RED))
    o += tag(s, ax.x0 + 12, ax.top - 18, RED, f"computed error, fitted slope {slope:.2f}")
    o += tag(s, ax.x0 + 330, ax.top - 18, O["dim"], "slope −2 reference, shifted up", dashed=True)
    o.append(H.label(s, ax.X(2) + 10, ax.Y(err[0]) + 52, f"{sci(err[0])} at N = 2", "label2", I["primary"]))
    o.append(H.label(s, ax.X(64) - 12, ax.Y(err[-1]) + 30, f"{sci(err[-1])} at N = 64", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(8), ax.Y(1e-5) - 4, "each doubling of N cuts the error about fourfold", "label2", I["secondary"]))
    pts = [[ax.X(n), ax.Y(e), f"N = {n}: error {e:.2e} (tip {fe_bar(n)[1][-1] * 1e3:.5f} mm, exact {u_exact * 1e3:.5f} mm)"] for n, e in zip(ns, err)]
    hv = H.hover_attr(ax.box, pts)
    aria = ("Relative error of the finite-element tip displacement of the tapered bar against the number of elements, 2 to 64, on log-log "
            "axes: six red points on a straight line of slope about minus two, from 1.1 times ten to the minus two at 2 elements to 1.1 times "
            "ten to the minus five at 64, with a dashed slope minus two reference line above.")
    return finish(VB, aria, s, o, hv)


# ================================================================ svg #16: Lab B, when is the linear law valid
def fig16():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    eps = np.linspace(1e-4, 0.5, 4000)
    lam = 1 + eps
    dn = np.abs(lam ** 2 - 1 / lam - 3 * eps) / (3 * eps)
    k = 48.0
    df = np.abs(np.exp(k * eps) - 1 - k * eps) / (k * eps)
    lim_n = eps[np.where(dn > 0.05)[0][0]]
    lim_f = eps[np.where(df > 0.05)[0][0]]
    assert abs(lim_n - 0.47) < 0.01 and abs(lim_f - 0.002) < 0.0005, (lim_n, lim_f)       # lines 493, 478-490
    ymax = 60.0
    ax = Ax((92, 56, 735, 310), (0, 12), (0, ymax))
    o = axes(s, ax, [(0, "0"), (2, "2%"), (4, "4%"), (6, "6%"), (8, "8%"), (10, "10%"), (12, "12%")], [(0, "0"), (10, "10"), (20, "20"), (30, "30"), (40, "40"), (50, "50"), (60, "60")],
             "engineering strain ε", "linear-law error (%)", ylab_x=32, xlab_dy=46)
    m = eps <= 0.12
    ex, dfm, dnm = eps[m] * 100, df[m] * 100, dn[m] * 100
    o.append(H.line(s, ax.x0, ax.Y(5), ax.x1, ax.Y(5), O["dim"], "ref", dash=H.DASH_REF))
    o.append(H.label(s, ax.x1 - 4, ax.Y(5) - 8, "5% tolerance", "label2", I["primary"], "end"))
    dk = np.unique(np.concatenate([np.arange(0, 40), np.arange(40, ex.size, 10), [ex.size - 1]]))
    o.append(curve(s, ax, ex[dk], dnm[dk], ORANGE))
    keep = dfm <= ymax
    j = int(np.argmin(keep))               # first index above the top
    xe = ex[j - 1] + (ex[j] - ex[j - 1]) * (ymax - dfm[j - 1]) / (dfm[j] - dfm[j - 1])
    kk = [q for q in range(0, j) if q < 30 or q % 3 == 0]
    xs_ = list(ex[kk]) + [xe]
    ys_ = list(dfm[kk]) + [ymax]
    o.append(curve(s, ax, xs_, ys_, RED))
    xf = lim_f * 100
    o.append(dot(s, ax.X(xf), ax.Y(5), I["primary"]))
    o.append(H.label(s, ax.X(xf) + 52, ax.Y(5) - 26, f"fibre law: 5% at ε = {xf:.2f}%", "label2", I["primary"]))
    o.append(H.line(s, ax.X(xf) + 3, ax.Y(5) - 4, ax.X(xf) + 48, ax.Y(5) - 22, I["rule"], "leader"))
    o.append(H.label(s, ax.X(xe) + 12, ax.top + 14, f"fibre error leaves the plot above ε = {xe:.1f}%", "label2", I["primary"]))
    o.append(H.label(s, ax.X(5.0), ax.Y(15), f"neo-Hookean: {dnm[-1]:.2f}% even at ε = 12%", "label2", I["primary"]))
    o.append(H.label(s, ax.X(5.0), ax.Y(10.5), f"(5% only at ε = {lim_n * 100:.0f}%, far off this axis)", "label2", I["secondary"]))
    o += tag(s, ax.x0, 30, RED, "fibre-reinforced law, k = 48")
    o += tag(s, ax.x0 + 280, 30, ORANGE, "neo-Hookean solid")
    idx = np.arange(0, ex.size, 1)
    pts = [[ax.X(ex[i]), [ax.Y(min(dfm[i], ymax)), ax.Y(dnm[i])],
            f"ε = {ex[i]:.2f}%: fibre {dfm[i]:.1f}%, neo-Hookean {dnm[i]:.2f}%"] for i in idx]
    hv = H.hover_attr(ax.box, pts)
    aria = ("Error of the small-strain linear law against engineering strain from 0 to 12 percent. The red fibre-reinforced curve rises "
            "through the dashed 5 percent tolerance at 0.2 percent strain and leaves the top of the plot at 60 percent near 1.8 percent "
            "strain; the orange neo-Hookean curve stays below half a percent over the whole axis and reaches 5 percent only at 47 percent strain.")
    return finish(VB, aria, s, o, hv)


# ================================================================ svg #18: Lab C, load sharing
def lab_c():
    nz, cv, L = 40, 1e-3, 1.0
    dz = L / nz
    dt = 0.4 * dz ** 2 / cv
    p = np.ones(nz + 1)
    p[0] = 0.0
    Ts, Fs = [0.0], [1.0]
    T50 = None
    for it in range(2000):
        lap = np.zeros_like(p)
        lap[1:-1] = (p[2:] - 2 * p[1:-1] + p[:-2]) / dz ** 2
        lap[-1] = (2 * p[-2] - 2 * p[-1]) / dz ** 2
        p = p + dt * cv * lap
        p[0] = 0.0
        Tn = cv * (it + 1) * dt / L ** 2
        if T50 is None and p.mean() < 0.5:
            T50 = Tn
        Ts.append(Tn)
        Fs.append(float(p.mean()))
    return np.array(Ts), np.array(Fs), T50


def fig18():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    Ts, Fs, T50 = lab_c()
    ser = terzaghi(Ts[1:])
    # text checks (lines 527, 538-540): 0.9659 at the first step, 0.2347 at T = 0.5, T50 = 0.195, series 0.2360, 0.6 %
    assert abs(Fs[1] - 0.9659) < 5e-4 and abs(Fs[-1] - 0.2347) < 5e-4 and abs(T50 - 0.195) < 5e-4, (Fs[1], Fs[-1], T50)
    assert abs(float(terzaghi(0.5)) - 0.2360) < 5e-4 and abs((0.2360 - Fs[-1]) / 0.2360 - 0.006) < 0.002
    ax = Ax((92, 84, 735, 325), (0, 0.5), (0, 1.0))
    o = axes(s, ax, [(0, "0"), (0.1, "0.1"), (0.2, "0.2"), (0.3, "0.3"), (0.4, "0.4"), (0.5, "0.5")], [(0, "0.00"), (0.25, "0.25"), (0.5, "0.50"), (0.75, "0.75"), (1, "1.00")],
             "dimensionless time T = c" + H.sub("v", s) + "t/L²", "share of the applied load", ylab_x=32, xlab_dy=46)
    idx = list(range(0, 41)) + list(range(45, 2001, 12))
    if idx[-1] != 2000:
        idx.append(2000)
    fxy = [(ax.X(Ts[i]), ax.Y(Fs[i])) for i in idx]
    uxy = [(ax.X(Ts[i]), ax.Y(1 - Fs[i])) for i in idx]
    sxy = [(ax.X(Ts[i]), ax.Y(float(ser[i - 1]))) for i in idx[1:]]
    o.append(H.line(s, ax.X(T50), ax.Y(0.5), ax.X(T50), ax.y0, O["dim"], "ref", dash=H.DASH_REF))
    o.append(poly1(sxy, ORANGE, s, "curve_multi", dash=(3, 3)))
    o.append(poly1(fxy, BLUE, s))
    o.append(poly1(uxy, RED, s))
    o.append(dot(s, ax.X(T50), ax.Y(0.5), I["primary"]))
    o.append(dot(s, ax.X(Ts[1]), ax.Y(Fs[1]), I["primary"], hollow=True))
    o.append(dot(s, ax.X(Ts[-1]), ax.Y(Fs[-1]), I["primary"], hollow=True))
    o.append(dot(s, ax.X(Ts[-1]), ax.Y(1 - Fs[-1]), I["primary"], hollow=True))
    o.append(H.label(s, ax.X(T50) + 10, ax.y0 - 10, f"shares cross at T = {T50:.3f}", "label2", I["primary"]))
    o.append(H.label(s, ax.X(Ts[1]) + 12, ax.Y(Fs[1]) - 12, f"first step: fluid {Fs[1]:.3f}", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.5) - 12, ax.Y(1 - Fs[-1]) - 12, f"matrix {1 - Fs[-1]:.3f} at T = 0.5", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(0.5) - 12, ax.Y(Fs[-1]) + 22, f"fluid {Fs[-1]:.3f} at T = 0.5", "label2", I["primary"], "end"))
    o += tag(s, ax.x0, 26, BLUE, "fluid share F(T), finite differences")
    o += tag(s, ax.x0 + 280, 26, RED, "matrix share U(T) = 1 − F(T)")
    o += tag(s, ax.x0 + 530, 30, ORANGE, "Terzaghi series", dashed=True) if False else []
    o += tag(s, ax.x0, 48, ORANGE, f"Terzaghi series F(T): {float(terzaghi(0.5)):.4f} at T = 0.5, 0.6% above the finite-difference {Fs[-1]:.4f}", dashed=True)
    sel = list(range(0, 41, 1)) + list(range(45, 2001, 15))
    pts = [[ax.X(Ts[i]), [ax.Y(Fs[i]), ax.Y(1 - Fs[i])], f"T = {Ts[i]:.4f}: fluid {Fs[i]:.4f}, matrix {1 - Fs[i]:.4f}"] for i in sel]
    hv = H.hover_attr(ax.box, pts)
    aria = ("Load shares against dimensionless consolidation time T from 0 to 0.5. The blue fluid share falls from 0.966 at the first step "
            "to 0.235; the red matrix share rises from 0.034 to 0.765; they cross at T equal to 0.195. A dashed orange Terzaghi series "
            "lies almost on the blue curve and gives 0.2360 at T equal to 0.5.")
    return finish(VB, aria, s, o, hv)


FIGS = {
    5: ("Left: a linear stress-strain line of slope Young's modulus E", fig5),
    8: ('Axial stress along a tapered bar under end load: the exact h', fig8),
    9: ('Left: a tendon strip of aligned collagen fibres. Right: the ', fig9),
    10: ('Nominal stress versus stretch for a linear law, a neo-Hookea', fig10),
    11: ('Left: stress relaxation, a step strain producing a stress th', fig11),
    14: ('Lab A finite-element convergence: the relative error in the ', fig14),
    16: ('Lab B: the percentage error of the small-strain linear appro', fig16),
    18: ('Lab C: the layer-averaged share of a step load carried by th', fig18),
}
