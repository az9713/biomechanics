"""Module 13 whole-body figures (main text). Exposes the Lynch body kit once per page.

svg #2 (Fig. 1 sit to stand), #3 (montage of four everyday movements), #4 (Fig. 2 the case-study pipeline), #5 (Fig. 3
seat-off knee torque), #6 (Fig. 4 stairs), #7 (Fig. 5 lifting and the low back), #8 (Fig. 6 turning, top view),
#9 (Fig. 7 jar and door), #10 (Fig. 8 slope), #11 (Fig. 9 shared reserves).

Numbers (module13.html line numbers):
  chair rise: m = 70 kg, m_up = 0.8 m = 56 kg (assumed), g = 9.81, d = 0.20 m, tau_knee = m_up g d = 110 N m, 1.57 N m/kg
  (86, 90, 96); stairs: h = 0.17 m, U = m g h = 117 J per step, f = 1.8 steps/s, P = 210 W (106, 108);
  lifting: W_tr = 412 N, l_t = 0.346 m, d_m = 0.05 m, 20 kg box at d_L = 0.40 m, phi = 60 deg: d_tr = 0.30 m, F_m = 4040 N,
  F_comp = 4350 N; squat phi = 20 deg, d_L = 0.25 m: F_comp = 2530 N; NIOSH 3400 N (126, 128); turning: m = 70 kg,
  v = 1.3 m/s, beta = 60 deg, J = 2 m v sin(beta/2) = 91 N s (146, 148); jar: tau_resist = 2 N m, r = 0.035 m,
  mu = 0.7, F_grip = 82 N, F_t = 57 N; door: tau_door = 20 N m, d_hinge = 0.8 m, F_hand = 25 N (168, 170, 178);
  slope: m = 70 kg, v = 1.0 m/s, theta = 5, 10, 15 deg: P = 60, 119, 178 W (184, 186).
Stature: the module states none; bodies are drawn at the course reference H = 1.75 m (m05/body.py H_REF_M).
Body art: lynch_body.py (Patrick J. Lynch, CC BY 2.5); the forearm of #4 is the NIH BioArt arm (public domain).
"""
import html
import math

import house as H
import lynch_body as LB
from m01.arm import NIH, Posed, arc, dim, sym
from m01.body import PLANTAR, TILT0, UM, bisect, grip, joints, smooth_closed, stoop
from m05.body import arc_arrow, finish, it, wrap

SHARED_DEFS = LB.SHARED_DEFS
T, O, I = H.TISSUE, H.OVERLAY, H.INK
RED, BLU, BRN = O["force"], O["geometry"], O["load"]
BOXFILL, GRID = "#f7f4ef", "#e6e6e6"
BODY = H.MAX_DISPLAY_H_BODY
H_M = 1.75                                  # m, course reference stature (drawing only)
G = 9.81
M_KG = 70.0
_S0 = H.Scale(100, 100)                     # LB.draw ignores the scale; used by the pose solvers only

# ---------------------------------------------------------------- chair rise (86, 90, 96)
M_UP = 0.8 * M_KG                            # 56 kg
D_CHAIR = 0.20                               # m
TAU_KNEE = M_UP * G * D_CHAIR                # 110 N m
assert (round(M_UP), round(TAU_KNEE), round(TAU_KNEE / M_KG, 2)) == (56, 110, 1.57), (M_UP, TAU_KNEE)
W_UP = M_UP * G                              # 549 N

# ---------------------------------------------------------------- stairs (106, 108)
H_STEP, F_STEP = 0.17, 1.8
U_STEP = M_KG * G * H_STEP
P_STAIR = U_STEP * F_STEP
assert (round(U_STEP), round(P_STAIR, -1)) == (117, 210), (U_STEP, P_STAIR)

# ---------------------------------------------------------------- lifting (124, 126, 128)
W_TR, W_L, D_M, NIOSH = 42.0 * G, 20.0 * G, 0.05, 3400.0            # N (412, 196), m, N
ELL_T = 0.30 / math.sin(math.radians(60.0))                       # 0.346 m, so that d_tr = 0.30 m at 60 deg


def lift_numbers(phi, d_l):
    d_tr = ELL_T * math.sin(math.radians(phi))
    f_m = (W_TR * d_tr + W_L * d_l) / D_M
    return d_tr, f_m, f_m + (W_TR + W_L) * math.cos(math.radians(phi))


assert [round(v, -1) for v in lift_numbers(60, 0.40)[1:]] == [4040, 4350], lift_numbers(60, 0.40)
assert round(lift_numbers(60, 0.40)[0], 2) == 0.30
assert [round(v, -1) for v in lift_numbers(20, 0.25)[1:]] == [1960, 2530], lift_numbers(20, 0.25)

# ---------------------------------------------------------------- turning, jar, door, slope
M_TURN, V_TURN, BETA = 70.0, 1.3, 60.0
J_TURN = 2 * M_TURN * V_TURN * math.sin(math.radians(BETA / 2))
assert round(J_TURN) == 91
TAU_RES, R_LID, MU_LID = 2.0, 0.035, 0.7
F_GRIP = TAU_RES / (MU_LID * R_LID)
F_TAN = MU_LID * F_GRIP
assert (round(F_GRIP), round(F_TAN)) == (82, 57)
TAU_DOOR, D_HINGE = 20.0, 0.8
F_HAND = TAU_DOOR / D_HINGE
assert round(F_HAND) == 25
SLOPE_P = {th: M_KG * G * 1.0 * math.sin(math.radians(th)) for th in (5, 10, 15)}
assert [round(v) for v in SLOPE_P.values()] == [60, 119, 178], SLOPE_P


# ================================================================ small helpers
def defs(p, s):
    return f"<defs>{H.markers(p, s)}</defs>"


def kit(P, x, y, hgt, **kw):
    """Kit body with its anchor point at (x, y); hgt = stature in figure units."""
    return LB.draw("", _S0, P, x, y, hgt, **kw)


def floor(s, x0, x1, y):
    return H.line(s, x0, y, x1, y, I["rule"], "axis")


def white_under(s, x1, y1, x2, y2, w=4):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#fff" '
            f'stroke-width="{s(w):.2f}" opacity="0.85"/>')


def dline(s, x1, y1, x2, y2, col=None, w="ref", dash=H.DASH_REF):
    """Dashed reference line with a white under-stroke so it reads over the art."""
    return white_under(s, x1, y1, x2, y2) + H.line(s, x1, y1, x2, y2, col or O["dim"], w, dash=dash)


def leader(s, x1, y1, x2, y2, col=None):
    return H.line(s, x1, y1, x2, y2, col or I["secondary"], "leader")


def rect(s, x, y, w, h, fill=BOXFILL, stroke=None, sw=1.3, extra=""):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" '
            f'stroke="{stroke or I["secondary"]}" stroke-width="{s(sw):.2f}" {extra}/>')


def text2(s, x, y, lines, anchor="start", size="label2", fill=None, dy=None, first="label"):
    """Several label lines; the first may use the main size."""
    out, fs = [], s(H.PX[size])
    for i, t in enumerate(lines):
        yy = y + (0 if i == 0 else (s(H.PX[first]) * 0.95 if i == 1 and first != size else 0) + (i - 1 if first != size else i) * (dy or fs * 1.3))
        out.append(H.label(s, x, yy, t, first if i == 0 else size, fill or (I["primary"] if i == 0 else I["secondary"]), anchor))
    return "".join(out)


def credit_at(s, VB, width=None, extra="", n=2, x=None):
    """Kit credit at the bottom of the figure."""
    width = width if width else VB[2] - s(16)
    y = VB[1] + VB[3] - s(6) - (n - 1) * s(H.PX["credit"]) * 1.25
    return LB.credit(s, VB[0] + s(8) if x is None else x, y, width=width, extra=extra)


def credit_lines(s, VB, extra="", x=None, width=None):
    """Credit anchored to the bottom edge, whatever number of lines the width wraps to."""
    width = width if width else VB[2] - s(16)
    probe = LB.credit(s, 0, 0, width=width, extra=extra)
    n = probe.count("<text")
    return credit_at(s, VB, width, extra, n, x)


def sym_(v, sb, s, size="label"):
    return sym(v, sb, s, size)


def asserted_box(bbox, VB, s, what):
    x0, y0, x1, y1 = bbox
    assert x0 >= VB[0] and y0 >= VB[1] and x1 <= VB[0] + VB[2] and y1 <= VB[1] + VB[3], (what, bbox, VB)


NAMES = {"head": "head_neck", "trunk": "pelvis_trunk", "upper_arm": "upper_arm", "forearm": "forearm", "hand": "hand",
         "thigh": "thigh"}


def com_above_knee(J):
    """Winter mass-weighted centre of everything above the knees (head, trunk, both arms, both thighs)."""
    sx = sy = m = 0.0
    for k, w in NAMES.items():
        for sfx in (("",) if k in ("head", "trunk") else ("", "_far")):
            c, mf = J["com_" + k + sfx], LB.WINTER[w]["mass_frac"]
            sx, sy, m = sx + c[0] * mf, sy + c[1] * mf, m + mf
    return (sx / m, sy / m), m


