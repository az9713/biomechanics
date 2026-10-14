"""Module 9, group `body_prob`: conceptual and derivational problems with a body or leg-spring drawing
(C1-C8: svg #19 #20 #22 #23 #24 #25 #26; D2-D5, D8, D10: svg #30 #31 #32 #33 #36 #38), house style, 400 px.

Whole bodies come from the posable Lynch skeleton (lynch_body.py); m09/body_main.py is the only group that puts its
defs on the page, so this file does NOT expose SHARED_DEFS.  The page states no stature: 1.75 m, so 1 cm =
LB.H_U / 175 body units (as m08/body_c.py).  The SLIP models (spring leg, COM mark) are drawn over the skeleton; every
number on a figure is computed here from the constants module09.html states (line numbers beside each constant).
The kit's standing foot-to-COM distance is 0.580 H = 1.01 m, which is the text's leg length L0 = 1.0 m (lines 693, 172).
"""
import math

import numpy as np

import house as H
import lynch_body as LB
from m05.body import finish, it
from m05.plots_prob import Plot, label as plabel, legend

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
CM = LB.H_U / 175.0                     # body units per cm (stature 1.75 m)
BOX = "#f7f4ef"
S0 = H.Scale(400, 400, display_w=400)   # dry-run scale for pose searches
STAT = 1.75                             # m, stature (the page states none)

# ---------------------------------------------------------------- numbers module09.html states
M, G, L0 = 70.0, 9.81, 1.0              # kg, m/s^2, m (lines 361, 693)
BW = M * G                              # N, body weight
K_LEG = 15000.0                         # N/m, effective leg stiffness (line 694; "k between about 11 and 19 kN/m", 144)
ALPHA0, VX0, VY0 = 70.0, 4.0, -0.7      # deg, m/s, m/s: Lab 1 jog touchdown (lines 362-364)
TC, TF = 0.20, 0.10                     # s, jog contact and flight time (lines 77, 696)
FR_RUN = 0.5                            # Froude number at which people switch to running (lines 162, 172, 699)
D_PUSH, F_PUSH = 0.40, 515.0            # m, N: representative push-off (line 218)
U_ACH, R_ACH = 31.0, 0.92               # J, resilience: Achilles energy per step (lines 234, 242)
H_DROP = 0.5                            # m, drop height (lines 296, 298, 406)
M_IMP, V_IMP, KC_STIFF, KC_SOFT = 8.0, 1.0, 200e3, 40e3     # kg, m/s, N/m (line 316)


def close(v, ref, tol):
    assert abs(v - ref) <= tol * 1.0001, (v, ref)


def slip(k, alpha=ALPHA0, vx0=VX0, vy0=VY0, dt=1e-4):
    """Lab 1 (lines 339-358), line for line.  Rows: t, x, y, vx, vy, r, Fz  (foot at the origin, SI)."""
    a = math.radians(alpha)
    x, y, vx, vy, t = -L0 * math.cos(a), L0 * math.sin(a), vx0, vy0, 0.0
    rows = []
    while True:
        r = math.hypot(x, y)
        F = k * (L0 - r)
        ax, ay = F * x / r / M, F * y / r / M - G
        rows.append((t, x, y, vx, vy, r, F * y / r))
        vx, vy = vx + ax * dt, vy + ay * dt
        x, y = x + vx * dt, y + vy * dt
        t += dt
        if math.hypot(x, y) >= L0 and t > 5 * dt:
            break
        if y <= 0 or t > 2.0:
            break
    return np.array(rows)


for _k, _bw, _ms in ((11000, 2.1, 211), (26000, 3.6, 150)):                 # line 369
    _R = slip(_k)
    close(_R[:, 6].max() / BW, _bw, 0.05)
    close(_R[-1, 0] * 1000, _ms, 1.0)
RUN = slip(K_LEG)                                                           # the figures' stance (k = 15 kN/m)
PHI = np.degrees(np.arctan2(RUN[:, 2], RUN[:, 1]))                          # leg angle to the ground, 110 -> ~67 deg
I_MID = int(np.argmin(abs(PHI - 90.0)))
R_MID = RUN[I_MID, 5]                                                       # shortest leg, at midstance
close(RUN[:, 6].max() / BW, 2.6, 0.05)                                      # "peak near 2.6 body weights" (line 140)
close(RUN[-1, 4], 0.46, 0.01)                                               # takeoff vy 0.46 m/s (line 160)
Y_TD = L0 * math.sin(math.radians(ALPHA0))                                  # touchdown COM height, 0.940 m


def at_phi(phi):
    """The stance sample whose leg angle is closest to phi (deg)."""
    return RUN[int(np.argmin(abs(PHI - phi)))]


def energies(row, k=K_LEG):
    """(KE, PE, spring) in J at a stance sample: the three terms of (2.2), line 113."""
    t, x, y, vx, vy, r, _ = row
    return 0.5 * M * (vx * vx + vy * vy), M * G * y, 0.5 * k * (L0 - r) ** 2


E_TOT = sum(energies(RUN[0]))
close(max(sum(energies(q)) for q in RUN) - min(sum(energies(q)) for q in RUN), 0, 0.5)    # E constant to 0.5 J

# Lab 2 (lines 376-396)
_TP, _FPK = 0.30, 2.5
_t2 = np.linspace(0, _TP, 400)


def jump_profile(front):
    return 1.0 + (_FPK - 1.0) * np.sin(np.pi * (_t2 / _TP) ** front) ** 1.55


def jump_numbers(front):
    imp = float(np.trapezoid((jump_profile(front) - 1.0) * M * G, _t2))
    return imp, (imp / M) ** 2 / (2 * G)


IMP_SJ, H_SJ = jump_numbers(1.0)
IMP_CMJ, H_CMJ = jump_numbers(0.8)
close(H_SJ * 100, 30.0, 0.05)                    # line 220, 222
close(H_CMJ * 100, 32.0, 0.05)
close(IMP_SJ, 169.9, 0.05)                       # line 222
close(IMP_CMJ, 175.5, 0.05)
close(IMP_CMJ / IMP_SJ - 1, 0.033, 0.0005)
close(H_CMJ / H_SJ - 1, 0.067, 0.001)

# vertical jump (line 218): 515 N net over 0.40 m
V0 = math.sqrt(2 * F_PUSH * D_PUSH / M)
H_APEX = V0 * V0 / (2 * G)
close(V0, 2.4, 0.05)
close(H_APEX * 100, 30.0, 0.05)

# landing (lines 296, 406-414)
V_LAND = math.sqrt(2 * G * H_DROP)
close(V_LAND, 3.1, 0.05)


def f_avg(ds):
    """Prop 8.1: average landing force, N."""
    return 0.5 * M * V_LAND ** 2 / ds + BW


for _ds, _bw in ((0.05, 11.0), (0.15, 4.3), (0.30, 2.7), (0.45, 2.1)):     # line 414
    close(f_avg(_ds) / BW, _bw, 0.05)
close(f_avg(0.40) / BW, 2.25, 0.005)                                        # "about 2" (lines 296, 298)

# impact (line 316)
def impact(kc):
    om = math.sqrt(kc / M_IMP)
    fp = V_IMP * math.sqrt(kc * M_IMP)
    return om, fp, (math.pi / 2) / om, 2 / math.pi * V_IMP * kc / BW


for _kc, _fp, _bw, _tr, _rate in ((KC_STIFF, 1265, 1.8, 9.9, 185), (KC_SOFT, 566, 0.8, 22.2, 37)):
    _om, _f, _t, _rt = impact(_kc)
    close(_f, _fp, 1.0)
    close(_f / BW, _bw, 0.05)
    close(_t * 1000, _tr, 0.05)
    close(_rt, _rate, 0.5)

# tendon (lines 234, 242)
E_RET, E_LOSS = R_ACH * U_ACH, (1 - R_ACH) * U_ACH
close(E_RET, 28.5, 0.05)
close(E_LOSS, 2.5, 0.05)
close(2 * U_ACH, 62.0, 0.05)
close(2 / (1 - R_ACH), 25.0, 0.05)

# Froude (lines 162, 168, 172)
V_FR1 = math.sqrt(G * L0)
close(V_FR1, 3.1, 0.05)


# ---------------------------------------------------------------- drawing helpers (idiom of m08/body_c.py)
def sub(t, s, size="label"):
    return H.sub(t, s, size)


def lab(s, x, y, text, size="label", fill=I["primary"], anchor="start", extra=""):
    return H.label(s, x, y, text, size, fill, anchor, extra)


def floor(s, x0, x1, y, hatch=True):
    o = [H.line(s, x0, y, x1, y, I["axis"], "axis")]
    if hatch:
        n = int((x1 - x0) / s(10))
        o += [H.line(s, x0 + s(10) * i + s(8), y + s(1), x0 + s(10) * i, y + s(7), I["rule"], "leader")
              for i in range(n)]
    return "".join(o)


def credit(s, vb, extra=""):
    """Lynch credit at the bottom of the viewBox, wrapped to its width (the wrap rule of LB.credit)."""
    w = vb[2] - s(12)
    t = H.ATTRIBUTION["by"].format(
        author="Patrick J. Lynch, medical illustrator",
        title="Skeleton lateral.svg” and “Skeleton whole body ant lat views.svg", licence="CC BY 2.5",
        changes="Recoloured, split into segments and reposed; arms from the anterior view." + extra)
    n = max(20, int(w / (s(H.PX["credit"]) * 0.47)))
    lines, cur = 0, ""
    for wd in t.split():
        if cur and len(cur) + 1 + len(wd) > n:
            lines, cur = lines + 1, wd
        else:
            cur = (cur + " " + wd).strip()
    y = vb[1] + vb[3] - s(6) - lines * s(H.PX["credit"]) * 1.25
    return LB.credit(s, vb[0] + s(6), y, width=w, extra=extra)


def credit_lines(s, vb, extra=""):
    """Number of credit lines (for layout)."""
    w = vb[2] - s(12)
    t = H.ATTRIBUTION["by"].format(author="Patrick J. Lynch, medical illustrator",
                                   title="Skeleton lateral.svg” and “Skeleton whole body ant lat views.svg",
                                   licence="CC BY 2.5",
                                   changes="Recoloured, split into segments and reposed; arms from the anterior view."
                                   + extra)
    n = max(20, int(w / (s(H.PX["credit"]) * 0.47)))
    k, cur = 0, ""
    for wd in t.split():
        if cur and len(cur) + 1 + len(wd) > n:
            k, cur = k + 1, wd
        else:
            cur = (cur + " " + wd).strip()
    return k + 1


