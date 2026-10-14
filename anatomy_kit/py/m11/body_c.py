"""Module 11, group `body_c`: problem figures C1-C4, C6-C10 and D1 (svg #21-24, #26-31), house style, 400 px.

Arms, hands and whole bodies are the posable Lynch skeleton (lynch_body.py); m11/body_main.py puts its defs on the page,
this group only <use>s them (the shoulder crop comes from body_main SHARED_DEFS, the hip crop is embedded here).  C7 embeds two Lynch crops (hip, shoulder) through art_image,
the way Module 3's deep-versus-shallow-socket figure does.  The page states a stature nowhere: 1.75 m, so one centimetre
is LB.H_U / 175 body units.  The kit's arm is Winter's: upper arm 0.329 m, elbow to fingertip 0.443 m (the text's
two-link arm, Definition 1 and line 116, uses 0.30 and 0.45 m); every planar quantity below is computed from the kit's
own joint positions, so a label always agrees with the drawing.  Poses the text does not fix are design values (marked).
Numbers the text states, with module11.html line numbers:
  Definition 1 (line 104)   theta_2 = 0 is a straight arm; two-link arm, ell_2 = elbow to fingertip (line 116: 0.45 m)
  Proposition 3.1 (147)     theta_2 = +-arccos((r^2 - l1^2 - l2^2) / (2 l1 l2)); the signs are elbow-down and elbow-up
  line 156                  near r = l1 + l2 theta_2 has an infinite slope in r (the arccos has a vertical tangent)
  Definition 3 (183)        N(J) is one-dimensional for a 2x3 Jacobian of full rank (shoulder, elbow, wrist, fingertip pinned)
  Proposition 7.1 (226-232) F_t / F_c <= tan(alpha); shoulder alpha ~ 22 deg (Module 3's beta), tan 22 deg ~ 0.40 (line 232); the page gives no
                            hip alpha, so the hip uses Module 3's beta ~ 55 deg (module03.html lines 510, 514)
  Proposition 8.1 (244)     F_g >= W / (2 mu); line 464: mu falls from about 0.5 toward 0.1-0.2
  Definition 5 (268)        F_g,min = L / (2 mu), F_g = (1 + s) F_g,min, s typically 0.1 to 0.4; line 472: reflex within ~70 ms
  Lab B (lines 327-357)     m2 = 1.65 kg, lc2 = 0.22 m, I2 = 0.025: M22 = 0.10486; wave amplitude 0.5 rad; 4.7, 18.6 N m
  line 541                  crossover of M22 A (2 pi f)^2 with m2 lc2 g near 1.3 Hz (here 1.31 Hz)
"""
import math

import numpy as np

import house as H
import lynch_body as LB
from m03.joints import Place, angle_arc, cone, head_outline, lynch, pol, HIP_C, HUM_C
from m05.body import art_image, finish, it
from m05.plots_prob import Plot, hov, label as plabel, legend

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
CM = LB.H_U / 175.0                      # body units per cm (stature 1.75 m)
BOX = "#f7f4ef"
GRID = "#e6e6e6"
G = 9.81

# ---------------------------------------------------------------- the kit's planar arm (exact, asserted against LB.pose)
LU, LF, LH = LB.OFF["arm_upper"]["elbow"][1], LB.OFF["arm_fore"]["wrist"][1], LB.OFF["arm_hand"]["fingertip"][1]
SHO = LB.pose().j["shoulder"]            # shoulder in body units, hip at the origin (trunk upright)
L1 = LU                                  # shoulder to elbow
L2 = LF + LH                             # elbow to fingertip (wrist neutral: the hand is collinear with the forearm)


def _pt(p, length, a_deg):
    a = math.radians(a_deg)
    return (p[0] + length * math.cos(a), p[1] - length * math.sin(a))      # math angle, y up -> screen y down


def fk(sh, el, wr=0.0):
    """Joints (body units, screen y down) of the near arm.  Absolute angles (deg, ccw from +x): upper arm -90 + sh,
    forearm that + el, hand that + wr.  Same convention as the kit's flexion angles."""
    a1 = -90.0 + sh
    e = _pt(SHO, LU, a1)
    w = _pt(e, LF, a1 + el)
    f = _pt(w, LH, a1 + el + wr)
    return {"shoulder": SHO, "elbow": e, "wrist": w, "fingertip": f}


def _check_fk():
    for sh, el, wr in ((0, 0, 0), (35, 80, -20), (100, 57, 10), (-15, 150, -45)):
        j = LB.pose(near=dict(shoulder=sh, elbow=el, wrist=wr)).j
        q = fk(sh, el, wr)
        assert max(math.dist(q[k], j[k]) for k in q) < 1e-6, (sh, el, wr)


_check_fk()


def close(v, ref, tol):
    assert abs(v - ref) <= tol * 1.0001, (v, ref)


def ik(target, branch=+1):
    """Two-link inverse kinematics of Proposition 3.1 for the kit's arm (wrist neutral).  target in body units.
    branch +1 = elbow flexed (elbow-down), -1 = the other sign of theta_2.  Returns (shoulder flexion, elbow flexion) deg."""
    x, y = target[0] - SHO[0], SHO[1] - target[1]                 # math frame at the shoulder, y up
    r2 = x * x + y * y
    c2 = (r2 - L1 * L1 - L2 * L2) / (2 * L1 * L2)
    assert abs(c2) <= 1
    t2 = branch * math.acos(c2)
    t1 = math.atan2(y, x) - math.atan2(L2 * math.sin(t2), L1 + L2 * math.cos(t2))
    return math.degrees(t1) + 90.0, math.degrees(t2)


# ---------------------------------------------------------------- drawing helpers
def lab(s, x, y, text, size="label", fill=I["primary"], anchor="start", extra=""):
    return H.label(s, x, y, text, size, fill, anchor, extra)


def lines(s, x, y, rows, size="label2", anchor="start", lead=1.3, fill=I["primary"]):
    return "".join(lab(s, x, y + i * s(H.PX[size]) * lead, t, size, fill, anchor) for i, t in enumerate(rows))


def VBs(h):
    return (0, 0, 400, h), H.Scale(400, h, display_w=400, max_h=H.MAX_DISPLAY_H_BODY)


def mn(v, f="{:g}"):
    return f.format(v).replace("-", "−")


def sub(t, s, size="label"):
    return H.sub(t, s, size)


def dot(s, x, y, col, r=4.5):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{col}" stroke="#fff" '
            f'stroke-width="{s(1.5):.2f}"/>')


def ring(s, x, y, col, r=7.0):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="none" stroke="#fff" stroke-width="{s(4.5):.2f}"/>'
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="none" stroke="{col}" stroke-width="{s(2.2):.2f}"/>')


def ext(s, x0, y0, x1, y1, col=O["dim"]):
    return H.line(s, x0, y0, x1, y1, col, "ref", H.DASH_REF)


def floor(s, x0, x1, y, hatch=True):
    o = [H.line(s, x0, y, x1, y, I["axis"], "axis")]
    if hatch:
        n = int((x1 - x0) / s(10))
        o += [H.line(s, x0 + s(10) * i + s(8), y + s(1), x0 + s(10) * i, y + s(7), I["rule"], "leader") for i in range(n)]
    return "".join(o)


def chair(s, J, span=(-0.16, 0.20)):
    """Seat and legs under the hip: a schematic stool (design value), not anatomy."""
    hx, hy = J["hip"]
    h = J["floor_y"] - J["vertex"][1]
    y = hy + 0.075 * h
    xa, xb = hx + span[0] * h, hx + span[1] * h
    o = [H.line(s, xa, y, xb, y, I["rule"], "axis", extra='stroke-linecap="round"')]
    for xx in (xa + (xb - xa) * 0.06, xa + (xb - xa) * 0.94):
        o.append(H.line(s, xx, y, xx, J["floor_y"], I["rule"], "axis"))
    return "".join(o)


def cup(s, x, y, w, fill=True):
    """A mug (schematic object, fluid-blue tissue tokens) with its base centre at (x, y)."""
    h = w * 1.15
    f, ln = T["fluid"]
    return (f'<path d="M{x + w / 2:.2f},{y - h * 0.72:.2f} q{w * 0.45:.2f},{h * 0.02:.2f} {w * 0.04:.2f},{h * 0.42:.2f}" '
            f'fill="none" stroke="{ln}" stroke-width="{s(1.6):.2f}"/>'
            f'<rect x="{x - w / 2:.2f}" y="{y - h:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{w * 0.08:.2f}" fill="{f}" '
            f'stroke="{ln}" stroke-width="{s(1.2):.2f}"/>')