# ================================================================ svg #5  Fig. 3 seat-off knee torque
def seatoff_pose():
    """The kit's seat-off pose with the trunk turned until the COM of the body above the knees is d = 0.20 m
    from the knee (line 90): the horizontal distance is the Winter COM of head, trunk, arms and thighs."""
    base = dict(LB.POSES["sit_to_stand"])

    def pose_t(tr):
        kw = dict(base)
        kw["trunk"] = tr
        return LB.pose(**kw)

    def f(tr):
        J = joints(pose_t(tr))
        return (J["knee"][0] - com_above_knee(J)[0][0]) * UM
    tr = bisect(f, 0.0, 70.0, D_CHAIR)
    P = pose_t(tr)
    assert abs(f(tr) - D_CHAIR) < 1e-4
    return P, tr


def fig5():
    p = "m13f5_"
    VB = (0, 135, 760, 505)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    P, tr = seatoff_pose()
    hgt, fy, hx = 560.0, 490.0, 262.0
    body, J = kit(P, hx, fy, hgt)
    asserted_box(J["bbox"], VB, s, "fig5")
    k = hgt / H_M                                              # figure units per metre
    (cu, m_frac) = com_above_knee(J)
    knee = J["knee"]
    com = (knee[0] - D_CHAIR * k, cu[1])                       # x = the text's d; height = Winter's centre
    seat_y = knee[1] + 0.012 * hgt
    sx0, sx1 = J["hip"][0] - 0.30 * k, knee[0] - 0.13 * k
    o = [defs(p, s), floor(s, 20, 740, fy),
         rect(s, sx0, seat_y, sx1 - sx0, s(7), "#e9e2d6", I["secondary"], 1.2),
         H.line(s, sx0 + s(8), seat_y + s(7), sx0 + s(8), fy, I["secondary"], "ref"),
         H.line(s, sx1 - s(8), seat_y + s(7), sx1 - s(8), fy, I["secondary"], "ref"),
         body]
    o.append(H.label(s, sx0 + s(14), fy - s(34), "seat", "label2", I["secondary"]))
    # plumb lines through the knee and through the COM, and the arm d between them under the floor line
    yd = fy + s(26)
    o.append(dline(s, knee[0], knee[1] + s(8), knee[0], yd + s(8)))
    o.append(dline(s, com[0], com[1] + s(40), com[0], yd + s(8)))
    o.append(dim(s, p, com[0], knee[0], yd, BLU, "geometry"))
    o.append(H.label(s, com[0] - s(8), yd + s(5), f'{it("d")} = 0.20 m', fill=BLU, anchor="end"))
    # weight of the body above the knees
    o.append(H.com_mark(s, *com))
    wy = fy - s(30)
    o.append(H.arrow(s, p, com[0], com[1] + s(9), com[0], wy, "load"))
    o.append(H.joint_centre(s, *knee))
    # muscle torque: extensor torque about the knee, clockwise on the page (the weight line falls behind the knee)
    o.append(arc_arrow(s, p, knee[0], knee[1], s(34), -72, 58, "force"))
    # labels on the right
    lx = 520.0
    ty = knee[1] - s(2)
    o.append(leader(s, knee[0] + s(40), ty, lx - s(8), ty))
    o.append(H.label(s, lx, ty - s(5), f'{sym("τ", "knee", s)} = {sym("m", "up", s)}{it("g d")} ≈ 110 N m', fill=RED))
    o.append(H.label(s, lx, ty + s(13), "= 1.57 N m per kg of body mass", "label2", I["secondary"]))
    o.append(H.label(s, lx, ty + s(31), "knee extensors: the demand", "label2", I["secondary"]))
    o.append(leader(s, com[0] + s(10), com[1], lx - s(8), com[1] - s(70)))
    cy0 = com[1] - s(70)
    o.append(H.label(s, lx, cy0 - s(22), "COM of the body above the knees", "label2", I["secondary"]))
    o.append(H.label(s, lx, cy0 - s(4), f'{sym("m", "up", s)} = 0.8 {it("m")} = 56 kg (assumed)', fill=BRN))
    o.append(H.label(s, lx, cy0 + s(16), f'{sym("W", "", s)} = {sym("m", "up", s)}{it("g")} ≈ 549 N', fill=BRN))
    o.append(H.label(s, lx, cy0 + s(34), f"acts {it('d')} = 0.20 m behind the knee", "label2", I["secondary"]))
    o.append(H.label(s, lx, fy - s(70), "A lower seat moves the COM further", "label2", I["secondary"]))
    o.append(H.label(s, lx, fy - s(52), f"behind the knee: {it('d')} and the demand grow.", "label2", I["secondary"]))
    o.append(credit_lines(s, VB, " Seat, arrows and marks drawn for this course; arrows are not to force scale."))
    aria = ("Side view of a skeleton at seat-off from a chair, facing right: the thighs are near horizontal on the seat, "
            "the trunk is pitched forward. The centre of mass of the body above the knees, mass 56 kilograms, is marked "
            "0.20 metres behind the knee on a horizontal distance d; its weight of about 549 newtons acts straight down "
            "from it. A curved arrow at the knee shows the extensor torque of about 110 newton metres, 1.57 newton "
            "metres per kilogram, that balances the weight moment.")
    return finish(VB, aria, s, o)


# ================================================================ svg #7  Fig. 5 lifting and the low back
def squat_pose(phi=20.0, reach=0.25, grip_h=0.35, pel=25.0):
    """Squat lift: trunk phi from vertical, arms straight with the grip `reach` m ahead of L5/S1 and `grip_h` m above the
    floor, the COM of body + box over the middle of the foot. Solved with three bisections nested as a Gauss-Seidel loop."""
    from scipy.optimize import least_squares
    tr = phi - TILT0 - pel

    def pose_v(v):
        d = dict(hip=v[1], knee=v[0], shoulder=v[2])
        return LB.pose(pelvis=pel, trunk=tr, near=dict(d), far=dict(d))

    def res(v):
        J = joints(pose_v(v))
        g = grip(J)
        comx = (J["com"][0] * M_KG + g[0] * 20.0) / (M_KG + 20.0)
        return [((J["floor_y"] - g[1]) * UM - grip_h) * 10, ((g[0] - J["l5s1"][0]) * UM - reach) * 10,
                ((comx - J["ankle"][0]) * UM - 0.05) * 10]
    r = least_squares(res, [125, 115, 40])
    assert max(abs(v) for v in r.fun) < 1e-6, r.fun
    return pose_v(r.x), r.x


def lift_panel(p, s, k, heel, phi, d_l, P, detail):
    """One lifting figure: kit body (anchor heel), box in the hands, weights, arms and the erector spinae.
    detail=True: values on every label; False: symbols only (the loads are the same as in the other panel)."""
    body, J = kit(P, heel[0], heel[1], H_M * k)
    L5 = J["l5s1"]
    ax = (J["neck"][0] - L5[0], J["neck"][1] - L5[1])
    n = math.hypot(*ax)
    u = (ax[0] / n, ax[1] / n)                              # unit vector up the trunk
    bk = LB.rot(u, -90)                                     # toward the back

    def along(t, nrm=0.0):
        return (L5[0] + t * k * u[0] + nrm * k * bk[0], L5[1] + t * k * u[1] + nrm * k * bk[1])
    beta = math.degrees(math.atan2(u[0], -u[1]))
    assert abs(beta - phi) < 0.05, (beta, phi)
    Gp = grip(J)
    assert abs((Gp[0] - L5[0]) / k - d_l) < 2e-3, ((Gp[0] - L5[0]) / k, d_l)
    d_tr, f_m, f_c = lift_numbers(phi, d_l)
    Cub = along(ELL_T)
    assert abs((Cub[0] - L5[0]) / k - d_tr) < 1e-3
    bw, bh = 0.30 * k, 0.24 * k
    by = Gp[1] - 0.02 * k
    Bc = (Gp[0], by + bh / 2)
    fy = heel[1]
    o = [rect(s, Gp[0] - bw / 2, by, bw, bh, BOXFILL, BRN, 1.3), body]
    if detail:
        o.append(H.label(s, Bc[0], Bc[1] + s(5), "20 kg", "label2", I["secondary"], "middle"))
    y_l = fy + s(22)
    y_tr = L5[1] + 0.28 * k if detail else fy + s(46)
    o.append(H.line(s, *along(-0.10), *along(ELL_T + 0.05), O["dim"], "leader", H.DASH_REF))
    o.append(dline(s, L5[0], L5[1] + s(8), L5[0], max(y_l, y_tr) + s(6)))
    r_b = 0.085 * k
    o.append(arc(s, L5[0], L5[1], r_b, 90.0, 90.0 + phi, BLU, 1.6))
    t1 = 0.27
    o.append(H.arrow(s, p, *along(t1, D_M), *along(0.05, D_M), "force"))
    o.append(H.line(s, *L5, *along(0.0, D_M), BLU, "geom"))
    tail = along(t1, D_M)
    o.append(H.joint_centre(s, *L5))
    r0, r1 = along(-0.16, -0.015), along(-0.02, -0.015)
    o.append(H.arrow(s, p, *r0, *r1, "reaction"))
    o.append(H.com_mark(s, *Cub))
    w1 = (y_tr - s(10)) if detail else (Cub[1] + 0.20 * k)
    o.append(H.arrow(s, p, Cub[0], Cub[1] + s(8), Cub[0], w1, "load"))
    if not detail:
        o.append(H.line(s, Cub[0], w1 + s(2), Cub[0], y_tr + s(6), O["dim"], "leader", H.DASH_REF))
    wl0, wl1 = by + bh + s(1), fy - s(14)
    o.append(H.arrow(s, p, Bc[0], wl0, Bc[0], wl1, "load"))
    o.append(H.line(s, Bc[0], wl1 + s(2), Bc[0], y_l + s(6), O["dim"], "leader", H.DASH_REF))
    o.append(dim(s, p, L5[0], Cub[0], y_tr, BRN, "load"))
    o.append(dim(s, p, L5[0], Bc[0], y_l, BRN, "load"))
    if detail:
        o.append(H.label(s, L5[0] + s(6), y_tr + s(18), f'{sym("d", "tr", s)} = {d_tr:.2f} m', fill=BRN, anchor="start"))
    else:
        o.append(H.label(s, Cub[0] + s(8), y_tr + s(5), f'{sym("d", "tr", s)} = {d_tr:.2f} m', fill=BRN, anchor="start"))
    o.append(H.label(s, (L5[0] + Bc[0]) / 2 if detail else Bc[0] + s(8), y_l + (s(18) if detail else s(5)),
                     f'{sym("d", "L", s)} = {d_l:.2f} m', fill=BRN, anchor="middle" if detail else "start"))
    if detail:
        o.append(H.label(s, Cub[0] + s(8), w1 - s(24), f'{sym("W", "tr", s)}', fill=BRN))
        o.append(H.label(s, Cub[0] + s(8), w1 - s(6), "= 412 N", fill=BRN))
        o.append(H.label(s, Bc[0] + s(9), wl1 - s(22), f'{sym("W", "L", s)}', fill=BRN))
        o.append(H.label(s, Bc[0] + s(9), wl1 - s(4), "= 196 N", fill=BRN))
    else:
        o.append(H.label(s, Cub[0] + s(8), Cub[1] + s(40), f'{sym("W", "tr", s)}', fill=BRN))
        o.append(H.label(s, Bc[0] + s(9), wl1 - s(4), f'{sym("W", "L", s)}', fill=BRN))
    o.append(H.label(s, tail[0] - s(10), tail[1] - s(6), f'{sym("F", "m", s)} ≈ {round(f_m, -1):.0f} N', fill=RED, anchor="end"))
    o.append(H.label(s, tail[0] - s(10), tail[1] + s(11), "erector spinae", "label2", I["secondary"], "end"))
    o.append(H.label(s, r0[0] - s(8), r0[1] + s(4), f'{sym("F", "comp", s)}', fill=I["primary"], anchor="end"))
    o.append(H.label(s, r0[0] - s(8), r0[1] + s(22), f"≈ {round(f_c, -1):.0f} N", fill=I["primary"], anchor="end"))
    o.append(H.label(s, L5[0] - s(14), L5[1] - s(12), "L5/S1", "label2", anchor="end"))
    if detail:
        o.append(H.label(s, L5[0] + s(8), L5[1] + r_b + s(14), f"φ = {phi:.0f}°", fill=BLU, anchor="start"))
    else:                                   # the arc is narrow: label right of the W_tr plumb line, with a leader
        am = math.radians(90.0 + phi / 2)
        ax0, ay0 = L5[0] + r_b * math.cos(am), L5[1] + r_b * math.sin(am)
        lx, ly = Cub[0] + s(10), L5[1] + r_b + s(24)
        o.append(leader(s, ax0, ay0, lx - s(3), ly - s(5), BLU))
        o.append(H.label(s, lx, ly, f"φ = {phi:.0f}°", fill=BLU, anchor="start"))
    lab = dict(tail=tail, Cub=Cub, L5=L5, J=J, f_m=f_m, f_c=f_c)
    return "".join(o), lab


