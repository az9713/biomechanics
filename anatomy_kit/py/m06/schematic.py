"""Module 6, group `schematic`: collagen, tendon, muscle-tendon unit, viscoelastic networks and roadmap, house style.

Main text (760 px): svg 4, 6, 7, 10, 11, 14, 15, 16, 17, 22, 30.  Problems (400 px): svg 32 (C2), 35 (C5), 36 (C6),
38 (C8), 45 (D5).  Every number is computed here from a value module06.html states (line numbers beside each
constant).  Bone ends: NIH NIAID BioArt 244 femur (public domain), the one-path crop m00 uses, cut in Python to its
distal end (a clip-path would leave the hidden shaft in getBBox, so the geometry is cut, not clipped).
"""
import math
import random
import re

import house as H
from m00.tissue import arclen, dpath, femur_d, rope, wave
from m05.body import wrap
from m05.plots_main import Ax, axes, poly
from m05.plots_main import legend as plegend
from m05.schematic import box, finish, it
from m05.tissue import angle_arc, circ, fibre_line, halo_line, legend, muscle_grad, path, rect, sw_line, sw_rect, tissue

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
GRID = "#e6e6e6"

# ---------------------------------------------------------------- constants the module states
D_NM, LC_NM = 67.0, 300.0                  # line 186 (D-period), line 182 (L_c = 300 nm)
GAP_MEAS = 0.54                            # line 191 (measured gap 0.54 D)
EPS_STAR = 0.03                            # line 167 / 178 (toe ends at 3 %)
A0_MM2, L0_MM, X_PUSH = 80.0, 250.0, 16.0  # line 264 (Achilles A0, L0), line 312 (x at push-off)
K_MEAS = (150.0, 400.0)                    # line 266: measured free-Achilles stiffness range, N/mm
F_PUSH = 5000.0                            # line 312: tension at a hard running push-off, N
TS, TE, ER = 0.050, 0.090, 1.20e9          # line 543 / 1068: tau_sigma, tau_eps (s), E_R (Pa)
EPS0 = 0.01                                # line 1067 (K5 code, e0 = 0.01): strain step 1 %
RATIO_LAB2 = 3.3                           # line 384: tendon recoil / fibre speed from the coupled dynamics
TH_P = 25.0                                # pennation drawn (Module 5's figures use 25 deg)

DOT = "̇"                             # combining dot above: σ̇, ε̇ (Georgia stacks it on Greek)


def dotted(ch, back):
    """ch with a spacing dot above, placed by hand: Georgia has no ℓ and the fallback font does not stack U+0307.
    back = how far (em) the dot steps back over the letter; the second tspan restores the baseline."""
    return (f'{it(ch)}<tspan dx="-{back:.2f}em" dy="-0.50em">˙</tspan>'
            f'<tspan dx="{back - 0.50:.2f}em" dy="0.50em">​</tspan>')


def femur_credit(s, x, y, n=118):
    cr = H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt (Ryan Kissinger)", title="Human Upper Leg Bones (BioArt 244)",
                                    changes="One femur end only; recoloured.")
    return H.credit(s, x, y, wrap(cr, n))


# ---------------------------------------------------------------- the femur end: flatten, cut, place
def _femur_poly(n=8):
    """The femur fill path (M, relative c, z only) as a polygon, art units."""
    tok = re.findall(r"[A-Za-z]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", femur_d())
    assert set(t for t in tok if t.isalpha()) == {"M", "c", "z"}
    i, pts, cur = 0, [], (0.0, 0.0)
    while i < len(tok):
        t = tok[i]
        if t == "M":
            cur = (float(tok[i + 1]), float(tok[i + 2]))
            pts.append(cur)
            i += 3
        elif t == "c":
            i += 1
            while i < len(tok) and not tok[i].isalpha():
                v = [float(q) for q in tok[i:i + 6]]
                p0 = cur
                p1, p2, p3 = (p0[0] + v[0], p0[1] + v[1]), (p0[0] + v[2], p0[1] + v[3]), (p0[0] + v[4], p0[1] + v[5])
                for k in range(1, n + 1):
                    u = k / n
                    a, b, c, d = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
                    pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
                cur = p3
                i += 6
        else:
            i += 1
    return pts


def _clip_y(pts, y_cut):
    """Sutherland-Hodgman against the half-plane y >= y_cut (keeps the distal end)."""
    out = []
    for a, b in zip(pts, pts[1:] + pts[:1]):
        ia, ib = a[1] >= y_cut, b[1] >= y_cut
        if ia:
            out.append(a)
        if ia != ib:
            t = (y_cut - a[1]) / (b[1] - a[1])
            out.append((a[0] + t * (b[0] - a[0]), y_cut))
    return out


def femur_end(x_left, y_c, w, y_cut=292.0, facing="right"):
    """Distal femur end, cut at art y = y_cut, turned so the shaft runs horizontal (cut face at x_left) and the
    condyles face `facing`. w = drawn width across the bone axis. Returns (svg, (x_min, x_max, y_min, y_max))."""
    q = _clip_y(_femur_poly(), y_cut)
    xs, ys = [p[0] for p in q], [p[1] for p in q]
    k = w / (max(xs) - min(xs))
    x_face = x_left + (max(ys) - min(ys)) * k
    xm = (max(xs) + min(xs)) / 2
    sg = 1 if facing == "right" else -1
    # art (x, y) -> figure: along = (y - ymax) (distal tip at x_face), across = (x - xm)
    fig = [(x_face + sg * (y - max(ys)) * k, y_c + (x - xm) * k * sg) for x, y in q]
    d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in fig) + " Z"
    fx, fy = [p[0] for p in fig], [p[1] for p in fig]
    svg = (f'<path d="{d}" fill="{T["bone"][0]}" stroke="{T["bone"][1]}" stroke-width="1.2" stroke-linejoin="round"/>')
    return svg, (min(fx), max(fx), min(fy), max(fy))


# ---------------------------------------------------------------- shared element drawings
def zig(x0, x1, y, n=8, amp=8.0, lead=10.0):
    pts = [(x0, y), (x0 + lead, y)]
    w = (x1 - x0 - 2 * lead) / n
    for i in range(n):
        pts.append((x0 + lead + (i + 0.5) * w, y + (amp if i % 2 else -amp)))
    return pts + [(x1 - lead, y), (x1, y)]


def spring(s, x0, x1, y, n=8, amp=8.0, lead=10.0, col=None, w=1.8):
    """Ideal spring symbol (ink)."""
    return path(dpath(zig(x0, x1, y, n, amp, lead)), col or I["primary"], s(w), extra='stroke-linejoin="round"')


def tissue_spring(s, x0, x1, y, kind="tendon", n=8, amp=9.0, lead=8.0, w_out=6.0, w_in=3.4):
    """A spring drawn in a tissue's colours (outer line colour, inner fill colour), as m00's rope."""
    f, l_ = T[kind]
    d = dpath(zig(x0, x1, y, n, amp, lead))
    return (path(d, l_, s(w_out), extra='stroke-linejoin="round" stroke-linecap="round"')
            + path(d, f, s(w_in), extra='stroke-linejoin="round" stroke-linecap="round"'))


def dashpot(s, x0, x1, y, h=20.0, col=None, w=1.8):
    """Dashpot: rod from x0 to a piston inside a fluid-filled cylinder open on the left, rod from the cylinder to x1."""
    col = col or I["primary"]
    L = x1 - x0
    c0, c1 = x0 + 0.30 * L, x0 + 0.78 * L
    xp = x0 + 0.55 * L
    o = [rect(c0, y - h / 2, c1 - c0, h, T["fluid"][0], None, 0, 0, 'opacity="0.75"'),
         path(f"M{c0:.1f},{y - h / 2:.1f} L{c1:.1f},{y - h / 2:.1f} L{c1:.1f},{y + h / 2:.1f} L{c0:.1f},{y + h / 2:.1f}",
              col, s(w)),
         H.line(s, x0, y, xp, y, col, "ref", extra=f'stroke-width="{s(w):.2f}"'),
         H.line(s, xp, y - 0.36 * h, xp, y + 0.36 * h, col, "ref", extra=f'stroke-width="{s(w + 1.6):.2f}"'),
         H.line(s, c1, y, x1, y, col, "ref", extra=f'stroke-width="{s(w):.2f}"')]
    return "".join(o)


def node(s, x, y, r=3.2):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s(r):.2f}" fill="{I["primary"]}"/>'


def wire(s, pts, col=None, w=1.8):
    return path(dpath(pts), col or I["primary"], s(w), extra='stroke-linejoin="round"')


def crossbar(s, x, y0, y1, w=5.0):
    return rect(x - w / 2, y0, w, y1 - y0, I["secondary"], None, 0, 1)


def wall(s, x, y0, y1, side="left"):
    """Fixed ground: a solid line with hatching on the far side."""
    o = [H.line(s, x, y0, x, y1, I["primary"], "axis", extra=f'stroke-width="{s(2.2):.2f}"')]
    sg = -1 if side == "left" else 1
    yy = y0 + 4
    while yy < y1:
        o.append(H.line(s, x, yy, x + sg * 8, yy + 8, I["secondary"], "leader"))
        yy += 9
    return "".join(o)


def dim(s, p, x0, x1, y, txt, ty=None, meaning="geometry", ext=(None, None), size="label2", anchor="middle", tx=None):
    """Dimension line with heads at both ends, extension ticks from ext=(y_a, y_b) and a label above it."""
    o = []
    for x, ye in zip((x0, x1), ext):
        if ye is not None:
            o.append(H.line(s, x, ye, x, y + (4 if ye < y else -4), O["dim"], "leader"))
    o.append(H.arrow(s, p, x0, y, x1, y, meaning, both=True))
    col = O[meaning] if meaning != "dim" else I["primary"]
    o.append(H.label(s, tx if tx is not None else (x0 + x1) / 2, ty if ty is not None else y - 7, txt, size, col, anchor))
    return "".join(o)


def liang(x0, y0, x1, y1, bx0, by0, bx1, by1):
    """Clip segment to a rectangle (Liang-Barsky). Returns the clipped segment or None."""
    dx, dy = x1 - x0, y1 - y0
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, x0 - bx0), (dx, bx1 - x0), (-dy, y0 - by0), (dy, by1 - y0)):
        if pp == 0:
            if qq < 0:
                return None
            continue
        r = qq / pp
        if pp < 0:
            t0 = max(t0, r)
        else:
            t1 = min(t1, r)
        if t0 > t1:
            return None
    return (x0 + t0 * dx, y0 + t0 * dy, x0 + t1 * dx, y0 + t1 * dy)


