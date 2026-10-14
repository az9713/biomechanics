"""Module 14 main-text and lab plots in the house style (group `plots_main`).

svg #4 (margin framework), #5 (strength reserve), #7 (cartilage stress + joint), #8 (delay erodes the envelope),
#9 (AGE crosslinks), #10 (fall-risk model), #11 (mechanostat), #14 (Lab A), #16 (Lab B), #18 (Lab C), #20 (Lab D).
Every plotted number is computed here from the formula or the lab code the module states (line numbers of
module14.html beside each constant):
  Prop. 2.1 / Lab A (82, 264-284), Prop. 3.1-3.2 / Lab B (135, 145, 287-308), Prop. 4.1 (159-163) and Lab C code
  (311-336), Prop. 5.1 (175-177), Def. 5.2 / Prop. 5.3 (195-204), Prop. 6.1 and Lab D code (214-224, 339-366),
  Prop. 7.1 (232-234).
All figures use a 760-unit-wide viewBox, so one user unit is one rendered px (svg #7 is the same width).
"""
import html
import math

import house as H
from m04.tissue import KNEE, KNEE_RECOLOUR, knee_art, knee_credit
from m05.body import art_image
from m05.plots_main import Ax, axes, curve, dot, legend, legend_col, mn, poly, svg, tw

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
GRID = "#e6e6e6"
KNEE_ID = "m14art_knee"
DASH_SER = (7, 4)
SUB = lambda t, s: H.sub(t, s, "label2")  # noqa: E731


def SHARED_DEFS():
    """The m04 DBCLS knee crop once per page as #m14art_knee (svg 7 <use>s it)."""
    return f'<g id="{KNEE_ID}">{art_image("<svg>" + knee_art() + "</svg>", KNEE)}</g>'


def hv(ax, xs, ys, texts):
    """Hover points (user units) sorted by x for one panel; ys may be lists."""
    pts = []
    for x, y, t in zip(xs, ys, texts):
        yy = [round(v, 2) for v in y] if isinstance(y, (list, tuple)) else round(y, 2)
        pts.append([round(x, 2), yy, t])
    pts.sort(key=lambda p: p[0])
    return [round(v, 2) for v in ax.box], pts


def hov(*panels):
    return H.hover_attr(list(panels))


def esup(s, txt):
    """e raised to txt: a thin space after the e, then a superscript tspan (Georgia: e + sup renders as epsilon without it)."""
    return f'e <tspan baseline-shift="super" font-size="{s(H.PX["label"] * 0.7):.2f}">{txt}</tspan>'


