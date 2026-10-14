"""Module 1 whole-body figures: svg #6 (Fig. 5 lumbar stack), #7 (Fig. 6 stooped lift), #8 (Fig. 7 base of
support), #9 (Fig. 8 leaning forward), and the problem figures #12 (C2), #15 (C5), #16 (C6), #17 (C7), #18 (C8),
#25 (D5), #26 (D6), #27 (D7), #29 (D9), #30 (D10).

Bodies: lynch_body.py (Lynch skeleton, CC BY 2.5, Winter proportions), drawn with <use> of the page's shared
hbody_ groups (this group exposes SHARED_DEFS once per page). Module 1 states no stature: text lengths in metres
are drawn at the course reference stature H = 1.75 m (m05/body.py H_REF_M). Every pose is solved from the number
the text gives (beta, reach, d_COM); module01.html line numbers sit beside each constant.
Foot outlines in the #8 top view: the kit's schematic plantar outline (foot_plantar.py control points): no
open-licence plantar art exists in svg_paths/ or art_sources/.
"""
import math
import re

import house as H
import lynch_body as LB
from m01.arm import arc, dim, sym
from m05.body import arc_arrow, finish, it, wrap

SHARED_DEFS = LB.SHARED_DEFS
T, O, I = H.TISSUE, H.OVERLAY, H.INK
RED, BLU, BRN, BLK = O["force"], O["geometry"], O["load"], O["reaction"]
H_M = 1.75                         # m, course reference stature (m05/body.py), drawing only
G = 9.81                           # line 892
M_BODY = 70.0                      # kg, line 875
W_BODY = 687.0                     # N, lines 378, 401 (70 x 9.81 = 686.7)
M_UB, M_BOX = 42.0, 20.0           # kg, upper body 0.60 M (line 881) and the box (line 365)
R_T, R_BOX, D_ES = 0.30, 0.40, 0.05   # m, lines 365, 883, 885, 886
BETA = 60.0                        # deg, line 882
ELL_T = R_T / math.sin(math.radians(BETA))   # 0.346 m, line 884
D_COM = 0.05                       # m, line 401
TAU_LB = G * (M_UB * R_T + M_BOX * R_BOX)             # (line 366) 202 N m
F_ES = TAU_LB / D_ES                                   # (line 367) 4040 N
C_DISC = F_ES + (M_UB + M_BOX) * G * math.cos(math.radians(BETA))   # (6.1), line 378: 4.35 kN
TAU_ANK = W_BODY * D_COM                               # line 403: 34 N m
assert (round(TAU_LB), round(F_ES, -1), round((M_UB + M_BOX) * G * 0.5), round(C_DISC / 1e3, 2),
        round(TAU_ANK), round(ELL_T, 3)) == (202, 4040, 304, 4.35, 34, 0.346)

UM = H_M / LB.H_U                  # metres per kit body unit
TILT0 = math.degrees(math.atan2(LB.LJ["neck"][0] - LB.LJ["l5s1"][0], LB.LJ["l5s1"][1] - LB.LJ["neck"][1]))
_S0 = H.Scale(100, 100)            # draw() ignores the scale; used only by the pose solvers


# ================================================================ pose solvers (kit body units)
def joints(P):
    return LB.draw("", _S0, P, 0, 0, LB.H_U)[1]


def bisect(f, lo, hi, target, n=50):
    """x in [lo, hi] with f(x) = target; f monotonic."""
    up = f(hi) > f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        if (f(mid) < target) == up:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def grip(J, sfx=""):
    """Where the hand holds a handle: 0.45 of the way from the wrist to the middle fingertip."""
    return LB.lerp(J["wrist" + sfx], J["fingertip" + sfx], 0.45)


def stoop(beta=BETA, reach=R_BOX, pel=40.0, phi=12.0):
    """Straight-knee stoop: the L5/S1 -> C7 line `beta` from vertical, thighs `phi` behind vertical, arms straight
    with the grip `reach` metres ahead of L5/S1. Returns the pose kwargs."""
    tr = beta - TILT0 - pel

    def kw(sh):
        return dict(pelvis=pel, trunk=tr, near=dict(hip=pel + phi, shoulder=sh), far=dict(hip=pel + phi, shoulder=sh))

    def f(sh):
        J = joints(LB.pose(**kw(sh)))
        return (grip(J)[0] - J["l5s1"][0]) * UM
    return kw(bisect(f, 0.0, 150.0, reach))


def lean(d=D_COM, pel=25.0):
    """Trunk leaned `pel` deg forward at the hips, legs tilted back about the ankles until the whole-body COM is
    `d` metres ahead of the ankle; arms hang vertically."""
    def kw(phi):
        return dict(pelvis=pel, near=dict(hip=pel + phi, shoulder=pel), far=dict(hip=pel + phi, shoulder=pel))

    def f(phi):
        J = joints(LB.pose(**kw(phi)))
        return (J["com"][0] - J["ankle"][0]) * UM
    return kw(bisect(f, 0.0, 20.0, d))


# ================================================================ drawing helpers
def body(P, x, y, hgt, **kw):
    """Kit body with its anchor at (x, y); `hgt` = stature in figure units."""
    return LB.draw("", _S0, P, x, y, hgt, **kw)


def vref(s, x, y0, y1):
    """Dashed vertical reference line (a plumb line through a joint)."""
    return H.line(s, x, y0, x, y1, O["dim"], "leader", H.DASH_REF)


def cop_dot(s, x, y):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(4.2):.2f}" fill="{BLK}" stroke="#fff" '
            f'stroke-width="{s(1.2):.2f}"/>')


def floor(s, x0, x1, y):
    return H.line(s, x0, y, x1, y, I["rule"], "axis")


def box(s, x, y, w, h):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="#f7f4ef" stroke="{BRN}" '
            f'stroke-width="{s(1.3):.2f}"/>')


def credit(s, x, y, width, extra=""):
    return LB.credit(s, x, y, width=width, extra=extra)


def ruled(s, VB, n):
    """y of the first credit line so that n lines end 6 px above the bottom edge."""
    return VB[1] + VB[3] - s(6) - (n - 1) * s(H.PX["credit"]) * 1.25


def credit_bottom(s, VB, extra="", x=None, width=None):
    x = VB[0] + s(8) if x is None else x
    width = VB[2] - s(16) if width is None else width
    probe = credit(s, 0, 0, width, extra)
    n = probe.count("<text")
    return credit(s, x, ruled(s, VB, n), width, extra)


def sub(v, sb, s, size="label"):
    return sym(v, sb, s, size)