def fibre_field(s, bx0, by0, bx1, by1, angles, pitch, col, w=0.9, op=0.75, seed=1):
    """Straight fibre lines at the given angles (deg) filling a rectangle, clipped in Python."""
    rnd = random.Random(seed)
    o = []
    cx, cy = (bx0 + bx1) / 2, (by0 + by1) / 2
    R = math.hypot(bx1 - bx0, by1 - by0)
    for a in angles:
        ux, uy = math.cos(math.radians(a)), -math.sin(math.radians(a))
        nx, ny = -uy, ux
        off = -R / 2 + rnd.uniform(0, pitch)
        while off < R / 2:
            px, py = cx + nx * off, cy + ny * off
            seg = liang(px - ux * R, py - uy * R, px + ux * R, py + uy * R, bx0, by0, bx1, by1)
            if seg:
                o.append(f'<line x1="{seg[0]:.1f}" y1="{seg[1]:.1f}" x2="{seg[2]:.1f}" y2="{seg[3]:.1f}" stroke="{col}" '
                         f'stroke-width="{s(w):.2f}" opacity="{op}"/>')
            off += pitch
    return "".join(o)


def cord(s, x0, x1, y, h, kind="tendon", lines=4, op=0.7):
    """A cord of tissue (tendon) as a filled band with longitudinal fascicle lines."""
    f, l_ = T[kind]
    o = [rect(x0, y - h / 2, x1 - x0, h, f, l_, s(1.0), 2)]
    for j in range(1, lines + 1):
        yy = y - h / 2 + j * h / (lines + 1)
        o.append(f'<line x1="{x0 + 3:.1f}" y1="{yy:.1f}" x2="{x1 - 3:.1f}" y2="{yy:.1f}" stroke="{l_}" '
                 f'stroke-width="{s(0.8):.2f}" opacity="{op}"/>')
    return "".join(o)


def zig_fibril(x0, x1, y, Lc, n=8):
    """A fibril of contour length Lc spanning x0..x1: a planar zig-zag (crimp) if Lc > span, else straight."""
    X = x1 - x0
    if Lc <= X:
        return [(x0, y), (x1, y)], True
    h = math.sqrt((Lc / n) ** 2 - (X / n) ** 2)
    pts = [(x0, y)]
    for i in range(1, n + 1):
        pts.append((x0 + X * i / n, y + (h / 2 if i % 2 else -h / 2) * (0 if i == n else 1)))
    pts[-1] = (x1, y)
    return pts, False


def fibril_rope(s, pts, taut, w_out=4.2, w_in=2.2):
    d = dpath(pts)
    outer = O["force"] if taut else T["tendon"][1]
    return (path(d, outer, s(w_out), extra='stroke-linecap="round" stroke-linejoin="round"')
            + path(d, T["tendon"][0], s(w_in), extra='stroke-linecap="round" stroke-linejoin="round"'))


# ================================================================ svg #4  Fig. 2: rope of ropes, and the crimp
def fig4():
    VB = (0, 0, 760, 392)
    s = H.Scale(VB[2], VB[3])
    p = "m6f4_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    tf, tl = T["tendon"]
    cy = 92
    cxs = [80 + 150 * i for i in range(5)]
    titles = ["tendon", "fascicle", "fibre", "fibril", "tropocollagen"]
    notes = [("the whole cord,", "bone to muscle"), ("a bundle of", "crimped fibres"), ("a bundle of", "fibrils"),
             ("banded every", f"{it('D')} = {D_NM:.0f} nm"), ("triple helix,", f"{it('L')}{H.sub('c', s, 'label2')} = {LC_NM:.0f} nm long")]
    for cx, t, (n1, n2) in zip(cxs, titles, notes):
        o.append(H.label(s, cx, 20, t, "label", I["primary"], "middle"))
        o.append(H.label(s, cx, 158, n1, "label2", I["secondary"], "middle"))
        o.append(H.label(s, cx, 174, n2, "label2", I["secondary"], "middle"))
    zoom, nxt = [], []
    # 1 tendon: a cord with fascicle lines and a cut face showing fascicles end-on
    c = cxs[0]
    o.append(cord(s, c - 62, c + 50, cy, 44, lines=5))
    o.append(f'<ellipse cx="{c + 50:.1f}" cy="{cy}" rx="10" ry="22" fill="{tf}" stroke="{tl}" stroke-width="{s(1.0):.2f}"/>')
    for j, (dx, dy) in enumerate(((-3, -14), (3, -6), (-4, 2), (3, 10), (-2, 16), (4, -16))):
        o.append(circ(c + 50 + dx * 0.9, cy + dy, 3.2, "#fff", tl, 0.8))
    zoom.append((c + 42, cy - 8, 12, 16))
    # 2 fascicle: a sheathed bundle of crimped fibres
    c = cxs[1]
    fx0, fx1 = c - 58, c + 58
    o.append(rect(fx0, cy - 22, fx1 - fx0, 44, tf, tl, s(1.0), 12))
    for j in range(5):
        yy = cy - 14 + j * 7
        o.append(path(dpath(zig(fx0 + 6, fx1 - 6, yy, 14, 2.2, 1)), tl, s(1.3), extra='stroke-linejoin="round"'))
    zoom.append((c - 10, cy - 18, 20, 9))
    nxt.append((fx0, cy - 22, cy + 22))
    # 3 fibre: crimped fibrils as ropes
    c = cxs[2]
    o.append(rect(c - 58, cy - 20, 116, 40, "#fff", tl, s(1.0), 10, 'fill-opacity="0"'))
    for j in range(4):
        yy = cy - 12 + j * 8
        o.append(rope(zig(c - 54, c + 54, yy, 12, 2.0, 1), s, 4.4, 2.4))
    zoom.append((c - 8, cy - 18, 16, 8))
    nxt.append((c - 58, cy - 20, cy + 20))
    # 4 fibril: one rope with D-banding (gap zones darker), one period dimensioned
    c = cxs[3]
    per = 22.0
    bx0 = c - 2.5 * per
    o.append(rect(bx0, cy - 8, 5 * per, 16, tf, tl, s(1.0), 8))
    for k in range(5):
        g0 = bx0 + k * per + per * (LC_NM / D_NM - 4)
        o.append(rect(g0, cy - 8, per * (5 - LC_NM / D_NM), 16, tl, None, 0, 0, 'opacity="0.55"'))
    o.append(dim(s, p, bx0 + per, bx0 + 2 * per, cy + 22, it("D"), ty=cy + 40, ext=(cy + 9, None)))
    o.append(H.line(s, bx0 + 2 * per, cy + 9, bx0 + 2 * per, cy + 18, O["dim"], "leader"))
    zoom.append((c - 6, cy - 9, 12, 18))
    nxt.append((c - 58, cy - 20, cy + 20))
    # 5 tropocollagen: three strands wound as a helix
    c = cxs[4]
    x3a, x3b = c - 54, c + 54
    for k in range(3):
        pts = [(x3a + (x3b - x3a) * i / 160, cy + 9 * math.sin(2 * math.pi * 4.5 * i / 160 + 2 * math.pi * k / 3))
               for i in range(161)]
        o.append(path(dpath(pts), tl, s(2.6), extra='stroke-linecap="round"'))
    nxt.append((x3a, cy - 12, cy + 12))
    nxt = [(fx0, cy - 22, cy + 22)] + nxt[1:]
    for (bx, by, bw, bh), (tx, ty0, ty1) in zip(zoom, nxt):
        o.append(rect(bx, by, bw, bh, "none", I["primary"], 1.0))
        o.append(H.line(s, bx + bw, by, tx, ty0, I["rule"], "leader", (3, 3)))
        o.append(H.line(s, bx + bw, by + bh, tx, ty1, I["rule"], "leader", (3, 3)))
    # ---- row 2: the crimp pulled out. Five fibrils, crimp strains uniform on (0, eps*], zig-zags drawn to the strain
    o.append(H.label(s, 380, 214, "Pulling the tendon: crimp straightens first (toe), then straight collagen is stretched "
                     "(linear)", "label", I["primary"], "middle"))
    ec = [EPS_STAR * (i + 0.5) / 5 for i in range(5)]           # 0.3, 0.9, 1.5, 2.1, 2.7 %
    states = [(0.0, "at rest"), (0.018, "toe"), (0.045, "linear")]
    X0, top = 196.0, 240.0
    for j, (e, name) in enumerate(states):
        xl = 22 + j * 250
        xr = xl + X0 * (1 + e)
        n_taut = 0
        for i, ei in enumerate(ec):
            pts, taut = zig_fibril(xl, xr, top + 10 + i * 14, X0 * (1 + ei))
            n_taut += taut
            o.append(fibril_rope(s, pts, taut))
        assert abs(n_taut / 5 - min(1.0, e / EPS_STAR)) < 1e-9          # Phi = eps / eps* (uniform crimp, line 167)
        for xg in (xl, xr):
            o.append(rect(xg - 3, top, 6, 76, I["secondary"], None, 0, 1))
        if e > 0:
            o.append(H.arrow(s, p, xr + 5, top + 38, xr + 30, top + 38, "force"))
        phi = "0" if n_taut == 0 else ("1" if n_taut == 5 else f"{n_taut / 5:.1f}")
        o.append(H.label(s, xl, top + 100, f"{name}: ε = {e * 100:.1f} %".replace(".0 %", " %"), "label2", I["primary"]))
        o.append(H.label(s, xl, top + 116, f"{n_taut} of 5 straight, Φ = {phi}", "label2", I["secondary"]))
    lg, _ = legend(s, 22, 384, [(sw_rect(tf, tl), "tendon tissue"),
                                (sw_line(tl, 3.6), "fibril, crimped (slack)"),
                                (sw_line(O["force"], 3.6), "fibril straight: carries tension"),
                                (sw_line(O["force"], 2.5), "pull")], gap=16)
    o.append(lg)
    aria = ("Collagen hierarchy, left to right: a tendon cord whose cut face shows fascicles; a fascicle, a sheathed bundle "
            "of crimped fibres; a fibre, a bundle of crimped fibrils; one fibril, banded every D-period of 67 nanometres; "
            "and the tropocollagen triple helix, 300 nanometres long. Below, five fibrils held between two grips, with "
            "crimp strains spread evenly up to 3 percent and drawn as zig-zags to that strain. At rest none is straight; "
            "at 1.8 percent strain, in the toe, three of five are straight and carry tension (red edge), recruited "
            "fraction 0.6; at 4.5 percent, in the linear region, all five are straight and the collagen itself is "
            "stretched.")
    return finish(VB, aria, s, o)


