"""Module 8, group `body_d`: derivational problems D1-D10 (svg #27-#36), house style, 400 px.

Bodies are the posable Lynch skeleton (lynch_body.py); body_main.py puts its defs on the page, this group only
<use>s them.  Stature 1.75 m (the text states none).  The walker is the text's point-mass pendulum: the COM mark sits
at the reference length l = 0.95 m from the stance contact (module08.html lines 203, 223), and the poses are solved
so that the skeleton's hip lies 2.25 cm below that point (l - 0.530 H), on the model's leg line.  The reference gait
(lines 491-507) fixes every number: M = 70 kg, l = 0.95 m, v = 1.3 m/s, L* = 0.6847 m (Lab 2), alpha = 21.1 deg.
Every number on a figure is computed here from the formula or lab code the module states (line numbers beside it).
"""
import math

import numpy as np

import house as H
import lynch_body as LB
from m05.body import finish, it
from m05.plots_prob import Plot, label as plabel, legend

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
BOX = "#f7f4ef"
GRID = "#e6e6e6"
H_M = 1.75                               # m, stature (design value)
UM = LB.H_U / H_M                        # body units per metre


def close(v, ref, tol):
    assert abs(v - ref) <= tol * 1.0001, (v, ref)


# ---------------------------------------------------------------- numbers module08.html states
G, ELL, M, V = 9.81, 0.95, 70.0, 1.3     # m/s^2, m, kg, m/s (lines 491, 670, 694)
KAPPA = 0.09                             # m^2, swing-cost coefficient (line 503)
W = M * G                                # N, body weight (line 449: 686.7 N)
W0 = math.sqrt(G / ELL)                  # 1/s (line 223)
_LG = np.linspace(0.35, 0.95, 200)       # Lab 2 grid (lines 694-704), ported line for line
_AG = np.arcsin(_LG / (2 * ELL))
_CG = 0.5 * M * V * V * np.sin(2 * _AG) ** 2 + KAPPA * (V / _LG) ** 2 * M
L_STAR = float(_LG[int(np.argmin(_CG))])


def cost(L, v=V):
    """Per-step cost proxy C(v, L) of section 7 (line 499): (transition, swing)."""
    a = np.arcsin(np.asarray(L) / (2 * ELL))
    return 0.5 * M * v * v * np.sin(2 * a) ** 2, KAPPA * M * (v / np.asarray(L)) ** 2


def _golden(f, lo, hi, n=80):
    r = (math.sqrt(5) - 1) / 2
    a, b = lo, hi
    for _ in range(n):
        c, d = b - r * (b - a), a + r * (b - a)
        if f(c) < f(d):
            b = d
        else:
            a = c
    return (a + b) / 2


L_OPT = _golden(lambda L: sum(cost(L)), 0.35, 0.95)           # continuous optimum (D8 solution: 0.684 m)
ALPHA = math.asin(L_STAR / (2 * ELL))                          # rad, reference half-angle
AD = math.degrees(ALPHA)
CAD = V / L_STAR                                               # steps/s
DH = ELL * (1 - math.cos(ALPHA))                               # Prop 2.1
FR = V * V / (G * ELL)                                         # Prop 2.2
E_LOSS = 0.5 * M * V * V * math.sin(2 * ALPHA) ** 2            # Prop 5.1
close(L_STAR, 0.6847, 0.00005)                  # lines 671, 708
close(L_OPT, 0.684, 0.0005)                     # lines 507, D8 solution (line 851)
close(AD, 21.1, 0.05)                           # lines 395, 507, 684
close(2 * AD, 42.2, 0.05)                       # line 402
close(CAD, 1.90, 0.005)                         # lines 507, 708
close(CAD * 60, 114, 0.5)                       # line 507
close(2 * L_STAR / V, 1.053, 0.0005)            # line 507
close(W0, 3.21, 0.005)                          # line 223
close(DH, 0.0638, 0.00005)                      # line 684
close(M * G * DH, 43.8, 0.05)                   # line 684
close(FR, 0.181, 0.0005)                        # lines 457, 684
close(math.sqrt(0.5 * G * ELL), 2.16, 0.005)    # line 247
close(1 - FR, 0.819, 0.0005)                    # line 457
close(W * (1 - FR), 562, 0.5)                   # line 457
close(E_LOSS, 26.7, 0.05)                       # line 402
_tr, _sw = cost(L_STAR)
close(_tr, 26.7, 0.05)                          # lines 507, 708
close(_sw, 22.7, 0.05)
close(_tr + _sw, 49.4, 0.05)
_c0 = sum(cost(L_STAR))
close(100 * (sum(cost(1.2 * L_STAR)) / _c0 - 1), 4.6, 0.05)   # line 511
close(100 * (sum(cost(0.8 * L_STAR)) / _c0 - 1), 8.2, 0.05)
close(math.cos(2 * ALPHA), 0.740, 0.0005)       # Prop 4.1 at the reference step (figure value)


def k1_fy(theta, v_mid=V):
    """K1 (line 873): rigid-vault ground reaction at leg angle theta (rad, + = COM ahead of the contact):
    (along-leg N, F_x, F_y), newtons.  The leg pushes from the contact toward the COM, along (sin theta, cos theta),
    so F_x < 0 (braking) while the COM is behind the contact."""
    v2 = v_mid ** 2 + 2 * G * ELL * (1 - math.cos(theta))
    n = M * (G * math.cos(theta) - v2 / ELL)
    return n, n * math.sin(theta), n * math.cos(theta)


close(k1_fy(math.radians(12))[2] / W, 0.737, 0.0005)   # K1 solution (line 873)
close(k1_fy(ALPHA)[2] / W, 0.576, 0.0005)


# ---------------------------------------------------------------- drawing helpers
def sub(t, s, size="label"):
    return H.sub(t, s, size)


def lab(s, x, y, text, size="label", fill=I["primary"], anchor="start", extra=""):
    return H.label(s, x, y, text, size, fill, anchor, extra)


def lines(s, x, y, rows, size="label2", anchor="start", fill=None):
    L = s(H.PX[size]) * 1.35
    return "".join(lab(s, x, y + i * L, t, size, fill or I["primary"], anchor) for i, t in enumerate(rows))


def mn(t):
    return t.replace("-", "−")


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
    nl, cur = 0, ""
    for wd in t.split():
        if cur and len(cur) + 1 + len(wd) > n:
            nl, cur = nl + 1, wd
        else:
            cur = (cur + " " + wd).strip()
    y = vb[1] + vb[3] - s(6) - nl * s(H.PX["credit"]) * 1.25
    return LB.credit(s, vb[0] + s(6), y, width=w)


def ext(s, x0, y0, x1, y1, col=None):
    """Dashed construction line."""
    return H.line(s, x0, y0, x1, y1, col or O["dim"], "ref", H.DASH_REF)


def white_under(s, x1, y1, x2, y2, w=4):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#fff" '
            f'stroke-width="{s(w):.2f}" opacity="0.85"/>')


def leg_line(s, a, b, col=None, dash=None, w="geom"):
    """A model leg (contact to COM): a line with a white under-stroke so it reads over the art."""
    return white_under(s, *a, *b, w=5) + H.line(s, *a, *b, col or O["geometry"], w, dash)


def path_d(pts, close_=False):
    return "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + ("Z" if close_ else "")


def arc_pts(cx, cy, r, a0, a1, n=24):
    """Screen angles in degrees (0 = +x, + = clockwise)."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def arc_arrow(s, p, cx, cy, r, a0, a1, meaning, w=None, both=False):
    w = w or {"geometry": "geom", "dim": "ref"}.get(meaning, "force")
    return (f'<path d="{path_d(arc_pts(cx, cy, r, a0, a1))}" fill="none" stroke="{O[meaning]}" '
            f'stroke-width="{s(H.PX[w]):.2f}" marker-end="url(#{p}a_{meaning})"'
            + (f' marker-start="url(#{p}a_{meaning})"' if both else "") + '/>')


def angle_arc(s, cx, cy, r, a0, a1, col=None):
    return (f'<path d="{path_d(arc_pts(cx, cy, r, a0, a1, 16))}" fill="none" stroke="{col or O["geometry"]}" '
            f'stroke-width="{s(H.PX["geom"]):.2f}"/>')


def rect(s, x, y, w, h, fill=BOX, stroke=I["secondary"]):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{s(1.2):.2f}"/>')


def contact_mark(s, x, y):
    """Pivot / contact point: a small filled dot with a white rim."""
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(4):.2f}" fill="{I["primary"]}" stroke="#fff" '
            f'stroke-width="{s(1.5):.2f}"/>')


def xcom_mark(s, x, y):
    """Extrapolated COM: open circle (Module 7's mark)."""
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(6):.2f}" fill="#fff" stroke="{I["primary"]}" '
            f'stroke-width="{s(2):.2f}"/>')


def pvb(h):
    return (0, 0, 400, h), H.Scale(400, h, display_w=400)


