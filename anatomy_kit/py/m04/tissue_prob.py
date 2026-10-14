"""Module 4, group `tissue_prob`: schematic and tissue problem figures in the house style (400 px).

svg 28-33, 35-37 (C1-C6, C8-C10), 38-40 (D1-D3), 45 (D8), 47 (D10), 52 (K3).
Every number is computed here from the values module04.html states (line numbers next to each constant).
Knee art: DBCLS "202108 Sagittal section through knee joint.svg" (CC BY 4.0), the crop m04/tissue.py shares as
#m4art_knee (svg_paths/202108_Sagittal_section_through_knee_joint_crop_m04knee.svg).
"""
import math
import random

import house as H
from m05.body import finish, wrap
from m05.plots_prob import Plot, hov, legend as plegend
from m05.schematic import box, it
from m04.tissue import KNEE as KNEE_WIN, KNEE_ID
from m05.tissue import circ, legend, rect, sw_dot, sw_rect

T, O, I = H.TISSUE, H.OVERLAY, H.INK
BOX, GRID = "#f7f4ef", "#e6e6e6"
FIX = GRID                                           # lab fixtures: platen, piston, bench (as m04/tissue.py)
FL = T["fluid"][1]                                   # fluid-flow arrows and water marks
CART = T["cartilage"]
COLL = T["tendon"][1]                                # collagen fibre lines

# ---------------------------------------------------------------- numbers stated in module04.html
TAU_RANGE = (1e3, 1e4)          # s, gel time "10^3-10^4 s" (line 1433)
H_A, E_TENS = 0.6, 12.0         # MPa (lines 1433, 1532-1533, 1549)
PI_SWELL = 0.16                 # MPa, resting swelling pressure (line 1459)
R_LOAD, R_EFF, E_STAR = 1715.0, 0.030, 6.67e6    # N, m, Pa (K3 statement, line 1988)
SPREAD = 1.3                    # a' = 1.3 a (lines 968, 1509)
C_F, C_0, R_G, THETA = 0.2, 0.15, 8.314, 310.0   # M, M, J/(mol K), K (D2, line 1694)
MU_EQ, MU_MEAS = 0.15, (0.005, 0.02)             # D8 solution (line 1845)
M3_MEAN = 1.7                   # MPa, Module 3 estimate (line 1988)


def hertz():
    a = (3 * R_LOAD * R_EFF / (4 * E_STAR)) ** (1 / 3)
    p0, pm = 3 * R_LOAD / (2 * math.pi * a * a), R_LOAD / (math.pi * a * a)
    a2 = SPREAD * a
    pb = 2 * R_LOAD / (math.pi * a2 * a2)
    # K3 solution (line 2009): a = 18.0 mm, p0 = 2.54 MPa, mean 1.69 MPa; section 6 (line 968): p_max = 2.0 MPa
    assert (round(a * 1e3, 1), round(p0 / 1e6, 2), round(pm / 1e6, 2)) == (18.0, 2.54, 1.69)
    assert round(a2 * 1e3, 1) == 23.3 and round(pb / 1e6, 1) == 2.0
    n = 20000                                        # both profiles carry R (caption line 1509)
    for amp, rad, f in ((p0, a, lambda u: math.sqrt(max(0.0, 1 - u * u))), (pb, a2, lambda u: 1 - u * u)):
        tot = sum(amp * f((k + 0.5) / n) * 2 * math.pi * (k + 0.5) / n * rad * rad / n for k in range(n))
        assert abs(tot - R_LOAD) < 0.001 * R_LOAD, tot
    return a * 1e3, p0 / 1e6, pm / 1e6, a2 * 1e3, pb / 1e6


def donnan():
    q = math.sqrt(C_F ** 2 + 4 * C_0 ** 2)
    cp, cm = (q + C_F) / 2, (q - C_F) / 2
    ex = q - 2 * C_0
    pi = R_G * THETA * ex * 1e3                       # Pa (mol/L -> mol/m3)
    # D2 solution (line 1713): 0.3606 M, excess 0.0606 M, R_g Theta = 2577 J/mol, pi ~ 1.56e5 Pa
    assert round(q, 4) == 0.3606 and round(ex, 4) == 0.0606 and round(R_G * THETA) == 2577 and round(pi / 1e4) == 16
    return cp, cm, ex, pi


# ---------------------------------------------------------------- local drawing helpers
def fl_marker(p, s):
    """Slim head for fluid-flow arrows (house.markers has no fluid meaning). Id: {p}a_fl."""
    sz = s(H.PX["head_geom"])
    return (f'<marker id="{p}a_fl" markerUnits="userSpaceOnUse" markerWidth="{sz*1.2:.2f}" markerHeight="{sz*0.8:.2f}" '
            f'refX="{sz*0.95:.2f}" refY="{sz*0.4:.2f}" orient="auto-start-reverse">'
            f'<path d="M0,0 L{sz:.2f},{sz*0.4:.2f} L0,{sz*0.8:.2f} Z" fill="{FL}"/></marker>')


def defs(p, s):
    return f'<defs>{H.markers(p, s)}{fl_marker(p, s)}</defs>'


def flow(s, p, x1, y1, x2, y2, w="geom"):
    return H.line(s, x1, y1, x2, y2, FL, w, extra=f'marker-end="url(#{p}a_fl)"')


def sw_flow(x, y):
    return (f'<line x1="{x}" y1="{y-5}" x2="{x+11}" y2="{y-5}" stroke="{FL}" stroke-width="2"/>'
            f'<path d="M{x+9},{y-8.5} L{x+15},{y-5} L{x+9},{y-1.5} Z" fill="{FL}"/>')


def curved(s, p, x1, y1, cx, cy, x2, y2, meaning="dim", w="ref"):
    return (f'<path d="M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="{O[meaning]}" '
            f'stroke-width="{s(H.PX[w]):.2f}" marker-end="url(#{p}a_{meaning})"/>')


def area(pts, fill, stroke, sw=1.0, extra=""):
    return (f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in pts)} Z" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linejoin="round" {extra}/>')


def dots(pts, r, fill, stroke, sw=0.7):
    """Many equal circles as one path (small page)."""
    d = "".join(f"M{x - r:.1f},{y:.1f}a{r},{r} 0 1 0 {2 * r},0a{r},{r} 0 1 0 {-2 * r},0" for x, y in pts)
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def ion(x, y, sign, r=4.6):
    """Mobile ion: fluid token (ions are never neural green). Cation filled with +, anion white with a minus."""
    f, l = T["fluid"]
    d = f"M{x - r * 0.55:.1f},{y:.1f}h{r * 1.1:.1f}" + (f"M{x:.1f},{y - r * 0.55:.1f}v{r * 1.1:.1f}" if sign > 0 else "")
    return circ(x, y, r, f if sign > 0 else "#fff", l, 0.9) + f'<path d="{d}" stroke="{I["primary"]}" stroke-width="1.2"/>'


def sw_ion(sign):
    return lambda x, y: ion(x + 7, y - 5, sign, 4.4)


def minus(x, y, w=5.0):
    return f'<path d="M{x - w / 2:.1f},{y:.1f}h{w:.1f}" stroke="{I["primary"]}" stroke-width="1.4"/>'


def brush(x, y0, y1, step=8.0, arm=8.0, charges=True):
    """Proteoglycan bottlebrush: core line (ink) with side chains, a fixed negative charge at each chain tip.
    Returns (svg, list of charge positions)."""
    o = [f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y1:.1f}" stroke="{I["secondary"]}" stroke-width="1.6"/>']
    tips, k, y = [], 0, y0 + step / 2
    while y < y1 - 2:
        sg = -1 if k % 2 == 0 else 1
        tx, ty = x + sg * arm, y - 3
        o.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{I["secondary"]}" stroke-width="1.0"/>')
        if charges:
            cx = tx + sg * 3.5
            o.append(minus(cx, ty))
            tips.append((cx, ty))
        y += step
        k += 1
    return "".join(o), tips


def sw_brush(x, y):
    return (f'<line x1="{x+7}" y1="{y-11}" x2="{x+7}" y2="{y+1}" stroke="{I["secondary"]}" stroke-width="1.6"/>'
            f'<line x1="{x+7}" y1="{y-6}" x2="{x+1}" y2="{y-8}" stroke="{I["secondary"]}" stroke-width="1"/>' + minus(x + 12, y - 4, 4))


def sw_fibre(x, y):
    return f'<line x1="{x}" y1="{y-5}" x2="{x+14}" y2="{y-5}" stroke="{COLL}" stroke-width="2.2"/>'


def lattice(x0, y0, x1, y1, gap, slope=0.75, w=1.8):
    """Collagen network: two families of straight fibres (slopes +-slope) clipped to a rectangle."""
    segs = []
    for sg in (1, -1):
        c = -abs(slope) * (x1 - x0) - gap / 2
        while c < (y1 - y0) + abs(slope) * (x1 - x0):
            # line y = y0 + c + sg*slope*(x - x0) for sg=1; mirrored for sg=-1
            pts = []
            for x in (x0, x1):
                y = y0 + c + slope * ((x - x0) if sg > 0 else (x1 - x))
                pts.append((x, y))
            (ax, ay), (bx, by) = pts
            def clip(px, py, qx, qy):
                if py < y0:
                    px, py = px + (y0 - py) * (qx - px) / (qy - py), y0
                if py > y1:
                    px, py = px + (y1 - py) * (qx - px) / (qy - py), y1
                return px, py
            if not ((ay < y0 and by < y0) or (ay > y1 and by > y1)):
                a2, b2 = clip(ax, ay, bx, by), clip(bx, by, ax, ay)
                if math.hypot(b2[0] - a2[0], b2[1] - a2[1]) > 8:
                    segs.append(f"M{a2[0]:.1f},{a2[1]:.1f}L{b2[0]:.1f},{b2[1]:.1f}")
            c += gap
    return (f'<path d="{"".join(segs)}" fill="none" stroke="{COLL}" stroke-width="{w}" stroke-linecap="round" '
            f'opacity="0.85"/>')


