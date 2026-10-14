"""Module 9 whole-body figures (main text). Exposes the Lynch body kit once per page.

svg #2 (Fig. 1 walking double support against running flight), #3 (Fig. 2 running bounce: COM path and leg spring),
#5 (Fig. 4 SLIP model), #6 (Fig. 5 vertical GRF), #7 (Fig. 6 flight parabola and the Froude ceiling), #9 (Fig. 8 jump
height), #10 (Fig. 9 muscle-tendon unit and tendon recoil).  (Fig. numbers = the CSS counter of module09.html;
the prose numbers every figure from #5 on one lower, see the report.)

Numbers (module09.html line numbers):
  Lab 1 SLIP integrator (339-358), its jog touchdown m = 70 kg, L0 = 1 m, alpha0 = 70 deg, v = (4.0, -0.7) m/s
  (361-366); k = 11 / 26 kN/m give 2.1 / 3.6 BW and 211 / 150 ms (369).  k = 15 kN/m (this file's choice for the
  "illustrative run" of lines 138-140 and 160) gives 2.58 BW, 188 ms and takeoff v_y = 0.46 m/s, the text's
  "near 2.6 body weights" (140), "t_c 188 ms" (old figure) and "0.46 m/s" (160).
  Flight Prop 4.1 (155) with v_x = 4, v_y = 0.9: t_f 0.18 s, apex 4 cm, range 0.7 m (160).  Froude (4.2, 167):
  F_z = mg (1 - Fr), ceiling Fr = 1 = 3.1 m/s for a 1 m leg (172), switch near Fr 0.5 (172).
  Jump: 515 N net over d = 0.40 m, 70 kg gives v_0 = 2.4 m/s and h = 30 cm (218); Lab 2 profiles (376-396):
  30.0 / 32.0 cm, impulses 169.9 / 175.5 N s, +3.3 % impulse -> +6.7 % height (222).
  Tendon (234): Module 6 toe + linear model, k_lin = E A / L0 = 1.3 GPa 80 mm2 / 250 mm = 4.16e5 N/m, x* = 7.5 mm;
  5 kN -> 16 mm, 31 J; R = 0.92 returns 28.5 J, loses 2.5 J; 4 kN -> 13.4 mm, 20.2 J.
Body art: lynch_body.py (Patrick J. Lynch, CC BY 2.5); tendon art: InjuryMap (CC BY-SA 4.0) via the m05 fig 21 crop.
The text states no stature.  Running figures (#2, #3, #5, #6): the runner is 1.65 m tall, so that the touchdown leg (COM to
heel, knee 12 deg) is the Lab 1 leg length L0 = 1 m; jump figure (#9): 1.75 m (course reference).  No running preset exists
in the kit: the running poses are joint-angle sets chosen here (design choice, reported).
"""
import math
from functools import lru_cache

import numpy as np

import house as H
import lynch_body as LB
from m05.plots_main import Ax, axes, curve, DASH_SER, legend
from m05.body import art_image, finish, inner_svg, it, wrap, F21
from m05.body import _read as read_art

SHARED_DEFS = LB.SHARED_DEFS
O, I, T = H.OVERLAY, H.INK, H.TISSUE
S0, S1, S2 = H.SERIES[0], H.SERIES[1], H.SERIES[2]
BOXFILL, GRID = "#f7f4ef", "#e6e6e6"
BODY = H.MAX_DISPLAY_H_BODY
H_M = 1.75                                   # course reference stature (the text states none)
G, M_KG = 9.81, 70.0
W_N = M_KG * G
trapz = getattr(np, "trapezoid", None) or np.trapz


# ================================================================ SLIP runs (Lab 1 integrator, lines 339-358)
def slip_run(k, alpha_deg, vx0, vy0, L0=1.0, dt=1e-4):
    """Lab 1's slip_stance (symplectic Euler), also recording the path.  Returns a dict of arrays."""
    a = math.radians(alpha_deg)
    x, y, vx, vy = -L0 * math.cos(a), L0 * math.sin(a), vx0, vy0
    t, rows = 0.0, []
    while True:
        r = math.hypot(x, y)
        F = k * (L0 - r)
        ax, ay = F * x / r / M_KG, F * y / r / M_KG - G
        rows.append((t, x, y, r, F * y / r, F * x / r))
        vx, vy = vx + ax * dt, vy + ay * dt
        x, y = x + vx * dt, y + vy * dt
        t += dt
        if math.hypot(x, y) >= L0 and t > 5 * dt:
            break
        if y <= 0 or t > 2.0:
            break
    R = np.array(rows)
    d = dict(t=R[:, 0], x=R[:, 1], y=R[:, 2], r=R[:, 3], Fz=R[:, 4], Fx=R[:, 5], vx=vx, vy=vy, tc=t, L0=L0,
             alpha=alpha_deg, k=k)
    im = int(np.argmin(np.abs(d["x"])))                           # leg vertical: midstance
    d.update(R_MID=float(d["r"][im]), Y_MID=float(d["y"][im]), FZ_MID=float(d["Fz"][im]),
             Y_TD=float(d["y"][0]), X_TD=float(d["x"][0]), Y_TO=float(d["y"][-1]), X_TO=float(d["x"][-1]),
             VX_TO=float(vx), VY_TO=float(vy), PK=float(d["Fz"].max()) / W_N)
    d["APEX"] = d["VY_TO"] ** 2 / (2 * G)                          # above the takeoff point (Prop 4.1)
    d["T_UP"] = d["VY_TO"] / G
    d["T_FL"] = 2 * d["VY_TO"] / G                                 # back to the takeoff height
    d["A_TD"] = math.degrees(math.atan2(d["X_TD"], d["Y_TD"]))     # leg angle from the vertical, - = foot ahead
    d["A_TO"] = math.degrees(math.atan2(d["X_TO"], d["Y_TO"]))
    d["A_ND"] = -math.degrees(math.atan2(math.sqrt(1.0 - d["Y_TO"] ** 2), d["Y_TO"]))   # next touchdown, takeoff height
    return d


def _chk(k):
    r = slip_run(k, 70, 4.0, -0.7)
    return round(r["PK"], 1), round(r["tc"] * 1000)


assert _chk(11000) == (2.1, 211) and _chk(26000) == (3.6, 150)                                    # line 369
LAB = slip_run(15000.0, 70, 4.0, -0.7)       # the "illustrative run" of Fig. 5 (lines 140, 160): GRF figure #6
assert round(LAB["PK"], 1) == 2.6 and round(LAB["tc"] * 1000) == 188 and round(LAB["VY_TO"], 2) == 0.46
# the symmetric steady run of section 5 (line 194): takeoff mirrors touchdown, t_c 0.169 s, v_y 0.479 m/s (the
# stiffness and angle of attack were found by root-finding so that it does; see m09/plots_main.py slip_sym)
SYM = slip_run(18625.0, 70.6883, 4.0, -0.479)
assert round(SYM["tc"], 3) == 0.169 and abs(SYM["VY_TO"] - 0.479) < 5e-4 and abs(SYM["Y_TO"] - SYM["Y_TD"]) < 1e-3
assert round(float(trapz(SYM["Fz"], SYM["t"])), 1) == 183.2                                       # line 194


def flight_xy(R, t):
    return R["X_TO"] + R["VX_TO"] * t, R["Y_TO"] + R["VY_TO"] * t - 0.5 * G * t * t


# ================================================================ small drawing helpers (m08/body_main idiom)
def defs(p, s, extra=""):
    return f"<defs>{H.markers(p, s)}{extra}</defs>"


def poly(s, pts, col, w="curve", dash=None, extra=""):
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    return (f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="none" stroke="{col}" '
            f'stroke-width="{s(H.PX[w]):.2f}" stroke-linejoin="round"{da} {extra}/>')


def white_under(s, x1, y1, x2, y2, w=4):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#fff" '
            f'stroke-width="{s(w):.2f}" opacity="0.85"/>')


def dline(s, x1, y1, x2, y2, col=None, w="ref", dash=H.DASH_REF):
    return white_under(s, x1, y1, x2, y2) + H.line(s, x1, y1, x2, y2, col or O["dim"], w, dash=dash)


def floor_line(s, x0, x1, y):
    return H.line(s, x0, y, x1, y, I["rule"], "axis")


def leader(s, x1, y1, x2, y2, col=None):
    return H.line(s, x1, y1, x2, y2, col or I["secondary"], "leader")