def ext(s, x0, y0, x1, y1):
    """Dashed construction line (reference grey)."""
    return H.line(s, x0, y0, x1, y1, O["dim"], "ref", H.DASH_REF)




def dim_v(s, p, x, y0, y1, text, side=1, size="label2", meaning="geometry", anchor=None):
    """Vertical dimension arrow at x from y0 to y1, text beside it (side +1 right, -1 left)."""
    o = [H.arrow(s, p, x, y0, x, y1, meaning, both=True)]
    o.append(lab(s, x + side * s(6), (y0 + y1) / 2 + s(4), text, size,
                 anchor=anchor or ("start" if side > 0 else "end")))
    return "".join(o)


def dvert(s, p, x, y0, y1, meaning="geometry"):
    """Vertical dimension from y0 to y1: arrowheads when long enough, end ticks when short."""
    if abs(y1 - y0) > s(26):
        return H.arrow(s, p, x, y0, x, y1, meaning, both=True)
    w = "geom" if meaning in ("geometry", "dim") else "force"
    return (H.line(s, x, y0, x, y1, O[meaning], w) + H.line(s, x - s(4), y0, x + s(4), y0, O[meaning], w)
            + H.line(s, x - s(4), y1, x + s(4), y1, O[meaning], w))


def arc(s, p, cx, cy, r, a0, a1, meaning="force", head=True):
    """Arc on a circle about (cx, cy), from screen angle a0 to a1 (deg, + = clockwise), arrowhead at a1."""
    q = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))  # noqa: E731
    (x0, y0), (x1, y1) = q(a0), q(a1)
    sweep = 1 if a1 > a0 else 0
    big = 1 if abs(a1 - a0) > 180 else 0
    mk = f' marker-end="url(#{p}a_{meaning})"' if head else ""
    w = "geom" if meaning in ("geometry", "dim") else "force"
    return (f'<path d="M{x0:.2f},{y0:.2f} A{r:.2f},{r:.2f} 0 {big} {sweep} {x1:.2f},{y1:.2f}" fill="none" '
            f'stroke="{O[meaning]}" stroke-width="{s(H.PX[w]):.2f}"{mk}/>')




def poly(s, pts, col, w="geom", dash=None):
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    return (f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="none" stroke="{col}" '
            f'stroke-width="{s(H.PX[w]):.2f}" stroke-linejoin="round"{da}/>')


def dot(s, x, y, col, r=4.5):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{col}" stroke="#fff" '
            f'stroke-width="{s(1.5):.2f}"/>')


def lines(s, x, y, rows, size="label2", anchor="start", lead=1.35):
    return "".join(lab(s, x, y + i * s(H.PX[size]) * lead, t, size, anchor=anchor) for i, t in enumerate(rows))




def coil(s, a, b, n=8, amp=6.0, lead=0.12, col=I["primary"], w=2.2):
    """A spring symbol from a to b as a <path> (schematic: the leg acts as a spring)."""
    L = math.dist(a, b)
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    nx, ny = -uy, ux
    pts = [a]
    for k in range(2 * n + 1):
        t = lead + (1 - 2 * lead) * k / (2 * n)
        side = 0 if k in (0, 2 * n) else (1 if k % 2 else -1)
        pts.append((a[0] + ux * L * t + nx * amp * side, a[1] + uy * L * t + ny * amp * side))
    pts.append(b)
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{s(w):.2f}" stroke-linejoin="round" '
            f'stroke-linecap="round"/>')


def vb_h(bottom, extra=""):
    """viewBox height that leaves room under `bottom` for the wrapped credit (u = 1 at 400 px)."""
    s = H.Scale(400, 400, display_w=400)
    return int(math.ceil(bottom + 10 + credit_lines(s, (0, 0, 400, 400), extra) * H.PX["credit"] * 1.25 + 6))


def VBs(h):
    vb = (0, 0, 400, h)
    return vb, H.Scale(400, h, display_w=400, max_h=H.MAX_DISPLAY_H_BODY)




def fmtn(v, nd=1):
    return f"{v:.{nd}f}".replace("-", "−")


# ---------------------------------------------------------------- body placement and pose fitting
def foot_x(J, org):
    """x of the SLIP foot origin: the mid-foot, the heel or the toe of the near foot."""
    return (J["heel"][0] + J["toe"][0]) / 2 if org == "mid" else J[org][0]


def place(p, s, P, ox, fy, hf, org="mid", **kw):
    """Draw pose P with stature hf so that the foot origin (see foot_x) is at x = ox and the floor at y = fy.
    Returns (svg, J, u) with u = figure units per metre; J["O"] = the foot origin (ox, fy)."""
    _, J0 = LB.draw(p, s, P, 0, 0, hf, **kw)
    dx = ox - foot_x(J0, org)
    dy = fy - J0["floor_y"]
    svg, J = LB.draw(p, s, P, dx, dy, hf, **kw)
    J["O"] = (ox, fy)
    J["_xy"] = (dx, dy)
    return svg, J, hf / STAT


def com_rel(P, hf=300.0, org="mid"):
    """(COM x from the foot origin, COM height above the floor) of pose P in metres."""
    _, J = LB.draw("", S0, P, 0, 0, hf)
    u = hf / STAT
    return (J["com"][0] - foot_x(J, org)) / u, (J["floor_y"] - J["com"][1]) / u


def fit_pose(make, x0, target, org="mid"):
    """Solve the two pose parameters (a, b) so that the COM sits at target = (dx, h) metres from the foot origin."""
    def res(v):
        dx, h = com_rel(make(*v), org=org)
        return [dx - target[0], h - target[1]]
    v = np.array(x0, dtype=float)                       # Newton with a finite-difference Jacobian (numpy only)
    for _ in range(60):
        r = np.array(res(v))
        if np.max(np.abs(r)) < 1e-9:
            break
        jac = np.empty((2, 2))
        for j in range(2):
            dv = np.zeros(2)
            dv[j] = 1e-4
            jac[:, j] = (np.array(res(v + dv)) - np.array(res(v - dv))) / 2e-4
        v = v - np.linalg.solve(jac, r)
    r = res(v)
    assert abs(r[0]) < 0.004 and abs(r[1]) < 0.004, (v, r)
    return make(*v), v


def run_pose(hip, knee, swing=105.0):
    """Running stance, side view: pelvis 10, trunk -2, foot flat, swing knee 105 deg, elbows 95 (m06/body.py RUN)."""
    return LB.pose(pelvis=10, trunk=-2, near=dict(hip=hip, knee=knee, shoulder=-25, elbow=95),
                   far=dict(hip=15, knee=swing, contact=None, ankle=-15, shoulder=30, elbow=95),
                   anchor=("heel", "near"))


def seg_pt(J, P, seg_name, far, local):
    """A point given in a segment's local art units -> figure units (pose P drawn with joints J, facing right)."""
    for name, o_, th, sc, mirror, f in P.segs:
        if name == seg_name and f == far:
            q = LB.add(o_, LB.rot(local, th))
            k = J["scale"]
            ax, ay = P.anchor
            x0, y0 = J["_xy"]
            return (x0 + k * (q[0] - ax), y0 + k * (q[1] - ay))
    raise KeyError(seg_name)


def bisect(f, lo, hi, n=50):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


# ================================================================ pose factories shared by several figures
def ds_pose(L, kf=20.0, near_arm=(-20, 10), far_arm=(20, 20)):
    """Walking double support (m08/body_c.py ds_pose): leading (near) heel down, trailing (far) toe down, the
    contacts L metres apart.  Leading thigh at asin(L / 2 L0) forward of vertical; the trailing thigh angle is solved
    so that trailing toe to leading heel = L."""
    a = math.degrees(math.asin(L / (2 * L0)))

    def mk(b):
        return LB.pose(near=dict(hip=a, knee=3, contact=None, ankle=0, shoulder=near_arm[0], elbow=near_arm[1]),
                       far=dict(hip=-b, knee=kf, contact="toe", shoulder=far_arm[0], elbow=far_arm[1]),
                       anchor=("heel", "near"))

    def err(b):
        try:
            _, J = LB.draw("", S0, mk(b), 0, 0, LB.H_U)
        except AssertionError:                              # trailing foot cannot reach: step too long
            return 1e9
        return (J["heel"][0] - J["toe_far"][0]) / CM - 100 * L

    b = bisect(err, 2.0, 40.0)
    close(err(b), 0, 0.05)
    return mk(b)


def flight_pose():
    """Running, mid-flight: lead leg reaching forward, trailing leg folded, elbows at 90 deg (m08/body_c.py)."""
    return LB.pose(pelvis=0, trunk=8, near=dict(hip=40, knee=25, contact=None, ankle=5, shoulder=-35, elbow=90),
                   far=dict(hip=-15, knee=85, contact=None, ankle=-15, shoulder=35, elbow=90), anchor=("hip", "near"))


def walk_pose(h, k):
    """Walking midstance: stance (near) leg under the hip, the far leg swinging through (LB.POSES gait_midstance)."""
    return LB.pose(near=dict(hip=h, knee=k, shoulder=0, elbow=10),
                   far=dict(hip=30, knee=60, contact=None, ankle=15, shoulder=5, elbow=15), anchor=("heel", "near"))


def squat_pose(h, lean, arms=40.0):
    """Two-legged squat, feet flat: hip flexion h, knee flexion 1.15 h, trunk leaned `lean` deg about the hips."""
    leg = dict(hip=h, knee=min(1.15 * h, 150.0), shoulder=arms, elbow=15)
    return LB.pose(pelvis=lean * 0.55, trunk=lean * 0.45, near=dict(leg), far=dict(leg), anchor=("heel", "near"))


def squat_to(h_com, dx=0.03):
    """Squat pose whose COM is at height h_com (m) and dx (m) ahead of the mid-foot: solve hip flexion and lean."""
    P, v = fit_pose(lambda h, ln: squat_pose(h, ln), (60.0, 30.0), (dx, h_com))
    return P


