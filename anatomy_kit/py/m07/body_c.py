"""Module 7, group `body_c`: conceptual problems C1-C10 (svg #26-#35), house style, 400 px.

Whole bodies come from the posable Lynch skeleton (lynch_body.py); body_main.py puts its defs on the page.
Stature 1.75 m (K4, module07.html line 862: l = 0.55 h - 0.06 m = 0.90 m at h = 1.75 m), so 1 cm = LB.H_U / 175
body units.  Quiet-standing COM mark at the text's values: 0.55 H above the floor (line 144), 0.02 m ahead of the
ankle (line 176).  Every number on a figure is computed here from the constants the module states (line numbers
beside each constant); the DDE runs are the Lab 1 integrator (lines 623-640), ported line for line.
"""
import math

import numpy as np

import house as H
import lynch_body as LB
from m05.body import finish, it
from m05.plots_prob import Plot, hov, label as plabel, legend

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
CM = LB.H_U / 175.0                     # body units per cm (stature 1.75 m)
BOX = "#f7f4ef"

# ---------------------------------------------------------------- numbers module07.html states
M, G, ELL, I_A = 70.0, 9.81, 0.9, 66.0  # kg, m/s^2, m, kg m^2 (line 357)
MGL = 618.0                             # N m/rad (lines 424, 621)
MG_T = 690.0                            # N, "Mg ~ 690 N" (lines 522, 835)
D_TOE, D_HEEL, X_COM = 0.12, 0.05, 0.02  # m (line 176)
COM_H = 0.55                            # COM height / stature (line 144)
KP, KD = 900.0, 120.0                   # representative gains (line 493)
KP1, KD1 = 1100.0, 150.0                # K1 gains (line 848)
K_INT = 0.9 * MGL                       # intrinsic ankle stiffness (line 425)
MT, RT, ML, RL, DE = 35.0, 0.30, 20.0, 0.40, 0.05   # worked lift (line 601)
LIMIT = 3400.0                          # N, injury-risk threshold (lines 603, 683)
K8 = ((1.0, 660.0), (2.0, 732.0))       # (recovery rate 1/s, cheapest K_p) at delay 0.15 s (line 878)
W0 = math.sqrt(M * G * ELL / I_A)       # toppling rate (line 360)


def close(v, ref, tol):
    assert abs(v - ref) <= tol * 1.0001, (v, ref)


def quartic(kp, kd):
    """Prop 6.3: crossing frequency and critical delay (lab code lines 652-655)."""
    a, b, c = I_A * I_A, 2 * I_A * MGL - kd ** 2, MGL ** 2 - kp ** 2
    wc = math.sqrt((-b + math.sqrt(b * b - 4 * a * c)) / (2 * a))
    return wc, math.atan(kd * wc / kp) / wc


def simulate(kp, kd, dly, t_end=25.0, dt=1e-3, th0=0.6):
    """Lab 1 method-of-steps integrator (lines 623-636); also returns the delayed rate for the COP."""
    n, nd = int(t_end / dt), int(round(dly / dt))
    th, w = np.zeros(n), np.zeros(n)
    th[0] = th0
    for k in range(n - 1):
        j = k - nd
        thd = th[j] if j >= 0 else th0
        wd = w[j] if j >= 0 else 0.0
        acc = (MGL * th[k] - kp * thd - kd * wd) / I_A
        w[k + 1] = w[k] + dt * acc
        th[k + 1] = th[k] + dt * w[k + 1]
    thd = np.concatenate([np.full(nd, th0), th[:n - nd]])
    wd = np.concatenate([np.zeros(nd), w[:n - nd]])
    return np.arange(n) * dt, th, thd, wd


WC, DCRIT = quartic(KP, KD)
WC1, DCRIT1 = quartic(KP1, KD1)
close(W0, 3.06, 0.005)                          # line 360
close(1 / W0, 0.33, 0.005)                      # line 360
close(M * G * ELL, MGL, 0.5)                    # line 424
close(WC, 2.2, 0.05)                            # line 494
close(WC / (2 * math.pi), 0.35, 0.005)          # lines 494, 667
close(DCRIT * 1e3, 129.7, 0.05)                 # line 666
close(WC1, 2.93, 0.005)                         # line 850
close(WC1 / (2 * math.pi), 0.47, 0.005)         # line 850
close(DCRIT1 * 1e3, 129.7, 0.05)                # line 850
close(1 + WC ** 2 / W0 ** 2, 1.52, 0.005)       # line 874
close(MG_T * D_TOE, 80, 3)                      # "near 80 N m" (line 522)
M_L5 = G * (MT * RT + ML * RL)                  # Prop 8.1 at phi = 90 deg
F_SP = M_L5 / DE                                # Prop 8.2, cos(phi) = 0
close(M_L5, 181, 0.5)                           # line 602
close(F_SP / 1e3, 3.6, 0.05)                    # line 602
close(F_SP / (M * G), 5.3, 0.05)                # line 603


# ---------------------------------------------------------------- drawing helpers
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


def arc(s, p, cx, cy, r, a0, a1, meaning="force"):
    """Curved arrow on a circle about (cx, cy), from screen angle a0 to a1 (deg, + = clockwise)."""
    q = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))  # noqa: E731
    (x0, y0), (x1, y1) = q(a0), q(a1)
    sweep = 1 if a1 > a0 else 0
    big = 1 if abs(a1 - a0) > 180 else 0
    return (f'<path d="M{x0:.2f},{y0:.2f} A{r:.2f},{r:.2f} 0 {big} {sweep} {x1:.2f},{y1:.2f}" fill="none" '
            f'stroke="{O[meaning]}" stroke-width="{s(H.PX["geom"]):.2f}" marker-end="url(#{p}a_{meaning})"/>')


def rect(s, x, y, w, h, fill=BOX, stroke=I["secondary"]):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{s(1.2):.2f}"/>')


def cmu(J):
    """Figure units per cm for a drawn body."""
    return CM * J["scale"]


def com_quiet(J, HF):
    """The text's quiet-standing COM: 0.55 H up, 0.02 m ahead of the ankle (lines 144, 176)."""
    return J["ankle"][0] + X_COM * 100 * cmu(J), J["floor_y"] - COM_H * HF


def whole_com(J, P, extra=()):
    """Mass-weighted COM of the drawn body (kit Winter masses) plus extra (point, mass fraction) items."""
    items = [(J["com_" + k], v[1]) for k, v in P.com.items()] + list(extra)
    m = sum(w for _, w in items)
    return sum(c[0] * w for c, w in items) / m, sum(c[1] * w for c, w in items) / m


def bisect(f, lo, hi, n=60):
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