def platen(s, x0, x1, y, h=8.0):
    """Porous platen (lab fixture): box fill with drainage holes."""
    o = [rect(x0, y, x1 - x0, h, FIX, I["axis"], 1.0)]
    x = x0 + 6
    while x < x1 - 3:
        o.append(circ(x, y + h / 2, 1.6, "#fff", I["rule"], 0.6))
        x += 9
    return "".join(o)


def sealed(s, x0, x1, y):
    """Impermeable base: heavy ink rule with hatch below."""
    o = [H.line(s, x0, y, x1, y, I["axis"], "force")]
    x = x0 + 3
    while x < x1:
        o.append(H.line(s, x, y + 1, x - 6, y + 8, I["axis"], "leader"))
        x += 8
    return "".join(o)


def walls(s, x0, x1, yt, yb):
    return H.line(s, x0, yt, x0, yb, I["axis"], "axis") + H.line(s, x1, yt, x1, yb, I["axis"], "axis")


def credit_dbcls(s, x, y, n=70):
    c = H.ATTRIBUTION["by"].format(author="DataBase Center for Life Science (DBCLS)",
                                   title="202108 Sagittal section through knee joint.svg", licence="CC BY 4.0",
                                   changes="Cropped and recoloured; overlays drawn for this course.")
    lines = wrap(c, n)
    return H.credit(s, x, y, lines), len(lines)


# ---------------------------------------------------------------- knee art: m04/tissue.py puts the DBCLS crop on the page
# once as #m4art_knee (SHARED_DEFS, source units, its own local recolour); these figures show a window of it.
# Landmarks in the sheet's user units (Chrome getPointAtLength on the sheet's paths)
KN = dict(fem_cart=(190.0, 266.0),      # femoral cartilage, lowest arc (y 268.7 at x 190)
          tib_cart=(205.0, 277.5),      # tibial cartilage, between y 274.2 and 280.5 at x 205
          men_post=(163.0, 275.0),      # posterior meniscus horn
          men_ant=(222.0, 267.0),       # anterior meniscus horn
          cavity=(244.0, 244.0),        # joint cavity in front of the condyle
          femur=(200.0, 232.0))         # femoral condyle, medullary bone


def knee(p, win, fx, fy, k):
    """Show the window win = (x0, y0, w, h) of #m4art_knee at (fx, fy), k figure units per sheet unit. A pattern
    fill (not a clip-path) bounds the art to the window, so check_frame measures the window only.
    Returns (svg, map sheet point -> figure point)."""
    x0, y0, w, h = win
    assert x0 >= KNEE_WIN[0] and y0 >= KNEE_WIN[1] and x0 + w <= KNEE_WIN[0] + KNEE_WIN[2] and y0 + h <= KNEE_WIN[1] + KNEE_WIN[3]
    W, Hh = w * k, h * k
    svg = (f'<defs><pattern id="{p}knee" patternUnits="userSpaceOnUse" x="{fx:.2f}" y="{fy:.2f}" width="{W:.2f}" '
           f'height="{Hh:.2f}"><use href="#{KNEE_ID}" transform="scale({k:.4f}) translate({-x0:.2f} {-y0:.2f})"/>'
           f'</pattern></defs><rect x="{fx:.2f}" y="{fy:.2f}" width="{W:.2f}" height="{Hh:.2f}" fill="url(#{p}knee)"/>')
    return svg, (lambda q: (fx + (q[0] - x0) * k, fy + (q[1] - y0) * k))


def lead(s, x1, y1, x2, y2):
    return H.line(s, x1, y1, x2, y2, I["secondary"], "leader") + circ(x1, y1, 1.8, I["primary"])