# ================================================================ svg #6  Prop. 1': gap and overlap from L_c
def fig6():
    VB = (0, 0, 760, 274)
    s = H.Scale(VB[2], VB[3])
    p = "m6f6_"
    k = LC_NM / D_NM
    ov = k - math.floor(k)
    assert abs(k - 4.478) < 5e-4 and round(ov * D_NM) == 32 and round((1 - ov) * D_NM) == 35
    S = 1.0                                     # px per nm
    xa, xb = 26.0, 744.0
    Dp, Lp = D_NM * S, LC_NM * S
    y0, dy, h = 52.0, 20.0, 10.0
    tf, tl = T["tendon"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # zone shading through the array: overlap (5 cross) and gap (4 cross), period D from the first molecule start
    zt, zb = y0 - 9, y0 + 4 * dy + 9
    kk = -1
    while xa + kk * Dp < xb:
        a0 = xa + kk * Dp
        for u0, u1, col, op in ((0, ov, O["geometry"], 0.13), (ov, 1, O["flag"], 0.22)):
            g0, g1 = max(xa, a0 + u0 * Dp), min(xb, a0 + u1 * Dp)
            if g1 > g0:
                o.append(rect(g0, zt, g1 - g0, zb - zt, col, None, 0, 0, f'opacity="{op}"'))
        kk += 1
    # five rows; row j holds molecules starting at j D + 5 n D (one molecule per stagger)
    hl = None
    for j in range(5):
        yy = y0 + j * dy
        for n in range(-2, 3):
            m0 = xa + (j + 5 * n) * Dp
            m1 = m0 + Lp
            g0, g1 = max(xa, m0), min(xb, m1)
            if g1 <= g0:
                continue
            full = g0 == m0 and g1 == m1
            o.append(rect(g0, yy - h / 2, g1 - g0, h, tf, tl, s(1.1), h / 2 if full else 0))
            if j == 0 and n == 0:
                hl = (m0, m1, yy)
    m0, m1, yy = hl
    o.append(rect(m0, yy - h / 2, m1 - m0, h, "none", I["primary"], s(1.6), h / 2))
    o.append(dim(s, p, m0, m1, 22, f"one molecule: {it('L')}{H.sub('c', s, 'label2')} = {LC_NM:.0f} nm = {k:.2f} {it('D')}",
                 meaning="dim", ext=(yy - 6, yy - 6)))
    # zone strip with molecule counts, and the dimensions of one period
    ys = zb + 26
    kk = 0
    while xa + kk * Dp < xb:
        a0 = xa + kk * Dp
        for u0, u1, col, op, n in ((0, ov, O["geometry"], 0.30, "5"), (ov, 1, O["flag"], 0.45, "4")):
            g0, g1 = max(xa, a0 + u0 * Dp), min(xb, a0 + u1 * Dp)
            if g1 > g0:
                o.append(rect(g0, ys - 9, g1 - g0, 18, col, None, 0, 0, f'opacity="{op}"'))
                if g1 - g0 > 20:
                    o.append(H.label(s, (g0 + g1) / 2, ys + 5, n, "label2", I["primary"], "middle"))
        kk += 1
    a0 = xa + 5 * Dp
    yd = ys + 36
    o.append(dim(s, p, a0, a0 + Dp, yd, f"one period {it('D')} = {D_NM:.0f} nm", ty=yd + 22, ext=(ys + 10, ys + 10)))
    o.append(dim(s, p, a0 + Dp, a0 + Dp + ov * Dp, yd, "", ext=(None, ys + 10)))
    o.append(H.label(s, a0 + Dp + ov * Dp + 6, yd + 5, f"overlap {ov:.2f} {it('D')} = {ov * D_NM:.0f} nm", "label2", O["geometry"]))
    o.append(dim(s, p, a0 - (1 - ov) * Dp, a0, yd, "", ext=(ys + 10, None)))
    o.append(H.label(s, a0 - (1 - ov) * Dp - 6, yd + 5, f"gap {1 - ov:.2f} {it('D')} = {(1 - ov) * D_NM:.0f} nm", "label2",
                     O["geometry"], "end"))
    o.append(H.label(s, xa, ys + 82, "molecules crossing a plane: 5 in the overlap zone, 4 in the gap zone",
                     "label2", I["secondary"]))
    o.append(H.label(s, xa, ys + 100, f"{it('L')}{H.sub('c', s, 'label2')}/{it('D')} = 300/67 = {k:.3f}: the crowded fraction of "
                     f"each period is {ov:.3f}. Measured gap: {GAP_MEAS:.2f} {it('D')} ≈ {GAP_MEAS * D_NM:.0f} nm.",
                     "label2", I["secondary"]))
    lg, _ = legend(s, 500, ys + 82, [(sw_rect(O["geometry"], None, 0.4), "overlap"), (sw_rect(O["flag"], None, 0.5), "gap")], gap=14)
    o.append(lg)
    aria = ("Staggered tropocollagen array drawn to scale, 1 pixel per nanometre: five rows of 300 nanometre molecules, each "
            "row offset by one D-period of 67 nanometres, so one molecule starts every period. One molecule is outlined: "
            "length 300 nanometres, 4.48 D. Blue overlap zones of 0.48 D, 32 nanometres, where five molecules cross a plane, "
            "alternate with orange gap zones of 0.52 D, 35 nanometres, where four cross. Measured gap 0.54 D, about 36 "
            "nanometres.")
    return finish(VB, aria, s, o)


# ================================================================ svg #7  Fig. 4: tendon segment, material -> structural
def fig7():
    VB = (0, 0, 760, 268)
    s = H.Scale(VB[2], VB[3])
    p = "m6f7_"
    eps = X_PUSH / L0_MM
    assert abs(eps - 0.064) < 1e-9
    yc, th = 128.0, 34.0
    bone, (bx0, bx1, by0, by1) = femur_end(28.0, yc, 70.0)
    xa = bx1 - 10                                # tendon fibres run into the bone end
    L0p = 470.0
    xr, xe = xa + L0p, xa + L0p * (1 + eps)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(cord(s, xa, xe, yc, th, lines=4))
    o.append(bone)
    o.append(H.label(s, (bx0 + bx1) / 2 - 10, by0 - 10, "bone", "label", I["primary"], "middle"))
    o.append(H.label(s, xa + 120, yc + 5, "tendon", "label", I["primary"], "middle"))
    # cross-section: a cut across the tendon, the face shown above it
    xc = xa + 300
    o.append(H.line(s, xc, yc - th / 2 - 6, xc, yc + th / 2 + 6, O["dim"], "ref", H.DASH_REF))
    o.append(f'<ellipse cx="{xc:.1f}" cy="{yc - 70:.1f}" rx="9" ry="{th / 2:.1f}" fill="{T["tendon"][0]}" '
             f'stroke="{T["tendon"][1]}" stroke-width="{s(1.2):.2f}"/>')
    o.append(H.line(s, xc, yc - th / 2 - 8, xc, yc - 70 + th / 2 + 4, I["rule"], "leader", (3, 3)))
    o.append(H.label(s, xc + 18, yc - 72, f"cross-section, area {it('A')}{H.sub('0', s)}", "label", I["primary"]))
    # rest end, elongation, rest length
    o.append(H.line(s, xr, yc - th / 2 - 22, xr, yc + th / 2 + 10, O["dim"], "ref", H.DASH_REF))
    o.append(H.label(s, xr - 6, yc - th / 2 - 26, "rest end", "label2", I["secondary"], "end"))
    o.append(dim(s, p, xr, xe, yc - th / 2 - 12, it("x"), ty=yc - th / 2 - 20, ext=(None, yc - th / 2), size="label",
                 anchor="start", tx=xe + 6))
    o.append(dim(s, p, xa, xr, yc + th / 2 + 26, f"rest length {it('L')}{H.sub('0', s, 'label2')}", ty=yc + th / 2 + 44,
                 ext=(yc + th / 2 + 2, yc + th / 2 + 10)))
    o.append(H.arrow(s, p, xe + 2, yc, xe + 64, yc, "force"))
    o.append(H.label(s, xe + 30, yc - 12, it("F"), "label", O["force"], "middle"))
    o.append(H.label(s, xe + 4, yc + 24, "muscle tension", "label2", I["secondary"]))
    o.append(H.label(s, 380, 22, f"structural:  {it('F')} = {it('σ')} {it('A')}{H.sub('0', s)},   elongation  {it('x')} = "
                     f"{it('ε')} {it('L')}{H.sub('0', s)}", "label", I["primary"], "middle"))
    o.append(H.label(s, xa, yc + th / 2 + 68, f"drawn at {it('ε')} = {eps * 100:.1f} %: the Achilles at a running push-off, "
                     f"{it('x')} ≈ {X_PUSH:.0f} mm of {it('L')}{H.sub('0', s, 'label2')} ≈ {L0_MM:.0f} mm "
                     f"({it('A')}{H.sub('0', s, 'label2')} ≈ {A0_MM2:.0f} mm²)", "label2", I["secondary"]))
    o.append(femur_credit(s, 10, 252))
    aria = ("A tendon segment anchored to a bone end at the left and pulled by muscle tension F at the right. Its rest "
            "length L zero runs from the bone to a dashed rest end; under F it elongates by x past that line. A dashed cut "
            "across the tendon shows its cross-section of area A zero. Structural force F equals sigma A zero, elongation "
            "x equals epsilon L zero. The stretch is drawn at 6.4 percent, the Achilles at a running push-off: about 16 "
            "millimetres of 250, cross-section about 80 square millimetres.")
    return finish(VB, aria, s, o)


# ================================================================ svg #10  Fig. 7: two springs, one peak force
def fig10():
    VB = (0, 0, 760, 398)
    s = H.Scale(VB[2], VB[3])
    kc, ks = K_MEAS
    F = F_PUSH
    xs_, xc_ = F / ks, F / kc                    # mm
    Us, Uc = 0.5 * F * xs_ / 1000, 0.5 * F * xc_ / 1000
    assert abs(Us - F ** 2 / (2 * ks * 1e3)) < 1e-9 and round(Us, 1) == 31.2 and round(Uc, 1) == 83.3
    ax = Ax((92, 50, 730, 316), (0, 40), (0, 6))
    o = []
    o.append(f'<path d="M{ax.X(0):.2f},{ax.Y(0):.2f} L{ax.X(xc_):.2f},{ax.Y(F / 1e3):.2f} L{ax.X(xc_):.2f},{ax.Y(0):.2f} Z" '
             f'fill="{SER[1]}" opacity="0.14"/>')
    o.append(f'<path d="M{ax.X(0):.2f},{ax.Y(0):.2f} L{ax.X(xs_):.2f},{ax.Y(F / 1e3):.2f} L{ax.X(xs_):.2f},{ax.Y(0):.2f} Z" '
             f'fill="{SER[0]}" opacity="0.20"/>')
    o += axes(s, ax, [(v, f"{v}") for v in range(0, 41, 10)], [(v, f"{v}") for v in range(7)],
              "elongation x (mm)", "force F (kN)")
    o.append(H.line(s, ax.X(0), ax.Y(F / 1e3), ax.X(xc_), ax.Y(F / 1e3), O["dim"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(xc_) + 8, ax.Y(F / 1e3) + 5, "same peak force", "label2", I["primary"]))
    o.append(H.label(s, ax.X(xc_) + 8, ax.Y(F / 1e3) + 21, f"{it('F')} = {F / 1e3:.0f} kN", "label2", I["primary"]))
    for xm, col in ((xs_, SER[0]), (xc_, SER[1])):
        o.append(poly(s, [(ax.X(0), ax.Y(0)), (ax.X(xm), ax.Y(F / 1e3))], col))
    o.append(H.label(s, ax.X(xs_) + 8, ax.Y(4.4), f"stiff, {it('k')} = {ks:.0f} N/mm", "label2", I["primary"]))
    o.append(H.label(s, ax.X(xs_) + 8, ax.Y(4.4) + 16, f"{it('x')} = {xs_:.1f} mm", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(xs_ / 2) + 22, ax.Y(0.55), f"{it('U')} = {Us:.0f} J", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(24), ax.Y(2.15), f"compliant, {it('k')} = {kc:.0f} N/mm", "label2", I["primary"]))
    o.append(H.label(s, ax.X(24), ax.Y(2.15) + 16, f"{it('x')} = {xc_:.1f} mm", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(26), ax.Y(0.8), f"{it('U')} = ½{it('F x')} = {it('F')}²/2{it('k')} = {Uc:.0f} J",
                     "label2", I["primary"], "middle"))
    o += plegend(s, 110, 28, [(SER[0], None, f"stiff spring (k = {ks:.0f} N/mm), area U = {Us:.0f} J"),
                              (SER[1], None, f"compliant spring (k = {kc:.0f} N/mm), area U = {Uc:.0f} J")], gap=20)
    o.append(H.label(s, 730, 390, "stiffnesses: the measured free-Achilles range, 150–400 N/mm (§2); "
                     "F: a hard running push-off (§3)", "label2", I["muted"], "end"))
    hv = []
    for i in range(161):
        x = 40 * i / 160
        ys, txt = [], [f"x = {x:.2f} mm"]
        if x <= xs_:
            ys.append(ax.Y(ks * x / 1e3))
            txt.append(f"stiff {ks * x / 1e3:.2f} kN, U {0.5 * ks * x * x / 1e3:.1f} J")
        if x <= xc_:
            ys.append(ax.Y(kc * x / 1e3))
            txt.append(f"compliant {kc * x / 1e3:.2f} kN, U {0.5 * kc * x * x / 1e3:.1f} J")
        if ys:
            hv.append([ax.X(x), ys, ", ".join(txt)])
    aria = ("Force against elongation for two linear springs pulled to the same peak force of 5 kilonewtons. The stiff "
            "spring, 400 newtons per millimetre (red), stretches 12.5 millimetres and encloses a triangle of 31 joules; "
            "the compliant spring, 150 newtons per millimetre (blue), stretches 33.3 millimetres and encloses 83 joules. "
            "The two stiffnesses are the ends of the measured free-Achilles range.")
    return finish(VB, aria, s, o, extra=H.hover_attr(ax.box, hv))


# ================================================================ svg #11  Fig. 8: the muscle-tendon unit
def pennate_left(s, p, xb, ya, yt, wl, th, pitch=20.0):
    """Unipennate sheet: origin aponeurosis on y = ya from xb to xb + wl, fibres down-right at th to the insertion
    aponeurosis on y = yt. Returns (svg, run)."""
    run = (yt - ya) / math.tan(th)
    o = [f'<defs>{muscle_grad(p + "mg", xb, ya, xb + run, yt)}</defs>',
         tissue(s, [(xb, ya), (xb + wl, ya), (xb + wl + run, yt), (xb + run, yt)], fill=f"url(#{p}mg)")]
    x = xb + pitch / 2
    while x < xb + wl:
        o.append(fibre_line(s, x, ya, x + run, yt, 0.75, 1.0))
        x += pitch
    return "".join(o), run


def fig11():
    VB = (0, 0, 760, 330)
    s = H.Scale(VB[2], VB[3])
    p = "m6f11_"
    th = math.radians(TH_P)
    ya, yt = 70.0, 156.0
    bone, (bx0, bx1, by0, by1) = femur_end(12.0, (ya + yt) / 2, 104.0, y_cut=318.0)
    xb = bx1 - 4
    o = [f'<defs>{H.markers(p, s)}</defs>', bone]
    wl = 112.0
    sheet, run = pennate_left(s, p, xb, ya, yt, wl, th)
    o.append(rect(xb - 2, ya - 6, wl + 4, 7, T["tendon"][0], T["tendon"][1], s(1.0), 3))     # origin aponeurosis
    o.append(sheet)
    xi = xb + run                                 # insertion end of the first fibre: the CE's projected end
    xs0 = xi + wl + 10                            # aponeurosis -> free tendon
    xe = 612.0
    o.append(rect(xi - 2, yt - 1, wl + 14, 7, T["tendon"][0], T["tendon"][1], s(1.0), 3))     # insertion aponeurosis
    o.append(tissue_spring(s, xs0, xe, yt + 2.5, n=9, amp=11))
    o.append(circ(xe, yt + 2.5, 5, T["tendon"][0], T["tendon"][1], s(1.2)))
    # the one fibre the Hill model lumps: outlined, length l along it, angle theta_p to the line of action
    o.append(H.line(s, xb, ya, xi, yt, T["muscle_dk"][1], "geom", extra=f'stroke-width="{s(3.2):.2f}"'))
    o.append(H.line(s, xi - 64, yt, xi + 40, yt, O["dim"], "ref", H.DASH_REF))      # line of action through the fibre end
    o.append(angle_arc(s, xi, yt, 48, 180, 180 - TH_P))
    o.append(H.label(s, xi - 54, yt - 14, f"{it('θ')}{H.sub('p', s)}", "label", O["geometry"], "end"))
    mx, my = (xb + xi) / 2, (ya + yt) / 2
    o.append(H.label(s, mx - 16, my + 4, it("ℓ"), "label", I["primary"], "end"))
    o.append(H.label(s, xb + 30, 30, "contractile element (CE): Module 5’s pennate muscle", "label", I["primary"]))
    o.append(H.label(s, xs0 - 20, yt - 52, "series-elastic element (SE):", "label", I["primary"]))
    o.append(H.label(s, xs0 - 20, yt - 34, "the tendon, drawn as a spring", "label", I["primary"]))
    o.append(H.arrow(s, p, xe + 8, yt + 2.5, xe + 70, yt + 2.5, "force"))
    o.append(H.label(s, xe + 40, yt - 10, it("F"), "label", O["force"], "middle"))
    o.append(H.label(s, xe + 12, yt + 26, "one tension", "label2", I["secondary"]))
    o.append(H.label(s, xe + 12, yt + 41, "through both", "label2", I["secondary"]))
    # tendon stretch x past its slack length
    eps_draw = X_PUSH / L0_MM
    xts = xi + (xe - xi) / (1 + eps_draw)
    o.append(H.line(s, xts, yt - 14, xts, yt + 22, O["dim"], "ref", H.DASH_REF))
    # dimensions: projected fibre, tendon, whole unit (they chain: L_MTU = l cos theta_p + L_T)
    y1, y2, y3 = 210.0, 246.0, 286.0
    o.append(dim(s, p, xb, xi, y1, f"{it('ℓ')} cos {it('θ')}{H.sub('p', s, 'label2')}", ext=(ya + 4, yt + 6)))
    o.append(dim(s, p, xi, xts, y1, f"slack length {it('L')}{H.sub('Ts', s, 'label2')}", ext=(None, yt + 22)))
    o.append(dim(s, p, xts, xe, y1, it("x"), ext=(None, yt + 10)))
    o.append(dim(s, p, xi, xe, y2, f"tendon {it('L')}{H.sub('T', s, 'label2')} = {it('L')}{H.sub('Ts', s, 'label2')} + "
                 f"{it('x')}", meaning="dim", ext=(y1 + 4, y1 + 4)))
    o.append(dim(s, p, xb, xe, y3, f"whole unit {it('L')}{H.sub('MTU', s, 'label2')} = {it('ℓ')} cos "
                 f"{it('θ')}{H.sub('p', s, 'label2')} + {it('L')}{H.sub('T', s, 'label2')}", meaning="dim",
                 ext=(y2 + 4, y1 + 4)))
    lg, _ = legend(s, 10, 316, [(sw_rect(T["muscle"][0], T["muscle"][1]), "muscle fibres"),
                                (sw_rect(T["tendon"][0], T["tendon"][1]), "tendon and aponeurosis"),
                                (sw_rect(T["bone"][0], T["bone"][1]), "bone"),
                                (sw_line(O["force"]), "tension"), (sw_line(O["geometry"], 2), "length, angle")], gap=14)
    o.append(lg)
    aria = ("Muscle-tendon unit. From a femur end at the left, a unipennate muscle, the contractile element CE of Module 5, "
            "runs between two aponeuroses; its fibres make the pennation angle theta p, 25 degrees here, with the line of "
            "action. One fibre of length l is outlined; its projection on the line of action is l cos theta p. The "
            "insertion aponeurosis continues into the tendon, the series-elastic element SE, drawn as a spring, of length "
            "L T, its slack length L Ts plus the stretch x. One tension F pulls through both. The whole-unit length is "
            "L MTU = l cos theta p + L T.")
    return finish(VB, aria, s, o)


# ================================================================ svg #14  Fig. 11: spring and dashpot
def step_panel(s, ax, kind):
    """Strain response to a step stress at t = 0: spring holds sigma0/E; dashpot ramps at sigma0/eta."""
    ts = [ax.xr[0] + (ax.xr[1] - ax.xr[0]) * i / 100 for i in range(101)]
    ep = [0.0 if t < 0 else (1.0 if kind == "spring" else t) for t in ts]
    pts = [(ax.X(t), ax.Y(e)) for t, e in zip(ts, ep)]
    i0 = next(i for i, t in enumerate(ts) if t >= 0)
    pts.insert(i0, (ax.X(0), ax.Y(0)))
    hv = [[ax.X(t), ax.Y(e), f"t = {t:.2f}: ε = {e:.2f} " + ("σ₀/E" if kind == "spring" else "σ₀ t₁/η")] for t, e in zip(ts, ep)]
    return poly(s, pts, SER[0]), hv


def fig14():
    VB = (0, 0, 760, 330)
    s = H.Scale(VB[2], VB[3])
    p = "m6f14_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    rows = [(78.0, "spring", "Hookean spring (elastic)", f"{it('σ')} = {it('E ε')}",
             "responds to strain: stores energy, returns all, no rate dependence"),
            (238.0, "dashpot", "Newtonian dashpot (viscous)", f"{it('σ')} = {it('η ε' + DOT)}",
             "responds to strain rate: dissipates all as heat, force ∝ speed")]
    hvs = []
    for yc, kind, name, law, note in rows:
        o.append(H.label(s, 24, yc - 46, name, "label", I["primary"]))
        o.append(node(s, 60, yc))
        o.append(spring(s, 60, 300, yc, 8, 12) if kind == "spring" else dashpot(s, 60, 300, yc, 26))
        o.append(node(s, 300, yc))
        o.append(H.arrow(s, p, 56, yc, 22, yc, "force"))
        o.append(H.arrow(s, p, 304, yc, 338, yc, "force"))
        o.append(H.label(s, 18, yc - 8, it("σ"), "label", O["force"], "end"))
        o.append(H.label(s, 342, yc - 8, it("σ"), "label", O["force"]))
        o.append(H.label(s, 180, yc + 38, law, "label", I["primary"], "middle"))
        o.append(H.label(s, 24, yc + 60, note, "label2", I["secondary"]))
        ax = Ax((480, yc - 54, 730, yc + 36), (-0.25, 1.0), (0, 1.25))
        o += axes(s, ax, [(0, "0")], [], "", "", grid=False)
        o.append(H.label(s, ax.x1, ax.y0 + 20, it("t"), "label2", I["primary"], "end"))
        o.append(H.label(s, ax.x0 - 8, ax.top + 10, it("ε"), "label2", I["primary"], "end"))
        o.append(H.line(s, ax.X(0), ax.top, ax.X(0), ax.y0, O["dim"], "ref", H.DASH_REF))
        o.append(H.label(s, ax.X(0) + 4, ax.top - 6, f"step stress {it('σ')}{H.sub('0', s, 'label2')} at {it('t')} = 0",
                         "label2", I["secondary"]))
        pl, hv = step_panel(s, ax, kind)
        o.append(pl)
        hvs.append((ax.box, hv))
        if kind == "spring":
            o.append(H.label(s, ax.X(0.55), ax.Y(1.0) + 22, f"instant jump to {it('σ')}{H.sub('0', s, 'label2')}/{it('E')}, held",
                             "label2", I["primary"], "middle"))
        else:
            o.append(H.label(s, ax.X(0.05), ax.Y(1.0), "ramps without bound,", "label2", I["primary"]))
            o.append(H.label(s, ax.X(0.05), ax.Y(1.0) + 16, f"slope {it('σ')}{H.sub('0', s, 'label2')}/{it('η')}",
                             "label2", I["primary"]))
    lg, _ = legend(s, 480, 322, [(sw_line(SER[0]), "strain response ε(t)"), (sw_rect(T["fluid"][0], None, 0.75), "viscous fluid")],
                   gap=14)
    o.append(lg)
    aria = ("The two ideal elements. Top: a coil spring pulled by stress sigma at both ends, law sigma = E epsilon; under a "
            "step stress sigma zero at t = 0 its strain jumps at once to sigma zero over E and holds. Bottom: a dashpot, a "
            "piston in a cylinder of viscous fluid, law sigma = eta times the strain rate; under the same step its strain "
            "ramps up without bound at slope sigma zero over eta.")
    return finish(VB, aria, s, o, extra=H.hover_attr(hvs))