def put(s, P, x_left, y_floor, hpx):
    """Draw pose P at stature hpx with its bbox left edge at x_left and its floor at y_floor.  Returns (svg, J)."""
    _, J0 = LB.draw("m11", s, P, 0.0, y_floor, hpx)
    return LB.draw("m11", s, P, x_left - J0["bbox"][0], y_floor, hpx)


def ghost(P, s, J, op=0.30, names=("arm_upper", "arm_fore", "arm_hand")):
    """Only the near-arm segments of pose P, drawn where the figure drew its body (J carries the placement)."""
    P2 = LB.Pose(P.view)
    P2.segs = [q for q in P.segs if q[0] in names and not q[5]]
    P2.j, P2.com, P2.anchor, P2.floor_y = P.j, P.com, P.anchor, P.floor_y
    sv, _ = LB.draw("m11", s, P2, J["_x"], J["_y"], J["_h"])
    return f'<g opacity="{op}">{sv}</g>'


def put2(s, P, x_left, y_floor, hpx):
    """put() that also records the placement in J, so ghost() can redraw arm segments in place."""
    _, J0 = LB.draw("m11", s, P, 0.0, y_floor, hpx)
    x = x_left - J0["bbox"][0]
    sv, J = LB.draw("m11", s, P, x, y_floor, hpx)
    J["_x"], J["_y"], J["_h"] = x, y_floor, hpx
    return sv, J


def fig_pt(J, P, q):
    """A body-unit point q of pose P -> figure units, using the placement in J."""
    ax, ay = P.anchor
    k = J["scale"]
    return (J["_x"] + k * (q[0] - ax), J["_y"] + k * (q[1] - ay))


def credit(s, vb, extra=""):
    t = H.ATTRIBUTION["by"].format(
        author="Patrick J. Lynch, medical illustrator",
        title="Skeleton lateral.svg” and “Skeleton whole body ant lat views.svg", licence="CC BY 2.5",
        changes="Recoloured, split into segments and reposed; arms from the anterior view." + extra)
    w = vb[2] - s(12)
    n = max(20, int(w / (s(H.PX["credit"]) * 0.47)))
    rows, cur = [], ""
    for wd in t.split():
        if cur and len(cur) + 1 + len(wd) > n:
            rows.append(cur)
            cur = wd
        else:
            cur = (cur + " " + wd).strip()
    rows.append(cur)
    y = vb[1] + vb[3] - s(6) - (len(rows) - 1) * s(H.PX["credit"]) * 1.25
    return H.credit(s, vb[0] + s(6), y, rows)


CREDIT_H = 46                          # user units reserved under a figure for a 3-line credit at 400 px


