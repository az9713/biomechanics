"""Module 13, group `body_c`: problem figures C1-C3, C5-C10 and D1 (svg #20-22, #24-30), house style, 400 px.

Whole bodies, arms and hands are the posable Lynch skeleton (lynch_body.py); m13/body_main.py puts its defs on the page,
this group only <use>s them (no art crop is embedded here, no SHARED_DEFS).  The page states no stature, so every
metre-to-drawing conversion uses 1.75 m (a design value, as Module 11 does): one metre is M_U = LB.H_U / 1.75 body units.
Every number printed on a figure is computed here from the text's formula and constants; module13.html line numbers:
  line 86, 90   m_up = 0.8 m = 56 kg (m = 70 kg), g = 9.81, d = 0.20 m: tau_knee = m_up g d = 110 N m = 1.57 N m/kg
  line 96, 213  older adult peak 1 to 1.5 N m/kg, young 2 to 3 (K10 baseline 2.5: a chair rise spends 63 %)
  line 655      chair knee-to-COM distance d = 0.15 to 0.28 m (Appendix)
  line 106, 112 riser h = 0.17 m, U_step = m g h = 117 J, f = 1.8 steps/s, P = 210 W; ceiling 250 W (84 %)
  line 126, 132 W_tr = 412 N, l_t = 0.346 m, d_m = 0.05 m, W_L = 196.2 N (20 kg); stoop phi = 60 deg: d_L 0.40 m gives
                F_m = 4040 N, F_comp = 4350 N; d_L 0.25 m gives 3760 N (a 14 % saving); NIOSH limit 3400 N
  line 146      m = 70 kg, v = 1.3 m/s, beta = 60 deg: J = 2 m v sin(beta/2) = 91 N s
  line 154-156  xi = x_com + xdot / omega_0, omega_0 = sqrt(g / l), l = 1.0 m: 3.13 rad/s (Appendix line 674)
  line 168, 174 mu_lid 0.5 (dry skin) / 0.7 / 1.0 (rubber), r = 0.035 m, tau_resist = 2 N m, grip 60 N (weak)
  line 176      tau_door = 20 N m, d_hinge = 0.8 m: F = 25 N
  line 184      m = 70 kg, v = 1.0 m/s: P_slope = m g v sin(theta) = 60, 119, 178 W at 5, 10, 15 deg
  line 425      bag 10 kg at d_b = 0.30 m: 29.4 N m, x_lean = W_b d_b / W_tr = 0.071 m (W_tr = 412 N)
Poses the text does not fix are design values (marked in the code).
"""
import math

import house as H
import lynch_body as LB

T, O, I = H.TISSUE, H.OVERLAY, H.INK
M_U = LB.H_U / 1.75                       # body units per metre (stature 1.75 m, a design value)
BOX = "#f7f4ef"
G = 9.81
MASS, M_UP = 70.0, 56.0                   # line 90
UP = ["head", "trunk"] + [a + s for a in ("upper_arm", "forearm", "hand", "thigh") for s in ("", "_far")]


# ---------------------------------------------------------------- drawing helpers
def VBs(h):
    return (0, 0, 400, h), H.Scale(400, h, display_w=400, max_h=H.MAX_DISPLAY_H_BODY)


def lab(s, x, y, text, size="label", fill=I["primary"], anchor="start", extra=""):
    return H.label(s, x, y, text, size, fill, anchor, extra)


def lines(s, x, y, rows, size="label2", anchor="start", lead=1.3, fill=I["primary"]):
    return "".join(lab(s, x, y + i * s(H.PX[size]) * lead, t, size, fill, anchor) for i, t in enumerate(rows))


def it(v):
    return f'<tspan font-style="italic">{v}</tspan>'


def sb(t, s, size="label"):
    return H.sub(t, s, size)


def ext(s, x0, y0, x1, y1, col=O["dim"]):
    return H.line(s, x0, y0, x1, y1, col, "ref", H.DASH_REF)


def floor(s, x0, x1, y):
    n = int((x1 - x0) / s(10))
    o = [H.line(s, x0, y, x1, y, I["axis"], "axis")]
    o += [H.line(s, x0 + s(10) * i + s(8), y + s(1), x0 + s(10) * i, y + s(7), I["rule"], "leader") for i in range(n)]
    return "".join(o)


def finish(vb, aria, s, body):
    """Close a figure; drop the arrowheads it never uses."""
    import re
    body = "".join(body)
    body = re.sub(r'<marker id="([^"]+)".*?</marker>',
                  lambda m: m.group(0) if f"url(#{m.group(1)})" in body else "", body)
    body = body.replace("<defs></defs>", "")
    return H.svg_open(vb, aria.replace("&", "&amp;").replace('"', "&quot;"), s) + body + "</svg>"


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


CREDIT_H = 46                              # user units reserved for a 3-line credit at 400 px


def put(P, x_left, y_floor, hpx, **kw):
    """Draw pose P at stature hpx, bbox left edge at x_left, anchor level at y_floor.  Returns (svg, J)."""
    _, J0 = LB.draw("m13", H.Scale(400, 400), P, 0.0, y_floor, hpx, **kw)
    return LB.draw("m13", H.Scale(400, 400), P, x_left - J0["bbox"][0], y_floor, hpx, **kw)


def arc_arrow(s, p, cx, cy, r, a0, a1, meaning="force", w="force"):
    """Arc about (cx, cy) from screen angle a0 to a1 (deg, 0 = +x, 90 = down); a1 > a0 runs clockwise on screen."""
    sweep = 1 if a1 > a0 else 0
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if abs(a1 - a0) > 180 else 0
    return (f'<path d="M{x0:.2f},{y0:.2f} A{r:.2f},{r:.2f} 0 {large} {sweep} {x1:.2f},{y1:.2f}" fill="none" '
            f'stroke="{O[meaning]}" stroke-width="{s(H.PX[w]):.2f}" marker-end="url(#{p}a_{meaning})"/>')


def upper_com(P, J=None):
    """Centre of mass of the body above the knees (head, trunk, both arms, both thighs; Winter fractions of the kit),
    in body units (J None) or in figure units (J from draw).  Returns (point, mass fraction)."""
    tot = x = y = 0.0
    for k in UP:
        c, m = P.com[k]
        if J is not None:
            c = J["com_" + k]
        tot += m
        x += c[0] * m
        y += c[1] * m
    return (x / tot, y / tot), tot


def d_knee(P):
    """Horizontal distance, knee to the upper-body COM, metres (+ = COM behind the knee)."""
    return (P.j["knee"][0] - upper_com(P)[0][0]) / M_U