# ================================================================ svg #15  Fig. 12: three networks
def net_maxwell(s, x0, x1, y, sub=True):
    xm = x0 + 0.48 * (x1 - x0)
    o = [node(s, x0, y), spring(s, x0, xm, y, 7, 10), dashpot(s, xm, x1, y, 22), node(s, x1, y)]
    lab = [(x0 + (xm - x0) / 2, y - 18, f"{it('E')}{H.sub('M', s) if sub else ''}"), (xm + 0.55 * (x1 - xm), y - 18, it("η"))]
    return "".join(o), lab


def net_kv(s, x0, x1, y, dyb=24.0, sub=True):
    b0, b1 = x0 + 34, x1 - 34
    o = [node(s, x0, y), node(s, x1, y), wire(s, [(x0, y), (b0, y)]), wire(s, [(b1, y), (x1, y)]),
         crossbar(s, b0, y - dyb - 4, y + dyb + 4), crossbar(s, b1, y - dyb - 4, y + dyb + 4),
         spring(s, b0, b1, y - dyb, 8, 9), dashpot(s, b0, b1, y + dyb, 22)]
    lab = [((b0 + b1) / 2, y - dyb - 16, f"{it('E')}{H.sub('K', s) if sub else ''}"), (b0 + 0.66 * (b1 - b0), y + dyb - 16, it("η"))]
    return "".join(o), lab


