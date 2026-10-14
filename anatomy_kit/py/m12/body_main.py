"""Module 12 whole-body figures (main text) and the body-kit problem figures. Exposes the Lynch body kit once per page.

svg #2 (Fig. 1 motor equivalence), #6 (Fig. 5 impedance, peg insertion), and the problem figures (primary class f, 400 px):
#19 (C1 two signatures), #21 (C3 failed self-tickle), #22 (C4 stiffening), #26 (C8 cheap walking), #27 (C9 a few knobs),
#33 (D5 endpoint stiffness), #43 (K3 orienting the ellipse), #51 (K7 uncontrolled manifold).

Numbers (module12.html line numbers):
  Fig. 1: "twice the size" (47): the large signature is drawn exactly 2 x the small one (the same curve, two scales).
  Arm = Module 11's planar two-link arm, l1 = 0.30 m, l2 = 0.45 m (line 53, K3 520, K7 668); stature 1.75 m (course
  reference; the text states none).  Hole = Module 11's reach goal (0.45, 0.10) m from the shoulder, insertion axis 30 deg
  (K3 520, 528-529), joint stiffness K_q = 32.5 I N m/rad (budget 65, K3 520-521).  Computed here, asserted against the
  text: eigenvalues 723 and 88 N/m, ratio 8.24, long axis 31.2 deg (elbow below the hand line) against 173.9 deg (elbow
  above it); along/across ratio at the 30 deg axis 8.21 and 1.63 (K3 521).
  K7 (668-669): q = (81.3, -107.2) deg, hand-x Jacobian row (-0.1000, 0.1966) m/rad, null (0.891, 0.453), task (0.453,
  -0.891); sigma = 0.02 rad, rho = 0.15, N = 4000, seed 0: Var(null) 3.938e-4, Var(task) 6.160e-5, ratio 6.39 (1/rho 6.67).
  C8 (430-432, 234 CPG), C9 (436; Definition 7 line 219: m(t) = sum c_i(t) w_i, 3-5 synergies, ~50 muscles line 49).
Elbow naming: the text calls q = (81.3, -107.2) deg "elbow-down" (K7 668, K3 521/523/553).  With theta_2 < 0 the elbow sits
  0.297 m ABOVE the shoulder, above the shoulder-hand line (Module 11's own naming: theta_2 < 0 = elbow-up).  The figures
  draw the true geometry and name the postures by their elbow, so "elbow up" here is the text's "elbow-down".
Body art: lynch_body.py (Patrick J. Lynch, CC BY 2.5); muscle art for #27: InjuryMap "Leg muscles.svg" (CC BY-SA 4.0),
  crop svg_paths/Leg_muscles_crop_m12syn.svg (crop_art.py ../svg_paths/Leg_muscles.svg m12syn 690 360 1000 700
  --drop "#Names, #Shadow, text" --png 0.4), embedded once in #27 only.
"""
import math

import numpy as np

import house as H
import lynch_body as LB
from m05.body import _read, art_image, finish, inner_svg
from m11.body_main import (arc_arrow, arm_pose, arm_svg, defs, dline, dot, fk, ik, jac, leader, math_xy, pol, put, ring,
                           seated, stool)

SHARED_DEFS = LB.SHARED_DEFS
O, I = H.OVERLAY, H.INK
S0, S1 = H.SERIES[0], H.SERIES[1]
BOXFILL, GRID = "#f7f4ef", "#e6e6e6"
BODY = H.MAX_DISPLAY_H_BODY
HM = 1.75
HOLE = (0.45, 0.10)                       # m from the shoulder (K3 520)
AXIS = 30.0                               # deg, insertion axis (K3 520)
KQ = 32.5                                 # N m/rad per joint (K3 520-521)
Q_DN = ik(*HOLE, up=False)                # (-56.3, 107.2): elbow below the shoulder-hand line (the text's "elbow-up")
Q_UP = ik(*HOLE, up=True)                 # (81.3, -107.2): elbow above the line (the text's "elbow-down")


# ---------------------------------------------------------------- stiffness ellipse (Proposition 5.1)
def kx_of(q, kq=KQ):
    """K_x = J^-T K_q J^-1 for K_q = kq I, q in degrees. Returns the 2x2 matrix in N/m (x forward, y up)."""
    Ji = np.linalg.inv(jac(*np.radians(q)))
    return Ji.T @ (kq * np.eye(2)) @ Ji


def eig(K):
    """(major, minor, long-axis angle in deg from +x, counter-clockwise, 0..180)."""
    w, V = np.linalg.eigh(K)
    return float(w[1]), float(w[0]), float(np.degrees(np.arctan2(V[1, 1], V[0, 1])) % 180.0)


def ratio_along(K, deg=AXIS):
    a = np.array([math.cos(math.radians(deg)), math.sin(math.radians(deg))])
    b = np.array([-a[1], a[0]])
    return float((a @ K @ a) / (b @ K @ b))


K_DN, K_UP = kx_of(Q_DN), kx_of(Q_UP)
E_DN, E_UP = eig(K_DN), eig(K_UP)
assert (round(Q_DN[0], 1), round(Q_DN[1], 1), round(Q_UP[0], 1), round(Q_UP[1], 1)) == (-56.3, 107.2, 81.3, -107.2)
assert (round(E_DN[0]), round(E_DN[1]), round(E_DN[0] / E_DN[1], 2), round(E_DN[2], 1), round(E_UP[2], 1)) == \
    (723, 88, 8.24, 31.2, 173.9), (E_DN, E_UP)
assert (round(ratio_along(K_DN), 2), round(ratio_along(K_UP), 2)) == (8.21, 1.63)


def ellipse(s, c, K, kpx, col, op=0.18, dash=None, w="geom"):
    """Stiffness ellipse at c: the image of the unit displacement circle, semi-axes kpx * eigenvalue (px per N/m)."""
    big, small, ang = eig(K)
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    return (f'<ellipse cx="{c[0]:.2f}" cy="{c[1]:.2f}" rx="{kpx * big:.2f}" ry="{kpx * small:.2f}" '
            f'transform="rotate({-ang:.2f} {c[0]:.2f} {c[1]:.2f})" fill="{col}" fill-opacity="{op}" stroke="{col}" '
            f'stroke-width="{s(H.PX[w]):.2f}"{da}/>')


def ax_pt(c, ang_deg, d):
    """Point d px from c along the math angle ang_deg (counter-clockwise, y up)."""
    return c[0] + d * math.cos(math.radians(ang_deg)), c[1] - d * math.sin(math.radians(ang_deg))


# ---------------------------------------------------------------- scenes
def scene(s, hgt, sh_xy, q, stand=False):
    """The kit body with the near arm at the module's angles q (deg). Returns (svg, J, km, P, org)."""
    P = arm_pose(LB.pose(), *q) if stand else seated(*q)
    body, J, org = put(s, P, hgt, sh_xy)
    km = hgt / HM
    hd = math_xy(J["shoulder"], km, fk(*q)[1])
    assert abs(hd[0] - J["fingertip"][0]) < 0.5 and abs(hd[1] - J["fingertip"][1]) < 0.5, (hd, J["fingertip"])
    return body, J, km, P, org