# ================================================================ stooped lift: svg #7 (Fig. 6), #17 (C7), #25 (D5)
def stoop_scene(s, p, k, heel, mode):
    """The beta = 60 deg stoop with a 20 kg box. k = figure units per metre; heel = (x, floor y).
    mode: "main" (values), "c7" (symbols), "d5" (symbols + along-trunk distances l_t, l_L)."""
    P = LB.pose(**stoop())
    svg, J = body(P, heel[0], heel[1], H_M * k)
    L5 = J["l5s1"]
    ax = (J["neck"][0] - L5[0], J["neck"][1] - L5[1])
    u = (ax[0] / math.hypot(*ax), ax[1] / math.hypot(*ax))     # unit vector L5/S1 -> C7 (up the trunk)
    bk = LB.rot(u, -90)                                       # unit normal toward the back

    def along(t, n=0.0):
        """Point t metres up the trunk axis from L5/S1 and n metres toward the back."""
        return (L5[0] + t * k * u[0] + n * k * bk[0], L5[1] + t * k * u[1] + n * k * bk[1])
    beta = math.degrees(math.atan2(u[0], -u[1]))
    assert abs(beta - BETA) < 0.05, beta
    Gp = grip(J)
    assert abs((Gp[0] - L5[0]) / k - R_BOX) < 1e-3
    bw, bh = 0.30 * k, 0.24 * k                        # box 0.30 m deep, 0.24 m tall, handles at the grip
    by = Gp[1] - 0.02 * k
    Bc = (Gp[0], by + bh / 2)
    Cub = along(ELL_T)                                 # upper-body COM, l_t along the trunk (line 884)
    assert abs((Cub[0] - L5[0]) / k - R_T) < 1e-3
    o = [box(s, Gp[0] - bw / 2, by, bw, bh), svg]
    o.append(H.label(s, Bc[0], Bc[1] + s(5), "20 kg" if mode == "main" else sym("m", "L", s), "label2",
                     I["secondary"], "middle"))
    fy = heel[1]
    y_rt = L5[1] + 0.25 * k                            # r_t row, under the trunk
    y_rl = fy + s(20)                                  # r_L row, under the floor
    # trunk axis (dashed) and the plumb line through L5/S1; beta between the plumb line and the axis below L5/S1
    o.append(H.line(s, *along(-0.12), *along(0.52 if mode == "d5" else ELL_T + 0.04), O["dim"], "leader", H.DASH_REF))
    o.append(vref(s, L5[0], L5[1] + s(8), y_rl + s(6)))
    if mode != "c7":
        r_b = 0.085 * k
        o.append(arc(s, L5[0], L5[1], r_b, 90.0, 90.0 + beta, BLU, 1.6))
        am = math.radians(90.0 + beta / 2)
        o.append(H.label(s, L5[0] + (r_b + s(8)) * math.cos(am), L5[1] + (r_b + s(8)) * math.sin(am) + s(9),
                         "β = 60°" if mode == "main" else "β", fill=BLU, anchor="end"))
    # erector spinae: parallel to the trunk axis, d_es behind it, pulling the trunk toward the disc
    t1 = 0.20 if mode == "d5" else 0.26
    o.append(H.arrow(s, p, *along(t1, n=D_ES), *along(0.04, n=D_ES), "force"))
    o.append(H.line(s, *L5, *along(0.0, n=D_ES), BLU, "geom"))
    tail = along(t1, n=D_ES)
    if mode == "d5":
        q = along(0.14, n=0.095)
        o.append(H.label(s, q[0], q[1] + s(5), sym("F", "es", s), fill=RED, anchor="middle"))
    else:
        o.append(H.label(s, tail[0] - s(10), tail[1] - s(12), sym("F", "es", s) + (" ≈ 4.04 kN" if mode == "main" else ""),
                         fill=RED, anchor="end"))
    if mode == "main":
        o.append(H.label(s, tail[0] - s(10), tail[1] + s(5), "erector spinae", "label2", I["secondary"], "end"))
    e0 = along(0.0, n=D_ES)
    o.append(H.label(s, e0[0] - s(6), e0[1] + s(2), sym("d", "es", s) + (" = 0.05 m" if mode == "main" else ""),
                     fill=BLU, anchor="end"))
    o.append(H.joint_centre(s, *L5))
    o.append(H.label(s, L5[0] + s(12), L5[1] + s(20), "L5/S1"))
    # weights
    o.append(H.com_mark(s, *Cub))
    w_ub = y_rt - s(10) - Cub[1]
    o.append(H.arrow(s, p, Cub[0], Cub[1] + s(8), Cub[0], Cub[1] + w_ub, "load"))
    wl0, wl1 = by + bh + s(1), fy - s(14)
    o.append(H.arrow(s, p, Bc[0], wl0, Bc[0], wl1, "load"))
    if mode == "main":
        o.append(H.label(s, Cub[0] - s(8), Cub[1] + w_ub - s(22), sym("W", "ub", s) + " = 412 N", fill=BRN,
                         anchor="end"))
        o.append(H.label(s, Cub[0] - s(8), Cub[1] + w_ub - s(5), "upper body", "label2", I["secondary"], "end"))
        o.append(H.label(s, Bc[0] + s(10), wl1 - s(4), sym("W", "L", s) + " = 196 N", fill=BRN))
    else:
        o.append(H.label(s, Cub[0] - s(7), Cub[1] + w_ub - s(4), sym("W", "ub", s), fill=BRN, anchor="end"))
        o.append(H.label(s, Bc[0] + s(8), wl1 - s(4), sym("W", "L", s), fill=BRN))
    # horizontal arms
    o.append(H.line(s, Bc[0], wl1 + s(2), Bc[0], y_rl + s(6), O["dim"], "leader", H.DASH_REF))
    o.append(dim(s, p, L5[0], Cub[0], y_rt, BRN, "load"))
    o.append(dim(s, p, L5[0], Bc[0], y_rl, BRN, "load"))
    if mode == "d5":
        lt, ll = sym("ℓ", "t", s) + " sin β", sym("ℓ", "L", s) + " sin β"
    else:
        lt = sym("r", "t", s) + (" = 0.30 m" if mode == "main" else "")
        ll = sym("r", "L", s) + (" = 0.40 m" if mode == "main" else "")
    o.append(H.label(s, (L5[0] + Cub[0]) / 2, y_rt + s(18), lt, fill=BRN, anchor="middle"))
    o.append(H.label(s, (L5[0] + Bc[0]) / 2, y_rl + s(18), ll, fill=BRN, anchor="middle"))
    if mode == "d5":                                   # along-trunk distances l_t, l_L (line 604), behind the back
        ell_l = R_BOX / math.sin(math.radians(BETA))
        Pl = along(ell_l)
        o.append(H.line(s, Pl[0], Pl[1], Bc[0], by - s(2), O["dim"], "leader", H.DASH_REF))
        o.append(f'<circle cx="{Pl[0]:.2f}" cy="{Pl[1]:.2f}" r="{s(3):.2f}" fill="{BRN}"/>')
        o.append(H.line(s, *along(0.0, n=D_ES), *along(0.0, n=0.235), O["dim"], "leader"))
        for ell, nm, off, lab in ((ELL_T, "t", 0.14, (ELL_T / 2, 0.18)), (ell_l, "L", 0.22, (0.30, 0.255))):
            o.append(H.line(s, *along(ell, n=0.0), *along(ell, n=off + 0.015), O["dim"], "leader"))
            o.append(H.line(s, *along(0.0, n=off), *along(ell, n=off), BRN, "ref",
                            extra=f'marker-start="url(#{p}a_load)" marker-end="url(#{p}a_load)"'))
            q = along(*lab)
            o.append(H.label(s, q[0], q[1] + s(5), sym("ℓ", nm, s), fill=BRN, anchor="middle"))
    return o, J


def stoop_fig(p, VB, s, k, heel, mode, aria, extra):
    o, J = stoop_scene(s, p, k, heel, mode)
    o = [f'<defs>{H.markers(p, s)}</defs>', floor(s, VB[0] + s(8), VB[0] + VB[2] - s(8), heel[1])] + o
    o.append(credit_bottom(s, VB, extra))
    return finish(VB, aria, s, o)