def net_sls(s, x0, x1, y, dyb=24.0):
    b0, b1 = x0 + 34, x1 - 34
    bm = b0 + 0.45 * (b1 - b0)
    o = [node(s, x0, y), node(s, x1, y), wire(s, [(x0, y), (b0, y)]), wire(s, [(b1, y), (x1, y)]),
         crossbar(s, b0, y - dyb - 4, y + dyb + 4), crossbar(s, b1, y - dyb - 4, y + dyb + 4),
         spring(s, b0, b1, y - dyb, 8, 9), spring(s, b0, bm, y + dyb, 6, 9), dashpot(s, bm, b1, y + dyb, 22)]
    lab = [((b0 + b1) / 2, y - dyb - 16, f"{it('E')}{H.sub('0', s)}"), ((b0 + bm) / 2, y + dyb - 16, f"{it('E')}{H.sub('1', s)}"),
           (bm + 0.62 * (b1 - bm), y + dyb - 16, it("η"))]
    return "".join(o), lab


def fig15():
    VB = (0, 0, 760, 372)
    s = H.Scale(VB[2], VB[3])
    p = "m6f15_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    x0, x1 = 40.0, 400.0
    rows = [(62.0, net_maxwell(s, x0, x1, 62.0), "Maxwell: spring and dashpot in series",
             f"{it('ε' + DOT)} = {it('σ' + DOT)}/{it('E')}{H.sub('M', s, 'label2')} + {it('σ')}/{it('η')}   (6.1)",
             "relaxes fully; creeps without bound"),
            (180.0, net_kv(s, x0, x1, 180.0), "Kelvin–Voigt: spring and dashpot in parallel",
             f"{it('σ')} = {it('E')}{H.sub('K', s, 'label2')}{it('ε')} + {it('η ε' + DOT)}   (6.2)",
             "bounded creep; no instant jump; no relaxation"),
            (306.0, net_sls(s, x0, x1, 306.0), "standard linear solid: E₀ ∥ (E₁ in series with η)",
             f"{it('τ')}{H.sub('σ', s, 'label2')}{it('σ' + DOT)} + {it('σ')} = {it('E')}{H.sub('R', s, 'label2')}"
             f"({it('ε')} + {it('τ')}{H.sub('ε', s, 'label2')}{it('ε' + DOT)})   (6.3)",
             "instant jump; bounded creep; relaxes to a plateau")]
    for yc, (net, labs), name, law, note in rows:
        o.append(net)
        for lx, ly, t in labs:
            o.append(H.label(s, lx, ly, t, "label", I["primary"], "middle"))
        o.append(H.arrow(s, p, x1 + 4, yc, x1 + 36, yc, "force"))
        o.append(H.label(s, x1 + 20, yc - 8, it("σ"), "label", O["force"], "middle"))
        o.append(H.label(s, 452, yc - 14, name.replace("E₀", f"{it('E')}{H.sub('0', s)}").replace("E₁", f"{it('E')}{H.sub('1', s)}")
                         .replace("η)", f"{it('η')})"),
                         "label", I["primary"]))
        o.append(H.label(s, 452, yc + 8, law, "label2", I["primary"]))
        o.append(H.label(s, 452, yc + 26, note, "label2", I["secondary"]))
    o.append(wall(s, x0 - 8, 44, 80))
    o.append(wire(s, [(x0 - 8, 62), (x0, 62)]))
    for yc in (180.0, 306.0):
        o.append(wall(s, x0 - 8, yc - 18, yc + 18))
        o.append(wire(s, [(x0 - 8, yc), (x0, yc)]))
    o.append(H.label(s, 380, 366, "series elements share stress and their strains add; parallel elements share strain "
                     "and their stresses add", "label2", I["muted"], "middle"))
    aria = ("Three viscoelastic networks, each fixed at a wall on the left and pulled by stress sigma on the right. "
            "Maxwell: a spring E M and a dashpot eta in series; it relaxes fully and creeps without bound. Kelvin-Voigt: a "
            "spring E K and a dashpot eta in parallel between two rigid crossbars; bounded creep, no instant jump, no "
            "relaxation. Standard linear solid: an equilibrium spring E 0 in parallel with a Maxwell arm, spring E 1 in "
            "series with dashpot eta; instant jump, bounded creep, relaxation to a plateau. Each row gives its law, "
            "equations 6.1 to 6.3.")
    return finish(VB, aria, s, o)


# ================================================================ svg #16  Fig. 13: series and parallel as free bodies
def block(s, x, y, w, h, txt):
    return rect(x, y - h / 2, w, h, "#f7f4ef", I["axis"], s(1.4), 4) + H.label(s, x + w / 2, y + 5, txt, "label", I["primary"], "middle")