def lift_bars(s, p, x0, x1, ytop, ybase, stoop_c, squat_c):
    """Disc compression of the two lifts against the NIOSH limit: two vertical bars, hover on each."""
    ymax = 5000.0
    Y = lambda v: ybase - (ybase - ytop) * v / ymax         # noqa: E731
    o = [H.label(s, x0, ytop - s(26), "disc compression F" + H.sub("comp", s, "label2") + " (N)", "label2", I["secondary"])]
    for v in (0, 2000, 4000):
        o.append(H.line(s, x0, Y(v), x1, Y(v), GRID if v else I["axis"], "ref" if v == 0 else "leader"))
        o.append(H.label(s, x0 - s(6), Y(v) + s(4), f"{v}", "tick", I["secondary"], "end"))
    bw = (x1 - x0) * 0.17
    cx = (x0 + (x1 - x0) * 0.25, x0 + (x1 - x0) * 0.60)
    pts = []
    for c, v, nm in ((cx[0], stoop_c, "stoop, φ = 60°"), (cx[1], squat_c, "squat, φ = 20°")):
        o.append(rect(s, c - bw / 2, Y(v), bw, ybase - Y(v), I["secondary"], I["axis"], 1.0))
        o.append(H.label(s, c, Y(v) - s(6), f"{round(v, -1):.0f} N", "label2", I["primary"], "middle"))
        o.append(H.label(s, c, ybase + s(17), nm, "label2", I["secondary"], "middle"))
        pct = (v / NIOSH - 1) * 100
        pts.append([c, Y(v), f"{nm}: F comp = {round(v, -1):.0f} N, {abs(pct):.0f}% {'above' if pct > 0 else 'below'} the NIOSH limit"])
    o.append(H.line(s, x0, Y(NIOSH), x1, Y(NIOSH), O["flag"], "geom", dash=H.DASH_REF))
    o.append(H.label(s, x1 + s(8), Y(NIOSH) + s(5), "NIOSH limit 3400 N", "label2", I["primary"]))
    box = (x0, ytop, x1, ybase)
    return "".join(o), H.hover_attr(box, pts)


def fig7():
    p = "m13f7_"
    VB = (0, 0, 760, 780)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    k, fy = 300.0, 470.0
    o = [defs(p, s), floor(s, 12, 748, fy)]
    P1 = LB.pose(**stoop(60.0, 0.40))
    svg1, a = lift_panel(p, s, k, (150.0, fy), 60.0, 0.40, P1, True)
    P2, _ = squat_pose(20.0, 0.25)
    svg2, b = lift_panel(p, s, k, (520.0, fy), 20.0, 0.25, P2, False)
    o += [svg1, svg2]
    o.append(H.label(s, 12, 22, "stoop: trunk 60° from vertical, box 0.40 m ahead", "label2", I["secondary"]))
    o.append(H.label(s, 748, 22, "squat: trunk 20°, box pulled in to 0.25 m", "label2", I["secondary"], "end"))
    bars, hov = lift_bars(s, p, 90, 440, 590, 710, a["f_c"], b["f_c"])
    o.append(bars)
    o.append(credit_lines(s, VB, " Box, arrows and marks drawn for this course; arrows are not to force scale."))
    aria = ("Two side views of a skeleton lifting a 20 kg box, facing right. Left, a stoop with the trunk 60 degrees from "
            "vertical and the box 0.40 metres ahead of the L5/S1 disc: the upper-body weight of 412 newtons acts 0.30 "
            "metres ahead of the disc, the box weight of 196 newtons 0.40 metres ahead, and the erector spinae pull of about "
            "4040 newtons runs along the back 5 centimetres behind the disc, so the disc is compressed with about 4350 "
            "newtons. Right, a squat with the trunk 20 degrees from vertical and the box pulled in to 0.25 metres: "
            "the disc compression is about 2530 newtons. A bar chart compares the two with the NIOSH limit of 3400 newtons.")
    return finish(VB, aria, s, o, hov)


# ================================================================ svg #6  Fig. 4 stairs
TREAD = 0.30                                  # m, drawing only (the text gives only the riser h)


def stair_pose(h=H_STEP, tread=TREAD):
    """Climbing: both feet flat on treads, the rear (far) foot one riser h below the near foot and one tread behind it.
    The near hip and knee flexion are solved from those two foot positions."""
    from scipy.optimize import least_squares

    def mk(v):
        far = dict(hip=-8, knee=10, shoulder=20, elbow=20, contact="flat")
        near = dict(hip=v[0], knee=v[1], shoulder=-15, elbow=15, contact="flat")
        return LB.pose(pelvis=5, trunk=5, near=near, far=far, anchor=("heel", "far"))

    def res(v):
        J = joints(mk(v))
        return [((J["heel"][0] - J["heel_far"][0]) * UM - tread) * 10, ((J["heel_far"][1] - J["heel"][1]) * UM - h) * 10]
    r = least_squares(res, [60, 70])
    assert max(abs(v) for v in r.fun) < 1e-6
    return mk(r.x)


def stairs(s, k, x_heel, y_heel_far, n_far, n0, n1, fy):
    """Staircase to scale: the rear heel stands on step n_far, 0.02 m behind its riser. Returns (svg, X, Y)."""
    def X(n):
        return x_heel - 0.02 * k + (n - n_far) * TREAD * k

    def Y(n):
        return y_heel_far - (n - n_far) * H_STEP * k
    pts = [(X(n0), fy)]
    for n in range(n0, n1 + 1):
        pts += [(X(n), Y(n)), (X(n + 1), Y(n))]
    pts += [(X(n1 + 1), fy)]
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    return (f'<path d="{d}" fill="#e9e2d6" stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}" stroke-linejoin="round"/>',
            X, Y)