def fig7():
    VB = (0, 0, 760, 700)
    aria = ("Side view of a skeleton in a straight-legged stoop, trunk flexed beta = 60 degrees from vertical, arms "
            "straight down holding a 20 kg box 0.40 m ahead of the L5/S1 disc. The upper-body weight W ub = 412 N acts "
            "at the head-arms-trunk centre of mass 0.30 m ahead of L5/S1; the box weight W L = 196 N acts 0.40 m ahead. "
            "The erector spinae pull F es of about 4.04 kN runs along the back, 0.05 m behind the disc, toward the pelvis.")
    return stoop_fig("m1f7_", VB, H.Scale(VB[2], VB[3]), 400.0, (150.0, 600.0), "main", aria,
                     " Box and overlays drawn for this course; arrows are not to force scale.")


def fig17():
    VB = (0, 0, 400, 590)
    aria = ("Problem C7 setup: a skeleton in a straight-legged stoop lifting a box. The upper-body weight W ub and the "
            "box weight W L hang at long horizontal arms r t and r L ahead of the L5/S1 disc; the erector spinae force "
            "F es pulls along the back through the short arm d es behind the disc.")
    return stoop_fig("m1f17_", VB, H.Scale(VB[2], VB[3], display_w=400), 300.0, (78.0, 470.0), "c7", aria,
                     " Box and overlays drawn for this course.")


def fig25():
    VB = (0, 0, 400, 590)
    aria = ("Problem D5 setup: a skeleton in a stoop, the trunk axis from L5/S1 tilted beta from vertical. The upper-body "
            "weight W ub sits at along-trunk distance l t and the box weight W L acts where its vertical line meets the "
            "trunk axis, at along-trunk distance l L; their horizontal arms are l t sin beta and l L sin beta. The "
            "erector spinae force F es acts at the short arm d es behind the disc.")
    return stoop_fig("m1f25_", VB, H.Scale(VB[2], VB[3], display_w=400), 300.0, (78.0, 470.0), "d5", aria,
                     " Box and overlays drawn for this course.")


# ================================================================ more pose solvers
def on_toes(ball=0.06, plantar=25.0):
    """Rising on the toes: feet plantarflexed `plantar` deg (heels up), the straight body leaned forward about the
    ankles until the whole-body COM is `ball` metres behind the toe tip (over the ball of the foot)."""
    def kw(lam):
        return dict(pelvis=lam, near=dict(hip=0.0, contact=None, ankle=lam - plantar),
                    far=dict(hip=0.0, contact="toe"), anchor=("toe", "near"))

    def f(lam):
        J = joints(LB.pose(**kw(lam)))
        return (J["toe"][0] - J["com"][0]) * UM
    return kw(bisect(f, 0.0, 15.0, ball))


def squat(mid=0.06):
    """Deep squat at the start of the rise (feet flat, thighs near horizontal, arms forward): the trunk lean is
    solved so that the whole-body COM is `mid` metres ahead of the ankle."""
    def kw(tr):
        L = dict(hip=115.0, knee=105.0, shoulder=75.0, elbow=10.0)
        return dict(pelvis=35.0, trunk=tr, near=dict(L), far=dict(L))

    def f(tr):
        J = joints(LB.pose(**kw(tr)))
        return (J["com"][0] - J["ankle"][0]) * UM
    return kw(bisect(f, -10.0, 40.0, mid))


H_STEP = 0.18                      # m, step height drawn (K8 sweeps h = 0.15, 0.18, 0.20 m, line 762)


def step_up(h=H_STEP):
    """Kit step_up preset with the leading (near) hip flexion solved so the near foot stands h metres up."""
    def kw(hp):
        d = dict(LB.POSES["step_up"])
        d["near"] = dict(d["near"], hip=hp, knee=hp + 10.0)
        return d

    def f(hp):
        J = joints(LB.pose(**kw(hp)))
        return (J["floor_y"] - J["heel"][1]) * UM
    return kw(bisect(f, 50.0, 85.0, h))


def reach(dx, dy):
    """Both arms posed (two-link inverse kinematics, elbow below the line) so the grip lies dx metres ahead of and
    dy metres below the shoulder joint centre of the upright kit body."""
    a, b = LB.L_UPPER * UM, (LB.L_FORE + 0.45 * LB.L_HAND) * UM
    D = math.hypot(dx, dy)
    e = 180.0 - math.degrees(math.acos((a * a + b * b - D * D) / (2 * a * b)))
    sh = math.degrees(math.atan2(dx, dy) - math.acos((a * a + D * D - b * b) / (2 * a * D)))
    return dict(near=dict(shoulder=sh, elbow=e), far=dict(shoulder=sh, elbow=e))


def arm_to(base, x_target, sh=None, elbow=None, ref="shoulder"):
    """Upright stance with the near and far arm posed so the grip lands x_target metres ahead of J[ref].
    Give `sh` to solve the elbow, or `elbow` to solve the shoulder."""
    def kw(v):
        L = dict(shoulder=sh if sh is not None else v, elbow=v if sh is not None else elbow)
        return dict(base, near=dict(base.get("near", {}), **L), far=dict(base.get("far", {}), **L))

    def f(v):
        J = joints(LB.pose(**kw(v)))
        return (grip(J)[0] - J[ref][0]) * UM
    return kw(bisect(f, 0.0, 150.0, x_target))


# ================================================================ more drawing helpers
def small_dim(s, x0, x1, y, col, marker):
    """A dimension too short for heads inside it: heads outside, pointing in."""
    a = s(16)
    return (H.line(s, x0, y, x1, y, col, "ref") +
            H.line(s, x0 - a, y, x0, y, col, "ref", extra=f'marker-end="url(#{marker})"') +
            H.line(s, x1 + a, y, x1, y, col, "ref", extra=f'marker-end="url(#{marker})"'))


def torque_arc(s, p, c, r, a0, a1, key="force"):
    return arc_arrow(s, p, c[0], c[1], r, a0, a1, key)


def cup(s, x, y, r):
    """A mug seen from the side (schematic prop), centre (x, y), half-width r."""
    st = f'fill="#f7f4ef" stroke="{I["secondary"]}" stroke-width="{s(1.1):.2f}"'
    return (f'<path d="M{x + r:.2f},{y - r * 0.55:.2f} c{r * 0.7:.2f},0 {r * 0.7:.2f},{r * 1.1:.2f} 0,{r * 1.1:.2f}" '
            f'fill="none" stroke="{I["secondary"]}" stroke-width="{s(1.6):.2f}"/>'
            f'<path d="M{x - r:.2f},{y - r:.2f} h{2 * r:.2f} l{-r * 0.12:.2f},{2 * r:.2f} h{-r * 1.76:.2f} Z" {st}/>')


def bag(s, x, y, w, h):
    """Shopping bag hanging from a hand at (x, y): handles + body. Returns (svg, centre)."""
    top = y + h * 0.28
    st = f'stroke="{BRN}" stroke-width="{s(1.3):.2f}"'
    return (f'<path d="M{x - w * 0.32:.2f},{top:.2f} L{x:.2f},{y:.2f} L{x + w * 0.32:.2f},{top:.2f}" fill="none" {st}/>'
            f'<path d="M{x - w / 2:.2f},{top:.2f} h{w:.2f} l{w * 0.06:.2f},{h * 0.72:.2f} h{-w * 1.12:.2f} Z" '
            f'fill="#f7f4ef" {st}/>'), (x, top + h * 0.36)


