"""Module 10, group `body_d`: derivational problems D1-D10 (svg #28-#37), house style, 400 px.

Bodies are the posable Lynch skeleton (lynch_body.py); m10/body_main.py puts its defs on the page, this group only
<use>s them (it exposes no SHARED_DEFS).  Stature 1.75 m (the text states none).  Every number on a figure is computed
here from the formula, constant or lab code the module states; the line numbers (module10.html) stand beside it:
  m = 70 kg, l = 1.0 m, omega0 = 3.1 1/s (the text rounds sqrt(g/l) to 3.1: lines 106, 136, 208, 558), b = 0.10 m,
  J_max = m omega0 b = 21.7 = 22 N s (106, 558); k_p = 20, k_d = 3 (136, 208); poles -1.5 +- 2.85 i (136);
  tau_c = 137 ms, marginal Omega = 3.6 rad/s (208, 210, 570); q = 2.2e-3 rad^2 s^-3 and sigma = 0.34 deg (232, 234);
  Lab C: tau = 0.10 s (449); K8: 40 N s push, t_step = 0.30 s, reach 0.60 m, xi_s = 0.467 m (746); walking speed
  1.4 m/s (106); mu_req = 0.20 (764; appendix 0.17-0.22, 862), mu_avail = 0.08 on ice (764).
"""
import math

import numpy as np

import house as H
import lynch_body as LB
from m05.body import finish, it
from m05.plots_prob import Plot, label as plabel, legend

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
BOX, GRID = "#f7f4ef", "#e6e6e6"
H_M = 1.75                                   # m, stature (design value; the text states none)
UM = LB.H_U / H_M                            # body units per metre


def close(v, ref, tol):
    assert abs(v - ref) <= tol * 1.0001, (v, ref)


# ---------------------------------------------------------------- numbers module10.html states
G, M, ELL = 9.81, 70.0, 1.0
W0 = 3.1                                     # 1/s (line 106: sqrt(9.81/1.0) = 3.13, written 3.1 throughout)
B_REST = 0.10                                # m (line 106)
COM_AHEAD, D_TOE, D_HEEL = 0.02, 0.12, 0.05  # m from the ankle: COM, toe edge, heel edge (Module 7 line 176; b = 0.10)
KP, KD = 20.0, 3.0                           # s^-2, s^-1 (line 136)
Q = 2.2e-3                                   # rad^2 s^-3 (line 234)
TAU_C = 0.10                                 # s, Lab C reaction delay (line 449)
V_WALK = 1.4                                 # m/s (line 106)
MU_REQ, MU_ICE = 0.20, 0.08                  # lines 764, 762
J_K8, T_STEP, L_STEP = 40.0, 0.10 + 0.20, 0.60   # N s, s, m (K8 solution, line 746; Lab D young set)
A0 = KP - W0 ** 2                            # 10.39 s^-2 (line 134: s^2 + k_d s + (k_p - omega0^2))

J_MAX = M * W0 * B_REST
close(J_MAX, 21.7, 0.05)                     # lines 106, 397 (21.7; the text rounds to 22)
_pole = np.roots([1, KD, A0])
close(_pole[0].real, -1.5, 1e-9)
close(abs(_pole[0].imag), 2.85, 0.005)       # line 136
_a = 2 * W0 ** 2 - KD ** 2
_O2 = (-_a + math.sqrt(_a * _a - 4 * (W0 ** 4 - KP ** 2))) / 2     # Omega^2 at the k_p = 20 crossing
OMEGA_C = math.sqrt(_O2)
TAU_CRIT = math.asin(KD * OMEGA_C / (_O2 + W0 ** 2)) / OMEGA_C     # Prop 4.2, k_p = 20, k_d = 3
close(TAU_CRIT, 0.137, 0.0005)               # lines 208, 570
close(OMEGA_C, 3.6, 0.05)                    # line 210
VAR_TH = Q / (2 * A0 * KD)                   # Prop 5.1 (line 225)
SIG_RAD = math.sqrt(VAR_TH)
SIG_DEG = math.degrees(SIG_RAD)
close(SIG_DEG, 0.34, 0.005)                  # lines 232, 234
VAR_RATE = Q / (2 * KD)
XI_PLUS = J_K8 / (M * W0)                    # xi right after the impulse (Definition 6, line 336)
XI_S = XI_PLUS * math.exp(W0 * T_STEP)       # xi at touchdown (line 746)
close(XI_S, 0.467, 0.0005)
X_S = XI_PLUS * math.sinh(W0 * T_STEP)       # COM position at touchdown (x = xi+ sinh(w t))
V_S = W0 * XI_PLUS * math.cosh(W0 * T_STEP)  # COM velocity at touchdown
close(X_S + V_S / W0, XI_S, 1e-9)
DELTA = 0.08                                 # m, capture margin drawn (the text fixes none; window 0..0.133 m, line 746)
close(L_STEP - XI_S, 0.133, 0.0005)
FOOT_M = (LB.LJ["toe"][0] - LB.LJ["heel"][0]) / LB.H_U * H_M       # heel to toe, m
close(V_WALK / W0, 0.45, 0.005)              # D10: delta xi = v/omega0 (line 313)


# ---------------------------------------------------------------- drawing helpers
def defs(p, s):
    return f"<defs>{H.markers(p, s)}</defs>"


def lab(s, x, y, text, size="label2", fill=I["primary"], anchor="start", extra=""):
    return H.label(s, x, y, text, size, fill, anchor, extra)


def lines(s, x, y, rows, size="label2", anchor="start", fill=None):
    d = s(H.PX[size]) * 1.35
    return "".join(lab(s, x, y + i * d, t, size, fill or I["primary"], anchor) for i, t in enumerate(rows))


def sup(t, s, size="label2"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def sb(t, s, size="label2"):
    return H.sub(t, s, size)


def accent(c, mark, dx, dy):
    """Italic letter with a spacing modifier drawn over it (Georgia has no combining marks in the SVG text path)."""
    return (f'<tspan font-style="italic">{c}</tspan><tspan dx="{dx}em" dy="{dy}em" font-style="normal">{mark}</tspan>'
            f'<tspan dy="{-dy}em">\u200a</tspan>')


def hat(c):
    return accent(c, "\u02c6", -0.5, 0.0)


def dot_(c):
    return accent(c, "\u02d9", -0.45, -0.2 if c == "θ" else -0.1)


def white_under(s, x1, y1, x2, y2, w=4):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#fff" '
            f'stroke-width="{s(w):.2f}" opacity="0.85"/>')


def vline(s, x, y1, y2, col=None, dash=H.DASH_REF, w="ref"):
    """Dashed reference line with a white under-stroke so it reads over the art."""
    return white_under(s, x, y1, x, y2) + H.line(s, x, y1, x, y2, col or O["dim"], w, dash=dash)


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


class Frame:
    """Metres from the near ankle -> figure units, for one body drawn with stature `hgt`."""

    def __init__(self, J, hgt):
        self.ax, self.ay, self.fy = J["ankle"][0], J["ankle"][1], J["floor_y"]
        self.k = hgt / H_M

    def x(self, m):
        return self.ax + self.k * m


def body_at(p, s, P, ank_x, fy, hgt, key="ankle"):
    """Draw pose P with its `key` joint at x = ank_x, floor at fy. Returns (svg, J)."""
    _, J0 = LB.draw(p, s, P, 0.0, fy, hgt)
    return LB.draw(p, s, P, ank_x - J0[key][0], fy, hgt)


def base_bar(s, F, lo, hi, y_off=2.0, h=7.0):
    """Base of support: a bar on the floor from lo to hi metres from the ankle, with end ticks."""
    o = [box(s, F.x(lo), F.fy + s(y_off), F.k * (hi - lo), s(h))]
    for m in (lo, hi):
        o.append(H.line(s, F.x(m), F.fy - s(6), F.x(m), F.fy + s(y_off + h + 4), I["secondary"], "leader"))
    return "".join(o)