def arc_pts(cx, cy, r, a0, a1, n=24):
    """Screen angles in degrees: 0 = +x, + = clockwise (y down)."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def angle_arc(s, cx, cy, r, a0, a1, col=None):
    pts = arc_pts(cx, cy, r, a0, a1, 16)
    return (f'<path d="M{" L".join(f"{x:.1f} {y:.1f}" for x, y in pts)}" fill="none" stroke="{col or O["geometry"]}" '
            f'stroke-width="{s(H.PX["geom"]):.2f}"/>')


def dot(s, x, y, col=None, r=3.5):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{col or I["primary"]}" stroke="#fff" '
            f'stroke-width="{s(1.2):.2f}"/>')


def mass(s, x, y, r=9):
    """Point mass of a model: dark disc with a white rim."""
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{I["primary"]}" stroke="#fff" '
            f'stroke-width="{s(2):.2f}"/>')


def box(s, x, y, w, h, fill=BOXFILL, stroke=None):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{s(4):.2f}" fill="{fill}" '
            f'stroke="{stroke or I["rule"]}" stroke-width="{s(1):.2f}"/>')


def lines(s, x, y, rows, size="label2", fill=None, anchor="start", dy=None):
    dy = dy or s(H.PX[size] * 1.3)
    return "".join(H.label(s, x, y + i * dy, t, size, fill or I["primary"], anchor) for i, t in enumerate(rows))


def pt(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def spring(s, a, b, n=7, amp=7.0, col=None, w=2.2, lead=0.14):
    """Zig-zag coil from a to b (a mark for the model's massless leg spring; the straight leads at both ends are
    the rigid end pieces).  amp = half-width in rendered px."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    pts = [a, (a[0] + ux * L * lead, a[1] + uy * L * lead)]
    for i in range(2 * n):
        f = lead + (1 - 2 * lead) * (i + 0.5) / (2 * n)
        sg = 1 if i % 2 == 0 else -1
        pts.append((a[0] + ux * L * f + nx * s(amp) * sg, a[1] + uy * L * f + ny * s(amp) * sg))
    pts += [(a[0] + ux * L * (1 - lead), a[1] + uy * L * (1 - lead)), b]
    c = col or I["primary"]
    d = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="#fff" stroke-width="{s(w + 3.2):.2f}" stroke-linejoin="round" '
            f'stroke-linecap="round" opacity="0.9"/>'
            f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{s(w):.2f}" stroke-linejoin="round" '
            f'stroke-linecap="round"/>')


# ================================================================ running poses (kit angles, degrees)
def build_pose(kind, **v):
    """Running poses.  hip + = flexion, knee + = flexion, ankle + = dorsiflexion (lynch_body.pose).
    v overrides the stance-leg knee and hip so a pose can be fitted to the SLIP run."""
    near, far = {}, {}
    if kind == "touchdown":
        near = dict(hip=v.get("hip", 30), knee=v.get("knee", 12), contact=None, ankle=8, shoulder=-30, elbow=90)
        far = dict(hip=-15, knee=75, contact=None, ankle=-10, shoulder=35, elbow=90)
        return LB.pose(pelvis=6, near=near, far=far, anchor=("heel", "near"))
    if kind == "midstance":
        near = dict(hip=v.get("hip", 8), knee=v.get("knee", 42), shoulder=5, elbow=90)
        far = dict(hip=55, knee=100, contact=None, ankle=0, shoulder=0, elbow=90)
        return LB.pose(pelvis=6, near=near, far=far, anchor=("heel", "near"))
    if kind == "toeoff":
        near = dict(hip=v.get("hip", -18), knee=v.get("knee", 25), contact=None, ankle=-35, shoulder=30, elbow=90)
        far = dict(hip=45, knee=85, contact=None, ankle=0, shoulder=-30, elbow=90)
        return LB.pose(pelvis=6, near=near, far=far, anchor=("toe", "near"))
    if kind == "flight":
        near = dict(hip=-20, knee=95, contact=None, ankle=-20, shoulder=30, elbow=90)
        far = dict(hip=55, knee=100, contact=None, ankle=10, shoulder=-30, elbow=90)
        return LB.pose(pelvis=6, near=near, far=far, anchor=("hip", "near"))
    raise KeyError(kind)


_S1 = H.Scale(100, 100)


def _draw(P, hb=300.0, x=0.0, y=0.0):
    return LB.draw("", _S1, P, x, y, hb)


def _bisect(f, lo, hi, n=26):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def metrics(kind, hip, knee):
    """Stance pose geometry in fractions of the stature: (COM height, COM x minus foot x, reach, leg angle in deg
    from the vertical).  Foot point = the centre of pressure: heel at touchdown, middle of the foot at midstance, toe
    at toe-off (the SLIP's point foot)."""
    P = build_pose(kind, hip=hip, knee=knee)
    _, J = _draw(P, 1.0, 0.0, 0.0)
    h = J["floor_y"] - J["com"][1]
    foot = {"toeoff": J["toe"], "touchdown": J["heel"]}.get(kind) or ((J["heel"][0] + J["toe"][0]) / 2, 0)
    dx = J["com"][0] - foot[0]
    return h, dx, math.hypot(h, dx), math.degrees(math.atan2(dx, h))


def fit(kind, angle, reach, hips, knee=None):
    """Hip (and knee, unless fixed) of a stance pose whose COM-to-foot line has the SLIP angle and reach (both in
    the run's units): for each hip the knee is bisected on the reach, the hip on the angle."""
    def knee_for(hip):
        if knee is not None:
            return knee
        return _bisect(lambda kn: metrics(kind, hip, kn)[2] - reach, 0.0, 80.0)

    hip = _bisect(lambda hp: metrics(kind, hp, knee_for(hp))[3] - angle, *hips)
    kn = knee_for(hip)
    m = metrics(kind, hip, kn)
    assert abs(m[3] - angle) < 0.05 and (knee is not None or abs(m[2] - reach) < 2e-3), (kind, m, angle, reach)
    return hip, kn


KNEE_TO = 45.0                                      # toe-off knee flexion (design choice; its reach is not fitted)


@lru_cache(maxsize=None)
def body_fits(name):
    """Stance poses fitted to a SLIP run (name 'sym' or 'lab'): touchdown, midstance, toe-off, next touchdown.
    Stature: the touchdown pose (knee 12 deg, a typical initial-contact flexion; the centre of pressure at the heel)
    has the SLIP leg length L0 = 1 m from the COM to the foot, so the drawn runner is H = 1 / reach tall (about
    1.65 m; the text states no stature).  Touchdown and midstance then match the SLIP leg angle and length (reach);
    toe-off and the next touchdown (lab run) match the angle only (a plantar-flexed push-off foot reaches 3-8 %
    farther than the SLIP leg)."""
    R = dict(sym=SYM, lab=LAB)[name]
    hp = _bisect(lambda hh: metrics("touchdown", hh, 12.0)[3] - R["A_TD"], 10, 60)
    H_run = 1.0 / metrics("touchdown", hp, 12.0)[2]
    r = lambda m: m / H_run                                           # noqa: E731
    hip_to = _bisect(lambda hh: metrics("toeoff", hh, KNEE_TO)[3] - R["A_TO"], -50, 10)
    hip_nd = _bisect(lambda hh: metrics("touchdown", hh, 12.0)[3] - R["A_ND"], 10, 70)
    F = dict(
        touchdown=dict(hip=hp, knee=12.0, kind="touchdown"),
        midstance=dict(zip(("hip", "knee"), fit("midstance", 0.0, r(R["R_MID"]), (0, 70))), kind="midstance"),
        toeoff=dict(hip=hip_to, knee=KNEE_TO, kind="toeoff"),
        nexttd=dict(hip=hip_nd, knee=12.0, kind="touchdown"))
    poses = {n: build_pose(v["kind"], hip=v["hip"], knee=v["knee"]) for n, v in F.items()}
    poses["flight"] = build_pose("flight")
    return H_run, poses


# ================================================================ svg #2  Fig. 1 double support replaced by flight
def slip_glyph(s, p, x, floor_y, k, com_h, r=None, label=None):
    """The spring-mass model beside a body: point mass at the COM height, massless spring to the foot point on the
    floor (r metres long; none in flight).  k = px per metre."""
    o = []
    my = floor_y - k * com_h
    if r is not None:
        o.append(spring(s, (x, my), (x, floor_y), n=6))
        o.append(dot(s, x, floor_y, I["primary"], 4.5))
    o.append(mass(s, x, my, 9))
    if label:
        o.append(H.label(s, x, my - s(16), label, "label2", anchor="middle"))
    return "".join(o)