def lean_scene(s, p, k, heel, mode):
    """Leaning forward: COM D_COM ahead of the ankle. mode "main" (values + faded upright body) or "d9"."""
    o = []
    if mode == "main":
        ghost, _ = body(LB.pose(), heel[0], heel[1], H_M * k)
        o.append(f'<g opacity="0.3">{ghost}</g>')
    svg, J = body(LB.pose(**lean()), heel[0], heel[1], H_M * k)
    o.append(svg)
    A, C, fy = J["ankle"], J["com"], heel[1]
    assert abs((C[0] - A[0]) / k - D_COM) < 1e-3
    o.append(vref(s, A[0], A[1] + s(8), fy + s(30)))
    wl = 0.42 * k
    o.append(vref(s, C[0], C[1] + wl + s(2), fy - 0.26 * k - s(2)))
    o.append(vref(s, C[0], fy + s(4), fy + s(30)))
    o.append(H.com_mark(s, *C))
    o.append(H.arrow(s, p, C[0], C[1] + s(9), C[0], C[1] + wl, "load"))
    o.append(H.arrow(s, p, C[0], fy - s(1), C[0], fy - 0.26 * k, "reaction"))
    o.append(cop_dot(s, C[0], fy))
    o.append(H.joint_centre(s, *A))
    o.append(torque_arc(s, p, A, 0.075 * k, -20.0, -160.0))
    o.append(small_dim(s, A[0], C[0], fy + s(22), BRN, f"{p}a_load"))
    if mode == "main":
        o.append(H.label(s, C[0] + s(12), C[1] - s(4), "COM"))
        o.append(H.label(s, C[0] + s(10), C[1] + wl - s(6), it("W") + " = " + it("Mg") + " = 687 N", fill=BRN))
        o.append(H.label(s, C[0] + s(10), fy - 0.26 * k + s(12), "GRF", fill=BLK))
        o.append(H.label(s, C[0] + s(10), fy - s(8), "COP", fill=BLK))
        o.append(H.label(s, C[0] + s(22), fy + s(27), sym("d", "COM", s) + " = 0.05 m", fill=BRN))
        o.append(H.label(s, A[0] - 0.075 * k - s(8), A[1] - s(30), sym("τ", "ankle", s) + " = " + it("W") +
                         sym(" d", "COM", s) + " ≈ 34 N·m", fill=RED, anchor="end"))
        o.append(H.label(s, A[0] - 0.075 * k - s(8), A[1] - s(13), "plantarflexors", "label2", I["secondary"], "end"))
    else:
        T_ = J["toe"]
        o.append(vref(s, T_[0], fy + s(4), fy + s(52)))
        o.append(dim(s, p, A[0], T_[0], fy + s(46), BLU, "geometry"))
        o.append(H.label(s, (A[0] + T_[0]) / 2, fy + s(64), sym("L", "f", s) + " (ankle to toe)", fill=BLU,
                         anchor="middle"))
        o.append(H.label(s, C[0] + s(11), C[1] - s(4), "COM"))
        o.append(H.label(s, C[0] + s(9), C[1] + wl - s(6), it("W"), fill=BRN))
        o.append(H.label(s, C[0] + s(9), fy - 0.26 * k + s(12), "GRF", fill=BLK))
        o.append(H.label(s, C[0] + s(9), fy - s(8), "COP", fill=BLK))
        o.append(H.label(s, C[0] + s(22), fy + s(27), sym("d", "COM", s), fill=BRN))
        o.append(H.label(s, A[0] - 0.075 * k - s(6), A[1] - s(18), sym("τ", "ankle", s), fill=RED, anchor="end"))
    return o, J


def fig9():
    p = "m1f9_"
    VB = (0, 0, 760, 700)
    s = H.Scale(VB[2], VB[3])
    k, heel = 320.0, (330.0, 600.0)
    o, J = lean_scene(s, p, k, heel, "main")
    o = [f'<defs>{H.markers(p, s)}</defs>', floor(s, 150, 640, heel[1])] + o
    o.append(H.label(s, J["vertex"][0] - 0.2 * k, 30, "faded: upright", "label2", I["secondary"], "end"))
    o.append(credit_bottom(s, VB, " Overlays drawn for this course; arrows are not to force scale."))
    aria = ("Side view of a skeleton leaning the trunk forward with the feet in place; a faded upright skeleton behind "
            "it. The whole-body centre of mass sits d COM = 0.05 m ahead of the ankle. Weight W = Mg = 687 N acts down "
            "through the COM; the ground reaction force acts up through the centre of pressure on the sole, directly "
            "below the COM. The calf muscles supply the ankle torque tau ankle = W d COM, about 34 N m.")
    return finish(VB, aria, s, o)


def fig29():
    p = "m1f29_"
    VB = (0, 0, 400, 580)
    s = H.Scale(VB[2], VB[3], display_w=400, max_h=H.MAX_DISPLAY_H_BODY)
    k, heel = 230.0, (150.0, 430.0)
    o, J = lean_scene(s, p, k, heel, "d9")
    o = [f'<defs>{H.markers(p, s)}</defs>', floor(s, 20, 380, heel[1])] + o
    o.append(credit_bottom(s, VB, " Overlays drawn for this course."))
    aria = ("Problem D9 setup: a skeleton leaning the trunk forward, feet in place. The centre of mass is d COM ahead of "
            "the ankle; the weight W acts down through it and the ground reaction force acts up through the centre of "
            "pressure below it. The ankle torque tau ankle holds the lean; L f marks the ankle-to-toe length of the foot.")
    return finish(VB, aria, s, o)


# ================================================================ quiet standing: svg #15 (C5)
def fig15():
    p = "m1f15_"
    VB = (0, 0, 400, 560)
    s = H.Scale(VB[2], VB[3], display_w=400, max_h=H.MAX_DISPLAY_H_BODY)
    k, heel = 230.0, (165.0, 432.0)
    svg, J = LB.standing_full("", s, heel[0], heel[1], H_M * k)
    C, fy = J["com"], heel[1]
    o = [f'<defs>{H.markers(p, s)}</defs>', floor(s, 20, 380, fy), svg]
    o.append(vref(s, C[0], C[1] + 0.30 * k + s(2), fy - 0.26 * k - s(2)))
    o.append(H.com_mark(s, *C))
    o.append(H.arrow(s, p, C[0], C[1] + s(9), C[0], C[1] + 0.30 * k, "load"))
    o.append(H.arrow(s, p, C[0], fy - s(1), C[0], fy - 0.26 * k, "reaction"))
    o.append(cop_dot(s, C[0], fy))
    o.append(H.label(s, C[0] + 0.12 * k, C[1] - s(4), "COM"))
    o.append(H.line(s, C[0] + s(8), C[1] - s(8), C[0] + 0.12 * k - s(3), C[1] - s(8), I["rule"], "leader"))
    o.append(H.label(s, C[0] + 0.12 * k, C[1] + 0.30 * k - s(4), it("W"), fill=BRN))
    o.append(H.label(s, C[0] + 0.12 * k, fy - 0.26 * k + s(10), "GRF", fill=BLK))
    o.append(H.label(s, C[0] + 0.15 * k, fy - s(10), "COP under COM", "label2", BLK))
    he, to = J["heel"][0], J["toe"][0]
    yb = fy + s(16)
    o.append(H.line(s, he, yb, to, yb, BLU, "geom"))
    o.append(H.line(s, he, yb - s(5), he, yb + s(5), BLU, "geom"))
    o.append(H.line(s, to, yb - s(5), to, yb + s(5), BLU, "geom"))
    o.append(H.label(s, (he + to) / 2, yb + s(18), "base of support", "label2", BLU, "middle"))
    o.append(H.label(s, he - s(6), yb + s(4), "heel", "label2", I["secondary"], "end"))
    o.append(H.label(s, to + s(6), yb + s(4), "toe", "label2", I["secondary"]))
    o.append(credit_bottom(s, VB, " Overlays drawn for this course."))
    aria = ("Problem C5 setup: side view of a person standing quietly (skeleton inside the body outline). The centre of "
            "mass sits above the foot; the weight W acts down through it and the ground reaction force acts up through "
            "the centre of pressure directly below it, inside the base of support that runs from heel to toe.")
    return finish(VB, aria, s, o)