def bvb(h):
    return (0, 0, 400, h), H.Scale(400, h, display_w=400, max_h=H.MAX_DISPLAY_H_BODY)


def unit(a, b):
    d = math.hypot(b[0] - a[0], b[1] - a[1])
    return ((b[0] - a[0]) / d, (b[1] - a[1]) / d)


def along(a, u, t):
    return (a[0] + u[0] * t, a[1] + u[1] * t)


# ---------------------------------------------------------------- poses (body units, hip at the origin, y down)
DC = (ELL - LB.HIP_F * H_M) * UM         # model COM above the hip: l - 0.530 H = 2.25 cm
FOOT_LEN = LB.LJ["toe"][0] - LB.LJ["heel"][0]      # heel to toe, body units (0.157 H)
PIV_FLAT = (LB.LJ["hip"][0] - LB.LJ["ankle"][0], -LB.LJ["ankle"][1])   # flat-foot pivot from the ankle: under the
                                                                          # standing hip (mid-foot)


def _solve1(f, lo, hi, n=60):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return (lo + hi) / 2


def _arms(near_fwd):
    """Arm swing opposite the legs (gait presets of lynch_body)."""
    a, b = (dict(shoulder=-22, elbow=10), dict(shoulder=22, elbow=25))
    return (a, b) if near_fwd else (b, a)


def hs_pose(alpha=ALPHA, far_knee=30.0, heel_heel=None, near=None):
    """Heel strike, near leg leading (heel contact), far leg trailing (toe contact), trunk upright.
    Default: the compass geometry, model COM C at l from both contacts at +-alpha (lead heel, trail toe).
    heel_heel=L: instead put the trailing heel's footfall (toe - foot length) L behind the lead heel."""
    sa, ca = ELL * math.sin(alpha) * UM, ELL * math.cos(alpha) * UM
    na, fa = _arms(True)

    def P(h, k, hf):
        return LB.pose(near=dict(hip=h, knee=k, contact=None, ankle=0, **na),
                       far=dict(hip=hf, knee=far_knee, contact="toe", **fa), anchor=("heel", "near"))

    def near_err(h, k):
        j = LB.pose(near=dict(hip=h, knee=k, contact=None, ankle=0), anchor=("heel", "near")).j
        return j["heel"][0] - sa, (j["heel"][1] - (-DC)) - ca    # C = (0, -DC)

    # near leg: hip flexion h and knee k so that the lead heel sits at (+sa, ca) from C
    best = None
    for k in np.arange(0, 20.01, 0.25):
        h = _solve1(lambda h: near_err(h, k)[0], 0, 45)
        e = abs(near_err(h, k)[1])
        if best is None or e < best[0]:
            best = (e, h, k)
    _, h, k = best
    if near:
        h, k = near

    def far_err(hf):
        j = P(h, k, hf).j
        if heel_heel is None:
            return (0 - j["toe_far"][0]) - sa
        return (j["heel"][0] - (j["toe_far"][0] - FOOT_LEN)) - heel_heel * UM

    ok = []
    for hf in np.arange(-45, 0.01, 0.5):          # the far toe must reach the floor
        try:
            ok.append((hf, far_err(hf)))
        except AssertionError:
            pass
    lo = next(a for (a, ea), (b, eb) in zip(ok, ok[1:]) if (ea > 0) != (eb > 0))
    hf = _solve1(far_err, lo, lo + 0.5)
    p = P(h, k, hf)
    p.C = (0.0, -DC)
    p.resid = best[0] / UM                        # m, height mismatch of the lead leg
    p.angles = (h, k, hf)
    return p


def mid_pose(theta=0.0, far=None, near_arm=None):
    """Single support on the near leg, foot flat; the model COM C at l from the mid-foot pivot at angle theta
    (rad, + = COM ahead of the pivot).  Solved: near hip flexion h and knee k so the hip is DC below C."""
    far = far or dict(hip=30, knee=60, contact=None, ankle=15)
    na, fa = _arms(theta < 0)
    na = near_arm or na

    def P(h, k):
        return LB.pose(near=dict(hip=h, knee=k, **na), far=dict(far, **fa), anchor=("heel", "near"))

    def err(h, k):
        j = P(h, k).j
        piv = (j["ankle"][0] + PIV_FLAT[0], j["ankle"][1] + PIV_FLAT[1])
        c = (0.0, -DC)
        return (c[0] - piv[0]) - ELL * math.sin(theta) * UM, (piv[1] - c[1]) - ELL * math.cos(theta) * UM

    best = None
    for k in np.arange(0, 25.01, 0.25):
        h = _solve1(lambda h: err(h, k)[0], -30, 30)
        e = abs(err(h, k)[1])
        if best is None or e < best[0]:
            best = (e, h, k)
    _, h, k = best
    p = P(h, k)
    j = p.j
    p.piv = (j["ankle"][0] + PIV_FLAT[0], j["ankle"][1] + PIV_FLAT[1])
    p.C = (0.0, -DC)
    p.resid = best[0] / UM
    p.angles = (h, k)
    return p


def body(p, s, P, q, x, fy, hf):
    """Draw pose P (stature hf figure units, facing right) with its pose point q at x and the floor at fy.
    Returns (svg, J, F); F maps any pose-frame point to figure units."""
    k = hf / LB.H_U
    ax, ay = P.anchor
    xa = x - k * (q[0] - ax)
    svg, J = LB.draw(p, s, P, xa, fy, hf)
    return svg, J, (lambda u: (xa + k * (u[0] - ax), fy + k * (u[1] - ay)))


FIGS = {}


def dim_v_out(s, p, x, ya, yb, meaning="geometry"):
    """A small vertical dimension between ya (upper) and yb (lower) with heads outside, pointing in."""
    col = O[meaning]
    return (H.line(s, x - s(6), ya, x + s(6), ya, col, "leader") + H.line(s, x - s(6), yb, x + s(6), yb, col, "leader")
            + H.arrow(s, p, x, ya - s(22), x, ya, meaning) + H.arrow(s, p, x, yb + s(22), x, yb, meaning)
            + H.line(s, x, ya, x, yb, col, "geom"))


# ================================================================ svg #28  D2 the vault height
def fig28():
    p = "m8f28_"
    VB, s = bvb(420)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy, px = 300.0, 352.0, 128.0
    P = mid_pose(0.0, far=dict(hip=25, knee=50, contact=None, ankle=10))
    svg, J, F = body(p, s, P, P.piv, px, fy, HF)
    piv, c = F(P.piv), F(P.C)
    k = HF / H_M                                          # figure units per metre
    r = ELL * k
    close(math.hypot(c[0] - piv[0], c[1] - piv[1]) / k, ELL, 0.001)
    o.append(floor(s, 8, 250, fy))
    o.append(svg)
    # the COM circle about the contact, from -alpha to +alpha (screen angles about the pivot: -90 = straight up)
    arc = arc_pts(piv[0], piv[1], r, -90 - AD, -90 + AD, 32)
    o.append(f'<path d="{path_d(arc)}" fill="none" stroke="#fff" stroke-width="{s(5):.2f}" opacity="0.85"/>')
    o.append(f'<path d="{path_d(arc)}" fill="none" stroke="{O["geometry"]}" stroke-width="{s(H.PX["geom"]):.2f}" '
             f'stroke-dasharray="{s(5):.2f} {s(3):.2f}"/>')
    e0, e1 = arc[0], arc[-1]
    o.append(leg_line(s, piv, c))
    o.append(leg_line(s, piv, e0, dash=H.DASH_REF, w="ref"))
    o.append(leg_line(s, piv, e1, dash=H.DASH_REF, w="ref"))
    # height references: midstance top and the step edges
    xr = 300.0
    o.append(ext(s, c[0] + s(9), c[1], xr + s(8), c[1]))
    o.append(ext(s, e1[0] + s(6), e1[1], xr + s(8), e1[1]))
    o.append(dim_v_out(s, p, xr, c[1], e1[1]))
    o.append(lab(s, xr + s(12), c[1] + (e1[1] - c[1]) / 2 + s(5), f"Δ{it('h')} = {DH:.4f} m", "label2"))
    o.append(angle_arc(s, piv[0], piv[1], s(46), -90, -90 + AD))
    o.append(lab(s, piv[0] + s(8), piv[1] - s(50), f"{it('α')}", "label2"))
    mid = LB.lerp(piv, c, 0.42)
    o.append(lab(s, mid[0] - s(8), mid[1], f"{it('ℓ')}", "label", anchor="end"))
    for q in (e0, e1):
        o.append(f'<circle cx="{q[0]:.2f}" cy="{q[1]:.2f}" r="{s(4):.2f}" fill="#fff" stroke="{I["primary"]}" '
                 f'stroke-width="{s(1.5):.2f}"/>')
    o.append(H.com_mark(s, *c))
    o.append(contact_mark(s, *piv))
    o.append(lab(s, piv[0] + s(8), fy + s(18), "contact", "label2"))
    o.append(lab(s, e0[0] - s(8), e0[1] + s(18), f"{it('θ')} = −{it('α')}", "label2", anchor="end"))
    o.append(lab(s, e1[0] + s(8), e1[1] + s(18), f"{it('θ')} = +{it('α')}", "label2"))
    o.append(lab(s, c[0] + s(12), c[1] - s(10), "COM", "label2"))
    # the derivation
    x0 = 236
    o.append(lines(s, x0, 24, [f"stance leg: rigid link {it('ℓ')},", "COM on a circle about", "the contact:",
                               f"{it('y')} = {it('ℓ')} cos {it('θ')}"]))
    o.append(lines(s, x0, 112, [f"midstance, {it('θ')} = 0: {it('y')} = {it('ℓ')}",
                                f"edge, {it('θ')} = ±{it('α')}: {it('y')} = {it('ℓ')} cos {it('α')}"]))
    o.append(lines(s, 214, 268, [f"Δ{it('h')} = {it('ℓ')}(1 − cos {it('α')})",
                                 f"{it('ℓ')} = {ELL} m, {it('α')} = {AD:.1f}°",
                                 f"{it('Mg')}Δ{it('h')} = {M * G * DH:.1f} J per step"]))
    o.append(credit(s, VB))
    aria = (f"A skeleton (Lynch art) at midstance, its stance leg vertical. The stance leg is a rigid link of length l "
            f"= {ELL} m from the ground contact to the centre of mass, so the COM moves on a circle of radius l about "
            f"the contact (blue dashed arc) from theta = -alpha to +alpha, alpha = {AD:.1f} degrees. Its height is y = l "
            f"cos theta: l at midstance and l cos alpha at either step edge. The difference is the vault height "
            f"Delta h = l(1 - cos alpha) = {DH:.4f} m, and Mg Delta h = {M * G * DH:.1f} J per step.")
    return finish(VB, aria, s, o)