def timeline(s, x0, w, y, duty, name):
    """Footfall bars over one stride (m08/body_c.py): two feet, each in stance for `duty` of the stride, half a
    stride apart, and the strip below where both are down (blue) or neither is (orange)."""
    o, h = [], s(7)
    for k, (off, foot) in enumerate(((0.0, "R"), (0.5, "L"))):
        yy = y + k * (h + s(4))
        o.append(f'<rect x="{x0:.2f}" y="{yy:.2f}" width="{w:.2f}" height="{h:.2f}" fill="#fff" '
                 f'stroke="{I["rule"]}" stroke-width="{s(0.8):.2f}"/>')
        for a0, a1 in ((off, min(off + duty, 1.0)), (0.0, max(off + duty - 1.0, 0.0))):
            if a1 > a0:
                o.append(f'<rect x="{x0 + a0 * w:.2f}" y="{yy:.2f}" width="{(a1 - a0) * w:.2f}" height="{h:.2f}" '
                         f'fill="{I["secondary"]}"/>')
        o.append(lab(s, x0 - s(4), yy + h, foot, "tick", I["secondary"], anchor="end"))
    yb = y + 2 * h + s(6)
    if duty > 0.5:
        spans, col = [(0.0, duty - 0.5), (0.5, duty)], SER[1]
    else:
        spans, col = [(duty, 0.5), (0.5 + duty, 1.0)], SER[2]
    for a0, a1 in spans:
        o.append(f'<rect x="{x0 + a0 * w:.2f}" y="{yb:.2f}" width="{(a1 - a0) * w:.2f}" height="{s(4):.2f}" '
                 f'fill="{col}"/>')
    o.append(lab(s, x0 + w / 2, yb + s(19), name, "label2", anchor="middle"))
    return "".join(o)


BETA_RUN = TC / (2 * (TC + TF))                              # Prop 1.2, line 87
close(BETA_RUN, 1 / 3, 1e-9)                                 # lines 77, 697
BETA_WALK = 0.62                                             # design value > 1/2 (Module 8: 62 % of the stride)
V_Y_JOG = 0.9                                                # m/s, representative takeoff (line 160)


# ================================================================ svg #19  C1 walk: a foot always down; run: flight
def fig19():
    p = "m9f19_"
    HF, fy = 215.0, 292.0
    VB, s = VBs(vb_h(fy + 118))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    u = HF / STAT
    o.append(floor(s, 8, 392, fy))
    Pw = ds_pose(0.68)
    _, Jw0, _ = place(p, s, Pw, 0, fy, HF)
    body, Jw, _ = place(p, s, Pw, 108.0 - ((Jw0["heel"][0] + Jw0["toe_far"][0]) / 2 - Jw0["O"][0]), fy, HF)
    o.append(body)
    for q in (Jw["heel"], Jw["toe_far"]):
        o.append(dot(s, q[0], fy, SER[1]))
    Pr = flight_pose()
    _, Jr0 = LB.draw(p, s, Pr, 0, 0, HF)
    clear = (V_Y_JOG ** 2 / (2 * G)) * u                      # apex of the jog's flight above takeoff (line 160)
    low = max(Jr0["heel"][1], Jr0["toe"][1], Jr0["heel_far"][1], Jr0["toe_far"][1])
    xr = 296.0 - (Jr0["bbox"][0] + Jr0["bbox"][2]) / 2
    yr = fy - clear - low
    body2, Jr = LB.draw(p, s, Pr, xr, yr, HF)
    o.append(body2)
    o.append(lab(s, 10, 22, "walk"))
    o.append(lines(s, 10, 22 + s(17), ["one foot always down;", "both down at the exchange", "(double support)"]))
    o.append(lab(s, 392, 22, "run", anchor="end"))
    o.append(lines(s, 392, 22 + s(17), ["a flight phase: neither", "foot on the ground",
                                        f'{it("t")}{sub("f", s, "label2")} > 0, here {TF:.2f} s'], anchor="end"))
    ty = fy + s(52)
    o.append(lab(s, 30, ty - s(8), "one stride: when each foot (R, L) is down", "tick", I["secondary"]))
    o.append(timeline(s, 30, 150, ty, BETA_WALK, f'{it("β")} > ½: double support'))
    tc, tf = f'{it("t")}{sub("c", s, "label2")}', f'{it("t")}{sub("f", s, "label2")}'
    o.append(timeline(s, 236, 150, ty, BETA_RUN, f'{it("β")} = {tc}/2({tc}+{tf}) = ⅓: flight'))
    o.append(credit(s, VB))
    aria = ("Left, a walking skeleton (Lynch art) at the exchange between steps, both feet on the ground (blue "
            "dots): one foot is always down and for a moment both are, double support; its duty factor is above one "
            "half. Right, a runner in mid-flight, neither foot on the ground. Below, one stride of foot contacts: "
            "walking keeps each foot down more than half the stride, so the contacts overlap (blue); running keeps "
            "each foot down less than half, so there are gaps (orange). With contact time 0.20 s and flight time "
            "0.10 s the duty factor is one third.")
    return finish(VB, aria, s, o)


# ================================================================ svg #20  C2 run: COM lowest; walk: COM highest
def fig20():
    p = "m9f20_"
    HF, fy = 230.0, 318.0
    VB, s = VBs(vb_h(fy + 58))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    u = HF / STAT                                             # units per metre
    # run at midstance: COM straight above the mid-foot, at the shortest SLIP leg (k = 15 kN/m, Lab 1)
    Pr, _ = fit_pose(run_pose, (25.0, 55.0), (0.0, R_MID))
    xr, xw = 118.0, 270.0
    body_r, Jr, _u = place(p, s, Pr, xr, fy, HF)
    Pw, _ = fit_pose(walk_pose, (0.0, 8.0), (0.0, L0))
    body_w, Jw, _u = place(p, s, Pw, xw, fy, HF)
    # the walker's COM: straight leg of length L0 under it (kit COM 1.01 m, text L0 = 1.0 m)
    o.append(floor(s, 8, 392, fy))
    o.append(ext(s, 8, fy - Y_TD * u, 392, fy - Y_TD * u))
    o.append(body_r)
    o.append(body_w)
    # COM paths over the same stance: run = SLIP (Lab 1), walk = vault on a circle of radius L0
    px, py = RUN[:, 1], RUN[:, 2]
    o.append(poly(s, [(xr + a * u, fy - b * u) for a, b in zip(px[::40], py[::40])], O["geometry"], "curve"))
    xs = np.linspace(px[0], px[-1], 40)
    o.append(poly(s, [(xw + a * u, fy - math.sqrt(L0 * L0 - a * a) * u) for a in xs], O["geometry"], "curve"))
    # run: spring leg from the foot to the COM; walk: rigid strut
    cr = (xr, fy - R_MID * u)
    cw = (xw, fy - L0 * u)
    o.append(coil(s, (xr, fy), cr, n=7, amp=s(5.5)))
    o.append(H.line(s, xw, fy, cw[0], cw[1], O["force"], "force"))
    o.append(H.com_mark(s, *cr))
    o.append(H.com_mark(s, *cw))
    o.append(dot(s, xr, fy, I["primary"], 3.5))
    o.append(dot(s, xw, fy, I["primary"], 3.5))
    # labels
    o.append(lab(s, 8, 22, "run"))
    o.append(lines(s, 8, 22 + s(17), ["COM lowest at midstance:", "leg spring compressed",
                                      f'({it("k")}{sub("leg", s, "label2")} = 15 kN/m)']))
    o.append(lab(s, 392, 22, "walk", anchor="end"))
    o.append(lines(s, 392, 22 + s(17), ["COM highest at midstance:", "stiff leg, vault"], anchor="end"))
    o.append(dim_v(s, p, xr - s(60), fy, cr[1], f"{fmtn(R_MID, 2)} m", side=-1))
    o.append(dim_v(s, p, xw + s(62), fy, cw[1], f"{fmtn(L0, 2)} m", side=1))
    o.append(lab(s, xr, fy + s(30), "midstance", "label2", anchor="middle"))
    o.append(lab(s, xw, fy + s(30), "midstance", "label2", anchor="middle"))
    o.append(lab(s, 8, fy + s(50), f"dashed: the COM height at touchdown, {fmtn(Y_TD, 2)} m, both",
                 "tick", I["secondary"]))
    o.append(credit(s, VB))
    aria = ("Two side views of the Lynch skeleton at midstance with the point-mass model drawn over each. Left, a "
            "runner: the leg is a spring (dark coil) from the foot to the centre of mass, compressed to "
            f"{R_MID:.2f} m, so the centre of mass is at its lowest; the blue curve is its path over stance from the "
            f"SLIP integration of Lab 1 (k = 15 kN/m), {Y_TD:.2f} m at touchdown, {R_MID:.2f} m at midstance. Right, a "
            "walker: the stiff leg (red line) is 1.00 m, the centre of mass vaults on a circular arc of that radius "
            f"and is at its highest, 1.00 m, against the same {Y_TD:.2f} m at touchdown.")
    return finish(VB, aria, s, o)


# ================================================================ svg #22  C4 k_leg is a whole-limb stiffness
FOOT = dict(heel=(-9.5, 26.0), ach=(-19.5, 10.0))             # foot-local art units (m06/body.py, grid read)
SHANK_ACH = (-40.0, 150.0)                                    # shank-local: calf-tendon junction (m06/body.py)