def fig2():
    p = "m9f2_"
    VB = (0, 0, 760, 440)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    R = SYM
    H_run, fr = body_fits("sym")
    hb, fy = 244.0, 330.0
    k = hb / H_run
    walk = LB.pose(**LB.POSES["gait_heel_strike"])
    items = [("walk", walk, 0.0, "walking: double support", "both feet on the ground"),
             ("stance", fr["midstance"], R["Y_MID"], "running: stance", "one foot on the ground"),
             ("flight", fr["flight"], R["Y_TO"] + R["APEX"], "running: flight", "no foot on the ground")]
    o = [defs(p, s), floor_line(s, 8, 752, fy)]
    x = 14.0
    pos = {}
    for n, P, com_h, t1, t2 in items:
        y0 = fy if n != "flight" else fy - 100.0
        _, J0 = LB.draw("", s, P, 0.0, y0, hb)
        dx = x - J0["bbox"][0]
        svg, J = LB.draw("", s, P, dx, y0, hb)
        if n == "flight":
            dy = (fy - k * com_h) - J["com"][1]
            svg, J = LB.draw("", s, P, dx, y0 + dy, hb)
        o.append(svg)
        o.append(H.com_mark(s, *J["com"]))
        pos[n] = J
        x = J["bbox"][2] + (78.0 if n != "walk" else 40.0)
    # spring-mass model beside each running body (not instead of it): the mass at the body's COM height
    for n, com_h, rr, gl in (("stance", R["Y_MID"], R["R_MID"], "spring-mass model"),
                             ("flight", R["Y_TO"] + R["APEX"], None, "mass alone: free fall")):
        J = pos[n]
        gx = J["bbox"][2] + 40.0
        o.append(slip_glyph(s, p, gx, fy, k, com_h, rr, gl))
        o.append(dline(s, J["com"][0] + s(8), J["com"][1], gx - s(12), J["com"][1], I["secondary"], "leader"))
    for n, P, com_h, t1, t2 in items:
        J = pos[n]
        cx = (J["bbox"][0] + J["bbox"][2]) / 2
        o.append(H.label(s, cx, fy + s(22), t1, "label2", anchor="middle"))
        o.append(H.label(s, cx, fy + s(38), t2, "label2", I["secondary"], "middle"))
    o.append(lines(s, 14, 24, ["Running replaces double support with flight. Bodies: Lynch skeleton, Winter segment ratios.",
                               "The SLIP model (mass on a spring) is drawn beside each running body; the black dot is its foot."],
                   "label2", I["secondary"]))
    o.append(LB.credit(s, 14, fy + s(70), width=720))
    aria = ("Three skeletons on one floor line. Left, walking in double support: both feet are on the ground. Middle, running "
            "in stance: one foot on the ground, the knee bent and the centre of mass low; beside it the spring-mass model, a "
            "point mass on a compressed spring standing on a point foot. Right, running in flight: no foot touches the "
            "ground, the legs are tucked; beside it the model's mass alone, in free fall. Running replaces double support "
            "with flight.")
    return finish(VB, aria, s, o)


# ================================================================ svg #3  Fig. 2 running bounce
def fig3():
    p = "m9f3_"
    VB = (0, 0, 760, 470)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    hb, fy = 224.0, 330.0
    R = SYM
    H_run, fr = body_fits("sym")
    k = hb / H_run                                        # px per metre
    names = ["touchdown", "midstance", "toeoff", "flight", "touchdown2"]
    pose_of = dict(fr, touchdown2=fr["touchdown"])      # symmetric run: the next touchdown mirrors the first
    placed, x = [], 12.0
    for n in names:
        P = pose_of[n]
        y0 = fy if n != "flight" else fy - 100.0
        _, J0 = LB.draw("", s, P, 0.0, y0, hb)
        dx = x - J0["bbox"][0]
        svg, J = LB.draw("", s, P, dx, y0, hb)
        if n == "flight":                                  # COM at the apex height of the run
            dy = (fy - k * (R["Y_TO"] + R["APEX"])) - J["com"][1]
            svg, J = LB.draw("", s, P, dx, y0 + dy, hb)
        placed.append((n, svg, J))
        x = J["bbox"][2] + 4.0
    o = [defs(p, s), floor_line(s, 8, 752, fy)]
    o += [q[1] for q in placed]
    J = {q[0]: q[2] for q in placed}
    cx = {n: J[n]["com"][0] for n in names}
    cy = {n: J[n]["com"][1] for n in names}
    # COM path: stance from the run (x mapped piecewise-linearly onto the spaced bodies), flight from Prop 4.1; heights
    # are drawn to scale; a residual (a few px) joins the path to each body's Winter COM
    xr = [R["X_TD"], 0.0, R["X_TO"], flight_xy(R, R["T_UP"])[0], flight_xy(R, R["T_FL"])[0]]
    xf = [cx[n] for n in names]
    yr = [R["Y_TD"], R["Y_MID"], R["Y_TO"], R["Y_TO"] + R["APEX"], R["Y_TO"]]
    res = [cy[n] - (fy - k * y) for n, y in zip(names, yr)]
    sx = lambda xx: float(np.interp(xx, xr, xf))          # noqa: E731
    sres = lambda xx: float(np.interp(xx, xr, res))       # noqa: E731
    path = []
    for i in list(range(0, len(R["x"]), 40)) + [len(R["x"]) - 1]:
        xx, yy = float(R["x"][i]), float(R["y"][i])
        path.append((sx(xx), fy - k * yy + sres(xx)))
    for tt in np.linspace(0, R["T_FL"], 24)[1:]:
        xx, yy = flight_xy(R, float(tt))
        path.append((sx(xx), fy - k * yy + sres(xx)))
    o.append(poly(s, path, O["geometry"], "geom"))
    # leg springs (stance frames): COM to the centre-of-pressure point
    for n in ("touchdown", "midstance", "toeoff", "touchdown2"):
        j = J[n]
        foot = {"touchdown": j["heel"], "touchdown2": j["heel"], "toeoff": j["toe"]}.get(n) or ((j["heel"][0] + j["toe"][0]) / 2, fy)
        o.append(spring(s, j["com"], (foot[0], fy)))
    for n in names:
        o.append(H.com_mark(s, cx[n], cy[n]))
    # labels
    lab = dict(touchdown="touchdown", midstance="midstance", toeoff="toe-off", flight="flight, apex", touchdown2="next touchdown")
    rr = dict(touchdown=1.0, midstance=R["R_MID"], toeoff=1.0, touchdown2=1.0)
    for n in names:
        bx = (J[n]["bbox"][0] + J[n]["bbox"][2]) / 2
        o.append(H.label(s, bx, fy + s(20), lab[n], "label2", anchor="middle"))
        o.append(H.label(s, bx, fy + s(35), f"r = {rr[n]:.2f} m" if n in rr else "no leg force", "label2",
                         I["secondary"], "middle"))
    xm, ym = cx["midstance"], cy["midstance"]
    o.append(H.label(s, xm - 6, ym - 108, "COM lowest", "label2", O["geometry"], "middle"))
    o.append(leader(s, xm - 6, ym - 102, xm - 1, ym - 10, O["geometry"]))
    xf_, yf_ = cx["flight"], cy["flight"]
    o.append(H.label(s, xf_ + 10, yf_ - 118, "COM highest, in flight", "label2", O["geometry"], "middle"))
    o.append(leader(s, xf_ + 10, yf_ - 112, xf_ + 1, yf_ - 10, O["geometry"]))
    # time brackets under the floor
    yb = fy + s(62)

    def bracket(xa, xb, text, col):
        return (H.line(s, xa, yb, xb, yb, col, "force", extra=f'marker-start="url(#{p}a_dim)" marker-end="url(#{p}a_dim)"')
                + H.label(s, (xa + xb) / 2, yb + s(18), text, "label2", anchor="middle"))
    o.append(bracket(J["touchdown"]["bbox"][0] + 20, J["toeoff"]["bbox"][2] - 10,
                     f"contact time t{H.sub('c', s)} = {R['tc'] * 1000:.0f} ms", I["axis"]))
    o.append(bracket(J["toeoff"]["bbox"][2] + 6, J["touchdown2"]["bbox"][0] + 30,
                     f"flight time t{H.sub('f', s)} = {R['T_FL'] * 1000:.0f} ms", O["flag"]))
    o.append(lines(s, 12, 22, [f"COM path (blue): the steady SLIP run of section 5, t{H.sub('c', s)} = 0.169 s, v{H.sub('y', s)} = 0.479 m/s. "
                               "Heights to scale:",
                               f"the COM dips {100 * (R['Y_TD'] - R['Y_MID']):.1f} cm below its touchdown height and rises {100 * R['APEX']:.1f} cm in "
                               "flight. Bodies spaced apart.",
                               "Dark coil: the leg as a spring, from the COM to the foot (the centre of pressure); r = its length, L" +
                               H.sub("0", s) + " = 1 m."],
                   "label2", I["secondary"]))
    o.append(LB.credit(s, 12, fy + s(112), width=720))
    aria = ("Running bounce, five skeletons left to right: touchdown, midstance, toe-off, the apex of the flight, and the next "
            "touchdown. In each stance frame a dark coil runs from the centre of mass to the foot: it is full length at "
            "touchdown and toe-off and compressed at midstance, when the centre of mass is lowest. A blue centre-of-mass "
            "path dips to its lowest point at midstance and is highest at the flight apex. Brackets below the floor mark "
            f"the contact time, {R['tc'] * 1000:.0f} milliseconds, and the flight time, {R['T_FL'] * 1000:.0f} milliseconds.")
    return finish(VB, aria, s, o)