# ================================================================ upward acceleration: svg #16 (C6), #27 (D7)
A_DRAW = 0.5                       # drawn a = 0.5 g: GRF arrow 1.5 x the weight arrow (C6 and D7 state no value)


def accel_scene(s, p, k, anchor_pt, P, mode):
    svg, J = body(P, anchor_pt[0], anchor_pt[1], H_M * k)
    C, fy = J["com"], J["floor_y"]
    wl = 0.24 * k
    o = [svg]
    o.append(vref(s, C[0], C[1] + wl + s(2), fy - (1 + A_DRAW) * wl - s(2)))
    o.append(H.com_mark(s, *C))
    o.append(H.arrow(s, p, C[0], C[1] + s(9), C[0], C[1] + wl, "load"))
    o.append(H.arrow(s, p, C[0], fy - s(1), C[0], fy - (1 + A_DRAW) * wl, "reaction"))
    o.append(cop_dot(s, C[0], fy))
    ax0 = C[0] + 0.20 * k
    o.append(H.arrow(s, p, ax0, C[1] + 0.06 * k, ax0, C[1] - 0.12 * k, "geometry"))
    o.append(H.label(s, ax0 + s(7), C[1] - 0.06 * k, it("a") + (" (COM)" if mode == "c6" else "(" + it("t") + ")"),
                     fill=BLU))
    o.append(H.label(s, C[0] - s(10), C[1] + wl - s(4), it("W") + " = " + it("Mg"), fill=BRN, anchor="end"))
    lab = (sym("F", "GRF", s) + " = " + it("W") + " + " + it("Ma") if mode == "c6" else
           sym("F", "GRF", s) + "(" + it("t") + ") = " + it("M") + "(" + it("g") + " + " + it("a") + ")")
    if mode == "d7":                               # behind the shins, under the thighs
        lx, ly, an = C[0] - s(10), fy - 0.17 * k, "end"
    else:
        lx, ly, an = C[0] + s(10), fy - (1 + A_DRAW) * wl + s(12), "start"
    o.append(H.label(s, lx, ly, lab, fill=BLK, anchor=an))
    o.append(H.label(s, lx, ly + s(17), "longer than " + it("W"), "label2", I["secondary"], an))
    o.append(H.label(s, C[0] + s(9), fy - s(8), "COP", "label2", BLK))
    return o, J


def fig16():
    p = "m1f16_"
    VB = (0, 0, 400, 560)
    s = H.Scale(VB[2], VB[3], display_w=400, max_h=H.MAX_DISPLAY_H_BODY)
    k = 230.0
    P = LB.pose(**on_toes())
    _, J0 = body(P, 0, 0, H_M * k)
    toe = (140.0 + (J0["toe"][0] - J0["bbox"][0]), 470.0)
    o, J = accel_scene(s, p, k, toe, P, "c6")
    o = [f'<defs>{H.markers(p, s)}</defs>', floor(s, 20, 380, J["floor_y"])] + o
    o.append(H.label(s, 20, 30, "rising onto the toes", "label2", I["secondary"]))
    o.append(credit_bottom(s, VB, " Overlays drawn for this course; arrows drawn for a = 0.5 g."))
    aria = ("Problem C6 setup: side view of a skeleton rising onto the toes, heels off the floor, its centre of mass "
            "accelerating upward with a. The weight W = Mg acts down through the COM; the ground reaction force under "
            "the ball of the foot, F GRF = W + Ma, is drawn longer than W.")
    return finish(VB, aria, s, o)


def fig27():
    p = "m1f27_"
    VB = (0, 0, 400, 470)
    s = H.Scale(VB[2], VB[3], display_w=400, max_h=H.MAX_DISPLAY_H_BODY)
    k = 230.0
    P = LB.pose(**squat())
    _, J0 = body(P, 0, 0, H_M * k)
    heel = (110.0 + (J0["heel"][0] - J0["bbox"][0]), 380.0)
    o, J = accel_scene(s, p, k, heel, P, "d7")
    o = [f'<defs>{H.markers(p, s)}</defs>', floor(s, 20, 380, J["floor_y"])] + o
    o.append(H.label(s, 20, 30, "rising from a squat", "label2", I["secondary"]))
    o.append(credit_bottom(s, VB, " Overlays drawn for this course; arrows drawn for a = 0.5 g."))
    aria = ("Problem D7 setup: side view of a skeleton in a squat, starting to rise, its centre of mass accelerating "
            "upward with a(t). The weight W = Mg acts down through the COM; the ground reaction force F GRF(t) = "
            "M(g + a(t)) acts up through the centre of pressure and is drawn longer than W.")
    return finish(VB, aria, s, o)


# ================================================================ stair step: svg #30 (D10)
def fig30():
    p = "m1f30_"
    VB = (0, 0, 400, 520)
    s = H.Scale(VB[2], VB[3], display_w=400, max_h=H.MAX_DISPLAY_H_BODY)
    k = 220.0
    P = LB.pose(**step_up())
    _, J0 = body(P, 0, 0, H_M * k)
    heel = (95.0 + (J0["heel_far"][0] - J0["bbox"][0]), 430.0)
    svg, J = body(P, heel[0], heel[1], H_M * k)
    fy, C = heel[1], J["com"]
    top = J["heel"][1]
    assert abs((fy - top) / k - H_STEP) < 1e-3
    x0, x1 = J["heel"][0] - 0.06 * k, VB[2] - s(12)
    st = f'fill="#f7f4ef" stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"'
    o = [f'<defs>{H.markers(p, s)}</defs>', floor(s, 12, x0, fy),
         f'<path d="M{x0:.2f},{fy:.2f} V{top:.2f} H{x1:.2f} V{fy:.2f} Z" {st}/>', svg]
    o.append(H.line(s, x0 - s(14), fy, x0 - s(14), top, BLU, "ref",
                    extra=f'marker-start="url(#{p}a_geometry)" marker-end="url(#{p}a_geometry)"'))
    o.append(H.label(s, x0 - s(20), (fy + top) / 2 + s(5), it("h"), fill=BLU, anchor="end"))
    o.append(H.com_mark(s, *C))
    o.append(H.arrow(s, p, C[0], C[1] + s(9), C[0], C[1] + 0.26 * k, "load"))
    o.append(H.label(s, C[0] + s(9), C[1] + 0.26 * k - s(4), it("Mg"), fill=BRN))
    vx = C[0] + 0.24 * k
    o.append(H.arrow(s, p, vx, C[1] + 0.06 * k, vx, C[1] - 0.14 * k, "geometry"))
    o.append(H.label(s, vx + s(7), C[1] - 0.05 * k, it("v") + " = " + it("fh"), fill=BLU))
    o.append(H.label(s, C[0] - s(12), C[1] - s(8), "COM", anchor="end"))
    o.append(H.label(s, x1 - s(6), top - s(10), it("P") + " = " + it("Mgv"), anchor="end"))
    o.append(credit_bottom(s, VB, f" Step drawn for this course at h = {H_STEP:.2f} m.", width=VB[2] - s(16)))
    aria = ("Problem D10 setup: side view of a skeleton stepping up onto a stair of height h, the leading foot on the "
            "step and the trailing foot on the floor. The centre of mass rises at vertical speed v = f h; the weight "
            "Mg acts down through it; the mechanical power is P = M g v.")
    return finish(VB, aria, s, o)