def fig6():
    p = "m13f6_"
    VB = (0, 0, 760, 545)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    P = stair_pose()
    hgt, fy = 380.0, 482.0
    k = hgt / H_M
    n_far, xh = 2, 230.0
    yh = fy - n_far * H_STEP * k
    body, J = kit(P, xh, yh, hgt)
    asserted_box(J["bbox"], VB, s, "fig6")
    st, X, Y = stairs(s, k, xh, yh, n_far, 0, 4, fy)
    o = [defs(p, s), st, body]
    # riser height, beside the first riser
    xd = X(1) - s(12)
    o.append(dline(s, X(1) - s(22), Y(1), X(1), Y(1)))
    o.append(H.arrow(s, p, xd, Y(0), xd, Y(1), "geometry", both=True))
    o.append(H.label(s, xd - s(8), (Y(0) + Y(1)) / 2 + s(5), f'{it("h")} = 0.17 m', fill=BLU, anchor="end"))
    # COM now and one step later: it rises by h
    com = J["com"]
    com2 = (com[0] + TREAD * k, com[1] - H_STEP * k)
    xs = com2[0] + s(40)
    o.append(dline(s, com[0] + s(8), com[1], xs + s(6), com[1]))
    o.append(dline(s, com2[0] + s(8), com2[1], xs + s(6), com2[1]))
    o.append(H.com_mark(s, *com))
    o.append(f'<g opacity="0.55">{H.com_mark(s, *com2)}</g>')
    o.append(H.arrow(s, p, xs, com[1], xs, com2[1], "geometry", both=True))
    o.append(H.label(s, xs + s(8), (com[1] + com2[1]) / 2 + s(5), f'{it("h")}', fill=BLU))
    o.append(H.label(s, com2[0] - s(6), com2[1] - s(22), "COM, one step later", "label2", I["secondary"]))
    # right column: the work, the power, and the ascent / descent contrast
    lx, ty = 505.0, 60.0
    o.append(H.label(s, lx, ty, "each step raises the COM by h", "label2", I["secondary"]))
    o.append(H.label(s, lx, ty + s(22), f'{it("U")}{H.sub("step", s)} = {it("m g h")} = 70 × 9.81 × 0.17', fill=BRN))
    o.append(H.label(s, lx, ty + s(42), "≈ 117 J per step", fill=BRN))
    o.append(H.label(s, lx, ty + s(70), f'{it("P")} = {it("m g h f")} = 117 J × 1.8 steps/s', fill=BRN))
    o.append(H.label(s, lx, ty + s(90), f"≈ 210 W ({it('v')}{H.sub('vert', s, 'label2')} = {H_STEP * F_STEP:.2f} m/s)", fill=BRN))
    ya = ty + s(150)
    o.append(H.arrow(s, p, lx + s(7), ya + s(36), lx + s(7), ya, "force"))
    o.append(H.label(s, lx + s(24), ya + s(10), f'ascent: +{it("U")}, concentric work', fill=RED))
    o.append(H.label(s, lx + s(24), ya + s(28), "failure: a slow-down", "label2", I["secondary"]))
    yb = ya + s(78)
    o.append(H.arrow(s, p, lx + s(7), yb, lx + s(7), yb + s(36), "force"))
    o.append(H.label(s, lx + s(24), yb + s(12), f'descent: −{it("U")}, eccentric braking', fill=RED))
    o.append(H.label(s, lx + s(24), yb + s(30), "failure: a fall", "label2", I["secondary"]))
    o.append(credit_lines(s, VB, " Stairs, arrows and marks drawn for this course; the stairs and the ghost COM are to scale (riser 0.17 m)."))
    aria = ("Side view of a skeleton climbing a flight of stairs to the right, rear foot on one tread and front foot on the "
            "next, drawn to scale with a riser of 0.17 metres marked beside the first riser. The centre of mass is marked, "
            "with a faint copy one step ahead and 0.17 metres higher. Text gives the work per step, mgh = 117 joules, and the "
            "climbing power, 210 watts at 1.8 steps per second. An upward arrow marks ascent as positive concentric work, "
            "failure being a slow-down; a downward arrow marks descent as negative eccentric braking, failure being a fall.")
    return finish(VB, aria, s, o)


# ================================================================ svg #10  Fig. 8 slope
def slope_pose(th):
    """Upright walker on a slope of th deg: thighs vertical, trunk leaning into the hill by th, stance foot flat on the
    slope (toe up by th: ankle = shank angle + th); the swing leg is forward."""
    near = dict(hip=th, knee=8, contact=None, ankle=8 + th, shoulder=th - 10, elbow=10)
    far = dict(hip=th + 28, knee=55, contact=None, ankle=3 + th, shoulder=th + 25, elbow=15)
    return LB.pose(pelvis=th, near=near, far=far, anchor=("heel", "near"))


def fig10():
    p = "m13f10_"
    TH = 10.0
    th = math.radians(TH)
    VB = (0, 0, 760, 560)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    P = slope_pose(TH)
    hgt = 380.0
    hx, hy = 330.0, 400.0
    body, J = kit(P, hx, hy, hgt)
    asserted_box(J["bbox"], VB, s, "fig10")
    heel, toe = J["heel"], J["toe"]
    ang = math.degrees(math.atan2(heel[1] - toe[1], toe[0] - heel[0]))
    assert abs(ang - TH) < 0.3, ang
    ex, ey = math.cos(th), -math.sin(th)          # unit vector up the slope (screen)
    nx, ny = math.sin(th), math.cos(th)           # unit vector into the slope

    def at(x):
        return heel[1] + (x - heel[0]) * ey / ex
    x0, x1 = 40.0, 735.0
    yb = at(x0)
    ground = (f'<path d="M{x0:.1f} {yb:.1f} L{x1:.1f} {at(x1):.1f} L{x1:.1f} {yb + s(16):.1f} L{x0:.1f} {yb + s(16):.1f} Z" '
              f'fill="#e9e2d6" stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}" stroke-linejoin="round"/>')
    o = [defs(p, s), ground, body]
    o.append(dline(s, x0, yb, x1, yb))
    r = 150.0
    o.append(arc(s, x0, yb, r, -TH, 0.0, BLU, 1.6))
    o.append(H.label(s, x0 + r + s(10), yb - s(9), "θ = 10°", fill=BLU))
    com = J["com"]
    L = 175.0
    o.append(H.com_mark(s, *com))
    tip = (com[0], com[1] + L)
    c_par = (com[0] - ex * L * math.sin(th), com[1] - ey * L * math.sin(th))   # down the slope
    c_perp = (com[0] + nx * L * math.cos(th), com[1] + ny * L * math.cos(th))  # into the slope
    o.append(dline(s, tip[0], tip[1], c_par[0], c_par[1], BRN, "leader"))
    o.append(dline(s, tip[0], tip[1], c_perp[0], c_perp[1], BRN, "leader"))
    o.append(H.arrow(s, p, com[0], com[1] + s(9), tip[0], tip[1], "load"))
    o.append(H.arrow(s, p, com[0] - s(1), com[1] + s(3), c_par[0], c_par[1], "load", w="geom"))
    o.append(H.arrow(s, p, com[0] + s(1), com[1] + s(9), c_perp[0], c_perp[1], "load", w="geom"))
    o.append(H.label(s, tip[0] - s(8), tip[1] + s(14), f'{it("mg")}', fill=BRN, anchor="end"))
    o.append(H.label(s, c_par[0] - s(8), c_par[1] + s(4), f'{it("mg")} sinθ', fill=BRN, anchor="end"))
    o.append(H.label(s, c_perp[0] + s(8), c_perp[1] + s(12), f'{it("mg")} cosθ', fill=BRN))
    # walking speed, up the slope
    vx, vy = 560.0, at(560.0) - s(46)
    o.append(H.arrow(s, p, vx, vy, vx + ex * 100.0, vy + ey * 100.0, "geometry"))
    o.append(H.label(s, vx + 10, vy - s(12), f'{it("v")} = 1.0 m/s', fill=BLU))
    # text, top left
    lx, ty = 40.0, 36.0
    o.append(H.label(s, lx, ty, "extra power against gravity, beyond level walking", "label2", I["secondary"]))
    o.append(H.label(s, lx, ty + s(24), f'{it("P")}{H.sub("slope", s)} = {it("m g v")} sinθ', fill=BRN))
    o.append(H.label(s, lx, ty + s(50), "uphill: the muscles supply +P, an aerobic demand", "label2", I["secondary"]))
    o.append(H.label(s, lx, ty + s(68), "downhill: the same P is absorbed eccentrically,", "label2", I["secondary"]))
    o.append(H.label(s, lx, ty + s(86), "a control and joint-load demand", "label2", I["secondary"]))
    # table, top right: P for 5, 10 and 15 degrees
    tx, ty2 = 500.0, 36.0
    o.append(H.label(s, tx, ty2, "m = 70 kg, v = 1.0 m/s", "label2", I["secondary"]))
    cols = (tx, tx + s(52), tx + s(142))
    o.append(H.label(s, cols[0], ty2 + s(22), "θ", "label2", I["secondary"]))
    o.append(H.label(s, cols[1], ty2 + s(22), "grade", "label2", I["secondary"]))
    o.append(H.label(s, cols[2], ty2 + s(22), it("P"), "label2", I["secondary"]))
    for i, thd in enumerate((5, 10, 15)):
        yy = ty2 + s(44) + i * s(20)
        col = I["primary"]
        o.append(H.label(s, cols[0], yy, f"{thd}°", "label2", col))
        o.append(H.label(s, cols[1], yy, f"{math.tan(math.radians(thd)) * 100:.0f}%", "label2", col))
        o.append(H.label(s, cols[2], yy, f"{SLOPE_P[thd]:.0f} W" + ("  (drawn)" if thd == 10 else ""), "label2", col))
    o.append(credit_lines(s, VB, " Slope, arrows and marks drawn for this course; arrows are not to force scale."))
    aria = ("Side view of a skeleton walking up a slope of 10 degrees to the right, stance foot flat on the slope. At the "
            "centre of mass the weight mg is drawn straight down and resolved into a component mg sin theta along the slope, "
            "pointing down the slope, and a component mg cos theta perpendicular to it. An arrow marks the walking speed "
            "1.0 metres per second up the slope. Text gives the extra power P = m g v sin theta, supplied uphill and absorbed "
            "eccentrically downhill, and a table: 60, 119 and 178 watts at 5, 10 and 15 degrees (grades 9, 18 and 27 percent).")
    return finish(VB, aria, s, o)