def lin(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


# ---------------------------------------------------------------- constants the module states
D_CHAIR, TAU_P, R_LOSS, A0 = 110.0, 175.0, 0.01, 40.0           # 82: demand N m, peak N m, 1/yr, yr


def a_star(tau_p):
    """Prop. 2.1 (81)."""
    return A0 + (1 - D_CHAIR / tau_p) / R_LOSS


def tau_max(a, tau_p=TAU_P):
    return tau_p * (1 - R_LOSS * (a - A0))


# ================================================================ svg #4: the margin framework
def fig4():
    VB = (0, 0, 760, 366)
    s = H.Scale(VB[2], VB[3])
    A = Ax((72, 52, 350, 290), (40, 95), (0, 200))
    B = Ax((452, 52, 735, 290), (40, 95), (0, 2))
    ages = lin(40, 95, 56)
    ast = a_star(TAU_P)
    o = axes(s, A, [(v, str(v)) for v in (40, 60, 80)], [(v, str(v)) for v in (0, 50, 100, 150, 200)],
             "age (yr)", "torque (N m)", ylab_x=18)
    o += axes(s, B, [(v, str(v)) for v in (40, 60, 80)], [(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2)],
              "age (yr)", "reserve R = C / D", ylab_x=B.x0 - 52)
    o.append(H.label(s, A.x0, A.top - 22, "capacity and demand", "label", I["primary"]))
    o.append(H.label(s, B.x0, B.top - 22, f"reserve R = C/D", "label", I["primary"]))
    # panel A
    o.append(H.line(s, A.x0, A.Y(D_CHAIR), A.x1, A.Y(D_CHAIR), SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, A, ages, [tau_max(a) for a in ages], SER[0], "curve_multi"))
    o.append(H.line(s, A.X(ast), A.y0, A.X(ast), A.Y(D_CHAIR), I["rule"], "leader", (4, 3)))
    o.append(dot(s, A.X(ast), A.Y(D_CHAIR), O["flag"]))
    o.append(H.label(s, A.X(ast) + 8, A.Y(D_CHAIR) - 12, f"fails at {ast:.0f} yr", "label2", I["primary"]))
    o.append(H.label(s, A.x0 + 8, A.Y(D_CHAIR) + 18, "demand D = 110 N m", "label2", I["primary"]))
    o.append(H.label(s, A.X(41), A.Y(tau_max(41)) - 12, "capacity C(a)", "label2", I["primary"]))
    o += legend_col(s, A.x0 + 14, A.Y(38), [(SER[0], None, "capacity C(a) = τ" + SUB("max", s) + "(a)"),
                                              (SER[1], DASH_SER, "demand D (fixed)")], dy=19)
    # panel B
    o.append(H.line(s, B.x0, B.Y(1), B.x1, B.Y(1), SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, B, ages, [tau_max(a) / D_CHAIR for a in ages], SER[0], "curve_multi"))
    o.append(H.line(s, B.X(ast), B.y0, B.X(ast), B.Y(1), I["rule"], "leader", (4, 3)))
    o.append(dot(s, B.X(ast), B.Y(1), O["flag"]))
    o.append(H.label(s, B.X(48), B.Y(1) + 22, "R > 1: task possible", "label2", I["primary"]))
    o.append(H.label(s, B.X(94), B.Y(1) - 10, "R < 1: fails", "label2", I["primary"], "end"))
    o.append(H.label(s, B.X(41), B.Y(1.59) - 12, "R(40) = 1.59", "label2", I["primary"]))
    o += legend_col(s, B.x0 + 14, B.Y(0.5), [(SER[0], None, "reserve R(a)"), (SER[1], DASH_SER, "limit R = 1")], dy=19)
    aria = (f"Two panels against age 40 to 95 years for the chair-rise example. Left: capacity, the peak joint torque, "
            f"falls linearly from 175 newton metres by 1 percent of its peak per year; the task demand is fixed at "
            f"110 newton metres (dashed). Right: the reserve R = capacity over demand falls from 1.59 and crosses "
            f"one at age {ast:.1f}, where the task first fails.")
    ha = hv(A, [A.X(a) for a in ages], [A.Y(tau_max(a)) for a in ages],
            [f"age {a:.0f} yr: C = {tau_max(a):.0f} N m, D = 110 N m" for a in ages])
    hb = hv(B, [B.X(a) for a in ages], [B.Y(tau_max(a) / D_CHAIR) for a in ages],
            [f"age {a:.0f} yr: R = {tau_max(a)/D_CHAIR:.2f}" for a in ages])
    return svg(VB, aria, s, o, hov(ha, hb))


# ================================================================ svg #5: strength reserve for two peaks
def fig5():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    A = Ax((80, 40, 735, 320), (40, 95), (0, 2))
    ages = lin(40, 95, 56)
    o = axes(s, A, [(v, str(v)) for v in (40, 50, 60, 70, 80, 90)], [(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2)],
             "age (yr)", "strength reserve R = τ" + H.sub("max", s) + " / D")
    o.append(H.line(s, A.x0, A.Y(1), A.x1, A.Y(1), I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, A.x0 + 8, A.Y(1) + 18, "R = 1: the task is at its limit", "label2", I["primary"]))
    cols = {175.0: SER[0], 210.0: SER[1]}
    fails = {}
    for tp, col in cols.items():
        o.append(curve(s, A, ages, [tau_max(a, tp) / D_CHAIR for a in ages], col, "curve_multi"))
        fails[tp] = a_star(tp)
    for tp, col in cols.items():
        o.append(dot(s, A.X(fails[tp]), A.Y(1), col))
        o.append(H.line(s, A.X(fails[tp]), A.Y(1) + 6, A.X(fails[tp]), A.y0, I["rule"], "leader", (4, 3)))
        o.append(H.label(s, A.X(fails[tp]) - 6, A.y0 - 8, f"{fails[tp]:.1f} yr", "label2", I["primary"], "end"))
    o.append(H.label(s, A.X(41.5), A.Y(1.59) + 30, "τ" + H.sub("p", s) + " = 175 N m", "label2", I["primary"]))
    o.append(H.label(s, A.X(41.5), A.Y(1.909) - 13, "τ" + H.sub("p", s) + " = 210 N m (+20 %)", "label2", I["primary"]))
    y = A.Y(0.56)
    o.append(H.arrow(s, "m14f5_", A.X(fails[175.0]) + 4, y, A.X(fails[210.0]) - 4, y, "geometry", both=True))
    o.append(H.label(s, (A.X(fails[175.0]) + A.X(fails[210.0])) / 2, y - 9,
                     f"{fails[210.0]-fails[175.0]:.1f} yr banked", "label2", I["primary"], "middle"))
    o += legend_col(s, A.x0 + 14, A.Y(0.44), [(SER[0], None, "typical peak, τ" + SUB("p", s) + " = 175 N m"),
                                                (SER[1], None, "20 % stronger, τ" + SUB("p", s) + " = 210 N m")], dy=19)
    aria = (f"Strength reserve R against age 40 to 95 for the chair-rise demand of 110 newton metres. Typical peak torque "
            f"175 newton metres starts at R = 1.59 and crosses one at age {fails[175.0]:.1f}; a peak 20 percent higher, 210, "
            f"starts at 1.91 and crosses one at {fails[210.0]:.1f}, {fails[210.0]-fails[175.0]:.1f} years later.")
    pts = hv(A, [A.X(a) for a in ages], [[A.Y(tau_max(a, 175.0) / D_CHAIR), A.Y(tau_max(a, 210.0) / D_CHAIR)] for a in ages],
             [f"age {a:.0f} yr: R = {tau_max(a, 175.0)/D_CHAIR:.2f} (175), {tau_max(a, 210.0)/D_CHAIR:.2f} (210)" for a in ages])
    return svg(VB, aria, s, o, hov(pts))


# ================================================================ svg #7: cartilage thickness and peak stress
P0, H0, NC = 3.0, 2.0, 0.7                                          # 161: MPa, mm, working exponent


def p_peak(h, n=NC):
    """Prop. 4.1 (160)."""
    return P0 * (H0 / h) ** n


def wrap_credit(text, n=108):
    from m05.body import wrap
    return wrap(text, n)


def _arc_pts(cx, cy, r, x0, x1, n=24):
    """Points on the lower half of a circle between x0 and x1 (x relative to cx)."""
    return [(cx + x, cy + math.sqrt(r * r - x * x)) for x in lin(x0, x1, n)]


def contact_inset(s, cx, yc, h_mm, a, label, ptxt, W=74):
    """Schematic cross-section at the contact: condyle over a flat plateau, cartilage layers h on both, contact
    patch of half-width a (user units). 11 units per mm. The condyle is pressed down so its cartilage is flattened
    over the patch."""
    k = 11.0
    h = h_mm * k
    Rb = 90.0
    Rs = Rb + h
    dlt = a * a / (2 * Rs)
    cy = yc - Rs + dlt                       # centre of the condyle circle
    xs = lin(-W, W, 31)
    surf = [(cx + x, min(cy + math.sqrt(Rs * Rs - x * x), yc)) for x in xs]
    bone_arc = _arc_pts(cx, cy, Rb, -W, W, 31)
    top = yc - 62
    cart_top = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in surf) + " L" + " L".join(
        f"{x:.2f},{y:.2f}" for x, y in reversed(bone_arc)) + " Z"
    bone_top = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in bone_arc) + f" L{cx+W:.2f},{top:.2f} L{cx-W:.2f},{top:.2f} Z"
    plate_y = yc + h
    o = [f'<path d="{bone_top}" fill="{T["bone"][0]}" stroke="{T["bone"][1]}" stroke-width="{s(1.2):.2f}"/>',
         f'<path d="{cart_top}" fill="{T["cartilage"][0]}" stroke="{T["bone"][1]}" stroke-width="{s(1.2):.2f}"/>',
         f'<rect x="{cx-W:.2f}" y="{yc:.2f}" width="{2*W:.2f}" height="{h:.2f}" fill="{T["cartilage"][0]}" '
         f'stroke="{T["bone"][1]}" stroke-width="{s(1.2):.2f}"/>',
         f'<rect x="{cx-W:.2f}" y="{plate_y:.2f}" width="{2*W:.2f}" height="{44:.2f}" fill="{T["bone"][0]}" '
         f'stroke="{T["bone"][1]}" stroke-width="{s(1.2):.2f}"/>']
    # contact patch: the flattened part of the interface, drawn in the geometry colour
    o.append(H.line(s, cx - a, yc, cx + a, yc, O["geometry"], "force"))
    o.append(H.label(s, cx, plate_y + 44 + 17, label, "label2", I["primary"], "middle"))
    o.append(H.label(s, cx, plate_y + 44 + 34, ptxt, "label2", I["primary"], "middle"))
    return o


