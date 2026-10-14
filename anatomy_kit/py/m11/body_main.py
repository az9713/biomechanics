"""Module 11 whole-body figures (main text). Exposes the Lynch body kit once per page.

svg #2 (Fig. 1 shoulder and arm bones), #3 (Fig. 2 arm chain), #4 (Fig. 3 forward kinematics), #5 (Fig. 4 Jacobian),
#6 (Fig. 5 two elbows and the workspace), #7 (Fig. 6 force-torque duality), #8 (Fig. 7 redundancy),
#10 (Fig. 9 concavity-compression), #11 (Fig. 10 pinch and friction cone), #14 (Lab A reach, slider), #20 (Lab D ellipses).
Seated figures: the kit's lateral skeleton, thighs horizontal, shanks vertical; the module's angles (theta1 from +x,
theta2 relative, + = flexion) map to the kit as shoulder flexion theta1 + 90 deg and elbow flexion theta2.

Numbers (module11.html line numbers):
  planar two-link arm l1 = 0.30 m, l2 = 0.45 m (Definition 1 line 104, Appendix lines 642-643), stature 1.75 m (course
  reference; the text states none); workspace annulus 0.15 to 0.75 m (line 116); IK, Prop 3.1 (line 147);
  Jacobian and det J = l1 l2 sin th2 (131); statics: cup m = 0.4 kg, W = mg = 3.9 N (173); alpha = 25 deg, tan alpha =
  0.47 (232); pinch: m = 0.5 kg, W = 4.9 N, mu = 0.5 dry, 0.2 wet, F_g >= W / 2 mu (252); Lab A (283-324): start
  (0.10, -0.30), goal (0.45, 0.10), elbow-up sweeps 62.8 / 36.6 deg, elbow-down shoulder 109.1 deg; Lab D (404-434):
  th1 = 30 deg, th2 = 0.3, pi/2, 2.6 rad, w = l1 l2 |sin th2| = 0.040, 0.135, 0.070.
Arm proportions: the text says its lengths "follow the Winter segment proportions used for the figures" (line 639) and
  states l1 = 0.30, l2 = 0.45 m.  Figures that use those two numbers draw the kit arm with its upper-arm art stretched
  along its axis to 0.30 m (x0.912) and forearm + hand to 0.45 m (x1.016); #3 and #8 keep the kit's own Winter lengths.
Body art: lynch_body.py (Patrick J. Lynch, CC BY 2.5), the Module 3 shoulder crop of the same Lynch art (#2, #10):
  SHARED_DEFS embeds the crop once as #m3art_shoulder; #2, #10 (here) and #27, #37 (other groups) show a window of it.
Fig. 7 (#8): the text gives no lengths for the three-link arm of Section 5 (the Appendix gives 0.25 m for K5 and K7 only),
  so #8 uses the kit's Winter lengths.
"""
import math

import numpy as np

import house as H
import lynch_body as LB
from m03.joints import HUM_C, Place, angle_arc, cone, credit_lynch, head_outline, lead, lynch
from m05.body import art_image, finish, it, wrap
from m05.plots_prob import Plot, hov, label as plabel, legend



def SHARED_DEFS():  # noqa: N802 (apply_figs calls this name)
    """The Lynch body kit once, and the Module 3 shoulder crop once (#m3art_shoulder; #2, #10, #27, #37 show a window of it)."""
    from m03.joints import ART
    f, bx = ART["shoulder"]
    return LB.SHARED_DEFS() + f'<g id="m3art_shoulder">{art_image("<svg>" + f() + "</svg>", bx)}</g>'

O, I, T = H.OVERLAY, H.INK, H.TISSUE
BOXFILL, GRID = "#f7f4ef", "#e6e6e6"
BODY = H.MAX_DISPLAY_H_BODY

# ---------------------------------------------------------------- module constants (line numbers in the docstring)
HM = 1.75                                     # m, stature
L1, L2 = 0.30, 0.45                           # m, upper arm and forearm + hand
UM = LB.H_U / HM                              # body units per metre
K1 = L1 * UM / LB.L_UPPER                     # axial stretch of the upper-arm art (0.912)
K2 = L2 * UM / (LB.L_FORE + LB.L_HAND)        # axial stretch of forearm and hand art (1.016)
assert round(K1, 3) == 0.912 and round(K2, 3) == 1.016, (K1, K2)
SIT = dict(hip=90, knee=90)


# ---------------------------------------------------------------- geometry of the module's arm (math frame: x forward, y up)
def fk(t1, t2, l1=L1, l2=L2):
    """Proposition 1.1 (line 111): elbow and hand, metres from the shoulder; angles in degrees."""
    a, b = math.radians(t1), math.radians(t1 + t2)
    return (l1 * math.cos(a), l1 * math.sin(a)), (l1 * math.cos(a) + l2 * math.cos(b), l1 * math.sin(a) + l2 * math.sin(b))


def ik(x, y, up=False, l1=L1, l2=L2):
    """Proposition 3.1 (line 147): (theta1, theta2) in degrees; up=True is the elbow-up branch (theta2 < 0)."""
    c2 = (x * x + y * y - l1 * l1 - l2 * l2) / (2 * l1 * l2)
    t2 = (-1 if up else 1) * math.acos(max(-1.0, min(1.0, c2)))
    t1 = math.atan2(y, x) - math.atan2(l2 * math.sin(t2), l1 + l2 * math.cos(t2))
    return math.degrees(t1), math.degrees(t2)


def jac(t1, t2, l1=L1, l2=L2):
    """Proposition 2.1 (line 131); angles in radians."""
    s1, s12, c1, c12 = math.sin(t1), math.sin(t1 + t2), math.cos(t1), math.cos(t1 + t2)
    return np.array([[-l1 * s1 - l2 * s12, -l2 * s12], [l1 * c1 + l2 * c12, l2 * c12]])


# ---------------------------------------------------------------- the posed body
def arm_pose(P, t1, t2, t3=0.0, scaled=True):
    """Set the near arm of the lateral Pose P to the module's angles (degrees; t1 from +x, counter-clockwise; t2 the
    elbow relative to the upper arm, + = flexion; t3 the wrist relative to the forearm) and return P.  scaled=True
    stretches the art to l1 = 0.30 m, l2 = 0.45 m."""
    sh = P.j["shoulder"]
    k1, kf = (K1, K2) if scaled else (1.0, 1.0)
    thu = -(t1 + 90.0)
    thf, thw = thu - t2, thu - t2 - t3
    el = LB.add(sh, LB.rot((0.0, LB.L_UPPER * k1), thu))
    wr = LB.add(el, LB.rot((0.0, LB.L_FORE * kf), thf))
    ft = LB.add(wr, LB.rot((0.0, LB.L_HAND * kf), thw))
    P.j["elbow"], P.j["wrist"], P.j["fingertip"] = el, wr, ft
    segs = [q for q in P.segs if not (q[0].startswith("arm_") and not q[5])]
    segs += [("arm_upper", sh, thu, (1, k1), False, False), ("arm_hand", wr, thw, (1, kf), False, False),
             ("arm_fore", el, thf, (1, kf), False, False)]
    P.segs = segs
    return P


def seated(t1, t2, t3=0.0, scaled=True):
    """Seated lateral pose (thighs horizontal, shanks vertical, feet flat) with the near arm at the module's angles."""
    return arm_pose(LB.pose(near=dict(SIT), far=dict(SIT)), t1, t2, t3, scaled)


def put(s, P, hgt, shoulder_xy):
    """Draw P at stature hgt so that its near shoulder lands on shoulder_xy. Returns (svg, J, origin)."""
    _, J0 = LB.draw("", s, P, 0.0, 0.0, hgt)
    org = (shoulder_xy[0] - J0["shoulder"][0], shoulder_xy[1] - J0["shoulder"][1])
    sv, J = LB.draw("", s, P, org[0], org[1], hgt)
    return sv, J, org


def only_arm(P):
    """A copy of P that draws only the near arm (a ghost posture or a floating arm)."""
    P2 = LB.Pose(P.view)
    P2.segs = [q for q in P.segs if q[0].startswith("arm_") and not q[5]]
    P2.j, P2.com, P2.anchor, P2.floor_y = P.j, P.com, P.anchor, P.floor_y
    return P2


def no_near_arm(P):
    """A copy of P without its near arm (the body that a separately drawn arm belongs to)."""
    P2 = LB.Pose(P.view)
    P2.segs = [q for q in P.segs if not (q[0].startswith("arm_") and not q[5])]
    P2.j, P2.com, P2.anchor, P2.floor_y = P.j, P.com, P.anchor, P.floor_y
    return P2