# ================================================================ svg #21  C1 the waiter's tray
def fig21():
    p = "m11f21_"
    VB, s = VBs(408)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 255.0, 332.0
    W_N = 1.0                                    # tray weight, symbol only (the text gives none)
    cases = [("tucked", -10.0, 150.0, 8.0), ("at arm’s length", 88.0, 5.0, 204.0)]     # design poses: sh, el
    ds = []
    for name, sh, el, xl in cases:
        wr = 90.0 - sh - el                                  # hand horizontal: the tray lies flat on the palm
        P = LB.pose(near=dict(shoulder=sh, elbow=el, wrist=wr))
        sv, J = put2(s, P, xl, fy, HF)
        q = fk(sh, el, wr)
        palm = (q["wrist"][0] + 0.45 * (q["fingertip"][0] - q["wrist"][0]),
                q["wrist"][1] + 0.45 * (q["fingertip"][1] - q["wrist"][1]))
        pm, sp = fig_pt(J, P, palm), fig_pt(J, P, q["shoulder"])
        d_cm = (palm[0] - q["shoulder"][0]) / CM
        ds.append(d_cm)
        o.append(sv)
        tw, th = 0.20 * HF, s(5)
        ty = pm[1] - 0.026 * HF                              # tray sits on the palm
        o.append(f'<rect x="{pm[0] - tw / 2:.2f}" y="{ty - th:.2f}" width="{tw:.2f}" height="{th:.2f}" rx="{s(2):.2f}" '
                 f'fill="{BOX}" stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
        yd = fy - 0.40 * HF                                   # dimension line level (torso height)
        o.append(ext(s, sp[0], sp[1], sp[0], yd))
        o.append(H.arrow(s, p, pm[0], ty - th - s(34), pm[0], ty - th - s(2), "load"))       # W acts down on the tray
        o.append(ext(s, pm[0], ty, pm[0], yd, O["load"]))
        o.append(H.joint_centre(s, *sp))
        x0, x1 = sorted((sp[0], pm[0]))
        o.append(H.arrow(s, p, sp[0], yd, pm[0], yd, "load", both=True))
        o.append(lab(s, (x0 + x1) / 2, yd + s(26), f'{it("d")} = {d_cm:.0f} cm', "label", O["load"], "middle"))
        o.append(lab(s, pm[0] + s(7), ty - th - s(20), f'{it("W")}', "label", O["load"]))
        o.append(lab(s, xl + 90 * (HF / 255.0), fy + s(20), name, "label", I["primary"], "middle"))
    ratio = ds[1] / ds[0]
    o.append(floor(s, 8, 392, fy))
    o.append(lab(s, 200, 22, "same tray weight, same body", "label", I["primary"], "middle"))
    o.append(lab(s, 200, 22 + s(18), f"shoulder torque τ = d × W: {ratio:.1f} times larger at arm’s length", "label2",
                 I["secondary"], "middle"))
    o.append(credit(s, VB))
    aria = ("Two standing skeletons (Lynch art) carry the same tray flat on one hand. Left, the tray is tucked in: the "
            f"palm is {ds[0]:.0f} cm ahead of the shoulder joint, so the shoulder torque, the weight W times that "
            f"horizontal distance d, is small. Right, the arm is held out straight: the palm is {ds[1]:.0f} cm ahead, "
            f"{ratio:.1f} times as far, and so is the torque. The weight acts down on the tray (brown arrow); the brown "
            "double arrow is the horizontal distance d from the shoulder joint to the line of the weight.")
    return finish(VB, aria, s, o)


# ================================================================ svg #22  C2 which elbow
def fig22():
    p = "m11f22_"
    VB, s = VBs(492)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 485.0, 440.0
    # design target: the mug 0.55 m ahead of the shoulder and 0.22 m below it (a tabletop reach), planar
    tx, ty = SHO[0] + 0.55 * 100 * CM, SHO[1] + 0.22 * 100 * CM
    r = math.hypot(tx - SHO[0], ty - SHO[1]) / CM / 100
    sh_d, el_d = ik((tx, ty), +1)
    sh_u, el_u = ik((tx, ty), -1)
    assert el_d > 0 > el_u and abs(el_d + el_u) < 1e-9
    for sh, el in ((sh_d, el_d), (sh_u, el_u)):                # both put the fingertip on the target
        assert math.dist(fk(sh, el)["fingertip"], (tx, ty)) < 1e-6
    Pd = LB.pose(near=dict(hip=90, knee=90, shoulder=sh_d, elbow=el_d), far=dict(hip=90, knee=90))
    Pu = LB.pose(near=dict(hip=90, knee=90, shoulder=sh_u, elbow=el_u), far=dict(hip=90, knee=90))
    sv, J = put2(s, Pd, 24.0, fy, HF)
    tgt = fig_pt(J, Pd, (tx, ty))
    cw = 0.062 * HF                                            # the mug stands on the table, fingertips at its side
    cbase = tgt[1] + 0.58 * cw * 1.15
    o.append(chair(s, J))
    o.append(floor(s, 8, 392, fy))
    o.append(H.line(s, tgt[0] - 0.03 * HF, cbase, 392, cbase, I["rule"], "axis", extra='stroke-linecap="round"'))
    o.append(H.line(s, 384, cbase, 384, fy, I["rule"], "axis"))
    o.append(ghost(Pu, s, J, 0.34))
    o.append(sv)
    o.append(cup(s, tgt[0] + cw * 0.5, cbase, cw))
    ed, eu = fig_pt(J, Pd, fk(sh_d, el_d)["elbow"]), fig_pt(J, Pu, fk(sh_u, el_u)["elbow"])
    sp = fig_pt(J, Pd, SHO)
    o.append(ext(s, sp[0], sp[1], tgt[0], tgt[1]))
    for q in (sp, ed, eu):
        o.append(H.joint_centre(s, *q))
    o.append(lab(s, 200, 22, "same hand position, two arm configurations", "label", I["primary"], "middle"))
    # elbow-up label: in the free space right of the faint elbow
    o.append(H.line(s, eu[0] + s(8), eu[1] - s(3), eu[0] + s(28), eu[1] - s(14), I["muted"], "leader"))
    o.append(lab(s, eu[0] + s(31), eu[1] - s(12), "elbow-up (faint)", "label", I["primary"]))
    o.append(lab(s, eu[0] + s(31), eu[1] + s(5), f"θ{sub('2', s, 'label2')} = {mn(el_u, '{:+.0f}')}°: past straight", "label2",
                 I["secondary"]))
    # elbow-down label: below the table, leader up to the elbow
    ly = cbase + s(40)
    o.append(H.line(s, ed[0] + s(7), ed[1] + s(7), ed[0] + s(26), ly - s(16), I["muted"], "leader"))
    o.append(lab(s, ed[0] + s(28), ly - s(8), "elbow-down", "label", I["primary"]))
    o.append(lab(s, ed[0] + s(28), ly + s(9), f"θ{sub('2', s, 'label2')} = {mn(el_d, '{:+.0f}')}°", "label2", I["secondary"]))
    o.append(lab(s, 380, cbase + s(20), f"mug {r:.2f} m from the shoulder", "label2", I["secondary"], "end"))
    o.append(credit(s, VB))
    aria = ("A seated skeleton (Lynch art) reaches a mug on a table 0.55 m ahead of and 0.22 m below the shoulder. "
            f"Two arm configurations put the fingertips on the mug: elbow-down (solid, shoulder flexion {sh_d:.0f} "
            f"degrees, elbow angle theta 2 = {el_d:+.0f} degrees) and elbow-up (faint, shoulder flexion {sh_u:.0f} "
            f"degrees, theta 2 = {el_u:+.0f} degrees, which is an elbow bent past straight, outside the range of motion). "
            "They are mirror images across the dashed shoulder-to-mug line: the two signs of theta 2 in Proposition 3.1.")
    return finish(VB, aria, s, o)


# ================================================================ svg #23  C3 bend to place, straighten to brace
def jacobian(t1, t2):
    """Two-link Jacobian (Proposition 2.1) for the kit's arm; angles in degrees, lengths in metres."""
    l1, l2 = L1 / LB.H_U * 1.75, L2 / LB.H_U * 1.75
    a, b = math.radians(t1), math.radians(t1 + t2)
    return np.array([[-l1 * math.sin(a) - l2 * math.sin(b), -l2 * math.sin(b)],
                     [l1 * math.cos(a) + l2 * math.cos(b), l2 * math.cos(b)]]), l1, l2


def ellipse_path(s, c, axes_xy, semi, col, fill_op, dash=None, w="geom"):
    """Ellipse about c with principal directions axes_xy (unit vectors, math frame) and semi-axes semi (px)."""
    pts = []
    for k in range(73):
        a = 2 * math.pi * k / 72
        ex = axes_xy[0][0] * semi[0] * math.cos(a) + axes_xy[1][0] * semi[1] * math.sin(a)
        ey = axes_xy[0][1] * semi[0] * math.cos(a) + axes_xy[1][1] * semi[1] * math.sin(a)
        pts.append((c[0] + ex, c[1] - ey))
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z"
    return (f'<path d="{d}" fill="{col}" fill-opacity="{fill_op}" stroke="{col}" stroke-width="{s(H.PX[w]):.2f}" '
            f'stroke-linejoin="round"{da}/>')


def fig23():
    p = "m11f23_"
    VB, s = VBs(436)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 250.0, 306.0
    cases = [("bent: place", 20.0, 90.0, 8.0), ("straight: brace", 80.0, 12.0, 204.0)]      # design poses: sh, el
    info = []
    for name, sh, el, xl in cases:
        P = LB.pose(near=dict(shoulder=sh, elbow=el))
        sv, J = put2(s, P, xl, fy, HF)
        o.append(sv)
        fp = fig_pt(J, P, fk(sh, el)["fingertip"])
        Jm, l1, l2 = jacobian(-90.0 + sh, el)
        U, sig, Vt = np.linalg.svd(Jm)
        w = l1 * l2 * abs(math.sin(math.radians(el)))
        close(abs(np.linalg.det(Jm)), w, 1e-9)                 # det J = l1 l2 sin(theta_2)  (D2)
        close(sig[0] * sig[1], w, 1e-9)
        F_axes = (U[:, 0], U[:, 1])
        # the force ellipse of D5: J^-T on the unit circle, same axes, semi-axes 1 / sigma
        Fm = np.linalg.inv(Jm).T
        Uf, sf, _ = np.linalg.svd(Fm)
        close(sf[0], 1 / sig[1], 1e-9)
        close(abs(float(Uf[:, 0] @ U[:, 1])), 1.0, 1e-9)
        info.append((name, sh, el, fp, sig, w, U, l1 * l2))
    # each ellipse is scaled so its long semi-axis is 42 px: only shape and direction are compared
    for name, sh, el, fp, sig, w, U, l12 in info:
        v_semi = [42.0, 42.0 * sig[1] / sig[0]]
        f_semi = [42.0, 42.0 * sig[1] / sig[0]]               # semi-axes 1/sigma_2 : 1/sigma_1 = sigma_1 : sigma_2 reversed
        # force ellipse: long axis along U[:,1] (length 1/sigma_2), short along U[:,0] (length 1/sigma_1)
        o.append(ellipse_path(s, fp, (U[:, 0], U[:, 1]), v_semi, O["geometry"], 0.16))
        o.append(ellipse_path(s, fp, (U[:, 1], U[:, 0]), f_semi, O["force"], 0.0, H.DASH_REF, "force"))
    # the stuck door: a vertical edge at the hand of the straight arm (schematic object)
    fp2 = info[1][3]
    o.append(H.line(s, fp2[0] + s(28), fp2[1] - 0.20 * HF, fp2[0] + s(28), fp2[1] + 0.20 * HF, I["rule"], "axis"))
    o.append(lab(s, fp2[0] + s(28), fp2[1] + 0.20 * HF + s(15), "door", "label2", I["secondary"], "middle"))
    o.append(floor(s, 8, 392, fy))
    for (name, sh, el, fp, sig, w, U, l12), xc in zip(info, (100, 296)):
        o.append(lab(s, xc, fy + s(20), name, "label", I["primary"], "middle"))
        o.append(lab(s, xc, fy + s(37), f"θ{sub('2', s, 'label2')} = {el:.0f}°, w = {w / l12:.2f} ℓ{sub('1', s, 'label2')}"
                                         f"ℓ{sub('2', s, 'label2')}", "label2", I["secondary"], "middle"))
        o.append(lab(s, xc, fy + s(53), f"axis ratio σ{sub('1', s, 'label2')}/σ{sub('2', s, 'label2')} = "
                                         f"{sig[0] / sig[1]:.1f}", "label2", I["secondary"], "middle"))
    ratios = [i[4][0] / i[4][1] for i in info]
    o.append(H.line(s, 12, 18 - 4.5, 32, 18 - 4.5, O["geometry"], "geom"))
    o.append(lab(s, 38, 18, "hand velocity ellipse (J on the unit circle)", "label2", I["secondary"]))
    o.append(H.line(s, 12, 36 - 4.5, 32, 36 - 4.5, O["force"], "force", H.DASH_REF))
    o.append(lab(s, 38, 36, f"hand force ellipse (J{sub('−T', s, 'label2')} on the unit circle)", "label2", I["secondary"]))
    o.append(lab(s, 12, 54, "each ellipse scaled to fit: shape and axes only", "label2", I["muted"]))
    o.append(credit(s, VB))
    aria = ("Two standing skeletons (Lynch art) with the hand velocity ellipse (blue, filled) and the hand force ellipse "
            "(red, dashed) drawn at the fingertips. Left, the elbow is bent to 90 degrees: the two ellipses are "
            f"fat (axis ratio {ratios[0]:.1f}) and the manipulability w = l1 l2 sin(theta 2) is at its maximum. "
            f"Right, the arm is nearly straight, theta 2 = 12 degrees, w is {info[1][5] / info[1][7]:.2f} of its maximum: "
            f"the velocity ellipse is a thin sliver across the arm (axis ratio {ratios[1]:.1f}) and the force ellipse is "
            "long along the arm, against a door. The force ellipse is the velocity ellipse turned 90 degrees.")
    return finish(VB, aria, s, o)


# ================================================================ shared: a seated body holding a mug (C4, C6)
def hold_body(s, p, x_left, y_floor, hpx):
    """Seated skeleton (kit arm, wrist neutral) with a mug at the hand.  Returns (svg, J, fingertip, (mug base, mug w))."""
    arm = dict(hip=90, knee=90, shoulder=30, elbow=75, wrist=-10)
    P = LB.pose(near=arm, far=arm)
    sv, J = put2(s, P, x_left, y_floor, hpx)
    fp = fig_pt(J, P, fk(30, 75, -10)["fingertip"])
    cw = 0.075 * hpx
    base = (fp[0] - cw * 0.10, fp[1] + 0.62 * cw * 1.15)
    o = chair(s, J) + floor(s, x_left - 4, x_left + 0.62 * hpx, y_floor) + sv + cup(s, base[0], base[1], cw)
    return o, J, fp, (base, cw)


def force_icon(s, p, cx, cy, w, h, scale, grip_w):
    """Free-body diagram of the mug alone: grip F_g in at both faces (red), friction up (black), weight down (brown).
    Arrow lengths: `scale` px per W; each pad carries W/2 by friction (<= mu F_g), Proposition 8.1."""
    o = [f'<rect x="{cx - w / 2:.2f}" y="{cy - h / 2:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{s(2):.2f}" '
         f'fill="{T["fluid"][0]}" stroke="{T["fluid"][1]}" stroke-width="{s(1.2):.2f}"/>']
    lg = grip_w * scale
    for sg in (-1, 1):
        x_face = cx + sg * w / 2
        o.append(H.arrow(s, p, x_face + sg * (lg + s(2)), cy, x_face + sg * s(1), cy, "force"))
        xf = x_face - sg * s(7)
        o.append(H.arrow(s, p, xf, cy + 0.25 * scale, xf, cy - 0.25 * scale, "reaction"))
    o.append(H.arrow(s, p, cx, cy + h / 2 + s(1), cx, cy + h / 2 + scale + s(1), "load"))
    return "".join(o)


# ================================================================ svg #24  C4 the soapy glass
def fig24():
    p = "m11f24_"
    VB, s = VBs(506)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    body, J, fp, (base, cw) = hold_body(s, p, 8.0, 222.0, 262.0)
    o.append(body)
    mus = [(0.5, "dry, μ = 0.5"), (0.2, "soapy, μ = 0.2")]
    sc = 34.0                                              # px per weight W
    close(1 / (2 * mus[0][0]), 1.0, 1e-12)
    close(1 / (2 * mus[1][0]), 2.5, 1e-12)
    o.append(legend(s, 176, 20, [(O["force"], "grip", None), (O["reaction"], "friction", None), (O["load"], "weight W", None)], gap=2))
    for k, (mu, name) in enumerate(mus):
        cy = 74 + k * 92
        fg = 1 / (2 * mu)
        o.append(force_icon(s, p, 286.0, cy, 36, 44, sc, fg))
        o.append(lab(s, 392, cy - 40, name, "label2", I["primary"], "end"))
        o.append(lab(s, 392, cy - 24, f"F{sub('g', s, 'label2')} ≥ {fg:.1f} W", "label2", I["primary"], "end"))
    # the plot of F_g/W = 1/(2 mu)
    P = Plot(s, (62, 272, 378, 408), (0.05, 0.60), (0, 5.5))
    mu = np.linspace(0.10, 0.60, 200)
    fgw = 1 / (2 * mu)
    o.append(P.axes([(v, f"{v:g}") for v in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6)], [(v, f"{v:g}") for v in (0, 1, 2, 3, 4, 5)],
                    "friction coefficient μ", "grip F" + sub("g", s) + " (× W)", grid=(1, 2, 3, 4, 5), ytx=18))
    o.append(P.curve(mu, fgw, SER[0]))
    for v, tx, dx, dy, anchor in ((0.5, "dry: 1.0 W", 0, -10, "middle"), (0.2, "soapy: 2.5 W", 10, -6, "start"),
                                  (0.1, "5.0 W", 10, 4, "start")):
        o.append(P.dot(v, 1 / (2 * v), SER[0]))
        o.append(plabel(s, P.X(v) + dx, P.Y(1 / (2 * v)) + dy, tx, "label2", I["primary"], anchor))
    o.append(plabel(s, P.X(0.36), P.Y(4.4), "F" + sub("g", s, "label2") + " = W / (2μ)", "label", I["primary"], "start"))
    o.append(plabel(s, P.X(0.36), P.Y(4.4) + 17, "halve μ: double the grip", "label2", I["secondary"], "start"))
    o.append(credit(s, VB))
    aria = ("Top left, a seated skeleton (Lynch art) holds a mug between thumb and finger. Top right, two free-body "
            "diagrams of the mug, arrows to one scale: for dry hands, mu = 0.5, each of two pads grips with Fg = 1.0 W "
            "(red) and friction, at most mu Fg, carries W/2 each (black), with the weight W (brown) down; for soapy "
            "hands, mu = 0.2, the grip must be 2.5 W for the same friction forces. Below, the grip force Fg = W/(2 mu) "
            "against mu from 0.1 to 0.6: a hyperbola, 1.0 W at 0.5, 2.5 W at 0.2, 5.0 W at 0.1, steepest where friction "
            "is smallest.")
    hv = hov(P, mu[::2], [fgw[::2]], lambda i: f"μ = {mu[::2][i]:.2f}: grip ≥ {fgw[::2][i]:.2f} W")
    return finish(VB, aria, s, o, H.hover_attr(P.box, hv))