def fig7():
    VB = (0, 0, 760, 488)
    s = H.Scale(VB[2], VB[3])
    pre = "m14f7_"
    A = Ax((452, 46, 735, 390), (0.4, 2.1), (0, 11))
    hs = lin(0.5, 2.0, 91)
    o = [H.markers(pre, s)]
    # --- knee art (left) with the contact point marked, from m04's DBCLS crop (CC BY 4.0)
    k = 0.92
    ax0, ay0 = 14, 52
    o.append(f'<use href="#{KNEE_ID}" transform="translate({ax0 - KNEE[0]*k:.2f} {ay0 - KNEE[1]*k:.2f}) scale({k})"/>')
    cxk, cyk = ax0 + (196.0 - KNEE[0]) * k, ay0 + (271.3 - KNEE[1]) * k          # m04 KA["contact"]
    o.append(f'<circle cx="{cxk:.2f}" cy="{cyk:.2f}" r="{s(9):.2f}" fill="none" stroke="{O["flag"]}" stroke-width="{s(2):.2f}"/>')
    o.append(H.label(s, ax0, ay0 - 14, "knee, sagittal section", "label2", I["secondary"]))
    # --- two schematic insets of the contact; contact half-width a goes as h^0.35 (between h^0.25 and h^0.5)
    a2 = 30.0
    cxi, y1, y2 = 306, 118, 318
    o += contact_inset(s, cxi, y1, 2.0, a2, "healthy: h = 2.0 mm", f"peak stress {p_peak(2.0):.1f} MPa")
    o += contact_inset(s, cxi, y2, 0.6, a2 * (0.6 / 2.0) ** 0.35, "worn: h = 0.6 mm", f"peak stress {p_peak(0.6):.1f} MPa")
    o.append(H.line(s, cxk + s(9), cyk - 2, cxi - 80, y1 + 6, I["secondary"], "leader"))
    o.append(H.line(s, cxk + s(9), cyk + 2, cxi - 80, y2 + 6, I["secondary"], "leader"))
    for yc in (y1, y2):
        o.append(H.arrow(s, pre, cxi, yc - 98, cxi, yc - 66, "load", w="load"))
        o.append(H.label(s, cxi + 10, yc - 78, "same load F", "label2", I["primary"]))
    # contact-patch key (left column, below the art)
    o.append(H.line(s, 14, 340, 40, 340, O["geometry"], "force"))
    o.append(H.label(s, 48, 344, "contact patch:", "label2", I["primary"]))
    o.append(H.label(s, 48, 361, "narrower when thin", "label2", I["primary"]))
    # --- plot
    o += axes(s, A, [(0.5, "0.5"), (1.0, "1.0"), (1.5, "1.5"), (2.0, "2.0")], [(v, str(v)) for v in (0, 2, 4, 6, 8, 10)],
              "cartilage thickness h (mm)", "peak contact stress (MPa)", ylab_x=A.x0 - 46)
    o.append(curve(s, A, hs, [p_peak(h, 1.0) for h in hs], SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, A, hs, [p_peak(h, 0.5) for h in hs], SER[2], "curve_multi", DASH_SER))
    o.append(curve(s, A, hs, [p_peak(h) for h in hs], SER[0], "curve"))
    for h in (2.0, 1.2, 0.6):
        o.append(dot(s, A.X(h), A.Y(p_peak(h)), O["flag"]))
    o.append(H.label(s, A.X(1.12), A.Y(p_peak(1.12, 1.0)) - 12, "n" + SUB("c", s) + " = 1", "label2", I["primary"]))
    o.append(H.label(s, A.X(1.0), A.Y(p_peak(1.0, 0.5)) + 30, "n" + SUB("c", s) + " = 0.5", "label2", I["primary"]))
    o += legend_col(s, A.X(0.78), A.Y(10.5), [(SER[0], None, "working law, n" + SUB("c", s) + " = 0.7"),
                                               (SER[1], DASH_SER, "n" + SUB("c", s) + " = 1, incompressible"),
                                               (SER[2], DASH_SER, "n" + SUB("c", s) + " = 0.5, compressible")], dy=18)
    o += legend(s, A.X(0.78), A.Y(10.5) + 54, [(O["flag"], None, "h = 2.0, 1.2, 0.6 mm: 3.0, 4.3, 7.0", "dot")])
    o.append(H.credit(s, 14, 464, wrap_credit(knee_credit("Contact insets are schematic, not anatomy."))))
    aria = ("Left: a knee in sagittal section with the femoral-tibial contact circled, and two schematic cross-sections of "
            "that contact under the same load: a healthy 2.0 millimetre cartilage layer with a wide contact patch and a "
            f"worn 0.6 millimetre layer with a narrower one. Right: peak contact stress against cartilage thickness. The "
            f"working curve with exponent 0.7 rises from 3.0 megapascals at 2.0 millimetres to {p_peak(1.2):.1f} at 1.2 and "
            f"{p_peak(0.6):.1f} at 0.6; dashed curves for exponents 0.5 and 1 bracket it.")
    pts = hv(A, [A.X(h) for h in hs], [[A.Y(p_peak(h)), A.Y(p_peak(h, 0.5)), A.Y(p_peak(h, 1.0))] for h in hs],
             [f"h = {h:.2f} mm: {p_peak(h):.1f} MPa (n 0.7); {p_peak(h,0.5):.1f} (0.5), {p_peak(h,1.0):.1f} (1)" for h in hs])
    return svg(VB, aria, s, o, hov(pts))