def peg(s, hand, km, plate=True):
    """Peg held at the hand along the 30 deg axis, and a plate with a hole just ahead of it (schematic sizes)."""
    a_end = ax_pt(hand, AXIS, 0.115 * km)
    # a peg is one stroke: dark rim, light core
    rim = (f'<line x1="{hand[0]:.2f}" y1="{hand[1]:.2f}" x2="{a_end[0]:.2f}" y2="{a_end[1]:.2f}" stroke="{I["secondary"]}" '
           f'stroke-width="{s(10):.2f}" stroke-linecap="round"/>'
           f'<line x1="{hand[0]:.2f}" y1="{hand[1]:.2f}" x2="{a_end[0]:.2f}" y2="{a_end[1]:.2f}" stroke="{BOXFILL}" '
           f'stroke-width="{s(7.2):.2f}" stroke-linecap="round"/>')
    o = [rim]
    if plate:
        hc = ax_pt(hand, AXIS, 0.150 * km)
        n = AXIS + 90.0
        gap, ln, th_ = s(8.5), s(40), s(11)
        for sgn in (+1, -1):
            c0 = ax_pt(hc, n, sgn * gap)
            c1 = ax_pt(hc, n, sgn * (gap + ln))
            o.append(f'<line x1="{c0[0]:.2f}" y1="{c0[1]:.2f}" x2="{c1[0]:.2f}" y2="{c1[1]:.2f}" stroke="{I["secondary"]}" '
                     f'stroke-width="{th_ + s(2):.2f}" stroke-linecap="butt"/>'
                     f'<line x1="{c0[0]:.2f}" y1="{c0[1]:.2f}" x2="{c1[0]:.2f}" y2="{c1[1]:.2f}" stroke="{BOXFILL}" '
                     f'stroke-width="{th_:.2f}" stroke-linecap="butt"/>')
    return "".join(o), a_end


# ================================================================ signatures (#2, #19)
def signature():
    """One cursive-looking trace (prolate cycloid with a decaying loop height and an underline flourish), unit width,
    math frame (y up). The same curve is drawn at two scales, so 'same shape' is literally true."""
    t = np.linspace(0.0, 4.4 * math.pi, 110)
    b = 0.55 + 1.5 * np.exp(-0.11 * t)
    x = 0.5 * t - b * np.sin(t)
    y = -0.62 * b * np.cos(t)
    x = x + 0.45 * y
    xe, ye = x[-1], y[-1]
    ux = np.linspace(xe + 0.2, x[0] - 0.1, 3)
    uy = np.full(3, y.min() - 0.5)
    X = np.concatenate([x, ux])
    Y = np.concatenate([y, uy])
    w = X.max() - X.min()
    return (X - X.min()) / w, (Y - Y.min()) / w


SIG = signature()


def sig_pts(x0, y0, width):
    """Trace with its left end at x0 and its lowest point at y0 (figure units, y down), `width` wide."""
    X, Y = SIG
    return [(x0 + width * a, y0 - width * b) for a, b in zip(X, Y)]


def sig_poly(s, x0, y0, width, col):
    pts = sig_pts(x0, y0, width)
    return (f'<polyline points="{" ".join(f"{a:.2f},{b:.2f}" for a, b in pts)}" fill="none" stroke="{col}" '
            f'stroke-width="{s(H.PX["curve"]):.2f}" stroke-linejoin="round" stroke-linecap="round"/>')


def callout(s, x, y, w, h, width, col, title):
    """Box with a trace of `width` px (enlarged sample), left end centred, and a label under the box."""
    sig_h = width * max(b for b in SIG[1])
    o = [f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{BOXFILL}" stroke="{I["secondary"]}" '
         f'stroke-width="{s(1):.2f}"/>',
         sig_poly(s, x + (w - width) / 2, y + (h + sig_h) / 2, width, col)]
    return "".join(o) + H.label(s, x + w / 2, y + h + s(17), title, "label2", I["primary"], "middle")


Q_PAPER = ik(0.60, -0.26, up=False)       # forearm flat on a desk 0.26 m below the shoulder (design values)
Q_BOARD = ik(0.58, 0.02, up=False)        # arm out to a whiteboard at shoulder height (design values)
W_SMALL, W_LARGE = 42.0, 84.0             # drawn trace widths in the callouts: exactly 1 : 2 ("twice the size", line 47)


def fig2():
    p = "m12f2_"
    hgt, F = 330.0, 352.0
    s = H.Scale(760, 600, max_h=BODY)
    VB = (0, 0, 760, 432)
    km = hgt / HM
    o = [defs(p, s), H.line(s, 20, F, 740, F, I["rule"], "axis")]
    # left: seated at a desk, the forearm rests on the paper, the pen moves with the fingers and wrist
    body, J, _, _, _ = scene(s, hgt, (92.0, F - 0.573 * hgt), Q_PAPER)
    o += [stool(s, J), body]
    hd = J["fingertip"]
    desk_y = J["elbow"][1] + s(14)
    o.append(H.line(s, J["shoulder"][0] + 0.12 * km, desk_y, hd[0] + 0.10 * km, desk_y, I["rule"], "axis",
                    extra='stroke-linecap="round"'))
    o.append(H.line(s, hd[0] + 0.08 * km, desk_y, hd[0] + 0.08 * km, F, I["rule"], "axis"))
    o.append(dot(s, hd[0], hd[1], S1, 4.5))
    o.append(ring(s, *J["wrist"], S1))
    o.append(H.label(s, 190, 36, "paper: small, fingers and wrist", anchor="middle"))
    cx, cy, cw, ch = 262.0, 104.0, 112.0, 74.0
    o.append(leader(s, hd[0] + s(5), hd[1] - s(4), cx, cy + ch / 2, S1))
    o.append(callout(s, cx, cy, cw, ch, W_SMALL, S1, "small signature"))
    o.append(H.label(s, J["wrist"][0] + s(4), J["wrist"][1] + s(34), "wrist and", "label2", I["primary"], "middle"))
    o.append(H.label(s, J["wrist"][0] + s(4), J["wrist"][1] + s(50), "fingers move", "label2", I["primary"], "middle"))
    # right: standing at a whiteboard, the shoulder and elbow sweep the pen
    body2, J2, _, _, _ = scene(s, hgt, (430.0, F - 0.818 * hgt), Q_BOARD, stand=True)
    o.append(body2)
    hd2 = J2["fingertip"]
    by0 = J2["shoulder"][1] - 0.20 * km
    o.append(f'<rect x="{hd2[0] + s(3):.2f}" y="{by0:.2f}" width="{s(46):.2f}" height="{0.64 * km:.2f}" fill="{BOXFILL}" '
             f'stroke="{I["secondary"]}" stroke-width="{s(1.4):.2f}"/>')
    o.append(dot(s, hd2[0], hd2[1], S0, 4.5))
    for q in (J2["shoulder"], J2["elbow"]):
        o.append(ring(s, q[0], q[1], S0))
    o.append(H.label(s, 575, 36, "whiteboard: large, shoulder and elbow", anchor="middle"))
    cx2, cy2, cw2, ch2 = 620.0, 104.0, 124.0, 92.0
    o.append(leader(s, hd2[0] + s(5), hd2[1] - s(3), cx2, cy2 + ch2 / 2, S0))
    o.append(callout(s, cx2, cy2, cw2, ch2, W_LARGE, S0, "signature, twice the size"))
    o.append(H.label(s, J2["elbow"][0] - s(10), J2["elbow"][1] + s(24), "elbow", "label2", I["primary"], "end"))
    o.append(H.label(s, J2["shoulder"][0] - s(12), J2["shoulder"][1] - s(10), "shoulder", "label2", I["primary"], "end"))
    o.append(H.label(s, 380, 384, "both signature samples are enlarged by the same factor; the right one is 2 times the left,",
                     "label2", I["secondary"], "middle"))
    o.append(H.label(s, 380, 402, "and it is the same curve", "label2", I["secondary"], "middle"))
    o.append(LB.credit(s, 20, 414, width=720))
    aria = ("Two skeletons write the same signature. Left, a seated skeleton at a desk rests its forearm on the paper and "
            "writes a small signature with the fingers and wrist (blue marks and blue trace sample). Right, a standing "
            "skeleton writes a signature twice that size on a whiteboard with the shoulder and elbow (red marks and red "
            "trace sample). The two enlarged samples are the same curve at 1 and 2 times the size.")
    return finish(VB, aria, s, o)