FIGS = {}


# ================================================================ svg #28  D1 the margin is a critical impulse
def fig28():
    p = "m10f28_"
    VB, s = bvb(494)
    o = [defs(p, s)]
    HF, fy, ax = 330.0, 400.0, 128.0
    _, J0 = LB.standing_full(p, s, 0.0, fy, HF)
    body, J = LB.standing_full(p, s, ax - J0["ankle"][0], fy, HF)
    F = Frame(J, HF)
    o.append(floor(s, 8, 200, fy))
    o.append(body)
    o.append(base_bar(s, F, -D_HEEL, D_TOE))
    com = (F.x(COM_AHEAD), F.ay - F.k * ELL)                   # the text's COM: l = 1.0 m above the ankle
    o.append(vline(s, com[0], com[1], fy))
    o.append(H.com_mark(s, *com))
    # the impulse at the COM
    o.append(H.arrow(s, p, 12, com[1], com[0] - s(30), com[1], "force"))
    o.append(lab(s, 12, com[1] - s(10), f'{it("J")} (impulse)', "label", O["force"]))
    # xi after J = J_max: on the front edge
    edge = F.x(D_TOE)
    o.append(xi_mark(s, edge, fy))
    o.append(dim_h(s, p, com[0], edge, fy + s(30), "geometry"))
    o.append(lab(s, edge + s(10), fy + s(35), f'{it("b")} = {B_REST:.2f} m', "label2", I["primary"]))
    o.append(H.line(s, edge + s(4), fy - s(8), edge + s(46), fy - s(34), I["secondary"], "leader"))
    o.append(lines(s, edge + s(50), fy - s(40), [f'ξ after {it("J")}{sb("max", s)}:', "on the front edge"]))
    o.append(lab(s, com[0] + s(10), com[1] - s(10), "COM", "label2"))
    o.append(lab(s, com[0] + s(10), com[1] + s(8), f'{it("ℓ")} = 1.0 m', "label2", I["secondary"]))
    o.append(lab(s, F.x(-D_HEEL) - s(6), fy + s(18), "base of support", "label2", I["primary"], "end"))
    xc = it("x") + sb("com", s)
    x0 = 216
    o.append(lines(s, x0, 26, [f'{it("b")} = {it("x")}{sb("edge", s)} − ξ,', f'ξ = {xc} + (d{xc}/d{it("t")})/ω₀',
                               f'from rest: ξ = 0, {it("b")} = {it("x")}{sb("edge", s)}']))
    o.append(lines(s, x0, 100, [f'impulse {it("J")} at the COM:', f'Δ(d{xc}/d{it("t")}) = {it("J")}/{it("m")}',
                                f'Δ{xc} = 0 (instant)', f'so ξ jumps: Δξ = {it("J")}/({it("m")}ω₀)']))
    o.append(lines(s, x0, 192, ["fixed support holds iff", f'ξ ≤ {it("x")}{sb("edge", s)} = {it("b")}:']))
    o.append(lab(s, x0, 244, f'{it("J")}{sb("max", s)} = {it("m")}ω₀{it("b")}', "label"))
    o.append(lines(s, x0, 268, [f'= {M:.0f} × {W0} × {B_REST:.2f}', f'= {J_MAX:.1f} ≈ {J_MAX:.0f} N s']))
    o.append(credit(s, VB))
    aria = ("A standing skeleton (Lynch art) with its centre of mass marked 1.0 metre above the ankle and a dashed drop "
            "to the floor. A red arrow pushes horizontally at the centre of mass with impulse J. A bar on the floor "
            "is the base of support, from 5 centimetres behind to 12 centimetres ahead of the ankle; the margin b = "
            f"{B_REST:.2f} metres runs from the centre of mass projection to the front edge, where the extrapolated "
            "COM xi lands when J reaches its largest value. The impulse changes the COM velocity by J/m and leaves "
            "its position unchanged, so xi jumps by J/(m omega0). Fixed support holds while xi is at most b, so J_max "
            f"= m omega0 b = {M:.0f} x {W0} x {B_REST:.2f} = {J_MAX:.1f}, about {J_MAX:.0f} newton-seconds.")
    return finish(VB, aria, s, o)


FIGS[28] = (r'D1: Starting from the definition of the extrapolated COM, de', fig28)


# ================================================================ svg #29  D2 state space and controllability
def lean_pose(a):
    """Whole body rigid, turned a degrees forward about the ankle (the lynch_body lean_forward idea)."""
    return LB.pose(pelvis=a, near=dict(hip=0), far=dict(hip=0))


def fig29():
    p = "m10f29_"
    VB, s = bvb(488)
    o = [defs(p, s)]
    HF, fy, ax, a = 250.0, 316.0, 150.0, 9.0
    body, J = body_at(p, s, lean_pose(a), ax, fy, HF)
    F = Frame(J, HF)
    ank = (F.ax, F.ay)
    k = F.k
    com = (ank[0] + k * ELL * math.sin(math.radians(a)), ank[1] - k * ELL * math.cos(math.radians(a)))
    o.append(floor(s, 8, 200, fy))
    o.append(body)
    o.append(H.line(s, ank[0], ank[1], com[0], com[1], O["dim"], "ref", H.DASH_REF))
    o.append(vline(s, ank[0], ank[1], ank[1] - k * ELL * 1.02))
    o.append(angle_arc(s, ank[0], ank[1], s(120), -90, -90 + a))
    o.append(lab(s, ank[0] + s(28), ank[1] - s(118), it("θ"), "label"))
    o.append(H.com_mark(s, *com))
    o.append(lab(s, com[0] - s(10), com[1] - s(10), "COM", "label2", anchor="end"))
    o.append(lab(s, (ank[0] + com[0]) / 2 + s(10), (ank[1] + com[1]) / 2, it("ℓ"), "label", I["primary"]))
    # ankle torque (restoring, counter-clockwise) and gravity's tip-over (clockwise)
    o.append(arc_arrow(s, p, ank[0], ank[1], s(46), -112, -172, "force"))
    o.append(arc_arrow(s, p, ank[0], ank[1], s(46), -68, 2, "load"))
    o.append(H.joint_centre(s, *ank))
    o.append(lines(s, ank[0] - s(54), ank[1] - s(56), ["ankle torque,", f'{it("u")} = {it("τ")}{sb("ank", s)}/({it("mℓ")}²)'],
                   anchor="end"))
    o.append(lines(s, ank[0] + s(52), ank[1] - s(28), ["gravity:", f'ω₀²{it("θ")}']))
    o.append(lab(s, ank[0], fy + s(18), "ankle", "label2", anchor="middle"))
    # right of the body: the state-space model and the plant block
    x0 = 232
    o.append(lines(s, x0, 26, [f'state {it("x")} = [{it("θ")}, {dot_("θ")}]ᵀ,', f'd²{it("θ")}/d{it("t")}² = ω₀²{it("θ")} + {it("u")}']))
    o.append(lines(s, x0, 78, [f'{it("A")} = [0 1; ω₀² 0],', f'{it("B")} = [0; 1]']))
    bx, by, bw, bh = x0 + 14, 128, 110, 42
    o.append(box(s, bx, by, bw, bh, extra=f'rx="{s(6):.2f}"'))
    o.append(lab(s, bx + bw / 2, by + s(17), "plant", "label2", I["primary"], "middle"))
    o.append(lab(s, bx + bw / 2, by + s(34), f'{dot_("x")} = {it("Ax")} + {it("Bu")}', "label2", I["primary"], "middle"))
    o.append(H.arrow(s, p, x0 - s(2), by + bh / 2, bx, by + bh / 2, "dim"))
    o.append(lab(s, x0 - s(2), by + bh / 2 - s(7), it("u"), "label2", I["primary"]))
    o.append(H.arrow(s, p, bx + bw, by + bh / 2, 396, by + bh / 2, "dim"))
    o.append(lab(s, 394, by + bh / 2 - s(7), it("x"), "label2", I["primary"], "end"))
    # below the floor: controllability
    o.append(lines(s, 22, fy + s(50), [f'{it("AB")} = [1; 0],  {it("C")} = [{it("B")}  {it("AB")}] = [0 1; 1 0]',
                                       f'det {it("C")} = −1 ≠ 0: rank 2 = dim {it("x")}, so ({it("A")}, {it("B")}) is controllable',
                                       'state feedback can place the closed-loop poles anywhere']))
    o.append(credit(s, VB))
    aria = ("A skeleton (Lynch art) leaning forward as one rigid body about its ankle by the angle theta, with the "
            "centre of mass a distance l above the ankle along the dashed line. Two curved arrows at the ankle: the "
            "ankle torque, written as the commanded angular acceleration u, turns the body back; gravity, omega0 squared "
            "times theta, turns it further forward. The linearised pendulum theta double dot = omega0^2 theta + u is "
            "the state-space plant x dot = A x + B u with x = [theta, theta dot], A = [0 1; omega0^2 0], B = [0; 1], "
            "drawn as a block with input u and output x. A B = [1; 0], so the controllability matrix [B AB] = [0 1; "
            "1 0] has determinant -1, rank 2 equal to the state dimension: the pair is controllable.")
    return finish(VB, aria, s, o)