def arm_svg(s, P, org, hgt, op=1.0):
    """The near arm of P alone, drawn at the origin that put() returned; op < 1 makes it a faint ghost."""
    sv, J = LB.draw("", s, only_arm(P), org[0], org[1], hgt)
    return (sv if op >= 1 else f'<g opacity="{op}">{sv}</g>'), J


def stool(s, J, span=(-0.16, 0.20)):
    """Seat and two legs under the hip: a schematic stool (design value), not anatomy."""
    hx, hy = J["hip"]
    h = J["floor_y"] - J["vertex"][1]
    y = hy + 0.075 * h
    xa, xb = hx + span[0] * h, hx + span[1] * h
    o = [H.line(s, xa, y, xb, y, I["rule"], "axis", extra='stroke-linecap="round"')]
    for xx in (xa + (xb - xa) * 0.06, xa + (xb - xa) * 0.94):
        o.append(H.line(s, xx, y, xx, J["floor_y"], I["rule"], "axis"))
    return "".join(o)


# ---------------------------------------------------------------- small drawing helpers
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


def dline(s, x1, y1, x2, y2, col=None, w="ref", dash=H.DASH_REF):
    """Dashed reference line with a white under-stroke so it reads over the art."""
    return white_under(s, x1, y1, x2, y2) + H.line(s, x1, y1, x2, y2, col or O["dim"], w, dash=dash)


def leader(s, x1, y1, x2, y2, col=None):
    return H.line(s, x1, y1, x2, y2, col or I["secondary"], "leader")


def floor_line(s, x0, x1, y):
    return H.line(s, x0, y, x1, y, I["axis"], "axis")


def dot(s, x, y, col=None, r=3.5):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{col or I["primary"]}" stroke="#fff" '
            f'stroke-width="{s(1.2):.2f}"/>')


def ring(s, x, y, col, r=6.0):
    """Open mark (target, special point): white-backed ring."""
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="none" stroke="#fff" stroke-width="{s(4.2):.2f}"/>'
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="none" stroke="{col}" stroke-width="{s(2.0):.2f}"/>')


def lines(s, x, y, rows, size="label2", fill=None, anchor="start", dy=None):
    dy = dy or s(H.PX[size] * 1.3)
    return "".join(H.label(s, x, y + i * dy, t, size, fill or I["primary"], anchor) for i, t in enumerate(rows))


def swatch(s, x, y, col, dash=None, w="curve_multi"):
    """Short line mark that carries identity beside an ink label."""
    return H.line(s, x, y, x + s(20), y, col, w, dash)


