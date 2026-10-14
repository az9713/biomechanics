"""Module 2, group `beam`: beam bending, sections, stress fields and mechanics schematics in the house style.

Main text (760 px): svg #2 (setup for (3.1)), #4 (pure-bending kinematics, slider + Play).
Problem figures (400 px): #12 C1, #13 C2, #14 C3, #16 C5, #19 C8, #22 D1, #24 D3, #25 D4, #26 D5, #28 D7,
#30 D9, #31 D10.
Colours, one meaning each in the whole group: tension = SERIES[0] red, compression = SERIES[1] blue (light tints
for regions, solid for lines); applied loads and end moments = load brown; support reactions = black; dimensions =
geometry blue (dim grey #555555 in #2 and #13, which also show compression blue); cortex = bone tokens, medullary canal = marrow token; mineral platelets = bone_shade, collagen =
tendon (as m00/tissue.py fig2). Bending sense: sagging (compression on top) everywhere; y is measured from the
neutral axis toward the tension face, so sigma = M y / I and epsilon = kappa y are positive in tension (Def. 1.1).
Every number is computed here from a value module02.html states (line numbers beside each constant).
"""
import math

import numpy as np

import house as H
from m05.body import finish
from m05.plots_main import Ax, axes, curve, dot
from m05.tissue import circ, path, rect, sw_line, sw_rect

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
TEN, COM = SER[0], SER[1]
TINT = 0.22
BOX = "#f7f4ef"
BONE, BONE_L = T["bone"]
MARROW = T["marrow"][0]

# ---------------------------------------------------------------- values the module states
R_MM, r_MM = 14.0, 7.0                     # line 188 (femoral tube), line 194 (I, Z), line 325 (J)
SIG_C, SIG_T = 170.0, 130.0                # line 242, line 678 (compressive, tensile strength, MPa)
SIG_NOM, KT_LO, KT_HI, SIG_LOC = 40.0, 2.0, 3.0, 100.0   # line 688, 691
E_M, E_C, V_M = 100.0, 1.0, 0.5            # line 336, 767 (GPa, mineral volume fraction)
E_BONE = 17.0                              # line 178, 336
M_EFF, H_FALL, K_S, G = 28.0, 0.5, 5e4, 9.81   # line 415, 775


def it(t):
    return f'<tspan font-style="italic">{t}</tspan>'


def legend(s, x, y, items, gap=18):
    """One legend row; items = [(swatch_fn(x, y), text)]. Text width estimated at 0.5 em (Georgia)."""
    o = []
    for sw, txt in items:
        o.append(sw(x, y))
        o.append(H.label(s, x + s(19), y, txt, "label2", I["secondary"]))
        x += s(19) + s(13) * 0.5 * len(txt) + s(gap)
    return "".join(o), x


def sw_tint(col):
    return lambda x, y: rect(x, y - 10, 14, 10, col, None, 0, 0, f'fill-opacity="{TINT + 0.1}"')


def dim(s, p, x1, y1, x2, y2):
    """Dimension: geometry-blue double-headed arrow."""
    return H.arrow(s, p, x1, y1, x2, y2, "geometry", both=True)


def tick(s, x1, y1, x2, y2):
    return H.line(s, x1, y1, x2, y2, O["dim"], "leader")


def moment_arc(s, p, cx, cy, r, a0, a1):
    """Curved moment arrow, load brown, from screen angle a0 to a1 (degrees, y down; a1 > a0 = clockwise)."""
    pt = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))  # noqa: E731
    (x0, y0), (x1, y1) = pt(a0), pt(a1)
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 1 if a1 > a0 else 0
    return path(f"M{x0:.2f},{y0:.2f} A{r},{r} 0 {large} {sweep} {x1:.2f},{y1:.2f}", O["load"], s(H.PX["load"]),
                extra=f'marker-end="url(#{p}a_load)"')


def arcpts(cx, cy, rad, ph0, ph1, n=40):
    """Points of a circle arc about (cx, cy); ph measured from straight down (y down), positive to the right."""
    return [(cx + rad * math.sin(ph), cy + rad * math.cos(ph)) for ph in np.linspace(ph0, ph1, n)]


def dpath(pts, close=False):
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + (" Z" if close else "")


def ann(cx, cy, ro, ri, fill, stroke, sw):
    """Annulus as one even-odd path."""
    d = (f"M{cx - ro:.2f},{cy:.2f} a{ro},{ro} 0 1,0 {2 * ro:.2f},0 a{ro},{ro} 0 1,0 {-2 * ro:.2f},0 Z "
         f"M{cx - ri:.2f},{cy:.2f} a{ri},{ri} 0 1,0 {2 * ri:.2f},0 a{ri},{ri} 0 1,0 {-2 * ri:.2f},0 Z")
    return f'<path d="{d}" fill="{fill}" fill-rule="evenodd" stroke="{stroke}" stroke-width="{sw:.2f}"/>'


def tube(s, cx, cy, R, r):
    """Femoral midshaft section: cortex in bone tokens, canal in the marrow token."""
    return (circ(cx, cy, r, MARROW, BONE_L, s(1.0)) + ann(cx, cy, R, r, BONE, BONE_L, s(1.4)))


def hatch(s, x0, x1, y, n=None):
    o = [H.line(s, x0, y, x1, y, I["axis"], "axis")]
    k = n or int((x1 - x0) / 9)
    for i in range(k):
        x = x0 + 4 + i * (x1 - x0 - 8) / max(k - 1, 1)
        o.append(H.line(s, x, y, x - 6, y + 7, I["axis"], "leader"))
    return "".join(o)


def section_numbers():
    """Lines 194, 325: I = 2.83e-8 m^4, Z = 2.02e-6 m^3, J = 5.66e-8 m^4 for R = 14, r = 7 mm."""
    R, r = R_MM / 1e3, r_MM / 1e3
    Iv = math.pi / 4 * (R ** 4 - r ** 4)
    Zv, Jv = Iv / R, math.pi / 2 * (R ** 4 - r ** 4)
    assert abs(Iv - 2.83e-8) < 0.005e-8 and abs(Zv - 2.02e-6) < 0.005e-6 and abs(Jv - 5.66e-8) < 0.005e-8
    return Iv, Zv, Jv


def ratio(b):
    """Prop. 3.3 / D4: Z_hollow / Z_solid at equal area."""
    return (1 + b * b) / math.sqrt(1 - b * b)