# ================================================================ svg #8: delay erodes the recoverable envelope
W0 = 3.1                                                              # 177: rad/s


def fig8():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    A = Ax((72, 92, 350, 310), (0, 0.30), (0, 1.15))
    B = Ax((452, 92, 735, 310), (0, 0.30), (0, 1.0))
    ts = lin(0, 0.30, 91)
    pre = "m14f8_"
    o = axes(s, A, [(v, f"{v:.2f}") for v in (0, 0.1, 0.2, 0.3)], [(v, f"{v:g}") for v in (0, 0.5, 1.0)],
             "time after the perturbation (s)", "extrapolated COM  ξ / ξ" + H.sub("c", s), ylab_x=14)
    o += axes(s, B, [(v, f"{v:.2f}") for v in (0, 0.1, 0.2, 0.3)], [(v, f"{v:g}") for v in (0, 0.5, 1.0)],
              "reaction delay Δt (s)", "recoverable fraction", ylab_x=B.x0 - 52)
    o.append(H.label(s, A.x0, 26, "the COM keeps diverging during the lag", "label", I["primary"]))
    o.append(H.label(s, B.x0, 26, "recoverable fraction = " + esup(s, "−ω₀Δt"), "label", I["primary"]))
    # panel A: largest catchable perturbation for two delays, xi(t) = xi0 e^(w0 t) reaching xi_c at t = dt
    o.append(H.line(s, A.x0, A.Y(1), A.x1, A.Y(1), I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, A.x0 + 8, A.Y(1) - 13, "bound ξ" + H.sub("c", s), "label2", I["primary"]))
    for dt, col in ((0.12, SER[1]), (0.20, SER[0])):
        x0v = math.exp(-W0 * dt)
        tt = [t for t in ts if t <= dt + 1e-9]
        if tt[-1] < dt:
            tt.append(dt)
        o.append(curve(s, A, tt, [x0v * math.exp(W0 * t) for t in tt], col, "curve_multi"))
        o.append(dot(s, A.X(0), A.Y(x0v), col))
        o.append(dot(s, A.X(dt), A.Y(1), col))
        o.append(H.line(s, A.X(dt), A.Y(1) + 6, A.X(dt), A.y0, I["rule"], "leader", (4, 3)))
        o.append(H.label(s, A.X(0.20) - 4 if dt == 0.20 else A.X(0.12) - 4, A.y0 - 8, f"Δt = {dt:.2f} s", "label2", I["primary"], "end"))
    o += legend_col(s, A.x0, 48, [(SER[1], None, "Δt = 0.12 s, ξ₀ = 0.69 ξ" + SUB("c", s)),
                                                (SER[0], None, "Δt = 0.20 s, ξ₀ = 0.54 ξ" + SUB("c", s))], dy=19)
    # panel B: the factor
    o.append(curve(s, B, ts, [math.exp(-W0 * t) for t in ts], SER[0], "curve"))
    f12, f20 = math.exp(-W0 * 0.12), math.exp(-W0 * 0.20)
    o.append(H.line(s, B.X(0.12), B.Y(f12), B.X(0.20), B.Y(f12), I["secondary"], "ref", H.DASH_REF))
    o.append(H.line(s, B.X(0.20), B.Y(f12) + 3, B.X(0.20), B.Y(f20) - 3, O["geometry"], "geom",
                    extra=f'marker-start="url(#{pre}a_geometry)" marker-end="url(#{pre}a_geometry)"'))
    o.append(dot(s, B.X(0.12), B.Y(f12), SER[1]))
    o.append(dot(s, B.X(0.20), B.Y(f20), SER[0]))
    r = f20 / f12
    o.append(H.label(s, B.X(0.12) + 5, B.Y(f12) - 12, f"{f12:.2f}", "label2", I["primary"]))
    o.append(H.label(s, B.X(0.20) - 8, B.Y(f20) + 18, f"{f20:.2f}", "label2", I["primary"], "end"))
    o.append(H.label(s, B.X(0.20) + 8, (B.Y(f12) + B.Y(f20)) / 2 - 22, f"×{r:.2f}", "label2", I["primary"]))
    o.append(H.label(s, B.X(0.20) + 8, (B.Y(f12) + B.Y(f20)) / 2 - 6, f"(−{100*(1-r):.0f} %)", "label2", I["primary"]))
    aria = (f"Two panels. Left: after a perturbation the extrapolated centre of mass grows as e to the omega-zero t; the "
            f"largest perturbation that can still be caught, for a reaction delay of 0.12 s, starts at {f12:.2f} of the "
            f"capturable bound and for 0.20 s at {f20:.2f}, each reaching the bound when the response starts. Right: the "
            f"recoverable fraction e to the minus omega-zero delta-t with omega-zero 3.1 per second falls from 1 at no "
            f"delay to {f12:.2f} at 0.12 s and {f20:.2f} at 0.20 s, a {100*(1-r):.0f} percent loss.")
    ha = hv(A, [A.X(t) for t in ts], [[A.Y(math.exp(-W0 * 0.12) * math.exp(W0 * t)) if t <= 0.12 else A.Y(1.0),
                                       A.Y(math.exp(-W0 * 0.20) * math.exp(W0 * t)) if t <= 0.20 else A.Y(1.0)] for t in ts],
            [f"t = {t:.2f} s: ξ/ξc = {min(1.0, math.exp(-W0*0.12)*math.exp(W0*t)):.2f} (Δt 0.12), "
             f"{min(1.0, math.exp(-W0*0.20)*math.exp(W0*t)):.2f} (Δt 0.20)" for t in ts])
    hb = hv(B, [B.X(t) for t in ts], [B.Y(math.exp(-W0 * t)) for t in ts],
            [f"Δt = {t:.2f} s: recoverable fraction {math.exp(-W0*t):.2f}" for t in ts])
    return svg(VB, aria, s, [H.markers(pre, s)] + o, hov(ha, hb))