# ================================================================ svg #26  C6 the numb fingertip (Lab C numbers)
MG_KG = 0.5                          # kg, Lab C cup (line 372)
S_HEALTHY, MU0, MU1, T_DROP, T_REFLEX = 0.30, 0.6, 0.3, 0.5, 0.070   # s, mu before / after (design: a wet patch), s, 70 ms (line 472)
S_BIG = 3.0                          # design: "a margin several times larger" (line 472); the text gives no number


def numb_traces(t):
    load = MG_KG * G
    floor0, floor1 = load / (2 * MU0), load / (2 * MU1)
    floor_ = np.where(t < T_DROP, floor0, floor1)
    g0, g1 = (1 + S_HEALTHY) * floor0, (1 + S_HEALTHY) * floor1
    ramp = np.clip((t - T_DROP) / T_REFLEX, 0, 1)
    healthy = g0 + (g1 - g0) * ramp                     # the reflex raises the grip over 70 ms
    return floor_, healthy, np.full_like(t, g0), np.full_like(t, (1 + S_BIG) * floor0)


def fig26():
    p = "m11f26_"
    VB, s = VBs(506)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    body, J, fp, (base, cw) = hold_body(s, p, 8.0, 222.0, 262.0)
    o.append(body)
    o.append(ring(s, fp[0], fp[1], O["flag"], 6.5))
    o.append(H.line(s, fp[0] + s(5), fp[1] - s(5), fp[0] + s(20), fp[1] - s(20), I["muted"], "leader"))
    o.append(lab(s, fp[0] + s(22), fp[1] - s(20), "fingertips numbed", "label2", I["primary"]))
    t = np.linspace(0, 1.0, 401)
    fl, hl, ga, gb = numb_traces(t)
    close(1.3 * MG_KG * G / (2 * MU0), 5.31, 0.005)          # line 399: 5.31 N per pad at mu = 0.6
    o.append(lines(s, 214, 96, ["a wet patch drops μ", f"from {MU0} to {MU1} at t = {T_DROP} s:", "the slip floor L/2μ",
                                 f"doubles, {fl[0]:.2f} to {fl[-1]:.2f} N"], "label2", fill=I["secondary"], lead=1.35))
    P = Plot(s, (62, 272, 380, 408), (0, 1.0), (0, 18))
    o.append(P.axes([(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1.0)], [(v, f"{v}") for v in (0, 6, 12, 18)],
                    "time t (s)", "grip force per pad (N)", grid=(6, 12, 18), ytx=18))
    k = t >= T_DROP
    ring_pts = [(P.X(a), P.Y(b)) for a, b in zip(t[k], fl[k])] + [(P.X(a), P.Y(b)) for a, b in zip(t[k][::-1], ga[k][::-1])]
    o.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in ring_pts)}" fill="{SER[0]}" opacity="0.14"/>')
    o.append(H.line(s, P.X(T_DROP), P.y0, P.X(T_DROP), P.y1, I["rule"], "ref", H.DASH_REF))
    o.append(P.curve(t, fl, I["secondary"], multi=True, dash=H.DASH_REF))
    o.append(P.curve(t, gb, SER[2], multi=True))
    o.append(P.curve(t, ga, SER[0], multi=True))
    o.append(P.curve(t, hl, SER[1], multi=True))
    o.append(plabel(s, P.X(0.04), P.Y(gb[-1]) + 16, f"numb, big margin: {gb[-1]:.0f} N", "label2", I["primary"], "start"))
    o.append(plabel(s, P.X(0.04), P.Y(gb[-1]) + 32, "crush risk, tiring", "label2", I["secondary"], "start"))
    o.append(plabel(s, P.X(0.54), P.Y(hl[-1]) - 8, f"healthy: {hl[-1]:.1f} N", "label2", I["primary"], "start"))
    o.append(plabel(s, P.X(0.54), P.Y(fl[-1]) + 15, f"slip floor {fl[-1]:.1f} N", "label2", I["primary"], "start"))
    o.append(plabel(s, P.X(0.54), P.Y(ga[0]) + 14, f"numb, old grip {ga[0]:.1f} N", "label2", I["primary"], "start"))
    o.append(plabel(s, P.X(0.54), P.Y(ga[0]) + 29, "slips: the mug drops", "label2", I["secondary"], "start"))
    o.append(plabel(s, P.X(T_DROP) - 6, P.Y(1.4), "μ falls", "label2", I["secondary"], "end"))
    o.append(legend(s, 62, 262, [(SER[1], "healthy", None), (SER[0], "numb, old grip", None), (SER[2], "numb, big margin", None)], gap=6))
    o.append(credit(s, VB))
    aria = ("Top left, a seated skeleton (Lynch art) holds a mug; the fingertips are marked numbed. Below, grip force per "
            f"pad against time for a mug of 0.5 kg when a wet patch drops the friction coefficient from {MU0} to {MU1} at "
            f"0.5 s, so the slip floor L/(2 mu), dashed, doubles from {fl[0]:.2f} to {fl[-1]:.2f} N. A healthy hand "
            f"(blue) holds 30 percent above the floor, {hl[0]:.2f} N, and its slip reflex raises the grip to {hl[-1]:.1f} N "
            "within 70 ms. A numb hand that keeps the old grip (red) falls below the floor, shaded, and the mug slips "
            f"and drops. A numb hand that always grips with a margin of 3, {gb[-1]:.0f} N (orange), never slips but "
            "squeezes hard enough to crush a fragile object and tires the hand.")
    hv = hov(P, t[::4], [fl[::4], hl[::4], ga[::4], gb[::4]],
             lambda i: f"t = {t[::4][i]:.2f} s: floor {fl[::4][i]:.1f}, healthy {hl[::4][i]:.1f}, "
                       f"old grip {ga[::4][i]:.1f}, big margin {gb[::4][i]:.1f} N")
    return finish(VB, aria, s, o, H.hover_attr(P.box, hv))