def omega(s):
    return f'ω{sub("0", s, "label2")}'


# ================================================================ svg #26  C1 broomstick on the palm vs the body
BROOM_L = 1.2                            # m, a broomstick (design choice; the text gives no length)


def fig26():
    p = "m7f26_"
    VB, s = VBs(455)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 240.0, 368.0
    P = LB.pose(near=dict(shoulder=40, elbow=110, wrist=-60))
    body, J = LB.draw(p, s, P, 112.0, fy, HF, skin=True)
    cm = cmu(J)
    o.append(floor(s, 30, 300, fy))
    # broomstick: uniform stick, pivot on the palm, leaning 6 deg forward
    wr, ft = J["wrist"], J["fingertip"]
    px_, py_ = LB.lerp(wr, ft, 0.42)
    py_ -= s(4)
    lean = math.radians(6)
    Lb = BROOM_L * 100 * cm
    top = (px_ + Lb * math.sin(lean), py_ - Lb * math.cos(lean))
    bc = ((px_ + top[0]) / 2, (py_ + top[1]) / 2)
    o.append(body)
    o.append(H.line(s, px_, py_, top[0], top[1], I["secondary"], "force",
                    extra=f'stroke-linecap="round" style="stroke-width:{s(5):.2f}"'))
    # body pendulum: ankle -> COM (text values)
    ax, ay = J["ankle"]
    cx, cy = com_quiet(J, HF)
    o.append(ext(s, ax, ay, cx, cy))
    xd = J["heel"][0] - s(26)
    o.append(ext(s, xd - s(4), ay, ax - s(6), ay))
    o.append(ext(s, xd - s(4), cy, cx - s(8), cy))
    o.append(H.arrow(s, p, xd, ay, xd, cy, "geometry", both=True))
    o.append(lab(s, xd - s(6), (ay + cy) / 2 + s(5), f'{it("ℓ")} = 0.9 m', anchor="end"))
    o.append(H.arrow(s, p, cx, cy, cx, cy + s(46), "load"))
    o.append(lab(s, cx + s(6), cy + s(44), f'{it("Mg")}', "label2"))
    o.append(H.com_mark(s, cx, cy))
    o.append(H.joint_centre(s, ax, ay))
    o.append(arc(s, p, ax, ay, s(17), 150, 30, "force"))
    o.append(lab(s, ax + s(22), ay - s(14), f'ankle torque {it("τ")}', "label2"))
    # broom pendulum: palm -> broom COM
    nx, ny = math.cos(lean), math.sin(lean)              # unit normal to the stick (to the right)
    off = s(14)
    a0 = (px_ + nx * off, py_ + ny * off)
    a1 = (bc[0] + nx * off, bc[1] + ny * off)
    o.append(H.arrow(s, p, a0[0], a0[1], a1[0], a1[1], "geometry", both=True))
    o.append(lab(s, a1[0] + s(6), (a0[1] + a1[1]) / 2 + s(5), f'{it("ℓ")}{sub("b", s)}'))
    o.append(H.arrow(s, p, bc[0], bc[1], bc[0], bc[1] + s(34), "load"))
    o.append(H.com_mark(s, *bc))
    ya = py_ + s(22)
    o.append(H.arrow(s, p, px_ - s(8), ya, px_ + s(30), ya, "force"))
    o.append(lab(s, px_ + s(34), ya + s(4), "palm moves", "label2"))
    # text
    L2 = s(H.PX["label2"]) * 1.35
    for i, t in enumerate(["body: pivot = ankle,", f'control = ankle torque {it("τ")}',
                           f'{it("ℓ")} = 0.9 m: {omega(s)} ≈ 3.06 s⁻¹',
                           f'{it("τ")}{sub("c", s, "label2")} = 1/{omega(s)} ≈ 0.33 s']):
        o.append(lab(s, 10, 24 + i * L2, t, "label2"))
    for i, t in enumerate(["broomstick: pivot = palm,", "control = palm motion",
                           f'shorter {it("ℓ")}: larger {omega(s)},', "falls faster"]):
        o.append(lab(s, 392, 24 + i * L2, t, "label2", anchor="end"))
    o.append(lab(s, 200, fy + s(26), f'same model: {omega(s)} = √({it("Mgℓ")}/{it("I")}), toppling time 1/{omega(s)}',
                 "label2", anchor="middle"))
    o.append(credit(s, VB))
    aria = ("Side view of a standing skeleton (Lynch art) balancing a broomstick upright on its raised palm. Both are "
            "inverted pendulums: the body pivots at the ankle with its centre of mass l = 0.9 m above it and is "
            "controlled by ankle torque; the stick pivots on the palm with its centre of mass at l_b, a shorter "
            "distance, and is controlled by moving the palm. Same model, omega0 = sqrt(Mgl/I): the body's omega0 is "
            "about 3.06 per second (toppling time 0.33 s); the shorter l of the stick gives a larger omega0, so it "
            "falls faster.")
    return finish(VB, aria, s, o)