# ================================================================ svg #9: AGE crosslink fraction
K_TURN_T, K_TURN_B = 0.005, 0.10                                      # 200: 1/yr
PHI_SS_BONE = 0.06                                                    # 200, 202
K_AGE_GLC = PHI_SS_BONE * K_TURN_B / (1 - PHI_SS_BONE)                # k_AGE * 5.5 mM, from 0.06 = x/(x+0.10)


def phi(t, k_turn, glc_factor=1.0):
    """Prop. 5.3 closed form, t = years since age 20."""
    x = K_AGE_GLC * glc_factor
    ss = x / (x + k_turn)
    return ss * (1 - math.exp(-(x + k_turn) * t))


def fig9():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    A = Ax((80, 40, 640, 320), (20, 80), (0, 0.30))
    ages = lin(20, 80, 61)
    ser = [("tendon, k" + SUB("turn", s) + " = 0.005 /yr", SER[0], None, lambda a: phi(a - 20, K_TURN_T)),
           ("bone, normoglycemic (5.5 mM)", SER[1], None, lambda a: phi(a - 20, K_TURN_B)),
           ("bone, hyperglycemic (11 mM)", SER[1], DASH_SER, lambda a: phi(a - 20, K_TURN_B, 2.0))]
    o = axes(s, A, [(v, str(v)) for v in (20, 30, 40, 50, 60, 70, 80)], [(v, f"{v:.2f}") for v in (0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30)],
             "age (yr)", "AGE crosslink fraction φ", ylab_x=A.x0 - 62)
    for _, col, dash, f in ser:
        o.append(curve(s, A, ages, [f(a) for a in ages], col, "curve_multi", dash))
    for lab, col, dash, f in ser:
        o.append(dot(s, A.X(80), A.Y(f(80)), col))
        o.append(H.label(s, A.X(80) + 12, A.Y(f(80)) + 5, f"{f(80):.3f}", "label2", I["primary"]))
    o.append(H.label(s, A.X(80) - 120, A.Y(phi(60, K_TURN_T)) - 14, "tendon: never resets", "label2", I["primary"]))
    o.append(H.label(s, A.X(64), A.Y(phi(44, K_TURN_B, 2.0)) - 14, "bone, 11 mM", "label2", I["primary"]))
    o.append(H.label(s, A.X(64), A.Y(phi(44, K_TURN_B)) + 22, "bone, 5.5 mM", "label2", I["primary"]))
    o += legend_col(s, A.x0 + 18, A.Y(0.285), [(c, d, l) for l, c, d, _ in ser], dy=19)
    aria = ("AGE crosslink fraction against age from 20 to 80, from the closed form of Proposition 5.3. A tendon curve with "
            f"near-zero collagen turnover rises steadily to {phi(60, K_TURN_T):.3f} at 80 and is still rising. A bone curve with "
            f"decade-scale turnover levels off at {phi(60, K_TURN_B):.3f} under normal glucose; a dashed bone curve under "
            f"double glucose levels off near {phi(60, K_TURN_B, 2.0):.3f}.")
    pts = hv(A, [A.X(a) for a in ages], [[A.Y(f(a)) for _, _, _, f in ser] for a in ages],
             [f"age {a:.0f}: tendon {ser[0][3](a):.3f}, bone {ser[1][3](a):.3f}, bone 11 mM {ser[2][3](a):.3f}" for a in ages])
    return svg(VB, aria, s, o, hov(pts))


# ================================================================ svg #10: fall-risk model vs age
M_KG = 70.0                                                           # 339
B40, B85, DT40, DT85, CS40, CS85 = 0.10, 0.05, 0.12, 0.20, 0.010, 0.020


def drift(a, q40, q85):
    return q40 + (a - 40) / 45 * (q85 - q40)


def jeff(b, dt, cs):
    return M_KG * W0 * (b - cs) * math.exp(-W0 * dt)


def j_age(a):
    return jeff(drift(a, B40, B85), drift(a, DT40, DT85), drift(a, CS40, CS85))


