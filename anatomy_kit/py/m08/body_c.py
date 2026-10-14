"""Module 8, group `body_c`: conceptual problems C1-C10 (svg #17-#26), house style, 400 px.

Whole bodies come from the posable Lynch skeleton (lynch_body.py); body_main.py puts its defs on the page.
The page states no stature: 1.75 m, so 1 cm = LB.H_U / 175 body units.  Every number on a figure is computed here
from the constants module08.html states (line numbers beside each constant); Lab 2 and Lab 3 are ported line for
line.  Model overlays (pendulum legs, COM marks) use the text's point-mass walker: the COM sits l = 0.95 m from the
contact point (line 223), so at double support it is l cos(alpha) above the floor, midway between the contacts.
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

# ---------------------------------------------------------------- numbers module08.html states
M, G, ELL, V = 70.0, 9.81, 0.95, 1.3    # kg, m/s^2, m, m/s: reference gait (lines 491, 694)
KAPPA = 0.09                            # m^2, swing-cost coefficient (lines 503, 695)
STANCE = 0.62                           # stance fraction of a stride (lines 191, 720)
ALPHA9, GAMMA9 = 0.30, 0.05             # rad: section 9 passive walker (line 585)
X_P, V_P, DELAY, REACH = 0.03, 0.45, 0.20, 0.415   # Lab 4 reference perturbation (line 644)


def close(v, ref, tol):
    assert abs(v - ref) <= tol * 1.0001, (v, ref)


def loss(two_a, v=V):
    """Prop 5.1: heel-strike redirection loss."""
    return 0.5 * M * v * v * math.sin(two_a) ** 2


def cost_terms(L):
    """Section 7 proxy C(v, L) at the reference speed: (transition, swing)."""
    return loss(2 * math.asin(L / (2 * ELL))), KAPPA * (V / L) ** 2 * M


# Lab 2 (lines 694-704), line for line
_L = np.linspace(0.35, 0.95, 200)
_al = np.arcsin(_L / (2 * ELL))
_cost = 0.5 * M * V * V * np.sin(2 * _al) ** 2 + KAPPA * (V / _L) ** 2 * M
L_STAR = float(_L[int(np.argmin(_cost))])
ALPHA = math.asin(L_STAR / (2 * ELL))
T_STRIDE = 2 * L_STAR / V
E_LOSS, E_SWING = cost_terms(L_STAR)
E_SPLIT = 0.5 * M * V * V * math.tan(ALPHA) ** 2          # Prop 5.2, n = 2 (line 395)
DH = ELL * (1 - math.cos(ALPHA))                           # Prop 2.1
E_VAULT = M * G * DH
close(L_STAR, 0.6847, 0.00005)                  # line 708
close(math.degrees(ALPHA), 21.1, 0.05)          # line 507
close(2 * math.degrees(ALPHA), 42.2, 0.05)      # line 402
close(E_LOSS, 26.7, 0.05)                       # lines 402, 507
close(E_SWING, 22.7, 0.05)                      # line 507
close(E_SPLIT, 8.8, 0.05)                       # line 402
close(E_SPLIT / E_LOSS, 0.330, 0.0005)          # line 395
close(1 / (4 * math.cos(ALPHA) ** 4), E_SPLIT / E_LOSS, 1e-9)
close(DH, 0.0638, 0.00005)                      # line 684
close(E_VAULT, 43.8, 0.05)                      # lines 684, 783
close(T_STRIDE, 1.053, 0.0005)                  # line 507
close(V / L_STAR, 1.90, 0.005)                  # line 507
FR = V * V / (G * ELL)
close(FR, 0.181, 0.0005)                        # line 684
close(math.sqrt(0.5 * G * ELL), 2.16, 0.005)    # line 247
L_LONG = 1.2 * L_STAR                           # "a 20 % longer step" (line 511)
E_LOSS_L, E_SWING_L = cost_terms(L_LONG)
close((E_LOSS_L + E_SWING_L) / (E_LOSS + E_SWING) - 1, 0.046, 0.0005)   # line 511
close(sum(cost_terms(0.8 * L_STAR)) / (E_LOSS + E_SWING) - 1, 0.082, 0.0005)
ALPHA_L = math.asin(L_LONG / (2 * ELL))

# section 8 arm swing (lines 540-544)
M_LEG, D_LEG, M_ARM, D_ARM, V_ARM = 0.161 * M, 0.09, 0.050 * M, 0.20, 0.6
H_LEGS = 2 * M_LEG * D_LEG * V
H_ARMS = 2 * M_ARM * D_ARM * V_ARM
TQ_STILL = 2 * H_LEGS / (T_STRIDE / 2)
TQ_SWING = 2 * (H_LEGS - H_ARMS) / (T_STRIDE / 2)
close(M_LEG, 11.3, 0.05)
close(H_LEGS, 2.64, 0.005)
close(H_ARMS, 0.84, 0.005)
close(H_ARMS / H_LEGS, 0.32, 0.005)
close(H_LEGS - H_ARMS, 1.80, 0.005)
close(T_STRIDE / 2, 0.527, 0.0005)
close(TQ_STILL, 10.0, 0.05)
close(TQ_SWING, 6.8, 0.05)

# section 9 passive walker (line 585) and C9 (line 807)
L9 = 2 * ELL * math.sin(ALPHA9)
E_GRAV = M * G * L9 * math.sin(GAMMA9)
V9 = math.sqrt(2 * G * L9 * math.sin(GAMMA9)) / math.sin(2 * ALPHA9)     # exact balance (K9)
close(E_GRAV, 19.3, 0.05)                       # line 807
close(math.sqrt(G * ELL * math.sin(GAMMA9) / ALPHA9), 1.25, 0.005)      # line 585
close(V9, 1.31, 0.005)                          # line 585
close(loss(2 * ALPHA9, V9), E_GRAV, 1e-9)
close(math.degrees(GAMMA9), 2.865, 0.0005)    # text says 2.87 (line 585); 0.05 rad = 2.865 deg
close(math.degrees(2 * ALPHA9), 34.4, 0.05)

# section 10 / Lab 4 (line 644)
W0 = math.sqrt(G / ELL)
XI = X_P + V_P * DELAY + V_P / W0
close(W0, 3.21, 0.005)
close(XI, 0.260, 0.0005)
close(REACH - XI, 0.155, 0.0005)
close(V_P * DELAY, 0.090, 0.0005)


def lab3():
    """Lab 3 (lines 718-733), line for line."""
    W, Tt = M * G, 2 * 0.6847 / 1.3
    T_st = STANCE * Tt
    s = np.linspace(0, 1, 601)
    t = s * T_st
    shape = np.sin(np.pi * s) ** 0.40 * (1 - 0.245 * np.cos(4 * np.pi * (s - 0.5)))
    Fy = shape * (W * Tt / 2) / np.trapezoid(shape, t)
    x_cop = -0.04 + 0.225 * s
    tau = Fy * x_cop
    omega = 2.3 * np.exp(-((s - 0.80) / 0.10) ** 2)
    P = tau * omega
    close(np.trapezoid(Fy, t), 361.7, 0.05)                 # line 737
    close((Fy / W).max(), 1.10, 0.005)
    close(Fy[300] / W, 0.75, 0.005)
    close(tau.max(), 95.8, 0.05)
    close(s[int(np.argmax(tau))], 0.76, 0.005)
    close(P.max(), 215, 0.5)
    close(P.max() / M, 3.07, 0.005)
    close(s[int(np.argmax(P))], 0.79, 0.005)
    close(np.trapezoid(np.maximum(P, 0), t), 22.6, 0.05)
    close(0.04 / 0.225, 0.18, 0.005)                       # crosses the ankle at 18 % of stance
    return s, Fy / W, x_cop


S3, FYW, XCOP = lab3()


# ---------------------------------------------------------------- drawing helpers (idiom of m07/body_c.py)
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


def credit(s, vb):
    """Lynch credit at the bottom of the viewBox, wrapped to its width (the wrap rule of LB.credit)."""
    w = vb[2] - s(12)
    t = H.ATTRIBUTION["by"].format(
        author="Patrick J. Lynch, medical illustrator",
        title="Skeleton lateral.svg” and “Skeleton whole body ant lat views.svg", licence="CC BY 2.5",
        changes="Recoloured, split into segments and reposed; arms from the anterior view.")
    n = max(20, int(w / (s(H.PX["credit"]) * 0.47)))
    lines, cur = 0, ""
    for wd in t.split():
        if cur and len(cur) + 1 + len(wd) > n:
            lines, cur = lines + 1, wd
        else:
            cur = (cur + " " + wd).strip()
    y = vb[1] + vb[3] - s(6) - lines * s(H.PX["credit"]) * 1.25
    return LB.credit(s, vb[0] + s(6), y, width=w)


def ext(s, x0, y0, x1, y1):
    """Dashed construction line (reference grey)."""
    return H.line(s, x0, y0, x1, y1, O["dim"], "ref", H.DASH_REF)


def dim_h(s, p, x0, x1, y, text, below=False, size="label2"):
    o = [H.arrow(s, p, x0, y, x1, y, "geometry", both=True)]
    ty = y + s(H.PX[size]) + s(3) if below else y - s(5)
    o.append(lab(s, (x0 + x1) / 2, ty, text, size, anchor="middle"))
    return "".join(o)


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


def rect(s, x, y, w, h, fill=BOX, stroke=I["secondary"]):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{s(1.2):.2f}"/>')


def poly(s, pts, col, w="geom", dash=None):
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    return (f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="none" stroke="{col}" '
            f'stroke-width="{s(H.PX[w]):.2f}" stroke-linejoin="round"{da}/>')


def dot(s, x, y, col, r=4.5):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{col}" stroke="#fff" '
            f'stroke-width="{s(1.5):.2f}"/>')


def cmu(J):
    """Figure units per cm for a drawn body."""
    return CM * J["scale"]


def lines(s, x, y, rows, size="label2", anchor="start", lead=1.35):
    return "".join(lab(s, x, y + i * s(H.PX[size]) * lead, t, size, anchor=anchor) for i, t in enumerate(rows))


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


def VBs(h):
    vb = (0, 0, 400, h)
    return vb, H.Scale(400, h, display_w=400, max_h=H.MAX_DISPLAY_H_BODY)


def deg(r):
    return f"{math.degrees(r):.1f}°"


def ds_pose(L, kf=20.0, near_arm=(-20, 10), far_arm=(20, 20), lead=None):
    """Double support: leading (near) heel down, trailing (far) toe down, contacts L metres apart.
    Leading thigh at alpha = asin(L / 2l) forward of vertical (the model's half-angle); the trailing thigh angle is
    solved so that trailing toe to leading heel = L."""
    a = math.degrees(math.asin(L / (2 * ELL))) if lead is None else lead

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
    return mk(b), a, b


def model_com(J, L, alpha):
    """Point-mass COM of the model at double support: midway between the contacts, l cos(alpha) up."""
    m = 100 * cmu(J)
    x0, x1 = J["toe_far"][0], J["heel"][0]
    return ((x0 + x1) / 2, J["floor_y"] - ELL * math.cos(alpha) * m), m


def vec(s, p, x, y, ang, length, meaning):
    """Arrow from (x, y) at screen angle ang (deg, + = clockwise from +x)."""
    return H.arrow(s, p, x, y, x + length * math.cos(math.radians(ang)), y + length * math.sin(math.radians(ang)),
                   meaning)


# ================================================================ svg #17  C1 controlled falling and catching
def fig17():
    p = "m8f17_"
    VB, s = VBs(452)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 300.0, 352.0
    P, a, b = ds_pose(L_STAR)
    _, J0 = LB.draw(p, s, P, 0, 0, HF)
    m = 100 * cmu(J0)
    x_new = 138 + L_STAR * m * 1.5                           # leading heel
    body, J = LB.draw(p, s, P, x_new, fy, HF)
    (cx, cy), m = model_com(J, L_STAR, ALPHA)
    x_old = J["toe_far"][0]
    o.append(floor(s, 8, 392, fy))
    o.append(body)
    # COM path: old vault about the old contact, from its start (-alpha) through midstance (0) to the cusp (+alpha)
    th = np.linspace(-ALPHA, ALPHA, 60)
    pt = lambda x0, t: (x0 + ELL * math.sin(t) * m, fy - ELL * math.cos(t) * m)  # noqa: E731
    rise = [pt(x_old, t) for t in th[:30]] + [pt(x_old, 0.0)]
    fall = [pt(x_old, 0.0)] + [pt(x_old, t) for t in th[30:]]
    nxt = [pt(x_new, t) for t in np.linspace(-ALPHA, 0, 30)]
    o.append(poly(s, rise, O["geometry"], "curve"))
    o.append(poly(s, fall, SER[2], "curve"))
    o.append(poly(s, nxt, O["geometry"], "geom", H.DASH_REF))
    # model legs: old (trailing) and new (leading) contact to the COM
    o.append(ext(s, x_old, fy, cx, cy))
    o.append(ext(s, x_new, fy, cx, cy))
    mid = pt(x_old, 0.0)
    o.append(ext(s, x_old, fy, mid[0], mid[1]))
    # heel-strike impulse along the new leg (the catch)
    ux, uy = (cx - x_new) / (ELL * m), (cy - fy) / (ELL * m)
    o.append(H.arrow(s, p, x_new + ux * s(14), fy + uy * s(14), x_new + ux * s(70), fy + uy * s(70), "reaction"))
    # velocity just before (perpendicular to the old leg) and just after (perpendicular to the new leg)
    vl = s(58)
    o.append(vec(s, p, cx, cy, math.degrees(ALPHA), vl, "dim"))
    vp = vl * math.cos(2 * ALPHA)                           # Prop 4.1: speed scaled by cos 2alpha
    o.append(vec(s, p, cx, cy, -math.degrees(ALPHA), vp, "dim"))
    o.append(arc(s, p, cx, cy, vl * 0.62, -math.degrees(ALPHA), math.degrees(ALPHA), "geometry", head=False))
    o.append(lab(s, cx + vl + s(4), cy + vl * math.sin(ALPHA) + s(8), f'{it("v")}⁻', "label2"))
    o.append(lab(s, cx + vp * math.cos(ALPHA) + s(4), cy - vp * math.sin(ALPHA) - s(2), f'{it("v")}⁺', "label2"))
    o.append(lab(s, cx + vl * 0.62 + s(4), cy + s(4), f'2{it("α")} = {2 * math.degrees(ALPHA):.1f}°', "label2"))
    o.append(H.com_mark(s, cx, cy))
    o.append(H.com_mark(s, *mid))
    o.append(dot(s, x_old, fy, I["primary"]))
    o.append(dot(s, x_new, fy, I["primary"]))
    yd = fy + s(18)
    o.append(dim_h(s, p, x_old, x_new, yd, f'{it("L")} = {L_STAR:.2f} m', below=True))
    o.append(lab(s, x_old - s(4), fy - s(6), "old contact", "label2", anchor="end"))
    o.append(lab(s, x_new + s(5), fy - s(6), "new contact", "label2"))
    o.append(lab(s, mid[0], mid[1] - s(14), "midstance", "label2", anchor="middle"))
    # labels on the two halves
    r0 = rise[6]
    o.append(lab(s, r0[0] + s(2), r0[1] + s(20), "rise", "label2", anchor="middle"))
    f0 = fall[len(fall) // 2]
    o.append(lab(s, f0[0] - s(2), f0[1] + s(20), "fall", "label2", anchor="middle"))
    o.append(lines(s, 10, 22, ["fall (orange, midstance to contact):", "nearly conservative, PE → KE,",
                               "costs almost nothing", "",
                               "catch (heel strike + loading): an", "impulse along the new leg turns",
                               f'{it("v")} by 2{it("α")}; {E_LOSS:.1f} J lost per step', "(Prop 5.1)"]))
    o.append(credit(s, VB))
    aria = ("Side view of a walking skeleton (Lynch art) at the instant the leading heel strikes, with the "
            "point-mass model drawn over it. The centre of mass vaults over the old contact on an arc of radius "
            "l = 0.95 m: it rises to midstance (blue) and then falls toward the new contact (orange), a nearly "
            "conservative exchange that costs almost nothing. The catch is the heel strike and loading response: an "
            "impulse along the new leg turns the velocity from v-minus to v-plus through 2 alpha = 42.2 degrees and "
            "shortens it by cos 2 alpha, so 26.7 J are lost per step. The contacts are L = 0.68 m apart; the next vault (dashed) starts at the cusp.")
    return finish(VB, aria, s, o)


# ================================================================ svg #18  C2 double support vs flight
def run_pose():
    """Running, mid-flight: lead leg reaching forward, trailing leg folded, elbows at 90 deg (design pose)."""
    return LB.pose(pelvis=0, trunk=8, near=dict(hip=40, knee=25, contact=None, ankle=5, shoulder=-35, elbow=90),
                   far=dict(hip=-15, knee=85, contact=None, ankle=-15, shoulder=35, elbow=90), anchor=("hip", "near"))


RUN_DUTY = 0.35        # stance fraction of a running stride (design value; flight needs < 0.5)


def timeline(s, x0, w, y, duty, name):
    """Footfall bars over one stride: two feet, each in stance for `duty` of the stride, half a stride apart."""
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
        spans = [(0.0, duty - 0.5), (0.5, duty)]
        col = SER[1]
    else:
        spans = [(duty, 0.5), (0.5 + duty, 1.0)]
        col = SER[2]
    for a0, a1 in spans:
        o.append(f'<rect x="{x0 + a0 * w:.2f}" y="{yb:.2f}" width="{(a1 - a0) * w:.2f}" height="{s(4):.2f}" '
                 f'fill="{col}"/>')
    o.append(lab(s, x0 + w / 2, yb + s(19), name, "label2", anchor="middle"))
    return "".join(o)


def fig18():
    p = "m8f18_"
    VB, s = VBs(440)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 240.0, 300.0
    o.append(floor(s, 8, 392, fy))
    P, a, b = ds_pose(L_STAR)
    _, J0 = LB.draw(p, s, P, 0, 0, HF)
    body, J = LB.draw(p, s, P, 100 - (J0["bbox"][0] + J0["bbox"][2]) / 2 + 0, fy, HF)
    o.append(body)
    for q in (J["heel"], J["toe_far"]):
        o.append(dot(s, q[0], fy, SER[1]))
    Pr = run_pose()
    _, Jr0 = LB.draw(p, s, Pr, 0, 0, HF)
    clear = 0.06 * 100 * cmu(Jr0)                            # flight clearance 6 cm (design value)
    xr = 300 - (Jr0["bbox"][0] + Jr0["bbox"][2]) / 2
    yr = fy - clear - Jr0["bbox"][3]
    body2, Jr = LB.draw(p, s, Pr, xr, yr, HF)
    o.append(body2)
    o.append(lab(s, Jr["knee_far"][0] + s(4), fy - s(8), "no foot on the ground", "label2", anchor="middle"))
    o.append(lab(s, 10, 22, "walk"))
    o.append(lines(s, 10, 22 + s(18), ["one foot always down;", "both down at the exchange",
                                       f"Fr = v²/gℓ = {FR:.2f}: inverted", "pendulum, vault"]))
    o.append(lab(s, 392, 22, "run", anchor="end"))
    o.append(lines(s, 392, 22 + s(18), ["no double support;", "an aerial (flight) phase",
                                        "faster than Fr ≈ 0.5", f"({math.sqrt(0.5 * G * ELL):.2f} m/s): spring-mass"],
                   anchor="end"))
    ty = fy + s(30)
    o.append(timeline(s, 30, 150, ty, STANCE, f"stance {STANCE * 100:.0f} %: double support"))
    o.append(timeline(s, 236, 150, ty, RUN_DUTY, "stance < 50 %: flight"))
    o.append(lab(s, 30, ty - s(6), "one stride: R and L foot contact", "tick", I["secondary"]))
    o.append(credit(s, VB))
    aria = ("Two side views (Lynch skeleton art). Left: walking at the step-to-step exchange, both feet on the "
            "ground (blue dots): at least one foot is always down and there is a double-support period; at Froude "
            "number 0.18 the body vaults over the stance leg like an inverted pendulum. Right: running in mid-flight, "
            "both feet off the ground. Below, one stride of foot contacts: walking keeps each foot down 62 % of the "
            "stride, so the contacts overlap (blue, double support); running keeps each foot down less than half the "
            "stride (drawn 35 %), so there are gaps with no foot down (orange, flight) and the mechanics become "
            "spring-mass, above Fr about 0.5, 2.16 m/s.")
    return finish(VB, aria, s, o)


# ================================================================ svg #19  C3 exchange vs loss over one step
def fig19():
    p = "m8f19_"
    VB, s = VBs(318)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    ad = math.degrees(ALPHA)
    pl = Plot(s, (62, 58, 300, 252), (-24, 24), (-50, 50))
    o.append(pl.axes([(v, f"{v:g}".replace("-", "−")) for v in (-20, -10, 0, 10, 20)],
                     [(v, f"{v:g}".replace("-", "−")) for v in (-40, -20, 0, 20, 40)],
                     "leg angle θ (degrees; 0 = midstance)", "energy change (J)", grid=(-40, -20, 20, 40)))
    th = np.linspace(-ALPHA, ALPHA, 161)
    dpe = M * G * ELL * (np.cos(th) - math.cos(ALPHA))
    dke = -dpe
    tdeg = np.degrees(th)
    o.append(H.line(s, pl.X(0), pl.Y(50), pl.X(0), pl.Y(-50), I["rule"], "ref", H.DASH_REF))
    o.append(pl.curve(tdeg, dpe, SER[1], multi=True))
    o.append(pl.curve(tdeg, dke, SER[0], multi=True))
    tot = [(pl.X(-ad), pl.Y(0)), (pl.X(ad), pl.Y(0)), (pl.X(ad), pl.Y(-E_LOSS)), (pl.X(24), pl.Y(-E_LOSS))]
    o.append(poly(s, tot, I["primary"], "curve_multi"))
    o.append(H.arrow(s, p, pl.X(ad) + s(9), pl.Y(0) + s(2), pl.X(ad) + s(9), pl.Y(-E_LOSS), "load"))
    o.append(pl.dot(0, E_VAULT, SER[1]))
    o.append(pl.dot(0, -E_VAULT, SER[0]))
    o.append(legend(s, 62, 22, [(SER[1], "PE", None), (SER[0], "KE", None), (I["primary"], "total", None)]))
    e15 = M * G * ELL * (math.cos(math.radians(15)) - math.cos(ALPHA))
    o.append(plabel(s, pl.X(0) + s(8), pl.Y(E_VAULT) - s(6), f"+{E_VAULT:.1f} J", "label2"))
    o.append(plabel(s, pl.X(0) + s(8), pl.Y(-E_VAULT) + s(14), f"−{E_VAULT:.1f} J", "label2"))
    o.append(plabel(s, pl.X(-15) - s(4), pl.Y(e15) - s(6), "PE", "label2", anchor="end"))
    o.append(plabel(s, pl.X(-15) - s(4), pl.Y(-e15) + s(15), "KE", "label2", anchor="end"))
    o.append(plabel(s, pl.X(-8), pl.Y(0) - s(6), "total", "label2", anchor="middle"))
    xr = 306
    o.append(lines(s, xr, pl.Y(36), ["vault:", f"{E_VAULT:.1f} J", "exchanged", "each way,", "not lost"]))
    o.append(lines(s, xr, pl.Y(-12), ["transition:", f"{E_LOSS:.1f} J", "destroyed", "(Prop 5.1)"]))
    o.append(plabel(s, 62, 40, f"one step, θ = −{ad:.1f}° to +{ad:.1f}° (Mg∆h = {E_VAULT:.1f} J, Lab 1)",
                    "label2", I["secondary"]))
    pts = [[pl.X(tdeg[i]), [pl.Y(dpe[i]), pl.Y(dke[i]), pl.Y(0)],
            f"θ {tdeg[i]:.1f}°: PE {dpe[i]:+.1f} J, KE {dke[i]:+.1f} J, total 0".replace("-", "−")]
           for i in range(len(th))]
    pts += [[pl.X(x), pl.Y(-E_LOSS), f"after heel strike: total −{E_LOSS:.1f} J"] for x in np.linspace(ad + 0.3, 24, 6)]
    aria = ("Energy changes over one step of the inverted-pendulum vault at the reference gait, against the leg "
            "angle from -21.1 to +21.1 degrees. Potential energy (blue) rises by Mg delta h = 43.8 J to midstance and "
            "falls back; kinetic energy (red) does the opposite, so the total (black) stays flat: midstance is an "
            "exchange, not a loss. Only at the step-to-step transition, after +21.1 degrees, does the total drop, "
            "by 26.7 J destroyed in the heel-strike collision (Prop 5.1). The exchange is larger than the loss, and "
            "only the loss has to be paid for.")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ svg #20  C4 COP heel to toe (Lab 3)
C4_S = (0.10, 0.28, 0.50, 0.72, 0.95)     # stance fractions marked (0.28 / 0.72 = the 1.10 W peaks, 0.50 = trough)


def fig20():
    p = "m8f20_"
    VB, s = VBs(352)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    Pf = LB.pose()
    Q = LB.Pose("lat")
    Q.__dict__.update(Pf.__dict__)
    Q.segs = [g for g in Pf.segs if g[0] == "lat_foot" and not g[5]]
    HB = 1700.0
    fy = 128.0
    _, J0 = LB.draw(p, s, Q, 0, 0, HB)
    xa = 104.0
    foot, JF = LB.draw(p, s, Q, xa - (J0["ankle"][0] - J0["heel"][0]), fy, HB)
    cm = cmu(JF)
    ax, ay = JF["ankle"]
    close((ax - JF["heel"][0]) / cm, 4.3, 0.05)              # kit: heel 4.3 cm behind the malleolus tip
    o.append(floor(s, 20, 392, fy))
    o.append(foot)
    o.append(H.joint_centre(s, ax, ay))
    o.append(lab(s, ax - s(9), ay - s(10), "ankle", "label2", anchor="end"))
    o.append(ext(s, ax, ay + s(8), ax, fy - s(6)))
    X = lambda xm: ax + xm * 100 * cm  # noqa: E731
    sel = (S3 >= C4_S[0])
    o.append(poly(s, [(X(x), fy - s(2.5)) for x in XCOP[sel][::10]], O["geometry"], "curve"))
    kW = s(80)                                               # 1 body weight = 80 px of arrow
    yr = fy + 1.10 * kW + s(18)
    for sv in C4_S:
        i = int(round(sv * 600))
        x, f = X(XCOP[i]), FYW[i]
        o.append(H.arrow(s, p, x, fy + f * kW, x, fy + s(1), "reaction"))
        o.append(dot(s, x, fy - s(2.5), O["geometry"], 3.5))
        anc, xl = ("end", x + s(12)) if sv == C4_S[0] else ("middle", x)       # the 10 % and 28 % labels would touch
        o.append(lab(s, xl, yr, f"{sv * 100:.0f} %", "label2", anchor=anc))
        o.append(lab(s, xl, yr + s(15), f"{f:.2f} W", "tick", I["secondary"], anchor=anc))
    o.append(lab(s, X(XCOP[60]) - s(6), fy - s(9), "COP", "label2", anchor="end"))
    o.append(lines(s, 392, 20, ["heel strike → foot flat → push-off:", "load moves forward, so the",
                                "pressure-weighted mean moves", "from heel to toes, crossing the",
                                "ankle at 18 % of stance (Lab 3)"], anchor="end"))
    o.append(lines(s, 10, yr + s(36), ["arrows: vertical ground reaction at the COP, in body weights W, at",
                                       "five instants (% of stance); x = −0.04 + 0.225 s m from the ankle"],
                   "tick", lead=1.25))
    o.append(credit(s, VB))
    fw = ", ".join(f"{FYW[int(round(v * 600))]:.2f}" for v in C4_S)
    aria = ("Side view of the foot bones (Lynch art) on the floor, enlarged, with the centre of pressure (blue) "
            "moving forward under the foot during stance, as Lab 3 models it: x = -0.04 + 0.225 s metres from the "
            "ankle. Upward vertical ground-reaction arrows sit at the centre of pressure at 10, 28, 50, 72 and 95 % "
            f"of stance, scaled to their Lab 3 values ({fw} body weights). Load passes "
            "from the heel at heel strike through the midfoot to the forefoot at push-off, so the pressure-weighted "
            "mean moves from heel to toes and crosses the ankle at 18 % of stance.")
    return finish(VB, aria, s, o)


# ================================================================ svg #21  C5 long steps cost more per step
def fig21():
    p = "m8f21_"
    VB, s = VBs(492)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 235.0, 318.0
    o.append(floor(s, 8, 392, fy))
    rows = []
    for k, (L, al, el, es, x_heel) in enumerate(((L_STAR, ALPHA, E_LOSS, E_SWING, 168.0),
                                                 (L_LONG, ALPHA_L, E_LOSS_L, E_SWING_L, 352.0))):
        P, a, b = ds_pose(L, lead=None if k == 0 else 28.0)   # long step: lead thigh 28 deg so the trailing toe reaches
        body, J = LB.draw(p, s, P, x_heel, fy, HF)
        (cx, cy), m = model_com(J, L, al)
        o.append(body)
        x0, x1 = J["toe_far"][0], J["heel"][0]
        o.append(ext(s, x0, fy, cx, cy))
        o.append(ext(s, x1, fy, cx, cy))
        r = s(34)
        a0, a1 = 90 + math.degrees(al), 90 - math.degrees(al)
        o.append(arc(s, p, cx, cy, r, a1, a0, "geometry", head=False))
        o.append(H.com_mark(s, cx, cy))
        o.append(lab(s, cx + s(10), cy - s(9), f'2{it("α")} = {2 * math.degrees(al):.1f}°', "label2"))
        o.append(dot(s, x0, fy, I["primary"]))
        o.append(dot(s, x1, fy, I["primary"]))
        o.append(dim_h(s, p, x0, x1, fy + s(16), f'{it("L")} = {L:.2f} m', below=True))
        rows.append((x0, x1, L, al, el, es))
    L2 = s(H.PX["label2"]) * 1.35
    yt = fy + s(56)
    for (x0, x1, L, al, el, es), anchor, xx in zip(rows, ("start", "start"), (10, 206)):
        c = V / L
        o.append(lines(s, xx, yt, [f"cadence {c:.2f} steps/s",
                                   f"collision {el:.1f} J per step", f"swing {es:.1f} J per step",
                                   f"total {el + es:.1f} J per step"]))
    o.append(lab(s, 10, 22, "preferred step (Lab 2)"))
    o.append(lab(s, 206, 22, "20 % longer step"))
    o.append(lines(s, 10, 22 + s(18), [f"{it('v')} = {V} m/s for both;", "collision ∝ sin²2α"]))
    o.append(lines(s, 206, 22 + s(18), ["lower cadence, but the", "collision term grows faster",
                                        f"than swing falls: +{((E_LOSS_L + E_SWING_L) / (E_LOSS + E_SWING) - 1) * 100:.1f} %"]))
    o.append(credit(s, VB))
    aria = ("Two walkers (Lynch skeleton art) at the step-to-step exchange, both at 1.3 m/s, with the point-mass "
            "model legs drawn from each contact to the centre of mass. Left, the preferred step L = 0.68 m: the legs "
            "meet at 2 alpha = 42.2 degrees, cadence 1.90 steps per second, collision loss 26.7 J and swing cost "
            "22.7 J per step. Right, a step 20 % longer, L = 0.82 m: 2 alpha = 51.2 degrees, cadence only 1.58 steps "
            "per second, but the collision loss rises to 36.0 J while the swing cost falls only to 15.8 J, so each "
            "step costs 4.6 % more. A wider angle between successive pendulum arcs means more velocity to redirect.")
    return finish(VB, aria, s, o)


# ================================================================ svg #22  C6 push-off before the collision
def hodo(s, p, x, y, k, turns, name, cost):
    """Velocity diagram: arrows from (x, y); turns = [(angle deg, speed m/s, label)], k = units per m/s."""
    o = [H.line(s, x - s(6), y, x + k * 1.55, y, I["rule"], "leader")]
    for ang, sp, t in turns:
        o.append(vec(s, p, x, y, ang, sp * k, "dim"))
        ex, ey = x + sp * k * math.cos(math.radians(ang)), y + sp * k * math.sin(math.radians(ang))
        o.append(lab(s, ex + s(4), ey + (s(12) if ang > 0 else (s(4) if ang == 0 else s(-2))), t, "label2"))
    o.append(lab(s, x - s(6), y - s(40), name, "label2"))
    o.append(lab(s, x - s(6), y + s(58), cost, "label2"))
    return "".join(o)


def fig22():
    p = "m8f22_"
    VB, s = VBs(400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 270.0, 310.0
    P, a, b = ds_pose(L_STAR)
    _, J0 = LB.draw(p, s, P, 0, 0, HF)
    body, J = LB.draw(p, s, P, 10 - J0["bbox"][0], fy, HF)
    (cx, cy), m = model_com(J, L_STAR, ALPHA)
    o.append(floor(s, 8, 196, fy))
    o.append(body)
    x0, x1 = J["toe_far"][0], J["heel"][0]
    o.append(ext(s, x0, fy, cx, cy))
    o.append(ext(s, x1, fy, cx, cy))
    for (xc, mean, txt) in ((x0, "force", "1"), (x1, "reaction", "2")):
        ux, uy = (cx - xc) / (ELL * m), (cy - fy) / (ELL * m)
        o.append(H.arrow(s, p, xc + ux * s(16), fy + uy * s(16), xc + ux * s(78), fy + uy * s(78), mean))
        tx, ty = xc + ux * s(46), fy + uy * s(46)
        o.append(lab(s, tx + s(9), ty + s(4), txt, "label2"))
    o.append(H.com_mark(s, cx, cy))
    o.append(dot(s, x0, fy, I["primary"]))
    o.append(dot(s, x1, fy, I["primary"]))
    o.append(lab(s, x0 - s(6), fy + s(17), "1 push-off", "label2"))
    o.append(lab(s, x1 + s(6), fy + s(17), "2 heel strike", "label2", anchor="middle"))
    ad = math.degrees(ALPHA)
    k = s(54)
    o.append(hodo(s, p, 214, 138, k, [(ad, V, "v⁻"), (-ad, V * math.cos(2 * ALPHA), "v⁺")],
                  f"collision only: 2α = {2 * ad:.1f}° at once", f"lost {E_LOSS:.1f} J per step"))
    o.append(hodo(s, p, 214, 256, k, [(ad, V, "v⁻"), (0, V / math.cos(ALPHA), "after 1"), (-ad, V, "after 2")],
                  f"push-off first: α, then α ({ad:.1f}°)", f"lost {E_SPLIT:.1f} J per step"))
    o.append(lines(s, 392, 22, ["COM velocity (m/s, drawn to scale):",
                                "push-off (1) turns it before the", "leading heel strikes (2), so the",
                                "collision has less left to destroy"], anchor="end"))
    o.append(lab(s, 392, fy + s(30), f"{E_LOSS:.1f} J → {E_SPLIT:.1f} J: ratio {E_SPLIT / E_LOSS:.3f}, "
                 f"a factor {E_LOSS / E_SPLIT:.2f} (Prop 5.2)", "label2", anchor="end"))
    o.append(credit(s, VB))
    aria = ("Left: a walker (Lynch skeleton art) at the step-to-step transition with the point-mass model legs. "
            "Arrow 1 (red) is the trailing leg's push-off impulse along that leg; arrow 2 (black) is the heel-strike "
            "impulse along the leading leg. Right: the centre-of-mass velocity. Collision only: the heel strike "
            "turns v-minus through the whole 42.2 degrees at once and 26.7 J are lost per step. Push-off first: the "
            "push-off turns the velocity through 21.1 degrees (adding speed), the heel strike turns the remaining "
            "21.1 degrees, and only 8.8 J are lost, a ratio of 0.330, a factor 3.03 (Prop 5.2).")
    return finish(VB, aria, s, o)


# ================================================================ svg #23  C7 the sign of joint power
def fig23():
    p = "m8f23_"
    VB, s = VBs(470)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 300.0, 380.0
    P, a, b = ds_pose(L_STAR)
    _, J0 = LB.draw(p, s, P, 0, 0, HF)
    body, J = LB.draw(p, s, P, 200 - (J0["bbox"][0] + J0["bbox"][2]) / 2, fy, HF)
    o.append(floor(s, 8, 392, fy))
    o.append(body)
    # trailing (far) ankle in push-off: plantarflexor torque and plantarflexion velocity, both clockwise on screen
    ax, ay = J["ankle_far"]
    o.append(arc(s, p, ax, ay, s(18), -60, 40, "force"))
    o.append(arc(s, p, ax, ay, s(30), -50, 50, "geometry"))
    o.append(H.joint_centre(s, ax, ay))
    o.append(lab(s, ax - s(20), ay - s(18), f'{it("τ")}', "label2", anchor="end"))
    o.append(lab(s, ax + s(28), ay - s(26), f'{it("θ̇")}', "label2"))
    # leading (near) knee in loading response: extensor torque (counter-clockwise), knee flexing (clockwise)
    kx, ky = J["knee"]
    o.append(arc(s, p, kx, ky, s(18), 60, -40, "force"))
    o.append(arc(s, p, kx, ky, s(30), -50, 50, "geometry"))
    o.append(H.joint_centre(s, kx, ky))
    o.append(lab(s, kx + s(22), ky - s(20), f'{it("τ")}', "label2"))
    o.append(lab(s, kx + s(34), ky + s(30), f'{it("θ̇")}', "label2"))
    o.append(lines(s, 10, 22, ["trailing ankle,", "in push-off: τ and θ̇", "turn the same way,",
                               f'{it("P")} > 0: adds energy', "(Lab 3 peak 215 W,", "3.07 W/kg)"]))
    o.append(lines(s, 392, 22, ["leading knee, after", "heel strike: extensor τ", "while the knee flexes,",
                                f'{it("P")} < 0: absorbs', "(section 6 figure:", "−1.2 W/kg at 16 %)"], anchor="end"))
    o.append(legend(s, 10, fy + s(30), [(O["force"], "net joint torque τ", None),
                                        (O["geometry"], "angular velocity θ̇", None)]))
    o.append(lab(s, 392, fy + s(30), f'{it("P")} = {it("τ")}{it("θ̇")}', "label2", anchor="end"))
    o.append(credit(s, VB))
    aria = ("A walker (Lynch skeleton art) at the step-to-step transition, with two joints marked. At the trailing "
            "ankle in push-off, the net plantarflexor torque (red arc) and the plantarflexion velocity (blue arc) "
            "turn the same way, so the power P = tau theta-dot is positive: the joint adds mechanical energy (Lab 3: "
            "peak 215 W, 3.07 W/kg). At the leading knee just after heel strike, the net extensor torque turns one "
            "way while the knee flexes the other way, so P is negative: the joint absorbs energy (about -1.2 W/kg at "
            "16 % of the cycle in the section 6 figure).")
    return finish(VB, aria, s, o)


# ================================================================ svg #24  C8 arm swing cancels leg yaw momentum
def fig24():
    p = "m8f24_"
    VB, s = VBs(430)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 270.0, 336.0
    # near = left side (the subject faces right): left leg in stance, right leg swinging forward;
    # left arm forward, right arm back (the arm opposite each leg)
    P = LB.pose(near=dict(hip=0, knee=8, shoulder=22, elbow=15),
                far=dict(hip=25, knee=45, contact=None, ankle=5, shoulder=-22, elbow=10), anchor=("heel", "near"))
    _, J0 = LB.draw(p, s, P, 0, 0, HF)
    body, J = LB.draw(p, s, P, 84 - (J0["bbox"][0] + J0["bbox"][2]) / 2, fy, HF)
    o.append(floor(s, 8, 176, fy))
    o.append(body)
    kn, wr = J["knee_far"], J["wrist"]
    o.append(H.arrow(s, p, kn[0] + s(10), kn[1], kn[0] + s(34), kn[1], "dim"))
    o.append(lab(s, kn[0] + s(38), kn[1] + s(4), "R leg", "label2"))
    o.append(H.arrow(s, p, wr[0] + s(8), wr[1] - s(12), wr[0] + s(32), wr[1] - s(12), "dim"))
    o.append(lab(s, wr[0] + s(36), wr[1] - s(8), "L arm", "label2"))
    # top view: forward = up the page, the subject's left on the left
    cx, k, kv = 296.0, s(330), s(40)                         # units per metre of offset; units per m/s
    ysh, yhp = 150.0, 232.0
    o.append(lab(s, cx, 92, "seen from above: forward = up, m/s", "label2", anchor="middle"))
    o.append(H.line(s, cx - D_ARM * k, ysh, cx + D_ARM * k, ysh, I["secondary"], "ref"))
    o.append(H.line(s, cx - D_LEG * k - s(10), yhp, cx + D_LEG * k + s(10), yhp, I["secondary"], "ref"))
    o.append(H.line(s, cx, ysh, cx, yhp, I["rule"], "leader"))
    for side, d, vv, yy, col, mk, name in ((-1, D_ARM, V_ARM, ysh, SER[1], "geometry", "L arm"),
                                           (1, D_ARM, -V_ARM, ysh, SER[1], "geometry", "R arm"),
                                           (-1, D_LEG, -V, yhp, SER[0], "force", "L leg"),
                                           (1, D_LEG, V, yhp, SER[0], "force", "R leg")):
        x = cx + side * d * k
        o.append(H.line(s, x, yy, x, yy - vv * kv, col, "curve", extra=f'marker-end="url(#{p}a_{mk})"'))
        o.append(dot(s, x, yy, col))
        ty = yy + s(16) if vv > 0 else yy - s(7)
        o.append(lab(s, x, ty, name, "tick", I["secondary"], anchor="middle"))
        o.append(lab(s, x + side * s(6), yy - vv * kv / 2 + s(4), f"{abs(vv):g}", "tick", I["secondary"],
                     anchor="start" if side > 0 else "end"))
    o.append(arc(s, p, cx, yhp, s(17), 150, 30, "force"))
    o.append(arc(s, p, cx, ysh, s(17), -150, -30, "geometry"))

    o.append(legend(s, 196, 290, [(SER[0], f"legs {H_LEGS:.2f}", None), (SER[1], f"arms {H_ARMS:.2f}", None)]))
    o.append(lab(s, 196, 306, "yaw momentum, kg m²/s", "tick", I["secondary"]))
    o.append(lines(s, 10, 22, ["legs: opposite sides, opposite ways, so", "their yaw momenta add; each arm swings",
                               f"against its leg and cancels {H_ARMS / H_LEGS * 100:.0f} % of it"]))
    o.append(lines(s, 196, 330, [f"trunk yaw torque, mean over each", f"half stride ({T_STRIDE / 2:.3f} s):",
                                 f"arms held {TQ_STILL:.1f} N m,", f"arms swinging {TQ_SWING:.1f} N m"]))
    o.append(credit(s, VB))
    aria = ("Left: a walker (Lynch skeleton art) with the right leg swinging forward and the left arm forward, the "
            "arm opposite each leg. Right: the same instant seen from above. The legs (red), 0.09 m either side of "
            "the midline, move at 1.3 m/s in opposite directions, so their yaw momenta add to 2.64 kg m^2/s about "
            "the vertical axis; the arms (blue), 0.20 m out, move at 0.6 m/s the other way and carry 0.84 kg m^2/s "
            "of the opposite sense, cancelling 32 %. The trunk must reverse only the residual 1.80 kg m^2/s each "
            "half stride of 0.527 s: a mean yaw torque of 6.8 N m with the arms swinging against 10.0 N m with "
            "them held still.")
    return finish(VB, aria, s, o)


# ================================================================ svg #25  C9 passive walker: slope vs level
def fig25():
    p = "m8f25_"
    VB, s = VBs(440)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 235.0, 314.0
    gd = math.degrees(GAMMA9)
    P, a, b = ds_pose(L9, kf=12)
    for k, xh in enumerate((150.0, 340.0)):
        body, J = LB.draw(p, s, P, xh, fy, HF)
        (cx, cy), m = model_com(J, L9, ALPHA9)
        x0 = J["toe_far"][0]
        if k == 0:                                           # slope: the whole walker turned by gamma about the heel
            ys = lambda x: fy + (x - xh) * math.tan(GAMMA9)  # noqa: E731
            o.append(H.line(s, 10, ys(10), 196, ys(196), I["axis"], "axis"))
            o.append(H.line(s, 196, ys(196), 40, ys(196), O["dim"], "ref", H.DASH_REF))
            o.append(f'<g transform="rotate({gd:.3f} {xh:.2f} {fy:.2f})">' + body + ext(s, x0, fy, cx, cy)
                     + ext(s, xh, fy, cx, cy) + H.com_mark(s, cx, cy) + "</g>")
            o.append(lab(s, 10, ys(196) + s(16), f"γ = {GAMMA9} rad ({gd:.2f}°), drawn true", "tick", I["secondary"]))
            o.append(lab(s, 10, ys(196) + s(31), f"COM drops L sin γ = {L9 * math.sin(GAMMA9) * 100:.1f} cm per step",
                         "tick", I["secondary"]))
            ccx = xh + (cx - xh) * math.cos(GAMMA9) - (cy - fy) * math.sin(GAMMA9)
            ccy = fy + (cx - xh) * math.sin(GAMMA9) + (cy - fy) * math.cos(GAMMA9)
            o.append(H.arrow(s, p, ccx + s(14), ccy + s(8), ccx + s(14), ccy + s(48), "load"))
            o.append(lab(s, ccx + s(19), ccy + s(44), f'{it("Mg")}', "label2"))
        else:
            o.append(H.line(s, 206, fy, 392, fy, I["axis"], "axis"))
            o.append(body + ext(s, x0, fy, cx, cy) + ext(s, xh, fy, cx, cy) + H.com_mark(s, cx, cy))
            ux, uy = (cx - x0) / (ELL * m), (cy - fy) / (ELL * m)
            o.append(H.arrow(s, p, x0 + ux * s(14), fy + uy * s(14), x0 + ux * s(70), fy + uy * s(70), "force"))
            o.append(lab(s, x0 + ux * s(40) - s(10), fy + uy * s(40), "push-off", "label2", anchor="end"))
    o.append(lab(s, 10, 22, "on a slope: no motor"))
    o.append(lines(s, 10, 22 + s(18), [f"gravity supplies MgL sin γ = {E_GRAV:.1f} J", "per step; heel strike destroys",
                                       f"½Mv² sin²2α = {E_GRAV:.1f} J at", f"{it('v')} = {V9:.2f} m/s: steady gait"]))
    o.append(lab(s, 392, 22, "on the level", anchor="end"))
    o.append(lines(s, 392, 22 + s(18), ["gravity supplies 0 J; the only", "balance is v = 0. To keep",
                                        f"{V9:.2f} m/s, muscle must add", f"the {E_GRAV:.1f} J lost per step"],
                   anchor="end"))
    o.append(lab(s, 200, fy + s(54), f"same walker: L = {L9:.2f} m, 2α = {math.degrees(2 * ALPHA9):.1f}° "
                 f"(section 9)", "label2", anchor="middle"))
    o.append(credit(s, VB))
    aria = ("Two walkers (Lynch skeleton art) at the step-to-step exchange, both the section 9 walker with step "
            "length 0.56 m and 2 alpha = 34.4 degrees. Left, on a slope of gamma = 0.05 rad (2.86 degrees, drawn at "
            "the true angle) with no motor: the centre of mass drops 2.8 cm per step, so gravity supplies "
            "MgL sin gamma = 19.3 J per step, exactly what the heel strike destroys at 1.31 m/s, and the gait "
            "repeats. Right, on level ground: gravity supplies nothing, the only balance is v = 0, so to keep "
            "walking at 1.31 m/s the trailing leg's push-off (red) must add the 19.3 J lost at every step.")
    return finish(VB, aria, s, o)


# ================================================================ svg #26  C10 the fall stack
def fig26():
    p = "m8f26_"
    VB, s = VBs(450)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 225.0, 300.0
    # a forward trip: trunk pitched 48 deg forward, the stance leg behind on its toes, the other leg swinging
    # forward to step, arms thrown forward (design pose; the kit's Winter COM: the text states none for a fall)
    P = LB.pose(pelvis=30, trunk=18, neck=-15,
                near=dict(hip=75, knee=25, contact=None, ankle=15, shoulder=80, elbow=20),
                far=dict(hip=10, knee=15, contact="toe", shoulder=100, elbow=15), anchor=("toe", "far"))
    _, J0 = LB.draw(p, s, P, 0, 0, HF)
    body, J = LB.draw(p, s, P, 14 - J0["bbox"][0], fy, HF)
    o.append(floor(s, 8, 168, fy))
    o.append(body)
    c = J["com"]
    o.append(H.com_mark(s, *c))
    o.append(ext(s, c[0], c[1] + s(8), c[0], fy))
    o.append(H.arrow(s, p, c[0] + s(8), c[1] - s(8), c[0] + s(36), c[1] - s(8), "dim"))
    o.append(lines(s, 10, fy + s(20), ["trip: the COM runs ahead of", "the stance foot faster than",
                                       "a step can follow"], "tick"))
    bx, bw, bh, gap = 176.0, 216.0, s(78), s(12)
    rows = [("Physics: the visible event", ["one step recovers only if", "ξ = x + ẋ/ω₀ ≤ step reach;",
                                             "impact energy,", "contact path"]),
            ("Biology: control reserve", ["sarcopenia, slow noisy sensing,", "reaction delay;",
                                          "after the fall: pain, fear,", "deconditioning"]),
            ("Chemistry / materials", ["vitamin D, glycation, drugs;", "bone mineral, collagen",
                                       "cross-links set the", "fracture threshold"])]
    # box height from its content: header line, then the body rows at 1.25 lead
    bh = s(31) + (max(len(r) for _, r in rows) - 1) * s(H.PX["tick"]) * 1.25 + s(9)
    y0 = 36.0
    for i, (head, body_rows) in enumerate(rows):
        y = y0 + i * (bh + gap)
        o.append(rect(s, bx, y, bw, bh))
        o.append(lab(s, bx + s(7), y + s(16), head, "label2"))
        o.append(lines(s, bx + s(7), y + s(31), body_rows, "tick", lead=1.25))
        if i:
            o.append(H.arrow(s, p, bx + bw / 2, y - s(1), bx + bw / 2, y - gap + s(2), "dim"))
    o.append(lab(s, bx, 22, "read the stack from the bottom up:", "label2"))
    o.append(lines(s, bx, y0 + 3 * (bh + gap) + s(4),
                   [f"Lab 4 reference: ξ = {XI:.3f} m against a", f"{REACH} m reach, margin {REACH - XI:.3f} m;",
                    f"a {DELAY:.2f} s reaction delay spends {V_P * DELAY:.3f} m"], "tick"))
    o.append(credit(s, VB))
    aria = ("Left: a skeleton (Lynch art) tripping forward, its centre of mass running ahead of the stance foot. "
            "Right: the causal stack, read from the bottom up. Chemistry and materials (vitamin D, glycation, drugs; "
            "bone mineral and collagen cross-links) set the tissue substrate and the fracture threshold at impact. "
            "Biology (sarcopenia, slow and noisy sensing, reaction delay; after the fall pain, fear and "
            "deconditioning) sets the control reserve. Physics is the visible event: one step recovers only if the "
            "extrapolated centre of mass xi = x + x-dot/omega0 stays within step reach; in the Lab 4 reference xi = "
            "0.260 m against a 0.415 m reach, a margin of 0.155 m, of which a 0.20 s delay spends 0.090 m.")
    return finish(VB, aria, s, o)


FIGS = {
    17: ("C1: Identify which part of a walking step is controlled fall", fig17),
    18: ("C2: Explain why walking has double support but running has f", fig18),
    19: ("C3: Why is midstance not the most energetically expensive pa", fig19),
    20: ("C4: Why does the COP move from heel to toe in stance? (foot ", fig20),
    21: ("C5: Explain why long steps can be costly even if cadence is ", fig21),
    22: ("C6: Why does ankle push-off reduce heel-strike loss? (body p", fig22),
    23: ("C7: What does positive joint power mean? (body pose, force v", fig23),
    24: ("C8: Why can arm swing reduce walking cost? (body pose, force", fig24),
    25: ("C9: Why is passive dynamic walking not free on level ground?", fig25),
    26: ("C10: Why do older-adult falls require physics, chemistry, an", fig26),
}