def sup(t):
    return t.translate(str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"))


def sci(v, n=2):
    e = math.floor(math.log10(abs(v)))
    return f"{v / 10 ** e:.{n}f} × 10{sup(str(e))}"


# ================================================================ svg #2: setup for (3.1)
def fig2():
    p = "m2f2_"
    VB = (0, 0, 760, 384)
    s = H.Scale(VB[2], VB[3])
    Iv, Zv, _ = section_numbers()
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # ---- left: a bent segment, sagging; the centre of curvature C sits above it
    cx, cy, Rn, c, ph = 205.0, 30.0, 236.0, 44.0, math.radians(32)
    top, neu, bot = arcpts(cx, cy, Rn - c, -ph, ph), arcpts(cx, cy, Rn, -ph, ph), arcpts(cx, cy, Rn + c, -ph, ph)
    o.append(path(dpath(top + neu[::-1], True), "none", 0, fill=COM, extra=f'fill-opacity="{TINT}"'))
    o.append(path(dpath(neu + bot[::-1], True), "none", 0, fill=TEN, extra=f'fill-opacity="{TINT}"'))
    o.append(path(dpath(top + bot[::-1], True), BONE_L, s(1.2)))
    o.append(path(dpath(top), COM, s(2.0)))
    o.append(path(dpath(bot), TEN, s(2.0)))
    o.append(path(dpath(neu), I["primary"], s(1.4)))
    # plane sections: radial lines; the two end faces extended (dashed) to C
    ends = []
    for k in (-1.0, -0.5, 0.5, 1.0):
        a = k * ph
        (x1, y1), (x2, y2) = arcpts(cx, cy, Rn - c, a, a, 1)[0], arcpts(cx, cy, Rn + c, a, a, 1)[0]
        o.append(H.line(s, x1, y1, x2, y2, I["primary"], "ref"))
        if abs(k) == 1.0:
            o.append(H.line(s, cx, cy, x1, y1, O["dim"], "leader", H.DASH_REF))
            ends.append((x1, y1))
    o.append(circ(cx, cy, s(3), I["primary"]))
    o.append(H.label(s, cx + 12, cy + 5, "centre of curvature:", "label2", I["secondary"]))
    o.append(H.label(s, cx + 36, cy + 21, "plane sections stay plane and rotate about it", "label2", I["secondary"]))
    lx, ly = (cx + ends[0][0]) / 2, (cy + ends[0][1]) / 2
    o.append(H.label(s, lx - 8, ly + 4, f'{it("R")}{H.sub("κ", s, "label2")} = 1/{it("κ")}', "label2", I["secondary"], "end"))
    ym = cy + Rn
    o.append(H.label(s, cx, ym - c / 2 + 5, "compression", "label2", I["primary"], "middle"))
    o.append(H.label(s, cx, ym + 5, f'neutral axis, {it("ε")} = 0', "label2", I["primary"], "middle"))
    o.append(H.label(s, cx, ym - c - 10, "top fibres shorten", "label2", I["primary"], "middle"))
    o.append(H.label(s, cx, ym + c + 22, "bottom fibres lengthen: tension;", "label2", I["primary"], "middle"))
    o.append(H.label(s, cx, ym + c + 38, f'a fibre at distance {it("y")} has {it("ε")} = {it("κy")}', "label2", I["primary"], "middle"))
    # y: from the neutral axis toward the tension face, at a fibre between two sections
    ay = ph * 0.75
    (nx, ny) = arcpts(cx, cy, Rn, ay, ay, 1)[0]
    (fx, fy) = arcpts(cx, cy, Rn + 30, ay, ay, 1)[0]
    o.append(H.arrow(s, p, nx, ny, fx, fy, "dim", w="geom"))
    o.append(circ(fx, fy, s(2.6), I["primary"]))
    o.append(H.label(s, nx + 7, ny + 17, it("y"), "label", O["dim"]))
    # end moments (sagging): left end clockwise, right end counter-clockwise
    for sgn in (-1, 1):
        (ex, ey) = arcpts(cx, cy, Rn, sgn * ph, sgn * ph, 1)[0]
        out = math.degrees(math.atan2(-math.sin(ph), -math.cos(ph))) if sgn < 0 else math.degrees(-ph)
        a0, a1 = (out - 62, out + 62) if sgn < 0 else (out + 62, out - 62)
        o.append(moment_arc(s, p, ex, ey, 34, a0, a1))
        o.append(H.label(s, ex + sgn * 52, ey - 24, it("M"), "label", O["load"], "middle"))
    # ---- right: the femoral section (R/r = 2) and the linear stress across it
    k = 4.3                                       # px per mm
    sx, R, r = 486.0, R_MM * k, r_MM * k
    o.append(tube(s, sx, ym, R, r))
    o.append(H.line(s, sx - R - 14, ym, 712, ym, I["primary"], "ref", H.DASH_REF))
    o.append(H.label(s, sx - R - 16, ym + 4, "N.A.", "label2", I["secondary"], "end"))
    o.append(H.arrow(s, p, sx, ym, sx, ym + 46, "dim", w="geom"))
    o.append(H.label(s, sx + 6, ym + 32, it("y"), "label", O["dim"]))
    da, db = math.radians(-40), math.radians(-140)
    o.append(H.arrow(s, p, sx, ym, sx + R * math.cos(da), ym + R * math.sin(da), "dim", w="geom"))
    o.append(H.label(s, sx + R * math.cos(da) + 6, ym + R * math.sin(da) - 4, f'{it("R")} = {R_MM:.0f} mm', "label2", O["dim"]))
    o.append(H.arrow(s, p, sx, ym, sx + r * math.cos(db), ym + r * math.sin(db), "dim", w="geom"))
    o.append(H.label(s, sx + r * math.cos(db) - 6, ym + r * math.sin(db) - 8, f'{it("r")} = {r_MM:.0f} mm', "label2", O["dim"], "end"))
    o.append(H.label(s, sx - R, ym - R - 46, f'{it("I")} = π({it("R")}⁴ − {it("r")}⁴)/4 = {sci(Iv)} m⁴', "label2", I["primary"]))
    o.append(H.label(s, sx - R, ym - R - 28, f'{it("Z")} = {it("I")}/{it("R")} = {sci(Zv)} m³', "label2", I["primary"]))
    # stress profile sigma = M y / I (y toward the tension face), on the section's own y
    px, w = 652.0, 54.0
    for yy in (ym - R, ym + R):
        o.append(H.line(s, sx, yy, px + w + 4, yy, O["dim"], "leader", H.DASH_REF))
    o.append(path(f"M{px},{ym - R:.2f} L{px - w},{ym - R:.2f} L{px},{ym:.2f} Z", "none", 0, fill=COM, extra=f'fill-opacity="{TINT + 0.08}"'))
    o.append(path(f"M{px},{ym + R:.2f} L{px + w},{ym + R:.2f} L{px},{ym:.2f} Z", "none", 0, fill=TEN, extra=f'fill-opacity="{TINT + 0.08}"'))
    for f in (0.45, 0.8):
        for sg in (-1, 1):
            o.append(H.arrow(s, p, px + sg, ym + sg * f * R, px + sg * (f * w - 2), ym + sg * f * R, "dim", w="ref"))
    o.append(H.line(s, px - w, ym - R, px + w, ym + R, I["primary"], "geom"))
    o.append(H.line(s, px, ym - R - 6, px, ym + R + 6, I["axis"], "axis"))
    o.append(H.label(s, px - w - 4, ym - R - 8, f'−{it("Mc")}/{it("I")}', "label2", I["primary"], "middle"))
    o.append(H.label(s, px + w + 4, ym + R + 20, f'+{it("Mc")}/{it("I")}', "label2", I["primary"], "middle"))
    o.append(H.label(s, px + 8, ym - 8, f'{it("σ")}({it("y")}) = {it("My")}/{it("I")}', "label2", I["primary"]))
    lg, _ = legend(s, 24, 374, [(sw_rect(BONE, BONE_L), "cortical bone"), (sw_rect(MARROW, BONE_L), "medullary canal"),
                                (sw_tint(COM), "compression (blue)"), (sw_tint(TEN), "tension (red)"),
                                (sw_line(O["load"], 2.5), "applied moment M")])
    o.append(lg)
    aria = ("Left: a beam segment in pure sagging bending under end moments M (brown). Plane sections stay plane and "
            "rotate about the centre of curvature at radius R kappa = 1 over kappa. The top fibres (blue, compression) "
            "shorten, the bottom fibres (red, tension) lengthen, and the neutral axis keeps its length, epsilon = 0. "
            "A fibre at distance y from the neutral axis, toward the tension face, has strain kappa y. Right: the "
            "femoral midshaft section, cortical bone with outer radius R = 14 mm around a medullary canal of radius "
            "r = 7 mm, neutral axis through the centre, and beside it the linear stress sigma(y) = M y / I, from minus "
            f"M c / I (top) to plus M c / I (bottom). I = {sci(Iv)} m4, Z = {sci(Zv)} m3.")
    return finish(VB, aria, s, o)


# ================================================================ svg #4: pure-bending kinematics (slider + Play)
F4 = dict(L=600.0, c=40.0, xm=380.0, yN=168.0, strains=[k / 100 for k in range(9)])   # outer-fibre strain c*kappa


def f4_geom(e):
    """Fibre polylines for outer strain e = c*kappa: top, neutral, bottom, and the section angles."""
    L, c, xm, yN = F4["L"], F4["c"], F4["xm"], F4["yN"]
    if e == 0:
        xs = np.linspace(xm - L / 2, xm + L / 2, 9)
        line = lambda y: [(x, y) for x in xs]  # noqa: E731
        return line(yN - c), line(yN), line(yN + c), None
    Rk = c / e
    th = L / Rk
    cy = yN - Rk
    return (arcpts(xm, cy, Rk - c, -th / 2, th / 2, 9), arcpts(xm, cy, Rk, -th / 2, th / 2, 9),
            arcpts(xm, cy, Rk + c, -th / 2, th / 2, 9), (cy, Rk, th))


def f4_frame(s, p, e):
    top, neu, bot, arc = f4_geom(e)
    if arc:
        cy, Rk, th = arc
        c = F4["c"]
        top_d, neu_d, bot_d = (arcpts(F4["xm"], cy, Rk + d, -th / 2, th / 2, 20) for d in (-c, 0, c))
    else:
        top_d, neu_d, bot_d = [top[0], top[-1]], [neu[0], neu[-1]], [bot[0], bot[-1]]
    pl = lambda q: " ".join(f"{x:.1f},{y:.1f}" for x, y in q)  # noqa: E731
    o = [f'<path d="M{pl(top_d + bot_d[::-1]).replace(" ", " L")} Z" fill="{BONE}" stroke="{BONE_L}" stroke-width="{s(1.0):.2f}"/>']
    for (x1, y1), (x2, y2) in ((top[0], bot[0]), (top[-1], bot[-1])):
        o.append(H.line(s, x1, y1, x2, y2, I["primary"], "ref"))
    for pts, col, w in ((top_d, COM, "curve"), (neu_d, I["primary"], "curve_multi"), (bot_d, TEN, "curve")):
        o.append(f'<polyline points="{pl(pts)}" fill="none" stroke="{col}" stroke-width="{s(H.PX[w]):.2f}"/>')
    # material points: the same 9 sections on every fibre; their spacing is the fibre's stretch
    for pts, col in ((top, COM), (neu, I["primary"]), (bot, TEN)):
        o.append(f'<g fill="#fff" stroke="{col}" stroke-width="1.3">'
                 + "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.4"/>' for x, y in pts[1:-1]) + "</g>")
    xm, yN, c = F4["xm"], F4["yN"], F4["c"]
    pct = f"{e * 100:.0f} %"
    o.append(H.label(s, xm, yN - c - 12, f'top fibre shortens: {it("ε")} = −{pct}' if e else f'top fibre: {it("ε")} = 0',
                     "label2", I["primary"], "middle"))
    o.append(H.label(s, xm, yN - 20, f'neutral fibre: length unchanged, {it("ε")} = 0', "label2", I["primary"], "middle"))
    o.append(H.label(s, xm, yN + c + 22, f'bottom fibre lengthens: {it("ε")} = +{pct}' if e else f'bottom fibre: {it("ε")} = 0',
                     "label2", I["primary"], "middle"))
    if arc:
        cy, Rk, th = arc
        for sgn in (-1, 1):
            ex, ey = neu[0] if sgn < 0 else neu[-1]
            out = math.degrees(math.atan2(-math.sin(th / 2), -math.cos(th / 2))) if sgn < 0 else math.degrees(-th / 2)
            a0, a1 = (out - 60, out + 60) if sgn < 0 else (out + 60, out - 60)
            o.append(moment_arc(s, p, ex, ey, 30, a0, a1))
            o.append(H.label(s, ex + sgn * 46, ey - 18, it("M"), "label", O["load"], "middle"))
    return "".join(o)


def f4_extent():
    """Union bounding box of every frame (fibres + moment arcs), so no hidden frame leaves the viewBox."""
    xs, ys = [], []
    for e in F4["strains"]:
        top, neu, bot, arc = f4_geom(e)
        for q in (top, bot):
            xs += [x for x, _ in q]
            ys += [y for _, y in q]
        if arc:
            for x, y in (neu[0], neu[-1]):
                xs += [x - 34, x + 34]
                ys += [y - 34, y + 34]
    return min(xs), min(ys), max(xs), max(ys)


def fig4():
    p = "m2f4_"
    VB = (0, 0, 760, 262)
    s = H.Scale(VB[2], VB[3])
    x0, y0, x1, y1 = f4_extent()
    assert x0 > VB[0] and y0 > VB[1] and x1 < VB[2] and y1 < 236, (x0, y0, x1, y1)
    n = len(F4["strains"])
    frames = "".join(H.frame(k, n - 1, f4_frame(s, p, e)) for k, e in enumerate(F4["strains"]))
    lg, _ = legend(s, 70, 254, [(sw_line(COM), "top fibre (compression)"), (sw_line(I["primary"], 2.0), "neutral fibre"),
                                (sw_line(TEN), "bottom fibre (tension)"), (sw_line(O["load"]), "applied moment M")])
    vals = [f"±{e * 100:.0f} %" if e else "0" for e in F4["strains"]]
    extra = H.frames_attr("outer-fibre strain cκ", vals, n - 1)
    aria = ("Pure bending of a straight beam, drawn to scale, its length 15 times its half-depth c. A slider "
            "steps the outer-fibre strain c kappa from 0 to 8 percent; the default view is 8 percent. The three "
            "fibres are concentric arcs about one centre of curvature: the top fibre (blue) shortens by c kappa "
            "(compression), the neutral fibre (black) keeps its length, the bottom fibre (red) lengthens by c kappa "
            "(tension). White dots mark the same material sections on each fibre; their spacing shows the stretch. "
            "End moments M (brown) bend the beam.")
    return finish(VB, aria, s, [f'<defs>{H.markers(p, s)}</defs>', frames, lg], extra=extra)


# ================================================================ svg #12 (C1): equal-area tube and rod
def fig12():
    p = "m2f12_"
    VB = (0, 0, 420, 262)
    s = H.Scale(VB[2], VB[3], display_w=400)
    b = r_MM / R_MM
    a_rel = math.sqrt(1 - b * b)                       # a = sqrt(R^2 - r^2)
    q = ratio(b)
    assert abs(a_rel - 0.866) < 0.001 and abs(q - 1.443) < 0.0005
    R = 64.0
    yc = 112.0
    o = [f'<defs>{H.markers(p, s)}</defs>']
    for cxx, rad, solid in ((106.0, R, False), (308.0, R * a_rel, True)):
        o.append(circ(cxx, yc, rad, BONE, BONE_L, s(1.4)) if solid else tube(s, cxx, yc, R, R * b))
        o.append(H.line(s, cxx - R - 10, yc, cxx + R + 10, yc, I["primary"], "ref", H.DASH_REF))
        o.append(H.arrow(s, p, cxx, yc, cxx, yc - rad, "geometry"))
    o.append(H.label(s, 112, yc - 40, f'{it("c")} = {it("R")}', "label2", O["geometry"]))
    o.append(H.label(s, 314, yc - 34, f'{it("c")} = {it("a")}', "label2", O["geometry"]))
    o.append(H.label(s, 106, yc + R + 22, f'hollow tube, {it("R")}/{it("r")} = 2', "label", I["primary"], "middle"))
    o.append(H.label(s, 106, yc + R + 40, f'area {it("A")} = π({it("R")}² − {it("r")}²)', "label2", I["secondary"], "middle"))
    o.append(H.label(s, 308, yc + R + 22, "solid rod, same area", "label", I["primary"], "middle"))
    o.append(H.label(s, 308, yc + R + 40, f'{it("a")} = √({it("R")}² − {it("r")}²) = {a_rel:.2f} {it("R")}', "label2", I["secondary"], "middle"))
    o.append(H.label(s, 210, 22, f'same mass per length; {it("Z")}{H.sub("tube", s)} / {it("Z")}{H.sub("rod", s)} = {q:.2f}',
                     "label", I["primary"], "middle"))
    lg, _ = legend(s, 50, 252, [(sw_rect(BONE, BONE_L), "cortical bone"), (sw_rect(MARROW, BONE_L), "medullary canal")])
    o.append(lg)
    aria = ("Problem C1 setup: two cross-sections of equal area, hence equal mass per length. Left, the hollow femoral "
            "tube with R over r = 2, area pi (R squared minus r squared), its outer fibre at c = R. Right, a solid rod "
            f"of the same area, radius a = square root of (R squared minus r squared) = {a_rel:.2f} R, outer fibre at "
            f"c = a. The neutral axis is dashed through each centre. Section-modulus ratio tube to rod = {q:.2f}.")
    return finish(VB, aria, s, o)


# ================================================================ svg #13 (C2): linear stress across the section
def fig13():
    p = "m2f13_"
    VB = (0, 0, 420, 276)
    s = H.Scale(VB[2], VB[3], display_w=400)
    b = r_MM / R_MM
    lostA, lostI = b ** 2, b ** 4                       # bore share of the full disc's area and of its I
    assert abs(lostA - 0.25) < 1e-9 and abs(lostI - 0.0625) < 1e-9
    R, cx, yc = 66.0, 100.0, 122.0
    r = R * b
    o = [f'<defs>{H.markers(p, s)}</defs>', tube(s, cx, yc, R, r)]
    px, w = 300.0, 66.0
    o.append(H.line(s, cx - R - 12, yc, px + w + 10, yc, I["primary"], "ref", H.DASH_REF))
    o.append(H.label(s, cx - R - 6, yc - 7, "N.A.", "label2", I["secondary"]))
    o.append(H.arrow(s, p, cx, yc, cx, yc + 26, "dim", w="geom"))
    o.append(H.label(s, cx + 6, yc + 22, it("y"), "label", O["dim"]))
    for yy, col in ((yc - R, O["dim"]), (yc + R, O["dim"]), (yc - r, I["rule"]), (yc + r, I["rule"])):
        x_out = cx + math.sqrt(max(R * R - (yy - yc) ** 2, 0))
        o.append(H.line(s, x_out, yy, px + w * (yy - yc) / R + (4 if yy > yc else -4), yy, col, "leader", H.DASH_REF))
    o.append(path(f"M{px},{yc - R:.2f} L{px - w},{yc - R:.2f} L{px},{yc:.2f} Z", "none", 0, fill=COM, extra=f'fill-opacity="{TINT + 0.08}"'))
    o.append(path(f"M{px},{yc + R:.2f} L{px + w},{yc + R:.2f} L{px},{yc:.2f} Z", "none", 0, fill=TEN, extra=f'fill-opacity="{TINT + 0.08}"'))
    o.append(H.line(s, px - w, yc - R, px + w, yc + R, I["primary"], "geom"))
    o.append(H.line(s, px, yc - R - 8, px, yc + R + 8, I["axis"], "axis"))
    o.append(H.label(s, px - w, yc - R - 10, f'−{it("Mc")}/{it("I")}: compression', "label2", I["primary"], "middle"))
    o.append(H.label(s, px + w - 10, yc + R + 22, f'+{it("Mc")}/{it("I")}: tension', "label2", I["primary"], "middle"))
    o.append(H.label(s, px + 8, yc - 8, f'{it("σ")} = {it("My")}/{it("I")}', "label2", I["primary"]))
    o.append(H.label(s, px + 8, yc - r - 12, "half the peak", "label2", I["secondary"]))
    o.append(H.label(s, px + 8, yc - r + 4, f'at |{it("y")}| = {it("r")}', "label2", I["secondary"]))
    o.append(H.label(s, px - 8, yc + 18, "zero on the axis", "label2", I["secondary"], "end"))
    o.append(H.label(s, 210, 228, f'the bore disc (radius {it("r")}) holds {lostA * 100:.0f} % of the full disc’s area',
                     "label2", I["primary"], "middle"))
    o.append(H.label(s, 210, 244, f'but only {lostI * 100:.2f} % of its {it("I")}', "label2", I["primary"], "middle"))
    lg, _ = legend(s, 20, 268, [(sw_rect(BONE, BONE_L), "cortex"), (sw_rect(MARROW, BONE_L), "canal"),
                                (sw_tint(COM), "compression"), (sw_tint(TEN), "tension")])
    o.append(lg)
    aria = ("Problem C2 setup: the femoral section, cortex around a medullary canal with R over r = 2, its neutral axis "
            "dashed through the centre and y measured toward the tension face. Beside it the bending stress sigma = M "
            "y / I varies linearly: minus M c over I (compression, blue) at the top fibre, zero on the axis, plus M c "
            "over I (tension, red) at the bottom fibre, and half the peak at y = r. The bore disc of radius r holds 25 "
            "percent of the full disc's area but only 6.25 percent of its second moment of area I.")
    return finish(VB, aria, s, o)


# ================================================================ svg #14 (C3): a bent beam cracks on its tension face
def fig14():
    p = "m2f14_"
    VB = (0, 0, 440, 292)
    s = H.Scale(VB[2], VB[3], display_w=400)
    frac = SIG_T / SIG_C                                 # compression face, in units of its limit, at tensile failure
    assert abs(frac - 0.765) < 0.001
    xa, xb, yb, hd, vmax = 74.0, 366.0, 118.0, 34.0, 18.0
    Lb = xb - xa
    xs = np.linspace(xa - 14, xb + 14, 50)

    def v(x):                                            # central-load deflection shape (Euler-Bernoulli), drawn at vmax
        u = np.clip((x - xa) / Lb, 0, 1)
        u = np.where(u > 0.5, 1 - u, u)
        return vmax * u * (3 - 4 * u * u)
    vv = v(xs)
    top = [(x, yb - hd / 2 + d) for x, d in zip(xs, vv)]
    neu = [(x, yb + d) for x, d in zip(xs, vv)]
    bot = [(x, yb + hd / 2 + d) for x, d in zip(xs, vv)]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(path(dpath(top + neu[::-1], True), "none", 0, fill=COM, extra=f'fill-opacity="{TINT}"'))
    o.append(path(dpath(neu + bot[::-1], True), "none", 0, fill=TEN, extra=f'fill-opacity="{TINT}"'))
    o.append(path(dpath(top + bot[::-1], True), BONE_L, s(1.2)))
    o.append(path(dpath(top), COM, s(2.0)))
    o.append(path(dpath(bot), TEN, s(2.0)))
    xm = (xa + xb) / 2
    ybot = yb + hd / 2 + vmax
    # supports (pin, roller) and their reactions
    for x, roller in ((xa, False), (xb, True)):
        yt = yb + hd / 2 + float(v(np.array([x]))[0])
        o.append(path(f"M{x:.1f},{yt:.1f} L{x - 10:.1f},{yt + 16:.1f} L{x + 10:.1f},{yt + 16:.1f} Z", I["axis"], s(1.2), fill=BOX))
        if roller:
            o.append(circ(x - 5, yt + 20, 3.5, BOX, I["axis"], s(1.0)) + circ(x + 5, yt + 20, 3.5, BOX, I["axis"], s(1.0)))
        yh = yt + (24 if roller else 17)
        o.append(hatch(s, x - 16, x + 16, yh, 5))
        o.append(H.arrow(s, p, x, yh + 52, x, yh + 12, "reaction"))
        o.append(H.label(s, x + (-8 if x < xm else 8), yh + 44, f'{it("P")}/2', "label2", I["primary"], "end" if x < xm else "start"))
    o.append(H.arrow(s, p, xm, 26, xm, yb - hd / 2 + vmax - 3, "load"))
    o.append(H.label(s, xm + 9, 40, f'load {it("P")} (fall)', "label2", O["load"]))
    o.append(H.label(s, xa - 12, yb - hd / 2 - 12, f'compression face: limit ≈ {SIG_C:.0f} MPa', "label2", I["primary"]))
    # crack: starts on the tension face at midspan
    cr = [(xm, ybot), (xm - 3, ybot - 5), (xm + 2, ybot - 9), (xm - 2, ybot - 13), (xm + 1, ybot - 17)]
    o.append(path(dpath(cr), I["primary"], s(2.2), extra='stroke-linejoin="round"'))
    o.append(H.label(s, xm, ybot + 24, f'tension face: limit ≈ {SIG_T:.0f} MPa,', "label2", I["primary"], "middle"))
    o.append(H.label(s, xm, ybot + 40, "reached first: the crack starts here", "label2", I["primary"], "middle"))
    o.append(H.label(s, 220, 236, f'Both faces carry the same |{it("σ")}|{H.sub("max", s, "label2")}. At tensile failure the compression',
                     "label2", I["secondary"], "middle"))
    o.append(H.label(s, 220, 252, f'face is at {SIG_T:.0f}/{SIG_C:.0f} = {frac * 100:.0f} % of its limit. Deflection exaggerated.',
                     "label2", I["secondary"], "middle"))
    lg, _ = legend(s, 46, 282, [(sw_tint(COM), "compression"), (sw_tint(TEN), "tension"), (sw_line(O["load"]), "load"),
                                (sw_line(O["reaction"]), "support reaction")], gap=12)
    o.append(lg)
    aria = ("Problem C3 setup: a bone beam on two supports, bent by a central load P from a fall (brown); each support "
            "pushes up with P over 2 (black). The deflection is drawn exaggerated. The top face is in compression "
            "(blue), limit about 170 MPa; the bottom face is in tension (red), limit about 130 MPa. Both faces carry "
            "the same peak stress magnitude, so the tension face reaches its lower limit first and a crack starts on "
            f"it at midspan. At that moment the compression face is at 130/170 = {frac * 100:.0f} percent of its limit.")
    return finish(VB, aria, s, o)


# ================================================================ svg #16 (C5): stress trajectories past a screw hole
def kirsch(x, y):
    """Plane stress round a circular hole of radius 1 in a wide plate under unit tension along x (Kirsch)."""
    r2 = x * x + y * y
    th = math.atan2(y, x)
    c2, c4, s2, s4 = math.cos(2 * th), math.cos(4 * th), math.sin(2 * th), math.sin(4 * th)
    a2, a4 = 1 / r2, 1 / (r2 * r2)
    sxx = 1 - a2 * (1.5 * c2 + c4) + 1.5 * a4 * c4
    syy = -a2 * (0.5 * c2 - c4) - 1.5 * a4 * c4
    sxy = -a2 * (0.5 * s2 + s4) + 1.5 * a4 * s4
    return sxx, syy, sxy


def trajectory(y0, xl, xr, step=0.02):
    """Integrate one principal-tension trajectory from (xl, y0) to x = xr (hole radius 1)."""
    x, y, d = xl, y0, (1.0, 0.0)
    pts = [(x, y)]
    while x < xr:
        def dirn(px, py, prev):
            sxx, syy, sxy = kirsch(px, py)
            ph = 0.5 * math.atan2(2 * sxy, sxx - syy)
            v = (math.cos(ph), math.sin(ph))
            return v if v[0] * prev[0] + v[1] * prev[1] >= 0 else (-v[0], -v[1])
        k1 = dirn(x, y, d)
        k2 = dirn(x + 0.5 * step * k1[0], y + 0.5 * step * k1[1], k1)
        x, y, d = x + step * k2[0], y + step * k2[1], k2
        rr = math.hypot(x, y)
        if rr < 1.04:                                   # keep a line that meets the hole on its rim
            x, y = x * 1.04 / rr, y * 1.04 / rr
        pts.append((x, y))
    return pts


def thin(pts, d):
    """Keep a point only when it is at least d from the last kept one (and always the last point)."""
    out = [pts[0]]
    for q in pts[1:-1]:
        if math.hypot(q[0] - out[-1][0], q[1] - out[-1][1]) >= d:
            out.append(q)
    return out + [pts[-1]]


def fig16():
    p = "m2f16_"
    VB = (0, 0, 440, 280)
    s = H.Scale(VB[2], VB[3], display_w=400)
    assert abs(SIG_LOC / SIG_NOM - 2.5) < 1e-9 and KT_LO <= SIG_LOC / SIG_NOM <= KT_HI
    xl, xr, yt, yb = 52.0, 388.0, 70.0, 190.0
    hx, hy, a = (xl + xr) / 2, (yt + yb) / 2, 17.0
    o = [f'<defs>{H.markers(p, s)}</defs>', rect(xl, yt, xr - xl, yb - yt, BONE, BONE_L, s(1.2), 2)]
    half = (yb - yt) / 2
    nl = 10
    for k in range(nl):
        y0 = -half + (k + 0.5) * (2 * half / nl)
        tr = trajectory(y0 / a, (xl - hx) / a, (xr - hx) / a)
        pts = thin([(hx + a * u, hy + a * v) for u, v in tr], 4.0)
        pts = [(x, min(max(y, yt + 1.5), yb - 1.5)) for x, y in pts]
        o.append(path(dpath(pts), O["force"], s(1.1), extra='stroke-opacity="0.85"'))
    o.append(circ(hx, hy, a, "#fff", I["axis"], s(1.3)))
    for sgn in (-1, 1):
        x0 = xl if sgn < 0 else xr
        for yy in (yt + 22, hy, yb - 22):
            o.append(H.arrow(s, p, x0 + sgn * 3, yy, x0 + sgn * 34, yy, "load"))
    o.append(H.label(s, 14, yt - 10, f'{it("σ")}{H.sub("nom", s, "label2")} = {SIG_NOM:.0f} MPa', "label2", O["load"]))
    for sgn in (-1, 1):
        o.append(f'<circle cx="{hx:.2f}" cy="{hy + sgn * a:.2f}" r="{s(3.6):.2f}" fill="{O["flag"]}" stroke="#fff" stroke-width="{s(1.2):.2f}"/>')
    o.append(H.line(s, hx, hy - a - 4, hx + 22, 54, I["secondary"], "leader"))
    o.append(H.label(s, hx + 44, 24, f'hot spots: {it("σ")}{H.sub("local", s, "label2")} = {it("K")}{H.sub("t", s, "label2")}'
                     f'{it("σ")}{H.sub("nom", s, "label2")}', "label2", I["primary"]))
    o.append(H.label(s, hx + 44, 44, f'≈ {SIG_LOC:.0f} MPa ({it("K")}{H.sub("t", s, "label2")} ≈ {KT_LO:.0f}–{KT_HI:.0f})', "label2", I["primary"]))
    o.append(H.line(s, hx - a * 0.72, hy + a * 0.72, hx - 52, yb + 14, I["secondary"], "leader"))
    o.append(H.label(s, hx - 54, yb + 24, "healed screw hole", "label2", I["primary"], "end"))
    o.append(H.label(s, hx + 70, yb + 24, "trajectories crowd at the flanks", "label2", I["primary"], "middle"))
    o.append(H.label(s, hx + 70, yb + 40, "(elastic solution, hole in a wide plate)", "label2", I["muted"], "middle"))
    lg, _ = legend(s, 22, 268, [(sw_rect(BONE, BONE_L), "cortex"), (sw_line(O["force"], 1.4), "tension trajectories"),
                                (sw_line(O["load"]), "load"), (sw_rect(O["flag"]), "hot spot")], gap=10)
    o.append(lg)
    aria = ("Problem C5 setup: a strip of cortex with a healed screw hole, pulled at both ends by a nominal stress of 40 "
            "MPa (brown arrows). Red principal-tension trajectories, computed from the elastic solution for a hole in a "
            "wide plate, run evenly far from the hole and crowd at its two flanks. Orange dots mark the hot spots on the "
            "flanks, where the local stress is K t times sigma nom, about 100 MPa, with K t about 2 to 3 for a circular hole.")
    return finish(VB, aria, s, o)


# ================================================================ svg #19 (C8): mineral platelets, a deflected and bridged crack
def fig19():
    p = "m2f19_"
    VB = (0, 0, 440, 300)
    s = H.Scale(VB[2], VB[3], display_w=400)
    xl, xr, yt, yb = 48.0, 392.0, 40.0, 178.0
    o = [f'<defs>{H.markers(p, s)}</defs>', rect(xl, yt, xr - xl, yb - yt, T["tendon"][0], T["tendon"][1], s(1.0), 4)]
    # collagen fibrils run along the load axis (x); platelets sit staggered between them
    rows, pl, th, gap = 6, 80.0, 10.0, 12.0
    pitch = (yb - yt) / rows
    for k in range(1, rows):
        y = yt + k * pitch
        o.append(H.line(s, xl, y, xr, y, T["tendon"][1], "leader", extra='stroke-opacity="0.8"'))
    plates = []
    for k in range(rows):
        y = yt + (k + 0.5) * pitch - th / 2
        off = 0 if k % 2 == 0 else (pl + gap) / 2
        x = xl + 6 - off
        while x < xr - 6:
            x0, x1 = max(x, xl + 3), min(x + pl, xr - 3)
            if x1 - x0 > 14:
                plates.append((x0, y, x1, k))
                o.append(rect(x0, y, x1 - x0, th, T["bone_shade"][0], T["bone"][1], s(1.0), 2))
            x += pl + gap
    # crack from the top edge: straight down through matrix, deflected along each platelet it meets
    x = 222.0
    cr = [(x, yt)]
    defl = None
    for k in range(rows - 1):
        ytop = yt + (k + 0.5) * pitch - th / 2
        hit = [q for q in plates if q[3] == k and q[0] - 2 <= x <= q[2] + 2]
        if hit:
            q = hit[0]
            nx = q[2] + 3 if (q[2] - x) < (x - q[0]) else q[0] - 3
            cr += [(x, ytop - 1.5), (nx, ytop - 1.5)]
            if defl is None and k > 0:
                defl = ((x + nx) / 2, ytop - 1.5)
            x = nx
        cr.append((x, yt + (k + 1) * pitch + 3))
    tip = cr[-1]
    o.append(path(dpath(cr), I["primary"], s(2.2), extra='stroke-linejoin="round"'))
    # bridges: intact fibrils spanning the crack on its vertical runs
    bridges = []
    for (x1, y1), (x2, y2) in zip(cr, cr[1:]):
        if abs(x1 - x2) < 0.1 and y2 - y1 > 10:
            for kk in range(1, rows):
                yy = yt + kk * pitch
                if y1 + 2 < yy < y2 - 2:
                    bridges.append((x1, yy))
    for bx, by in bridges:
        o.append(H.line(s, bx - 8, by, bx + 8, by, T["tendon"][1], "geom"))
    ym = (yt + yb) / 2
    o.append(H.arrow(s, p, xl - 2, ym, xl - 34, ym, "load"))
    o.append(H.arrow(s, p, xr + 2, ym, xr + 34, ym, "load"))
    o.append(H.label(s, xl - 18, ym - 10, it("σ"), "label", O["load"], "middle"))
    o.append(H.label(s, xr + 18, ym - 10, it("σ"), "label", O["load"], "middle"))
    o.append(H.label(s, cr[0][0], yt - 8, "crack", "label2", I["primary"], "middle"))
    dx, dy = defl
    o.append(H.line(s, dx, dy + 1, 120, yb + 14, I["secondary"], "leader"))
    o.append(H.label(s, 18, yb + 26, "deflected along a", "label2", I["primary"]))
    o.append(H.label(s, 18, yb + 42, "mineral–collagen interface", "label2", I["primary"]))
    bx, by = bridges[-1]
    o.append(H.line(s, bx + 8, by, 330, yb + 14, I["secondary"], "leader"))
    o.append(H.label(s, 422, yb + 26, "collagen fibrils bridge", "label2", I["primary"], "end"))
    o.append(H.label(s, 422, yb + 42, "it and shield the tip", "label2", I["primary"], "end"))
    o.append(H.label(s, 220, yb + 68, f'about {V_M * 100:.0f} % mineral by volume', "label2", I["secondary"], "middle"))
    for j, (sw, txt) in enumerate(((sw_rect(T["bone_shade"][0], T["bone"][1]), f'apatite platelet: stiff, brittle, {it("E")} ≈ {E_M:.0f} GPa'),
                                   (sw_rect(T["tendon"][0], T["tendon"][1]), f'collagen: compliant, tough, {it("E")} ≈ {E_C:.0f} GPa'))):
        o.append(legend(s, 90, 272 + j * 20, [(sw, txt)])[0])
    aria = ("Problem C8 setup: bone's nanostructure as staggered stiff hydroxyapatite platelets (about 100 GPa, brittle) "
            "between collagen fibrils (about 1 GPa, compliant and tough) that run along the load axis, pulled by a "
            "stress sigma at both ends (brown). A crack enters from the top and is deflected sideways along each "
            "mineral-collagen interface it meets; intact collagen fibrils bridge its vertical runs and shield the tip. "
            "About 50 percent mineral by volume.")
    return finish(VB, aria, s, o)


# ================================================================ svg #22 (D1): the strip dA = b dy
def fig22():
    p = "m2f22_"
    VB = (0, 0, 420, 240)
    s = H.Scale(VB[2], VB[3], display_w=400)
    xl, w, yt, hh = 76.0, 92.0, 34.0, 152.0
    yc = yt + hh / 2
    ys, dyv = yc + 44, 9.0
    o = [f'<defs>{H.markers(p, s)}</defs>', rect(xl, yt, w, hh, BONE, BONE_L, s(1.4))]
    o.append(rect(xl, ys - dyv / 2, w, dyv, O["flag"], None, 0, 0, 'fill-opacity="0.55"'))
    o.append(H.line(s, xl - 14, yc, xl + w + 14, yc, I["primary"], "ref", H.DASH_REF))
    o.append(H.label(s, xl + w + 18, yc + 4, "N.A.", "label2", I["secondary"]))
    o.append(H.label(s, xl + w + 18, yc + 20, "(centroid)", "label2", I["secondary"]))
    o.append(H.arrow(s, p, xl + 30, yc, xl + 30, ys - dyv / 2, "geometry"))
    o.append(H.label(s, xl + 36, yc + 28, it("y"), "label", O["geometry"]))
    o.append(tick(s, xl + w + 2, ys - dyv / 2, xl + w + 22, ys - dyv / 2) + tick(s, xl + w + 2, ys + dyv / 2, xl + w + 22, ys + dyv / 2))
    o.append(H.arrow(s, p, xl + w + 16, ys - dyv / 2 - 14, xl + w + 16, ys - dyv / 2, "geometry"))
    o.append(H.arrow(s, p, xl + w + 16, ys + dyv / 2 + 14, xl + w + 16, ys + dyv / 2, "geometry"))
    o.append(H.label(s, xl + w + 26, ys + 5, f'{it("dy")}', "label2", O["geometry"]))
    o.append(H.label(s, xl + w / 2, ys + dyv / 2 + 18, f'strip {it("dA")}', "label2", I["primary"], "middle"))
    yd = yt + hh + 16
    o.append(tick(s, xl, yt + hh + 4, xl, yd + 6) + tick(s, xl + w, yt + hh + 4, xl + w, yd + 6))
    o.append(dim(s, p, xl, yd, xl + w, yd))
    o.append(H.label(s, xl + w / 2, yd + 20, it("b"), "label", O["geometry"], "middle"))
    xd = xl - 22
    o.append(tick(s, xl - 4, yt, xd - 6, yt) + tick(s, xl - 4, yt + hh, xd - 6, yt + hh))
    o.append(dim(s, p, xd, yt, xd, yt + hh))
    o.append(H.label(s, xd - 6, yc + 5, f'{it("h")}{H.sub("sec", s)}', "label", O["geometry"], "end"))
    tx = 290
    o.append(H.label(s, tx, 80, f'{it("dA")} = {it("b")} {it("dy")}', "label", I["primary"]))
    o.append(H.label(s, tx, 110, f'{it("I")} = ∫ {it("y")}² {it("dA")}', "label", I["primary"]))
    o.append(H.label(s, tx, 140, f'= {it("b h")}{H.sub("sec", s)}³ / 12', "label", I["primary"]))
    o.append(H.label(s, tx, 170, f'{it("c")} = {it("h")}{H.sub("sec", s, "label2")} / 2', "label2", I["secondary"]))
    lg, _ = legend(s, 290, 230, [(sw_rect(O["flag"], None, 0.55), "strip element")], gap=8)
    o.append(lg)
    aria = ("Problem D1 setup: a rectangular cross-section of width b and height h sec, with its neutral axis dashed "
            "through the centroid. An orange horizontal strip of thickness dy at distance y from the axis has area dA "
            "= b dy. Integrating I = integral of y squared dA gives b h sec cubed over 12; the outer fibre is at c = "
            "h sec over 2.")
    return finish(VB, aria, s, o)


# ================================================================ svg #24 (D3): the annular ring dA = 2 pi rho d rho
def fig24():
    p = "m2f24_"
    VB = (0, 0, 420, 232)
    s = H.Scale(VB[2], VB[3], display_w=400)
    _, _, Jv = section_numbers()
    Iv = Jv / 2
    R, r, cx, cy = 78.0, 39.0, 104.0, 112.0
    rho, drho = 58.0, 9.0
    o = [f'<defs>{H.markers(p, s)}</defs>', tube(s, cx, cy, R, r)]
    o.append(ann(cx, cy, rho + drho / 2, rho - drho / 2, O["flag"], "none", 0).replace('fill="', 'fill-opacity="0.55" fill="', 1))
    a1 = math.radians(-50)
    o.append(H.arrow(s, p, cx, cy, cx + (rho - drho / 2) * math.cos(a1), cy + (rho - drho / 2) * math.sin(a1), "geometry"))
    o.append(H.label(s, cx + 30 * math.cos(a1) + 8, cy + 30 * math.sin(a1) - 2, it("ρ"), "label", O["geometry"]))
    o.append(H.arrow(s, p, cx, cy, cx - R, cy, "geometry"))
    o.append(H.label(s, cx - R / 2 - 4, cy - 6, it("R"), "label", O["geometry"], "middle"))
    a2 = math.radians(120)
    o.append(H.arrow(s, p, cx, cy, cx + r * math.cos(a2), cy + r * math.sin(a2), "geometry"))
    o.append(H.label(s, cx + 22 * math.cos(a2) - 9, cy + 22 * math.sin(a2) + 4, it("r"), "label", O["geometry"], "end"))
    # d rho: across the ring at angle 0, outside the circle with a leader
    o.append(H.arrow(s, p, cx + rho - drho / 2 - 12, cy, cx + rho - drho / 2, cy, "geometry"))
    o.append(H.arrow(s, p, cx + rho + drho / 2 + 12, cy, cx + rho + drho / 2, cy, "geometry"))
    o.append(H.line(s, cx + rho + drho / 2 + 12, cy, cx + R + 14, cy + 22, I["secondary"], "leader"))
    o.append(H.label(s, cx + R + 16, cy + 30, f'ring width {it("dρ")}', "label2", O["geometry"]))
    tx = 228
    o.append(H.label(s, tx, 30, f'{it("dA")} = 2π{it("ρ")} {it("dρ")}', "label", I["primary"]))
    o.append(H.label(s, tx, 58, f'{it("J")} = ∫ {it("ρ")}² {it("dA")} = (π/2)({it("R")}⁴ − {it("r")}⁴)', "label2", I["primary"]))
    o.append(H.label(s, tx, 82, f'{it("I")} = {it("J")}/2 = (π/4)({it("R")}⁴ − {it("r")}⁴)', "label2", I["primary"]))
    o.append(H.label(s, tx, 178, f'femur, {it("R")} = {R_MM:.0f} mm, {it("r")} = {r_MM:.0f} mm:', "label2", I["secondary"]))
    o.append(H.label(s, tx, 196, f'{it("J")} = {sci(Jv)} m⁴', "label2", I["secondary"]))
    o.append(H.label(s, tx, 214, f'{it("I")} = {sci(Iv)} m⁴', "label2", I["secondary"]))
    lg, _ = legend(s, 20, 224, [(sw_rect(O["flag"], None, 0.55), "ring element")], gap=8)
    o.append(lg)
    aria = ("Problem D3 setup: the hollow femoral section, outer radius R, inner r, with an orange thin ring of radius "
            "rho and width d rho, area dA = 2 pi rho d rho. Integrating J = integral of rho squared dA from r to R "
            "gives pi over 2 times (R to the 4 minus r to the 4), and I = J over 2. For the femur, R = 14 mm, r = 7 mm: "
            f"J = {sci(Jv)} m4, I = {sci(Iv)} m4.")
    return finish(VB, aria, s, o)


# ================================================================ svg #25 (D4): tube vs equal-area rod, ratio vs bore
def fig25():
    p = "m2f25_"
    VB = (0, 0, 480, 290)
    s = H.Scale(VB[2], VB[3], display_w=400)
    beta = 0.5
    q = ratio(beta)
    a_rel = math.sqrt(1 - beta ** 2)
    assert abs(q - 1.443) < 0.0005
    R, cx, cy = 68.0, 118.0, 104.0
    o = [f'<defs>{H.markers(p, s)}</defs>', tube(s, cx, cy, R, R * beta)]
    o.append(circ(cx, cy, R * a_rel, "none", I["primary"], s(1.6), f'stroke-dasharray="{s(6):.1f} {s(4):.1f}"'))
    o.append(H.arrow(s, p, cx, cy, cx, cy - R, "geometry"))
    o.append(H.label(s, cx + 5, cy - R + 18, it("R"), "label", O["geometry"]))
    a3 = math.radians(150)
    o.append(H.arrow(s, p, cx, cy, cx + R * beta * math.cos(a3), cy + R * beta * math.sin(a3), "geometry"))
    o.append(H.label(s, cx - 30, cy + 34, f'{it("r")} = {it("βR")}', "label2", O["geometry"], "end"))
    o.append(H.label(s, cx, cy + R + 20, "dashed: equal-area rod", "label2", I["primary"], "middle"))
    o.append(H.label(s, cx, cy + R + 37, f'{it("a")} = {a_rel:.2f} {it("R")}', "label2", I["primary"], "middle"))
    o.append(H.label(s, cx, cy + R + 54, f'π{it("a")}² = π({it("R")}² − {it("r")}²)', "label2", I["secondary"], "middle"))
    # ratio vs bore: (1 + b^2) / sqrt(1 - b^2)
    ax = Ax((288, 30, 466, 206), (0, 0.9), (1, 4.5))
    o += axes(s, ax, [(0, "0"), (0.3, "0.3"), (0.6, "0.6"), (0.9, "0.9")], [(1, "1"), (2, "2"), (3, "3"), (4, "4")],
              f'bore ratio {it("β")} = {it("r")}/{it("R")}', f'{it("Z")}{H.sub("hollow", s, "label2")} / {it("Z")}{H.sub("solid", s, "label2")}',
              xlab_dy=40, ylab_x=256)
    o.append(H.label(s, ax.X(0.02), ax.top + 6, f'(1 + {it("β")}²)/√(1 − {it("β")}²)', "label2", I["primary"]))
    bs = np.linspace(0, 0.9, 91)
    qs = [ratio(b) for b in bs]
    o.append(curve(s, ax, bs, qs, SER[0]))
    o.append(dot(s, ax.X(beta), ax.Y(q), SER[0]))
    o.append(H.line(s, ax.X(beta), ax.Y(q), ax.X(beta), ax.y0, O["dim"], "leader", H.DASH_REF))
    o.append(H.label(s, ax.X(beta) - 6, ax.Y(q) - 12, f'{it("β")} = ½: {q:.3f}', "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(0.9) - 12, ax.Y(ratio(0.9)) + 12, f'→ ∞ as {it("β")} → 1', "label2", I["secondary"], "end"))
    hv = [[ax.X(b), ax.Y(v), f"β = {b:.3f}: Z ratio {v:.3f}"] for b, v in zip(bs, qs)]
    lg, _ = legend(s, 16, 282, [(sw_rect(BONE, BONE_L), "cortex"), (sw_rect(MARROW, BONE_L), "canal"),
                                (sw_line(I["primary"], 1.6, "6 4"), "equal-area rod"), (sw_line(SER[0]), "Z ratio")], gap=12)
    o.append(lg)
    aria = ("Problem D4 setup. Left: a hollow tube, cortex of outer radius R around a canal of radius r = beta R with "
            f"beta = one half, and the dashed outline of a solid rod of the same area, radius a = {a_rel:.2f} R (pi a "
            "squared = pi (R squared minus r squared)). Right, red curve: the section-modulus ratio Z hollow over Z solid "
            "= (1 + beta squared) over the square root of (1 minus beta squared), for beta from 0 to 0.9; it is "
            f"{q:.3f} at beta = one half and grows without bound as beta tends to 1.")
    return finish(VB, aria, s, o, extra=H.hover_attr(ax.box, hv))


# ================================================================ svg #26 (D5): end moments bend the beam into an arc
def fig26():
    p = "m2f26_"
    VB = (0, 0, 420, 262)
    s = H.Scale(VB[2], VB[3], display_w=400)
    cx, cy, Rk, c, ph = 210.0, 214.0, 160.0, 11.0, math.radians(42)
    up = lambda rad, a0, a1, n=60: [(cx + rad * math.sin(t), cy - rad * math.cos(t)) for t in np.linspace(a0, a1, n)]  # noqa: E731
    outer, neu, inner = up(Rk + c, -ph, ph), up(Rk, -ph, ph), up(Rk - c, -ph, ph)
    o = [f'<defs>{H.markers(p, s)}</defs>', path(dpath(outer + inner[::-1], True), BONE_L, s(1.2), fill=BONE)]
    o.append(path(dpath(neu), I["primary"], s(1.0), extra=f'stroke-dasharray="{s(6):.1f} {s(4):.1f}"'))
    o.append(H.line(s, cx, cy, cx, cy - Rk, O["dim"], "ref", H.DASH_REF))
    o.append(circ(cx, cy, s(3), I["primary"]))
    o.append(H.label(s, cx + 8, cy - Rk / 2, f'{it("R")}{H.sub("κ", s)} = 1/{it("κ")}', "label", I["primary"]))
    o.append(H.label(s, cx + 8, cy + 4, "centre of curvature", "label2", I["secondary"]))
    for sgn in (-1, 1):
        ex, ey = neu[0] if sgn < 0 else neu[-1]
        # hogging: left end counter-clockwise, right end clockwise (screen)
        out = math.degrees(math.atan2(math.sin(ph), -math.cos(ph))) if sgn < 0 else math.degrees(math.atan2(math.sin(ph), math.cos(ph)))
        a0, a1 = (out + 65, out - 65) if sgn < 0 else (out - 65, out + 65)
        o.append(moment_arc(s, p, ex, ey, 28, a0, a1))
        o.append(H.label(s, ex + sgn * 44, ey + 36, it("M"), "label", O["load"], "middle"))
    o.append(H.label(s, 210, 22, f'{it("κ")} = {it("M")}/({it("EI")})', "label", I["primary"], "middle"))
    o.append(H.label(s, 210, 40, f'bending stiffness {it("EI")}; scale every length by {it("λ")}: {it("EI")} ∝ {it("λ")}⁴',
                     "label2", I["secondary"], "middle"))
    lg, _ = legend(s, 60, 254, [(sw_rect(BONE, BONE_L), "beam"), (sw_line(I["primary"], 1.0, "6 4"), "neutral axis"),
                                (sw_line(O["load"]), "end moment M")], gap=12)
    o.append(lg)
    aria = ("Problem D5 setup: a beam bent by equal and opposite end moments M (brown) into a circular arc. A dashed "
            "radius runs from the centre of curvature to the neutral axis: R kappa = 1 over kappa. Above: kappa = M "
            "over EI, with EI the bending stiffness, which scales as lambda to the 4 when every length is scaled by lambda.")
    return finish(VB, aria, s, o)


# ================================================================ svg #28 (D7): pure shear, the wedge and its force triangle
def fig28():
    p = "m2f28_"
    VB = (0, 0, 470, 262)
    s = H.Scale(VB[2], VB[3], display_w=400)
    a = 84.0
    cols = (78.0, 238.0, 392.0)                          # column centres for the text rows
    # ---- element in pure shear
    x0, y0 = cols[0] - a / 2, 50.0
    o = [f'<defs>{H.markers(p, s)}</defs>', rect(x0, y0, a, a, BONE, BONE_L, s(1.4))]
    g = 9.0
    o.append(H.arrow(s, p, x0 + 12, y0 - g, x0 + a - 12, y0 - g, "dim", w="geom"))
    o.append(H.arrow(s, p, x0 + a - 12, y0 + a + g, x0 + 12, y0 + a + g, "dim", w="geom"))
    o.append(H.arrow(s, p, x0 - g, y0 + 12, x0 - g, y0 + a - 12, "dim", w="geom"))
    o.append(H.arrow(s, p, x0 + a + g, y0 + a - 12, x0 + a + g, y0 + 12, "dim", w="geom"))
    o.append(H.label(s, x0 + a / 2, y0 - g - 8, it("τ"), "label", I["primary"], "middle"))
    o.append(H.label(s, x0 + a + g + 8, y0 + a / 2 + 5, it("τ"), "label", I["primary"]))
    o.append(H.line(s, x0, y0, x0 + a, y0 + a, I["primary"], "ref", H.DASH_REF))
    # ---- the lower-left wedge: faces a, a; diagonal a sqrt 2
    wx, wy = cols[1] - a / 2 - 12, y0
    o.append(path(f"M{wx},{wy} L{wx},{wy + a} L{wx + a},{wy + a} Z", BONE_L, s(1.4), fill=BONE))
    o.append(H.arrow(s, p, wx - g, wy + 12, wx - g, wy + a - 12, "dim", w="geom"))
    o.append(H.arrow(s, p, wx + a - 12, wy + a + g, wx + 12, wy + a + g, "dim", w="geom"))
    o.append(H.label(s, wx - g - 6, wy + a / 2 + 5, f'{it("τa")}', "label2", I["primary"], "end"))
    o.append(H.label(s, wx + a / 2, wy + a + g + 18, f'{it("τa")}', "label2", I["primary"], "middle"))
    mx, my = wx + a / 2, wy + a / 2
    u = 1 / math.sqrt(2)
    o.append(H.arrow(s, p, mx + 3 * u, my - 3 * u, mx + 46 * u, my - 46 * u, "force"))
    o.append(H.label(s, mx + 40 * u + 6, my - 46 * u - 4, f'{it("τa")}√2', "label2", O["force"]))
    o.append(H.label(s, wx + 5, wy + a * 0.6, it("a"), "label2", O["geometry"]))
    o.append(H.label(s, wx + a * 0.36, wy + a - 7, it("a"), "label2", O["geometry"], "middle"))
    o.append(H.label(s, wx + 0.75 * a + 9, wy + 0.75 * a - 1, f'{it("a")}√2', "label2", O["geometry"]))
    # ---- force triangle: the two face forces, head to tail, close with tau a sqrt 2
    L = 52.0
    tx, ty = cols[2] + L / 2, y0 + 10
    o.append(H.arrow(s, p, tx, ty, tx, ty + L, "dim", w="geom"))
    o.append(H.arrow(s, p, tx, ty + L, tx - L, ty + L, "dim", w="geom"))
    o.append(H.line(s, tx, ty, tx - L, ty + L, I["primary"], "ref", H.DASH_REF))
    o.append(H.label(s, tx + 6, ty + L / 2 + 4, f'{it("τa")}', "label2", I["primary"]))
    o.append(H.label(s, tx - L / 2, ty + L + 18, f'{it("τa")}', "label2", I["primary"], "middle"))
    o.append(H.label(s, tx - L / 2 - 8, ty + L / 2 - 6, f'{it("τa")}√2', "label2", I["primary"], "end"))
    # ---- text rows, one column per panel
    r1, r2 = 186.0, 202.0
    for (t1, t2), x in zip(((("pure shear", "45° cut dashed")),
                            (f'{it("σ")} = {it("τa")}√2 / ({it("a")}√2) = +{it("τ")}', "tension, no shear"),
                            ("face forces add:", "sum ⟂ the cut")), cols):
        o.append(H.label(s, x, r1, t1, "label2", I["primary"], "middle"))
        o.append(H.label(s, x, r2, t2, "label2", I["secondary"], "middle"))
    o.append(H.label(s, 235, 236, f'Cut the other diagonal: {it("σ")}₂ = −{it("τ")} (compression).', "label2", I["primary"], "middle"))
    lg, _ = legend(s, 53, 256, [(sw_rect(BONE, BONE_L), "bone element"), (sw_line(I["secondary"], 2.0), "shear τ"),
                         (sw_line(O["force"]), "normal stress: tension")], gap=12)
    o.append(lg)
    aria = ("Problem D7 setup, Lemma 4.2 in three parts. Left: a square bone element in pure shear tau (grey arrows), with the 45 "
            "degree cut dashed. Middle: the lower-left wedge, faces a and a, diagonal a root 2. The face forces tau a "
            "on the two short faces are balanced by a force tau a root 2 normal to the diagonal, so the diagonal carries "
            "a normal stress tau a root 2 over a root 2 = plus tau, tension (red arrow), and no shear. Right: the force triangle, "
            "tau a and tau a head to tail, closed by tau a root 2 perpendicular to the cut. Cutting the other diagonal "
            "gives sigma 2 = minus tau, compression.")
    return finish(VB, aria, s, o)


# ================================================================ svg #30 (D9): Voigt and Reuss
def fig30():
    p = "m2f30_"
    VB = (0, 0, 440, 270)
    s = H.Scale(VB[2], VB[3], display_w=400)
    EV = V_M * E_M + (1 - V_M) * E_C
    ER = 1 / (V_M / E_M + (1 - V_M) / E_C)
    assert abs(EV - 50.5) < 1e-9 and abs(ER - 1.98) < 0.005 and ER < E_BONE < EV
    MIN, COL = (T["bone_shade"][0], T["bone"][1]), (T["tendon"][0], T["tendon"][1])
    o = [f'<defs>{H.markers(p, s)}</defs>']
    L, hh, yc = 104.0, 56.0, 104.0
    # Voigt: layers parallel to the load, rigid end plates (equal strain)
    vx = 54.0
    o.append(rect(vx, yc - hh / 2, L, hh / 2, *MIN, s(1.0)))
    o.append(rect(vx, yc, L, hh / 2, *COL, s(1.0)))
    # Reuss: layers in series along the load (equal stress)
    rx = 278.0
    o.append(rect(rx, yc - hh / 2, L / 2, hh, *MIN, s(1.0)))
    o.append(rect(rx + L / 2, yc - hh / 2, L / 2, hh, *COL, s(1.0)))
    for x0 in (vx, rx):
        for xp in (x0 - 5, x0 + L):
            o.append(rect(xp, yc - hh / 2 - 6, 5, hh + 12, I["axis"]))
        o.append(H.arrow(s, p, x0 - 8, yc, x0 - 38, yc, "load"))
        o.append(H.arrow(s, p, x0 + L + 8, yc, x0 + L + 38, yc, "load"))
    o.append(H.label(s, vx + L / 2, 30, "Voigt: in parallel", "label", I["primary"], "middle"))
    o.append(H.label(s, vx + L / 2, 48, f'equal strain {it("ε")}', "label2", I["secondary"], "middle"))
    o.append(H.label(s, rx + L / 2, 30, "Reuss: in series", "label", I["primary"], "middle"))
    o.append(H.label(s, rx + L / 2, 48, f'equal stress {it("σ")}', "label2", I["secondary"], "middle"))
    vm = f'{it("v")}{H.sub("m", s, "label2")}'
    Em, Ec = f'{it("E")}{H.sub("m", s, "label2")}', f'{it("E")}{H.sub("c", s, "label2")}'
    o.append(H.label(s, vx + L / 2, yc + hh / 2 + 34, f'{it("E")}{H.sub("V", s, "label2")} = {vm}{Em} + (1 − {vm}){Ec}', "label2", I["primary"], "middle"))
    o.append(H.label(s, vx + L / 2, yc + hh / 2 + 54, f'= {EV:.1f} GPa', "label2", I["primary"], "middle"))
    o.append(H.label(s, rx + L / 2, yc + hh / 2 + 34, f'1/{it("E")}{H.sub("R", s, "label2")} = {vm}/{Em} + (1 − {vm})/{Ec}', "label2", I["primary"], "middle"))
    o.append(H.label(s, rx + L / 2, yc + hh / 2 + 54, f'{it("E")}{H.sub("R", s, "label2")} = {ER:.2f} GPa', "label2", I["primary"], "middle"))
    o.append(H.label(s, 220, 214, f'{it("E")}{H.sub("R", s)} = {ER:.2f} ≤ {it("E")} = {E_BONE:.0f} ≤ {it("E")}{H.sub("V", s)} = {EV:.1f} GPa',
                     "label", I["primary"], "middle"))
    o.append(H.label(s, 220, 234, f'{vm} = {V_M}, {Em} = {E_M:.0f} GPa, {Ec} = {E_C:.0f} GPa', "label2", I["secondary"], "middle"))
    lg, _ = legend(s, 40, 262, [(sw_rect(*MIN), "apatite"), (sw_rect(*COL), "collagen"),
                                (sw_rect(I["axis"]), "rigid end plate"), (sw_line(O["load"]), "load")], gap=12)
    o.append(lg)
    aria = ("Problem D9 setup. Left, Voigt: an apatite (mineral) layer and a collagen layer side by side, parallel to "
            "the load (brown), between rigid end plates, so both phases share one strain; E V = v m E m + (1 minus v m) "
            f"E c = {EV:.1f} GPa. Right, Reuss: the two phases in series along the load, so both carry one stress; 1 "
            f"over E R = v m over E m + (1 minus v m) over E c, E R = {ER:.2f} GPa. With v m = 0.5, E m = 100 GPa, E c "
            f"= 1 GPa the measured 17 GPa lies inside the bracket {ER:.2f} to {EV:.1f} GPa.")
    return finish(VB, aria, s, o)


# ================================================================ svg #31 (D10): a mass falls onto a soft spring
def spring(x, y_top, y_bot, w=13.0, n=7):
    lead = 6.0
    pts = [(x, y_top), (x, y_top + lead)]
    seg = (y_bot - y_top - 2 * lead) / n
    for i in range(n):
        pts.append((x + (w if i % 2 == 0 else -w), y_top + lead + (i + 0.5) * seg))
    pts += [(x, y_bot - lead), (x, y_bot)]
    return dpath(pts)


def fig31():
    p = "m2f31_"
    VB = (0, 0, 440, 316)
    s = H.Scale(VB[2], VB[3], display_w=400)
    Wt = M_EFF * G
    F = math.sqrt(2 * K_S * M_EFF * G * H_FALL)
    xc = F / K_S
    rat = F / Wt
    assert abs(F - 3.7e3) < 0.02e3 and abs(xc - 0.074) < 0.0005 and round(rat) == 13
    k = 270.0                                            # user units per metre: h and x to scale
    yg, Lfree, bw, bh = 282.0, 64.0, 62.0, 30.0
    ytop = yg - Lfree
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # ---- left: released at height h above the spring
    x1 = 90.0
    yb1 = ytop - H_FALL * k
    o.append(hatch(s, x1 - 44, x1 + 44, yg))
    o.append(path(spring(x1, ytop, yg), I["axis"], s(1.6), extra='stroke-linejoin="round"'))
    o.append(rect(x1 - bw / 2, yb1 - bh, bw, bh, BOX, I["axis"], s(1.3), 3))
    o.append(H.label(s, x1, yb1 - bh / 2 + 5, f'{it("m")}{H.sub("eff", s)}', "label", I["primary"], "middle"))
    xd = x1 + bw / 2 + 16
    o.append(tick(s, x1 + bw / 2 + 2, yb1, xd + 6, yb1) + tick(s, x1 + 18, ytop, xd + 6, ytop))
    o.append(dim(s, p, xd, yb1, xd, ytop))
    o.append(H.label(s, xd + 6, (yb1 + ytop) / 2 + 5, f'{it("h")} = {H_FALL} m', "label2", O["geometry"]))
    o.append(H.label(s, x1, yb1 - bh - 26, "released", "label2", I["primary"], "middle"))
    o.append(H.label(s, x1, yb1 - bh - 10, f'{it("m")}{H.sub("eff", s, "label2")} = {M_EFF:.0f} kg', "label2", I["secondary"], "middle"))
    o.append(H.label(s, x1 - 20, ytop + 34, f'{it("k")}{H.sub("s", s, "label2")}', "label2", I["primary"], "end"))
    # ---- right: peak compression x
    x2 = 262.0
    ycomp = ytop + xc * k
    o.append(hatch(s, x2 - 44, x2 + 44, yg))
    o.append(path(spring(x2, ycomp, yg), I["axis"], s(1.6), extra='stroke-linejoin="round"'))
    o.append(rect(x2 - bw / 2, ycomp - bh, bw, bh, BOX, I["axis"], s(1.3), 3))
    o.append(H.label(s, x2, ycomp - bh / 2 + 5, f'{it("m")}{H.sub("eff", s)}', "label", I["primary"], "middle"))
    o.append(H.line(s, 150, ytop, x2 - 14, ytop, O["dim"], "leader", H.DASH_REF))
    o.append(H.label(s, 150, ytop - 6, "rest level", "label2", I["muted"]))
    xx = x2 - 46
    o.append(dim(s, p, xx, ytop, xx, ycomp))
    o.append(H.label(s, xx - 6, ycomp + 18, f'{it("x")} = {xc:.3f} m', "label2", O["geometry"], "end"))
    # forces on the mass at that instant, drawn to one force scale
    Lw = 13.0
    LF = Lw * rat
    xa = x2 + bw / 2 + 14
    o.append(H.arrow(s, p, xa, ycomp, xa, ycomp - LF, "reaction"))
    o.append(H.label(s, xa + 8, ycomp - LF + 12, f'{it("F")}{H.sub("peak", s, "label2")} ≈ {F / 1e3:.1f} kN', "label2", I["primary"]))
    o.append(H.label(s, xa + 8, ycomp - LF + 32, f'= {rat:.1f} × weight', "label2", I["secondary"]))
    xw = xa + 18
    o.append(H.arrow(s, p, xw, ycomp - bh, xw, ycomp - bh + Lw, "load"))
    o.append(H.label(s, xw + 7, ycomp - bh + 12, f'weight {Wt:.0f} N', "label2", O["load"]))
    o.append(H.label(s, x2 + 10, yb1 - bh - 26, "peak compression", "label2", I["primary"], "middle"))
    o.append(H.label(s, x2 + 10, yb1 - bh - 10, "(forces to one scale)", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 220, 306, f'{it("m")}{H.sub("eff", s, "label2")}{it("gh")} = ½{it("k")}{H.sub("s", s, "label2")}{it("x")}² ({it("x")} ≪ {it("h")})  ⇒  '
                     f'{it("F")}{H.sub("peak", s, "label2")} = √(2{it("k")}{H.sub("s", s, "label2")}{it("m")}{H.sub("eff", s, "label2")}{it("gh")})',
                     "label2", I["primary"], "middle"))
    aria = ("Problem D10 setup, lengths and forces to scale. Left: an effective mass m eff = 28 kg released a height h "
            "= 0.5 m above a soft spring of stiffness k s (5 times 10 to the 4 newtons per metre). Right: at peak "
            f"compression x = {xc:.3f} m the spring pushes up on the mass with F peak about {F / 1e3:.1f} kN (black), "
            f"{rat:.1f} times the weight m eff g = {Wt:.0f} N (brown). Energy balance m eff g h = one half k s x "
            "squared, for x much smaller than h, gives F peak = square root of 2 k s m eff g h.")
    return finish(VB, aria, s, o)


FIGS = {
    2: ("Left: a beam segment bending so plane sections rotate, fibre", fig2),
    4: ("A straight beam bends downward and back; coloured fibres abo", fig4),
    12: ("Two equal-area cross-sections: a hollow tube with material f", fig12),
    13: ("A hollow section with its neutral axis, and the linear stres", fig13),
    14: ("A beam bent by a central load: the top face is in compressio", fig14),
    16: ("A loaded plate with a screw hole: the far-field stress lines", fig16),
    19: ("Stiff mineral platelets embedded in a collagen matrix; a cra", fig19),
    22: ("A rectangular cross-section of width b and height h with a s", fig22),
    24: ("A hollow circular section with an annular ring element dA eq", fig24),
    25: ("A hollow tube and an equal-area solid rod (dashed) overlaid,", fig25),
    26: ("A beam bent by a pair of equal and opposite end moments into", fig26),
    28: ("Left: a square element in pure shear with the 45 degree cut ", fig28),
    30: ("Two-phase composite as mineral and collagen in parallel (Voi", fig30),
    31: ("An effective mass falling a height h onto a soft spring of s", fig31),
}