def fig10():
    VB = (0, 0, 760, 440)
    s = H.Scale(VB[2], VB[3])
    A = Ax((80, 40, 735, 290), (34, 90), (0, 16))
    ages = lin(40, 85, 91)
    o = axes(s, A, [(v, str(v)) for v in (40, 50, 60, 70, 80, 90)], [(v, str(v)) for v in (0, 4, 8, 12, 16)],
             None, "J" + H.sub("eff", s) + " (N s)", ylab_x=A.x0 - 46)
    o.append(curve(s, A, ages, [j_age(a) for a in ages], SER[0], "curve"))
    marks = (40, 55, 70, 85)
    for a in marks:
        o.append(dot(s, A.X(a), A.Y(j_age(a)), O["flag"]))
        o.append(H.label(s, A.X(a) + 9, A.Y(j_age(a)) - 12, f"{j_age(a):.2f}", "label2", I["primary"]))
    # parameter rows under the axis, in the same x positions
    rows = (("b (m)", lambda a: drift(a, B40, B85), "{:.3f}"), ("Δt (s)", lambda a: drift(a, DT40, DT85), "{:.3f}"),
            ("cσ (m)", lambda a: drift(a, CS40, CS85), "{:.4f}"))
    for i, (nm, f, fmt) in enumerate(rows):
        y = A.y0 + 56 + 20 * i
        o.append(H.label(s, A.x0 - 9, y, nm, "label2", I["primary"], "end"))
        for a in marks:
            o.append(H.label(s, A.X(a), y, fmt.format(f(a)), "label2", I["primary"], "middle"))
    o.append(H.label(s, (A.x0 + A.x1) / 2, A.y0 + 130, "age (yr); each parameter drifts linearly between 40 and 85 (an assumption)",
                     "label", I["primary"], "middle"))
    o.append(H.label(s, A.X(52), A.Y(15.2), "J" + H.sub("eff", s) + " = m ω₀ (b − cσ) " + esup(s, "−ω₀Δt").replace(f'{s(H.PX["label"] * 0.7):.2f}', f'{s(H.PX["label2"] * 0.7):.2f}'), "label2", I["primary"]))
    aria = (f"Effective recoverable impulse against age from 40 to 85 years. It falls from {j_age(40):.2f} newton seconds at 40 "
            f"through {j_age(55):.2f} at 55 and {j_age(70):.2f} at 70 to {j_age(85):.2f} at 85, as the balance margin b halves "
            f"from 0.10 to 0.05 metres, the reaction delay rises from 0.12 to 0.20 seconds and the sway cost c sigma rises "
            f"from 0.01 to 0.02 metres. A table under the axis lists the three parameters at ages 40, 55, 70 and 85.")
    pts = hv(A, [A.X(a) for a in ages], [A.Y(j_age(a)) for a in ages],
             [f"age {a:.0f}: J = {j_age(a):.2f} N s (b {drift(a,B40,B85):.3f} m, Δt {drift(a,DT40,DT85):.3f} s)" for a in ages])
    return svg(VB, aria, s, o, hov(pts))


# ================================================================ svg #11: the mechanostat rate law
def fig11():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    A = Ax((80, 40, 735, 320), (0, 2), (-1.1, 1.1))
    xs = lin(0, 2, 41)
    o = [f'<rect x="{A.x0}" y="{A.Y(0):.2f}" width="{A.X(1)-A.x0:.2f}" height="{A.y0-A.Y(0):.2f}" fill="{SER[0]}" opacity="0.10"/>',
         f'<rect x="{A.X(1):.2f}" y="{A.top}" width="{A.x1-A.X(1):.2f}" height="{A.Y(0)-A.top:.2f}" fill="{SER[1]}" opacity="0.10"/>']
    o += axes(s, A, [(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2)], [(v, mn(v, "{:g}")) for v in (-1, -0.5, 0, 0.5, 1)],
              "habitual stimulus Σ / setpoint Σ" + "₀", "dC/dt  (units of k" + H.sub("ad", s) + " Σ" + "₀" + ")",
              ylab_x=A.x0 - 52)
    o.append(H.line(s, A.x0, A.Y(0), A.x1, A.Y(0), I["secondary"], "ref"))
    o.append(curve(s, A, xs, [x - 1 for x in xs], SER[0], "curve"))
    o.append(dot(s, A.X(1), A.Y(0), O["flag"]))
    o.append(H.label(s, A.X(1) + 10, A.Y(0) + 22, "Σ = Σ" + "₀" + ": dC/dt = 0, maintained", "label2", I["primary"]))
    o.append(H.label(s, A.X(0.08), A.Y(0) + 24, "disuse: Σ < Σ" + "₀", "label2", I["primary"]))
    o.append(H.label(s, A.X(0.08), A.Y(0) + 42, "capacity resorbs", "label2", I["primary"]))
    o.append(H.label(s, A.X(1.92), A.Y(0) - 24, "training: Σ > Σ" + "₀", "label2", I["primary"], "end"))
    o.append(H.label(s, A.X(1.92), A.Y(0) - 42, "capacity builds", "label2", I["primary"], "end"))
    o += legend(s, A.x0 + 18, A.Y(0.93), [(SER[0], None, "dC/dt = k" + SUB("ad", s) + " (Σ − Σ" + "₀" + ")"),
                                           (SER[0], None, "resorbing (below setpoint)", "band"),
                                           (SER[1], None, "building (above setpoint)", "band")], gap=18)
    aria = ("The mechanostat rate law: rate of change of tissue capacity, in units of the adaptation rate times the setpoint, "
            "against habitual stimulus divided by the setpoint from 0 to 2. A straight line rises from minus one at zero "
            "stimulus through zero at the setpoint (maintenance) to plus one at twice the setpoint; negative values "
            "are disuse resorption, positive values training build-up.")
    pts = hv(A, [A.X(x) for x in xs], [A.Y(x - 1) for x in xs],
             [f"Σ/Σ0 = {x:.2f}: dC/dt = {mn(x-1, '{:.2f}', True)} kad Σ0" for x in xs])
    return svg(VB, aria, s, o, hov(pts))


# ================================================================ svg #14: Lab A, failure age against peak strength
def fig14():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    A = Ax((80, 40, 735, 320), (110, 260), (40, 150))
    tps = lin(110, 260, 101)
    o = axes(s, A, [(v, str(v)) for v in (110, 130, 150, 175, 210, 230, 250)], [(v, str(v)) for v in (40, 60, 80, 100, 120, 140)],
             "peak knee torque τ" + H.sub("p", s) + " (N m)", "chair-failure age a* (yr)", ylab_x=A.x0 - 48)
    ceil = A0 + 1 / R_LOSS
    o.append(H.line(s, A.x0, A.Y(ceil), A.x1, A.Y(ceil), I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, A.x1 - 4, A.Y(ceil) - 12, "ceiling a" + "₀" + " + 1/r = 140 yr, reached as τ" + H.sub("p", s) + " → ∞",
                     "label2", I["primary"], "end"))
    o.append(curve(s, A, tps, [a_star(t) for t in tps], SER[0], "curve"))
    for tp in (175.0, 210.0):
        a = a_star(tp)
        o.append(H.line(s, A.X(tp), A.y0, A.X(tp), A.Y(a), I["rule"], "leader", (4, 3)))
        o.append(H.line(s, A.x0, A.Y(a), A.X(tp), A.Y(a), I["rule"], "leader", (4, 3)))
        o.append(dot(s, A.X(tp), A.Y(a), O["flag"]))
        o.append(H.label(s, A.X(tp) + 4, A.Y(a) + 24, f"{tp:.0f} N m → {a:.1f} yr", "label2", I["primary"], "middle" if False else "start"))
    o.append(dot(s, A.X(D_CHAIR), A.Y(A0), I["secondary"], hollow=True))
    o.append(H.label(s, A.X(127), A.Y(A0) - 8, "τ" + H.sub("p", s) + " = D = 110 N m: a* = a" + "₀" + " = 40 yr",
                     "label2", I["primary"]))
    aria = (f"Chair-rise failure age against peak knee torque from 110 to 260 newton metres, a-star = 40 + 100 (1 minus 110 over "
            f"torque). It starts at 40 years when torque equals the 110 newton metre demand, rises steeply, passes "
            f"{a_star(175):.1f} years at 175 and {a_star(210):.1f} at 210, and flattens toward a ceiling of 140 years.")
    pts = hv(A, [A.X(t) for t in tps], [A.Y(a_star(t)) for t in tps],
             [f"τp = {t:.0f} N m: a* = {a_star(t):.1f} yr" for t in tps])
    return svg(VB, aria, s, o, hov(pts))