# ================================================================ cup close vs extended: svg #12 (C2)
CUP_R = 0.045                      # m, mug half-width (schematic prop)


def fig12():
    p = "m1f12_"
    VB = (0, 0, 400, 510)
    s = H.Scale(VB[2], VB[3], display_w=400, max_h=H.MAX_DISPLAY_H_BODY)
    k = 210.0
    chest = 0.211                  # m, body outline 1.30 m up: 0.21 m ahead of the shoulder joint (lynch_lat_body skin)
    poses = [(reach(chest + CUP_R, 0.15), "close"), (dict(near=dict(shoulder=90.0), far=dict(shoulder=90.0)), "extended")]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    fy = 395.0
    o.append(floor(s, 12, VB[2] - 12, fy))
    for (kw, name), hx in zip(poses, (40.0, 205.0)):
        svg, J = body(LB.pose(**kw), hx, fy, H_M * k, skin=True)
        Sh, Gp = J["shoulder"], grip(J)
        o.append(svg)
        o.append(cup(s, Gp[0], Gp[1] - CUP_R * k * 0.6, CUP_R * k))
        yb = Gp[1] + CUP_R * k * 0.5
        o.append(H.arrow(s, p, Gp[0], yb, Gp[0], yb + 0.20 * k, "load"))
        o.append(H.label(s, Gp[0] + s(7), yb + 0.20 * k - s(2), sym("W", "L", s), fill=BRN))
        yd = fy + s(18)
        o.append(vref(s, Sh[0], Sh[1] + s(8), yd + s(6)))
        o.append(vref(s, Gp[0], yb + 0.20 * k + s(2), yd + s(6)))
        o.append(dim(s, p, Sh[0], Gp[0], yd, BRN, "load"))
        o.append(H.label(s, (Sh[0] + Gp[0]) / 2, yd + s(17), it("d"), fill=BRN, anchor="middle"))
        o.append(H.joint_centre(s, *Sh))
        o.append(H.label(s, hx + 0.10 * k, 24, name, "label2", I["secondary"], "middle"))
    o.append(credit_bottom(s, VB, " Cup and overlays drawn for this course."))
    aria = ("Problem C2 setup: two side views of the same standing person holding the same cup. Left: the cup held "
            "against the chest, a short horizontal distance d in front of the shoulder joint. Right: the arm extended "
            "straight forward, the cup a long distance d in front of the shoulder. The cup weight W L is the same in both.")
    return finish(VB, aria, s, o)


# ================================================================ box close vs in front: svg #18 (C8)
BOX_D = 0.25                       # m, box depth (front to back) drawn in C8
BELLY = 0.105                      # m, body outline at L5/S1 height: 0.105 m ahead of L5/S1 (lynch_lat_body skin)
D_SH = 0.098                       # m, kit shoulder joint behind L5/S1 when upright


def fig18():
    p = "m1f18_"
    VB = (0, 0, 400, 470)
    s = H.Scale(VB[2], VB[3], display_w=400, max_h=H.MAX_DISPLAY_H_BODY)
    k = 200.0
    close = BELLY + BOX_D / 2
    poses = [(reach(close + D_SH, 0.37), "pressed to the belly"),
             (arm_to(dict(), R_BOX, elbow=0.0, ref="l5s1"), "held out in front")]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    fy = 395.0
    o.append(floor(s, 12, VB[2] - 12, fy))
    for (kw, name), hx in zip(poses, (45.0, 215.0)):
        svg, J = body(LB.pose(**kw), hx, fy, H_M * k, skin=True)
        L5, Gp = J["l5s1"], grip(J)
        xc = L5[0] + (close if name.startswith("pressed") else R_BOX) * k
        assert abs(Gp[0] - xc) < 0.5
        bw, bh = BOX_D * k, 0.22 * k
        o.append(box(s, xc - bw / 2, Gp[1] - bh / 2, bw, bh))
        o.append(svg)
        o.append(H.arrow(s, p, xc, Gp[1] + bh / 2 + s(1), xc, Gp[1] + bh / 2 + 0.18 * k, "load"))
        o.append(H.label(s, xc + s(7), Gp[1] + bh / 2 + 0.18 * k - s(2), sym("W", "L", s), fill=BRN))
        yd = fy - 0.22 * k
        o.append(vref(s, L5[0], L5[1] + s(8), yd + s(6)))
        o.append(vref(s, xc, Gp[1] + bh / 2 + 0.18 * k + s(2), yd + s(6)))
        o.append(dim(s, p, L5[0], xc, yd, BRN, "load"))
        o.append(H.label(s, (L5[0] + xc) / 2, yd + s(17), sym("r", "L", s), fill=BRN, anchor="middle"))
        o.append(H.joint_centre(s, *L5))
        o.append(H.label(s, hx + 0.10 * k, 24, name, "label2", I["secondary"], "middle"))
        if name.startswith("pressed"):
            o.append(H.label(s, L5[0] - s(12), L5[1] + s(5), "L5/S1", "label2", anchor="end"))
    o.append(credit_bottom(s, VB, " Box and overlays drawn for this course."))
    aria = ("Problem C8 setup: two side views of the same upright person carrying the same box. Left: the box pressed "
            "against the belly, its weight W L a short horizontal distance r L ahead of the L5/S1 disc. Right: the box "
            "held out in front with straight arms, r L much longer.")
    return finish(VB, aria, s, o)


# ================================================================ two-foot stance, load to one side: svg #26 (D6)
M_BAG = 10.0                       # kg, load drawn in D6 (the text gives none)