# ================================================================ svg #27  C2 sitting vs standing
def fig27():
    p = "m7f27_"
    VB, s = VBs(400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 240.0, 318.0
    o.append(floor(s, 8, 392, fy))
    # sitting (kit pose, kit COM: the text states no seated COM)
    P = LB.pose(**LB.POSES["sitting"])
    _, J0 = LB.draw(p, s, P, 0, 0, HF)
    x_s = 22 - (J0["hip"][0] - 0.10 * HF)                  # chair back at x = 22
    body, J = LB.draw(p, s, P, x_s, fy, HF)
    top = J["hip"][1] + 0.06 * HF                          # seat as in pilot_body/build_gallery.py
    back, front = J["hip"][0] - 0.10 * HF, J["hip"][0] + 0.20 * HF
    o.append(rect(s, back, top, front - back, s(6)))
    for xx in (back + s(3), front - s(6)):
        o.append(rect(s, xx, top + s(6), s(3), fy - top - s(6)))
    o.append(body)
    c = J["com"]
    o.append(ext(s, c[0], c[1] + s(8), c[0], fy))
    o.append(H.com_mark(s, *c))
    yb = fy + s(16)
    o.append(H.arrow(s, p, back, yb, J["toe"][0], yb, "geometry", both=True))
    o.append(lab(s, back, yb + s(17), "base of support: seat to toes", "label2"))
    # standing (text COM)
    body2, J2 = LB.standing_full(p, s, 300.0, fy, HF)
    o.append(body2)
    c2 = com_quiet(J2, HF)
    o.append(ext(s, c2[0], c2[1] + s(8), c2[0], fy))
    o.append(H.com_mark(s, *c2))
    cm = cmu(J2)
    xa = J2["ankle"][0]
    o.append(H.arrow(s, p, xa - D_HEEL * 100 * cm, yb, xa + D_TOE * 100 * cm, yb, "geometry", both=True))
    o.append(lab(s, xa + 3.5 * cm, yb + s(17), f"foot base {D_HEEL + D_TOE:.2f} m", "label2", anchor="middle"))
    L2 = s(H.PX["label2"]) * 1.35
    o.append(lab(s, 10, 24, "sitting"))
    for i, t in enumerate(["COM low, far inside a wide", "base: no control needed;", "asleep, it stays put"]):
        o.append(lab(s, 10, 24 + (i + 1) * L2, t, "label2"))
    o.append(lab(s, 392, 24, "standing", anchor="end"))
    for i, t in enumerate(["COM high (0.55 H) over", "a small base: needs active", "feedback; asleep, it falls"]):
        o.append(lab(s, 392, 24 + (i + 1) * L2, t, "label2", anchor="end"))
    o.append(credit(s, VB))
    aria = ("Two side views (Lynch skeleton art). Left: a skeleton sitting on a chair; its centre of mass is low and "
            "its gravity line falls far inside a wide base of support that runs from the back of the seat to the toes, "
            "so it stays put with no active control. Right: a standing figure with the centre of mass high, at 0.55 of "
            "stature, over a foot base only 0.17 m long, which needs continuous active feedback and falls without it.")
    return finish(VB, aria, s, o)


# ================================================================ svg #28  C3 toe and heel margins
def fig28():
    p = "m7f28_"
    VB, s = VBs(360)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 220.0, 270.0
    body, J = LB.standing_full(p, s, 40.0, fy, HF)
    o.append(floor(s, 8, 120, fy, hatch=False))
    o.append(body)
    c = com_quiet(J, HF)
    o.append(H.com_mark(s, *c))
    sh = J["shoulder"]
    o.append(H.arrow(s, p, J["heel"][0] - s(26), sh[1] + s(20), J["heel"][0] + s(2), sh[1] + s(20), "load"))
    o.append(lab(s, J["heel"][0] - s(26), sh[1] + s(6), "push", "label2"))
    # zoom box on the foot
    zx0, zy0, zx1, zy1 = J["heel"][0] - s(4), fy - s(14), J["toe"][0] + s(4), fy + s(3)
    o.append(f'<rect x="{zx0:.2f}" y="{zy0:.2f}" width="{zx1 - zx0:.2f}" height="{zy1 - zy0:.2f}" fill="none" '
             f'stroke="{I["rule"]}" stroke-width="{s(1):.2f}"/>')
    # enlarged foot (foot bones only)
    Pf = LB.pose()
    HB = 1470.0
    Q = LB.Pose("lat")
    Q.__dict__.update(Pf.__dict__)
    Q.segs = [g for g in Pf.segs if g[0] == "lat_foot" and not g[5]]
    fy2 = 230.0
    xa = 192.0
    _, J0 = LB.draw(p, s, Q, 0, 0, HB)
    footb, JF = LB.draw(p, s, Q, xa - (J0["ankle"][0] - J0["heel"][0]), fy2, HB)
    cmb = cmu(JF)
    ax, ay = JF["ankle"]
    o.append(H.line(s, zx1, zy0, JF["heel"][0] - s(6), JF["bbox"][1], I["rule"], "leader"))
    o.append(H.line(s, zx1, zy1, JF["heel"][0] - s(6), fy2 + s(4), I["rule"], "leader"))
    o.append(floor(s, JF["heel"][0] - s(18), 396, fy2))
    o.append(footb)
    xh, xt, xc = ax - D_HEEL * 100 * cmb, ax + D_TOE * 100 * cmb, ax + X_COM * 100 * cmb
    o.append(H.joint_centre(s, ax, ay))
    o.append(lab(s, ax - s(4), ay - s(16), "ankle", "label2", anchor="middle"))
    o.append(ext(s, xc, 104, xc, fy2))
    o.append(lab(s, xc + s(5), 114, "gravity line", "label2"))
    o.append(lab(s, xc + s(5), 114 + s(16), "(COM 0.9 m above", "label2"))
    o.append(lab(s, xc + s(5), 114 + s(32), "the ankle)", "label2"))
    r1, r2 = fy2 + s(14), fy2 + s(42)
    for xx in (xh, xt):
        o.append(H.line(s, xx, fy2 - s(8), xx, r2 + s(4), I["axis"], "axis"))
    o.append(ext(s, ax, ay + s(8), ax, r1))
    o.append(ext(s, xc, fy2, xc, r2))
    o.append(dim_h(s, p, xh, ax, r1, f"{D_HEEL:.2f} m", below=True))
    o.append(dim_h(s, p, ax, xt, r1, f"{D_TOE:.2f} m", below=True))
    o.append(dim_h(s, p, xh, xc, r2, f"{D_HEEL + X_COM:.2f} m", below=True))
    o.append(dim_h(s, p, xc, xt, r2, f"{D_TOE - X_COM:.2f} m", below=True))
    o.append(lab(s, xh - s(4), r2 + s(32), "heel margin", "label2", anchor="start"))
    o.append(lab(s, xt + s(4), r2 + s(32), "toe margin", "label2", anchor="end"))
    o.append(lab(s, xt + s(7), r1 + s(4), "toe edge:", "label2"))
    o.append(lab(s, xt + s(7), r1 + s(4) + s(15), "balls of feet", "label2"))
    L2 = s(H.PX["label2"]) * 1.35
    for i, t in enumerate(["pushed forward: the COP can run 0.10 m", "to the toe edge, a large restoring torque;",
                           "pushed back: only 0.07 m to the heel,", "so the hip or a step is needed sooner"]):
        o.append(lab(s, 150, 18 + i * L2, t, "label2"))
    o.append(credit(s, VB))
    aria = ("Left: a standing figure (Lynch art) pushed forward, with a box around its foot. Right: the foot bones "
            "enlarged. The usable base reaches 0.12 m ahead of the ankle (the toe edge, under the balls of the feet) but "
            "only 0.05 m behind it. The gravity line falls 0.02 m ahead of the ankle, so the forward margin is 0.10 m "
            "and the backward margin 0.07 m: a forward push can be met by moving the centre of pressure far toward the "
            "toes, a backward push runs out of heel sooner.")
    return finish(VB, aria, s, o)


# ================================================================ svg #29  C4 COP trace vs COM
def run_c4():
    t, th, thd, wd = simulate(KP, KD, DCRIT, t_end=9.0)
    pk = [i for i in range(1, len(t) - 1) if th[i - 1] < th[i] >= th[i + 1]]
    n = pk[-1] + 1                                       # end at the last lean peak, where COP and COM differ most
    t, th, thd, wd = t[:n], th[:n], thd[:n], wd[:n]
    r = math.pi / 180
    x_com = ELL * th * r * 1e3                           # mm, x_com = l theta
    x_cop = (KP * thd + KD * wd) * r / (MGL / ELL) * 1e3  # mm, x_cop = tau / (Mg), Mg = Mgl / l
    return t, x_com, x_cop


def fig29():
    p = "m7f29_"
    VB, s = VBs(320)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 200.0, 224.0
    body, J = LB.standing_full(p, s, 26.0, fy, HF)
    o.append(rect(s, J["heel"][0] - s(10), fy, J["toe"][0] - J["heel"][0] + s(20), s(8)))
    o.append(body)
    c = com_quiet(J, HF)
    o.append(ext(s, c[0], c[1] + s(8), c[0], fy - s(2)))
    o.append(H.com_mark(s, *c))
    o.append(H.arrow(s, p, c[0], fy + s(40), c[0], fy + s(8), "reaction"))
    o.append(lab(s, c[0] + s(6), fy + s(36), f'{it("N")} at COP', "label2"))
    o.append(lab(s, 6, fy + s(22), "force plate", "label2"))
    t, xc, xp = run_c4()
    pl = Plot(s, (150, 52, 356, 206), (0, t[-1]), (-16, 16))
    o.append(pl.axes([(v, f"{v:g}") for v in (0, 2, 4, 6, 8)], [(v, f"{v:g}".replace("-", "−")) for v in (-15, 0, 15)],
                     "time (s)", "forward position (mm)", grid=(0,), ytx=112))
    o.append(pl.curve(t, xp, SER[1], multi=True, nmax=100))
    o.append(pl.curve(t, xc, I["primary"], multi=True, nmax=100))
    late = t > 3.0
    ratio = (xp[late].max() - xp[late].min()) / (xc[late].max() - xc[late].min())
    close(ratio, 1 + WC ** 2 / W0 ** 2, 0.01)
    o.append(legend(s, 150, 18, [(SER[1], "COP = τ/Mg", None), (I["primary"], "COM = ℓθ", None)]))
    o.append(plabel(s, pl.X(t[-1]) + s(6), pl.Y(xp[-1]) + s(4), "COP", "label2"))
    o.append(plabel(s, pl.X(t[-1]) + s(6), pl.Y(xc[-1]) + s(4), "COM", "label2"))
    o.append(plabel(s, 150, 40, f"COP swing = {ratio:.2f} × COM swing (0.35 Hz)", "label2", I["secondary"]))
    idx = list(range(0, len(t), 40))
    pts = [[pl.X(t[i]), [pl.Y(xc[i]), pl.Y(xp[i])], f"t {t[i]:.2f} s: COM {xc[i]:.1f} mm, COP {xp[i]:.1f} mm"]
           for i in idx]
    o.append(credit(s, VB))
    aria = ("Left: a standing figure (Lynch art) on a force plate; the plate measures the centre of pressure, where the "
            "upward ground force N acts, not the centre of mass. Right: the lean of the delayed-feedback model of "
            "section 6 (K_p = 900, K_d = 120, delay 0.13 s) over 8 s: the centre of pressure (blue) swings 1.52 times "
            "wider than the centre of mass (black) and starts ahead of it, because it is the controller's output, the "
            "ankle torque divided by body weight.")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ svg #30  C5 cadaver vs living ankle
def fig30():
    p = "m7f30_"
    VB, s = VBs(300)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    pl = Plot(s, (62, 62, 380, 222), (0, 1000), (0, 3.5))
    x0, y0, x1, y1 = pl.X(MGL), pl.Y(3.5), pl.X(1000), pl.Y(0)
    o.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}" fill="{O["neural"]}" '
             f'fill-opacity="0.09"/>')
    o.append(pl.axes([(v, f"{v:g}") for v in (0, 200, 400, 600, 800, 1000)], [(v, f"{v:g}") for v in (0, 1, 2, 3)],
                     "ankle stiffness K (N·m/rad)", "growth rate s₊ (1/s)", grid=(1, 2, 3)))
    ks = np.linspace(0, MGL, 200)
    sp = np.sqrt((MGL - ks) / I_A)
    o.append(pl.curve(ks, sp, SER[0], nmax=100))
    o.append(H.line(s, pl.X(MGL), pl.Y(3.5), pl.X(MGL), pl.Y(0), I["secondary"], "ref", H.DASH_REF))
    s_cad = math.sqrt((MGL - K_INT) / I_A)
    o.append(pl.dot(0, W0, SER[0]))
    o.append(pl.dot(K_INT, s_cad, SER[2]))
    o.append(pl.dot(KP, 0, O["neural"]))
    o.append(plabel(s, pl.X(0) + s(8), pl.Y(W0) - s(12), f'no stiffness: {omega(s)} = {W0:.2f}/s', "label2"))
    o.append(plabel(s, pl.X(K_INT) - s(16), pl.Y(s_cad) + s(6), f"cadaver: 0.9 Mgℓ = {K_INT:.0f}", "label2",
                    anchor="end"))
    o.append(plabel(s, pl.X(K_INT) - s(16), pl.Y(s_cad) + s(22), f"s₊ = {s_cad:.2f}/s: still falls", "label2",
                    anchor="end"))
    o.append(plabel(s, pl.X(MGL) + s(5), pl.Y(3.5) + s(14), f"Mgℓ = {MGL:.0f}", "label2"))
    o.append(plabel(s, pl.X(KP), pl.Y(0) - s(12), f"living: K = {KP:.0f}", "label2", anchor="middle"))
    o.append(plabel(s, pl.X(820), pl.Y(2.6), "stable:", "label2", anchor="middle"))
    o.append(plabel(s, pl.X(820), pl.Y(2.6) + s(15), "K > Mgℓ", "label2", anchor="middle"))
    o.append(plabel(s, 10, 20, "Stability needs K > Mgℓ (Prop. 5.1). Passive stiffness", "label2"))
    o.append(plabel(s, 10, 20 + s(17), "alone, 0.9 Mgℓ, leaves a growing root; muscle adds the rest.", "label2"))
    pts = [[pl.X(k), pl.Y(v), f"K {k:.0f} N·m/rad: s+ {v:.2f} 1/s"] for k, v in zip(ks, sp)]
    pts += [[pl.X(k), pl.Y(0), f"K {k:.0f} N·m/rad: stable (no growing root)"] for k in np.linspace(630, 1000, 30)]
    aria = ("Growth rate of the toppling mode, s+ = sqrt((Mgl - K)/I), against ankle stiffness K with no damping. At "
            "K = 0 it is omega0 = 3.06 per second; the cadaver's passive stiffness, 0.9 Mgl = 556 N m/rad (orange), "
            "still leaves s+ = 0.97 per second, so the body falls; the root reaches zero only at K = Mgl = 618 "
            "(dashed). The shaded region K > Mgl is stable; the living ankle reaches it, for example K = 900, by "
            "adding active muscle stiffness.")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ svg #31  C6 sway is the controller working