# ================================================================ svg #5  Fig. 4 the SLIP model
def fig5():
    p = "m9f5_"
    VB = (0, 0, 760, 560)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    R = LAB
    H_run, fr = body_fits("lab")
    k = 235.0                                                 # px per metre: L0 = 1 m
    hb, fy = k * H_run, 452.0
    o = [defs(p, s), floor_line(s, 10, 750, fy)]
    sub0 = H.sub("0", s)
    # ghost runner (same stance frames as Fig. 5) behind the model: the model keeps the COM and the foot point
    P1, P2 = fr["touchdown"], fr["midstance"]
    _, J0 = LB.draw("", s, P1, 0.0, fy, hb)
    sv1, J1 = LB.draw("", s, P1, 280.0 - J0["heel"][0], fy, hb)
    foot1, m1 = (J1["heel"][0], fy), J1["com"]
    _, J0 = LB.draw("", s, P2, 0.0, fy, hb)
    sv2, J2 = LB.draw("", s, P2, 0.0, fy, hb)
    sv2, J2 = LB.draw("", s, P2, 590.0 - (J2["heel"][0] + J2["toe"][0]) / 2, fy, hb)
    foot2, m2 = ((J2["heel"][0] + J2["toe"][0]) / 2, fy), J2["com"]
    o.append(f'<g opacity="0.38">{sv1}{sv2}</g>')
    # ---- left: touchdown
    o.append(spring(s, m1, foot1, n=7, amp=8.0, w=2.4))
    o.append(dot(s, *foot1, I["primary"], 5))
    v = (R["X_TD"] * 0 + 4.0, -(-0.7))                         # screen: +x right, +y down; v0 = (4.0, -0.7) m/s
    sc = 18.0
    o.append(white_under(s, *m1, m1[0] + sc * v[0], m1[1] + sc * v[1], 5) + H.arrow(s, p, *m1, m1[0] + sc * v[0], m1[1] + sc * v[1], "dim"))
    o.append(H.label(s, m1[0] + sc * v[0] - s(2), m1[1] + sc * v[1] + s(18), it("v") + sub0, "label", I["secondary"], "end"))
    wg = 40.0
    o.append(white_under(s, m1[0], m1[1], m1[0], m1[1] + wg, 5) + H.arrow(s, p, m1[0], m1[1], m1[0], m1[1] + wg, "load"))
    o.append(H.label(s, m1[0] - s(8), m1[1] + wg, it("mg"), "label2", O["load"], "end"))
    o.append(mass(s, *m1, 9))
    o.append(H.label(s, m1[0] - s(14), m1[1] - s(10), it("m"), "label", anchor="end"))
    o.append(angle_arc(s, foot1[0], foot1[1], 62, 180, 250))
    a = math.radians(215)
    o.append(H.label(s, foot1[0] + 82 * math.cos(a) - s(2), foot1[1] + 82 * math.sin(a) + s(5), it("α") + sub0, "label", O["geometry"], "end"))
    o.append(dline(s, foot1[0] - 120, fy, foot1[0], fy, O["dim"], "leader"))
    mid = pt(m1, foot1, 0.5)
    o.append(H.label(s, mid[0] - s(26), mid[1] - s(4), it("L") + sub0, "label", O["geometry"], "end"))
    o.append(H.label(s, mid[0] - s(26), mid[1] + s(16), it("k") + H.sub("leg", s), "label", O["geometry"], "end"))
    o.append(H.label(s, 20, 26, "touchdown: spring at rest length", "label"))
    o.append(H.label(s, 20, 44, "the leg meets the ground at the angle of attack α" + sub0, "label2", I["secondary"]))
    # ---- right: midstance
    o.append(dline(s, foot2[0], fy, foot2[0], fy - k * 1.0, O["dim"], "ref"))
    o.append(spring(s, m2, foot2, n=7, amp=8.0, w=2.4))
    o.append(dot(s, *foot2, I["primary"], 5))
    fs = (R["FZ_MID"] / W_N) * wg                              # spring force k (L0 - r), vertical at midstance
    xo = m2[0] + 26
    o.append(white_under(s, xo, m2[1], xo, m2[1] - fs, 5) + H.arrow(s, p, xo, m2[1], xo, m2[1] - fs, "force"))
    o.append(H.label(s, xo + s(8), m2[1] - fs * 0.55, it("k") + H.sub("leg", s) + "(" + it("L") + sub0 + " − " + it("r") + ")", "label2", O["force"]))
    o.append(white_under(s, xo, m2[1], xo, m2[1] + wg, 5) + H.arrow(s, p, xo, m2[1], xo, m2[1] + wg, "load"))
    o.append(H.label(s, xo + s(8), m2[1] + wg * 0.8, it("mg"), "label2", O["load"]))
    o.append(mass(s, *m2, 9))
    o.append(H.label(s, m2[0] - s(14), m2[1] - s(10), it("m"), "label", anchor="end"))
    xd = foot2[0] - 56
    o.append(H.line(s, xd, foot2[1], xd, m2[1], O["geometry"], "ref", extra=f'marker-start="url(#{p}a_geometry)" marker-end="url(#{p}a_geometry)"'))
    o.append(H.label(s, xd - s(6), (foot2[1] + m2[1]) / 2 + s(4), it("r") + f" = {R['R_MID']:.2f} m", "label", O["geometry"], "end"))
    o.append(H.label(s, foot2[0] - s(8), fy - k * 1.0 - s(4), it("L") + sub0 + " = 1 m", "label2", I["secondary"], "end"))
    o.append(angle_arc(s, foot2[0], foot2[1], 40, -90, 0))
    o.append(f'<path d="M{foot2[0] + 12:.1f},{fy:.1f} v-12 h-12" fill="none" stroke="{O["geometry"]}" stroke-width="{s(1.4):.2f}"/>')
    o.append(H.label(s, foot2[0] + 48, fy - s(7), it("φ") + " = 90°", "label", O["geometry"]))
    o.append(H.label(s, 430, 26, "midstance: spring compressed", "label"))
    o.append(H.label(s, 430, 44, "r < L" + sub0 + ", the leg is vertical", "label2", I["secondary"]))
    o.append(lines(s, 20, fy + s(28), [f"Lab 1 jog: m = 70 kg, L{sub0} = 1 m, α{sub0} = 70°, v{sub0} = (4.0, −0.7) m/s, "
                                       f"k = {R['k'] / 1000:.0f} kN/m; midstance spring force {R['FZ_MID'] / W_N:.1f} mg.",
                                       "Faint skeleton: the runner the model stands for. The mass sits at its COM,",
                                       "the point foot at its centre of pressure."], "label2", I["secondary"]))
    o.append(LB.credit(s, 20, fy + s(88), width=720))
    aria = ("The spring-loaded inverted pendulum drawn over a faint running skeleton. Left, at touchdown: a point mass m sits "
            "at the centre of mass atop a massless spring leg of rest length L0 and stiffness k leg, planted at the "
            "angle of attack alpha 0, 70 degrees to the ground; a blue velocity arrow v0 points forward and slightly "
            "down and a brown arrow mg points down. Right, at midstance: the leg is vertical, the spring is compressed "
            f"to length r, {R['R_MID']:.2f} metres against the 1 metre rest length, and the angle phi to the ground is 90 degrees; "
            f"a red arrow of {R['FZ_MID'] / W_N:.1f} times the weight, the spring force k leg times L0 minus r, points up and the brown "
            "weight arrow mg points down.")
    return finish(VB, aria, s, o)


# ================================================================ svg #6  Fig. 5 vertical GRF
def walk_template(s_):
    """Module 8 Lab 3's assumed walking F_y over the stance fraction, in body weights: peaks 1.10 W at 28 % and 72 %,
    0.75 W at midstance (module08 text), stance = 62 % of the stride."""
    sh = lambda q: np.sin(np.pi * q) ** 0.40 * (1 - 0.245 * np.cos(4 * np.pi * (q - 0.5)))   # noqa: E731
    ss = np.linspace(0, 1, 6001)
    return sh(s_) / (2 * 0.62 * float(trapz(sh(ss), ss)))


_sw = np.linspace(0, 1, 601)
_fw = walk_template(_sw)
assert (round(float(_fw.max()), 2), round(float(_fw[300]), 2), round(float(_sw[int(np.argmax(_fw[:300]))]), 2)) == (1.10, 0.75, 0.28)


def _plot_hover(ax, rows):
    return H.hover_attr([round(v, 2) for v in ax.box], rows)