def fig26():
    p = "m1f26_"
    VB = (0, 0, 400, 615)
    s = H.Scale(VB[2], VB[3], display_w=400, max_h=H.MAX_DISPLAY_H_BODY)
    k = 210.0
    P = LB.pose_ant(r=dict(hip=8.0, shoulder=14.0, elbow=0.0, wrist=0.0), l=dict(hip=8.0, **LB._ANT_ARMS))
    _, J0 = body(P, 0, 0, H_M * k)
    fy = 420.0
    svg, J = body(P, 215.0, fy - J0["floor_y"], H_M * k)
    Gp = grip(J, "_r")
    bsvg, Bc = bag(s, Gp[0], Gp[1], 0.20 * k, 0.26 * k)
    xR, xL = J["sole_r"][0], J["sole_l"][0]
    xc = (M_BODY * J["com"][0] + M_BAG * Bc[0]) / (M_BODY + M_BAG)       # combined COM, screen x
    yc = (M_BODY * J["com"][1] + M_BAG * Bc[1]) / (M_BODY + M_BAG)
    # moments about the left foot, x positive toward the subject's right (= image left)
    W = (M_BODY + M_BAG) * G
    RR = W * (xL - xc) / (xL - xR)
    RL = W - RR
    assert RR > RL > 0
    sc = 0.30 * k / W                                                     # arrow length per newton
    o = [f'<defs>{H.markers(p, s)}</defs>', floor(s, 12, VB[2] - 12, fy), svg, bsvg]
    o.append(H.arrow(s, p, Bc[0], Bc[1] + 0.10 * k, Bc[0], Bc[1] + 0.22 * k, "load"))
    o.append(H.label(s, Bc[0] - s(7), Bc[1] + 0.22 * k - s(2), sym("W", "load", s), fill=BRN, anchor="end"))
    o.append(H.com_mark(s, xc, yc))
    o.append(H.arrow(s, p, xc, yc + s(9), xc, yc + 0.22 * k, "load"))
    o.append(H.label(s, xc + s(9), yc + 0.22 * k - s(2), sym("W", "tot", s), fill=BRN))
    o.append(H.label(s, xc + s(10), yc - s(8), "COM (body + load)", "label2"))
    o.append(vref(s, xc, yc + 0.22 * k + s(2), fy - s(5)))
    o.append(cop_dot(s, xc, fy))
    for x, R, nm in ((xR, RR, "R"), (xL, RL, "L")):
        o.append(H.arrow(s, p, x, fy + R * sc, x, fy + s(1), "reaction"))
        o.append(H.label(s, x + (-s(8) if nm == "R" else s(8)), fy + R * sc - s(4), sym("R", nm, s), fill=BLK,
                         anchor="end" if nm == "R" else "start"))
    yx = fy + 0.30 * k * max(RR, RL) / W + s(24)
    for x, nm, foot in ((xR, sym("x", "R", s), "right foot"), (xc, sym("x", "COP", s), ""),
                        (xL, sym("x", "L", s), "left foot")):
        o.append(H.line(s, x, yx - s(5), x, yx + s(5), I["axis"], "axis"))
        o.append(H.label(s, x, yx + (s(20) if foot else -s(9)), nm, "label", anchor="middle"))
        if foot:
            o.append(H.label(s, x, yx + s(36), foot, "label2", I["secondary"], "middle"))
    o.append(H.line(s, VB[2] - s(40), yx, s(40), yx, I["axis"], "axis", extra=f'marker-end="url(#{p}a_dim)"'))
    o.append(H.label(s, s(34), yx + s(5), it("x"), "label", anchor="end"))
    o.append(H.label(s, s(12), 24, "front view: the subject’s right is on the image left", "label2", I["secondary"]))
    o.append(credit_bottom(s, VB, f" Load (drawn as {M_BAG:.0f} kg on a 70 kg body), arrows and overlays drawn for "
                                  "this course."))
    aria = ("Problem D6 setup: front view of a skeleton standing on two feet with a bag in its right hand, held out to "
            "the side. The combined centre of mass of body and load sits toward the loaded right foot, and so does the "
            "centre of pressure x COP between the foot positions x R and x L; the floor pushes up with R R under the "
            "right foot, larger than R L under the left. The x axis points toward the subject's right.")
    return finish(VB, aria, s, o)


# ================================================================ lumbar stack: svg #6 (Fig. 5)
# Anterior kit body (pose_ant standing, anchor = mid-hip point at the origin), body units U, read off a 0.2-U grid
# render of hbody_ant_trunk + hbody_ant_pelvis: lumbar bodies L1 -151.8..-140.5, L4 -110..-94, L5 -89.5..-74.5;
# the L4/L5 disc -94..-89.5; the L5/S1 disc -73..-66.3 (its lower edge = lynch_body l5s1, -66.3); sacrum below.
LUMBAR = dict(win=(-46.0, -162.0, 92.0, 120.0), L1=-146.0, L4=-102.0, L45=-91.8, L5=-82.0, L5S1=-69.6, sacrum=-52.0)


def fig6():
    p = "m1f6_"
    VB = (0, 0, 680, 520)
    s = H.Scale(VB[2], VB[3])
    kA = 3.5                                      # figure units per body unit
    wx, wy = 196.0, 16.0
    x0u, y0u, wu, hu = LUMBAR["win"]
    ox, oy = wx - x0u * kA, wy - y0u * kA         # where the mid-hip point lands
    svg, J = body(LB.pose_ant(**LB.POSES_ANT["standing"]), ox, oy, LB.H_U * kA)
    svg = re.sub(r'<use href="#hbody_(?!ant_trunk"|ant_pelvis")[^>]*/>', "", svg)
    assert svg.count("<use") == 2
    ww, wh = wu * kA, hu * kA
    o = [f'<defs>{H.markers(p, s)}<pattern id="{p}w" patternUnits="userSpaceOnUse" x="{wx:.2f}" y="{wy:.2f}" '
         f'width="{ww:.2f}" height="{wh:.2f}"><g transform="translate({-wx:.2f} {-wy:.2f})">{svg}</g></pattern></defs>',
         f'<rect x="{wx:.2f}" y="{wy:.2f}" width="{ww:.2f}" height="{wh:.2f}" fill="url(#{p}w)"/>']
    Y = lambda v: oy + v * kA  # noqa: E731
    xl = wx - s(14)
    for txt, yv, xu_ in (("vertebral body (L4)", LUMBAR["L4"], -6.0), ("intervertebral disc", LUMBAR["L45"], -8.0),
                         ("L5/S1 disc", LUMBAR["L5S1"], -9.0), ("sacrum", LUMBAR["sacrum"], -4.0)):
        o.append(H.line(s, xl + s(4), Y(yv), ox + xu_ * kA, Y(yv), I["rule"], "leader"))
        o.append(H.label(s, xl, Y(yv) + s(5), txt, anchor="end"))
    # the lumbar column L1..L5, bracketed on the right
    xb = wx + ww + s(12)
    top, bot = Y(-151.8), Y(-74.5)
    o.append(f'<path d="M{xb - s(6):.2f},{top:.2f} h{s(6):.2f} V{bot:.2f} h{-s(6):.2f}" fill="none" '
             f'stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
    o.append(H.label(s, xb + s(8), (top + bot) / 2 - s(4), "lumbar vertebrae"))
    o.append(H.label(s, xb + s(8), (top + bot) / 2 + s(14), "L1 to L5", "label2", I["secondary"]))
    # the compression C through the L5/S1 disc: the two neighbours pressed together
    o.append(H.arrow(s, p, ox, Y(-88.0), ox, Y(-73.5), "reaction"))
    o.append(H.arrow(s, p, ox, Y(-50.0), ox, Y(-65.8), "reaction"))
    o.append(H.label(s, ox + s(8), Y(-82.0) + s(4), it("C"), fill=BLK))
    o.append(H.label(s, ox + s(8), Y(-56.0) + s(4), it("C"), fill=BLK))
    o.append(H.label(s, wx + ww / 2, wy + wh + s(18), "front view", "label2", I["secondary"], "middle"))
    t = H.ATTRIBUTION["by"].format(
        author="Patrick J. Lynch, medical illustrator", title="Skeleton whole body ant lat views.svg",
        licence="CC BY 2.5", changes="Recoloured; the lumbar region of the anterior view. Labels and arrows drawn "
                                     "for this course.")
    lines = wrap(t, 100)
    o.append(H.credit(s, s(8), ruled(s, VB, len(lines)), lines))
    aria = ("Front view of the lower spine from the Lynch skeleton: the five lumbar vertebrae L1 to L5 stacked above the "
            "sacrum, each vertebral body separated from the next by an intervertebral disc. Two opposed arrows C press "
            "L5 and the sacrum together across the lowest disc, L5/S1.")
    return finish(VB, aria, s, o)


# ================================================================ base of support: svg #8 (Fig. 7)
# foot_plantar.py plantar_outline_path: right foot, u heel -> toe (0..0.98 of the length), v < 0 lateral.
PLANTAR = [(0.00, 0.08), (0.02, -0.10), (0.08, -0.16), (0.18, -0.14), (0.32, -0.12), (0.50, -0.14), (0.68, -0.16),
           (0.82, -0.12), (0.94, -0.04), (0.98, 0.04), (0.96, 0.12), (0.88, 0.16), (0.72, 0.14), (0.55, 0.10),
           (0.40, 0.06), (0.25, 0.04), (0.12, 0.06), (0.04, 0.10)]


def smooth_closed(pts):
    """Closed Catmull-Rom spline through pts as cubic Beziers."""
    n, d = len(pts), [f"M{pts[0][0]:.2f},{pts[0][1]:.2f}"]
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p2[0]:.2f},{p2[1]:.2f}")
    return "".join(d) + "Z"