# ================================================================ svg #2  Fig. 1 sit to stand
def seat_y_of(J, hgt):
    """Seat top under the thigh: just below the knee joint line or the sitting bones, whichever is lower."""
    return max(J["knee"][1] + 0.012 * hgt, J["hip"][1] + 0.03 * hgt)


def chair(s, J, hgt, fy, x_back=0.30, x_front=0.13):
    """A schematic seat (a slab on two legs) under the thighs."""
    k = hgt / H_M
    sy = seat_y_of(J, hgt)
    sx0, sx1 = J["hip"][0] - x_back * k, J["knee"][0] - x_front * k
    return (rect(s, sx0, sy, sx1 - sx0, s(6), "#e9e2d6", I["secondary"], 1.2)
            + H.line(s, sx0 + s(7), sy + s(6), sx0 + s(7), fy, I["secondary"], "ref")
            + H.line(s, sx1 - s(7), sy + s(6), sx1 - s(7), fy, I["secondary"], "ref"))


def fig2():
    p = "m13f2_"
    VB = (0, 0, 760, 505)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    hgt, fy = 330.0, 360.0
    k = hgt / H_M
    P_off, _ = seatoff_pose()
    frames = (("sit", LB.pose(**LB.POSES["sitting"], anchor=("heel", "near")), 135.0, True),
              ("seat-off", P_off, 355.0, True), ("stand", LB.pose(anchor=("heel", "near")), 590.0, False))
    notes = (("COM 0.30 m behind the heels,", "over the seat"), ("COM 0.01 m inside the", "rear edge of the BoS"),
             ("COM 0.08 m inside", "the BoS"))
    o = [defs(p, s), floor(s, 12, 748, fy)]
    for (name, P, hx, seat), note in zip(frames, notes):
        body, J = kit(P, hx, fy, hgt)
        asserted_box(J["bbox"], VB, s, "fig2 " + name)
        he, to, com = J["heel"][0], J["toe"][0], J["com"]
        d_heel = (com[0] - he) / k
        assert (name != "sit" or d_heel < -0.25) and (name != "seat-off" or 0.0 < d_heel < 0.03) and \
               (name != "stand" or 0.06 < d_heel < 0.10), (name, d_heel)
        if seat:
            o.append(chair(s, J, hgt, fy))
        o.append(body)
        yb = fy + s(10)
        o.append(rect(s, he, yb - s(4), to - he, s(8), BLU, BLU, 1.0, 'fill-opacity="0.30"'))
        o.append(dline(s, com[0], com[1] + s(8), com[0], yb + s(14)))
        o.append(H.com_mark(s, *com))
        o.append(H.label(s, hx + 0.05 * k, 30.0, name, "label", I["primary"], "middle"))
        o.append(H.label(s, hx + 0.05 * k, fy + s(46), note[0], "label2", I["secondary"], "middle"))
        o.append(H.label(s, hx + 0.05 * k, fy + s(62), note[1], "label2", I["secondary"], "middle"))
        if name == "seat-off":                          # extensor torques at the hip and the knee
            hip, knee = J["hip"], J["knee"]
            o.append(arc_arrow(s, p, hip[0], hip[1], s(30), 20, -70, "force"))
            o.append(arc_arrow(s, p, knee[0], knee[1], s(30), -75, 40, "force"))
            o.append(H.label(s, hip[0] - s(34), hip[1] - s(24), "hip extension", "label2", RED, "end"))
            o.append(H.label(s, knee[0] + s(36), knee[1] - s(10), "knee extension", "label2", RED))
    o.append(rect(s, 20, 438, s(16), s(8), BLU, BLU, 1.0, 'fill-opacity="0.30"'))
    o.append(H.label(s, 20 + s(22), 438 + s(8), "base of support (BoS): heel to toe", "label2", I["secondary"]))
    o.append(H.com_mark(s, 300, 442))
    o.append(H.label(s, 312, 447, "whole-body COM (Winter), dashed down to the floor", "label2", I["secondary"]))
    o.append(credit_lines(s, VB, " Seat, bars and marks drawn for this course."))
    aria = ("Three side views of a skeleton rising from a chair, facing right: seated, at seat-off, and standing. In each, the "
            "whole-body centre of mass is marked and dashed down to the floor, where a bar marks the base of support from heel "
            "to toe. Seated, the centre of mass is 0.30 metres behind the heels, over the seat; at seat-off it is 0.01 metres "
            "inside the rear edge of the base of support; standing it is 0.08 metres inside. At seat-off, red curved arrows "
            "mark the hip and knee extension torques.")
    return finish(VB, aria, s, o)


# ================================================================ svg #3  montage
def stumble_pose(toe_h=0.06):
    """A trip: the swing foot has just met an obstacle in front of it (toe `toe_h` m above the floor) while the trunk keeps
    going forward and the arms start to swing forward. The stance (far) foot is flat on the floor, behind the body."""
    def mk(kn):
        near = dict(hip=48, knee=kn, contact=None, ankle=0, shoulder=70, elbow=25)         # swing leg
        far = dict(hip=6, knee=10, contact="flat", shoulder=95, elbow=20)                  # stance leg
        return LB.pose(pelvis=14, trunk=18, neck=-8, near=near, far=far, anchor=("heel", "far"))

    def f(kn):
        J = joints(mk(kn))
        return (J["heel_far"][1] - J["toe"][1]) * UM
    return mk(bisect(f, 5.0, 45.0, toe_h))


def fig3():
    p = "m13f3_"
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    hgt, fy = 225.0, 285.0
    k = hgt / H_M
    o = [defs(p, s), floor(s, 12, 748, fy)]
    # 1 rise
    P, _ = seatoff_pose()
    body, J = kit(P, 70.0, fy, hgt)
    asserted_box(J["bbox"], VB, s, "fig3 rise")
    o += [chair(s, J, hgt, fy), body]
    # 2 climb
    P = stair_pose()
    xh = 240.0
    yh = fy - 2 * H_STEP * k
    body, J = kit(P, xh, yh, hgt)
    asserted_box(J["bbox"], VB, s, "fig3 climb")
    st, X, Y = stairs(s, k, xh, yh, 2, 0, 3, fy)
    o += [st, body]
    # 3 lift: the 60 degree stoop of Fig. 5
    body, J = kit(LB.pose(**stoop(60.0, 0.40)), 420.0, fy, hgt)
    asserted_box(J["bbox"], VB, s, "fig3 lift")
    Gp = grip(J)
    bw, bh = 0.30 * k, 0.24 * k
    o += [rect(s, Gp[0] - bw / 2, Gp[1] - 0.02 * k, bw, bh, BOXFILL, BRN, 1.3), body]
    # 4 catch a stumble: the swing foot meets a low block
    P = stumble_pose()
    body, J = kit(P, 510.0, fy, hgt)
    asserted_box(J["bbox"], VB, s, "fig3 stumble")
    toe = J["toe"]
    bh_ = max(0.07 * k, fy - toe[1] + 0.03 * k)
    o.append(rect(s, toe[0] + 0.015 * k, fy - bh_, 0.10 * k, bh_, "#e9e2d6", I["secondary"], 1.2))
    o.append(body)
    o.append(H.arrow(s, p, toe[0] + 0.015 * k - s(4), toe[1] + s(4), toe[0] + 0.015 * k - s(44), toe[1] + s(4), "force"))
    labels = (("rise", "Section 2", 105.0), ("climb", "Section 3", 300.0), ("lift", "Section 4", 450.0),
              ("catch a stumble", "Section 5", 640.0))
    for t_, sec, x in labels:
        o.append(H.label(s, x, fy + s(30), t_, "label", I["primary"], "middle"))
        o.append(H.label(s, x, fy + s(48), sec, "label2", I["secondary"], "middle"))
    o.append(credit_lines(s, VB, " Seat, stairs, box, block and arrow drawn for this course."))
    aria = ("A montage of four everyday movements, each a skeleton in side view facing right: rising from a chair at seat-off, "
            "climbing a flight of stairs with one foot on each of two treads, lifting a box in a forward stoop, and catching "
            "a stumble, with the swing foot stopped by a low block, a red arrow marking the obstacle's backward force on the "
            "foot, and the trunk pitching forward. Each is labelled with its section of the module.")
    return finish(VB, aria, s, o)