# ================================================================ svg #27  C7 why the shoulder, not the hip
ALPHA_SH, ALPHA_HIP = 22.0, 55.0     # deg: shoulder line 232 (= Module 3's beta ~ 22 deg); hip = Module 3's coverage angle beta ~ 55 deg (module03.html lines 510, 514)


def socket_art(s, p, which, win, d, k, alpha, Lc):
    """Head in socket on embedded Lynch art, with the stability cone of half-angle alpha about the compressive force F_c,
    F_c along the axis, F_t at the limit F_c tan(alpha) across it, and their resultant on the rim line."""
    pl = Place(win[:2], d, k)
    if which == "hip":
        img = pl.image(lynch("hip"), win)
        c, r, ax = pl(HIP_C[:2]), HIP_C[2] * k, -90.0
    else:
        img = pl.image("shoulder", win, p)
        c, r, ax = pl(HUM_C[:2]), HUM_C[2] * k, 180.0
    rim = Lc / math.cos(math.radians(alpha))                 # the cone edges end exactly at the tip of F_t
    o = [img, head_outline(s, c, r), cone(s, c, ax, alpha, rim)]
    tip = pol(c, Lc, ax)                                   # F_c: from the head centre into the socket
    o.append(H.arrow(s, p, c[0], c[1], tip[0], tip[1], "force"))
    ft = Lc * math.tan(math.radians(alpha))
    tip2 = pol(tip, ft, ax + 90.0)                         # F_t across the axis, towards the rim line at +alpha
    o.append(H.arrow(s, p, tip[0], tip[1], tip2[0], tip2[1], "load"))
    o.append(angle_arc(s, c, 0.62 * Lc, ax, ax + alpha))
    o.append(H.joint_centre(s, *c))
    la = pol(c, 0.62 * Lc + s(13), ax + alpha / 2)
    o.append(lab(s, la[0], la[1] + s(5), "α", "label", O["geometry"], "middle", 'font-style="italic"'))
    lc = pol(c, s(22), ax + 180.0)                           # F_c label: at the tail of the force, behind the head centre
    o.append(lab(s, lc[0], lc[1] + s(5), f"F{sub('c', s)}", "label", O["force"], "middle"))
    lt = pol(tip2, s(18), ax + 90.0)
    o.append(lab(s, lt[0], lt[1] + s(5), f"F{sub('t', s)}", "label", O["load"], "middle"))
    return o, c


def fig27():
    p = "m11f27_"
    VB, s = VBs(402)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    k = 0.31
    close(math.tan(math.radians(ALPHA_SH)), 0.40, 0.005)               # line 232
    q, c = socket_art(s, p, "sh", (660, 1430, 1240, 2040), (6.0, 46.0), k, ALPHA_SH, 64)
    o += q
    q2, c2 = socket_art(s, p, "hip", (300, 3640, 860, 4380), (216.0, 38.0), k, ALPHA_HIP, 40)
    o += q2
    for xc, title in ((100, "Shoulder: shallow glenoid"), (300, "Hip: deep acetabulum")):
        o.append(lab(s, xc, 22, title, "label", I["primary"], "middle", 'font-weight="bold"'))
    o.append(H.line(s, 200, 34, 200, 300, GRID, "leader"))
    for xc, al in ((100, ALPHA_SH), (300, ALPHA_HIP)):
        ta = math.tan(math.radians(al))
        o.append(lab(s, xc, 282, f"α ≈ {al:.0f}°: tan α = {ta:.2f}", "label", I["primary"], "middle"))
        o.append(lab(s, xc, 300, f"F{sub('t', s, 'label2')} ≤ {ta:.2f} F{sub('c', s, 'label2')} before it dislocates", "label2",
                     I["secondary"], "middle"))
    o.append(lab(s, 200, 320, "dashed blue: the rim line; beyond it the head rides out", "label2", I["secondary"], "middle"))
    t = H.ATTRIBUTION["by"].format(author="Patrick J. Lynch, medical illustrator", title="Skeleton whole body ant lat views.svg",
                                   licence="CC BY 2.5", changes="Left hip and left shoulder, front view; recoloured, cropped; "
                                   "head outline, cone and forces drawn for this course. α is the text value, not measured on the art.")
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
    aria = ("Left, a shoulder (Lynch skeleton art, front view): the humeral head sits in the shallow glenoid. The cuff "
            "presses the head into the socket with force Fc (red); the dislocating force Ft (brown) the head resists "
            f"is at most Fc tan alpha, with socket half-arc alpha about {ALPHA_SH:.0f} degrees, so tan alpha is "
            f"{math.tan(math.radians(ALPHA_SH)):.2f}; the blue dashed rim line carries the resultant at the limit. Right, "
            f"a hip: the deep acetabulum has half-arc about {ALPHA_HIP:.0f} degrees, tan alpha "
            f"{math.tan(math.radians(ALPHA_HIP)):.2f}, so the hip resists a dislocating force about three and a half times as large "
            "for the same compression.")
    return finish(VB, aria, s, o)


# ================================================================ small shared pieces for C8-C10, D1
def arc(s, p, cx, cy, r, a0, a1, meaning="geometry"):
    """Arc about (cx, cy) from screen angle a0 to a1 (deg, + = clockwise), slim head at a1."""
    q = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))  # noqa: E731
    (x0, y0), (x1, y1) = q(a0), q(a1)
    big = 1 if abs(a1 - a0) > 180 else 0
    w = "geom" if meaning in ("geometry", "dim") else "force"
    return (f'<path d="M{x0:.2f},{y0:.2f} A{r:.2f},{r:.2f} 0 {big} {1 if a1 > a0 else 0} {x1:.2f},{y1:.2f}" fill="none" '
            f'stroke="{O[meaning]}" stroke-width="{s(H.PX[w]):.2f}" marker-end="url(#{p}a_{meaning})"/>')


def dash_arc(s, cx, cy, r, a0, a1, col=O["dim"]):
    """Dashed circular arc (a <path>, so the overlap gate does not treat it as a curve)."""
    q = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))  # noqa: E731
    (x0, y0), (x1, y1) = q(a0), q(a1)
    return (f'<path d="M{x0:.2f},{y0:.2f} A{r:.2f},{r:.2f} 0 {1 if abs(a1 - a0) > 180 else 0} {1 if a1 > a0 else 0} '
            f'{x1:.2f},{y1:.2f}" fill="none" stroke="{col}" stroke-width="{s(H.PX["ref"]):.2f}" '
            f'stroke-dasharray="{s(H.DASH_REF[0]):.2f} {s(H.DASH_REF[1]):.2f}"/>')