def hull(pts):
    """Convex hull (monotone chain), counter-clockwise."""
    q = sorted(set(pts))
    if len(q) < 3:
        return q

    def half(seq):
        h = []
        for pt in seq:
            while len(h) >= 2 and ((h[-1][0] - h[-2][0]) * (pt[1] - h[-2][1]) -
                                   (h[-1][1] - h[-2][1]) * (pt[0] - h[-2][0])) <= 0:
                h.pop()
            h.append(pt)
        return h
    lo, up = half(q), half(q[::-1])
    return lo[:-1] + up[:-1]


def fig8():
    p = "m1f8_"
    VB = (0, 0, 760, 600)
    s = H.Scale(VB[2], VB[3])
    k, heel = 270.0, (130.0, 510.0)
    svg, J = LB.standing_full("", s, heel[0], heel[1], H_M * k)
    C, fy = J["com"], heel[1]
    o = [f'<defs>{H.markers(p, s)}</defs>', floor(s, 30, 360, fy), svg]
    o.append(vref(s, C[0], C[1] + 0.30 * k + s(2), fy - 0.28 * k - s(2)))
    o.append(H.com_mark(s, *C))
    o.append(H.arrow(s, p, C[0], C[1] + s(9), C[0], C[1] + 0.30 * k, "load"))
    o.append(H.arrow(s, p, C[0], fy - s(1), C[0], fy - 0.28 * k, "reaction"))
    o.append(cop_dot(s, C[0], fy))
    lx = C[0] + 0.16 * k
    o.append(H.line(s, C[0] + s(8), C[1], lx - s(4), C[1], I["rule"], "leader"))
    o.append(H.label(s, lx, C[1] + s(5), "COM"))
    o.append(H.label(s, lx, C[1] + 0.30 * k - s(4), it("W") + " = " + it("Mg"), fill=BRN))
    o.append(H.label(s, lx, fy - 0.28 * k + s(10), "GRF", fill=BLK))
    o.append(H.line(s, C[0] + s(6), fy - s(3), lx - s(4), fy - s(12), I["rule"], "leader"))
    o.append(H.label(s, lx, fy - s(8), "COP", fill=BLK))
    he, to = J["heel"][0], J["toe"][0]
    yb = fy + s(16)
    o.append(H.line(s, he, yb, to, yb, BLU, "geom"))
    for x in (he, to):
        o.append(H.line(s, x, yb - s(5), x, yb + s(5), BLU, "geom"))
    o.append(H.label(s, (he + to) / 2, yb + s(18), "base of support, side view", "label2", BLU, "middle"))
    o.append(H.label(s, 30, 30, "side view", "label2", I["secondary"]))
    # ---- top view of both soles; the subject faces up the page (toes up, subject's right = image right)
    kt = 640.0                                    # figure units per metre in the top view
    Lf = (LB.LAT["toe_x"] - LB.LAT["heel_x"]) * UM          # heel-to-toe length of the side-view foot, 0.274 m
    sep = (joints(LB.pose_ant(**LB.POSES_ANT["standing"]))["sole_l"][0] -
           joints(LB.pose_ant(**LB.POSES_ANT["standing"]))["sole_r"][0]) * UM   # 0.14 m between the foot centres
    cx, hy = 500.0, 440.0                         # midline x, heel line y
    L = Lf / 0.98 * kt
    feet = []
    for side in (1, -1):                          # 1 = subject's right (image right)
        xc = cx + side * sep / 2 * kt
        feet.append([(xc - side * v * L, hy - u_ * L) for u_, v in PLANTAR])
    Hl = hull([q for f in feet for q in f])
    o.append(f'<path d="M{"L".join(f"{x:.2f},{y:.2f}" for x, y in Hl)}Z" fill="{BLU}" fill-opacity="0.10" '
             f'stroke="{BLU}" stroke-width="{s(H.PX["geom"]):.2f}" stroke-dasharray="{s(6):.2f} {s(4):.2f}"/>')
    for f in feet:
        o.append(f'<path d="{smooth_closed(f)}" fill="{T["skin"][0]}" stroke="{T["skin"][1]}" '
                 f'stroke-width="{s(1.4):.2f}"/>')
    ankle_u = (LB.LAT["ankle"][0] - LB.LAT["heel_x"]) * UM
    cop = (cx, hy - (ankle_u + (C[0] - J["ankle"][0]) / k) * kt)
    o.append(cop_dot(s, *cop))
    xr = max(x for x, _ in Hl)
    o.append(H.line(s, cop[0] + s(6), cop[1], xr + s(14), cop[1], I["rule"], "leader"))
    o.append(H.label(s, xr + s(18), cop[1] + s(5), "COP, under the COM", fill=BLK))
    o.append(H.label(s, xr + s(18), hy - 0.62 * L + s(5), "base of support", fill=BLU))
    o.append(H.line(s, xr + s(2), hy - 0.62 * L, xr + s(14), hy - 0.62 * L, I["rule"], "leader"))
    o.append(H.label(s, cx - sep / 2 * kt, hy + s(22), "left foot", "label2", I["secondary"], "middle"))
    o.append(H.label(s, cx + sep / 2 * kt, hy + s(22), "right foot", "label2", I["secondary"], "middle"))
    o.append(H.label(s, cx, 30, "top view (toes up)", "label2", I["secondary"], "middle"))
    o.append(credit_bottom(s, VB, " Foot outlines (top view): schematic, drawn for this course. Overlays drawn for "
                                  "this course; arrows are not to force scale."))
    aria = ("Two panels. Left, side view: a person standing quietly; the weight W = Mg acts down through the centre of "
            "mass and the ground reaction force acts up through the centre of pressure on the sole, directly below it; "
            "the base of support runs from heel to toe. Right, top view of both soles: the base of support is the dashed "
            "outline drawn around both feet, and the centre of pressure lies inside it, under the centre of mass.")
    return finish(VB, aria, s, o)


FIGS = {
    6: ("Lumbar vertebrae for low-back moment discussion.", fig6),
    7: ("Stooped lift: erector-spinae force at L5/S1 and the load at horizontal reach r_L"[:60], fig7),
    8: ("Base of support: outline of contact patch under the feet", fig8),
    9: ("Ankle moment balance: COM forward of ankle, COP under the foot", fig9),
    12: ("The same cup held close to the trunk versus extended forward.", fig12),
    15: ("Quiet standing: COM above the base of support, COP tracking beneath it."[:60], fig15),
    16: ("Upward COM acceleration: the GRF grows beyond body weight.", fig16),
    17: ("Stooped lift: trunk weight and load act at long horizontal arms about L5/S1, opposed by the short "
         "erector-spinae arm."[:60], fig17),
    18: ("Load carried at the side/against the trunk versus out in front."[:60], fig18),
    25: ("Trunk flexed at angle beta; horizontal moment arms grow as sin beta."[:60], fig25),
    26: ("Two-foot stance with an asymmetric load; COP shifts toward the load."[:60], fig26),
    27: ("Rising from a squat: GRF exceeds body weight during upward acceleration."[:60], fig27),
    29: ("Leaning forward: COM shifts ahead of the ankle, COP slides toward the toe."[:60], fig29),
    30: ("Climbing one step of height h at vertical speed v.", fig30),
}