def fig22():
    p = "m9f22_"
    HF, fy = 290.0, 336.0
    VB, s = VBs(vb_h(fy + 108))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    u = HF / STAT
    Pr, _ = fit_pose(run_pose, (25.0, 55.0), (0.0, R_MID))
    ox = 214.0
    body, J, _ = place(p, s, Pr, ox, fy, HF)
    o.append(floor(s, 8, 392, fy))
    o.append(body)
    cx, cy = ox, fy - R_MID * u
    o.append(coil(s, (ox, fy), (cx, cy), n=8, amp=s(7.0), w=2.6))
    o.append(H.com_mark(s, cx, cy))
    o.append(dot(s, ox, fy, I["primary"], 3.5))
    # the parts of the limb that the one number lumps together: numbered marks, key below
    heel = seg_pt(J, Pr, "lat_foot", False, FOOT["heel"])
    ach = seg_pt(J, Pr, "lat_foot", False, FOOT["ach"])
    calf = seg_pt(J, Pr, "lat_shank", False, SHANK_ACH)
    kn, hp = J["knee"], J["hip"]
    o.append(H.line(s, ach[0], ach[1], calf[0], calf[1], O["geometry"], "geom", H.DASH_LOA))
    for n, q, (dx, dy) in ((1, ((ach[0] + calf[0]) / 2, (ach[1] + calf[1]) / 2), (-62, -22)),
                           (2, heel, (-46, -8)), (3, kn, (46, 14)), (4, hp, (50, -14))):
        bx, by = q[0] + s(dx), q[1] + s(dy)
        o.append(H.line(s, q[0], q[1], bx, by, I["secondary"], "leader"))
        o.append(dot(s, q[0], q[1], I["primary"], 2.6))
        o.append(f'<circle cx="{bx:.2f}" cy="{by:.2f}" r="{s(9):.2f}" fill="#fff" stroke="{I["primary"]}" '
                 f'stroke-width="{s(1.2):.2f}"/>')
        o.append(f'<text x="{bx:.2f}" y="{by + s(4.5):.2f}" font-size="{s(13):.2f}" fill="{I["primary"]}" '
                 f'text-anchor="middle">{n}</text>')
    kl = f'{it("k")}{sub("leg", s)}'
    o.append(lab(s, 8, 22, f"{kl}: one effective stiffness for the whole limb"))
    o.append(lines(s, 8, 22 + s(18), [f"≈ {K_LEG / 1000:.0f} kN/m; the dark coil is its model: the leg is",
                                      f"{fmtn(L0 - R_MID, 2)} m shorter than its {fmtn(L0, 1)} m rest length at midstance"]))
    o.append(lines(s, 8, fy + s(32), [f"{kl} lumps together:",
                                      f"1  the Achilles tendon (dashed blue): a large part, not all",
                                      "2  the heel pad",
                                      "3  active muscle holding the knee and the hip",
                                      "4  joint geometry: the angles that set the lever arms"]))
    o.append(credit(s, VB))
    aria = ("A runner at midstance, side view (Lynch skeleton art), with the SLIP leg drawn over it: one dark coil from "
            "the foot to the centre of mass, the whole-limb spring of stiffness k leg, about 15 kN/m, shortened by "
            "0.12 m from the 1.0 m rest length. Leaders name what the one number lumps together: the Achilles tendon "
            "(dashed blue, a large contributor but only one), the heel pad, the active muscles holding the knee and "
            "hip, and the joint geometry that sets the lever arms. So k leg is an effective whole-limb stiffness, "
            "not the stiffness of the Achilles tendon.")
    return finish(VB, aria, s, o)


# ================================================================ svg #23  C5 the walking ceiling Fr <= 1
def vault_body(p, s, ox, fy, HF):
    """Walker at midstance on a straight stance leg of length L0 (COM straight above the mid-foot)."""
    Pw, _ = fit_pose(walk_pose, (0.0, 8.0), (0.0, L0))
    return place(p, s, Pw, ox, fy, HF)


def vault_arc(s, ox, fy, u, half=0.62):
    xs = np.linspace(-half, half, 41)
    return poly(s, [(ox + a * u, fy - math.sqrt(L0 * L0 - a * a) * u) for a in xs], O["geometry"], "geom",
                H.DASH_REF)


def fig23():
    p = "m9f23_"
    HF, fy = 200.0, 262.0
    VB, s = VBs(vb_h(fy + 62))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    u = HF / STAT
    Lw = 64.0                                                  # px of arrow for one body weight
    o.append(floor(s, 8, 392, fy))
    for ox, fr in ((100.0, FR_RUN), (298.0, 1.0)):
        v = math.sqrt(fr * G * L0)
        body, J, _ = vault_body(p, s, ox, fy, HF)
        o.append(body)
        o.append(vault_arc(s, ox, fy, u))
        cy = fy - L0 * u
        o.append(H.line(s, ox, fy, ox, cy, O["force"], "force"))
        o.append(H.com_mark(s, ox, cy))
        o.append(dot(s, ox, fy, I["primary"], 3.5))
        o.append(H.arrow(s, p, ox + s(24), cy, ox + s(24) + s(40), cy, "geometry"))
        o.append(lab(s, ox + s(24) + s(20), cy - s(7), f'{it("v")} = {v:.1f} m/s', "label2", anchor="middle"))
        o.append(H.arrow(s, p, ox - s(26), cy - s(4), ox - s(26), cy - s(4) + Lw, "load"))
        o.append(lab(s, ox - s(30), cy + s(34), f'{it("mg")}', "label2", anchor="end"))
        if fr < 1:
            L = (1 - fr) * Lw
            o.append(H.arrow(s, p, ox + s(34), fy - s(1), ox + s(34), fy - L, "reaction"))
            o.append(lab(s, ox + s(40), fy - L / 2 - s(4), f'{it("F")}{sub("z", s, "label2")}', "label2"))
            o.append(lab(s, ox + s(40), fy - L / 2 + s(11), f"= {1 - fr:.1f} {it('mg')}", "label2"))
        else:
            o.append(lab(s, ox + s(10), fy - s(10), f'{it("F")}{sub("z", s, "label2")} = 0', "label2"))
        o.append(lab(s, ox, 22, f'Fr = {fr:g}', "label", anchor="middle"))
    o.append(lines(s, 100, 22 + s(18), ["a vault: the ground", "still pushes up"], anchor="middle"))
    o.append(lines(s, 298, 22 + s(18), ["the ceiling: nothing holds", "the COM on the arc"], anchor="middle"))
    o.append(lines(s, 200, fy + s(30), [f'{it("F")}{sub("z", s, "label2")} = {it("mg")}(1 − Fr) ≥ 0 only if '
                                        f'Fr = {it("v")}² / ({it("g")}{it("L")}{sub("0", s, "label2")}) ≤ 1: '
                                        f'{it("v")} ≤ {V_FR1:.1f} m/s for a {L0:.0f} m leg',
                                        "people switch to running earlier, near Fr ≈ 0.5"], anchor="middle"))
    o.append(credit(s, VB))
    aria = ("Two walkers at midstance (Lynch skeleton art) vaulting over a stiff leg of length 1.0 m, the centre of "
            "mass on a dashed circular arc of that radius. Left, Froude number 0.5, speed 2.2 m/s: the weight mg points "
            "down and the ground reaction F z = mg(1 - Fr) = 0.5 mg points up. Right, Froude number 1, speed 3.1 m/s: "
            "the ground reaction is zero, nothing holds the centre of mass on the arc, and any faster the walker "
            "must run. Walking needs Fr no larger than 1; people switch to running near Fr 0.5.")
    return finish(VB, aria, s, o)


# ================================================================ svg #33  D5 the vault forces and the Froude ceiling
def fig33():
    p = "m9f33_"
    HF, fy = 250.0, 300.0
    VB, s = VBs(vb_h(fy + 20))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    u = HF / STAT
    Lw = 80.0
    fr = FR_RUN
    v = math.sqrt(fr * G * L0)
    ox = 104.0
    o.append(floor(s, 8, 392, fy))
    body, J, _ = vault_body(p, s, ox, fy, HF)
    o.append(body)
    o.append(vault_arc(s, ox, fy, u, 0.7))
    cy = fy - L0 * u
    o.append(H.line(s, ox, fy, ox, cy, O["dim"], "ref", H.DASH_REF))
    o.append(H.com_mark(s, ox, cy))
    o.append(dot(s, ox, fy, I["primary"], 3.5))
    o.append(H.arrow(s, p, ox, cy, ox + s(60), cy, "geometry"))
    o.append(lab(s, ox + s(64), cy - s(6), f'{it("v")}', "label2"))
    # weight at the COM; the ground force at the foot; the net downward force the circle needs
    o.append(H.arrow(s, p, ox - s(26), cy, ox - s(26), cy + Lw, "load"))
    o.append(lab(s, ox - s(30), cy + Lw + s(14), f'{it("mg")}', "label2", anchor="end"))
    o.append(H.arrow(s, p, ox + s(26), cy, ox + s(26), cy + fr * Lw, "dim"))
    o.append(lab(s, ox + s(32), cy + fr * Lw + s(14), f'{it("m")}{it("v")}² / {it("L")}{sub("0", s, "label2")}',
                 "label2"))
    o.append(H.arrow(s, p, ox + s(26), fy - s(1), ox + s(26), fy - (1 - fr) * Lw, "reaction"))
    o.append(lab(s, ox + s(32), fy - (1 - fr) * Lw / 2 + s(4), f'{it("F")}{sub("z", s, "label2")}', "label2"))
    o.append(dim_v(s, p, ox - s(56), fy, cy, f'{it("L")}{sub("0", s, "label2")}', side=-1))
    xr = 206.0
    L0s = f"{it('L')}{sub('0', s, 'label2')}"
    Fz = f"{it('F')}{sub('z', s, 'label2')}"
    rows = [("COM on a circle, radius " + L0s + ",", 0), ("so its acceleration is", 0),
            (f"{it('v')}² / {L0s}, toward the foot", 0), ("(downward)", 0.7),
            ("Newton, vertical:", 0),
            (f"{it('m')}(−{it('v')}² / {L0s}) = {Fz} − {it('mg')}", 0),
            (f"{Fz} = {it('mg')} − {it('m')}{it('v')}² / {L0s}", 0),
            (f"     = {it('mg')}(1 − Fr)", 0),
            (f"Fr = {it('v')}² / ({it('g')}{L0s})", 0.7),
            (f"Fr = {fr:g}: {it('v')} = {v:.1f} m/s,", 0), (f"{Fz} = {1 - fr:.1f} {it('mg')}", 0.7),
            (f"{Fz} ≥ 0 (a foot only pushes)", 0), ("⇔ Fr ≤ 1", 0)]
    y = 30.0
    for txt, gap in rows:
        o.append(lab(s, xr, y, txt, "label2"))
        y += s(17.5) * (1 + gap)
    o.append(credit(s, VB))
    aria = ("A walker at midstance of a vault (Lynch skeleton art) at Froude number 0.5, speed 2.2 m/s, the centre of "
            "mass moving horizontally on a dashed circular arc of radius L0 = 1.0 m about the foot. Forces: weight mg "
            "down at the centre of mass, the ground reaction F z = mg(1 - Fr) up at the foot, and the net downward "
            "force m v squared over L0 that the circle needs, equal to mg minus F z. Newton's vertical law gives "
            "F z = mg(1 - Fr) with Fr = v squared over g L0; a foot only pushes, so F z is at least 0 exactly when "
            "Fr is at most 1.")
    return finish(VB, aria, s, o)


