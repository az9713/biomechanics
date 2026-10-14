"""Module 13, group `body_d`: problem figures D2-D7, D9, D10 and K10 (svg #31-36, 38, 39, 58), house style, 400 px.

Bodies are the posable Lynch skeleton (lynch_body.py); m13/body_main.py puts its defs on the page, this group only
<use>s them (it exposes no SHARED_DEFS).  The helpers (lab, lines, dim_h, credit, body_at ...) are copied from
m10/body_d.py on purpose: that file is edited by another group.  Stature 1.75 m (the text states none; course
reference).  Every number on a figure is computed here from the formula, constant or code the module states; the line
numbers (module13.html) stand beside it and every figure asserts its numbers against the text:
  D2  line 105-108: m = 70 kg, h = 0.17 m, f = 1.8 steps/s -> U = mgh = 117 J, P = mghf = 210 W, v_vert = hf = 0.31 m/s
  D3  line 125-128: W_tr = 412 N (0.60 m g), l_t = 0.346 m, d_m = 0.05 m, W_L = 196 N (20 kg), d_L = 0.40 m,
      phi = 60 deg -> d_tr = 0.300 m, F_m = 4040 N, F_comp = 4350 N; squat phi = 20 deg, d_L = 0.25 m -> 2530 N
  D4  line 146-148: m = 70 kg, v = 1.3 m/s, beta = 60 deg -> J = 2 m v sin(beta/2) = 91 N s
  D5  line 168-170: tau_resist = 2 N m, r = 0.035 m, mu_lid = 0.7 -> F_grip >= 82 N, tangential force 57 N
  D6  line 184-186: m = 70 kg, v = 1.0 m/s, theta = 10 deg -> P = m g v sin(theta) = 119 W (60 / 178 W at 5 / 15 deg)
  D7  line 90, 413, Appendix: m_up = 0.8 m = 56 kg, H = 0.40 m, v0 = 0.25 m/s, T_e = 0.4 s -> m_up g H = 220 J,
      m_up v0^2/2 = 1.8 J, 218 J; m_up v0 = 14 N s of m_up g T_e = 220 N s (about 6 %)
  D9  line 156, 305, 329, 421: l = 1.0 m, omega0 = sqrt(g/l) = 3.13 1/s, x0 = 0.05 m, xdot = 1.0 m/s -> xi = 0.37 m,
      reachable step L = 0.60 m, xdot_max = omega0 (L - x0) = 1.72 m/s
  D10 line 425: 10 kg bag (98.1 N) at d_b = 0.30 m -> 29.4 N m; W_tr = 412 N -> x_lean = 0.071 m
  K10 line 576-590: tau_young = 2.5 N m/kg x 70 kg = 175 N m, P_young = 250 W, m_up = 56 kg, h = 0.17 m ->
      88 / 84 / 63 / 48 / 47 % of the young reserve
Body art: Patrick J. Lynch (CC BY 2.5), through lynch_body.
"""
import math

import house as H
import lynch_body as LB
from m05.body import finish, it
from m05.plots_prob import Plot, label as plabel

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
BOX, GRID = "#f7f4ef", "#e6e6e6"
HM = 1.75                                    # m, stature (design value; the text states none)
UM = LB.H_U / HM                             # body units per metre
G = 9.81
M = 70.0


def close(v, ref, tol):
    assert abs(v - ref) <= tol * 1.0001, (v, ref)


# ---------------------------------------------------------------- drawing helpers (copied from m10/body_d.py)
def defs(p, s):
    return f"<defs>{H.markers(p, s)}</defs>"


def lab(s, x, y, text, size="label2", fill=I["primary"], anchor="start", extra=""):
    return H.label(s, x, y, text, size, fill, anchor, extra)


def lines(s, x, y, rows, size="label2", anchor="start", fill=None, lead=1.35):
    d = s(H.PX[size]) * lead
    return "".join(lab(s, x, y + i * d, t, size, fill or I["primary"], anchor) for i, t in enumerate(rows))


def sb(t, s, size="label2"):
    """Subscript plus a thin space, so a descender (p, g) never touches the next italic letter."""
    return H.sub(t, s, size) + " "


def sup(t, s, size="label2"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def accent(c, mark, dx, dy):
    """Italic letter with a spacing modifier drawn over it (Georgia has no combining marks in the SVG text path)."""
    return (f'<tspan font-style="italic">{c}</tspan><tspan dx="{dx}em" dy="{dy}em" font-style="normal">{mark}</tspan>'
            f'<tspan dy="{-dy}em"> </tspan>')


def dot_(c):
    return accent(c, "˙", -0.45, -0.2 if c == "θ" else -0.1)


def white_under(s, x1, y1, x2, y2, w=4):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#fff" '
            f'stroke-width="{s(w):.2f}" opacity="0.85"/>')


def vline(s, x, y1, y2, col=None, dash=H.DASH_REF, w="ref"):
    """Dashed reference line with a white under-stroke so it reads over the art."""
    return white_under(s, x, y1, x, y2) + H.line(s, x, y1, x, y2, col or O["dim"], w, dash=dash)


def seg(s, x1, y1, x2, y2, col=None, dash=H.DASH_REF, w="ref"):
    """Any dashed reference segment with a white under-stroke."""
    return white_under(s, x1, y1, x2, y2) + H.line(s, x1, y1, x2, y2, col or O["dim"], w, dash=dash)


def floor(s, x0, x1, y):
    return H.line(s, x0, y, x1, y, I["axis"], "axis")


def box(s, x, y, w, h, fill=BOX, stroke=None, extra=""):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" '
            f'stroke="{stroke or I["secondary"]}" stroke-width="{s(1):.2f}" {extra}/>')


def xi_mark(s, x, y, col=None):
    """Extrapolated COM: open circle (Module 7 line 190)."""
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(6):.2f}" fill="#fff" stroke="{col or I["primary"]}" '
            f'stroke-width="{s(2):.2f}"/>')


def contact_mark(s, x, y):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(4):.2f}" fill="{I["primary"]}" stroke="#fff" '
            f'stroke-width="{s(1.5):.2f}"/>')


def path_d(pts):
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts)