# ================================================================ svg #16: Lab B, fracture margin against density
S0_N, NB, G, HF, M_EFF, K_N = 7000.0, 2.0, 9.81, 0.70, 35.0, 40e3      # 287


def f_peak(k=K_N):
    return math.sqrt(2 * G * HF) * math.sqrt(M_EFF * k)


def fig16():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    A = Ax((80, 40, 735, 320), (50, 100), (0, 2.5))
    bm = lin(0.5, 1.0, 101)
    F0, F1 = f_peak(), f_peak(K_N / 2)
    crit0, crit1 = math.sqrt(F0 / S0_N), math.sqrt(F1 / S0_N)
    o = axes(s, A, [(v, str(v)) for v in (50, 60, 70, 80, 90, 100)], [(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2, 2.5)],
             "bone density (% of young)", "fracture margin S / F", ylab_x=A.x0 - 48)
    o.append(H.line(s, A.x0, A.Y(1), A.x1, A.Y(1), I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, A.x0 + 8, A.Y(1) - 8, "S / F = 1: fracture limit", "label2", I["primary"]))
    o.append(curve(s, A, [b * 100 for b in bm], [S0_N * b ** NB / F0 for b in bm], SER[0], "curve_multi"))
    o.append(curve(s, A, [b * 100 for b in bm], [S0_N * b ** NB / F1 for b in bm], SER[1], "curve_multi", DASH_SER))
    for c, col in ((crit0, SER[0]), (crit1, SER[1])):
        o.append(H.line(s, A.X(100 * c), A.Y(1) + 6, A.X(100 * c), A.y0, I["rule"], "leader", (4, 3)))
        o.append(dot(s, A.X(100 * c), A.Y(1), col))
        o.append(H.label(s, A.X(100 * c) - 5, A.y0 - 8, f"{100*c:.0f} %", "label2", I["primary"], "end"))
    o.append(H.label(s, A.X(86), A.Y(S0_N * 0.90 ** 2 / F0) - 14, "bare floor", "label2", I["primary"]))
    o.append(H.label(s, A.X(98), A.Y(S0_N / F1) - 12, "hip protector", "label2", I["primary"], "end"))
    o += legend_col(s, A.x0 + 14, A.Y(2.4), [
        (SER[0], None, f"bare floor, k = 40 kN/m: F = {F0/1000:.2f} kN, critical density {100*crit0:.0f} %"),
        (SER[1], DASH_SER, f"hip protector, k = 20 kN/m: F = {F1/1000:.2f} kN, critical density {100*crit1:.0f} %")], dy=19)
    aria = (f"Hip-fracture margin S over F against bone density from 50 to 100 percent of young, with S = 7000 newtons times "
            f"density squared. On a bare floor the impact force is {F0:.0f} newtons and the margin crosses one at "
            f"{100*crit0:.0f} percent density. A hip protector that halves landing stiffness cuts the force to {F1:.0f} "
            f"newtons and moves the crossing to {100*crit1:.0f} percent.")
    pts = hv(A, [A.X(100 * b) for b in bm], [[A.Y(S0_N * b ** NB / F0), A.Y(S0_N * b ** NB / F1)] for b in bm],
             [f"density {100*b:.0f} %: margin {S0_N*b**NB/F0:.2f} bare, {S0_N*b**NB/F1:.2f} with protector" for b in bm])
    return svg(VB, aria, s, o, hov(pts))


# ================================================================ svg #18: Lab C, cartilage feedback over time
KAPPA, BETA, DT_LAB = 0.010, 0.010, 0.5                               # 316


def lab_c(load):
    """The lab's forward-Euler loop (315-325), 120 steps; the curve ends at the first sample with h <= 0.30 mm."""
    h, ts, ps, hs = H0, [], [], []
    for i in range(120):
        p = P0 * (H0 / h) ** NC
        ts.append(i * DT_LAB)
        ps.append(p)
        hs.append(h)
        h = max(0.05, h + (-KAPPA * load * p + BETA * (H0 - h)) * DT_LAB)
    return ts, ps, hs