def fig6():
    p = "m9f6_"
    VB = (0, 0, 760, 450)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    R = LAB
    H_run, fr = body_fits("lab")
    hb, fy = 270.0, 350.0
    k = hb / H_run
    o = [defs(p, s)]
    # ---- left: the midstance frame of the run, the leg spring and the forces on the body
    P = fr["midstance"]
    _, J0 = LB.draw("", s, P, 0.0, fy, hb)
    svg, J = LB.draw("", s, P, 100.0 - J0["bbox"][0], fy, hb)
    o.append(floor_line(s, 10, 300, fy))
    o.append(svg)
    com = J["com"]
    foot = ((J["heel"][0] + J["toe"][0]) / 2, fy)
    o.append(spring(s, com, foot))
    bw = 44.0                                              # px per body weight
    fz = R["FZ_MID"] / W_N
    ax_ = foot[0] + 40
    o.append(white_under(s, ax_, fy, ax_, fy - fz * bw, 5) + H.arrow(s, p, ax_, fy, ax_, fy - fz * bw, "reaction"))
    o.append(H.label(s, ax_ + s(8), fy - fz * bw * 0.5, f"F{H.sub('z', s)}", "label", anchor="start"))
    o.append(H.label(s, ax_ + s(8), fy - fz * bw * 0.5 + s(16), f"{fz:.1f} mg", "label2", I["secondary"]))
    wx = com[0] + 38
    o.append(white_under(s, wx, com[1], wx, com[1] + bw, 5) + H.arrow(s, p, wx, com[1], wx, com[1] + bw, "load"))
    o.append(H.label(s, wx + s(8), com[1] + bw * 0.6, "mg", "label", O["load"]))
    o.append(H.com_mark(s, *com))
    o.append(H.label(s, 12, 24, "midstance of the SLIP run (Lab 1, k = 15 kN/m):", "label2", I["secondary"]))
    o.append(H.label(s, 12, 40, f"leg vertical, spring compressed from 1 m to r = {R['R_MID']:.2f} m", "label2", I["secondary"]))
    o.append(H.label(s, foot[0], fy + s(20), "foot (centre of pressure)", "label2", anchor="middle"))
    o.append(LB.credit(s, 12, fy + s(52), width=720))
    # ---- right: vertical GRF against percent of stance
    ax = Ax((380.0, 90.0, 735.0, 330.0), (0, 100), (0, 3))
    xt = [(v, f"{v}") for v in (0, 25, 50, 75, 100)]
    yt = [(v, f"{v}") for v in (0, 1, 2, 3)]
    o += axes(s, ax, xt, yt, "percent of stance", "vertical GRF (body weights)", ylab_x=ax.x0 - 40)
    o.append(H.line(s, ax.x0, ax.Y(1), ax.x1, ax.Y(1), I["secondary"], "ref", dash=H.DASH_REF))
    tq = R["t"] / R["tc"] * 100
    fr_run = R["Fz"] / W_N
    o.append(curve(s, ax, tq[::18], fr_run[::18], S0, "curve"))
    xs_w = _sw * 100
    o.append(curve(s, ax, xs_w[::6], _fw[::6], S1, "curve_multi", DASH_SER))
    i_pk = int(np.argmax(fr_run))
    o.append(dot(s, ax.X(tq[i_pk]), ax.Y(fr_run[i_pk]), S0))
    o.append(H.label(s, ax.X(tq[i_pk]) + s(10), ax.Y(fr_run[i_pk]) - s(6), f"peak {R['PK']:.1f} BW", "label2"))
    o.append(H.label(s, ax.X(50), ax.Y(1) - s(7), "1 BW: standing", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.X(50), ax.Y(1.8), "running: single hump", "label2", anchor="middle"))
    o.append(H.label(s, ax.X(50), ax.Y(0.45), "walking: double hump", "label2", anchor="middle"))
    o.append(H.label(s, ax.X(50), ax.Y(0.45) + s(15), "dips below 1 BW at midstance", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.X(96), ax.Y(2.55), f"t{H.sub('c', s)} = {R['tc'] * 1000:.0f} ms", "label2", anchor="end"))
    o += legend(s, ax.x0 + s(6), ax.top - s(30), [(S0, None, "running (SLIP)"), (S1, DASH_SER, "walking (Module 8)")])
    rows = []
    for q in range(0, 101, 1):
        yr = float(np.interp(q, tq, fr_run))
        yw = float(np.interp(q, xs_w, _fw))
        rows.append([ax.X(q), [ax.Y(yr), ax.Y(yw)], f"{q} % of stance: running {yr:.2f} BW, walking {yw:.2f} BW"])
    aria = ("Left: a skeleton at midstance of a run, the leg drawn as a dark coil from the centre of mass to the foot, "
            f"compressed to {R['R_MID']:.2f} metres. A black arrow of {fz:.1f} body weights, the vertical ground reaction "
            "force, points up beside the leg; a brown arrow of one body weight, the weight mg, points down from the centre of "
            "mass. Right: vertical ground reaction force in body weights against percent of stance. Running (red, solid) is "
            f"a single hump that peaks at {R['PK']:.1f} body weights at midstance and lasts {R['tc'] * 1000:.0f} milliseconds. "
            "Walking (blue, dashed) is a double hump with peaks of 1.10 body weights at 28 and 72 percent that dips to 0.75 "
            "body weights at midstance, below the 1 body weight line.")
    return finish(VB, aria, s, o, _plot_hover(ax, rows))


# ================================================================ svg #7  Fig. 6 flight parabola and the Froude ceiling
VXJ, VYJ = 4.0, 0.9                                      # the jog takeoff of line 160
TFJ, HAJ, DFJ = 2 * VYJ / G, VYJ ** 2 / (2 * G), 2 * VXJ * VYJ / G
assert (round(TFJ, 2), round(100 * HAJ), round(DFJ, 1)) == (0.18, 4, 0.7)                    # line 160, Prop 4.1
L0_FR = 1.0
assert round(math.sqrt(G * L0_FR), 1) == 3.1 and round(math.sqrt(0.5 * G * L0_FR), 1) == 2.2  # line 172


def fig7():
    p = "m9f7_"
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    o = [defs(p, s)]
    # ---- left: the ballistic COM path at one scale for x and y (so the shallow arc is shown as it is)
    k = 380.0                                              # px per metre
    x0, yt = 28.0, 252.0
    X = lambda m: x0 + k * m                               # noqa: E731
    Y = lambda m: yt - k * m                               # noqa: E731
    ts = np.linspace(0, TFJ, 61)
    hy = lambda t_: VYJ * t_ - 0.5 * G * t_ * t_           # noqa: E731
    px = [(X(VXJ * t_), Y(hy(t_))) for t_ in ts]
    o.append(dline(s, x0 - 14, yt, X(DFJ) + 14, yt, I["secondary"], "ref"))
    o.append(H.label(s, x0 - 14, yt + s(16), "takeoff height", "label2", I["secondary"]))
    o.append(poly(s, px, O["geometry"], "curve"))
    xa, ya = X(VXJ * TFJ / 2), Y(HAJ)
    o.append(H.line(s, xa, yt, xa, ya, O["geometry"], "ref",
                    extra=f'marker-start="url(#{p}a_geometry)" marker-end="url(#{p}a_geometry)"'))
    sc = 20.0                                              # px per m/s, velocity arrows only
    for xs_, vy, nm in ((X(0), VYJ, "to"), (X(DFJ), -VYJ, "td")):
        ex, ey = xs_ + sc * VXJ, yt - sc * vy
        o.append(white_under(s, xs_, yt, ex, ey, 5) + H.arrow(s, p, xs_, yt, ex, ey, "dim"))
        o.append(H.label(s, ex + s(4), ey - s(6) if vy > 0 else ey + s(16), it("v") + H.sub(nm, s), "label2",
                         I["secondary"], "start"))
    o.append(H.com_mark(s, X(0), yt))
    o.append(H.com_mark(s, X(DFJ), yt))
    o.append(H.com_mark(s, xa, ya))
    o.append(H.label(s, xa, ya - s(40), f"apex: {it('v')}{H.sub('y', s)}² / 2{it('g')} = {100 * HAJ:.1f} cm", "label2", O["geometry"], "middle"))
    o.append(leader(s, xa, ya - s(34), xa, ya - s(10), O["geometry"]))
    yr_ = yt + 46
    o.append(H.line(s, X(0), yr_, X(DFJ), yr_, O["dim"], "ref",
                    extra=f'marker-start="url(#{p}a_dim)" marker-end="url(#{p}a_dim)"'))
    o.append(H.label(s, X(DFJ / 2), yr_ + s(18), f"range {it('v')}{H.sub('x', s)} {it('t')}{H.sub('f', s)} = {DFJ:.2f} m",
                     "label2", anchor="middle"))
    o.append(H.label(s, X(DFJ / 2), yr_ + s(36),
                     f"flight time {it('t')}{H.sub('f', s)} = 2{it('v')}{H.sub('y', s)} / {it('g')} = {TFJ:.2f} s",
                     "label2", anchor="middle"))
    o.append(H.label(s, 14, 26, "flight: the COM is a projectile (Prop 2.3)", "label"))
    o.append(H.label(s, 14, 44, f"jog takeoff {it('v')}{H.sub('x', s)} = {VXJ:g} m/s, {it('v')}{H.sub('y', s)} = {VYJ} m/s; "
                     "x and y to one scale", "label2", I["secondary"]))
    o.append(H.label(s, 14, 60, "grey arrows: velocity, length proportional to speed", "label2", I["secondary"]))
    hl = [[X(VXJ * t_), Y(hy(t_)),
           f"t = {t_:.3f} s: {VXJ * t_:.2f} m forward, {100 * hy(t_):.1f} cm above takeoff"] for t_ in ts]
    boxl = [round(v, 2) for v in (x0 - 14, 80.0, X(DFJ) + 14, yr_ + 40)]
    # ---- right: vault force against the Froude number (Prop 4.2)
    ax = Ax((470.0, 100.0, 735.0, 300.0), (0, 1.1), (0, 1.05))
    o.append(f'<rect x="{ax.X(0):.2f}" y="{ax.top:.2f}" width="{ax.X(0.5) - ax.X(0):.2f}" height="{ax.y0 - ax.top:.2f}" '
             f'fill="{BOXFILL}"/>')
    o.append(f'<rect x="{ax.X(0.5):.2f}" y="{ax.top:.2f}" width="{ax.X(1.1) - ax.X(0.5):.2f}" height="{ax.y0 - ax.top:.2f}" '
             f'fill="{S1}" fill-opacity="0.10"/>')
    xt = [(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1.0)]
    yt_ = [(v, f"{v:g}") for v in (0, 0.5, 1.0)]
    o += axes(s, ax, xt, yt_, f"Froude number Fr = {it('v')}² / ({it('g')}{it('L')}{H.sub('0', s)})",
              f"vault force {it('F')}{H.sub('z', s)} / {it('mg')}", ylab_x=ax.x0 - 40)
    fr_ = np.linspace(0, 1.0, 41)
    o.append(curve(s, ax, fr_, 1 - fr_, S0, "curve"))
    o.append(H.line(s, ax.X(0.5), ax.top, ax.X(0.5), ax.y0, I["secondary"], "ref", dash=H.DASH_REF))
    o.append(dot(s, ax.X(0.5), ax.Y(0.5), O["flag"], 5))
    o.append(dot(s, ax.X(1.0), ax.Y(0.0), S0, 5))
    o.append(H.label(s, ax.X(0.5) - s(8), ax.Y(0.22), "Fr ≈ 0.5: humans", "label2", anchor="end"))
    o.append(H.label(s, ax.X(0.5) - s(8), ax.Y(0.22) + s(15), "switch to running", "label2", anchor="end"))
    o.append(H.label(s, ax.X(1.09), ax.Y(0.50), f"Fr = 1: {it('F')}{H.sub('z', s)} = 0", "label2", anchor="end"))
    o.append(H.label(s, ax.X(1.09), ax.Y(0.41), "ceiling, 3.1 m/s", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(0.25), ax.top + s(18), "walking: vault", "label2", anchor="middle"))
    o.append(H.label(s, ax.X(0.8), ax.top + s(18), "running: bounce", "label2", anchor="middle"))
    # speed scale on top (L0 = 1 m): v = sqrt(Fr g L0)
    for f_ in (0.25, 0.5, 0.75, 1.0):
        o.append(H.line(s, ax.X(f_), ax.top, ax.X(f_), ax.top - 5, I["axis"], "leader"))
        o.append(H.label(s, ax.X(f_), ax.top - s(9), f"{math.sqrt(f_ * G * L0_FR):.1f}", "tick", I["secondary"], "middle"))
    o.append(H.label(s, ax.X(0), ax.top - s(26), f"speed {it('v')} for {it('L')}{H.sub('0', s)} = 1 m (m/s)", "label2",
                     I["secondary"]))
    rows = [[ax.X(f_), ax.Y(1 - f_), f"Fr = {f_:.2f} (v = {math.sqrt(f_ * G * L0_FR):.2f} m/s for L0 = 1 m): Fz = {1 - f_:.2f} mg"]
            for f_ in np.linspace(0, 1.0, 101)]
    o.append(H.label(s, 14, 380, f"Prop 4.1: t{H.sub('f', s)} = {TFJ:.2f} s, apex {100 * HAJ:.1f} cm, range {DFJ:.2f} m.   "
                     f"Prop 4.2: F{H.sub('z', s)} = mg (1 − Fr).", "label2", I["secondary"]))
    aria = ("Left: the ballistic path of the centre of mass in flight, drawn with one scale for both axes. From takeoff, with "
            f"velocity {VXJ:g} metres per second forward and {VYJ} up, the blue path rises only {100 * HAJ:.1f} centimetres to its "
            f"apex and lands {DFJ:.2f} metres on, after a flight time of {TFJ:.2f} seconds; grey arrows show the takeoff and "
            "touchdown velocities. Right: the walking vault's midstance force over body weight against the Froude number is "
            "the straight line 1 minus Fr, falling from 1 at Fr 0 to 0 at Fr 1, the ceiling at 3.1 metres per second for a "
            "1 metre leg. A dashed line at Fr 0.5 marks where humans switch from walking to running.")
    return finish(VB, aria, s, o, H.hover_attr([(boxl, hl), ([round(v, 2) for v in ax.box], rows)]))