FIGS[29] = (r'D2: Write the linearised inverted pendulum with ankle contro', fig29)


# ================================================================ svg #30  D3 closed-loop poles in the s-plane
def mn(t):
    return t.replace("-", "−")


def fig30():
    p = "m10f30_"
    VB, s = pvb(374)
    o = []
    x0, x1, yt, yb = 34.0, 386.0, 22.0, 262.0
    sc = (x1 - x0) / 10.0                                       # px per unit, both axes (Re -6..4)
    ym = (yt + yb) / 2
    X = lambda v: x0 + (v + 6.0) * sc                           # noqa: E731
    Y = lambda v: ym - v * sc                                   # noqa: E731
    o.append(f'<rect x="{x0}" y="{yt}" width="{X(0) - x0:.2f}" height="{yb - yt}" fill="{BOX}"/>')
    o.append(H.line(s, x0, ym, x1, ym, I["axis"], "axis"))
    o.append(H.line(s, X(0), yt, X(0), yb, I["axis"], "axis"))
    for v in (-6, -4, -2, 2, 4):
        o.append(H.line(s, X(v), ym, X(v), ym + s(5), I["axis"], "leader"))
        o.append(plabel(s, X(v), ym + s(21), mn(str(v)), "tick", I["secondary"], "middle"))
    for v in (-3, -2, -1, 1, 2, 3):
        o.append(H.line(s, X(0) - s(5), Y(v), X(0), Y(v), I["axis"], "leader"))
        if abs(v) == 2:
            o.append(plabel(s, X(0) - s(8), Y(v) + 4.5, mn(f"{v}i"), "tick", I["secondary"], "end"))
    o.append(plabel(s, x1 - 4, ym - 8, "Re s (1/s)", "label2", I["primary"], "end"))
    o.append(plabel(s, X(0) + 8, yt + 14, "Im s", "label2", I["primary"]))
    o.append(plabel(s, x0 + 6, yt + 14, "stable: Re s < 0", "label2", I["secondary"]))
    o.append(plabel(s, x1 - 4, yt + 14, "unstable", "label2", I["secondary"], "end"))
    # root locus of s^2 + k_d s + (k_p - w0^2) = 0 for k_p = 0 ... 20 (the real-root part lies on the axis)
    kc = W0 ** 2 + (KD / 2) ** 2                                # k_p of the double root at -k_d/2 (11.86)
    kr = np.linspace(0.0, kc, 60)
    disc = np.sqrt(np.maximum(KD ** 2 - 4 * (kr - W0 ** 2), 0))
    sp, sm = (-KD + disc) / 2, (-KD - disc) / 2
    kc2 = np.linspace(kc, KP, 40)
    im = np.sqrt(np.maximum(kc2 - kc, 0))
    col = SER[1]
    w = s(H.PX["curve_multi"])

    def pl(xs, ys):
        return (f'<polyline points="{" ".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in zip(xs, ys))}" fill="none" '
                f'stroke="{col}" stroke-width="{w:.2f}" stroke-linejoin="round"/>')

    o.append(pl(sp, np.zeros_like(sp)))
    o.append(pl(sm, np.zeros_like(sm)))
    o.append(pl(-KD / 2 * np.ones_like(kc2), im))
    o.append(pl(-KD / 2 * np.ones_like(kc2), -im))

    def cross(x, y, c):
        r = s(6)
        d = f"M{x - r:.2f},{y - r:.2f}L{x + r:.2f},{y + r:.2f}M{x - r:.2f},{y + r:.2f}L{x + r:.2f},{y - r:.2f}"
        return (f'<path d="{d}" stroke="#fff" stroke-width="{s(5):.2f}" fill="none"/>'
                f'<path d="{d}" stroke="{c}" stroke-width="{s(2.5):.2f}" fill="none"/>')

    for v in (-W0, W0):
        o.append(cross(X(v), Y(0), SER[0]))
    im_c = abs(_pole[0].imag)
    for sg in (1, -1):
        o.append(cross(X(-KD / 2), Y(sg * im_c), SER[1]))
    o.append(f'<circle cx="{X(0):.2f}" cy="{Y(0):.2f}" r="{s(4):.2f}" fill="#fff" stroke="{I["primary"]}" '
             f'stroke-width="{s(1.5):.2f}"/>')
    # labels
    o.append(plabel(s, X(-KD / 2) + s(12), Y(im_c) + 5, f"−1.5 + {im_c:.2f}i", "label2", I["primary"]))
    o.append(plabel(s, X(-KD / 2) + s(12), Y(-im_c) + 5, f"−1.5 − {im_c:.2f}i", "label2", I["primary"]))
    o.append(plabel(s, X(W0), Y(0) + s(40), f"+ω₀ = {W0}", "label2", I["primary"], "middle"))
    o.append(plabel(s, X(-W0), Y(0) + s(40), f"−ω₀ = −{W0}", "label2", I["primary"], "middle"))
    o.append(plabel(s, X(0) + s(9), Y(0) - s(30), f"{it('k')}{sb('p', s)} = ω₀² = {W0 ** 2:.2f}:", "label2"))
    o.append(plabel(s, X(0) + s(9), Y(0) - s(13), "a pole at 0", "label2"))
    o.append(plabel(s, x0 + 6, Y(1.45), f"{it('k')}{sb('p', s)}: 0 → {KP:.0f}", "label2", I["primary"]))
    o.append(legend(s, 38, yb + 34, [(SER[0], "open loop: ±ω₀", None),
                                     (SER[1], f"closed loop, {it('k')}{sb('d', s)} = {KD:g}", None)], gap=12))
    kp_, kd_ = it("k") + sb("p", s), it("k") + sb("d", s)
    o.append(lines(s, 38, yb + 62, [f'{it("s")}² + {kd_}{it("s")} + ({kp_} − ω₀²) = 0, {kd_} = {KD:g}, ω₀ = {W0}',
                                    f'{kp_} = {KP:.0f}: {it("s")} = −{kd_}/2 ± {it("i")}√({kp_} − ω₀² − {kd_}²/4)',
                                    f'= −1.5 ± {im_c:.2f}{it("i")}: Re {it("s")} < 0, a stable spiral']))
    # hover: the real-axis position of a pole -> the gain that puts one there
    xs = np.linspace(sm[0], sp[0], 120)
    pts = []
    for v in xs:
        kpv = W0 ** 2 - v * v - KD * v
        txt = (f"s = {v:.2f}: k_p = {kpv:.2f}" if abs(v + KD / 2) > 0.04 else
               f"s = -1.50: double root at k_p = {kc:.2f}; above it s = -1.5 ± i√(k_p - {kc:.2f})")
        pts.append([X(v), Y(0), mn(txt)])
    aria = (f"An s-plane plot, real axis from -6 to 4 and imaginary axis from -3.4 to 3.4, left half-plane shaded as stable. "
            f"Open-loop poles of the inverted pendulum, red crosses at +omega0 and -omega0 = +-{W0}, the right one in the "
            f"unstable half. The closed-loop characteristic polynomial s^2 + k_d s + (k_p - omega0^2) with k_d = {KD:g} has, "
            f"as k_p rises from 0 to 20, a blue locus: the unstable pole moves left along the real axis and crosses 0 at "
            f"k_p = omega0^2 = {W0 ** 2:.2f}, meets the other real pole at -1.5 at k_p = {kc:.2f}, then the pair leaves the "
            f"axis. At k_p = 20 the poles, blue crosses, are -1.5 +- {im_c:.2f} i, a stable spiral.")
    return finish(VB, aria, s, o, extra=H.hover_attr([x0, yt, x1, yb], pts))