def arc_pts(cx, cy, r, a0, a1, n=24):
    """Screen angles in degrees: 0 = +x, + = clockwise (y down), -90 = up."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def arc_arrow(s, p, cx, cy, r, a0, a1, meaning):
    w = {"geometry": "geom", "dim": "ref"}.get(meaning, "force")
    pts = arc_pts(cx, cy, r, a0, a1)
    return (f'<path d="{path_d(pts)}" fill="none" stroke="#fff" stroke-width="{s(H.PX[w] + 2.5):.2f}" opacity="0.85"/>'
            f'<path d="{path_d(pts)}" fill="none" stroke="{O[meaning]}" stroke-width="{s(H.PX[w]):.2f}" '
            f'marker-end="url(#{p}a_{meaning})"/>')


def angle_arc(s, cx, cy, r, a0, a1, col=None):
    return (f'<path d="{path_d(arc_pts(cx, cy, r, a0, a1, 16))}" fill="none" stroke="{col or O["geometry"]}" '
            f'stroke-width="{s(H.PX["geom"]):.2f}"/>')


def dim_h(s, p, x1, x2, y, meaning="geometry", tick=5):
    col = O[meaning]
    return (H.arrow(s, p, x1, y, x2, y, meaning, both=True) + H.line(s, x1, y - s(tick), x1, y + s(tick), col, "leader")
            + H.line(s, x2, y - s(tick), x2, y + s(tick), col, "leader"))


def dim_v(s, p, x, y1, y2, meaning="geometry", tick=5):
    col = O[meaning]
    return (H.arrow(s, p, x, y1, x, y2, meaning, both=True) + H.line(s, x - s(tick), y1, x + s(tick), y1, col, "leader")
            + H.line(s, x - s(tick), y2, x + s(tick), y2, col, "leader"))


def credit(s, vb):
    """Lynch credit at the bottom of the viewBox, wrapped to its width (the wrap rule of LB.credit)."""
    w = vb[2] - s(12)
    t = H.ATTRIBUTION["by"].format(
        author="Patrick J. Lynch, medical illustrator",
        title="Skeleton lateral.svg” and “Skeleton whole body ant lat views.svg", licence="CC BY 2.5",
        changes="Recoloured, split into segments and reposed; arms from the anterior view.")
    n = max(20, int(w / (s(H.PX["credit"]) * 0.47)))
    nl, cur = 0, ""
    for wd in t.split():
        if cur and len(cur) + 1 + len(wd) > n:
            nl, cur = nl + 1, wd
        else:
            cur = (cur + " " + wd).strip()
    y = vb[1] + vb[3] - s(6) - nl * s(H.PX["credit"]) * 1.25
    return LB.credit(s, vb[0] + s(6), y, width=w)


def pvb(h):
    return (0, 0, 400, h), H.Scale(400, h, display_w=400)


def bvb(h):
    return (0, 0, 400, h), H.Scale(400, h, display_w=400, max_h=H.MAX_DISPLAY_H_BODY)


def body_at(p, s, P, x, fy, hgt, key="ankle"):
    """Draw pose P with its `key` joint at x, floor at fy. Returns (svg, J)."""
    _, J0 = LB.draw(p, s, P, 0.0, fy, hgt)
    return LB.draw(p, s, P, x - J0[key][0], fy, hgt)


def pose_com(P):
    tot = sum(m for _, m in P.com.values())
    return (sum(c[0] * m for c, m in P.com.values()) / tot, sum(c[1] * m for c, m in P.com.values()) / tot)


def bis(f, lo, hi, n=60):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


FIGS = {}

# ================================================================ svg #58  K10 which task fails first
TAU_YOUNG, P_YOUNG = 2.5 * M, 250.0          # young reserves (line 580)
M_UP = 0.8 * M                               # 56 kg
H_RISER, F_STEP = 0.17, 1.8                  # m, steps/s (Appendix; line 106)
K10_TASKS = (                                # (name, demand, reserve, kind) as the code of line 581-590
    ("rise, low chair (d = 0.28 m)", M_UP * G * 0.28, TAU_YOUNG, "torque"),
    ("climb stairs at 1.8 steps/s", M * G * H_RISER * F_STEP, P_YOUNG, "power"),
    ("rise, standard chair (d = 0.20 m)", M_UP * G * 0.20, TAU_YOUNG, "torque"),
    ("walk a 10° slope at 1.0 m/s", M * G * 1.0 * math.sin(math.radians(10)), P_YOUNG, "power"),
    ("rise, high firm chair (d = 0.15 m)", M_UP * G * 0.15, TAU_YOUNG, "torque"),
)
K10_ORDER = sorted(K10_TASKS, key=lambda t: -t[1] / t[2])
assert [t[0] for t in K10_ORDER] == [t[0] for t in K10_TASKS]
for (nm, dem, res, kd), ref in zip(K10_ORDER, (0.88, 0.84, 0.63, 0.48, 0.47)):          # line 576
    close(dem / res, ref, 0.005)


def fig58():
    p = "m13f58_"
    VB, s = pvb(372)
    P = Plot(s, (24, 64, 240, 322), (0.0, 1.0), (0.0, 1.0))
    o = []
    # legend: the two reserves (identity by swatch AND by the label, not colour alone)
    for i, (kind, txt) in enumerate((("torque", f"torque-limited: knee extensors, {TAU_YOUNG:.0f} N m"),
                                     ("power", f"power-limited: legs, {P_YOUNG:.0f} W"))):
        col = SER[0] if kind == "torque" else SER[1]
        y = 20 + i * 20
        o.append(f'<rect x="24" y="{y - 11:.2f}" width="{s(14):.2f}" height="{s(10):.2f}" fill="{col}"/>')
        o.append(plabel(s, 24 + s(20), y - 1, txt, "label2", I["primary"]))
    row, pts, boxes = 50.0, [], []
    y0 = 70.0
    for i, (nm, dem, res, kind) in enumerate(K10_ORDER):
        col = SER[0] if kind == "torque" else SER[1]
        v = dem / res
        yt = y0 + i * row
        o.append(plabel(s, 24 + s(8), yt + 13, nm, "label2", I["primary"]))
        xe = P.X(v)
        o.append(f'<rect x="{P.X(0):.2f}" y="{yt + 20:.2f}" width="{xe - P.X(0):.2f}" height="{s(20):.2f}" '
                 f'fill="{col}" rx="{s(2):.2f}"/>')
        o.append(plabel(s, P.X(1) + s(12), yt + 20 + s(14), f"{v:.2f}", "label", I["primary"]))
        unit = "N m" if kind == "torque" else "W"
        o.append(plabel(s, P.X(1) + s(12) + s(40), yt + 20 + s(14), f"{dem:.0f} of {res:.0f} {unit}", "label2", I["secondary"]))
        boxes.append(([24.0, yt, 396.0, yt + row - 2.0],
                      [[xe, yt + 20 + s(10), f"{nm}: fails at s = {v:.2f} ({dem:.1f} of {res:.0f} {unit})"]]))
    ya = P.y0
    o.append(H.line(s, P.X(0), P.y1, P.X(0), ya, I["axis"], "axis"))
    o.append(H.line(s, P.X(0), ya, P.X(1), ya, I["axis"], "axis"))
    o.append(seg(s, P.X(1), P.y1, P.X(1), ya, I["rule"]))
    for v in (0, 0.25, 0.5, 0.75, 1.0):
        o.append(H.line(s, P.X(v), ya, P.X(v), ya + 5, I["axis"], "leader"))
        o.append(plabel(s, P.X(v), ya + 19, f"{v:g}", "tick", I["secondary"], "middle"))
    o.append(plabel(s, (P.X(0) + P.X(1)) / 2, ya + 38, "reserve factor s at which margin = 1", "label", I["primary"], "middle"))
    o.append(plabel(s, P.X(1), P.y1 - s(4), "young adult", "label2", I["secondary"], "middle"))
    aria = ("Horizontal bars, one per everyday task, ordered from the first task to fail to the last. Each bar is the "
            "common reserve factor s at which the task's margin reaches 1, that is its demand divided by the young "
            "reserve. Red bars are torque-limited chair rises against 175 newton metres of knee extensor torque, blue bars "
            "are power-limited tasks against 250 watts of leg power. From the top: the low chair 0.88, stair climbing at "
            "1.8 steps per second 0.84, the standard chair 0.63, a 10 degree slope at 1 metre per second 0.48 and the "
            "high firm chair 0.47. Hovering a row reads its numbers.")
    return finish(VB, aria, s, o, extra=H.hover_attr(boxes))


FIGS[58] = (r'K10: which task fails first? (multi-margin sweep). As overal', fig58)


# ================================================================ svg #33  D4 turning impulse
V_WALK, BETA = 1.3, 60.0                     # m/s (Appendix), deg (line 146)
J_TURN = 2 * M * V_WALK * math.sin(math.radians(BETA / 2))
close(J_TURN, 91.0, 0.05)                    # line 146, 148


def fig33():
    p = "m13f33_"
    VB, s = pvb(236)
    o = [defs(p, s)]
    cx, cy, kv = 112.0, 206.0, 100.0         # COM before and after the turn (one point), px per m/s
    L = V_WALK * kv
    b = math.radians(BETA)
    v1 = (cx + L, cy)
    v2 = (cx + L * math.cos(b), cy - L * math.sin(b))
    dv = (v2[0] - v1[0], v2[1] - v1[1])
    dvl = math.hypot(*dv)
    close(dvl / kv, 2 * V_WALK * math.sin(b / 2), 1e-9)          # |dv| = 2 v sin(beta/2) = 1.3 m/s
    ud = (dv[0] / dvl, dv[1] / dvl)
    # the walker's path: in along v1, out along v2
    o.append(seg(s, 8, cy, cx, cy, I["rule"]))
    o.append(seg(s, v2[0], v2[1], v2[0] + 0.45 * (v2[0] - cx), v2[1] + 0.45 * (v2[1] - cy), I["rule"]))
    o.append(angle_arc(s, cx, cy, s(48), -BETA, 0))
    o.append(lab(s, cx + s(60) * math.cos(b / 2), cy - s(60) * math.sin(b / 2) + s(5), "β", "label", O["geometry"]))
    o.append(H.arrow(s, p, cx, cy, *v1, "geometry"))
    o.append(H.arrow(s, p, cx, cy, *v2, "geometry"))
    o.append(H.line(s, v1[0], v1[1], v2[0], v2[1], O["geometry"], "geom", dash=H.DASH_REF, extra=f'marker-end="url(#{p}a_geometry)"'))
    vv = lambda n: f'{it("v")}{sb(n, s)}'                                                 # noqa: E731
    o.append(lab(s, cx + L / 2, cy + s(20), f'{vv("1")} = {V_WALK} m/s', "label2", I["primary"], "middle"))
    o.append(lab(s, (cx + v2[0]) / 2 - s(8), (cy + v2[1]) / 2 - s(10), f'{vv("2")}', "label", I["primary"], "end"))
    mid = ((v1[0] + v2[0]) / 2, (v1[1] + v2[1]) / 2)
    o.append(lines(s, mid[0] + s(32), mid[1] + s(14), [f'Δ{it("v")} = {vv("2")} − {vv("1")}', f'|Δ{it("v")}| = {dvl / kv:.1f} m/s'],
                   fill=I["primary"]))
    # impulse at the COM, toward the inside of the turn (parallel to dv)
    ja = 78.0
    jt = (cx + ud[0] * ja, cy + ud[1] * ja)
    o.append(H.arrow(s, p, cx + ud[0] * s(10), cy + ud[1] * s(10), *jt, "force"))
    o.append(lab(s, jt[0] - s(8), jt[1] - s(4), f'{it("J")} = {it("m")}Δ{it("v")}', "label", O["force"], "end"))
    o.append(lab(s, jt[0] - s(8), jt[1] + s(13), "inward", "label2", I["primary"], "end"))
    o.append(H.com_mark(s, cx, cy))
    o.append(lab(s, cx - s(10), cy + s(20), "COM, top view", "label2", I["primary"], "end"))
    x0 = 244.0
    o.append(lines(s, x0, 26, [f'|{vv("1")}| = |{vv("2")}| = {it("v")}, angle β', f'{it("J")} = {it("m")}|{vv("2")} − {vv("1")}|',
                               f'|{vv("2")} − {vv("1")}| = 2{it("v")} sin(β/2)', f'(isosceles: sides {it("v")}, {it("v")})']))
    o.append(lines(s, x0, 106, [f'{it("J")} = 2{it("mv")} sin(β/2)', f'= 2 × {M:.0f} × {V_WALK} × sin {BETA / 2:.0f}°',
                                f'= {J_TURN:.0f} N s, inward']))
    aria = ("Top view of a turning walk, the walker shown as its centre of mass mark. Two grey arrows of equal length, "
            f"the velocity before v1 and after v2, each {V_WALK} metres per second, leave the mark at the angle beta = "
            f"{BETA:.0f} degrees, marked by a blue arc. A blue arrow joins their tips: the velocity change delta v = v2 "
            f"- v1, of length 2 v sin(beta/2) = {dvl / kv:.1f} metres per second, the base of an isosceles triangle. A red "
            f"arrow at the mark, parallel to delta v and pointing toward the inside of the turn, is the ground impulse "
            f"J = m delta v. J = m |v2 - v1| = 2 m v sin(beta/2) = 2 x {M:.0f} x {V_WALK} x sin {BETA / 2:.0f} degrees = "
            f"{J_TURN:.0f} newton seconds.")
    return finish(VB, aria, s, o)


FIGS[33] = (r'D4: turning impulse. Derive the ground impulse needed to red', fig33)


# ================================================================ svg #31  D2 stair work and power
U_STEP = M * G * H_RISER
P_STAIR = U_STEP * F_STEP
V_VERT = H_RISER * F_STEP
close(U_STEP, 117.0, 0.5)                    # line 106, 108
close(P_STAIR, 210.0, 0.5)
close(M * G * V_VERT, P_STAIR, 1e-9)         # P = mghf = m g v_vert
close(V_VERT, 0.31, 0.005)


def stair_pose():
    """Ascent: the rear (far) leg extended on the lower tread, the front (near) foot flat on the next tread; the near hip
    is solved so the front heel stands exactly one riser (0.17 m) above the rear heel."""
    def build(h):
        return LB.pose(pelvis=5, trunk=5, near=dict(hip=h, knee=h, shoulder=-15, elbow=15),
                       far=dict(hip=-12, knee=12, shoulder=20, elbow=20), anchor=("heel", "far"))

    h = bis(lambda h: (build(h).j["heel_far"][1] - build(h).j["heel"][1]) / UM - H_RISER, 20.0, 90.0)
    return build(h)


def fig31():
    p = "m13f31_"
    VB, s = bvb(420)
    o = [defs(p, s)]
    HF, fy, hx = 250.0, 362.0, 112.0
    k = HF / HM
    P = stair_pose()
    close((P.j["heel_far"][1] - P.j["heel"][1]) / UM, H_RISER, 1e-6)
    body, J = body_at(p, s, P, hx, fy, HF, key="hip")
    close((J["heel_far"][1] - J["heel"][1]) / k, H_RISER, 1e-4)             # the drawn riser is 0.17 m
    xr = J["heel"][0] - 0.03 * k                                             # riser face just behind the front heel
    tread = 0.32 * k                                                         # design value: tread depth
    rh = H_RISER * k
    ys = [fy, fy - rh, fy - 2 * rh]
    st = (f'M8,{fy:.2f} H{xr:.2f} V{ys[1]:.2f} H{xr + tread:.2f} V{ys[2]:.2f} H{xr + tread + 0.30 * k:.2f} '
          f'V{fy + s(6):.2f} H8 Z')
    o.append(f'<path d="{st}" fill="{BOX}" stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}" stroke-linejoin="round"/>')
    o.append(body)
    o.append(dim_v(s, p, xr - s(12), fy - rh, fy))
    o.append(lab(s, xr - s(18), fy - rh / 2 + s(5), it("h"), "label2", O["geometry"], "end"))
    c = J["com"]
    o.append(seg(s, c[0], c[1] + rh, 214, c[1] + rh))
    o.append(seg(s, c[0], c[1], 214, c[1]))
    o.append(f'<g opacity="0.55">{H.com_mark(s, c[0], c[1] + rh)}</g>')
    o.append(H.com_mark(s, *c))
    o.append(H.arrow(s, p, c[0] + s(16), c[1] + s(2), c[0] + s(16), c[1] + s(46), "load"))
    o.append(lab(s, c[0] + s(22), c[1] + rh + s(20), f'{it("mg")}', "label", O["load"]))
    o.append(dim_v(s, p, 206, c[1] + rh, c[1]))
    o.append(lab(s, 211, c[1] + rh / 2 + s(5), f'{it("h")} = {H_RISER} m', "label2", O["geometry"]))
    o.append(lab(s, 211, c[1] - s(8), "COM", "label2", I["primary"]))
    o.append(lab(s, 211, c[1] + rh + s(16), "COM one step lower", "label2", I["secondary"]))
    x0 = 212.0
    o.append(lines(s, 8, 26, ['ΔKE = 0 per step, so', f'{it("U")} = ΔPE = {it("mgh")}', f'= {M:.0f} × {G} × {H_RISER}',
                               f'= {U_STEP:.0f} J per step'], lead=1.4))
    o.append(lines(s, x0, 26, [f'{it("P")} = {it("U")}{it("f")} = {U_STEP:.0f} × {F_STEP}', f'= {P_STAIR:.0f} W',
                                f'{it("v")}{sb("vert", s)} = {it("hf")} = {V_VERT:.2f} m/s',
                                f'{it("P")} = {it("mg")}{it("v")}{sb("vert", s)}'], lead=1.4))
    o.append(credit(s, VB))
    aria = ("A skeleton (Lynch art) climbing stairs to the right, the rear foot flat on the lower tread and the front "
            f"foot flat on the next, one riser of {H_RISER} metres higher. The centre of mass is marked, with a brown "
            "weight arrow mg pointing down and an open mark one riser lower joined by two dashed levels and a blue "
            f"dimension h = {H_RISER} metres. With the kinetic energy unchanged from step to step, the work per step "
            f"equals the potential energy gained, U = m g h = {M:.0f} x {G} x {H_RISER} = {U_STEP:.0f} joules. At "
            f"{F_STEP} steps per second the power is P = U f = {P_STAIR:.0f} watts, equal to m g v_vert with v_vert = h f "
            f"= {V_VERT:.2f} metres per second.")
    return finish(VB, aria, s, o)


FIGS[31] = (r'D2: stair work and power. Derive the work per step and the c', fig31)


# ================================================================ svg #32  D3 spinal compression
W_TR = 0.60 * M * G                          # 412 N upper-body weight (Appendix: m_ub = 0.60 M)
L_T, D_M, D_L = 0.346, 0.05, 0.40            # m (line 126)
W_L = 20.0 * G                               # 196 N, the 20 kg box
PHI = 60.0                                   # deg, the stoop (line 126)
D_TR = L_T * math.sin(math.radians(PHI))
F_M = (W_TR * D_TR + W_L * D_L) / D_M
F_COMP = F_M + (W_TR + W_L) * math.cos(math.radians(PHI))
close(W_TR, 412.0, 0.5)
close(D_TR, 0.300, 0.0005)                   # line 126, 128
close(F_M, 4040.0, 5.0)
F_COMP_TEXT = 4350.0                         # the text: 4042 + 608 cos 60 = 4346, 4350 to 3 sig. figs (Module 1, Lab C)
F_M_SHOWN = (W_TR * 0.300 + W_L * D_L) / D_M     # 4042 from the displayed d_tr = 0.300
F_COMP_SHOWN = F_M_SHOWN + (W_TR + W_L) * math.cos(math.radians(PHI))     # 4346
close(F_COMP, F_COMP_TEXT, 10.0)
_sq = L_T * math.sin(math.radians(20.0))
_fm_sq = (W_TR * _sq + W_L * 0.25) / D_M
close(_fm_sq + (W_TR + W_L) * math.cos(math.radians(20.0)), 2530.0, 5.0)    # line 126, 128 (squat)
NECK_TILT = math.degrees(math.atan2(-LB.OFF["lat_trunk"]["neck"][0], -LB.OFF["lat_trunk"]["neck"][1]))   # 6.3 deg


def lift_pose(sh):
    """Stoop with knees straight: the L5/S1-to-C7 axis is phi = 60 deg from vertical (pelvis + lumbar = 66.3 deg, the
    art's C7 sits 6.3 deg behind the trunk-local vertical), thighs 10 deg forward as the kit's stoop_lift, arms
    flexed to shoulder angle sh."""
    tot = PHI + NECK_TILT
    return LB.pose(pelvis=tot - 25.0, trunk=25.0, near=dict(hip=tot - 25.0 + 10.0, knee=0, shoulder=sh),
                   far=dict(hip=tot - 25.0 + 10.0, knee=0, shoulder=sh), anchor=("heel", "near"))


def fig32():
    p = "m13f32_"
    VB, s = bvb(516)
    o = [defs(p, s)]
    HF, fy, lx = 320.0, 394.0, 118.0
    k = HF / HM
    sh = bis(lambda a: (lift_pose(a).j["wrist"][0] - lift_pose(a).j["l5s1"][0]) / UM - D_L, 55.0, 90.0)
    P = lift_pose(sh)
    body, J = body_at(p, s, P, lx, fy, HF, key="l5s1")
    L5 = J["l5s1"]
    close((J["wrist"][0] - L5[0]) / k, D_L, 1e-4)                            # the drawn load arm is d_L = 0.40 m
    ph = math.radians(PHI)
    u = (math.sin(ph), -math.cos(ph))                                        # L5/S1 -> upper-body COM, phi from vertical
    n = (-math.cos(ph), -math.sin(ph))                                       # posterior normal
    wt = (L5[0] + u[0] * L_T * k, L5[1] + u[1] * L_T * k)
    close((wt[0] - L5[0]) / k, D_TR, 1e-3)                                   # the drawn trunk arm is d_tr = 0.300 m
    bw, bh = 0.30 * k, 0.22 * k                                              # box (design values)
    bx, by = J["wrist"][0], J["wrist"][1] + 0.06 * k
    o.append(floor(s, 8, 396, fy))
    o.append(box(s, bx - bw / 2, by - bh / 2, bw, bh, fill=BOX))
    o.append(body)
    # lines of action and moment arms, measured under the floor
    y1, y2 = fy + s(24), fy + s(46)
    for xx, ytop in ((L5[0], L5[1]), (wt[0], wt[1]), (bx, by)):
        o.append(vline(s, xx, ytop, y2 + s(5)))
    o.append(dim_h(s, p, L5[0], bx, y1, "geometry"))
    o.append(dim_h(s, p, L5[0], wt[0], y2, "geometry"))
    o.append(lab(s, bx + s(8), y1 + s(5), f'{it("d")}{sb("L", s)} = {D_L:.2f} m', "label2", O["geometry"]))
    o.append(lab(s, L5[0] - s(8), y2 + s(5), f'{it("d")}{sb("tr", s)} = {D_TR:.3f} m', "label2", O["geometry"], "end"))
    # forces
    o.append(H.arrow(s, p, wt[0], wt[1] + s(7), wt[0], wt[1] + s(7) + s(40), "load"))
    o.append(H.com_mark(s, *wt))
    o.append(lab(s, wt[0] + s(10), wt[1] + s(34), f'{it("W")}{sb("tr", s)}', "label", O["load"]))
    o.append(H.arrow(s, p, bx, by + bh / 2 + s(2), bx, by + bh / 2 + s(44), "load"))
    o.append(lab(s, bx + s(10), by + bh / 2 + s(38), f'{it("W")}{sb("L", s)}', "label", O["load"]))
    t0 = (L5[0] + n[0] * D_M * k + u[0] * 0.27 * k, L5[1] + n[1] * D_M * k + u[1] * 0.27 * k)
    t1 = (L5[0] + n[0] * D_M * k + u[0] * 0.05 * k, L5[1] + n[1] * D_M * k + u[1] * 0.05 * k)
    o.append(H.arrow(s, p, *t0, *t1, "force"))
    o.append(lab(s, t0[0] + n[0] * s(8) - s(6), t0[1] + n[1] * s(6), f'{it("F")}{sb("m", s)}', "label", O["force"], "end"))
    c1 = (L5[0] - u[0] * 0.20 * k, L5[1] - u[1] * 0.20 * k)
    o.append(H.arrow(s, p, L5[0], L5[1], *c1, "reaction"))
    o.append(lab(s, c1[0] - s(8), c1[1] + s(16), f'{it("F")}{sb("comp", s)}', "label", I["primary"], "end"))
    o.append(H.joint_centre(s, *L5))
    o.append(lab(s, L5[0] + s(12), L5[1] + s(22), "L5/S1", "label2", I["primary"]))
    mid = (L5[0] + n[0] * D_M * k * 0.5, L5[1] + n[1] * D_M * k * 0.5)
    o.append(H.line(s, mid[0] + n[0] * s(4), mid[1] + n[1] * s(4), mid[0] + n[0] * s(30) - s(14), mid[1] + n[1] * s(30), O["geometry"], "leader"))
    o.append(lab(s, mid[0] + n[0] * s(34) - s(16), mid[1] + n[1] * s(34) - s(2), f'{it("d")}{sb("m", s)} = {D_M:.2f} m', "label2", O["geometry"], "end"))
    o.append(lab(s, bx + bw / 2 + s(8), by - bh / 2 + s(12), "box, 20 kg", "label2", I["secondary"]))
    sq = round(_fm_sq + (W_TR + W_L) * math.cos(math.radians(20.0)), -1)
    FM_, FC_, FW_ = (f'{it("F")}{sb(n_, s)}' for n_ in ("m", "comp", "tr"))
    dtr_, dl_, dm_, wtr_, wl_ = (f'{it(a_)}{sb(b_, s)}' for a_, b_ in (("d", "tr"), ("d", "L"), ("d", "m"), ("W", "tr"), ("W", "L")))
    o.append(lines(s, 8, 24, [f'moments about L5/S1: {FM_}{dm_} = {wtr_}{dtr_} + {wl_}{dl_}',
                              f'{dtr_} = {it("ℓ")}{sb("t", s)} sin φ = {L_T} × sin {PHI:.0f}° = {D_TR:.3f} m',
                              f'{FM_} = ({W_TR:.0f} × {D_TR:.3f} + {W_L:.1f} × {D_L:.2f}) / {D_M:.2f} = {F_M_SHOWN:.0f} N',
                              f'force along the spine: {FC_} = {FM_} + ({wtr_} + {wl_}) cos φ',
                              f'= {F_M_SHOWN:.0f} + {W_TR + W_L:.0f} × cos {PHI:.0f}° = {F_COMP_SHOWN:.0f} ≈ {F_COMP_TEXT:.0f} N',
                              f'squat (φ = 20°, {dl_} = 0.25 m): {FC_} ≈ {sq:.0f} N;  arrows not to scale'], lead=1.4))
    o.append(credit(s, VB))
    aria = ("A skeleton (Lynch art) stooped forward with straight knees, the line from L5/S1 to the upper body's centre of "
            f"mass {PHI:.0f} degrees from vertical, holding a 20 kilogram box at arms' length. L5/S1 is marked. Brown "
            f"weight arrows point down: the upper-body weight W_tr = {W_TR:.0f} newtons at the centre of mass mark, "
            f"{D_TR:.3f} metres ahead of L5/S1, and the load W_L = {W_L:.0f} newtons at the box, {D_L:.2f} metres ahead. "
            f"Blue dimensions on the floor give these moment arms d_tr and d_L. A red arrow F_m along the back, "
            f"{D_M:.2f} metres behind the spine axis, is the erector spinae force; a black arrow F_comp along the spine is "
            f"the disc compression. Moment balance gives F_m = (W_tr d_tr + W_L d_L) / d_m = about {round(F_M, -1):.0f} newtons; force "
            f"balance along the spine gives F_comp = F_m + (W_tr + W_L) cos phi, about {F_COMP_TEXT:.0f} newtons. Squatting at "
            "20 degrees with the load at 0.25 metres brings it to about 2530 newtons.")
    return finish(VB, aria, s, o)


FIGS[32] = (r'D3: spinal compression. Derive the erector spinae force and ', fig32)


# ================================================================ svg #35  D6 slope power
V_SLOPE, THETA = 1.0, 10.0                   # m/s, deg (line 184, 186)
P_SLOPE = {a: M * G * V_SLOPE * math.sin(math.radians(a)) for a in (5.0, 10.0, 15.0)}
for _a, _w in ((5.0, 60.0), (10.0, 119.0), (15.0, 178.0)):
    close(P_SLOPE[_a], _w, 0.6)              # line 184: about 60, 119, 178 W


def slope_pose(th):
    """Walking up a slope facing right, mid-stance: the body stays vertical, the stance foot lies on the slope
    (toes up by theta), the swing leg reaches forward."""
    return LB.pose(near=dict(hip=0, knee=8, contact=None, ankle=8 + th, shoulder=-8, elbow=10),
                   far=dict(hip=24, knee=42, contact=None, ankle=10, shoulder=10, elbow=14), anchor=("heel", "near"))


def fig35():
    p = "m13f35_"
    VB, s = bvb(498)
    o = [defs(p, s)]
    HF, hx, fy = 270.0, 150.0, 405.0
    th = math.radians(THETA)
    t = (math.cos(th), -math.sin(th))                                        # up the slope (screen)
    n = (math.sin(th), math.cos(th))                                         # into the slope
    P = slope_pose(THETA)
    body, J = body_at(p, s, P, hx, fy, HF, key="heel")
    k = HF / HM
    sl = (J["toe"][1] - J["heel"][1]) / (J["toe"][0] - J["heel"][0])
    close(sl, -math.tan(th), 2e-3)                                           # the sole lies on the slope line
    yline = lambda x: fy - math.tan(th) * (x - hx)                           # noqa: E731
    xl, xr = 8.0, 392.0
    o.append(f'<polygon points="{xl},{yline(xl):.2f} {xr},{yline(xr):.2f} {xr},{yline(xl) + s(10):.2f} {xl},{yline(xl) + s(10):.2f}" '
             f'fill="{BOX}" stroke="{I["secondary"]}" stroke-width="{s(1.4):.2f}" stroke-linejoin="round"/>')
    o.append(body)
    c = J["com"]
    # the weight resolved, drawn to scale: 0.2 px per newton
    sc = 0.2
    W = M * G
    o.append(seg(s, xl, yline(xl), xr, yline(xl)))                          # horizontal reference
    o.append(angle_arc(s, xl, yline(xl), s(60), -THETA, 0))
    o.append(lab(s, xl + s(66), yline(xl) - s(4), "θ", "label", O["geometry"]))
    tip_w = (c[0], c[1] + W * sc)
    tip_par = (c[0] - t[0] * W * math.sin(th) * sc, c[1] - t[1] * W * math.sin(th) * sc)          # down the slope
    tip_perp = (c[0] + n[0] * W * math.cos(th) * sc, c[1] + n[1] * W * math.cos(th) * sc)
    o.append(seg(s, *tip_w, *tip_par))
    o.append(seg(s, *tip_w, *tip_perp))
    o.append(H.arrow(s, p, *c, *tip_perp, "dim"))
    o.append(H.arrow(s, p, *c, *tip_w, "load"))
    o.append(H.arrow(s, p, *c, *tip_par, "force"))
    o.append(H.com_mark(s, *c))
    o.append(lab(s, c[0] - s(12), c[1] - s(10), "COM", "label2", I["primary"], "end"))
    o.append(lab(s, c[0] - s(26), (c[1] + tip_w[1]) / 2 + s(14), f'{it("mg")}', "label", O["load"], "end"))
    o.append(lab(s, tip_perp[0] - s(6), tip_perp[1] + s(28), f'{it("mg")} cos θ', "label2", I["primary"]))
    o.append(lab(s, tip_par[0] - s(8), tip_par[1] + s(18), f'{it("mg")} sin θ = {W * math.sin(th):.0f} N', "label2", I["primary"], "end"))
    # velocity up the slope
    v0 = (J["toe"][0] + s(34), yline(J["toe"][0] + s(34)) - s(16))
    o.append(H.arrow(s, p, v0[0], v0[1], v0[0] + t[0] * 62, v0[1] + t[1] * 62, "geometry"))
    o.append(lab(s, v0[0] + t[0] * 62 + s(6), v0[1] + t[1] * 62 - s(8), f'{it("v")} = {V_SLOPE} m/s', "label2", O["geometry"]))
    pr = lambda a: f'{P_SLOPE[a]:.0f} W'                                    # noqa: E731
    o.append(lines(s, 8, 24, [f'weight along the path: {it("mg")} sin θ, down the slope',
                              f'going up at speed {it("v")}, the muscles work against it at rate',
                              f'{it("P")} = {it("mg")} sin θ · {it("v")} = {M:.0f} × {G} × sin {THETA:.0f}° × {V_SLOPE} = {P_SLOPE[10.0]:.0f} W',
                              f'(5°: {pr(5.0)}, 15°: {pr(15.0)}); same as {it("mg")} × {it("v")} sin θ, weight × climb rate',
                              'downhill the sign flips: the muscles absorb it'], lead=1.4))
    o.append(credit(s, VB))
    aria = ("A skeleton (Lynch art) walking up a slope of 10 degrees to the right, body upright, the stance foot lying on "
            "the slope and the swing leg reaching forward. A brown arrow mg points straight down from the centre of mass "
            f"mark, to scale at 0.2 pixels per newton; dashed lines resolve it into a red component mg sin theta = "
            f"{W * math.sin(th):.0f} newtons pointing down the slope and a grey component mg cos theta pressing into it. "
            f"A blue arrow marks the walking speed v = {V_SLOPE} metre per second up the slope, and a blue arc marks the "
            f"angle theta. Going up at speed v the muscles work against mg sin theta at the rate P = mg sin theta v = "
            f"{M:.0f} x {G} x sin 10 degrees x {V_SLOPE} = {P_SLOPE[10.0]:.0f} watts, which is {P_SLOPE[5.0]:.0f} watts at 5 "
            f"degrees and {P_SLOPE[15.0]:.0f} at 15; downhill the sign flips and the muscles absorb the power.")
    return finish(VB, aria, s, o)


FIGS[35] = (r'D6: slope power. Derive the extra power of walking on a grad', fig35)


# ================================================================ svg #36  D7 the momentum strategy
H_RISE, V0, T_E = 0.40, 0.25, 0.4            # m, m/s, s (Appendix; line 413)
E_RISE = M_UP * G * H_RISE
E_KIN = 0.5 * M_UP * V0 ** 2
J_SAVED = M_UP * V0
J_EXT = M_UP * G * T_E
close(E_RISE, 220.0, 0.5)                    # line 413: 220 J
close(E_KIN, 1.8, 0.05)                      # 1.8 J
close(E_RISE - E_KIN, 218.0, 0.5)            # 218 J
close(J_SAVED, 14.0, 0.05)                   # 14 N s
close(J_EXT, 220.0, 0.5)                     # about 220 N s
close(J_SAVED / J_EXT, 0.06, 0.005)          # about six percent
D_STD = 0.20                                 # the standard chair's d (Section 2, line 90): pose B is solved to it
ABOVE_KNEE = ("head", "trunk", "upper_arm", "upper_arm_far", "forearm", "forearm_far", "hand", "hand_far", "thigh", "thigh_far")


def rise_pose(tot):
    """Seat-off with the same lower body in both panels (thighs horizontal, shanks vertical, feet flat); the upper body
    is pitched forward by tot degrees (pelvis 55 %, lumbar 45 %) and the arms swing forward with it (0.75 tot)."""
    pel = 0.55 * tot
    sh = 0.75 * tot
    return LB.pose(pelvis=pel, trunk=0.45 * tot, near=dict(hip=90.0 + pel, knee=90, shoulder=sh),
                   far=dict(hip=90.0 + pel, knee=90, shoulder=sh), anchor=("heel", "near"))


def com_above_knee(P, J):
    """COM of the segments above the knees (head, trunk, arms, thighs; Winter mass fractions), figure units."""
    ms = sum(P.com[k][1] for k in ABOVE_KNEE)
    return (sum(J["com_" + k][0] * P.com[k][1] for k in ABOVE_KNEE) / ms, sum(J["com_" + k][1] * P.com[k][1] for k in ABOVE_KNEE) / ms)


def d_above(tot):
    P = rise_pose(tot)
    _, J = LB.draw("m13f36_", H.Scale(400, 400), P, 0.0, 0.0, 1000.0)
    cx, _ = com_above_knee(P, J)
    return (J["knee"][0] - cx) / (1000.0 / HM)


def fig36():
    p = "m13f36_"
    VB, s = bvb(504)
    o = [defs(p, s)]
    HF, fy = 235.0, 262.0
    k = HF / HM
    tot_b = bis(lambda a: d_above(a) - D_STD, 20.0, 80.0)
    close(d_above(tot_b), D_STD, 1e-6)
    d_a = d_above(0.0)
    o.append(floor(s, 8, 392, fy))
    for (kx, tot, name, d) in ((136.0, 0.0, "trunk upright", d_a), (300.0, tot_b, "trunk pitched forward", D_STD)):
        P = rise_pose(tot)
        body, J = body_at(p, s, P, kx, fy, HF, key="knee")
        cx, cy = com_above_knee(P, J)
        close((J["knee"][0] - cx) / k, d, 1e-4)
        hx, hy = J["hip"]
        sy = hy + 0.075 * HF
        xa, xb = hx - 0.16 * HF, hx + 0.20 * HF
        o.append(H.line(s, xa, sy, xb, sy, I["rule"], "axis", extra='stroke-linecap="round"'))
        for xx in (xa + (xb - xa) * 0.06, xa + (xb - xa) * 0.94):
            o.append(H.line(s, xx, sy, xx, fy, I["rule"], "axis"))
        o.append(body)
        o.append(vline(s, J["knee"][0], J["knee"][1], fy + s(32)))
        o.append(vline(s, cx, cy, fy + s(32)))
        o.append(dim_h(s, p, cx, J["knee"][0], fy + s(28), "geometry"))
        o.append(lab(s, (cx + J["knee"][0]) / 2, fy + s(52), f'{it("d")} = {d:.2f} m', "label2", O["geometry"], "middle"))
        o.append(lab(s, (cx + J["knee"][0]) / 2, fy + s(69), f'{it("τ")} = {it("m")}{sb("up", s)} {it("gd")} = {M_UP * G * d:.0f} N m', "label2", I["primary"], "middle"))
        o.append(H.arrow(s, p, cx, cy + s(7), cx, cy + s(7) + s(30), "load"))
        o.append(H.com_mark(s, cx, cy))
        o.append(lab(s, cx - s(8), cy + s(34), f'{it("m")}{sb("up", s)} {it("g")}', "label2", O["load"], "end"))
        o.append(lab(s, J["knee"][0] - s(26), 22, name, "label", I["primary"], "middle"))
        if tot > 0:
            o.append(H.arrow(s, p, cx, cy - s(8), cx, cy - s(8) - V0 * 120.0, "geometry"))
            o.append(lab(s, cx + s(8), cy - s(8) - V0 * 60.0 + s(4), f'{it("v")}{sb("0", s)} = {V0} m/s', "label2", O["geometry"]))
        else:
            o.append(lab(s, cx - s(8), cy - s(14), f'{it("v")}{sb("0", s)} = 0', "label2", I["secondary"], "end"))
        o.append(lab(s, J["knee"][0] - 0.0, J["knee"][1] - s(10), "knee", "label2", I["secondary"], "middle"))
    mu = f'{it("m")}{sb("up", s)} '
    o.append(lines(s, 8, fy + s(96), [
        f'extension phase, arriving at rest: ∫({it("F")}{sb("z", s)} − {mu}{it("g")})dt = −{mu}{it("v")}{sb("0", s)}',
        f'impulse saved: {mu}{it("v")}{sb("0", s)} = {M_UP:.0f} × {V0} = {J_SAVED:.0f} N s',
        f'of {mu}{it("g")}{it("T")}{sb("e", s)} = {M_UP:.0f} × {G} × {T_E} = {J_EXT:.0f} N s: about {100 * J_SAVED / J_EXT:.0f} %',
        f'energy: {mu}{it("gH")} − ½{mu}{it("v")}{sb("0", s)}² = {E_RISE:.0f} − {E_KIN:.1f} = {E_RISE - E_KIN:.0f} J (under 1 %)',
        f'the larger part is geometric: {it("d")} falls from {d_a:.2f} to {D_STD:.2f} m,',
        f'so {it("τ")} = {mu}{it("gd")} falls from {M_UP * G * d_a:.0f} to {M_UP * G * D_STD:.0f} N m'],
        lead=1.4))
    o.append(credit(s, VB))
    aria = ("Two skeletons (Lynch art) seen from the side, facing right, at the instant the buttocks leave a seat, "
            "thighs horizontal and feet flat. Left, the trunk is upright; right, it is pitched forward and the arms "
            "swing with it. In each, a black and white mark is the centre of mass of the body above the knees, with a "
            "brown weight arrow and a dashed drop; a blue dimension on the floor line gives the horizontal distance d "
            f"back to the knee: {d_a:.2f} metres upright and {D_STD:.2f} metres pitched, so the knee torque m_up g d "
            f"falls from {M_UP * G * d_a:.0f} to {M_UP * G * D_STD:.0f} newton metres (m_up = {M_UP:.0f} kg). On the right "
            f"figure a blue arrow marks the upward seat-off speed v0 = {V0} metres per second. Vertical impulse-momentum "
            f"over the extension phase, arriving at rest, gives the integral of (F_z - m_up g) dt = -m_up v0: the flexion "
            f"phase saves m_up v0 = {J_SAVED:.0f} newton seconds of the m_up g T_e = {J_EXT:.0f} of a 0.4 second "
            f"extension, about 6 percent. In energy, m_up g H - half m_up v0 squared = {E_RISE:.0f} - {E_KIN:.1f} = "
            f"{E_RISE - E_KIN:.0f} joules for a rise of 0.40 metres, a saving under 1 percent.")
    return finish(VB, aria, s, o)


FIGS[36] = (r'D7: the momentum strategy. Show why pitching the trunk forwa', fig36)


# ================================================================ svg #38  D9 the recovery step
ELL, W0, X0, XDOT, L_STEP, DT = 1.0, 3.13, 0.05, 1.0, 0.60, 0.10     # m, 1/s (line 305, Appendix), m, m/s, m, s
close(math.sqrt(G / ELL), W0, 0.005)                                  # omega0 = sqrt(g/l) = 3.13 (line 305)
XI = X0 + XDOT / W0
close(XI, 0.37, 0.005)                                                # line 329
XDOT_MAX = W0 * (L_STEP - X0)
close(XDOT_MAX, 1.72, 0.005)                                          # line 329
XDOT_MAX_DELAY = W0 * (L_STEP * math.exp(-W0 * DT) - X0)
close(XDOT_MAX_DELAY, 1.22, 0.005)                                    # line 329, 483


def trip_pose(a):
    """Just after a trip: stance leg flat on the floor, the whole body turned a degrees about the stance ankle, the swing
    leg forward with its toe 0.12 m above the floor; the arms swing opposite."""
    return LB.pose(pelvis=a, near=dict(hip=0, knee=0, shoulder=10, elbow=15),
                   far=dict(hip=30.0 + a, knee=20, contact=None, ankle=10, shoulder=-12, elbow=20), anchor=("heel", "near"))


def fig38():
    p = "m13f38_"
    VB, s = bvb(534)
    o = [defs(p, s)]
    HF, fy, ax = 250.0, 262.0, 100.0
    k = HF / HM
    a = bis(lambda a: (pose_com(trip_pose(a))[0] - trip_pose(a).j["ankle"][0]) / UM - X0, -8.0, 15.0)
    body, J = body_at(p, s, trip_pose(a), ax, fy, HF, key="ankle")
    close((J["com"][0] - J["ankle"][0]) / k, X0, 1e-3)                    # the art's COM is x0 = 0.05 m ahead of the ankle
    close((J["floor_y"] - J["com"][1]) / k, ELL, 0.03)                    # and about l = 1.0 m high
    o.append(floor(s, 8, 396, fy))
    o.append(body)
    ank = J["ankle"]
    xc = ank[0] + X0 * k
    cy = fy - ELL * k                                                     # COM height l = 1.0 m (the text's value)
    o.append(vline(s, xc, cy, fy))
    o.append(vline(s, ank[0], ank[1], fy + s(58)))
    o.append(H.com_mark(s, xc, cy))
    o.append(lab(s, xc - s(10), cy - s(8), "COM", "label2", I["primary"], "end"))
    o.append(H.arrow(s, p, xc + s(9), cy, xc + s(9) + XDOT * 60.0, cy, "geometry"))
    o.append(lab(s, xc + s(12), cy - s(10), f'{dot_("x")} = {XDOT} m/s', "label2", O["geometry"]))
    # distances along the floor from the stance ankle
    xi_x = ank[0] + XI * k
    xg = xc + XDOT / W0 * k
    close(xg, xi_x, 1e-6)
    y1, y2 = fy + s(24), fy + s(50)
    o.append(dim_h(s, p, xc, xg, y1, "geometry"))
    o.append(lab(s, xg + s(8), y1 + s(5), f'{dot_("x")}/ω₀ = {XDOT / W0:.2f} m', "label2", O["geometry"]))
    o.append(dim_h(s, p, ank[0], xc, y1, "geometry", tick=4))
    o.append(lab(s, ank[0] - s(6), y1 + s(5), f'{it("x")}{sb("0", s)} = {X0} m', "label2", O["geometry"], "end"))
    o.append(xi_mark(s, xi_x, fy))
    o.append(lab(s, xi_x - s(9), fy - s(8), "ξ", "label", I["primary"], "end"))
    o.append(dim_h(s, p, ank[0], xi_x, y2, "force"))
    o.append(lab(s, xi_x + s(8), y2 + s(5), f'step ≥ ξ = {XI:.2f} m', "label2", O["force"]))
    o.append(vline(s, xi_x, fy, y2 + s(5), O["force"]))
    xl = ank[0] + L_STEP * k
    o.append(H.line(s, xl, fy - s(10), xl, fy + s(4), I["secondary"], "ref"))
    o.append(lab(s, xl + s(6), fy - s(10), f'reach {it("L")} = {L_STEP:.2f} m', "label2", I["secondary"]))
    o.append(contact_mark(s, ank[0], fy))
    o.append(lab(s, ank[0], y2 + s(34), "stance ankle", "label2", I["secondary"], "middle"))
    e_ = 'e\u2009' + sup('ω₀Δ' + it('t'), s)
    o.append(lines(s, 8, fy + s(112), [
        f'pendulum rate ω₀ = √({it("g")}/{it("ℓ")}) = √({G}/{ELL:.1f}) = {W0} 1/s',
        f'the fall diverges along ξ = {it("x")}{sb("com", s)} + {dot_("x")}{sb("com", s)}/ω₀;',
        'a step arrests it only if the new base reaches ξ, so',
        f'minimum step ξ = {it("x")}{sb("0", s)} + {dot_("x")}/ω₀ = {X0} + {XDOT}/{W0} = {XI:.2f} m',
        f'largest speed one step covers: {dot_("x")}{sb("max", s)} = ω₀({it("L")} − {it("x")}{sb("0", s)}) = {XDOT_MAX:.2f} m/s',
        f'reaction delay Δ{it("t")} = {DT} s: ξ {e_}, so {dot_("x")}{sb("max", s)} = {XDOT_MAX_DELAY:.2f} m/s'],
        lead=1.4))
    o.append(credit(s, VB))
    aria = ("A skeleton (Lynch art) just after a trip, the stance foot flat on the floor and the swing leg raised forward. "
            f"The centre of mass is marked a height l = {ELL:.1f} metre above the floor and {X0} metres ahead of the stance "
            f"ankle, with a blue arrow for its forward speed {XDOT} metres per second. On the floor, a blue dimension of "
            f"{XDOT / W0:.2f} metres (the speed over omega0) leads from the centre of mass projection to the extrapolated "
            f"COM xi, an open circle, {XI:.2f} metres from the ankle; a red dimension marks the minimum step, at least xi. "
            f"A grey tick marks the maximum reach L = {L_STEP:.2f} metres. With omega0 = sqrt(g/l) = {W0} per second, "
            f"xi = x0 + xdot/omega0 = {X0} + {XDOT}/{W0} = {XI:.2f} metres; one step covers speeds up to omega0 (L - x0) = "
            f"{XDOT_MAX:.2f} metres per second, and a 0.1 second reaction delay multiplies xi by e to the omega0 delta t "
            f"and lowers that to {XDOT_MAX_DELAY:.2f}.")
    return finish(VB, aria, s, o)


FIGS[38] = (r'D9: the recovery step. Derive the minimum recovery-step leng', fig38)


# ================================================================ svg #39  D10 the carry lean
M_BAG, D_B = 10.0, 0.30                      # kg, m (Appendix; line 425)
W_B = M_BAG * G
MOM_B = W_B * D_B
X_LEAN = MOM_B / W_TR
close(W_B, 98.1, 0.05)                       # 10 kg bag
close(MOM_B, 29.4, 0.05)                     # line 425: 29.4 N m
close(X_LEAN, 0.071, 0.0005)                 # line 425: about 0.071 m
ALPHA = math.degrees(math.asin(X_LEAN / L_T))                 # trunk tilt that moves the upper-body COM by x_lean (11.9 deg)


def carry_pose(sh):
    """Frontal view: bag in the subject's right hand (image left), the trunk tilted ALPHA toward the subject's left
    (away from the bag); sh = extra abduction of the right arm."""
    A = LB._ANT_ARMS
    r = dict(A)
    r["shoulder"] = A["shoulder"] + sh
    r["hip"] = 3
    lft = dict(A)
    lft["hip"] = 3
    return LB.pose_ant(trunk=ALPHA, r=r, l=lft, anchor=("sole", "l"))


def fig39():
    p = "m13f39_"
    VB, s = bvb(446)
    o = [defs(p, s)]
    HF, fy, lx = 300.0, 330.0, 132.0
    k = HF / HM
    grip = lambda P: ((P.j["wrist_r"][0] + P.j["fingertip_r"][0]) / 2 - P.j["l5s1"][0]) / UM        # noqa: E731
    sh = bis(lambda a: grip(carry_pose(a)) + D_B, -20.0, 20.0)
    P = carry_pose(sh)
    body, J = body_at(p, s, P, lx, fy, HF, key="l5s1")
    L5 = J["l5s1"]
    gx = (J["wrist_r"][0] + J["fingertip_r"][0]) / 2
    gy = (J["wrist_r"][1] + J["fingertip_r"][1]) / 2
    close((L5[0] - gx) / k, D_B, 1e-4)                                      # the bag hangs d_b = 0.30 m from the spine
    al = math.radians(ALPHA)
    wt = (L5[0] + math.sin(al) * L_T * k, L5[1] - math.cos(al) * L_T * k)
    close((wt[0] - L5[0]) / k, X_LEAN, 1e-4)                                # the upper-body COM is x_lean = 0.071 m aside
    bw, bh = 0.17 * k, 0.20 * k                                             # the bag (design values)
    o.append(floor(s, 8, 396, fy))
    o.append(vline(s, L5[0], 24, fy + s(36)))
    o.append(f'<path d="M{gx - bw * 0.22:.2f},{gy:.2f} Q{gx:.2f},{gy - s(22):.2f} {gx + bw * 0.22:.2f},{gy:.2f}" fill="none" '
             f'stroke="{I["secondary"]}" stroke-width="{s(1.6):.2f}"/>')
    o.append(f'<rect x="{gx - bw / 2:.2f}" y="{gy:.2f}" width="{bw:.2f}" height="{bh:.2f}" rx="{s(4):.2f}" fill="{BOX}" '
             f'stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
    o.append(body)
    o.append(vline(s, gx, gy + bh / 2, fy + s(36)))
    o.append(vline(s, wt[0], wt[1], fy + s(36)))
    o.append(H.arrow(s, p, gx, gy + bh * 0.55, gx, gy + bh * 0.55 + s(40), "load"))
    o.append(lab(s, gx - s(8), gy + bh * 0.55 + s(30), f'{it("W")}{sb("b", s)}', "label", O["load"], "end"))
    o.append(H.com_mark(s, *wt))
    o.append(H.arrow(s, p, wt[0], wt[1] + s(8), wt[0], wt[1] + s(8) + s(40), "load"))
    o.append(lab(s, wt[0] + s(10), wt[1] + s(34), f'{it("W")}{sb("tr", s)}', "label", O["load"]))
    o.append(lab(s, wt[0] - s(24), wt[1] - s(8), "upper-body COM", "label2", I["primary"], "end"))
    o.append(H.joint_centre(s, *L5))
    y1 = fy + s(30)
    o.append(dim_h(s, p, gx, L5[0], y1, "geometry"))
    o.append(dim_h(s, p, L5[0], wt[0], y1, "geometry", tick=4))
    o.append(lab(s, L5[0] - s(8), y1 + s(20), f'{it("d")}{sb("b", s)} = {D_B:.2f} m', "label2", O["geometry"], "end"))
    o.append(lab(s, wt[0] + s(6), y1 + s(20), f'{it("x")}{sb("lean", s)} = {X_LEAN:.3f} m', "label2", O["geometry"]))
    o.append(lab(s, gx - bw / 2 - s(6), gy + bh / 2 + s(5), f'{M_BAG:.0f} kg', "label2", I["secondary"], "end"))
    x0 = 214.0
    wb, wt_, db, xl = (f'{it("W")}{sb("b", s)}', f'{it("W")}{sb("tr", s)}', f'{it("d")}{sb("b", s)}', f'{it("x")}{sb("lean", s)}')
    o.append(lines(s, x0, 26, [f'bag {wb} = {M_BAG:.0f} × {G} = {W_B:.1f} N', f'moment about the spine:', f'{wb}{db} = {W_B:.1f} × {D_B:.2f}', f'= {MOM_B:.1f} N m'], lead=1.4))
    o.append(lines(s, x0, 112, ['leaning away moves the body', f'weight {wt_} aside by {xl}:', f'{wt_}{xl} = {wb}{db}', f'{xl} = {wb}{db} / {wt_}',
                                f'= {MOM_B:.1f} / {W_TR:.0f} = {X_LEAN:.3f} m'], lead=1.4))
    o.append(lines(s, x0, 212, [f'{wt_} = {W_TR:.0f} N (Section 4); the', f'trunk tilts asin({xl}/{it("ℓ")}{sb("t", s)}) = {ALPHA:.1f}°', 'two bags: moments cancel,', 'no lean is needed'], lead=1.4))
    o.append(credit(s, VB))
    aria = ("A skeleton (Lynch art) seen from the front, the subject's right hand, on the left of the image, holding a "
            f"10 kilogram bag, {D_B:.2f} metres from the vertical dashed line through L5/S1. The trunk is tilted "
            f"{ALPHA:.1f} degrees toward the other side, away from the bag. A brown weight arrow W_b = {W_B:.1f} newtons "
            f"hangs from the bag; a brown arrow W_tr = {W_TR:.0f} newtons hangs from the upper-body centre of mass mark, "
            f"which the tilt has moved {X_LEAN:.3f} metres to the other side of the dashed line. Blue dimensions on the "
            f"floor give d_b and x_lean. The bag makes a moment W_b d_b = {W_B:.1f} x {D_B:.2f} = {MOM_B:.1f} newton "
            f"metres about the spine; the lean moves the body weight aside to cancel it, W_tr x_lean = W_b d_b, so "
            f"x_lean = {MOM_B:.1f} / {W_TR:.0f} = {X_LEAN:.3f} metres. Two symmetric bags cancel the moment and need no lean.")
    return finish(VB, aria, s, o)


FIGS[39] = (r'D10: the carry lean. Derive the trunk lean that recentres th', fig39)


# ================================================================ svg #34  D5 jar torque
TAU_RESIST, R_LID, MU_LID = 2.0, 0.035, 0.7  # N m, m, - (line 168)
F_GRIP = TAU_RESIST / (MU_LID * R_LID)
F_TAN = MU_LID * F_GRIP
close(F_GRIP, 82.0, 0.5)                     # line 168, 170: about 82 N
close(F_TAN, 57.0, 0.5)                      # about 57 N, equal to tau_resist / r
close(F_TAN, TAU_RESIST / R_LID, 1e-9)


def fig34():
    p = "m13f34_"
    VB, s = bvb(462)
    o = [defs(p, s)]
    cx, cy, R = 200.0, 150.0, 60.0           # the lid in top view (the lid radius r drawn as R px)
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{BOX}" stroke="{I["secondary"]}" stroke-width="{s(2):.2f}"/>')
    sc = 1.7                                 # the hand art (back of the left hand, fingers up) laid over the lid
    px, py = 11.0 * sc, 30.0 * sc            # palm centre, wrist-local, in art units x scale
    ox, oy = cx + px, cy + py                # rotated 180 deg: the palm centre lands on the lid centre
    o.append(f'<g transform="translate({ox:.2f} {oy:.2f}) rotate(180) scale({sc})" fill="none"><use href="#hbody_arm_hand"/></g>')
    # grip at the two rim contacts (thumb side and little-finger side), each carrying half of the total
    for sg in (-1, 1):
        xr = cx + sg * R
        o.append(H.arrow(s, p, xr + sg * s(44), cy, xr + sg * s(2), cy, "force"))
        o.append(H.arrow(s, p, xr, cy + sg * -s(2), xr, cy - sg * s(38), "reaction"))   # down on the left, up on the right
        o.append(contact_mark(s, xr, cy))
    o.append(lab(s, cx - R - s(46), cy - s(8), f'{it("F")}{sb("grip", s)}/2', "label2", O["force"], "end"))
    o.append(lab(s, cx + R + s(46), cy - s(8), f'{it("F")}{sb("grip", s)}/2', "label2", O["force"]))
    o.append(lab(s, cx - R - s(8), cy + s(54), f'{it("μF")}{sb("grip", s)}/2', "label2", I["primary"], "end"))
    o.append(lab(s, cx + R + s(8), cy - s(46), f'{it("μF")}{sb("grip", s)}/2', "label2", I["primary"]))
    # opening torque about the lid axis (counter-clockwise seen from above), outside the rim
    o.append(arc_arrow(s, p, cx, cy, R + s(14), 150, 30, "force"))
    o.append(lab(s, cx + (R + s(14)) * math.cos(math.radians(30)) + s(10), cy + (R + s(14)) * math.sin(math.radians(30)) + s(16), f'{it("τ")}{sb("open", s)}', "label", O["force"]))
    # the radius, measured from the lid axis to the rim contact
    yd = cy + R + s(54)
    o.append(vline(s, cx, cy, yd + s(5)))
    o.append(vline(s, cx + R, cy, yd + s(5)))
    o.append(dim_h(s, p, cx, cx + R, yd, "geometry"))
    o.append(lab(s, cx + R + s(8), yd + s(5), f'{it("r")} = {R_LID} m', "label2", O["geometry"]))
    fg, tr = f'{it("F")}{sb("grip", s)}', f'{it("τ")}{sb("resist", s)}'
    mu = f'{it("μ")}{sb("lid", s)}'
    ft = f'{it("F")}{sb("t", s)}'
    o.append(lines(s, 8, 292, [f'friction at the rim: {ft} ≤ {mu}{fg}',
                               f'torque about the lid axis: {it("τ")}{sb("open", s)} = {ft} {it("r")} ≤ {mu}{fg}{it("r")}',
                               f'to open the lid: {mu}{fg}{it("r")} ≥ {tr} = {TAU_RESIST:.0f} N m',
                               f'{fg} ≥ {tr} / ({mu}{it("r")}) = {TAU_RESIST:.0f} / ({MU_LID} × {R_LID}) = {F_GRIP:.0f} N',
                               f'tangential force {mu}{fg} = {F_TAN:.0f} N (= {tr} / {it("r")})',
                               'grip and friction are shared by the two contacts'], lead=1.4))
    o.append(credit(s, VB))
    aria = ("Top view of a jar lid, a circle, with the bones of a hand laid over it, fingers up. At the two rim contacts, "
            "left and right, red arrows push inward with half of the grip force F_grip each, and black arrows along the "
            "rim carry half of the friction force, down on the left and up on the right, which turns the lid "
            "counter-clockwise; a red curved arrow below the rim is the opening torque. A blue dimension gives the lid "
            f"radius r = {R_LID} metres. Friction limits the tangential force to mu_lid F_grip, so the torque is at most "
            f"mu_lid F_grip r; opening needs this to reach the resisting torque of {TAU_RESIST:.0f} newton metres, so "
            f"F_grip is at least tau_resist / (mu_lid r) = {TAU_RESIST:.0f} / ({MU_LID} x {R_LID}) = {F_GRIP:.0f} newtons, "
            f"with a tangential force of {F_TAN:.0f} newtons.")
    return finish(VB, aria, s, o)


FIGS[34] = (r'D5: jar torque. Derive the maximum opening torque a grip can', fig34)