# ================================================================ svg #9  Fig. 8 jump height from takeoff velocity
M_J, FPK, TP = 70.0, 2.5, 0.30                            # Lab 2 (lines 376-377)
_TJ = np.linspace(0, TP, 400)


def jump_profile(front):
    """Lab 2: same-peak force shape in body weights; front < 1 shifts force earlier (line 389)."""
    return 1.0 + (FPK - 1.0) * np.sin(np.pi * (_TJ / TP) ** front) ** 1.55


def jump_height(f_bw):
    """Lab 2: net impulse -> takeoff speed -> h = v0^2 / 2g.  Returns (h in m, net impulse in N s, v0)."""
    imp = float(trapz((f_bw - 1.0) * M_J * G, _TJ))
    v0 = imp / M_J
    return v0 * v0 / (2 * G), imp, v0


_hs, _is, _vs = jump_height(jump_profile(1.0))
_hc, _ic, _vc = jump_height(jump_profile(0.8))
assert (round(100 * _hs, 1), round(100 * _hc, 1)) == (30.0, 32.0)                                  # lines 220, 222, 399
assert (round(_is, 1), round(_ic, 1)) == (169.9, 175.5)                                            # line 222
assert (round(100 * (_ic / _is - 1), 1), round(100 * (_hc / _hs - 1), 1)) == (3.3, 6.7)            # line 222
F_NET, D_PUSH = 515.0, 0.40                               # line 218: mean net force and push-off distance
V0_J = math.sqrt(2 * F_NET * D_PUSH / M_J)
H_JUMP = V0_J ** 2 / (2 * G)
assert round(V0_J, 1) == 2.4 and round(100 * H_JUMP) == 30                                         # line 218


def _jump_poses():
    """Crouch (the kit's cmj_crouch scaled so the COM rises d = 0.40 m to the takeoff), takeoff on the toes with
    the arms up.  The text states no stature: 1.75 m (course reference)."""
    up = dict(hip=0, knee=0, contact=None, ankle=-45, shoulder=125, elbow=0)
    take = LB.pose(near=dict(up), far=dict(up), anchor=("toe", "near"))
    _, Jt = LB.draw("", _S1, take, 0.0, 0.0, 1.0)
    com_t = Jt["floor_y"] - Jt["com"][1]

    def crouch(a):
        d = dict(hip=120 * a, knee=120 * a, shoulder=-60 * a, elbow=10 * a)
        return LB.pose(pelvis=30 * a, trunk=20 * a, near=dict(d), far=dict(d), anchor=("heel", "near"))

    def dd(a):
        _, J = LB.draw("", _S1, crouch(a), 0.0, 0.0, 1.0)
        return (com_t - (J["floor_y"] - J["com"][1])) * H_M - D_PUSH
    a = _bisect(dd, 0.3, 1.0)
    return crouch(a), take, a