FIGS[30] = (r'D3: For feedback $u=-[k_p\ k_d]\mathbf x$, derive the closed', fig30)


# ================================================================ svg #31  D4 the stability island
def island(kmax=40.0):
    om = np.concatenate([np.linspace(0.02, 1.0, 60), np.linspace(1.0, 7.0, 400)])
    sn = KD * om / (om ** 2 + W0 ** 2)
    tau = np.arcsin(sn) / om
    kp = (om ** 2 + W0 ** 2) * np.cos(om * tau)
    keep = kp <= kmax
    return tau[keep][::-1], kp[keep][::-1]                      # ascending tau


def fig31():
    p = "m10f31_"
    VB, s = pvb(352)
    o = []
    tau, kp = island()
    kmax, tmax = 40.0, 0.35
    P = Plot(s, (58, 24, 384, 244), (0, tmax), (0, kmax))
    close(float(np.interp(TAU_CRIT, tau, kp)), KP, 0.05)
    close(float(kp[-1]), W0 ** 2, 0.2)                         # right tip at k_p = omega0^2
    close(float(tau[-1]), KD / W0 ** 2, 0.02)                  # and tau = k_d/omega0^2 = 0.312 s
    o.append(f'<rect x="{P.X(0.10):.2f}" y="{P.Y(kmax):.2f}" width="{P.X(0.20) - P.X(0.10):.2f}" '
             f'height="{P.Y(0) - P.Y(kmax):.2f}" fill="{GRID}" fill-opacity="0.7"/>')
    poly = [(P.X(t), P.Y(k)) for t, k in zip(tau, kp)] + [(P.X(tau[-1]), P.Y(W0 ** 2)), (P.X(0), P.Y(W0 ** 2)),
                                                          (P.X(0), P.Y(kmax))]
    o.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in poly)}" fill="{O["geometry"]}" '
             f'fill-opacity="0.13"/>')
    o.append(P.axes([(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3)], [(v, f"{v:g}") for v in (0, 10, 20, 30, 40)],
                    "feedback delay τ (s)", f"gain {it('k')}{sb('p', s, 'label')} (s⁻²)", grid=(10, 20, 30, 40)))
    o.append(H.line(s, P.X(0), P.Y(W0 ** 2), P.X(tau[-1]), P.Y(W0 ** 2), O["dim"], "ref", H.DASH_REF))
    o.append(P.curve(tau, kp, SER[0]))
    o.append(P.dot(TAU_CRIT, KP, SER[0]))
    o.append(plabel(s, P.X(0.13), P.Y(kmax) + 14, "loop delay", "label2", I["secondary"]))
    o.append(plabel(s, P.X(0.13), P.Y(kmax) + 30, "100–200 ms", "label2", I["secondary"]))
    o.append(plabel(s, P.X(0.012), P.Y(18), "stable island,", "label2"))
    o.append(plabel(s, P.X(0.012), P.Y(18) + 17, f"{it('k')}{sb('d', s)} = {KD:g}", "label2"))
    o.append(plabel(s, P.X(0.215), P.Y(30), "unstable", "label2"))
    o.append(plabel(s, P.X(0.012), P.Y(W0 ** 2) + 17, f"{it('k')}{sb('p', s)} = ω₀² = {W0 ** 2:.1f} (gravity)", "label2",
                    I["secondary"]))
    o.append(plabel(s, P.X(TAU_CRIT) + 14, P.Y(KP) - 18, f"{it('τ')}{sb('c', s)} = {TAU_CRIT * 1000:.0f} ms", "label2"))
    o.append(plabel(s, P.X(TAU_CRIT) + 14, P.Y(KP) - 2, f"at {it('k')}{sb('p', s)} = {KP:.0f}", "label2", I["secondary"]))
    kd_, kp_ = it("k") + sb("d", s), it("k") + sb("p", s)
    o.append(lines(s, 40, 302, [f'sin Ωτ = {kd_}Ω/(Ω² + ω₀²), {kp_} = (Ω² + ω₀²) cos Ωτ',
                                f'{kd_} = {KD:g}, ω₀ = {W0}: at {kp_} = {KP:.0f}, Ω = {OMEGA_C:.1f} rad/s']))
    pts = [[P.X(t), P.Y(k), f"τ = {t:.3f} s: stable for {W0 ** 2:.1f} < k_p < {k:.1f}"] for t, k in zip(tau, kp)]
    aria = (f"The stability island in the delay-gain plane at k_d = {KD:g}. The boundary of Proposition 4.2, traced by sweeping "
            f"the crossing frequency Omega, starts high at small delay and falls to k_p = omega0^2 = {W0 ** 2:.1f} at tau = "
            f"{KD / W0 ** 2:.2f} s; below it and above the dashed gravity floor k_p = omega0^2 the loop is stable (blue "
            f"shading). A grey band marks the 100 to 200 millisecond sensorimotor loop delay. At k_p = {KP:.0f} the "
            f"boundary is crossed at the critical delay tau_c = {TAU_CRIT * 1000:.0f} ms, marked, where Omega = "
            f"{OMEGA_C:.1f} rad/s.")
    return finish(VB, aria, s, o, extra=H.hover_attr(P.box, pts))


FIGS[31] = (r'D4: Insert a feedback delay $\tau$ and derive the characteristic', fig31)