def fig31():
    p = "m7f31_"
    VB, s = VBs(380)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    hv = []
    for k, (kp, kd, wc, dc, col, box) in enumerate(((KP, KD, WC, DCRIT, SER[0], (58, 40, 380, 150)),
                                                    (KP1, KD1, WC1, DCRIT1, SER[1], (58, 200, 380, 310)))):
        t, th, _, _ = simulate(kp, kd, dc, t_end=10.0)
        pl = Plot(s, box, (0, 10), (-0.8, 1.6))
        xt = [(v, f"{v:g}") for v in (0, 2, 4, 6, 8, 10)] if k == 1 else [(v, "") for v in (0, 2, 4, 6, 8, 10)]
        ax = pl.axes(xt, [(v, f"{v:g}".replace("-", "−")) for v in (-0.6, 0, 0.6)],
                     "time (s)" if k == 1 else "", "lean (°)", grid=(0,), ytx=14)
        o.append(ax)
        o.append(pl.curve(t, th, col, nmax=100))
        pk = [i for i in range(1, len(t) - 1) if th[i] > th[i - 1] and th[i] >= th[i + 1] and t[i] > 2.5]
        t1, t2 = t[pk[1]], t[pk[2]]
        per = t2 - t1
        close(1 / per, wc / (2 * math.pi), 0.005)
        yy = pl.Y(0.82)
        o.append(H.line(s, pl.X(t1), pl.Y(th[pk[1]]) - s(4), pl.X(t1), yy - s(4), O["dim"], "leader"))
        o.append(H.line(s, pl.X(t2), pl.Y(th[pk[2]]) - s(4), pl.X(t2), yy - s(4), O["dim"], "leader"))
        o.append(H.arrow(s, p, pl.X(t1), yy, pl.X(t2), yy, "geometry", both=True))
        o.append(plabel(s, (pl.X(t1) + pl.X(t2)) / 2, yy - s(6), f"period {per:.2f} s: {1 / per:.2f} Hz", "label2",
                        anchor="middle"))
        o.append(H.line(s, box[0] + s(6), box[1] + s(10), box[0] + s(26), box[1] + s(10), col, "curve"))
        o.append(plabel(s, box[0] + s(32), box[1] + s(15), f'{it("K")}{sub("p", s, "label2")} = {kp:.0f}, '
                        f'{it("K")}{sub("d", s, "label2")} = {kd:.0f}, delay {dc * 1e3:.0f} ms', "label2"))
        hv.append((pl.box, [[pl.X(t[i]), pl.Y(th[i]), f"t {t[i]:.2f} s: lean {th[i]:.3f}°"]
                            for i in range(0, len(t), 50)]))
    o.append(plabel(s, 200, 372, "one sharp frequency, shifted by the gains as Prop. 6.3 predicts", "label2",
                    I["secondary"], "middle"))
    aria = ("Two runs of the delayed-feedback standing model of section 6, each at its critical delay (130 ms), started "
            "from a 0.6 degree lean. Top (red): K_p = 900, K_d = 120; the lean settles into a steady sway with period "
            "2.85 s, 0.35 Hz. Bottom (blue): stiffer gains K_p = 1100, K_d = 150; period 2.14 s, 0.47 Hz. Each sway sits "
            "at one definite frequency that the gains set, as the quartic of Proposition 6.3 predicts; noise would have "
            "no such frequency.")
    return finish(VB, aria, s, o, extra=H.hover_attr(hv))