# ================================================================ svg #6  Fig. 5 impedance: the peg and the ellipse
KPX = 70.0 / E_DN[0]                         # px per N/m in Fig. 5


def mi(x, nd=1):
    """Number with a true minus sign."""
    return f"{x:.{nd}f}".replace("-", "−")


def fig6():
    p = "m12f6_"
    hgt = 470.0
    s = H.Scale(760, 600, max_h=BODY)
    body, J, km, P, org = scene(s, hgt, (150.0, 140.0), Q_DN)
    VB = (0, 0, 760, round(J["floor_y"] + 66))
    hand = J["fingertip"]
    pegsvg, tip = peg(s, hand, km)
    o = [defs(p, s), H.line(s, 20, J["floor_y"], 740, J["floor_y"], I["rule"], "axis"), stool(s, J), body, pegsvg]
    o.append(dline(s, *ax_pt(hand, AXIS, -0.18 * km), *ax_pt(hand, AXIS, 0.34 * km), I["secondary"]))
    o.append(ellipse(s, hand, K_DN, KPX, O["geometry"]))
    o.append(dot(s, hand[0], hand[1], I["primary"], 3.5))
    p0, p1 = ax_pt(hand, AXIS, 0.17 * km), ax_pt(hand, AXIS, 0.33 * km)
    o.append(H.arrow(s, p, p0[0] - s(2), p0[1] - s(12), p1[0] - s(2), p1[1] - s(12), "force"))
    tmaj = ax_pt(hand, E_DN[2], KPX * E_DN[0])
    tmin = ax_pt(hand, E_DN[2] + 90.0, KPX * E_DN[1])
    lx = 400.0
    o.append(leader(s, tmaj[0] + s(3), tmaj[1] - s(2), lx - s(6), 64.0))
    o.append(H.label(s, lx, 62, "stiff along the insertion axis: 723 N/m", "label"))
    o.append(H.label(s, lx, 80, "the peg is pushed home", "label2", I["secondary"]))
    o.append(leader(s, tmin[0], tmin[1] - s(2), lx - s(6), 112.0))
    o.append(H.label(s, lx, 110, "compliant across it: 88 N/m", "label"))
    o.append(H.label(s, lx, 128, "the peg slides into line instead of jamming", "label2", I["secondary"]))
    o.append(H.label(s, p1[0] + s(8), p1[1] - s(26), "push", "label2", O["force"]))
    for q in (J["shoulder"], J["elbow"]):
        o.append(H.joint_centre(s, *q))
    o.append(H.label(s, J["elbow"][0] + s(12), J["elbow"][1] + s(24), "elbow", "label2", I["secondary"]))
    o.append(H.label(s, J["shoulder"][0] - s(10), J["shoulder"][1] - s(14), "shoulder", "label2", I["secondary"], "end"))
    tb = 196.0
    o.append(H.label(s, lx, tb, "Proposition 5.1", "label2", I["secondary"]))
    o.append(H.label(s, lx, tb + s(20), f"K{H.sub('x', s)} = J⁻ᵀ K{H.sub('q', s)} J⁻¹", "label", I["primary"]))
    kq = f"K{H.sub('q', s, 'label2')}"
    rows = [f"posture: θ₁ = {mi(Q_DN[0])}°, θ₂ = {mi(Q_DN[1])}°",
            "(elbow below the shoulder-to-hand line)",
            f"hand at the hole ({HOLE[0]:.2f}, {HOLE[1]:.2f}) m from the shoulder",
            f"joint stiffness {kq} = {KQ:.1f} I N·m/rad, equal at both joints",
            f"eigenvalues {E_DN[0]:.0f} and {E_DN[1]:.0f} N/m, long axis {E_DN[2]:.1f}° (ratio {E_DN[0] / E_DN[1]:.2f})",
            f"insertion axis {AXIS:.0f}°: along/across stiffness {ratio_along(K_DN):.2f}",
            "ellipse drawn to scale: semi-axes proportional to stiffness"]
    for i, t_ in enumerate(rows):
        o.append(H.label(s, lx, tb + s(46) + i * s(19), t_, "label2", I["primary"] if i < 6 else I["secondary"]))
    o.append(LB.credit(s, 20, VB[3] - 32, width=720))
    aria = ("A seated skeleton, side view facing right, with its arm bent at the elbow, the elbow below the line from "
            "shoulder to hand, holds a peg at a plate with a hole. A thin blue stiffness ellipse at the hand is elongated "
            "along the 30 degree insertion axis: stiff, 723 newtons per metre, along the axis and compliant, 88 newtons "
            "per metre, across it. A red arrow pushes the peg along the axis.")
    return finish(VB, aria, s, o)


# ================================================================ problem figures (display width 400 px)
def pscale(h):
    return H.Scale(400, h, display_w=400, max_h=BODY)


def credit_at(s, y, extra=""):
    return LB.credit(s, 10, y, width=336, extra=extra)


def wrap_text(text, n):
    out, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return out + [cur]