def fig16():
    VB = (0, 0, 760, 330)
    s = H.Scale(VB[2], VB[3])
    p = "m6f16_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(H.label(s, 186, 22, "series: a chain, end to end", "label", I["primary"], "middle"))
    o.append(H.label(s, 574, 22, "parallel: side by side, shared ends", "label", I["primary"], "middle"))
    E1, E2 = f"{it('E')}{H.sub('1', s)}", f"{it('E')}{H.sub('2', s)}"
    # ---- series
    y = 88.0
    o.append(block(s, 60, y, 100, 40, E1))
    o.append(block(s, 212, y, 100, 40, E2))
    o.append(wire(s, [(160, y), (212, y)]))
    o.append(node(s, 186, y, 4.5))
    o.append(H.arrow(s, p, 56, y, 14, y, "force"))
    o.append(H.arrow(s, p, 316, y, 358, y, "force"))
    o.append(H.label(s, 30, y - 10, it("F"), "label", O["force"], "middle"))
    o.append(H.label(s, 340, y - 10, it("F"), "label", O["force"], "middle"))
    o.append(H.label(s, 186, y - 28, "junction", "label2", I["secondary"], "middle"))
    o.append(dim(s, p, 60, 160, y + 40, f"Δ{H.sub('1', s, 'label2')}", ty=y + 58, ext=(y + 22, y + 22)))
    o.append(dim(s, p, 212, 312, y + 40, f"Δ{H.sub('2', s, 'label2')}", ty=y + 58, ext=(y + 22, y + 22)))
    # free body of the massless junction
    yj = 192.0
    o.append(node(s, 186, yj, 5))
    o.append(H.arrow(s, p, 180, yj, 128, yj, "force"))
    o.append(H.arrow(s, p, 192, yj, 244, yj, "force"))
    o.append(H.label(s, 128, yj - 9, f"{it('F')}{H.sub('1', s)}", "label", O["force"]))
    o.append(H.label(s, 244, yj - 9, f"{it('F')}{H.sub('2', s)}", "label", O["force"], "end"))
    o.append(H.label(s, 186, yj + 24, f"massless junction: {it('F')}{H.sub('1', s, 'label2')} = {it('F')}{H.sub('2', s, 'label2')} = {it('F')}",
                     "label2", I["secondary"], "middle"))
    o.append(H.label(s, 20, 260, f"same force → {it('σ')}{H.sub('1', s)} = {it('σ')}{H.sub('2', s)}  (equilibrium)", "label"))
    o.append(H.label(s, 20, 284, f"elongations add → {it('ε')} = {it('ε')}{H.sub('1', s)} + {it('ε')}{H.sub('2', s)}  (compatibility)",
                     "label"))
    # ---- parallel: fixed crossbar (wall) on the left, free crossbar on the right pulled by F
    xl, xr0, xr = 430.0, 640.0, 664.0
    ya_, yb_, bt, bb = 66.0, 130.0, 46.0, 150.0
    o.append(wall(s, xl - 6, bt, bb))
    o.append(crossbar(s, xl, bt, bb, 7))
    o.append(rect(xr0 - 3.5, bt, 7, bb - bt, "none", I["rule"], s(1.0), 1, f'stroke-dasharray="{s(4):.1f} {s(3):.1f}"'))
    o.append(crossbar(s, xr, bt, bb, 7))
    for yy, t in ((ya_, E1), (yb_, E2)):
        o.append(block(s, xl + 32, yy, xr - xl - 64, 38, t))
        o.append(wire(s, [(xl + 3, yy), (xl + 32, yy)]))
        o.append(wire(s, [(xr - 32, yy), (xr - 3, yy)]))
    o.append(H.arrow(s, p, xr + 6, (ya_ + yb_) / 2, xr + 56, (ya_ + yb_) / 2, "force"))
    o.append(H.label(s, xr + 32, (ya_ + yb_) / 2 - 10, it("F"), "label", O["force"], "middle"))
    o.append(dim(s, p, xr0, xr, 166, "Δ: one stretch for both", ty=171, ext=(bb, bb), anchor="end", tx=xr0 - 8))
    # crossbar free body
    yf, xf = 212.0, 560.0
    o.append(crossbar(s, xf, yf - 20, yf + 20, 7))
    o.append(H.arrow(s, p, xf + 5, yf, xf + 60, yf, "force"))
    o.append(H.arrow(s, p, xf - 5, yf - 10, xf - 52, yf - 10, "force"))
    o.append(H.arrow(s, p, xf - 5, yf + 10, xf - 52, yf + 10, "force"))
    o.append(H.label(s, xf + 64, yf + 5, it("F"), "label", O["force"]))
    o.append(H.label(s, xf - 58, yf - 5, f"{it('F')}{H.sub('1', s)}", "label", O["force"], "end"))
    o.append(H.label(s, xf - 58, yf + 15, f"{it('F')}{H.sub('2', s)}", "label", O["force"], "end"))
    o.append(H.label(s, xf + 12, yf + 22, "free crossbar", "label2", I["secondary"]))
    o.append(H.label(s, 410, 260, f"shared stretch → {it('ε')}{H.sub('1', s)} = {it('ε')}{H.sub('2', s)}  (compatibility)", "label"))
    o.append(H.label(s, 410, 284, f"crossbar balance → {it('F')} = {it('F')}{H.sub('1', s)} + {it('F')}{H.sub('2', s)}, so "
                     f"{it('σ')} = {it('σ')}{H.sub('1', s)} + {it('σ')}{H.sub('2', s)}", "label"))
    o.append(H.label(s, 410, 302, "(equilibrium)", "label", I["primary"]))
    lg, _ = legend(s, 20, 322, [(sw_line(O["force"]), "force"), (sw_line(O["geometry"], 2), "elongation"),
                                (sw_rect(I["secondary"]), "rigid crossbar"),
                                (sw_line(I["rule"], 1.0, "4 3"), "free crossbar at rest")], gap=16)
    o.append(lg)
    aria = ("Free-body view of the two sharing rules. Left, series: elements E 1 and E 2 joined end to end at a junction "
            "and pulled by the same force F at both ends; a free body of the massless junction shows F 1 = F 2 = F, so "
            "sigma 1 = sigma 2 by equilibrium, and the elongations delta 1 and delta 2 add, epsilon = epsilon 1 + "
            "epsilon 2, by compatibility. Right, parallel: E 1 and E 2 span the same gap between a fixed crossbar and a "
            "free one, so they share one stretch delta, epsilon 1 = epsilon 2; a free body of the crossbar shows F 1 and "
            "F 2 balancing F, so F = F 1 + F 2 and sigma = sigma 1 + sigma 2.")
    return finish(VB, aria, s, o)


# ================================================================ svg #17  Fig. 14: creep and relaxation, three models
def responses():
    """Line 496 (Maxwell), 509 (Kelvin-Voigt), 528-529 (SLS). SLS constants line 543 / 1068 / 1088; Maxwell takes the SLS
    instantaneous modulus and tau_sigma, Kelvin-Voigt the relaxed modulus and tau_eps (a design choice, so the three rows
    share one stress and one strain scale); both then have the same eta = 1.08e8 Pa s."""
    EI = ER * TE / TS
    assert abs(EI - 2.16e9) < 1e3
    s0 = ER * EPS0                                  # 12 MPa: the held stress whose SLS equilibrium strain is eps0
    EM, eta_M = EI, EI * TS
    EK, eta_K = ER, ER * TE
    assert abs(eta_M - eta_K) < 1 and abs(eta_M - 1.08e8) < 1e3
    creep = {"M": lambda t: s0 / EM + s0 / eta_M * t,
             "K": lambda t: s0 / EK * (1 - math.exp(-t / TE)),
             "S": lambda t: s0 / EI + s0 * (1 / ER - 1 / EI) * (1 - math.exp(-t / TE))}
    relax = {"M": lambda t: EM * EPS0 * math.exp(-t / TS),
             "K": lambda t: EK * EPS0,
             "S": lambda t: ER * EPS0 + (EI - ER) * EPS0 * math.exp(-t / TS)}
    return s0, EI, creep, relax


def fig17():
    VB = (0, 0, 760, 584)
    s = H.Scale(VB[2], VB[3])
    p = "m6f17_"
    s0, EI, creep, relax = responses()
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(H.label(s, 290, 20, f"creep: stress {it('σ')}{H.sub('0', s)} = {s0 / 1e6:.0f} MPa held from {it('t')} = 0",
                     "label", I["primary"], "middle"))
    o.append(H.label(s, 590, 20, f"relaxation: strain {it('ε')}{H.sub('0', s)} = {EPS0 * 100:.0f} % held", "label",
                     I["primary"], "middle"))
    names = [("M", "Maxwell"), ("K", "Kelvin–Voigt"), ("S", "SLS")]
    T0, T1 = -0.04, 0.40
    tt = [T0 + (T1 - T0) * i / 110 for i in range(111)]
    panels = []
    for r, (key, nm) in enumerate(names):
        top = 52 + r * 160
        o.append(H.label(s, 12, top + 56, nm, "label", I["primary"]))
        axc = Ax((150, top, 420, top + 104), (T0, T1), (0, 2.0))
        axr = Ax((480, top, 750, top + 104), (T0, T1), (0, 25.0))
        last = r == 2
        xt = [(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3, 0.4)] if last else [(v, "") for v in (0, 0.1, 0.2, 0.3, 0.4)]
        o += axes(s, axc, xt, [(0, "0"), (1, "1"), (2, "2")], "t (s)" if last else "", "", grid=True)
        o += axes(s, axr, xt, [(0, "0"), (12, "12"), (24, "24")], "t (s)" if last else "", "", grid=True)
        o.append(H.label(s, axc.x0 + 6, axc.top - 6, "ε (%)", "label2", I["secondary"]))
        o.append(H.label(s, axr.x0 + 6, axr.top - 6, "σ (MPa)", "label2", I["secondary"]))
        # creep curve (stops at the top of the box when unbounded)
        cp, hc = [], []
        for t in tt:
            e = 0.0 if t < 0 else creep[key](t) * 100
            if e > 2.0:
                break
            cp.append((axc.X(t), axc.Y(e)))
            hc.append([axc.X(t), axc.Y(e), f"{nm}, t = {t:.3f} s: ε = {e:.3f} %"])
        i0 = next(i for i, (x, _) in enumerate(cp) if x >= axc.X(0))
        cp.insert(i0, (axc.X(0), axc.Y(0)))
        o.append(poly(s, cp, SER[0]))
        if key == "M":
            o.append(H.arrow(s, p, cp[-1][0] - 8, cp[-1][1] + 8 * 0.6, cp[-1][0] + 4, cp[-1][1] - 3, "force", w="curve"))
        # relaxation curve
        rp, hr = [], []
        for t in tt:
            sg = 0.0 if t < 0 else relax[key](t) / 1e6
            rp.append((axr.X(t), axr.Y(sg)))
            hr.append([axr.X(t), axr.Y(sg), f"{nm}, t = {t:.3f} s: σ = {sg:.2f} MPa"])
        i0 = next(i for i, (x, _) in enumerate(rp) if x >= axr.X(0))
        rp.insert(i0, (axr.X(0), axr.Y(0)))
        o.append(poly(s, rp, SER[1]))
        panels += [(axc.box, hc), (axr.box, hr)]
        # plateau references
        if key in ("K", "S"):
            o.append(H.line(s, axc.X(0), axc.Y(1.0), axc.x1, axc.Y(1.0), O["dim"], "ref", H.DASH_REF))
        if key == "S":
            o.append(H.line(s, axr.X(0), axr.Y(12), axr.x1, axr.Y(12), O["dim"], "ref", H.DASH_REF))
        # notes (ink)
        if key == "M":
            o.append(H.label(s, axc.X(0.17), axc.Y(1.45), "grows without bound", "label2", I["primary"]))
            o.append(H.label(s, axr.X(0.12), axr.Y(14), "decays to zero", "label2", I["primary"]))
            o.append(H.label(s, axr.X(0.12), axr.Y(14) + 16, f"{it('τ')} = {TS:.2f} s", "label2", I["secondary"]))
        elif key == "K":
            o.append(H.label(s, axc.X(0.16), axc.Y(0.45), f"no jump; bounded at {it('σ')}{H.sub('0', s, 'label2')}/{it('E')}"
                             f"{H.sub('K', s, 'label2')} = 1 %", "label2", I["primary"]))
            o.append(H.arrow(s, p, axr.X(0), axr.Y(13.5), axr.X(0), axr.top - 2, "force", w="curve"))
            o.append(H.label(s, axr.X(0.03), axr.top + 14, f"infinite at {it('t')} = 0", "label2", I["primary"]))
            o.append(H.label(s, axr.X(0.16), axr.Y(6), "then no relaxation:", "label2", I["primary"]))
            o.append(H.label(s, axr.X(0.16), axr.Y(6) + 16, f"{it('E')}{H.sub('K', s, 'label2')}{it('ε')}{H.sub('0', s, 'label2')}"
                             f" = 12 MPa", "label2", I["secondary"]))
        else:
            o.append(H.label(s, axc.X(0.16), axc.Y(0.4), f"jump to {s0 / EI * 100:.2f} %, creeps to 1 %", "label2",
                             I["primary"]))
            o.append(H.label(s, axr.X(0.13), axr.Y(17.5), f"jump to {EI * EPS0 / 1e6:.1f} MPa,", "label2", I["primary"]))
            o.append(H.label(s, axr.X(0.13), axr.Y(17.5) + 16, "relaxes to 12 MPa", "label2", I["primary"]))
    o.append(H.label(s, 12, 576, f"SLS: {it('E')}{H.sub('R', s, 'label2')} = 1.20 GPa, {it('E')}{H.sub('inst', s, 'label2')} = "
                     f"{EI / 1e9:.2f} GPa, {it('τ')}{H.sub('σ', s, 'label2')} = {TS:.2f} s, {it('τ')}{H.sub('ε', s, 'label2')} = "
                     f"{TE:.2f} s. Maxwell: {it('E')}{H.sub('M', s, 'label2')} = {it('E')}{H.sub('inst', s, 'label2')}, "
                     f"{it('τ')} = {it('τ')}{H.sub('σ', s, 'label2')}. Kelvin–Voigt: {it('E')}{H.sub('K', s, 'label2')} = "
                     f"{it('E')}{H.sub('R', s, 'label2')}, {it('τ')} = {it('τ')}{H.sub('ε', s, 'label2')}.", "label2", I["muted"]))
    o += plegend(s, 150, 552, [(SER[0], None, "strain ε(t) under held stress"), (SER[1], None, "stress σ(t) under held strain"),
                               (O["dim"], H.DASH_REF, "plateau")], gap=22)
    aria = ("Three-by-two grid of computed responses. Rows: Maxwell, Kelvin-Voigt, standard linear solid. Left column, creep "
            "under 12 megapascals held from t = 0: Maxwell jumps to 0.56 percent then grows linearly without bound; "
            "Kelvin-Voigt has no jump and creeps to 1 percent; the SLS jumps to 0.56 percent and creeps to 1 percent. "
            "Right column, relaxation under 1 percent strain held: Maxwell jumps to 21.6 megapascals and decays to zero; "
            "Kelvin-Voigt needs an infinite stress at t = 0 and then holds 12 megapascals; the SLS jumps to 21.6 and "
            "relaxes to 12. SLS constants: relaxed modulus 1.20 gigapascals, instantaneous 2.16, tau sigma 0.05 s, tau "
            "epsilon 0.09 s.")
    return finish(VB, aria, s, o, extra=H.hover_attr(panels))