def arm_pose(sh, el, wr=0.0, seated=True):
    leg = dict(hip=90, knee=90) if seated else {}
    return LB.pose(near=dict(leg, shoulder=sh, elbow=el, wrist=wr), far=dict(leg))


# ================================================================ svg #28  C8 the vigorous wave (Lab B numbers)
M2_KG, LC2_M, I2_KGM2, A_WAVE = 1.65, 0.22, 0.025, 0.5          # Lab B / Appendix (lines 333-336, 541)
M22 = I2_KGM2 + M2_KG * LC2_M ** 2                               # 0.10486 kg m^2
GRAV_BOUND = M2_KG * LC2_M * G                                   # m2 lc2 g = 3.56 N m (lines 173, 541)


def inertial_peak(f):
    return M22 * A_WAVE * (2 * math.pi * f) ** 2


F_CROSS = math.sqrt(GRAV_BOUND / (M22 * A_WAVE)) / (2 * math.pi)
close(M22, 0.10486, 1e-4)
close(F_CROSS, 1.31, 0.005)                                      # line 541
assert [round(inertial_peak(1.5), 1), round(inertial_peak(3.0), 1)] == [4.7, 18.6]          # lines 355, 367
close(inertial_peak(3.0) / inertial_peak(1.5), 4.0, 1e-9)


def fig28():
    p = "m11f28_"
    VB, s = VBs(566)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    el0 = math.degrees(1.0)                                       # Lab B: theta_2 = -1.0 rad = 57.3 deg of elbow flexion
    dA = math.degrees(A_WAVE)
    HF = 228.0
    P = arm_pose(100, el0)
    sv, J = put2(s, P, 8.0, 262.0, HF)
    o += [chair(s, J), floor(s, 4, 170, J["floor_y"])]
    for d in (-dA, dA):
        o.append(ghost(arm_pose(100, el0 + d), s, J, 0.34, names=("arm_fore", "arm_hand")))
    o.append(sv)
    ep = fig_pt(J, P, fk(100, el0)["elbow"])
    o.append(H.joint_centre(s, *ep))
    a_lo, a_hi = -(-90 + 100 + el0 - dA), -(-90 + 100 + el0 + dA)         # screen angles of the two forearm ends
    o.append(arc(s, p, ep[0], ep[1], 0.20 * HF, a_lo, a_hi))
    o.append(lines(s, 196, 150, ["the wave: elbow swings", f"{el0:.0f}° ± {dA:.0f}° (θ{sub('2', s, 'label2')} = −1.0 ± 0.5 rad)",
                                 "", "gravity part: set by posture,", "the same at every frequency",
                                 "", f"inertial part: M{sub('22', s, 'label2')} × angular", "acceleration, amplitude",
                                 f"M{sub('22', s, 'label2')} A (2πf)²"], "label2", fill=I["secondary"], lead=1.32))
    P2 = Plot(s, (62, 336, 378, 466), (0, 3.2), (0, 24))
    f = np.linspace(0, 3.2, 161)
    inert = np.array([inertial_peak(v) for v in f])
    o.append(P2.axes([(v, f"{v:g}") for v in (0, 1, 2, 3)], [(v, f"{v}") for v in (0, 6, 12, 18, 24)],
                     "wave frequency f (Hz)", "elbow torque amplitude (N m)", grid=(6, 12, 18, 24), ytx=18))
    o.append(P2.curve(f, np.full_like(f, GRAV_BOUND), O["load"], multi=True, dash=H.DASH_REF))
    o.append(P2.curve(f, inert, SER[1], multi=True))
    o.append(dot(s, P2.X(F_CROSS), P2.Y(GRAV_BOUND), O["flag"], 5))
    o.append(plabel(s, P2.X(F_CROSS) - 8, P2.Y(GRAV_BOUND) - 8, f"crossover {F_CROSS:.2f} Hz", "label2", I["primary"], "end"))
    for fv in (1.5, 3.0):
        o.append(P2.dot(fv, inertial_peak(fv), SER[1]))
    q15 = (P2.X(1.5), P2.Y(inertial_peak(1.5)))
    o.append(H.line(s, q15[0] - s(2), q15[1] - s(5), P2.X(0.95), P2.Y(10.5) + s(4), I["muted"], "leader"))
    o.append(plabel(s, P2.X(0.95) - 2, P2.Y(10.5), f"1.5 Hz: {inertial_peak(1.5):.1f} N m", "label2", I["primary"], "end"))
    o.append(plabel(s, P2.X(3.0) - 8, P2.Y(inertial_peak(3.0)) - 10, f"3 Hz: {inertial_peak(3.0):.1f} N m", "label2", I["primary"], "end"))
    o.append(plabel(s, P2.x1 - 2, P2.Y(GRAV_BOUND) - 8, f"gravity ≤ {GRAV_BOUND:.2f} N m", "label2", I["primary"], "end"))
    o.append(plabel(s, P2.X(0.06), P2.Y(22), "double f: four times the", "label2", I["secondary"], "start"))
    o.append(plabel(s, P2.X(0.06), P2.Y(22) + 16, "inertial torque", "label2", I["secondary"], "start"))
    o.append(legend(s, 62, 320, [(SER[1], "inertial", None), (O["load"], "gravity bound m₂ℓc₂g", H.DASH_REF)], gap=10))
    o.append(credit(s, VB))
    aria = ("Top left, a seated skeleton (Lynch art) waves: the elbow swings 57 degrees plus or minus 29 degrees "
            "(theta 2 = -1.0 plus or minus 0.5 rad), faint forearms at the two ends. Below, the elbow torque amplitude "
            "against wave frequency f from 0 to 3.2 Hz. The inertial part M22 A (2 pi f)^2 rises as f squared: "
            f"{inertial_peak(1.5):.1f} N m at 1.5 Hz and {inertial_peak(3.0):.1f} N m at 3 Hz, four times as much for twice "
            f"the frequency. The gravity part is bounded by m2 lc2 g = {GRAV_BOUND:.2f} N m and does not depend on f. "
            f"The two cross at {F_CROSS:.2f} Hz.")
    hv = hov(P2, f, [inert], lambda i: f"f = {f[i]:.2f} Hz: inertial {inert[i]:.1f} N m, gravity bound {GRAV_BOUND:.2f} N m")
    return finish(VB, aria, s, o, H.hover_attr(P2.box, hv))


# ================================================================ svg #29  C9 the pinned fingertip
def by_wrist(T, wr):
    """Self-motion of the 3-joint arm (shoulder, elbow, wrist) with the fingertip at T (body units): for a given wrist
    angle the forearm and the turned hand are one rigid second link; Proposition 3.1 then gives (shoulder, elbow)."""
    vx, vy = LF + LH * math.cos(math.radians(wr)), LH * math.sin(math.radians(wr))
    l2e, psi = math.hypot(vx, vy), math.degrees(math.atan2(vy, vx))
    x, y = T[0] - SHO[0], SHO[1] - T[1]
    c2 = (x * x + y * y - LU ** 2 - l2e ** 2) / (2 * LU * l2e)
    t2 = math.acos(c2)
    t1 = math.atan2(y, x) - math.atan2(l2e * math.sin(t2), LU + l2e * math.cos(t2))
    return math.degrees(t1) + 90.0, math.degrees(t2) - psi


