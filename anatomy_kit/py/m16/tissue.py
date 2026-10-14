"""Module 16, group `tissue`: continuum-mechanics figures in the house style.

Main text (760 px): svg #2 (Fig. 1 one-dimensional models to one continuum), #3 (Fig. 2 deformation gradient),
#4 (Fig. 3 stress cube and traction), #6 (Fig. 5 bar element), #12 (the two driving gradients across a cartilage layer).
Problem figures (400 px): #26 C8, #28 C10, #44 K5, #45 K6, #49 K8, #53 K10.
Art: only the NIH NIAID BioArt 244 femur (public domain), the one fill path of the m00 crop
(crop_art.py ... m00femur), <use>d from the shared #m16art_femur (body_main.SHARED_DEFS) in #2 and #28; #53 <use>s it for the dashed unbent outline and draws the bent femur as computed geometry. Everything else is a schematic of a MODEL (spring, dashpot,
bar, cube, layer), not of anatomy. Colours: force and normal stress = SERIES[0] red, length, displacement and shear
stress = geometry blue, loads = load brown; text is ink.
Every plotted number is computed here from a value module16.html states (line numbers beside each constant; the
K-problem scripts are ported line for line and their printed numbers asserted).
"""
import math

import numpy as np

import house as H
from m00.tissue import FEMUR_ART, strand_paths, zigzag
from m05.body import finish, wrap
from m05.plots_main import Ax, axes, dot, legend, poly
from m05.plots_main import curve as _curve
from m05.tissue import circ, path, rect

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
BOX, GRID = "#f7f4ef", "#e6e6e6"
BONE, BONE_L = T["bone"]
FEMUR_L = FEMUR_ART[3] - FEMUR_ART[1]            # femur length in art units
FEMUR_W = FEMUR_ART[2] - FEMUR_ART[0]
BONE_CREDIT = H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt (Ryan Kissinger)",
                                         title="Human Upper Leg Bones (BioArt 244)",
                                         changes="Cropped to one femur, recoloured.")


def it(t):
    return f'<tspan font-style="italic">{t}</tspan>'


def sub(t, s, size="label"):
    return H.sub(t, s, size)


def ilabel(s, x, y, t, size="label", anchor="start", fill=I["primary"], extra=""):
    return H.label(s, x, y, t, size, fill, anchor, extra)


def hv(ax, xs, ys_list, fmt):
    """Hover points in user units: x, y or [y...], text. xs sorted ascending."""
    out = []
    for i, x in enumerate(xs):
        ys = [round(ax.Y(y[i]), 2) for y in ys_list]
        out.append([round(ax.X(x), 2), ys[0] if len(ys) == 1 else ys, fmt(i)])
    return out