# ================================================================ svg #32  C7 ankle strategy vs hip strategy on a beam
BEAM_W, BEAM_H = 0.06, 0.12              # m, design choice (the text gives no beam size)


def hip_pose(hip):
    return LB.pose(pelvis=25, near=dict(hip=hip, shoulder=25, elbow=10), far=dict(hip=hip, shoulder=25, elbow=10))


def fig32():
    p = "m7f32_"
    VB, s = VBs(470)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 250.0, 362.0
    o.append(floor(s, 8, 392, fy))
    # ---- ankle strategy on the ground: rigid lean of 2 deg about the ankle
    P = LB.pose(pelvis=2, near=dict(hip=0), far=dict(hip=0))
    body, J = LB.draw(p, s, P, 50.0, fy, HF)
    cm = cmu(J)
    o.append(body)
    ax = J["ankle"][0]
    c = J["com"]
    xcop = ax + 0.09 * 100 * cm
    o.append(ext(s, c[0], c[1] + s(8), c[0], fy))
    o.append(H.com_mark(s, *c))
    o.append(H.arrow(s, p, xcop, fy + s(40), xcop, fy, "reaction"))
    o.append(lab(s, xcop + s(5), fy + s(36), f'{it("N")} at COP', "label2"))
    # ---- hip strategy on a beam; hip solved so the whole-body COM is over the beam centre
    bh = BEAM_H * 100 * CM * HF / LB.H_U
    by = fy - bh

    def place(hip):
        Pq = hip_pose(hip)
        _, Jq = LB.draw(p, s, Pq, 0, by, HF)
        return Pq, Jq

    def gap(hip):
        Pq, Jq = place(hip)
        return Jq["com"][0] - (Jq["ankle"][0] + X_COM * 100 * cmu(Jq))
    hip = bisect(gap, 25.0, 70.0)
    P2, J2 = place(hip)
    dx = 290.0 - J2["heel"][0]
    body2, J2 = LB.draw(p, s, P2, dx, by, HF)
    cm2 = cmu(J2)
    xb_c = J2["ankle"][0] + X_COM * 100 * cm2
    bw = BEAM_W * 100 * cm2
    o.append(rect(s, xb_c - bw / 2, by, bw, bh))
    o.append(body2)
    c2 = J2["com"]
    o.append(ext(s, c2[0], c2[1] + s(8), c2[0], by))
    o.append(H.com_mark(s, *c2))
    xe = xb_c + bw / 2
    o.append(H.arrow(s, p, xe, fy + s(40), xe, by, "reaction"))
    o.append(H.arrow(s, p, xe + s(2), by - s(4), xe - s(34), by - s(4), "reaction"))
    o.append(lab(s, xe - s(36), by - s(10), it("H"), "label2", anchor="end"))
    o.append(lab(s, xe - s(5), fy + s(36), f'{it("N")}: COP at beam edge', "label2", anchor="end"))
    trunk_mid = LB.lerp(J2["l5s1"], J2["shoulder"], 0.55)
    rr = math.dist(J2["hip"], trunk_mid)
    o.append(arc(s, p, J2["hip"][0], J2["hip"][1], rr, -100, -45, "force"))
    ta = math.radians(-100)
    o.append(lab(s, J2["hip"][0] + rr * math.cos(ta) - s(6), J2["hip"][1] + rr * math.sin(ta) - s(4), "trunk swings",
                 "label2", anchor="end"))
    L2 = s(H.PX["label2"]) * 1.35
    tau_g = M * G * D_TOE                                 # Prop 7.1 with the toe edge
    tau_b = M * G * (X_COM + BEAM_W / 2)                  # beam front edge, measured from the ankle
    for i, t in enumerate(["solid ground: ankle strategy", "COP moves within the foot,",
                           f'|{it("τ")}| ≤ {it("Mg")}·{it("d")}{sub("toe", s, "label2")} ≈ {tau_g:.0f} N·m']):
        o.append(lab(s, 10, 20 + i * L2, t, "label2"))
    for i, t in enumerate([f"beam {BEAM_W * 100:.0f} cm wide: hip strategy", f"COP range only {BEAM_W * 100:.0f} cm,",
                           f'|{it("τ")}| ≤ {tau_b:.0f} N·m: ankle saturates;', f"trunk rotation makes shear {it('H')}"]):
        o.append(lab(s, 392, 20 + i * L2, t, "label2", anchor="end"))
    o.append(credit(s, VB))
    aria = ("Two side views (Lynch skeleton art). Left, solid ground: the body leans as one piece about the ankle and "
            "the centre of pressure moves within the foot, whose base reaches 0.12 m ahead of the ankle, so the ankle "
            f"torque can reach Mg times 0.12 m, about {tau_g:.0f} N m. Right, on a 6 cm beam (an assumed width): the "
            f"centre of pressure can move only 6 cm and the ankle torque tops out near {tau_b:.0f} N m, so the ankle "
            "saturates and the body bends at the hip; the fast trunk rotation "
            "(red arc) makes a backward horizontal ground force H at the beam (black) that brakes the centre of mass "
            "with no further centre-of-pressure travel.")
    return finish(VB, aria, s, o)