FIGS[28] = (r'D2: Derive $\Delta h=\ell(1-\cos\alpha)$ for an inverted-pen', fig28)



def bold(t):
    return f'<tspan font-weight="bold">{t}</tspan>'


def sup(t, s, size="label2"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def dim_h(s, p, x0, x1, y, text, size="label2", meaning="geometry"):
    """Horizontal dimension with end ticks, its text below."""
    col = O[meaning]
    return (H.arrow(s, p, x0, y, x1, y, meaning, both=True) + H.line(s, x0, y - s(5), x0, y + s(5), col, "leader")
            + H.line(s, x1, y - s(5), x1, y + s(5), col, "leader")
            + lab(s, (x0 + x1) / 2, y + s(H.PX[size]) + s(3), text, size, anchor="middle"))


def bar_v(s, x, y0, w, h, col):
    return (f'<rect x="{x:.2f}" y="{y0 - h:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{col}" fill-opacity="0.85" '
            f'stroke="{col}" stroke-width="{s(1):.2f}"/>')


def signs(t, s):
    """Superscript minus / plus as tspans (the Unicode modifier signs fall back to another font)."""
    return t.replace("⁻", sup("−", s)).replace("⁺", sup("+", s))


def sb(name, s):
    """Bold vector with a subscript (F_grf, e_y)."""
    return f'{bold(name[0])}{sub(name[1:], s, "label2")}'


# ================================================================ svg #27  D1 v = cL
def fig27():
    p = "m8f27_"
    VB, s = bvb(440)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy, x_t = 240.0, 268.0, 46.0
    k = HF / H_M
    P = hs_pose(heel_heel=L_STAR, near=(22, 4), far_knee=25)
    trail = (P.j["toe_far"][0] - FOOT_LEN, P.floor_y)               # the trailing heel's footfall (pose frame)
    svg, J, F = body(p, s, P, trail, x_t, fy, HF)
    close((F(P.j["heel"])[0] - x_t) / k, L_STAR, 0.0005)
    feet = [x_t, x_t + L_STAR * k, x_t + 2 * L_STAR * k]
    o.append(floor(s, 8, 392, fy))
    o.append(svg)
    for i, x in enumerate(feet):
        o.append(contact_mark(s, x, fy) if i < 2 else
                 f'<circle cx="{x:.2f}" cy="{fy:.2f}" r="{s(4):.2f}" fill="#fff" stroke="{I["primary"]}" '
                 f'stroke-width="{s(1.5):.2f}"/>')
    yd = fy + s(22)
    for a, b in zip(feet, feet[1:]):
        o.append(dim_h(s, p, a, b, yd, f'{it("L")} = {L_STAR:.4f} m'))
    yt = yd + s(40)
    for x, t, n in zip(feet, (f'{it("t")} = 0', f'{it("t")} = 1/{it("c")}', f'{it("t")} = 2/{it("c")}'),
                       ("heel strike", "heel strike (now)", "next")):
        o.append(lab(s, x, yt, t, "label2", anchor="middle"))
        o.append(lab(s, x, yt + s(18), n, "label2", I["secondary"], "middle"))
    o.append(dim_h(s, p, feet[0], feet[2], yt + s(40), f'stride {it("L")}{sub("s", s, "label2")} = 2{it("L")} '
                   f'in 2/{it("c")} = {2 / CAD:.3f} s', meaning="dim"))
    x0 = 214
    o.append(lines(s, x0, 26, [f'cadence {it("c")} = {CAD:.2f} steps/s', f'({CAD * 60:.0f} steps per minute)',
                               f'step length {it("L")} = {L_STAR:.4f} m']))
    o.append(lines(s, x0, 98, [f'each step: forward {it("L")} in 1/{it("c")}', f'1/{it("c")} = {1 / CAD:.3f} s per step',
                               f'{it("v")} = {it("L")}/(1/{it("c")}) = {it("cL")}',
                               f'= {CAD:.2f} × {L_STAR:.4f} = {CAD * L_STAR:.2f} m/s']))
    close(CAD * L_STAR, V, 1e-9)
    o.append(credit(s, VB))
    aria = (f"A skeleton (Lynch art) at heel strike, walking to the right. The floor shows three successive heel "
            f"strikes, each one step length L = {L_STAR:.4f} m ahead of the last: the trailing foot's at t = 0, the "
            f"leading foot's now at t = 1/c, and the next one at t = 2/c. With cadence c = {CAD:.2f} steps per second "
            f"({CAD * 60:.0f} per minute) each step takes 1/c = {1 / CAD:.3f} s, so the speed is v = L/(1/c) = cL = "
            f"{CAD:.2f} x {L_STAR:.4f} = {V} m/s. One stride is 2L in 2/c = {2 / CAD:.3f} s, the same speed.")
    return finish(VB, aria, s, o)


# ================================================================ svg #29  D3 the Froude number
def fig29():
    p = "m8f29_"
    VB, s = bvb(530)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy, px = 280.0, 330.0, 100.0
    P = mid_pose(0.0, far=dict(hip=25, knee=50, contact=None, ankle=10))
    svg, J, F = body(p, s, P, P.piv, px, fy, HF)
    piv, c = F(P.piv), F(P.C)
    N = W * (1 - FR)                                     # Prop 2.2 (line 247)
    acc = V * V / ELL
    close(acc, 1.78, 0.005)
    fk = 72 / W                                          # px per newton
    o.append(floor(s, 8, 210, fy))
    o.append(svg)
    o.append(leg_line(s, piv, c, dash=H.DASH_REF, w="ref"))
    o.append(lab(s, piv[0] - s(8), fy - s(34), it("ℓ"), "label", anchor="end"))
    o.append(H.arrow(s, p, c[0], c[1] + s(8), c[0], c[1] + s(8) + W * fk, "load"))
    o.append(lab(s, c[0] + s(7), c[1] + s(8) + W * fk - s(2), f'{it("Mg")} = {W:.0f} N', "label2"))
    o.append(H.arrow(s, p, piv[0], fy + N * fk, piv[0], fy + s(2), "reaction"))
    o.append(lab(s, piv[0] + s(8), fy + N * fk - s(4), f'{it("N")} = {N:.0f} N', "label2"))
    o.append(H.arrow(s, p, c[0] + s(9), c[1], c[0] + s(9) + V * 42, c[1], "geometry"))
    o.append(lab(s, c[0] + s(12), c[1] - s(8), f'{it("v")} = {V} m/s', "label2"))
    o.append(H.arrow(s, p, c[0] - s(12), c[1] - s(2), c[0] - s(12), c[1] - s(2) + acc * 22, "geometry"))
    o.append(lines(s, c[0] - s(18), c[1] + s(10), [f'{it("v")}²/{it("ℓ")} =', f'{acc:.2f} m/s²'], anchor="end"))
    o.append(H.com_mark(s, *c))
    o.append(contact_mark(s, *piv))
    x0 = 226
    o.append(lines(s, x0, 24, ["at midstance the COM moves", f'on a circle of radius {it("ℓ")} about',
                               "the contact, so it accelerates", f'{it("v")}²/{it("ℓ")} downward']))
    o.append(lines(s, x0, 104, [f'vertical: {it("Mg")} − {it("N")} = {it("Mv")}²/{it("ℓ")}',
                                f'{it("N")} = {it("M")}({it("g")} − {it("v")}²/{it("ℓ")}) ≥ 0',
                                f'⇒ {it("v")}² ≤ {it("gℓ")}']))
    o.append(lines(s, x0, 166, [f'[{it("v")}²] = [{it("gℓ")}] = m²/s²:', f'Fr = {it("v")}²/({it("gℓ")}) has no units,',
                                f'{it("N")}/{it("Mg")} = 1 − Fr']))
    o.append(lines(s, x0, 228, [f'{it("ℓ")} = {ELL} m, {it("v")} = {V} m/s:', f'{it("N")} = {1 - FR:.3f} {it("Mg")}']))
    # Froude scale: Fr from 0 to 1 with the module's three marks
    lx0, lx1, ly = 40.0, 372.0, 458.0
    X = lambda f: lx0 + f * (lx1 - lx0)  # noqa: E731
    o.append(lab(s, lx0, ly - s(52), f'Froude number Fr = {it("v")}²/({it("gℓ")}), {it("ℓ")} = {ELL} m', "label2"))
    o.append(H.line(s, lx0, ly, lx1, ly, I["axis"], "axis"))
    for f in np.linspace(0, 1, 11):
        o.append(H.line(s, X(f), ly, X(f), ly + s(5), I["axis"], "leader"))
    for f in (0, 0.5, 1):
        o.append(plabel(s, X(f), ly + s(19), f"{f:g}", "tick", I["secondary"], "middle"))
    v05, v1 = math.sqrt(0.5 * G * ELL), math.sqrt(G * ELL)
    for f, col in ((FR, SER[0]), (0.5, SER[1]), (1.0, SER[2])):
        o.append(f'<circle cx="{X(f):.2f}" cy="{ly:.2f}" r="{s(H.PX["dot"]):.2f}" fill="{col}" stroke="#fff" '
                 f'stroke-width="{s(1.5):.2f}"/>')
    o.append(lab(s, X(FR) - s(8), ly - s(12), f'{FR:.3f}: {V} m/s, reference', "label2"))
    o.append(lab(s, X(0.5), ly - s(30), f'0.5: {v05:.2f} m/s, walk–run', "label2", anchor="middle"))
    o.append(lab(s, X(1.0), ly - s(12), f'{v1:.2f} m/s: {it("N")} = 0', "label2", anchor="end"))
    o.append(credit(s, VB))
    pts = [[X(f), ly, f"Fr {f:.2f}: v = {math.sqrt(f * G * ELL):.2f} m/s, N = {1 - f:.2f} Mg at midstance"]
           for f in np.linspace(0, 1, 101)]
    aria = (f"A skeleton (Lynch art) at midstance, stance leg vertical, its centre of mass at l = {ELL} m above the "
            f"contact and moving forward at v = {V} m/s. On the circle of radius l about the contact the COM "
            f"accelerates v^2/l = {acc:.2f} m/s^2 downward. Forces: weight Mg = {W:.0f} N down at the COM, ground "
            f"reaction N up at the contact. Vertical Newton: Mg - N = Mv^2/l, so N = M(g - v^2/l) >= 0 requires v^2 "
            f"<= g l. v^2 and g l both have units m^2/s^2, so Fr = v^2/(g l) is the dimensionless speed and N/Mg = 1 - "
            f"Fr. A Froude scale from 0 to 1 marks the reference gait, Fr = {FR:.3f} at {V} m/s (N = {N:.0f} N), the "
            f"walk-run switch near Fr = 0.5 at {v05:.2f} m/s, and Fr = 1 at {v1:.2f} m/s, where N reaches zero.")
    return finish(VB, aria, s, o, extra=H.hover_attr([lx0, ly - s(12), lx1, ly + s(12)], pts))


# ================================================================ svg #30  D4 F_grf = M a + Mg e_y
TH30 = -12.0                              # deg, early single support (one of K1's angles, line 873)


def fig30():
    p = "m8f30_"
    VB, s = bvb(490)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy, px = 280.0, 340.0, 150.0
    th = math.radians(TH30)
    P = mid_pose(th, far=dict(hip=-16, knee=45, contact=None, ankle=-20))
    svg, J, F = body(p, s, P, P.piv, px, fy, HF)
    piv, c = F(P.piv), F(P.C)
    n, fx, fyy = k1_fy(th)
    close(fyy / W, 0.737, 0.0005)                          # K1 solution, alpha = 12 deg
    assert fx < 0                                          # braking while the COM is behind the contact
    max_, may = fx, fyy - W                                # M a = F - Mg e_y (newtons, y up)
    a_mag = math.hypot(max_, may) / M
    fk = 105 / W
    o.append(floor(s, 8, 250, fy))
    o.append(svg)
    o.append(leg_line(s, piv, c, dash=H.DASH_REF, w="ref"))
    o.append(ext(s, piv[0], fy - s(4), piv[0], fy - s(60)))
    tip = along(piv, unit(piv, c), n * fk)
    o.append(H.arrow(s, p, *piv, *tip, "reaction"))
    o.append(lab(s, tip[0] + s(8), tip[1] + s(10), sb("Fgrf", s), "label2"))
    o.append(H.arrow(s, p, c[0], c[1] + s(8), c[0], c[1] + s(8) + W * fk, "load"))
    o.append(lab(s, c[0] - s(7), c[1] + s(8) + W * fk - s(4), f'−{it("Mg")}{sb("ey", s)}', "label2", anchor="end"))
    o.append(H.com_mark(s, *c))
    o.append(lab(s, c[0] - s(10), c[1] - s(10), "COM", "label2", anchor="end"))
    o.append(contact_mark(s, *piv))
    o.append(lab(s, piv[0] + s(6), fy + s(18), "contact (COP)", "label2"))
    o.append(angle_arc(s, piv[0], piv[1], s(40), -90, -90 + TH30))
    o.append(lab(s, piv[0] + s(6), piv[1] - s(44), f'{it("θ")} = {mn(f"{TH30:.0f}")}°', "label2"))
    # vector sum, tip to tail, same scale as the body arrows
    ox, oy = 318.0, 408.0
    q1 = (ox + max_ * fk, oy - may * fk)
    q2 = (q1[0], q1[1] - W * fk)
    close(q2[0], ox + fx * fk, 1e-6)
    close(q2[1], oy - fyy * fk, 1e-6)
    o.append(H.arrow(s, p, ox, oy, *q1, "geometry"))
    o.append(H.arrow(s, p, *q1, *q2, "load"))
    o.append(H.arrow(s, p, ox, oy, *q2, "reaction"))
    o.append(f'<circle cx="{ox:.2f}" cy="{oy:.2f}" r="{s(2.5):.2f}" fill="{I["primary"]}"/>')
    o.append(lab(s, ox + s(8), oy + s(16), f'{it("M")}{bold("a")} = {M * a_mag:.0f} N', "label2"))
    o.append(lines(s, q1[0] - s(8), (q1[1] + q2[1]) / 2 + s(4), [f'+{it("Mg")}{sb("ey", s)}', f'= {W:.0f} N'],
                   anchor="end"))
    o.append(lab(s, ox + s(10), (oy + q2[1]) / 2, f'{sb("Fgrf", s)} = {n:.0f} N', "label2"))
    o.append(lab(s, 392, q2[1] - s(14), "the sum, same scale", "label2", I["secondary"], "end"))
    x0 = 222
    o.append(lines(s, x0, 24, ["external forces on the body:", f'the ground reaction {sb("Fgrf", s)}',
                               f'and the weight −{it("Mg")}{sb("ey", s)}', "(air resistance neglected)"]))
    o.append(lines(s, x0, 104, [f'Newton: {sb("Fgrf", s)} − {it("Mg")}{sb("ey", s)} = {it("M")}{bold("a")}',
                                f'{sb("Fgrf", s)} = {it("M")}{bold("a")} + {it("Mg")}{sb("ey", s)}',
                                f'{bold("a")} = d²{bold("r")}{sub("com", s, "label2")}/d{it("t")}²']))
    o.append(lines(s, x0, 166, [f'rigid vault of K1 at {it("θ")} = {mn(f"{TH30:.0f}")}°,',
                                f'{it("v")}{sub("mid", s, "label2")} = {V} m/s:',
                                f'{it("F")}{sub("x", s, "label2")} = {mn(f"{fx:.0f}")} N (braking)',
                                f'{it("F")}{sub("y", s, "label2")} = {fyy:.0f} N = {fyy / W:.3f} {it("Mg")}',
                                f'|{bold("a")}| = {a_mag:.2f} m/s²']))
    o.append(credit(s, VB))
    aria = (f"A skeleton (Lynch art) early in single support, the centre of mass {abs(TH30):.0f} degrees behind the "
            f"stance contact. Two external forces act on the whole body: the ground reaction F_grf at the contact, "
            f"along the leg toward the COM, and the weight -Mg e_y at the COM. Newton's law gives F_grf - Mg e_y = M a, "
            f"so F_grf = M a + Mg e_y; a vector triangle on the same scale adds M a ({M * a_mag:.0f} N) and +Mg e_y "
            f"({W:.0f} N) tip to tail to give F_grf ({n:.0f} N). Values from the rigid vault of K1 at a midstance speed "
            f"of {V} m/s: F_x = {fx:.0f} N (braking), F_y = {fyy:.0f} N = {fyy / W:.3f} Mg, |a| = {a_mag:.2f} m/s^2.")
    return finish(VB, aria, s, o)


# ================================================================ svg #31  D5 relabelling at heel strike
def fig31():
    p = "m8f31_"
    VB, s = bvb(450)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 190.0, 236.0
    P = hs_pose()
    vk = 44.0                                             # px per m/s
    v_after = V * math.cos(2 * ALPHA)
    for i, (x, title) in enumerate(((96.0, "just before heel strike"), (300.0, "just after heel strike"))):
        svg, J, F = body(p, s, P, P.C, x, fy, HF)
        c, heel, toe = F(P.C), F(P.j["heel"]), F(P.j["toe_far"])
        close(math.hypot(heel[0] - c[0], heel[1] - c[1]) / (HF / H_M), ELL, 0.002)
        close(math.hypot(toe[0] - c[0], toe[1] - c[1]) / (HF / H_M), ELL, 0.002)
        o.append(floor(s, x - 90, x + 92, fy))
        o.append(svg)
        st, sw = (toe, heel) if i == 0 else (heel, toe)
        o.append(leg_line(s, st, c))
        o.append(leg_line(s, sw, c, dash=H.DASH_REF, w="ref"))
        o.append(ext(s, c[0], c[1] + s(10), c[0], fy - s(2)))
        o.append(contact_mark(s, *st))
        u = unit(st, c)                                    # stance leg, contact to COM
        d = (-u[1], u[0]) if -u[1] > 0 else (u[1], -u[0])  # perpendicular to it, pointing forward
        vv = V if i == 0 else v_after
        o.append(H.arrow(s, p, c[0] + d[0] * s(8), c[1] + d[1] * s(8), c[0] + d[0] * (s(8) + vv * vk),
                         c[1] + d[1] * (s(8) + vv * vk), "geometry"))
        tip = (c[0] + d[0] * (s(14) + vv * vk), c[1] + d[1] * (s(14) + vv * vk))
        o.append(lab(s, tip[0], tip[1] + (s(14) if i == 0 else s(-2)), f'{it("v")}{"⁻" if i == 0 else "⁺"}', "label2"))
        o.append(H.com_mark(s, *c))
        o.append(lab(s, x, 20, title, "label2", anchor="middle"))
        sl = "⁻" if i == 0 else "⁺"
        o.append(lab(s, st[0] + (s(-6) if i == 0 else s(6)), fy + s(18), f'stance {it("θ")}{sl}', "label2",
                     anchor="end" if i == 0 else "start"))
        o.append(lab(s, sw[0] + (s(6) if i == 0 else s(-6)), fy + s(18), f'swing {it("φ")}{sl}', "label2",
                     anchor="start" if i == 0 else "end"))
    dt = f'd{it("θ")}/d{it("t")}'
    rows = [f'angles from the vertical, + = COM ahead of that leg’s foot;',
            f'before: {it("θ")}⁻ = +{it("α")}, {it("φ")}⁻ = −{it("α")};  after: {it("θ")}⁺ = {it("φ")}⁻ = −{it("α")}, '
            f'{it("φ")}⁺ = {it("θ")}⁻ = +{it("α")}',
            "the impulse acts at the new contact, so the angular",
            f'momentum about it is kept: {it("Mℓ")}{it("v")}⁻ cos 2{it("α")} = {it("Mℓ")}{it("v")}⁺,',
            f'({dt})⁺ = ({dt})⁻ cos 2{it("α")} = {math.cos(2 * ALPHA):.3f} ({dt})⁻',
            f'2{it("α")} = {2 * AD:.1f}°: {it("v")}⁻ = {V} m/s → {it("v")}⁺ = {v_after:.3f} m/s,',
            f'kinetic energy kept: cos² 2{it("α")} = {math.cos(2 * ALPHA) ** 2:.3f}']
    o.append(lines(s, 14, 280, rows))
    o.append(credit(s, VB))
    o = [signs(x, s) for x in o]
    aria = (f"Two copies of the same skeleton (Lynch art) at heel strike, drawn as the compass walker: both legs of "
            f"length l = {ELL} m from the centre of mass to the contacts, inter-leg angle 2 alpha = {2 * AD:.1f} "
            f"degrees. Left, just before: the trailing leg is the stance leg (solid blue, pivot dot at the trailing "
            f"toe), theta- = +alpha, and the leading leg is the swing leg, phi- = -alpha; the COM velocity v- = {V} m/s "
            f"is perpendicular to the trailing leg. Right, just after: the leading foot is the new pivot; the labels "
            f"swap, theta+ = phi- = -alpha and phi+ = theta- = +alpha. The impact impulse acts at the new contact, so "
            f"angular momentum about it is conserved: (dtheta/dt)+ = (dtheta/dt)- cos 2 alpha = "
            f"{math.cos(2 * ALPHA):.3f} (dtheta/dt)-, and v+ = {v_after:.3f} m/s is perpendicular to the new stance leg.")
    return finish(VB, aria, s, o)


# ================================================================ svg #32  D6 the redirection loss
def fig32():
    p = "m8f32_"
    VB, s = bvb(420)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy, px = 300.0, 352.0, 126.0
    P = hs_pose()
    svg, J, F = body(p, s, P, P.C, px, fy, HF)
    c, heel, toe = F(P.C), F(P.j["heel"]), F(P.j["toe_far"])
    o.append(floor(s, 8, 260, fy))
    o.append(svg)
    o.append(leg_line(s, toe, c, dash=H.DASH_REF, w="ref"))
    o.append(leg_line(s, heel, c))
    o.append(contact_mark(s, *toe))
    o.append(contact_mark(s, *heel))
    o.append(lab(s, toe[0], fy + s(18), "old contact", "label2", anchor="middle"))
    o.append(lab(s, heel[0], fy + s(18), "new contact", "label2", anchor="middle"))
    vk = 92.0                                              # px per m/s
    vm = (math.cos(ALPHA), math.sin(ALPHA))                # v-: perpendicular to the old leg, forward and down
    tn = (math.cos(ALPHA), -math.sin(ALPHA))               # new admissible tangent: perpendicular to the new leg
    nl = (math.sin(ALPHA), math.cos(ALPHA))                # along the new leg, COM to the new contact
    kept, lost = V * math.cos(2 * ALPHA), V * math.sin(2 * ALPHA)
    close(vm[0] * nl[0] + vm[1] * nl[1], math.sin(2 * ALPHA), 1e-12)
    pv, pk = along(c, vm, V * vk), along(c, tn, kept * vk)
    close(math.hypot(pv[0] - pk[0], pv[1] - pk[1]) / vk, lost, 1e-9)
    o.append(H.arrow(s, p, *c, *pv, "geometry"))
    o.append(H.arrow(s, p, *pk, *pv, "flag"))
    o.append(H.line(s, *c, *pk, O["geometry"], "geom", (5, 3), extra=f'marker-end="url(#{p}a_geometry)"'))
    o.append(angle_arc(s, c[0], c[1], s(52), -AD, AD))
    o.append(lab(s, c[0] + s(57), c[1] + s(5), f'2{it("α")}', "label2"))
    o.append(lab(s, pv[0] + s(6), pv[1] + s(16), f'{it("v")}⁻ = {V} m/s, ⊥ old leg', "label2"))
    o.append(lab(s, pk[0] + s(6), pk[1] - s(6), f'kept: {it("v")} cos 2{it("α")} = {kept:.3f} m/s', "label2"))
    mid = LB.lerp(pk, pv, 0.45)
    o.append(lines(s, mid[0] + s(10), mid[1] - s(8), [f'lost: {it("v")} sin 2{it("α")}', f'= {lost:.3f} m/s,',
                                               "along the new leg"]))
    o.append(H.com_mark(s, *c))
    u = unit(heel, c)
    hi = along(heel, u, s(46))
    o.append(H.arrow(s, p, *along(heel, u, s(8)), *hi, "force"))
    o.append(lines(s, hi[0] + s(10), hi[1] + s(8), ["heel-strike impulse,", "along the new leg"]))
    o = [signs(x, s) for x in o]
    o.append(lines(s, 230, 24, ["perfectly inelastic heel strike:", "the new leg stops the velocity",
                                "component along itself",
                                f'{it("E")}{sub("loss", s, "label2")} = ½{it("M")}({it("v")} sin 2{it("α")})²',
                                f'= ½{it("Mv")}² sin²(2{it("α")}) = {E_LOSS:.1f} J',
                                f'{it("M")} = {M:.0f} kg, 2{it("α")} = {2 * AD:.1f}°']))
    o.append(credit(s, VB))
    aria = (f"A skeleton (Lynch art) at heel strike, drawn as the compass walker with inter-leg angle 2 alpha = "
            f"{2 * AD:.1f} degrees. Just before the strike the centre-of-mass velocity v- = {V} m/s (blue) is "
            f"perpendicular to the old (trailing) leg. The new leg admits only motion perpendicular to itself, a "
            f"direction turned 2 alpha from v-. Split v- into the kept part along that tangent, v cos 2 alpha = "
            f"{kept:.3f} m/s (blue dashed), and the part along the new leg, v sin 2 alpha = {lost:.3f} m/s (orange), "
            f"which the heel-strike impulse along the new leg (red) removes. The perfectly inelastic collision "
            f"destroys its kinetic energy: E_loss = 1/2 M v^2 sin^2(2 alpha) = {E_LOSS:.1f} J at M = {M:.0f} kg.")
    return finish(VB, aria, s, o)


# ================================================================ svg #33  D7 joint power
def lab3():
    """Lab 3 (lines 718-733), ported line for line."""
    W_, T_ = M * G, 2 * L_STAR / V
    T_st = 0.62 * T_
    sv = np.linspace(0, 1, 601)
    t = sv * T_st
    shape = np.sin(np.pi * sv) ** 0.40 * (1 - 0.245 * np.cos(4 * np.pi * (sv - 0.5)))
    Fy = shape * (W_ * T_ / 2) / np.trapezoid(shape, t)
    x_cop = -0.06 + 0.25 * sv
    tau = Fy * x_cop
    om = 2.3 * np.exp(-((sv - 0.80) / 0.10) ** 2)
    return sv, t, tau, om, tau * om


def fig33():
    p = "m8f33_"
    VB, s = bvb(420)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    sv, t, tau, om, Pw = lab3()
    i = int(np.argmax(Pw))
    close(tau.max(), 95.1, 0.05)                                   # line 737
    close(sv[int(np.argmax(tau))] * 100, 77, 0.5)
    close(Pw.max(), 214, 0.5)
    close(Pw.max() / M, 3.06, 0.005)
    close(sv[i] * 100, 79, 0.5)
    close(np.trapezoid(np.maximum(Pw, 0), t), 22.5, 0.05)
    HF, fy, px = 300.0, 352.0, 200.0
    P = LB.pose(near=dict(hip=-14, knee=28, contact="toe", shoulder=24, elbow=25),
                far=dict(hip=24, knee=5, contact=None, ankle=0, shoulder=-22, elbow=10), anchor=("heel", "far"))
    svg, J, F = body(p, s, P, P.j["hip"], px, fy, HF)
    a = J["ankle"]
    o.append(floor(s, 8, 300, fy))
    o.append(svg)
    o.append(arc_arrow(s, p, a[0], a[1], s(33), -150, 20, "force"))
    o.append(arc_arrow(s, p, a[0], a[1], s(20), -140, 0, "geometry"))
    o.append(H.joint_centre(s, *a))
    o.append(lines(s, a[0] - s(26), a[1] - s(44), [f'{it("τ")}: plantar-', "flexor torque"], anchor="end"))
    o.append(lines(s, a[0] + s(36), a[1] - s(2), [f'd{it("θ")}/d{it("t")}: plantar-', "flexion rate"]))
    o.append(lab(s, a[0], fy + s(20), "ankle", "label2", anchor="middle"))
    x0 = 232
    o.append(lines(s, x0, 24, [f'a torque {it("τ")} turning a joint', f'through d{it("θ")} does the work',
                               f'd{it("W")} = {it("τ")} d{it("θ")}; divide by d{it("t")}:']))
    o.append(lab(s, x0, 94, f'{it("P")}{sub("j", s)} = {it("τ")}{sub("j", s)} d{it("θ")}{sub("j", s)}/d{it("t")}'))
    o.append(lines(s, x0, 122, [f'{it("τ")} and d{it("θ")}/d{it("t")} in the same', f'sense: {it("P")} > 0, the ankle',
                                "does work on the body", "(opposite: the joint absorbs)"]))
    o.append(lines(s, x0, 210, [f'Lab 3, {sv[i] * 100:.0f} % of stance', "(push-off):", f'{it("τ")} = {tau[i]:.1f} N m',
                                f'd{it("θ")}/d{it("t")} = {om[i]:.2f} rad/s', f'{it("P")} = {Pw[i]:.0f} W',
                                f'= {Pw[i] / M:.2f} W/kg']))
    o.append(credit(s, VB))
    aria = (f"A skeleton (Lynch art) at push-off: the near (trailing) foot rolls on its toes while the far foot "
            f"reaches forward. At the near ankle a red curved arrow is the plantarflexor torque tau and a blue curved "
            f"arrow, in the same sense, the plantarflexion rate dtheta/dt. A torque turning a joint through dtheta does "
            f"work dW = tau dtheta; dividing by dt gives the joint power P_j = tau_j dtheta_j/dt, positive when torque "
            f"and rate share a sense (the joint does work) and negative when they oppose (it absorbs). Lab 3 at "
            f"{sv[i] * 100:.0f} % of stance: tau = {tau[i]:.1f} N m, dtheta/dt = {om[i]:.2f} rad/s, P = {Pw[i]:.0f} W "
            f"= {Pw[i] / M:.2f} W/kg.")
    return finish(VB, aria, s, o)


# ================================================================ svg #34  D8 the optimal step length
def foc(L):
    """The two sides of the D8 first-order condition (1/m)."""
    a = np.arcsin(np.asarray(L) / (2 * ELL))
    return np.sin(2 * a) * np.cos(2 * a) / (ELL * np.cos(a)), 2 * KAPPA / np.asarray(L) ** 3


def fig34():
    p = "m8f34_"
    VB, s = pvb(530)
    o = []
    Ls = np.linspace(0.35, 0.95, 241)
    tr, sw = cost(Ls)
    tot = tr + sw
    lh, rh = foc(Ls)
    lhs0, rhs0 = (float(v) for v in foc(L_OPT))
    close(lhs0, rhs0, 1e-6)                                        # the root of the condition is the minimum
    c_opt = float(sum(cost(L_OPT)))
    pa = Plot(s, (60, 46, 384, 236), (0.35, 0.95), (0, 100))
    pb = Plot(s, (60, 318, 384, 456), (0.35, 0.95), (0, 1.5))
    xt = [(v, f"{v:.1f}") for v in (0.4, 0.5, 0.6, 0.7, 0.8, 0.9)]
    o.append(pa.axes(xt, [(v, f"{v:g}") for v in (0, 25, 50, 75, 100)], "step length L (m)", "C per step (J)",
                     grid=(25, 50, 75, 100)))
    o.append(pb.axes(xt, [(v, f"{v:g}") for v in (0, 0.5, 1.0, 1.5)], "step length L (m)", "each side (1/m)",
                     grid=(0.5, 1.0, 1.5)))
    for P_, yr in ((pa, (0, 100)), (pb, (0, 1.5))):
        o.append(H.line(s, P_.X(L_OPT), P_.Y(yr[0]), P_.X(L_OPT), P_.Y(yr[1]), O["dim"], "ref", H.DASH_REF))
    o.append(pa.curve(Ls, tr, SER[1], multi=True))
    o.append(pa.curve(Ls, sw, SER[2], multi=True))
    o.append(pa.curve(Ls, tot, SER[0]))
    o.append(pa.dot(L_OPT, c_opt, SER[0]))
    f_tot = lambda L: float(sum(cost(L)))  # noqa: E731
    o.append(plabel(s, pa.X(L_OPT) + 6, pa.Y(c_opt) - 20, f"L* = {L_OPT:.3f} m, {c_opt:.1f} J", "label2"))
    o.append(plabel(s, pa.X(0.47), pa.Y(f_tot(0.47)) - 8, "total C", "label2"))
    o.append(plabel(s, pa.X(0.80), pa.Y(float(cost(0.80)[0])) + 18, "transition", "label2"))
    o.append(plabel(s, pa.X(0.86), pa.Y(float(cost(0.86)[1])) + 16, "swing", "label2", anchor="middle"))
    o.append(legend(s, 60, 20, [(SER[0], "total", None), (SER[1], "½Mv² sin²2α", None), (SER[2], "κM(v/L)²", None)],
                    gap=12))
    m = rh <= 1.5
    o.append(pb.curve(Ls, lh, SER[0], multi=True))
    o.append(pb.curve(Ls[m], rh[m], SER[1], multi=True))
    o.append(pb.dot(L_OPT, lhs0, I["primary"]))
    o.append(plabel(s, pb.X(0.86), pb.Y(float(foc(0.86)[0])) - 8, "left side", "label2", anchor="middle"))
    o.append(plabel(s, pb.X(0.55) + 12, pb.Y(float(foc(0.55)[1])) + 2, "right side", "label2"))
    o.append(plabel(s, pb.X(L_OPT) - 6, pb.Y(0.12), f"cross at L* = {L_OPT:.3f} m", "label2", anchor="end"))
    o.append(plabel(s, 384, pb.Y(1.38), "Mv² cancels:", "label2", anchor="end"))
    o.append(plabel(s, 384, pb.Y(1.38) + 17, "same L* at every v", "label2", anchor="end"))
    o.append(legend(s, 60, 292, [(SER[0], "sin 2α cos 2α/(ℓ cos α)", None), (SER[1], "2κ/L³", None)], gap=14))
    o.append(plabel(s, 200, 522, f"M = {M:.0f} kg, ℓ = {ELL} m, v = {V} m/s, κ = {KAPPA} m²", "label2", I["secondary"],
                    "middle"))
    ha = [[pa.X(L), [pa.Y(a), pa.Y(b), pa.Y(a + b)], f"L {L:.3f} m: transition {a:.1f}, swing {b:.1f}, total {a + b:.1f} J"]
          for L, a, b in zip(Ls, tr, sw)]
    hb = [[pb.X(L), [pb.Y(a), pb.Y(min(b, 1.5))], f"L {L:.3f} m: left {a:.3f}, right {b:.3f} 1/m"]
          for L, a, b in zip(Ls, lh, rh)]
    aria = (f"Two plots against step length L from 0.35 to 0.95 m at M = {M:.0f} kg, l = {ELL} m, v = {V} m/s, kappa = "
            f"{KAPPA} m^2. Top: the per-step cost proxy C(L) (red) is the transition term 1/2 M v^2 sin^2(2 arcsin(L/2l)) "
            f"(blue), rising with L, plus the swing term kappa M (v/L)^2 (orange), falling; the total has one minimum "
            f"in this range, L* = {L_OPT:.3f} m with C = {c_opt:.1f} J. Bottom: the two sides of the first-order "
            f"condition dC/dL = 0, sin 2 alpha cos 2 alpha / (l cos alpha) (red) and 2 kappa / L^3 (blue), cross at "
            f"the same L*; M v^2 has cancelled, so L* does not depend on speed.")
    return finish(VB, aria, s, o, extra=H.hover_attr([(pa.box, ha), (pb.box, hb)]))


# ================================================================ svg #35  D9 the capture inequality
X35, XD35, REACH = 0.03, 0.45, 0.415     # m, m/s, m (Lab 4 reference perturbation, line 644)


def lip(t, x0, xd0):
    """Linear inverted pendulum about a contact: x(t) = A e^(w t) + B e^(-w t) (Prop 10.1, line 639)."""
    A, B = 0.5 * (x0 + xd0 / W0), 0.5 * (x0 - xd0 / W0)
    return A * np.exp(W0 * t) + B * np.exp(-W0 * t)


def fig35():
    p = "m8f35_"
    VB, s = bvb(690)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    xi = X35 + XD35 / W0
    close(XD35 / W0, 0.140, 0.0005)                       # line 644
    close(xi + XD35 * 0.20, 0.260, 0.0005)                # line 644 (with the 0.20 s delay)
    close(REACH - (xi + XD35 * 0.20), 0.155, 0.0005)
    HF, fy, px = 196.0, 222.0, 70.0
    P = mid_pose(math.asin(X35 / ELL), far=dict(hip=28, knee=40, contact=None, ankle=5))
    svg, J, F = body(p, s, P, P.piv, px, fy, HF)
    piv, c = F(P.piv), F(P.C)
    o.append(floor(s, 8, 180, fy))
    o.append(svg)
    o.append(leg_line(s, piv, c))
    o.append(lab(s, piv[0] - s(5), fy - s(40), it("ℓ"), "label", anchor="end"))
    o.append(H.arrow(s, p, c[0] + s(9), c[1], c[0] + s(9) + XD35 * 80, c[1], "geometry"))
    o.append(lab(s, c[0] + s(12), c[1] - s(8), f'd{it("x")}/d{it("t")}', "label2"))
    o.append(lab(s, c[0] + s(12), c[1] + s(20), "COM", "label2"))
    o.append(H.com_mark(s, *c))
    o.append(contact_mark(s, *piv))
    dt = f'd{it("x")}/d{it("t")}'
    o.append(lines(s, 192, 24, ["linear inverted pendulum about", f'the new contact, ω₀ = √({it("g")}/{it("ℓ")}):',
                                f'd²{it("x")}/d{it("t")}² = ω₀²{it("x")}',
                                f'{it("x")} = {it("A")} exp(ω₀{it("t")}) + {it("B")} exp(−ω₀{it("t")})',
                                f'{it("A")} = ½({it("x")}₀ + ({dt})₀/ω₀)']))
    o.append(lines(s, 192, 116, [f'the {it("B")} term decays; the motion',
                                 f'stays bounded iff {it("A")} ≤ 0:',
                                 f'ξ = {it("x")} + ({dt})/ω₀ ≤ {it("x")}{sub("p", s, "label2")} ≤ '
                                 f'{it("x")}{sub("s", s, "label2")}{sup("max", s)}',
                                 "one step recovers iff ξ is", "within reach"]))
    # magnified floor, from the stance contact
    X = lambda m: 40 + m / 0.45 * 340  # noqa: E731
    ys = 318.0
    o.append(lab(s, 40, ys - s(58), "floor magnified: distance ahead of the stance contact (m)", "label2",
                 I["secondary"]))
    o.append(f'<rect x="{X(xi):.2f}" y="{ys - s(14):.2f}" width="{X(REACH) - X(xi):.2f}" height="{s(14):.2f}" '
             f'fill="{O["geometry"]}" fill-opacity="0.14"/>')
    o.append(H.line(s, X(0), ys, X(0.45), ys, I["axis"], "axis"))
    for v in np.arange(0, 0.451, 0.05):
        o.append(H.line(s, X(v), ys, X(v), ys + s(5), I["axis"], "leader"))
        if abs(v * 10 - round(v * 10)) < 1e-9:
            o.append(plabel(s, X(v), ys + s(19), f"{v:.1f}", "tick", I["secondary"], "middle"))
    o.append(contact_mark(s, X(0), ys))
    o.append(H.com_mark(s, X(X35), ys - s(28)))
    o.append(H.line(s, X(X35), ys - s(21), X(X35), ys, I["rule"], "leader"))
    o.append(lab(s, X(X35) + s(10), ys - s(24), f'{it("x")} = {X35} m', "label2"))
    o.append(xcom_mark(s, X(xi), ys))
    o.append(lab(s, X(xi), ys + s(38), f'ξ = {xi:.3f} m', "label2", anchor="middle"))
    o.append(H.line(s, X(REACH), ys - s(16), X(REACH), ys + s(4), O["force"], "force"))
    o.append(lab(s, 392, ys + s(38), f'{it("x")}{sub("s", s, "label2")}{sup("max", s)} = {REACH} m', "label2",
                 anchor="end"))
    o.append(lab(s, (X(xi) + X(REACH)) / 2, ys - s(20), "the new contact may land here", "label2", anchor="middle"))
    o.append(lab(s, 40, ys + s(60), f'{dt} = {XD35} m/s, ω₀ = {W0:.2f} s⁻¹: ξ = {X35} + {XD35 / W0:.3f} m', "label2",
                 I["secondary"]))
    # x(t) about the new contact for three placements
    pl = Plot(s, (60, 432, 384, 600), (0, 0.8), (-0.3, 0.15))
    tt = np.linspace(0, 0.8, 161)
    cases = [(xi + 0.06, SER[0]), (xi, SER[1]), (xi - 0.06, SER[2])]
    o.append(pl.axes([(v, f"{v:.1f}") for v in (0, 0.2, 0.4, 0.6, 0.8)],
                     [(v, mn(f"{v:g}")) for v in (-0.3, -0.2, -0.1, 0, 0.1)], "time after the step lands (s)",
                     "x − xₚ (m)", grid=(0,)))
    ys_ = []
    for xp, col in cases:
        y = lip(tt, X35 - xp, XD35)
        m = (y >= -0.3) & (y <= 0.15)
        o.append(pl.curve(tt[m], y[m], col, multi=True))
        ys_.append(np.clip(y, -0.3, 0.15))
    o.append(plabel(s, pl.X(0.08), pl.Y(-0.27), "beyond ξ: A < 0, rocks back", "label2"))
    o.append(plabel(s, pl.X(0.80), pl.Y(0) - 8, "at ξ: A = 0, arrives at rest", "label2", anchor="end"))
    o.append(plabel(s, pl.X(0.01), pl.Y(0.12), "short of ξ: A > 0, falls past", "label2"))
    o.append(legend(s, 60, 414, [(SER[0], "xₚ = ξ + 0.06 m", None), (SER[1], "xₚ = ξ", None),
                                 (SER[2], "xₚ = ξ − 0.06 m", None)], gap=10))
    hov = [[pl.X(t_), [pl.Y(float(y[i])) for y in ys_],
            f"t {t_:.2f} s: x − xp = " + ", ".join(f"{float(lip(t_, X35 - xp, XD35)):+.3f}" for xp, _ in cases) + " m"]
           for i, t_ in enumerate(tt)]
    o.append(credit(s, VB))
    aria = (f"Top: a skeleton (Lynch art) in single support, its centre of mass x = {X35} m ahead of the stance "
            f"contact at height l = {ELL} m and moving forward at {XD35} m/s. As a linear inverted pendulum about a new "
            f"contact x_p, x(t) - x_p = A exp(omega0 t) + B exp(-omega0 t) with omega0 = {W0:.2f} per second and A = "
            f"1/2 (x0 + v0/omega0); the B term decays, so the motion stays bounded only if A <= 0, that is xi = x + "
            f"(dx/dt)/omega0 <= x_p. A magnified floor marks the COM at {X35} m, the extrapolated COM xi = {xi:.3f} m "
            f"(open circle) and the farthest reachable contact x_s max = {REACH} m (red); the blue band between them "
            f"is where the new contact may land, so a step recovers if and only if xi <= x_s max. Bottom: x - x_p "
            f"against time for a contact 0.06 m beyond xi (red, rocks back), at xi (blue, arrives over the foot at "
            f"rest) and 0.06 m short of xi (orange, falls past the foot).")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, hov))