# ================================================================ svg #22  Fig. 19: fascia shares a pull across a sheet
def fig22():
    VB = (0, 0, 760, 300)
    s = H.Scale(VB[2], VB[3])
    p = "m6f22_"
    o = [f'<defs>{H.markers(p, s)}{muscle_grad(p + "mg", 30, 0, 236, 0)}</defs>']
    sx0, sx1, sy0, sy1 = 230.0, 590.0, 46.0, 236.0
    o.append(rect(sx0, sy0, sx1 - sx0, sy1 - sy0, T["tendon"][0], T["tendon"][1], s(1.2), 4))
    o.append(fibre_field(s, sx0 + 2, sy0 + 2, sx1 - 2, sy1 - 2, (0, 35, -35, 70), 13, T["tendon"][1], 0.9, 0.85))
    # the muscle whose pull enters the sheet's left edge
    ym = 141.0
    mus = [(36, ym - 18), (90, ym - 36), (180, ym - 34), (234, ym - 22), (234, ym + 22), (180, ym + 34), (90, ym + 36),
           (36, ym + 18)]
    o.append(tissue(s, mus, fill=f"url(#{p}mg)"))
    for dy in (-24, -12, 0, 12, 24):
        o.append(fibre_line(s, 52, ym + dy * 0.75, 226, ym + dy, 0.75, 1.0))
    o.append(H.arrow(s, p, 226, 76, 120, 76, "force"))
    o.append(H.label(s, 120, 66, f"muscle pull {it('F')} on the sheet", "label2", I["primary"]))
    o.append(H.label(s, 70, ym + 60, "muscle", "label", I["primary"], "middle"))
    # lateral transmission to four attachments on the far edge; their reactions share F
    ys = [74.0, 122.0, 170.0, 218.0]
    Fl, n = 104.0, len(ys)
    for k, yy in enumerate(ys):
        o.append(H.line(s, sx0 + 4, ym, sx1 - 6, yy, O["force"], "ref", H.DASH_LOA))
        o.append(circ(sx1, yy, 4.2, "#fff", I["primary"], s(1.4)))
        o.append(H.arrow(s, p, sx1 + 6, yy, sx1 + 6 + Fl / n, yy, "force"))
        o.append(H.label(s, sx1 + 12 + Fl / n, yy + 5, f"{it('F')}{H.sub(str(k + 1), s)}", "label", O["force"]))
    for j, tx_ in enumerate(("attachments:", "neighbouring", "muscle, bone")):
        o.append(H.label(s, 652, 112 + 16 * j, tx_, "label2", I["secondary"]))
    o.append(H.label(s, 750, 256, f"{it('F')}{H.sub('1', s)} + {it('F')}{H.sub('2', s)} + {it('F')}{H.sub('3', s)} + "
                     f"{it('F')}{H.sub('4', s)} = {it('F')}", "label2", I["primary"], "end"))
    o.append(H.label(s, 410, 30, "fascial sheet: collagen laid in a plane, fibres at a spread of angles", "label2",
                     I["primary"], "middle"))
    o.append(H.label(s, 400, 256, "force spreads laterally across the sheet (dashed), not down one cord", "label2",
                     I["secondary"], "middle"))
    lg, _ = legend(s, 10, 292, [(sw_rect(T["muscle"][0], T["muscle"][1]), "muscle"),
                                (sw_rect(T["tendon"][0], T["tendon"][1]), "fascia (collagen sheet)"),
                                (sw_line(O["force"]), "force"), (sw_line(O["force"], 1.4, "4 3"), "load path")], gap=16)
    o.append(lg)
    aria = ("A fascial sheet: a planar collagen membrane with fibres laid in the plane at several angles. A muscle at the "
            "left pulls on the sheet's edge with force F. Dashed load paths fan out across the sheet to four attachments on "
            "the far edge, to neighbouring muscle and bone, whose reactions F 1 to F 4 share the load: F 1 + F 2 + F 3 + F 4 "
            "= F. Force spreads laterally across an area, not down one cord.")
    return finish(VB, aria, s, o)


# ================================================================ svg #30  Fig. 24: idealisations and where they are repaid
def fig30():
    VB = (0, 0, 760, 300)
    s = H.Scale(VB[2], VB[3])
    p = "m6f30_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    rows = [("tissue as a 1-D lumped spring (§2)", "Module 9: running and jumping (SLIP)",
             "whole-body leg spring, stance and flight, gait energetics"),
            ("fixed constants, small strain (§1, §6)", "Module 14: damage and adaptation",
             "creep-to-rupture, fatigue, ageing, training"),
            ("linear viscoelasticity at one operating point (§6)", "Module 16: continuum",
             "finite strain, relaxation spectrum, poroelastic coupling"),
            ("planar crossed-cruciate four-bar (§8)", "Module 16 and later joint chapters",
             "3-D laxity envelope, coupled rotations, contact")]
    lx, lw, rx, rw, top, pitch = 10, 330, 420, 330, 52, 58
    o.append(H.label(s, lx, 20, "The Module 6 passive-tissue model idealises …", "label", I["primary"]))
    o.append(H.label(s, rx, 20, "… repaid in", "label", I["primary"]))
    o.append(box(s, lx, 32, lw, pitch * len(rows) + 8))
    for i, (ideal, mod, what) in enumerate(rows):
        yc = top + 14 + i * pitch
        o.append(H.label(s, lx + 14, yc + 5, ideal, "label", I["primary"]))
        o.append(H.arrow(s, p, lx + lw + 6, yc, rx - 6, yc, "dim", w="ref"))
        o.append(box(s, rx, yc - 23, rw, 46))
        o.append(H.label(s, rx + 12, yc - 4, mod, "label", I["primary"]))
        o.append(H.label(s, rx + 12, yc + 14, what, "label2", I["secondary"]))
    aria = ("Roadmap of the Module 6 idealisations and where each is repaid: the tissue as a one-dimensional lumped spring "
            "(section 2) in Module 9, running and jumping SLIP dynamics; fixed constants and small strain (sections 1 and 6) "
            "in Module 14, creep-to-rupture, fatigue, ageing and training; linear viscoelasticity at one operating point "
            "(section 6) in Module 16, the continuum with finite strain and poroelastic coupling; the planar crossed-cruciate "
            "four-bar (section 8) in Module 16 and later joint chapters.")
    return finish(VB, aria, s, o)


# ================================================================ problem figures (400 px)
def fig32():                                              # C2: tendon, ligament, fascia architectures
    VB = (0, 0, 420, 196)
    s = H.Scale(VB[2], VB[3], display_w=400)
    p = "m6f32_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(H.arrow(s, p, 210, 22, 404, 22, "force"))
    o.append(H.arrow(s, p, 210, 22, 16, 22, "force"))
    o.append(H.label(s, 210, 14, "load axis", "label2", I["primary"], "middle"))
    specs = [("tendon", (0.0,), 7, "fibres in line", "with the load"),
             ("ligament", (-14.0, 0.0, 14.0), 11, "less aligned:", "several directions"),
             ("fascia", (0.0, 45.0, -45.0, 90.0), 12, "planar sheet,", "fibres at many angles")]
    for k, (name, angs, pitch, n1, n2) in enumerate(specs):
        x0 = 14 + k * 136
        o.append(rect(x0, 44, 120, 78, T["tendon"][0], T["tendon"][1], s(1.2), 4))
        o.append(fibre_field(s, x0 + 2, 46, x0 + 118, 120, angs, pitch, T["tendon"][1], 1.1, 0.9, seed=k + 3))
        o.append(H.label(s, x0 + 60, 144, name, "label", I["primary"], "middle"))
        o.append(H.label(s, x0 + 60, 162, n1, "label2", I["secondary"], "middle"))
        o.append(H.label(s, x0 + 60, 178, n2, "label2", I["secondary"], "middle"))
    aria = ("Problem C2 setup: three patches of the same collagen, seen in the plane of their fibres, under one horizontal "
            "load axis. Tendon: fibres all in line with the load. Ligament: fibres less aligned, spread over a few "
            "directions. Fascia: a planar sheet with fibres at many angles in the plane.")
    return finish(VB, aria, s, o)


def mtu_small(s, p, xb, ya, yt, wl, xe, kind="spring"):
    """Muscle (unipennate sheet from a femur end) + tendon (spring or rigid band) ending at xe. Returns (svg, xi, xs0)."""
    th = math.radians(TH_P)
    bone, (bx0, bx1, _, _) = femur_end(xb, (ya + yt) / 2, (yt - ya) + 22, y_cut=336.0)
    xb = bx1 - 3
    sheet, run = pennate_left(s, p, xb, ya, yt, wl, th, pitch=14)
    o = [bone, rect(xb - 2, ya - 5, wl + 4, 6, T["tendon"][0], T["tendon"][1], s(1.0), 3), sheet]
    xi = xb + run
    xs0 = xi + wl + 6
    o.append(rect(xi - 2, yt - 1, wl + 10, 6, T["tendon"][0], T["tendon"][1], s(1.0), 3))
    if kind == "spring":
        o.append(tissue_spring(s, xs0, xe, yt + 2, n=8, amp=8, w_out=5.0, w_in=2.8))
    else:
        o.append(rect(xs0 - 2, yt - 3, xe - xs0 + 2, 10, T["tendon"][0], T["tendon"][1], s(1.2), 4))
    return "".join(o), xb, xi, xs0