def fig18():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    A = Ax((80, 40, 735, 320), (0, 60), (0, 12))
    t1, p1, h1 = lab_c(1.0)
    n = next(i for i, h in enumerate(h1) if h <= 0.30)
    t1, p1, h1 = t1[:n + 1], p1[:n + 1], h1[:n + 1]
    t0, p0v, _ = lab_c(0.0)
    o = axes(s, A, [(v, str(v)) for v in (0, 10, 20, 30, 40, 50, 60)], [(v, str(v)) for v in (0, 3, 6, 9, 12)],
             "time (yr)", "peak stress (MPa)", ylab_x=A.x0 - 48)
    o.append(curve(s, A, t0, p0v, SER[1], "curve_multi"))
    o.append(curve(s, A, t1, p1, SER[0], "curve_multi"))
    o.append(dot(s, A.X(t1[-1]), A.Y(p1[-1]), O["flag"]))
    o.append(H.label(s, A.X(t1[-1]) - 10, A.Y(p1[-1]) - 4, f"layer spent (h ≤ 0.30 mm)", "label2", I["primary"], "end"))
    o.append(H.label(s, A.X(t1[-1]) - 10, A.Y(p1[-1]) + 12, f"at {t1[-1]:.1f} yr, {p1[-1]:.1f} MPa", "label2", I["primary"], "end"))
    o.append(H.label(s, A.X(30), A.Y(3.0) - 10, "unloaded joint: h stays 2 mm, 3.0 MPa", "label2", I["primary"]))
    o.append(H.label(s, A.X(4), A.Y(7.0), "thinner layer, higher stress, faster thinning: the loop accelerates", "label2", I["primary"]))
    o += legend_col(s, A.x0 + 18, A.Y(11.2), [(SER[0], None, "L = 1, full load: runaway"), (SER[1], None, "L = 0, unloaded: maintained")], dy=19)
    aria = (f"Peak cartilage stress against time for the load-damage feedback dh/dt = minus kappa L p plus beta (h0 minus h). "
            f"At full load L = 1 the stress climbs from 3.0 megapascals, faster as the layer thins, to {p1[-1]:.1f} at "
            f"{t1[-1]:.1f} years when the layer reaches 0.30 millimetres and is taken as spent. At L = 0 the layer and the "
            f"3.0 megapascal stress stay constant.")
    ptsr = hv(A, [A.X(t) for t in t1], [A.Y(p) for p in p1], [f"t = {t:.1f} yr: {p:.1f} MPa, h = {h:.2f} mm" for t, p, h in zip(t1, p1, h1)])
    return svg(VB, aria, s, o, hov(ptsr))


# ================================================================ svg #20: Lab D, ranking the fall-risk factors
def fig20():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    A = Ax((90, 40, 740, 290), (0, 5), (0, 16))
    base = dict(b=B40, dt=DT40, cs=CS40)
    j0, j85 = jeff(**base), jeff(B85, DT85, CS85)
    bars = []
    for nm, key, aged, col, cap in (("margin b alone", "b", B85, SER[0], "b: 0.10 → 0.05 m"),
                                     ("delay Δt alone", "dt", DT85, SER[1], "Δt: 0.12 → 0.20 s"),
                                     ("noise cσ alone", "cs", CS85, SER[2], "cσ: 0.010 → 0.020 m")):
        p = dict(base)
        p[key] = aged
        j = jeff(**p)
        bars.append((nm, cap, j, col, 100 * (j0 - j) / (j0 - j85)))
    allb = [("young", "b, Δt, cσ all young", j0, I["rule"], None)] + bars + [("aged, 85 yr", "all three aged", j85, I["secondary"], 100.0)]
    o = axes(s, A, [], [(v, str(v)) for v in (0, 4, 8, 12, 16)], None, "J" + H.sub("eff", s) + " (N s)", ylab_x=A.x0 - 46)
    pts_x, pts_y, pts_t = [], [], []
    for i, (nm, cap, j, col, share) in enumerate(allb):
        xc = A.X(i + 0.5)
        o.append(f'<rect x="{xc-36:.2f}" y="{A.Y(j):.2f}" width="72" height="{A.y0-A.Y(j):.2f}" fill="{col}"/>')
        o.append(H.label(s, xc, A.Y(j) - 24 if share not in (None,) and 0 < share < 100 else A.Y(j) - 8, f"{j:.1f}", "label", I["primary"], "middle"))
        if share is not None and 0 < share < 100:
            o.append(H.label(s, xc, A.Y(j) - 8, f"{share:.0f} % of the drop", "label2", I["primary"], "middle"))
        o.append(H.label(s, xc, A.y0 + 20, nm, "label2", I["primary"], "middle"))
        o.append(H.label(s, xc, A.y0 + 37, cap, "label2", I["secondary"], "middle"))
        pts_x.append(xc)
        pts_y.append(A.Y(j))
        pts_t.append(f"{nm}: J = {j:.2f} N s" + (f" ({share:.0f} % of the drop)" if share and share < 100 else ""))
    o.append(H.label(s, 20, 372, "Shares exceed 100 % in total because the three factors multiply. Elasticities at the young point: "
                     "b +1.11, Δt −0.37, cσ −0.11.", "label2", I["primary"]))
    aria = (f"Bar chart of the effective recoverable impulse in newton seconds. Young, {j0:.1f}. Taking each parameter to its aged "
            f"value alone: margin b to 0.05 metres gives {bars[0][2]:.1f}, {bars[0][4]:.0f} percent of the drop; delay to 0.20 "
            f"seconds gives {bars[1][2]:.1f}, {bars[1][4]:.0f} percent; sensor noise c sigma to 0.020 metres gives "
            f"{bars[2][2]:.1f}, {bars[2][4]:.0f} percent. All three aged, {j85:.1f}.")
    return svg(VB, aria, s, o, hov((list(map(lambda v: round(v, 2), A.box)), [[x, y, t] for x, y, t in zip(pts_x, pts_y, pts_t)])))


FIGS = {
    4: ("Capacity declining with age toward a fixed task demand, and ", fig4),
    5: ("Strength reserve versus age for two peak strengths, each cro", fig5),
    7: ("Peak cartilage contact stress rising as the layer thins, bes", fig7),
    8: ("The recoverable-perturbation factor e to the minus omega-zer", fig8),
    9: ("AGE crosslink fraction against age from 20 to 80. A tendon c", fig9),
    10: ("The effective recoverable impulse falling with age as margin", fig10),
    11: ("The mechanostat rate law: rate of change of tissue capacity ", fig11),
    14: ("Chair-rise failure age versus peak midlife strength, rising ", fig14),
    16: ("Hip-fracture margin versus bone density, crossing one, and h", fig16),
    18: ("Peak cartilage stress over time for a degenerating joint (ru", fig18),
    20: ("Effective recoverable impulse when each aging parameter is t", fig20),
}
