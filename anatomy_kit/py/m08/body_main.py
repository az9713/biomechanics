"""Module 8 whole-body and model figures (main text). Exposes the Lynch body kit once per page.

svg #2 (Fig. 1 gait cycle), #3 (Fig. 2 stride timeline), #4 (Fig. 3 inverted-pendulum COM arc and energy
exchange), #5 (Fig. 4 COP path and GRF), #6 (Fig. 5 compass gait), #7 (Fig. 6 velocity redirection), #10 (Fig. 9
arm swing), #11 (Fig. 10 passive walker on a slope), #12 (Fig. 11 older-adult fall stack).

Numbers (module08.html line numbers):
  M = 70 kg, l = 0.95 m (contact to COM), v = 1.3 m/s, kappa = 0.09 m^2 (223, 491, 503); Lab 2 L* = 0.6847 m,
  alpha = 21.1 deg, T = 1.053 s (507, 694-708); stance 62 % of the stride (191, 461, 720), so two double-support
  periods of 12 % = 0.126 s (461); dh = 0.0638 m, Mg dh = 43.8 J, Fr = 0.181 (684); K1 midstance speed 1.3 m/s (873);
  collision-only 26.7 J, push-off split 8.8 J, ratio 0.330 (395, 402); Lab 3 Fy template and x_cop (718-737:
  1.10 W at 28 and 72 % of stance, 0.75 W at midstance); arm swing 0.161 M at 0.09 m and 1.3 m/s, 0.050 M at 0.20 m
  and 0.6 m/s -> 2.64, 0.84, 1.80 kg m^2/s, 10.0 / 6.8 N m (540-544); passive walker alpha 0.30 rad, gamma 0.05 rad,
  v 1.25 m/s small-angle / 1.31 m/s exact (585); fall margin x 0.03 m, xdot 0.45 m/s, delay 0.20 s, reach 0.415 m
  -> capture point 0.260 m, margin 0.155 m (629, 644).
Body art: lynch_body.py (Patrick J. Lynch, CC BY 2.5). The text states no stature: 1.75 m (course reference).
Gait poses: lynch_body.POSES gait presets (data/gait_angles_deg.json). Plantar outline: the foot_plantar.py control
points (schematic; no open-licence plantar art in svg_paths/ or art_sources/), COP path: data/cop_plantar_path.json.
"""
import json
import math
import re

import numpy as np

import house as H
import lynch_body as LB
from m05.body import finish, it

SHARED_DEFS = LB.SHARED_DEFS
O, I = H.OVERLAY, H.INK
S0, S1, S2 = H.SERIES[0], H.SERIES[1], H.SERIES[2]
BOXFILL, GRID = "#f7f4ef", "#e6e6e6"
BODY = H.MAX_DISPLAY_H_BODY
DATA = LB.KIT / "data"

# ---------------------------------------------------------------- module constants (line numbers above)
G, M_KG, ELL, V, KAPPA = 9.81, 70.0, 0.95, 1.3, 0.09
W_N = M_KG * G
H_M = 1.75
_L = np.linspace(0.35, 0.95, 200)                                        # Lab 2, lines 694-704
_C = 0.5 * M_KG * V * V * np.sin(2 * np.arcsin(_L / (2 * ELL))) ** 2 + KAPPA * (V / _L) ** 2 * M_KG
L_STAR = float(_L[int(np.argmin(_C))])
ALPHA = math.asin(L_STAR / (2 * ELL))
AD = math.degrees(ALPHA)
T_STR = 2 * L_STAR / V
STANCE = 0.62
DS = 2 * STANCE - 1                                                     # 0.24 of the stride, two periods
DH = ELL * (1 - math.cos(ALPHA))
MGDH = M_KG * G * DH
FR = V * V / (G * ELL)
E_COLL = 0.5 * M_KG * V * V * math.sin(2 * ALPHA) ** 2
E_SPLIT = 0.5 * M_KG * V * V * math.tan(ALPHA) ** 2
# Lab 3 (lines 718-728): stance template, scale fixed by the impulse W T / 2
_s = np.linspace(0, 1, 601)
_shape = np.sin(np.pi * _s) ** 0.40 * (1 - 0.245 * np.cos(4 * np.pi * (_s - 0.5)))
FY = _shape * (W_N * T_STR / 2) / np.trapezoid(_shape, _s * STANCE * T_STR)
XCOP = -0.04 + 0.225 * _s
# arm swing (lines 540-544)
H_LEGS = 2 * 0.161 * M_KG * 0.09 * 1.3
H_ARMS = 2 * 0.050 * M_KG * 0.20 * 0.6
H_RES = H_LEGS - H_ARMS
TQ_STILL, TQ_SWING = 2 * H_LEGS / (T_STR / 2), 2 * H_RES / (T_STR / 2)
# passive walker (line 585)
AP, GAM = 0.30, 0.05
V_SMALL = math.sqrt(G * ELL * math.sin(GAM) / AP)
L_P = 2 * ELL * math.sin(AP)
V_EXACT = math.sqrt(2 * G * L_P * math.sin(GAM)) / math.sin(2 * AP)
E_IN = M_KG * G * L_P * math.sin(GAM)
# fall margin (lines 629, 644)
W0 = math.sqrt(G / ELL)
XC, XD, DEL, REACH = 0.03, 0.45, 0.20, 0.415
CAP = XC + XD * DEL + XD / W0
MARGIN = REACH - CAP
_i28, _i72 = int(np.argmax(FY[:300])), 300 + int(np.argmax(FY[300:]))
assert (round(L_STAR, 4), round(AD, 1), round(T_STR, 3), round(DH, 4), round(MGDH, 1), round(FR, 3)) == \
    (0.6847, 21.1, 1.053, 0.0638, 43.8, 0.181)
assert (round(E_COLL, 1), round(E_SPLIT, 1), round(E_SPLIT / E_COLL, 3), round(DS / 2 * T_STR, 3)) == (26.7, 8.8, 0.330, 0.126)
assert (round(FY[_i28] / W_N, 2), round(FY[300] / W_N, 2), round(_s[_i28], 2), round(_s[_i72], 2)) == (1.10, 0.75, 0.28, 0.72)
assert (round(H_LEGS, 2), round(H_ARMS, 2), round(H_RES, 2), round(TQ_STILL, 1), round(TQ_SWING, 1)) == (2.64, 0.84, 1.80, 10.0, 6.8)
assert (round(V_SMALL, 2), round(V_EXACT, 2)) == (1.25, 1.31)
assert (round(W0, 2), round(CAP, 3), round(MARGIN, 3), round(XD * DEL, 3)) == (3.21, 0.260, 0.155, 0.090)


# ---------------------------------------------------------------- small helpers (m07/body_main idiom)
def defs(p, s, extra=""):
    return f"<defs>{H.markers(p, s)}{extra}</defs>"


def path_d(pts, close=False):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + ("Z" if close else "")


def poly(s, pts, col, w="curve", dash=None, extra=""):
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    return (f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="none" stroke="{col}" '
            f'stroke-width="{s(H.PX[w]):.2f}" stroke-linejoin="round"{da} {extra}/>')


def white_under(s, x1, y1, x2, y2, w=4):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#fff" '
            f'stroke-width="{s(w):.2f}" opacity="0.85"/>')


def dline(s, x1, y1, x2, y2, col=None, w="ref", dash=H.DASH_REF):
    """Dashed reference line with a white under-stroke so it reads over the art."""
    return white_under(s, x1, y1, x2, y2) + H.line(s, x1, y1, x2, y2, col or O["dim"], w, dash=dash)


def floor(s, x0, x1, y):
    return H.line(s, x0, y, x1, y, I["rule"], "axis")


def leader(s, x1, y1, x2, y2, col=None):
    return H.line(s, x1, y1, x2, y2, col or I["secondary"], "leader")