def fig29():
    p = "m11f29_"
    VB, s = VBs(470)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 410.0, 410.0
    T = (SHO[0] + 0.50 * 100 * CM, SHO[1])             # design: the fingertip on a wall 0.50 m ahead of the shoulder, at its height
    wrs = [-60.0, -30.0, 0.0, 30.0, 60.0]                # design: wrist angles of the five postures
    qs = [by_wrist(T, w) + (w,) for w in wrs]
    for sh, el, wr in qs:
        assert math.dist(fk(sh, el, wr)["fingertip"], T) < 1e-6 and 0 < el < 150
    # null space at the middle posture: the 2x3 Jacobian has full row rank, so dim N(J) = 3 - 2 = 1, and the
    # family's tangent (d shoulder, d elbow, d wrist) lies in N(J)
    tip = lambda q: np.array(fk(*q)["fingertip"])  # noqa: E731
    q0 = np.array(qs[2])
    Jn = np.zeros((2, 3))
    for k in range(3):
        dq = np.zeros(3)
        dq[k] = 1e-4
        Jn[:, k] = (tip(q0 + dq) - tip(q0 - dq)) / 2e-4
    U_, sv_, Vt_ = np.linalg.svd(Jn)
    assert sv_[1] > 1e-3 * sv_[0]
    dwr = 1e-3
    dq = np.array(by_wrist(T, dwr) + (dwr,)) - np.array(by_wrist(T, -dwr) + (-dwr,))
    assert abs(float(Vt_[2] @ dq)) / np.linalg.norm(dq) > 0.9999
    P = [arm_pose(q[0], q[1], q[2]) for q in qs]
    sv, J = put2(s, P[2], 18.0, fy, HF)
    tgt = fig_pt(J, P[2], T)
    sp = fig_pt(J, P[2], SHO)
    o += [chair(s, J), floor(s, 4, 392, fy)]
    o.append(H.line(s, tgt[0] + s(3), tgt[1] - 0.20 * HF, tgt[0] + s(3), tgt[1] + 0.24 * HF, I["rule"], "axis"))     # the wall
    o.append(lab(s, tgt[0] + s(10), tgt[1] + 0.24 * HF, "wall", "label2", I["secondary"], "start"))
    for k in (0, 1, 3, 4):
        o.append(ghost(P[k], s, J, 0.42))
    o.append(sv)
    ep = [fig_pt(J, P[k], fk(*qs[k])["elbow"]) for k in range(5)]
    R = math.dist(sp, ep[2])
    angs = [math.degrees(math.atan2(e[1] - sp[1], e[0] - sp[0])) for e in ep]
    o.append(dash_arc(s, sp[0], sp[1], R, min(angs) - 3, max(angs) + 3))
    for k in (0, 2, 4):
        o.append(H.joint_centre(s, *ep[k]))
    o.append(ring(s, tgt[0], tgt[1], O["force"], 7))
    o.append(lab(s, tgt[0] - s(10), tgt[1] - 0.20 * HF - s(8), "fingertip fixed", "label", I["primary"], "end"))
    o.append(H.line(s, tgt[0] - s(2), tgt[1] - s(9), tgt[0] - s(6), tgt[1] - 0.20 * HF - s(2), I["muted"], "leader"))
    o.append(lab(s, 392, 22, "three joints, two constraints:", "label", I["primary"], "end"))
    o.append(lab(s, 392, 22 + s(17), "a one-dimensional self-motion", "label", I["primary"], "end"))
    o.append(lab(s, 392, 22 + s(35), "faint arms: other postures, same", "label2", I["secondary"], "end"))
    o.append(lab(s, 392, 22 + s(51), "fingertip; forearm and hand turn", "label2", I["secondary"], "end"))
    o.append(lab(s, 392, 22 + s(67), "about it as the elbow moves", "label2", I["secondary"], "end"))
    swing = max(math.dist(a, b) for a in ep for b in ep) / (J["scale"] * CM)
    o.append(lab(s, ep[0][0] + s(12), ep[0][1] + s(22), f"elbow moves {swing:.0f} cm", "label2", I["primary"], "start"))
    o.append(credit(s, VB))
    aria = ("A seated skeleton (Lynch art) presses a fingertip on a wall 0.50 m ahead of the shoulder, at shoulder "
            "height (red ring). Five postures of the three-joint arm, shoulder, elbow and wrist, put the fingertip on "
            f"that spot (the middle one solid, the others faint): the wrist angle runs from {wrs[0]:.0f} to {wrs[-1]:.0f} "
            "degrees while shoulder and elbow adjust, so the forearm and hand fan out about the fingertip and the "
            f"elbow moves {swing:.0f} cm along the short dashed arc. The Jacobian is 2 by 3 of full rank, so its null space has "
            "dimension 3 minus 2 = 1, and these postures lie along it.")
    return finish(VB, aria, s, o)


# ================================================================ svg #30  C10 the frantic last centimetre
def fig30():
    p = "m11f30_"
    VB, s = VBs(592)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 272.0, 312.0
    sh0 = 100.0                                                       # design: arm straight, 10 deg above horizontal
    P = arm_pose(sh0, 0.0)
    sv, J = put2(s, P, 8.0, fy, HF)
    sp = fig_pt(J, P, SHO)
    tip = fig_pt(J, P, fk(sh0, 0.0)["fingertip"])
    R = math.dist(sp, tip)
    ang = math.degrees(math.atan2(tip[1] - sp[1], tip[0] - sp[0]))        # screen angle of the straight arm
    o += [chair(s, J), floor(s, 4, 392, fy)]
    o.append(dash_arc(s, sp[0], sp[1], R, ang - 34, ang + 40))
    o.append(sv)
    o.append(ring(s, tip[0], tip[1], O["force"], 7))
    ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    tx, ty = uy, -ux                                                      # tangent, pointing up along the arc
    o.append(H.arrow(s, p, tip[0] + ux * s(10), tip[1] + uy * s(10), tip[0] + ux * s(52), tip[1] + uy * s(52), "dim"))
    o.append(H.arrow(s, p, tip[0] + tx * s(9), tip[1] + ty * s(9), tip[0] + tx * s(50), tip[1] + ty * s(50), "geometry"))
    o.append(H.arrow(s, p, tip[0] - tx * s(9), tip[1] - ty * s(9), tip[0] - tx * s(50), tip[1] - ty * s(50), "geometry"))
    o.append(lab(s, tip[0] + ux * s(58), tip[1] + uy * s(58) + s(5), "outward: no motion", "label2", I["primary"]))
    o.append(lab(s, tip[0] - tx * s(46) + s(10), tip[1] - ty * s(46) + s(12), "along the arc: free", "label2", I["primary"]))
    p0 = (sp[0] + R * math.cos(math.radians(ang - 34)), sp[1] + R * math.sin(math.radians(ang - 34)))
    o.append(lab(s, p0[0] + s(10), p0[1] - s(2), f"workspace edge: r = ℓ{sub('1', s, 'label2')} + ℓ{sub('2', s, 'label2')}", "label2",
                 I["secondary"]))
    # the plot: elbow-angle cost of one more centimetre of reach, |d theta_2 / d r| (Proposition 3.1, line 156)
    l1, l2 = L1 / LB.H_U * 1.75, L2 / LB.H_U * 1.75
    rmax = l1 + l2
    r = np.linspace(0.40 * rmax, 0.99995 * rmax, 1200)
    th2 = np.arccos((r * r - l1 * l1 - l2 * l2) / (2 * l1 * l2))
    rate = r / (l1 * l2 * np.sin(th2)) * (180 / math.pi) / 100.0           # deg of theta_2 per cm of reach
    ymax = 14.0
    P2 = Plot(s, (62, 362, 378, 494), (0.40, 1.0), (0, ymax))
    o.append(P2.axes([(v, f"{v:g}") for v in (0.4, 0.6, 0.8, 1.0)], [(v, f"{v}") for v in (0, 4, 8, 12)],
                     "reach r / (ℓ₁ + ℓ₂)", "θ₂ change (deg per cm)", grid=(4, 8, 12), ytx=18))
    keep = rate <= ymax
    o.append(H.line(s, P2.X(1.0), P2.y0, P2.X(1.0), P2.y1, O["flag"], "ref", H.DASH_REF))
    o.append(P2.curve(r[keep] / rmax, rate[keep], SER[0]))
    vals = {}
    for v, anc in ((0.6, "start"), (0.9, "end"), (0.97, "end")):
        rr = v * rmax
        t2 = math.acos((rr * rr - l1 * l1 - l2 * l2) / (2 * l1 * l2))
        yv = rr / (l1 * l2 * math.sin(t2)) * (180 / math.pi) / 100.0
        vals[v] = yv
        o.append(P2.dot(v, yv, SER[0]))
        o.append(plabel(s, P2.X(v) + (8 if anc == "start" else -8), P2.Y(yv) - 8, f"{yv:.1f} at {v:.2f}", "label2", I["primary"], anc))
    o.append(plabel(s, P2.X(1.0) - 6, P2.y1 + 12, "→ ∞ at ℓ₁ + ℓ₂", "label2", I["primary"], "end"))
    o.append(plabel(s, P2.X(0.43), P2.Y(11.5), "θ₂ = arccos(…) has a vertical", "label2", I["secondary"], "start"))
    o.append(plabel(s, P2.X(0.43), P2.Y(11.5) + 16, "tangent at the end of the reach", "label2", I["secondary"], "start"))
    o.append(credit(s, VB))
    aria = ("Top, a seated skeleton (Lynch art) reaches with a straight arm to a target on the edge of the workspace, "
            "the dashed arc of radius l1 + l2 about the shoulder. At the hand, outward motion is blocked (grey arrow) and "
            "only motion along the arc is free (blue arrows). Below, the elbow-angle change needed per centimetre of "
            f"reach, d theta 2 / d r = r / (l1 l2 sin theta 2), against reach: {vals[0.9]:.1f} degrees per cm at 0.90 of "
            f"the full reach, {vals[0.97]:.1f} at 0.97, and unbounded at the full reach, where theta 2 = 0 and det J = 0.")
    hv = hov(P2, (r[keep] / rmax)[::6], [rate[keep][::6]], lambda i: f"r = {(r[keep] / rmax)[::6][i]:.3f} of the reach: "
                                                                    f"{rate[keep][::6][i]:.1f} deg per cm")
    return finish(VB, aria, s, o, H.hover_attr(P2.box, hv))