# ---------------------------------------------------------------- svg #19  C1 the two signatures
def fig19():
    p = "m12f19_"
    hgt = 250.0
    s = pscale(600)
    km = hgt / HM
    body, J, org = put(s, seated(*Q_BOARD), hgt, (66.0, 70.0))
    ghost, Jg = arm_svg(s, seated(*Q_PAPER), org, hgt, op=0.45)
    VB = (0, 0, 400, round(J["floor_y"] + 112))
    hd, hp = J["fingertip"], Jg["fingertip"]
    wall = hd[0] + s(4)
    desk_y = Jg["elbow"][1] + s(12)
    o = [defs(p, s), H.line(s, 10, J["floor_y"], 390, J["floor_y"], I["rule"], "axis"), stool(s, J)]
    o.append(H.line(s, J["shoulder"][0] + 0.12 * km, desk_y, wall, desk_y, I["rule"], "axis", extra='stroke-linecap="round"'))
    o.append(H.line(s, wall - s(6), desk_y, wall - s(6), J["floor_y"], I["rule"], "axis"))
    top = J["shoulder"][1] - 0.18 * km
    o.append(f'<rect x="{wall:.2f}" y="{top:.2f}" width="{s(14):.2f}" height="{desk_y - top:.2f}" fill="{BOXFILL}" '
             f'stroke="{I["secondary"]}" stroke-width="{s(1.4):.2f}"/>')
    o += [ghost, body]
    o.append(dot(s, hd[0], hd[1], S0, 4))
    o.append(dot(s, hp[0], hp[1], S1, 4))
    for q in (J["shoulder"], J["elbow"]):
        o.append(ring(s, q[0], q[1], S0, 5))
    o.append(ring(s, *Jg["wrist"], S1, 5))
    cx, cw = 196.0, 194.0
    o.append(leader(s, hd[0] + s(8), hd[1] - s(2), cx, 62.0, S0))
    o.append(callout(s, cx, 30.0, cw, 82.0, W_LARGE, S0, "large: shoulder and elbow"))
    o.append(leader(s, hp[0] + s(8), hp[1], cx, 170.0, S1))
    o.append(callout(s, cx, 142.0, cw, 62.0, W_SMALL, S1, "small: fingers and wrist"))
    o.append(H.label(s, 293, 242, "same curve at 2× and 1× size", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 10, 22, "solid arm: large; faint arm: small", "label2", I["secondary"]))
    o.append(credit_at(s, VB[3] - 60))
    aria = ("A seated skeleton at a desk in front of a whiteboard. The solid arm reaches the board at shoulder height "
            "(red marks at shoulder and elbow); the faint arm rests on the desk with the wrist and fingers writing "
            "(blue mark). Two enlarged samples at the right show the same signature curve, large in red from the "
            "shoulder and elbow and half the size in blue from the fingers and wrist.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #21  C3 the failed self-tickle
HK = 480.0                                       # stature of the art in this figure
KA = HK / LB.H_U


def seg_use(name, x, y, rot):
    return (f'<g transform="translate({x:.2f} {y:.2f}) scale({KA:.4f}) rotate({rot})" fill="none">'
            f'<use href="#hbody_{name}"/></g>')


def tickle_panel(s, p, y0, own):
    Lf, Lh = LB.L_FORE * KA, LB.L_HAND * KA
    tx, ty = 80.0, y0 + 84.0
    ytf = ty + Lf + Lh + 9.0
    o = [seg_use("arm_fore", 12.0, ytf, -90), seg_use("arm_hand", 12.0 + Lf, ytf, -90),
         seg_use("arm_fore", tx, ty, 0), seg_use("arm_hand", tx, ty + Lf, 0),
         dot(s, tx, ty + Lf + Lh, S1, 4),
         H.label(s, 10, y0 + 18, "your own touch" if own else "another person's touch", "label")]
    bx, by, bw, bh = 14.0, y0 + 40.0, 104.0, 26.0
    gcol = O["neural"] if own else I["muted"]
    dash = "" if own else f' stroke-dasharray="{s(5):.2f} {s(3):.2f}"'
    o.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="{BOXFILL}" stroke="{gcol}" '
             f'stroke-width="{s(1.4):.2f}"{dash}/>')
    o.append(H.label(s, bx + bw / 2, by + 17, "motor command" if own else "no motor command", "label2",
                     I["primary"] if own else I["secondary"], "middle"))
    if own:
        o.append(H.arrow(s, p, bx + bw / 2, by + bh, bx + bw / 2, ty - s(2), "neural"))
    else:
        o.append(H.label(s, tx + s(34), ty + s(12), "their hand", "label2", I["secondary"]))
    fx, fw = 218.0, 120.0
    o.append(f'<rect x="{fx}" y="{by}" width="{fw}" height="{bh}" fill="{BOXFILL}" stroke="{gcol}" '
             f'stroke-width="{s(1.4):.2f}"/>')
    o.append(H.label(s, fx + fw / 2, by + 17, "forward model", "label2", I["primary"] if own else I["secondary"], "middle"))
    if own:
        o.append(f'<line x1="{bx + bw:.2f}" y1="{by + bh / 2:.2f}" x2="{fx - s(2):.2f}" y2="{by + bh / 2:.2f}" '
                 f'stroke="{O["neural"]}" stroke-width="{s(H.PX["force"]):.2f}" stroke-dasharray="{s(5):.2f} {s(3):.2f}" '
                 f'marker-end="url(#{p}a_neural)"/>')
        o.append(H.label(s, (bx + bw + fx) / 2, by + bh / 2 - s(5), "efference copy", "label2", I["secondary"], "middle"))
        o.append(H.arrow(s, p, fx + fw / 2, by + bh + s(2), fx + fw / 2, y0 + 88.0, "neural"))
    X0, FULL = 218.0, 150.0
    rows = [("touch predicted", O["neural"], 1.0 if own else 0.0, y0 + 98.0),
            ("touch felt", S1, 1.0, y0 + 136.0),
            ("felt − predicted", I["primary"], 0.0 if own else 1.0, y0 + 178.0)]
    for lab, col, v, yy in rows:
        o.append(H.label(s, X0, yy - s(5), lab, "label2", I["primary"]))
        o.append(f'<rect x="{X0}" y="{yy}" width="{max(FULL * v, s(2.5)):.2f}" height="{s(12):.2f}" fill="{col}"/>')
    o.append(H.line(s, X0, y0 + 164.0, X0 + FULL, y0 + 164.0, I["rule"], "leader"))
    if own:
        o.append(H.label(s, X0 + s(10), y0 + 196.0, "≈ 0: no tickle", "label2", I["primary"]))
    else:
        o.append(H.label(s, X0 + FULL, y0 + 206.0, "full size: tickles", "label2", I["primary"], "end"))
    o.append(H.label(s, 10, y0 + 238.0, "the prediction cancels the touch" if own
                     else "nothing is predicted: the touch survives", "label2", I["secondary"]))
    return "".join(o)