# ================================================================ svg #32  D5 stationary sway
def fig32():
    p = "m10f32_"
    VB, s = pvb(346)
    o = []
    P = Plot(s, (58, 30, 384, 214), (-1.2, 1.2), (0, 1.4))
    th = np.linspace(-1.2, 1.2, 241)
    pdf = np.exp(-0.5 * (th / SIG_DEG) ** 2) / (SIG_DEG * math.sqrt(2 * math.pi))
    edge = float(np.exp(-0.5) / (SIG_DEG * math.sqrt(2 * math.pi)))
    inner = [(P.X(t), P.Y(v)) for t, v in zip(th, pdf) if abs(t) < SIG_DEG]
    band = [(P.X(-SIG_DEG), P.Y(0)), (P.X(-SIG_DEG), P.Y(edge))] + inner + [(P.X(SIG_DEG), P.Y(edge)), (P.X(SIG_DEG), P.Y(0))]
    o.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in band)}" fill="{O["geometry"]}" fill-opacity="0.15"/>')
    o.append(P.axes([(v, mn(f"{v:g}")) for v in (-1.0, -0.5, 0, 0.5, 1.0)], [(v, f"{v:g}") for v in (0, 0.5, 1.0)],
                    "sway θ (degrees)", "p(θ) (per degree)", grid=(0.5, 1.0)))
    for sg in (-1, 1):
        o.append(H.line(s, P.X(sg * SIG_DEG), P.Y(0), P.X(sg * SIG_DEG), P.Y(edge), O["dim"], "ref", H.DASH_REF))
    o.append(P.curve(th, pdf, SER[1]))
    o.append(plabel(s, P.X(0), P.Y(0.40), "68 %", "label2", I["primary"], "middle"))
    o.append(plabel(s, P.X(0), P.Y(0.40) + 16, "within ±σ", "label2", I["primary"], "middle"))
    o.append(plabel(s, P.X(0.52), P.Y(1.12), f"σ = √Var = {SIG_DEG:.2f}°", "label2"))
    o.append(plabel(s, P.X(0.52), P.Y(1.12) + 17, f"({SIG_RAD * 1000:.2f}×10⁻³ rad)", "label2", I["secondary"]))
    kp_, kd_ = it("k") + sb("p", s), it("k") + sb("d", s)
    o.append(lines(s, 40, 276, [f'Var({it("θ")}) = {it("q")}/[2({kp_} − ω₀²){kd_}]',
                                f'= {Q * 1000:.1f}×10⁻³/(2 × {A0:.2f} × {KD:g}) = {VAR_TH * 1e5:.2f}×10⁻⁵ rad²',
                                f'{kp_} = {KP:.0f}, {kd_} = {KD:g}, ω₀ = {W0}, {it("q")} = {Q * 1000:.1f}×10⁻³ rad² s⁻³',
                                f'Var({dot_("θ")}) = {it("q")}/(2{kd_}) = {VAR_RATE * 1e4:.1f}×10⁻⁴ rad²/s², Cov = 0']))
    pts = [[P.X(t), P.Y(v), mn(f"θ = {t:.2f}°: p = {v:.2f} per degree")] for t, v in zip(th, pdf)]
    aria = (f"A bell curve of the stationary sway angle theta in degrees, from -1.2 to 1.2, centred on 0 with standard "
            f"deviation sigma = {SIG_DEG:.2f} degrees; the band within one sigma, 68 percent, is shaded. The Lyapunov equation "
            f"for the stable closed loop driven by white noise of intensity q = {Q:.1e} gives Var(theta) = q/[2(k_p - "
            f"omega0^2) k_d] = {VAR_TH:.2e} rad^2 at k_p = {KP:.0f}, k_d = {KD:g}, omega0 = {W0}, so sigma = {SIG_RAD * 1000:.2f} "
            f"milliradians = {SIG_DEG:.2f} degrees; Var(theta dot) = q/(2 k_d) = {VAR_RATE:.2e} rad^2/s^2, and angle and "
            f"rate are uncorrelated.")
    return finish(VB, aria, s, o, extra=H.hover_attr(P.box, pts))


FIGS[32] = (r'D5: Model quiet standing as the stable closed loop driven by', fig32)


# ================================================================ svg #33  D6 the scalar Kalman gain
SIG_P, SIG_M, X_PRED, Y_MEAS = 1.0, 0.5, -0.6, 1.0     # assumed (the text fixes none): illustration values
KF = SIG_P ** 2 / (SIG_P ** 2 + SIG_M ** 2)
X_POST = X_PRED + KF * (Y_MEAS - X_PRED)
VAR_POST = (1 - KF) * SIG_P ** 2
close(KF, 0.80, 1e-9)
close(X_POST, 0.68, 1e-9)
close(VAR_POST, SIG_P ** 2 * SIG_M ** 2 / (SIG_P ** 2 + SIG_M ** 2), 1e-12)   # line 250


def gauss(x, m, sd):
    return np.exp(-0.5 * ((x - m) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))


def fig33():
    p = "m10f33_"
    VB, s = pvb(380)
    o = []
    P = Plot(s, (58, 44, 384, 226), (-3, 3), (0, 1.0))
    x = np.linspace(-3, 3, 241)
    sd_post = math.sqrt(VAR_POST)
    yp, ym_, yo = gauss(x, X_PRED, SIG_P), gauss(x, Y_MEAS, SIG_M), gauss(x, X_POST, sd_post)
    o.append(P.axes([(v, mn(f"{v:g}")) for v in (-3, -2, -1, 0, 1, 2, 3)], [(v, f"{v:g}") for v in (0, 0.5, 1.0)],
                    "state estimate x (illustrative units)", "density", grid=(0.5, 1.0)))
    o.append(P.curve(x, yp, SER[2], multi=True))
    o.append(P.curve(x, ym_, SER[1], multi=True))
    o.append(P.curve(x, yo, SER[0]))
    for m, sd, c in ((X_PRED, SIG_P, SER[2]), (Y_MEAS, SIG_M, SER[1]), (X_POST, sd_post, SER[0])):
        o.append(P.dot(m, float(gauss(m, m, sd)), c))
    o.append(legend(s, 58, 22, [(SER[2], "prediction", None), (SER[1], "measurement", None),
                                (SER[0], "fused (posterior)", None)], gap=10))
    o.append(plabel(s, P.X(-2.92), P.Y(0.33), "prediction", "label2", I["primary"]))
    o.append(plabel(s, P.X(1.75), P.Y(0.30), "measurement", "label2", I["primary"]))
    o.append(plabel(s, P.X(X_POST) - s(26), P.Y(0.96), "fused, narrowest", "label2", I["primary"], "end"))
    xh = hat("x")
    kf_, sp_, sm_ = it("K") + sb("f", s), "σ" + sb("p", s), "σ" + sb("m", s)
    o.append(lines(s, 40, 292, [f'assumed: {xh}⁻ = {mn(f"{X_PRED:g}")}, {sp_} = {SIG_P:.1f}; {it("y")} = {Y_MEAS:.1f}, '
                                f'{sm_} = {SIG_M:.1f}',
                                f'{kf_} = {sp_}²/({sp_}² + {sm_}²) = {SIG_P ** 2:.2f}/({SIG_P ** 2:.2f} + {SIG_M ** 2:.2f}) = '
                                f'{KF:.2f}',
                                f'{xh} = {xh}⁻ + {kf_}({it("y")} − {xh}⁻) = {mn(f"{X_PRED:g}")} + {KF:.2f} × '
                                f'{Y_MEAS - X_PRED:.1f} = {X_POST:.2f}',
                                f'σ₊² = (1 − {kf_}){sp_}² = {VAR_POST:.2f} < {sm_}² = {SIG_M ** 2:.2f} < {sp_}² = '
                                f'{SIG_P ** 2:.2f}']))
    pts = [[P.X(t), [P.Y(a), P.Y(b), P.Y(c)], mn(f"x = {t:.2f}: prediction {a:.2f}, measurement {b:.2f}, fused {c:.2f}")]
           for t, a, b, c in zip(x, yp, ym_, yo)]
    aria = (f"Three bell curves over the state estimate x. The model prediction, orange, is broad: mean {X_PRED:g}, standard "
            f"deviation sigma_p = {SIG_P:.1f}. The measurement, blue, is sharper: mean {Y_MEAS:.1f}, sigma_m = {SIG_M:.1f}. "
            f"Their minimum-variance fusion, red, has gain K_f = sigma_p^2/(sigma_p^2 + sigma_m^2) = {KF:.2f}, mean "
            f"{X_POST:.2f} = {X_PRED:g} + {KF:.2f} x {Y_MEAS - X_PRED:.1f}, and variance (1 - K_f) sigma_p^2 = {VAR_POST:.2f}, "
            f"smaller than both inputs: it is the narrowest and tallest curve. The values are illustrative.")
    return finish(VB, aria, s, o, extra=H.hover_attr(P.box, pts))