# ================================================================ SLIP overlays on a runner (svg #30, #31, #32)
def slip_body(p, s, ox, fy, hf, row, org="mid", x0=(40.0, 55.0)):
    """Runner drawn so that its COM sits at the SLIP state `row` (foot at the origin (ox, fy)).
    Returns (svg, J, u, (cx, cy)) with (cx, cy) the model COM in figure units."""
    P, _ = fit_pose(run_pose, x0, (row[1], row[2]), org=org)
    body, J, u = place(p, s, P, ox, fy, hf, org=org)
    return body, J, u, (ox + row[1] * u, fy - row[2] * u)


# ================================================================ svg #30  D2 SLIP in polar coordinates about the foot
def fig30():
    p = "m9f30_"
    HF, fy = 290.0, 340.0
    VB, s = VBs(vb_h(fy + 56))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    row = at_phi(100.0)
    t_, x, y, vx, vy, r, Fz = row
    phi = math.atan2(y, x)
    close(math.degrees(phi), 100.0, 0.1)
    Fs = K_LEG * (L0 - r)                                       # spring force on the mass, N
    ox = 196.0
    body, J, u, (cx, cy) = slip_body(p, s, ox, fy, HF, row)
    o.append(floor(s, 8, 392, fy))
    o.append(body)
    # ground line from the foot, the rest-length arc and the leg
    o.append(ext(s, ox, fy, ox + 150, fy))
    ang = [math.radians(a) for a in np.linspace(math.degrees(phi) + 14, math.degrees(phi) - 24, 20)]
    o.append(poly(s, [(ox + L0 * u * math.cos(a), fy - L0 * u * math.sin(a)) for a in ang], O["dim"], "ref", H.DASH_REF))
    o.append(coil(s, (ox, fy), (cx, cy), n=7, amp=s(6.0)))
    o.append(arc(s, p, ox, fy, s(46), 0, -math.degrees(phi), "geometry", head=False))
    o.append(lab(s, ox + s(52) * math.cos(phi / 2) - s(4), fy - s(52) * math.sin(phi / 2) + s(4), it("φ"), "label"))
    o.append(H.com_mark(s, cx, cy))
    o.append(dot(s, ox, fy, I["primary"], 3.5))
    # unit directions at the COM (screen: y down)
    rh = (math.cos(phi), -math.sin(phi))
    ph = (-math.sin(phi), -math.cos(phi))
    o.append(H.arrow(s, p, cx, cy, cx + rh[0] * s(40), cy + rh[1] * s(40), "dim"))
    o.append(lab(s, cx + rh[0] * s(40) - s(6), cy + rh[1] * s(40) - s(5), "radial", "label2", anchor="end"))
    o.append(H.arrow(s, p, cx, cy, cx + ph[0] * s(40), cy + ph[1] * s(40), "dim"))
    o.append(lab(s, cx + ph[0] * s(40) - s(5), cy + ph[1] * s(40) + s(14), "tangential", "label2", anchor="end"))
    kB = s(44)                                                  # px per body weight
    o.append(H.arrow(s, p, cx, cy, cx + rh[0] * Fs / BW * kB, cy + rh[1] * Fs / BW * kB, "force"))
    o.append(lab(s, cx + rh[0] * Fs / BW * kB + s(8), cy + rh[1] * Fs / BW * kB + s(4),
                 f'{it("k")}{sub("leg", s, "label2")}({it("L")}{sub("0", s, "label2")} − {it("r")})', "label2"))
    o.append(H.arrow(s, p, cx + s(26), cy, cx + s(26), cy + kB, "load"))
    o.append(lab(s, cx + s(32), cy + kB - s(2), it("mg"), "label2"))
    # r along the leg
    mx, my = (ox + cx) / 2, (fy + cy) / 2
    o.append(lab(s, mx + s(14), my + s(6), it("r"), "label"))
    o.append(lab(s, ox, fy + s(18), "foot = origin", "label2", anchor="middle"))
    o.append(lab(s, 8, 22, "SLIP stance, polar coordinates about the foot"))
    o.append(lines(s, 8, 22 + s(18), [f"the mass is at (r, φ): here r = {r:.2f} m, φ = {math.degrees(phi):.0f}°",
                                      f"(one instant of Lab 1: k = {K_LEG / 1000:.0f} kN/m, rest length "
                                      f"{it('L')}{sub('0', s, 'label2')} = {L0:.1f} m)"]))
    o.append(lines(s, 8, fy + s(34), [f"spring: {it('k')}{sub('leg', s, 'label2')}({it('L')}{sub('0', s, 'label2')} − "
                                      f"{it('r')}) along the leg",
                                      f"gravity: −{it('mg')} sin φ radial, −{it('mg')} cos φ tangential"], "tick"))
    o.append(credit(s, VB))
    aria = ("A runner early in stance (Lynch skeleton art) with the SLIP model drawn over it, in polar coordinates "
            f"about the foot at the origin: the mass is at distance r = {r:.2f} m along the leg (dark coil) and angle "
            f"phi = {math.degrees(phi):.0f} degrees from the ground, one instant of the Lab 1 stance at k = 15 kN/m. "
            "Two unit directions at the mass, radial along the leg and tangential across it. The spring force k leg "
            "times L0 minus r acts along the leg; gravity mg points down and projects as minus mg sin phi radially "
            "and minus mg cos phi tangentially.")
    return finish(VB, aria, s, o)


# ================================================================ svg #32  D4 the spring force and its vertical part
def fig32():
    p = "m9f32_"
    HF, fy = 270.0, 330.0
    VB, s = VBs(vb_h(fy + 40))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    i = int(np.argmin(abs(PHI - 75.0)))
    row = RUN[i]
    t_, x, y, vx, vy, r, Fz = row
    phi = math.atan2(y, x)
    Fs = K_LEG * (L0 - r)
    close(Fs * math.sin(phi), Fz, 1e-6)                          # (3.1) first form
    yd = (RUN[i + 1, 4] - RUN[i, 4]) / 1e-4                      # the integrator's own vertical acceleration
    close(M * (G + yd), Fz, 1e-6)                                # (3.1) second form
    ox = 96.0
    body, J, u, (cx, cy) = slip_body(p, s, ox, fy, HF, row)
    o.append(floor(s, 8, 392, fy))
    o.append(body)
    o.append(coil(s, (ox, fy), (cx, cy), n=7, amp=s(6.0), w=2.2))
    o.append(H.com_mark(s, cx, cy))
    o.append(dot(s, ox, fy, I["primary"], 3.5))
    kB = s(58)
    rh = (math.cos(phi), -math.sin(phi))
    fx, fyy = cx + rh[0] * Fs / BW * kB, cy + rh[1] * Fs / BW * kB
    o.append(H.arrow(s, p, cx, cy, fx, fyy, "force"))
    o.append(lab(s, fx + s(6), fyy + s(2), f'{it("k")}{sub("leg", s, "label2")}({it("L")}{sub("0", s, "label2")} − '
                 f'{it("r")})', "label2"))
    o.append(H.line(s, cx, cy, cx, fyy, I["rule"], "ref", extra=f'stroke-dasharray="{s(3):.1f} {s(3):.1f}"'))
    o.append(H.line(s, fx, fyy, cx, fyy, I["rule"], "ref", extra=f'stroke-dasharray="{s(3):.1f} {s(3):.1f}"'))
    o.append(arc(s, p, ox, fy, s(44), 0, -math.degrees(phi), "geometry", head=False))
    o.append(lab(s, ox + s(50), fy - s(30), it("φ"), "label"))
    o.append(H.arrow(s, p, cx + s(24), cy, cx + s(24), cy + kB, "load"))
    o.append(lab(s, cx + s(30), cy + kB * 0.6, it("mg"), "label2"))
    # the ground reaction at the foot: the vertical part of the spring force
    o.append(H.arrow(s, p, ox, fy - s(1), ox, fy - Fz / BW * kB, "reaction"))
    o.append(lab(s, ox - s(8), fy - Fz / BW * kB * 0.6, f'{it("F")}{sub("z", s, "label2")}', "label2", anchor="end"))
    o.append(lab(s, 8, 22, "the leg spring pushes along the leg;"))
    o.append(lab(s, 8, 22 + s(18), "the massless leg hands the force to the foot"))
    fz = f'{it("F")}{sub("z", s, "label2")}'
    o.append(lines(s, 226, 150, ["after midstance:", f"φ = {math.degrees(phi):.0f}°, r = {r:.2f} m",
                                 "spring force", f"  {Fs / 1000:.2f} kN = {Fs / BW:.2f} {it('mg')}",
                                 f"{fz} = {it('k')}({it('L')}{sub('0', s, 'label2')} − {it('r')}) sin φ",
                                 f"    = {Fz / 1000:.2f} kN = {Fz / BW:.2f} {it('mg')}",
                                 "", f"also {fz} = {it('m')}({it('g')} + {it('ÿ')}):",
                                 f"{it('ÿ')} = {yd:.1f} m/s²: {Fz / 1000:.2f} kN"]))
    o.append(credit(s, VB))
    aria = ("A runner just after midstance (Lynch skeleton art), the SLIP leg drawn over it as a dark coil from the foot "
            f"to the centre of mass, at leg angle phi = {math.degrees(phi):.0f} degrees and length r = {r:.2f} m. "
            f"The spring force k leg (L0 minus r) = {Fs / 1000:.2f} kN acts along the leg (red); its vertical part "
            f"(dashed projection) is the ground reaction F z = k leg (L0 - r) sin phi = {Fz / 1000:.2f} kN, "
            f"{Fz / BW:.2f} body weights, drawn upward at the foot because the massless leg carries it unchanged. "
            f"Newton's vertical law gives the same force, m(g + y double dot), with y double dot = {yd:.1f} m/s^2. "
            "Weight mg points down at the centre of mass.")
    return finish(VB, aria, s, o)