def fig35():                                              # C5: fibre slow, tendon fast
    VB = (0, 0, 420, 214)
    s = H.Scale(VB[2], VB[3], display_w=400)
    p = "m6f35_"
    ya, yt, xe = 40.0, 92.0, 330.0
    body, xb, xi, xs0 = mtu_small(s, p, 14, ya, yt, 46, xe)
    o = [f'<defs>{H.markers(p, s)}</defs>', body]
    o.append(H.label(s, xb + 10, 24, "fibre (CE)", "label2", I["primary"]))
    o.append(H.label(s, xs0 + 50, yt - 22, "tendon (SE)", "label2", I["primary"]))
    o.append(H.arrow(s, p, xe + 4, yt + 2, xe + 50, yt + 2, "force"))
    o.append(H.label(s, xe + 27, yt - 9, it("F"), "label", O["force"], "middle"))
    # shortening velocities drawn to the Lab 2 ratio: tendon recoil = 3.3 x the fibre's projected speed
    vf = 26.0
    vt = RATIO_LAB2 * vf
    y1, y2 = 140.0, 178.0
    o.append(H.line(s, xi, yt + 10, xi, y1 + 6, O["dim"], "leader", H.DASH_REF))
    o.append(H.arrow(s, p, xi, y1, xi - vf, y1, "geometry"))
    o.append(H.label(s, xi + 6, y1 + 5, f"fibre end: {dotted('ℓ', 0.36)} cos {it('θ')}{H.sub('p', s, 'label2')}, slow", "label2",
                     I["primary"]))
    o.append(H.line(s, xe, yt + 10, xe, y2 + 6, O["dim"], "leader", H.DASH_REF))
    o.append(H.arrow(s, p, xe, y2, xe - vf - vt, y2, "geometry"))
    o.append(H.label(s, xe - vf - vt - 6, y2 + 5, f"joint end: {dotted('L', 0.46)}{H.sub('MTU', s, 'label2')} = "
                     f"{dotted('ℓ', 0.36)} cos {it('θ')}{H.sub('p', s, 'label2')} + {it('ẋ')}", "label2", I["primary"], "end"))
    o.append(H.label(s, xe - vf - vt / 2, y2 + 24, f"fast: tendon recoil {it('ẋ')} ≈ {RATIO_LAB2:.1f} × fibre (Lab 2)",
                     "label2", I["secondary"], "middle"))
    aria = ("Problem C5 setup: a muscle-tendon unit from a femur end, a pennate muscle fibre (the contractile element) in "
            "series with a tendon spring, pulled by F. Shortening-speed arrows: the fibre end moves slowly, at l-dot cos "
            "theta p; the joint end moves at the sum, L-dot MTU = l-dot cos theta p + x-dot, with the tendon recoil x-dot "
            "drawn 3.3 times the fibre speed, the Lab 2 ratio.")
    return finish(VB, aria, s, o)


def fig36():                                              # C6: the stiff limit
    VB = (0, 0, 420, 222)
    s = H.Scale(VB[2], VB[3], display_w=400)
    p = "m6f36_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    xe = 312.0
    for k, (ya, kind) in enumerate(((30.0, "spring"), (160.0, "rigid"))):
        yt = ya + 46
        body, xb, xi, xs0 = mtu_small(s, p + str(k), 14, ya, yt, 40, xe, kind)
        o.append(body)
        o.append(H.arrow(s, p, xe + 4, yt + 2, xe + 48, yt + 2, "force"))
        o.append(H.label(s, xe + 26, yt - 9, it("F"), "label", O["force"], "middle"))
        if kind == "spring":
            xr = xi + (xe - xi) / 1.10
            o.append(H.line(s, xr, yt - 16, xr, yt + 14, O["dim"], "ref", H.DASH_REF))
            o.append(dim(s, p, xr, xe, yt + 22, f"{it('x')} = {it('F')}/{it('k')}{H.sub('T', s, 'label2')}", ty=yt + 38,
                         ext=(yt + 14, yt + 10)))
            o.append(H.label(s, xs0 + 4, ya - 4, f"compliant tendon, finite {it('k')}{H.sub('T', s, 'label2')}", "label2",
                             I["primary"]))
        else:
            o.append(H.label(s, xs0 + 4, ya - 4, f"rigid rod, {it('x')} = 0 (Module 5)", "label2", I["primary"]))
    o.append(H.arrow(s, p, 238, 116, 238, 140, "dim", w="ref"))
    o.append(H.label(s, 246, 133, f"{it('k')}{H.sub('T', s, 'label2')} → ∞", "label2", I["primary"]))
    aria = ("Problem C6 setup: top, a muscle-tendon unit whose tendon is a compliant spring of finite stiffness k T, "
            "stretched by x = F over k T past its rest end; bottom, the same unit with the tendon made a rigid rod, x = 0, "
            "Module 5's rigid tendon, reached as k T goes to infinity.")
    return finish(VB, aria, s, o)


def fig38():                                              # C8: the three networks
    VB = (0, 0, 420, 262)
    s = H.Scale(VB[2], VB[3], display_w=400)
    p = "m6f38_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    x0, x1 = 150.0, 404.0
    for yc, (net, labs), nm, sub in ((40.0, net_maxwell(s, x0, x1, 40.0), "Maxwell", "series"),
                                     (128.0, net_kv(s, x0, x1, 128.0, 22), "Kelvin–Voigt", "parallel"),
                                     (218.0, net_sls(s, x0, x1, 218.0, 22), "standard", "linear solid")):
        o.append(net)
        for lx, ly, t in labs:
            o.append(H.label(s, lx, ly, t, "label2", I["primary"], "middle"))
        o.append(H.label(s, 10, yc - 2, nm, "label", I["primary"]))
        o.append(H.label(s, 10, yc + 16, sub, "label2" if sub != "linear solid" else "label", I["secondary"] if sub !=
                         "linear solid" else I["primary"]))
    aria = ("Problem C8 setup: three spring-dashpot networks. Maxwell: a spring and a dashpot in series. Kelvin-Voigt: a "
            "spring and a dashpot in parallel. Standard linear solid: a spring E 0 in parallel with a spring E 1 in series "
            "with a dashpot.")
    return finish(VB, aria, s, o)


def fig45():                                              # D5: fibre and tendon springs in series
    VB = (0, 0, 420, 196)
    s = H.Scale(VB[2], VB[3], display_w=400)
    p = "m6f45_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    y = 70.0
    xw = 22.0
    kM, kT = 2.0, 1.0                            # drawn: tendon half as stiff as the fibre (any kT < kM shows the rule)
    LM, LT, xu = 110.0, 130.0, 22.0              # rest lengths and the fibre stretch drawn (px)
    xM, xT = xu, xu * kM / kT
    j, e = xw + LM + xM, xw + LM + xM + LT + xT
    o.append(wall(s, xw, y - 24, y + 24))
    o.append(tissue_spring(s, xw, j, y, "muscle", n=8, amp=10, w_out=5.0, w_in=2.8))
    o.append(tissue_spring(s, j, e, y, "tendon", n=8, amp=10, w_out=5.0, w_in=2.8))
    o.append(node(s, j, y, 3.8))
    o.append(H.arrow(s, p, e + 4, y, e + 48, y, "force"))
    o.append(H.label(s, e + 26, y - 10, it("F"), "label", O["force"], "middle"))
    o.append(H.label(s, (xw + j) / 2, y - 22, f"fibre {it('k')}{H.sub('M', s)}", "label", I["primary"], "middle"))
    o.append(H.label(s, (j + e) / 2, y - 22, f"tendon {it('k')}{H.sub('T', s)}", "label", I["primary"], "middle"))
    for xr in (xw + LM, xw + LM + xM + LT):
        o.append(H.line(s, xr, y - 14, xr, y + 34, O["dim"], "ref", H.DASH_REF))
    o.append(dim(s, p, xw + LM, j, y + 30, f"{it('F')}/{it('k')}{H.sub('M', s, 'label2')}", ty=y + 48,
                 ext=(None, y + 10)))
    o.append(dim(s, p, xw + LM + xM + LT, e, y + 30, f"{it('F')}/{it('k')}{H.sub('T', s, 'label2')}", ty=y + 48,
                 ext=(None, y + 10)))
    o.append(H.label(s, 210, 156, f"1/{it('k')} = 1/{it('k')}{H.sub('M', s)} + 1/{it('k')}{H.sub('T', s)}", "label",
                     I["primary"], "middle"))
    o.append(H.label(s, 210, 176, f"drawn with {it('k')}{H.sub('T', s, 'label2')} = {it('k')}{H.sub('M', s, 'label2')}/2: "
                     "dashed ticks mark the rest ends", "label2", I["secondary"], "middle"))
    aria = ("Problem D5 setup: a fibre spring k M and a tendon spring k T in series between a fixed wall and a force F. "
            "Dashed ticks mark each spring's rest end; the fibre stretches F over k M and the tendon F over k T, drawn with "
            "the tendon half as stiff, so it stretches twice as far. Series stiffness: 1 over k = 1 over k M + 1 over k T.")
    return finish(VB, aria, s, o)


FIGS = {
    4: ('Collagen hierarchy: a shaded tendon capsule draws out to a f', fig4),
    6: ('Five tropocollagen molecules drawn as staggered bars, each 4', fig6),
    7: ('Schematic of a tendon segment anchored to bone at the left w', fig7),
    10: ('Two spring lines from the origin reaching the same peak forc', fig10),
    11: ('Schematic of a muscle-tendon unit: a bone at the left, a sha', fig11),
    14: ('The two ideal elements. Top: a coil spring, the elastic elem', fig14),
    15: ('Three viscoelastic model networks. Maxwell: a spring and das', fig15),
    16: ('Free-body view of the two sharing rules. Left, series: two e', fig16),
    17: ('A three-by-two grid of responses. Rows are the Maxwell, Kelv', fig17),
    22: ('A fascial sheet: a planar collagen membrane. A single muscle', fig22),
    30: ('Roadmap: a central Module 6 box with arrows to Module 9 (run', fig30),
    32: ('tendon, ligament, fascia architectures', fig32),
    35: ('muscle-tendon unit with speed arrows', fig35),
    36: ('compliant tendon becomes rigid rod', fig36),
    38: ('Maxwell, Kelvin-Voigt, and SLS schematics', fig38),
    45: ('fibre and tendon springs in series', fig45),
}