def arc_pts(cx, cy, r, a0, a1, n=24):
    """Screen angles in degrees: 0 = +x, + = clockwise (y down)."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def arc_arrow(s, p, cx, cy, r, a0, a1, meaning, both=False, head=True):
    w = {"geometry": "geom", "dim": "ref"}.get(meaning, "force")
    ms = f' marker-start="url(#{p}a_{meaning})"' if both else ""
    me = f' marker-end="url(#{p}a_{meaning})"' if head else ""
    return (f'<path d="{path_d(arc_pts(cx, cy, r, a0, a1))}" fill="none" stroke="{O[meaning]}" '
            f'stroke-width="{s(H.PX[w]):.2f}"{me}{ms}/>')


def pol(c, r, deg):
    return (c[0] + r * math.cos(math.radians(deg)), c[1] + r * math.sin(math.radians(deg)))


def math_xy(sh, km, v):
    """Metres (x forward, y up) from the shoulder -> figure units."""
    return sh[0] + km * v[0], sh[1] - km * v[1]


def sc_ang(t):
    """Math angle (deg, counter-clockwise) -> screen angle (deg, clockwise)."""
    return -t


def th(n):
    return "θ" + {1: "₁", 2: "₂", 3: "₃"}[n]


# ================================================================ svg #3  Fig. 2 the arm as a serial chain (Winter lengths)
def dim_link(s, p, a, b, side, d, text, anchor="middle", dx=0.0, dy=0.0, col="geometry"):
    """Dimension line parallel to the link a-b, offset d user units to `side` (+1 = left of travel on screen)."""
    vx, vy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(vx, vy)
    nx, ny = side * vy / L, -side * vx / L
    a2, b2 = (a[0] + nx * d, a[1] + ny * d), (b[0] + nx * d, b[1] + ny * d)
    o = [H.arrow(s, p, a2[0], a2[1], b2[0], b2[1], col, both=True),
         H.line(s, a[0] + nx * d * 0.35, a[1] + ny * d * 0.35, a2[0] + nx * s(5), a2[1] + ny * s(5), O[col], "leader"),
         H.line(s, b[0] + nx * d * 0.35, b[1] + ny * d * 0.35, b2[0] + nx * s(5), b2[1] + ny * s(5), O[col], "leader")]
    rows = [text] if isinstance(text, str) else list(text)
    for i, tx_ in enumerate(rows):
        off = s(10) + s(16) * (len(rows) - 1 - i)
        m = ((a2[0] + b2[0]) / 2 + nx * off + dx, (a2[1] + b2[1]) / 2 + ny * off + dy)
        o.append(H.label(s, m[0], m[1] + s(4), tx_, "label2", I["primary"], anchor))
    return "".join(o)


def fig3():
    p = "m11f3_"
    hgt, fy = 520.0, 560.0
    VB = (0, 0, 760, 625)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    t1, t2 = -20.0, 30.0                                        # design values: reaching forward, a little down
    P = arm_pose(LB.pose(), t1, t2, 0.0, scaled=False)
    body, J = LB.draw("", s, P, 130.0, fy, hgt)
    sh, el, wr, ft = J["shoulder"], J["elbow"], J["wrist"], J["fingertip"]
    o = [defs(p, s), floor_line(s, 20, 740, fy), body]
    for a_, b_ in ((sh, el), (el, wr), (wr, ft)):
        o.append(H.line(s, a_[0], a_[1], b_[0], b_[1], O["geometry"], "geom"))
    for q in (sh, el, wr):
        o.append(H.joint_centre(s, *q))
    o.append(dot(s, ft[0], ft[1], I["primary"], 4.5))
    # dimension lines above the three links, each with its length as a fraction of stature H
    o.append(dim_link(s, p, sh, el, +1, s(28), ["upper arm", "0.188 H"], dy=s(-2)))
    o.append(dim_link(s, p, el, wr, +1, s(28), ["forearm", "0.145 H"], dy=s(-2)))
    o.append(dim_link(s, p, wr, ft, +1, s(28), ["hand", "0.108 H"], dy=s(-2)))
    vx = J["vertex"][0] - 0.16 * hgt
    o.append(H.arrow(s, p, vx, fy, vx, J["vertex"][1], "dim", both=True))
    o.append(H.line(s, vx - s(5), J["vertex"][1], vx + s(5), J["vertex"][1], O["dim"], "leader"))
    o.append(H.label(s, vx - s(8), (fy + J["vertex"][1]) / 2, "stature H", "label2", I["primary"], "end"))
    # joint names under the arm
    o.append(H.label(s, sh[0] + s(2), sh[1] + s(44), "shoulder", "label2", I["secondary"], "middle"))
    o.append(H.label(s, el[0], el[1] + s(34), "elbow", "label2", I["secondary"], "middle"))
    o.append(H.label(s, wr[0], wr[1] + s(34), "wrist", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ft[0] + s(10), ft[1] + s(5), "fingertip", "label2", I["secondary"]))
    tx = 470.0
    o.append(lines(s, tx, 120, ["The arm is a chain of three rigid links", "joined by three joints.", "",
                                "ℓ₁ = upper arm = 0.188 H", "ℓ₂ = forearm + hand", "     = (0.145 + 0.108) H = 0.253 H"],
                   "label2", I["primary"], dy=s(20)))
    o.append(lines(s, tx, 270, ["Winter (2009) proportions. At H = 1.75 m", "the three links are 0.33 m, 0.25 m", "and 0.19 m (the hand runs from the",
                                "wrist to the middle fingertip)."], "label2", I["secondary"], dy=s(19)))
    o.append(LB.credit(s, 20, VB[3] - 34, width=720))
    aria = ("A standing human skeleton seen from the side, facing right, with the near arm reaching forward and slightly "
            "down. Blue links join the shoulder, elbow, wrist and fingertip. Dimension lines above the links give the "
            "segment lengths as fractions of stature H: upper arm 0.188, forearm 0.145, hand 0.108. A vertical "
            "dimension at the left marks the stature.")
    return finish(VB, aria, s, o)


# ================================================================ svg #4  Fig. 3 forward kinematics
def fig4():
    p = "m11f4_"
    hgt = 520.0
    VB = (0, 0, 760, 545)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    km = hgt / HM
    t1, t2 = -25.0, 60.0                                        # design values: elbow below the shoulder-hand line
    P = seated(t1, t2)
    body, J, org = put(s, P, hgt, (185.0, 172.0))
    sh = J["shoulder"]
    el_m, hd_m = fk(t1, t2)
    el, hd = math_xy(sh, km, el_m), math_xy(sh, km, hd_m)
    assert abs(el[0] - J["elbow"][0]) < 0.5 and abs(hd[1] - J["fingertip"][1]) < 0.5, (el, J["elbow"], hd, J["fingertip"])
    o = [defs(p, s), floor_line(s, 20, 740, J["floor_y"]), stool(s, J), body]
    ax_len = km * 0.80
    o.append(H.line(s, sh[0], sh[1], sh[0] + ax_len, sh[1], I["axis"], "ref", dash=H.DASH_REF))
    o.append(H.arrow(s, p, sh[0] + ax_len * 0.9, sh[1], sh[0] + ax_len, sh[1], "dim"))
    o.append(H.label(s, sh[0] + ax_len + s(6), sh[1] + s(5), it("x"), "label", I["axis"]))
    o.append(H.arrow(s, p, sh[0], sh[1], sh[0], sh[1] - km * 0.40, "dim"))
    o.append(H.label(s, sh[0] + s(6), sh[1] - km * 0.40 - s(2), it("y"), "label", I["axis"]))
    o.append(H.arrow(s, p, sh[0], sh[1], el[0], el[1], "geometry"))
    o.append(H.arrow(s, p, el[0], el[1], hd[0], hd[1], "geometry"))
    r1, r2 = km * 0.15, km * 0.12
    o.append(arc_arrow(s, p, sh[0], sh[1], r1, 0, sc_ang(t1), "geometry"))
    ext = (el[0] + (el[0] - sh[0]) * 0.30, el[1] + (el[1] - sh[1]) * 0.30)
    o.append(dline(s, el[0], el[1], ext[0], ext[1], O["geometry"], "ref"))
    o.append(arc_arrow(s, p, el[0], el[1], r2, sc_ang(t1), sc_ang(t1 + t2), "geometry"))
    m1 = pol(sh, r1 + s(13), sc_ang(t1) / 2)
    o.append(H.label(s, m1[0] + s(2), m1[1] + s(5), th(1), "label", I["primary"]))
    m2 = pol(el, r2 + s(15), sc_ang(t1 + t2 / 2))
    o.append(H.label(s, m2[0], m2[1] + s(4), th(2), "label", I["primary"]))
    o.append(H.label(s, (sh[0] + el[0]) / 2 - s(18), (sh[1] + el[1]) / 2 + s(26), "ℓ₁", "label", I["primary"]))
    o.append(H.label(s, (el[0] + hd[0]) / 2 + s(4), (el[1] + hd[1]) / 2 - s(10), "ℓ₂", "label", I["primary"]))
    o.append(dline(s, hd[0], hd[1], hd[0], sh[1], I["secondary"]))
    o.append(dline(s, hd[0], hd[1], sh[0], hd[1], I["secondary"]))
    o.append(dot(s, hd[0], hd[1], I["primary"], 4.5))
    o.append(H.label(s, hd[0] + s(8), hd[1] - s(8), f"hand ({it('x')}, {it('y')})", "label"))
    o.append(H.label(s, hd[0] + s(7), (hd[1] + sh[1]) / 2 + s(4), it("y"), "label2", I["secondary"]))
    o.append(H.label(s, (hd[0] + sh[0]) / 2 + s(30), hd[1] - s(7), it("x"), "label2", I["secondary"], "middle"))
    o.append(H.joint_centre(s, sh[0], sh[1]))
    o.append(H.joint_centre(s, el[0], el[1]))
    o.append(H.label(s, sh[0] - s(24), sh[1] - s(14), "shoulder", "label2", I["secondary"], "end"))
    o.append(H.label(s, el[0] + s(4), el[1] + s(26), "elbow", "label2", I["secondary"], "middle"))
    x0, y0 = 490.0, 90.0
    o.append(lines(s, x0, y0, ["Definition 1: the planar two-link arm", "origin at the shoulder, " + it("x") + " forward, " + it("y") + " up",
                               "θ₁: upper arm from the " + it("x") + " axis", "θ₂: forearm from the extended upper arm",
                               "θ₂ = 0 is a straight arm"], "label2", I["secondary"], dy=s(19)))
    o.append(lines(s, x0, y0 + s(130), ["Proposition 1.1", it("x") + " = ℓ₁ cos θ₁ + ℓ₂ cos(θ₁ + θ₂)",
                                        it("y") + " = ℓ₁ sin θ₁ + ℓ₂ sin(θ₁ + θ₂)"], "label2", I["primary"], dy=s(19)))
    o.append(LB.credit(s, 20, VB[3] - 34, width=720))
    aria = ("A seated skeleton seen from the side, facing right, reaches forward. The origin of an x-y frame sits at the "
            "shoulder, x forward and y up. Two blue vectors walk out from the shoulder: the upper arm of length l1 at "
            "angle theta1, sloping down from the x axis, and the forearm of length l2 at elbow angle theta2, turned up "
            "from the extended upper arm, ending at the hand at (x, y). The elbow lies below the line from shoulder to "
            "hand. Dashed lines drop from the hand to the two axes.")
    return finish(VB, aria, s, o)


# ================================================================ svg #5  Fig. 4 the Jacobian
KV = 0.5                                                        # figure metres per (m/s) for the J arrows and ellipse


def fig5():
    p = "m11f5_"
    hgt = 500.0
    VB = (0, 0, 760, 600)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    km = hgt / HM
    t1, t2 = -30.0, 90.0                                        # design values: right-angle elbow below the line
    P = seated(t1, t2)
    body, J, org = put(s, P, hgt, (150.0, 245.0))
    sh, el, hd = J["shoulder"], J["elbow"], J["fingertip"]
    Jm = jac(math.radians(t1), math.radians(t2))
    assert abs(np.linalg.det(Jm) - L1 * L2 * math.sin(math.radians(t2))) < 1e-12 and abs(abs(np.linalg.det(Jm)) - 0.135) < 1e-9
    o = [defs(p, s), floor_line(s, 20, 740, J["floor_y"]), stool(s, J), body]
    # the ellipse: the image of the unit joint-rate circle (Definition 2), sampled
    ph = np.linspace(0, 2 * np.pi, 97)
    E = Jm @ np.vstack([np.cos(ph), np.sin(ph)])
    ex = hd[0] + km * KV * E[0]
    ey = hd[1] - km * KV * E[1]
    o.append(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in zip(ex, ey))}" fill="{O["geometry"]}" fill-opacity="0.10" stroke="none"/>')
    o.append(poly(s, list(zip(ex, ey)), O["geometry"], "geom", H.DASH_REF))
    # the columns of J: velocity of the hand for a unit rate of one joint
    for k, meaning in ((0, "geometry"), (1, "flag")):
        tip = (hd[0] + km * KV * Jm[0, k], hd[1] - km * KV * Jm[1, k])
        o.append(white_under(s, hd[0], hd[1], tip[0], tip[1], 5))
        o.append(H.arrow(s, p, hd[0], hd[1], tip[0], tip[1], meaning, w="force"))
    o.append(dot(s, hd[0], hd[1], I["primary"], 4.0))
    # unit rotation of each joint: an anticlockwise arc at the joint, in the colour of its column
    o.append(arc_arrow(s, p, sh[0], sh[1], km * 0.12, 25, -35, "geometry"))
    o.append(arc_arrow(s, p, el[0], el[1], km * 0.10, 75, 15, "flag"))
    o.append(H.joint_centre(s, sh[0], sh[1]))
    o.append(H.joint_centre(s, el[0], el[1]))
    a0 = pol(sh, km * 0.12 + s(14), -5)
    o.append(H.label(s, a0[0], a0[1] + s(5), "θ̇₁ = 1", "label2", I["primary"]))
    a1 = pol(el, km * 0.10 + s(14), 45)
    o.append(H.label(s, a1[0], a1[1] + s(5), "θ̇₂ = 1", "label2", I["primary"]))
    # key, right
    tx, ty = 440.0, 70.0
    o.append(swatch(s, tx, ty - 4, O["geometry"], None, "force"))
    o.append(lines(s, tx + s(28), ty, ["first column of J: hand velocity for", "a unit shoulder rate (both links swing)"],
                   "label2", I["primary"], dy=s(18)))
    ty += s(52)
    o.append(swatch(s, tx, ty - 4, O["flag"], None, "force"))
    o.append(lines(s, tx + s(28), ty, ["second column: hand velocity for a", "unit elbow rate (only the forearm swings)"],
                   "label2", I["primary"], dy=s(18)))
    ty += s(52)
    o.append(swatch(s, tx, ty - 4, O["geometry"], H.DASH_REF, "geom"))
    o.append(lines(s, tx + s(28), ty, ["manipulability ellipse: all unit joint", "rates through J; area ∝ |det J| =", f"ℓ₁ℓ₂|sin θ₂| = {abs(np.linalg.det(Jm)):.3f} m² at θ₂ = 90°"],
                   "label2", I["primary"], dy=s(18)))
    o.append(H.label(s, tx, ty + s(76), f"drawn at {KV} m of figure per m/s", "label2", I["secondary"]))
    o.append(LB.credit(s, 20, VB[3] - 34, width=720))
    aria = ("A seated skeleton seen from the side, facing right, with the arm bent to a right angle at the elbow, the elbow "
            "below the line from shoulder to hand and the forearm pointing up. From the hand two arrows point up and "
            "back: a blue one for the hand velocity of a unit shoulder rate and an orange one for a unit elbow rate. "
            "A dashed blue ellipse at the hand is the manipulability ellipse, the image of every unit joint-rate "
            "combination, with area proportional to the absolute determinant of the Jacobian, 0.135 square metres at "
            "this posture.")
    return finish(VB, aria, s, o)


# ================================================================ svg #6  Fig. 5 two elbows and the workspace
def fig6():
    p = "m11f6_"
    hgt = 460.0
    km = hgt / HM
    R, r0 = (L1 + L2) * km, abs(L1 - L2) * km
    VB = (0, 0, 760, 610)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    cx, cy = 255.0, 250.0
    tgt = (0.65, 0.02)                                          # design value: a target inside the annulus
    rr = math.hypot(*tgt)
    assert abs(L1 - L2) < rr < L1 + L2
    dn, up = ik(*tgt), ik(*tgt, up=True)
    assert abs(dn[1] + up[1]) < 1e-9 and dn[1] > 0
    for q in (dn, up):
        assert abs(fk(*q)[1][0] - tgt[0]) < 1e-9 and abs(fk(*q)[1][1] - tgt[1]) < 1e-9
    P_dn, P_up = seated(*dn), seated(*up)
    body, J, org = put(s, P_dn, hgt, (cx, cy))
    ghost_up, Ju = arm_svg(s, P_up, org, hgt, 0.55)
    o = [defs(p, s)]
    ann = (f'M{cx + R:.2f},{cy:.2f} A{R:.2f},{R:.2f} 0 1 0 {cx - R:.2f},{cy:.2f} A{R:.2f},{R:.2f} 0 1 0 {cx + R:.2f},{cy:.2f} Z '
           f'M{cx + r0:.2f},{cy:.2f} A{r0:.2f},{r0:.2f} 0 1 0 {cx - r0:.2f},{cy:.2f} A{r0:.2f},{r0:.2f} 0 1 0 {cx + r0:.2f},{cy:.2f} Z')
    o.append(f'<path d="{ann}" fill="{O["geometry"]}" fill-opacity="0.07" fill-rule="evenodd" stroke="none"/>')
    dash = f'stroke-dasharray="{s(6):.1f} {s(4):.1f}"'
    for rad in (R, r0):
        o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{rad:.2f}" fill="none" stroke="{O["geometry"]}" '
                 f'stroke-width="{s(1.6):.2f}" {dash}/>')
    o += [floor_line(s, 20, 500, J["floor_y"]), stool(s, J), body, ghost_up]
    tp = math_xy((cx, cy), km, tgt)
    assert abs(tp[0] - J["fingertip"][0]) < 0.5 and abs(tp[0] - Ju["fingertip"][0]) < 0.5
    o.append(ring(s, tp[0], tp[1], O["flag"], 7.0))
    o.append(H.joint_centre(s, cx, cy))
    # labels
    o.append(H.label(s, cx - s(24), cy - s(12), "shoulder", "label2", I["secondary"], "end"))
    eu, ed = Ju["elbow"], J["elbow"]
    o.append(H.label(s, eu[0] + s(6), eu[1] - s(14), "elbow-up", "label2", I["primary"]))
    o.append(H.label(s, ed[0] + s(6), ed[1] + s(24), "elbow-down", "label2", I["primary"]))
    o.append(H.label(s, tp[0] + s(12), tp[1] - s(10), "target", "label2", I["primary"]))
    # the two edges, named on the circles: outer above its top, inner by a leader to the free space behind the back
    o.append(H.label(s, cx, cy - R - s(8), "outer edge: r = ℓ₁ + ℓ₂ = 0.75 m", "label2", I["primary"], "middle"))
    qi = pol((cx, cy), r0, -135)
    o.append(leader(s, qi[0], qi[1], cx - R * 0.62, cy - R * 0.55))
    o.append(H.label(s, cx - R * 0.62 - s(4), cy - R * 0.55 - s(8), "inner edge: r = |ℓ₁ − ℓ₂| = 0.15 m", "label2", I["primary"], "start"))
    tx = 530.0
    o.append(swatch(s, tx, 66, O["geometry"], H.DASH_REF, "geom"))
    o.append(lines(s, tx + s(28), 70, ["workspace: the reachable annulus", "|ℓ₁ − ℓ₂| ≤ r ≤ ℓ₁ + ℓ₂"], "label2", I["primary"], dy=s(18)))
    o.append(ring(s, tx + s(10), 128, O["flag"], 6.0))
    o.append(lines(s, tx + s(28), 132, [f"target ({tgt[0]:.2f}, {tgt[1]:.2f}) m, r = {rr:.3f} m"], "label2", I["primary"]))
    o.append(lines(s, tx, 172, ["solid arm, elbow-down:", f"θ₂ = +{dn[1]:.1f}°, θ₁ = {dn[0]:.1f}°".replace("-", "−")], "label2", I["primary"], dy=s(18)))
    o.append(lines(s, tx, 222, ["faint arm, elbow-up:", f"θ₂ = {up[1]:.1f}°, θ₁ = +{up[0]:.1f}°".replace("-", "−")], "label2", I["primary"], dy=s(18)))
    o.append(lines(s, tx, 272, ["the two signs of θ₂ = ± arccos(·);", "on the outer edge they merge"], "label2", I["secondary"], dy=s(18)))
    o.append(LB.credit(s, 20, VB[3] - 34, width=720))
    aria = ("A seated skeleton seen from the side, facing right, with a large light-blue ring centred on the shoulder: the "
            "reachable workspace, outer radius l1 plus l2 equal to 0.75 metres and a small inner hole of radius 0.15 "
            "metres. An orange ring marks one target inside it. The solid arm reaches it elbow-down, with the elbow "
            "below the line from shoulder to hand; a faint second arm reaches the same target elbow-up, with the "
            "elbow above that line.")
    return finish(VB, aria, s, o)


# ================================================================ svg #7  Fig. 6 force-torque duality
M_CUP = 0.4                                                     # kg, line 173
W_CUP = M_CUP * 9.81


def cup(s, x, y, w, neutral=False):
    """A mug (schematic) with its base centre at (x, y): fluid-blue tissue tokens, or white with an ink outline."""
    h = w * 1.15
    f, ln = ("#ffffff", I["secondary"]) if neutral else T["fluid"]
    handle = "" if neutral else (f'<path d="M{x + w / 2:.2f},{y - h * 0.72:.2f} q{w * 0.45:.2f},{h * 0.02:.2f} {w * 0.04:.2f},{h * 0.42:.2f}" '
                                 f'fill="none" stroke="{ln}" stroke-width="{s(1.6):.2f}"/>')
    return (handle + f'<rect x="{x - w / 2:.2f}" y="{y - h:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{w * 0.08:.2f}" fill="{f}" '
            f'stroke="{ln}" stroke-width="{s(1.2):.2f}"/>')


def fig7():
    p = "m11f7_"
    hgt = 500.0
    VB = (0, 0, 760, 590)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    km = hgt / HM
    t1, t2 = -25.0, 60.0                                        # the posture of #4
    P = seated(t1, t2)
    body, J, org = put(s, P, hgt, (150.0, 175.0))
    sh, el, hd = J["shoulder"], J["elbow"], J["fingertip"]
    em, hm = fk(t1, t2)
    d1, d2 = hm[0], hm[0] - em[0]                               # horizontal moment arms (m)
    F = np.array([0.0, W_CUP])                                  # the hand holds the cup up: F = (0, +mg)
    tau = jac(math.radians(t1), math.radians(t2)).T @ F         # Proposition 4.1
    assert abs(tau[0] - d1 * W_CUP) < 1e-9 and abs(tau[1] - d2 * W_CUP) < 1e-9 and round(W_CUP, 1) == 3.9
    o = [defs(p, s), floor_line(s, 20, 740, J["floor_y"]), stool(s, J), body]
    cw = 0.075 * km
    o.append(cup(s, hd[0], hd[1] + cw * 0.58, cw))
    y1, y2 = sh[1] + 0.50 * km, sh[1] + 0.64 * km               # the two dimension lines
    for x0, y, col in ((sh[0], y1, "geometry"), (el[0], y2, "geometry")):
        o.append(dline(s, x0, (sh[1] if x0 == sh[0] else el[1]), x0, y, O["dim"], "ref"))
    o.append(dline(s, hd[0], hd[1] + cw * 0.5, hd[0], y2 + s(10), O["load"], "ref"))
    o.append(H.arrow(s, p, hd[0], hd[1] + cw * 0.5, hd[0], hd[1] + cw * 0.5 + 0.20 * km, "load", w="force"))
    o.append(H.label(s, hd[0] + s(10), hd[1] + cw * 0.5 + 0.12 * km, f"W = mg = {W_CUP:.1f} N", "label", I["primary"]))
    o.append(H.label(s, hd[0] + s(10), hd[1] + cw * 0.5 + 0.12 * km + s(18), f"(m = {M_CUP} kg)", "label2", I["secondary"]))
    for x0, x1, y, name, val, what in ((sh[0], hd[0], y1, "d₁", d1, "shoulder to the line of W"),
                                       (el[0], hd[0], y2, "d₂", d2, "elbow to the line of W")):
        o.append(H.arrow(s, p, x0, y, x1, y, "geometry", both=True))
        o.append(H.label(s, x1 + s(12), y + s(5), f"{name} = {val:.2f} m  ({what})", "label2", I["primary"]))
    # joint torques the muscles supply (anticlockwise), red force arcs
    o.append(arc_arrow(s, p, sh[0], sh[1], km * 0.13, 30, -40, "force"))
    o.append(arc_arrow(s, p, el[0], el[1], km * 0.11, 30, -50, "force"))
    o.append(H.joint_centre(s, sh[0], sh[1]))
    o.append(H.joint_centre(s, el[0], el[1]))
    a0 = pol(sh, km * 0.13 + s(14), -6)
    o.append(H.label(s, a0[0], a0[1] + s(5), "τ₁", "label", I["primary"]))
    a1 = pol(el, km * 0.11 + s(14), -10)
    o.append(H.label(s, a1[0], a1[1] + s(5), "τ₂", "label", I["primary"]))
    tx = 500.0
    o.append(lines(s, tx, 70, ["τ = Jᵀ F with F = (0, +mg)", "gives τᵢ = W × dᵢ:"], "label2", I["primary"], dy=s(18)))
    o.append(lines(s, tx, 120, [f"τ₁ = {d1:.2f} × {W_CUP:.1f} = {tau[0]:.1f} N·m", f"τ₂ = {d2:.2f} × {W_CUP:.1f} = {tau[1]:.1f} N·m"],
                   "label", I["primary"], dy=s(22)))
    o.append(lines(s, tx, 180, ["the cup alone: the arm's own weight", "adds to both (the worked example in", "Section 4 puts numbers on it)"],
                   "label2", I["secondary"], dy=s(18)))
    o.append(LB.credit(s, 20, VB[3] - 34, width=720))
    aria = ("A seated skeleton seen from the side, facing right, holds a cup at the hand with the arm bent so the elbow lies "
            "below the line from shoulder to hand. A brown arrow marks the cup's weight W equal to 3.9 newtons, "
            "pointing down. Two horizontal blue dimension lines give the moment arms: d1 = 0.64 metres from the "
            "shoulder to the line of W and d2 = 0.37 metres from the elbow to it. Red arcs at the shoulder and elbow "
            "mark the muscle torques tau1 and tau2, equal to W times each moment arm: 2.5 and 1.4 newton metres.")
    return finish(VB, aria, s, o)


# ================================================================ svg #8  Fig. 7 redundancy (three-link arm)
def fig8():
    p = "m11f8_"
    hgt = 600.0
    VB = (0, 0, 760, 690)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    km = hgt / HM
    a1, a2, a3 = LB.L_UPPER / UM, LB.L_FORE / UM, LB.L_HAND / UM     # the kit's Winter link lengths, metres
    tgt = (0.50, 0.15)                                          # design value: the fixed fingertip, in front of the chest
    phis = (15.0, 35.0, 55.0, 75.0, 95.0)                     # hand directions: the one free parameter of the family
    sol = []
    for phi in phis:
        w = (tgt[0] - a3 * math.cos(math.radians(phi)), tgt[1] - a3 * math.sin(math.radians(phi)))
        t1_, t2_ = ik(w[0], w[1], l1=a1, l2=a2)
        sol.append((phi, t1_, t2_, phi - t1_ - t2_))
        assert t2_ > 0 and abs(phi - t1_ - t2_) < 80, (phi, t1_, t2_)
    main = 2
    Pm = seated(*sol[main][1:], scaled=False)
    body, J, org = put(s, Pm, hgt, (150.0, 215.0))
    sh = J["shoulder"]
    tp = math_xy(sh, km, tgt)
    o = [defs(p, s), floor_line(s, 20, 740, J["floor_y"]), stool(s, J)]
    for k, (phi, t1_, t2_, t3_) in enumerate(sol):
        g, Jk = arm_svg(s, seated(t1_, t2_, t3_, scaled=False), org, hgt, 0.32)
        assert abs(Jk["fingertip"][0] - tp[0]) < 0.6 and abs(Jk["fingertip"][1] - tp[1]) < 0.6, (k, Jk["fingertip"], tp)
        if k != main:
            o.append(g)
    o.append(body)
    o.append(ring(s, tp[0], tp[1], O["flag"], 7.0))
    o.append(H.label(s, tp[0] + s(12), tp[1] - s(12), "fingertip target (fixed)", "label"))
    # self-motion: the wrist turns about the fixed fingertip (arc of radius l3 + margin), the elbow follows
    r = a3 * km + s(26)
    pts = [(tp[0] - r * math.cos(math.radians(ph)), tp[1] + r * math.sin(math.radians(ph))) for ph in np.linspace(phis[0], phis[-1], 25)]
    o.append(f'<path d="{path_d(pts)}" fill="none" stroke="{O["geometry"]}" stroke-width="{s(H.PX["geom"]):.2f}" '
             f'marker-end="url(#{p}a_geometry)"/>')
    o.append(H.label(s, tp[0] + s(16), tp[1] + r * 0.9, "self-motion: the hand turns about", "label2", I["primary"]))
    o.append(H.label(s, tp[0] + s(16), tp[1] + r * 0.9 + s(17), "the fixed fingertip; wrist and elbow follow", "label2", I["primary"]))
    o.append(H.joint_centre(s, sh[0], sh[1]))
    o.append(H.label(s, sh[0] - s(24), sh[1] - s(14), "shoulder", "label2", I["secondary"], "end"))
    tx = 500.0
    o.append(lines(s, tx, 66, ["three links, three joints, a", "two-number task: J is 2×3, so", "J q̇ = ṗ is underdetermined"],
                   "label2", I["primary"], dy=s(18)))
    o.append(lines(s, tx, 140, ["each arm is one point of a one-", "parameter family: the hand's direction φ",
                                f"is free ({phis[0]:.0f}° to {phis[-1]:.0f}° above horizontal here;", f"solid arm: φ = {phis[main]:.0f}°)"],
                   "label2", I["secondary"], dy=s(18)))
    o.append(LB.credit(s, 20, VB[3] - 34, width=720))
    aria = ("A seated skeleton seen from the side, facing right, with the arm bent to bring one fingertip to a fixed target in "
            "front of the chest, marked by an orange ring. Five postures are drawn, one solid and four faint. In each the "
            "hand points in a different direction, from forward-up to straight up, and the wrist and elbow are in "
            "different places, but every fingertip lands on the same target. A blue curved arrow around the target is "
            "labelled self-motion.")
    return finish(VB, aria, s, o)


# ================================================================ svg #11  Fig. 10 the pinch and its friction cone
M_GLASS, MU_DRY, MU_WET = 0.5, 0.5, 0.2                          # kg, and friction coefficients, line 252
W_GLASS = M_GLASS * 9.81


def pad(s, x, y, side):
    """A contact patch of skin (tissue token) on the cup wall; side = -1 on the left wall, +1 on the right."""
    f, ln = T["skin"]
    w, h = s(9), s(38)
    return (f'<rect x="{x - w if side < 0 else x:.2f}" y="{y - h / 2:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{w * 0.45:.2f}" '
            f'fill="{f}" stroke="{ln}" stroke-width="{s(1.4):.2f}"/>')


def fig11():
    p = "m11f11_"
    hgt = 430.0
    VB = (0, 0, 760, 520)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    t1, t2 = -30.0, 65.0                                        # design values: the pose of #7, the cup in the hand
    P = seated(t1, t2)
    body, J, org = put(s, P, hgt, (115.0, 190.0))
    hd = J["fingertip"]
    km = hgt / HM
    o = [defs(p, s), floor_line(s, 20, 370, J["floor_y"]), stool(s, J), body]
    cw = 0.07 * km
    o.append(cup(s, hd[0], hd[1] + cw * 0.58, cw))
    bx = (400.0, 50.0, 340.0, 400.0)
    o.append(f'<rect x="{bx[0]}" y="{bx[1]}" width="{bx[2]}" height="{bx[3]}" rx="{s(6):.2f}" fill="{BOXFILL}" stroke="{I["rule"]}" '
             f'stroke-width="{s(1):.2f}"/>')
    o.append(dline(s, hd[0] + cw * 0.6, hd[1], bx[0], hd[1] - 4, I["rule"], "ref"))
    cx, cy = bx[0] + 170.0, 180.0
    D = 130.0
    ch = D * 1.15
    o.append(H.label(s, cx, bx[1] + s(20), "detail: how the pinch holds", "label2", I["secondary"], "middle"))
    o.append(cup(s, cx, cy + ch / 2, D, neutral=True))
    kN = 10.0                                                    # figure units per newton
    phi = math.degrees(math.atan(MU_DRY))
    Fg = W_GLASS / (2 * MU_DRY)                                  # Proposition 8.1 at the dry coefficient
    Ft = W_GLASS / 2
    assert round(Fg, 1) == 4.9 and round(W_GLASS / (2 * MU_WET), 0) == 12.0
    for side, name in ((-1, "thumb pad"), (1, "finger pad")):
        wx = cx + side * D / 2
        L = D * 0.52
        a = [(wx - side * L * math.cos(math.radians(d)), cy + L * math.sin(math.radians(d))) for d in (-phi, phi)]
        o.append(f'<path d="M{wx:.2f},{cy:.2f} L{a[0][0]:.2f},{a[0][1]:.2f} L{a[1][0]:.2f},{a[1][1]:.2f} Z" fill="{O["geometry"]}" '
                 f'fill-opacity="0.12" stroke="none"/>')
        for q in a:
            o.append(dline(s, wx, cy, q[0], q[1], O["geometry"], "ref"))
        o.append(pad(s, wx, cy, side))
        tip = wx - side * kN * Fg                                # grip force inward, then friction up: a force triangle
        o.append(H.arrow(s, p, wx, cy, tip, cy, "force"))
        o.append(H.arrow(s, p, tip, cy, tip, cy - kN * Ft, "force", w="geom"))
        o.append(H.arrow(s, p, wx, cy, tip, cy - kN * Ft, "reaction", w="geom"))
        o.append(H.label(s, wx + side * s(12), cy + s(5), name, "label2", I["secondary"], "end" if side < 0 else "start"))
        o.append(H.label(s, (wx + tip) / 2, cy + s(40), "F" + H.sub("g", s, "label2"), "label2", I["primary"], "middle"))
        o.append(H.label(s, tip - side * s(6), cy - kN * Ft / 2 + s(4), "μF" + H.sub("g", s, "label2"), "label2", I["primary"],
                         "end" if side > 0 else "start"))
    o.append(H.arrow(s, p, cx, cy + s(30), cx, cy + s(30) + kN * W_GLASS, "load"))
    o.append(H.label(s, cx + s(8), cy + s(30) + kN * W_GLASS * 0.5 + s(5), "W", "label2", I["primary"]))
    o.append(H.label(s, cx, cy + ch / 2 + s(22), f"F{H.sub('g', s, 'label2')} = {Fg:.1f} N, W = mg = {W_GLASS:.1f} N (m = {M_GLASS} kg)", "label2", I["primary"], "middle"))
    ty = bx[1] + bx[3] - s(106)
    o.append(lines(s, bx[0] + s(12), ty, ["red: grip force F" + H.sub("g", s, "label2") + " and friction μF" + H.sub("g", s, "label2") + " at each pad", "black: their resultant, on the cone edge",
                                          f"blue cone: half-angle φ = arctan μ = {phi:.1f}° (μ = {MU_DRY})",
                                          "no slip: F" + H.sub("g", s, "label2") + " ≥ W/(2μ)",
                                          f"wet glass, μ = {MU_WET}: F" + H.sub("g", s, "label2") + f" ≥ {W_GLASS / (2 * MU_WET):.0f} N per pad"],
                   "label2", I["primary"], dy=s(19)))
    o.append(LB.credit(s, 20, VB[3] - 34, width=720))
    aria = ("A seated skeleton seen from the side, facing right, holds a cup in a precision pinch at the end of the "
            "forward arm. A dashed line leads to a detail box. In it, a cup is squeezed between a thumb pad on its left "
            "and a finger pad on its right by equal red grip forces F g of 4.9 newtons. At each pad a blue friction "
            "cone of half-angle 26.6 degrees opens toward the other pad; a red upward friction arrow and a black "
            "resultant along the cone edge show the grip at the verge of slipping. A brown arrow marks the weight "
            "of 4.9 newtons.")
    return finish(VB, aria, s, o)


# ================================================================ svg #14  Lab A: a straight reach, joint angles on the elbow-up branch
START, GOAL = np.array([0.10, -0.30]), np.array([0.45, 0.10])     # line 283
NS = 60                                                            # path samples, as the lab script
NF = 11                                                            # slider frames (steps of 0.1)
S_DEF = 5                                                          # default frame: the middle of the reach


def reach_branch(up=True, n=NS):
    sv = np.linspace(0.0, 1.0, n)
    path = (1 - sv)[:, None] * START + sv[:, None] * GOAL
    q = np.array([ik(x, y, up=up) for x, y in path])
    return sv, path, q


def fig14():
    p = "m11f14_"
    hgt = 450.0
    VB = (0, 0, 760, 510)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    km = hgt / HM
    sv, path, q = reach_branch(True)
    sw1, sw2 = np.ptp(q[:, 0]), np.ptp(q[:, 1])
    assert (round(sw1, 1), round(sw2, 1)) == (62.8, 36.6), (sw1, sw2)                  # line 324
    assert round(np.ptp(reach_branch(False)[2][:, 0]), 1) == 109.1                       # line 324
    Pg = seated(*q[-1])
    body, J, org = put(s, no_near_arm(Pg), hgt, (125.0, 185.0))
    sh = J["shoulder"]
    o = [defs(p, s), floor_line(s, 20, 400, J["floor_y"]), stool(s, J), body]
    M = lambda v: math_xy(sh, km, v)                             # noqa: E731
    pa, pb = M(START), M(GOAL)
    for k in (0, NS - 1):
        g, Jg = arm_svg(s, seated(*q[k]), org, hgt, 0.30)
        o.append(g + f'<g opacity="0.55">{poly(s, [Jg["shoulder"], Jg["elbow"], Jg["fingertip"]], O["geometry"], "geom")}</g>')
    o.append(dline(s, pa[0], pa[1], pb[0], pb[1], O["flag"], "force", H.DASH_REF))
    o.append(dot(s, pa[0], pa[1], O["flag"], 4.5))
    o.append(ring(s, pb[0], pb[1], O["flag"], 6.5))
    o.append(H.label(s, pa[0] + s(10), pa[1] + s(18), "start (lap)", "label2", I["primary"]))
    o.append(H.label(s, pb[0] + s(12), pb[1] - s(10), "goal (cup)", "label2", I["primary"]))
    o.append(H.label(s, (pa[0] + pb[0]) / 2 + s(22), (pa[1] + pb[1]) / 2, "hand path", "label2", I["primary"]))
    o.append(H.label(s, sh[0] - s(24), sh[1] - s(14), "shoulder", "label2", I["secondary"], "end"))
    o.append(H.label(s, 20, 30, "elbow-up branch: both faint arms and", "label2", I["secondary"]))
    o.append(H.label(s, 20, 47, "the moving arm are drawn at θ₂ < 0", "label2", I["secondary"]))
    Pl = Plot(s, (480, 90, 738, 340), (0, 1), (-150, 100))
    o.append(Pl.axes([(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1)], [(v, f"{v:g}".replace("-", "−")) for v in (-150, -100, -50, 0, 50, 100)],
                     "reach fraction", "joint angle (deg)", grid=(-100, -50, 50, 100), ytx=438))
    o.append(H.line(s, Pl.x0, Pl.Y(0), Pl.x1, Pl.Y(0), I["rule"], "ref"))
    o.append(Pl.curve(sv, q[:, 0], H.SERIES[0], multi=True))
    o.append(Pl.curve(sv, q[:, 1], H.SERIES[1], multi=True))
    o.append(legend(s, 480, 30, [(H.SERIES[0], f"shoulder θ₁, sweep {sw1:.1f}°", None)]))
    o.append(legend(s, 480, 50, [(H.SERIES[1], f"elbow θ₂, sweep {sw2:.1f}°", None)]))
    j = int(np.argmax(q[:, 0]))
    o.append(plabel(s, Pl.X(0.80), Pl.Y(q[j, 0]) - s(12), f"θ₁ max {q[j, 0]:.0f}°", "label2", I["primary"], "middle"))
    k2 = int(np.argmin(q[:, 1]))
    o.append(plabel(s, Pl.X(0.16), Pl.Y(q[k2, 1]) - s(14), f"θ₂ min {q[k2, 1]:.0f}°".replace("-", "−"), "label2", I["primary"], "middle"))
    fs = np.linspace(0, 1, NF)
    frames = []
    for k, sf in enumerate(fs):
        x, y = START + sf * (GOAL - START)
        t1_, t2_ = ik(x, y, up=True)
        g, Jk = arm_svg(s, seated(t1_, t2_), org, hgt, 1.0)
        hp = M((x, y))
        assert abs(Jk["fingertip"][0] - hp[0]) < 0.6 and abs(Jk["fingertip"][1] - hp[1]) < 0.6
        body_k = (g + poly(s, [Jk["shoulder"], Jk["elbow"], Jk["fingertip"]], O["geometry"], "geom")
                  + H.joint_centre(s, *Jk["elbow"]) + dot(s, hp[0], hp[1], I["primary"], 4.0)
                  + H.line(s, Pl.X(sf), Pl.y1, Pl.X(sf), Pl.y0, I["rule"], "leader")
                  + dot(s, Pl.X(sf), Pl.Y(t1_), H.SERIES[0], 4.0) + dot(s, Pl.X(sf), Pl.Y(t2_), H.SERIES[1], 4.0))
        frames.append(H.frame(k, S_DEF, body_k))
    o += frames
    o.append(LB.credit(s, 20, VB[3] - 34, width=720))
    hvp = hov(Pl, sv, [q[:, 0], q[:, 1]], lambda i: f"reach {sv[i]:.2f}: shoulder θ₁ = {q[i, 0]:.1f}°, elbow θ₂ = {q[i, 1]:.1f}°".replace("-", "−"))
    aria = ("Left: a seated skeleton seen from the side, facing right, with two faint arms at the start and goal of a reach "
            "and one solid arm that a slider moves between them. The hand moves along a straight orange dashed path from "
            "the lap to a cup. Right: the shoulder angle rises from 22 to 85 degrees and falls to 81, a sweep of 62.8 "
            "degrees, and the elbow angle runs from minus 135 down to minus 144 and back to minus 107, a sweep of 36.6 "
            "degrees. Neither is a straight line, although the hand moves at constant speed.")
    extra = H.hover_attr(Pl.box, hvp) + " " + H.frames_attr("reach fraction", [f"{v:.2f}" for v in fs], S_DEF)
    return finish(VB, aria, s, o, extra)


# ================================================================ svg #20  Lab D: velocity and force ellipses at three elbow angles
KE = 0.3                                                         # figure metres per (m/s) for the velocity ellipse


def fig20():
    p = "m11f20_"
    VB = (0, 0, 760, 430)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    hgt = 420.0
    km = hgt / HM
    t1 = 30.0
    cases = [(0.3, "θ₂ = 0.3 rad (near straight)"), (math.pi / 2, "θ₂ = π/2 (best)"), (2.6, "θ₂ = 2.6 rad (near folded)")]
    wref = [0.040, 0.135, 0.070]
    o = [defs(p, s)]
    phi = np.linspace(0, 2 * np.pi, 101)
    circ = np.vstack([np.cos(phi), np.sin(phi)])
    R90 = np.array([[0.0, -1.0], [1.0, 0.0]])
    for (t2r, name), x0, wr_ in zip(cases, (110.0, 365.0, 625.0), wref):
        J = jac(math.radians(t1), t2r)
        w = abs(np.linalg.det(J))
        assert abs(w - L1 * L2 * abs(math.sin(t2r))) < 1e-12 and round(w, 3) == wr_, (w, wr_)    # line 434
        vel = J @ circ                                           # the image of the unit joint-rate circle (line 423)
        frc = np.linalg.inv(J).T @ circ                          # the image under J^-T (line 424)
        # in 2 dimensions J^-T = R J R^T / det J, so w * (force ellipse) is the velocity ellipse turned by 90 degrees
        assert np.allclose(w * frc, np.sign(np.linalg.det(J)) * R90 @ J @ R90.T @ circ, atol=1e-9)
        P = seated(t1, math.degrees(t2r))
        sh = (x0 - 40.0, 285.0)
        g, Jp, org = put(s, only_arm(P), hgt, sh)
        o.append(g)
        hd = Jp["fingertip"]
        ve = list(zip(hd[0] + km * KE * vel[0], hd[1] - km * KE * vel[1]))
        fe = list(zip(hd[0] + km * KE * w * frc[0], hd[1] - km * KE * w * frc[1]))
        o.append(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in ve)}" fill="{O["geometry"]}" fill-opacity="0.10" stroke="none"/>')
        o.append(poly(s, ve, O["geometry"], "curve"))
        o.append(poly(s, fe, O["force"], "curve", H.DASH_REF))
        o.append(dot(s, hd[0], hd[1], I["primary"], 3.5))
        o.append(H.joint_centre(s, *sh))
        o.append(H.label(s, x0 - 8, 345, name, "label", I["primary"], "middle"))
        o.append(H.label(s, x0 - 8, 365, f"w = ℓ₁ℓ₂|sin θ₂| = {w:.3f} m²", "label2", I["primary"], "middle"))
    ty = 24.0
    o.append(swatch(s, 150, ty - 4, O["geometry"], None, "curve"))
    o.append(H.label(s, 150 + s(28), ty, "velocity ellipse: how easily the hand MOVES", "label", I["primary"]))
    o.append(swatch(s, 150, ty + 20 - 4, O["force"], H.DASH_REF, "curve"))
    o.append(H.label(s, 150 + s(28), ty + 20, "force ellipse (rescaled by w, turned 90°): how strongly it PUSHES", "label", I["primary"]))
    o.append(H.label(s, 150, ty + 42, f"θ₁ = {t1:.0f}°; velocity ellipse drawn at {KE} m of figure per m/s; the shoulder is marked", "label2", I["secondary"]))
    o.append(LB.credit(s, 20, VB[3] - 34, width=720))
    aria = ("Three side views of the right arm, floating without a body, at the same shoulder angle of 30 degrees and three "
            "elbow angles. At each hand a solid blue velocity ellipse and a dashed red force ellipse are drawn. Near "
            "straight, 0.3 radians, the velocity ellipse is a thin diagonal sliver; at a right-angle elbow it is fattest, "
            "with manipulability 0.135 square metres; near folded, 2.6 radians, it is a narrow ellipse again. At every "
            "posture the force ellipse is the velocity ellipse turned by 90 degrees.")
    return finish(VB, aria, s, o)


# ================================================================ svg #2  Fig. 1 the shoulder and the arm bones
SH_WIN = (650, 1420, 1300, 2100)                                  # the m03 shoulder crop window (Lynch anterior view), art units


def fig2():
    p = "m11f2_"
    VB = (0, 0, 760, 490)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    o = [defs(p, s)]
    # ---- left: the left shoulder, front view (Lynch crop), with the humeral head outlined
    pl = Place((650.0, 1420.0), (10.0, 52.0), 0.46)
    o.append(pl.image("shoulder", SH_WIN, p))
    c, r = pl(HUM_C[:2]), HUM_C[2] * pl.k
    o.append(head_outline(s, c, r))
    o.append(H.joint_centre(s, *c))
    for q, txt in (((705.0, 1478.0), "clavicle"), ((905.0, 1558.0), "acromion"), ((655.0, 1600.0), "coracoid"),
                   ((838.0, 1655.0), "humeral head"), ((690.0, 1880.0), "scapula"), ((970.0, 1960.0), "humerus")):
        a_ = pl(q)
        o.append(H.label(s, a_[0], a_[1], txt, "label2", I["primary"]))
    g = pl((835.0, 1775.0))
    o.append(lead(s, g[0] - s(3), g[1], 40, 376, I["secondary"]))
    o.append(H.label(s, 8, 392, "glenoid: a shallow dish on the", "label2", I["primary"]))
    o.append(H.label(s, 8, 409, "scapula that cups only part", "label2", I["primary"]))
    o.append(H.label(s, 8, 426, "of the humeral head", "label2", I["primary"]))
    o.append(H.label(s, 10, 34, "the shoulder: mobility from a shallow socket", "label", I["primary"]))
    # ---- right: the anterior-view arm bones, drawn with the two links of the chain
    Pa = LB.pose_ant(**LB.POSES_ANT["standing"])
    Pa2 = LB.Pose(Pa.view)
    Pa2.segs = [q for q in Pa.segs if q[0].startswith("arm_")]
    Pa2.j, Pa2.com, Pa2.anchor, Pa2.floor_y = Pa.j, Pa.com, Pa.anchor, Pa.floor_y
    hgt = 640.0
    _, J0 = LB.draw(p, s, Pa2, 0.0, 0.0, hgt)
    ox, oy = 440.0 - 0.5 * (J0["shoulder_l"][0] + J0["shoulder_r"][0]), 96.0 - J0["shoulder_l"][1]
    arms, J = LB.draw(p, s, Pa2, ox, oy, hgt)
    o.append(arms)
    sh, el, ft = J["shoulder_l"], J["elbow_l"], J["fingertip_l"]
    o.append(H.line(s, sh[0], sh[1], el[0], el[1], O["geometry"], "geom"))
    o.append(H.line(s, el[0], el[1], ft[0], ft[1], O["geometry"], "geom"))
    o.append(H.joint_centre(s, *sh))
    o.append(H.joint_centre(s, *el))
    o.append(dot(s, ft[0], ft[1], I["primary"], 4.0))
    lx = max(sh[0], el[0], ft[0]) + s(50)
    mid1 = ((sh[0] + el[0]) / 2, (sh[1] + el[1]) / 2)
    mid2 = ((el[0] + ft[0]) / 2, (el[1] + ft[1]) / 2)
    for (q, rows, dy_) in ((sh, ["shoulder (ball", "and socket)"], 0), (mid1, ["ℓ₁: humerus, the", "upper-arm link"], 0),
                           (el, ["elbow (hinge)"], 0), (mid2, ["ℓ₂: radius, ulna and", "hand, the forearm-", "and-hand link"], 0)):
        o.append(lead(s, q[0] + s(7), q[1], lx - s(5), q[1]))
        o.extend(H.label(s, lx, q[1] + s(5) + i * s(17), t_, "label2", I["primary"]) for i, t_ in enumerate(rows))
    o.append(H.label(s, 440, 34, "the arm: two links, two joints", "label", I["primary"], "middle"))
    o.append(H.credit(s, 10, VB[3] - 38, wrap(credit_lynch("Left: left shoulder, front view; right: arm bones, front view. "
                                                           "Recoloured, cropped, reposed; head outline, links and joint marks drawn for this course."), 150)))
    aria = ("Left: the left shoulder in front view from a skeleton drawing: the collarbone and the acromion run over the top "
            "of the round head of the humerus, which sits against the shallow glenoid dish of the shoulder blade. The "
            "head is outlined with a dashed circle. Right: the bones of both arms in front view, hanging at the sides; on "
            "one arm two blue links join the shoulder joint, the elbow and the fingertip: l1 along the humerus and l2 "
            "along the forearm and hand.")
    return finish(VB, aria, s, o)


# ================================================================ svg #10  Fig. 9 concavity-compression
ALPHA = 25.0                                                      # deg, the half-arc of the glenoid and labrum (line 232)
assert round(math.tan(math.radians(ALPHA)), 2) == 0.47


def fig10():
    p = "m11f10_"
    VB = (0, 0, 760, 505)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    hgt = 400.0
    t1, t2 = 40.0, 50.0                                          # design values: the arm raised in front
    P = seated(t1, t2)
    body, J, org = put(s, P, hgt, (118.0, 205.0))
    sh = J["shoulder"]
    o = [defs(p, s), floor_line(s, 20, 330, J["floor_y"]), stool(s, J), body, H.joint_centre(s, *sh)]
    o.append(H.label(s, sh[0] - s(24), sh[1] - s(14), "shoulder", "label2", I["secondary"], "end"))
    # the detail: front view of the left shoulder (m03 crop) with the cone of Proposition 7.1
    pl = Place((650.0, 1420.0), (390.0, 46.0), 0.52)
    wbox = pl.box(*SH_WIN)
    o.append(pl.image("shoulder", SH_WIN, p))
    c, r = pl(HUM_C[:2]), HUM_C[2] * pl.k
    o.append(dline(s, sh[0] + s(8), sh[1], wbox[0], c[1], I["rule"], "ref"))
    o.append(H.label(s, wbox[0] + wbox[2] / 2, 30, "detail: the left shoulder, front view", "label2", I["secondary"], "middle"))
    Lc, Fc = 190.0, 125.0
    o.append(head_outline(s, c, r))
    o.append(cone(s, c, 180.0, ALPHA, Lc))
    for sg in (-1, 1):
        q = pol(c, Lc + s(6), 180 + sg * ALPHA)
        o.append(H.label(s, q[0] - s(4), q[1] + (s(15) if sg < 0 else -s(4)), "rim", "label2", O["geometry"], "end"))
    o.append(angle_arc(s, c, 150, 180 - ALPHA, 180))
    m = pol(c, 160, 180 - ALPHA / 2)
    o.append(H.label(s, m[0] - s(6), m[1] + s(9), f"α = {ALPHA:.0f}°", "label2", I["primary"], "end"))
    Ft = Fc * math.tan(math.radians(ALPHA))                       # the verge of dislocation: F_t / F_c = tan alpha
    tipc = (c[0] - Fc, c[1])
    o.append(H.arrow(s, p, c[0], c[1], tipc[0], tipc[1], "force", w="force"))
    o.append(H.arrow(s, p, tipc[0], tipc[1], tipc[0], tipc[1] + Ft, "load", w="force"))
    o.append(H.arrow(s, p, c[0], c[1], tipc[0], tipc[1] + Ft, "reaction", w="geom"))
    o.append(H.joint_centre(s, *c))
    o.append(H.label(s, c[0] - Fc * 0.80, c[1] - s(9), "F" + H.sub("c", s), "label", I["primary"], "middle"))
    o.append(H.label(s, tipc[0] - s(6), tipc[1] + Ft / 2 + s(5), "F" + H.sub("t", s, "label2"), "label2", I["primary"], "end"))
    gq = pol(c, r, 205)
    o.append(lead(s, gq[0] - s(2), gq[1] + s(2), 458, 378))
    o.append(H.label(s, 462, 382, "glenoid (shallow socket)", "label2", I["secondary"]))
    hq = pol(c, r * 0.6, -35)
    o.append(lead(s, hq[0] + s(2), hq[1], 600, 96))
    o.append(H.label(s, 604, 100, "humeral head", "label2", I["secondary"]))
    tx = 590.0
    o.append(lines(s, tx, 150, [f"seated while F{H.sub('t', s, 'label2')}/F{H.sub('c', s, 'label2')} ≤ tan α", f"α = {ALPHA:.0f}°, tan α = {math.tan(math.radians(ALPHA)):.2f}",
                                "", f"red F{H.sub('c', s, 'label2')}: cuff compression", f"brown F{H.sub('t', s, 'label2')}: dislocating force",
                                "black: resultant, drawn at", "the limit (on the rim)"], "label2", I["primary"], dy=s(18)))
    o.append(LB.credit(s, 20, VB[3] - 34, width=720, extra=" Detail: the shoulder crop of the Module 3 figures; cone, forces and head outline drawn for this course."))
    aria = ("A seated skeleton seen from the side, facing right, with the arm raised in front and a dashed line from the "
            "shoulder to a detail of the left shoulder in front view. In the detail the humeral head, outlined by a dashed "
            "circle, sits against the shallow glenoid of the shoulder blade. A blue cone of half-angle alpha equal to 25 "
            "degrees opens toward the socket from the centre of the head, its two edges marked rim. A red arrow F c, "
            "the cuff compression, presses the head into the socket; a brown arrow F t is the dislocating force; their "
            "black resultant lies on the rim of the cone, the limit F t over F c equal to tan alpha, 0.47.")
    return finish(VB, aria, s, o)


FIGS = {
    2: ("Left: shoulder complex with shallow glenoid, humeral head, s", fig2),
    10: ("The glenohumeral joint as concavity-compression. The humeral", fig10),
    11: ("A precision pinch on a cup. Thumb and finger press inward wi", fig11),
    14: ("Left: a seated person's two-link arm at the start and goal o", fig14),
    20: ("Velocity (solid) and force (dashed) ellipses of the two-link ", fig20),
    3: ("Winter-proportion arm reach: shoulder, elbow, wrist chain wi", fig3),
    4: ("A seated person, shoulder at the origin of an x-y frame, rea", fig4),
    5: ("A seated person's two-link arm at a bent posture with the el", fig5),
    6: ("A seated person whose shoulder is the centre of the reachable ", fig6),
    7: ("A seated person holds a cup at the hand with the arm bent to ", fig7),
    8: ("A seated person's three-link arm reaching one fixed fingertip", fig8),
}
