"""Module 10 whole-body figures (main text). Exposes the Lynch body kit once per page.

svg #2 (Fig. 1 standing balance geometry), #3 (Fig. 2 push: xi inside the base versus past it), #4 (Fig. 3 margin of
stability), #6 (Fig. 5 four sensors on the body), #10 (Fig. 9 recovery ladder), #11 (Fig. 10 slip and trip).

Numbers (module10.html line numbers):
  m = 70 kg, COM height l = 1.0 m above the ankle, omega0 = sqrt(g/l) = 3.1 1/s, forward margin b = 0.10 m,
  J_max = m omega0 b = 22 N s, walking speed 1.4 m/s (106); capture-step reach model (336-337), Lab D (young
  tau 0.10 s, t_move 0.20 s, L_step 0.60 m; aged 0.18, 0.32, 0.42), K8 solution (746: a 40 N s push gives xi_s =
  0.467 m at touchdown, 0.60 m reach); sensor latencies 15 / 150 / 35 / 40 ms (158, 160, 162, 164); trip
  d_xi = v / omega0 (313); heel-strike mu_req = 0.20 and ice mu_avail = 0.08 (K10 solution, 764).
Base of support: the text gives only b = 0.10 m.  The usable base is taken from Module 7 (module07.html line 176):
  the quiet-standing COM is 0.02 m ahead of the ankle, the base runs 0.05 m behind to 0.12 m ahead of the ankle, so
  b = 0.12 - 0.02 = 0.10 m at rest.  Stature 1.75 m (course reference; the text states none).
Body art: lynch_body.py (Patrick J. Lynch, CC BY 2.5).
"""
import math

import numpy as np

import house as H
import lynch_body as LB
from m05.body import finish, it

SHARED_DEFS = LB.SHARED_DEFS
O, I, T = H.OVERLAY, H.INK, H.TISSUE
BOXFILL, GRID = "#f7f4ef", "#e6e6e6"
BODY = H.MAX_DISPLAY_H_BODY

# ---------------------------------------------------------------- module constants (line numbers above)
G, M_KG, ELL, H_M = 9.81, 70.0, 1.0, 1.75
W0 = 3.1                                                       # 1/s, as the text and every lab script (106, 136, Lab D)
COM_AHEAD, D_TOE, D_HEEL = 0.02, 0.12, 0.05                    # m from the ankle (Module 7 line 176)
B_REST = D_TOE - COM_AHEAD                                     # 0.10 m (line 106)
J_MAX = M_KG * W0 * B_REST                                     # 22 N s (line 106)
L_YOUNG, L_AGED = 0.60, 0.42                                   # capture reach (Lab D)
TAU, T_MOVE = 0.10, 0.20                                       # young reaction delay, foot travel time (Lab D)
T_STEP = TAU + T_MOVE
J_K8 = 40.0                                                    # K8 push (line 746)
XI_K8 = J_K8 / (M_KG * W0) * math.exp(W0 * T_STEP)             # 0.467 m at touchdown (line 746)
assert abs(W0 - math.sqrt(G / ELL)) < 0.05 and (round(J_MAX, 0), round(XI_K8, 3)) == (22.0, 0.467), (W0, J_MAX, XI_K8)
assert round(1.4 / W0, 2) == 0.45


# ---------------------------------------------------------------- small helpers
def defs(p, s):
    return f"<defs>{H.markers(p, s)}</defs>"


def poly(s, pts, col, w="curve", dash=None, extra=""):
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    return (f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="none" stroke="{col}" '
            f'stroke-width="{s(H.PX[w]):.2f}" stroke-linejoin="round"{da} {extra}/>')


def path_d(pts):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def white_under(s, x1, y1, x2, y2, w=4):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#fff" '
            f'stroke-width="{s(w):.2f}" opacity="0.85"/>')


def vline(s, x, y1, y2, col=None, dash=H.DASH_REF, w="ref"):
    """Dashed reference line with a white under-stroke so it reads over the art."""
    return white_under(s, x, y1, x, y2) + H.line(s, x, y1, x, y2, col or O["dim"], w, dash=dash)


def leader(s, x1, y1, x2, y2, col=None):
    return H.line(s, x1, y1, x2, y2, col or I["secondary"], "leader")


def dline(s, x1, y1, x2, y2, col=None, w="ref", dash=H.DASH_REF):
    return white_under(s, x1, y1, x2, y2) + H.line(s, x1, y1, x2, y2, col or O["dim"], w, dash=dash)


def floor(s, x0, x1, y):
    return H.line(s, x0, y, x1, y, I["rule"], "axis")


def dot(s, x, y, col=None, r=3.5):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{col or I["primary"]}" stroke="#fff" '
            f'stroke-width="{s(1.2):.2f}"/>')


def cop_mark(s, x, y):
    """Centre of pressure: blue cross-hair circle (a mark, not anatomy; Module 7 idiom)."""
    r, c = s(5.5), O["geometry"]
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="#fff" stroke="{c}" stroke-width="{s(2):.2f}"/>'
            f'<path d="M{x - r * 1.7:.2f},{y:.2f}h{r * 3.4:.2f}M{x:.2f},{y - r * 1.7:.2f}v{r * 3.4:.2f}" '
            f'stroke="{c}" stroke-width="{s(1.4):.2f}"/>')


def xi_mark(s, x, y, col=None):
    """Extrapolated COM: open circle (Module 7 line 190)."""
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(6):.2f}" fill="#fff" stroke="{col or I["primary"]}" '
            f'stroke-width="{s(2):.2f}"/>')


def lines(s, x, y, rows, size="label2", fill=None, anchor="start", dy=None):
    dy = dy or s(H.PX[size] * 1.3)
    return "".join(H.label(s, x, y + i * dy, t, size, fill or I["primary"], anchor) for i, t in enumerate(rows))


def box(s, x, y, w, h, fill=BOXFILL, stroke=None, extra=""):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" '
            f'stroke="{stroke or I["secondary"]}" stroke-width="{s(1):.2f}" {extra}/>')


