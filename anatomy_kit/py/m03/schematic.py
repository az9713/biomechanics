"""Module 3, group `schematic`: geometric schematics in the house style.

svg #5 (six freedoms of a rigid body, cabinet projection), #9 (constraint force normal to g(q) = 0) and #26 (the
nine idealizations and their repayments) are main-text figures (760 px); #41 (D4) and #42 (D5) are problem figures
(400 px). Geometry (tangents, normals, curvature, the Hertz dome) is computed here, not drawn by eye.
Anatomy in #26 comes from NIH BioArt (public domain): the femur of BioArt 244 (m00.tissue.femur_d) and the arm bones
of BioArt 208 (m05.body.Arm, the reposed arm the author approved for Module 5).
"""
import html
import math

import house as H
from m00.tissue import FEMUR_ART, femur_d
from m05.body import Arm, wrap

T, O, I = H.TISSUE, H.OVERLAY, H.INK
BOX = "#f7f4ef"
GRID = "#e6e6e6"
W = 400


def it(t):
    return f'<tspan font-style="italic">{t}</tspan>'


def sub(t, s, size="label"):
    return H.sub(t, s, size)


def sup(t, s, size="label"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def finish(vb, aria, s, body, extra=""):
    return H.svg_open(vb, html.escape(aria), s, extra) + "".join(body) + "</svg>"


def path(pts, col, w, s, extra=""):
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{s(H.PX[w]):.2f}" stroke-linejoin="round" {extra}/>'


def curved_arrow(s, p, pts, meaning, w="geom"):
    """A curved vector: path through pts with the slim house head at the last point."""
    return path(pts, O[meaning], w, s, f'stroke-linecap="round" marker-end="url(#{p}a_{meaning})"')


def poly(s, pts, col, w="curve"):
    return (f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{col}" '
            f'stroke-width="{s(H.PX[w]):.2f}" stroke-linejoin="round" stroke-linecap="round"/>')


def right_angle(s, P, t, n, size=11):
    a = (P[0] + t[0] * size, P[1] + t[1] * size)
    b = (a[0] + n[0] * size, a[1] + n[1] * size)
    c = (P[0] + n[0] * size, P[1] + n[1] * size)
    return path([a, b, c], I["secondary"], "leader", s)


def dotted(sym):
    """q-dot, q-double-dot, J-dot: Georgia has no combining dots (Chrome puts them beside the letter), so these
    glyphs use the serif fallback Times New Roman, whose combining marks attach (checked in a test render)."""
    return f'<tspan font-family="Times New Roman, Times, serif" font-style="italic">{sym}</tspan>'


QDOT, QDDOT, JDOT = dotted("q\u0307"), dotted("q\u0308"), dotted("J\u0307")


def Jc(s, size="label"):
    return f"{it('J')}{sub('c', s, size)}"


# ================================================================ svg #5: the six freedoms of a free rigid body
def fig5():
    VB = (0, 0, 760, 410)
    s = H.Scale(VB[2], VB[3])
    p = "m3f5_"
    C = (370.0, 222.0)
    c45 = 0.5 * math.cos(math.radians(45))            # cabinet projection: depth at 45 deg, half length

    def P(x, y, z):
        return (C[0] + x + c45 * z, C[1] - y - c45 * z)

    bx, by, bz = 75, 50, 60                           # half sizes of the box (user units)
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    # hidden edges at the back-bottom-left corner
    hc = P(-bx, -by, bz)
    for q in (P(bx, -by, bz), P(-bx, by, bz), P(-bx, -by, -bz)):
        o.append(H.line(s, hc[0], hc[1], q[0], q[1], I["rule"], "leader", (4, 3)))
    faces = [([(-bx, by, -bz), (bx, by, -bz), (bx, by, bz), (-bx, by, bz)], "#ffffff"),        # top
             ([(bx, -by, -bz), (bx, -by, bz), (bx, by, bz), (bx, by, -bz)], GRID),             # right
             ([(-bx, -by, -bz), (bx, -by, -bz), (bx, by, -bz), (-bx, by, -bz)], BOX)]           # front
    for pts, fill in faces:
        d = "M" + " L".join(f"{P(*q)[0]:.2f},{P(*q)[1]:.2f}" for q in pts) + " Z"
        o.append(f'<path d="{d}" fill="{fill}" stroke="{I["secondary"]}" stroke-width="{s(1.4):.2f}" stroke-linejoin="round"/>')
    o.append(H.label(s, P(bx, -by, -bz)[0] - 10, P(bx, -by, -bz)[1] - 10, "rigid body", "label2", I["muted"], "end"))

    # axis lines (dim, dashed), visible parts only: the box silhouette hides x in (-96, 96), y in (-71, 71), z in (-60, 201)
    def seg(a, b):
        return H.line(s, a[0], a[1], b[0], b[1], O["dim"], "leader", H.DASH_REF)
    o += [seg(P(-230, 0, 0), P(-97, 0, 0)), seg(P(97, 0, 0), P(246, 0, 0)),
          seg(P(0, -185, 0), P(0, -72, 0)), seg(P(0, 72, 0), P(0, 182, 0)),
          seg(P(0, 0, -470), P(0, 0, -62)), seg(P(0, 0, 202), P(0, 0, 430))]
    for (x, y, z), t in (((256, 0, 0), "x"), ((0, 192, 0), "y"), ((0, 0, 448), "z")):
        q = P(x, y, z)
        o.append(H.label(s, q[0], q[1] + 5, it(t), "label", I["primary"], "middle"))
    # translations: double-headed blue arrows on the negative half of each axis
    for a, b, lab, off in (((-110, 0, 0), (-215, 0, 0), "slide along x", (0, -12)),
                           ((0, -88, 0), (0, -172, 0), "slide along y", (12, 4)),
                           ((0, 0, -250), (0, 0, -450), "slide along z", (-14, 4))):
        A, B = P(*a), P(*b)
        o.append(H.arrow(s, p, A[0], A[1], B[0], B[1], "geometry", both=True))
        m = ((A[0] + B[0]) / 2 + off[0], (A[1] + B[1]) / 2 + off[1])
        anc = "middle" if off[0] == 0 else ("start" if off[0] > 0 else "end")
        o.append(H.label(s, m[0], m[1], lab, "label2", I["primary"], anc))

    # rotations: blue arcs (curved = rotation) around the positive half of each axis (right-hand sense)
    def arc(fn, r, t0=25, t1=325, n=60):
        return [P(*fn(r, math.radians(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]
    r = 30
    arcs = [(lambda r, t: (178, r * math.cos(t), r * math.sin(t)), "α, about x", (178, -r - 18, 0), "middle"),
            (lambda r, t: (r * math.sin(t), 140, r * math.cos(t)), "β, about y", (-r - 12, 140, 0), "end"),
            (lambda r, t: (r * math.cos(t), r * math.sin(t), 340), "γ, about z", (r + 12, 0, 340), "start")]
    for fn, lab, at, anc in arcs:
        o.append(curved_arrow(s, p, arc(fn, r), "geometry", "geom"))
        q = P(*at)
        o.append(H.label(s, q[0], q[1] + 5, lab, "label2", I["primary"], anc))
    # key, top left
    kx, ky = 24, 34
    o.append(H.arrow(s, p, kx, ky - 5, kx + 34, ky - 5, "geometry", both=True))
    o.append(H.label(s, kx + 44, ky, "straight: 3 translations (x, y, z)", "label2", I["primary"]))
    o.append(curved_arrow(s, p, [(kx + 17 + 14 * math.cos(math.radians(a)), ky + 22 + 7 * math.sin(math.radians(a)))
                                 for a in range(200, 521, 16)], "geometry", "geom"))
    o.append(H.label(s, kx + 44, ky + 26, "curved: 3 rotations (α, β, γ)", "label2", I["primary"]))
    o.append(H.label(s, kx, ky + 54, "3 + 3 = 6 degrees of freedom", "label", I["primary"]))
    o.append(H.label(s, kx, ky + 74, f"in the {it('x')}–{it('y')} plane only {it('x')}, {it('y')} and γ remain: 3",
                     "label2", I["secondary"]))
    aria = ("A rigid box drawn in cabinet projection, with three dashed axes x, y and z through its centre. On the negative "
            "half of each axis a blue double-headed arrow shows a translation: slide along x, along y, along z. Around the "
            "positive half of each axis a blue curved arrow shows a rotation: alpha about x, beta about y, gamma about z. "
            "Three translations plus three rotations make six degrees of freedom; in the x-y plane only x, y and gamma "
            "remain, three.")
    return finish(VB, aria, s, o)


# ================================================================ svg #9: the constraint force is normal to g(q) = 0
def surface9(x):
    """The drawn constraint surface y = f(x) in user units, and its slope."""
    return 222 - 62 * math.sin((x - 70) / 108), -62 / 108 * math.cos((x - 70) / 108)


def fig9():
    VB = (0, 0, 760, 340)
    s = H.Scale(VB[2], VB[3])
    p = "m3f9_"
    xs = [40 + i * 4 for i in range(171)]
    curve = [(x, surface9(x)[0]) for x in xs]
    px = 330.0
    py, m = surface9(px)
    L = math.hypot(1, m)
    t = (1 / L, m / L)                                # unit tangent (to the right)
    n = (m / L, -1 / L)                               # unit normal, pointing up off the surface
    assert abs(t[0] * n[0] + t[1] * n[1]) < 1e-12
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o.append(poly(s, curve, I["secondary"], "curve"))
    o.append(H.label(s, 520, surface9(520)[0] + 30, f"constraint surface {it('g')}({it('q')}) = 0", "label", I["primary"]))
    o.append(H.label(s, 520, surface9(520)[0] + 48, "(the allowed configurations)", "label2", I["secondary"]))
    # the normal line through P: the direction of the gradient, grad g = Jc transposed
    a, b = (px - n[0] * 70, py - n[1] * 70), (px + n[0] * 150, py + n[1] * 150)
    o.append(H.line(s, a[0], a[1], b[0], b[1], O["dim"], "leader", H.DASH_REF))
    # allowed velocity (tangent) and the constraint force (normal)
    v = (px + t[0] * 150, py + t[1] * 150)
    o.append(H.arrow(s, p, px, py, v[0], v[1], "geometry"))
    f = (px + n[0] * 118, py + n[1] * 118)
    o.append(H.arrow(s, p, px, py, f[0], f[1], "reaction", w="force"))
    o.append(right_angle(s, (px, py), t, n))
    o.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{s(4.5):.2f}" fill="{I["primary"]}" stroke="#fff" stroke-width="{s(1.2):.2f}"/>')
    o.append(H.label(s, px - 12, py + 16, it("P"), "label", I["primary"], "end"))
    o.append(H.label(s, f[0] + 12, f[1] + 4, f"constraint force {Jc(s)}{sup('T', s)}λ", "label", I["primary"]))
    o.append(H.label(s, f[0] + 12, f[1] + 22, f"normal to the surface, along ∇{it('g')}", "label2", I["secondary"]))
    tx, ty = v[0] + 14, v[1] - 44
    o.append(H.label(s, tx, ty, f"allowed velocity {QDOT}: tangent, {Jc(s, 'label2')}{QDOT} = 0", "label2", I["primary"]))
    o.append(H.label(s, tx, ty + 17, f"any virtual displacement δ{it('q')} is tangent too,", "label2", I["secondary"]))
    o.append(H.label(s, tx, ty + 34, f"so the force does no virtual work: ({Jc(s, 'label2')}{sup('T', s, 'label2')}λ) · δ{it('q')} = 0",
                     "label2", I["secondary"]))
    # configuration-space axes
    ox, oy = 36, 322
    o.append(H.arrow(s, p, ox, oy, ox + 44, oy, "dim"))
    o.append(H.arrow(s, p, ox, oy, ox, oy - 44, "dim"))
    o.append(H.label(s, ox + 50, oy + 5, f"{it('q')}{sub('1', s, 'label2')}", "label2", I["secondary"]))
    o.append(H.label(s, ox - 4, oy - 50, f"{it('q')}{sub('2', s, 'label2')}", "label2", I["secondary"]))
    o.append(H.label(s, ox + 14, oy - 14, "configuration space", "label2", I["muted"]))
    aria = ("A curved constraint surface g(q) = 0 in configuration space, with a point P on it. A blue arrow from P along "
            "the tangent is the allowed velocity q-dot, with Jc q-dot = 0; any virtual displacement delta q is tangent too. "
            "A black arrow from P perpendicular to the surface, along the dashed normal line, the direction of the gradient "
            "of g, is the constraint force Jc transposed lambda. A right-angle mark at P: the force does no virtual work on "
            "any allowed motion.")
    return finish(VB, aria, s, o)


# ================================================================ svg #41 (D4): differentiate the constraint twice
def fig41():
    VB = (0, 0, W, 214)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m3f41_"
    Cx, Cy, R = 200.0, 520.0, 420.0                   # the surface is a circular arc: its centre of curvature is known
    arc = [(Cx + R * math.cos(math.radians(a)), Cy + R * math.sin(math.radians(a))) for a in range(-118, -61)]
    th = math.radians(-100.0)
    P = (Cx + R * math.cos(th), Cy + R * math.sin(th))
    t = (-math.sin(th), math.cos(th))                 # tangent, direction of increasing angle (to the right)
    n_in = (-math.cos(th), -math.sin(th))             # inward normal, toward the centre of curvature
    v_len, a_t, a_n = 100.0, 38.0, 58.0
    V = (P[0] + t[0] * v_len, P[1] + t[1] * v_len)
    At = (P[0] + t[0] * a_t, P[1] + t[1] * a_t)
    A = (At[0] + n_in[0] * a_n, At[1] + n_in[1] * a_n)
    An = (P[0] + n_in[0] * a_n, P[1] + n_in[1] * a_n)
    o = [f"<defs>{H.markers(p, s)}</defs>", poly(s, arc, I["secondary"], "curve")]
    o.append(H.label(s, 388, arc[-1][1] + 16 if arc[-1][1] < 200 else 200, f"{it('g')}({it('q')}) = 0", "label", I["primary"], "end"))
    # components of the acceleration (thin dashed) and the acceleration itself
    o.append(H.line(s, At[0], At[1], A[0], A[1], O["flag"], "leader", (4, 3)))
    o.append(H.line(s, An[0], An[1], A[0], A[1], O["flag"], "leader", (4, 3)))
    o.append(H.arrow(s, p, P[0], P[1], An[0], An[1], "flag", w="geom"))
    o.append(H.arrow(s, p, P[0], P[1], A[0], A[1], "flag", w="force"))
    o.append(H.arrow(s, p, P[0], P[1], V[0], V[1], "geometry"))
    o.append(right_angle(s, P, t, n_in, 9))
    o.append(f'<circle cx="{P[0]:.2f}" cy="{P[1]:.2f}" r="{s(4.5):.2f}" fill="{I["primary"]}" stroke="#fff" stroke-width="{s(1.2):.2f}"/>')
    o.append(H.label(s, V[0] + 6, V[1] - 10, f"{QDOT}: {Jc(s, 'label2')}{QDOT} = 0 (tangent)", "label2", I["primary"]))
    o.append(H.label(s, A[0] + 8, A[1] + 6, QDDOT, "label", I["primary"]))
    o.append(H.label(s, An[0] - 8, An[1] + 4, "normal part:", "label2", I["primary"], "end"))
    o.append(H.label(s, An[0] - 8, An[1] + 20, f"{Jc(s, 'label2')}{QDDOT} = −{JDOT}{sub('c', s, 'label2')}{QDOT}",
                     "label2", I["primary"], "end"))
    o.append(H.label(s, An[0] - 8, An[1] + 36, "(centripetal, inward)", "label2", I["secondary"], "end"))
    o.append(H.label(s, 12, 22, f"once: {Jc(s, 'label2')}{QDOT} = 0;  twice: {Jc(s, 'label2')}{QDDOT} + "
                     f"{JDOT}{sub('c', s, 'label2')}{QDOT} = 0", "label2", I["primary"]))
    o.append(H.label(s, 12, 40, f"the tangential part of {QDDOT} is free", "label2", I["secondary"]))
    aria = ("Problem D4 figure: a point on a curved constraint surface g(q) = 0. Its velocity q-dot, blue, is tangent to the "
            "surface: Jc q-dot = 0. Its acceleration q-double-dot, orange, can turn: its tangential part is free, while its "
            "normal part points inward, toward the centre of curvature, and is fixed by the curve: Jc q-double-dot = minus "
            "Jc-dot q-dot, the centripetal term.")
    return finish(VB, aria, s, o)


# ================================================================ svg #42 (D5): the KKT system and the elimination
def fig42():
    VB = (0, 0, W, 252)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m3f42_"
    Jt = f"{Jc(s)}{sup('T', s)}"
    bw, bh, y0 = 50, 34, 30
    x0 = 24
    o = [f"<defs>{H.markers(p, s)}</defs>"]

    def block(x, y, w, txt, edge=I["rule"], fill=BOX, dash=False):
        da = f' stroke-dasharray="{s(3):.2f} {s(2):.2f}"' if dash else ""
        return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{bh}" rx="4" fill="{fill}" stroke="{edge}" '
                f'stroke-width="{s(1.2):.2f}"{da}/>' + H.label(s, x + w / 2, y + bh / 2 + 5.5, txt, "label", I["primary"], "middle"))

    def brackets(xa, xb):
        ya, yb = y0 - 4, y0 + 2 * bh + 6
        return (path([(xa + 6, ya), (xa, ya), (xa, yb), (xa + 6, yb)], I["axis"], "axis", s)
                + path([(xb - 6, ya), (xb, ya), (xb, yb), (xb - 6, yb)], I["axis"], "axis", s))
    # [M Jc^T; Jc 0]
    o.append(brackets(x0 - 6, x0 + 2 * bw + 8))
    o.append(block(x0, y0, bw, it("M")))
    o.append(block(x0 + bw + 2, y0, bw, Jt, O["geometry"]))
    o.append(block(x0, y0 + bh + 2, bw, Jc(s), O["geometry"]))
    o.append(block(x0 + bw + 2, y0 + bh + 2, bw, "0", I["rule"], "#ffffff", dash=True))
    # [q'' ; -lambda]
    xv = x0 + 2 * bw + 22
    o.append(brackets(xv - 6, xv + 44 + 6))
    o.append(block(xv, y0, 44, QDDOT))
    o.append(block(xv, y0 + bh + 2, 44, "−λ", O["reaction"]))
    o.append(H.label(s, xv + 66, y0 + bh + 7, "=", "label", I["primary"], "middle"))
    # [Q - c ; -Jdot q']
    xr = xv + 88
    o.append(brackets(xr - 6, xr + 80 + 6))
    o.append(block(xr, y0, 80, f"{it('Q')} − {it('c')}"))
    o.append(block(xr, y0 + bh + 2, 80, f"−{JDOT}{sub('c', s)}{QDOT}"))
    # row sizes
    o.append(H.label(s, xr + 96, y0 + bh / 2 + 5, f"{it('n')} rows:", "label2", I["secondary"]))
    o.append(H.label(s, xr + 96, y0 + bh / 2 + 21, "dynamics", "label2", I["secondary"]))
    o.append(H.label(s, xr + 96, y0 + bh * 1.5 + 7, f"{it('m')} rows:", "label2", I["secondary"]))
    o.append(H.label(s, xr + 96, y0 + bh * 1.5 + 23, "constraints", "label2", I["secondary"]))
    # the elimination, step by step
    ys = y0 + 2 * bh + 34
    steps = [("1", f"top row:  {QDDOT} = {it('M')}{sup('−1', s, 'label2')}({it('Q')} − {it('c')} + {Jc(s, 'label2')}{sup('T', s, 'label2')}λ)"),
             ("2", f"into the bottom row {Jc(s, 'label2')}{QDDOT} = −{JDOT}{sub('c', s, 'label2')}{QDOT}:"),
             ("", f"({Jc(s, 'label2')}{it('M')}{sup('−1', s, 'label2')}{Jc(s, 'label2')}{sup('T', s, 'label2')}) λ = "
                  f"−{Jc(s, 'label2')}{it('M')}{sup('−1', s, 'label2')}({it('Q')} − {it('c')}) − {JDOT}{sub('c', s, 'label2')}{QDOT}"),
             ("3", f"{Jc(s, 'label2')}{it('M')}{sup('−1', s, 'label2')}{Jc(s, 'label2')}{sup('T', s, 'label2')} is positive-definite "
                   f"when {Jc(s, 'label2')} has full row rank,"),
             ("", "so it inverts: λ in closed form, Proposition 3.2")]
    for i, (k, txt) in enumerate(steps):
        y = ys + i * 21
        if k:
            o.append(H.label(s, x0 - 6, y, f"{k}.", "label2", I["primary"], "end"))
        o.append(H.label(s, x0, y, txt, "label2", I["primary"]))
    aria = ("Problem D5 figure: the saddle-point KKT system as blocks. The matrix has M and Jc transposed in its top row "
            "and Jc and a zero block in its bottom row; it multiplies the vector of accelerations q-double-dot and minus "
            "lambda, and equals the vector Q minus c over minus Jc-dot q-dot. The top row holds n dynamical equations, the "
            "bottom row m constraint equations. Below, the elimination: 1, solve the top row for q-double-dot = M inverse "
            "times (Q minus c plus Jc transposed lambda); 2, put it into the bottom row to get (Jc M inverse Jc transposed) "
            "lambda = minus Jc M inverse (Q minus c) minus Jc-dot q-dot; 3, that matrix is positive-definite when Jc has full "
            "row rank, so it inverts and gives lambda in closed form, Proposition 3.2.")
    return finish(VB, aria, s, o)


# ================================================================ svg #26: the nine loans and their repayments
WINTER_THIGH_COM = 0.433            # Winter (2009): thigh centre of mass, fraction of segment length from the hip


def femur_use(s, p, x, y, h):
    """The NIH femur (head up), height h, top-left at (x, y); drawn once in <defs> and placed with <use>."""
    k = h / (FEMUR_ART[3] - FEMUR_ART[1])
    return (f'<use href="#{p}femur" transform="translate({x - FEMUR_ART[0] * k:.2f} {y - FEMUR_ART[1] * k:.2f}) '
            f'scale({k:.4f})"/>'), k


def fig26():
    VB = (0, 0, 760, 600)
    s = H.Scale(VB[2], VB[3])
    p = "m3f26_"
    cw, ch, top = 760 / 3, 178, 6
    grey = I["rule"]
    femur = (f'<g id="{p}femur"><path d="{femur_d()}" fill="{T["bone"][0]}" stroke="{T["bone"][1]}" '
             f'stroke-width="5" stroke-linejoin="round"/></g>')
    o = [f"<defs>{H.markers(p, s)}{femur}</defs>"]
    for c in (1, 2):
        o.append(H.line(s, c * cw, top, c * cw, top + 3 * ch, GRID, "leader"))
    for r in (1, 2):
        o.append(H.line(s, 6, top + r * ch, 754, top + r * ch, GRID, "leader"))
    cells = [("bone flexes", "Module 2"), ("tendon = spring", "Module 6"), ("contact pushes only (λ ≥ 0)", "Modules 4, 8"),
             ("friction μ ≈ 0.005", "Module 4"), ("axis migrates", "Module 6"), ("pressure field", "Module 4"),
             ("distributed mass", "Module 8"), ("muscle adds Q", "Modules 5, 7"), ("3-D joints", "Module 11")]
    for k, (name, mod) in enumerate(cells):
        cx, cy = (k % 3 + 0.5) * cw, top + (k // 3) * ch
        o.append(H.arrow(s, p, cx - 22, cy + 66, cx + 14, cy + 66, "dim", w="ref"))
        o.append(H.label(s, cx, cy + 146, name, "label", I["primary"], "middle"))
        o.append(H.label(s, cx, cy + 163, f"repaid in {mod}", "label2", I["muted"], "middle"))

    def cell(k):
        return (k % 3 + 0.5) * cw, top + (k // 3) * ch
    L, R = -72, 72                                     # idealization / real x offsets from the cell centre

    # 1. rigid bar -> femur that bends (dashed deflected centreline, end moments)
    cx, cy = cell(0)
    o.append(H.line(s, cx + L, cy + 18, cx + L, cy + 118, grey, "force"))
    fu, k = femur_use(s, p, cx + R - 18, cy + 14, 108)
    o.append(fu)
    fx0, fx1 = cx + R - 18, cx + R - 18 + (FEMUR_ART[2] - FEMUR_ART[0]) * k
    xm = (fx0 + fx1) / 2
    bend = [(xm + 9 * math.sin(math.pi * i / 20) - 2, cy + 24 + 88 * i / 20) for i in range(21)]
    o.append(path(bend, O["geometry"], "geom", s, f'stroke-dasharray="{s(4):.2f} {s(3):.2f}"'))
    for yy, sg in ((cy + 20, 1), (cy + 114, -1)):
        pts = [(xm + 20 * math.cos(math.radians(a)), yy + sg * 9 * math.sin(math.radians(a))) for a in range(200, 341, 10)]
        o.append(curved_arrow(s, p, pts if sg > 0 else pts[::-1], "force", "force"))
    o.append(H.label(s, xm + 26, cy + 18, it("M"), "label2", I["primary"]))
    o.append(H.label(s, xm + 22, cy + 70, f"σ = {it('My')}/{it('I')}", "label2", I["primary"]))

    # 2. rigid link -> tendon as a spring
    cx, cy = cell(1)
    o.append(H.line(s, cx + L, cy + 18, cx + L, cy + 118, grey, "force"))
    zx, zy0, zy1, n = cx + R, cy + 30, cy + 106, 8
    zz = [(zx, cy + 18), (zx, zy0)] + [(zx + (9 if i % 2 else -9), zy0 + (i + 0.5) * (zy1 - zy0) / n) for i in range(n)] + \
         [(zx, zy1), (zx, cy + 118)]
    o.append(path(zz, T["tendon"][1], "force", s))
    o.append(H.arrow(s, p, zx, cy + 120, zx, cy + 134, "force"))
    o.append(H.label(s, zx - 8, cy + 132, it("F"), "label2", I["primary"], "end"))
    o.append(H.label(s, zx + 16, cy + 62, "stores and", "label2", I["secondary"]))
    o.append(H.label(s, zx + 16, cy + 78, "returns energy", "label2", I["secondary"]))

    # 3. two-sided constraint -> contact that can only push (lift-off allowed)
    cx, cy = cell(2)
    o.append(H.line(s, cx + L - 30, cy + 104, cx + L + 30, cy + 104, grey, "axis"))
    o.append(f'<rect x="{cx + L - 15:.2f}" y="{cy + 84}" width="30" height="20" fill="{grey}" opacity="0.5"/>')
    o.append(H.arrow(s, p, cx + L, cy + 76, cx + L, cy + 30, "dim", w="ref"))
    o.append(H.arrow(s, p, cx + L, cy + 112, cx + L, cy + 128, "dim", w="ref"))
    o.append(H.label(s, cx + L + 6, cy + 26, "pull or push", "label2", I["muted"], "start"))
    o.append(H.line(s, cx + R - 34, cy + 104, cx + R + 34, cy + 104, I["axis"], "axis"))
    o.append(f'<rect x="{cx + R - 15:.2f}" y="{cy + 58}" width="30" height="20" fill="{BOX}" stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
    o.append(f'<rect x="{cx + R - 15:.2f}" y="{cy + 84}" width="30" height="20" fill="none" stroke="{grey}" '
             f'stroke-width="{s(1):.2f}" stroke-dasharray="{s(3):.2f} {s(2):.2f}"/>')
    o.append(H.arrow(s, p, cx + R, cy + 103, cx + R, cy + 82, "reaction", w="force"))
    o.append(H.label(s, cx + R - 20, cy + 100, "λ ≥ 0", "label2", I["primary"], "end"))
    o.append(H.label(s, cx + R, cy + 50, "lifts off", "label2", I["secondary"], "middle"))

    # 4. frictionless -> friction (block on a surface sliding right)
    cx, cy = cell(3)
    for xc, real in ((cx + L, False), (cx + R, True)):
        o.append(H.line(s, xc - 36, cy + 98, xc + 36, cy + 98, I["axis"] if real else grey, "axis"))
        o.append(f'<rect x="{xc - 18:.2f}" y="{cy + 72}" width="36" height="26" fill="{BOX if real else grey}" '
                 f'{"" if real else "opacity=\"0.5\""} stroke="{I["secondary"] if real else "none"}" stroke-width="{s(1.2):.2f}"/>')
        o.append(H.arrow(s, p, xc, cy + 98, xc, cy + 40, "reaction" if real else "dim", w="force" if real else "ref"))
        o.append(H.label(s, xc + 6, cy + 46, it("N"), "label2", I["primary"]))
    o.append(H.arrow(s, p, cx + R - 20, cy + 104, cx + R - 50, cy + 104, "reaction"))
    o.append(H.label(s, cx + R - 26, cy + 122, f"μ{it('N')}", "label2", I["primary"], "end"))
    o.append(H.arrow(s, p, cx + R + 22, cy + 84, cx + R + 44, cy + 84, "geometry"))
    o.append(H.label(s, cx + R + 22, cy + 76, "slides", "label2", I["secondary"]))
    o.append(H.label(s, cx + L, cy + 116, "no tangential", "label2", I["muted"], "middle"))
    o.append(H.label(s, cx + L, cy + 131, "force", "label2", I["muted"], "middle"))

    # 5. fixed pin -> a rolling profile (schematic, not anatomy) whose instantaneous axis migrates
    cx, cy = cell(4)
    o.append(H.line(s, cx + L, cy + 30, cx + L, cy + 76, grey, "force"))
    o.append(f'<circle cx="{cx + L:.2f}" cy="{cy + 82}" r="{s(6):.2f}" fill="#fff" stroke="{grey}" stroke-width="{s(2):.2f}"/>')
    o.append(H.label(s, cx + L, cy + 112, "one fixed axis", "label2", I["muted"], "middle"))
    ex, ey = cx + R, cy + 72
    o.append(f'<ellipse cx="{ex:.2f}" cy="{ey:.2f}" rx="30" ry="22" fill="{BOX}" stroke="{I["secondary"]}" '
             f'stroke-width="{s(1.2):.2f}" transform="rotate(-18 {ex:.2f} {ey:.2f})"/>')
    o.append(H.line(s, ex - 46, cy + 96, ex + 46, cy + 96, I["axis"], "axis"))
    ic = [(ex - 22, cy + 96), (ex - 2, cy + 90), (ex + 20, cy + 94)]
    o.append(path(ic, O["geometry"], "leader", s, f'stroke-dasharray="{s(3):.2f} {s(2):.2f}"'))
    for q in ic:
        o.append(f'<circle cx="{q[0]:.2f}" cy="{q[1]:.2f}" r="{s(3):.2f}" fill="{O["geometry"]}"/>')
    o.append(curved_arrow(s, p, [(ex + 34 * math.cos(math.radians(a)), ey + 34 * math.sin(math.radians(a)))
                                 for a in range(-150, -59, 10)], "geometry"))
    o.append(H.label(s, ex, cy + 116, "rolls and glides", "label2", I["secondary"], "middle"))

    # 6. point load -> Hertz pressure field p(r) = p0 sqrt(1 - (r/a)^2) (arrow length proportional to p)
    cx, cy = cell(5)
    o.append(H.line(s, cx + L - 30, cy + 100, cx + L + 30, cy + 100, grey, "axis"))
    o.append(H.arrow(s, p, cx + L, cy + 36, cx + L, cy + 98, "dim", w="force"))
    a_px, p0_px = 34.0, 50.0
    o.append(H.line(s, cx + R - 44, cy + 100, cx + R + 44, cy + 100, I["axis"], "axis"))
    dome = [(cx + R + r, cy + 100 - 6 - p0_px * math.sqrt(max(0.0, 1 - (r / a_px) ** 2))) for r in
            [a_px * (i / 20 - 1) * 1.0 for i in range(41)]]
    o.append(path(dome, O["force"], "leader", s))
    for i in range(-3, 4):
        r = a_px * i / 3.6
        hgt = p0_px * math.sqrt(1 - (r / a_px) ** 2)
        o.append(H.arrow(s, p, cx + R + r, cy + 94 - hgt, cx + R + r, cy + 98, "force", w="leader"))
    o.append(H.label(s, cx + R + 26, cy + 38, f"{it('p')}({it('r')})", "label2", I["primary"]))

    # 7. point mass -> distributed mass: the thigh segment, centre of mass between the joints (Winter: 0.433 from the hip)
    cx, cy = cell(6)
    o.append(H.line(s, cx + L, cy + 26, cx + L, cy + 110, grey, "ref"))
    o.append(f'<circle cx="{cx + L:.2f}" cy="{cy + 110}" r="{s(7):.2f}" fill="{grey}"/>')
    o.append(H.label(s, cx + L + 12, cy + 114, it("m"), "label2", I["primary"]))
    fu, k = femur_use(s, p, cx + R - 30, cy + 14, 108)
    o.append(fu)
    hip = (cx + R - 30 + (52.0 - FEMUR_ART[0]) * k, cy + 14 + (60.0 - FEMUR_ART[1]) * k)
    knee = (cx + R - 30 + (33.0 - FEMUR_ART[0]) * k, cy + 14 + (360.0 - FEMUR_ART[1]) * k)
    com = (hip[0] + WINTER_THIGH_COM * (knee[0] - hip[0]), hip[1] + WINTER_THIGH_COM * (knee[1] - hip[1]))
    o.append(H.joint_centre(s, *hip))
    o.append(H.joint_centre(s, *knee))
    o.append(H.com_mark(s, *com))
    o.append(H.label(s, com[0] + 14, com[1] + 4, "COM", "label2", I["primary"]))
    o.append(H.label(s, com[0] + 14, com[1] + 20, f"{it('m')}, {it('I')}", "label2", I["secondary"]))

    # 8. bare bone -> muscle adds the applied force Q (the m05 reposed NIH arm with biceps)
    cx, cy = cell(7)
    K = 2.7                                            # px per cm
    for xo, musc in ((L - 18, False), (R - 30, True)):
        E = (cx + xo, cy + 102)
        arm = Arm(p + ("b" if musc else "a"), s, E, K)
        body = arm.bones(hand=False)
        if musc:
            bi, _, _ = arm.biceps()
            body += bi
        o.append(body if musc else f'<g opacity="0.55">{body}</g>')
        if musc:
            ux, uy = arm.B[0] - arm.I[0], arm.B[1] - arm.I[1]
            Lr = math.hypot(ux, uy)
            o.append(H.arrow(s, p, arm.I[0], arm.I[1], arm.I[0] + ux / Lr * 34, arm.I[1] + uy / Lr * 34, "force"))
            o.append(H.label(s, E[0] + 30, cy + 124, f"muscle force → {it('Q')}", "label2", I["primary"], "middle"))

    # 9. planar axes -> spatial axes
    cx, cy = cell(8)
    ox, oy = cx + L - 16, cy + 96
    o.append(H.arrow(s, p, ox, oy, ox + 44, oy, "dim", w="ref"))
    o.append(H.arrow(s, p, ox, oy, ox, oy - 54, "dim", w="ref"))
    ox, oy = cx + R - 10, cy + 90
    for dx, dy, tx in ((42, 0, "x"), (0, -54, "y"), (-26, 26, "z")):
        o.append(H.arrow(s, p, ox, oy, ox + dx, oy + dy, "geometry"))
        o.append(H.label(s, ox + dx * 1.22 + (4 if dx >= 0 else -4), oy + dy * 1.12 + 5, it(tx), "label2", I["primary"],
                         "middle"))
    o.append(H.label(s, cx + R + 6, cy + 24, f"spatial {Jc(s, 'label2')}", "label2", I["secondary"], "middle"))

    c1 = H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt (Ryan Kissinger)", title="Human Upper Leg Bones (BioArt 244)",
                                    changes="Femur only; recoloured.")
    c2 = H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt 208", title="Human Arm Bones",
                                    changes="Recoloured; reposed. Muscle and overlays drawn for this course.")
    o.append(H.credit(s, 10, top + 3 * ch + 14, wrap(c1, 120) + wrap(c2, 120)))
    aria = ("A 3-by-3 grid of the nine idealizations of Module 3 and the later module that repays each. In every cell a grey "
            "idealization on the left turns, via an arrow, into the real behaviour on the right, drawn in tissue colours. "
            "1: a rigid bar becomes a femur that bends under end moments, sigma = My/I (Module 2). 2: a rigid link becomes "
            "a tendon spring that stores and returns energy (Module 6). 3: a two-sided constraint that can pull or push "
            "becomes a contact that only pushes, lambda at least zero, and can lift off (Modules 4 and 8). 4: a "
            "frictionless block gains a friction force mu N opposing the slide, mu about 0.005 (Module 4). 5: a fixed pin "
            "becomes a profile that rolls and glides, its instantaneous axis migrating (Module 6). 6: a point load becomes "
            "a Hertz pressure field (Module 4). 7: a point mass becomes a thigh segment with its centre of mass between hip "
            "and knee and a moment of inertia (Module 8). 8: a bare arm gains a muscle whose force supplies the applied "
            "force Q (Modules 5 and 7). 9: planar axes become spatial x, y, z axes (Module 11).")
    return finish(VB, aria, s, o)


FIGS = {
    5: ("A shaded three-dimensional box in cabinet projection with th", fig5),
    9: ("A curved constraint surface with a point on it; the allowed ", fig9),
    26: ("A 3-by-3 grid of before-and-after sketches. In each cell a g", fig26),
    41: ("A point confined to a curved constraint surface; its velocit", fig41),
    42: ("The 2-by-2 block KKT matrix with M and Jc transpose on the t", fig42),
}
