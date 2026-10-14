"""Module 11, group `body_d`: problem figures D2-D4, D6-D10 and K3-K7 (svg #32-34, 36-40, 43-47), house style, 400 px.

Bodies, arms and hands are the posable Lynch skeleton (lynch_body.py); m11/body_main.py puts its defs on the page, this
group only <use>s them (it exposes no SHARED_DEFS).  The pose helpers (fk, ik, jac, arm_pose, seated, put ...) are
copied here from m11/body_main.py on purpose: that file is edited by another group, and a rename there must not break
this one.  Stable modules are imported (house, lynch_body, m05.body, m05.plots_prob, m03.joints).
Stature 1.75 m (the text states none, course reference).  Numbers (module11.html line numbers) asserted below:
  two-link arm l1 = 0.30 m, l2 = 0.45 m (Definition 1 line 104; Appendix lines 642-643), Winter-proportion art stretched
  along its axis to these lengths (upper arm x0.912, forearm+hand x1.016); det J = l1 l2 sin th2 (D2, line 497);
  th2 = +-arccos((r^2 - l1^2 - l2^2)/(2 l1 l2)) (D3, line 501); tau = J^T F (Prop 4.1, line 164); F_g >= W/(2 mu) (D6,
  Prop 8.1); alpha ~ 25 deg, tan alpha ~ 0.47 (line 232); J^+ and the null space (Prop 5.1, line 181); masses and
  inertias m1 = 2.1, m2 = 1.65 kg, lc1 = 0.15, lc2 = 0.22 m, I1 = 0.016, I2 = 0.025 kg m^2 (Appendix lines 645-648),
  M22 = I2 + m2 lc2^2 = 0.10486 (line 206); K3 line 544-545: 0.5 kg cup, s = 0.3, 5.31 / 15.9 / 31.9 N; K4 line 549:
  r = 0.541 m, w = 0.135, 0.95 band 0.46-0.61 m; K5 line 553: l_i = 0.25 m, q0 = (0.4, 1.90, 0.3) rad, elbow 1.90 to
  1.005 rad, fingertip error 6e-11 m; K6 line 557: tau_max = 15 N m, (0.45, 0.10) m elbow-up, F_y max 34.5 N, F_x max 99.4
  N, and 31.9 / 350.5 N at (0.73, 0.10) m; K7 line 561: null vector (0.1411, -0.5272, 0.8379), (+15.4, -34.0, +43.2) deg,
  drift 3.1e-5 m.
Body art: Patrick J. Lynch (CC BY 2.5), through lynch_body; D7 embeds a small crop of the same art (m03 shoulder crop).
"""
import math
import re
from pathlib import Path

import numpy as np

import house as H
import lynch_body as LB
from m03.joints import HUM_C, Place, angle_arc, cone, head_outline, lynch, pol
from m05.body import art_image, finish, it
from m05.plots_prob import Plot, hov, label as plabel, legend

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
BOX, GRID = "#f7f4ef", "#e6e6e6"
BODY = H.MAX_DISPLAY_H_BODY
KIT_SVG = Path(__file__).resolve().parents[2] / "svg_paths"

# ---------------------------------------------------------------- module constants (line numbers in the docstring)
HM = 1.75                                     # m, stature
L1, L2 = 0.30, 0.45                           # m, upper arm and forearm + hand
LI = 0.25                                     # m, each link of the three-link arm (K5, K7)
G = 9.81
UM = LB.H_U / HM                              # body units per metre
K1 = L1 * UM / LB.L_UPPER                     # axial stretch of the upper-arm art (0.912)
K2 = L2 * UM / (LB.L_FORE + LB.L_HAND)        # axial stretch of forearm and hand art (1.016)
SIT = dict(hip=90, knee=90)


def close(v, ref, tol):
    assert abs(v - ref) <= tol * 1.0001, (v, ref)


close(K1, 0.912, 0.0005)
close(K2, 1.016, 0.0005)


# ---------------------------------------------------------------- geometry of the module's arm (math frame: x forward, y up)
def fk(t1, t2, l1=L1, l2=L2):
    """Proposition 1.1: elbow and hand, metres from the shoulder; angles in degrees."""
    a, b = math.radians(t1), math.radians(t1 + t2)
    return (l1 * math.cos(a), l1 * math.sin(a)), (l1 * math.cos(a) + l2 * math.cos(b), l1 * math.sin(a) + l2 * math.sin(b))


def ik(x, y, up=False, l1=L1, l2=L2):
    """Proposition 3.1: (theta1, theta2) in degrees; up=True is the elbow-up branch (theta2 < 0)."""
    c2 = (x * x + y * y - l1 * l1 - l2 * l2) / (2 * l1 * l2)
    t2 = (-1 if up else 1) * math.acos(max(-1.0, min(1.0, c2)))
    t1 = math.atan2(y, x) - math.atan2(l2 * math.sin(t2), l1 + l2 * math.cos(t2))
    return math.degrees(t1), math.degrees(t2)


def jac(t1, t2, l1=L1, l2=L2):
    """Proposition 2.1; angles in radians."""
    s1, s12, c1, c12 = math.sin(t1), math.sin(t1 + t2), math.cos(t1), math.cos(t1 + t2)
    return np.array([[-l1 * s1 - l2 * s12, -l2 * s12], [l1 * c1 + l2 * c12, l2 * c12]])


def fk3(q, l=LI):
    """Three-link arm, angles in radians (relative), metres from the shoulder: [elbow, wrist, fingertip].
    l = one length or three."""
    ls = np.broadcast_to(np.asarray(l, dtype=float), (3,))
    a = np.cumsum(q)
    pts, p = [], np.zeros(2)
    for ai, li in zip(a, ls):
        p = p + li * np.array([math.cos(ai), math.sin(ai)])
        pts.append(p.copy())
    return pts


def jac3(q, l=LI):
    ls = np.broadcast_to(np.asarray(l, dtype=float), (3,))
    a = np.cumsum(q)
    Jm = np.zeros((2, 3))
    for k in range(3):
        Jm[0, k] = -(ls[k:] * np.sin(a[k:])).sum()
        Jm[1, k] = (ls[k:] * np.cos(a[k:])).sum()
    return Jm


def null_unit(q, l=LI, ref=None):
    """Unit null vector of the 2x3 Jacobian (smallest right-singular vector), sign continued from ref."""
    n = np.linalg.svd(jac3(q, l))[2][-1]
    if ref is not None and n @ ref < 0:
        n = -n
    return n


def self_motion(q0, l, path, n_step=800):
    """Integrate q' = n (unit null vector, sign continued) for a path length `path` (rad); return the final q."""
    q = np.array(q0, dtype=float)
    ref = null_unit(q, l)
    if path < 0:
        ref = -ref
    h = abs(path) / n_step
    for _ in range(n_step):
        n = null_unit(q, l, ref)
        ref = n
        q = q + h * n
    return q


# ---------------------------------------------------------------- the posed body
def arm_pose(P, t1, t2, t3=0.0, k=(K1, K2, K2)):
    """Set the near arm of the lateral Pose P to the module's angles (degrees; t1 from +x, counter-clockwise; t2 the
    elbow relative to the upper arm, + = flexion; t3 the wrist relative to the forearm) and return P.  k = axial
    stretch of (upper arm, forearm, hand) art."""
    sh = P.j["shoulder"]
    thu = -(t1 + 90.0)
    thf, thw = thu - t2, thu - t2 - t3
    el = LB.add(sh, LB.rot((0.0, LB.L_UPPER * k[0]), thu))
    wr = LB.add(el, LB.rot((0.0, LB.L_FORE * k[1]), thf))
    ft = LB.add(wr, LB.rot((0.0, LB.L_HAND * k[2]), thw))
    P.j["elbow"], P.j["wrist"], P.j["fingertip"] = el, wr, ft
    segs = [q for q in P.segs if not (q[0].startswith("arm_") and not q[5])]
    segs += [("arm_upper", sh, thu, (1, k[0]), False, False), ("arm_hand", wr, thw, (1, k[2]), False, False),
             ("arm_fore", el, thf, (1, k[1]), False, False)]
    P.segs = segs
    return P


K3L = (LI * UM / LB.L_UPPER, LI * UM / LB.L_FORE, LI * UM / LB.L_HAND)       # three equal links of 0.25 m


def seated(t1, t2, t3=0.0, k=(K1, K2, K2)):
    """Seated lateral pose (thighs horizontal, shanks vertical, feet flat) with the near arm at the module's angles."""
    return arm_pose(LB.pose(near=dict(SIT), far=dict(SIT)), t1, t2, t3, k)


def put(p, s, P, hgt, shoulder_xy):
    """Draw P at stature hgt so that its near shoulder lands on shoulder_xy. Returns (svg, J, origin)."""
    _, J0 = LB.draw(p, s, P, 0.0, 0.0, hgt)
    org = (shoulder_xy[0] - J0["shoulder"][0], shoulder_xy[1] - J0["shoulder"][1])
    sv, J = LB.draw(p, s, P, org[0], org[1], hgt)
    return sv, J, org


def only_arm(P):
    """A copy of P that draws only the near arm (a ghost posture or a floating arm)."""
    P2 = LB.Pose(P.view)
    P2.segs = [q for q in P.segs if q[0].startswith("arm_") and not q[5]]
    P2.j, P2.com, P2.anchor, P2.floor_y = P.j, P.com, P.anchor, P.floor_y
    return P2


def arm_svg(p, s, P, org, hgt, op=1.0):
    """The near arm of P alone, drawn at the origin that put() returned; op < 1 makes it a faint ghost."""
    sv, J = LB.draw(p, s, only_arm(P), org[0], org[1], hgt)
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


def lab(s, x, y, text, size="label2", fill=I["primary"], anchor="start", extra=""):
    return H.label(s, x, y, text, size, fill, anchor, extra)


def lines(s, x, y, rows, size="label2", anchor="start", fill=None, lead=1.35):
    d = s(H.PX[size]) * lead
    return "".join(lab(s, x, y + i * d, t, size, fill or I["primary"], anchor) for i, t in enumerate(rows))


def sb(t, s, size="label2"):
    return H.sub(t, s, size)


def sub(t, s, size="label"):
    return H.sub(t, s, size)