def bisect(f, lo, hi, target, n=60):
    flo = f(lo) - target
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        fm = f(mid) - target
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- seat-off pose (design values, tuned to the text's d)
def sts_pose(hf, trunk, th_s=15.0, pelvis=25.0, sh=45.0, el=0.0):
    """Seat-off, both legs alike.  hf = hip flexion (the thigh turned from vertical, pelvis tilt removed), shank leaning
    th_s deg forward (the kit's sit_to_stand has 15), arms reaching forward."""
    kf = th_s - pelvis + hf
    L = dict(hip=hf, knee=kf, shoulder=sh, elbow=el)
    return LB.pose(pelvis=pelvis, trunk=trunk, near=dict(L), far=dict(L))


def sts_for_d(hf, d_m):
    """Seat-off pose whose upper-body COM is d_m metres behind the knee: the trunk lean is solved."""
    tr = bisect(lambda t: d_knee(sts_pose(hf, t)), -10.0, 80.0, d_m)
    P = sts_pose(hf, tr)
    assert abs(d_knee(P) - d_m) < 1e-6
    return P, tr


def seat(s, J, kind, HF):
    """Schematic seat under the hip (not anatomy): a plank on four legs, or a low soft armchair."""
    hx, hy = J["hip"]
    y = hy + 0.052 * HF                                   # hip joint centre to the seat surface (design value)
    fl = J["floor_y"]
    o = []
    if kind == "stool":
        xa, xb = hx - 0.20 * HF, hx + 0.08 * HF
        o.append(f'<rect x="{xa:.2f}" y="{y:.2f}" width="{xb - xa:.2f}" height="{s(6):.2f}" rx="{s(2):.2f}" fill="{BOX}" '
                 f'stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
        for xx in (xa + s(8), xb - s(8)):
            o.append(H.line(s, xx, y + s(6), xx, fl, I["secondary"], "axis"))
    else:
        xa, xb = hx - 0.30 * HF, hx + 0.09 * HF
        yb = y + s(14)
        o.append(f'<rect x="{xa:.2f}" y="{y - 0.34 * HF:.2f}" width="{s(16):.2f}" height="{fl - (y - 0.34 * HF):.2f}" '
                 f'rx="{s(6):.2f}" fill="{BOX}" stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
        o.append(f'<rect x="{xa:.2f}" y="{y:.2f}" width="{xb - xa:.2f}" height="{fl - y:.2f}" rx="{s(8):.2f}" '
                 f'fill="{BOX}" stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
        o.append(f'<path d="M{xa + s(16):.2f},{yb:.2f} H{xb - s(4):.2f}" stroke="{I["rule"]}" stroke-width="{s(1.0):.2f}" '
                 f'fill="none" stroke-dasharray="{s(3):.2f} {s(3):.2f}"/>')
    return "".join(o)


def sts_marks(s, p, P, J, HF, d_m, y_dim, label_col=O["geometry"], show_w=True, wlen=0.20):
    """Knee centre, upper-body COM, its weight, the dashed lines and the d dimension.  Returns (svg, com, knee)."""
    com, _ = upper_com(P, J)
    kn = J["knee"]
    o = [ext(s, kn[0], kn[1], kn[0], y_dim),
         ext(s, com[0], com[1], com[0], y_dim, O["load"])]
    o.append(H.arrow(s, p, kn[0] - 0.0, y_dim, com[0], y_dim, "geometry", both=True))
    o.append(H.joint_centre(s, *kn))
    o.append(H.com_mark(s, *com))
    if show_w:
        o.append(H.arrow(s, p, com[0], com[1] + s(8), com[0], com[1] + wlen * HF, "load"))
    return "".join(o), com, kn


# ================================================================ svg #20  C1 the low soft chair
def put_hip(P, hip_x, y_floor, hpx):
    """Draw pose P with its hip joint at x = hip_x and the anchor level at y_floor."""
    _, J0 = LB.draw("m13", H.Scale(400, 400), P, 0.0, y_floor, hpx)
    return LB.draw("m13", H.Scale(400, 400), P, hip_x - J0["hip"][0], y_floor, hpx)


def fig20():
    p = "m13f20_"
    HF, fy = 285.0, 304.0
    VB, s = VBs(fy + 62 + CREDIT_H)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    cases = [("tall firm stool", "stool", 75.0, 0.15, 100.0), ("low soft armchair", "armchair", 125.0, 0.28, 292.0)]
    taus = []
    for name, kind, hf, d_m, hx in cases:
        P, tr = sts_for_d(hf, d_m)
        sv, J = put_hip(P, hx, fy, HF)
        tau = M_UP * G * d_m
        taus.append(tau)
        o.append(seat(s, J, kind, HF))
        o.append(sv)
        y_dim = fy - 0.115 * HF
        mk, com, kn = sts_marks(s, p, P, J, HF, d_m, y_dim)
        o.append(mk)
        o.append(lab(s, hx + 0.12 * HF, 20, name, "label", I["primary"], "middle"))
        o.append(lab(s, (com[0] + kn[0]) / 2, y_dim + s(17), f'{it("d")} = {d_m:.2f} m', "label2", O["geometry"], "middle"))
        o.append(lab(s, com[0] - s(6), com[1] + 0.11 * HF, f'{it("m")}{sb("up", s, "label2")} {it("g")}', "label2", O["load"], "end"))
        o.append(lines(s, hx + 0.12 * HF, fy + s(24), [f'{it("τ")} = {it("m")}{sb("up", s, "label2")} {it("g d")} = {tau:.0f} N m',
                                                      f'= {tau / MASS:.1f} N m per kg'], "label2", "middle"))
    ratio = taus[1] / taus[0]
    o.append(lab(s, 200, 40, f"same person, 56 kg above the knees: {ratio:.1f} times the knee torque", "label2",
                 I["secondary"], "middle"))
    o.append(floor(s, 6, 394, fy))
    o.append(credit(s, VB))
    aria = ("Two skeletons (Lynch art) at the instant the thighs leave the seat, side view, each with the centre of mass of "
            "the body above the knees (black and white mark), its weight m_up g = 549 N (brown arrow) and the horizontal "
            "distance d from the knee joint to that weight line (blue double arrow). Left, a tall firm stool: d = 0.15 m, "
            f"knee torque {taus[0]:.0f} N m. Right, a low soft armchair: d = 0.28 m, {taus[1]:.0f} N m, {ratio:.1f} times as "
            "much. The torque is 56 kg times 9.81 times d.")
    return finish(VB, aria, s, o)


# ================================================================ svg #30  D1 chair-rise torque
def fig30():
    p = "m13f30_"
    HF, fy = 300.0, 270.0
    VB, s = VBs(fy + 16 + CREDIT_H)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    d_m = 0.20
    P, tr = sts_for_d(105.0, d_m)
    sv, J = put_hip(P, 78, fy, HF)
    o.append(seat(s, J, "stool", HF))
    o.append(sv)
    y_dim = fy - 0.10 * HF
    mk, com, kn = sts_marks(s, p, P, J, HF, d_m, y_dim, wlen=0.20)
    o.append(mk)
    tau = M_UP * G * d_m
    o.append(arc_arrow(s, p, kn[0], kn[1], s(24), 200, 330, "force"))
    o.append(lab(s, kn[0] + s(28), kn[1] - s(24), f'{it("τ")}{sb("knee", s)}', "label", O["force"]))
    o.append(lab(s, (com[0] + kn[0]) / 2, y_dim + s(18), f'{it("d")} = {d_m:.2f} m', "label", O["geometry"], "middle"))
    o.append(lab(s, com[0] - s(6), com[1] + 0.045 * HF, f'{it("m")}{sb("up", s)} {it("g")}', "label", O["load"], "end"))
    o.append(lab(s, 200, 20, "moments about the knee, quasi-static", "label", I["primary"], "middle"))
    o.append(lines(s, 236, 74, [f'{it("m")}{sb("up", s, "label2")} = 0.8 × 70 = {M_UP:.0f} kg',
                                f'{it("m")}{sb("up", s, "label2")} {it("g")} = {M_UP * G:.0f} N at the COM',
                                f'{it("d")} = {d_m:.2f} m, COM behind',
                                'the knee joint',
                                f'{it("τ")}{sb("knee", s, "label2")} = {it("m")}{sb("up", s, "label2")} {it("g d")}',
                                f'= {M_UP * G:.0f} N × {d_m:.2f} m',
                                f'≈ {tau:.0f} N m',
                                f'= {tau / MASS:.2f} N m per kg'], "label2", lead=1.45))
    o.append(floor(s, 6, 394, fy))
    o.append(credit(s, VB))
    aria = ("A skeleton (Lynch art) in side view at seat-off. The black and white mark is the centre of mass of the body above "
            "the knees; its weight, 56 kg times 9.81 or 549 N, is the brown arrow. The blue double arrow is the horizontal "
            "distance d = 0.20 m from the knee joint to that weight line. The red arc at the knee is the extensor torque "
            f"that balances it: {tau:.0f} N m, or {tau / MASS:.2f} N m per kilogram of body mass.")
    return finish(VB, aria, s, o)


# ================================================================ arm helpers (planar, lateral view)
def arm_ik(S, T, th_t, branch=1):
    """Shoulder flexion and elbow flexion (deg) that put the fingertip at T (body units) for a shoulder at S, hand collinear
    with the forearm.  th_t = trunk angle (deg).  The elbow bends forward (kit convention: th_f = th_u - elbow)."""
    L1, L2 = LB.L_UPPER, LB.L_FORE + LB.L_HAND
    dx, dy = T[0] - S[0], T[1] - S[1]
    r = math.hypot(dx, dy)
    assert r <= L1 + L2 + 1e-9, (r, L1 + L2)
    r = max(r, abs(L1 - L2) + 1e-9)
    e = math.pi - math.acos(max(-1.0, min(1.0, (L1 * L1 + L2 * L2 - r * r) / (2 * L1 * L2))))
    g = math.acos(max(-1.0, min(1.0, (L1 * L1 + r * r - L2 * L2) / (2 * L1 * r))))
    th_T = math.atan2(-dx, dy)
    th_u = math.degrees(th_T + g)
    return th_t - th_u, math.degrees(e)


def fig_pt(J, P, q):
    """A body-unit point q of pose P -> figure units, using the placement in J."""
    ax, ay = P.anchor
    k = J["scale"]
    return (J["_x"] + k * (q[0] - ax), J["_y"] + k * (q[1] - ay))


def put2(P, x_left, y_floor, hpx):
    """put() that records the placement (x, y, height) in J."""
    _, J0 = LB.draw("m13", H.Scale(400, 400), P, 0.0, y_floor, hpx)
    x = x_left - J0["bbox"][0]
    sv, J = LB.draw("m13", H.Scale(400, 400), P, x, y_floor, hpx)
    J["_x"], J["_y"], J["_h"] = x, y_floor, hpx
    return sv, J


# ================================================================ svg #22  C3 keep it close (stoop, load near or far)
W_TR, LT, DM, W_L = 412.0, 0.30 / math.sin(math.radians(60)), 0.05, 20.0 * G     # lines 126, 355 (Lab C: d_tr = 0.30 m at 60 deg)
PHI = 60.0                                                  # stoop, line 126


def lift_numbers(phi, d_l):
    d_tr = LT * math.sin(math.radians(phi))
    fm = (W_TR * d_tr + W_L * d_l) / DM
    return d_tr, fm, fm + (W_TR + W_L) * math.cos(math.radians(phi))


def stoop_pose(d_l, hand_h=0.34):
    """Stoop (trunk phi = 60 deg from vertical, knees straight, design split pelvis 35 + lumbar 25); both arms straight to
    the box, fingertip d_l metres ahead of L5/S1 and hand_h stature above the floor."""
    base = dict(pelvis=35.0, trunk=25.0)
    leg = dict(hip=45.0)
    P0 = LB.pose(near=dict(leg), far=dict(leg), **base)
    S = P0.j["shoulder"]
    T = (P0.j["l5s1"][0] + d_l * M_U, P0.floor_y - hand_h * LB.H_U)
    sh, el = arm_ik(S, T, base["pelvis"] + base["trunk"])
    arm = dict(leg, shoulder=sh, elbow=el)
    P = LB.pose(near=dict(arm), far=dict(arm), **base)
    q = P.j["fingertip"]
    assert math.hypot(q[0] - T[0], q[1] - T[1]) < 1e-6
    return P


# the text's rounded values (l.126-132): the computed ones (3453/3757, 4042/4346 N) agree to under 5 N
TXT_FM_FC = {0.25: (3450, 3760), 0.40: (4040, 4350)}


def fig22():
    p = "m13f22_"
    HF, fy = 240.0, 250.0
    VB, s = VBs(fy + 104 + CREDIT_H)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    nums = []
    for name, d_l, xl in (("load close", 0.25, 24.0), ("load far", 0.40, 214.0)):
        P = stoop_pose(d_l)
        _, J0 = put2(P, xl, fy, HF)
        sv, J = put2(P, xl, fy, HF)
        d_tr, fm_x, fc_x = lift_numbers(PHI, d_l)
        fm, fc = TXT_FM_FC[d_l]                                 # the text's rounded values; computed ones asserted below
        nums.append((d_l, fm, fc, fm_x, fc_x))
        l5, hand = J["l5s1"], J["fingertip"]
        bw = 0.30 * HF / 1.75                                   # a 20 kg box, 0.30 m a side (design value)
        bx, by = l5[0] + d_l * HF / 1.75, hand[1] + 0.25 * bw
        o.append(f'<rect x="{bx - bw / 2:.2f}" y="{by - bw / 2:.2f}" width="{bw:.2f}" height="{bw:.2f}" rx="{s(2):.2f}" '
                 f'fill="{BOX}" stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
        o.append(sv)
        y_dim = fy + s(16)
        o.append(ext(s, l5[0], l5[1], l5[0], y_dim))
        o.append(ext(s, bx, by + bw / 2, bx, y_dim, O["load"]))
        o.append(H.arrow(s, p, l5[0], y_dim, bx, y_dim, "geometry", both=True))
        o.append(H.joint_centre(s, *l5))
        o.append(H.arrow(s, p, bx, by + bw / 2 + s(2), bx, by + bw / 2 + 0.16 * HF, "load"))
        o.append(lab(s, bx + s(6), by + bw / 2 + 0.11 * HF, f'{it("W")}{sb("L", s, "label2")} = {W_L:.0f} N', "label2", O["load"]))
        o.append(lab(s, (l5[0] + bx) / 2, y_dim + s(17), f'{it("d")}{sb("L", s, "label2")} = {d_l:.2f} m', "label2", O["geometry"], "middle"))
        cx = xl + 92
        o.append(lab(s, cx, 20, name, "label", I["primary"], "middle"))
        o.append(lines(s, cx, fy + s(52), [f'{it("F")}{sb("m", s, "label2")} ≈ {fm:.0f} N',
                                          f'{it("F")}{sb("comp", s, "label2")} ≈ {fc:.0f} N'], "label2", "middle"))
        o.append(lab(s, l5[0] - s(9), l5[1] - s(6), "L5/S1", "label2", I["primary"], "end"))
    saving = 1 - nums[0][4] / nums[1][4]
    per_cm = W_L / DM / 100
    o.append(lab(s, 200, 40, f"same stoop (φ = 60°), same box: {saving * 100:.0f}% less compression when close", "label2",
                 I["secondary"], "middle"))
    o.append(lab(s, 200, fy + s(98), f"each cm of reach adds {it('W')}{sb('L', s, 'label2')} / {it('d')}{sb('m', s, 'label2')} / 100 = "
                 f"{per_cm:.0f} N of back-muscle force", "label2", I["secondary"], "middle"))
    o.append(floor(s, 6, 394, fy))
    o.append(credit(s, VB))
    aria = ("Two skeletons (Lynch art), side view, bent forward 60 degrees from vertical with straight legs, each holding the same "
            "20 kg box (weight 196 N, brown arrow) in straight arms. The blue double arrow is the horizontal distance d_L from "
            f"the L5/S1 joint (crosshair) to the load line. Left, the box is close: d_L = 0.25 m, back-muscle force about {nums[0][1]:.0f} N, "
            f"disc compression about {nums[0][2]:.0f} N. Right, the box is far: d_L = 0.40 m, about {nums[1][1]:.0f} N and {nums[1][2]:.0f} N, "
            f"{saving * 100:.0f} percent more.")
    assert abs(nums[1][4] - 4350) < 5 and abs(nums[0][4] - 3760) < 5 and abs(saving - 0.14) < 0.006, nums
    assert abs(nums[1][3] - 4040) < 5 and abs(nums[0][3] - 3450) < 5, nums
    return finish(VB, aria, s, o)


# ================================================================ leg helper: put an ankle on a target (planar, lateral view)
def leg_ik(D, pelvis):
    """Hip flexion, knee flexion and shank angle (deg) that put the ankle at D (body units, hip at the origin), knee forward."""
    a, b = LB.OFF["lat_thigh"]["knee"], LB.OFF["lat_shank"]["ankle"]
    l1, l2, r = math.hypot(*a), math.hypot(*b), math.hypot(*D)
    assert abs(l1 - l2) < r < l1 + l2, (r, l1, l2)
    ga = math.acos((l1 * l1 + r * r - l2 * l2) / (2 * l1 * r))
    ang = math.atan2(D[1], D[0]) - ga                       # smaller screen angle = knee turned forward (+x)
    th_th = math.degrees(ang - math.atan2(a[1], a[0]))
    A = LB.rot(a, th_th)
    B = (D[0] - A[0], D[1] - A[1])
    th_s = math.degrees(math.atan2(B[1], B[0]) - math.atan2(b[1], b[0]))
    return pelvis - th_th, th_s - th_th, th_s


def solve_leg(base, fixed_side, fixed_leg, vec_fn, th_foot, arms=None):
    """The `fixed_side` leg ('near' or 'far') is given; the other leg's ankle goes to the fixed ankle + vec_fn(fixed ankle).
    Both feet are turned th_foot deg (+ = clockwise on screen, so negative = toe up).  Returns the Pose."""
    arms = arms or {}
    other = "far" if fixed_side == "near" else "near"
    leg = dict(fixed_leg)
    th_th = base.get("pelvis", 0.0) - leg["hip"]
    th_s = th_th + leg["knee"]
    leg["contact"], leg["ankle"] = None, th_s - th_foot
    leg.update(arms)
    Pa = LB.pose(**base, **{fixed_side: leg, other: dict(arms)})
    sfx = "" if fixed_side == "near" else "_far"
    T = vec_fn(Pa.j["ankle" + sfx])
    hf, kf, th_s2 = leg_ik((T[0] - Pa.j["hip"][0], T[1] - Pa.j["hip"][1]), base.get("pelvis", 0.0))
    oth = dict(hip=hf, knee=kf, contact=None, ankle=th_s2 - th_foot)
    oth.update(arms)
    P = LB.pose(**base, **{fixed_side: leg, other: oth})
    sfo = "_far" if other == "far" else ""
    q = P.j["ankle" + sfo]
    assert math.hypot(q[0] - T[0], q[1] - T[1]) < 1e-6, (q, T)
    return P


def tread_poly(s, pts, y_base):
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + f" L{pts[-1][0]:.2f},{y_base:.2f} L{pts[0][0]:.2f},{y_base:.2f} Z"
    return (f'<path d="{d}" fill="{BOX}" stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}" stroke-linejoin="round"/>')


# ================================================================ svg #21  C2 down is worse than up (stairs)
H_RISE = 0.17                                               # line 106
U_STEP = MASS * G * H_RISE                                  # 117 J
P_STAIR = MASS * G * H_RISE * 1.8                           # 210 W at 1.8 steps/s


def stair_pose(up):
    base = dict(pelvis=4.0, trunk=6.0) if up else dict(pelvis=0.0, trunk=16.0)
    arms = dict(shoulder=-10.0, elbow=15.0) if up else dict(shoulder=18.0, elbow=25.0)
    dy = -H_RISE * M_U if up else H_RISE * M_U
    if up:        # trailing leg (far) on the lower tread, nearly straight; the near leg is on the next tread
        P = solve_leg(base, "far", dict(hip=-8.0, knee=10.0), lambda a: (a[0] + 0.30 * M_U, a[1] + dy), 0.0, arms=arms)
        P.anchor = (P.j["heel_far"][0], P.j["heel_far"][1])
    else:         # the near leg is on the upper tread, knee flexed under load; the far leg reaches down to the next tread
        P = solve_leg(base, "near", dict(hip=80.0, knee=110.0), lambda a: (a[0] + 0.30 * M_U, a[1] + dy), 0.0, arms=arms)
    return P


def fig21():
    p = "m13f21_"
    HF, fy = 232.0, 268.0
    VB, s = VBs(fy + 122 + CREDIT_H)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    for up, xl in ((True, 14.0), (False, 206.0)):
        P = stair_pose(up)
        sv, J = put2(P, xl + (6 if up else 0), fy, HF)
        h_px = H_RISE * HF / 1.75
        if up:
            y_lo, y_hi = fy, fy - h_px
            xr = (J["toe_far"][0] + J["heel"][0]) / 2
            polys = [(-10, y_lo), (xr, y_lo), (xr, y_hi), (410, y_hi)]
        else:
            y_hi, y_lo = fy, fy + h_px
            xr = (J["toe"][0] + J["heel_far"][0]) / 2
            polys = [(-10, y_hi), (xr, y_hi), (xr, y_lo), (410, y_lo)]
        polys = [(max(xl - 6, min(xl + 190, x)), y) for x, y in polys]
        o.append(tread_poly(s, polys, fy + 26 + h_px))
        o.append(sv)
        com = J["com"]
        o.append(H.com_mark(s, *com))
        o.append(H.arrow(s, p, com[0], com[1] + s(9), com[0], com[1] + 0.20 * HF, "load"))
        o.append(lab(s, com[0] + s(7), com[1] + 0.15 * HF, f'{it("m g")}', "label2", O["load"]))
        ax = com[0] - 0.20 * HF
        y0, y1 = (com[1], com[1] - h_px) if up else (com[1], com[1] + h_px)
        o.append(H.arrow(s, p, ax, y0, ax, y1, "geometry"))
        o.append(ext(s, ax, y0, com[0] - s(8), y0))
        o.append(lab(s, ax - s(5), (y0 + y1) / 2 + s(4), f'{"+" if up else "−"}{it("h")}', "label2", O["geometry"], "end"))
        cx = xl + 98
        o.append(lab(s, cx, 20, "ascent" if up else "descent", "label", I["primary"], "middle"))
        rows = ([f'+{it("m g h")} = +{U_STEP:.0f} J per step', f'{it("m g h f")} ≈ {P_STAIR:.0f} W at 1.8 steps/s',
                 "legs shorten: positive work"] if up else
                [f'−{it("m g h")} = −{U_STEP:.0f} J per step', "knee extensors lengthen under",
                 "load: negative work (eccentric)"])
        o.append(lines(s, cx, fy + s(70), rows, "label2", "middle"))
    o.append(lab(s, 200, 40, f"riser {it('h')} = {H_RISE:.2f} m, {it('m')} = {MASS:.0f} kg: a step moves the centre of mass by {it('h')}",
                 "label2", I["secondary"], "middle"))
    o.append(credit(s, VB))
    aria = ("Two skeletons (Lynch art), side view, on stairs with a 0.17 m riser; each has the centre of mass marked (black and "
            "white) with its weight m g (brown arrow) and a blue arrow of length h = 0.17 m. Left, ascent: the centre of mass "
            f"rises h, the legs shorten and do positive work m g h = {U_STEP:.0f} J per step, about {P_STAIR:.0f} W at 1.8 steps "
            "per second. Right, descent: the centre of mass drops h and the knee extensors lengthen under load, negative work "
            f"of {U_STEP:.0f} J per step.")
    assert abs(U_STEP - 117) < 1 and abs(P_STAIR - 210) < 1
    return finish(VB, aria, s, o)


# ================================================================ svg #28  C9 lungs up, knees down (slope)
THETA, V_SLOPE = 15.0, 1.0                                 # 15 deg: the steepest grade of line 184 (178 W)


def slope_pose(up):
    th = THETA
    rad = math.radians(th)
    if up:
        base, foot = dict(pelvis=4.0, trunk=7.0), -th                       # rise to the right: toe up
        P = solve_leg(base, "near", dict(hip=-14.0, knee=18.0),
                      lambda a: (a[0] + 0.40 * M_U * math.cos(rad), a[1] - 0.40 * M_U * math.sin(rad)), foot,
                      arms=dict(shoulder=-14.0, elbow=15.0))
    else:
        base, foot = dict(pelvis=-2.0, trunk=0.0), th                       # fall to the right: toe down
        P = solve_leg(base, "near", dict(hip=-10.0, knee=34.0),
                      lambda a: (a[0] + 0.36 * M_U * math.cos(rad), a[1] + 0.36 * M_U * math.sin(rad)), foot,
                      arms=dict(shoulder=14.0, elbow=20.0))
    return P


def fig28():
    p = "m13f28_"
    HF, fy = 232.0, 322.0
    VB, s = VBs(fy + 116 + CREDIT_H)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    rad = math.radians(THETA)
    mgN = MASS * G
    along, perp = mgN * math.sin(rad), mgN * math.cos(rad)
    P_W = along * V_SLOPE
    kf = 0.105                                              # px per newton
    for up, xl in ((True, 10.0), (False, 206.0)):
        P = slope_pose(up)
        sv, J = put2(P, xl, fy, HF)
        hl, tp = J["heel"], J["toe"]
        ang = math.atan2(tp[1] - hl[1], tp[0] - hl[0])
        assert abs(math.degrees(ang) - (-THETA if up else THETA)) < 0.2, math.degrees(ang)
        slope = math.tan(ang)
        x0, x1 = xl - 4, xl + 186
        ys = lambda x: hl[1] + slope * (x - hl[0])          # noqa: E731
        y_base = max(ys(x0), ys(x1)) + 20
        o.append(tread_poly(s, [(x0, ys(x0)), (x1, ys(x1))], y_base))
        o.append(sv)
        com = J["com"]
        o.append(H.com_mark(s, *com))
        # weight and its two components (brown: all three are the weight)
        u_dn = (-math.cos(rad), math.sin(rad)) if up else (math.cos(rad), math.sin(rad))
        n_in = (math.sin(rad), math.cos(rad)) if up else (-math.sin(rad), math.cos(rad))
        wx, wy = com[0], com[1] + mgN * kf
        o.append(H.arrow(s, p, com[0], com[1] + s(8), wx, wy, "load"))
        ax_, ay_ = com[0] + u_dn[0] * along * kf, com[1] + u_dn[1] * along * kf
        nx_, ny_ = com[0] + n_in[0] * perp * kf, com[1] + n_in[1] * perp * kf
        o.append(ext(s, wx, wy, ax_, ay_, O["load"]))
        o.append(ext(s, wx, wy, nx_, ny_, O["load"]))
        o.append(H.arrow(s, p, com[0], com[1], ax_, ay_, "load"))
        o.append(H.arrow(s, p, com[0], com[1], nx_, ny_, "load"))
        sg = 1 if up else -1                                 # uphill: the into-slope component leans right of the weight
        o.append(lab(s, wx - sg * s(5), wy + s(14), f'{it("m g")}', "label2", O["load"], "end" if up else "start"))
        o.append(lab(s, nx_ + sg * s(7), ny_ + s(12), f'{it("m g")} cos{it("θ")}', "label2", O["load"], "start" if up else "end"))
        o.append(lab(s, ax_ - sg * s(5), ay_ - s(3), f'{it("m g")} sin{it("θ")}', "label2", O["load"], "end" if up else "start"))
        vx0 = xl + 112 if up else xl + 120
        d_ = (math.cos(ang), math.sin(ang))
        vy0 = ys(vx0) - 0.68 * HF
        o.append(H.arrow(s, p, vx0, vy0, vx0 + d_[0] * s(34), vy0 + d_[1] * s(34), "dim"))
        o.append(lab(s, vx0 + s(14), vy0 - s(8), f'{it("v")}', "label2", O["dim"]))
        cx = xl + 98
        o.append(lab(s, cx, 20, "uphill" if up else "downhill", "label", I["primary"], "middle"))
        rows = ([f'muscles add +{P_W:.0f} W', "positive work: an aerobic", "demand on lungs and heart"] if up else
                [f'muscles absorb −{P_W:.0f} W', "negative work: eccentric", "braking, loads the knee"])
        o.append(lines(s, cx, 40, rows, "label2", "middle"))
    yb = fy + 90
    o.append(lab(s, 200, yb, f"slope {it('θ')} = {THETA:.0f}° ({math.tan(rad) * 100:.0f}% grade), {it('m')} = {MASS:.0f} kg, "
                 f"{it('v')} = {V_SLOPE:.1f} m/s", "label2", I["secondary"], "middle"))
    o.append(lab(s, 200, yb + s(17), f"{it('P')} = {it('m g v')} sin{it('θ')} = {along:.0f} N × {V_SLOPE:.1f} m/s = {P_W:.0f} W "
                 f"(sign: + uphill, − downhill)", "label2", I["primary"], "middle"))
    o.append(credit(s, VB))
    aria = ("Two skeletons (Lynch art), side view, walking at 1.0 m/s on a 15 degree slope, uphill on the left and downhill on the "
            "right. Each has the centre of mass marked with its weight m g (brown arrow) split into a component along the slope, "
            f"m g sin theta = {along:.0f} N, and one into the slope, m g cos theta. Uphill the muscles add {P_W:.0f} W (positive "
            f"work, an aerobic demand); downhill they absorb {P_W:.0f} W eccentrically, which loads the quadriceps and knee.")
    assert abs(P_W - 178) < 1
    return finish(VB, aria, s, o)


# ================================================================ svg #24  C5 the lean away (anterior view)
W_B, D_B = 10.0 * G, 0.30                                   # bag 10 kg at 0.30 m (lines 425, 671)
X_LEAN = W_B * D_B / W_TR                                   # 0.0714 m (line 425)


def put_ant(P, x_mid, y_floor, hpx):
    """Draw an anterior pose with the mid-hip point at x_mid and the soles on y_floor."""
    _, J0 = LB.draw("m13", H.Scale(400, 400), P, 0.0, y_floor, hpx)
    return LB.draw("m13", H.Scale(400, 400), P, x_mid - J0["hip_mid"][0], y_floor, hpx)


def bag_pose(psi):
    """Anterior pose, trunk leaning psi deg away from the bag (bag in the subject's left hand, screen right); the left arm is
    swung so the grip (35% of the way from wrist to fingertip) hangs d_b = 0.30 m from the mid-hip axis."""
    A = LB._ANT_ARMS

    def grip_x(sh):
        P = LB.pose_ant(trunk=-psi, r=dict(A), l=dict(A, shoulder=sh), anchor=("sole", "l"))
        j = P.j
        return (j["wrist_l"][0] + 0.35 * (j["fingertip_l"][0] - j["wrist_l"][0])) / M_U
    sh = bisect(grip_x, -20.0, 50.0, D_B)
    P = LB.pose_ant(trunk=-psi, r=dict(A), l=dict(A, shoulder=sh), anchor=("sole", "l"))
    assert abs(grip_x(sh) - D_B) < 1e-6
    return P


def fig24():
    p = "m13f24_"
    HF, fy = 262.0, 316.0
    VB, s = VBs(fy + 26 + 70 + CREDIT_H)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    k = HF / 1.75                                            # px per metre
    psi = math.degrees(math.asin(X_LEAN / LT))
    moment = W_B * D_B
    for lean, xm in ((False, 84.0), (True, 278.0)):
        P = bag_pose(psi if lean else 0.0)
        sv, J = put_ant(P, xm, fy, HF)
        l5 = J["l5s1"]
        th_t = -(psi if lean else 0.0)
        ub = (l5[0] + LT * k * math.sin(math.radians(th_t)), l5[1] - LT * k * math.cos(math.radians(th_t)))
        gx = J["wrist_l"][0] + 0.35 * (J["fingertip_l"][0] - J["wrist_l"][0])
        gy = J["wrist_l"][1] + 0.35 * (J["fingertip_l"][1] - J["wrist_l"][1])
        bw, bh = 0.26 * k, 0.30 * k
        btop = gy + 0.07 * k
        o.append(f'<path d="M{gx:.2f},{gy:.2f} L{gx - 0.06 * k:.2f},{btop:.2f} M{gx:.2f},{gy:.2f} L{gx + 0.06 * k:.2f},{btop:.2f}" '
                 f'fill="none" stroke="{I["secondary"]}" stroke-width="{s(1.6):.2f}"/>')
        o.append(f'<rect x="{gx - bw / 2:.2f}" y="{btop:.2f}" width="{bw:.2f}" height="{bh:.2f}" rx="{s(4):.2f}" fill="{BOX}" '
                 f'stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
        o.append(sv)
        ax_x = J["hip_mid"][0]
        o.append(ext(s, ax_x, l5[1] - 0.24 * HF, ax_x, fy + s(16)))                       # the spine axis
        y_dim = fy + s(16)
        o.append(ext(s, gx, btop + bh, gx, y_dim, O["load"]))
        o.append(H.arrow(s, p, ax_x, y_dim, gx, y_dim, "geometry", both=True))
        o.append(lab(s, (ax_x + gx) / 2, y_dim + s(15), f'{it("d")}{sb("b", s, "label2")} = {D_B:.2f} m', "label2", O["geometry"], "middle"))
        o.append(H.arrow(s, p, gx, btop + bh / 2, gx, btop + bh + s(24), "load"))
        o.append(lab(s, gx + s(6), btop + bh + s(18), f'{it("W")}{sb("b", s, "label2")} = {W_B:.0f} N', "label2", O["load"]))
        o.append(H.joint_centre(s, *l5))
        o.append(H.com_mark(s, *ub))
        o.append(H.arrow(s, p, ub[0], ub[1] + s(8), ub[0], ub[1] + 0.13 * HF, "load"))
        o.append(lab(s, ub[0] - s(7), ub[1] + 0.09 * HF, f'{it("W")}{sb("tr", s, "label2")}', "label2", O["load"], "end"))
        o.append(arc_arrow(s, p, l5[0], l5[1], s(17), 25, 155, "force"))                   # bag moment (clockwise on screen)
        if lean:
            o.append(arc_arrow(s, p, l5[0], l5[1], s(27), 155, 25, "force"))              # lean moment (counter-clockwise)
            o.append(ext(s, ub[0], ub[1], ub[0], l5[1] - 0.24 * HF))
        o.append(lab(s, xm, 20, "lean away" if lean else "upright", "label", I["primary"], "middle"))
        rows = ([f'{it("W")}{sb("b", s, "label2")} {it("d")}{sb("b", s, "label2")} = {W_B:.0f} N × {D_B:.2f} m',
                 f'= {moment:.1f} N m side-bending',
                 f'({it("W")}{sb("tr", s, "label2")} acts on the axis)'] if not lean else
                [f'{it("x")}{sb("lean", s, "label2")} = {it("ℓ")}{sb("t", s, "label2")} sin {psi:.1f}° = {X_LEAN:.3f} m',
                 f'{it("W")}{sb("tr", s, "label2")} {it("x")}{sb("lean", s, "label2")} = {W_TR:.0f} N × {X_LEAN:.3f} m',
                 f'= {W_TR * X_LEAN:.1f} N m: cancels the bag'])
        o.append(lines(s, xm, fy + s(52), rows, "label2", "middle"))
    o.append(lab(s, 200, 40, f"one-hand carry: {W_B / G:.0f} kg bag, {it('W')}{sb('tr', s, 'label2')} = {W_TR:.0f} N upper body", "label2",
                 I["secondary"], "middle"))
    o.append(floor(s, 6, 394, fy))
    o.append(credit(s, VB))
    aria = ("Two skeletons (Lynch art), front view, each carrying a 10 kg bag (weight 98 N, brown arrow) in the subject's left hand, "
            "0.30 m from the vertical axis through the spine (blue double arrow). The black and white mark is the centre of "
            "mass of the upper body, with its 412 N weight. Left, upright: the bag makes a 29.4 N m side-bending moment (red "
            f"arc) that the trunk muscles must balance. Right, leaning {psi:.1f} degrees away: the upper-body weight moves "
            f"{X_LEAN:.3f} m to the other side of the axis and its moment (second red arc) is 412 N times {X_LEAN:.3f} m, "
            "29.4 N m, equal and opposite.")
    assert abs(moment - 29.4) < 0.1 and abs(X_LEAN - 0.071) < 0.001 and abs(W_TR * X_LEAN - moment) < 1e-9
    return finish(VB, aria, s, o)


# ================================================================ svg #25  C6 falls happen at corners (turn + trip)
V_WALK, BETA, W0 = 1.3, 60.0, math.sqrt(G / 1.0)           # lines 146, 674: v 1.3 m/s, beta 60 deg, omega_0 = sqrt(g / 1 m)


def trip_pose():
    """Whole body pitched forward about the stance ankle, swing foot (far) caught by an obstacle (design values)."""
    base = dict(pelvis=14.0, trunk=10.0, neck=6.0)
    arms = dict(shoulder=70.0, elbow=20.0)
    near = dict(hip=14.0, knee=0.0, **arms)
    P0 = LB.pose(near=dict(near), far=dict(arms), **base)
    thf = 30.0
    T_toe = (P0.j["toe"][0] + 0.14 * M_U, P0.floor_y)
    off = LB.rot(LB.OFF["lat_foot"]["toe"], thf)
    D = (T_toe[0] - off[0] - P0.j["hip"][0], T_toe[1] - off[1] - P0.j["hip"][1])
    hf, kf, ths = leg_ik(D, base["pelvis"])
    far = dict(hip=hf, knee=kf, contact=None, ankle=ths - thf, **arms)
    P = LB.pose(near=dict(near), far=far, **base)
    assert abs(P.j["toe_far"][1] - P.floor_y) < 1e-6
    return P


def fig25():
    p = "m13f25_"
    HF, fy = 205.0, 256.0
    VB, s = VBs(fy + 112 + CREDIT_H)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    J_imp = MASS * 2 * V_WALK * math.sin(math.radians(BETA / 2))        # 91 N s
    dv = 2 * V_WALK * math.sin(math.radians(BETA / 2))
    off_x = V_WALK / W0                                               # xdot / omega_0, metres
    # ---------------- left: plan view of the turn (the arrow tip of v is the XcoM: scale 1 m = Lv / off_x px)
    Lv = 70.0
    kp = Lv / off_x
    ox, oy = 52.0, fy - 8
    t1 = (ox + Lv, oy)
    t2 = (ox + Lv * math.cos(math.radians(BETA)), oy - Lv * math.sin(math.radians(BETA)))
    o.append(lab(s, 100, 20, "turn (plan view, from above)", "label", I["primary"], "middle"))
    fl, fw = 0.26 * kp, 0.10 * kp                                     # stance foot 0.26 m x 0.10 m (design values)
    o.append(f'<rect x="{ox - fl * 0.35:.2f}" y="{oy - fw / 2:.2f}" width="{fl:.2f}" height="{fw:.2f}" rx="{fw / 2:.2f}" fill="{BOX}" '
             f'stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
    o.append(H.arrow(s, p, ox, oy, t1[0], t1[1], "geometry"))
    o.append(H.arrow(s, p, ox, oy, t2[0], t2[1], "geometry"))
    o.append(H.line(s, t1[0], t1[1], t2[0], t2[1], O["dim"], "ref", H.DASH_REF))
    jl = 46.0
    jd = (t2[0] - t1[0], t2[1] - t1[1])
    n = math.hypot(*jd)
    jd = (jd[0] / n, jd[1] / n)
    o.append(H.arrow(s, p, ox, oy, ox + jd[0] * jl, oy + jd[1] * jl, "force"))
    r_a = 26.0
    o.append(f'<path d="M{ox + r_a:.2f},{oy:.2f} A{r_a:.2f},{r_a:.2f} 0 0 0 {ox + r_a * math.cos(math.radians(BETA)):.2f},'
             f'{oy - r_a * math.sin(math.radians(BETA)):.2f}" fill="none" stroke="{O["geometry"]}" stroke-width="{s(H.PX["geom"]):.2f}"/>')
    o.append(lab(s, ox + 10, oy - 10 + s(4), f'{it("β")}', "label2", O["geometry"]))
    for q in (t1, t2):
        o.append(f'<path d="M{q[0]:.2f},{q[1] - s(6):.2f} l{s(5):.2f},{s(6):.2f} l{-s(5):.2f},{s(6):.2f} l{-s(5):.2f},{-s(6):.2f} Z" '
                 f'fill="{O["flag"]}" stroke="#fff" stroke-width="{s(1.2):.2f}"/>')
    o.append(H.com_mark(s, ox, oy))
    o.append(lab(s, t1[0] + s(9), t1[1] + s(5), f'{it("v")}{sb("1", s, "label2")}', "label2", O["geometry"]))
    o.append(lab(s, t2[0] + s(9), t2[1] - s(3), f'{it("v")}{sb("2", s, "label2")}', "label2", O["geometry"]))
    o.append(lab(s, ox + jd[0] * jl - s(6), oy + jd[1] * jl - s(2), f'{it("J")}', "label", O["force"], "end"))
    o.append(lab(s, (t1[0] + t2[0]) / 2 + s(9), (t1[1] + t2[1]) / 2 + s(4), f'{it("Δv")}', "label2", O["dim"]))
    o.append(lines(s, 100, fy + s(30), [f'{it("J")} = 2 {it("m v")} sin({it("β")}/2) = {J_imp:.0f} N s',
                                        f'{it("β")} = {BETA:.0f}°, {it("m")} = {MASS:.0f} kg, {it("v")} = {V_WALK:.1f} m/s',
                                        'arrow tip = XcoM, ahead of',
                                        f'the COM by {it("v")} / {it("ω")}{sb("0", s, "label2")} = {off_x:.2f} m',
                                        f'inward swing {it("Δv")} / {it("ω")}{sb("0", s, "label2")} = {dv / W0:.2f} m'],
                       "label2", "middle"))
    # ---------------- right: the trip (side view)
    P = trip_pose()
    sv, J = put(P, 224, fy, HF)
    k = HF / 1.75
    com = J["com"]
    xi = com[0] + off_x * k
    ob_w, ob_h = 0.07 * HF, 0.045 * HF
    o.append(f'<rect x="{J["toe_far"][0] + s(2):.2f}" y="{fy - ob_h:.2f}" width="{ob_w:.2f}" height="{ob_h:.2f}" rx="{s(1.5):.2f}" fill="{BOX}" '
             f'stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
    o.append(sv)
    o.append(ext(s, com[0], com[1], com[0], fy))
    o.append(H.line(s, J["heel"][0], fy - s(3), J["toe"][0], fy - s(3), O["geometry"], "geom", extra='stroke-linecap="round"'))
    o.append(H.com_mark(s, *com))
    y_dim = fy + s(14)
    o.append(H.arrow(s, p, com[0], y_dim, xi, y_dim, "geometry", both=True))
    o.append(f'<path d="M{xi:.2f},{fy - s(7):.2f} l{s(5):.2f},{s(7):.2f} l{-s(5):.2f},{s(7):.2f} l{-s(5):.2f},{-s(7):.2f} Z" '
             f'fill="{O["flag"]}" stroke="#fff" stroke-width="{s(1.2):.2f}"/>')
    o.append(ext(s, xi, fy, xi, y_dim, O["flag"]))
    o.append(lab(s, (com[0] + xi) / 2, y_dim + s(15), f'{it("v")} / {it("ω")}{sb("0", s, "label2")} = {off_x:.2f} m', "label2", O["geometry"], "middle"))
    assert xi > J["toe"][0] + 0.02 * HF, (xi, J["toe"][0])
    o.append(lab(s, 300, 20, "trip (side view)", "label", I["primary"], "middle"))
    o.append(lab(s, xi + s(8), fy - s(10), "XcoM", "label2", I["primary"]))
    o.append(lab(s, J["heel"][0] - s(3), fy - s(8), "base", "label2", O["geometry"], "end"))
    o.append(lines(s, 300, fy + s(52), [f'{it("ξ")} = {it("x")}{sb("com", s, "label2")} + {it("v")} / {it("ω")}{sb("0", s, "label2")}',
                                        'XcoM past the toe:', 'a reactive step is mandatory'], "label2", "middle"))
    o.append(lab(s, 200, 40, f"{it('ω')}{sb('0', s, 'label2')} = √({it('g')}/{it('ℓ')}) = {W0:.2f} rad/s ({it('ℓ')} = 1.0 m)", "label2", I["secondary"], "middle"))
    o.append(credit(s, VB))
    aria = ("Left, a plan view of a turn: the walker's centre of mass (black and white mark) over the stance foot, velocity before "
            "the turn v1 and after v2 (blue arrows, both 1.3 m/s, 60 degrees apart), the velocity change (dashed) and the ground "
            f"impulse J = 2 m v sin(beta/2) = {J_imp:.0f} N s pointing inward (red). The tip of each velocity arrow is the "
            f"extrapolated centre of mass (orange diamond), {off_x:.2f} m ahead of the centre of mass along the velocity, so it swings "
            "inward through the turn. Right, a skeleton (Lynch art) tripping on an obstacle: the base of support under the stance "
            f"foot (blue bar) is short of the extrapolated centre of mass, {off_x:.2f} m ahead of the centre of mass, so a "
            "reactive step is mandatory.")
    assert abs(J_imp - 91) < 0.5
    return finish(VB, aria, s, o)


# ================================================================ svg #26  C7 the rubber jar-opener (top view of a hand on a lid)
R_LID, F_GRIP, TAU_RES = 0.035, 60.0, 2.0                   # lines 168, 174: r 0.035 m, weak grip 60 N, tau_resist 2 N m
PALM = (22.0, 40.0)                                         # palm centre in the hand segment's local frame (body units)


def hand_use(cx, cy, k_px_per_u, rot_deg=180.0):
    """The kit's hand (Lynch art, wrist at the origin, fingers along +y) with its palm centre at (cx, cy), fingers up."""
    return (f'<g fill="none"><use href="#hbody_arm_hand" transform="translate({cx:.2f} {cy:.2f}) rotate({rot_deg:.1f}) '
            f'scale({k_px_per_u:.4f}) translate({-PALM[0]:.2f} {-PALM[1]:.2f})"/></g>')


def fig26():
    p = "m13f26_"
    VB, s = VBs(444)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    R = 32.0
    kpx = R / R_LID / M_U                                    # px per body unit: the lid is drawn at true size next to the hand
    ky = 0.46                                                # px per newton, forces
    cy = 162.0
    for name, mu, cx in (("bare hand", 0.5, 100.0), ("rubber pad", 1.0, 300.0)):
        tau = mu * F_GRIP * R_LID
        opens = tau >= TAU_RES
        o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R:.2f}" fill="{BOX}" stroke="{T["fluid"][1] if False else I["secondary"]}" '
                 f'stroke-width="{s(3.0):.2f}"/>')
        if mu > 0.9:                                         # the pad: a ring around the rim
            o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{R + s(2):.2f}" fill="none" stroke="{I["muted"]}" '
                     f'stroke-width="{s(4):.2f}" stroke-dasharray="{s(2):.2f} {s(2):.2f}"/>')
        o.append(hand_use(cx, cy, kpx))
        for sg in (1, -1):                                   # two opposite contacts: grip inward, friction tangential
            x_c = cx + sg * (R + s(1))
            o.append(H.arrow(s, p, x_c + sg * (F_GRIP * ky + s(6)), cy, x_c + sg * s(2), cy, "force"))
            fy_ = mu * F_GRIP * ky
            o.append(H.arrow(s, p, x_c + sg * s(9), cy + sg * s(2), x_c + sg * s(9), cy - sg * (fy_ + s(2)), "reaction"))
        o.append(H.line(s, cx, cy, cx + R * math.cos(math.radians(-50)), cy + R * math.sin(math.radians(-50)), O["geometry"], "geom"))
        o.append(lab(s, cx + R * 0.62, cy - R * 1.0 - s(2), f'{it("r")}', "label2", O["geometry"]))
        o.append(lab(s, cx, 20, f"{name}: {it('μ')} = {mu:.1f}", "label", I["primary"], "middle"))
        # torque bar against the 2 N m the lid resists
        bx0, bw = cx - 78, 156.0
        sc = bw / 2.6
        by = 276.0
        o.append(f'<rect x="{bx0:.2f}" y="{by:.2f}" width="{tau * sc:.2f}" height="{s(12):.2f}" fill="{O["force"]}"/>')
        o.append(f'<rect x="{bx0:.2f}" y="{by:.2f}" width="{bw:.2f}" height="{s(12):.2f}" fill="none" stroke="{I["rule"]}" '
                 f'stroke-width="{s(1):.2f}"/>')
        o.append(H.line(s, bx0 + TAU_RES * sc, by - s(5), bx0 + TAU_RES * sc, by + s(17), O["flag"], "geom"))
        o.append(lab(s, bx0 + TAU_RES * sc, by - s(8), f"{TAU_RES:.0f} N m to open", "label2", I["primary"], "middle"))
        o.append(lab(s, bx0, by + s(30), f'{it("τ")} = {it("μ F")}{sb("grip", s, "label2")} {it("r")} = {tau:.2f} N m', "label2", I["primary"]))
        o.append(lab(s, cx, by + s(50), "opens" if opens else "stays shut", "label", I["primary"], "middle"))
    o.append(lab(s, 200, 40, f"same grip {it('F')}{sb('grip', s, 'label2')} = {F_GRIP:.0f} N, lid radius {it('r')} = {R_LID:.3f} m, lid resists {TAU_RES:.0f} N m",
                 "label2", I["secondary"], "middle"))
    ly = 352.0
    o.append(H.line(s, 14, ly - s(4), 40, ly - s(4), O["force"], "force"))
    o.append(lab(s, 46, ly, f"grip force {it('F')}{sb('grip', s, 'label2')} presses in at the rim", "label2"))
    o.append(H.line(s, 14, ly + s(15), 40, ly + s(15), I["primary"], "force"))
    o.append(lab(s, 46, ly + s(19), f"friction {it('μ F')}{sb('grip', s, 'label2')} along the rim: {0.5 * F_GRIP:.0f} N bare, {1.0 * F_GRIP:.0f} N rubber", "label2"))
    o.append(credit(s, VB))
    aria = ("Two views from above of a hand gripping a jar lid of radius 0.035 m (Lynch hand bones over the lid circle). In both, "
            "the grip force is 60 N (red arrows pressing inward at the rim) and friction acts along the rim (black arrows). "
            f"Left, a bare hand, friction coefficient 0.5: torque {0.5 * F_GRIP * R_LID:.2f} N m, below the 2 N m the lid resists, so it "
            f"stays shut. Right, with a rubber pad, coefficient 1.0: {1.0 * F_GRIP * R_LID:.2f} N m, above 2 N m, so it opens. "
            "A bar under each shows the torque against an orange mark at 2 N m.")
    assert abs(0.5 * F_GRIP * R_LID - 1.05) < 1e-9 and 1.0 * F_GRIP * R_LID >= TAU_RES
    return finish(VB, aria, s, o)


# ================================================================ svg #27  C8 handles far from hinges (plan view of a door)
TAU_DOOR, D_FAR, D_NEAR, DOOR_W = 20.0, 0.8, 0.20, 0.90    # line 176: 20 N m, 0.8 m; near-hinge 0.20 m and door width 0.90 m: design


def fig27():
    p = "m13f27_"
    VB, s = VBs(448)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    kd = 340.0 / DOOR_W                                      # px per metre
    kpx = kd / M_U                                           # px per body unit (the hand is drawn at the door's scale)
    hx = 28.0
    cf = 0.8                                                 # px per newton
    for row, (title, dd) in enumerate((("push at the handle, far edge", D_FAR), ("push near the hinge", D_NEAR))):
        y0 = 36.0 + row * 168.0
        yd = y0 + 36
        F = TAU_DOOR / dd
        xp = hx + dd * kd
        o.append(lab(s, 200, y0 - 8, title, "label", I["primary"], "middle"))
        o.append(f'<rect x="{hx:.2f}" y="{yd:.2f}" width="{DOOR_W * kd:.2f}" height="{s(12):.2f}" rx="{s(2):.2f}" fill="{BOX}" '
                 f'stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
        o.append(hand_use_door(xp, yd + s(12), kpx))
        o.append(H.arrow(s, p, xp, yd + s(12) + F * cf + s(4), xp, yd + s(13), "force"))
        o.append(H.joint_centre(s, hx, yd + s(6)))
        o.append(lab(s, hx + s(8), yd + s(34), "hinge", "label2", I["primary"]))
        y_dim = yd - s(16)
        o.append(ext(s, hx, y_dim - s(4), hx, yd))
        o.append(ext(s, xp, y_dim - s(4), xp, yd))
        o.append(H.arrow(s, p, hx, y_dim, xp, y_dim, "geometry", both=True))
        dl = f'{it("d")}{sb("hinge", s, "label2")} = {dd:g} m' if row == 0 else f'{it("d")}{sb("hinge", s, "label2")} = {dd:.2f} m'
        if row == 0:
            o.append(lab(s, (hx + xp) / 2, y_dim - s(6), dl, "label2", O["geometry"], "middle"))
        else:
            o.append(lab(s, xp + s(9), y_dim + s(4), dl, "label2", O["geometry"]))
        tx = xp + s(26) if row == 0 else xp + s(46)
        tx = min(tx, 330.0) if row == 0 else tx
        o.append(lines(s, tx if row else hx + 100, yd + s(46) if row else yd + s(42),
                       [f'{it("F")}{sb("hand", s, "label2")} = {it("τ")}{sb("door", s, "label2")} / {it("d")}{sb("hinge", s, "label2")}',
                        f'= {TAU_DOOR:.0f} N m / {dd:g} m = {F:.0f} N'], "label2", "start", fill=O["force"]))
    o.append(lines(s, 200, 372, [f"same door torque {it('τ')}{sb('door', s, 'label2')} = {TAU_DOOR:.0f} N m in both rows:",
                                 f"the hand force goes as 1 / {it('d')}{sb('hinge', s, 'label2')}, {TAU_DOOR / D_NEAR / (TAU_DOOR / D_FAR):.0f} times as much at the hinge side"],
                   "label2", "middle", fill=I["secondary"]))
    o.append(credit(s, VB))
    aria = ("Plan view, from above, of a door hinged at its left end (crosshair), pushed by a hand (Lynch hand bones, fingertips on "
            "the door) with the same 20 N m resisting torque in both. Top: the hand is at the handle, 0.8 m from the hinge "
            f"(blue double arrow), and needs {TAU_DOOR / D_FAR:.0f} N (red arrow). Bottom: the hand is near the hinge, {D_NEAR:.2f} m "
            f"away, and needs {TAU_DOOR / D_NEAR:.0f} N, four times as much.")
    assert abs(TAU_DOOR / D_FAR - 25) < 1e-9
    return finish(VB, aria, s, o)


def hand_use_door(x, y, k):
    """The kit's hand, fingertips up at (x, y) on the door's lower face, wrist below (plan view, from above)."""
    return (f'<g fill="none"><use href="#hbody_arm_hand" transform="translate({x:.2f} {y + LB.L_HAND * k:.2f}) rotate(180) '
            f'scale({k:.4f})"/></g>')


# ================================================================ svg #29  C10 one weakness, many failures (shared reserve)
def fig29():
    p = "m13f29_"
    HF, fy = 128.0, 248.0
    VB, s = VBs(fy + 126 + CREDIT_H)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    bx0, bx1, by0, by1 = 56.0, 344.0, 30.0, 78.0
    o.append(f'<rect x="{bx0:.2f}" y="{by0:.2f}" width="{bx1 - bx0:.2f}" height="{by1 - by0:.2f}" rx="{s(8):.2f}" fill="{BOX}" '
             f'stroke="{O["force"]}" stroke-width="{s(2):.2f}"/>')
    o.append(lab(s, 200, by0 + s(20), "weak knee extensors (quadriceps)", "label", I["primary"], "middle"))
    o.append(lab(s, 200, by0 + s(39), f"the shared reserve: old peak torque 1 to 1.5 N m/kg, young 2 to 3", "label2", I["secondary"], "middle"))
    tau_chair = M_UP * G * 0.20 / MASS                         # 1.57 N m/kg (line 90)
    cols = [(70.0, "chair rise", "seat-off"), (200.0, "stair ascent", "legs shorten"), (330.0, "downhill walking", "eccentric")]
    # --- chair rise
    cx, ttl, _ = cols[0]
    P, _tr = sts_for_d(105.0, 0.20)
    sv, J = put_c(P, cx, fy, HF)
    o.append(seat(s, J, "stool", HF))
    o.append(sv)
    o.append(H.com_mark(s, *upper_com(P, J)[0]))
    knees = [J["knee"]]
    # --- stair ascent
    cx, ttl, _ = cols[1]
    P = stair_pose(True)
    sv, J = put_c(P, cx, fy, HF)
    h_px = H_RISE * HF / 1.75
    xr = (J["toe_far"][0] + J["heel"][0]) / 2
    o.append(tread_poly(s, [(cx - 62, fy), (xr, fy), (xr, fy - h_px), (cx + 62, fy - h_px)], fy + 8))
    o.append(sv)
    knees.append(J["knee"])
    # --- downhill walking
    cx, ttl, _ = cols[2]
    P = slope_pose(False)
    sv, J = put_c(P, cx, fy, HF)
    hl, tp = J["heel"], J["toe"]
    sl = (tp[1] - hl[1]) / (tp[0] - hl[0])
    ys = lambda x: hl[1] + sl * (x - hl[0])                  # noqa: E731
    x0, x1 = cx - 62, cx + 62
    o.append(tread_poly(s, [(x0, ys(x0)), (x1, ys(x1))], max(ys(x0), ys(x1)) + 8))
    o.append(sv)
    knees.append(J["knee"])
    for (cx, ttl, sub_), kn in zip(cols, knees):
        o.append(H.arrow(s, p, cx, by1 + s(2), cx, by1 + s(24), "force"))
        o.append(lab(s, cx, by1 + s(40), ttl, "label", I["primary"], "middle"))
        o.append(f'<circle cx="{kn[0]:.2f}" cy="{kn[1]:.2f}" r="{s(7):.2f}" fill="none" stroke="#fff" stroke-width="{s(4.5):.2f}"/>'
                 f'<circle cx="{kn[0]:.2f}" cy="{kn[1]:.2f}" r="{s(7):.2f}" fill="none" stroke="{O["force"]}" stroke-width="{s(2.2):.2f}"/>')
    y_r = fy + s(26)
    o.append(lines(s, 70, y_r, [f'needs {tau_chair:.2f} N m/kg', f'{tau_chair / 2.5 * 100:.0f}% of a young', 'adult’s 2.5',
                                'old (≤ 1.5): fails'], "label2", "middle"))
    o.append(lines(s, 200, y_r, [f'needs {P_STAIR:.0f} W', f'{P_STAIR / 250 * 100:.0f}% of the 250 W', 'ceiling',
                                 'less: slows or stops'], "label2", "middle"))
    along = MASS * G * math.sin(math.radians(THETA)) * V_SLOPE
    o.append(lines(s, 330, y_r, [f'absorbs {along:.0f} W', f'({THETA:.0f}°, {V_SLOPE:.1f} m/s)', 'eccentric brake;', 'weak: a fall'], "label2", "middle"))
    o.append(lab(s, 200, fy + s(26) + 4 * s(17) + s(12), "red ring = the knee, where the quadriceps work in each task", "label2", I["secondary"], "middle"))
    o.append(credit(s, VB))
    aria = ("A box at the top, weak knee extensors (the quadriceps), is joined by three red arrows to three small skeletons (Lynch "
            "art), each with a red ring at the knee. Chair rise at seat-off needs "
            f"{tau_chair:.2f} N m per kilogram, {tau_chair / 2.5 * 100:.0f} percent of a young adult's 2.5, and an older adult's peak of "
            f"at most 1.5 fails it. Stair ascent needs {P_STAIR:.0f} W, {P_STAIR / 250 * 100:.0f} percent of the 250 W ceiling. "
            f"Downhill walking at 15 degrees and 1 m/s absorbs {along:.0f} W eccentrically. One weak reserve cuts into all three.")
    assert abs(tau_chair - 1.57) < 0.005 and round(P_STAIR / 250 * 100) == 84 and round(tau_chair / 2.5 * 100) == 63
    return finish(VB, aria, s, o)


def put_c(P, cx, y_floor, hpx):
    """Draw pose P with the middle of its bbox at x = cx and the anchor level at y_floor."""
    _, J0 = LB.draw("m13", H.Scale(400, 400), P, 0.0, y_floor, hpx)
    return LB.draw("m13", H.Scale(400, 400), P, cx - (J0["bbox"][0] + J0["bbox"][2]) / 2, y_floor, hpx)


FIGS = {
    20: ("C1: the low soft chair. Why is a low, soft armchair so much ", fig20),
    24: ("C5: the lean away. Why do you instinctively lean away from a", fig24),
    25: ("C6: falls happen at corners. Why do turns and trips, rather ", fig25),
    26: ("C7: the rubber jar-opener. Why does a thin rubber pad let yo", fig26),
    27: ("C8: handles far from hinges. Why is a door handle placed at ", fig27),
    21: ("C2: down is worse than up. Stair falls happen far more on de", fig21),
    22: ("C3: keep it close. Safe-lifting advice says hold the load cl", fig22),
    28: ("C9: lungs up, knees down. Why does walking uphill tax the lu", fig28),
    29: ("C10: one weakness, many failures. Why does a single deficit ", fig29),
    30: ("D1: chair-rise torque. Derive the quasi-static knee extensor", fig30),
}

if __name__ == "__main__":
    for k, (_, f) in FIGS.items():
        print(k, len(f()))