# ================================================================ svg #4  Fig. 2 the case-study pipeline
def fig4():
    p = "m13f4_"
    VB = (0, 0, 760, 500)
    s = H.Scale(VB[2], VB[3])
    o = [defs(p, s)]
    steps = (("1", "idealize", "links and joints"), ("2", "free-body", "diagram"), ("3", "govern", "ΣM = 0 or Δp, energy"),
             ("4", "estimate", "human numbers"), ("5", "test", "find the failure mode"))
    bw, gap, y0, bh = 132.0, 22.0, 18.0, 74.0
    x0 = (VB[2] - (5 * bw + 4 * gap)) / 2
    for i, (n, a, b) in enumerate(steps):
        x = x0 + i * (bw + gap)
        o.append(f'<rect x="{x:.1f}" y="{y0}" width="{bw}" height="{bh}" rx="{s(8):.1f}" fill="{BOXFILL}" '
                 f'stroke="{T["muscle"][1]}" stroke-width="{s(1.6):.2f}"/>')
        o.append(H.label(s, x + s(10), y0 + s(20), n, "label", T["muscle"][1]))
        o.append(H.label(s, x + bw / 2, y0 + s(40), a, "label", I["primary"], "middle"))
        o.append(H.label(s, x + bw / 2, y0 + s(60), b, "label2", I["secondary"], "middle"))
        if i < 4:
            o.append(H.arrow(s, p, x + bw + s(3), y0 + bh / 2, x + bw + gap - s(3), y0 + bh / 2, "dim"))
    # the second box is the one drawn below
    xb = x0 + 1 * (bw + gap) + bw / 2
    o.append(H.line(s, xb, y0 + bh + s(3), xb, 140.0, I["rule"], "leader", H.DASH_REF))
    o.append(H.label(s, VB[2] / 2, 168.0, "example of step 2 and 3: moment balance about a joint (the elbow, a load in the hand)",
                     "label2", I["secondary"], "middle"))
    K, Ec = 8.0, (112.0, 292.0)
    A = Posed(p, s, Ec, K, th=0.0)
    xw = Ec[0] + 0.35 * 100 * K                                # load in the hand, 0.35 m from the elbow (Module 1)
    o.append(A.bones(upper=False))
    Ex, Ey = Ec
    o.append(H.joint_centre(s, Ex, Ey))
    o.append(H.label(s, Ex - s(14), Ey + s(26), "joint", "label", I["primary"], "end"))
    o.append(arc_arrow(s, p, Ex, Ey, s(34), -150, -35, "force"))
    o.append(H.label(s, Ex - s(6), Ey - s(46), f'{sym("τ", "muscle", s)}', fill=RED, anchor="end"))
    o.append(H.arrow(s, p, xw, Ey + s(10), xw, Ey + 105.0, "load"))
    o.append(H.label(s, xw + s(10), Ey + 80.0, f'{it("W")} (external)', fill=BRN))
    yd = Ey + 135.0
    o.append(dline(s, Ex, Ey + s(12), Ex, yd + s(8)))
    o.append(dline(s, xw, Ey + 110.0, xw, yd + s(8)))
    o.append(dim(s, p, Ex, xw, yd, BLU, "geometry"))
    o.append(H.label(s, (Ex + xw) / 2, yd + s(20), f'moment arm {it("d")}', fill=BLU, anchor="middle"))
    # the balance, right column
    lx = 520.0
    o.append(H.label(s, lx, 235.0, "ΣM = 0 about the joint:", "label2", I["secondary"]))
    o.append(H.label(s, lx, 259.0, f'{sym("τ", "muscle", s)} = {it("F")}{H.sub("muscle", s)}{it("d")}{H.sub("muscle", s)}', fill=RED))
    o.append(H.label(s, lx, 283.0, f'= {it("W d")}', fill=BRN))
    o.append(H.label(s, lx, 311.0, "the muscle torque balances the", "label2", I["secondary"]))
    o.append(H.label(s, lx, 329.0, "external load times its moment arm", "label2", I["secondary"]))
    o.append(credit_bottom_nih(s, VB))
    aria = ("Top: the five-step case-study pipeline as five boxes joined by arrows: idealize to links and joints, free-body "
            "diagram, govern with a moment balance or an impulse or energy law, estimate with human numbers, and test by finding "
            "the failure mode. Below, a worked example of the free-body and balance steps: a forearm and hand held horizontal, "
            "isolated at the elbow joint. A curved arrow at the joint is the muscle torque; the external load W hangs from the "
            "hand at the moment arm d from the joint, and the muscle torque equals W times d.")
    return finish(VB, aria, s, o)


def credit_bottom_nih(s, VB):
    lines = wrap(NIH + " Overlays drawn for this course.", 120)
    return H.credit(s, 8, VB[1] + VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines)




# ================================================================ svg #8  Fig. 6 turning, top view
def foot_path(cx, cy, heading, length, side):
    """Closed plantar outline (the kit's control points) centred on (cx, cy), toes along `heading` (deg, a left turn is
    positive on the page). side +1 = the subject's right foot, -1 = left foot."""
    h = math.radians(heading)
    ex, ey = math.cos(h), -math.sin(h)                 # toe direction on the page
    rx, ry = math.sin(h), math.cos(h)                  # the subject's right-hand side
    pts = []
    for u, v in PLANTAR:                               # u heel -> toe, v < 0 lateral (right foot)
        a, b = (u - 0.5) * length, -side * v * length
        pts.append((cx + a * ex + b * rx, cy + a * ey + b * ry))
    return smooth_closed(pts)


def fig8():
    p = "m13f8_"
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    kt = 140.0                                         # figure units per metre in the top view
    o = [defs(p, s)]
    # ---- left: the walker's centre line: straight, a 60 degree turn to the left, straight (drawing geometry)
    R, L1, L3 = 0.80, 0.85, 0.85
    A0 = (30.0, 280.0)
    arc_len = R * math.radians(BETA)
    cx_c, cy_c = A0[0] + L1 * kt, A0[1] - R * kt         # centre of the turn circle

    def at_s(sm):
        """(x, y, heading deg) at path length sm (m)."""
        if sm <= L1:
            return A0[0] + sm * kt, A0[1], 0.0
        if sm <= L1 + arc_len:
            ang = (sm - L1) / R
            return cx_c + R * kt * math.sin(ang), cy_c + R * kt * math.cos(ang), math.degrees(ang)
        d, ang = sm - L1 - arc_len, math.radians(BETA)
        return (cx_c + R * kt * math.sin(ang) + d * kt * math.cos(ang), cy_c + R * kt * math.cos(ang) - d * kt * math.sin(ang), BETA)
    total = L1 + arc_len + L3
    pth = [at_s(total * i / 60) for i in range(61)]
    o.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y, _ in pth)}" fill="none" stroke="{I["rule"]}" '
             f'stroke-width="{s(1.4):.2f}" stroke-dasharray="{s(6):.2f} {s(4):.2f}"/>')
    sm, side = 0.25, 1
    while sm < total - 0.05:
        x, y, hd = at_s(sm)
        h = math.radians(hd)
        fx, fy_ = x + 0.085 * side * kt * math.sin(h), y + 0.085 * side * kt * math.cos(h)
        o.append(f'<path d="{foot_path(fx, fy_, hd, 0.274 * kt, side)}" fill="{T["skin"][0]}" stroke="{T["skin"][1]}" '
                 f'stroke-width="{s(1.4):.2f}"/>')
        sm, side = sm + 0.55, -side
    # the turning angle between the straight line and the new direction, at the tangent intersection
    xa, ya, _ = at_s(L1)
    Tp = (xa + R * math.tan(math.radians(BETA / 2)) * kt, A0[1])
    d2 = (math.cos(math.radians(BETA)), -math.sin(math.radians(BETA)))
    o.append(dline(s, xa - 10.0, A0[1], Tp[0] + 80.0, A0[1]))
    o.append(dline(s, Tp[0], Tp[1], Tp[0] + d2[0] * 110.0, Tp[1] + d2[1] * 110.0))
    o.append(arc(s, Tp[0], Tp[1], 60.0, -BETA, 0.0, BLU, 1.6))
    o.append(H.label(s, Tp[0] + 66.0, Tp[1] - 22.0, "β", fill=BLU))
    # speeds before and after the turn
    o.append(H.arrow(s, p, A0[0] + 4.0, A0[1] + 44.0, A0[0] + 4.0 + 1.3 * 45.0, A0[1] + 44.0, "geometry"))
    o.append(H.label(s, A0[0] + 4.0 + 1.3 * 45.0 + s(8), A0[1] + 49.0, f'{sym("v", "1", s)}', fill=BLU))
    xe, ye, _ = at_s(total - 0.35)
    r_ = (math.sin(math.radians(BETA)), math.cos(math.radians(BETA)))
    qx, qy = xe + r_[0] * 40.0, ye + r_[1] * 40.0
    o.append(H.arrow(s, p, qx - d2[0] * 1.3 * 45.0, qy - d2[1] * 1.3 * 45.0, qx, qy, "geometry"))
    o.append(H.label(s, qx + s(8), qy + s(14), f'{sym("v", "2", s)}', fill=BLU))
    # the ground impulse, toward the inside of the turn, from the middle of the arc
    xm, ym, hm = at_s(L1 + arc_len / 2)
    hmr = math.radians(hm)
    inw = (-math.sin(hmr), -math.cos(hmr))
    o.append(H.arrow(s, p, xm + inw[0] * 30.0, ym + inw[1] * 30.0, xm + inw[0] * 110.0, ym + inw[1] * 110.0, "force"))
    o.append(H.label(s, xm + inw[0] * 110.0 - s(8), ym + inw[1] * 110.0 - s(2), f'{it("J")}: ground impulse,', fill=RED, anchor="end"))
    o.append(H.label(s, xm + inw[0] * 110.0 - s(8), ym + inw[1] * 110.0 + s(14), "toward the inside", "label2", I["secondary"], "end"))
    o.append(H.label(s, 30.0, 26.0, "top view: footprints along the turn", "label2", I["secondary"]))
    o.append(H.label(s, 30.0, 360.0, "the extrapolated COM must stay over the moving base (Module 10)", "label2", I["secondary"]))
    # ---- right: the velocity triangle, one scale for the three vectors (1 m/s = 90 units)
    sv = 90.0
    O_ = (500.0, 270.0)
    v1 = (O_[0] + V_TURN * sv, O_[1])
    v2 = (O_[0] + V_TURN * sv * d2[0], O_[1] + V_TURN * sv * d2[1])
    o.append(H.arrow(s, p, O_[0], O_[1], v1[0], v1[1], "geometry"))
    o.append(H.arrow(s, p, O_[0], O_[1], v2[0], v2[1], "geometry"))
    o.append(H.arrow(s, p, v1[0], v1[1], v2[0], v2[1], "force"))
    o.append(arc(s, O_[0], O_[1], 40.0, -BETA, 0.0, BLU, 1.6))
    o.append(H.label(s, O_[0] + 48.0, O_[1] - 12.0, f"β = {BETA:.0f}°", fill=BLU))
    o.append(H.label(s, v1[0] + s(8), v1[1] + s(5), f'{sym("v", "1", s)}', fill=BLU))
    o.append(H.label(s, v2[0] - s(8), v2[1] - s(4), f'{sym("v", "2", s)}', fill=BLU, anchor="end"))
    o.append(H.label(s, v1[0] + s(12), (v1[1] + v2[1]) / 2 + s(4), f'Δ{it("v")} = {sym("v", "2", s)} − {sym("v", "1", s)}', fill=RED))
    o.append(H.label(s, O_[0], O_[1] + 30.0, f'|{sym("v", "1", s)}| = |{sym("v", "2", s)}| = {V_TURN} m/s', "label2", I["secondary"]))
    o.append(H.label(s, 420.0, 60.0, f'{it("J")} = {it("m")}|Δ{it("v")}| = 2{it("m v")} sin(β/2)', fill=RED))
    o.append(H.label(s, 420.0, 84.0, "= 2 × 70 × 1.3 × sin 30° ≈ 91 N s", fill=RED))
    o.append(H.label(s, 420.0, 108.0, f"|Δ{it('v')}| = 2{it('v')} sin(β/2) = {2 * V_TURN * math.sin(math.radians(BETA / 2)):.2f} m/s",
                     "label2", I["secondary"]))
    o.append(H.label(s, 420.0, 126.0, "along Δv: toward the inside of the turn", "label2", I["secondary"]))
    o.append(H.credit(s, 8.0, VB[3] - 6.0, ["Footprints: the kit's schematic plantar outline, drawn for this course. "
                                            "Overlays drawn for this course; arrows are not to force scale."]))
    aria = ("Top view of a walker turning left through 60 degrees at 1.3 metres per second: footprints along a dashed path, "
            "a velocity v1 before the turn and v2 after it, the turning angle beta between the two directions, and a red arrow "
            "for the ground impulse J pointing toward the inside of the turn. Right, the two velocity vectors drawn from one "
            "point 60 degrees apart and the red difference vector joining their tips: the triangle is equilateral, so the "
            "velocity change has magnitude 1.3 metres per second and J = m times that = 91 newton seconds.")
    return finish(VB, aria, s, o)