FIGS[33] = (r'D6: Derive the scalar Kalman gain: the minimum-variance weig', fig33)


# ================================================================ svg #34  D7 the delay predictor
X_DELAYED = np.array([0.10, 0.50])             # rad, rad/s: assumed example state at t - tau (the text gives none)
_c, _sh = math.cosh(W0 * TAU_C), math.sinh(W0 * TAU_C)
E_TAU = np.array([[_c, _sh / W0], [W0 * _sh, _c]])      # e^(A tau) for A = [0 1; w0^2 0] in closed form
X_PRED_NOW = E_TAU @ X_DELAYED                  # u = 0 over the interval (the integral term of line 259 is zero)
close(X_PRED_NOW[0], 0.156, 0.0005)
close(X_PRED_NOW[1], 0.622, 0.0005)
close(float(np.linalg.det(E_TAU)), 1.0, 1e-9)    # e^(A tau) has determinant e^(trace A tau) = 1


def ex(arg, s):
    return f'e\u2006{sup(arg, s, "label2")}'


def fig34():
    p = "m10f34_"
    VB, s = bvb(520)
    o = [defs(p, s)]
    HF, fy = 215.0, 290.0
    th = [math.degrees(X_DELAYED[0]), math.degrees(X_PRED_NOW[0])]
    xs = (84.0, 276.0)
    o.append(floor(s, 8, 392, fy))
    for i, (ax, a) in enumerate(zip(xs, th)):
        body, J = body_at(p, s, lean_pose(a), ax, fy, HF)
        F = Frame(J, HF)
        ank, k = (F.ax, F.ay), F.k
        com = (ank[0] + k * ELL * math.sin(math.radians(a)), ank[1] - k * ELL * math.cos(math.radians(a)))
        o.append(body)
        o.append(vline(s, ank[0], ank[1], ank[1] - k * ELL * 1.02))
        o.append(H.line(s, ank[0], ank[1], com[0], com[1], O["dim"], "ref", H.DASH_REF))
        o.append(angle_arc(s, ank[0], ank[1], s(150), -90, -90 + a))
        o.append(lab(s, ank[0] + s(30), ank[1] - s(150), it("θ"), "label"))
        o.append(H.com_mark(s, *com))
        o.append(H.line(s, ank[0], fy - s(6), ank[0], fy + s(6), I["axis"], "leader"))
        o.append(lab(s, ank[0], fy + s(24), ("t − τ", "t (now)")[i], "label2", I["primary"], "middle"))
        o.append(lab(s, ank[0] + s(4), 26, f'{hat("x")}({("t − τ", "t")[i]})', "label", I["primary"], "middle"))
        o.append(lab(s, ank[0] + s(4), 44, ("delayed estimate", "predicted: now")[i], "label2", I["secondary"], "middle"))
    ymid = fy - 0.58 * HF
    o.append(H.arrow(s, p, xs[0] + 62, ymid, xs[1] - 52, ymid, "geometry"))
    o.append(lab(s, (xs[0] + xs[1]) / 2 + s(4), ymid - s(10), f'push forward by {ex(f"{it(chr(65))}τ", s)}', "label2",
                 I["primary"], "middle"))
    o.append(dim_h(s, p, xs[0], xs[1], fy + s(42), "dim"))
    o.append(lab(s, (xs[0] + xs[1]) / 2, fy + s(62), f'τ = {TAU_C:.2f} s (Lab C)', "label2", I["primary"], "middle"))
    xh, A_, B_, tau = hat("x"), it("A"), it("B"), it("τ")
    ints = f'∫{sb("0", s)}{sup("τ", s)}'
    o.append(lines(s, 24, fy + s(90), [
        f'{it("x")}({it("t")}) = {ex(f"{A_}τ", s)}{it("x")}({it("t")} − τ) + {ints} {ex(f"{A_}(τ − {it(chr(115))})", s)}'
        f'{B_}{it("u")}({it("t")} − τ + {it("s")}) d{it("s")}',
        f'error of {xh}({it("t")}) = {ex(f"{A_}τ", s)} × error of {xh}({it("t")} − τ)',
        f'{it("u")} = −{it("K")}{xh}({it("t")}): the loop acts as the delay-free {A_} − {B_}{it("K")}',
        f'assumed example, {it("u")} = 0 in the interval, τ = {TAU_C:.2f} s:',
        f'{xh}({it("t")} − τ) = [{X_DELAYED[0]:.3f} rad, {X_DELAYED[1]:.2f} rad/s]',
        f'{xh}({it("t")}) = [{X_PRED_NOW[0]:.3f} rad, {X_PRED_NOW[1]:.2f} rad/s]: lean {th[0]:.1f}° → {th[1]:.1f}°']))
    o.append(credit(s, VB))
    aria = (f"Two copies of one skeleton (Lynch art) leaning forward as a rigid body about the ankle, joined by a blue "
            f"arrow labelled push forward by e^(A tau). Left, the delayed estimate x-hat(t - tau), measured tau = "
            f"{TAU_C:.2f} s ago, leans {th[0]:.1f} degrees; right, the predicted present state x-hat(t) leans {th[1]:.1f} "
            f"degrees. The predictor of Proposition 6.2 is x(t) = e^(A tau) x(t - tau) + the integral of e^(A(tau - s)) B u; "
            f"its error is e^(A tau) times the filter's estimation error, and feeding u = -K x-hat(t) lets the loop act as "
            f"the delay-free A - BK. Assumed example with u = 0: [{X_DELAYED[0]:.3f} rad, {X_DELAYED[1]:.2f} rad/s] becomes "
            f"[{X_PRED_NOW[0]:.3f} rad, {X_PRED_NOW[1]:.2f} rad/s].")
    return finish(VB, aria, s, o)


FIGS[34] = (r'D7: Derive the delay predictor that maps the filtered estimate ', fig34)


# ================================================================ svg #35  D8 the capture point
def pose_com(P):
    tot = sum(m for _, m in P.com.values())
    return (sum(c[0] * m for c, m in P.com.values()) / tot, sum(c[1] * m for c, m in P.com.values()) / tot)


def _bis(f, lo, hi, n=60):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def step_pose(gap_m):
    """Touchdown of a capture step: near (front) leg lands its heel gap_m ahead of the COM; far (rear) leg on its toe.
    Solved on the near hip flexion; the trunk is upright."""
    def build(h):
        return LB.pose(near=dict(hip=h, knee=6, contact="heel", shoulder=-15, elbow=12),
                       far=dict(hip=-12, knee=32, contact="toe", shoulder=18, elbow=20), anchor=("heel", "near"))

    def err(h):
        P = build(h)
        return (P.j["heel"][0] - pose_com(P)[0]) / UM - gap_m

    h = _bis(err, 15.0, 45.0)
    P = build(h)
    P.h = h
    return P


XD_OVER_W = XI_S - X_S                           # (dx/dt)/omega0 at touchdown = 0.270 m
close(XD_OVER_W, V_S / W0, 1e-9)
close(XD_OVER_W, 0.270, 0.0005)