def fig9():
    p = "m9f9_"
    VB = (0, 0, 840, 440)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    P_c, P_t, a_c = _jump_poses()
    hb, fy = 200.0, 335.0
    k = hb / H_M                                           # px per metre
    o = [defs(p, s), floor_line(s, 8, 520, fy)]
    # crouch
    _, J0 = LB.draw("", s, P_c, 0.0, fy, hb)
    svg_c, Jc = LB.draw("", s, P_c, 14.0 - J0["bbox"][0], fy, hb)
    # takeoff, on the toes (anchor = toe at the floor)
    _, J0 = LB.draw("", s, P_t, 0.0, fy, hb)
    svg_t, Jt = LB.draw("", s, P_t, Jc["bbox"][2] + 70.0 - J0["bbox"][0], fy, hb)
    # apex: the takeoff pose raised by h (the COM rises h above its takeoff height)
    _, J0 = LB.draw("", s, P_t, 0.0, fy, hb)
    xa = Jt["bbox"][2] + 54.0 - J0["bbox"][0]
    svg_a, Ja = LB.draw("", s, P_t, xa, fy - k * H_JUMP, hb)
    o += [svg_c, svg_t, svg_a]
    cc, ct, ca = Jc["com"], Jt["com"], Ja["com"]
    for J in (Jc, Jt, Ja):
        o.append(H.com_mark(s, *J["com"]))
    # push-off distance d: crouch COM height to takeoff COM height
    xd = Jc["bbox"][2] + 30.0
    o.append(dline(s, cc[0] + s(8), cc[1], xd + 14, cc[1], I["secondary"], "leader"))
    o.append(dline(s, ct[0] - s(8), ct[1], xd - 14, ct[1], I["secondary"], "leader"))
    o.append(H.line(s, xd, cc[1], xd, ct[1], O["geometry"], "ref",
                    extra=f'marker-start="url(#{p}a_geometry)" marker-end="url(#{p}a_geometry)"'))
    o.append(H.label(s, xd - s(6), (cc[1] + ct[1]) / 2 + s(4), it("d") + f" = {D_PUSH:.2f} m", "label2", O["geometry"], "end"))
    # height h: takeoff COM height to apex COM height
    xh = Ja["bbox"][2] + 22.0
    o.append(dline(s, ct[0] + s(8), ct[1], xh + 12, ct[1], I["secondary"], "leader"))
    o.append(dline(s, ca[0] + s(8), ca[1], xh + 12, ca[1], I["secondary"], "leader"))
    o.append(H.line(s, xh, ct[1], xh, ca[1], O["geometry"], "ref",
                    extra=f'marker-start="url(#{p}a_geometry)" marker-end="url(#{p}a_geometry)"'))
    o.append(H.label(s, xh + s(8), (ct[1] + ca[1]) / 2 + s(4), it("h") + f" = {100 * H_JUMP:.0f} cm", "label2", O["geometry"]))
    # forces in the crouch frame: ground force beside the feet, weight at the COM
    bw = 36.0
    fz = (F_NET + M_J * G) / (M_J * G)
    fxp = (Jc["heel"][0] + Jc["toe"][0]) / 2 - 40
    o.append(white_under(s, fxp, fy, fxp, fy - fz * bw, 5) + H.arrow(s, p, fxp, fy, fxp, fy - fz * bw, "reaction"))
    o.append(H.label(s, fxp - s(6), fy - fz * bw / 2 + s(4), f"{it('F')}{H.sub('z', s)}", "label", anchor="end"))
    # takeoff velocity
    vs = 28.0
    o.append(white_under(s, ct[0], ct[1] - s(8), ct[0], ct[1] - s(8) - vs * V0_J, 5)
             + H.arrow(s, p, ct[0], ct[1] - s(8), ct[0], ct[1] - s(8) - vs * V0_J, "dim"))
    o.append(H.label(s, ct[0] + s(8), ct[1] - s(8) - vs * V0_J * 0.55, it("v") + H.sub("0", s), "label", I["secondary"]))
    o.append(H.label(s, (Jc["bbox"][0] + Jc["bbox"][2]) / 2, fy + s(20), "push-off", "label2", anchor="middle"))
    o.append(H.label(s, (Jc["bbox"][0] + Jc["bbox"][2]) / 2, fy + s(35), "from the crouch", "label2", I["secondary"], "middle"))
    o.append(H.label(s, (Jt["bbox"][0] + Jt["bbox"][2]) / 2, fy + s(20), "takeoff", "label2", anchor="middle"))
    o.append(H.label(s, (Ja["bbox"][0] + Ja["bbox"][2]) / 2, fy + s(20), "apex", "label2", anchor="middle"))
    o.append(H.label(s, 14, 24, f"push-off: mean net force {F_NET:.0f} N over {it('d')} = {D_PUSH:.2f} m, {M_J:.0f} kg "
                     f"(mean {it('F')}{H.sub('z', s)} = {fz:.2f} {it('mg')})", "label2", I["secondary"]))
    o.append(H.label(s, 14, 40, f"{it('v')}{H.sub('0', s)} = {V0_J:.1f} m/s, {it('h')} = {it('v')}{H.sub('0', s)}² / 2{it('g')} = "
                     f"{100 * H_JUMP:.0f} cm", "label2", I["secondary"]))
    # ---- right: Lab 2 force-time curves
    ax = Ax((580.0, 110.0, 825.0, 305.0), (0, TP), (0, 3))
    xt = [(v, f"{v:.2f}") for v in (0, 0.1, 0.2, 0.3)]
    yt = [(v, f"{v}") for v in (0, 1, 2, 3)]
    o += axes(s, ax, xt, yt, "push-off time (s)", "vertical force (body weights)", ylab_x=ax.x0 - 38)
    o.append(H.line(s, ax.x0, ax.Y(1), ax.x1, ax.Y(1), I["secondary"], "ref", dash=H.DASH_REF))
    fs, fc = jump_profile(1.0), jump_profile(0.8)
    o.append(curve(s, ax, _TJ[::5], fs[::5], S1, "curve"))
    o.append(curve(s, ax, _TJ[::5], fc[::5], S0, "curve"))
    o.append(H.label(s, ax.x1, ax.Y(1) + s(15), "1 BW: body weight", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(0.03), ax.Y(2.88), "CMJ: " + f"{100 * _hc:.1f} cm", "label", anchor="start"))
    o.append(H.label(s, ax.X(0.03), ax.Y(2.88) + s(15), f"{_ic:.1f} N s", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(0.30), ax.Y(2.88), "SJ: " + f"{100 * _hs:.1f} cm", "label", anchor="end"))
    o.append(H.label(s, ax.X(0.30), ax.Y(2.88) + s(15), f"{_is:.1f} N s", "label2", I["secondary"], "end"))
    o += legend(s, ax.x0 - s(20), ax.top - s(50), [(S0, None, "CMJ: countermovement jump")])
    o += legend(s, ax.x0 - s(20), ax.top - s(32), [(S1, None, "SJ: squat jump")])
    rows = [[ax.X(t_), [ax.Y(c), ax.Y(q)], f"t = {t_:.3f} s: CMJ {c:.2f} BW, SJ {q:.2f} BW"]
            for t_, c, q in zip(_TJ, fc, fs)]
    o.append(lines(s, 14, fy + s(50), [f"Right: Lab 2, same peak force {FPK} BW and duration {TP:.2f} s; CMJ is front-loaded "
                                f"(+{100 * (_ic / _is - 1):.1f} % impulse, +{100 * (_hc / _hs - 1):.1f} % height)."], "label2", I["secondary"]))
    o.append(LB.credit(s, 14, fy + s(70), width=800))
    aria = ("Left: a skeleton in the crouch from which the push-off starts, a second skeleton at takeoff, standing on the toes "
            f"with the arms up, and a third at the apex of the jump. The ground reaction force F z pushes up through the feet "
            f"over the push-off distance d, {D_PUSH:.2f} metres, the rise of the centre of mass from crouch to takeoff; the "
            f"takeoff velocity v0 is {V0_J:.1f} metres per second and the centre of mass then rises h, {100 * H_JUMP:.0f} "
            "centimetres, equal to v0 squared over 2 g. Right: vertical force in body weights against push-off time for two "
            f"jumps with the same 2.5 body-weight peak. The countermovement jump (red) is front-loaded: net impulse {_ic:.1f} newton "
            f"seconds and height {100 * _hc:.1f} centimetres. The squat jump (blue) peaks later: {_is:.1f} newton seconds and "
            f"{100 * _hs:.1f} centimetres.")
    return finish(VB, aria, s, o, H.hover_attr([round(v, 2) for v in ax.box], rows))


# ================================================================ svg #10  Fig. 9 muscle-tendon unit and tendon recoil
# Module 6 structural tendon (Eq. 2.3): A0 = 80 mm2, L0 = 250 mm, E_lin = 1.3 GPa, toe to x* = 7.5 mm.
K_LIN, X_STAR = 1.3e9 * 80e-6 / 0.250, 0.0075
assert round(K_LIN) == 416000 and round(K_LIN * X_STAR / 2) == 1560                      # module06 fig m06-8: 1.56 kN at x*


def f_load(x):
    x = np.asarray(x, dtype=float)
    return np.where(x <= X_STAR, K_LIN * x ** 2 / (2 * X_STAR), K_LIN * (x - X_STAR / 2))


def tendon_u(f_pk):
    xm = f_pk / K_LIN + X_STAR / 2
    g = np.linspace(0, xm, 20001)
    return xm, float(trapz(f_load(g), g))


_x4, _u4 = tendon_u(4000.0)
assert round(_x4 * 1e3, 1) == 13.4 and round(_u4, 1) == 20.2                              # line 234 (Module 6 K2)
X_PK, U_STORE = tendon_u(5000.0)
assert round(X_PK * 1e3) == 16 and round(U_STORE) == 31                                   # line 234
R_RES = 0.92                                                                              # line 232 / 234


def _unload(n, xg):
    """Unloading branch: the same peak force, then F = F_pk (F_load(x) / F_pk)^n (n > 1: it falls faster)."""
    return 5000.0 * (f_load(xg) / 5000.0) ** n


_XG = np.linspace(0, X_PK, 2001)
N_UN = _bisect(lambda n: float(trapz(_unload(n, _XG), _XG)) - R_RES * U_STORE, 1.0, 6.0)
U_RET = float(trapz(_unload(N_UN, _XG), _XG))
assert round(U_RET, 1) == 28.5 and round(U_STORE - U_RET, 1) == 2.5                       # line 234