def surface(x0, x1, yt, dent, n=60):
    return [(x0 + (x1 - x0) * i / n, yt + dent(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]


# ================================================================ svg 28 (C1): thumb vs book, one gel time
def fig28():
    p = "m4f28_"
    VB = (0, 0, 400, 334)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [defs(p, s)]
    yt, th = 112.0, 40.0
    for cx, title, D, wbook in ((100, "thumb press, ~1 s", 2.0, None), (300, "book, an afternoon", 13.0, 90.0)):
        x0, x1 = cx - 82, cx + 82
        if wbook:
            dent = lambda x, cx=cx, D=D, hw=wbook / 2: D * 0.5 * (1 - math.tanh((abs(x - cx) - hw) / 5.0))  # noqa: E731
        else:
            dent = lambda x, cx=cx, D=D: D * math.exp(-((x - cx) / 9.0) ** 2)  # noqa: E731
        top = surface(x0, x1, yt, dent)
        o.append(area(top + [(x1, yt + th), (x0, yt + th)], CART[0], CART[1], 1.2))
        # interstitial water: the drained layer under the book has lost some (sparser grid there)
        wd = []
        for j, y in enumerate(range(int(yt) + 7, int(yt + th) - 3, 9)):
            for i, x in enumerate(range(x0 + 7, x1 - 3, 11)):
                if y < yt + dent(x) + 5:
                    continue
                if wbook and abs(x - cx) < wbook / 2 + 4 and (i + j) % 2:
                    continue
                wd.append((x, y))
        o.append(dots(wd, 2.1, T["fluid"][0], FL))
        o.append(rect(x0 - 8, yt + th, x1 - x0 + 16, 9, FIX, I["rule"], 1.0))
        o.append(H.label(s, cx, 22, title, "label", I["primary"], "middle"))
        if wbook:
            bx0, bx1, by1 = cx - wbook / 2, cx + wbook / 2, yt + D
            o.append(rect(bx0, by1 - 24, wbook, 24, BOX, I["axis"], 1.2, 2))
            o.append(H.label(s, cx, by1 - 8, "book", "label2", I["primary"], "middle"))
            o.append(H.arrow(s, p, cx, 40, cx, by1 - 27, "load"))
            o.append(H.label(s, cx + 8, 56, "weight", "label2", I["secondary"]))
            for sg in (-1, 1):                                   # fluid leaves at the free surface and the cut edges
                o.append(flow(s, p, cx + sg * (wbook / 2 + 10), yt - 1, cx + sg * (wbook / 2 + 24), yt - 17))
                o.append(flow(s, p, cx + sg * 80, yt + th / 2, cx + sg * 97, yt + th / 2))
            o.append(H.label(s, cx, 177, "sinks, stays dented:", "label2", I["primary"], "middle"))
            o.append(H.label(s, cx, 193, "fluid exudes, soft matrix left", "label2", I["secondary"], "middle"))
            o.append(H.label(s, cx, 214, f"drained: {it('F')} → 0", "label", I["primary"], "middle"))
        else:
            o.append(H.arrow(s, p, cx, 40, cx, yt - 1, "load"))
            o.append(H.label(s, cx + 8, 56, "thumb", "label2", I["secondary"]))
            o.append(H.label(s, cx, 177, "barely dents, feels firm:", "label2", I["primary"], "middle"))
            o.append(H.label(s, cx, 193, "fluid has no time to leave", "label2", I["secondary"], "middle"))
            o.append(H.label(s, cx, 214, f"undrained: {it('F')} ≈ 1", "label", I["primary"], "middle"))
    o.append(H.line(s, 200, 14, 200, 222, GRID, "leader"))
    # loading time on a log axis; the gel time band divides the two regimes (line 1433)
    xa0, xa1, ya = 26.0, 374.0, 268.0
    X = lambda t: xa0 + math.log10(t) / 5 * (xa1 - xa0)     # noqa: E731
    xl, xr = X(TAU_RANGE[0]), X(TAU_RANGE[1])
    o.append(rect(xl, ya - 12, xr - xl, 12, O["geometry"], extra='opacity="0.18"'))
    o.append(H.line(s, xa0, ya, xa1, ya, I["axis"], "axis"))
    for t, name in ((1, "1 s"), (60, "1 min"), (3600, "1 h"), (86400, "1 day")):
        o.append(H.line(s, X(t), ya, X(t), ya + 5, I["axis"], "leader"))
        o.append(H.label(s, X(t), ya + 19, name, "tick", I["secondary"], "middle"))
    xm = (xl + xr) / 2
    o.append(H.label(s, xm, ya - 34, f"gel time {it('τ')} ∼ h²/(H{H.sub('A', s, 'label2')}k)", "label2", I["primary"], "middle"))
    o.append(H.label(s, xm, ya - 18, "≈ 10³–10⁴ s", "label2", I["primary"], "middle"))
    o.append(H.label(s, xa0, ya - 6, "loading time (log scale)", "label2", I["secondary"]))
    o.append(H.label(s, xl - 6, ya + 37, f"thumb ≪ {it('τ')}: undrained", "label2", I["primary"], "end"))
    o.append(H.label(s, 396, ya + 37, f"book ≫ {it('τ')}: drained", "label2", I["primary"], "end"))
    lg, _ = legend(s, 14, 328, [(sw_rect(CART[0], CART[1]), "cartilage"), (sw_dot(T["fluid"][0], FL), "water"),
                                (sw_flow, "fluid flow"), (sw_rect(FIX, I["rule"]), "bench")], gap=16)
    o.append(lg)
    aria = ("Problem C1 setup. Left: a thumb presses a cartilage sample on a bench for about one second; the layer "
            "barely dents and feels firm because the interstitial water has no time to leave: undrained, F about 1. "
            "Right: a book rests on the same sample for an afternoon; water exudes at the free surface and the cut "
            "edges, the layer sinks and stays dented: drained, F goes to 0. Below, a logarithmic loading-time axis "
            "from 1 second to 1 day with the gel time tau, about h squared over H A k, shaded from 10 to the 3 to 10 "
            "to the 4 seconds: the thumb, at 1 second, sits 3 decades below the band; the book, held for hours, sits above it.")
    return finish(VB, aria, s, o)


# ================================================================ svg 29 (C2): charge makes pre-stress
def fig29():
    p = "m4f29_"
    VB = (0, 0, 400, 306)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [defs(p, s)]
    x0, x1, y0, y1 = 82.0, 318.0, 62.0, 196.0
    o.append(rect(x0, y0, x1 - x0, y1 - y0, CART[0], CART[1], 1.2, 10))
    # collagen network: a loose mesh of taut fibres spanning the matrix (it holds the swelling)
    o.append(lattice(x0 + 4, y0 + 4, x1 - 4, y1 - 4, 34.0))
    # proteoglycans with fixed negative charges; mobile Na+ counter-ions crowd round them
    rnd = random.Random(4)
    for xb in (118, 166, 234, 282):
        b, tips = brush(xb, 92, 168)
        o.append(b)
    pts = []
    while len(pts) < 16:
        x, y = rnd.uniform(x0 + 14, x1 - 14), rnd.uniform(y0 + 12, y1 - 12)
        if all(abs(x - xb) > 16 for xb in (118, 166, 234, 282)) and all(math.hypot(x - a, y - b) > 18 for a, b in pts):
            pts.append((x, y))
    o.extend(ion(x, y, +1) for x, y in pts)
    # water drawn in from the bath (osmosis)
    for y in (96, 129, 162):
        o.append(flow(s, p, 14, y, x0 - 4, y, "force"))
    o.append(H.label(s, 8, 82, "water in", "label2", I["primary"]))
    o.append(H.label(s, 8, 216, "saline", "label2", I["secondary"]))
    o.append(H.label(s, 8, 231, "bath", "label2", I["secondary"]))
    # swelling pressure pushes out; the collagen tension holds it
    for x1_, y1_, x2_, y2_ in ((200, y0 - 2, 200, y0 - 26), (x1 + 2, 129, x1 + 26, 129), (200, y1 + 2, 200, y1 + 24)):
        o.append(H.arrow(s, p, x1_, y1_, x2_, y2_, "force"))
    o.append(H.label(s, 210, 32, f"swelling pressure {it('π')} ≈ {PI_SWELL} MPa", "label2", I["primary"]))
    o.append(H.label(s, x1 + 8, 152, "collagen", "label2", I["primary"]))
    o.append(H.label(s, x1 + 8, 167, "tension", "label2", I["primary"]))
    o.append(H.label(s, x1 + 8, 182, "holds it", "label2", I["primary"]))
    o.append(H.label(s, 200, 240, "unloaded, yet pre-stressed: collagen in tension,", "label2", I["primary"], "middle"))
    o.append(H.label(s, 200, 256, f"gel in compression at {it('π')}", "label2", I["primary"], "middle"))
    lg1, _ = legend(s, 10, 282, [(sw_rect(CART[0], CART[1]), "matrix"), (sw_fibre, "collagen fibre"),
                                 (sw_brush, "proteoglycan, fixed − charge")], gap=10)
    lg2, _ = legend(s, 10, 300, [(sw_ion(+1), "Na⁺ counter-ion"), (sw_flow, "water flow"),
                                 (lambda x, y: H.line(s, x, y - 5, x + 14, y - 5, O["force"], "force"), "swelling pressure")], gap=10)
    o += [lg1, lg2]
    aria = ("Problem C2 setup: a block of cartilage matrix in a saline bath. Four proteoglycan bottlebrushes carry fixed "
            "negative charges; mobile sodium counter-ions crowd into the matrix to neutralise them, and water follows "
            "osmotically from the bath. The excess ions set a swelling pressure pi of about 0.16 megapascal that "
            "pushes outward, held in check by the tension of a collagen fibre network: unloaded, the tissue is "
            "already pre-stressed, collagen in tension and gel in compression.")
    return finish(VB, aria, s, o)


# ================================================================ svg 30 (C3): who carries the first instant
def spring(x, y0, y1, n=7, w=12.0):
    """Zigzag spring from y0 (bottom) to y1 (top): the solid matrix."""
    pts = [(x, y0), (x, y0 - 6)]
    L = (y0 - 6) - (y1 + 6)
    for k in range(2 * n):
        pts.append((x + (w if k % 2 == 0 else -w), y0 - 6 - L * (k + 0.5) / (2 * n)))
    pts += [(x, y1 + 6), (x, y1)]
    return (f'<path d="M{" L".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{T["bone"][1]}" '
            f'stroke-width="3.0" stroke-linejoin="round"/>')               # width as m04/tissue.py (SOLID, 3.0)


def valve(s, x, y, open_):
    """Drain tube on the piston with a valve symbol (two triangles): filled = closed, white = open."""
    o = [rect(x - 4, y - 22, 8, 22, "#fff", I["axis"], 1.0)]
    o.append(f'<path d="M{x-8},{y-30} L{x+8},{y-22} L{x+8},{y-30} L{x-8},{y-22} Z" fill="{"#fff" if open_ else I["axis"]}" '
             f'stroke="{I["axis"]}" stroke-width="1"/>')
    return "".join(o)


def fig30():
    p = "m4f30_"
    VB = (0, 0, 400, 300)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [defs(p, s)]
    yb = 214.0
    for cx, title, ypist in ((100, "t = 0: drain closed", 92.0), (300, "t ≫ τ: drain open", 122.0)):
        x0, x1 = cx - 54, cx + 54
        o.append(rect(x0, ypist + 12, x1 - x0, yb - ypist - 12, T["fluid"][0], extra='opacity="0.75"'))
        o.append(spring(cx - 18, yb, ypist + 12, n=7 if ypist < 100 else 9))
        o.append(walls(s, x0, x1, 70, yb) + H.line(s, x0, yb, x1, yb, I["axis"], "axis"))
        o.append(rect(x0 + 1, ypist, x1 - x0 - 2, 12, FIX, I["axis"], 1.2))
        o.append(valve(s, cx + 30, ypist, ypist > 100))
        o.append(H.arrow(s, p, cx - 18, 34, cx - 18, ypist - 2, "load"))
        o.append(H.label(s, cx - 10, 50, it("σ"), "label", I["primary"]))
        o.append(H.label(s, cx, 20, title, "label", I["primary"], "middle"))
    o.append(flow(s, p, 330, 88, 330, 62))
    o.append(H.label(s, 338, 68, "water out", "label2", I["secondary"]))
    # what carries the load in each state (lines 1463, 1482)
    rows = [((100, f"ε = 0, so σ{H.sub('E', s, 'label2')} = H{H.sub('A', s, 'label2')}ε = 0 for any H{H.sub('A', s, 'label2')}"),
             (300, f"ε = σ/H{H.sub('A', s, 'label2')}, σ{H.sub('E', s, 'label2')} = σ")),
            ((100, f"{it('p')} = σ: fluid carries all, {it('F')} = 1"), (300, f"{it('p')} = 0: solid carries all, {it('F')} → 0"))]
    for k, row in enumerate(rows):
        for cx, t in row:
            o.append(H.label(s, cx, 236 + 17 * k, t, "label2", I["primary"], "middle"))
    o.append(H.line(s, 200, 12, 200, 220, GRID, "leader"))
    zig = (lambda x, y: f'<path d="M{x},{y-5} l2.5,-4 l3,8 l3,-8 l3,8 l2.5,-4" fill="none" stroke="{T["bone"][1]}" '
           f'stroke-width="2"/>')
    lg, _ = legend(s, 10, 294, [(sw_rect(T["fluid"][0]), "water = fluid"), (zig, "spring = solid matrix"),
                                (sw_rect(FIX, I["axis"]), "piston")], gap=16)
    o.append(lg)
    aria = ("Problem C3 setup: a sealed water-filled chamber with a spring, under a piston loaded by sigma. Left, t = 0, "
            "drain closed: no water can leave, so the spring is not compressed, epsilon = 0 and the solid stress "
            "sigma E = H A epsilon = 0 for any spring stiffness H A; the water pressure p = sigma carries all the "
            "load, F = 1. Right, long after the gel time with the drain open: water has left, the piston has sunk, "
            "the spring is compressed to epsilon = sigma over H A and carries all the load, p = 0, F goes to 0.")
    return finish(VB, aria, s, o)


# ================================================================ svg 31 (C4): bearing vs cartilage at v = 0
def fig31():
    p = "m4f31_"
    VB = (0, 0, 400, 350)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [defs(p, s)]
    # journal bearing at rest: shaft sits on the bushing, oil squeezed out of the contact
    cx, cy, rb, rs = 96.0, 122.0, 54.0, 47.0
    o.append(circ(cx, cy, rb + 12, GRID, I["axis"], 1.2))
    o.append(circ(cx, cy, rb, T["fluid"][0], FL, 0.8))
    o.append(circ(cx, cy + rb - rs, rs, BOX, I["axis"], 1.2))
    o.append(H.arrow(s, p, cx, cy - 40, cx, cy + 10, "load"))
    o.append(lead(s, cx + 30, cy - rb + 6, 150, 76))
    o.append(H.label(s, 154, 80, "oil", "label2", I["primary"]))
    o.append(H.label(s, cx + 8, cy - 22, "load", "label2", I["secondary"]))
    o.append(lead(s, cx, cy + rb, cx, cy + rb + 15))
    o.append(H.label(s, 8, 18, "journal bearing", "label", I["primary"]))
    o.append(H.label(s, cx, cy + rb + 30, "metal on metal", "label2", I["primary"], "middle"))
    o.append(H.label(s, 8, 260, f"{it('v')} = 0: no wedge, no film,", "label2", I["primary"]))
    o.append(H.label(s, 8, 276, "high friction at start", "label2", I["primary"]))
    o.append(H.label(s, 8, 36, "(film forms only when", "label2", I["secondary"]))
    o.append(H.label(s, 8, 51, "spin drags oil in)", "label2", I["secondary"]))
    # cartilage in the knee: the sheet's femoral condyle on the tibial plateau
    art, M = knee(p, (146, 206, 116, 104), 200, 48, 1.66)
    o.append(art)
    o.append(H.label(s, 214, 18, "knee cartilage", "label", I["primary"]))
    fx, fy = M(KN["femur"])
    o.append(H.label(s, fx - 30, fy + 8, "femur", "label2", I["primary"], "middle"))
    tx, ty = M((222, 300))
    o.append(H.label(s, tx, ty, "tibia", "label2", I["primary"], "middle"))
    o.append(H.arrow(s, p, fx, 26, fx, fy - 6, "load"))
    o.append(H.label(s, fx + 8, 40, "load", "label2", I["secondary"]))
    for key, (lx, ly) in (("tib_cart", (340, 238)), ("men_post", (236, 238)), ("cavity", (372, 92))):
        ax, ay = M(KN[key])
        o.append(lead(s, ax, ay, lx, ly - 12))
    o.append(H.label(s, 398, 238, "cartilage", "label2", I["primary"], "end"))
    o.append(H.label(s, 204, 238, "meniscus", "label2", I["primary"]))
    o.append(H.label(s, 398, 90, "synovial", "label2", I["primary"], "end"))
    o.append(H.label(s, 398, 105, "fluid", "label2", I["primary"], "end"))
    o.append(H.label(s, 204, 260, f"{it('v')} = 0, freshly loaded: interstitial", "label2", I["primary"]))
    o.append(H.label(s, 204, 276, f"fluid pressurised, {it('F')} ≈ 1, so", "label2", I["primary"]))
    o.append(H.label(s, 204, 292, f"μ{H.sub('eff', s, 'label2')} = μ{H.sub('eq', s, 'label2')}(1 − {it('F')}) ≈ 0",
                     "label2", I["primary"]))
    cr, n = credit_dbcls(s, 8, 314)
    o.append(cr)
    aria = ("Problem C4 setup. Left: a journal bearing at rest; the loaded shaft sits on the bushing, metal on metal, "
            "because at v = 0 no wedge drags oil in to build a film, so friction is high at the start. Right: the "
            "knee in sagittal section, femoral condyle on the tibial plateau with articular cartilage, menisci and "
            "synovial fluid; freshly loaded at v = 0 the cartilage's interstitial fluid is already pressurised, "
            "F about 1, so mu eff = mu eq times (1 minus F) is about 0.")
    return finish(VB, aria, s, o)


# ================================================================ svg 32 (C5) and 52 (K3): knee contact pressure
def contact_plot(s, xr=(-30, 30)):
    P = Plot(s, (58, 52, 388, 232), xr, (0, 3))
    ax = P.axes([(v, str(v).replace("-", "−")) for v in range(xr[0], xr[1] + 1, 10)],
                [(v, str(v)) for v in range(4)], "radius r (mm)", "contact pressure p (MPa)", grid=(1, 2, 3), ytx=16)
    return P, ax


def cap(r, a, p0):
    return p0 * math.sqrt(1 - (r / a) ** 2) if abs(r) < a else 0.0


def para(r, a, pm):
    return pm * (1 - (r / a) ** 2) if abs(r) < a else 0.0


def fig32():
    VB = (0, 0, 400, 300)
    s = H.Scale(VB[2], VB[3], display_w=400)
    a, p0, _, a2, pb = hertz()
    P, ax = contact_plot(s)
    rs = [-30 + 0.1 * k for k in range(601)]
    rc = [a * math.sin(math.pi * (k / 300 - 0.5)) for k in range(301)]          # dense at the cap edges
    o = [ax, P.curve(rc, [cap(r, a, p0) for r in rc], H.SERIES[0], multi=True),
         P.curve([r for r in rs if abs(r) <= a2], [para(r, a2, pb) for r in rs if abs(r) <= a2], H.SERIES[1], multi=True)]
    o.append(plegend(s, 58, 18, [(H.SERIES[0], f"dry Hertz cap: p{H.sub('0', s, 'label2')} = {p0:.2f} MPa, a = {a:.1f} mm", None)]))
    o.append(plegend(s, 58, 36, [(H.SERIES[1], f"biphasic parabola: p{H.sub('max', s, 'label2')} = {pb:.1f} MPa, "
                                               f"a′ = 1.3a = {a2:.1f} mm", None)]))
    o.append(H.label(s, P.X(-13.6), P.Y(2.02), "Hertz", "label2", I["primary"], "end"))
    o.append(H.label(s, P.X(20.2), P.Y(0.86), "biphasic", "label2", I["primary"]))
    o.append(H.label(s, P.X(-29.3), P.Y(2.82), "same load:", "label2", I["secondary"]))
    o.append(H.label(s, P.X(-29.3), P.Y(2.56), "∫p dA = 1715 N", "label2", I["secondary"]))
    pts = hov(P, rs, [[cap(r, a, p0) for r in rs], [para(r, a2, pb) for r in rs]],
              lambda i: f"r = {rs[i]:.1f} mm: Hertz {cap(rs[i], a, p0):.2f} MPa, biphasic {para(rs[i], a2, pb):.2f} MPa")
    aria = (f"Problem C5 plot: contact pressure against radius across the knee contact, both carrying the same load of "
            f"1715 newtons. Red, the dry Hertz cap: peak {p0:.2f} megapascal, contact radius {a:.1f} millimetres. Blue, "
            f"the broader biphasic parabola of section 6: peak {pb:.1f} megapascal over a radius 1.3 a = {a2:.1f} "
            f"millimetres. The biphasic profile is lower in the middle and lifted at the edges.")
    return finish(VB, aria, s, o, extra=H.hover_attr(P.box, pts))


def fig52():
    VB = (0, 0, 400, 300)
    s = H.Scale(VB[2], VB[3], display_w=400)
    p = "m4f52_"
    a, p0, pm, _, _ = hertz()
    P, ax = contact_plot(s, (-25, 25))
    rc = [a * math.sin(math.pi * (k / 300 - 0.5)) for k in range(301)]
    o = [f'<defs>{H.markers(p, s)}</defs>', ax, P.curve(rc, [cap(r, a, p0) for r in rc], H.SERIES[0])]
    o.append(H.line(s, P.X(-a), P.Y(pm), P.X(a), P.Y(pm), O["dim"], "ref", H.DASH_REF))
    o.append(H.arrow(s, p, P.X(0), P.Y(0.22), P.X(a) - 1, P.Y(0.22), "geometry", both=True))
    o.append(H.label(s, P.X(a / 2), P.Y(0.22) - 6, f"a = {a:.1f} mm", "label2", I["primary"], "middle"))
    o.append(H.label(s, P.X(0), P.Y(p0) - 10, f"p{H.sub('0', s, 'label2')} = 3R/(2πa²) = {p0:.2f} MPa", "label2", I["primary"],
                     "middle"))
    o.append(H.label(s, P.X(0), P.Y(pm) + 20, f"mean p̄ = R/(πa²) = {pm:.2f} MPa", "label2", I["primary"], "middle"))
    o.append(H.label(s, P.X(0), P.Y(pm) + 36, f"Module 3: {M3_MEAN} MPa", "label2", I["secondary"], "middle"))
    o.append(H.label(s, P.X(0), P.Y(pm) + 52, f"p{H.sub('0', s, 'label2')}/p̄ = 3/2", "label2", I["secondary"], "middle"))
    o.append(plegend(s, 58, 18, [(H.SERIES[0], f"Hertz cap, R = 1715 N, R{H.sub('eff', s, 'label2')} = 30 mm, "
                                               f"E* = 6.67 MPa", None)]))
    o.append(plegend(s, 58, 36, [(O["dim"], "mean over the contact", H.DASH_REF)]))
    rs = [-25 + 0.1 * k for k in range(501)]
    pts = hov(P, rs, [[cap(r, a, p0) for r in rs]], lambda i: f"r = {rs[i]:.1f} mm: p = {cap(rs[i], a, p0):.2f} MPa")
    aria = (f"Problem K3 plot: the Hertz pressure cap across the knee contact for R = 1715 newtons, R eff = 30 "
            f"millimetres and E star = 6.67 megapascal. Contact radius a = {a:.1f} millimetres, peak p0 = {p0:.2f} "
            f"megapascal, and a dashed line at the mean pressure {pm:.2f} megapascal, against the Module 3 estimate of "
            f"1.7 megapascal. The peak is 3/2 of the mean.")
    return finish(VB, aria, s, o, extra=H.hover_attr(P.box, pts))


# ================================================================ svg 33 (C6): fibres pull, gel squishes
def wavy(x0, x1, y, amp, n, k=3.0):
    pts = [(x0 + (x1 - x0) * i / n, y + amp * math.sin(2 * math.pi * k * i / n)) for i in range(n + 1)]
    return f'M{" L".join(f"{a:.1f},{b:.1f}" for a, b in pts)}'


def fig33():
    p = "m4f33_"
    VB = (0, 0, 400, 318)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [defs(p, s)]
    # tension: strip pulled at both ends, collagen fibres straight and taut
    x0, x1, y0, y1 = 34.0, 166.0, 70.0, 116.0
    o.append(rect(x0, y0, x1 - x0, y1 - y0, CART[0], CART[1], 1.2, 4))
    for xb in (72, 128):
        o.append(brush(xb, y0 + 6, y1 - 6, step=9, arm=6, charges=False)[0])
    d = "".join(f"M{x0 + 3},{y:.1f}L{x1 - 3},{y:.1f}" for y in (78, 88, 98, 108))
    o.append(f'<path d="{d}" stroke="{COLL}" stroke-width="2.2" fill="none"/>')
    for xa, xb in ((x0 - 2, 6), (x1 + 2, 194)):
        o.append(H.arrow(s, p, xa, 93, xb, 93, "force"))
    o.append(H.label(s, 100, 22, "stretch", "label", I["primary"], "middle"))
    o.append(H.label(s, 100, 42, "collagen fibres pull taut", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 100, 142, f"stiff: E{H.sub('tens', s, 'label2')} ≈ {E_TENS:.0f} MPa", "label2", I["primary"], "middle"))
    # compression: strip squeezed, fibres buckle, the swollen gel resists
    x0, x1, y0, y1 = 232.0, 368.0, 78.0, 108.0
    o.append(rect(x0, y0, x1 - x0, y1 - y0, CART[0], CART[1], 1.2, 4))
    d = "".join(wavy(x0 + 3, x1 - 3, y, 2.6, 60, 4) for y in (84, 93, 102))
    o.append(f'<path d="{d}" stroke="{COLL}" stroke-width="2.2" fill="none"/>')
    for xb in (262, 300, 338):
        b, _ = brush(xb, y0 + 3, y1 - 3, step=7, arm=5)
        o.append(b)
    for ya, yb in ((52, y0 - 2), (134, y1 + 2)):
        o.append(H.arrow(s, p, 300, ya, 300, yb, "geometry", w="force"))   # compression blue
    o.append(H.label(s, 300, 22, "squeeze", "label", I["primary"], "middle"))
    o.append(H.label(s, 300, 42, "fibres buckle; the gel resists", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 300, 152, f"soft: H{H.sub('A', s, 'label2')} ≈ {H_A} MPa", "label2", I["primary"], "middle"))
    o.append(H.line(s, 200, 10, 200, 160, GRID, "leader"))
    # the two moduli to one scale (lines 1532, 1549)
    P = Plot(s, (70, 186, 390, 266), (0, 2), (0, 12))
    o.append(P.axes([], [(v, str(v)) for v in (0, 4, 8, 12)], "", "modulus (MPa)", grid=(4, 8, 12), ytx=20))
    hv = []
    for k, (v, name, sym) in enumerate(((E_TENS, "tension", f"E{H.sub('tens', s, 'label2')}"),
                                        (H_A, "compression", f"H{H.sub('A', s, 'label2')}"))):
        xc = P.X(0.5 + k)
        o.append(rect(xc - 30, P.Y(v), 60, P.y0 - P.Y(v), H.SERIES[k], extra='fill-opacity="0.85"'))
        o.append(H.label(s, xc, P.Y(v) - 6, f"{v:g} MPa", "tick", I["primary"], "middle"))
        o.append(H.label(s, xc, P.y0 + 18, f"{name}, {sym}", "label2", I["primary"], "middle"))
        hv.append([round(xc, 2), round(P.Y(v), 2), f"{name}: {v:g} MPa"])
    o.append(H.label(s, 388, 202, f"ratio {E_TENS:.0f} / {H_A} = {E_TENS / H_A:.0f}", "label2", I["primary"], "end"))
    lg, _ = legend(s, 10, 310, [(sw_rect(CART[0], CART[1]), "matrix"), (sw_fibre, "collagen fibre"),
                                (sw_brush, "proteoglycan gel")], gap=14)
    o.append(lg)
    aria = (f"Problem C6 setup. Left: a cartilage strip stretched at both ends; its collagen fibres pull taut, so it is "
            f"stiff in tension, E tens about {E_TENS:.0f} megapascal. Right: the strip squeezed from above and below; "
            f"the fibres buckle and only the swollen proteoglycan gel resists, so it is soft in compression, H A about "
            f"{H_A} megapascal. Below, the two moduli as bars on one scale: 12 against 0.6 megapascal, a ratio of 20.")
    assert abs(E_TENS / H_A - 20) < 1e-9
    return finish(VB, aria, s, o, extra=H.hover_attr(P.box, hv))


# ================================================================ svg 35 (C8): the vicious cycle
def fig35():
    p = "m4f35_"
    VB = (0, 0, 400, 262)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [defs(p, s)]
    k = it("k")
    boxes = [((106, 6, 188, 52), [f"matrix damage: {k} rises", "charge loss, collagen disruption"]),
             ((236, 102, 162, 58), [f"fluid drains faster: {it('F')} sags", f"{it('τ')} = h²/(H{H.sub('A', s, 'label2')}{k}) shorter"]),
             ((106, 204, 188, 52), ["solid stress and friction rise", f"μ{H.sub('eff', s, 'label2')} = μ{H.sub('eq', s, 'label2')}(1 − {it('F')})"]),
             ((2, 102, 162, 58), ["surface abrades,", "fibrillates (“wear”)"])]
    for (x, y, w, h), (l1, l2) in boxes:
        o.append(box(s, x, y, w, h, accent=O["force"]))
        o.append(H.label(s, x + w / 2 + 2, y + h / 2 - 3, l1, "label2", I["primary"], "middle"))
        o.append(H.label(s, x + w / 2 + 2, y + h / 2 + 14, l2, "label2", I["secondary"], "middle"))
    o.append(curved(s, p, 296, 32, 330, 40, 330, 98))
    o.append(curved(s, p, 330, 164, 330, 222, 298, 230))
    o.append(curved(s, p, 104, 230, 70, 222, 70, 164))
    o.append(curved(s, p, 70, 98, 70, 40, 102, 32))
    o.append(H.label(s, 200, 127, "positive", "label2", I["primary"], "middle"))
    o.append(H.label(s, 200, 143, "feedback", "label2", I["primary"], "middle"))
    aria = ("Problem C8: osteoarthritis as a loop of four stages. Matrix damage (charge loss, collagen disruption) "
            "raises the permeability k; fluid drains faster and the fluid load support F sags, because the gel time "
            "tau = h squared over H A k is shorter; solid stress and friction rise, mu eff = mu eq times (1 minus F); "
            "the surface abrades and fibrillates, which is the wear, and that damages more matrix. Each pass feeds the "
            "next: positive feedback.")
    return finish(VB, aria, s, o)


# ================================================================ svg 36 (C9): 1 mm vs 2 mm, path squared
def plug(s, p, x0, x1, ytop, ybot, drained_top=True, drained_bot=False, water=True):
    """Confined-compression plug: cartilage between impermeable walls; porous platen where drained."""
    o = [rect(x0, ytop, x1 - x0, ybot - ytop, CART[0], CART[1], 1.0)]
    if water:
        o.append(dots([(x, y) for y in range(int(ytop) + 8, int(ybot) - 4, 11) for x in range(int(x0) + 8, int(x1) - 4, 11)],
                      1.9, T["fluid"][0], FL, 0.6))
    o.append(walls(s, x0 - 1, x1 + 1, ytop - 14, ybot + (14 if drained_bot else 0)))
    if drained_top:
        o.append(platen(s, x0, x1, ytop - 8))
    if drained_bot:
        o.append(platen(s, x0, x1, ybot))
    else:
        o.append(sealed(s, x0 - 1, x1 + 1, ybot))
    return "".join(o)


def fig36():
    p = "m4f36_"
    VB = (0, 0, 400, 280)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [defs(p, s)]
    mm, yb = 52.0, 170.0                      # 52 px per mm; both plugs on one base line
    for cx, hmm in ((110, 1), (290, 2)):
        x0, x1, yt = cx - 40, cx + 40, yb - hmm * mm
        o.append(plug(s, p, x0, x1, yt, yb))
        for dx in (-22, 0, 22):
            o.append(flow(s, p, cx + dx, yt - 10, cx + dx, yt - 26))
        o.append(H.arrow(s, p, x0 - 14, yb - 1, x0 - 14, yt + 1, "geometry", both=True))
        o.append(H.label(s, x0 - 20, (yt + yb) / 2 + 5, f"{hmm} mm", "label2", I["primary"], "end"))
    o.append(H.label(s, 200, 18, "same tissue, same D; drained top, sealed base", "label2", I["secondary"], "middle"))
    # gel time to one scale: tau = h^2 / D, so 1 : 4 (lines 1598, 1615)
    t1 = 52.0
    o.append(H.label(s, 20, 206, f"gel time {it('τ')} = h²/D:", "label2", I["primary"]))
    for k, hmm in enumerate((1, 2)):
        y = 226 + 20 * k
        o.append(H.arrow(s, p, 130, y, 130 + t1 * hmm ** 2, y, "geometry", both=True))
        o.append(H.label(s, 124, y + 5, f"{hmm} mm", "label2", I["secondary"], "end"))
        o.append(H.label(s, 136 + t1 * hmm ** 2, y + 5, it("τ") if k == 0 else f"4{it('τ')}", "label2", I["primary"]))
    o.append(H.label(s, 20, 272, "path doubled → time ×4", "label2", I["secondary"]))
    lg, _ = legend(s, 214, 272, [(sw_dot(T["fluid"][0], FL), "water"), (sw_flow, "flow out")], gap=12)
    o.append(lg)
    aria = ("Problem C9 setup: two confined plugs of the same cartilage, 1 millimetre and 2 millimetres thick, drawn to "
            "scale, each drained through a porous platen on top over a sealed base. The fluid in the thicker plug must "
            "travel twice as far. Below, the gel times tau = h squared over D to one scale: tau for 1 millimetre, 4 tau "
            "for 2 millimetres.")
    return finish(VB, aria, s, o)


# ================================================================ svg 37 (C10): daily fluid loss and recovery
def fig37():
    p = "m4f37_"
    VB = (0, 0, 400, 346)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [defs(p, s)]
    art, M = knee(p, (146, 214, 110, 92), 8, 8, 1.0)
    o.append(art)
    zx, zy = M((190, 274))
    o.append(rect(zx - 12, zy - 8, 24, 14, "none", O["geometry"], 1.4, 2))
    o.append(H.label(s, 128, 26, "the layer that thins (boxed): articular", "label2", I["primary"]))
    o.append(H.label(s, 128, 42, "cartilage, and the spinal discs", "label2", I["primary"]))
    o.append(H.label(s, 128, 58, "(most of the height change)", "label2", I["secondary"]))
    # three snapshots of the same layer through a day
    yb, th0, th1, hw = 204.0, 34.0, 23.0, 45.0
    snaps = [(60, th0, "morning", "full thickness"), (200, th1, "evening", "thinner: fluid out"),
             (340, th0, "next morning", "recovered")]
    for cx, th, t1, t2 in snaps:
        x0, x1 = cx - hw, cx + hw
        o.append(rect(x0, yb - th, 2 * hw, th, CART[0], CART[1], 1.0))
        n = 3 if th > 30 else 2
        o.append(dots([(x, yb - th + 6 + j * (th - 10) / max(1, n - 1)) for j in range(n)
                       for x in range(int(x0) + 7, int(x1) - 3, 11)], 1.9, T["fluid"][0], FL, 0.6))
        o.append(H.line(s, x0 - 4, yb, x1 + 4, yb, T["bone"][1], "geom"))
        o.append(H.label(s, cx, 124, t1, "label", I["primary"], "middle"))
        o.append(H.label(s, cx, yb + 22, t2, "label2", I["secondary"], "middle"))
    o.append(H.arrow(s, p, 104, 119, 150, 119, "dim", w="ref"))
    o.append(H.arrow(s, p, 246, 119, 284, 119, "dim", w="ref"))
    o.append(H.label(s, 127, 110, "day", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 265, 110, "night", "label2", I["secondary"], "middle"))
    o.append(H.arrow(s, p, 200, 138, 200, yb - th1 - 3, "load"))
    o.append(H.label(s, 207, 152, "body weight", "label2", I["secondary"]))
    for sg in (-1, 1):
        o.append(flow(s, p, 200 + sg * (hw + 1), yb - th1 / 2, 200 + sg * (hw + 17), yb - th1 / 2))
    for x in (312, 340, 368):
        o.append(flow(s, p, x, 146, x, yb - th0 - 2))
    o.append(H.label(s, 340, 141, f"{it('π')} draws water in", "label2", I["primary"], "middle"))
    o.append(H.label(s, 8, 258, f"Reversible while the fixed charge, and so {it('π')}, survives. If the", "label2", I["primary"]))
    o.append(H.label(s, 8, 274, f"charge is lost, {it('π')} → 0: water is not drawn back, the layer", "label2", I["primary"]))
    o.append(H.label(s, 8, 290, "stays thin and ratchets down (K9).", "label2", I["primary"]))
    cr, n = credit_dbcls(s, 8, 312)
    o.append(cr)
    aria = ("Problem C10 setup. Top left: the knee in sagittal section, with a box on the articular cartilage of the "
            "tibial plateau; the spinal discs behave the same way and give most of the height change. Below, three "
            "snapshots of the cartilage layer: in the morning it has its full thickness; after a day under body weight "
            "fluid has exuded and it is thinner; unloaded overnight the swelling pressure pi draws water back in and "
            "by the next morning it has recovered. The cycle is reversible while the fixed charge, and so pi, "
            "survives; if the charge is lost, water is not drawn back and the layer stays thin.")
    return finish(VB, aria, s, o)


# ================================================================ svg 38 (D1): one face vs both faces drained
def fig38():
    p = "m4f38_"
    VB = (0, 0, 400, 300)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [defs(p, s)]
    yt, yb, A = 56.0, 206.0, 58.0
    Z = lambda z: yb - z * (yb - yt)          # noqa: E731   z = height above the base / h
    for x0, title, both in ((54, "one face drained", False), (244, "both faces drained", True)):
        x1 = x0 + 56
        o.append(plug(s, p, x0, x1, yt, yb, True, both, water=False))
        o.append(H.label(s, (x0 + x1) / 2 + 40, 22, title, "label", I["primary"], "middle"))
        for dx in (-16, 0, 16):
            o.append(flow(s, p, (x0 + x1) / 2 + dx, yt - 10, (x0 + x1) / 2 + dx, yt - 24))
            if both:
                o.append(flow(s, p, (x0 + x1) / 2 + dx, yb + 10, (x0 + x1) / 2 + dx, yb + 24))
        # fundamental pressure mode beside the plug (D1 solution, line 1691)
        xz = x1 + 10
        o.append(H.line(s, xz, yt, xz, yb, I["rule"], "leader"))
        zs = [k / 100 for k in range(101)]
        if both:
            ps = [math.sin(math.pi * z) for z in zs]               # sin(pi z / h): zero at both faces
        else:
            ps = [math.cos(math.pi * z / 2) for z in zs]           # cos(pi z / 2h): peak at the sealed base, zero on top
        pts = " ".join(f"{xz + A * q:.1f},{Z(z):.1f}" for z, q in zip(zs, ps))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{H.SERIES[0]}" stroke-width="{s(H.PX["curve"]):.2f}"/>')
        o.append(H.label(s, xz + A + 6, Z(0.5) + 5 if both else Z(0.12), f"{it('p')}(z)", "label2", I["primary"]))
        if both:
            o.append(H.line(s, x0 - 22, Z(0.5), x1, Z(0.5), O["dim"], "leader", H.DASH_REF))
            o.append(H.arrow(s, p, x0 - 14, Z(0.5) - 1, x0 - 14, yt + 1, "geometry", both=True))
            o.append(H.arrow(s, p, x0 - 14, Z(0.5) + 1, x0 - 14, yb - 1, "geometry", both=True))
            for zz in (0.75, 0.25):
                o.append(H.label(s, x0 - 20, Z(zz) + 5, "h/2", "label2", I["primary"], "end"))
            o.append(H.label(s, 296, 248, f"mode sin(πz/h), λ{H.sub('1', s, 'label2')} = π/h", "label2", I["primary"],
                             "middle"))
            o.append(H.label(s, 296, 266, f"τ{H.sub('2', s, 'label2')} = h²/(π²D) = τ{H.sub('1', s, 'label2')}/4",
                             "label2", I["primary"], "middle"))
            o.append(H.label(s, 296, 284, "path halved → time ÷4", "label2", I["secondary"], "middle"))
        else:
            o.append(H.arrow(s, p, x0 - 14, yb - 1, x0 - 14, yt + 1, "geometry", both=True))
            o.append(H.label(s, x0 - 20, Z(0.5) + 5, "h", "label2", I["primary"], "end"))
            o.append(H.label(s, x0 - 4, yb + 14, "sealed", "label2", I["secondary"], "end"))
            o.append(H.label(s, 100, 248, f"mode cos(πz/2h), λ{H.sub('1', s, 'label2')} = π/2h", "label2", I["primary"],
                             "middle"))
            o.append(H.label(s, 100, 266, f"τ{H.sub('1', s, 'label2')} = 4h²/(π²D)", "label2", I["primary"], "middle"))
    o.append(H.line(s, 196, 10, 196, 292, GRID, "leader"))
    aria = ("Problem D1 setup: two confined plugs of thickness h. Left: drained through a porous platen on top, sealed "
            "base; the fundamental pressure mode p(z) = cos(pi z over 2h) peaks at the sealed base and is zero at the "
            "drain, lambda 1 = pi over 2h, and the drainage path is the full thickness h: tau 1 = 4 h squared over pi "
            "squared D. Right: drained on both faces; the mode sin(pi z over h) is zero at both faces and peaks at "
            "mid-depth, lambda 1 = pi over h, and the path is h over 2 to either face: tau 2 = h squared over pi "
            "squared D = tau 1 over 4.")
    return finish(VB, aria, s, o)


# ================================================================ svg 39 (D2): Donnan, two compartments
def scatter(rnd, n, box_, dmin, avoid=(), tries=20000):
    x0, y0, x1, y1 = box_
    pts = []
    for _ in range(tries):
        if len(pts) == n:
            break
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if all(math.hypot(x - a, y - b) >= dmin for a, b in pts) and all(f(x, y) for f in avoid):
            pts.append((x, y))
    assert len(pts) == n, (n, len(pts))
    return pts


def fig39():
    p = "m4f39_"
    VB = (0, 0, 400, 330)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [defs(p, s)]
    cp, cm, ex, pi = donnan()
    per = 100                                    # dots per mol/L in each compartment (1 dot = 0.01 M)
    n_cp, n_cm, n_f, n_b = round(cp * per), round(cm * per), round(C_F * per), round(C_0 * per)
    assert (n_cp, n_cm, n_f, n_b) == (28, 8, 20, 15) and n_cp == n_cm + n_f      # electroneutral in dots too
    T0, B0, Y0, Y1 = (10.0, 190.0), (210.0, 390.0), 40.0, 184.0
    o.append(rect(T0[0], Y0, T0[1] - T0[0], Y1 - Y0, CART[0], CART[1], 1.2, 4))
    o.append(rect(B0[0], Y0, B0[1] - B0[0], Y1 - Y0, "#fff", T["fluid"][1], 1.2, 4))
    o.append(H.line(s, 200, Y0 - 6, 200, Y1 + 6, I["axis"], "ref", (3, 3)))
    o.append(H.label(s, 100, 26, "tissue", "label", I["primary"], "middle"))
    o.append(H.label(s, 300, 26, "bath", "label", I["primary"], "middle"))
    o.append(H.label(s, 200, Y1 + 22, "membrane: ions pass, fixed charge cannot", "label2", I["secondary"], "middle"))
    # fixed charges on four proteoglycan chains (5 each = 20 = 0.20 M)
    xs = (38, 82, 126, 170)
    charges = 0
    for xb in xs:
        b, tips = brush(xb, Y0 + 22, Y0 + 22 + 5 * 9.0 + 2, step=9.0, arm=7)
        o.append(b)
        charges += len(tips)
    assert charges == n_f, charges
    band = lambda x, y: not (Y0 + 10 < y < Y0 + 84 and any(abs(x - xb) < 19 for xb in xs))   # noqa: E731
    mid = lambda x, y: not (abs(y - 112) < 12 and abs(x - 200) < 34)                          # noqa: E731
    low = lambda x, y: y < Y1 - 24                                                             # noqa: E731
    rnd = random.Random(7)
    tis = scatter(rnd, n_cp + n_cm, (T0[0] + 9, Y0 + 9, T0[1] - 9, Y1 - 9), 12.5, (band, mid, low))
    bat = scatter(rnd, 2 * n_b, (B0[0] + 9, Y0 + 9, B0[1] - 9, Y1 - 9), 15.0, (mid, low))
    o.extend(ion(x, y, +1) for x, y in tis[:n_cp])
    o.extend(ion(x, y, -1) for x, y in tis[n_cp:])
    o.extend(ion(x, y, +1 if k % 2 == 0 else -1) for k, (x, y) in enumerate(bat))
    o.append(flow(s, p, 226, 112, 172, 112, "force"))
    o.append(H.label(s, 100, Y1 - 6, f"{n_cp} Na⁺, {n_cm} Cl⁻, {n_f} fixed −", "label2", I["primary"], "middle"))
    o.append(H.label(s, 300, Y1 - 6, f"{n_b} Na⁺, {n_b} Cl⁻", "label2", I["primary"], "middle"))
    lines = [f"electroneutrality: c{H.sub('+', s, 'label2')} = c{H.sub('−', s, 'label2')} + c{H.sub('F', s, 'label2')};   Donnan: c{H.sub('+', s, 'label2')}c{H.sub('−', s, 'label2')} = c₀²",
             f"c{H.sub('F', s, 'label2')} = {C_F} M, c₀ = {C_0} M  ⇒  c{H.sub('+', s, 'label2')} = {cp:.3f} M, c{H.sub('−', s, 'label2')} = {cm:.3f} M",
             f"{it('π')} = R{H.sub('g', s, 'label2')}Θ(c{H.sub('+', s, 'label2')} + c{H.sub('−', s, 'label2')} − 2c₀) = {R_G * THETA:.0f} J/mol × "
             f"{ex * 1e3:.1f} mol/m³ ≈ {pi / 1e6:.2f} MPa"]
    for k, t in enumerate(lines):
        o.append(H.label(s, 10, 232 + 18 * k, t, "label2", I["primary"]))
    lg, _ = legend(s, 10, 300, [(sw_ion(+1), "Na⁺"), (sw_ion(-1), "Cl⁻"), (sw_brush, "fixed charge"),
                                (sw_flow, "water drawn in")], gap=14)
    o.append(lg)
    o.append(H.label(s, 10, 320, "Dots per area: 1 dot = 0.01 M. Na⁺ × Cl⁻: 28 × 8 = 224 ≈ 15² = 225.",
                     "label2", I["secondary"]))
    assert abs(n_cp * n_cm - n_b ** 2) <= 1
    aria = (f"Problem D2 setup: a charged tissue and a salt bath across a membrane that passes ions but not the fixed "
            f"charge. Dots per area show concentrations, one dot per 0.01 molar: the tissue holds 20 fixed negative "
            f"charges on proteoglycan chains, 28 sodium and 8 chloride ions; the bath holds 15 of each. "
            f"Electroneutrality c plus = c minus + c F and Donnan equilibrium c plus times c minus = c0 squared give, "
            f"for c F = 0.2 and c0 = 0.15 molar, c plus = {cp:.3f} and c minus = {cm:.3f} molar. The ion excess, "
            f"{ex * 1e3:.1f} moles per cubic metre, draws water in: pi = R g Theta times the excess, about "
            f"{pi / 1e6:.2f} megapascal.")
    return finish(VB, aria, s, o)


# ================================================================ svg 40 (D3): control slab, Darcy flux
def fig40():
    p = "m4f40_"
    VB = (0, 0, 400, 316)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [defs(p, s)]
    x0, x1, yt, yb = 64.0, 160.0, 56.0, 216.0
    o.append(plug(s, p, x0, x1, yt, yb, water=False))
    for x in (82, 112, 142):
        o.append(H.arrow(s, p, x, 14, x, yt - 11, "load"))
    o.append(H.label(s, x1 + 8, 30, f"{it('σ')} held constant", "label2", I["primary"]))
    zs0, zs1 = 128.0, 156.0
    o.append(rect(x0, zs0, x1 - x0, zs1 - zs0, T["fluid"][0], FL, 1.0, extra='fill-opacity="0.55"'))
    o.append(flow(s, p, 112, zs1 + 24, 112, zs1 + 2, "force"))
    o.append(flow(s, p, 112, zs0 + 2, 112, zs0 - 22, "force"))
    o.append(H.label(s, 120, zs1 + 22, f"{it('q')}(z)", "label2", I["primary"]))
    o.append(H.label(s, 120, zs0 - 10, f"{it('q')}(z + dz)", "label2", I["primary"]))
    o.append(H.arrow(s, p, x1 + 12, zs1, x1 + 12, zs0, "geometry", both=True))
    o.append(H.label(s, x1 + 18, (zs0 + zs1) / 2 + 5, "dz", "label2", I["primary"]))
    o.append(H.arrow(s, p, 30, yb, 30, yt - 4, "dim", w="ref"))
    o.append(H.label(s, 30, yt - 12, it("z"), "label", I["primary"], "middle"))
    o.append(H.label(s, (x0 + x1) / 2, yb + 26, "sealed base", "label2", I["secondary"], "middle"))
    sb = lambda t: H.sub(t, s, "label2")      # noqa: E731
    rows = [("(i) kinematics:", "ε = ∂u/∂z"),
            (f"(ii) σ = σ{sb('E')} − {it('p')} fixed:", f"σ{sb('E')} = H{sb('A')}ε ⇒ H{sb('A')} ∂ε/∂t = ∂{it('p')}/∂t"),
            ("(iii) continuity:", f"∂ε/∂t = −∂{it('q')}/∂z"),
            ("(iv) Darcy:", f"{it('q')} = −{it('k')} ∂{it('p')}/∂z")]
    y = 72
    for a, b in rows:
        o.append(H.label(s, 214, y, a, "label2", I["primary"]))
        o.append(H.label(s, 226, y + 16, b, "label2", I["primary"]))
        y += 38
    o.append(box(s, 10, 246, 380, 58, accent=O["geometry"]))
    o.append(H.label(s, 22, 268, f"(ii) into (iii) + (iv): ∂{it('p')}/∂t = H{sb('A')}{it('k')} ∂²{it('p')}/∂z², and so",
                     "label2", I["primary"]))
    o.append(H.label(s, 22, 292, f"∂u/∂t = H{H.sub('A', s)}{it('k')} ∂²u/∂z²,   D ≡ H{H.sub('A', s)}{it('k')}", "label",
                     I["primary"]))
    lg, _ = legend(s, 214, 228, [(sw_flow, "Darcy flux q")], gap=8)
    o.append(lg)
    aria = ("Problem D3 setup: a confined cartilage plug under a constant applied stress sigma on a porous platen, "
            "sealed at the base, with the z axis upward. A control slab of thickness dz is shaded; the Darcy flux q(z) "
            "enters its lower face and q(z + dz) leaves its upper face. The four ingredients: (i) kinematics epsilon = "
            "du/dz; (ii) total stress sigma = sigma E minus p held fixed with sigma E = H A epsilon, so H A depsilon/dt "
            "= dp/dt; (iii) continuity depsilon/dt = minus dq/dz; (iv) Darcy q = minus k dp/dz. Combined: du/dt = H A k "
            "d2u/dz2, with D = H A k.")
    return finish(VB, aria, s, o)


# ================================================================ svg 45 (D8): friction rides the solid share
def fig45():
    p = "m4f45_"
    VB = (0, 0, 400, 384)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [defs(p, s)]
    x0, x1 = 30.0, 370.0
    yu0, yu1, yl0, yl1 = 58.0, 84.0, 94.0, 120.0
    o.append(rect(x0, yl0 - 10, x1 - x0, 10, T["fluid"][0], extra='opacity="0.8"'))
    o.append(rect(x0, yu0, x1 - x0, yu1 - yu0, CART[0], CART[1], 1.2))
    o.append(rect(x0, yl0, x1 - x0, yl1 - yl0, CART[0], CART[1], 1.2))
    spots = (88, 168, 248, 328)
    for x in spots:
        o.append(rect(x - 6, yu1 - 1, 12, yl0 - yu1 + 2, CART[0], CART[1], 1.0))
        o.append(H.arrow(s, p, x + 4, yu1 - 8, x - 16, yu1 - 8, "force"))
    o.append(H.arrow(s, p, 200, 12, 200, yu0 - 3, "load"))
    o.append(H.label(s, 208, 28, it("N"), "label", I["primary"]))
    o.append(H.arrow(s, p, x1 - 60, 40, x1, 40, "dim", w="ref"))
    o.append(H.label(s, x1 - 66, 45, f"sliding {it('v')}", "label2", I["secondary"], "end"))
    o.append(lead(s, 128, 89, 128, 146))
    o.append(H.label(s, 30, 160, f"fluid pressure: {it('F')}{it('N')}, no shear", "label2", I["primary"]))
    o.append(lead(s, 248, 89, 262, 146))
    o.append(H.label(s, 236, 160, f"solid contact: (1 − {it('F')}){it('N')},", "label2", I["primary"]))
    o.append(H.label(s, 236, 176, "friction only here", "label2", I["primary"]))
    mu = lambda t: f"μ{H.sub(t, s)}"           # noqa: E731
    o.append(H.label(s, 200, 204, f"{it('f')} = {mu('eq')}(1 − {it('F')}){it('N')}  ⇒  {mu('eff')} = {it('f')}/{it('N')} = "
                     f"{mu('eq')}(1 − {it('F')})", "label", I["primary"], "middle"))
    # the law itself, with the measured range (line 1845): F = 1 - mu / mu_eq
    P = Plot(s, (64, 232, 384, 316), (0, 1), (0, 0.18))
    o.append(P.axes([(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1)], [(v, f"{v:g}") for v in (0, 0.05, 0.1, 0.15)],
                    f"fluid load fraction {it('F')}", f"μ{H.sub('eff', s, 'label2')}", grid=(0.05, 0.1, 0.15), ytx=22))
    fa, fb = 1 - MU_MEAS[1] / MU_EQ, 1 - MU_MEAS[0] / MU_EQ
    o.append(rect(P.X(fa), P.y1, P.X(fb) - P.X(fa), P.y0 - P.y1, H.SERIES[1], extra='opacity="0.18"'))
    Fs = [k / 200 for k in range(201)]
    o.append(P.curve(Fs, [MU_EQ * (1 - F) for F in Fs], H.SERIES[0]))
    o.append(H.label(s, P.X(0.06), P.Y(0.163), f"drained, {it('F')} = 0: μ{H.sub('eq', s, 'label2')} ≈ {MU_EQ}", "label2",
                     I["primary"]))
    o.append(H.label(s, P.X(fa) - 6, P.Y(0.118), f"measured μ {MU_MEAS[0]}–{MU_MEAS[1]}", "label2", I["primary"], "end"))
    o.append(H.label(s, P.X(fa) - 6, P.Y(0.093), f"⇒ {it('F')} ≈ {fa:.2f}–{fb:.2f}", "label2", I["primary"], "end"))
    pts = hov(P, Fs, [[MU_EQ * (1 - F) for F in Fs]], lambda i: f"F = {Fs[i]:.3f}: μ eff = {MU_EQ * (1 - Fs[i]):.4f}")
    lg, _ = legend(s, 10, 378, [(sw_rect(CART[0], CART[1]), "cartilage"), (sw_rect(T["fluid"][0]), "pressurised fluid"),
                                (sw_rect(H.SERIES[1], op=0.3), "measured range")], gap=14)
    o.append(lg)
    assert (round(fa, 2), round(fb, 2)) == (0.87, 0.97)
    aria = (f"Problem D8 setup: two cartilage layers in sliding contact under a normal load N. Pressurised interstitial "
            f"fluid between them carries the share F N and no shear; solid contact spots carry (1 minus F) N and alone "
            f"transmit friction, f = mu eq (1 minus F) N, so mu eff = f over N = mu eq (1 minus F). Below, mu eff "
            f"against F falls linearly from mu eq about {MU_EQ} at F = 0 to 0 at F = 1; the measured friction "
            f"coefficients {MU_MEAS[0]} to {MU_MEAS[1]} correspond to F about {fa:.2f} to {fb:.2f}, shaded.")
    return finish(VB, aria, s, o, extra=H.hover_attr(P.box, pts))


# ================================================================ svg 47 (D10): loop gain G
def fig47():
    p = "m4f47_"
    VB = (0, 0, 400, 380)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [defs(p, s)]
    k, d = it("k"), it("d")
    bx = [(2, "support drops:", f"{d} = 1 − {it('F')} rises"), (138, "more solid stress,", "friction, wear"),
          (274, "matrix damage:", f"{k} rises")]
    for x, l1, l2 in bx:
        o.append(box(s, x, 18, 124, 48, accent=O["force"]))
        o.append(H.label(s, x + 65, 38, l1, "label2", I["primary"], "middle"))
        o.append(H.label(s, x + 65, 55, l2, "label2", I["secondary"], "middle"))
    o.append(H.arrow(s, p, 127, 42, 137, 42, "dim", w="ref"))
    o.append(H.arrow(s, p, 263, 42, 273, 42, "dim", w="ref"))
    o.append(curved(s, p, 336, 68, 200, 118, 64, 70))
    o.append(H.label(s, 200, 116, f"× {it('G')} per pass round the loop", "label2", I["primary"], "middle"))
    o.append(H.label(s, 200, 134, f"first factor, exact (D4): ∂ln {d}/∂ln {k} = ½", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 200, 152, f"the other two are assumed: {it('G')} > 1 needs them > 2", "label2", I["secondary"], "middle"))
    # x_n = G^n x_0 (D10 solution, line 1889); G values are illustrative, on either side of the threshold
    G = (1.25, 1.0, 0.8)
    P = Plot(s, (60, 196, 330, 336), (0, 8), (0, 6))
    o.append(P.axes([(n, str(n)) for n in range(9)], [(v, str(v)) for v in range(7)], f"pass {it('n')}",
                    f"deficit {it('x')}{H.sub('n', s, 'label2')}/{it('x')}{H.sub('0', s, 'label2')}", grid=(2, 4, 6), ytx=20))
    ns = list(range(9))
    cols = (H.SERIES[0], I["rule"], H.SERIES[1])
    for g, col in zip(G, cols):
        o.append(P.curve(ns, [g ** n for n in ns], col, multi=True, dash=H.DASH_REF if g == 1 else None))
        o.extend(P.dot(n, g ** n, col) for n in ns)
    o.append(H.label(s, P.X(8) + 8, P.Y(G[0] ** 8) + 5, "G = 1.25", "label2", I["primary"]))
    o.append(H.label(s, P.X(8) + 8, P.Y(1) + 1, "G = 1", "label2", I["primary"]))
    o.append(H.label(s, P.X(8) + 8, P.Y(G[2] ** 8) + 9, "G = 0.8", "label2", I["primary"]))
    o.append(plegend(s, 60, 174, [(cols[0], "G > 1: grows (runaway)", None), (cols[2], "G < 1: decays (heals)", None)]))
    pts = hov(P, ns, [[g ** n for n in ns] for g in G],
              lambda i: f"n = {i}: G 1.25 → {1.25 ** i:.2f}, G 1 → 1, G 0.8 → {0.8 ** i:.2f}")
    assert abs(1.25 ** 8 - 5.96) < 0.01 and abs(0.8 ** 8 - 0.168) < 0.001
    aria = ("Problem D10 setup: the degeneration loop as three boxes. Fluid support drops, so d = 1 minus F rises; "
            "more solid stress, friction and wear follow; matrix damage raises k, which feeds back to a further drop "
            "in support, times G per pass. The first factor is exact from D4: d ln d over d ln k = one half; the other "
            "two are assumed, so G > 1 needs their product above 2. Below, the deficit x n over x 0 = G to the n for "
            "eight passes with illustrative gains: G = 1.25 grows to 5.96, G = 1 stays at 1 (the threshold), G = 0.8 "
            "decays to 0.17.")
    return finish(VB, aria, s, o, extra=H.hover_attr(P.box, pts))


FIGS = {
    28: ("Two panels of a cartilage layer on bone. Left: a thumb press", fig28),
    29: ("Cartilage matrix carrying fixed negative charges on proteogl", fig29),
    30: ("A sealed water-filled chamber under a piston: because the sa", fig30),
    31: ("A fluid-film bearing needs sliding speed to build a load-bea", fig31),
    32: ("Two contact-pressure profiles carrying the same knee load: t", fig32),
    33: ("Cartilage is a composite: stiff collagen fibres resist tensi", fig33),
    35: ("The osteoarthritis cascade as a vicious cycle: rising permea", fig35),
    36: ("Two plugs of the same cartilage, one twice as thick: the thi", fig36),
    37: ("Over a day of standing the cartilage slowly loses fluid and ", fig37),
    38: ("Two confined cartilage plugs. Left: drained on the top face ", fig38),
    39: ("Two compartments across a membrane: the charged tissue with ", fig39),
    40: ("A control slab of thickness dz inside the cartilage: Darcy f", fig40),
    45: ("The normal load splits into a fluid-pressure share F that ca", fig45),
    47: ("The degeneration feedback as a loop with gain G: a small dro", fig47),
    52: ("Two contact-pressure profiles carrying the same knee load: t", fig52),
}