# ================================================================ svg #31  D3 the SLIP energy is conserved
def fig31():
    p = "m9f31_"
    HF, fy = 200.0, 236.0
    VB, s = VBs(vb_h(fy + 270))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    u = HF / STAT
    ox = 100.0
    Pr, _ = fit_pose(run_pose, (25.0, 55.0), (0.0, R_MID))
    body, J, _ = place(p, s, Pr, ox, fy, HF)
    o.append(floor(s, 8, 392, fy))
    o.append(body)
    o.append(coil(s, (ox, fy), (ox, fy - R_MID * u), n=7, amp=s(5.0)))
    o.append(H.com_mark(s, ox, fy - R_MID * u))
    o.append(dot(s, ox, fy, I["primary"], 3.5))
    L0s = f"{it('L')}{sub('0', s, 'label2')}"
    kl = f"{it('k')}{sub('leg', s, 'label2')}"
    o.append(lines(s, 200, 30, ["E = KE + PE + spring", "KE = ½m (speed)²", f"PE = {it('mg')}{it('y')}",
                                f"spring = ½{kl}({L0s} − {it('r')})²", "", "constant through stance:",
                                f"dE/dt = 0 (Prop 2.2)", f"here E = {E_TOT:.0f} J (Lab 1)"]))
    # states: touchdown, midstance, takeoff, flight apex
    t_, x, y, vx, vy, r, Fz = RUN[-1]
    y_apex = y + vy * vy / (2 * G)
    states = [("touchdown", energies(RUN[0])), ("midstance", energies(RUN[I_MID])), ("takeoff", energies(RUN[-1])),
              ("flight apex", (0.5 * M * vx * vx, M * G * y_apex, 0.0))]
    for nm, e in states:
        close(sum(e), E_TOT, 1.0)
    top = 300.0
    base = 458.0
    pl = Plot(s, (62, top, 388, base), (0, 4), (0, 1400))
    o.append(pl.axes([], [(v, f"{v}") for v in (0, 400, 800, 1200)], "instants of one stride", "energy (J)",
                     grid=(400, 800, 1200)))
    cols = (SER[0], SER[1], SER[2])                              # KE red, PE blue, spring orange (as m08 fig19)
    bw = 0.62
    pts = []
    for k, (nm, e) in enumerate(states):
        xc = k + 0.5
        lo = 0.0
        for val, col in zip(e, cols):
            if val < 0.5:
                continue
            y0, y1 = pl.Y(lo), pl.Y(lo + val)
            o.append(f'<rect x="{pl.X(xc - bw / 2):.2f}" y="{y1:.2f}" width="{pl.X(bw) - pl.X(0):.2f}" '
                     f'height="{y0 - y1:.2f}" fill="{col}" stroke="#fff" stroke-width="{s(1.2):.2f}"/>')
            if y0 - y1 > s(20):
                o.append(plabel(s, pl.X(xc), (y0 + y1) / 2 + s(4.5), f"{val:.0f}", "tick", I["primary"], "middle"))
            elif col == SER[2]:
                o.append(plabel(s, pl.X(xc + bw / 2) + s(4), y1 + s(17), f"{val:.0f}", "tick", I["primary"]))
            lo += val
        o.append(plabel(s, pl.X(xc), base + s(19), nm, "tick", I["secondary"], "middle"))
        pts.append([pl.X(xc), pl.Y(sum(e)), f"{nm}: KE {e[0]:.0f} J, PE {e[1]:.0f} J, spring {e[2]:.0f} J, "
                    f"total {sum(e):.0f} J"])
    o.append(H.line(s, pl.x0, pl.Y(E_TOT), pl.x1, pl.Y(E_TOT), I["secondary"], "ref", H.DASH_REF))
    o.append(plabel(s, pl.x1, pl.Y(E_TOT) - s(6), f"E = {E_TOT:.0f} J, the same at every instant", "label2",
                    I["primary"], "end"))
    o.append(legend(s, 62, top - s(30), [(SER[0], "KE", None), (SER[1], "PE", None),
                                         (SER[2], f"spring ½k({it('L')}{sub('0', s, 'label2')} − {it('r')})²", None)]))
    o.append(credit(s, VB))
    aria = (f"A runner at midstance (Lynch skeleton art) with the spring leg drawn over it, beside the total energy "
            f"E = KE + PE + spring energy of the SLIP model, k = 15 kN/m, 70 kg, from Lab 1. Below, four stacked bars at "
            f"touchdown, midstance, takeoff and the apex of flight: kinetic energy (blue), potential energy (red) and "
            f"spring energy (orange) trade places, the spring term {states[1][1][2]:.0f} J only at midstance, but each bar "
            f"totals E = {E_TOT:.0f} J, so the energy passes unbroken from stance into flight.")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ jump and landing figures (svg #24, #26, #36, #38)
STAND_H = com_rel(LB.pose())[1]                       # kit COM height in quiet standing, 1.015 m (0.580 H)
DEPTH = {}


def crouch(h_com):
    """Squat pose with COM height h_com (m), cached."""
    key = round(h_com, 4)
    if key not in DEPTH:
        DEPTH[key] = squat_to(h_com)
    return DEPTH[key]


def tsub(s, name, size="label2"):
    return sub(name, s, size)


# ================================================================ svg #24  C6 squat jump against countermovement jump
def fig24():
    p = "m9f24_"
    HF, fy = 168.0, 214.0
    VB, s = VBs(vb_h(fy + 292))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    u = HF / STAT
    h_cr = STAND_H - D_PUSH                           # crouch depth = the push-off distance, 0.40 m (line 218)
    Pc = crouch(h_cr)
    o.append(floor(s, 8, 392, fy))
    for ox, name, cm in ((92.0, "squat jump", False), (310.0, "countermovement jump", True)):
        body, J, _ = place(p, s, Pc, ox, fy, HF)
        o.append(body)
        c = J["com"]
        ys = fy - STAND_H * u
        o.append(ext(s, ox - s(60), ys, ox + s(60), ys))
        if cm:
            xd = ox - s(50)
            o.append(H.arrow(s, p, xd, ys, xd, c[1] - s(2), "force"))
            o.append(lab(s, xd - s(4), (c[1] + ys) / 2 + s(4), "dip", "label2", anchor="end"))
        else:
            xa = ox + s(58)
            o.append(H.arrow(s, p, xa, c[1], xa, ys + s(2), "geometry"))
            o.append(lab(s, xa + s(5), (c[1] + ys) / 2 + s(4), f'{it("d")} = {D_PUSH:.2f} m', "label2"))
        o.append(H.com_mark(s, *c))
        o.append(lab(s, ox, fy + s(20), name, "label", anchor="middle"))
    o.append(lab(s, 8, 22, f"same depth, same push-off distance {it('d')} = {D_PUSH:.2f} m"))
    o.append(lab(s, 92, fy + s(38), "starts from rest", "label2", anchor="middle"))
    o.append(lab(s, 310, fy + s(38), "dips first, then reverses", "label2", anchor="middle"))
    o.append(lab(s, 392, fy - STAND_H * u - s(5), "COM standing", "tick", I["secondary"], "end"))
    # force-time curves of the push-off (Lab 2)
    top, base = fy + 100.0, fy + 244.0
    pl = Plot(s, (62, top, 388, base), (0, _TP * 1000), (0, 3))
    o.append(pl.axes([(v, f"{v}") for v in (0, 100, 200, 300)], [(v, f"{v}") for v in (0, 1, 2, 3)],
                     "time in the push-off (ms)", "vertical force (body weights)", grid=(1, 2, 3)))
    fs, fc = jump_profile(1.0), jump_profile(0.8)
    tt = _t2 * 1000
    o.append(H.line(s, pl.x0, pl.Y(1), pl.x1, pl.Y(1), I["secondary"], "ref", H.DASH_REF))
    o.append(pl.curve(tt, fs, SER[1], multi=True))
    o.append(pl.curve(tt, fc, SER[0], multi=True))
    o.append(plabel(s, pl.x0 + s(6), pl.Y(1) + s(15), "body weight", "label2", I["secondary"]))
    o.append(plabel(s, pl.X(8), pl.Y(2.62), f"countermovement: {IMP_CMJ:.1f} N s, {H_CMJ * 100:.1f} cm", "label2"))
    o.append(plabel(s, pl.X(150), pl.Y(0.55), f"squat: {IMP_SJ:.1f} N s, {H_SJ * 100:.1f} cm", "label2"))
    o.append(legend(s, 62, top - s(12), [(SER[0], "countermovement", None), (SER[1], "squat", None)]))
    pts = [[pl.X(tt[i]), [pl.Y(fs[i]), pl.Y(fc[i])],
            f"t = {tt[i]:.0f} ms: squat {fs[i]:.2f} BW, countermovement {fc[i]:.2f} BW"] for i in range(len(tt))]
    o.append(credit(s, VB))
    aria = ("Two skeletons (Lynch art) in the same crouch, 0.40 m below standing, at the start of the push-off: a squat "
            "jump that starts from rest and a countermovement jump that dipped first. Below, the vertical force "
            "against time for each push-off from Lab 2, both at a peak of 2.5 body weights over 0.30 s. The "
            "countermovement force (red) is front-loaded, reaching its peak earlier, so it carries a net impulse of "
            "175.5 N s against 169.9 N s (3.3 percent more) and a takeoff height of 32.0 cm against 30.0 cm for the squat "
            "jump (blue), because height goes as the square of the impulse.")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ svg #26  C8 stiff against soft landing
def fig26():
    p = "m9f26_"
    HF, fy = 190.0, 262.0
    VB, s = VBs(vb_h(fy + 88))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    u = HF / STAT
    kB = 13.0                                         # px per body weight of average force
    o.append(floor(s, 8, 392, fy))
    for ox, ds, name in ((110.0, 0.05, "stiff"), (276.0, 0.40, "soft")):
        P = crouch(STAND_H - ds)
        body, J, _ = place(p, s, P, ox, fy, HF)
        o.append(body)
        c = J["com"]
        y0 = fy - STAND_H * u                         # COM height at first contact
        o.append(ext(s, ox - s(46), y0, ox + s(40), y0))
        xd = ox - s(46)
        o.append(dvert(s, p, xd, y0, c[1]))
        o.append(lab(s, xd, y0 - s(13), f'{it("d")}{tsub(s, "s")} = {ds * 100:.0f} cm', "label2", anchor="middle"))
        fav = f_avg(ds) / BW
        xf = ox + s(54)
        o.append(H.arrow(s, p, xf, fy - s(1), xf, fy - fav * kB, "reaction"))
        o.append(lab(s, xf + s(6), fy - fav * kB / 2 + s(4), f'{fav:.2f} {it("mg")}' if fav < 5 else
                     f'{fav:.1f} {it("mg")}', "label2"))
        o.append(H.com_mark(s, *c))
        o.append(lab(s, ox, 22 + s(18), f"{name}: {it('d')}{tsub(s, 's', 'label')} = {ds * 100:.0f} cm", "label",
                     anchor="middle"))
    o.append(lab(s, 200, 22, f"same drop, {H_DROP} m: {it('v')}{tsub(s, 'land', 'label')} = {V_LAND:.1f} m/s, same momentum",
                 "label", anchor="middle"))
    o.append(lines(s, 200, fy + s(28), [f"black arrows: the average force {it('F̄')} = ½{it('m')}{it('v')}{tsub(s, 'land')}² / "
                                        f"{it('d')}{tsub(s, 's')} + {it('mg')}",
                                        "eight times the distance, about a fifth of the force:",
                                        f"{f_avg(0.05) / BW:.1f} against {f_avg(0.40) / BW:.2f} body weights"],
                   anchor="middle"))
    o.append(credit(s, VB))
    aria = ("Two skeletons (Lynch art) at the end of the same 0.5 m drop, landing speed 3.1 m/s, drawn to scale at the "
            "lowest point of the stop with the dashed line at the height of the centre of mass at first contact. Left, "
            "a stiff landing: the centre of mass travels only d s = 5 cm and the average force, black arrow, is 11.0 body "
            "weights. Right, a soft landing with the knees bent: it travels d s = 40 cm, eight times farther, and the "
            "average force is 2.25 body weights. The average force is half m v squared over d s plus m g, inversely "
            "proportional to the stopping distance.")
    return finish(VB, aria, s, o)


# ================================================================ svg #36  D8 takeoff speed and jump height
def jump_pose():
    """Takeoff: legs extended, up on the toes, arms overhead (design pose: the page states no angles)."""
    leg = dict(hip=-4, knee=0, contact="toe", shoulder=165, elbow=5)
    return LB.pose(near=dict(leg), far=dict(leg), anchor=("toe", "near"))


def fig36():
    p = "m9f36_"
    HF, fy = 180.0, 292.0
    VB, s = VBs(vb_h(fy + 106))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    u = HF / STAT
    P = jump_pose()
    ox = 130.0
    body, J, _ = place(p, s, P, ox, fy, HF, org="toe")
    c0 = J["com"]
    o.append(floor(s, 8, 196, fy))
    o.append(body)
    dh = H_APEX * u
    xg = 296.0
    g_svg, Jg = LB.draw(p, s, P, xg, fy - dh, HF)
    # the ghost: same body at the apex, drawn lighter, its toe line a height h above the floor
    o.append(f'<g opacity="0.5">{g_svg}</g>')
    cg = Jg["com"]
    o.append(H.com_mark(s, *c0))
    o.append(H.com_mark(s, *cg))
    o.append(ext(s, c0[0] + s(10), c0[1], cg[0] + s(30), c0[1]))
    o.append(ext(s, c0[0] + s(10), cg[1], cg[0] + s(30), cg[1]))
    xa = cg[0] + s(26)
    o.append(H.arrow(s, p, xa, c0[1] - s(1), xa, cg[1] + s(1), "geometry"))
    o.append(lab(s, xa + s(5), (c0[1] + cg[1]) / 2 + s(5), f'{it("h")} = {H_APEX * 100:.1f} cm', "label2"))
    kv = s(28)
    o.append(H.arrow(s, p, c0[0] - s(22), c0[1], c0[0] - s(22), c0[1] - V0 * kv, "load"))
    o.append(lab(s, c0[0] - s(28), c0[1] - V0 * kv / 2 + s(4), f'{it("v")}{tsub(s, "0")} = {V0:.2f} m/s', "label2",
                 anchor="end"))
    o.append(lab(s, xg, fy + s(24), f'apex: {it("v")} = 0', "label2", anchor="middle"))
    o.append(lab(s, ox, fy + s(24), "takeoff", "label2", anchor="middle"))
    o.append(lab(s, 8, 22, "takeoff speed from the push-off, height from the flight"))
    o.append(lines(s, 8, fy + s(46), [f"push-off: ½{it('m')}{it('v')}{tsub(s, '0')}² = (net force) × {it('d')}",
                                      f"  = {F_PUSH:.0f} N × {D_PUSH:.2f} m = {F_PUSH * D_PUSH:.0f} J, so {it('v')}{tsub(s, '0')} = {V0:.2f} m/s",
                                      f"flight: ½{it('m')}{it('v')}{tsub(s, '0')}² = {it('mg')}{it('h')}, so "
                                      f"{it('h')} = {it('v')}{tsub(s, '0')}² / 2{it('g')} = {H_APEX * 100:.1f} cm"],
                   "tick"))
    o.append(credit(s, VB))
    aria = ("A jumper at takeoff (Lynch skeleton art): legs extended, up on the toes, arms overhead, with an upward "
            "arrow at the centre of mass for the takeoff speed v0 = 2.43 m/s. A lighter copy of the same body at the apex "
            "of the jump is 30.0 cm higher, the height h = v0 squared over 2g, between two dashed lines at the heights of "
            "the centre of mass. The takeoff speed follows from the push-off work: half m v0 squared equals the net force "
            "515 N times the push-off distance 0.40 m, 206 J. The height follows from conserving energy in flight: half "
            "m v0 squared equals m g h.")
    return finish(VB, aria, s, o)


# ================================================================ svg #38  D10 average force over the stop and the impact peak
def fig38():
    p = "m9f38_"
    HF, fy = 180.0, 222.0
    ds = 0.15
    VB, s = VBs(vb_h(fy + 262))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    u = HF / STAT
    ox = 138.0
    P = crouch(STAND_H - ds)
    body, J, _ = place(p, s, P, ox, fy, HF)
    o.append(floor(s, 8, 392, fy))
    o.append(body)
    c = J["com"]
    y0 = fy - STAND_H * u
    o.append(ext(s, ox - s(46), y0, ox + s(50), y0))
    xd = ox - s(46)
    o.append(dvert(s, p, xd, y0, c[1]))
    o.append(lab(s, xd - s(6), (c[1] + y0) / 2 + s(4), f'{it("d")}{tsub(s, "s")} = {ds * 100:.0f} cm', "label2",
                 anchor="end"))
    o.append(H.com_mark(s, *c))
    fav = f_avg(ds) / BW
    xf = ox + s(40)
    kB = 15.0
    o.append(H.arrow(s, p, xf, fy - s(1), xf, fy - fav * kB, "reaction"))
    o.append(lab(s, xf + s(6), fy - fav * kB / 2 + s(4), f'{it("F̄")} = {fav:.1f} {it("mg")}', "label2"))
    o.append(H.arrow(s, p, ox - s(6), 40, ox - s(6), 40 + s(34), "dim"))
    o.append(lab(s, ox + s(2), 40 + s(14), f'{it("v")}{tsub(s, "land")}', "label2"))
    xr = 196.0
    mi = f"{it('m')}{tsub(s, 'imp')}"
    kc = f"{it('k')}{tsub(s, 'c')}"
    o.append(lines(s, xr, 26, [f"stop: ({it('F̄')} − {it('mg')}){it('d')}{tsub(s, 's')} = ½{it('m')}{it('v')}{tsub(s, 'land')}²",
                               f"{it('F̄')} = ½{it('m')}{it('v')}{tsub(s, 'land')}² / {it('d')}{tsub(s, 's')} + {it('mg')}",
                               f"0.5 m drop, {ds * 100:.0f} cm stop: {fav:.1f} {it('mg')}", "",
                               f"first contact: {mi} = {M_IMP:.0f} kg on {kc},",
                               f"{it('F')}(t) = {it('v')}{tsub(s, 'imp')}√({kc}{mi}) sin ωt",
                               f"{it('F')}{tsub(s, 'peak')} = {it('v')}{tsub(s, 'imp')}√({kc}{mi}),",
                               f"loading rate (2/π) {it('v')}{tsub(s, 'imp')}{kc}"]))
    # the impact transients (section 9): first quarter cycle of each contact
    top, base = fy + 76.0, fy + 210.0
    tmax = 25.0
    pl = Plot(s, (62, top, 388, base), (0, tmax), (0, 2.0))
    o.append(pl.axes([(v, f"{v}") for v in (0, 5, 10, 15, 20, 25)], [(v, f"{v:g}") for v in (0, 0.5, 1.0, 1.5, 2.0)],
                     "time from first contact (ms)", "impact force (body weights)", grid=(0.5, 1.0, 1.5, 2.0)))
    pts, curves = [], []
    for kc_, col, nm in ((KC_STIFF, SER[0], "stiff"), (KC_SOFT, SER[1], "soft")):
        om, fp, tr, rate = impact(kc_)
        tt = np.linspace(0, tr, 60)
        ff = fp * np.sin(om * tt) / BW
        o.append(pl.curve(tt * 1000, ff, col, multi=True))
        o.append(pl.dot(tr * 1000, fp / BW, col))
        curves.append((nm, fp, tr, rate, kc_, col))
    legend_items = [(SER[0], f"stiff, {KC_STIFF / 1000:.0f} kN/m", None), (SER[1], f"soft, {KC_SOFT / 1000:.0f} kN/m", None)]
    o.append(legend(s, 62, top - s(12), legend_items))
    nm, fp, tr, rate, kc_, col = curves[0]
    o.append(plabel(s, pl.X(tr * 1000) + s(8), pl.Y(fp / BW) + s(4), f"{fp:.0f} N = {fp / BW:.1f} mg",
                    "label2"))
    o.append(plabel(s, pl.X(tr * 1000) + s(8), pl.Y(fp / BW) + s(19), f"{tr * 1000:.1f} ms, {rate:.0f} mg/s", "label2"))
    nm, fp, tr, rate, kc_, col = curves[1]
    o.append(plabel(s, pl.X(tr * 1000) + s(4), pl.Y(fp / BW) - s(14), f"{fp:.0f} N = {fp / BW:.1f} mg",
                    "label2", I["primary"], "end"))
    o.append(plabel(s, pl.X(tr * 1000) + s(4), pl.Y(fp / BW) + s(24), f"{tr * 1000:.1f} ms, {rate:.0f} mg/s",
                    "label2", I["primary"], "end"))
    for nm, fp, tr, rate, kc_, col in curves:
        om = math.sqrt(kc_ / M_IMP)
        for tms in np.linspace(0, tr * 1000, 24):
            pts.append([pl.X(tms), pl.Y(fp * math.sin(om * tms / 1000) / BW),
                        f"{nm}, t = {tms:.1f} ms: {fp * math.sin(om * tms / 1000) / BW:.2f} BW"])
    pts.sort(key=lambda q: q[0])
    o.append(credit(s, VB))
    aria = ("Top left, a skeleton (Lynch art) at the end of a landing from a 0.5 m drop, the centre of mass having "
            "travelled the stopping distance d s = 15 cm below its height at first contact (dashed line); the average "
            "force over the stop, F bar = half m v land squared over d s plus m g, is 4.3 body weights. Top right, the "
            "two relations the problem derives: the stop gives F bar by the work-energy theorem, and the first contact "
            "is a foot and lower-leg mass of 8 kg on a contact spring k c, simple harmonic motion with peak force "
            "v imp times the square root of k c m imp and loading rate 2 over pi times v imp k c. Bottom, the first "
            "quarter cycle of that impact force against time for a stiff contact, 200 kN/m (red), peak 1265 N, 1.8 body "
            "weights, in 9.9 ms, 185 body weights per second, and a soft one, 40 kN/m (blue), peak 566 N, 0.8 body "
            "weights, in 22.2 ms, 37 body weights per second.")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ svg #25  C7 the tendon, not the muscle, does the work
SHANK_CALF = (-40.0, 55.0)                                    # shank-local: top of the calf muscle belly (design value)


def fig25():
    p = "m9f25_"
    extra = " Bars, Achilles coil and labels drawn for this course."
    VBh = vb_h(548, extra)
    VB, s = (0, 0, 400, VBh), H.Scale(400, VBh, display_w=400, max_h=H.MAX_DISPLAY_H_BODY)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy, ox = 270.0, 318.0, 300.0
    Pr, _ = fit_pose(run_pose, (25.0, 55.0), (0.0, R_MID))
    body, J, _ = place(p, s, Pr, ox, fy, HF)
    o.append(floor(s, 196, 392, fy))
    o.append(body)
    top = seg_pt(J, Pr, "lat_shank", False, SHANK_CALF)             # calf belly, calf-tendon junction, heel
    jn = seg_pt(J, Pr, "lat_shank", False, SHANK_ACH)
    ach = seg_pt(J, Pr, "lat_foot", False, FOOT["ach"])
    mf, ms = T["muscle"]
    for col, w in ((ms, s(8.0)), (mf, s(5.0))):                     # the muscle: thick tissue-coloured stroke
        o.append(f'<line x1="{top[0]:.2f}" y1="{top[1]:.2f}" x2="{jn[0]:.2f}" y2="{jn[1]:.2f}" stroke="{col}" '
                 f'stroke-width="{w:.2f}" stroke-linecap="round"/>')
    o.append(coil(s, jn, ach, n=7, amp=s(4.5), col=O["force"], w=2.2))      # the tendon: the spring, in series
    o += [dot(s, jn[0], jn[1], O["force"], 2.8), dot(s, ach[0], ach[1], O["force"], 2.8)]
    lx, rx = 8.0, 190.0
    yc, yt = 150.0, 238.0                                            # label blocks, above the foot
    cc = ((top[0] + jn[0]) / 2, (top[1] + jn[1]) / 2)
    tt = ((jn[0] + ach[0]) / 2, (jn[1] + ach[1]) / 2)
    o.append(H.line(s, rx, yc + s(6), cc[0] - s(4), cc[1], I["secondary"], "leader"))
    o.append(lab(s, lx, yc, "calf muscle", "label2"))
    o.append(lines(s, lx, yc + s(15), ["(gastrocnemius, soleus)", "contracts, but supplies only", f"the loss, (1 − {it('R')}){it('U')} ≈ {E_LOSS:.1f} J"]))
    o.append(H.line(s, rx, yt + s(6), tt[0] - s(4), tt[1], O["force"], "leader"))
    o.append(lab(s, lx, yt, "Achilles tendon: the spring", "label2"))
    o.append(lines(s, lx, yt + s(15), [f"stores {it('U')} ≈ {U_ACH:.0f} J on landing,",
                                          f"returns {it('R')}{it('U')} = {E_RET:.1f} J ({it('R')} ≈ {R_ACH})"]))
    o.append(lab(s, 8, 22, "where the work of a running step comes from"))
    # bars: mechanical work per step, elastic leg against rigid leg
    x0, x1, k = 138.0, 392.0, 254.0 / (2 * U_ACH)
    yb = 372.0
    hh = s(26)
    tendon_f, tendon_s = T["tendon"]
    musc_f, musc_s = T["muscle"]

    def seg(xa, xb, y, fill, stroke, text=None):
        o.append(f'<rect x="{xa:.2f}" y="{y:.2f}" width="{xb - xa:.2f}" height="{hh:.2f}" fill="{fill}" stroke="{stroke}" '
                 f'stroke-width="{s(1.2):.2f}"/>')
        if text:
            o.append(lab(s, (xa + xb) / 2, y + hh / 2 + s(4.5), text, "label2", anchor="middle"))

    o.append(lab(s, 8, yb - s(18), "mechanical work in one step (J):", "label"))
    seg(x0, x0 + E_RET * k, yb, tendon_f, tendon_s, f"tendon recoil {E_RET:.1f}")
    seg(x0 + E_RET * k, x0 + U_ACH * k, yb, musc_f, musc_s)
    o.append(lab(s, x0 + U_ACH * k + s(5), yb + hh / 2 + s(4.5), f"muscle {E_LOSS:.1f}", "label2"))
    o.append(lines(s, 8, yb + s(11), ["elastic leg"], "label2"))
    y2 = yb + hh + s(30)
    seg(x0, x0 + U_ACH * k, y2, musc_f, musc_s, f"absorbs {U_ACH:.0f}")
    seg(x0 + U_ACH * k, x0 + 2 * U_ACH * k, y2, musc_f, musc_s, f"regenerates {U_ACH:.0f}")
    o.append(lines(s, 8, y2 + s(11), ["rigid leg:", "muscle only"], "label2"))
    for xx, yy in ((x0, yb + hh), (x0, y2 + hh)):
        pass
    o.append(H.line(s, x0, yb - s(4), x0, y2 + hh + s(4), I["axis"], "axis"))
    for v in (0, 31, 62):
        o.append(H.line(s, x0 + v * k, y2 + hh + s(4), x0 + v * k, y2 + hh + s(9), I["axis"], "leader"))
        o.append(lab(s, x0 + v * k, y2 + hh + s(22), f"{v}", "tick", I["secondary"], "middle"))
    # legend: tissue colours
    ly = y2 + hh + s(46)
    for xx, (f_, s_), nm in ((x0, (tendon_f, tendon_s), "tendon"), (x0 + 90, (musc_f, musc_s), "muscle")):
        o.append(f'<rect x="{xx:.2f}" y="{ly - s(11):.2f}" width="{s(14):.2f}" height="{s(11):.2f}" fill="{f_}" '
                 f'stroke="{s_}" stroke-width="{s(1.2):.2f}"/>')
        o.append(lab(s, xx + s(19), ly, nm, "label2"))
    o.append(lines(s, 8, ly + s(24), [f"muscle work per step: {2 * U_ACH:.0f} J ÷ {E_LOSS:.1f} J = {2 / (1 - R_ACH):.0f} = 2/(1 − {it('R')}):",
                                      f"the muscle pays only the tendon's loss, {(1 - R_ACH) * 100:.0f} % of {it('U')}"]))
    o.append(credit(s, VB, extra))
    aria = ("A runner at midstance, side view (Lynch skeleton art): the calf muscle, gastrocnemius and soleus, drawn as a "
            "thick stroke, is in series with the Achilles tendon, drawn as a red coil that runs to the heel bone. The "
            "tendon is the spring that stores about 31 J on landing and returns 28.5 J, a resilience "
            "of 0.92, and the muscle supplies only the 2.5 J lost. Below, two bars of mechanical work in one step: with "
            "the elastic tendon, 28.5 J of tendon recoil plus 2.5 J of muscle work; with a rigid leg, the muscle alone "
            "would absorb 31 J and then regenerate 31 J, 62 J, twenty-five times the 2.5 J, which is 2 over (1 minus R).")
    return finish(VB, aria, s, o)


FIGS = {
    19: ("A runner in stance with one foot down beside a runner airbor", fig19),
    20: ("At midstance a runner's centre of mass is low on a compresse", fig20),
    22: ("A body on a leg spring labelled k_leg, defined as the combin", fig22),
    23: ("A walking centre of mass vaulting on a circular arc, limited", fig23),
    24: ("A squat jump from a still crouch beside a countermovement ju", fig24),
    25: ("A calf muscle in series with an Achilles tendon spring that ", fig25),
    26: ("A stiff landing with small stopping distance and large force", fig26),
    30: ("The SLIP mass in polar coordinates: leg length r and angle p", fig30),
    31: ("A body on a leg spring with its conserved total energy.", fig31),
    32: ("The leg-spring force and its vertical component, the ground ", fig32),
    33: ("The vaulting centre of mass: gravity, the centripetal requir", fig33),
    36: ("A jumper leaving at v0 and rising to apex height v0 squared ", fig36),
    38: ("A landing stopped over a stopping distance, with the average", fig38),
}