# ================================================================ svg #33  C8 co-contraction on ice
def fig33():
    p = "m7f33_"
    VB, s = VBs(400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    Pf = LB.pose()
    Q = LB.Pose("lat")
    Q.__dict__.update(Pf.__dict__)
    Q.segs = [g for g in Pf.segs if g[0] in ("lat_shank", "lat_foot") and not g[5]]   # near shank + foot only
    HB, fy = 760.0, 262.0
    leg, J = LB.draw(p, s, Q, 22.0, fy, HB)
    cm = cmu(J)
    o.append(f'<rect x="8" y="{fy:.2f}" width="{J["toe"][0] + s(14) - 8:.2f}" height="{s(7):.2f}" '
             f'fill="{T["fluid"][0]}" stroke="{T["fluid"][1]}" stroke-width="{s(0.8):.2f}"/>')
    o.append(lab(s, J["toe"][0] + s(4), fy + s(22), "ice", "label2", anchor="end"))
    o.append(leg)
    ax, ay = J["ankle"]
    hx = J["heel"][0]
    P0 = lambda xc, h: (hx + xc * cm, fy - h * cm)   # noqa: E731  (cm from the heel, height above the floor)
    calf0, calf1 = P0(0.6, 4.5), P0(1.6, 21.0)       # calcaneal tuberosity -> up the Achilles line
    shin0, shin1 = P0(12.0, 5.5), P0(9.5, 19.0)      # first cuneiform -> up the front of the tibia
    o.append(H.arrow(s, p, *calf0, *calf1, "force"))
    o.append(H.arrow(s, p, *shin0, *shin1, "force"))
    o.append(H.joint_centre(s, ax, ay))
    o.append(lab(s, calf1[0] - s(4), calf1[1] - s(8), f'calf: {it("T")}{sub("a", s)}, {it("k")}{sub("a", s)}', "label2"))
    o.append(lab(s, shin1[0] + s(10), shin1[1] + s(12), f'shin: {it("T")}{sub("b", s)}, {it("k")}{sub("b", s)}',
                 "label2"))
    # ---- price of stiffness (module numbers, K8): bars of K_p = Mgl + active part
    pl = Plot(s, (262, 60, 380, 236), (0, 2), (0, 800))
    o.append(pl.axes([(0.5, "σ = 1/s"), (1.5, "σ = 2/s")], [(v, f"{v:g}") for v in (0, 200, 400, 600, 800)],
                     "recovery rate", "", grid=(200, 400, 600, 800)))
    o.append(plabel(s, 214, 46, f'cost ∝ {it("K")}{sub("p", s)} (N·m/rad)', "label2"))
    pts = []
    bw = s(34)
    for i, (sig, kp) in enumerate(K8):
        xc = pl.X(0.5 + i)
        o.append(f'<rect x="{xc - bw / 2:.2f}" y="{pl.Y(MGL):.2f}" width="{bw:.2f}" height="{pl.Y(0) - pl.Y(MGL):.2f}" '
                 f'fill="#e6e6e6" stroke="{I["rule"]}" stroke-width="{s(0.8):.2f}"/>')
        o.append(f'<rect x="{xc - bw / 2:.2f}" y="{pl.Y(kp):.2f}" width="{bw:.2f}" height="{pl.Y(MGL) - pl.Y(kp):.2f}" '
                 f'fill="{SER[0]}"/>')
        o.append(plabel(s, xc, pl.Y(kp) - s(5), f"{kp:.0f}", "label2", anchor="middle"))
        o.append(plabel(s, xc, pl.Y(MGL / 2) + s(4), "Mgℓ", "label2", anchor="middle"))
        pts.append([xc, pl.Y(kp), f"rate {sig:g}/s: Kp {kp:.0f} = Mgl {MGL:.0f} + active {kp - MGL:.0f} N·m/rad"])
    rise = K8[1][1] / K8[0][1] - 1
    act = (K8[1][1] - MGL) / (K8[0][1] - MGL)
    close(rise, 0.11, 0.005)                    # "only about 11 %" (line 878)
    close(act, 2.7, 0.05)                       # "a factor of 2.7" (line 878)
    L2 = s(H.PX["label2"]) * 1.35
    yb = 300
    o.append(lab(s, 10, yb, f'net torque {it("T")}{sub("a", s, "label2")} − {it("T")}{sub("b", s, "label2")}: unchanged; '
                 f'stiffness {it("K")}{sub("p", s, "label2")} = {it("k")}{sub("a", s, "label2")} + '
                 f'{it("k")}{sub("b", s, "label2")}: up', "label2"))
    o.append(lab(s, 10, yb + L2, f"doubling σ (K8, 0.15 s delay): red part ×{act:.1f},", "label2"))
    o.append(lab(s, 10, yb + 2 * L2, f"total activation, which sets the cost, +{rise * 100:.0f} %",
                 "label2"))
    o.append(credit(s, VB))
    aria = ("Left: Lynch shank and foot bones standing on ice, with two red muscle-force arrows: the calf pulling up on "
            "the heel (torque T_a, stiffness k_a) and the shin muscle pulling up on the top of the foot (T_b, k_b). "
            "Their torques subtract, so the net ankle torque is unchanged, but their stiffnesses add, K_p = k_a + k_b. "
            "Right: the price, from problem K8 at the 0.15 s delay: a recovery rate of 1 per second needs K_p = 660 "
            "N m/rad, 2 per second needs 732; the part above Mgl = 618 (red) grows 2.7 times while the total "
            "activation, which sets the metabolic cost, grows 11 percent.")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ svg #34  C9 locked vs soft knees
KNEE_LOCK, KNEE_SOFT = -5.0, 20.0       # deg; locked = 5 deg hyperextension at the stop (design choice)


def knee_pose(knee, lean=0.0, hip=0.0):
    leg = dict(knee=knee, hip=hip)
    return LB.pose(pelvis=lean, near=dict(leg), far=dict(leg))


def com_ahead(P):
    _, J = LB.draw("x", H.Scale(400, 400), P, 0, 0, LB.H_U)
    return (J["com"][0] - J["ankle"][0]) / CM, (J["com"][0] - J["knee"][0]) / CM


LEAN_LOCK = bisect(lambda a: com_ahead(knee_pose(KNEE_LOCK, lean=a))[0] - X_COM * 100, -5.0, 5.0)
HIP_SOFT = bisect(lambda h: com_ahead(knee_pose(KNEE_SOFT, hip=h))[0] - X_COM * 100, 0.0, 15.0)
OFF_LOCK = com_ahead(knee_pose(KNEE_LOCK, lean=LEAN_LOCK))[1]
OFF_SOFT = com_ahead(knee_pose(KNEE_SOFT, hip=HIP_SOFT))[1]
assert OFF_LOCK > 0 > OFF_SOFT, (OFF_LOCK, OFF_SOFT)


def fig34():
    p = "m7f34_"
    VB, s = VBs(485)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 270.0, 352.0
    o.append(floor(s, 8, 392, fy))
    L2 = s(H.PX["label2"]) * 1.35
    for k, (P, x, title, lines) in enumerate((
            (knee_pose(KNEE_LOCK, lean=LEAN_LOCK), 70.0, "locked knee",
             [f"weight line {OFF_LOCK:.1f} cm in front", "of the knee: ligaments carry", "it, quadriceps relax"]),
            (knee_pose(KNEE_SOFT, hip=HIP_SOFT), 262.0, "soft knee",
             [f"weight line {-OFF_SOFT:.1f} cm behind", "the knee: quadriceps", "must hold it"]))):
        body, J = LB.draw(p, s, P, x, fy, HF)
        o.append(body)
        c = J["com"]
        o.append(H.line(s, c[0], c[1] + s(8), c[0], fy - s(2), O["reaction"], "ref", H.DASH_LOA))
        o.append(H.arrow(s, p, c[0], fy + s(40), c[0], fy, "reaction"))
        o.append(H.com_mark(s, *c))
        o.append(H.joint_centre(s, *J["knee"]))
        if k == 1:
            tt = J["knee"][0] + 1.5 * cmu(J), J["knee"][1] + 7.0 * cmu(J)       # tibial tuberosity
            th = LB.lerp(J["knee"], J["hip"], 0.6)
            o.append(H.arrow(s, p, tt[0], tt[1], th[0] + 4.5 * cmu(J), th[1], "force"))
        xt = 10 if k == 0 else 392
        anc = "start" if k == 0 else "end"
        o.append(lab(s, xt, 22, title, anchor=anc))
        for i, t in enumerate(lines):
            o.append(lab(s, xt, 22 + (i + 1) * L2, t, "label2", anchor=anc))
    o.append(lab(s, 200, fy + s(54), "locked: no muscle cost, but no small knee corrections;", "label2", anchor="middle"))
    o.append(lab(s, 200, fy + s(54) + L2, "soft: costs effort, keeps the control loop and circulation working",
                 "label2", anchor="middle"))
    o.append(credit(s, VB))
    aria = (f"Two side views (Lynch skeleton art), each with its centre of mass 2 cm ahead of the ankle and the "
            f"vertical ground-reaction line through it. Left, locked knee (at its extension stop, 5 degrees past "
            f"straight): the line passes {OFF_LOCK:.1f} cm in front of the knee centre, so the ligaments carry the "
            f"moment and the quadriceps relax. Right, soft knee ({KNEE_SOFT:.0f} degrees bent): the line passes {-OFF_SOFT:.1f} cm "
            f"behind the knee, so the quadriceps (red arrow) must pull continuously; that costs energy but keeps the "
            f"small corrections and the muscle pump working.")
    return finish(VB, aria, s, o)


# ================================================================ svg #35  C10 the stoop-lift low-back lever
TRUNK_TILT = math.degrees(math.atan2(-LB.OFF["lat_trunk"]["neck"][0], -LB.OFF["lat_trunk"]["neck"][1]))
PEL10 = 55.0                            # pelvis tilt; lumbar flexion = the rest of phi (design split)


def stoop(hip, shoulder):
    th_t = 90.0 + TRUNK_TILT            # L5/S1 -> C7 axis horizontal: phi = 90 deg (line 601)
    arm = dict(hip=hip, shoulder=shoulder, elbow=0, wrist=0)
    return LB.pose(pelvis=PEL10, trunk=th_t - PEL10, near=dict(arm), far=dict(arm))


def fig35():
    p = "m7f35_"
    VB, s = VBs(350)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 360.0, 300.0
    th_t = 90.0 + TRUNK_TILT

    def grip(J):
        return LB.lerp(J["wrist"], J["fingertip"], 0.4)

    def build(hip, sh, x=0.0):
        P = stoop(hip, sh)
        return P, LB.draw(p, s, P, x, fy, HF)

    def reach_err(sh, hip):
        _, (_, J) = build(hip, sh)
        return (grip(J)[0] - J["l5s1"][0]) / cmu(J) - RL * 100

    def com_err(hip):
        sh = bisect(lambda a: reach_err(a, hip), th_t - 30, th_t + 30)
        P, (_, J) = build(hip, sh)
        cm = cmu(J)
        g = grip(J)
        cx, _ = whole_com(J, P, [((g[0], g[1] + 6 * cm), ML / M)])
        return cx - (J["ankle"][0] + 4.0 * cm)           # body + load over the mid-foot, 4 cm ahead of the ankle
    hip = bisect(com_err, PEL10 + 0.0, PEL10 + 40.0)
    sh = bisect(lambda a: reach_err(a, hip), th_t - 30, th_t + 30)
    P, (_, J0) = build(hip, sh)
    dx = 40.0 - J0["bbox"][0]
    P, (body, J) = build(hip, sh, dx)
    cm = cmu(J)
    g = grip(J)
    cx_all, _ = whole_com(J, P, [((g[0], g[1] + 6 * cm), ML / M)])
    assert J["heel"][0] <= cx_all <= J["toe"][0]          # COM over the feet (line 570)
    o.append(floor(s, 8, 392, fy))
    o.append(body)
    lx, ly = J["l5s1"]
    xt, xl = lx + RT * 100 * cm, lx + RL * 100 * cm
    bwid, bht = 0.24 * 100 * cm, 0.16 * 100 * cm
    o.append(rect(s, xl - bwid / 2, g[1] - s(2), bwid, bht))
    yt = ly + 1.0 * cm                                     # trunk COM on the L5/S1 - C7 axis
    o.append(H.com_mark(s, xt, yt))
    o.append(H.arrow(s, p, xt, yt + s(7), xt, yt + s(7) + s(34), "load"))
    o.append(lab(s, xt + s(6), yt + s(36), f'{it("m")}{sub("t", s, "label2")}{it("g")} = {MT * G:.0f} N', "label2"))
    yl = g[1] + bht / 2
    o.append(H.arrow(s, p, xl, yl, xl, yl + s(40), "load"))
    o.append(lab(s, xl - s(6), yl + s(40), f'{it("m")}{sub("L", s, "label2")}{it("g")} = {ML * G:.0f} N', "label2",
                 anchor="end"))
    # erector spinae line, d dorsal (above) the L5/S1 centre; disc compression at L5/S1
    de = DE * 100 * cm
    ye = ly - de
    o.append(H.arrow(s, p, lx + s(70), ye, lx + s(4), ye, "force"))
    o.append(H.arrow(s, p, lx - s(52), ly, lx - s(7), ly, "reaction"))
    o.append(H.joint_centre(s, lx, ly))
    xd = lx - s(12)
    o.append(H.line(s, xd - s(4), ye, lx, ye, O["dim"], "ref", H.DASH_REF))
    o.append(H.arrow(s, p, xd, ye - s(14), xd, ye, "geometry"))
    o.append(H.arrow(s, p, xd, ly + s(14), xd, ly, "geometry"))
    o.append(lab(s, xd - s(2), ly + s(17), f'{it("d")} ≈ 0.05 m', "label2", anchor="end"))
    o.append(lab(s, lx + s(72), ye + s(4), f'erector spinae {it("F")}{sub("e", s, "label2")}', "label2"))
    o.append(lab(s, lx - s(66), ly + s(34), "disc compression", "label2"))
    o.append(lab(s, lx - s(66), ly + s(34) + s(15), "at L5/S1", "label2"))
    # load arms above the back
    ytop = J["bbox"][1]
    r1, r2 = ytop - s(10), ytop - s(36)
    o.append(ext(s, lx, ly - s(10), lx, r2 - s(6)))
    for xx, rr in ((xt, r1), (xl, r2)):                   # trunk COM and load lines, drawn above the back only
        o.append(ext(s, xx, ytop, xx, rr - s(6)))
    for rr, txt in ((r1, f'{it("r")}{sub("t", s, "label2")} = {RT:.2f} m'), (r2, f'{it("r")}{sub("L", s, "label2")} = '
                                                                               f'{RL:.2f} m')):
        o.append(H.arrow(s, p, lx, rr, xt if rr == r1 else xl, rr, "geometry", both=True))
        o.append(lab(s, lx - s(6), rr + s(4), txt, "label2", anchor="end"))
    L2 = s(H.PX["label2"]) * 1.35
    xb, yb = 250, fy - s(96)
    for i, t in enumerate([f'{it("M")} = {it("g")}({it("m")}{sub("t", s, "label2")}{it("r")}{sub("t", s, "label2")} + '
                           f'{it("m")}{sub("L", s, "label2")}{it("r")}{sub("L", s, "label2")})',
                           f"= {M_L5:.0f} N·m",
                           f'{it("F")}{sub("spine", s, "label2")} ≈ {it("M")}/{it("d")} ≈ {F_SP / 1e3:.1f} kN',
                           f"= {F_SP / (M * G):.1f} × body weight,", f"above the {LIMIT / 1e3:.1f} kN risk line",
                           "(arrows not to scale)"]):
        o.append(lab(s, xb, yb + i * L2, t, "label2", I["secondary"] if i == 5 else I["primary"]))
    o.append(credit(s, VB))
    aria = ("Side view of a skeleton (Lynch art) stoop-lifting with straight knees, the trunk horizontal and a 20 kg "
            "box hanging from the hands. The L5/S1 disc is the pivot. The trunk weight m_t g = 343 N acts r_t = 0.30 m "
            "ahead of it and the load m_L g = 196 N acts r_L = 0.40 m ahead; the erector spinae (red) pull on an arm "
            "of only d = 0.05 m above the disc. The moment M = 181 N m therefore needs an erector force of about "
            "3.6 kN, 5.3 times body weight, which presses on the disc (black): more than the 3.4 kN risk threshold.")
    return finish(VB, aria, s, o)


FIGS = {
    26: ("C1: A juggler balances a broomstick upright on one palm; a p", fig26),
    27: ("C2: Why can you doze off sitting in a chair but not standing", fig27),
    28: ("C3: Pushed gently forward, you rise onto the balls of your f", fig28),
    29: ("C4: A clinician reads only the centre-of-pressure trace from", fig29),
    30: ("C5: A cadaver ankle has nearly the same passive stiffness as", fig30),
    31: ("C6: Two students argue: one says quiet-standing sway is 'mot", fig31),
    32: ("C7: Standing on a narrow beam, you feel your hips start to j", fig32),
    33: ("C8: Stepping onto an icy patch, you instinctively stiffen — ", fig33),
    34: ("C9: A soldier told to stand at attention for a long time is ", fig34),
    35: ("C10 low-back lever: a person stoop-lifting a load, bent forw", fig35),
}