def arc_pts(cx, cy, r, a0, a1, n=24):
    """Screen angles in degrees: 0 = +x, + = clockwise (y down)."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def angle_arc(s, cx, cy, r, a0, a1, col=None):
    return (f'<path d="{path_d(arc_pts(cx, cy, r, a0, a1, 16))}" fill="none" stroke="{col or O["geometry"]}" '
            f'stroke-width="{s(H.PX["geom"]):.2f}"/>')


def arc_arrow(s, p, cx, cy, r, a0, a1, meaning, col=None):
    col = col or O[meaning]
    w = {"geometry": "geom", "dim": "ref"}.get(meaning, "force")
    return (f'<path d="{path_d(arc_pts(cx, cy, r, a0, a1))}" fill="none" stroke="{col}" '
            f'stroke-width="{s(H.PX[w]):.2f}" marker-end="url(#{p}a_{meaning})"/>')


def dot(s, x, y, col=None, r=3.5):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{col or I["primary"]}" stroke="#fff" '
            f'stroke-width="{s(1.2):.2f}"/>')


def cop_mark(s, x, y):
    """Centre of pressure: blue cross-hair circle (a mark, not anatomy; m07 idiom)."""
    r, c = s(5.5), O["geometry"]
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="#fff" stroke="{c}" stroke-width="{s(2):.2f}"/>'
            f'<path d="M{x - r * 1.7:.2f},{y:.2f}h{r * 3.4:.2f}M{x:.2f},{y - r * 1.7:.2f}v{r * 3.4:.2f}" '
            f'stroke="{c}" stroke-width="{s(1.4):.2f}"/>')


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


def link(s, x1, y1, x2, y2, col=None, w="force"):
    """A rigid link of a mechanical model (not anatomy)."""
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{col or I["primary"]}" '
            f'stroke-width="{s(H.PX[w] * 1.4):.2f}" stroke-linecap="round"/>')


def only(svg, keep):
    """Keep only the near-side <use> elements whose def id is in `keep`."""
    def f(m):
        name = re.search(r'href="#hbody_(\w+)"', m.group(0)).group(1)
        return m.group(0) if name in keep and "filter=" not in m.group(0) else ""
    return re.sub(r"<use [^>]*/>", f, svg)


def pt(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def unit(dx, dy):
    n = math.hypot(dx, dy)
    return dx / n, dy / n


# ---------------------------------------------------------------- gait poses (lynch_body presets = data json)
GAIT = json.loads((DATA / "gait_angles_deg.json").read_text(encoding="utf-8"))
_MS = LB.POSES["gait_midstance"]
POSE_SWING = dict(near=_MS["far"], far=_MS["near"], anchor=("heel", "far"))   # right leg in mid-swing
FRAMES = [("heel strike", 0, LB.POSES["gait_heel_strike"]), ("midstance", 31, _MS),
          ("toe-off", 62, LB.POSES["gait_toe_off"]), ("mid-swing", 80, POSE_SWING),
          ("next heel strike", 100, LB.POSES["gait_heel_strike"])]
assert GAIT["events"]["midswing"]["hip"] == _MS["far"]["hip"] and GAIT["events"]["midswing"]["knee"] == _MS["far"]["knee"]
T_TRANS = (DS / 4 * 100, 50 + DS / 4 * 100)          # 6 % and 56 %: the middle of each double-support period


def theta_ip(t):
    """Stance-leg angle of the inverted pendulum at t % of the stride: -alpha .. +alpha between transitions."""
    f = ((t - T_TRANS[0]) % 50) / 50
    return -ALPHA + 2 * ALPHA * f


# ================================================================ svg #2  Fig. 1 gait cycle
def fig2():
    p = "m8f2_"
    VB = (0, 0, 760, 450)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    hb, fy, gap = 285.0, 360.0, 6.0
    k = hb / H_M
    o = [defs(p, s)]
    # place the five bodies left to right by their bounding boxes
    placed, x = [], 18.0
    for name, t, P in FRAMES:
        svg0, J0 = LB.draw("", s, LB.pose(**P), 0.0, fy, hb)
        dx = x - J0["bbox"][0]
        svg, J = LB.draw("", s, LB.pose(**P), dx, fy, hb)
        placed.append((name, t, svg, J))
        x = J["bbox"][2] + gap
    o.append(floor(s, 10, 750, fy))
    o += [q[2] for q in placed]
    # COM path: inverted-pendulum arcs at the text's height (l = 0.95 m, Prop 2.1), drawn at true vertical scale;
    # horizontal positions follow the spaced-out bodies (interpolated between the frames' COM x)
    ft = [q[1] for q in placed]
    fx = [q[3]["com"][0] for q in placed]
    ts = np.linspace(0, 100, 101)
    ts = np.unique(np.concatenate([ts, T_TRANS]))
    path = [(float(np.interp(t, ft, fx)), fy - k * ELL * math.cos(theta_ip(t))) for t in ts]
    o.append(white_under(s, *path[0], *path[1], 0) + poly(s, path, O["geometry"], "geom"))
    for name, t, svg, J in placed:
        o.append(H.com_mark(s, J["com"][0], fy - k * ELL * math.cos(theta_ip(t))))
    for tt in T_TRANS:
        xc = float(np.interp(tt, ft, fx))
        o.append(dot(s, xc, fy - k * ELL * math.cos(ALPHA), O["flag"], 4))
    # path labels
    xm = fx[1]
    ytop = fy - k * ELL
    yl = fy - hb - s(12)
    o.append(H.label(s, xm, yl, "COM rises over the stance leg", "label2", O["geometry"], "middle"))
    o.append(leader(s, xm, yl + s(4), xm, ytop - s(10), O["geometry"]))
    xc2 = float(np.interp(T_TRANS[1], ft, fx))
    yc = fy - k * ELL * math.cos(ALPHA)
    o.append(H.label(s, xc2 - s(8), yl, "redirected at the transition", "label2", O["flag"]))
    o.append(leader(s, xc2, yl + s(4), xc2, yc - s(6), O["flag"]))
    # vertical scale note: the rise is small at true scale
    o.append(H.label(s, 18, 20, "COM path (blue): circular arcs about each stance foot, radius ℓ = 0.95 m; "
                     f"rise Δh = {DH * 100:.1f} cm, drawn to scale", "label2", I["secondary"]))
    o.append(H.label(s, 18, 37, "bodies spaced apart for clarity (one stride is 1.37 m); near (light) limbs = right, "
                     "far (shaded) = left", "label2", I["secondary"]))
    for name, t, svg, J in placed:
        cx = (J["bbox"][0] + J["bbox"][2]) / 2
        o.append(H.label(s, cx, fy + s(22), name, "label2", anchor="middle"))
        o.append(H.label(s, cx, fy + s(38), f"{t} % of stride", "label2", I["secondary"], "middle"))
    o.append(LB.credit(s, 18, fy + s(62), width=720))
    aria = ("Gait cycle of the right leg drawn as five skeletons, left to right: heel strike at 0 percent of the "
            "stride, midstance at 31, toe-off at 62, mid-swing at 80 and the next heel strike at 100. A blue centre-of-"
            "mass path joins the centre-of-mass marks: it is a chain of circular arcs about each stance foot, highest "
            "at midstance and meeting in orange cusps at the step-to-step transitions, where the velocity is "
            f"redirected. The rise is {DH * 100:.1f} centimetres, drawn to scale.")
    return finish(VB, aria, s, o)


# ================================================================ svg #3  Fig. 2 stride timeline
def fig3():
    p = "m8f3_"
    VB = (0, 0, 760, 270)
    s = H.Scale(VB[2], VB[3])
    x0, x1 = 112.0, 735.0
    X = lambda pc: x0 + (x1 - x0) * pc / 100  # noqa: E731
    rows = {"right": (78.0, S0), "left": (128.0, S1)}
    bh = 30.0
    o = [defs(p, s)]
    st, dsw = STANCE * 100, DS / 2 * 100              # 62 %, 12 %
    # double-support bands (flag orange: the overlap, always labelled)
    for a, b in ((0, dsw), (50, 50 + dsw)):
        o.append(f'<rect x="{X(a):.2f}" y="{rows["right"][0] - 8:.2f}" width="{X(b) - X(a):.2f}" '
                 f'height="{rows["left"][0] + bh + 8 - rows["right"][0] + 8:.2f}" fill="{O["flag"]}" fill-opacity="0.16"/>')
    segs = {"right": [(0, st, "stance"), (st, 100, "swing")],
            "left": [(0, dsw, "stance"), (dsw, 50, "swing"), (50, 100, "stance")]}
    for leg, (y, col) in rows.items():
        for a, b, kind in segs[leg]:
            if kind == "stance":
                o.append(f'<rect x="{X(a):.2f}" y="{y:.2f}" width="{X(b) - X(a):.2f}" height="{bh}" fill="{col}" '
                         f'fill-opacity="0.30" stroke="{col}" stroke-width="{s(1.4):.2f}"/>')
            else:
                o.append(f'<rect x="{X(a):.2f}" y="{y:.2f}" width="{X(b) - X(a):.2f}" height="{bh}" fill="{BOXFILL}" '
                         f'stroke="{I["rule"]}" stroke-width="{s(1):.2f}"/>')
            txt = {"right": f"right {kind} {b - a:.0f} %", "left": f"left {kind} {b - a:.0f} %"}[leg]
            if leg == "left" and kind == "stance":
                txt = "stance" if b - a < 20 else "left stance (with 0–12 %: 62 %)"
            o.append(H.label(s, (X(a) + X(b)) / 2, y + bh / 2 + s(5), txt, "label2", anchor="middle"))
        o.append(f'<rect x="{x0 - s(96):.2f}" y="{y + bh / 2 - s(5):.2f}" width="{s(10):.2f}" height="{s(10):.2f}" '
                 f'fill="{col}" fill-opacity="0.30" stroke="{col}" stroke-width="{s(1.4):.2f}"/>')
        o.append(H.label(s, x0 - s(82), y + bh / 2 + s(5), f"{leg} leg", "label2"))
    # events
    ev = [(0, "HS", "right"), (dsw, "TO", "left"), (31, "mid", "right"), (50, "HS", "left"), (st, "TO", "right"),
          (100, "HS", "right")]
    yt = rows["right"][0] - 8
    for pc, nm, leg in ev:
        col = rows[leg][1]
        o.append(H.line(s, X(pc), yt - s(12), X(pc), yt, col, "geom"))
        lab = f"{nm} {leg[0].upper()}"
        o.append(H.label(s, X(pc), yt - s(17), lab, "label2", I["primary"], "middle"))
    for (a, b), txt in (((0, dsw), "double support"), ((50, 50 + dsw), "double support")):
        yb = rows["left"][0] + bh + 8
        o.append(H.label(s, (X(a) + X(b)) / 2, yb + s(16), txt, "label2", I["primary"], "middle"))
        o.append(H.label(s, (X(a) + X(b)) / 2, yb + s(31), f"{DS / 2 * T_STR:.3f} s", "label2", I["secondary"], "middle"))
    # axes: percent of stride and time
    ya = 222.0
    o.append(H.line(s, x0, ya, x1, ya, I["axis"], "axis"))
    for pc in (0, 25, 50, 75, 100):
        o.append(H.line(s, X(pc), ya, X(pc), ya + s(5), I["axis"], "axis"))
        o.append(H.label(s, X(pc), ya + s(19), f"{pc}", "tick", I["primary"], "middle"))
    o.append(H.label(s, x0 - s(10), ya + s(19), "% of stride", "tick", I["secondary"], "end"))
    for tsec in (0.25, 0.5, 0.75, 1.0):
        xx = X(tsec / T_STR * 100)
        o.append(H.line(s, xx, ya, xx, ya - s(5), I["axis"], "axis"))
        o.append(H.label(s, xx, ya - s(8), f"{tsec:g} s", "tick", I["secondary"], "middle"))
    o.append(H.label(s, x1, ya + s(38), f"one stride, T = {T_STR:.3f} s (reference gait, Lab 2)", "label2",
                     I["secondary"], "end"))
    aria = ("Timeline of one stride from 0 to 100 percent, about 1.05 seconds. The right leg (red bar) is in stance "
            "from 0 to 62 percent and in swing from 62 to 100. The left leg (blue bar) is in stance from 0 to 12 and "
            "from 50 to 100 percent, in swing from 12 to 50. Orange bands mark the two double-support periods, 0 to 12 "
            "and 50 to 62 percent, each 0.126 seconds. Ticks mark heel strike (HS), toe-off (TO) and midstance (mid) "
            "of each leg.")
    return finish(VB, aria, s, o)


# ================================================================ svg #4  Fig. 3 inverted-pendulum COM arc
def fig4():
    p = "m8f4_"
    VB = (0, 0, 760, 510)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    hb, fy = 360.0, 400.0
    k = hb / H_M
    o = [defs(p, s)]
    P = LB.pose(**_MS)
    svg, J = LB.draw("", s, P, 0.0, fy, hb)
    shift = 175.0 - J["com"][0]
    svg, J = LB.draw("", s, P, shift, fy, hb)
    o.append(floor(s, 20, 345, fy))
    o.append(svg)
    px = J["com"][0]                                   # contact point under the COM at midstance
    cy = fy - k * ELL
    R = k * ELL
    arc = [(px + R * math.sin(t), fy - R * math.cos(t)) for t in np.linspace(-ALPHA, ALPHA, 61)]
    ends = (arc[0], arc[-1])
    for e in ends:
        o.append(dline(s, px, fy, e[0], e[1], O["dim"]))
    o.append(dline(s, px, fy, px, cy - s(30), O["dim"]))
    o.append(white_under(s, *arc[0], *arc[1], 0) + poly(s, arc, O["geometry"], "geom"))
    for e in ends:
        o.append(f'<circle cx="{e[0]:.2f}" cy="{e[1]:.2f}" r="{s(4):.2f}" fill="#fff" stroke="{O["geometry"]}" '
                 f'stroke-width="{s(1.6):.2f}"/>')
    o.append(white_under(s, px, fy, px, cy, 5) + H.line(s, px, fy, px, cy, O["geometry"], "geom"))
    o.append(H.com_mark(s, px, cy))
    o.append(cop_mark(s, px, fy))
    # labels: l, alpha, dh
    o.append(H.label(s, px + s(4), cy + 0.45 * R, it("ℓ"), "label", O["geometry"]))
    o.append(angle_arc(s, px, fy, 70, -90, -90 + AD))
    a = math.radians(-90 + AD + 9)
    o.append(H.label(s, px + 74 * math.cos(a), fy + 74 * math.sin(a) + s(4), it("α"), "label", O["geometry"]))
    o.append(H.label(s, px - s(30), fy + s(20), "contact point", "label2", I["secondary"], "end"))
    o.append(leader(s, px - s(28), fy + s(14), px - s(7), fy + s(3)))
    o.append(H.label(s, px - s(10), cy - s(34), "COM", "label2", anchor="end"))
    o.append(leader(s, px - s(8), cy - s(30), px - s(5), cy - s(6)))
    xr = ends[1][0] + s(14)
    ye = ends[1][1]
    o.append(dline(s, px + s(8), cy, xr + s(40), cy, I["secondary"], "leader"))
    o.append(dline(s, ends[1][0] + s(5), ye, xr + s(40), ye, I["secondary"], "leader"))
    o.append(H.line(s, xr + s(30), cy, xr + s(30), ye, O["geometry"], "geom"))
    o.append(H.label(s, xr + s(44), (cy + ye) / 2 - s(4), "Δh = ℓ(1 − cos α)", "label2", O["geometry"]))
    o.append(H.label(s, xr + s(44), (cy + ye) / 2 + s(13), f"= {DH * 100:.1f} cm", "label2", O["geometry"]))
    o.append(lines(s, 20, fy + s(42), [f"ℓ = 0.95 m from the contact point to the COM;",
                                        f"the leg sweeps from −α to +α, α = {AD:.1f}°"], "label2", I["secondary"]))
    o.append(LB.credit(s, 20, fy + s(86), width=720))
    # ---- right: energy exchange over single support, K1 (line 873): v(θ)² = v_mid² + 2gℓ(1 − cos θ)
    bx0, bx1, by0, by1 = 440.0, 735.0, 70.0, 330.0
    th = np.linspace(-ALPHA, ALPHA, 85)
    KE = 0.5 * M_KG * (V * V + 2 * G * ELL * (1 - np.cos(th)))
    PE = M_KG * G * ELL * (np.cos(th) - math.cos(ALPHA))
    E0 = float(KE[0])
    xs = lambda d: bx0 + (bx1 - bx0) * (d + 25) / 50  # noqa: E731
    ys = lambda e: by1 - (by1 - by0) * e / 120  # noqa: E731
    for e in (0, 20, 40, 60, 80, 100, 120):
        o.append(H.line(s, bx0, ys(e), bx1, ys(e), GRID, "leader"))
        o.append(H.label(s, bx0 - s(6), ys(e) + s(4), f"{e}", "tick", I["primary"], "end"))
    for d in (-20, -10, 0, 10, 20):
        o.append(H.line(s, xs(d), by1, xs(d), by1 + s(5), I["axis"], "axis"))
        o.append(H.label(s, xs(d), by1 + s(19), f"{d}".replace("-", "−"), "tick", I["primary"], "middle"))
    o.append(H.line(s, bx0, by1, bx1, by1, I["axis"], "axis") + H.line(s, bx0, by0, bx0, by1, I["axis"], "axis"))
    o.append(H.label(s, (bx0 + bx1) / 2, by1 + s(38), "leg angle θ (degrees), single support", "label2", anchor="middle"))
    o.append(H.label(s, bx0 - s(6), by0 - s(12), "energy (J)", "label2", I["secondary"], "start"))
    D = np.degrees(th)
    ke = [(xs(d), ys(e)) for d, e in zip(D, KE)]
    pe = [(xs(d), ys(e)) for d, e in zip(D, PE)]
    o.append(poly(s, [(xs(-AD), ys(E0)), (xs(AD), ys(E0))], I["secondary"], "curve_multi", dash=H.DASH_REF))
    o.append(poly(s, ke, S0, "curve_multi"))
    o.append(poly(s, pe, S1, "curve_multi"))
    o.append(H.label(s, xs(0), ys(E0) - s(8), f"total {E0:.1f} J (no work done)", "label2", I["primary"], "middle"))
    o.append(H.label(s, xs(0), ys(float(KE.min())) + s(17), "kinetic", "label2", anchor="middle"))
    o.append(H.label(s, xs(-8), ys(12), "potential", "label2", anchor="middle"))
    # Mg dh bracket at midstance
    o.append(H.line(s, xs(0), ys(0), xs(0), ys(MGDH), O["dim"], "ref", dash=H.DASH_REF))
    o.append(H.label(s, xs(1) + s(4), ys(26), "Mg Δh", "label2"))
    o.append(H.label(s, xs(1) + s(4), ys(26) + s(15), f"= {MGDH:.1f} J", "label2"))
    for d in (-AD, AD):
        o.append(H.line(s, xs(d), by0, xs(d), by1, I["rule"], "leader", dash=H.DASH_REF))
    o.append(H.label(s, xs(-AD) + s(3), by0 + s(12), "−α", "label2", I["secondary"]))
    o.append(H.label(s, xs(AD) - s(3), by0 + s(12), "+α", "label2", I["secondary"], "end"))
    # legend
    lx, ly = bx0 + s(4), by0 - s(40)
    o.append(H.line(s, lx, ly, lx + s(22), ly, S0, "curve_multi"))
    o.append(H.label(s, lx + s(28), ly + s(4), "kinetic ½Mv²", "label2"))
    o.append(H.line(s, lx + s(140), ly, lx + s(162), ly, S1, "curve_multi"))
    o.append(H.label(s, lx + s(168), ly + s(4), "potential above step edge", "label2"))
    pts = [[xs(d), [ys(a), ys(b)], f"θ {d:+.1f}°: kinetic {a:.1f} J, potential {b:.1f} J"] for d, a, b in zip(D, KE, PE)]
    aria = ("Left: a skeleton at midstance with its centre of mass 0.95 metres above the contact point under the "
            "foot. The stance leg, a blue line of length l, sweeps from minus alpha to plus alpha, alpha 21.1 degrees, "
            "so the centre of mass moves on a blue circular arc that is highest at midstance and 6.4 centimetres "
            "lower at each step edge. Right: kinetic energy (red) falls from 103.0 to 59.2 joules toward midstance "
            "while potential energy (blue) rises by 43.8 joules, then the exchange reverses; their sum stays at "
            "103.0 joules.")
    return finish(VB, aria, s, o, H.hover_attr([bx0, by0, bx1, by1], pts))


# ================================================================ svg #5  Fig. 4 COP path and GRF
# foot_plantar.py plantar_outline_path: right foot, u heel -> toe, v < 0 lateral (the m01 copy of the points).
PLANTAR = [(0.00, 0.08), (0.02, -0.10), (0.08, -0.16), (0.18, -0.14), (0.32, -0.12), (0.50, -0.14), (0.68, -0.16),
           (0.82, -0.12), (0.94, -0.04), (0.98, 0.04), (0.96, 0.12), (0.88, 0.16), (0.72, 0.14), (0.55, 0.10),
           (0.40, 0.06), (0.25, 0.04), (0.12, 0.06), (0.04, 0.10)]
COP_PATH = json.loads((DATA / "cop_plantar_path.json").read_text(encoding="utf-8"))["cop_path"]


def smooth_closed(pts):
    """Closed Catmull-Rom spline through pts as cubic Beziers (m01 idiom)."""
    n, d = len(pts), [f"M{pts[0][0]:.2f},{pts[0][1]:.2f}"]
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p2[0]:.2f},{p2[1]:.2f}")
    return "".join(d) + "Z"


def _edge(u, side):
    """Outline v at heel-to-toe position u on the lateral (side -1) or medial (+1) edge, by linear interpolation."""
    lat = sorted(q for q in PLANTAR[1:10] if q[1] < 0.05)
    med = sorted(q for q in PLANTAR[9:] + [PLANTAR[0]])
    e = lat if side < 0 else med
    return float(np.interp(u, [q[0] for q in e], [q[1] for q in e]))


def fig5():
    p = "m8f5_"
    VB = (0, 0, 760, 510)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    o = [defs(p, s)]
    # ---- left: sole seen from below, heel left, toes right; lateral edge up
    x0, y0, Lf = 40.0, 200.0, 300.0
    F = lambda u, v: (x0 + u * Lf, y0 + v * Lf)  # noqa: E731
    o.append(f'<path d="{smooth_closed([F(u, v) for u, v in PLANTAR])}" fill="{H.TISSUE["skin"][0]}" '
             f'stroke="{H.TISSUE["skin"][1]}" stroke-width="{s(1.6):.2f}"/>')
    cp = []
    for q in COP_PATH:              # y across the local width: 0 = medial edge, 1 = lateral edge
        vm, vl = _edge(q["x"], 1), _edge(q["x"], -1)
        cp.append((F(q["x"], vm + q["y"] * (vl - vm)), q["label"]))
    o.append(poly(s, [c for c, _ in cp], O["geometry"], "geom"))
    for (a, _), (b, _) in zip(cp[:-1], cp[1:]):
        m = pt(a, b, 0.62)
        d = unit(b[0] - a[0], b[1] - a[1])
        o.append(H.arrow(s, p, m[0] - d[0] * s(6), m[1] - d[1] * s(6), m[0] + d[0] * s(2), m[1] + d[1] * s(2), "geometry"))
    for c, lab in cp:
        o.append(cop_mark(s, *c))
    o.append(H.label(s, cp[0][0][0], cp[0][0][1] - s(14), "heel COP", "label2", anchor="middle"))
    o.append(H.label(s, cp[2][0][0], cp[2][0][1] - s(14), "lateral midfoot", "label2", anchor="middle"))
    o.append(H.label(s, cp[4][0][0] - s(4), cp[4][0][1] + s(24), "medial forefoot (hallux)", "label2", anchor="middle"))
    o.append(H.label(s, x0 + 0.5 * Lf, y0 - 0.16 * Lf - s(8), "lateral edge", "label2", I["secondary"], "middle"))
    o.append(H.label(s, x0 + 0.40 * Lf, y0 + 0.10 * Lf + s(26), "medial arch", "label2", I["secondary"], "middle"))
    o.append(H.label(s, x0, y0 + 0.16 * Lf + s(26), "heel", "label2", I["secondary"]))
    o.append(H.label(s, x0 + Lf, y0 + 0.16 * Lf + s(26), "toes", "label2", I["secondary"], "end"))
    o.append(H.label(s, x0 - s(4), 96, "right foot, sole seen from below", "label"))
    o.append(H.label(s, x0 - s(4), 114, "COP path, heel to toe (teaching schematic)", "label2", I["secondary"]))
    # ---- right: side view of the same foot at midstance, GRF at three instants of stance (Lab 3)
    fy, k = 430.0, 690.0                               # figure units per metre
    P = LB.pose(near=dict(hip=0, knee=8), far=dict(hip=0, knee=8))
    svg, J = LB.draw("", s, P, 0.0, fy, H_M * k)
    svg, J = LB.draw("", s, P, 470.0 - J["heel"][0], fy, H_M * k)
    o.append(floor(s, 420, 750, fy))
    o.append(only(svg, {"lat_shank", "lat_foot"}))
    ax, ay = J["ankle"]
    kx, ky = J["knee"]
    xm = float(XCOP[300])
    arrows = []
    for i in (_i28, 300, _i72):
        xc = float(XCOP[i])
        xcom = xm + V * (float(_s[i]) - 0.5) * STANCE * T_STR   # COM over the COP at midstance, moving at v
        phi = math.atan2(xcom - xc, ELL)                         # GRF along the leg, contact -> COM (Prop 2.2)
        Fm = float(FY[i]) / math.cos(phi) / W_N
        c = (ax + k * xc, fy)
        e = (c[0] + 150.0 * Fm * math.sin(phi), c[1] - 150.0 * Fm * math.cos(phi))
        top = (c[0] + (fy - ky + s(14)) * math.tan(phi), ky - s(14))   # line of action up past the knee
        arrows.append((i, c, e, phi, top))
    for i, c, e, phi, top in arrows:
        o.append(dline(s, e[0], e[1], top[0], top[1], I["secondary"], "leader", H.DASH_LOA))
    for i, c, e, phi, top in arrows:
        o.append(white_under(s, c[0], c[1], e[0], e[1], 5) + H.arrow(s, p, c[0], c[1], e[0], e[1], "reaction"))
        o.append(cop_mark(s, *c))
        o.append(H.label(s, c[0], fy + s(20), f"{_s[i] * 100:.0f} %", "label2", anchor="middle"))
    o.append(H.joint_centre(s, ax, ay))
    o.append(H.joint_centre(s, kx, ky))
    o.append(H.label(s, ax - s(14), ay + s(4), "ankle", "label2", anchor="end"))
    xl = (arrows[0][4][0] + min(kx, arrows[1][4][0])) / 2       # between the early and the middle line at the knee
    o.append(H.label(s, xl, ky + s(28), "knee", "label2", anchor="middle"))
    o.append(leader(s, xl, ky + s(16), kx - s(5), ky + s(3)))
    o.append(H.label(s, 420, 22, "side view: GRF (black) at three instants", "label"))
    o.append(H.label(s, 420, 40, "of stance; dashed: its line of action", "label2", I["secondary"]))
    # numbers, under the plantar view
    rows = [f"Lab 3, at {_s[_i28] * 100:.0f} % of stance: {FY[_i28] / W_N:.2f} W up, tilted back {abs(math.degrees(arrows[0][3])):.1f}°: braking",
            f"at 50 %: {FY[300] / W_N:.2f} W up, vertical: the COM is pulled down",
            f"at {_s[_i72] * 100:.0f} %: {FY[_i72] / W_N:.2f} W up, tilted forward: propulsive",
            "tilt: the force points from the COP to the COM (Prop 2.2),",
            "the COM over the COP at midstance and moving at 1.3 m/s;",
            "the line of action passes behind the knee early, ahead late"]
    o.append(lines(s, 40, 330, rows, "label2"))
    o.append(LB.credit(s, 20, fy + s(44), width=720, extra=" Foot sole outline: schematic."))
    aria = ("Left: the sole of a right foot seen from below, heel at left. A blue centre-of-pressure path runs from "
            "the heel, out to the lateral midfoot, then in to the medial forefoot under the big toe. Right: the same "
            "foot and shank from the side. Black ground-reaction arrows start at three centre-of-pressure points that "
            "move toward the toes: at 28 percent of stance, 1.10 body weights tilted backward (braking), its line of "
            "action behind the knee; at 50 percent, 0.75 body weights, vertical; at 72 percent, 1.10 body weights "
            "tilted forward (propulsive), ahead of the ankle and knee. As the pressure point advances the force "
            "rotates and its moment arms about the ankle and knee change.")
    return finish(VB, aria, s, o)


# ================================================================ svg #6  Fig. 5 compass gait
def _solve(f, lo, hi, n=40):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def _leg_ang(J, a):
    return math.degrees(math.atan2(J[a][0] - J["hip"][0], J[a][1] - J["hip"][1]))


def compass_pose():
    """Walker just before heel strike with its two hip-to-contact lines at +-alpha (the compass legs)."""
    arms = dict(near=dict(shoulder=-25, elbow=10), far=dict(shoulder=25, elbow=25))
    def mk(h1, h2):
        return LB.pose(near=dict(hip=h1, knee=5, contact=None, ankle=0, **arms["near"]),
                       far=dict(hip=h2, knee=20, contact="toe", **arms["far"]))
    s1 = H.Scale(100, 100)
    ang = lambda P, a: _leg_ang(LB.draw("", s1, P, 0, 0, LB.H_U)[1], a)  # noqa: E731
    h1 = _solve(lambda h: ang(mk(h, -10), "heel") - AD, 20, 45)
    h2 = _solve(lambda h: ang(mk(h1, h), "toe_far") + AD, -5, -24)
    return mk(h1, h2)


def fig6():
    p = "m8f6_"
    VB = (0, 0, 760, 450)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    hb, fy = 340.0, 380.0
    o = [defs(p, s)]
    P = compass_pose()
    svg, J = LB.draw("", s, P, 0.0, fy, hb)
    svg, J = LB.draw("", s, P, 60.0 - J["bbox"][0], fy, hb)
    o.append(floor(s, 20, 745, fy))
    o.append(f'<g opacity="0.5">{svg}</g>')
    hip, piv, nhs = J["hip"], J["toe_far"], J["heel"]
    piv, nhs = (piv[0], fy), (nhs[0], fy)
    o.append(dline(s, hip[0], hip[1] - s(30), hip[0], fy))
    o.append(link(s, *piv, *hip))
    o.append(link(s, *nhs, *hip, S1))
    o.append(mass(s, *hip, 10))
    o.append(angle_arc(s, hip[0], hip[1], 78, 90, 90 + AD))
    o.append(angle_arc(s, hip[0], hip[1], 96, 90 - AD, 90, S1))
    a1, a2 = math.radians(90 + AD / 2), math.radians(90 - AD / 2)
    o.append(H.label(s, hip[0] + 92 * math.cos(a1) - s(2), hip[1] + 92 * math.sin(a1) + s(5), it("θ"), "label",
                     O["geometry"], "end"))
    o.append(H.label(s, hip[0] + 110 * math.cos(a2) + s(3), hip[1] + 110 * math.sin(a2) + s(5), it("φ"), "label", S1))
    o.append(H.joint_centre(s, *piv))
    o.append(dot(s, *nhs, O["flag"], 5))
    o.append(H.label(s, piv[0], fy + s(22), "stance foot: pinned pivot", "label2", anchor="middle"))
    o.append(H.label(s, nhs[0], fy + s(22), "next heel strike", "label2", O["flag"], "middle"))
    o.append(H.label(s, hip[0] + s(14), hip[1] - s(10), "hip mass " + it("M"), "label2"))
    mst = pt(piv, hip, 0.42)
    o.append(H.label(s, mst[0] - s(12), mst[1], "stance leg, " + it("ℓ"), "label2", anchor="end"))
    msw = pt(nhs, hip, 0.42)
    o.append(H.label(s, msw[0] + s(12), msw[1], "swing leg, " + it("ℓ"), "label2", S1))
    o.append(H.label(s, 20, 26, "just before heel strike: the model (lines) drawn over a walker", "label"))
    o.append(H.label(s, 20, 44, f"|θ| = |φ| = α = {AD:.1f}°, inter-leg angle 2α = {2 * AD:.1f}° (reference gait)",
                     "label2", I["secondary"]))
    # ---- right: after the impact the labels swap
    bx, by, bw, bh = 470.0, 120.0, 272.0, 228.0
    o.append(box(s, bx, by, bw, bh))
    ox, gy, Lm = bx + bw / 2, by + 150.0, 92.0
    hp = (ox, gy - Lm * math.cos(ALPHA))
    rear, front = (ox - Lm * math.sin(ALPHA), gy), (ox + Lm * math.sin(ALPHA), gy)
    o.append(H.line(s, bx + 18, gy, bx + bw - 18, gy, I["rule"], "axis"))
    o.append(link(s, *rear, *hp, S1))
    o.append(link(s, *front, *hp))
    o.append(mass(s, *hp, 7))
    o.append(H.joint_centre(s, *front))
    o.append(H.label(s, front[0] + s(4), gy + s(20), "new stance", "label2", anchor="middle"))
    o.append(H.label(s, rear[0] - s(4), gy + s(20), "new swing", "label2", S1, "middle"))
    o.append(H.label(s, ox, by + s(24), "at heel strike the legs swap roles", "label2", anchor="middle"))
    o.append(H.label(s, ox, by + s(44), "θ̇⁺ = θ̇⁻ cos 2α  (Prop 4.1)", "label2", anchor="middle"))
    o.append(H.label(s, ox, gy + s(46), f"cos 2α = {math.cos(2 * ALPHA):.3f}: {math.sin(2 * ALPHA) ** 2 * 100:.0f} % of",
                     "label2", I["secondary"], "middle"))
    o.append(H.label(s, ox, gy + s(62), "the kinetic energy is lost each step", "label2", I["secondary"], "middle"))
    o.append(LB.credit(s, 20, fy + s(46), width=720, extra=" Lines and hip mass: the compass-gait model."))
    aria = ("Compass gait model drawn over a faded walking skeleton just before heel strike. Two straight legs of "
            "length l meet at a hip mass M. The rear leg is the stance leg, pinned at the stance foot, at angle theta "
            "from the vertical; the front leg is the swing leg at angle phi, about to make the next heel strike. Both "
            f"are {AD:.1f} degrees from the vertical, an inter-leg angle of {2 * AD:.1f} degrees. A panel at right "
            "shows the relabeling at heel strike: the front leg becomes the new stance leg, the rear leg the new swing "
            f"leg, and the angular velocity is scaled by cos 2 alpha, {math.cos(2 * ALPHA):.3f}, so 45 percent of the kinetic energy is "
            "lost.")
    return finish(VB, aria, s, o)


# ================================================================ svg #7  Fig. 6 velocity redirection
def _transition(s, p, ox, fy, k, kv, push):
    """One panel: old and new pendulum arcs meeting at the transition, velocities drawn from the COM."""
    o = []
    A, B = (ox + 70.0, fy), (ox + 70.0 + k * L_STAR, fy)
    C = ((A[0] + B[0]) / 2, fy - k * ELL * math.cos(ALPHA))
    R = k * ELL
    old = [(A[0] + R * math.sin(t), fy - R * math.cos(t)) for t in np.linspace(-ALPHA, ALPHA, 60)]
    new = [(B[0] + R * math.sin(t), fy - R * math.cos(t)) for t in np.linspace(-ALPHA, ALPHA, 60)]
    o.append(H.line(s, A[0] - 60, fy, B[0] + 60, fy, I["rule"], "axis"))
    o.append(poly(s, old, I["muted"], "geom", dash=H.DASH_REF))
    o.append(poly(s, new, O["geometry"], "geom", dash=H.DASH_REF))
    o.append(H.line(s, *A, *C, I["rule"], "ref") + H.line(s, *B, *C, I["rule"], "ref"))
    o.append(H.joint_centre(s, *A) + H.joint_centre(s, *B))
    o.append(H.label(s, A[0], fy + s(20), "old contact", "label2", I["secondary"], "middle"))
    o.append(H.label(s, B[0], fy + s(20), "new contact", "label2", I["secondary"], "middle"))
    vm = (math.cos(ALPHA), math.sin(ALPHA))            # incoming: perpendicular to AC, forward and down
    vp = (math.cos(ALPHA), -math.sin(ALPHA))           # outgoing: perpendicular to BC, forward and up
    Q = lambda v, d: (C[0] + kv * v * d[0], C[1] + kv * v * d[1])  # noqa: E731
    q = Q(V, vm)
    o.append(H.arrow(s, p, *C, *q, "dim"))
    o.append(H.label(s, q[0] + s(4), q[1] + s(18), it("v") + "⁻", "label", I["secondary"], "middle"))
    if not push:
        e = Q(V * math.cos(2 * ALPHA), vp)
        o.append(H.arrow(s, p, *q, *e, "reaction"))
        o.append(H.arrow(s, p, *C, *e, "geometry"))
        o.append(H.label(s, e[0] + s(4), e[1] - s(8), it("v") + "⁺", "label", O["geometry"], "middle"))
        m = pt(q, e, 0.45)
        o.append(H.label(s, m[0] + s(10), m[1] + s(4), "heel strike", "label2"))
        o.append(angle_arc(s, *C, 46, math.degrees(-ALPHA), math.degrees(ALPHA), I["secondary"]))
        o.append(H.label(s, C[0] + 52, C[1] + s(5), "2α", "label2", I["secondary"]))
        rows = [f"v⁻ = {V:.2f} m/s along the old arc",
                f"heel strike removes v sin 2α = {V * math.sin(2 * ALPHA):.2f} m/s",
                f"v⁺ = v cos 2α = {V * math.cos(2 * ALPHA):.2f} m/s",
                f"lost: ½Mv² sin² 2α = {E_COLL:.1f} J per step"]
        return o, C, rows
    vmid = V / math.cos(ALPHA)
    a = Q(vmid, (1.0, 0.0))                            # after push-off: horizontal, v/cos α
    e = Q(V, vp)
    o.append(H.arrow(s, p, *q, *a, "force"))
    o.append(H.arrow(s, p, *C, *a, "dim"))
    o.append(H.arrow(s, p, *a, *e, "reaction"))
    o.append(H.arrow(s, p, *C, *e, "geometry"))
    o.append(H.label(s, e[0] + s(4), e[1] - s(8), it("v") + "⁺", "label", O["geometry"], "middle"))
    o.append(H.label(s, q[0] + s(10), (q[1] + a[1]) / 2 + s(10), "push-off", "label2", O["force"]))
    o.append(H.label(s, a[0] + s(8), (a[1] + e[1]) / 2 + s(6), "heel strike", "label2"))
    rows = [f"push-off along the trailing leg adds v tan α = {V * math.tan(ALPHA):.2f} m/s:",
            f"the COM moves level at v/cos α = {vmid:.2f} m/s (grey, middle)",
            f"heel strike removes {vmid * math.sin(ALPHA):.2f} m/s: v⁺ = {V:.2f} m/s",
            f"lost, and resupplied by the push-off: ½Mv² tan² α = {E_SPLIT:.1f} J,",
            f"{E_SPLIT / E_COLL:.3f} of the collision-only cost"]
    return o, C, rows


def fig7():
    p = "m8f7_"
    VB = (0, 0, 760, 462)
    s = H.Scale(VB[2], VB[3])
    o = [defs(p, s)]
    fy, k, kv = 285.0, 190.0, 100.0
    titles = ("collision only", "push-off, then collision")
    for (ox, push), t1 in zip(((15.0, False), (388.0, True)), titles):
        q, C, rows = _transition(s, p, ox, fy, k, kv, push)
        o += q
        o.append(H.com_mark(s, *C))
        o.append(H.label(s, ox, 28, t1, "label"))
        o.append(lines(s, ox, fy + s(50), rows, "label2"))
    o.append(H.line(s, 375, 14, 375, 412, GRID, "axis"))
    o.append(lines(s, 20, 426, [f"Reference gait: M = 70 kg, v = 1.3 m/s, L = {L_STAR:.3f} m, ℓ = 0.95 m, "
                                f"2α = {2 * AD:.1f}°. Dashed: old arc (grey), new arc (blue).",
                                "From the COM: velocity in (grey) and out (blue); impulses per unit mass: push-off "
                                "(red), heel strike (black)."], "label2", I["secondary"]))
    aria = ("Two velocity diagrams at the step-to-step transition, where the old inverted-pendulum arc about the old "
            "contact meets the new arc about the new contact. Left, collision only: the incoming velocity, 1.3 metres "
            "per second along the old arc, is turned through 2 alpha, 42.2 degrees, by the heel strike alone, which "
            "removes the component 0.87 metres per second along the new leg and leaves 0.96; 26.7 joules are lost "
            "per step. Right, push-off first: an impulse along the trailing leg turns the velocity through alpha and "
            "raises it to 1.39 metres per second; the heel strike then turns it through the remaining alpha and "
            "returns it to 1.3. Only 8.8 joules are lost, 0.330 of the collision-only cost.")
    return finish(VB, aria, s, o)


# ================================================================ svg #10  Fig. 9 arm swing
def fig10():
    p = "m8f10_"
    VB = (0, 0, 760, 480)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    hb, fy = 330.0, 380.0
    o = [defs(p, s)]
    P = LB.pose(**LB.POSES["gait_heel_strike"])
    svg, J = LB.draw("", s, P, 0.0, fy, hb)
    svg, J = LB.draw("", s, P, 95.0 - J["bbox"][0], fy, hb)
    o.append(floor(s, 20, 370, fy))
    o.append(svg)
    o.append(H.label(s, J["toe_far"][0], fy + s(20), "left leg back", "label2", anchor="middle"))
    o.append(H.label(s, J["heel"][0] + s(10), fy + s(20), "right leg forward", "label2", anchor="middle"))
    o.append(H.label(s, J["fingertip_far"][0] + s(8), J["fingertip_far"][1], "left arm forward", "label2"))
    o.append(H.label(s, J["fingertip"][0] - s(8), J["fingertip"][1], "right arm back", "label2", anchor="end"))
    o.append(H.label(s, 20, 26, "side view at right heel strike", "label"))
    o.append(H.label(s, 20, 44, "near (light) limbs = right, far (shaded) = left", "label2", I["secondary"]))
    # ---- right: plan view, subject facing up the page; masses and speeds relative to the trunk (lines 540-544)
    cx, cy, km, kvel = 585.0, 205.0, 520.0, 62.0
    o.append(H.label(s, 420, 26, "seen from above, facing up the page", "label"))
    o.append(H.label(s, 420, 44, "segments as point masses, speeds relative to the trunk", "label2", I["secondary"]))
    o.append(f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{km * 0.20:.2f}" ry="{km * 0.07:.2f}" fill="{BOXFILL}" '
             f'stroke="{I["rule"]}" stroke-width="{s(1):.2f}"/>')
    o.append(H.line(s, cx, cy - km * 0.07 - s(6), cx, cy + km * 0.07 + s(6), I["rule"], "leader", dash=H.DASH_REF))
    assert (S0, S1) == (O["force"], O["geometry"])      # leg arrows use the force head, arm arrows the geometry head
    items = [(-0.09, -1.3, "left leg"), (0.09, 1.3, "right leg"), (-0.20, 0.6, "left arm"), (0.20, -0.6, "right arm")]
    for yoff, vx, nm in items:
        leg = "leg" in nm
        x, col = cx + km * yoff, (S0 if leg else S1)
        y = cy + (s(10) if leg else 0)
        tip = y - kvel * vx
        o.append(H.arrow(s, p, x, y, x, tip, "force" if leg else "geometry"))
        o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(7 if leg else 5):.2f}" fill="{col}" stroke="#fff" '
                 f'stroke-width="{s(1.5):.2f}"/>')
        side = 1 if yoff > 0 else -1
        o.append(H.label(s, x + side * s(9), tip + (s(14) if vx > 0 else -s(4)), f"{abs(vx):g} m/s", "tick", col,
                         "start" if side > 0 else "end"))
    for yoff, vx, nm in items:
        x = cx + km * yoff
        leg = "leg" in nm
        y = cy + (s(10) if leg else 0)
        yy = y + s(24) if vx > 0 else y - s(14)
        o.append(H.label(s, x, yy, nm, "label2", anchor="middle"))
    o.append(arc_arrow(s, p, cx, cy, 150, 160, 20, "force", S0))
    o.append(H.label(s, cx, cy + 150 + s(18), f"legs: {H_LEGS:.2f} kg m²/s, counter-clockwise", "label2", S0, "middle"))
    o.append(arc_arrow(s, p, cx, cy, 128, -150, -30, "geometry", S1))
    o.append(H.label(s, cx, cy - 128 - s(8), f"arms: {H_ARMS:.2f} kg m²/s, clockwise", "label2", S1, "middle"))
    ty = 392.0
    o.append(lines(s, 420, ty, ["legs: 2 × 11.3 kg × 0.09 m × 1.3 m/s",
                                "arms: 2 × 3.5 kg × 0.20 m × 0.6 m/s",
                                f"residual {H_RES:.2f} kg m²/s ({H_ARMS / H_LEGS * 100:.0f} % cancelled): trunk yaw",
                                f"torque {TQ_STILL:.1f} N m arms still, {TQ_SWING:.1f} N m swinging"], "label2"))
    o.append(LB.credit(s, 20, fy + s(44), width=370))
    aria = ("Left: a walking skeleton seen from the side at right heel strike, with the right leg forward, the left "
            "leg back, the left arm forward and the right arm back. Right: the same walker seen from above as point "
            "masses about the trunk. The legs (red) move 1.3 metres per second in opposite directions at 0.09 metres "
            "from the midline, giving 2.64 kilogram metres squared per second about the vertical axis; the arms "
            "(blue) move 0.6 metres per second the other way at 0.20 metres, giving 0.84 in the opposite sense. The "
            "residual 1.80 needs a trunk yaw torque of 6.8 newton metres, against 10.0 with the arms held still.")
    return finish(VB, aria, s, o)


# ================================================================ svg #11  Fig. 10 passive walker on a slope
def fig11():
    p = "m8f11_"
    VB = (0, 0, 760, 450)
    s = H.Scale(VB[2], VB[3])
    o = [defs(p, s)]
    k = 300.0
    gx, gy = 40.0, 345.0                                       # slope point at the left end
    su = (math.cos(GAM), math.sin(GAM))                       # down-slope unit (screen, +y down)
    nu = (math.sin(GAM), -math.cos(GAM))                      # slope normal, upward
    Sxy = lambda d: (gx + d * su[0], gy + d * su[1])  # noqa: E731
    o.append(H.line(s, *Sxy(0), *Sxy(690), I["secondary"], "axis"))
    for d in np.arange(10, 690, 22):
        a = Sxy(d)
        o.append(H.line(s, a[0], a[1], a[0] - s(8), a[1] + s(9), I["rule"], "leader"))
    # horizontal reference and gamma
    ga = Sxy(420)
    o.append(dline(s, *ga, ga[0] + 250, ga[1], I["rule"], "leader"))
    o.append(angle_arc(s, ga[0], ga[1], 230, 0, math.degrees(GAM), O["geometry"]))
    o.append(H.label(s, ga[0] + 240, ga[1] - s(6), f"γ = {math.degrees(GAM):.2f}°", "label2", O["geometry"], "end"))
    o.append(H.label(s, ga[0] + 10, ga[1] - s(6), "horizontal", "label2", I["secondary"]))
    # the walker at heel strike: legs at +-alpha about the slope normal, step L = 2 l sin(alpha) along the slope
    d0 = 210.0
    rear, front = Sxy(d0), Sxy(d0 + k * L_P)
    mid = Sxy(d0 + k * L_P / 2)
    hp = (mid[0] + k * ELL * math.cos(AP) * nu[0], mid[1] + k * ELL * math.cos(AP) * nu[1])
    o.append(dline(s, *mid, hp[0] + nu[0] * s(30), hp[1] + nu[1] * s(30), O["dim"]))
    o.append(link(s, *rear, *hp))
    o.append(link(s, *front, *hp, S1))
    o.append(mass(s, *hp, 10))
    ang_n = math.degrees(math.atan2(-nu[1], -nu[0]))           # screen angle of the downward normal from the hip
    apd = math.degrees(AP)
    o.append(angle_arc(s, hp[0], hp[1], 70, ang_n, ang_n + apd, O["geometry"]))
    o.append(angle_arc(s, hp[0], hp[1], 70, ang_n - apd, ang_n, O["geometry"]))
    for sg in (1, -1):
        a = math.radians(ang_n + sg * (apd + 7))
        o.append(H.label(s, hp[0] + 74 * math.cos(a), hp[1] + 74 * math.sin(a) + s(5), it("α"), "label", O["geometry"],
                         "end" if sg > 0 else "start"))
    o.append(H.arrow(s, p, hp[0] + s(3), hp[1] + s(12), hp[0] + s(3), hp[1] + 150, "load"))
    o.append(H.label(s, hp[0] + s(10), hp[1] + 146, it("Mg"), "label", O["load"]))
    o.append(H.label(s, hp[0] + s(16), hp[1] - s(8), "hip mass " + it("M"), "label2"))
    o.append(H.label(s, hp[0] - s(16), hp[1] - s(8), f"α = {AP:.2f} rad = {apd:.1f}°", "label2", O["geometry"], "end"))
    o.append(H.joint_centre(s, *rear))
    o.append(dot(s, *front, O["flag"], 5))
    o.append(H.label(s, front[0] + s(10), front[1] + s(26), "heel strike", "label2", O["flag"]))
    o.append(H.label(s, rear[0] - s(8), rear[1] + s(26), "trailing foot", "label2", anchor="end"))
    o.append(H.label(s, mid[0] - s(6), mid[1] - 60, "slope normal", "label2", I["secondary"], "end"))
    # step length and drop
    off = (nu[0] * -s(48), nu[1] * -s(48))
    a, b = (rear[0] + off[0], rear[1] + off[1]), (front[0] + off[0], front[1] + off[1])
    o.append(H.arrow(s, p, *a, *b, "geometry", both=True))
    o.append(H.label(s, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + s(18), f"step L = 2ℓ sin α = {L_P:.3f} m", "label2",
                     O["geometry"], "middle"))
    o.append(H.label(s, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + s(34),
                     f"the hip mass drops L sin γ = {L_P * math.sin(GAM) * 100:.1f} cm per step", "label2", I["secondary"],
                     "middle"))
    # energy budget
    bx, by = 470.0, 70.0
    o.append(box(s, bx, by, 278, 130))
    o.append(lines(s, bx + 12, by + s(22), [
        f"gravity in: MgL sin γ = {E_IN:.1f} J per step",
        f"heel strike out: ½Mv² sin² 2α = {E_IN:.1f} J",
        f"balance at v = {V_EXACT:.2f} m/s (exact, K9)",
        f"small-angle form v² ≈ gℓ sin γ / α: {V_SMALL:.2f} m/s",
        "Prop 9.1 limit cycle; on the level, v = 0"], "label2"))
    o.append(H.label(s, 20, 26, f"passive compass walker, no motor: ℓ = 0.95 m, M = 70 kg, γ = {GAM:.2f} rad", "label"))
    aria = ("A compass walker on a downhill slope of gamma 0.05 radians, 2.86 degrees: two straight legs of length "
            "0.95 metres meet at a hip mass M, each at alpha 0.30 radians, 17.2 degrees, from the slope normal, the "
            "rear foot trailing and the front foot at heel strike. The step along the slope is 0.561 metres and the "
            "mass drops 2.8 centimetres per step. A box gives the energy budget: gravity supplies 19.3 joules per step "
            "and the heel strike dissipates 19.3 joules when the speed is 1.31 metres per second; the small-angle "
            "formula gives 1.25.")
    return finish(VB, aria, s, o)


# ================================================================ svg #12  Fig. 11 older-adult fall stack
def fig12():
    p = "m8f12_"
    VB = (0, 0, 760, 540)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    hb, fy = 270.0, 320.0
    k = hb / H_M
    o = [defs(p, s)]
    # tripping walker: swing toe caught on an obstacle beside the stance foot, trunk pitched forward
    P = LB.pose(pelvis=8, trunk=8, near=dict(hip=8, knee=6, shoulder=40, elbow=30),
                far=dict(hip=55, knee=70, contact=None, ankle=-20, shoulder=30, elbow=20), anchor=("heel", "near"))
    svg, J = LB.draw("", s, P, 0.0, fy, hb)
    svg, J = LB.draw("", s, P, 70.0 - J["bbox"][0], fy, hb)
    o.append(floor(s, 20, 340, fy))
    o.append(svg)
    toe = J["toe_far"]
    o.append(f'<rect x="{toe[0] + s(1):.2f}" y="{fy - s(14):.2f}" width="{s(22):.2f}" height="{s(14):.2f}" '
             f'fill="{O["load"]}" fill-opacity="0.75"/>')
    o.append(H.label(s, toe[0] + s(30), fy - s(4), "trip", "label2", O["load"]))
    c = J["com"]
    o.append(H.com_mark(s, *c))
    o.append(H.arrow(s, p, c[0] + s(8), c[1], c[0] + s(8) + 100 * XD, c[1], "geometry"))
    o.append(H.label(s, c[0] + s(12), c[1] - s(10), "COM, 0.45 m/s", "label2", O["geometry"]))
    x_or = c[0] - k * XC                                         # stance contact: the COM is 0.03 m ahead of it
    o.append(cop_mark(s, x_or, fy))
    # number line of Prop 10.1 (lines 629, 644), its own scale
    ky, k2 = 420.0, 600.0
    X = lambda m: 40.0 + k2 * m  # noqa: E731
    o.append(H.line(s, X(0), ky, X(0.45), ky, I["axis"], "axis"))
    for m in (0, 0.1, 0.2, 0.3, 0.4):
        o.append(H.line(s, X(m), ky, X(m), ky + s(5), I["axis"], "axis"))
        o.append(H.label(s, X(m), ky + s(18), f"{m:.1f}", "tick", I["primary"], "middle"))
    o.append(H.label(s, X(0.45) + s(4), ky + s(18), "m", "tick", I["secondary"]))
    segs = [(0, XC, I["primary"]), (XC, XC + XD * DEL, O["flag"]), (XC + XD * DEL, CAP, O["geometry"])]
    for a, b, col in segs:
        o.append(f'<line x1="{X(a):.2f}" y1="{ky - s(6):.2f}" x2="{X(b):.2f}" y2="{ky - s(6):.2f}" stroke="{col}" '
                 f'stroke-width="{s(6):.2f}"/>')
    o.append(H.label(s, X(XC + XD * DEL / 2), ky - s(40), f"delay drift ẋΔ = {XD * DEL:.3f}", "label2", O["flag"], "middle"))
    o.append(H.label(s, X(XC + XD * DEL + XD / W0 / 2), ky - s(18), f"ẋ/ω₀ = {XD / W0:.3f}", "label2", O["geometry"],
                     "middle"))
    for xm in (CAP, REACH):
        o.append(H.line(s, X(xm), ky - s(32), X(xm), ky, I["primary"], "geom"))
    o.append(H.arrow(s, p, X(CAP), ky - s(24), X(REACH), ky - s(24), "dim", both=True))
    o.append(H.label(s, (X(CAP) + X(REACH)) / 2, ky - s(30), f"margin {MARGIN:.3f}", "label2", anchor="middle"))
    o.append(H.label(s, X(CAP) + s(18), ky + s(36), f"capture point {CAP:.3f}", "label2", anchor="end"))
    o.append(H.label(s, X(REACH) - s(18), ky + s(36), f"reach {REACH:.3f}", "label2"))
    o.append(H.label(s, 20, ky + s(56), "from the stance contact (blue mark): x = 0.03 m, ẋ = 0.45 m/s,", "label2",
                     I["secondary"]))
    o.append(H.label(s, 20, ky + s(72), "Δ = 0.20 s, ω₀ = 3.21 s⁻¹; black: x, the COM ahead of the contact", "label2",
                     I["secondary"]))
    o.append(H.label(s, 20, 26, "physics: can a step catch the COM?", "label"))
    o.append(H.label(s, 20, 44, "x + ẋΔ + ẋ/ω₀ ≤ step reach (Prop 10.1)", "label2", I["secondary"]))
    # ---- right: the causal stack, read bottom to top
    bx, bw, bh, gap = 400.0, 345.0, 74.0, 22.0
    layers = [("physics: the visible fall event", ["toe clearance, reaction delay,", "step reach, COM speed, impact path"]),
              ("biology: the control reserve", ["sarcopenia, coarser motor units, noisy", "vestibular, visual, proprioceptive signals"]),
              ("chemistry and materials: the substrate", ["vitamin D, Ca–PTH, inflammation, glycation,",
                                                          "drugs; bone density, collagen cross-links"])]
    ys = [70.0 + i * (bh + gap) for i in range(3)]
    for (t, rows), y in zip(layers, ys):
        o.append(box(s, bx, y, bw, bh))
        o.append(H.label(s, bx + 12, y + s(22), t, "label"))
        o.append(lines(s, bx + 12, y + s(42), rows, "label2", I["secondary"]))
    for y_lo, y_hi in ((ys[2], ys[1] + bh), (ys[1], ys[0] + bh)):
        o.append(H.arrow(s, p, bx + 40, y_lo - s(2), bx + 40, y_hi + s(3), "dim"))
    o.append(H.label(s, bx + 52, ys[2] - s(6), "sets", "label2", I["secondary"]))
    o.append(H.label(s, bx + 52, ys[1] - s(6), "sets", "label2", I["secondary"]))
    o.append(H.label(s, bx, 44, "read bottom to top", "label2", I["secondary"]))
    yp = ys[2] + bh + 26.0
    o.append(box(s, bx, yp, bw, 82, "#fff", I["rule"]))
    o.append(H.label(s, bx + 12, yp + s(22), "after the fall: biology and chemistry", "label"))
    o.append(lines(s, bx + 12, yp + s(42), ["pain and fear: unloading, less activity; sarcopenia,",
                                             "bone loss, inflammation: the next fall is more likely"], "label2",
                   I["secondary"]))
    o.append(f'<path d="M{bx + bw:.2f},{ys[0] + bh / 2:.2f} C{bx + bw + 13:.2f},{ys[0] + bh / 2:.2f} '
             f'{bx + bw + 13:.2f},{yp + 41:.2f} {bx + bw + 2:.2f},{yp + 41:.2f}" fill="none" stroke="{O["dim"]}" '
             f'stroke-width="{s(H.PX["ref"]):.2f}" marker-end="url(#{p}a_dim)"/>')
    o.append(f'<path d="M{bx:.2f},{yp + 60:.2f} C{bx - 16:.2f},{yp + 60:.2f} {bx - 16:.2f},{ys[1] + bh / 2:.2f} '
             f'{bx - 2:.2f},{ys[1] + bh / 2:.2f}" fill="none" stroke="{O["dim"]}" stroke-width="{s(H.PX["ref"]):.2f}" '
             f'marker-end="url(#{p}a_dim)"/>')
    o.append(LB.credit(s, 20, VB[3] - s(24), width=720))
    aria = ("Left: a walking skeleton trips, its swing toe caught on a low obstacle, its centre of mass moving forward "
            "at 0.45 metres per second. Below, a number line from the stance contact adds the centre-of-mass offset "
            "0.030 metres, the drift during a 0.20 second reaction delay, 0.090, and the speed over omega zero, 0.140, "
            "to a capture point at 0.260 metres; against a step reach of 0.415 metres the margin is 0.155. Right: the "
            "causal stack read from bottom to top, chemistry and materials setting biology and biology setting the "
            "physics of the visible fall; an arrow from the fall leads to the post-fall biology and chemistry, which "
            "feed back into the biology layer.")
    return finish(VB, aria, s, o)


FIGS = {
    2: ("Gait cycle showing heel strike, midstance, toe off, swing, a", fig2),
    3: ("Gait-cycle timeline for one stride: right and left leg stanc", fig3),
    4: ("Inverted pendulum COM arc with leg length ell, angle alpha, ", fig4),
    5: ("Plantar foot with COP path from heel to toe (lateral then me", fig5),
    6: ("Compass gait schematic with stance leg pivot, swing leg angl", fig6),
    7: ("Velocity redirection diagram showing old arc, new arc, colli", fig7),
    10: ("Side view of a Winter-proportion walker with reciprocal arm ", fig10),
    11: ("A compass walker on a downhill slope: two legs at plus and m", fig11),
    12: ("Older adult fall stack: chemistry biology physics fall stack", fig12),
}