def fig21():
    p = "m12f21_"
    s = pscale(600)
    VB = (0, 0, 400, 606)
    o = [defs(p, s), tickle_panel(s, p, 0.0, True), H.line(s, 10, 254, 390, 254, GRID, "axis"),
         tickle_panel(s, p, 262.0, False),
         H.label(s, 10, 528, "bars: size of each signal (schematic)", "label2", I["secondary"]),
         credit_at(s, 546)]
    aria = ("Two panels, each showing a forearm lying flat and a hand touching it from above. Top, your own touch: your "
            "motor command drives the touching hand and an efference copy goes to a forward model, which predicts the "
            "touch. Bars show the touch predicted and the touch felt at equal size, so felt minus predicted is about "
            "zero and there is no tickle. Bottom, another person's touch: no command of yours, nothing is predicted, so "
            "felt minus predicted is the full touch and it tickles.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #22  C4 stiffening in the dark
KPX22 = 30.0 / E_DN[0]
COCON = 2.0                                   # co-contraction doubles K_q (design value; the text gives no factor)


def fig22():
    p = "m12f22_"
    hgt = 270.0
    s = pscale(600)
    body, J, km, P, org = scene(s, hgt, (84.0, 100.0), Q_DN)
    VB = (0, 0, 400, 380)
    hand = J["fingertip"]
    o = [defs(p, s), H.line(s, 10, J["floor_y"], 390, J["floor_y"], I["rule"], "axis"), stool(s, J), body]
    o.append(ellipse(s, hand, COCON * K_DN, KPX22, O["force"], op=0.14))
    o.append(ellipse(s, hand, K_DN, KPX22, O["geometry"], op=0.22))
    o.append(dot(s, hand[0], hand[1], I["primary"], 3.5))
    x0 = 206.0
    kq = f"K{H.sub('q', s, 'label2')}"
    for yy, col, t1, t2 in ((54.0, O["geometry"], "relaxed", f"{kq} = {KQ:.1f} I N·m/rad"),
                            (112.0, O["force"], "co-contracted", f"{kq} = {KQ * COCON:.0f} I N·m/rad")):
        o.append(H.line(s, x0, yy - s(5), x0 + s(22), yy - s(5), col, "curve"))
        o.append(H.label(s, x0 + s(30), yy, t1))
        o.append(H.label(s, x0 + s(30), yy + s(18), t2, "label2", I["secondary"]))
    kxs = f"K{H.sub('x', s, 'label2')}"
    o.append(H.label(s, x0, 168, f"{kxs} = J⁻ᵀ {kq} J⁻¹: the same", "label2", I["primary"]))
    o.append(H.label(s, x0, 186, f"shape, scaled by {COCON:.0f}", "label2", I["primary"]))
    o.append(H.label(s, x0, 204, "(the posture J is unchanged)", "label2", I["secondary"]))
    o.append(H.label(s, x0, 228, f"along: {E_DN[0]:.0f} → {COCON * E_DN[0]:.0f} N/m", "label2", I["primary"]))
    o.append(H.label(s, x0, 246, f"across: {E_DN[1]:.0f} → {COCON * E_DN[1]:.0f} N/m", "label2", I["primary"]))
    o.append(H.label(s, 10, 280, "cost: both muscles pull against each other", "label2", I["secondary"]))
    o.append(H.label(s, 10, 298, "(energy, and a dull sense of touch)", "label2", I["secondary"]))
    o.append(credit_at(s, VB[3] - 60))
    aria = ("A seated skeleton with its arm held out, the elbow below the shoulder-to-hand line. At the hand are two "
            "nested stiffness ellipses of the same shape and orientation: a small blue one for the relaxed arm and one "
            "twice as large in red for the co-contracted arm, because doubling the joint stiffness doubles the endpoint "
            "stiffness. The posture is unchanged.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #26  C8 cheap walking
def fig26():
    p = "m12f26_"
    hgt = 320.0
    s = pscale(600)
    P = LB.pose(**LB.POSES["gait_heel_strike"])
    body, J = LB.draw(p, s, P, 142.0, 346.0, hgt)
    VB = (0, 0, 400, 430)
    o = [defs(p, s), H.line(s, 10, J["floor_y"], 390, J["floor_y"], I["rule"], "axis"), body]
    cx, cy, r = 300.0, 92.0, 36.0
    o.append(arc_arrow(s, p, cx, cy, r, -90, 250, "neural"))
    o.append(f'<circle cx="{cx:.2f}" cy="{cy - r:.2f}" r="{s(4.5):.2f}" fill="{O["neural"]}" stroke="#fff" '
             f'stroke-width="{s(1.2):.2f}"/>')
    hip = J["hip"]
    end = (hip[0] + s(14), hip[1] - s(10))
    o.append(f'<line x1="{cx - r - s(8):.2f}" y1="{cy:.2f}" x2="{end[0]:.2f}" y2="{end[1]:.2f}" stroke="{O["neural"]}" '
             f'stroke-width="{s(H.PX["force"]):.2f}" stroke-dasharray="{s(6):.2f} {s(4):.2f}" marker-end="url(#{p}a_neural)"/>')
    o.append(H.label(s, cx, cy + r + s(22), "spinal oscillator (CPG)", "label", I["primary"], "middle"))
    o.append(H.label(s, cx, cy + r + s(40), "one turn = one stride", "label2", I["secondary"], "middle"))
    o.append(H.label(s, cx, cy + r + s(56), "dot: heel strike, as drawn", "label2", I["secondary"], "middle"))
    for i, t_ in enumerate(("the higher centre sets only", "a few parameters:", "frequency, amplitude")):
        o.append(H.label(s, 226, 214 + i * s(18), t_, "label2", I["primary"]))
    for i, t_ in enumerate(("feedback only nudges", "the phase; no command for", "each muscle at each instant")):
        o.append(H.label(s, 226, 280 + i * s(18), t_, "label2", I["secondary"]))
    o.append(credit_at(s, VB[3] - 60))
    aria = ("A walking skeleton in side view at heel strike, facing right. At upper right a green ring is a spinal "
            "central pattern generator, one turn per stride with a dot at the heel-strike phase. A dashed green arrow "
            "runs from the oscillator to the hip: the oscillator supplies the stepping rhythm open loop. The higher "
            "centre sets only the frequency and amplitude, and feedback only nudges the phase.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #27  C9 a few knobs, many muscles
CALF2 = (738, 360, 247, 340)                    # crop window of Leg_muscles_crop_m12syn.svg, source units
N_MUSCLES = 50                                  # line 49 ("some fifty muscles")


def fig27():
    p = "m12f27_"
    s = pscale(600)
    VB = (0, 0, 400, 528)
    art = inner_svg(_read("Leg_muscles_crop_m12syn.svg"))
    assert 'id="Names"' not in art and "<text" not in art
    kx_, ax_ = 0.40, 286.0
    art_id = f"{p}art"
    o = [defs(p, s), f'<defs><g id="{art_id}">{art_image("<svg>" + art + "</svg>", CALF2)}</g>'
                     f'<radialGradient id="{p}fade"><stop offset="0.6" stop-color="#fff"/><stop offset="1" stop-color="#000"/>'
                     f'</radialGradient><mask id="{p}mask" maskContentUnits="objectBoundingBox" x="0" y="0" width="1" '
                     f'height="1"><rect x="0" y="0" width="1" height="1" fill="url(#{p}fade)"/></mask></defs>']

    def use_art(y):
        """The crop with soft edges (a radial mask), so the window edge does not read as a cut."""
        return (f'<g mask="url(#{p}mask)"><use href="#{art_id}" transform="translate({ax_ - CALF2[0] * kx_:.2f} '
                f'{y - CALF2[1] * kx_:.2f}) scale({kx_})"/></g>')

    ya = 22.0
    o.append(H.label(s, 10, ya, "independent control: 50 commands", "label"))
    for k in range(N_MUSCLES):
        c, r_ = k % 10, k // 10
        o.append(f'<circle cx="{26 + c * 13.5:.1f}" cy="{ya + 34 + r_ * 13.5:.1f}" r="{s(3.6):.2f}" fill="{O["neural"]}"/>')
    o.append(H.arrow(s, p, 168.0, ya + 62.0, 276.0, ya + 62.0, "dim"))
    o.append(H.label(s, 224, ya + 54, "one command", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 224, ya + 84, "per muscle", "label2", I["secondary"], "middle"))
    o.append(use_art(ya + 8))
    o.append(H.label(s, ax_ + 44, ya + 8 + CALF2[3] * kx_ + s(14), "~50 muscles", "label2", I["primary"], "middle"))
    yb = 236.0
    o.append(H.label(s, 10, yb, "synergies: 3 commands", "label"))
    for i, ang in enumerate((-50.0, 25.0, 100.0)):
        cx_, cy_ = 38 + i * 56.0, yb + 58.0
        o.append(f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="{s(19):.2f}" fill="{BOXFILL}" stroke="{O["neural"]}" '
                 f'stroke-width="{s(2):.2f}"/>')
        nx, ny = pol((cx_, cy_), s(15), ang - 90)
        o.append(H.line(s, cx_, cy_, nx, ny, O["neural"], "force", extra='stroke-linecap="round"'))
        o.append(H.label(s, cx_, cy_ + s(36), "c" + "₁₂₃"[i], "label", I["primary"], "middle"))
    o.append(H.arrow(s, p, 204.0, yb + 58.0, 276.0, yb + 58.0, "dim"))
    o.append(H.label(s, 242, yb + 44, "fixed", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 242, yb + 76, "weights", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 242, yb + 92, "w₁ w₂ w₃", "label2", I["secondary"], "middle"))
    o.append(use_art(yb + 8))
    o.append(H.label(s, ax_ + 44, yb + 8 + CALF2[3] * kx_ + s(14), "~50 muscles", "label2", I["primary"], "middle"))
    o.append(H.label(s, 10, 428, "m(t) = c₁(t) w₁ + c₂(t) w₂ + c₃(t) w₃ (Definition 7)", "label2", I["primary"]))
    o.append(H.label(s, 10, 446, "50 numbers to set become 3; the calf stands for the muscles", "label2", I["secondary"]))
    cr = H.ATTRIBUTION["by-sa"].format(author="InjuryMap", title="Leg muscles.svg",
                                       changes="Cropped, labels removed; schematic commands drawn for this course.")
    o.append(H.credit(s, 10, 466, wrap_text(cr, int(380 / (s(H.PX["credit"]) * 0.47)))))
    aria = ("Two rows. Top, independent control: a grid of 50 green dots, one command per muscle, with an arrow to "
            "a drawing of calf muscles labelled about 50 muscles. Bottom, synergies: three green dials c1, c2 and c3 with an "
            "arrow labelled fixed weights w1, w2, w3 to the same muscle drawing. The 50 numbers to set become 3, because "
            "muscle activation is m(t) equal to the sum of ci(t) times wi.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #33  D5 endpoint stiffness
U_DX = 110.0                                   # deg, direction of the small displacement (design value)
KPX33 = 40.0 / E_DN[0]


def fig33():
    p = "m12f33_"
    hgt = 260.0
    s = pscale(600)
    body, J, km, P, org = scene(s, hgt, (84.0, 96.0), Q_DN)
    VB = (0, 0, 400, round(J["floor_y"] + 164))
    hand = J["fingertip"]
    u = np.array([math.cos(math.radians(U_DX)), math.sin(math.radians(U_DX))])
    Ji = np.linalg.inv(jac(*np.radians(Q_DN)))
    dq = Ji @ u                                                      # step 1: dq = J^-1 dx (rad per m)
    dtau = -KQ * dq                                                  # step 2: dtau = -K_q dq
    dF = Ji.T @ dtau                                                 # step 3: dF = J^-T dtau
    assert np.allclose(dF, -(K_DN @ u))
    o = [defs(p, s), H.line(s, 10, J["floor_y"], 390, J["floor_y"], I["rule"], "axis"), stool(s, J), body]
    o.append(ellipse(s, hand, K_DN, KPX33, O["geometry"], op=0.16))
    dx_end = ax_pt(hand, U_DX, 30.0)
    o.append(H.arrow(s, p, hand[0], hand[1], dx_end[0], dx_end[1], "dim"))
    fv = (KPX33 * dF[0], -KPX33 * dF[1])                             # the tip lies on the ellipse
    o.append(H.arrow(s, p, hand[0], hand[1], hand[0] + fv[0], hand[1] + fv[1], "force"))
    o.append(dot(s, hand[0], hand[1], I["primary"], 3.5))
    o.append(H.label(s, dx_end[0] + s(6), dx_end[1] - s(2), "δx", "label", I["primary"]))
    o.append(H.label(s, hand[0] + fv[0] - s(4), hand[1] + fv[1] + s(16), "δF", "label", O["force"], "end"))
    sh, el, wr = J["shoulder"], J["elbow"], J["wrist"]
    for jt, nxt, idx, base_off, lab_dx in ((sh, el, 0, -120.0, -34.0), (el, wr, 1, -165.0, -34.0)):
        base = math.degrees(math.atan2(nxt[1] - jt[1], nxt[0] - jt[0])) + base_off
        sw = -1.0 if dq[idx] > 0 else 1.0                            # counter-clockwise on the page = angle decreasing
        a1 = base + sw * 55.0
        o.append(arc_arrow(s, p, jt[0], jt[1], s(24), base, a1, "dim"))
        o.append(arc_arrow(s, p, jt[0], jt[1], s(35), a1, base, "force"))       # restoring torque: the other way
        m = pol(jt, s(48), (base + a1) / 2)
        o.append(H.label(s, m[0], m[1] + s(4), "δq" + "₁₂"[idx], "label2", I["primary"], "middle"))
    o.append(H.joint_centre(s, *sh))
    o.append(H.joint_centre(s, *el))
    x0 = 214.0
    rows = [("grey: displacement", O["dim"]), ("red: restoring force, torque", O["force"])]
    for i, (t_, col) in enumerate(rows):
        yy = 40.0 + i * 20.0
        o.append(H.line(s, x0, yy - s(5), x0 + s(20), yy - s(5), col, "curve"))
        o.append(H.label(s, x0 + s(28), yy, t_, "label2", I["primary"]))
    for i, t_ in enumerate(("joint springs resist δq with", "torque δτ; the hand feels δF,", "whose tip is on the ellipse,",
                            "not along −δx")):
        o.append(H.label(s, x0, 100 + i * s(18), t_, "label2", I["secondary"]))
    kq = f"K{H.sub('q', s, 'label2')}"
    ys = J["floor_y"] + 26.0
    chain = ["1.  δq = J⁻¹ δx          (inverse differential kinematics)",
             f"2.  δτ = −{kq} δq          (the joints resist)",
             "3.  δF = J⁻ᵀ δτ          (force-torque duality)",
             f"      = −J⁻ᵀ {kq} J⁻¹ δx = −K{H.sub('x', s, 'label2')} δx"]
    for i, t_ in enumerate(chain):
        o.append(H.label(s, 10, ys + i * s(19), t_, "label2", I["primary"]))
    o.append(credit_at(s, VB[3] - 60))
    aria = ("A seated skeleton with the arm held out and a blue stiffness ellipse at the hand. A grey arrow from the "
            "hand is a small displacement and a red arrow is the restoring force, whose tip lies on the ellipse and is "
            "not opposite the displacement. At the shoulder and elbow, grey arcs show the joint displacement and red arcs "
            "the opposing joint torque. Three steps below derive the endpoint stiffness: joint displacement, joint "
            "torque, endpoint force.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #43  K3 orienting the stiffness ellipse
KPX43 = 58.0 / E_DN[0]


def fig43():
    p = "m12f43_"
    hgt = 260.0
    s = pscale(600)
    body, J, km, P, org = scene(s, hgt, (84.0, 124.0), Q_DN)
    ghost, Jg = arm_svg(s, seated(*Q_UP), org, hgt, op=0.42)
    VB = (0, 0, 400, round(J["floor_y"] + 160))
    hand = J["fingertip"]
    assert abs(Jg["fingertip"][0] - hand[0]) < 0.5 and abs(Jg["fingertip"][1] - hand[1]) < 0.5
    o = [defs(p, s), H.line(s, 10, J["floor_y"], 390, J["floor_y"], I["rule"], "axis"), stool(s, J), ghost, body]
    o.append(dline(s, *ax_pt(hand, AXIS, -0.19 * km), *ax_pt(hand, AXIS, 0.30 * km), I["secondary"]))
    o.append(ellipse(s, hand, K_UP, KPX43, O["dim"], op=0.10, dash=H.DASH_REF))
    o.append(ellipse(s, hand, K_DN, KPX43, O["geometry"], op=0.20))
    o.append(dot(s, hand[0], hand[1], I["primary"], 3.5))
    o.append(ring(s, *Jg["elbow"], O["dim"], 5))
    o.append(ring(s, *J["elbow"], O["geometry"], 5))
    x0 = 206.0
    for yy, col, dash, rows in (
            (118.0, O["geometry"], None, ("elbow down (solid arm)", f"long axis {E_DN[2]:.1f}°",
                                           f"ratio {ratio_along(K_DN):.2f}")),
            (190.0, O["dim"], H.DASH_REF, ("elbow up (faint arm)", f"long axis {E_UP[2]:.1f}°",
                                           f"ratio {ratio_along(K_UP):.2f}"))):
        o.append(H.line(s, x0, yy - s(5), x0 + s(20), yy - s(5), col, "curve", dash=dash))
        o.append(H.label(s, x0 + s(28), yy, rows[0]))
        o.append(H.label(s, x0 + s(28), yy + s(18), rows[1], "label2", I["secondary"]))
        o.append(H.label(s, x0 + s(28), yy + s(35), rows[2], "label2", I["secondary"]))
    tp = ax_pt(hand, AXIS, 0.30 * km)
    o.append(H.label(s, tp[0] + s(8), tp[1] - s(2), "insertion axis, 30°", "label2", I["primary"]))
    ys = J["floor_y"] + 22.0
    kq = f"K{H.sub('q', s, 'label2')}"
    for i, t_ in enumerate((f"hand at the hole ({HOLE[0]:.2f}, {HOLE[1]:.2f}) m; {kq} = {KQ:.1f} I N·m/rad",
                            f"eigenvalues {E_DN[0]:.0f} and {E_DN[1]:.0f} N/m in both postures",
                            "ratio = stiffness along / across the 30° axis",
                            "posture rotates the ellipse; it does not reshape it")):
        o.append(H.label(s, 10, ys + i * s(18), t_, "label2", I["primary"] if i < 3 else I["secondary"]))
    o.append(credit_at(s, VB[3] - 60))
    aria = ("A seated skeleton holds its hand at a hole 0.45 metres ahead of and 0.10 metres above the shoulder, with a "
            "dashed 30 degree insertion axis through the hand. The solid arm has its elbow below the shoulder-to-hand "
            "line and gives a blue stiffness ellipse elongated close to the axis, long axis 31.2 degrees, along-to-across "
            "ratio 8.21. A faint second arm reaches the same hand with the elbow raised and gives a grey dashed ellipse "
            "of the same size turned to 173.9 degrees, ratio 1.63. Same muscles, same effort, different posture.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #51  K7 the uncontrolled manifold
SIGMA, RHO, NTR = 0.02, 0.15, 4000             # K7 668-669
L1_, L2_ = 0.30, 0.45


def k7_data():
    """K7's code (lines 679-695) verbatim in its arithmetic: seed 0, N = 4000."""
    t1, t2 = np.radians(Q_UP)
    Jx = np.array([-L1_ * np.sin(t1) - L2_ * np.sin(t1 + t2), -L2_ * np.sin(t1 + t2)])
    null = np.array([-Jx[1], Jx[0]])
    null = -null / np.linalg.norm(null)
    task = -Jx / np.linalg.norm(Jx)
    rng = np.random.default_rng(0)
    n = rng.normal(0.0, SIGMA, (NTR, 2))
    e = n @ Jx
    dq = n - (1 - np.sqrt(RHO)) * np.outer(e, Jx) / (Jx @ Jx)
    return Jx, null, task, dq, float(np.var(dq @ null)), float(np.var(dq @ task))


K7 = k7_data()
assert (round(K7[0][0], 4), round(K7[0][1], 4)) == (-0.1000, 0.1966)
assert (round(K7[1][0], 3), round(K7[1][1], 3), round(K7[2][0], 3), round(K7[2][1], 3)) == (0.891, 0.453, 0.453, -0.891)
assert (round(K7[4] * 1e4, 3), round(K7[5] * 1e5, 3), round(K7[4] / K7[5], 2)) == (3.938, 6.160, 6.39), K7[4:]
N_SHOWN = 500                                   # Lab D shows 500 of the 4000 plotted outcomes (line 379 caption)


def fig51():
    p = "m12f51_"
    hgt = 220.0
    s = pscale(700)
    body, J, km, P, org = scene(s, hgt, (84.0, 96.0), Q_UP)
    Jx, null, task, dq, vn, vt = K7
    hand = J["fingertip"]
    bx0, bx1, by0, by1 = 78.0, 318.0, 296.0, 536.0
    R = 0.075                                                        # rad, half range of both axes
    X = lambda v: bx0 + (v + R) / (2 * R) * (bx1 - bx0)              # noqa: E731
    Y = lambda v: by1 - (v + R) / (2 * R) * (by1 - by0)              # noqa: E731
    VB = (0, 0, 400, 700)
    o = [defs(p, s), H.line(s, 10, J["floor_y"], 390, J["floor_y"], I["rule"], "axis"), stool(s, J), body]
    xt = hand[0]
    o.append(dline(s, xt, hand[1] - 0.45 * km, xt, J["floor_y"] - s(8), O["flag"]))
    o.append(dot(s, hand[0], hand[1], O["flag"], 4))
    o.append(H.label(s, xt + s(8), hand[1] - 0.45 * km + s(6), "task: hand x fixed", "label2", I["primary"]))
    o.append(H.label(s, xt + s(8), hand[1] - 0.45 * km + s(22), f"x = {HOLE[0]:.2f} m", "label2", I["secondary"]))
    for q in (J["shoulder"], J["elbow"]):
        o.append(H.joint_centre(s, *q))
    for i, t_ in enumerate((f"q = ({Q_UP[0]:.1f}°, {mi(Q_UP[1])}°):", "elbow above the shoulder-", "to-hand line")):
        o.append(H.label(s, 226, 120 + i * s(18), t_, "label2", I["secondary"]))
    # scatter
    o.append(f'<rect x="{bx0}" y="{by0}" width="{bx1 - bx0}" height="{by1 - by0}" fill="#fff" stroke="{I["rule"]}" '
             f'stroke-width="{s(1):.2f}"/>')
    for v in (-0.06, -0.03, 0.0, 0.03, 0.06):
        o.append(H.line(s, X(v), by0, X(v), by1, GRID, "leader"))
        o.append(H.line(s, bx0, Y(v), bx1, Y(v), GRID, "leader"))
        o.append(H.label(s, X(v), by1 + s(16), f"{v:g}".replace("-", "−"), "tick", I["secondary"], "middle"))
        o.append(H.label(s, bx0 - s(6), Y(v) + s(4), f"{v:g}".replace("-", "−"), "tick", I["secondary"], "end"))
    o.append(H.line(s, X(0), by0, X(0), by1, I["rule"], "axis"))
    o.append(H.line(s, bx0, Y(0), bx1, Y(0), I["rule"], "axis"))
    hov, dots = [], []
    for k in range(N_SHOWN):
        a, b = dq[k]
        dots.append(f"M{X(a):.1f} {Y(b):.1f}h0")                     # one round dot each: zero-length segment, round cap
        hov.append([X(a), Y(b), f"δθ₁ = {a:+.3f} rad, δθ₂ = {b:+.3f} rad".replace("-", "−")])
    o.append(f'<path d="{"".join(dots)}" fill="none" stroke="{I["secondary"]}" stroke-opacity="0.45" '
             f'stroke-width="{s(4.2):.2f}" stroke-linecap="round"/>')
    hov.sort(key=lambda r: r[0])
    t = R * 0.95 / max(abs(null[0]), abs(null[1]))
    o.append(dline(s, X(-t * null[0]), Y(-t * null[1]), X(t * null[0]), Y(t * null[1]), O["geometry"], "geom"))
    o.append(H.line(s, X(0), Y(0), X(0.040 * task[0]), Y(0.040 * task[1]), O["flag"], "force",
                    extra=f'marker-end="url(#{p}a_flag)"'))
    o.append(H.label(s, X(0.040 * task[0]) + s(6), Y(0.040 * task[1]) + s(4), "task direction", "label2", I["primary"]))
    o.append(H.label(s, X(t * null[0]) - s(4), Y(t * null[1]) - s(8), "null direction", "label2", O["geometry"], "end"))
    o.append(H.label(s, bx0, 280, f"{N_SHOWN} of {NTR} trials: joint-angle scatter", "label2", I["secondary"]))
    o.append(H.label(s, (bx0 + bx1) / 2, by1 + s(36), "δθ₁ (rad)", "label2", I["primary"], "middle"))
    o.append(f'<text x="{bx0 - s(42):.2f}" y="{(by0 + by1) / 2:.2f}" font-size="{s(H.PX["label2"]):.2f}" fill="{I["primary"]}" '
             f'text-anchor="middle" transform="rotate(-90 {bx0 - s(42):.2f} {(by0 + by1) / 2:.2f})" stroke="#fff" '
             f'stroke-width="{s(H.PX["label2"]) * 0.28:.2f}" paint-order="stroke">δθ₂ (rad)</text>')
    o.append(H.label(s, 10, 594, f"variance along the null direction {vn * 1e4:.3f}×10⁻⁴ rad², along the task", "label2",
                     I["primary"]))
    o.append(H.label(s, 10, 612, f"direction {vt * 1e5:.3f}×10⁻⁵ rad²: ratio {vn / vt:.2f} (1/ρ = {1 / RHO:.2f})", "label2",
                     I["primary"]))
    o.append(credit_at(s, 636))
    box = [bx0, by0, bx1, by1]
    aria = ("A seated skeleton holds its hand at x equal to 0.45 metres, marked by a vertical dashed orange line: only the "
            "hand's horizontal position is the task. Its elbow is raised above the shoulder-to-hand line, joint angles "
            "81.3 and minus 107.2 degrees. Below, a scatter of 500 of 4000 trials of joint-angle error, delta theta 1 "
            "against delta theta 2, is a long cloud stretched along the dashed blue null direction (0.891, 0.453) and "
            "narrow along the task direction (0.453, minus 0.891). The variance along the null direction is 6.39 times "
            "the variance along the task direction.")
    return finish(VB, aria, s, o, extra=H.hover_attr(box, hov))


FIGS = {
    2: ("Motor equivalence: a seated person signs the same shape twic", fig2),
    6: ("Impedance control for peg insertion: a seated person guides ", fig6),
    19: ("C1: the two signatures. Your signature on paper and on a whi", fig19),
    21: ("C3: the failed self-tickle. You cannot tickle yourself, but ", fig21),
    22: ("C4: stiffening in the dark. Faced with an unstable or unpredic", fig22),
    26: ("C8: cheap walking. Rhythmic movements like walking are metabol", fig26),
    27: ("C9: a few knobs, many muscles. Why does the nervous system c", fig27),
    33: (r"D5: endpoint stiffness. Derive $K_x=J^{-\mathsf T}K_qJ^{-1}$", fig33),
    43: ("K3: orienting the stiffness ellipse (optimisation). For a pe", fig43),
    51: ("K7: the uncontrolled manifold in a redundant reach (joint-sp", fig51),
}