def arc_pts(cx, cy, r, a0, a1, n=24):
    """Screen angles in degrees: 0 = +x, + = clockwise (y down)."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def arc_arrow(s, p, cx, cy, r, a0, a1, meaning, both=False):
    w = {"geometry": "geom", "dim": "ref"}.get(meaning, "force")
    ms = f' marker-start="url(#{p}a_{meaning})"' if both else ""
    return (f'<path d="{path_d(arc_pts(cx, cy, r, a0, a1))}" fill="none" stroke="{O[meaning]}" '
            f'stroke-width="{s(H.PX[w]):.2f}" marker-end="url(#{p}a_{meaning})"{ms}/>')


def dim_h(s, p, x1, x2, y, meaning="geometry", tick=6):
    col = O[meaning]
    return (H.arrow(s, p, x1, y, x2, y, meaning, both=True)
            + H.line(s, x1, y - s(tick), x1, y + s(tick), col, "leader")
            + H.line(s, x2, y - s(tick), x2, y + s(tick), col, "leader"))


def com_model(a):
    """COM of the text (l = 1.0 m above the ankle, 0.02 m ahead at rest) after the whole body turns a degrees about
    the ankle (+ = forward). Returns metres (forward, up) from the ankle."""
    v = LB.rot((COM_AHEAD, -ELL), a)
    return v[0], -v[1]


def lean_for(x_com):
    """Whole-body lean a (deg) that puts the model COM x_com metres ahead of the ankle."""
    r = math.hypot(COM_AHEAD, ELL)
    return math.degrees(math.asin(x_com / r) - math.atan2(COM_AHEAD, ELL))


def body_at(p, s, P, ank_x, fy, hgt, ref="ankle"):
    """Draw pose P with its ankle (`ref`: near, or the far one) at x = ank_x, floor at fy. Returns (svg, J)."""
    _, J0 = LB.draw(p, s, P, 0.0, fy, hgt)
    return LB.draw(p, s, P, ank_x - J0[ref][0], fy, hgt)


class Frame:
    """Metres from the near ankle -> figure units, for one body."""

    def __init__(self, J, hgt):
        self.ax, self.ay, self.fy = J["ankle"][0], J["ankle"][1], J["floor_y"]
        self.k = hgt / H_M

    def x(self, m):
        return self.ax + self.k * m

    def com(self, a):
        fx, up = com_model(a)
        return self.ax + self.k * fx, self.ay - self.k * up

    def cm(self, v):
        return v * self.k


def base_bar(s, F, lo, hi, y_off=2.0, h=7.0):
    """Base of support: a bar on the floor from lo to hi metres from the ankle, with end ticks."""
    o = [box(s, F.x(lo), F.fy + s(y_off), F.k * (hi - lo), s(h))]
    for m in (lo, hi):
        o.append(H.line(s, F.x(m), F.fy - s(6), F.x(m), F.fy + s(y_off + h + 4), I["secondary"], "leader"))
    return "".join(o)


# ================================================================ svg #2  Fig. 1 standing balance geometry
def fig2():
    p = "m10f2_"
    hgt, fy = 440.0, 470.0
    VB = (0, 0, 760, 620)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    body, J = LB.standing_full(p, s, 110.0, fy, hgt)
    F = Frame(J, hgt)
    o = [defs(p, s), floor(s, 20, 740, fy), body]
    x_rest = F.x(COM_AHEAD)                                    # ground projection of the quiet-standing COM
    com = (x_rest, F.ay - F.k * ELL)
    # capture region: from the front edge of the base to the reach L_step, measured from the rest COM projection
    cap0, cap1 = F.x(D_TOE), x_rest + F.k * L_YOUNG
    o.append(box(s, F.x(-D_HEEL), fy + s(2), F.k * (D_TOE + D_HEEL), s(8)))
    o.append(box(s, cap0, fy + s(2), cap1 - cap0, s(8), fill=O["geometry"], stroke=O["geometry"],
                 extra='fill-opacity="0.28"'))
    for xx in (F.x(-D_HEEL), cap0, cap1):
        o.append(H.line(s, xx, fy - s(6), xx, fy + s(14), I["secondary"], "leader"))
    o.append(vline(s, com[0], com[1], fy))
    o.append(H.com_mark(s, *com))
    # COM label (right of the body)
    lx = F.x(L_YOUNG + 0.12)
    o.append(leader(s, com[0] + s(9), com[1], lx - s(6), com[1]))
    o.append(H.label(s, lx, com[1] + s(5), "centre of mass (COM)"))
    o.append(H.label(s, lx, com[1] + s(23), "ℓ = 1.0 m above the ankle", "label2", I["secondary"]))
    vy = com[1] + 0.20 * hgt
    o.append(leader(s, com[0] + s(3), vy, lx - s(6), vy))
    o.append(H.label(s, lx, vy + s(5), "its ground projection lands inside the base", "label2"))
    # labels below the floor, to the right of the bars
    lx2 = cap1 + s(40)
    o.append(leader(s, lx2 - s(6), fy + s(34), cap0 - s(20), fy + s(11), O["geometry"]))
    o.append(H.label(s, lx2, fy + s(38), "capture region: where a step can land", "label2", O["geometry"]))
    o.append(leader(s, lx2 - s(6), fy + s(58), F.x(0.0), fy + s(12)))
    o.append(H.label(s, lx2, fy + s(62), "base of support: 0.05 m behind to 0.12 m ahead of the ankle", "label2"))
    ydim = fy + s(92)
    o.append(dim_h(s, p, x_rest, cap1, ydim, "geometry"))
    o.append(H.line(s, x_rest + F.k * L_AGED, ydim - s(6), x_rest + F.k * L_AGED, ydim + s(6), O["geometry"], "leader"))
    o.append(H.label(s, cap1 + s(12), ydim + s(5), f"reach {it('L')}{H.sub('step', s, 'label2')}: {L_YOUNG:.2f} m young "
                     f"(Lab D), {L_AGED:.2f} m aged (tick)", "label2", O["geometry"]))
    o.append(LB.credit(s, 20, fy + s(124), width=720))
    aria = ("Lateral view of a standing human skeleton inside its body outline, facing right. The centre of mass is "
            "marked 1.0 metre above the ankle, and a dashed vertical drops from it to a point inside the base of "
            "support, a bar on the floor from 5 centimetres behind to 12 centimetres ahead of the ankle. Beyond the "
            "front edge a blue band marks the capture region where a step can land, out to the reach of 0.60 "
            "metres for a young adult, with a tick at 0.42 metres for an aged adult.")
    return finish(VB, aria, s, o)


# ================================================================ svg #3  Fig. 2 push: xi inside the base or past it
def strip(s, p, F, x_anchor, zs, zy, xs):
    """Floor under one body, magnified: ankle at x_anchor, zs units per metre. Returns (svg, X) with X(metres from the
    ankle) -> x. Dotted leaders join the base bar of the body to the magnified one."""
    X = lambda m: x_anchor + zs * m            # noqa: E731
    o = [H.line(s, F.x(-D_HEEL), F.fy + s(14), X(-D_HEEL), zy - s(12), I["rule"], "leader"),
         H.line(s, F.x(D_TOE), F.fy + s(14), X(D_TOE), zy - s(12), I["rule"], "leader"),
         H.line(s, X(-0.07), zy, X(xs), zy, I["rule"], "leader"),
         box(s, X(-D_HEEL), zy - s(5), zs * (D_TOE + D_HEEL), s(10))]
    for m, t in ((-D_HEEL, "−5"), (0.0, "0"), (D_TOE, "12")):
        o.append(H.line(s, X(m), zy + s(5), X(m), zy + s(11), I["axis"], "leader"))
        o.append(H.label(s, X(m), zy + s(26), t, "tick", I["secondary"], "middle"))
    return "".join(o), X


def fig3():
    p = "m10f3_"
    hgt, fy, zy, zs = 310.0, 330.0, 420.0, 450.0
    VB = (0, 0, 760, 590)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    o = [defs(p, s)]
    panels = [(0.0, 15.0, "modest push", False), (380.0, J_K8, "harder push", True)]
    for x0, Jn, title, step in panels:
        xi0 = Jn / (M_KG * W0)                                  # xi right after the impulse, from rest (line 336)
        body, J = body_at(p, s, LB.pose(), x0 + 100.0, fy, hgt)  # upright at the instant of the push
        F = Frame(J, hgt)
        com = F.com(0.0)
        o += [body, floor(s, x0 + 20, x0 + 360, fy), base_bar(s, F, -D_HEEL, D_TOE)]
        o.append(vline(s, com[0], com[1], fy))
        o.append(H.com_mark(s, *com))
        o.append(H.arrow(s, p, com[0] - s(78), com[1], com[0] - s(14), com[1], "force"))
        o.append(H.label(s, com[0] - s(52), com[1] - s(10), f"{it('J')} = {Jn:.0f} N·s", "label2", O["force"],
                         "middle"))
        o.append(H.label(s, x0 + 190, 26, title, anchor="middle"))
        # magnified floor
        sv, X = strip(s, p, F, x0 + 60.0, zs, zy, 0.66 if step else 0.30)
        o.append(sv)
        xr = COM_AHEAD
        o.append(H.com_mark(s, X(xr), zy - s(20)))
        o.append(H.label(s, X(xr) + s(14), zy - s(38), "COM at rest", "label2", I["secondary"], "end"))
        xi = xr + xi0
        o.append(H.arrow(s, p, X(xr) + s(8), zy - s(20), X(xi) - s(8), zy - s(20), "dim"))
        o.append(xi_mark(s, X(xi), zy - s(20)))
        o.append(H.label(s, X(xi) + s(10), zy - s(36), f"ξ = {xi0 * 100:.1f} cm", "label2", I["primary"]))
        sub = f"{it('ξ')} = {it('J')}/({it('m')}{it('ω')}₀), measured from the rest COM"
        if not step:
            o.append(H.label(s, x0 + 190, zy + s(64), "ξ is inside the base (edge 10 cm from the rest COM)", "label2",
                             I["primary"], "middle"))
            o.append(H.label(s, x0 + 190, zy + s(82), "ankle, then hip, arrests the lean: no step", "label2",
                             I["primary"], "middle"))
            o.append(H.label(s, x0 + 190, zy + s(100), sub, "label2", I["secondary"], "middle"))
        else:
            xs_ = xr + XI_K8                                    # xi at touchdown, line 746
            xf = xs_ + 0.08                                     # front edge of the new base: xi_s + Delta
            o.append(box(s, X(xf - (D_HEEL + D_TOE)), zy + s(10) - s(15), zs * (D_HEEL + D_TOE), s(10)))
            o.append(H.line(s, X(xf), zy - s(10), X(xf), zy + s(14), I["secondary"], "leader"))
            o.append(H.label(s, X(xf), zy + s(26), f"{it('x')}{H.sub('foot', s, 'tick')}", "tick", I["secondary"],
                             "middle"))
            o.append(H.arrow(s, p, X(xi) + s(10), zy - s(20), X(xs_) - s(10), zy - s(20), "dim"))
            o.append(xi_mark(s, X(xs_), zy - s(20)))
            o.append(H.label(s, X(xs_) + s(10), zy - s(36), f"ξ = {XI_K8 * 100:.0f} cm", "label2", I["primary"]))
            o.append(H.label(s, X(xs_) + s(10), zy - s(52), "at touchdown", "label2", I["secondary"]))
            o.append(H.label(s, x0 + 190, zy + s(64), "ξ is past the edge: only a step can catch the fall", "label2",
                             I["primary"], "middle"))
            o.append(H.label(s, x0 + 190, zy + s(82), f"new base planted at ξ + Δ (Δ = 8 cm), {T_STEP:.2f} s later",
                             "label2", I["primary"], "middle"))
            o.append(H.label(s, x0 + 190, zy + s(100), sub, "label2", I["secondary"], "middle"))
    o.append(H.label(s, 20, zy + s(44), "floor under each body, magnified: cm from the ankle", "label2", I["secondary"]))
    o.append(LB.credit(s, 20, 556, width=720))
    aria = ("Two standing skeletons just after a forward push, each with a base-of-support bar on the floor, a dashed "
            "drop from the centre of mass, and the floor magnified below in centimetres from the ankle. Left, a 15 "
            "newton-second push puts the extrapolated centre of mass xi 6.9 centimetres ahead of the rest position, "
            "inside the 10 centimetre margin, so the ankle and hip arrest it with no step. Right, a 40 newton-second "
            "push puts xi 18.4 centimetres ahead, past the foot edge; xi grows to 47 centimetres by touchdown at 0.30 "
            "seconds, and a new base is planted ahead of it.")
    return finish(VB, aria, s, o)


# ================================================================ svg #4  Fig. 3 margin of stability
def fig4():
    p = "m10f4_"
    hgt, fy, zy, zs = 400.0, 400.0, 500.0, 1250.0
    VB = (0, 0, 760, 600)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    xc, xd = 0.04, 0.10                                        # illustrative state: x_com (m from the ankle), xdot (m/s)
    lead = xd / W0
    xi = xc + lead
    b = D_TOE - xi
    jm = M_KG * W0 * b
    assert (round(lead * 100, 1), round(xi * 100, 1), round(b * 100, 1), round(jm, 1)) == (3.2, 7.2, 4.8, 10.4)
    a = lean_for(xc)
    body, J = body_at(p, s, LB.pose(pelvis=a), 150.0, fy, hgt)
    F = Frame(J, hgt)
    com = F.com(a)
    o = [defs(p, s), body, floor(s, 20, 400, fy), base_bar(s, F, -D_HEEL, D_TOE)]
    o.append(vline(s, com[0], com[1], fy))
    o.append(H.com_mark(s, *com))
    o.append(H.arrow(s, p, com[0] - s(78), com[1], com[0] - s(12), com[1], "force"))
    o.append(H.label(s, com[0] - s(52), com[1] - s(10), f"impulse {it('J')}", "label2", O["force"], "middle"))
    o.append(H.arrow(s, p, com[0] + s(12), com[1], com[0] + s(60), com[1], "geometry"))
    o.append(H.label(s, com[0] + s(64), com[1] + s(5), f"{it('ẋ')} = {xd:.2f} m/s", "label2", O["geometry"]))
    o.append(H.label(s, com[0] + s(64), com[1] - s(32), "centre of mass (COM)", "label2", I["primary"]))
    o.append(leader(s, com[0] + s(8), com[1] - s(8), com[0] + s(62), com[1] - s(28)))
    # magnified floor (ankle at x = 520, 1250 units per metre)
    sv, X = strip(s, p, F, 520.0, zs, zy, 0.17)
    o.append(sv)
    y1 = zy - s(22)
    o.append(H.com_mark(s, X(xc), y1))
    o.append(H.arrow(s, p, X(xc) + s(8), y1, X(xi) - s(8), y1, "dim"))
    o.append(xi_mark(s, X(xi), y1))
    o.append(H.label(s, X(xc) - s(8), y1 - s(14), f"{it('x')}{H.sub('com', s, 'label2')}", "label2", I["primary"], "end"))
    o.append(H.label(s, X(xi) + s(2), y1 - s(14), "ξ", "label", I["primary"], "middle"))
    ylead = zy - s(56)
    o.append(dim_h(s, p, X(xc), X(xi), ylead, "dim"))
    o.append(H.label(s, (X(xc) + X(xi)) / 2, ylead - s(9), f"{it('ẋ')}/ω₀ = {lead * 100:.1f} cm", "label2", I["primary"],
                     "middle"))
    yb = zy - s(92)
    o.append(dim_h(s, p, X(xi), X(D_TOE), yb, "geometry"))
    o.append(H.label(s, (X(xi) + X(D_TOE)) / 2, yb - s(9), f"margin {it('b')} = {b * 100:.1f} cm", "label2", O["geometry"],
                     "middle"))
    o.append(vline(s, X(D_TOE), yb + s(8), zy - s(12), O["geometry"]))
    o.append(H.label(s, X(D_TOE) + s(6), zy - s(30), "front edge", "label2", I["secondary"]))
    o.append(poly(s, [(X(xi) + s(10), zy - s(126)), (X(D_TOE) - s(10), zy - s(126))], O["force"], "force", dash=H.DASH_REF,
                  extra=f'marker-end="url(#{p}a_force)"'))
    o.append(H.label(s, X(D_TOE) + s(4), zy - s(136), f"{it('J')} moves ξ toward the edge by {it('J')}/({it('m')}{it('ω')}₀)",
                     "label2", O["force"], "end"))
    # numbers
    rows = [("illustrative state", I["secondary"]),
            (f"m = 70 kg, ℓ = 1.0 m, ω₀ = √(g/ℓ) ≈ {W0:.1f} s⁻¹", I["primary"]),
            (f"{it('x')}{H.sub('com', s, 'label2')} = {xc * 100:.1f} cm from the ankle, {it('ẋ')} = {xd:.2f} m/s",
             I["primary"]),
            (f"ξ = {it('x')}{H.sub('com', s, 'label2')} + {it('ẋ')}/ω₀ = {xc * 100:.1f} + {lead * 100:.1f} = "
             f"{xi * 100:.1f} cm", I["primary"]),
            (f"{it('b')} = {it('x')}{H.sub('edge', s, 'label2')} − ξ = {D_TOE * 100:.1f} − {xi * 100:.1f} = "
             f"{b * 100:.1f} cm", I["primary"]),
            (f"{it('J')}{H.sub('max', s, 'label2')} = {it('m')}ω₀{it('b')} = 70 × {W0:.1f} × {b:.3f} = {jm:.1f} N·s",
             I["primary"]),
            (f"at rest ({it('b')} = {B_REST * 100:.0f} cm) the same formula gives {J_MAX:.0f} N·s", I["secondary"])]
    for i, (txt, col) in enumerate(rows):
        o.append(H.label(s, 430, 44 + i * s(19), txt, "label2", col))
    o.append(H.label(s, 20, zy + s(44), "floor, magnified: cm from the ankle", "label2", I["secondary"]))
    o.append(LB.credit(s, 20, 572, width=720))
    aria = ("A standing skeleton leaning slightly forward with its centre of mass marked, 4 centimetres ahead of the "
            "ankle and moving forward at 0.10 metres per second, with a dashed line dropping the centre of mass to "
            "its ground projection x_com. Below, the floor is magnified: the extrapolated centre of mass xi sits 3.2 "
            "centimetres ahead of x_com (xdot over omega-zero), at 7.2 centimetres, and the margin of stability b is "
            "the remaining 4.8 centimetres to the front edge of the base of support at 12 centimetres. A forward "
            "impulse J moves xi toward that edge; the largest impulse still arrested is 10.4 newton-seconds.")
    return finish(VB, aria, s, o)


# ================================================================ svg #6  Fig. 5 four sensor channels
SENSORS = [   # (title, two description lines, latency ms, line of the text, site on the body)
    ("Vision (retina, optic flow)", ("sway θ from the drift of the scene", "wide-field, but slow to process"),
     150, 164),
    ("Vestibular organs (inner ear)", ("canals: head angular velocity", "otoliths: tilt and linear acceleration"),
     15, 158),
    ("Muscle spindle (Ia, II)", ("muscle length and its rate: ankle θ, θ̇", "afferent of the stretch reflex"),
     35, 160),
    ("Golgi tendon organ (Ib)", ("tendon tension: the muscle's force", "complements the spindle's length"),
     40, 162),
]


def fig6():
    p = "m10f6_"
    hgt, fy = 470.0, 520.0
    VB = (0, 0, 760, 600)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    body, J = LB.standing_full(p, s, 70.0, fy, hgt)
    F = Frame(J, hgt)
    o = [defs(p, s), floor(s, 20, 150, fy), body]
    k = hgt / H_M
    vx, vy = J["vertex"]
    nk = J["neck"]
    kx, ky = J["knee"]
    ax, ay = J["ankle"]
    sites = [(vx + 0.034 * hgt, vy + 0.052 * hgt),                         # retina: front of the skull
             (vx - 0.012 * hgt, vy + 0.074 * hgt),                         # inner ear: behind the eye, low in the skull
             (kx + 0.40 * (ax - kx) - 0.018 * hgt, ky + 0.34 * (ay - ky)),  # calf belly (muscle spindle)
             (kx + 0.78 * (ax - kx) - 0.014 * hgt, ky + 0.72 * (ay - ky))]  # muscle-tendon junction (Golgi organ)
    rows_y = [92.0, 222.0, 352.0, 482.0]
    xl = 330.0
    lat_x0, lat_w, lat_max = 580.0, 150.0, 160.0                           # latency bar: 0..160 ms
    rng = np.random.default_rng(10)
    for i, ((title, desc, lat, ln), (sx, sy), col, ry) in enumerate(zip(SENSORS, sites, H.SERIES[:3] + ["#7b4a9e"], rows_y)):  # 4th sensor purple: green is neural drive
        o.append(H.line(s, sx + s(6), sy, xl - s(8), ry - s(5), col, "leader"))
        o.append(f'<circle cx="{sx:.2f}" cy="{sy:.2f}" r="{s(6):.2f}" fill="#fff" stroke="{col}" stroke-width="{s(2.2):.2f}"/>'
                 f'<circle cx="{sx:.2f}" cy="{sy:.2f}" r="{s(2.4):.2f}" fill="{col}"/>')
        o.append(box(s, xl - s(2), ry - s(11), s(11), s(11), fill=col, stroke=col))
        o.append(H.label(s, xl + s(16), ry, title))
        o.append(H.label(s, xl + s(16), ry + s(20), desc[0], "label2", I["secondary"]))
        o.append(H.label(s, xl + s(16), ry + s(37), desc[1], "label2", I["secondary"]))
        # latency, to scale
        o.append(H.label(s, lat_x0, ry, f"latency {lat} ms", "label2", I["primary"]))
        o.append(box(s, lat_x0, ry + s(6), lat_w * lat / lat_max, s(8), fill=col, stroke=col))
        o.append(H.line(s, lat_x0, ry + s(20), lat_x0 + lat_w, ry + s(20), GRID, "leader"))
        # noise sample: zero-mean, equal amplitude for every channel (the text gives no noise levels)
        y = rng.normal(0.0, 1.0, 36)
        pts = [(lat_x0 + lat_w * j / 35, ry + s(44) - 5.0 * y[j]) for j in range(36)]
        o.append(poly(s, pts, col, "curve_multi"))
    o.append(H.label(s, lat_x0, rows_y[0] - s(52), "afferent latency, to scale,", "label2", I["secondary"]))
    o.append(H.label(s, lat_x0, rows_y[0] - s(36), "and a sample of the noise", "label2", I["secondary"]))
    o.append(H.label(s, xl + s(16), fy + s(36), "noise samples: schematic, equal amplitude, fixed seed", "label2",
                     I["secondary"]))
    o.append(LB.credit(s, 20, fy + s(52), width=720))
    aria = ("A standing skeleton in side view with four marked sensor sites, each joined by a coloured line to a label "
            "row. Vision (red site at the eye, optic flow) has a latency of about 150 milliseconds. The vestibular "
            "organs (the inner ear, canals and otoliths) have about 15 milliseconds. The muscle spindle in the calf "
            "reports muscle length and rate, hence ankle angle, with about 35 milliseconds and drives the stretch "
            "reflex. The Golgi tendon organ at the tendon reports tendon force with about 40 milliseconds. Each row "
            "shows a latency bar drawn to scale and a sample noise trace.")
    return finish(VB, aria, s, o)


# ================================================================ svg #10  Fig. 9 recovery ladder
def com_dx(J, hgt):
    """Kit (Winter) COM, metres ahead of the ankle."""
    return (J["com"][0] - J["ankle"][0]) / (hgt / H_M)


def solve_pose(make, target, hgt, lo=-4.0, hi=70.0):
    """Bisection on the pose parameter a so that the kit COM is `target` metres ahead of the ankle."""
    s0 = H.Scale(760, 600, max_h=BODY)
    for _ in range(40):
        mid = (lo + hi) / 2
        _, J = LB.draw("", s0, make(mid), 0.0, 400.0, hgt)
        lo, hi = (mid, hi) if com_dx(J, hgt) < target else (lo, mid)
    return (lo + hi) / 2


def hip_pose(a):
    """Hip strategy: the trunk and arms turn forward by a, the hips go back (thigh 6 deg behind the vertical)."""
    arm = dict(hip=a + 6.0, shoulder=1.2 * a - 70.0, elbow=15.0)
    return LB.pose(pelvis=a, trunk=0.2 * a, near=arm, far=arm)


STEP_DELTA = 0.10                                          # Delta drawn in Fig. 9 (m); the text leaves it free (line 285)


def step_pose(xi, step, hgt):
    """Stance leg = far (rigid, foot flat); stepping leg = near, its ankle `step` m ahead of the stance ankle at the
    same height (2-D Newton on hip and knee); the lean a is set so that the kit COM is xi m ahead of the stance ankle."""
    s0 = H.Scale(760, 600, max_h=BODY)
    k = hgt / H_M

    def jn(a, h, kn):
        P = LB.pose(pelvis=a, near=dict(hip=h, knee=kn), far=dict(hip=0), anchor=("heel", "far"))
        return LB.draw("", s0, P, 0.0, 400.0, hgt)[1]

    def res(J):
        return ((J["ankle"][0] - J["ankle_far"][0]) / k - step, (J["ankle"][1] - J["ankle_far"][1]) / k)

    def legs(a):
        h, kn, d = 12.0, 25.0, 0.05
        for _ in range(40):
            f0 = res(jn(a, h, kn))
            if abs(f0[0]) + abs(f0[1]) < 1e-8:
                break
            fh, fk = res(jn(a, h + d, kn)), res(jn(a, h, kn + d))
            m = [[(fh[0] - f0[0]) / d, (fk[0] - f0[0]) / d], [(fh[1] - f0[1]) / d, (fk[1] - f0[1]) / d]]
            det = m[0][0] * m[1][1] - m[0][1] * m[1][0]
            h -= (f0[0] * m[1][1] - f0[1] * m[0][1]) / det
            kn -= (m[0][0] * f0[1] - m[1][0] * f0[0]) / det
        return h, kn

    a = 8.0
    for _ in range(8):
        h, kn = legs(a)
        J = jn(a, h, kn)
        e = (J["com"][0] - J["ankle_far"][0]) / k - xi
        a -= e / (ELL * math.pi / 180)
    assert abs(e) < 1e-4 and abs(res(J)[0]) < 1e-4 and abs(res(J)[1]) < 1e-4, (e, res(J))
    return LB.pose(pelvis=a, near=dict(hip=h, knee=kn), far=dict(hip=0), anchor=("heel", "far"))


def fig10():
    p = "m10f10_"
    hgt, fy = 300.0, 330.0
    VB = (0, 0, 760, 560)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    XI = [0.060, 0.105, 0.150]                                 # xi at rest, metres ahead of the ankle
    makers = [lambda a: LB.pose(pelvis=a), hip_pose, lambda a: LB.pose(pelvis=a)]
    titles = [("1. ankle", "small lean, ankle torque"), ("2. hip", "trunk and arms counter-rotate"),
              ("3. step", "foot planted at ξ + Δ")]
    o = [defs(p, s)]
    for i, (xi, mk) in enumerate(zip(XI, makers)):
        x0 = 253.0 * i
        if i < 2:
            body, J = body_at(p, s, mk(solve_pose(mk, xi, hgt)), x0 + 80.0, fy, hgt)
        else:
            body, J = body_at(p, s, step_pose(xi, xi + STEP_DELTA - D_TOE, hgt), x0 + 80.0, fy, hgt, ref="ankle_far")
        F = Frame(J, hgt)
        if i == 2:
            F.ax, F.ay = J["ankle_far"]
        com = J["com"]
        o += [body, floor(s, x0 + 12, x0 + 245, fy), base_bar(s, F, -D_HEEL, D_TOE)]
        o.append(H.line(s, F.x(D_TOE), fy - s(6), F.x(D_TOE), fy + s(14), O["flag"], "geom"))
        o.append(vline(s, com[0], com[1], fy))
        o.append(H.com_mark(s, *com))
        o.append(xi_mark(s, F.x(xi), fy))
        o.append(H.label(s, x0 + 127, 24, titles[i][0], anchor="middle"))
        o.append(H.label(s, x0 + 127, 42, titles[i][1], "label2", I["secondary"], "middle"))
        o.append(H.label(s, x0 + 127, fy + s(50), f"ξ = {xi * 100:.1f} cm, {it('b')} = {(D_TOE - xi) * 100:+.1f} cm".replace("-", "−"),
                         "label2", I["primary"], "middle"))
        if i == 0:
            ax_, ay_ = J["ankle"]
            o.append(arc_arrow(s, p, ax_, ay_, s(40), -30, -120, "geometry"))
            o.append(H.joint_centre(s, ax_, ay_))
        elif i == 1:
            hj = J["hip"]
            o.append(cop_mark(s, F.x(D_TOE), fy))
            o.append(H.label(s, F.x(D_TOE) + s(14), fy + s(30), "COP at the edge", "label2", O["geometry"]))
            o.append(arc_arrow(s, p, hj[0], hj[1], s(52), -70, -20, "geometry"))
            o.append(H.joint_centre(s, *hj))
        else:
            xf = F.x(xi + STEP_DELTA)                           # front edge of the new base: x_foot = xi + Delta
            o.append(box(s, xf - F.k * (D_TOE + D_HEEL), fy + s(14), F.k * (D_TOE + D_HEEL), s(7), stroke=O["geometry"]))
            o.append(H.line(s, xf, fy + s(10), xf, fy + s(25), O["geometry"], "geom"))
            o.append(H.label(s, xf + s(6), fy + s(30), f"{it('x')}{H.sub('foot', s, 'label2')}", "label2", O["geometry"]))
    # the ξ axis (magnified), foot edge marked
    ya, zs, ax0 = 445.0, 3000.0, 70.0
    X = lambda m: ax0 + zs * m                             # noqa: E731
    o.append(f'<rect x="{X(0):.2f}" y="{ya - s(22):.2f}" width="{zs * D_TOE:.2f}" height="{s(22):.2f}" fill="{BOXFILL}"/>')
    o.append(f'<rect x="{X(D_TOE):.2f}" y="{ya - s(22):.2f}" width="{zs * (0.21 - D_TOE):.2f}" height="{s(22):.2f}" '
             f'fill="{O["flag"]}" fill-opacity="0.18"/>')
    o.append(H.line(s, X(0), ya, X(0.21), ya, I["axis"], "axis"))
    for cm in (0, 5, 10, 15, 20):
        o.append(H.line(s, X(cm / 100), ya, X(cm / 100), ya + s(5), I["axis"], "axis"))
        o.append(H.label(s, X(cm / 100), ya + s(19), f"{cm}", "tick", I["primary"], "middle"))
    o.append(H.line(s, X(D_TOE), ya - s(34), X(D_TOE), ya + s(5), O["flag"], "geom"))
    o.append(H.label(s, X(D_TOE), ya - s(40), "foot edge (b = 0): 12", "label2", O["flag"], "middle"))
    for i, xi in enumerate(XI):
        o.append(xi_mark(s, X(xi), ya - s(11)))
        o.append(H.label(s, X(xi), ya - s(26), str(i + 1), "label", I["primary"], "middle"))
    o.append(H.label(s, X(0.0), ya + s(40), "ξ inside: fixed support (ankle, hip)", "label2", I["primary"]))
    o.append(H.label(s, X(0.21), ya + s(40), "ξ past the edge: a step is mandatory", "label2", I["primary"], "end"))
    o.append(H.label(s, X(0.105), ya + s(58), "extrapolated COM ξ, cm ahead of the ankle (rest, leaning body)", "label2",
                     I["secondary"], "middle"))
    o.append(LB.credit(s, 20, 526, width=720))
    aria = ("Three skeletons forming a recovery ladder, indexed by the extrapolated centre of mass xi. In the first, a "
            "small lean puts xi 6 centimetres ahead of the ankle, inside the base, and the centre of pressure shifts "
            "forward: an ankle response. In the second, xi is 10.5 centimetres ahead, just inside the 12 centimetre "
            "foot edge, and the trunk and arms counter-rotate about the hip with the centre of pressure at the toe "
            "edge. In the third, xi is 15 centimetres ahead, past the edge, and a new base is planted ahead of xi. "
            "A bottom axis in centimetres marks the foot edge at 12 centimetres, where a step becomes mandatory.")
    return finish(VB, aria, s, o)


# ================================================================ svg #11  Fig. 10 slip and trip
MU_REQ, MU_ICE = 0.20, 0.08                                    # heel-strike demand (Appendix), ice (K10 solution, 764)
V_WALK = 1.4                                                   # walking speed, m/s (line 106)


def fig11():
    p = "m10f11_"
    hgt, fy = 300.0, 352.0
    VB = (0, 0, 760, 490)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    k = hgt / H_M
    o = [defs(p, s), floor(s, 12, 372, fy), floor(s, 392, 748, fy)]
    # ---- slip: heel strike, lead foot slides forward, the body falls backward
    slip = LB.pose(pelvis=-8, trunk=-4, near=dict(hip=22, knee=4, contact="heel", shoulder=60, elbow=15),
                   far=dict(hip=-10, knee=45, contact=None, ankle=-20, shoulder=75, elbow=15), anchor=("heel", "near"))
    hx = 285.0
    body, J = LB.draw(p, s, slip, hx, fy, hgt)
    com = J["com"]
    o += [body, vline(s, com[0], com[1], fy)]
    o.append(box(s, J["heel"][0], fy + s(2), J["toe"][0] - J["heel"][0], s(7)))
    o.append(H.com_mark(s, *com))
    o.append(H.label(s, com[0] - s(10), fy + s(20), "COM lands behind the base", "label2", I["primary"], "end"))
    # forces on the foot at the heel contact
    cx = J["heel"][0]
    fv, fh = 105.0, 105.0 * MU_REQ
    lim = math.atan(MU_ICE)
    o.append(white_under(s, cx, fy, cx, fy - fv, 5))
    o.append(H.arrow(s, p, cx, fy, cx, fy - fv, "reaction"))
    o.append(H.arrow(s, p, cx, fy - s(1), cx - fh, fy - s(1), "reaction"))
    o.append(H.line(s, cx, fy, cx - fh, fy - fv, I["secondary"], "ref", dash=H.DASH_REF))
    o.append(H.line(s, cx, fy, cx - fv * math.tan(lim), fy - fv, O["flag"], "geom", dash=H.DASH_LOA))
    o.append(H.label(s, cx + s(8), fy - fv + s(4), f"{it('F')}{H.sub('v', s, 'label2')}", "label2"))
    o.append(H.label(s, cx - fh - s(4), fy - s(6), f"{it('F')}{H.sub('h', s, 'label2')}", "label2", anchor="end"))
    o.append(H.label(s, cx + s(26), fy - 0.55 * fv, f"friction-cone edge, {it('μ')}{H.sub('avail', s, 'label2')}", "label2",
                     O["flag"]))
    o.append(H.arrow(s, p, cx - s(6), fy + s(24), J["toe"][0] + s(40), fy + s(24), "dim"))
    o.append(H.label(s, cx + s(20), fy + s(42), "foot slides forward", "label2", I["primary"], "middle"))
    vx, vy = J["vertex"]
    R = math.hypot(vx - cx, vy - fy) + s(10)
    a0 = math.degrees(math.atan2(vy - fy, vx - cx))
    o.append(arc_arrow(s, p, cx, fy, R, a0, a0 - 20, "force"))
    ex, ey = cx + R * math.cos(math.radians(a0 - 20)), fy + R * math.sin(math.radians(a0 - 20))
    o.append(H.label(s, ex - s(10), ey + s(20), "falls backward", "label2", O["force"]))
    o.append(H.label(s, 192, 24, "SLIP", anchor="middle"))
    o.append(H.label(s, 192, 42, "the base leaves from under the COM", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 192, fy + s(66), f"{it('μ')}{H.sub('req', s, 'label2')} = |{it('F')}{H.sub('h', s, 'label2')}|/"
                     f"{it('F')}{H.sub('v', s, 'label2')} = {MU_REQ:.2f} > {it('μ')}{H.sub('avail', s, 'label2')} = "
                     f"{MU_ICE:.2f} (ice, assumed)", "label2", O["force"], "middle"))
    o.append(H.label(s, 192, fy + s(84), "so the foot slides; the arrows show the ratio, not a scale", "label2",
                     I["secondary"], "middle"))
    # ---- trip: the swing foot meets a block, the body pitches forward about it
    trip = LB.pose(pelvis=6, trunk=4, near=dict(hip=45, knee=50, contact=None, ankle=-10, shoulder=-20, elbow=20),
                   far=dict(hip=6, knee=0, shoulder=25, elbow=20), anchor=("heel", "far"))
    body, J = LB.draw(p, s, trip, 470.0, fy, hgt)
    com = J["com"]
    bw, bh = 16.0, 11.0
    bx = J["toe"][0] + 3.0
    o += [body]
    o.append(box(s, bx, fy - bh, bw, bh, fill=I["rule"], stroke=I["secondary"]))
    o.append(box(s, J["heel_far"][0], fy + s(2), J["toe_far"][0] - J["heel_far"][0], s(7)))
    o.append(vline(s, com[0], com[1], fy))
    o.append(H.com_mark(s, *com))
    o.append(H.arrow(s, p, com[0] + s(12), com[1], com[0] + s(70), com[1], "geometry"))
    o.append(H.label(s, com[0] + s(74), com[1] + s(5), f"{it('v')} = {V_WALK} m/s", "label2", O["geometry"]))
    bc = (bx, fy - bh)                                           # pivot: the top-left corner of the block
    R = math.hypot(com[0] - bc[0], com[1] - bc[1]) + s(20)
    a0 = math.degrees(math.atan2(com[1] - bc[1], com[0] - bc[0]))
    o.append(arc_arrow(s, p, bc[0], bc[1], R, a0, a0 + 24, "force"))
    ex, ey = bc[0] + R * math.cos(math.radians(a0 + 24)), bc[1] + R * math.sin(math.radians(a0 + 24))
    o.append(H.label(s, ex + s(8), ey - s(4), "pitches forward:", "label2", O["force"]))
    o.append(H.label(s, ex + s(8), ey + s(13), f"{it('H')} = {it('m')}{it('v')}ℓ about the block", "label2", O["force"]))
    ly = J["heel_far"][0] - s(16)
    o.append(dline(s, ly - s(4), com[1], com[0] - s(8), com[1], I["secondary"], "leader"))
    o.append(dline(s, ly - s(4), bc[1], bc[0], bc[1], I["secondary"], "leader"))
    o.append(H.arrow(s, p, ly, bc[1], ly, com[1], "dim", both=True))
    o.append(H.label(s, ly - s(6), (fy + com[1]) / 2, "ℓ", "label", I["primary"], "end"))
    o.append(leader(s, bx + bw / 2, fy - bh - s(4), bx + s(30), fy - s(50)))
    o.append(H.label(s, bx + s(34), fy - s(52), "obstacle", "label2", I["primary"]))
    dxi = V_WALK / W0
    xs = com[0] + k * dxi
    yd = fy + s(26)
    o.append(H.arrow(s, p, com[0] + s(8), yd, xs - s(10), yd, "dim"))
    o.append(xi_mark(s, xs, fy))
    o.append(H.label(s, xs + s(10), fy - s(10), "ξ", "label", I["primary"]))
    o.append(H.label(s, 572, 24, "TRIP", anchor="middle"))
    o.append(H.label(s, 572, 42, "the foot stops, the body keeps moving", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 572, fy + s(66), f"Δξ = {it('v')}/ω₀ = {V_WALK}/{W0:.1f} = {dxi:.2f} m: ξ jumps past the block",
                     "label2", O["force"], "middle"))
    o.append(H.label(s, 572, fy + s(84), "early swing: elevate; late swing: lower, step with the other leg",
                     "label2", I["secondary"], "middle"))
    o.append(LB.credit(s, 12, 452, width=736))
    aria = ("Left, a slip: a skeleton at heel strike with the lead foot sliding forward and the body falling backward, "
            "the centre of mass dropping to the floor behind the sliding foot. At the heel the ground reaction has a "
            "vertical part and a backward horizontal part; the required friction ratio of 0.20 exceeds the 0.08 "
            "available on ice, so the foot slides. Right, a trip: a skeleton whose swing foot meets a block while "
            "the body, moving forward at 1.4 metres per second, pitches forward about the block with angular "
            "momentum m v l; the extrapolated centre of mass jumps forward by 0.45 metres, past the block, so a "
            "capture step is required.")
    return finish(VB, aria, s, o)


FIGS = {
    2: ("Standing balance: Winter body, COM, base of support, and cap", fig2),
    3: ("Two standing figures taking a horizontal push. On the left a", fig3),
    4: ("A standing body over its base of support. A dashed line drop", fig4),
    6: ("A standing body with four labelled sensor sites. The inner-e", fig6),
    10: ("Three standing figures forming a recovery ladder. On the lef", fig10),
    11: ("Left, a slip: the stance foot slides forward while the body", fig11),
}