# ================================================================ svg #9  Fig. 7 jar and door
def fig9():
    p = "m13f9_"
    VB = (0, 0, 760, 450)
    s = H.Scale(VB[2], VB[3])
    o = [defs(p, s)]
    # ---- left: the lid seen from above, r = 0.035 m drawn as 92 units
    cx, cy, Rr = 160.0, 200.0, 84.0
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{Rr}" fill="{BOXFILL}" stroke="{I["secondary"]}" stroke-width="{s(2):.2f}"/>')
    for i in range(48):                                  # knurled rim
        a = math.radians(i * 7.5)
        o.append(H.line(s, cx + (Rr - 7) * math.cos(a), cy + (Rr - 7) * math.sin(a), cx + Rr * math.cos(a), cy + Rr * math.sin(a),
                        I["muted"], "leader"))
    pads = (200.0, 340.0, 20.0, 160.0)                   # fingertip contacts (screen angle on the lid)
    for ang in pads:
        a = math.radians(ang)
        px, py = cx + (Rr + 10) * math.cos(a), cy + (Rr + 10) * math.sin(a)
        o.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{s(11):.1f}" ry="{s(15):.1f}" '
                 f'transform="rotate({ang + 90:.1f} {px:.1f} {py:.1f})" fill="{T["skin"][0]}" stroke="{T["skin"][1]}" '
                 f'stroke-width="{s(1.4):.2f}"/>')
        o.append(H.arrow(s, p, cx + (Rr + 52) * math.cos(a), cy + (Rr + 52) * math.sin(a),
                         cx + (Rr + 24) * math.cos(a), cy + (Rr + 24) * math.sin(a), "force"))
    for ang in pads:                                     # friction along the rim, in the opening sense (anticlockwise)
        a = math.radians(ang)
        px, py = cx + (Rr + 10) * math.cos(a), cy + (Rr + 10) * math.sin(a)
        tx, ty = math.sin(a), -math.cos(a)
        o.append(H.arrow(s, p, px + tx * 14.0, py + ty * 14.0, px + tx * 52.0, py + ty * 52.0, "force"))
    o.append(arc_arrow(s, p, cx, cy, 44.0, 40.0, -200.0, "force"))
    o.append(H.label(s, cx, cy - s(6), f'{sym("τ", "open", s)}', fill=RED, anchor="middle"))
    o.append(H.arrow(s, p, cx, cy, cx + Rr * math.cos(math.radians(105)), cy + Rr * math.sin(math.radians(105)), "geometry", both=True))
    o.append(H.label(s, cx - 8.0, cy + 70.0, f'{it("r")}', fill=BLU, anchor="end"))
    o.append(H.label(s, cx, 28.0, "jar lid, top view", "label", I["primary"], "middle"))
    a0 = math.radians(340.0)
    o.append(H.label(s, cx + (Rr + 52) * math.cos(a0) + s(6), cy + (Rr + 52) * math.sin(a0) - s(6), f'{sym("F", "grip", s)}', fill=RED))
    a1 = math.radians(20.0)
    o.append(H.label(s, cx + (Rr + 10) * math.cos(a1) + math.sin(a1) * 54.0 + s(6), cy + (Rr + 10) * math.sin(a1) - math.cos(a1) * 54.0 - s(6),
                     f'{sym("μ", "lid", s)}{sym("F", "grip", s)}', fill=RED))
    y = 322.0
    o.append(H.label(s, 12.0, y, f'{sym("τ", "open", s)} = {sym("μ", "lid", s)}{sym("F", "grip", s)}{it("r")}', fill=RED))
    o.append(H.label(s, 12.0, y + 22.0, f'stuck lid: {sym("τ", "resist", s, "label2")} = 2 N m, {it("r")} = 0.035 m, {sym("μ", "lid", s, "label2")} = 0.7', "label2", I["secondary"]))
    o.append(H.label(s, 12.0, y + 42.0, f'rim force {sym("μ", "lid", s, "label2")}{sym("F", "grip", s, "label2")} = {sym("τ", "resist", s, "label2")}/{it("r")} ≈ 57 N', "label2", I["secondary"]))
    o.append(H.label(s, 12.0, y + 62.0, f'grip {sym("F", "grip", s, "label2")} = {sym("τ", "resist", s, "label2")}/({sym("μ", "lid", s, "label2")}{it("r")}) ≈ 82 N', "label2", RED))
    o.append(H.label(s, 12.0, y + 84.0, f"{sym('μ', 'lid', s, 'label2')} 0.5 (dry skin) → {TAU_RES / (0.5 * R_LID):.0f} N; "
                     f"1.0 (rubber pad) → {TAU_RES / (1.0 * R_LID):.0f} N", "label2", I["secondary"]))
    # ---- right: the door seen from above, hinge at the left end of the doorway
    hx, hy, kd = 480.0, 300.0, 215.0
    L = 0.9 * kd
    th = math.radians(24.0)
    ex, ey = math.cos(th), -math.sin(th)                 # leaf direction on the page
    tx, ty = ey * 1.0, -ex                               # anticlockwise tangent (the opening sense)
    o.append(H.line(s, hx - 80.0, hy, hx, hy, I["secondary"], "axis"))
    o.append(H.line(s, hx + L, hy, hx + L + 50.0, hy, I["secondary"], "axis"))
    o.append(dline(s, hx, hy, hx + L, hy))
    o.append(f'<path d="M{hx + L:.1f},{hy:.1f} A{L:.1f},{L:.1f} 0 0 0 {hx + L * ex:.1f},{hy + L * ey:.1f}" fill="none" '
             f'stroke="{I["rule"]}" stroke-width="{s(1.2):.2f}" stroke-dasharray="{s(5):.2f} {s(4):.2f}"/>')
    t_ = 0.04 * kd
    nx_, ny_ = -tx, -ty                                  # toward the closed side
    leaf = [(hx, hy), (hx + L * ex, hy + L * ey), (hx + L * ex + nx_ * t_, hy + L * ey + ny_ * t_), (hx + nx_ * t_, hy + ny_ * t_)]
    o.append(f'<polygon points="{" ".join(f"{x:.1f},{y_:.1f}" for x, y_ in leaf)}" fill="#e9e2d6" stroke="{I["secondary"]}" '
             f'stroke-width="{s(1.4):.2f}"/>')
    o.append(H.joint_centre(s, hx, hy))
    o.append(H.label(s, hx - s(12), hy + s(26), "hinge", "label", I["primary"], "end"))
    dh = D_HINGE * kd
    hdx, hdy = hx + dh * ex, hy + dh * ey
    o.append(f'<circle cx="{hdx + nx_ * t_:.1f}" cy="{hdy + ny_ * t_:.1f}" r="{s(4):.1f}" fill="{I["secondary"]}"/>')
    # the hand pushes at the handle, perpendicular to the leaf, in the opening sense
    bx, by = hdx + nx_ * t_, hdy + ny_ * t_
    o.append(f'<ellipse cx="{bx + nx_ * 12.0:.1f}" cy="{by + ny_ * 12.0:.1f}" rx="{s(12):.1f}" ry="{s(9):.1f}" '
             f'transform="rotate({math.degrees(math.atan2(ty, tx)):.1f} {bx + nx_ * 12.0:.1f} {by + ny_ * 12.0:.1f})" '
             f'fill="{T["skin"][0]}" stroke="{T["skin"][1]}" stroke-width="{s(1.4):.2f}"/>')
    o.append(H.arrow(s, p, bx + nx_ * 58.0, by + ny_ * 58.0, bx + nx_ * 20.0, by + ny_ * 20.0, "force"))
    o.append(H.label(s, bx + nx_ * 58.0, by + ny_ * 58.0 + s(34), f'{sym("F", "hand", s)} ≈ 25 N', fill=RED, anchor="middle"))
    # the self-closer torque about the hinge, in the closing sense (clockwise on the page), on the back of the hinge
    o.append(arc_arrow(s, p, hx, hy, 46.0, 200.0, 285.0, "load"))
    o.append(H.label(s, hx - 54.0, hy - 52.0, f'{sym("τ", "door", s)} = 20 N m', fill=BRN, anchor="end"))
    o.append(H.label(s, hx - 54.0, hy - 34.0, "self-closer", "label2", I["secondary"], "end"))
    # d_hinge, along the leaf on the closed side
    off = -34.0
    p0 = (hx + nx_ * off, hy + ny_ * off)
    p1 = (hdx + nx_ * off, hdy + ny_ * off)
    o.append(H.arrow(s, p, p0[0], p0[1], p1[0], p1[1], "geometry", both=True))
    o.append(dline(s, hx - nx_ * 4.0, hy - ny_ * 4.0, hx + nx_ * (off - 6.0), hy + ny_ * (off - 6.0), BLU, "leader", None))
    o.append(dline(s, hdx - nx_ * 4.0, hdy - ny_ * 4.0, hdx + nx_ * (off - 6.0), hdy + ny_ * (off - 6.0), BLU, "leader", None))
    mid = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    o.append(H.label(s, mid[0] + nx_ * 10.0 - s(8), mid[1] + ny_ * 10.0 - s(4), f'{sym("d", "hinge", s)} = 0.8 m', fill=BLU, anchor="end"))
    o.append(H.label(s, 600.0, 28.0, "door, top view", "label", I["primary"], "middle"))
    o.append(H.label(s, 440.0, 366.0, f'{sym("F", "hand", s)} = {sym("τ", "door", s)}/{sym("d", "hinge", s)} = 20/0.8 ≈ 25 N', fill=RED))
    o.append(H.label(s, 440.0, 388.0, "the handle far from the hinge needs only a modest push", "label2", I["secondary"]))
    o.append(H.credit(s, 8.0, VB[3] - 6.0, ["Fingertip pads and the door are schematic, drawn for this course; arrows are not to force scale."]))
    aria = ("Two panels from above. Left, a jar lid of radius r gripped by four fingertips: grip forces press inward and "
            "friction forces act along the rim in the opening sense, giving the opening torque tau = mu F_grip r; for a stuck "
            "2 newton metre lid at mu 0.7 the rim force is about 57 newtons and the grip force about 82 newtons. Right, a door "
            "hinged at the left end of the doorway, held a little open: the hand pushes at the handle, 0.8 metres from the "
            "hinge, against a 20 newton metre self-closer torque, so F_hand = tau_door over d_hinge is about 25 newtons.")
    return finish(VB, aria, s, o)