def fig35():
    p = "m10f35_"
    VB, s = bvb(562)
    o = [defs(p, s)]
    HF, fy, xc = 290.0, 336.0, 120.0
    gap = XD_OVER_W + DELTA                      # front heel ahead of the COM projection = x_foot - x_com = 0.350 m
    P = step_pose(gap)
    _, J0 = LB.draw(p, s, P, 0.0, fy, HF)
    body, J = LB.draw(p, s, P, xc - J0["com"][0], fy, HF)
    k = HF / H_M
    xcom = J["com"][0]
    close((J["heel"][0] - xcom) / k, gap, 0.002)
    xi_x = xcom + k * XD_OVER_W
    heel = J["heel"][0]
    o.append(floor(s, 8, 396, fy))
    o.append(body)
    o.append(vline(s, xcom, J["com"][1], fy))
    o.append(H.com_mark(s, *J["com"]))
    o.append(lab(s, xcom - s(10), J["com"][1] - s(8), "COM", "label2", anchor="end"))
    o.append(xi_mark(s, xi_x, fy))
    o.append(contact_mark(s, heel, fy))
    y1 = fy + s(24)
    o.append(dim_h(s, p, xcom, xi_x, y1, "geometry"))
    o.append(dim_h(s, p, xi_x, heel, y1, "force"))
    o.append(lab(s, xi_x - s(2), fy + s(46), f'{dot_("x")}/ω₀ = {XD_OVER_W:.2f} m', "label2", I["primary"], "end"))
    o.append(H.line(s, (xi_x + heel) / 2, y1 + s(6), heel + s(6), fy + s(52), O["force"], "leader"))
    o.append(lab(s, heel + s(8), fy + s(62), f'Δ = {DELTA * 100:.0f} cm', "label2", O["force"]))
    o.append(lab(s, xi_x - s(2), fy - s(14), "ξ", "label", I["primary"], "end"))
    o.append(lab(s, heel + s(8), fy - s(30), f'{it("x")}{sb("foot", s)} = ξ + Δ', "label", I["primary"]))
    o.append(lab(s, heel + s(8), fy - s(12), "heel strike", "label2", I["secondary"]))
    xc_ = it("x") + sb("com", s)
    xf_ = it("x") + sb("foot", s)
    o.append(lines(s, 22, fy + s(94), [
        f'new foot at {xf_}: {it("x")}′ = {xc_} − {xf_}, ξ′ = ξ − {xf_}',
        f'rest over the new foot needs ξ′ ≤ 0, i.e. {xf_} ≥ ξ',
        f'{xf_} = ξ: ξ′ = 0, marginal;  {xf_} = ξ + Δ: ξ′ = −Δ',
        f'K8 (40 N s push, step at {T_STEP:.2f} s): ξ{sb("s", s)} = {XI_S:.3f} m, reach {L_STEP:.2f} m',
        f'window 0 ≤ Δ ≤ {L_STEP - XI_S:.3f} m; Δ = {DELTA * 100:.0f} cm is drawn']))
    o.append(credit(s, VB))
    aria = (f"A skeleton (Lynch art) at touchdown of a capture step, trunk upright, the rear foot on its toe and the front "
            f"heel planted ahead. The centre of mass is marked with a dashed drop to the floor. On the floor, a blue "
            f"dimension of {XD_OVER_W:.2f} metres (the COM velocity over omega0) leads from the COM projection to the "
            f"extrapolated COM xi, an open circle, and a red {DELTA * 100:.0f} centimetre dimension Delta leads on to the new "
            f"foot at x_foot = xi + Delta. After the step the divergent coordinate about the new foot is xi' = xi - x_foot; "
            f"coming to rest over it needs xi' at most 0, so x_foot at least xi; x_foot = xi is the marginal case, and "
            f"x_foot = xi + Delta leaves xi' = -Delta. K8: xi_s = {XI_S:.3f} m against a reach of {L_STEP:.2f} m, so the "
            f"window is 0 to {L_STEP - XI_S:.3f} m.")
    return finish(VB, aria, s, o)


FIGS[35] = (r'D8: Derive the capture-step placement that arrests a fall in', fig35)


# ================================================================ svg #36  D9 the slip condition
def fig36():
    p = "m10f36_"
    VB, s = bvb(548)
    o = [defs(p, s)]
    HF, fy, hx = 250.0, 300.0, 132.0
    P = LB.pose(**LB.POSES["gait_heel_strike"])
    body, J = body_at(p, s, P, hx, fy, HF, key="heel")
    heel, c = J["heel"], J["com"]
    ang_req, ang_av = math.degrees(math.atan(MU_REQ)), math.degrees(math.atan(MU_ICE))
    o.append(floor(s, 8, 196, fy))
    o.append(body)
    o.append(contact_mark(s, heel[0], fy))
    o.append(H.com_mark(s, *c))
    o.append(lab(s, c[0] + s(12), c[1] + s(4), "COM", "label2"))
    # the slip: the foot slides forward, the body falls backward about the contact
    ax0 = heel[0] - s(10)
    o.append(H.arrow(s, p, ax0, fy + s(14), ax0 + s(50), fy + s(14), "flag", w="force"))
    o.append(lab(s, ax0 + s(25), fy + s(34), "foot slides forward", "label2", I["primary"], "middle"))
    r = math.hypot(c[0] - heel[0], c[1] - fy) + s(30)
    a_c = math.degrees(math.atan2(c[1] - fy, c[0] - heel[0]))
    o.append(arc_arrow(s, p, heel[0], fy, r, a_c + 6, a_c - 16, "load"))
    e = (heel[0] + r * math.cos(math.radians(a_c - 16)), fy + r * math.sin(math.radians(a_c - 16)))
    o.append(lab(s, s(6), e[1] + s(34), "backward fall", "label2", I["primary"]))
    # inset: the ground reaction at the heel, to scale (F_h = mu_req F_v), against the friction cone of the ice
    bx, by, bw, bh = 206.0, 40.0, 188.0, 300.0
    o.append(box(s, bx, by, bw, bh))
    o.append(lab(s, bx + bw / 2, by + s(20), "ground reaction at the heel", "label2", I["primary"], "middle"))
    ox, oy = 300.0, 252.0
    fv = 150.0
    fh = MU_REQ * fv
    cone = 160.0
    tl = (ox - cone * math.tan(math.radians(ang_av)), oy - cone)
    tr = (ox + cone * math.tan(math.radians(ang_av)), oy - cone)
    o.append(f'<polygon points="{ox:.2f},{oy:.2f} {tl[0]:.2f},{tl[1]:.2f} {tr[0]:.2f},{tr[1]:.2f}" '
             f'fill="{O["flag"]}" fill-opacity="0.25"/>')
    o.append(H.line(s, bx + s(8), oy, bx + bw - s(8), oy, I["axis"], "axis"))
    o.append(H.line(s, ox, oy, *tl, O["flag"], "ref", H.DASH_REF))
    o.append(H.line(s, ox, oy, *tr, O["flag"], "ref", H.DASH_REF))
    o.append(H.line(s, ox, oy, ox - fh, oy - fv, O["dim"], "ref", H.DASH_REF))
    o.append(H.arrow(s, p, ox, oy - s(2), ox, oy - fv, "reaction"))
    o.append(H.arrow(s, p, ox, oy - s(9), ox - fh, oy - s(9), "force"))
    o.append(contact_mark(s, ox, oy))
    fv_, fh_ = f'{it("F")}{sb("v", s)}', f'{it("F")}{sb("h", s)}'
    o.append(lab(s, ox + s(18), oy - fv + s(8), fv_, "label", I["primary"]))
    o.append(lab(s, ox - fh - s(4), oy - s(14), fh_, "label", O["force"], "end"))
    o.append(lab(s, ox - fh - s(7), oy - fv - s(2), it("R"), "label", I["primary"], "end"))
    o.append(lines(s, bx + s(10), oy + s(24), [f'{it("R")}: {fh_}/{fv_} = {it("μ")}{sb("req", s)} = {MU_REQ:.2f} ({ang_req:.1f}°)',
                                               f'cone: {it("μ")}{sb("avail", s)} = {MU_ICE:.2f} ice ({ang_av:.1f}°)',
                                               f'{it("R")} is outside the cone: slip']))
    mu_ = it("μ")
    o.append(lines(s, 22, fy + s(76), [
        f'Coulomb limit on the foot: |{fh_}| ≤ {mu_}{sb("avail", s)} {fv_}',
        f'divide by {fv_}: {mu_}{sb("req", s)} = |{fh_}|/{fv_} ≤ {mu_}{sb("avail", s)} holds the foot',
        f'{mu_}{sb("req", s)} > {mu_}{sb("avail", s)}: it slips',
        f'heel strike {mu_}{sb("req", s)} = {MU_REQ:.2f} > ice {mu_}{sb("avail", s)} = {MU_ICE:.2f}: slip',
        'the leading foot slides forward, the support leaves from',
        'under the COM, and gravity’s moment turns the body back:',
        'a backward fall']))
    o.append(credit(s, VB))
    aria = (f"A skeleton (Lynch art) at heel strike, walking to the right, with its leading heel on the floor, a dot. An "
            f"orange arrow shows the foot sliding forward and a curved brown arrow the body falling backward about the "
            f"contact. Beside it, a boxed inset draws the ground reaction at the heel to scale: the vertical component F_v "
            f"(black arrow up) and the horizontal component F_h (red arrow backward) of {MU_REQ:.2f} F_v, whose sum R, a "
            f"dashed line, is tilted {ang_req:.1f} degrees from the vertical: F_h/F_v = mu_req = {MU_REQ:.2f}. An orange "
            f"shaded friction cone of half-angle {ang_av:.1f} degrees, mu_avail = {MU_ICE:.2f} for ice, holds only reactions "
            f"inside it; R lies outside, so the foot slips. The slip condition is mu_req = |F_h|/F_v greater than "
            f"mu_avail, from the Coulomb limit |F_h| at most mu_avail F_v.")
    return finish(VB, aria, s, o)