def sp(t, s, size="label2"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


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


def swatch(s, x, y, col, dash=None, w="curve_multi"):
    """Short line mark that carries identity beside an ink label."""
    return H.line(s, x, y, x + s(20), y, col, w, dash)


def arc_pts(cx, cy, r, a0, a1, n=24):
    """Screen angles in degrees: 0 = +x, + = clockwise (y down)."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def arc_arrow(s, p, cx, cy, r, a0, a1, meaning, both=False, head=True, w=None):
    w = w or {"geometry": "geom", "dim": "ref"}.get(meaning, "force")
    ms = f' marker-start="url(#{p}a_{meaning})"' if both else ""
    me = f' marker-end="url(#{p}a_{meaning})"' if head else ""
    return (f'<path d="{path_d(arc_pts(cx, cy, r, a0, a1))}" fill="none" stroke="{O[meaning]}" '
            f'stroke-width="{s(H.PX[w]):.2f}"{me}{ms}/>')


def math_xy(sh, km, v):
    """Metres (x forward, y up) from the shoulder -> figure units."""
    return sh[0] + km * v[0], sh[1] - km * v[1]


def sc_ang(t):
    """Math angle (deg, counter-clockwise) -> screen angle (deg, clockwise)."""
    return -t


def mn(v, f="{:g}"):
    return f.format(v).replace("-", "−")


def th(n):
    return "θ" + {1: "₁", 2: "₂", 3: "₃"}[n]


def cup(s, x, y, w):
    """A mug (schematic object, fluid-blue tissue tokens) with its base centre at (x, y)."""
    h = w * 1.15
    f, ln = T["fluid"]
    return (f'<path d="M{x + w / 2:.2f},{y - h * 0.72:.2f} q{w * 0.45:.2f},{h * 0.02:.2f} {w * 0.04:.2f},{h * 0.42:.2f}" '
            f'fill="none" stroke="{ln}" stroke-width="{s(1.6):.2f}"/>'
            f'<rect x="{x - w / 2:.2f}" y="{y - h:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{w * 0.08:.2f}" fill="{f}" '
            f'stroke="{ln}" stroke-width="{s(1.2):.2f}"/>')


def box(s, x, y, w, h, fill=BOX, stroke=None, extra=""):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" '
            f'stroke="{stroke or I["rule"]}" stroke-width="{s(1):.2f}" rx="{s(6):.2f}" {extra}/>')


def credit(s, vb, extra=""):
    """Lynch credit at the bottom of the viewBox, wrapped to its width (the wrap rule of LB.credit)."""
    w = vb[2] - s(12)
    t = H.ATTRIBUTION["by"].format(
        author="Patrick J. Lynch, medical illustrator",
        title="Skeleton lateral.svg” and “Skeleton whole body ant lat views.svg", licence="CC BY 2.5",
        changes="Recoloured, split into segments and reposed; arms from the anterior view." + extra)
    n = max(20, int(w / (s(H.PX["credit"]) * 0.47)))
    nl, cur = 0, ""
    for wd in t.split():
        if cur and len(cur) + 1 + len(wd) > n:
            nl, cur = nl + 1, wd
        else:
            cur = (cur + " " + wd).strip()
    y = vb[1] + vb[3] - s(6) - nl * s(H.PX["credit"]) * 1.25
    return LB.credit(s, vb[0] + s(6), y, width=w, extra=extra)


def bvb(h, w=400):
    return (0, 0, w, h), H.Scale(w, h, display_w=400, max_h=BODY)


FIGS = {}


# ================================================================ svg #32  D2 the Jacobian and its determinant
def fig32():
    p = "m11f32_"
    hgt = 350.0
    km = hgt / HM
    VB, s = bvb(388)
    t1, t2 = -25.0, 50.0                                        # design values: elbow below the line, not at the maximum
    P = seated(t1, t2)
    body, J, org = put(p, s, P, hgt, (92.0, 118.0))
    sh, el, hd = J["shoulder"], J["elbow"], J["fingertip"]
    Jm = jac(math.radians(t1), math.radians(t2))
    det = np.linalg.det(Jm)
    close(det, L1 * L2 * math.sin(math.radians(t2)), 1e-12)     # D2: det J = l1 l2 sin th2 (line 497)
    close(abs(det), 0.1034, 0.0001)
    em, hm = fk(t1, t2)
    assert abs(math_xy(sh, km, hm)[0] - hd[0]) < 0.5 and abs(math_xy(sh, km, hm)[1] - hd[1]) < 0.5, (hd, math_xy(sh, km, hm))
    kv = 0.42 * km                                              # figure units per (m/s)
    # the straight arm at the same shoulder angle: a faint ghost with its two columns on one line
    Pst = seated(t1, 0.0)
    ghost, Jg = arm_svg(p, s, Pst, org, hgt, 0.70)
    hg = Jg["fingertip"]
    Jst = jac(math.radians(t1), 0.0)
    close(np.linalg.det(Jst), 0.0, 1e-12)
    o = [defs(p, s), floor_line(s, 8, 300, J["floor_y"]), stool(s, J), body, ghost]
    c1 = (hd[0] + kv * Jm[0, 0], hd[1] - kv * Jm[1, 0])
    c2 = (hd[0] + kv * Jm[0, 1], hd[1] - kv * Jm[1, 1])
    c12 = (c1[0] + kv * Jm[0, 1], c1[1] - kv * Jm[1, 1])
    o.append(f'<polygon points="{hd[0]:.1f},{hd[1]:.1f} {c1[0]:.1f},{c1[1]:.1f} {c12[0]:.1f},{c12[1]:.1f} '
             f'{c2[0]:.1f},{c2[1]:.1f}" fill="{O["geometry"]}" fill-opacity="0.10" stroke="none"/>')
    for tip, meaning in ((c1, "geometry"), (c2, "flag")):
        o.append(white_under(s, hd[0], hd[1], tip[0], tip[1], 5))
        o.append(H.arrow(s, p, hd[0], hd[1], tip[0], tip[1], meaning, w="force"))
    o.append(dot(s, hd[0], hd[1], I["primary"], 4.0))
    for k_, meaning in ((0, "geometry"), (1, "flag")):
        tip = (hg[0] + kv * Jst[0, k_], hg[1] - kv * Jst[1, k_])
        o.append(white_under(s, hg[0], hg[1], tip[0], tip[1], 5))
        o.append(H.arrow(s, p, hg[0], hg[1], tip[0], tip[1], meaning, w="force"))
    o.append(dot(s, hg[0], hg[1], I["primary"], 4.0))
    o.append(arc_arrow(s, p, sh[0], sh[1], 0.15 * km, 25, -35, "geometry"))
    o.append(arc_arrow(s, p, el[0], el[1], 0.13 * km, 75, 5, "flag"))
    o.append(H.joint_centre(s, *sh))
    o.append(H.joint_centre(s, *el))
    # right column: what the picture shows
    x0 = 248.0
    o.append(swatch(s, x0, 24, O["geometry"], None, "force"))
    o.append(lines(s, x0 + 26, 28, ["column 1 of J: hand", "velocity for a unit", "shoulder rate"]))
    o.append(swatch(s, x0, 86, O["flag"], None, "force"))
    o.append(lines(s, x0 + 26, 90, ["column 2: for a", "unit elbow rate"]))
    o.append(lines(s, x0, 146, ["parallelogram area", "|det J| = ℓ₁ℓ₂|sin θ₂|", f"= {abs(det):.3f} m² at θ₂ = {t2:.0f}°"]))
    o.append(lines(s, x0, 202, ["faint arm, θ₂ = 0:", "columns on one line,", "area 0, det J = 0", "(also at θ₂ = π)"]))
    o.append(leader(s, hg[0] + s(6), hg[1] + s(2), x0 - s(4), 232))
    o.append(credit(s, VB))
    aria = ("A seated skeleton seen from the side, facing right, with the arm bent at the elbow, the elbow below the line from "
            "shoulder to hand. From the hand a blue arrow gives the hand velocity for a unit shoulder rate (first column of "
            "J) and an orange arrow the velocity for a unit elbow rate (second column). The pale blue parallelogram they "
            f"span has area equal to the absolute determinant, l1 l2 sin theta2 = {abs(det):.3f} square metres at theta2 = "
            f"{t2:.0f} degrees. A faint straight arm at the same shoulder angle has both arrows along one line: the columns "
            "of J are parallel, the determinant is zero, and the hand has lost one direction of motion. The same holds for "
            "the folded arm, theta2 = pi.")
    return finish(VB, aria, s, o)


FIGS[32] = ("D2: the Jacobian and its determinant. Differentiate the forw", fig32)


# ================================================================ svg #33  D3 inverse kinematics, two solutions
def fig33():
    p = "m11f33_"
    hgt = 320.0
    km = hgt / HM
    VB, s = bvb(398)
    tgt = (0.55, 0.25)                                          # design value: a target inside the annulus
    rr = math.hypot(*tgt)
    assert abs(L1 - L2) < rr < L1 + L2
    dn, up = ik(*tgt), ik(*tgt, up=True)
    assert abs(dn[1] + up[1]) < 1e-9 and dn[1] > 0
    for q in (dn, up):                                          # both branches reach the target (line 501)
        assert abs(fk(*q)[1][0] - tgt[0]) < 1e-9 and abs(fk(*q)[1][1] - tgt[1]) < 1e-9
    close(rr, 0.604, 0.0005)
    close(dn[1], 74.4, 0.05)
    P_dn, P_up = seated(*dn), seated(*up)
    cx, cy = 92.0, 152.0
    body, J, org = put(p, s, P_dn, hgt, (cx, cy))
    ghost, Ju = arm_svg(p, s, P_up, org, hgt, 0.55)
    sh = J["shoulder"]
    tp = math_xy(sh, km, tgt)
    assert abs(tp[0] - J["fingertip"][0]) < 0.5 and abs(tp[0] - Ju["fingertip"][0]) < 0.5
    R = (L1 + L2) * km
    o = [defs(p, s)]
    o.append(f'<path d="{path_d(arc_pts(sh[0], sh[1], R, -50, 38, 40))}" fill="none" stroke="{O["geometry"]}" '
             f'stroke-width="{s(1.6):.2f}" stroke-dasharray="{s(6):.1f} {s(4):.1f}"/>')
    o += [floor_line(s, 8, 205, J["floor_y"]), stool(s, J), body, ghost]
    o.append(dline(s, sh[0], sh[1], tp[0], tp[1], O["geometry"], "geom"))
    for Jx, dash in ((Ju, H.DASH_REF), (J, None)):                  # the two link chains over the art
        pts = [sh, Jx["elbow"], Jx["fingertip"]]
        o.append(poly(s, pts, I["primary"], "ref", dash))
    o.append(ring(s, tp[0], tp[1], O["flag"], 6.5))
    o.append(H.joint_centre(s, *sh))
    eu, ed = Ju["elbow"], J["elbow"]
    o.append(lab(s, eu[0] - s(6), eu[1] - s(11), "elbow-up", "label2", I["primary"], "end"))
    o.append(lab(s, ed[0] + s(8), ed[1] + s(22), "elbow-down", "label2", I["primary"]))
    mid = ((sh[0] + tp[0]) / 2, (sh[1] + tp[1]) / 2)
    o.append(lab(s, mid[0] + s(2), mid[1] - s(8), it("r"), "label", I["primary"]))
    o.append(lab(s, tp[0] + s(10), tp[1] - s(8), "target", "label2", I["primary"]))
    q = pol(sh, R, -34)
    o.append(lab(s, q[0] + s(6), q[1] - s(4), "r = ℓ₁ + ℓ₂", "label2", I["primary"]))
    o.append(lab(s, 200, 20, "cos θ₂ = (r² − ℓ₁² − ℓ₂²) / (2ℓ₁ℓ₂),  θ₂ = ± arccos(·)", "label2", I["primary"], "middle"))
    x0, y0 = 236.0, 178.0
    o.append(lines(s, x0, y0, ["target (0.55, 0.25) m,", "r = 0.604 m", "solid arm, elbow-down:", f"θ₂ = +{dn[1]:.1f}°, θ₁ = {mn(dn[0], '{:.1f}')}°",
                               "faint arm, elbow-up:", f"θ₂ = {mn(up[1], '{:.1f}')}°, θ₁ = +{up[0]:.1f}°"], lead=1.4))
    o.append(lines(s, x0, y0 + 124, ["on the dashed edge", "cos θ₂ = ±1: the two", "arms coincide"], fill=I["secondary"], lead=1.4))
    o.append(credit(s, VB))
    aria = ("A seated skeleton seen from the side, facing right, with a dashed blue arc of radius l1 plus l2 = 0.75 metres "
            "around the shoulder, the outer edge of the reachable workspace. An orange ring marks one target, 0.55 m forward "
            "and 0.25 m up, at distance r = 0.604 m, joined to the shoulder by a dashed blue line. The solid arm reaches it "
            f"elbow-down, theta2 = +{dn[1]:.1f} degrees, with the elbow below the line from shoulder to target; a faint "
            f"second arm reaches the same target elbow-up, theta2 = {up[1]:.1f} degrees, with the elbow above it. The two "
            "joint-angle solutions are the two signs of arccos; on the outer edge cos theta2 = 1, the signs merge and the "
            "two arms coincide.")
    return finish(VB, aria, s, o)


FIGS[33] = ("D3: inverse kinematics. Given a target $(x,y)$ inside the wo", fig33)


# ================================================================ svg #34  D4 virtual work: tau = J^T F
def fig34():
    p = "m11f34_"
    hgt = 350.0
    km = hgt / HM
    VB, s = bvb(388)
    t1, t2 = -25.0, 60.0                                        # design values (the posture of Figure 3)
    P = seated(t1, t2)
    body, J, org = put(p, s, P, hgt, (92.0, 118.0))
    sh, el, hd = J["shoulder"], J["elbow"], J["fingertip"]
    Jm = jac(math.radians(t1), math.radians(t2))
    F = 10.0 * np.array([math.cos(math.radians(60)), math.sin(math.radians(60))])     # design value: 10 N at 60 degrees
    dq = np.array([0.05, 0.08])                                 # design value: a small virtual joint rotation, rad
    tau = Jm.T @ F                                              # Proposition 4.1
    dp = Jm @ dq                                                # delta p = J delta q
    wj, we = float(tau @ dq), float(F @ dp)
    close(wj, we, 1e-12)                                        # the virtual works are equal for every delta q (line 164)
    close(wj, 0.3967, 0.0005)
    em, hm = fk(t1, t2)
    assert abs(math_xy(sh, km, hm)[0] - hd[0]) < 0.5 and abs(math_xy(sh, km, em)[1] - el[1]) < 0.5
    o = [defs(p, s), floor_line(s, 8, 300, J["floor_y"]), stool(s, J), body]
    o.append(poly(s, [sh, el, hd], I["primary"], "ref"))
    # F: the force the hand applies to the world (red), delta p (blue), direction only
    fl = 50.0
    ft = (hd[0] + fl * F[0] / 10.0, hd[1] - fl * F[1] / 10.0)
    o.append(white_under(s, hd[0], hd[1], ft[0], ft[1], 5))
    o.append(H.arrow(s, p, hd[0], hd[1], ft[0], ft[1], "force"))
    dl = 46.0
    dpt = (hd[0] + dl * dp[0] / np.hypot(*dp), hd[1] - dl * dp[1] / np.hypot(*dp))
    o.append(white_under(s, hd[0], hd[1], dpt[0], dpt[1], 5))
    o.append(H.arrow(s, p, hd[0], hd[1], dpt[0], dpt[1], "geometry"))
    o.append(dot(s, hd[0], hd[1], I["primary"], 4.0))
    o.append(lab(s, ft[0] + s(4), ft[1] - s(4), it("F"), "label", I["primary"]))
    o.append(lab(s, dpt[0] - s(4), dpt[1] - s(6), "δp", "label", I["primary"], "end"))
    # delta q (blue, inner) and tau (red, outer) at the two joints, both counter-clockwise
    for c, rq, rt, a0, a1, nm in ((sh, 0.10 * km, 0.17 * km, 75, -5, 1), (el, 0.09 * km, 0.155 * km, 115, 35, 2)):
        o.append(arc_arrow(s, p, c[0], c[1], rq, a0, a1, "geometry"))
        o.append(arc_arrow(s, p, c[0], c[1], rt, a0, a1, "force"))
        o.append(H.joint_centre(s, *c))
        q = pol(c, rq - s(2), a0 + 18)
        o.append(lab(s, q[0], q[1] + s(5), f"δq{'₁₂'[nm - 1]}", "label2", I["primary"], "end"))
        q = pol(c, rt + s(8), a1 - 8)
        o.append(lab(s, q[0], q[1] + s(5), f"τ{'₁₂'[nm - 1]}", "label2", I["primary"]))
    x0 = 232.0
    o.append(swatch(s, x0, 100, O["force"], None, "force"))
    o.append(lines(s, x0 + 26, 104, ["F: force of hand on", "world; τ: joint torque"]))
    o.append(swatch(s, x0, 140, O["geometry"], None, "force"))
    o.append(lines(s, x0 + 26, 144, ["δq: virtual joint turn;", "δp = J δq: hand move"]))
    o.append(lab(s, x0, 180, "(directions, not to scale)", "label2", I["secondary"]))
    rows = [f"F = ({F[0]:.1f}, {F[1]:.1f}) N", f"δq = ({dq[0]:.2f}, {dq[1]:.2f}) rad",
            f"τ = Jᵀ F = ({tau[0]:.2f}, {tau[1]:.2f}) N m", f"δp = J δq = ({1000 * dp[0]:.0f}, {1000 * dp[1]:.0f}) mm".replace("-", "−"),
            f"τᵀδq = {wj:.3f} J", f"Fᵀδp = {we:.3f} J: equal,", "so net virtual work is 0"]
    o.append(lines(s, x0, 204, rows, lead=1.4))
    o.append(credit(s, VB))
    aria = ("A seated skeleton seen from the side, facing right, with the arm bent at the elbow, the elbow below the line from "
            "shoulder to hand. A red arrow F at the hand, 10 newtons at 60 degrees above horizontal, is the force the hand "
            "applies to the world. A blue arrow delta-p at the hand is the virtual hand displacement J delta-q. At the "
            "shoulder and elbow a small blue arc is the virtual joint rotation delta-q and a larger red arc the joint "
            f"torque tau. With delta-q = (0.05, 0.08) rad, tau = J transpose F = ({tau[0]:.2f}, {tau[1]:.2f}) newton metres; "
            f"the joint virtual work tau transpose delta-q and the hand virtual work F transpose delta-p are both {wj:.3f} "
            "joules, so the net virtual work is zero.")
    return finish(VB, aria, s, o)


FIGS[34] = (r"D4: the force-torque transpose. Prove $\boldsymbol\tau=J^{\m", fig34)


# ================================================================ svg #36  D6 minimum grip force
M_CUP, MU_DRY, MU_WET = 0.5, 0.5, 0.2                           # kg, line 252-256 (full glass; dry and wet skin on glass)
W_CUP = M_CUP * G


def fig36():
    p = "m11f36_"
    hgt = 300.0
    km = hgt / HM
    VB, s = bvb(402)
    t1, t2 = -15.0, 55.0                                        # design values: the cup held at about shoulder height
    P = seated(t1, t2)
    body, J, org = put(p, s, P, hgt, (80.0, 106.0))
    sh, hd = J["shoulder"], J["fingertip"]
    em, hm = fk(t1, t2)
    assert abs(math_xy(sh, km, hm)[0] - hd[0]) < 0.5
    cw = 0.075 * hgt
    base = (hd[0] + cw * 0.15, hd[1] + 0.62 * cw * 1.15)
    o = [defs(p, s), floor_line(s, 8, 220, J["floor_y"]), stool(s, J), body, cup(s, base[0], base[1], cw)]
    # detail panel: free body of the cup
    bx, by, bw, bh = 238.0, 14.0, 158.0, 326.0
    o.append(box(s, bx, by, bw, bh))
    ccx, ccy = bx + bw / 2, 86.0
    o.append(H.line(s, base[0] + cw * 0.5 + s(3), base[1] - cw * 0.6, bx, ccy, I["rule"], "leader", H.DASH_REF))
    o.append(lab(s, bx + bw / 2, by + s(16), "forces on the cup", "label2", I["secondary"], "middle"))
    wc, hc = 44.0, 56.0
    sc = 44.0                                                   # px per weight W
    fg = 1 / (2 * MU_DRY)                                       # F_g at the minimum, in W (dry skin)
    close(fg, 1.0, 1e-12)
    f, ln = T["fluid"]
    o.append(f'<rect x="{ccx - wc / 2:.2f}" y="{ccy - hc / 2:.2f}" width="{wc:.2f}" height="{hc:.2f}" rx="{s(3):.2f}" '
             f'fill="{f}" stroke="{ln}" stroke-width="{s(1.2):.2f}"/>')
    for sg in (-1, 1):
        xf = ccx + sg * wc / 2
        o.append(H.arrow(s, p, xf + sg * (fg * sc + s(2)), ccy, xf + sg * s(1), ccy, "force"))
        xr = xf - sg * s(8)
        o.append(H.arrow(s, p, xr, ccy + 0.25 * sc, xr, ccy - 0.25 * sc, "reaction"))
    o.append(H.arrow(s, p, ccx, ccy + hc / 2 + s(1), ccx, ccy + hc / 2 + sc + s(1), "load"))
    yl = ccy - hc / 2 - s(8)
    o.append(lab(s, ccx - wc / 2 - fg * sc * 0.5, ccy - s(8), f"F{sb('g', s)}", "label2", I["primary"], "middle"))
    o.append(lab(s, ccx + wc / 2 + fg * sc * 0.5, ccy - s(8), f"F{sb('g', s)}", "label2", I["primary"], "middle"))
    o.append(lab(s, ccx + s(10), ccy + hc / 2 + sc * 0.6, it("W"), "label", I["primary"]))
    # legend and the derivation
    ly = by + 168.0
    o.append(swatch(s, bx + 10, ly - 4, O["force"], None, "force"))
    o.append(lab(s, bx + 38, ly, f"grip F{sb('g', s)} at each pad", "label2"))
    o.append(swatch(s, bx + 10, ly + 18, O["reaction"], None, "force"))
    o.append(lab(s, bx + 38, ly + 22, f"friction F{sb('t', s)}, ≤ μF{sb('g', s)}", "label2"))
    o.append(swatch(s, bx + 10, ly + 40, O["load"], None, "force"))
    o.append(lab(s, bx + 38, ly + 44, "weight W = mg", "label2"))
    wet = W_CUP / (2 * MU_WET)
    close(W_CUP, 4.9, 0.01)
    close(W_CUP / (2 * MU_DRY), 4.9, 0.01)
    close(wet, 12.3, 0.05)
    rows = [f"F{sb('t', s)}₁ + F{sb('t', s)}₂ = W, each W/2", f"W/2 ≤ μF{sb('g', s)}  ⇒  F{sb('g', s)} ≥ W/(2μ)",
            f"m = {M_CUP} kg, W = {W_CUP:.1f} N:", f"μ = {MU_DRY}: F{sb('g', s)} ≥ {W_CUP / (2 * MU_DRY):.1f} N",
            f"μ = {MU_WET}: F{sb('g', s)} ≥ {wet:.1f} N"]
    o.append(lines(s, bx + 10, ly + 76, rows, lead=1.4))
    o.append(credit(s, VB))
    aria = ("Left, a seated skeleton seen from the side, facing right, holds a mug at the hand between thumb and finger. "
            "Right, a free-body diagram of the mug. Two red arrows are the grip force F_g, one from each side; two black "
            "arrows are the friction at the two pads, each W/2 upward; a brown arrow is the weight W downward. Vertical "
            "balance gives F_t1 + F_t2 = W, each W/2; Coulomb friction caps each at mu F_g, so no slip needs F_g at "
            f"least W/(2 mu). For a {M_CUP} kg cup, W = {W_CUP:.1f} N: mu = {MU_DRY} needs {W_CUP / (2 * MU_DRY):.1f} N "
            f"per pad, mu = {MU_WET} needs {wet:.1f} N.")
    return finish(VB, aria, s, o)


FIGS[36] = ("D6: minimum grip force. Derive the least grip force that hol", fig36)


# ================================================================ svg #37  D7 the stability ratio (shoulder)
ALPHA = 25.0                                                    # deg, glenoid effective half-arc (line 232, Appendix 651)
RATIO_DRAWN = 0.35                                              # design value: F_t / F_c drawn inside the cone


def fig37():
    p = "m11f37_"
    VB, s = bvb(500)
    close(math.tan(math.radians(ALPHA)), 0.47, 0.005)           # line 232: tan 25 deg = 0.47
    psi = math.degrees(math.atan(RATIO_DRAWN))
    assert psi < ALPHA
    win = (730, 1520, 1100, 1840)
    k = 0.80
    pl = Place(win[:2], (52.0, 16.0), k)
    img = pl.image("shoulder", win, p)
    c, r = pl(HUM_C[:2]), HUM_C[2] * k
    ax, Lc = 180.0, 108.0
    o = [defs(p, s), img, head_outline(s, c, r), cone(s, c, ax, ALPHA, 1.3 * Lc)]
    tip = pol(c, Lc, ax)                                        # F_c: from the head centre into the socket
    o.append(H.arrow(s, p, c[0], c[1], tip[0], tip[1], "force"))
    tip2 = pol(tip, RATIO_DRAWN * Lc, ax - 90.0)                # F_t across the axis (downward in the picture)
    o.append(white_under(s, tip[0], tip[1], tip2[0], tip2[1], 5))
    o.append(H.arrow(s, p, tip[0], tip[1], tip2[0], tip2[1], "load"))
    o.append(white_under(s, c[0], c[1], tip2[0], tip2[1], 5))
    o.append(H.arrow(s, p, c[0], c[1], tip2[0], tip2[1], "reaction"))
    o.append(angle_arc(s, c, 0.62 * Lc, ax, ax + ALPHA))
    o.append(angle_arc(s, c, 0.46 * Lc, ax, ax - psi, I["primary"]))
    o.append(H.joint_centre(s, *c))
    la = pol(c, 0.62 * Lc + s(15), ax + ALPHA * 0.5)
    o.append(lab(s, la[0], la[1] + s(5), "α", "label", O["geometry"], "middle", 'font-style="italic"'))
    lp = pol(c, 0.46 * Lc + s(14), ax - psi * 0.5)
    o.append(lab(s, lp[0], lp[1] + s(5), "ψ", "label", I["primary"], "middle", 'font-style="italic"'))
    o.append(lab(s, tip[0] + s(8), c[1] - s(9), f"F{sb('c', s, 'label')}", "label", I["primary"], "start"))
    o.append(lab(s, tip[0] - s(9), (tip[1] + tip2[1]) / 2 + s(6), f"F{sb('t', s, 'label')}", "label", I["primary"], "end"))
    o.append(lab(s, 14, 36, "glenoid", "label2", I["secondary"]))
    o.append(leader(s, 38, 42, tip[0] - s(8), tip[1] - 0.36 * Lc))
    hq = pol(c, r, -50)
    o.append(lab(s, 386, 36, "humeral head", "label2", I["secondary"], "end"))
    o.append(leader(s, 330, 42, hq[0], hq[1]))
    # key and the result, below the art
    y0 = 298.0
    o.append(swatch(s, 14, y0 - 4, O["force"], None, "force"))
    o.append(lab(s, 40, y0, f"compressive F{sb('c', s)}: cuff, into the socket", "label2"))
    o.append(swatch(s, 14, y0 + 18, O["load"], None, "force"))
    o.append(lab(s, 40, y0 + 22, f"dislocating F{sb('t', s)}: tangential", "label2"))
    o.append(swatch(s, 14, y0 + 40, O["reaction"], None, "force"))
    o.append(lab(s, 40, y0 + 44, "resultant, at angle ψ from the socket axis", "label2"))
    o.append(swatch(s, 14, y0 + 58, O["geometry"], H.DASH_REF, "geom"))
    o.append(lab(s, 40, y0 + 62, "rim lines, half-arc α (socket edge)", "label2"))
    ta = math.tan(math.radians(ALPHA))
    o.append(lines(s, 14, y0 + 94, [f"seated iff ψ = arctan(F{sb('t', s)}/F{sb('c', s)}) ≤ α, i.e. F{sb('t', s)}/F{sb('c', s)} ≤ tan α",
                                    f"α ≈ {ALPHA:.0f}°: tan α = {ta:.2f}; drawn F{sb('t', s)}/F{sb('c', s)} = {RATIO_DRAWN:.2f},",
                                    f"ψ = {psi:.1f}° < α: seated"], lead=1.4))
    t = H.ATTRIBUTION["by"].format(author="Patrick J. Lynch, medical illustrator", title="Skeleton whole body ant lat views.svg",
                                   licence="CC BY 2.5", changes="Left shoulder, front view; recoloured, cropped; head outline, cone and forces "
                                   "drawn for this course. α is the text value, not measured on the art.")
    n = int((VB[2] - s(12)) / (s(H.PX["credit"]) * 0.47))
    rows, cur = [], ""
    for wd in t.split():
        if cur and len(cur) + 1 + len(wd) > n:
            rows.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    rows.append(cur)
    o.append(H.credit(s, 6, VB[3] - 6 - (len(rows) - 1) * s(H.PX["credit"]) * 1.25, rows))
    aria = ("A left shoulder in front view (Lynch skeleton art): the round humeral head sits in the shallow glenoid. A "
            "red arrow F_c from the head centre points into the socket along the socket axis; a brown arrow F_t across "
            f"the axis is the dislocating force, drawn at F_t/F_c = {RATIO_DRAWN:.2f}. Their black resultant makes angle psi = "
            f"{psi:.1f} degrees with the axis. A blue wedge of half-angle alpha = {ALPHA:.0f} degrees about the axis is the "
            "socket: while the resultant lies inside it, psi at most alpha, the head stays seated. That is F_t/F_c at most "
            f"tan alpha = {ta:.2f}.")
    return finish(VB, aria, s, o)


FIGS[37] = ("D7: the stability ratio. Derive the concavity-compression co", fig37)


# ================================================================ svg #38  D8 redundancy resolution
def fig38():
    p = "m11f38_"
    hgt = 340.0
    km = hgt / HM
    VB, s = bvb(400)
    ls = np.array([LB.L_UPPER, LB.L_FORE, LB.L_HAND]) / UM          # the kit's own Winter links, m (0.329, 0.254, 0.189)
    kk = (1.0, 1.0, 1.0)
    q0 = np.radians([-20.0, 55.0, 25.0])                            # design values: a forward reach, elbow below
    Jm = jac3(q0, ls)
    Jp = Jm.T @ np.linalg.inv(Jm @ Jm.T)                            # Proposition 5.1 (line 181)
    close(float(np.abs(Jp - np.linalg.pinv(Jm)).max()), 0.0, 1e-12)
    close(float(np.abs(Jm @ Jp - np.eye(2)).max()), 0.0, 1e-12)     # J J+ = I
    pdot = np.array([0.10, 0.05])                                   # design value: desired hand velocity, m/s
    z = np.array([0.0, 0.0, 1.0])                                   # design value: the secondary wish, rad/s
    Pn = np.eye(3) - Jp @ Jm                                        # projector onto the null space
    qmin, qnull = Jp @ pdot, Pn @ z
    close(float(np.abs(Jm @ qnull).max()), 0.0, 1e-12)              # the null part moves nothing
    close(float(np.abs(Jm @ (qmin + qnull) - pdot).max()), 0.0, 1e-12)
    close(float(qmin @ qnull), 0.0, 1e-12)                          # the two parts are orthogonal
    close(float(np.abs(Pn @ Pn - Pn).max()), 0.0, 1e-12)            # idempotent (and symmetric)
    close(float(np.abs(Pn - Pn.T).max()), 0.0, 1e-12)
    assert qmin @ qmin + qnull @ qnull >= qmin @ qmin
    P0 = seated(*np.degrees(q0), k=kk)
    body, J, org = put(p, s, P0, hgt, (92.0, 120.0))
    sh, el, hd = J["shoulder"], J["elbow"], J["fingertip"]
    pts = fk3(q0, ls)
    assert abs(math_xy(sh, km, pts[2])[0] - hd[0]) < 0.5 and abs(math_xy(sh, km, pts[2])[1] - hd[1]) < 0.5, (hd, pts[2])
    o = [defs(p, s), floor_line(s, 8, 300, J["floor_y"]), stool(s, J)]
    ghosts = []
    for sgn, path in ((-1, -0.9), (1, 0.9)):
        qg = self_motion(q0, ls, path)
        assert np.linalg.norm(fk3(qg, ls)[2] - pts[2]) < 1e-3       # the fingertip stays put
        Pg = seated(*np.degrees(qg), k=kk)
        g, Jg = arm_svg(p, s, Pg, org, hgt, 0.6)
        ghosts.append(g)
    o += ghosts + [body]
    kv = 55.0 / float(np.hypot(*pdot))                              # figure units per (m/s), both arrows
    tip = (hd[0] + kv * pdot[0], hd[1] - kv * pdot[1])
    o.append(white_under(s, hd[0], hd[1], tip[0], tip[1], 5))
    o.append(H.arrow(s, p, hd[0], hd[1], tip[0], tip[1], "geometry", w="force"))
    o.append(dot(s, hd[0], hd[1], I["primary"], 4.0))
    wr = J["wrist"]
    a = np.cumsum(q0)
    qd = qnull
    vel = np.array([-(ls[0] * math.sin(a[0])) * qd[0] - ls[1] * math.sin(a[1]) * (qd[0] + qd[1]),
                    ls[0] * math.cos(a[0]) * qd[0] + ls[1] * math.cos(a[1]) * (qd[0] + qd[1])])   # wrist velocity, m/s
    etip = (wr[0] + kv * vel[0], wr[1] - kv * vel[1])
    o.append(white_under(s, wr[0], wr[1], etip[0], etip[1], 5))
    o.append(H.arrow(s, p, wr[0], wr[1], etip[0], etip[1], "flag", w="force"))
    o.append(H.joint_centre(s, *sh))
    o.append(H.joint_centre(s, *el))
    x0 = 246.0
    o.append(swatch(s, x0, 26, O["geometry"], None, "force"))
    o.append(lines(s, x0 + 26, 30, ["hand velocity ṗ,", "reached by J⁺ṗ"]))
    o.append(swatch(s, x0, 68, O["flag"], None, "force"))
    o.append(lines(s, x0 + 26, 72, ["wrist velocity in the", "self-motion (I−J⁺J)z"]))
    o.append(lab(s, x0, 112, "same scale. Faint arms:", "label2", I["secondary"]))
    o.append(lab(s, x0, 130, "the self-motion, tip fixed", "label2", I["secondary"]))
    fmt = lambda v: "(" + ", ".join(mn(x, "{:.2f}") for x in v) + ")"      # noqa: E731
    rows = [f"ṗ = ({pdot[0]:.2f}, {pdot[1]:.2f}) m/s", f"J⁺ṗ = {fmt(qmin)}", f"z = (0, 0, 1), (I−J⁺J)z =", f"  {fmt(qnull)}",
            f"J(I−J⁺J)z = (0, 0) m/s", f"|J⁺ṗ|² = {qmin @ qmin:.3f}", f"|q̇|² = {qmin @ qmin:.3f} + {qnull @ qnull:.3f}",
            f"  = {(qmin + qnull) @ (qmin + qnull):.3f} ≥ |J⁺ṗ|²"]
    o.append(lines(s, x0 - s(14), 172, rows, lead=1.4))
    o.append(credit(s, VB))
    aria = ("A seated skeleton seen from the side, facing right, with a three-link arm (shoulder, elbow, wrist, fingertip) "
            "reaching forward. A blue arrow at the fingertip is the desired hand velocity p-dot. Two faint arms show the "
            "self-motion: the elbow and wrist take other positions while the fingertip stays on the same spot. An orange "
            "arrow at the elbow is the elbow velocity of that self-motion, (I minus J-plus J) z, drawn to the same scale. "
            f"Numbers: p-dot = (0.10, 0.05) m/s gives the minimum-norm joint rate J-plus p-dot with squared norm "
            f"{qmin @ qmin:.3f}; the null-space part has squared norm {qnull @ qnull:.3f} and moves the hand by zero; "
            f"the squares add, {(qmin + qnull) @ (qmin + qnull):.3f}, so the pseudoinverse term is the minimum-norm solution.")
    return finish(VB, aria, s, o)


FIGS[38] = (r"D8: redundancy resolution. For a full-row-rank $2\times3$ Ja", fig38)


# ================================================================ svg #39  D9 the mass matrix
M1_, M2_, LC1, LC2, I1_, I2_ = 2.1, 1.65, 0.15, 0.22, 0.016, 0.025   # Appendix lines 645-648


def mass_matrix(t2_deg):
    c2 = math.cos(math.radians(t2_deg))
    m11 = I1_ + I2_ + M1_ * LC1 ** 2 + M2_ * (L1 ** 2 + LC2 ** 2 + 2 * L1 * LC2 * c2)
    m12 = I2_ + M2_ * (LC2 ** 2 + L1 * LC2 * c2)
    return np.array([[m11, m12], [m12, I2_ + M2_ * LC2 ** 2]])


def fig39():
    p = "m11f39_"
    hgt = 340.0
    km = hgt / HM
    VB, s = bvb(404)
    t1, t2a, t2b = -25.0, 80.0, 20.0                            # design values: one posture solid, one faint
    m22 = I2_ + M2_ * LC2 ** 2
    close(m22, 0.10486, 0.00001)                                # line 206 (as used in line 541)
    Pa, Pb = seated(t1, t2a), seated(t1, t2b)
    body, J, org = put(p, s, Pa, hgt, (92.0, 122.0))
    ghost, Jb = arm_svg(p, s, Pb, org, hgt, 0.55)
    sh = J["shoulder"]
    o = [defs(p, s), floor_line(s, 8, 300, J["floor_y"]), stool(s, J), ghost, body]
    res = []
    for t2, Jx, dash in ((t2a, J, None), (t2b, Jb, H.DASH_REF)):
        em, hm = fk(t1, t2)
        elp = math_xy(sh, km, em)
        assert abs(elp[0] - Jx["elbow"][0]) < 0.5 and abs(elp[1] - Jx["elbow"][1]) < 0.5
        a12 = math.radians(t1 + t2)
        c2m = (em[0] + LC2 * math.cos(a12), em[1] + LC2 * math.sin(a12))        # link 2 centre of mass (line 210)
        c2p = math_xy(sh, km, c2m)
        r = math.hypot(*c2m)
        close(r * r, L1 ** 2 + LC2 ** 2 + 2 * L1 * LC2 * math.cos(math.radians(t2)), 1e-12)
        res.append((t2, r, mass_matrix(t2)[0, 0], c2p))
        o.append(dline(s, sh[0], sh[1], c2p[0], c2p[1], O["geometry"], "geom", dash=dash or (1e-6, 0)) if dash else
                 white_under(s, sh[0], sh[1], c2p[0], c2p[1]) + H.line(s, sh[0], sh[1], c2p[0], c2p[1], O["geometry"], "geom"))
        o.append(H.com_mark(s, *c2p))
    # link 1 centre of mass (from the shoulder, line 210) and the elbow distance l_c2 of the solid arm
    c1p = math_xy(sh, km, (LC1 * math.cos(math.radians(t1)), LC1 * math.sin(math.radians(t1))))
    o.append(H.com_mark(s, *c1p))
    o.append(H.joint_centre(s, *sh))
    o.append(H.joint_centre(s, *J["elbow"]))
    o.append(lab(s, c1p[0] - s(2), c1p[1] + s(24), "m₁", "label2", I["primary"], "middle"))
    c2s = res[0][3]
    o.append(lab(s, c2s[0] + s(2), c2s[1] - s(11), "m₂", "label2", I["primary"], "middle"))
    o.append(lines(s, 214.0, 22, ["M₁₁ = I₁ + I₂ + m₁ℓc₁² + m₂r²", "r² = ℓ₁² + ℓc₂² + 2ℓ₁ℓc₂cos θ₂"], lead=1.4))
    o.append(lines(s, 214.0, 192, [f"solid arm, θ₂ = {t2a:.0f}°:", f"r = {res[0][1]:.3f} m, M₁₁ = {res[0][2]:.3f}",
                                   f"faint arm, θ₂ = {t2b:.0f}°:", f"r = {res[1][1]:.3f} m, M₁₁ = {res[1][2]:.3f}",
                                   f"M₂₂ = I₂ + m₂ℓc₂² = {m22:.3f}", "at every θ₂ (all in kg m²)"], lead=1.4))
    o.append(lab(s, 214.0, 306, "blue line: r (to m₂ centre)", "label2", I["secondary"]))
    o.append(credit(s, VB))
    aria = ("A seated skeleton seen from the side, facing right, with the two-link arm bent at the elbow. A centre-of-mass "
            "mark sits on the upper arm, 0.15 m from the shoulder (m1), and one on the forearm, 0.22 m from the elbow (m2). "
            f"A blue line from the shoulder to the centre of m2 has length r = {res[0][1]:.3f} m with the elbow bent "
            f"{t2a:.0f} degrees; a faint second arm with the elbow bent {t2b:.0f} degrees has r = {res[1][1]:.3f} m. "
            "r squared = l1 squared + lc2 squared + 2 l1 lc2 cos theta2, so M11 depends on theta2: "
            f"{res[0][2]:.3f} against {res[1][2]:.3f} kg m squared. M22 = I2 + m2 lc2 squared = {m22:.3f} kg m squared is "
            "the same for every theta2, because link 2 turns about the elbow at a fixed radius lc2.")
    return finish(VB, aria, s, o)


FIGS[39] = (r"D9: the mass matrix. Derive the mass matrix $M(\mathbf q)$ o", fig39)


# ================================================================ svg #40  D10 endpoint stiffness
KQ = np.diag([40.0, 20.0])                                      # N m/rad, design values (the text states no K_q)


def fig40():
    p = "m11f40_"
    hgt = 340.0
    km = hgt / HM
    VB, s = bvb(400)
    t1, t2 = -20.0, 70.0                                        # design values: a non-singular posture
    P = seated(t1, t2)
    body, J, org = put(p, s, P, hgt, (92.0, 122.0))
    sh, el, hd = J["shoulder"], J["elbow"], J["fingertip"]
    Jm = jac(math.radians(t1), math.radians(t2))
    Ji = np.linalg.inv(Jm)
    Kx = Ji.T @ KQ @ Ji                                         # D10: K_x = J^-T K_q J^-1 (line 530)
    close(float(np.abs(Kx - Kx.T).max()), 0.0, 1e-9)
    dp = np.array([0.003, -0.002])                              # check: the force through the chain equals -K_x dp
    dF = Ji.T @ (-KQ @ (Ji @ dp))
    close(float(np.abs(dF + Kx @ dp).max()), 0.0, 1e-12)
    w, V = np.linalg.eigh(Kx)
    em, hm = fk(t1, t2)
    assert abs(math_xy(sh, km, hm)[0] - hd[0]) < 0.5 and abs(math_xy(sh, km, em)[1] - el[1]) < 0.5
    stiff = V[:, 1]
    ang = math.degrees(math.atan2(stiff[1], stiff[0])) % 180
    o = [defs(p, s), floor_line(s, 8, 300, J["floor_y"]), stool(s, J), body]
    o.append(poly(s, [sh, el, hd], I["primary"], "ref"))
    # joint stiffness: dotted rings (torsional springs)
    for c in (sh, el):
        o.append(f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{s(15):.2f}" fill="none" stroke="#fff" stroke-width="{s(4.5):.2f}"/>'
                 f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{s(15):.2f}" fill="none" stroke="{O["force"]}" '
                 f'stroke-width="{s(2.2):.2f}" stroke-dasharray="{s(2.5):.1f} {s(3):.1f}" stroke-linecap="round"/>')
        o.append(H.joint_centre(s, *c))
    # endpoint stiffness ellipse: the force K_x dp for every small displacement dp of one length; drawn so the longest
    # semi-axis is 55 px (the shape is the point, the eigenvalues are in the text)
    ph = np.linspace(0, 2 * np.pi, 97)
    Fe = Kx @ np.vstack([np.cos(ph), np.sin(ph)])
    kf = 55.0 / w[1]
    ex, ey = hd[0] + kf * Fe[0], hd[1] - kf * Fe[1]
    o.append(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in zip(ex, ey))}" fill="{O["force"]}" fill-opacity="0.12" stroke="none"/>')
    o.append(poly(s, list(zip(ex, ey)), O["force"], "geom"))
    o.append(dot(s, hd[0], hd[1], I["primary"], 3.5))
    x0 = 252.0
    KQs, KXs = f"K{sb('q', s)}", f"K{sb('x', s)}"
    o.append(f'<circle cx="{x0 + s(10):.2f}" cy="{22:.2f}" r="{s(7):.2f}" fill="none" stroke="{O["force"]}" '
             f'stroke-width="{s(2.2):.2f}" stroke-dasharray="{s(2.5):.1f} {s(3):.1f}" stroke-linecap="round"/>')
    o.append(lines(s, x0 + 26, 20, [f"joint stiffness {KQs}", "(design values)"]))
    o.append(swatch(s, x0, 62, O["force"], None, "geom"))
    o.append(lines(s, x0 + 26, 66, [f"endpoint stiffness {KXs}", "(long axis: stiffest)"]))
    o.append(lines(s, 214.0, 176, [f"{KQs} = diag(40, 20) N m/rad", f"{KXs} = J⁻ᵀ {KQs} J⁻¹ ="]))
    o.append(lines(s, 214.0, 214, [f"[{Kx[0, 0]:.0f}  {Kx[0, 1]:.0f}; {Kx[1, 0]:.0f}  {Kx[1, 1]:.0f}] N/m".replace("-", "−"),
                                   f"stiffest {w[1]:.0f} N/m at {ang:.0f}°,", f"softest {w[0]:.0f} N/m across it", f"θ₁ = {mn(t1)}°, θ₂ = {t2:.0f}°"],
                   lead=1.4))
    o.append(credit(s, VB))
    aria = ("A seated skeleton seen from the side, facing right, with the arm bent at the elbow, the elbow below the line "
            "from shoulder to hand. A dotted red ring at the shoulder and at the elbow marks the joint stiffness K_q, "
            "diag(40, 20) newton metres per radian (design values). A red ellipse at the hand is the endpoint stiffness "
            "K_x = J^-T K_q J^-1: the force K_x times delta-p for every 1 cm displacement delta-p. "
            f"K_x = [{Kx[0, 0]:.0f}, {Kx[0, 1]:.0f}; {Kx[1, 0]:.0f}, {Kx[1, 1]:.0f}] N/m, stiffest {w[1]:.0f} N/m at "
            f"{ang:.0f} degrees and softest {w[0]:.0f} N/m across it.")
    return finish(VB, aria, s, o)


FIGS[40] = (r"D10: endpoint stiffness. Starting from $\boldsymbol\tau=J^{" + chr(92), fig40)


# ================================================================ svg #43  K3 grip force against friction, and a lift
S_MARGIN = 0.30                                                 # safety margin (line 544)
DASH = (6, 4)


def grip_floor(mu, load=M_CUP * G):
    """Per-pad grip with margin, F_g = (1 + s) L / (2 mu)  (Definition 5, line 268; K3 line 545)."""
    return (1 + S_MARGIN) * load / (2 * mu)


def lift(t):
    """Lab C code (lines 380-385): a(t) = 4 exp(-((t - 0.6)/0.12)^2), load = m (g + a), mu = 0.6."""
    a = 4.0 * np.exp(-(((t - 0.6) / 0.12) ** 2))
    load = M_CUP * (G + a)
    return load, grip_floor(0.6, load), load / (2 * 0.6)


def fig43():
    p = "m11f43_"
    VB, s = bvb(506)
    for mu_i, ref in ((0.6, 5.31), (0.2, 15.9), (0.1, 31.9)):   # K3 solution, line 545
        close(grip_floor(mu_i), ref, 0.05)
    hgt = 200.0
    km = hgt / HM
    Pb = seated(-15.0, 55.0)
    body, J, org = put(p, s, Pb, hgt, (46.0, 84.0))
    cw = 0.075 * hgt
    hd = J["fingertip"]
    base = (hd[0] + cw * 0.15, hd[1] + 0.62 * cw * 1.15)
    o = [defs(p, s), floor_line(s, 6, 150, J["floor_y"]), stool(s, J), body, cup(s, base[0], base[1], cw)]
    o.append(lab(s, 78, J["floor_y"] + s(18), "pinch grip: two pads", "label2", I["secondary"], "middle"))
    # panel 1: the sweep
    P1 = Plot(s, (222, 34, 388, 176), (0.1, 0.8), (0, 35))
    mu = np.linspace(0.1, 0.8, 141)
    fg = grip_floor(mu)
    o.append(P1.axes([(v, f"{v:g}") for v in (0.1, 0.2, 0.4, 0.6, 0.8)], [(v, f"{v}") for v in (0, 10, 20, 30)],
                     "friction μ", "grip per pad (N)", grid=(10, 20, 30), ytx=176))
    o.append(P1.curve(mu, fg, SER[1]))
    for v, dx, dy, an in ((0.1, 8, 4, "start"), (0.2, 8, -6, "start"), (0.6, 0, -10, "middle")):
        o.append(P1.dot(v, grip_floor(v), SER[1]))
        o.append(plabel(s, P1.X(v) + dx, P1.Y(grip_floor(v)) + dy, f"{grip_floor(v):.2f} N" if v == 0.6 else f"{grip_floor(v):.1f} N", "label2", I["primary"], an))
    o.append(plabel(s, P1.X(0.30), P1.Y(27.5), f"F{sub('g', s, 'label2')} = (1 + s) mg / 2μ", "label2", I["primary"]))
    o.append(plabel(s, P1.X(0.30), P1.Y(27.5) + 16, "s = 0.3, m = 0.5 kg", "label2", I["secondary"]))
    # panel 2: the lift at mu = 0.6
    P2 = Plot(s, (62, 288, 388, 408), (0, 1.5), (0, 12))
    tt = np.linspace(0, 1.5, 181)
    load, grip, floor_ = lift(tt)
    close(float(grip[0]), 5.31, 0.005)
    o.append(legend(s, 14, 262, [(SER[1], "grip F" + sub("g", s, "label2") + " per pad", None), (SER[0], "load L", None),
                                 (I["secondary"], "slip floor L/2μ", DASH)]))
    o.append(P2.axes([(v, f"{v:.1f}") for v in (0, 0.5, 1.0, 1.5)], [(v, f"{v}") for v in (0, 3, 6, 9, 12)],
                     "time t (s), lift at μ = 0.6", "force (N)", grid=(3, 6, 9, 12), ytx=22))
    o.append(P2.curve(tt, floor_, I["secondary"], multi=True, dash=DASH))
    o.append(P2.curve(tt, load, SER[0], multi=True))
    o.append(P2.curve(tt, grip, SER[1], multi=True))
    j = int(np.argmax(grip))
    o.append(plabel(s, P2.X(0.74), P2.Y(grip[j]) - 4, f"grip peak {grip[j]:.1f} N", "label2", I["primary"]))
    o.append(plabel(s, P2.X(0.04), P2.Y(11.2), "grip tracks the load pulse, margin kept", "label2", I["secondary"]))
    o.append(credit(s, VB))
    aria = ("Top left, a seated skeleton (Lynch art) holds a cup between thumb and finger. Top right, the grip force per "
            "pad against friction mu from 0.1 to 0.8, with a 30 percent safety margin and a 0.5 kg cup: a hyperbola, "
            f"{grip_floor(0.6):.2f} N at mu 0.6, {grip_floor(0.2):.1f} N at 0.2 and {grip_floor(0.1):.1f} N at 0.1, steepest "
            "where friction is smallest. Below, a 1.5 second lift at mu 0.6: the load rises with an acceleration pulse "
            f"peaking at 4 metres per second squared and the grip rises with it, from {grip[0]:.2f} to {grip[j]:.1f} N, "
            "a constant 30 percent above the dashed slip floor.")
    hv1 = hov(P1, mu[::2], [fg[::2]], lambda i: f"μ = {mu[::2][i]:.2f}: grip {fg[::2][i]:.1f} N per pad")
    hv2 = hov(P2, tt, [grip, load, floor_], lambda i: f"t = {tt[i]:.2f} s: grip {grip[i]:.2f}, load {load[i]:.2f}, "
                                                    f"slip floor {floor_[i]:.2f} N")
    return finish(VB, aria, s, o, H.hover_attr([(P1.box, hv1), (P2.box, hv2)]))


FIGS[43] = ("K3: grip force with a slip reflex (simulation + sensitivity)", fig43)


# ================================================================ svg #44  K4 the most dexterous reach distance
def w_of_r(r):
    c2 = (r * r - L1 ** 2 - L2 ** 2) / (2 * L1 * L2)
    return L1 * L2 * np.sqrt(np.clip(1 - c2 * c2, 0.0, None))


def fig44():
    p = "m11f44_"
    VB, s = bvb(520)
    r_star = math.hypot(L1, L2)
    close(r_star, 0.541, 0.0005)                                # K4 solution, line 549
    close(L1 * L2, 0.135, 1e-9)
    th_lo, th_hi = math.degrees(math.asin(0.95)), 180 - math.degrees(math.asin(0.95))
    close(th_lo, 71.8, 0.05)
    close(th_hi, 108.2, 0.05)
    rr = lambda th_: math.sqrt(L1 ** 2 + L2 ** 2 + 2 * L1 * L2 * math.cos(math.radians(th_)))      # noqa: E731
    r_lo, r_hi = rr(th_hi), rr(th_lo)
    close(r_lo, 0.46, 0.005)
    close(r_hi, 0.61, 0.005)
    close(100 * (r_hi - r_lo), 16, 0.5)
    P = Plot(s, (62, 34, 388, 196), (0.15, 0.75), (0, 0.15))
    r = np.linspace(0.15, 0.75, 241)
    w = w_of_r(r)
    close(float(w.max()), 0.135, 1e-4)
    o = [defs(p, s)]
    o.append(f'<rect x="{P.X(r_lo):.1f}" y="{P.y1:.1f}" width="{P.X(r_hi) - P.X(r_lo):.1f}" height="{P.y0 - P.y1:.1f}" '
             f'fill="{O["geometry"]}" opacity="0.10"/>')
    o.append(P.axes([(v, f"{v:.2f}") for v in (0.15, 0.30, 0.45, 0.60, 0.75)], [(v, f"{v:.2f}") for v in (0, 0.05, 0.10, 0.15)],
                    "reach r (m)", "manipulability w (m²)", grid=(0.05, 0.10, 0.15), ytx=18))
    o.append(P.curve(r, w, SER[0]))
    o.append(P.dot(r_star, 0.135, SER[0]))
    o.append(plabel(s, P.X(r_star), P.Y(0.135) - 9, "max 0.135 m² at 0.541 m", "label2", I["primary"], "middle"))
    xm = (P.X(r_lo) + P.X(r_hi)) / 2
    o.append(plabel(s, xm, P.Y(0.075), "within 5%:", "label2", I["secondary"], "middle"))
    o.append(plabel(s, xm, P.Y(0.075) + 15, "0.46–0.61 m", "label2", I["secondary"], "middle"))
    # the best posture: the right-angle elbow at r = 0.541 m
    hgt = 224.0
    km = hgt / HM
    t1, t2 = ik(r_star, 0.0)
    close(t2, 90.0, 1e-6)
    Pb = seated(t1, t2)
    body, J, org = put(p, s, Pb, hgt, (62.0, 300.0))
    sh, el, hd = J["shoulder"], J["elbow"], J["fingertip"]
    em, hm = fk(t1, t2)
    assert abs(math_xy(sh, km, hm)[0] - hd[0]) < 0.5 and abs(math_xy(sh, km, hm)[1] - hd[1]) < 0.5
    o += [floor_line(s, 8, 190, J["floor_y"]), stool(s, J), body]
    o.append(dline(s, sh[0], sh[1], hd[0], hd[1], O["geometry"], "geom"))
    o.append(poly(s, [sh, el, hd], I["primary"], "ref"))
    ext = (el[0] + (el[0] - sh[0]) * 0.30, el[1] + (el[1] - sh[1]) * 0.30)
    o.append(dline(s, el[0], el[1], ext[0], ext[1], O["geometry"], "ref"))
    o.append(arc_arrow(s, p, el[0], el[1], 0.10 * km, sc_ang(t1), sc_ang(t1 + t2), "geometry", head=False, w="geom"))
    q = pol(el, 0.10 * km + s(16), sc_ang(t1 + t2 / 2))
    o.append(lab(s, q[0], q[1] + s(5), "90°", "label2", I["primary"], "middle"))
    o.append(H.joint_centre(s, *sh))
    o.append(H.joint_centre(s, *el))
    o.append(dot(s, hd[0], hd[1], I["primary"], 3.5))
    mid = ((sh[0] + hd[0]) / 2, (sh[1] + hd[1]) / 2)
    o.append(lab(s, mid[0], mid[1] - s(8), it("r"), "label", I["primary"], "middle"))
    o.append(lines(s, 214.0, 262, ["best posture:", "right-angle elbow,", "r² = ℓ₁² + ℓ₂²,", "r = 0.541 m", "w = ℓ₁ℓ₂ = 0.135 m²"], lead=1.4))
    o.append(lines(s, 214.0, 366, ["|sin θ₂| ≥ 0.95 for", f"θ₂ = {th_lo:.1f}° to {th_hi:.1f}°:", f"a {100 * (r_hi - r_lo):.0f} cm band of r;", "w = 0 at r = 0.15, 0.75 m"], lead=1.4,
                   fill=I["secondary"]))
    o.append(credit(s, VB))
    aria = ("Top, manipulability w = l1 l2 |sin theta2| against reach r from 0.15 to 0.75 metres: an arch that is zero at "
            "the folded and the straight arm and peaks at 0.135 square metres at r = 0.541 m, where theta2 is 90 degrees. "
            "A pale blue band marks 0.46 to 0.61 m, a 16 cm range in which w stays within 5 percent of the maximum. "
            "Below, a seated skeleton (Lynch art) with the arm in the best posture, a right-angle elbow, the hand 0.541 m "
            "from the shoulder on a dashed blue line.")
    hv = hov(P, r[::2], [w[::2]], lambda i: f"r = {r[::2][i]:.3f} m: w = {w[::2][i]:.3f} m²")
    return finish(VB, aria, s, o, H.hover_attr(P.box, hv))


FIGS[44] = ("K4: the most dexterous reach distance (optimisation). Manipu", fig44)


# ================================================================ svg #45 K5 and #47 K7: the three-link arm (l_i = 0.25 m)
Q0 = np.array([0.4, 1.90, 0.3])                                 # rad, K5 / K7 (lines 553, 561)


def no_near_arm(P):
    """A copy of P without its near arm (the body that a separately drawn arm belongs to)."""
    P2 = LB.Pose(P.view)
    P2.segs = [q for q in P.segs if not (q[0].startswith("arm_") and not q[5])]
    P2.j, P2.com, P2.anchor, P2.floor_y = P.j, P.com, P.anchor, P.floor_y
    return P2


def k5_run(t_keep, dt=1e-3, t_end=4.0, ke=50.0, kh=3.0):
    """K5 (line 553): q' = J+ ke e - (I - J+J) kh grad H, H = (theta2 - 1)^2 / 2; returns {t: q} and the fingertip error."""
    p0 = fk3(Q0)[2]
    q = Q0.copy()
    out = {0.0: q.copy()}
    keep = {round(x / dt) for x in t_keep}
    err = 0.0
    for i in range(1, round(t_end / dt) + 1):
        Jm = jac3(q)
        Jp = np.linalg.pinv(Jm)
        e = p0 - fk3(q)[2]
        q = q + dt * (Jp @ (ke * e) - (np.eye(3) - Jp @ Jm) @ (kh * np.array([0.0, q[1] - 1.0, 0.0])))
        if i in keep:
            out[round(i * dt, 6)] = q.copy()
        err = float(np.linalg.norm(p0 - fk3(q)[2]))
    return out, err


def k7_run(s_keep, dt=1e-3, s_end=1.0):
    """K7 (line 561): q' = n, the unit null vector (smallest right-singular vector, sign continued)."""
    q = Q0.copy()
    ref = null_unit(q)
    out = {0.0: q.copy()}
    keep = {round(x / dt) for x in s_keep}
    drift = 0.0
    p0 = fk3(Q0)[2]
    for i in range(1, round(s_end / dt) + 1):
        n = null_unit(q, ref=ref)
        ref = n
        q = q + dt * n
        drift = max(drift, float(np.linalg.norm(fk3(q)[2] - p0)))
        if i in keep:
            out[round(i * dt, 6)] = q.copy()
    return out, q, drift, ref


def three_scene(p, s, hgt, shoulder_xy):
    """Seated body without its near arm, plus the arm drawing helper. Returns (body svg, J, org, km, draw_arm)."""
    km = hgt / HM
    P0 = no_near_arm(seated(*np.degrees(Q0), k=K3L))
    body, J, org = put(p, s, P0, hgt, shoulder_xy)

    def draw_arm(q, op=1.0):
        Pq = seated(*np.degrees(q), k=K3L)
        g, Jq = arm_svg(p, s, Pq, org, hgt, op)
        pts = fk3(q)
        for key, pt in zip(("elbow", "wrist", "fingertip"), pts):
            xy = math_xy(J["shoulder"], km, pt)
            assert abs(xy[0] - Jq[key][0]) < 0.5 and abs(xy[1] - Jq[key][1]) < 0.5, (key, xy, Jq[key])
        return g, Jq
    return body, J, org, km, draw_arm


def links(s, sh, Jq, dash=None):
    """The three links as thin ink lines over the art, with the elbow and wrist marked."""
    pts = [sh, Jq["elbow"], Jq["wrist"], Jq["fingertip"]]
    return poly(s, pts, I["primary"], "ref", dash) + "".join(dot(s, *q, I["primary"], 2.6) for q in pts[1:3])


def fig45():
    p = "m11f45_"
    hgt = 380.0
    VB, s = bvb(474)
    ts = (0.0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0)
    run, err = k5_run(ts)
    qf = run[4.0]
    close(Q0[1], 1.90, 1e-12)
    close(qf[1], 1.005, 0.0005)                                 # line 553: elbow 1.900 -> 1.005 rad
    close(err, 6e-11, 3e-11)                                    # line 553: 6e-11 m
    body, J, org, km, draw_arm = three_scene(p, s, hgt, (122.0, 176.0))
    sh = J["shoulder"]
    p0 = fk3(Q0)[2]
    tgt = math_xy(sh, km, p0)
    ghost, Jg = draw_arm(Q0, 0.45)
    elg = Jg["elbow"]
    ghost += links(s, sh, Jg, H.DASH_REF)
    o = [defs(p, s), floor_line(s, 8, 300, J["floor_y"]), stool(s, J), body, ghost]
    # the soft limit: the forearm direction at theta2 = 2.0 rad (dashed orange ray from the start elbow)
    a_lim = math.degrees(Q0[0] + 2.0)
    ln = 0.25 * km * 0.9
    lim = (elg[0] + ln * math.cos(math.radians(a_lim)), elg[1] - ln * math.sin(math.radians(a_lim)))
    o.append(dline(s, elg[0], elg[1], lim[0], lim[1], O["flag"], "geom"))
    o.append(lab(s, 8, lim[1] + s(12), "soft limit 2.0 rad", "label2", I["primary"], "start"))
    o.append(leader(s, 8 + s(100), lim[1] + s(6), lim[0] - s(2), lim[1] + s(1)))
    frames = []
    for k, tt in enumerate(ts):
        q = run[tt]
        g, Jq = draw_arm(q)
        frames.append(H.frame(k, len(ts) - 1, g + links(s, sh, Jq) +
                              lab(s, 392.0, 22, f"t = {tt:g} s: elbow {q[1]:.3f} rad", "label2", I["primary"], "end")))
    o += frames
    o.append(ring(s, tgt[0], tgt[1], O["flag"], 6.5))
    o.append(H.joint_centre(s, *sh))
    o.append(lab(s, tgt[0], tgt[1] - s(13), "fingertip fixed", "label2", I["primary"], "middle"))
    x0 = 190.0
    o.append(lines(s, x0, 70, ["three links, ℓᵢ = 0.25 m", "q₀ = (0.4, 1.90, 0.3) rad", "faint arm: start, elbow 1.90",
                                f"solid arm: end, elbow {qf[1]:.3f}", "fingertip error 6×10⁻¹¹ m"], lead=1.4))
    kh_, ke_ = f"k{sb('H', s)}", f"k{sb('e', s)}"
    o.append(lines(s, x0, 212, [f"q̇ = J⁺ {ke_} e − (I−J⁺J) {kh_} ∇H", f"H = ½(θ₂ − 1.0)², {ke_} = 50 s⁻¹,", f"{kh_} = 3 s⁻¹, Δt = 1 ms, 4 s"],
                   fill=I["secondary"], lead=1.4))
    o.append(credit(s, VB, " Three links of 0.25 m: the art is stretched along each segment."))
    aria = ("A seated skeleton seen from the side, facing right, with a three-link arm, each link 0.25 m, raised so the "
            "fingertip is behind and above the shoulder, marked by an orange ring: fingertip fixed. A faint arm shows the "
            "start, elbow at 1.90 radians, close to a dashed orange soft limit at 2.0 radians; the solid arm is the end, "
            f"elbow at {qf[1]:.3f} radians, after the null-space solve of 4 seconds. The fingertip error stays at "
            "6 times 10 to the minus 11 metres. A slider and a Play button step the arm through time.")
    return finish(VB, aria, s, o, H.frames_attr("t (s)", [f"{x:g}" for x in ts], len(ts) - 1))


FIGS[45] = ("K5: resolving redundancy off a joint limit (inverse solve wi", fig45)


def fig47():
    p = "m11f47_"
    hgt = 380.0
    VB, s = bvb(474)
    ss = tuple(round(0.1 * k, 1) for k in range(11))
    run, qf, drift, nvec = k7_run(ss)
    nref = np.array([0.1411, -0.5272, 0.8379])
    close(float(np.abs(null_unit(Q0, ref=nref) - nref).max()), 0.0, 1e-4)
    d = np.degrees(qf - Q0)
    close(d[0], 15.4, 0.05)
    close(d[1], -34.0, 0.05)
    close(d[2], 43.2, 0.05)                                     # line 561
    close(drift, 3.1e-5, 0.1e-5)
    body, J, org, km, draw_arm = three_scene(p, s, hgt, (122.0, 176.0))
    sh = J["shoulder"]
    tgt = math_xy(sh, km, fk3(Q0)[2])
    ghost, Jg = draw_arm(Q0, 0.45)
    ghost += links(s, sh, Jg, H.DASH_REF)
    o = [defs(p, s), floor_line(s, 8, 300, J["floor_y"]), stool(s, J), body, ghost]
    # the path of the elbow through the self-motion (a polyline over the frames)
    path = [math_xy(sh, km, fk3(run[x])[0]) for x in ss]
    o.append(poly(s, path, O["flag"], "geom", H.DASH_REF))
    frames = []
    for k, x in enumerate(ss):
        q = run[x]
        g, Jq = draw_arm(q)
        frames.append(H.frame(k, len(ss) - 1, g + links(s, sh, Jq) +
                              lab(s, 392.0, 22, f"s = {x:.1f} s: Δθ₂ = {mn(np.degrees(q[1] - Q0[1]), '{:.1f}')}°", "label2", I["primary"], "end")))
    o += frames
    o.append(ring(s, tgt[0], tgt[1], O["flag"], 6.5))
    o.append(H.joint_centre(s, *sh))
    o.append(lab(s, tgt[0], tgt[1] - s(13), "fingertip", "label2", I["primary"], "middle"))
    x0 = 190.0
    o.append(lines(s, x0, 70, ["q̇ = n, the unit null vector", "n = (0.1411, −0.5272, 0.8379)", "for 1.0 s, Δt = 1 ms:",
                                f"Δq = ({d[0]:+.1f}, {d[1]:+.1f}, {d[2]:+.1f})°".replace("-", "−"),
                                f"fingertip drift {drift * 1e5:.1f}×10⁻⁵ m"], lead=1.4))
    o.append(lines(s, x0, 188, ["faint arm: start; orange path:", "the elbow; the fingertip stays", "on the ring (drift is the",
                                "step truncation, not motion)"], fill=I["secondary"], lead=1.4))
    o.append(credit(s, VB, " Three links of 0.25 m: the art is stretched along each segment."))
    aria = ("A seated skeleton seen from the side, facing right, with a three-link arm, each link 0.25 m, raised so the "
            "fingertip is behind and above the shoulder, marked by an orange ring. A faint arm shows the start. A dashed "
            "orange path follows the elbow while the joints move along the null vector n = (0.1411, -0.5272, 0.8379) for "
            f"1 second; the solid arm is the end, with the joints turned by ({d[0]:+.1f}, {d[1]:+.1f}, {d[2]:+.1f}) degrees, "
            f"the elbow angle alone by {d[1]:+.1f} degrees, while the fingertip drifts only {drift * 1e5:.1f} times 10 to the "
            "minus 5 metres. A slider and a Play button step the arm through the motion.")
    return finish(VB, aria, s, o, H.frames_attr("s (s)", [f"{x:.1f}" for x in ss], len(ss) - 1))


FIGS[47] = ("K7: a self-motion that moves nothing (null-space simulation)", fig47)


# ================================================================ svg #46  K6 the strongest push (force polygon)
TAU_MAX = 15.0                                                  # N m per joint (Appendix line 657)


def force_box(target, up=True):
    """F = J^-T tau over the torque box |tau_i| <= 15: (J^-T, vertices of the parallelogram, F_y max, F_x max)."""
    t1, t2 = ik(*target, up=up)
    A = np.linalg.inv(jac(math.radians(t1), math.radians(t2))).T
    V = np.array([A @ np.array([a, b]) for a, b in ((1, 1), (1, -1), (-1, -1), (-1, 1))]) * TAU_MAX
    return (t1, t2), A, V, TAU_MAX * np.abs(A[1]).sum(), TAU_MAX * np.abs(A[0]).sum()


def fig46():
    p = "m11f46_"
    VB, s = bvb(514)
    (t1, t2), A, V, fy, fx = force_box((0.45, 0.10))
    close(fy, 34.5, 0.05)                                       # line 557
    close(fx, 99.4, 0.05)
    close(float(V[:, 1].max()), fy, 1e-9)
    _, _, V2, fy2, fx2 = force_box((0.73, 0.10))
    close(fy2, 31.9, 0.05)
    close(fx2, 350.5, 0.05)
    close(fy / (M_CUP * G), 7.0, 0.05)                          # "about 7 x the weight of the 0.5 kg cup"
    assert t2 < 0 and abs(t2 + 107.2) < 0.05                    # the elbow-up branch (line 557)
    hgt = 250.0
    km = hgt / HM
    P = seated(t1, t2)
    body, J, org = put(p, s, P, hgt, (84.0, 110.0))
    sh, el, hd = J["shoulder"], J["elbow"], J["fingertip"]
    em, hm = fk(t1, t2)
    assert abs(math_xy(sh, km, hm)[0] - hd[0]) < 0.5 and abs(math_xy(sh, km, hm)[1] - hd[1]) < 0.5
    o = [defs(p, s), floor_line(s, 8, 200, J["floor_y"]), stool(s, J), body]
    o.append(poly(s, [sh, el, hd], I["primary"], "ref"))
    fl = 44.0
    o.append(white_under(s, hd[0], hd[1], hd[0], hd[1] - fl, 5))
    o.append(H.arrow(s, p, hd[0], hd[1], hd[0], hd[1] - fl, "force"))
    o.append(dot(s, hd[0], hd[1], I["primary"], 3.5))
    o.append(lab(s, hd[0] + s(8), hd[1] - fl + s(8), f"F{sb('y', s, 'label')}", "label", I["primary"]))
    o.append(H.joint_centre(s, *sh))
    o.append(H.joint_centre(s, *el))
    o.append(lab(s, el[0] - s(8), el[1] - s(10), "elbow-up", "label2", I["primary"], "end"))
    xr = 212.0
    o.append(lines(s, xr, 30, ["pose (0.45, 0.10) m, elbow-up:", f"θ₁ = {t1:.1f}°, θ₂ = {mn(t2, '{:.1f}')}°", "|τᵢ| ≤ 15 N m at both joints",
                               "F = J⁻ᵀ τ: the torque box maps", "to the polygon below"], lead=1.4))
    o.append(lines(s, xr, 136, [f"F{sb('y', s)} max = {fy:.1f} N, {fy / (M_CUP * G):.0f}× the", f"weight of the 0.5 kg cup;", f"F{sb('x', s)} max = {fx:.1f} N",
                                "(0.73, 0.10) m, straight arm:", f"F{sb('y', s)} max {fy2:.1f} N (lower),",
                                f"F{sb('x', s)} max {fx2:.1f} N (was {fx:.1f})"], lead=1.4, fill=I["secondary"]))
    # the polygon, equal scales on both axes, in a framed box
    kx = 1.46                                                   # px per N, both axes
    x0p, y0p = 200.0, 356.0                                     # figure position of F = (0, 0)
    px = lambda f: x0p + kx * f                                 # noqa: E731
    py = lambda f: y0p - kx * f                                 # noqa: E731
    o.append(f'<rect x="{px(-110):.1f}" y="{py(46):.1f}" width="{px(110) - px(-110):.1f}" height="{py(-46) - py(46):.1f}" '
             f'fill="none" stroke="{GRID}" stroke-width="{s(1):.2f}"/>')
    o.append(H.line(s, px(-110), py(0), px(110), py(0), I["rule"], "ref"))
    o.append(H.line(s, px(0), py(46), px(0), py(-46), I["rule"], "ref"))
    for v in (-100, -50, 0, 50, 100):
        o.append(H.line(s, px(v), py(-46), px(v), py(-46) + 5, I["axis"], "leader"))
        o.append(plabel(s, px(v), py(-46) + 19, mn(v), "tick", I["secondary"], "middle"))
    for v in (-40, -20, 0, 20, 40):
        o.append(H.line(s, px(-110) - 5, py(v), px(-110), py(v), I["axis"], "leader"))
        o.append(plabel(s, px(-110) - 8, py(v) + 4.5, mn(v), "tick", I["secondary"], "end"))
    o.append(plabel(s, px(0), py(-46) + 38, "F" + sub("x", s) + " (N)", "label", I["primary"], "middle"))
    o.append(plabel(s, px(-110), py(46) - 8, "F" + sub("y", s) + " (N)", "label", I["primary"], "start"))
    pts = [(px(a), py(b)) for a, b in V]
    o.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="{O["geometry"]}" fill-opacity="0.12" stroke="none"/>')
    o.append(poly(s, pts + [pts[0]], O["geometry"], "curve_multi"))
    top = V[int(np.argmax(V[:, 1]))]
    o.append(dot(s, px(top[0]), py(top[1]), O["flag"], 4.5))
    o.append(plabel(s, px(top[0]) + 10, py(top[1]) - 6, f"F{sub('y', s, 'label2')} max = {fy:.1f} N", "label2", I["primary"]))
    o.append(credit(s, VB))
    aria = ("Top left, a seated skeleton (Lynch art) seen from the side, facing right, reaches to the point (0.45, 0.10) m "
            f"with the elbow up, theta1 = {t1:.1f} and theta2 = {t2:.1f} degrees; a red arrow at the hand is the vertical "
            "push F_y. Bottom, the force polygon: with each joint torque limited to 15 newton metres the hand force "
            "F = J^-T tau fills a blue parallelogram, equal scales on both axes, reaching F_x = 99.4 N across but only "
            f"F_y = {fy:.1f} N up, about 7 times the weight of the 0.5 kg cup. At the straight-arm pose (0.73, 0.10) m the "
            f"vertical maximum is slightly lower, {fy2:.1f} N, while F_x rises to {fx2:.1f} N.")
    # hover: the polygon's two boundary chains against F_x
    xs = np.linspace(V[:, 0].min(), V[:, 0].max(), 61)
    hv = []
    for xv in xs:
        ys = []
        for i in range(4):
            a, b = V[i], V[(i + 1) % 4]
            if min(a[0], b[0]) - 1e-9 <= xv <= max(a[0], b[0]) + 1e-9 and abs(b[0] - a[0]) > 1e-12:
                ys.append(a[1] + (b[1] - a[1]) * (xv - a[0]) / (b[0] - a[0]))
        lo, hi = min(ys), max(ys)
        hv.append([round(px(xv), 2), [round(py(hi), 2), round(py(lo), 2)], f"F_x = {mn(xv, '{:.0f}')} N: F_y from {mn(lo, '{:.1f}')} to {mn(hi, '{:.1f}')} N"])
    box = [px(-110), py(46), px(110), py(-46)]
    return finish(VB, aria, s, o, H.hover_attr(box, hv))


FIGS[46] = ("K6: strongest push in a direction (constrained optimisation)", fig46)