# ================================================================ svg #11  Fig. 9 shared reserves
RESERVES = (("leg strength", "knee extensor strength and power"), ("eccentric control", "braking while the muscle lengthens"),
            ("tissue tolerance", "disc, bone, joint"), ("balance margin", "lateral margin and reaction"),
            ("grip strength", "hand force"), ("arm strength", "upper-body push"))
TASKS = (("chair rise", "§2"), ("stair ascent", "§3"), ("slope up", "§7"), ("stair descent", "§3"), ("slope down", "§7"),
         ("lift / carry", "§4"), ("turn / stumble", "§5"), ("jar", "§6"), ("door", "§6"))
# edges: the "Binding margin" column of the table (module13.html lines 202-210), plus the caption (leg strength binds the chair,
# the stairs and the downhill; eccentric control: stair descent and slope down; tissue: lifting and the downhill joint tolerance)
EDGES = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (2, 5), (2, 4), (3, 6), (4, 7), (5, 8))


def fig11():
    p = "m13f11_"
    VB = (0, 0, 760, 560)
    s = H.Scale(VB[2], VB[3])
    o = [defs(p, s)]
    n_t = len(TASKS)
    ty0, th, tgap = 70.0, 36.0, 8.0
    ty = [ty0 + i * (th + tgap) for i in range(n_t)]
    tc = [y + th / 2 for y in ty]
    # reserves centred on the mean height of their tasks
    links = {r: [t for rr, t in EDGES if rr == r] for r in range(len(RESERVES))}
    rh = 46.0
    rc = [sum(tc[t] for t in links[r]) / len(links[r]) for r in range(len(RESERVES))]
    for i in range(1, len(rc)):                         # keep the boxes apart
        rc[i] = max(rc[i], rc[i - 1] + rh + 8.0)
    xl0, xl1, xr0, xr1 = 30.0, 250.0, 520.0, 725.0
    o.append(H.label(s, (xl0 + xl1) / 2, 34.0, "reserves", "label", I["primary"], "middle"))
    o.append(H.label(s, (xr0 + xr1) / 2, 34.0, "daily tasks", "label", I["primary"], "middle"))
    pts = []
    for r, t in EDGES:
        col = RED if r == 0 else I["rule"]
        w = "geom" if r == 0 else "ref"
        o.append(H.line(s, xl1, rc[r], xr0, tc[t], col, w))
    for r, (name, sub_) in enumerate(RESERVES):
        y = rc[r] - rh / 2
        o.append(f'<rect x="{xl0}" y="{y:.1f}" width="{xl1 - xl0}" height="{rh}" rx="{s(10):.1f}" fill="{BOXFILL}" '
                 f'stroke="{RED if r == 0 else I["secondary"]}" stroke-width="{s(2 if r == 0 else 1.5):.2f}"/>')
        o.append(H.label(s, (xl0 + xl1) / 2, y + s(22), name, "label", I["primary"], "middle"))
        o.append(H.label(s, (xl0 + xl1) / 2, y + s(40), f"{sub_}", "label2", I["secondary"], "middle"))
    for t, (name, sec) in enumerate(TASKS):
        o.append(f'<rect x="{xr0}" y="{ty[t]:.1f}" width="{xr1 - xr0}" height="{th}" rx="{s(10):.1f}" fill="{BOXFILL}" '
                 f'stroke="{I["secondary"]}" stroke-width="{s(1.5):.2f}"/>')
        o.append(H.label(s, xr0 + s(12), tc[t] + s(5), name, "label", I["primary"]))
        o.append(H.label(s, xr1 - s(10), tc[t] + s(5), sec, "label2", I["secondary"], "end"))
    # count of tasks per reserve, on the link side of each reserve box
    for r in range(len(RESERVES)):
        n = len(links[r])
        o.append(H.label(s, xl1 + s(8), rc[r] - s(8), f"{n} task" + ("s" if n > 1 else ""), "label2",
                         RED if r == 0 else I["secondary"]))
    o.append(H.line(s, xl0, 520.0, xl0 + s(34), 520.0, RED, "geom"))
    o.append(H.label(s, xl0 + s(42), 525.0, "leg strength: the caption's example (chair, stairs, downhill, uphill)", "label2", I["secondary"]))
    o.append(H.label(s, xl0, 548.0, "links follow the Binding-margin column of the table below the figure", "label2", I["secondary"]))
    aria = ("A map from six body reserves on the left to nine daily tasks on the right. Leg strength, in red, links to the "
            "chair rise, stair ascent, slope up, stair descent and slope down. Eccentric control links to stair descent and "
            "slope down. Tissue tolerance links to lift or carry and slope down. Balance margin links to turn or stumble, "
            "grip strength to the jar and arm strength to the door.")
    return finish(VB, aria, s, o)


FIGS = {
    2: ("Sit-to-stand: seated and standing poses with Winter proporti", fig2),
    3: ("A montage of everyday movements the module analyses: rising", fig3),
    4: ("The five-step case-study pipeline as a flow of boxes: ideali", fig4),
    5: ("A person at seat-off rising from a chair: the body above the", fig5),
    6: ("A person climbing stairs, raising the centre of mass by the ", fig6),
    7: ("A person bent forward lifting a box: the trunk weight and th", fig7),
    8: ("Top view of a turn: the velocity vector rotates from v1 to v", fig8),
    9: ("Left: a hand gripping a jar lid, friction converting grip fo", fig9),
    10: ("A walker on an incline, with the weight vector resolved into", fig10),
    11: ("A bipartite map linking five body reserves on the left to th", fig11),
}