def curve(s, ax, xs, ys, col, w="curve", dash=None, extra=""):
    """m05 curve, thinned to at most 120 points (the page-size gate)."""
    xs, ys = list(xs), list(ys)
    if len(xs) > 120:
        k = -(-len(xs) // 120)
        keep = list(range(0, len(xs), k)) + ([len(xs) - 1] if (len(xs) - 1) % k else [])
        xs, ys = [xs[i] for i in keep], [ys[i] for i in keep]
    return _curve(s, ax, xs, ys, col, w, dash, extra)


def ref_dash(s, x1, y1, x2, y2, col=I["rule"]):
    return H.line(s, x1, y1, x2, y2, col, "ref", H.DASH_REF)


# ================================================================ model icons (shared by #2 and #28)
def femur_h(s, x, yc, length):
    """The NIH femur lying horizontal, head on the left, from x to x + length, centred on yc (a <use> of the shared #m16art_femur from body_main.SHARED_DEFS)."""
    k = length / FEMUR_L
    cx = FEMUR_ART[0] + FEMUR_W / 2
    return (f'<use href="#m16art_femur" fill="{BONE}" stroke="{BONE_L}" stroke-width="{s(H.PX["art_line"]) / k:.2f}" '
            f'stroke-linejoin="round" transform="translate({x:.2f} {yc:.2f}) rotate(-90) scale({k:.5f}) '
            f'translate({-cx:.2f} {-FEMUR_ART[1]:.2f})"/>')


def beam_icon(s, p, x0, x1, yc, sag=14.0):
    """Euler-Bernoulli beam: a line (neutral axis) on two supports, a transverse load, the sagged shape dashed."""
    o = [H.line(s, x0, yc, x1, yc, I["primary"], "axis")]
    for x in (x0, x1):
        o.append(path(f"M{x:.1f},{yc + 1:.1f} l-6,10 h12 Z", I["axis"], s(1.2), fill=GRID))
    xm = (x0 + x1) / 2
    pts = [(x0 + (x1 - x0) * u / 40, yc + sag * math.sin(math.pi * u / 40)) for u in range(41)]
    o.append(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{I["rule"]}" '
             f'stroke-width="{s(H.PX["ref"]):.2f}" stroke-dasharray="{s(H.DASH_REF[0]):.1f} {s(H.DASH_REF[1]):.1f}"/>')
    o.append(H.arrow(s, p, xm, yc - 32, xm, yc - 3, "load"))
    return "".join(o)


def spring_icon(s, x0, x1, yc, amp=8.0, n=7):
    return path(zigzag(x0, x1, yc, n, amp, 14.0), I["primary"], s(H.PX["geom"]), extra='stroke-linejoin="round"')


def tendon_icon(s, x0, x1, yc):
    """Collagen strands as rope (m00 idiom): the tissue the spring stands for."""
    return strand_paths(x0, x1, yc, 5.0, 48.0, [0.0, 2.1, 4.2], s(7), s(4))


def cartilage_icon(s, x0, x1, yc, h=40.0):
    """A cartilage layer: matrix in the cartilage token, pores filled with fluid blue."""
    o = [rect(x0, yc - h / 2, x1 - x0, h, T["cartilage"][0], T["cartilage"][1], s(1.2), s(4))]
    for i in range(int((x1 - x0) // 14) - 1):
        for j in range(int(h // 13) - 1):
            o.append(circ(x0 + 12 + 14 * i + (7 if j % 2 else 0), yc - h / 2 + 11 + 13 * j, s(2.4),
                          T["fluid"][0], T["fluid"][1], s(0.6)))
    return "".join(o)


def kelvin_icon(s, x0, x1, yc, gap=16.0):
    """Spring and dashpot side by side between two plates (the cartilage column of Module 4)."""
    w = s(H.PX["geom"])
    ink = I["primary"]
    xm = (x0 + x1) / 2
    o = [H.line(s, x0, yc - gap - 6, x0, yc + gap + 6, ink, "axis"), H.line(s, x1, yc - gap - 6, x1, yc + gap + 6, ink, "axis")]
    o.append(path(zigzag(x0, x1, yc - gap, 6, 6.0, 12.0), ink, w, extra='stroke-linejoin="round"'))
    ya = yc + gap
    cyl = f"M{xm + 8:.1f},{ya - 8:.1f} H{xm - 14:.1f} V{ya + 8:.1f} H{xm + 8:.1f}"
    o.append(H.line(s, x0, ya, xm - 14, ya, ink, "geom"))
    o.append(path(cyl, ink, w, extra='stroke-linejoin="round"'))
    o.append(H.line(s, xm - 2, ya - 5, xm - 2, ya + 5, ink, "geom"))
    o.append(H.line(s, xm - 2, ya, x1, ya, ink, "geom"))
    return "".join(o)


# ================================================================ the stress cube (#2, #4)
def cube(s, p, x0, y0, a, full=True, labels=True):
    """Isometric stress element. (x0, y0) = bottom-left of the front face, a = edge in user units.
    Normals (red) on the three visible faces; shear (blue): one per face (full=False) or the three complementary
    pairs (full=True: tau_zx/tau_xz, tau_zy/tau_yz, tau_yx/tau_xy, positive faces, positive directions)."""
    dx, dy = 0.42 * a, -0.36 * a                       # screen shift per unit of depth (away from the viewer)

    def P(x, y, z):                                    # x right, y up, z toward the viewer, each 0..1
        d = 1 - z
        return x0 + a * x + dx * d, y0 - a * y + dy * d
    zl = math.hypot(dx, dy)
    E = {"x": (1.0, 0.0), "y": (0.0, -1.0), "z": (-dx / zl, -dy / zl)}      # screen unit vectors

    def face(pts, fill):
        return (f'<polygon points="{" ".join("%.1f,%.1f" % P(*q) for q in pts)}" fill="{fill}" '
                f'stroke="{I["secondary"]}" stroke-width="{s(1.3):.2f}" stroke-linejoin="round"/>')
    o = [face([(0, 1, 1), (1, 1, 1), (1, 1, 0), (0, 1, 0)], T["tendon"][0]),
         face([(1, 0, 1), (1, 0, 0), (1, 1, 0), (1, 1, 1)], T["marrow"][0]),
         face([(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)], BOX)]
    labs = []

    def vec(pt, ax, length, meaning, text, lab_off):
        x, y = P(*pt)
        ex, ey = E[ax]
        x2, y2 = x + ex * length, y + ey * length
        o.append(H.arrow(s, p, x, y, x2, y2, meaning, w="force" if meaning == "force" else "geom"))
        labs.append((x2 + lab_off[0], y2 + lab_off[1], text))

    nl = 0.34 * a
    sg = "σ"
    ta = "τ"

    def L(sym, ij):
        return f'{it(sym)}{sub(ij, s)}' if full else it(sym)
    # normals, from the centre of each visible face, outward
    vec((1, .62, .5), "x", nl, "force", L(sg, "xx"), (6, 5))
    vec((.72, 1, .5), "y", nl, "force", L(sg, "yy"), (-4, -6))
    vec((.66, .62, 1), "z", nl, "force", L(sg, "zz"), (-6, 16))
    sl = 0.30 * a
    if full:
        vec((.36, .12, 1), "x", sl, "geometry", L(ta, "zx"), (6, 4))
        vec((.12, .12, 1), "y", sl, "geometry", L(ta, "zy"), (-26, -4))
        vec((.06, 1, .3), "x", sl * 0.9, "geometry", L(ta, "yx"), (6, -4))
        vec((.06, 1, .42), "z", sl * 0.9, "geometry", L(ta, "yz"), (-28, 14))
        vec((1, .1, .3), "y", sl * 0.9, "geometry", L(ta, "xy"), (6, 0))
        vec((1, .1, .42), "z", sl * 0.9, "geometry", L(ta, "xz"), (-28, 14))
    else:
        vec((.5, .12, 1), "x", sl, "geometry", L(ta, ""), (6, 4))
        vec((.06, 1, .3), "x", sl * 0.9, "geometry", L(ta, ""), (6, -4))
        vec((1, .1, .3), "y", sl * 0.9, "geometry", L(ta, ""), (6, 0))
    for x, y, t in (labs if labels else []):
        o.append(ilabel(s, x, y, t, "label2" if full else "label"))
    return "".join(o)


# ================================================================ svg #2  Fig. 1: one-dimensional models -> one continuum
def fig2():
    idx, p = 2, "m16f2_"
    VB = (0, 0, 760, 392)
    s = H.Scale(VB[2], VB[3])
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(ilabel(s, 22, 22, "tissue", "label", "start", I["secondary"]))
    o.append(ilabel(s, 238, 22, "one-dimensional model", "label", "start", I["secondary"]))
    o.append(ilabel(s, 604, 22, "three-dimensional continuum", "label", "middle", I["secondary"]))
    rows = [(72, "bone = beam", "(Module 2)"), (182, "tendon = spring", "(Module 6)"),
            (292, "cartilage = spring + dashpot", "(Module 4)")]
    o.append(femur_h(s, 24, rows[0][0], 176))
    o.append(beam_icon(s, p, 252, 412, rows[0][0] + 6))
    o.append(tendon_icon(s, 24, 200, rows[1][0]))
    o.append(spring_icon(s, 252, 412, rows[1][0]))
    o.append(cartilage_icon(s, 24, 200, rows[2][0]))
    o.append(kelvin_icon(s, 262, 412, rows[2][0]))
    for y, a, b in rows:
        o.append(ilabel(s, 24, y + 52, f"{a} {b}", "label2", "start", I["secondary"]))
    # three one-dimensional models resolve into one continuum
    xj = 432
    o.append(path(f"M424,{rows[0][0] + 6} H{xj} V{rows[2][0]} M424,{rows[1][0]} H{xj} M424,{rows[2][0]} H{xj}",
                  I["rule"], s(H.PX["leader"] * 1.4)))
    o.append(H.arrow(s, p, xj, rows[1][0], 532, rows[1][0], "dim"))
    o.append(ilabel(s, 484, rows[1][0] - 12, "one continuum", "label", "middle"))
    o.append(cube(s, p, 546, 262, 120, full=False))
    o.append(ilabel(s, 604, 330, "stress element: 6 components", "label2", "middle", I["secondary"]))
    o.append(H.credit(s, 22, 366, wrap(BONE_CREDIT, 118)))
    aria = ("Three one-dimensional models from earlier modules, each beside the tissue it stands for: a bone (NIH femur art) "
            "as a beam on two supports under a transverse load, a tendon (collagen strands) as a spring, and a cartilage layer "
            "as a spring and dashpot side by side. All three resolve, through one arrow, into a single three-dimensional "
            "stress element, a cube with a normal stress sigma in red and a shear stress tau in blue on each visible face, "
            "six independent components in all.")
    return finish(VB, aria, s, o)


# ================================================================ svg #3  Fig. 2: the deformation gradient
F_DEF = np.array([[1.30, 0.35], [0.0, 1.15]])         # the matrix of the page's old Fig. 2 grid (steps 1.30, 1.15, shear 0.35)
J_DEF = float(np.linalg.det(F_DEF))
assert f"{J_DEF:.3f}" == "1.495", J_DEF                # the old figure and caption print 1.49 (1.495 cut, not rounded)


def fig3():
    idx, p = 3, "m16f3_"
    VB = (0, 0, 760, 330)
    s = H.Scale(VB[2], VB[3])
    C = 60.0                                           # reference cell edge, user units
    ox, oy, dxo = 50.0, 270.0, 410.0                   # reference and deformed origins (bottom-left, y up -> screen)

    def ref(q):
        return ox + q[0], oy - q[1]

    def dfm(q):
        v = F_DEF @ np.array(q, float)
        return dxo + v[0], oy - v[1]
    n = 3
    o = [f'<defs>{H.markers(p, s)}</defs>']
    sq = [(0, 0), (n * C, 0), (n * C, n * C), (0, n * C)]
    o.append(f'<polygon points="{" ".join("%.1f,%.1f" % ref(q) for q in sq)}" fill="{T["tendon"][0]}" stroke="none"/>')
    o.append(f'<polygon points="{" ".join("%.1f,%.1f" % dfm(q) for q in sq)}" fill="{T["tendon"][0]}" stroke="none"/>')
    # the reference outline, dashed, under the deformed body
    o.append(f'<polygon points="{" ".join("%.1f,%.1f" % (dxo + q[0], oy - q[1]) for q in sq)}" fill="none" '
             f'stroke="{I["rule"]}" stroke-width="{s(H.PX["ref"]):.2f}" stroke-dasharray="{s(H.DASH_REF[0]):.1f} {s(H.DASH_REF[1]):.1f}"/>')
    for f, col, w in ((ref, T["bone"][1], 1.6), (dfm, T["muscle"][1], 1.8)):
        d = ""
        for i in range(n + 1):
            a, b = f((i * C, 0)), f((i * C, n * C))
            c, e = f((0, i * C)), f((n * C, i * C))
            d += f"M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f} M{c[0]:.1f},{c[1]:.1f} L{e[0]:.1f},{e[1]:.1f} "
        o.append(path(d, col, s(w)))
    # one material fibre across the centre cell: dX -> dx = F dX
    a0, a1 = (C, C), (2 * C, 2 * C)
    p0, p1 = ref(a0), ref(a1)
    q0, q1 = dfm(a0), dfm(a1)
    o.append(H.arrow(s, p, p0[0], p0[1], p1[0], p1[1], "geometry"))
    o.append(H.arrow(s, p, q0[0], q0[1], q1[0], q1[1], "geometry"))
    o.append(circ(p0[0], p0[1], s(3), O["geometry"], "#fff", s(1)))
    o.append(circ(q0[0], q0[1], s(3), O["geometry"], "#fff", s(1)))
    o.append(ilabel(s, p0[0] + (p1[0] - p0[0]) / 2 - 8, p0[1] + (p1[1] - p0[1]) / 2 + 18, it("dX"), "label", "end"))
    o.append(ilabel(s, q0[0] + (q1[0] - q0[0]) / 2 + 12, q0[1] + (q1[1] - q0[1]) / 2 + 20, it("dx"), "label", "start"))
    o.append(ilabel(s, ox + n * C / 2, 26, "reference body", "label", "middle", I["secondary"]))
    o.append(ilabel(s, dxo + (F_DEF @ np.array([n * C / 2, n * C / 2]))[0], 26, "deformed body", "label", "middle", I["secondary"]))
    # the map F, its matrix and J
    xm = 316.0
    o.append(H.arrow(s, p, xm - 36, 150, xm + 36, 150, "dim"))
    o.append(ilabel(s, xm, 138, it("F"), "label", "middle"))
    o.append(ilabel(s, xm, 172, f'{it("dx")} = {it("F")} {it("dX")}', "label2", "middle", I["secondary"]))
    ry = 214.0
    o.append(ilabel(s, xm - 68, ry + 11, f'{it("F")} =', "label", "end"))
    for r_i, yy in enumerate((ry, ry + 22)):
        for c_i, xx in enumerate((xm - 40, xm + 10)):
            o.append(ilabel(s, xx + 24, yy + 5, f"{F_DEF[r_i, c_i]:.2f}", "label", "end"))
    o.append(path(f"M{xm - 54:.1f},{ry - 14:.1f} h-6 v52 h6 M{xm + 40:.1f},{ry - 14:.1f} h6 v52 h-6", I["axis"], s(1.3)))
    o.append(ilabel(s, xm, 276, f'{it("J")} = det {it("F")} = {J_DEF:.3f}', "label", "middle"))
    o.append(ilabel(s, xm, 296, "(volume ratio)", "label2", "middle", I["secondary"]))
    o.append(ilabel(s, dxo, 318, "dashed: the reference outline", "label2", "start", I["secondary"]))
    aria = ("A square reference body with a three-by-three grid of material lines on the left, mapped by the deformation "
            f"gradient F = [[{F_DEF[0, 0]:.2f}, {F_DEF[0, 1]:.2f}], [{F_DEF[1, 0]:.2f}, {F_DEF[1, 1]:.2f}]] to a stretched "
            "and sheared body on the right, the reference outline dashed beneath it. A blue arrow dX along the diagonal "
            f"of the centre cell maps to the longer, steeper arrow dx = F dX; the volume ratio is J = det F = {J_DEF:.3f}.")
    return finish(VB, aria, s, o)


# ================================================================ svg #4  Fig. 3: stress cube and traction
SIG2 = np.array([[1.0, 0.3], [0.3, 0.2]])             # arbitrary-unit plane stress used only to draw t = sigma n


def cut_block(s, p, cx, cy, half, n_ang, title):
    """A block of material with a dashed cut through its centre, outward normal n and traction t = sigma n."""
    o = [rect(cx - half, cy - half, 2 * half, 2 * half, BOX, I["rule"], s(1.2))]
    n = np.array([math.cos(math.radians(n_ang)), math.sin(math.radians(n_ang))])
    tvec = SIG2 @ n
    tx, ty = -n[1], n[0]
    L = half * 1.15
    o.append(ref_dash(s, cx - tx * L, cy + ty * L, cx + tx * L, cy - ty * L, I["axis"]))
    sc = 78.0                                           # user units per unit of stress (n has length 0.5 sc)
    o.append(H.arrow(s, p, cx, cy, cx + n[0] * sc * 0.55, cy - n[1] * sc * 0.55, "dim"))
    o.append(H.arrow(s, p, cx, cy, cx + tvec[0] * sc, cy - tvec[1] * sc, "force"))
    return "".join(o), n, tvec


def fig4():
    idx, p = 4, "m16f4_"
    VB = (0, 0, 760, 330)
    s = H.Scale(VB[2], VB[3])
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(cube(s, p, 50, 282, 168, full=True))
    o.append(ilabel(s, 150, 318, "stress cube: 3 normal + 3 independent shear", "label2", "middle", I["secondary"]))
    # right: one stress state, two cuts
    half = 52.0
    pa, pb = (470, 150), (650, 150)
    for (cx, cy), ang, ttl in ((pa, 0.0, "cut A: n = x"), (pb, 90.0, "cut B: n = y")):
        g, n, tv = cut_block(s, p, cx, cy, half, ang, ttl)
        o.append(g)
        o.append(ilabel(s, cx, cy - half - 14, ttl, "label", "middle"))
        nx, ny = cx + n[0] * 78 * 0.55, cy - n[1] * 78 * 0.55
        tx_, ty_ = cx + tv[0] * 78, cy - tv[1] * 78
        o.append(ilabel(s, nx - 4, ny + 18, it("n"), "label", "start") if ang == 0 else ilabel(s, nx - 18, ny + 4, it("n"), "label", "start"))
        o.append(ilabel(s, tx_ + 8, ty_ - 3, it("t"), "label", "start"))
        o.append(ilabel(s, cx, cy + half + 26, f'{it("t")} = ({tv[0]:.2f}, {tv[1]:.2f})', "label2", "middle", I["secondary"]))
    o.append(ilabel(s, 560, 262, f'{it("t")} = {it("σ")} {it("n")}: same {it("σ")}, different cut, different {it("t")}',
                    "label", "middle"))
    o.append(ilabel(s, 560, 284, f'{it("σ")}{sub("xx", s, "label2")} = 1, {it("σ")}{sub("yy", s, "label2")} = 0.2, '
                    f'{it("τ")}{sub("xy", s, "label2")} = {it("τ")}{sub("yx", s, "label2")} = 0.3 (arbitrary units)',
                    "label2", "middle", I["secondary"]))
    aria = ("Left: an isometric stress cube. Each visible face carries a red normal stress (sigma xx on the x face, sigma yy "
            "on the top face, sigma zz on the front face) and two blue shear stresses, arranged as the three complementary "
            "pairs tau zx with tau xz, tau zy with tau yz, tau yx with tau xy. Right: one plane stress state cut two ways. "
            "For cut A with normal along x the traction t = sigma n is (1.00, 0.30); for cut B with normal along y it is "
            "(0.30, 0.20): the traction changes in size and direction as the cut turns.")
    return finish(VB, aria, s, o)


# ================================================================ svg #6  Fig. 5: the bar element
def fig6():
    idx, p = 6, "m16f6_"
    VB = (0, 0, 760, 330)
    s = H.Scale(VB[2], VB[3])
    o = [f'<defs>{H.markers(p, s)}</defs>']
    yc, hh = 104.0, 30.0
    n1, n2 = 150.0, 450.0                               # undeformed node positions (L = 300 units)
    u1, u2 = 16.0, 46.0                                 # exaggerated displacements: u2 > u1, a stretch
    # undeformed (dashed) and deformed (solid) element
    o.append(f'<rect x="{n1:.1f}" y="{yc - hh:.1f}" width="{n2 - n1:.1f}" height="{2 * hh:.1f}" fill="none" '
             f'stroke="{I["rule"]}" stroke-width="{s(H.PX["ref"]):.2f}" stroke-dasharray="{s(H.DASH_REF[0]):.1f} {s(H.DASH_REF[1]):.1f}"/>')
    o.append(rect(n1 + u1, yc - hh, n2 + u2 - n1 - u1, 2 * hh, BONE, BONE_L, s(1.4)))
    for xn in (n1 + u1, n2 + u2):
        o.append(circ(xn, yc, s(5.5), I["primary"], "#fff", s(1.5)))
    # forces at the nodes (a stretch: f1 pulls left, f2 right)
    o.append(H.arrow(s, p, n1 + u1 - 8, yc, n1 + u1 - 62, yc, "force"))
    o.append(H.arrow(s, p, n2 + u2 + 8, yc, n2 + u2 + 62, yc, "force"))
    o.append(ilabel(s, n1 + u1 - 66, yc - 10, f'{it("f")}{sub("1", s)}', "label", "end"))
    o.append(ilabel(s, n2 + u2 + 66, yc - 10, f'{it("f")}{sub("2", s)}', "label", "start"))
    o.append(ilabel(s, n1 + u1, yc - hh - 12, "node 1", "label", "middle"))
    o.append(ilabel(s, n2 + u2, yc - hh - 12, "node 2", "label", "middle"))
    # nodal displacements, from the dashed to the solid node position
    ya = yc + hh + 26
    for xa, u, sb in ((n1, u1, "1"), (n2, u2, "2")):
        o.append(ref_dash(s, xa, yc + hh, xa, ya + 4))
        o.append(H.arrow(s, p, xa, ya, xa + u, ya, "geometry"))
        o.append(ilabel(s, xa + u / 2, ya + 20, f'{it("u")}{sub(sb, s)}', "label", "middle"))
    # length L
    o.append(H.arrow(s, p, n1, yc - hh - 40, n2, yc - hh - 40, "geometry", both=True))
    o.append(ref_dash(s, n1, yc - hh - 44, n1, yc - hh - 14))
    o.append(ref_dash(s, n2, yc - hh - 44, n2, yc - hh - 14))
    o.append(ilabel(s, (n1 + n2) / 2, yc - hh - 48, it("L"), "label", "middle"))
    o.append(ilabel(s, (n1 + n2) / 2, yc + 6, f'cross-section {it("A")}, modulus {it("E")}', "label2", "middle", I["secondary"]))
    # equivalent spring and the matrix
    ys = 252.0
    o.append(circ(112, ys, s(5.5), I["primary"], "#fff", s(1.5)))
    o.append(circ(292, ys, s(5.5), I["primary"], "#fff", s(1.5)))
    o.append(spring_icon(s, 112, 292, ys, 9.0, 6))
    o.append(ilabel(s, 202, ys - 20, f'{it("k")} = {it("EA")}/{it("L")}', "label", "middle"))
    o.append(ilabel(s, 202, ys + 34, "constant strain: a spring", "label2", "middle", I["secondary"]))
    mx, my = 540.0, 238.0
    o.append(ilabel(s, mx - 76, my + 28, f'{it("k")}{sub("e", s)} = ({it("EA")}/{it("L")})', "label", "end"))
    for r_i, yy in enumerate((my, my + 24)):
        for c_i, xx in enumerate((mx - 40, mx + 6)):
            v = ("1", "−1") if r_i == 0 else ("−1", "1")
            o.append(ilabel(s, xx + 22, yy + 14, v[c_i], "label", "middle"))
    o.append(path(f"M{mx - 62:.1f},{my - 2:.1f} h-7 v56 h7 M{mx + 46:.1f},{my - 2:.1f} h7 v56 h-7", I["axis"], s(1.3)))
    o.append(ilabel(s, mx + 66, my + 28, f'{it("f")} = {it("k")}{sub("e", s)} {it("u")}', "label2", "start", I["secondary"]))
    aria = ("A two-node axial bar element of length L, cross-section A and modulus E, drawn dashed before loading and solid "
            "after a stretch. Red arrows are the nodal forces f1 pulling left at node 1 and f2 pulling right at node 2; blue "
            "arrows are the nodal displacements u1 and u2, with u2 larger than u1. Below, the element as a spring of "
            "stiffness k = EA/L, and its two-by-two stiffness matrix (EA/L) times [[1, -1], [-1, 1]].")
    return finish(VB, aria, s, o)


# ================================================================ svg #12: the two driving gradients across one cartilage layer
SIG0, CV, T_FOOT, L_CART = 1.7e6, 6e-10, 1.0, 2e-3    # line 381 (contact pressure), K8 line 737 (c_v), footstep, 2 mm layer
PI_SURF, PI_BONE = 42e3, 156e3                         # line 381 (Pa toward the surface / toward the bone)
G_P = SIG0 / math.sqrt(math.pi * CV * T_FOOT)
G_PI = (PI_BONE - PI_SURF) / L_CART
assert abs(G_P / 1e10 - 3.9) < 0.05 and abs(G_PI / 1e7 - 5.7) < 0.05, (G_P, G_PI)      # line 381
assert round(G_P / G_PI, -1) == 690, G_P / G_PI                                        # "about 690"
assert G_PI / G_P < 0.0015                                                              # "under 0.15%"


def p_front(z_m):
    return SIG0 * np.array([math.erf(v / (2 * math.sqrt(CV * T_FOOT))) for v in z_m])


def fig12():
    idx, p = 12, "m16f12_"
    VB = (0, 0, 760, 428)
    s = H.Scale(VB[2], VB[3])
    X0, PXMM = 84.0, 200.0                              # strip and plot share one depth scale: 200 units per mm
    X1 = X0 + 2 * PXMM
    o = [f'<defs>{H.markers(p, s)}<linearGradient id="{p}cf" x1="0" y1="0" x2="1" y2="0">'
         f'<stop offset="0" stop-color="{T["cartilage"][0]}"/><stop offset="1" stop-color="{T["fibrocart"][0]}"/>'
         f'</linearGradient></defs>']
    # the layer: surface on the left, sealed bone on the right
    ys0, ys1 = 38.0, 84.0
    o.append(rect(X0, ys0, X1 - X0, ys1 - ys0, f"url(#{p}cf)", T["cartilage"][1], s(1.2)))
    o.append(rect(X1, ys0 - 8, 62, ys1 - ys0 + 16, BONE, BONE_L, s(1.2)))
    o.append(ilabel(s, X1 + 31, (ys0 + ys1) / 2 + 5, "bone", "label2", "middle"))
    o.append(ilabel(s, X0, ys0 - 12, "surface (drained, loaded)", "label2", "start", I["secondary"]))
    o.append(ilabel(s, X1 + 62, ys0 - 16, "sealed", "label2", "end", I["secondary"]))
    o.append(ilabel(s, X0 + 6, (ys0 + ys1) / 2 + 5, f'{it("c")}{sub("F", s, "label2")} ≈ 0.1 M', "label2", "start"))
    o.append(ilabel(s, X1 - 6, (ys0 + ys1) / 2 + 5, f'{it("c")}{sub("F", s, "label2")} ≈ 0.2 M', "label2", "end"))
    o.append(ilabel(s, (X0 + X1) / 2, ys1 + 20,
                    f'darker = higher fixed-charge density {it("c")}{sub("F", s, "label2")} (zoned, illustrative two-point profile)',
                    "label2", "middle", I["secondary"]))
    # main plot: p(z, 1 s) and Pi(z) on one pressure axis
    ax = Ax((X0, 150, X1, 352), (0, 2.0), (0, 1.8))
    zz = np.concatenate([np.linspace(0, 0.1, 51), np.linspace(0.1, 2.0, 60)[1:]])
    pp = p_front(zz * 1e-3) / 1e6
    pi = (PI_SURF + (PI_BONE - PI_SURF) * zz * 1e-3 / L_CART) / 1e6
    o += axes(s, ax, [(v, f"{v:g}") for v in (0, 0.5, 1.0, 1.5, 2.0)], [(v, f"{v:g}") for v in (0, 0.5, 1.0, 1.5)],
              "depth z (mm)", "pressure (MPa)", ylab_x=24)
    o.append(ref_dash(s, ax.x0, ax.Y(1.7), ax.x1, ax.Y(1.7)))
    o.append(curve(s, ax, zz, pp, SER[0]))
    o.append(curve(s, ax, zz, pi, SER[1]))
    o.append(ilabel(s, ax.X(0.12), ax.Y(1.7) - 8, f'{it("σ")}{sub("0", s, "label2")} = 1.7 MPa', "label2", "start", I["secondary"]))
    o.append(ilabel(s, ax.X(1.2), ax.Y(0.12) - 18, f'{it("Π")} ({it("z")}): 0.042 → 0.156 MPa', "label2", "start"))
    tx, ty = ax.X(0.42), ax.Y(1.28)
    o.append(ilabel(s, tx, ty, f'|∂{it("p")}/∂{it("z")}| at the face = {it("σ")}{sub("0", s, "label2")}/√(π {it("c")}{sub("v", s, "label2")} {it("t")}) = 3.9×10¹⁰ Pa/m', "label2"))
    o.append(ilabel(s, tx, ty + 20, f'|∂{it("Π")}/∂{it("z")}| = (156 − 42) kPa / 2 mm = 5.7×10⁷ Pa/m', "label2"))
    o.append(ilabel(s, tx, ty + 40, "ratio ≈ 690: the osmotic gradient is", "label2", "start", I["secondary"]))
    o.append(ilabel(s, tx, ty + 58, "under 0.15 % of the mechanical one", "label2", "start", I["secondary"]))
    o += legend(s, X0, 140, [(SER[0], None, f'mechanical: {it("p")} at {it("t")} = 1 s'), (SER[1], None, "osmotic swelling pressure Π")])
    # zoom of the first 0.1 mm: the thin front
    bx = Ax((612, 150, 736, 352), (0, 0.1), (0, 1.8))
    z2 = np.linspace(0, 0.1, 101)
    p2 = p_front(z2 * 1e-3) / 1e6
    pi2 = (PI_SURF + (PI_BONE - PI_SURF) * z2 * 1e-3 / L_CART) / 1e6
    for v in (0.5, 1.0, 1.5):
        o.append(H.line(s, bx.x0, bx.Y(v), bx.x1, bx.Y(v), GRID, "leader"))
    o.append(H.line(s, bx.x0, bx.y0, bx.x1, bx.y0, I["axis"], "axis"))
    o.append(H.line(s, bx.x0, bx.y0, bx.x0, bx.top, I["axis"], "axis"))
    for v in (0, 0.05, 0.1):
        o.append(H.line(s, bx.X(v), bx.y0, bx.X(v), bx.y0 + 5, I["axis"], "leader"))
        o.append(ilabel(s, bx.X(v), bx.y0 + 20, f"{v:g}", "tick", "middle", I["secondary"]))
    o.append(ilabel(s, (bx.x0 + bx.x1) / 2, bx.y0 + 46, "z (mm), first 0.1 mm", "label", "middle"))
    o.append(curve(s, bx, z2, p2, SER[0]))
    o.append(curve(s, bx, z2, pi2, SER[1]))
    zt = SIG0 / G_P * 1e3
    o.append(poly(s, [(bx.X(0), bx.Y(0)), (bx.X(zt), bx.Y(1.7))], I["muted"], "ref", H.DASH_REF))
    for j, tx_ in enumerate(("dashed: slope", "at the face,", "3.9×10¹⁰ Pa/m")):
        o.append(ilabel(s, bx.x1 - 2, bx.Y(0.7) + 16 * j, tx_, "label2", "end", I["secondary"]))
    o.append(ilabel(s, bx.X(0.1) - 4, bx.Y(1.7) - 8, f"front ≈ 2√({it('c')}{sub('v', s, 'label2')} {it('t')}) = 49 µm", "label2", "end", I["secondary"]))
    pts1 = hv(ax, zz, [pp, pi], lambda i: f"z = {zz[i]:.3f} mm: p = {pp[i]:.3f} MPa, Π = {pi[i]:.3f} MPa")
    pts2 = hv(bx, z2, [p2, pi2], lambda i: f"z = {z2[i]:.3f} mm: p = {p2[i]:.3f} MPa, Π = {pi2[i]:.3f} MPa")
    aria = ("A cartilage layer 2 millimetres deep, drained and loaded at the left surface and sealed against bone at the right, "
            "shaded darker with depth for rising fixed-charge density from about 0.1 to 0.2 molar. Beneath it, on the same depth "
            "axis, two pressures at the first second of a footstep: the mechanical pore pressure p rises from zero at the drained "
            "face to 1.7 megapascals within about 49 micrometres, a gradient of 3.9 times 10 to the 10 pascals per metre at the "
            "face, while the osmotic swelling pressure rises linearly from 0.042 to 0.156 megapascals, a gradient of 5.7 times 10 "
            "to the 7 pascals per metre, about 690 times smaller. A zoom of the first 0.1 millimetre shows the thin front.")
    return finish(VB, aria, s, o, extra=H.hover_attr([(ax.box, pts1), (bx.box, pts2)]))


# ================================================================ problem figures (400 px)
W = 400


def pvg(vb, aria, s, body, hover=None):
    return finish(vb, aria, s, body, extra=H.hover_attr(*hover) if hover else "")


def hover_panels(*panels):
    return ([(ax.box, pts) for ax, pts in panels],)


def pw(v):
    """Power-of-ten tick text with Unicode superscripts."""
    e = int(round(math.log10(v)))
    if e == 0:
        return "1"
    if e in (1, 2):
        return f"{v:g}"
    sup = str(abs(e)).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
    return f"10{'⁻' if e < 0 else ''}{sup}"


# ---------------------------------------------------------------- #26 C8: stiff fast, soft slow
def fig26():
    idx, p = 26, "m16f26_"
    VB = (0, 0, W, 292)
    s = H.Scale(W, VB[3], display_w=400)
    ax = Ax((62, 28, 386, 226), (0.01, 100.0), (0, 1.0), xlog=True)
    xs = np.logspace(-2, 2, 161)
    ys = xs * (1 - np.exp(-1 / xs))        # (G_app - G_inf)/(G_0 - G_inf) for a ramp of duration t_f = tau / x (Def. 8.1)
    assert abs(1 * (1 - math.exp(-1)) - 0.632) < 5e-4
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o += axes(s, ax, [(v, pw(v)) for v in (0.01, 0.1, 1, 10, 100)], [(0, "G∞"), (0.5, "½"), (1.0, "G₀")],
              "loading rate 1/t" + sub("f", s) + " (in units of 1/τ)", "apparent stiffness", ylab_x=18, xlab_dy=44)
    o.append(curve(s, ax, xs, ys, SER[0]))
    o.append(ref_dash(s, ax.x0, ax.Y(1.0), ax.x1, ax.Y(1.0), I["muted"]))
    o.append(dot(s, ax.X(1.0), ax.Y(ys[80]), O["flag"]))
    o.append(ilabel(s, ax.X(1.0) + 10, ax.Y(ys[80]) + 22, "t" + sub("f", s, "label2") + " = τ: 0.63 of the way", "label2", "start"))
    o.append(ilabel(s, ax.X(1.0) + 10, ax.Y(ys[80]) + 38, "from G∞ to G₀", "label2", "start"))
    o.append(ilabel(s, ax.X(0.011), ax.Y(0.3), "slow: soft, G∞", "label2", "start", I["secondary"]))
    o.append(ilabel(s, ax.X(95), ax.Y(0.78), "fast: stiff, G₀", "label2", "end", I["secondary"]))
    pts = hv(ax, xs, [ys], lambda i: f"rate = {xs[i]:.3g}/τ: stiffness = G∞ + {ys[i]:.2f} (G₀ − G∞)")
    aria = ("Problem C8 plot. Apparent stiffness of a tissue with a relaxation time tau, loaded by a ramp of duration t, against "
            "loading rate 1/t on a logarithmic axis from 0.01 to 100 over tau, normalised so that the floor is the equilibrium "
            "modulus G-infinity and the ceiling the instantaneous modulus G-zero. Slow loading gives G-infinity, fast loading "
            "gives G-zero, and a ramp lasting exactly tau reaches 0.63 of the way up.")
    return pvg(VB, aria, s, o, hover_panels((ax, pts)))


# ---------------------------------------------------------------- #28 C10: the parent theory
def fig28():
    idx, p = 28, "m16f28_"
    VB = (0, 0, W, 398)
    s = H.Scale(W, VB[3], display_w=400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(cube(s, p, 168, 96, 62, full=False, labels=False))
    o.append(ilabel(s, 156, 62, "continuum", "label", "end"))
    o.append(ilabel(s, 156, 80, "stress, strain, energy", "label2", "end", I["secondary"]))
    cols = [(70, "beam", ["slender body,", "plane sections"]),
            (200, "spring", ["one fibre direction,", "one dimension"]),
            (330, "biphasic column", ["fluid flow in", "one dimension"])]
    for cx, name, lim in cols:
        o.append(H.arrow(s, p, 200, 116, cx, 158, "dim"))
        ym = 192.0
        if name == "beam":
            o.append(femur_h(s, cx - 52, ym, 104))
            o.append(beam_icon(s, p, cx - 52, cx + 52, ym + 54, sag=9))
        elif name == "spring":
            o.append(tendon_icon(s, cx - 52, cx + 52, ym))
            o.append(spring_icon(s, cx - 52, cx + 52, ym + 56, 7.0, 6))
        else:
            o.append(cartilage_icon(s, cx - 52, cx + 52, ym, 36.0))
            o.append(kelvin_icon(s, cx - 52, cx + 52, ym + 60, gap=13))
        o.append(ilabel(s, cx, ym + 112, name, "label", "middle"))
        o.append(ilabel(s, cx, ym + 130, lim[0], "label2", "middle", I["secondary"]))
        o.append(ilabel(s, cx, ym + 146, lim[1], "label2", "middle", I["secondary"]))
    o.append(H.credit(s, 12, 366, wrap(BONE_CREDIT, 74)))
    aria = ("Problem C10 diagram. At the top, the three-dimensional continuum drawn as a stress element. Three arrows lead "
            "down to the models it contains: a beam, shown as a femur and a beam on two supports, the limit of a slender body "
            "with plane sections; a spring, shown as tendon strands and a spring, the limit of one fibre direction in one "
            "dimension; and a biphasic column, shown as a cartilage layer and a spring with a dashpot, the limit of fluid flow in "
            "one dimension.")
    return pvg(VB, aria, s, o)


# ---------------------------------------------------------------- #44 K5: the validity band
def crossing(f, lo, hi, n=80):
    """Bisection for f(x) = 0 on [lo, hi] (f changes sign once)."""
    for _ in range(n):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(lo) * f(mid) > 0 else (lo, mid)
    return (lo + hi) / 2


KFIB = 48.0                                            # line 481 and 679: e^(k eps) - 1, k = 48
neo_err = lambda e: abs((1 + e) ** 2 - 1 / (1 + e) - 3 * e) / (3 * e)            # noqa: E731  Lab B, line 484
fib_err = lambda e: abs(math.exp(KFIB * e) - 1 - KFIB * e) / (KFIB * e)         # noqa: E731  Lab B, line 487
E_NEO = crossing(lambda e: neo_err(e) - 0.05, 0.01, 0.5)
E_FIB = crossing(lambda e: fib_err(e) - 0.05, 1e-5, 0.1)
assert abs(E_NEO - 0.47) < 0.005 and abs(E_FIB - 0.002) < 0.0003, (E_NEO, E_FIB)         # lines 479, 679
assert 200 < E_NEO / E_FIB < 240


def fig44():
    idx, p = 44, "m16f44_"
    VB = (0, 0, W, 306)
    s = H.Scale(W, VB[3], display_w=400)
    ax = Ax((66, 38, 386, 228), (0.01, 50.0), (1e-4, 100.0), xlog=True, ylog=True)
    eps = np.logspace(-4, math.log10(0.5), 260)
    en = np.array([neo_err(e) * 100 for e in eps])
    ef = np.array([fib_err(e) * 100 for e in eps])
    kn = en >= 1e-4
    kf = ef <= 100.0
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o += axes(s, ax, [(v, pw(v)) for v in (0.01, 0.1, 1, 10)] + [(50, "50")], [(v, pw(v)) for v in (1e-4, 1e-2, 1, 100)],
              "strain ε (%)", "linear-law error (%)", ylab_x=16, xlab_dy=44)
    o.append(ref_dash(s, ax.x0, ax.Y(5.0), ax.x1, ax.Y(5.0), I["muted"]))
    o.append(curve(s, ax, eps[kn] * 100, en[kn], SER[1]))
    o.append(curve(s, ax, eps[kf] * 100, ef[kf], SER[0]))
    for e in (E_FIB, E_NEO):
        o.append(dot(s, ax.X(e * 100), ax.Y(5.0), O["flag"]))
    o.append(ilabel(s, ax.X(E_FIB * 100) + 10, ax.Y(5.0) + 16, f"{E_FIB * 100:.2f} %", "label2", "start"))
    o.append(ilabel(s, ax.X(E_NEO * 100) - 8, ax.Y(5.0) - 8, f"{E_NEO * 100:.0f} %", "label2", "end"))
    o.append(ilabel(s, ax.x0 + 6, ax.Y(5.0) - 8, "5 % limit", "label2", "start", I["secondary"]))
    o.append(ilabel(s, ax.X(0.07), ax.Y(0.0035), "slope 2", "label2", "start", I["secondary"]))
    o.append(ilabel(s, ax.X(0.03), ax.Y(0.1), "slope 1", "label2", "start", I["secondary"]))
    o += legend(s, 66, 22, [(SER[0], None, "fibre law (k = 48)"), (SER[1], None, "neo-Hookean")])
    o.append(ilabel(s, (ax.X(E_FIB * 100) + ax.X(E_NEO * 100)) / 2, ax.Y(5.0) + 34, f"≈ {E_NEO / E_FIB:.0f}× wider", "label2", "middle"))
    idxs = list(range(0, len(eps), 2))
    pts = hv(ax, eps[idxs] * 100, [np.clip(ef[idxs], 1e-4, 100), np.clip(en[idxs], 1e-4, 100)],
             lambda i: f"ε = {eps[idxs][i] * 100:.3g} %: fibre error {ef[idxs][i]:.3g} %, neo-Hookean {en[idxs][i]:.3g} %")
    aria = ("Problem K5 plot, both axes logarithmic. The error of the small-strain linear law against strain from 0.01 to 50 "
            "percent. The fibre law, exponential with k = 48, rises with slope 1 and crosses the 5 percent line at 0.20 percent "
            "strain; the neo-Hookean solid rises with slope 2 and crosses it at about 47 percent, roughly 230 times later.")
    return pvg(VB, aria, s, o, hover_panels((ax, pts)))


# ---------------------------------------------------------------- #45 K6: the anisotropy sweep
E_MAT, E_0 = 0.12, 1.50                                # K6 script, line 688 (GPa, assumed)
E_F = E_0 - E_MAT
E_th = lambda th: E_MAT + E_F * np.cos(np.radians(th)) ** 4                     # noqa: E731  line 684
for q, v in ((0, 1.500), (15, 1.321), (30, 0.896), (45, 0.465), (60, 0.206), (90, 0.120)):         # lines 700-705
    assert abs(float(E_th(q)) - v) < 6e-4, (q, E_th(q))
TH_HALF = float(np.degrees(np.arccos(((E_0 / 2 - E_MAT) / E_F) ** 0.25)))
assert abs(TH_HALF - 34.7) < 0.05 and abs(E_0 / E_MAT - 12.5) < 1e-9                  # lines 706-707


def fig45():
    idx, p = 45, "m16f45_"
    VB = (0, 0, W, 296)
    s = H.Scale(W, VB[3], display_w=400)
    ax = Ax((62, 40, 386, 226), (0, 90), (0, 1.6))
    th = np.linspace(0, 90, 181)
    e4 = E_th(th)
    e2 = E_MAT + E_F * np.cos(np.radians(th)) ** 2
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o += axes(s, ax, [(v, f"{v}°") for v in (0, 15, 30, 45, 60, 75, 90)], [(v, f"{v:g}") for v in (0, 0.5, 1.0, 1.5)],
              "load angle θ to the fibres", "stiffness E(θ) (GPa)", ylab_x=16, xlab_dy=44)
    o.append(ref_dash(s, ax.x0, ax.Y(E_0 / 2), ax.x1, ax.Y(E_0 / 2), I["muted"]))
    o.append(curve(s, ax, th, e2, SER[1], "curve_multi", (7, 4)))
    o.append(curve(s, ax, th, e4, SER[0]))
    for q in (0, 15, 30, 45, 60, 90):
        o.append(dot(s, ax.X(q), ax.Y(float(E_th(q))), SER[0]))
    o.append(dot(s, ax.X(TH_HALF), ax.Y(E_0 / 2), O["flag"]))
    o.append(ilabel(s, ax.X(TH_HALF) - 8, ax.Y(E_0 / 2) + 18, f"halves at {TH_HALF:.1f}°", "label2", "end"))
    o.append(ilabel(s, ax.X(2), ax.Y(1.5) - 10, f"{E_0:.2f} GPa along the fibres", "label2", "start"))
    o.append(ilabel(s, ax.X(90), ax.Y(1.12), f"at 90°: {E_MAT:.2f} GPa,", "label2", "end"))
    o.append(ilabel(s, ax.X(90), ax.Y(1.12) + 16, f"ratio {E_0 / E_MAT:.1f}", "label2", "end"))
    o.append(ilabel(s, ax.X(45) - 8, ax.Y(float(E_th(45))) + 18, f"{float(E_th(45)):.3f} at 45°", "label2", "end"))
    o += legend(s, 62, 22, [(SER[0], None, "cos⁴θ: two projections"), (SER[1], (7, 4), "cos²θ: one")], gap=14)
    pts = hv(ax, th, [e4, e2], lambda i: f"θ = {th[i]:.1f}°: E = {e4[i]:.3f} GPa (cos⁴), {e2[i]:.3f} GPa (cos² for comparison)")
    aria = ("Problem K6 plot. Directional stiffness E of a fibre-reinforced tissue against the angle theta between the load and "
            "the fibres, 0 to 90 degrees: E = 0.12 + 1.38 cos to the fourth of theta in gigapascals, falling from 1.50 along the "
            "fibres to 0.12 across them, a ratio of 12.5, and halving at 34.7 degrees. Dots mark 0, 15, 30, 45, 60 and 90 degrees. "
            "A dashed curve with cos squared shows what a single projection would give.")
    return pvg(VB, aria, s, o, hover_panels((ax, pts)))


# ---------------------------------------------------------------- #49 K8: the consolidation clock
CV_K8 = 1e-3                                           # line 741 (m^2/s)


def t_half_fd(L, cv=CV_K8, nz=40):
    """K8 script, lines 741-755, unchanged: time for the layer-averaged pore pressure to fall to one half."""
    dz = L / nz
    dt = 0.4 * dz ** 2 / cv
    q = np.ones(nz + 1)
    q[0] = 0.0
    for it_ in range(2000000):
        lap = np.zeros_like(q)
        lap[1:-1] = (q[2:] - 2 * q[1:-1] + q[:-2]) / dz ** 2
        lap[-1] = (2 * q[-2] - 2 * q[-1]) / dz ** 2
        q = q + dt * cv * lap
        q[0] = 0.0
        if q.mean() < 0.5:
            return (it_ + 1) * dt
    return float("nan")


def F_terz(T_, nmax=400):
    """Terzaghi series, K8 script lines 758-761 (and the module's boxed F(T), line 355)."""
    T_ = np.asarray(T_, float)
    return sum(8 / ((2 * n + 1) ** 2 * math.pi ** 2) * np.exp(-((2 * n + 1) * math.pi / 2) ** 2 * T_) for n in range(nmax))


TH = {L: t_half_fd(L) for L in (1.0, 0.5, 0.25)}
for L, v in ((1.0, 194.50), (0.5, 48.63), (0.25, 12.16)):                          # line 737
    assert abs(TH[L] - v) < 0.006, (L, TH[L])
CART = [(1.0, "footstep"), (60.0, "1 min"), (3600.0, "1 h")]                      # line 737: F = 0.986, 0.893, 0.214
for (t_, _), v in zip(CART, (0.986, 0.893, 0.214)):
    assert abs(float(F_terz(6e-10 * t_ / (2e-3) ** 2)) - v) < 6e-4


def fig49():
    idx, p = 49, "m16f49_"
    VB = (0, 0, W, 492)
    s = H.Scale(W, VB[3], display_w=400)
    cols = {1.0: SER[0], 0.5: SER[1], 0.25: SER[2]}
    a = Ax((62, 40, 386, 188), (0.1, 1000.0), (0, 1.0), xlog=True)
    b = Ax((62, 292, 386, 440), (1e-4, 1.0), (0, 1.0), xlog=True)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o += axes(s, a, [(v, pw(v)) for v in (0.1, 1, 10, 100, 1000)], [(v, f"{v:g}") for v in (0, 0.5, 1.0)],
              "time t (s)", "fluid share F", ylab_x=16, xlab_dy=42)
    o += axes(s, b, [(v, pw(v)) for v in (1e-4, 1e-3, 1e-2, 1e-1, 1.0)], [(v, f"{v:g}") for v in (0, 0.5, 1.0)],
              "T = c" + sub("v", s, "label") + "t/L²", "fluid share F", ylab_x=16, xlab_dy=42)
    o.append(ref_dash(s, a.x0, a.Y(0.5), a.x1, a.Y(0.5), I["muted"]))
    o.append(ref_dash(s, b.x0, b.Y(0.5), b.x1, b.Y(0.5), I["muted"]))
    tt = np.logspace(-1, 3, 200)
    for L, c in cols.items():
        o.append(curve(s, a, tt, F_terz(CV_K8 * tt / L ** 2), c, "curve_multi"))
        o.append(dot(s, a.X(TH[L]), a.Y(0.5), O["flag"]))
    fa = {L: F_terz(CV_K8 * tt / L ** 2) for L in cols}
    ap = [[a.X(t_), [a.Y(float(fa[L][i])) for L in cols],
           f"t = {t_:.3g} s: F = " + ", ".join(f"{float(fa[L][i]):.3f} (L = {L:g} m)" for L in cols)] for i, t_ in enumerate(tt)]
    for j, (L, c) in enumerate(cols.items()):
        yy = a.Y(0.30) + 17 * j
        o.append(H.line(s, a.x0 + 10, yy - 4.5, a.x0 + 34, yy - 4.5, c, "curve_multi"))
        o.append(ilabel(s, a.x0 + 40, yy, f"L = {L:g} m: t½ = {TH[L]:.2f} s", "label2", "start"))
    o.append(ilabel(s, a.x1, a.top + 16, "c" + sub("v", s, "label2") + " = 10⁻³ m²/s", "label2", "end", I["secondary"]))
    o.append(ilabel(s, a.x1, a.top + 33, "t½ ∝ L²", "label2", "end", I["secondary"]))
    TT = np.logspace(-4, 0, 200)
    FT = F_terz(TT)
    for L, c in cols.items():
        o.append(curve(s, b, TT, FT, c, "curve", extra=f'stroke-width="{s({1.0: 7.5, 0.5: 4.5, 0.25: 1.6}[L]):.2f}"'))
    o.append(dot(s, b.X(0.195), b.Y(0.5), O["flag"]))
    o.append(ilabel(s, b.X(0.195) - 8, b.Y(0.5) + 18, "T½ = 0.195, all three", "label2", "end"))
    for t_, nm in CART:
        T_ = 6e-10 * t_ / (2e-3) ** 2
        o.append(dot(s, b.X(T_), b.Y(float(F_terz(T_))), I["primary"], hollow=True))
        o.append(ilabel(s, b.X(T_) + (-8 if nm == "1 h" else 8), b.Y(float(F_terz(T_))) + (-10 if nm != "1 h" else 18), nm,
                        "label2", "end" if nm == "1 h" else "start"))
    o.append(ilabel(s, b.x0 + 10, b.Y(0.30), "circles: cartilage, L = 2 mm,", "label2", "start", I["secondary"]))
    o.append(ilabel(s, b.x0 + 10, b.Y(0.30) + 16, "c" + sub("v", s, "label2") + " = 6×10⁻¹⁰ m²/s", "label2", "start", I["secondary"]))
    bp = [[b.X(T_), b.Y(float(f_)), f"T = {T_:.3g}: F = {float(f_):.3f}"] for T_, f_ in zip(TT, FT)]
    o.append(ilabel(s, 224, 266, "one curve in T: thickness is absorbed", "label", "middle"))
    aria = ("Problem K8 plots of the fluid share F of a step load against time, from the consolidation series. Top: F against t on "
            "a logarithmic axis for layers of 1, 0.5 and 0.25 metres at c-v of 10 to the minus 3 square metres per second; the "
            "curves cross F = 0.5 at 194.50, 48.63 and 12.16 seconds, each a factor 4 of the one before. Bottom: the same "
            "three layers against the dimensionless time T = c-v t over L squared collapse onto one curve crossing 0.5 at T = "
            "0.195; circles mark cartilage (L = 2 mm, c-v 6 times 10 to the minus 10) after a 1 second footstep, 1 minute and 1 hour, "
            "with F = 0.986, 0.893 and 0.214.")
    return pvg(VB, aria, s, o, hover_panels((a, ap), (b, bp)))


# ---------------------------------------------------------------- #53 K10: what one beam element does and does not know
NU, KAP = 0.3, 5.0 / 6.0                                # line 823
shear = lambda lh: 100 * (2 * (1 + NU) / (4 * KAP)) * (1.0 / lh) ** 2          # noqa: E731  line 833 (per cent)
for lh_, v in ((20, 0.20), (10, 0.78), (5, 3.12), (3, 8.67), (2, 19.50)):                # lines 839-843
    assert abs(shear(lh_) - v) < 0.006, (lh_, shear(lh_))
EI, LB_, P_ = 1.0, 1.0, 1.0
KMAT = (EI / LB_ ** 3) * np.array([[12, 6 * LB_, -12, 6 * LB_], [6 * LB_, 4 * LB_ ** 2, -6 * LB_, 2 * LB_ ** 2],
                                   [-12, -6 * LB_, 12, -6 * LB_], [6 * LB_, 2 * LB_ ** 2, -6 * LB_, 4 * LB_ ** 2]])
W2, TH2 = np.linalg.solve(KMAT[2:, 2:], np.array([P_, 0.0]))                           # lines 824-828
assert abs(W2 - P_ * LB_ ** 3 / (3 * EI)) < 1e-12                                       # difference 0.00e+00


def fig53():
    from m02.bone import SEGS, SHAFT_A, SHAFT_B, emit
    idx, p = 53, "m16f53_"
    VB = (0, 0, W, 444)
    s = H.Scale(W, VB[3], display_w=400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # ---- the element: a femur as the cantilever, bent by the element's own cubic (Hermite) shape, exaggerated
    XW, YA, LPX, SAG = 56.0, 92.0, 280.0, 46.0
    k = LPX / FEMUR_L
    ax_c = (SHAFT_A[0] + SHAFT_B[0]) / 2

    def wshape(u):                                       # exact tip-loaded cubic: w/delta = (3 u^2 - u^3) / 2
        return SAG * (3 * u * u - u ** 3) / 2
    assert abs(wshape(1.0) - SAG) < 1e-12

    def place(q, bend):
        u = (FEMUR_ART[3] - q[1]) / FEMUR_L
        return XW + u * LPX, YA - (q[0] - ax_c) * k + (wshape(u) if bend else 0.0)
    # the unbent outline = the shared femur path under place(q, False): x = XW + (ART3 - qy) k, y = YA - (qx - ax_c) k
    o.append(f'<use href="#m16art_femur" fill="none" stroke="{I["rule"]}" stroke-width="{s(1.1) / k:.2f}" '
             f'stroke-dasharray="{s(4) / k:.2f} {s(3) / k:.2f}" '
             f'transform="matrix(0 {-k:.5f} {-k:.5f} 0 {XW + FEMUR_ART[3] * k:.2f} {YA + ax_c * k:.2f})"/>')
    o.append(path(emit(SEGS, lambda q: place(q, True)), BONE_L, s(H.PX["art_line"]), fill=BONE, extra='stroke-linejoin="round"'))
    o.append(rect(XW - 18, YA - 40, 18, 80, GRID, I["rule"], s(1.0)))
    o.append(path("".join(f"M{XW - 18:.1f},{YA - 32 + 11 * i:.1f} l18,-9" for i in range(8)), I["rule"], s(0.8)))
    xt, yt = XW + LPX, YA + SAG
    o.append(circ(XW, YA, s(5.5), I["primary"], "#fff", s(1.5)))
    o.append(circ(xt, yt, s(5.5), I["primary"], "#fff", s(1.5)))
    o.append(H.arrow(s, p, xt, yt - 66, xt, yt - 8, "load"))
    o.append(ilabel(s, xt + 8, yt - 44, it("P"), "label", "start"))
    o.append(H.arrow(s, p, xt + 32, YA, xt + 32, yt, "geometry", both=True))
    o.append(ref_dash(s, xt + 6, YA, xt + 38, YA))
    o.append(ilabel(s, xt + 38, YA + SAG / 2 + 5, "δ", "label", "start"))
    o.append(ilabel(s, XW - 10, YA + 56, "node 1 (fixed)", "label2", "start"))
    o.append(ilabel(s, xt - 46, yt + 22, "node 2 (tip)", "label2", "middle"))
    o.append(ilabel(s, W / 2, 24, f'one element: δ = {it("P")}{it("L")}³/3{it("EI")} exactly (difference 0)', "label", "middle"))
    o.append(ilabel(s, W / 2, 42, "deflection exaggerated; the shape is the element's cubic", "label2", "middle", I["secondary"]))
    # ---- what the element cannot know: the shear deflection a Timoshenko beam adds
    ax = Ax((66, 206, 376, 336), (1.0, 30.0), (0.1, 100.0), xlog=True, ylog=True)
    lh = np.logspace(0, math.log10(30), 120)
    sh = shear(lh)
    o += axes(s, ax, [(v, f"{v}") for v in (1, 2, 5, 10, 20)], [(v, pw(v)) for v in (0.1, 1, 10, 100)],
              "slenderness L/h", "shear adds (%)", ylab_x=18, xlab_dy=44)
    o.append(curve(s, ax, lh, sh, SER[0]))
    for v in (20, 10, 5, 3, 2):
        o.append(dot(s, ax.X(v), ax.Y(shear(v)), SER[0]))
        o.append(ilabel(s, ax.X(v) + 8, ax.Y(shear(v)) - 6, f"{shear(v):.2f}", "label2", "start"))
    o.append(dot(s, ax.X(10), ax.Y(shear(10)), O["flag"]))
    o.append(dot(s, ax.X(1), ax.Y(shear(1)), O["flag"], hollow=True))
    o.append(ilabel(s, ax.X(10) - 10, ax.Y(shear(10)) + 20, "femur, L/h ≈ 10", "label2", "end"))
    o.append(ilabel(s, ax.X(1) + 10, ax.Y(1.0), "vertebral body, L/h ≈ 1:", "label2", "start"))
    o.append(ilabel(s, ax.X(1) + 10, ax.Y(1.0) + 16, "not a beam", "label2", "start"))
    o.append(ilabel(s, 66, 190, "shear deflection a Timoshenko beam adds", "label", "start"))
    pts = hv(ax, lh, [sh], lambda i: f"L/h = {lh[i]:.3g}: shear adds {sh[i]:.3g} %")
    o.append(H.credit(s, 12, 394, wrap(BONE_CREDIT, 74)))
    aria = ("Problem K10 figure. Top: a femur drawn as a cantilever, fixed at node 1 and loaded by a tip force P at node 2; it "
            "is bent, exaggerated, by the single beam element's own cubic shape, with the tip deflection delta equal to P L cubed over "
            "3 E I exactly. Bottom, logarithmic axes: the shear deflection a Timoshenko beam adds, as a percentage, against "
            "slenderness L over h: 0.20 percent at 20, 0.78 at 10, 3.12 at 5, 8.67 at 3 and 19.50 at 2, with a femur at about "
            "10 and a vertebral body at about 1, which is not a beam.")
    return pvg(VB, aria, s, o, hover_panels((ax, pts)))


FIGS = {
    2: ("Three one-dimensional tissue models from earlier modules - a", fig2),
    3: ("A reference square grid on the left mapped by the deformatio", fig3),
    4: ("An isometric stress cube with normal stresses on its faces a", fig4),
    6: ("A two-node axial bar element with nodal displacements and fo", fig6),
    12: ("A cartilage layer in cross-section, fixed-charge density ris", fig12),
    26: ("C8: stiff fast, soft slow. Why does cartilage resist a quick", fig26),
    28: ("C10: the parent theory. In what sense is the continuum the p", fig28),
    44: ("K5: the validity band (sensitivity). Find the strain at whic", fig44),
    45: ("K6: the anisotropy sweep. Derive how the directional stiffness", fig45),
    49: ("K8: the consolidation clock. Solve the consolidation equatio", fig49),
    53: ("K10: what one beam element does and does not know. Compare a", fig53),
}