def fig10():
    p = "m9f10_"
    VB = (0, 0, 840, 620)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    sc, ox, oy = 0.50, 10.0, 52.0
    P = lambda x, y: (ox + sc * (x - 20.0), oy + sc * (y - 290.0))                        # noqa: E731
    o = [defs(p, s)]
    art = inner_svg(read_art("Lower_leg_muscles_crop_fig21.svg"))
    assert 'id="Names"' not in art and "<text" not in art
    img = art_image("<svg>" + H.recolour(art, "injurymap") + "</svg>", (20, 290, 740, 905))
    o.append(f'<g transform="translate({ox:.1f} {oy:.1f}) scale({sc}) translate(-20 -290)">{img}</g>')
    # ---- the model beside the leg: muscle (contractile) in series with the tendon (a spring), fixed at the heel
    cx = 318.0
    ym0, ym1 = P(0, 560)[1], P(0, 745)[1]
    ys0, ys1 = P(0, 752)[1], P(0, 1030)[1]
    yh = P(0, F21["insertion"][1])[1]
    o.append(f'<ellipse cx="{cx:.1f}" cy="{(ym0 + ym1) / 2:.1f}" rx="{s(30):.1f}" ry="{(ym1 - ym0) / 2:.1f}" fill="{T["muscle"][0]}" '
             f'stroke="{T["muscle"][1]}" stroke-width="{s(1.4):.2f}"/>')
    o.append(spring(s, (cx, ys0), (cx, ys1), n=8, amp=9.0, col=O["geometry"], w=2.4))
    o.append(f'<rect x="{cx - s(36):.1f}" y="{ys1:.1f}" width="{s(72):.1f}" height="{yh - ys1 + s(2):.1f}" rx="{s(3):.1f}" '
             f'fill="{T["bone"][0]}" stroke="{T["bone"][1]}" stroke-width="{s(1.4):.2f}"/>')
    o.append(floor_line(s, cx - s(60), cx + s(60), yh + s(2)))
    # leaders from the art to the model
    mx, my = P(450, 600)
    o.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="{s(2.5):.1f}" fill="{T["muscle"][1]}"/>')
    o.append(leader(s, mx, my, cx - s(30), (ym0 + ym1) / 2, T["muscle"][1]))
    tx, ty = P(*F21["tendon_c"])
    o.append(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="{s(2.5):.1f}" fill="{O["geometry"]}"/>')
    o.append(leader(s, tx, ty, cx - s(9), ty, O["geometry"]))
    ix, iy = P(*F21["insertion"])
    o.append(f'<circle cx="{ix:.1f}" cy="{iy:.1f}" r="{s(3):.1f}" fill="{O["load"]}" stroke="#fff" stroke-width="{s(1):.2f}"/>')
    o.append(leader(s, ix, iy, cx - s(36), iy - s(2), O["load"]))
    # tendon force
    fx = cx + 22.0
    o.append(white_under(s, fx, ys1, fx, ys0 + 10, 5) + H.arrow(s, p, fx, ys1, fx, ys0 + 10, "force"))
    o.append(H.label(s, fx + s(8), ys1 - s(34), f"{it('F')} ≈ 5 kN", "label", O["force"]))
    o.append(H.label(s, fx + s(8), ys1 - s(18), "hard push-off", "label2", I["secondary"]))
    # labels
    o.append(H.label(s, cx + s(34), ys0 + s(38), "most of the leg spring " + it("k") + H.sub("leg", s), "label2", I["secondary"]))
    o.append(H.label(s, cx + s(38), (ym0 + ym1) / 2 - s(4), "calf muscle", "label", T["muscle"][1]))
    o.append(H.label(s, cx + s(38), (ym0 + ym1) / 2 + s(12), "(contractile)", "label2", I["secondary"]))
    o.append(H.label(s, cx + s(34), ys0 + s(6), "Achilles tendon", "label", O["geometry"]))
    o.append(H.label(s, cx + s(34), ys0 + s(22), "= a spring, in series", "label2", I["secondary"]))
    o.append(H.label(s, cx + s(44), yh + s(16), "heel (calcaneus)", "label2", O["load"]))
    o.append(H.label(s, 14, 24, "muscle-tendon unit: triceps surae through the Achilles tendon", "label"))
    o.append(H.label(s, 14, 42, "model beside the leg: muscle in series with a spring tendon", "label2", I["secondary"]))
    # ---- right: tendon force-elongation loop
    ax = Ax((560.0, 100.0, 825.0, 400.0), (0, 18), (0, 5.5))
    xt = [(v, f"{v}") for v in (0, 4, 8, 12, 16)]
    yt = [(v, f"{v}") for v in (0, 1, 2, 3, 4, 5)]
    o += axes(s, ax, xt, yt, "tendon elongation (mm)", "tendon force (kN)", ylab_x=ax.x0 - 36)
    xs = np.linspace(0, X_PK, 160)
    fl, fu = f_load(xs) / 1000, _unload(N_UN, xs) / 1000
    load = [(ax.X(x * 1e3), ax.Y(f)) for x, f in zip(xs, fl)]
    unl = [(ax.X(x * 1e3), ax.Y(f)) for x, f in zip(xs, fu)]
    pts = lambda q: " ".join(f"{a:.2f},{b:.2f}" for a, b in q)                              # noqa: E731
    base = [(ax.X(X_PK * 1e3), ax.Y(0)), (ax.X(0), ax.Y(0))]
    o.append(f'<polygon points="{pts(unl + base)}" fill="{S1}" fill-opacity="0.14"/>')
    o.append(f'<polygon points="{pts(load + unl[::-1])}" fill="{S2}" fill-opacity="0.40"/>')
    o.append(poly(s, load[::2] + [load[-1]], S0, "curve"))
    o.append(poly(s, unl[::2] + [unl[-1]], S1, "curve"))
    o.append(dot(s, ax.X(X_PK * 1e3), ax.Y(5.0), S0))
    o.append(H.label(s, ax.X(X_PK * 1e3) - s(8), ax.Y(5.0) - s(8), f"5 kN, {X_PK * 1e3:.1f} mm", "label2", anchor="end"))
    o.append(H.label(s, ax.X(0.4), ax.Y(4.5), f"loading: stores U = {U_STORE:.0f} J", "label2", anchor="start"))
    o.append(H.label(s, ax.X(0.4), ax.Y(4.5) + s(15), "(area under the red curve)", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(17.6), ax.Y(0.95), f"recoil returns {U_RET:.1f} J", "label2", S1, "end"))
    o.append(H.label(s, ax.X(17.6), ax.Y(0.95) + s(15), f"R = {R_RES}", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(0.4), ax.Y(3.55), f"loop: {U_STORE - U_RET:.1f} J lost as heat", "label2"))
    xl_ = 11.0e-3
    o.append(leader(s, ax.X(5.2), ax.Y(3.55) + s(4), ax.X(xl_ * 1e3), ax.Y((f_load(xl_) + _unload(N_UN, xl_)) / 2000), I["primary"]))
    o += legend(s, ax.x0 - s(40), ax.top - s(36), [(S0, None, "loading"), (S1, None, "unloading"), (S2, None, "heat loss", "band")])
    rows = [[ax.X(x * 1e3), [ax.Y(a), ax.Y(b)], f"{x * 1e3:.1f} mm: loading {a:.2f} kN, unloading {b:.2f} kN"]
            for x, a, b in zip(xs, fl, fu)]
    o.append(lines(s, ax.x0 - s(36), ax.y0 + s(72), ["Module 6 toe + linear tendon,",
                                                    f"k = {K_LIN / 1e3:.0f} kN/m, toe ends at x* = 7.5 mm.",
                                                    "Unloading branch (schematic):",
                                                    f"F = 5 kN × (F{H.sub('load', s)} / 5 kN)ⁿ, n = {N_UN:.2f},",
                                                    f"so that the energy returned is R U, R = {R_RES}."], "label2", I["secondary"]))
    cr = H.ATTRIBUTION["by-sa"].format(author="InjuryMap", title="Lower leg muscles.svg",
                                       changes="Lateral leg only; labels removed, cropped, overlays added.")
    o.append(H.credit(s, 14, 556, wrap(cr, 74)))
    aria = ("Left: the lateral view of the lower leg (InjuryMap art) with the calf muscle narrowing into the Achilles tendon "
            "that inserts on the heel bone. Beside it, a model: a red muscle ellipse in series with a blue coil spring, the "
            "tendon, fixed to the heel; leaders join muscle, tendon and heel to the art, and an arrow marks the 5 kilonewton "
            "tendon force of a hard running push-off. Right: tendon force in kilonewtons against elongation in millimetres. "
            f"The loading curve rises from zero through a toe region to 5 kilonewtons at {X_PK * 1e3:.1f} millimetres, storing "
            f"{U_STORE:.0f} joules. The unloading curve falls back below it; the area under it, {U_RET:.1f} joules, is returned "
            f"(resilience {R_RES}), and the thin loop between the two, {U_STORE - U_RET:.1f} joules, is lost as heat.")
    return finish(VB, aria, s, o, H.hover_attr([round(v, 2) for v in ax.box], rows))


FIGS = {
    10: ("Left: a lower leg with the calf muscle in series with the Ac", fig10),
    9: ("Left: a jumper crouches and pushes off with vertical force F", fig9),
    7: ("Left: the ballistic centre-of-mass parabola between takeoff ", fig7),
    2: ("Running: stance vault and flight pose with Winter proportion", fig2),
    3: ("A runner shown at touchdown, midstance, toe-off and flight. ", fig3),
    5: ("The spring-loaded inverted pendulum. Left: at touchdown a bo", fig5),
    6: ("Left: a runner at midstance with a vertical ground reaction ", fig6),
}