FIGS[36] = (r'D9: Derive the slip condition from the Coulomb friction limit', fig36)


# ================================================================ svg #37  D10 the trip
def trip_pose():
    return LB.pose(near=dict(hip=0, knee=4, shoulder=10, elbow=15),
                   far=dict(hip=20, knee=35, contact=None, ankle=15, shoulder=-12, elbow=20), anchor=("heel", "near"))


def fig37():
    p = "m10f37_"
    VB, s = bvb(598)
    o = [defs(p, s)]
    HF, fy, ax = 280.0, 310.0, 96.0
    P = trip_pose()
    body, J = body_at(p, s, P, ax, fy, HF)
    k = HF / H_M
    toe = J["toe_far"]
    hb = fy - toe[1]                                              # block height: the swing toe touches its back face
    bh = hb + s(5)
    cx, cy = toe[0], toe[1]
    wid = 0.12 * k
    o.append(floor(s, 8, 396, fy))
    o.append(body)
    o.append(box(s, cx, fy - bh, wid, bh, fill=GRID, stroke=I["secondary"]))
    o.append(lab(s, cx + wid / 2 - s(4), fy - bh - s(10), "block", "label2", I["secondary"], "middle"))
    ell = ELL * k
    com = (J["com"][0], cy - ell)                                 # the text's COM: l = 1.0 m above the block contact
    o.append(vline(s, com[0], com[1], fy))
    o.append(H.com_mark(s, *com))
    o.append(lab(s, com[0] - s(10), com[1] - s(8), "COM", "label2", anchor="end"))
    # velocity v, height l, pitch about the block
    vk = 52.0 / V_WALK
    o.append(H.arrow(s, p, com[0] + s(9), com[1], com[0] + s(9) + V_WALK * vk, com[1], "geometry"))
    o.append(lab(s, com[0] + s(12), com[1] - s(10), f'{it("v")} = {V_WALK} m/s', "label2", I["primary"]))
    xr = cx + wid + s(52)
    o.append(H.line(s, com[0] + s(9) + V_WALK * vk + s(14), com[1], xr + s(6), com[1], O["dim"], "ref", H.DASH_REF))
    o.append(H.line(s, cx + wid + s(6), cy, xr + s(6), cy, O["dim"], "ref", H.DASH_REF))
    o.append(H.arrow(s, p, xr, (com[1] + cy) / 2 - s(18), xr, com[1], "dim"))
    o.append(H.arrow(s, p, xr, (com[1] + cy) / 2 + s(18), xr, cy, "dim"))
    o.append(lab(s, xr, (com[1] + cy) / 2 + s(5), it("ℓ"), "label", I["primary"], "middle"))
    r = 0.55 * ell
    o.append(arc_arrow(s, p, cx, cy, r, -128, -88, "force"))
    o.append(lab(s, cx + s(8), cy - r - s(8), f'{dot_("θ")}⁺ = {it("v")}/{it("ℓ")}', "label", O["force"]))
    o.append(contact_mark(s, cx, cy))
    # delta xi against the foot length, on the floor
    xg = com[0]
    dx = V_WALK / W0 * k
    y1 = fy + s(24)
    o.append(dim_h(s, p, xg, xg + dx, y1, "geometry"))
    o.append(lab(s, xg + dx + s(8), y1 + s(5), f'Δξ = {it("v")}/ω₀ = {V_WALK / W0:.2f} m', "label2", I["primary"]))
    o.append(dim_h(s, p, xg, xg + FOOT_M * k, y1 + s(24), "dim"))
    o.append(lab(s, xg + FOOT_M * k + s(8), y1 + s(29), f'foot {FOOT_M:.2f} m', "label2", I["secondary"]))
    o.append(xi_mark(s, xg + dx, fy))
    o.append(lab(s, xg + dx, fy - s(24), "ξ", "label", I["primary"], "middle"))
    xd = dot_("x")
    o.append(lines(s, 22, fy + s(88), [
        'the block force has no moment about the block, so angular',
        'momentum about it is kept:',
        f'before H = {it("mvℓ")}, after H = {it("I")}{dot_("θ")}⁺ with {it("I")} = {it("mℓ")}²',
        f'{dot_("θ")}⁺ = {it("v")}/{it("ℓ")} = {V_WALK}/{ELL:.1f} = {V_WALK / ELL:.1f} rad/s ({math.degrees(V_WALK / ELL):.0f}°/s)',
        f'COM speed kept: {xd}⁺ = {it("ℓ")}{dot_("θ")}⁺ = {it("v")}',
        f'Δξ = {xd}⁺/ω₀ = {it("v")}/ω₀ = {V_WALK}/{W0} = {V_WALK / W0:.2f} m > foot {FOOT_M:.2f} m:',
        'ξ is past the base, so a capture step is forced']))
    o.append(credit(s, VB))
    aria = (f"A skeleton (Lynch art) walking to the right in mid-swing, its swing foot just caught on a block on the "
            f"floor, the stance foot flat. The centre of mass is marked a height l = {ELL:.1f} m above the block contact, "
            f"moving forward at v = {V_WALK} m/s (blue arrow). A red curved arrow about the contact is the forward pitch "
            f"rate. The block force has no moment about the block, so angular momentum about it is conserved: before H = "
            f"m v l, after H = I theta-dot with I = m l^2, so theta-dot+ = v/l = {V_WALK / ELL:.1f} rad/s. The COM speed "
            f"is kept, so the extrapolated COM jumps by delta xi = v/omega0 = {V_WALK / W0:.2f} m, drawn on the floor "
            f"beside the foot length of {FOOT_M:.2f} m: xi lies past the base and a capture step is forced.")
    return finish(VB, aria, s, o)


FIGS[37] = ("D10: A walking body's swing foot is fully arrested by an obs", fig37)