# ================================================================ svg #36  D10 passive downhill walking
AL36, GA36 = 0.30, 0.05                  # rad, step half-angle and slope (line 585, K9 line 913)


def fig36():
    p = "m8f36_"
    VB, s = bvb(470)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    L = 2 * ELL * math.sin(AL36)
    a = math.cos(2 * AL36) ** 2
    b = M * G * L * math.sin(GA36)
    E = b / (1 - a)
    vs = math.sqrt(2 * E / M)
    loss = 0.5 * M * vs ** 2 * math.sin(2 * AL36) ** 2
    close(L, 0.5615, 0.00005)                              # K9 solution (line 913)
    close(a, 0.6812, 0.00005)
    close(b, 19.27, 0.005)
    close(E, 60.44, 0.005)
    close(vs, 1.314, 0.0005)
    close(loss, b, 1e-9)                                   # Prop 9.1 balance (line 577)
    close(math.degrees(GA36), 2.87, 0.0055)                # line 585 (2.865 deg)
    HF, fy, px = 270.0, 350.0, 120.0
    k = HF / H_M
    P = hs_pose(alpha=AL36, far_knee=22)
    svg, J, F = body(p, s, P, P.C, px, fy, HF)
    c0, heel, toe = F(P.C), F(P.j["heel"]), F(P.j["toe_far"])
    gd = math.degrees(GA36)
    R = lambda q: (heel[0] + (q[0] - heel[0]) * math.cos(GA36) - (q[1] - heel[1]) * math.sin(GA36),  # noqa: E731
                   heel[1] + (q[0] - heel[0]) * math.sin(GA36) + (q[1] - heel[1]) * math.cos(GA36))
    c, tp = R(c0), R(toe)
    sl = (math.cos(GA36), math.sin(GA36))
    o.append(f'<g transform="rotate({gd:.4f} {heel[0]:.2f} {heel[1]:.2f})">'
             f'{floor(s, heel[0] - 112, heel[0] + 212, fy)}{svg}</g>')
    o.append(leg_line(s, tp, c))
    o.append(leg_line(s, heel, c))
    o.append(contact_mark(s, *tp))
    o.append(contact_mark(s, *heel))
    d = (sl[0] * L * k, sl[1] * L * k)                     # the next heel strike, one step L down the slope
    c2, h2 = (c[0] + d[0], c[1] + d[1]), (heel[0] + d[0], heel[1] + d[1])
    o.append(leg_line(s, heel, c2, dash=H.DASH_REF, w="ref"))
    o.append(leg_line(s, h2, c2, dash=H.DASH_REF, w="ref"))
    o.append(f'<circle cx="{c2[0]:.2f}" cy="{c2[1]:.2f}" r="{s(4.5):.2f}" fill="#fff" stroke="{I["primary"]}" '
             f'stroke-width="{s(1.5):.2f}"/>')
    o.append(contact_mark(s, *h2))
    o.append(lab(s, h2[0], h2[1] + s(22), "next heel strike", "label2", anchor="middle"))
    o.append(H.com_mark(s, *c))
    o.append(H.arrow(s, p, c[0], c[1] + s(9), c[0], c[1] + s(62), "load"))
    o.append(lab(s, c[0] + s(6), c[1] + s(60), it("Mg"), "label2"))
    xr = 252.0
    o.append(ext(s, c[0] + s(9), c[1], xr + s(8), c[1]))
    o.append(ext(s, c2[0] + s(7), c2[1], xr + s(8), c2[1]))
    o.append(dim_v_out(s, p, xr, c[1], c2[1]))
    o.append(lab(s, xr + s(12), (c[1] + c2[1]) / 2 + s(5), f'{it("L")} sin {it("γ")} = {L * math.sin(GA36) * 100:.1f} cm',
                 "label2"))
    o.append(lab(s, 14, tp[1] + s(30), f'slope {it("γ")} = {GA36} rad ({gd:.2f}°)', "label2"))
    # energy per step: in = out
    bx, by, bw, bk = 290.0, 300.0, 30.0, 2.6
    o.append(H.line(s, bx - s(8), by, bx + 2 * bw + s(38), by, I["axis"], "axis"))
    o.append(bar_v(s, bx, by, bw, b * bk, SER[0]))
    o.append(bar_v(s, bx + bw + s(30), by, bw, loss * bk, SER[1]))
    o.append(lab(s, bx + bw + s(15), by - b * bk - s(8), f'{b:.2f} J each', "label2", anchor="middle"))
    o.append(lines(s, bx + bw / 2, by + s(16), ["gravity", "in"], anchor="middle"))
    o.append(lines(s, bx + 1.5 * bw + s(30), by + s(16), ["heel strike", "out"], anchor="middle"))
    o.append(lines(s, 14, 22, ["periodic gait: the energy", "repeats every step; passive:", "no actuator work, so",
                               "gravity in = collision out"]))
    o.append(lines(s, 214, 22, [f'{it("MgL")} sin {it("γ")} = ½{it("Mv")}² sin² 2{it("α")}',
                                f'{it("ℓ")} = {ELL} m, {it("α")} = {AL36} rad,',
                                f'{it("L")} = 2{it("ℓ")} sin {it("α")} = {L:.4f} m,',
                                f'balance at {it("v")} = {vs:.3f} m/s (K9)']))
    o.append(credit(s, VB))
    pts = [[bx + bw / 2, by - b * bk, f"gravity work per step MgL sin γ = {b:.2f} J"],
           [bx + 1.5 * bw + s(30), by - b * bk, f"heel-strike loss ½Mv² sin² 2α = {loss:.2f} J at v = {vs:.3f} m/s"]]
    aria = (f"A skeleton (Lynch art) walking down a slope of gamma = {GA36} rad ({gd:.2f} degrees), drawn at heel strike "
            f"as the passive compass walker: legs of length l = {ELL} m, half-angle alpha = {AL36} rad, step L = 2 l sin "
            f"alpha = {L:.4f} m. A dashed ghost compass marks the next heel strike one step down the slope, where the "
            f"centre of mass is L sin gamma = {L * math.sin(GA36) * 100:.1f} cm lower. On a periodic gait the energy "
            f"repeats every step, and a passive walker has no actuator work, so the gravity work per step MgL sin gamma "
            f"must equal the heel-strike loss 1/2 M v^2 sin^2 2 alpha. Two equal bars (red gravity in, blue heel strike out) show both at {b:.2f} J, reached "
            f"at v = {vs:.3f} m/s (K9).")
    return finish(VB, aria, s, o, extra=H.hover_attr([bx - 4, by - 70, bx + 2 * bw + 34, by], pts))


FIGS.update({
    27: (r'D1: Derive $v=cL$ for symmetric walking. (body pose)', fig27),
    29: (r'D3: Derive the Froude number by nondimensionalizing $v^2$ wi', fig29),
    30: (r"D4: Starting from Newton's law, derive $\mathbf F_{\rm grf}=", fig30),
    31: (r'D5: Derive the compass-gait relabeling condition at heel str', fig31),
    32: (r'D6: Derive the redirection loss $\frac12 Mv^2\sin^2(2\alpha)', fig32),
    33: (r'D7: Derive $P_j=\tau_j\dot\theta_j$ from work rate. (body po', fig33),
    34: (r'D8: Derive a first-order condition for optimal step length i', fig34),
    35: (r'D9: Derive the capture inequality $x+\dot x/\omega_0\le x_s^', fig35),
    36: (r'D10: Show why passive downhill walking needs slope work to e', fig36),
})
FIGS = dict(sorted(FIGS.items()))