# ================================================================ svg #31  D1 forward kinematics and the workspace
def fig31():
    p = "m11f31_"
    VB, s = VBs(466)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    R_out = 160.0
    k = R_out / (L1 + L2)                                              # px per body unit
    HF = k * LB.H_U
    cx, cy = 190.0, 246.0
    th1, th2 = 25.0, 45.0                                              # design: theta_1, theta_2 (deg)
    sh, el = th1 + 90.0, th2
    P = arm_pose(sh, el, seated=False)
    Pst = arm_pose(sh, 0.0, seated=False)
    body_names = ("lat_head", "lat_trunk", "lat_pelvis", "arm_upper", "arm_fore", "arm_hand")
    keep = lambda Q: _only(Q, body_names)  # noqa: E731
    Pb, Ps = keep(P), keep(Pst)
    _, J0 = LB.draw(p, s, Pb, 0.0, 0.0, HF)
    x0, y0 = J0["shoulder"]
    sv, J = LB.draw(p, s, Pb, cx - x0, cy - y0, HF)
    J["_x"], J["_y"], J["_h"] = cx - x0, cy - y0, HF
    q = fk(sh, el)
    E, F = (fig_pt(J, Pb, q[n]) for n in ("elbow", "fingertip"))
    S0 = (cx, cy)
    close(math.dist(S0, E), L1 * k, 1e-9)
    close(math.dist(E, F), L2 * k, 1e-9)
    r_in = abs(math.dist(E, F) - math.dist(S0, E))
    o.append(f'<path d="M{cx - R_out:.2f},{cy:.2f} a{R_out:.2f},{R_out:.2f} 0 1 0 {2 * R_out:.2f},0 a{R_out:.2f},{R_out:.2f} 0 1 0 {-2 * R_out:.2f},0 Z '
             f'M{cx - r_in:.2f},{cy:.2f} a{r_in:.2f},{r_in:.2f} 0 1 0 {2 * r_in:.2f},0 a{r_in:.2f},{r_in:.2f} 0 1 0 {-2 * r_in:.2f},0 Z" '
             f'fill="{O["geometry"]}" fill-opacity="0.09" fill-rule="evenodd" stroke="none"/>')
    for rr in (R_out, r_in):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{rr:.2f}" fill="none" stroke="{O["geometry"]}" stroke-width="{s(H.PX["ref"]):.2f}" '
                 f'stroke-dasharray="{s(H.DASH_REF[0]):.2f} {s(H.DASH_REF[1]):.2f}"/>')
    o.append(H.arrow(s, p, cx - R_out - s(2), cy, cx + R_out + s(14), cy, "dim"))
    o.append(H.arrow(s, p, cx, cy + s(20), cx, cy - R_out - s(14), "dim"))
    o.append(lab(s, cx + R_out + s(18), cy + s(5), "x", "label", I["secondary"], "start", 'font-style="italic"'))
    o.append(lab(s, cx + s(8), cy - R_out - s(10), "y", "label", I["secondary"], "start", 'font-style="italic"'))
    o.append(ghost(Ps, s, J, 0.30, names=("arm_upper", "arm_fore", "arm_hand")))
    o.append(sv)
    o.append(H.joint_centre(s, *S0))
    o.append(H.joint_centre(s, *E))
    o.append(H.arrow(s, p, S0[0], S0[1], F[0], F[1], "force"))
    a1 = math.degrees(math.atan2(E[1] - S0[1], E[0] - S0[0]))
    a2 = math.degrees(math.atan2(F[1] - E[1], F[0] - E[0]))
    close(-a1, th1, 1e-6)
    close(-a2, th1 + th2, 1e-6)
    o.append(arc(s, p, S0[0], S0[1], 46, 0, a1))
    o.append(arc(s, p, E[0], E[1], 38, a1, a2))
    o.append(ext(s, E[0], E[1], E[0] + math.cos(math.radians(a1)) * s(62), E[1] + math.sin(math.radians(a1)) * s(62)))
    m1 = (S0[0] + 62 * math.cos(math.radians(a1 / 2)), S0[1] + 62 * math.sin(math.radians(a1 / 2)))
    o.append(lab(s, m1[0], m1[1] + s(5), f"θ{sub('1', s)}", "label", O["geometry"], "start"))
    m2 = (E[0] + 58 * math.cos(math.radians((a1 + a2) / 2)), E[1] + 58 * math.sin(math.radians((a1 + a2) / 2)))
    o.append(lab(s, m2[0], m2[1] + s(5), f"θ{sub('2', s)}", "label", O["geometry"], "start"))
    mid1 = ((S0[0] + E[0]) / 2, (S0[1] + E[1]) / 2)
    mid2 = ((E[0] + F[0]) / 2, (E[1] + F[1]) / 2)
    o.append(lab(s, mid1[0] + s(4), mid1[1] - s(10), f"ℓ{sub('1', s)}", "label", I["primary"], "end"))
    o.append(lab(s, mid2[0] + s(2), mid2[1] - s(12), f"ℓ{sub('2', s)}", "label", I["primary"], "end"))
    o.append(lab(s, F[0] + s(8), F[1] - s(6), '<tspan font-weight="bold">p</tspan> = (x, y)', "label", O["force"], "start"))
    o.append(lab(s, cx + s(30), cy + s(30), 'r = ‖<tspan font-weight="bold">p</tspan>‖', "label", O["force"], "start"))
    o.append(lab(s, cx - R_out * 0.70, cy - R_out * 0.50, "outer circle", "label2", I["secondary"], "start"))
    o.append(lab(s, cx - R_out * 0.70, cy - R_out * 0.50 + s(15), f"r = ℓ{sub('1', s, 'label2')} + ℓ{sub('2', s, 'label2')}", "label2",
                 I["secondary"], "start"))
    o.append(lab(s, cx - r_in - s(12), cy + s(28), f"inner circle r = |ℓ{sub('1', s, 'label2')} − ℓ{sub('2', s, 'label2')}|", "label2",
                 I["secondary"], "end"))
    o.append(lab(s, 200, 22, "reachable set = the annulus", "label", I["primary"], "middle"))
    o.append(lab(s, 200, 22 + s(17), f"|ℓ{sub('1', s, 'label2')} − ℓ{sub('2', s, 'label2')}| ≤ ‖p‖ ≤ ℓ{sub('1', s, 'label2')} + "
                 f"ℓ{sub('2', s, 'label2')}", "label2", I["secondary"], "middle"))
    o.append(credit(s, VB))
    aria = ("The planar two-link arm on the Lynch skeleton's arm art, shoulder at the origin of the x (forward) and y (up) "
            f"axes. The upper arm, length l1, makes angle theta 1 = {th1:.0f} degrees with the x-axis; the forearm with the "
            f"hand, length l2, makes angle theta 2 = {th2:.0f} degrees with the upper arm, and reaches the fingertip p = "
            "(x, y) at distance r = norm p. A faint straight arm (theta 2 = 0) reaches the outer circle r = l1 + l2; a "
            "fully folded arm would reach the inner circle r = |l1 - l2|; the shaded annulus between them is the reachable "
            "set, swept as theta 1 turns.")
    return finish(VB, aria, s, o)


def _only(Q, names):
    """A copy of pose Q keeping only the segments called `names` (the far arm included in the filter by name)."""
    Q2 = LB.Pose(Q.view)
    Q2.segs = [q for q in Q.segs if q[0] in names and not q[5]]
    Q2.j, Q2.com, Q2.anchor, Q2.floor_y = Q.j, Q.com, Q.anchor, Q.floor_y
    return Q2


FIGS = {
    21: ("C1: the waiter's tray. A waiter carries a tray on a flat han", fig21),
    22: ("C2: which elbow. Inverse kinematics offers two arm configura", fig22),
    23: ("C3: bend to place, straighten to brace. A surgeon threading ", fig23),
    24: ("C4: the soapy glass. Why does a wet or soapy glass demand a ", fig24),
    26: ("C6: the numb fingertip. After a dental anaesthetic block of ", fig26),
    27: ("C7: why the shoulder, not the hip. The shoulder dislocates f", fig27),
    28: ("C8: the vigorous wave. A brisk, fast wave tires the arm out ", fig28),
    29: ("C9: the pinned fingertip. Press your fingertip on a fixed sp", fig29),
    30: ("C10: the frantic last centimetre. Reaching for something at ", fig30),
    31: ("D1: forward kinematics and the workspace. Derive the endpoin", fig31),
}
