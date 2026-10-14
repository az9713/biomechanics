"""Module 7 whole-body figures (main text). Exposes the Lynch body kit once per page.

svg #2 (Fig. 1 two pendulums), #3 (Fig. 2 standing body, COM, base of support), #4 (Fig. 3 extrapolated COM),
#5 (Fig. 4 foot pressure and COP), #7 (Fig. 6 inverted-pendulum free body), #8 (Fig. 7 COP behind the
accelerating COM), #15 (Fig. 14 animated sway), #16 (Fig. 15 ankle vs hip strategy), #17 (Fig. 16 co-contraction
and knee locking), #18 (Fig. 17 lumbar vertebrae and discs), #19 (Fig. 18 stooped lift about L5/S1).
Displayed figure numbers count every <figure> of module07.html (svg #3 and #18 have no FIG marker).

Numbers (module07.html line numbers):
  stature h = 1.75 m, COM 0.55 h above the floor (144, 263); ankle height h_a = 0.06 m, l = 0.90 m (263);
  quiet-standing COM 0.02 m ahead of the ankle, usable base 0.12 m ahead / 0.05 m behind the ankle (176);
  M = 70 kg, I = 66 kg m^2, Mgl = 618 N m/rad, omega0 = sqrt(Mgl/I) = 3.06 1/s (357-360, 314);
  point-mass omega0 = sqrt(g/l) for the extrapolated COM (182-185, Fig. 3 caption 190);
  Kp = 900, Kd = 120, Delta_crit ~ 0.13 s, f ~ 0.35 Hz (493-494); Lab 1 simulate() (620-639);
  intrinsic stiffness 0.9 Mgl (425); m_t = 35 kg, r_t = 0.30 m, m_L = 20 kg, r_L = 0.40 m, d = 0.05 m (599-603).
Body art: lynch_body.py (Patrick J. Lynch, CC BY 2.5). One body unit U = 1.75 m / H_U.
"""
import base64
import html
import math
import re
from urllib.parse import quote

import numpy as np

import house as H
import lynch_body as LB

SHARED_DEFS = LB.SHARED_DEFS
T, O, I = H.TISSUE, H.OVERLAY, H.INK
BOXFILL = "#f7f4ef"
GRID = "#e6e6e6"

# ---------------------------------------------------------------- module constants (line numbers above)
G = 9.81
H_M = 1.75                       # stature (m)
M_KG, I_ANK, MGL = 70.0, 66.0, 618.0
ELL = 0.90                       # ankle to COM (m)
W0 = math.sqrt(MGL / I_ANK)      # 3.06 1/s, distributed body
W0_PM = math.sqrt(G / ELL)       # 3.30 1/s, point mass (sec. 1)
D_TOE, D_HEEL, COM_AHEAD = 0.12, 0.05, 0.02
KP, KD = 900.0, 120.0
UM = LB.H_U / H_M                # body units per metre
ANK = LB.LJ["ankle"]
COM_STD = (ANK[0] + COM_AHEAD * UM, -0.55 * LB.H_U)          # the text's standing COM, body units
ALPHA0 = math.degrees(math.atan2(COM_STD[0] - ANK[0], ANK[1] - COM_STD[1]))   # 1.28 deg: its lean at rest


# ---------------------------------------------------------------- small helpers
def it(v):
    return f'<tspan font-style="italic">{v}</tspan>'


def esc(t):
    return html.escape(t)


def finish(vb, aria, s, body, extra=""):
    body = "".join(body)
    body = re.sub(r'<marker id="([^"]+)".*?</marker>',                   # drop arrowheads the figure never uses
                  lambda m: m.group(0) if f"url(#{m.group(1)})" in body else "", body)
    return H.svg_open(vb, esc(aria), s, extra) + body + "</svg>"


def defs(p, s):
    return f"<defs>{H.markers(p, s)}</defs>"


def poly(s, pts, col, w="curve", dash=None, extra=""):
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    return (f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="none" stroke="{col}" '
            f'stroke-width="{s(H.PX[w]):.2f}" stroke-linejoin="round"{da} {extra}/>')


def path_d(pts, close=True):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + ("Z" if close else "")


def white_under(s, x1, y1, x2, y2, w=4):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#fff" '
            f'stroke-width="{s(w):.2f}" opacity="0.85"/>')


def vline(s, x, y1, y2, col, dash=H.DASH_REF, w="ref"):
    """A dashed reference line with a white under-stroke so it reads over the art."""
    return white_under(s, x, y1, x, y2) + H.line(s, x, y1, x, y2, col, w, dash=dash)


def leader(s, x1, y1, x2, y2, col=None):
    return H.line(s, x1, y1, x2, y2, col or I["secondary"], "leader")


def floor(s, x0, x1, y):
    return H.line(s, x0, y, x1, y, I["rule"], "axis")


def dim_h(s, p, x1, x2, y, meaning="geometry", tick=6):
    """Horizontal dimension with heads at both ends and end ticks."""
    col = O[meaning]
    return (H.arrow(s, p, x1, y, x2, y, meaning, both=True)
            + H.line(s, x1, y - s(tick), x1, y + s(tick), col, "leader")
            + H.line(s, x2, y - s(tick), x2, y + s(tick), col, "leader"))


def arc_arrow(s, p, cx, cy, r, a0, a1, meaning, w=None, both=False):
    """Circular arc from angle a0 to a1 (deg, screen: 0 = +x, + = clockwise) with a head at a1 (both: and a0)."""
    n = 24
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    w = w or {"geometry": "geom", "dim": "ref"}.get(meaning, "force")
    return (f'<path d="{path_d(pts, False)}" fill="none" stroke="{O[meaning]}" stroke-width="{s(H.PX[w]):.2f}" '
            f'marker-end="url(#{p}a_{meaning})"' + (f' marker-start="url(#{p}a_{meaning})"' if both else "") + '/>')


def angle_arc(s, cx, cy, r, a0, a1, col=None):
    n = 16
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return (f'<path d="{path_d(pts, False)}" fill="none" stroke="{col or O["geometry"]}" '
            f'stroke-width="{s(H.PX["geom"]):.2f}"/>')


def cop_mark(s, x, y):
    """Centre of pressure: blue cross-hair circle (a mark, not anatomy)."""
    r, c = s(5.5), O["geometry"]
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="#fff" stroke="{c}" stroke-width="{s(2):.2f}"/>'
            f'<path d="M{x - r * 1.7:.2f},{y:.2f}h{r * 3.4:.2f}M{x:.2f},{y - r * 1.7:.2f}v{r * 3.4:.2f}" '
            f'stroke="{c}" stroke-width="{s(1.4):.2f}"/>')


def xcom_mark(s, x, y):
    """Extrapolated COM: open circle (line 190: open marker)."""
    r = s(6)
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="#fff" stroke="{I["primary"]}" '
            f'stroke-width="{s(2):.2f}"/>')


def dot(s, x, y, col=None, r=3.5):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{col or I["primary"]}" stroke="#fff" stroke-width="{s(1.2):.2f}"/>'


def rot(v, deg):
    return LB.rot(v, deg)


# ---------------------------------------------------------------- the body
def lean(s, theta, x, y, height, p="", **kw):
    """Whole body rigid about the ankle, foot flat; theta = model lean of the ankle-to-COM line (deg, + forward).
    J["comT"] = the text's COM (0.55 H, 0.02 m ahead of the ankle at rest) carried with the body."""
    a = theta - ALPHA0
    P = LB.pose(pelvis=a)
    svg, J = LB.draw(p, s, P, x, y, height, **kw)
    k = J["scale"]
    d = rot((COM_STD[0] - ANK[0], COM_STD[1] - ANK[1]), a)
    J["comT"] = (J["ankle"][0] + k * d[0], J["ankle"][1] + k * d[1])
    return svg, J


def m2u(J, metres):
    """Metres -> figure units for a body drawn with draw()."""
    return metres * UM * J["scale"]


# ---------------------------------------------------------------- foot pressure model (Fig. 2 inset, Fig. 4)
# Right foot, foot frame in metres: x forward from the heel tip, y lateral (+). Foot length = the Lynch foot,
# heel tip to toe tip (155.7 U = 0.274 m at 1.75 m); the ankle (lateral malleolus) is 24.6 U = 0.043 m ahead
# of the heel tip.  Schematic model, not data: the contact patch is a union of ellipses (heel, lateral column,
# forefoot, toes) and the pressure a sum of Gaussian lobes under the foot tripod (calcaneus, 1st and 5th
# metatarsal heads) plus small midfoot and toe lobes.  The heel lobe weight is solved so that the COP sits
# 0.02 m ahead of the ankle, the quiet-standing value of line 176.
FOOT_L = (LB.LAT["toe_x"] - LB.LAT["heel_x"]) / UM
ANK_X = (LB.LAT["ankle"][0] - LB.LAT["heel_x"]) / UM
PATCH = [(0.040, 0.004, 0.040, 0.029), (0.110, 0.026, 0.062, 0.014), (0.185, 0.003, 0.028, 0.046),
         (0.252, -0.026, 0.019, 0.016), (0.246, -0.003, 0.011, 0.009), (0.238, 0.013, 0.010, 0.008),
         (0.228, 0.027, 0.009, 0.008), (0.215, 0.040, 0.008, 0.007)]      # (x, y, rx, ry): heel, lateral
# column, forefoot ball, hallux and the four lesser toes
TRIPOD = {"calcaneus": (0.037, 0.000), "MT1": (0.195, -0.027), "MT5": (0.182, 0.033)}
LOBES_F = [(0.195, -0.027, 0.011, 0.011, 0.26), (0.200, -0.002, 0.012, 0.012, 0.34),
           (0.182, 0.033, 0.011, 0.010, 0.20), (0.251, -0.024, 0.009, 0.009, 0.12),
           (0.246, 0.012, 0.010, 0.018, 0.08)]                            # forefoot lobes, weights sum 1
LOBE_MID = (0.105, 0.026, 0.030, 0.008)                                   # lateral column, weight 0.06 of forefoot
LOBE_HEEL = (0.040, 0.002, 0.021, 0.018)
DXY = 0.002                                                                # model grid (m)


def _gauss(X, Y, x, y, sx, sy):
    return np.exp(-0.5 * (((X - x) / sx) ** 2 + ((Y - y) / sy) ** 2))


def foot_model():
    xs = np.arange(-0.004, FOOT_L + 0.006, DXY)
    ys = np.arange(-0.060, 0.062, DXY)
    X, Y = np.meshgrid(xs, ys)
    S = np.min([((X - x) / rx) ** 2 + ((Y - y) / ry) ** 2 for x, y, rx, ry in PATCH], axis=0)
    mask = S <= 1.0
    fore = sum(w * _gauss(X, Y, x, y, sx, sy) for x, y, sx, sy, w in LOBES_F)
    fore = fore + 0.06 * _gauss(X, Y, *LOBE_MID)
    heel = _gauss(X, Y, *LOBE_HEEL)
    target = ANK_X + COM_AHEAD
    Ff, Fh = (fore * mask).sum(), (heel * mask).sum()
    Mf, Mh = (X * fore * mask).sum(), (X * heel * mask).sum()
    wh = (target * Ff - Mf) / (Mh - target * Fh)          # heel weight putting the centroid at target
    p = (fore + wh * heel) * mask
    cop = ((X * p).sum() / p.sum(), (Y * p).sum() / p.sum())
    return dict(xs=xs, ys=ys, X=X, Y=Y, S=S, p=p / p.max(), cop=cop, heel_share=(wh * Fh) / (wh * Fh + Ff))


def contours(xs, ys, F, level):
    """Marching squares: closed polylines (model units) of F = level (F sampled on ys x xs)."""
    segs = []
    ny, nx = F.shape
    pad = np.full((ny + 2, nx + 2), F.min() - 1.0)
    pad[1:-1, 1:-1] = F
    dx, dy = xs[1] - xs[0], ys[1] - ys[0]
    gx = np.concatenate([[xs[0] - dx], xs, [xs[-1] + dx]])
    gy = np.concatenate([[ys[0] - dy], ys, [ys[-1] + dy]])

    def cut(i0, j0, i1, j1):
        a, b = pad[i0, j0], pad[i1, j1]
        t = (level - a) / (b - a)
        return (round(gx[j0] + t * (gx[j1] - gx[j0]), 6), round(gy[i0] + t * (gy[i1] - gy[i0]), 6))
    for i in range(ny + 1):
        for j in range(nx + 1):
            c = [pad[i, j] > level, pad[i, j + 1] > level, pad[i + 1, j + 1] > level, pad[i + 1, j] > level]
            e = {0: (i, j, i, j + 1), 1: (i, j + 1, i + 1, j + 1), 2: (i + 1, j, i + 1, j + 1), 3: (i, j, i + 1, j)}
            ed = [k for k, (a, b) in enumerate([(0, 1), (1, 2), (3, 2), (0, 3)]) if c[a] != c[b]]
            if len(ed) == 2:
                segs.append((cut(*e[ed[0]]), cut(*e[ed[1]])))
            elif len(ed) == 4:
                segs += [(cut(*e[0]), cut(*e[3])), (cut(*e[1]), cut(*e[2]))]
    nb = {}
    for a, b in segs:
        nb.setdefault(a, []).append(b)
        nb.setdefault(b, []).append(a)
    seen, out = set(), []
    for a0 in list(nb):
        if a0 in seen:
            continue
        line, prev, cur = [a0], None, a0
        seen.add(a0)
        while True:
            nxt = [q for q in nb[cur] if q != prev and q not in seen]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            seen.add(cur)
            line.append(cur)
        if len(line) > 3:
            out.append(rdp(line, 0.0006))
    return out


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    a, b = np.array(pts[0]), np.array(pts[-1])
    d = b - a
    L = math.hypot(*d)
    dist = [abs(d[0] * (q[1] - a[1]) - d[1] * (q[0] - a[0])) / L if L > 1e-12 else math.dist(q, a) for q in pts]
    i = int(np.argmax(dist))
    if dist[i] <= eps or i in (0, len(pts) - 1):
        return [pts[0], pts[-1]]
    return rdp(pts[:i + 1], eps)[:-1] + rdp(pts[i:], eps)


_FM = {}


def fm():
    if "m" not in _FM:
        _FM["m"] = foot_model()
    return _FM["m"]


def footprint(mapf):
    """Contact-patch outline(s) of the model foot through mapf(x, y_lateral) -> figure point."""
    m = fm()
    return [[mapf(x, y) for x, y in c] for c in contours(m["xs"], m["ys"], -m["S"], -1.0)]


# ================================================================ svg #3  Fig. 2: standing body, COM, BoS
def fig3():
    p = "m7f3_"
    hgt, hx, fy = 680.0, 150.0, 760.0                              # stature, heel x, floor y (figure units)
    tmp = H.Scale(760, 900, max_h=H.MAX_DISPLAY_H_BODY)
    body, J = LB.standing_full(p, tmp, hx, fy, hgt)
    k = J["scale"]
    com = (J["ankle"][0] + k * (COM_STD[0] - ANK[0]), fy + k * COM_STD[1])
    x0, y0 = J["bbox"][0] - 70, J["bbox"][1] - 20
    VB = (round(x0), round(y0), 760, round(fy + 64 - y0))
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    o = [defs(p, s), body]
    heel, toe = J["heel"][0], J["toe"][0]
    o.append(floor(s, VB[0] + s(4), toe + s(60), fy))
    o.append(f'<rect x="{heel:.2f}" y="{fy + s(1.5):.2f}" width="{toe - heel:.2f}" height="{s(7):.2f}" '
             f'fill="{BOXFILL}" stroke="{I["secondary"]}" stroke-width="{s(1):.2f}"/>')
    for xx in (heel, toe):
        o.append(H.line(s, xx, fy - s(6), xx, fy + s(13), I["secondary"], "leader"))
    o.append(H.label(s, (heel + toe) / 2, fy + s(29), "base of support (side view): heel to toe", "label2",
                     I["secondary"], "middle"))
    o.append(vline(s, com[0], com[1], fy, O["geometry"]))
    o.append(H.com_mark(s, *com))
    lx = J["bbox"][2] + s(40)
    o.append(leader(s, com[0] + s(9), com[1], lx - s(5), com[1], I["primary"]))
    o.append(H.label(s, lx, com[1] + s(5), "centre of mass (COM)"))
    o.append(H.label(s, lx, com[1] + s(23), "0.55 H above the floor, 0.02 m ahead of the ankle", "label2",
                     I["secondary"]))
    vy = com[1] + 0.13 * hgt
    o.append(leader(s, com[0] + s(3), vy, lx - s(5), vy, O["geometry"]))
    o.append(H.label(s, lx, vy + s(5), "vertical through the COM: it lands inside the base", "label2", O["geometry"]))
    o.append(H.joint_centre(s, *J["ankle"]))
    o.append(leader(s, J["ankle"][0] - s(9), J["ankle"][1] - s(3), J["ankle"][0] - s(34), J["ankle"][1] - s(22)))
    o.append(H.label(s, J["ankle"][0] - s(37), J["ankle"][1] - s(25), "ankle", "label2", I["secondary"], "end"))
    o.append(inset_bos(s, p, lx, y0 + s(16)))
    o.append(LB.credit(s, VB[0] + s(6), fy + s(48), width=VB[2] - s(12)))
    aria = ("Lateral view of a standing human skeleton inside its body outline, facing right, with the arm hanging. "
            "The centre of mass is marked 0.55 of stature above the floor, 2 cm ahead of the ankle; a dashed vertical "
            "drops from it into the base of support, heel to toe. An inset top view shows both footprints, the three "
            "contact points of each foot (heel, first and fifth metatarsal heads) and their convex hull, the base of "
            "support, with the COM projection inside it.")
    return finish(VB, aria, s, o)


def inset_bos(s, p, x0, ytop):
    """Top view (subject faces +x): both footprints, each foot tripod, the convex hull of both = base of support.
    Stance (not in the text, schematic): heel centres 0.13 m apart, each foot turned out 8 deg."""
    sc = s(720)                                      # figure units per metre in the inset
    half_gap, toe_out = 0.065, 8.0
    ax_x = x0 + s(50)                                # ankle axis x in the inset
    y0 = ytop + s(30) + 0.115 * sc                   # midline between the feet
    o = []

    def mapper(sg):                                  # sg = +1 subject's right foot (screen +y), -1 left
        a, xc = math.radians(toe_out * sg), TRIPOD["calcaneus"][0]

        def f(x, y_lat):
            v = (x - xc, sg * y_lat)
            u = (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))
            return (ax_x + (xc - ANK_X + u[0]) * sc, y0 + (sg * half_gap + u[1]) * sc)
        return f
    pts = {}
    for sg in (1, -1):
        f = mapper(sg)
        for c in footprint(f):
            o.append(f'<path d="{path_d(c)}" fill="{T["skin"][0]}" stroke="{T["skin"][1]}" stroke-width="{s(1):.2f}"/>')
        pts[sg] = [f(x, y) for x, y in TRIPOD.values()]
    hull = convex_hull(pts[1] + pts[-1])
    o.append(f'<path d="{path_d(hull)}" fill="{O["geometry"]}" fill-opacity="0.10" stroke="{O["geometry"]}" '
             f'stroke-width="{s(1.6):.2f}" stroke-dasharray="{s(6):.2f} {s(4):.2f}"/>')
    o.append(f'<path d="{path_d(pts[1])}" fill="none" stroke="{I["primary"]}" stroke-width="{s(1.2):.2f}"/>')
    for q in pts[1] + pts[-1]:
        o.append(dot(s, *q))
    cx = ax_x + COM_AHEAD * sc
    o.append(H.com_mark(s, cx, y0))
    bot = max(q[1] for q in hull)
    o.append(H.label(s, x0, ytop + s(12), "top view of both feet (forward = right)", "label2", I["secondary"]))
    right = max(q[0] for q in hull)
    o.append(leader(s, right - s(10), y0 - s(18), right + s(16), y0 - s(18)))
    o.append(H.label(s, right + s(19), y0 - s(22), "convex hull of both", "label2", O["geometry"]))
    o.append(H.label(s, right + s(19), y0 - s(6), "tripods = base of support", "label2", O["geometry"]))
    mt5 = pts[1][2]
    o.append(leader(s, mt5[0] + s(4), mt5[1] + s(4), right + s(16), bot + s(18)))
    o.append(H.label(s, right + s(19), bot + s(16), "one foot&#8217;s tripod: heel,", "label2"))
    o.append(H.label(s, right + s(19), bot + s(32), "1st and 5th metatarsal heads", "label2"))
    o.append(leader(s, cx + s(8), y0 + s(4), cx + s(30), y0 + s(26), I["primary"]))
    o.append(H.label(s, cx + s(32), y0 + s(36), "COM projection", "label2", extra='font-style="italic"'))
    return "".join(o)


def convex_hull(P):
    P = sorted(set(P))

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for q in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(P):
        while len(up) >= 2 and cr(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    return lo[:-1] + up[:-1]


# ================================================================ svg #2  Fig. 1: two pendulums
def fig2():
    p = "m7f2_"
    VB = (0, 0, 760, 560)
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    o = [defs(p, s)]
    fy = 470.0
    o.append(H.line(s, 360, 20, 360, fy + 40, GRID, "axis"))
    # ---- left: a mass hanging below its pivot (schematic pendulum)
    px, py, Lp, th = 165.0, 100.0, 270.0, 20.0
    bx, by = px + Lp * math.sin(math.radians(th)), py + Lp * math.cos(math.radians(th))
    o.append(f'<rect x="{px - 46:.2f}" y="{py - 22:.2f}" width="92" height="14" fill="{BOXFILL}" '
             f'stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
    o.append(H.line(s, px, py - 8, px, py, I["secondary"], "ref"))
    o.append(vline(s, px, py, py + Lp + 40, O["dim"]))
    o.append(H.line(s, px, py, bx, by, I["primary"], "force"))
    o.append(H.joint_centre(s, px, py))
    o.append(H.label(s, px - 12, py + 4, "pivot", "label2", I["secondary"], "end"))
    o.append(angle_arc(s, px, py, 70, 90 - th, 90))
    o.append(H.label(s, px + 8, py + 94, it("θ"), fill=O["geometry"]))
    o.append(f'<circle cx="{bx:.2f}" cy="{by:.2f}" r="20" fill="{BOXFILL}" stroke="{I["primary"]}" '
             f'stroke-width="{s(1.4):.2f}"/>')
    o.append(H.label(s, bx, by + 5, it("m"), anchor="middle"))
    o.append(H.arrow(s, p, bx, by + 20, bx, by + 100, "load"))
    o.append(H.label(s, bx + 9, by + 82, it("mg"), fill=O["load"]))
    o.append(arc_arrow(s, p, px, py, Lp - 60, 90 - th + 1, 90 - 5, "load"))
    o.append(H.label(s, bx + 28, by - 40, "restoring moment:", "label2", O["load"]))
    o.append(H.label(s, bx + 28, by - 24, "gravity pulls it back", "label2", O["load"]))
    o.append(H.label(s, 180, 30, "stable: mass below its pivot", anchor="middle"))
    # ---- right: the standing body balanced above the ankle
    thb, hgt = 10.0, 380.0
    body, J = lean(s, thb, 470.0, fy, hgt, p=p)
    ax, ay = J["ankle"]
    c = J["comT"]
    o.append(body)
    o.append(floor(s, 380, 750, fy))
    o.append(vline(s, ax, ay, ay - 330, O["dim"]))
    o.append(white_under(s, ax, ay, c[0], c[1]) + H.line(s, ax, ay, c[0], c[1], O["geometry"], "geom", dash=H.DASH_REF))
    o.append(angle_arc(s, ax, ay, 120, -90, -90 + thb))
    o.append(H.label(s, ax + 5, ay - 128, it("θ"), fill=O["geometry"]))
    o.append(H.joint_centre(s, ax, ay))
    o.append(H.label(s, ax - 14, ay + 22, "ankle (pivot)", "label2", I["secondary"], "end"))
    o.append(H.com_mark(s, *c))
    o.append(H.arrow(s, p, c[0], c[1] + 9, c[0], c[1] + 110, "load"))
    o.append(H.label(s, c[0] + 9, c[1] + 90, it("Mg"), fill=O["load"]))
    rr = math.dist((ax, ay), c)
    o.append(arc_arrow(s, p, ax, ay, rr + 40, -90 + thb + 2, -90 + thb + 16, "load"))
    e = (ax + (rr + 40) * math.cos(math.radians(-90 + thb + 16)), ay + (rr + 40) * math.sin(math.radians(-90 + thb + 16)))
    o.append(H.label(s, e[0] + 12, e[1] - 4, "toppling moment:", "label2", O["load"]))
    o.append(H.label(s, e[0] + 12, e[1] + 12, "gravity pulls it further", "label2", O["load"]))
    o.append(leader(s, c[0] - 8, c[1] - 2, c[0] - 40, c[1] - 26, I["primary"]))
    o.append(H.label(s, c[0] - 43, c[1] - 30, "COM", "label2", anchor="end"))
    o.append(H.label(s, 560, 30, "unstable: mass above its pivot", anchor="middle"))
    o.append(H.label(s, 560, 48, f"the standing body about the ankle, drawn leaning {thb:.0f}°", "label2",
                     I["secondary"], "middle"))
    o.append(LB.credit(s, 380, fy + 30, width=370))
    aria = ("Two panels. Left: a mass hanging below a fixed pivot, displaced by angle theta; its weight mg pulls it "
            "back toward the vertical, a restoring moment, so it is stable. Right: a skeleton standing on the floor, "
            "leaning forward 10 degrees as one rigid body about the ankle; its weight Mg acts at the centre of mass "
            "above the ankle and pulls it further from the vertical, a toppling moment, so it is unstable.")
    return finish(VB, aria, s, o)


# ================================================================ svg #4  Fig. 3: extrapolated COM
XC_COM, XC_V = 0.08, 0.30          # COM 0.08 m ahead of the ankle, speed 0.30 m/s (design values, see report)


def fig4():
    p = "m7f4_"
    VB = (0, 0, 760, 640)
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    o = [defs(p, s), H.line(s, 380, 20, 380, 560, GRID, "axis")]
    coast = XC_V / W0_PM
    th = math.degrees(math.asin(XC_COM / ELL))
    fy, hgt, zoom_y, zs = 330.0, 280.0, 452.0, 1000.0          # floor, stature, strip y, strip units per metre
    panels = [(XC_V, "COM moving fast toward the toes", "falls: the extrapolated COM is beyond the toe edge"),
              (-XC_V, "same position, moving backward", "recoverable: the extrapolated COM is inside the base")]
    for k, (v, title, verdict) in enumerate(panels):
        x0 = 380.0 * k
        body, J = lean(s, th, x0 + 150, fy, hgt, p=p)
        ax = J["ankle"][0]
        c = J["comT"]
        o.append(body)
        o.append(floor(s, x0 + 20, x0 + 360, fy))
        o.append(H.com_mark(s, *c))
        xv = c[0] + (60 if v > 0 else -60)
        o.append(H.arrow(s, p, c[0] + (10 if v > 0 else -10), c[1] - 24, xv, c[1] - 24, "geometry"))
        o.append(H.label(s, (c[0] + xv) / 2, c[1] - 32, f"{it('v')} = {v:+.2f} m/s".replace("-", "−"), "label2",
                         O["geometry"], "middle"))
        o.append(H.label(s, x0 + 190, 26, title, anchor="middle"))
        sx = lambda m, x0=x0: x0 + 120 + m * zs          # noqa: E731   strip: ankle at the origin, metres
        lo_m, hi_m = -0.07, 0.20
        bx0, bx1 = ax + lo_m * UM * J["scale"], ax + hi_m * UM * J["scale"]
        o.append(H.line(s, bx0, fy + 4, sx(lo_m), zoom_y - 48, I["rule"], "leader"))
        o.append(H.line(s, bx1, fy + 4, sx(hi_m), zoom_y - 48, I["rule"], "leader"))
        o.append(f'<rect x="{sx(-D_HEEL):.2f}" y="{zoom_y - 8:.2f}" width="{(D_HEEL + D_TOE) * zs:.2f}" height="16" '
                 f'fill="{BOXFILL}" stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
        o.append(H.line(s, sx(lo_m), zoom_y, sx(hi_m), zoom_y, I["rule"], "leader"))
        for m, t in ((-D_HEEL, "−5"), (0.0, "0"), (D_TOE, "12")):
            o.append(H.line(s, sx(m), zoom_y + 8, sx(m), zoom_y + 14, I["axis"], "leader"))
            o.append(H.label(s, sx(m), zoom_y + 29, t, "tick", I["secondary"], "middle"))
        o.append(H.label(s, sx(-D_HEEL), zoom_y + 46, "heel edge", "label2", I["secondary"], "middle"))
        o.append(H.label(s, sx(D_TOE), zoom_y + 46, "toe edge", "label2", I["secondary"], "middle"))
        o.append(H.label(s, sx(0.0), zoom_y + 46, "ankle", "label2", I["secondary"], "middle"))
        xx = XC_COM + v / W0_PM
        y1 = zoom_y - 24
        o.append(H.com_mark(s, sx(XC_COM), zoom_y))
        o.append(H.arrow(s, p, sx(XC_COM) + (8 if v > 0 else -8), y1, sx(xx), y1, "dim"))
        o.append(H.label(s, (sx(XC_COM) + sx(xx)) / 2, y1 - 9, f"{it('v')}/ω₀ = {coast * 100:.1f} cm", "label2",
                         I["primary"], "middle"))
        o.append(xcom_mark(s, sx(xx), zoom_y))
        o.append(H.label(s, x0 + 190, 535, verdict, "label2", I["primary"], "middle"))
        lab = (f"{it('x')}{H.sub('com', s, 'label2')} = {XC_COM * 100:.0f} cm,  "
               f"{it('x')}{H.sub('xcom', s, 'label2')} = {xx * 100:.1f} cm").replace("-", "−")
        o.append(H.label(s, x0 + 190, 553, lab, "label2", I["secondary"], "middle"))
    o.append(H.label(s, 380, 366, "floor under each body, magnified: cm from the ankle", "label2", I["secondary"],
                     "middle"))
    o.append(H.com_mark(s, 26, 584))
    o.append(H.label(s, 38, 589, "COM", "label2"))
    o.append(xcom_mark(s, 92, 584))
    o.append(H.label(s, 104, 589, f"extrapolated COM, {it('x')}{H.sub('com', s, 'label2')} + {it('v')}/ω₀", "label2"))
    o.append(H.label(s, 752, 589, f"ω₀ = √(g/ℓ) = {W0_PM:.2f} s⁻¹, ℓ = 0.90 m", "label2", I["secondary"], "end"))
    o.append(LB.credit(s, 8, 610, width=744))
    aria = ("Two panels, each a skeleton leaning 5 degrees forward with its centre of mass 8 cm ahead of the ankle, "
            "over a base of support that runs from 5 cm behind to 12 cm ahead of the ankle, shown magnified below. "
            "Left: the COM moves forward at 0.30 metres per second; the extrapolated COM, 9.1 cm further on, lies "
            "beyond the toe edge: it falls. Right: the same position moving backward; the extrapolated COM lies inside "
            "the base: it can recover.")
    return finish(VB, aria, s, o)


# ================================================================ svg #5  Fig. 4: plantar pressure and its resultant
P_LEVELS = (0.06, 0.18, 0.40, 0.70)          # shaded bands: pressure above these fractions of the peak


def fig5():
    p = "m7f5_"
    VB = (0, 0, 760, 500)
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    m = fm()
    o = [defs(p, s), H.line(s, 318, 20, 318, 400, GRID, "axis")]
    # ---- left: top view, toes up, the right foot
    tsc, bx, by = 1180.0, 175.0, 380.0                         # units per metre; heel tip at (bx, by)
    F = lambda x, y: (bx + y * tsc, by - x * tsc)               # noqa: E731
    for c in contours(m["xs"], m["ys"], -m["S"], -1.0):
        o.append(f'<path d="{path_d([F(*q) for q in c])}" fill="{T["skin"][0]}" stroke="{T["skin"][1]}" '
                 f'stroke-width="{s(1.2):.2f}"/>')
    for lv in P_LEVELS:
        for c in contours(m["xs"], m["ys"], m["p"], lv):
            o.append(f'<path d="{path_d([F(*q) for q in c])}" fill="{O["force"]}" fill-opacity="0.22"/>')
    cop = F(*m["cop"])
    o.append(cop_mark(s, *cop))
    o.append(leader(s, cop[0] + 9, cop[1], 250, cop[1], O["geometry"]))
    o.append(H.label(s, 254, cop[1] + 5, "COP", fill=O["geometry"]))
    hp, m1, m5 = F(*TRIPOD["calcaneus"]), F(*TRIPOD["MT1"]), F(*TRIPOD["MT5"])
    o.append(leader(s, hp[0] - 34, hp[1] + 4, 96, hp[1] + 4))
    o.append(H.label(s, 92, hp[1] + 9, "heel", "label2", anchor="end"))
    o.append(leader(s, m1[0] - 10, m1[1], 96, m1[1]))
    o.append(H.label(s, 92, m1[1] - 3, "1st metatarsal", "label2", anchor="end"))
    o.append(H.label(s, 92, m1[1] + 13, "head", "label2", anchor="end"))
    o.append(leader(s, m5[0] + 10, m5[1], 250, m5[1]))
    o.append(H.label(s, 254, m5[1] - 3, "5th meta-", "label2"))
    o.append(H.label(s, 254, m5[1] + 13, "tarsal head", "label2"))
    o.append(H.label(s, 160, 26, "pressure field p(x, y), right foot from above", "label2", anchor="middle"))
    pct = ", ".join(f"{v * 100:.0f}" for v in P_LEVELS)
    o.append(H.label(s, 160, by + 24, f"shading: p above {pct} % of the peak", "label2", I["secondary"], "middle"))
    # ---- right: side view, the same distribution as a line load, then its resultant
    ssc, hx0 = 1000.0, 345.0
    k = ssc / UM                                                     # figure units per body unit
    q = m["p"].sum(axis=0)                                           # integrate across the foot width
    xs = m["xs"]
    q = q / q.max()
    xr = hx0 + FOOT_L * ssc + 22
    for row, fy in enumerate((150.0, 330.0)):
        ank = (hx0 + ANK_X * ssc, fy - (LB.LAT["floor"] - LB.LAT["ankle"][1]) * k)
        o.append(f'<g transform="translate({ank[0]:.2f} {ank[1]:.2f}) scale({k:.4f})"><use href="#hbody_lat_foot"/></g>')
        o.append(floor(s, hx0 - 18, hx0 + FOOT_L * ssc + 12, fy))
        if row == 0:
            prof = [(hx0 + x * ssc, fy + 5 + 64 * v) for x, v in zip(xs[::2], q[::2]) if v > 0.003]
            for x, v in zip(xs[::5], q[::5]):
                if v > 0.05:
                    X = hx0 + x * ssc
                    o.append(H.arrow(s, p, X, fy + 5 + 64 * v, X, fy + 2, "reaction", w="leader"))
            o.append(poly(s, prof, I["primary"], "ref"))
            o.append(H.label(s, xr, fy + 26, "the distribution:", "label2"))
            o.append(H.label(s, xr, fy + 42, "pressure at", "label2"))
            o.append(H.label(s, xr, fy + 58, "every point", "label2"))
        else:
            X = hx0 + m["cop"][0] * ssc
            o.append(H.arrow(s, p, X, fy + 64, X, fy + 2, "reaction"))
            o.append(H.label(s, X + 12, fy + 54, f"{it('F')}{H.sub('z', s)} = ∫ {it('p')} d{it('A')}"))
            o.append(cop_mark(s, X, fy))
            o.append(H.label(s, xr, fy + 26, "its resultant:", "label2"))
            o.append(H.label(s, xr, fy + 42, "one force at", "label2"))
            o.append(H.label(s, xr, fy + 58, "the COP", "label2"))
    o.append(H.label(s, 330, 26, "side view: the same foot, the same pressure", "label2"))
    o.append(H.label(s, xr + 30, 244, "=", "label", anchor="middle"))
    o.append(H.label(s, 330, 428, f"COP {m['cop'][0] * 100:.1f} cm from the heel, "
                     f"{(m['cop'][0] - ANK_X) * 100:.1f} cm ahead of the ankle", "label2", O["geometry"]))
    o.append(LB.credit(s, 8, 452, width=744, extra=" Pressure field: schematic model, not measured data."))
    aria = ("Left: a right footprint seen from above with the plantar pressure shaded; pressure concentrates under "
            "the heel and the metatarsal heads, and a cross-hair marks the centre of pressure, the pressure-weighted "
            "centroid, 2 cm ahead of the ankle. Right, top: the foot skeleton from the side with the same pressure as "
            "a row of upward arrows along the sole. Right, bottom: the same foot with one upward force F z at the "
            "centre of pressure, statically equivalent to the distribution.")
    return finish(VB, aria, s, o)


# ================================================================ svg #7  Fig. 6: free-body diagram
def fig7():
    p = "m7f7_"
    VB = (0, 0, 760, 600)
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    th, hgt, fy = 10.0, 500.0, 540.0
    body, J = lean(s, th, 300.0, fy, hgt, p=p)
    ax, ay = J["ankle"]
    c = J["comT"]
    o = [defs(p, s), body, floor(s, 120, 640, fy)]
    for i in range(14):
        xx = 130 + 36 * i
        o.append(H.line(s, xx, fy, xx - 12, fy + 12, I["rule"], "leader"))
    o.append(vline(s, ax, ay, c[1] - 40, O["dim"]))
    o.append(white_under(s, ax, ay, c[0], c[1]) + H.line(s, ax, ay, c[0], c[1], O["geometry"], "geom", dash=H.DASH_REF))
    o.append(angle_arc(s, ax, ay, 150, -90, -90 + th))
    o.append(H.label(s, ax + 9, ay - 160, it("θ"), fill=O["geometry"]))
    mid = ((ax + c[0]) / 2, (ay + c[1]) / 2)
    o.append(leader(s, mid[0] + 4, mid[1], mid[0] + 60, mid[1] - 12, O["geometry"]))
    o.append(H.label(s, mid[0] + 64, mid[1] - 8, f"{it('ℓ')} = 0.90 m (ankle to COM)", fill=O["geometry"]))
    # l sin(theta): horizontal from the vertical through O to the COM, at the COM height
    yd = c[1] - 24
    o.append(dim_h(s, p, ax, c[0], yd))
    o.append(H.label(s, (ax + c[0]) / 2, yd - 12, f"{it('ℓ')} sin {it('θ')}", fill=O["geometry"], anchor="middle"))
    o.append(H.com_mark(s, *c))
    o.append(leader(s, c[0] + 8, c[1] + 2, c[0] + 66, c[1] + 2, I["primary"]))
    o.append(H.label(s, c[0] + 70, c[1] + 7, "COM"))
    o.append(H.arrow(s, p, c[0], c[1] + 9, c[0], c[1] + 150, "load"))
    o.append(H.label(s, c[0] + 10, c[1] + 136, it("Mg"), fill=O["load"]))
    o.append(H.label(s, c[0] + 70, c[1] + 40, f"gravity’s moment about {it('O')}:", "label2", O["load"]))
    o.append(H.label(s, c[0] + 70, c[1] + 56, f"{it('Mg ℓ')} sin {it('θ')}, forward (toppling)", "label2", O["load"]))
    o.append(H.joint_centre(s, ax, ay))
    o.append(H.label(s, ax - 14, ay + 4, it("O"), anchor="end"))
    # restoring ankle torque tau: counter-clockwise arc about O (backward)
    o.append(arc_arrow(s, p, ax, ay, 58, -20, -150, "force"))
    o.append(H.label(s, ax - 74, ay - 40, it("τ"), fill=O["force"], anchor="end"))
    o.append(H.label(s, ax - 74, ay - 24, "ankle torque", "label2", O["force"], "end"))
    o.append(H.label(s, ax - 74, ay - 8, "(plantarflexors, restoring)", "label2", O["force"], "end"))
    o.append(H.label(s, 380, 24, f"the body above the ankle as one rigid segment, drawn at {it('θ')} = {th:.0f}°",
                     "label2", I["secondary"], "middle"))
    o.append(LB.credit(s, 120, fy + 30, width=520))
    aria = ("Free-body diagram on a skeleton leaning forward 10 degrees as one rigid segment hinged at the ankle O. "
            "A dashed line from O to the centre of mass has length ell = 0.90 m at angle theta from the vertical; the "
            "weight Mg acts straight down at the centre of mass, with horizontal moment arm ell sin theta, a forward "
            "toppling moment; a curved arrow at the ankle is the restoring ankle torque tau of the plantarflexors.")
    return finish(VB, aria, s, o)


# ================================================================ svg #8  Fig. 7: COP behind the accelerating COM
A_COM, TH8 = 0.8, 7.0               # forward COM acceleration (m/s^2) and drawn lean (deg): design values


def fig8():
    p = "m7f8_"
    VB = (0, 0, 760, 690)
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    hgt, fy = 520.0, 560.0
    body, J = lean(s, TH8, 250.0, fy, hgt, p=p)
    ax, ay = J["ankle"]
    c = J["comT"]
    um = m2u(J, 1.0)
    off = -A_COM / W0 ** 2                                   # Prop. 3.3, metres
    xcop = c[0] + off * um
    acc = f"{it('a')}{H.sub('com', s)}"
    o = [defs(p, s), body, floor(s, 100, 660, fy)]
    for i in range(16):
        xx = 110 + 34 * i
        o.append(H.line(s, xx, fy, xx - 12, fy + 12, I["rule"], "leader"))
    o.append(vline(s, c[0], c[1] + 9, fy, O["dim"]))
    o.append(H.com_mark(s, *c))
    o.append(H.arrow(s, p, c[0] + 10, c[1], c[0] + 120, c[1], "geometry"))
    o.append(H.label(s, c[0] + 130, c[1] + 5, f"COM acceleration {acc} &gt; 0", fill=O["geometry"]))
    o.append(leader(s, c[0] - 8, c[1] - 4, c[0] - 50, c[1] - 30, I["primary"]))
    o.append(H.label(s, c[0] - 54, c[1] - 34, "COM", anchor="end"))
    o.append(H.arrow(s, p, c[0], c[1] + 30, c[0], c[1] + 150, "load"))
    o.append(H.label(s, c[0] + 9, c[1] + 138, it("Mg"), fill=O["load"]))
    o.append(H.arrow(s, p, xcop, fy, xcop, fy - 170, "reaction"))
    o.append(H.label(s, xcop - 10, fy - 140, f"{it('N')} ≈ {it('Mg')}", anchor="end"))
    o.append(dot(s, c[0], fy, I["primary"], 4))
    o.append(cop_mark(s, xcop, fy))
    o.append(H.joint_centre(s, ax, ay))
    o.append(H.label(s, ax - 14, ay + 4, it("O"), anchor="end"))
    yd = fy + 34
    o.append(H.line(s, c[0], fy + 6, c[0], yd + 10, I["rule"], "leader"))
    o.append(H.line(s, xcop, fy + 7, xcop, yd + 10, I["rule"], "leader"))
    o.append(dim_h(s, p, xcop, c[0], yd, tick=4))
    o.append(H.label(s, c[0] + 8, fy + 22, f"{it('x')}{H.sub('com', s, 'label2')}", "label2"))
    o.append(H.label(s, xcop - 10, fy + 22, f"{it('x')}{H.sub('cop', s, 'label2')}", "label2", O["geometry"], "end"))
    o.append(H.label(s, c[0] + 40, yd + 10,
                     f"{it('x')}{H.sub('cop', s)} − {it('x')}{H.sub('com', s)} = −{acc}/ω₀²  (Prop. 3.3)"))
    o.append(H.label(s, c[0] + 40, yd + 30,
                     f"example: {acc} = {A_COM:.1f} m/s², ω₀ = {W0:.2f} s⁻¹ gives {off * 100:.1f} cm".replace("-", "−"),
                     "label2", I["secondary"]))
    o.append(H.label(s, 380, 24, f"to move the COM forward, the ground pushes behind it (lean drawn at {TH8:.0f}°)",
                     "label2", I["secondary"], "middle"))
    o.append(LB.credit(s, 100, fy + 86, width=560))
    aria = ("A skeleton leaning 7 degrees forward about the ankle O, its centre of mass accelerating forward. The "
            "vertical ground reaction N, about Mg, acts upward at the centre of pressure, which sits behind the point "
            "under the centre of mass; the weight Mg acts down at the centre of mass. A dimension on the floor gives "
            "x cop minus x com = minus the COM acceleration over omega0 squared: -0.8 / 3.06 squared m = -8.5 cm.")
    return finish(VB, aria, s, o)


# ================================================================ svg #15  Fig. 14: animated sway at the margin
SWAY_AMP = 2.0                      # degrees, drawn lean amplitude (the DDE is linear; scale is free)
N_FR = 24


def delta_crit():
    """Prop. 6.3: the quartic in omega and the critical delay."""
    a, b, c = I_ANK ** 2, 2 * I_ANK * MGL - KD ** 2, MGL ** 2 - KP ** 2
    w2 = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
    w = math.sqrt(w2)
    return w, math.atan(KD * w / KP) / w


def simulate(Kp, Kd, D, T=25.0, dt=1e-3, th0=0.6):
    """Lab 1 (module07 lines 625-639), unchanged."""
    n, nd = int(T / dt), int(round(D / dt))
    th, w = np.zeros(n), np.zeros(n)
    th[0] = th0
    for k in range(n - 1):
        j = k - nd
        thd = th[j] if j >= 0 else th0
        wd = w[j] if j >= 0 else 0.0
        acc = (MGL * th[k] - Kp * thd - Kd * wd) / I_ANK
        w[k + 1] = w[k] + dt * acc
        th[k + 1] = th[k] + dt * w[k + 1]
    return np.arange(n) * dt, th


_SW = {}


def sway():
    """One settled period of the Lab 1 run at the critical delay, scaled to SWAY_AMP; COM and COP in metres."""
    if "s" in _SW:
        return _SW["s"]
    wc, dc = delta_crit()
    t, th = simulate(KP, KD, dc)
    dt = t[1] - t[0]
    acc = np.gradient(np.gradient(th, dt), dt)
    up = [i for i in range(len(th) - 1) if th[i] < 0 <= th[i + 1] and t[i] > 15.0]
    i0, i1 = up[0], up[1]
    amp = np.abs(th[i0:i1]).max()
    g = math.radians(SWAY_AMP) / amp
    xc = ELL * th * g                                       # x_com = l theta (linear)
    xp = xc - (I_ANK / (M_KG * G * ELL)) * ELL * acc * g    # Prop. 3.3: x_cop = x_com - xdd_com / omega0^2
    per = t[i1] - t[i0]
    tf = [t[i0] + per * k / N_FR for k in range(N_FR)]
    idx = [int(round((v - t[0]) / dt)) for v in tf]
    S = dict(wc=wc, dc=dc, per=per, t=t[i0:i1 + 1] - t[i0], xc=xc[i0:i1 + 1], xp=xp[i0:i1 + 1],
             th=np.degrees(th[i0:i1 + 1] * g), idx=[i - i0 for i in idx], tf=[v - t[i0] for v in tf])
    # phase of the COP relative to the COM (cross-correlation peak, s)
    a, b = S["xc"] - S["xc"].mean(), S["xp"] - S["xp"].mean()
    lags = range(-len(a) // 2, len(a) // 2)
    S["lead"] = max(lags, key=lambda L: float(np.dot(np.roll(b, -L), a))) * dt * -1
    S["ratio"] = (S["xp"].max() - S["xp"].min()) / (S["xc"].max() - S["xc"].min())
    _SW["s"] = S
    return S


def fig15():
    p = "m7f15_"
    VB = (0, 0, 760, 600)
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    S = sway()
    hgt, fy, hx = 470.0, 540.0, 150.0
    o = [defs(p, s), floor(s, 40, 380, fy)]
    _, J0 = lean(s, 0.0, hx, fy, hgt, p=p)
    ax, ay = J0["ankle"]
    um = m2u(J0, 1.0)
    o.append(f'<rect x="{ax - D_HEEL * um:.2f}" y="{fy + 2:.2f}" width="{(D_HEEL + D_TOE) * um:.2f}" height="7" '
             f'fill="{BOXFILL}" stroke="{I["secondary"]}" stroke-width="{s(1):.2f}"/>')
    o.append(H.label(s, ax + 0.035 * um, fy + 26, "base of support", "label2", I["secondary"], "middle"))
    # trace panel: x_com and x_cop over one period
    box = (470.0, 110.0, 730.0, 330.0)
    tmax = S["per"]
    xm = 0.06
    X = lambda t: box[0] + t / tmax * (box[2] - box[0])     # noqa: E731
    Y = lambda v: (box[1] + box[3]) / 2 - v / xm * (box[3] - box[1]) / 2   # noqa: E731
    for v in (-0.04, 0.0, 0.04):
        o.append(H.line(s, box[0], Y(v), box[2], Y(v), GRID if v else I["rule"], "leader"))
        o.append(H.label(s, box[0] - 8, Y(v) + 4.5, f"{v * 100:+.0f}".replace("-", "−").replace("+0", "0"),
                         "tick", I["secondary"], "end"))
    o.append(H.line(s, box[0], box[3], box[2], box[3], I["axis"], "axis"))
    o.append(H.line(s, box[0], box[1], box[0], box[3], I["axis"], "axis"))
    for tv in np.arange(0, tmax, 1.0):
        o.append(H.line(s, X(tv), box[3], X(tv), box[3] + 5, I["axis"], "leader"))
        o.append(H.label(s, X(tv), box[3] + 20, f"{tv:.0f}", "tick", I["secondary"], "middle"))
    o.append(H.label(s, (box[0] + box[2]) / 2, box[3] + 42, "time in one sway cycle (s)", "label2", anchor="middle"))
    yl = (box[1] + box[3]) / 2
    o.append(H.label(s, box[0] - 40, yl, "cm ahead of the ankle", "label2", anchor="middle",
                     extra=f'transform="rotate(-90 {box[0] - 40:.2f} {yl:.2f})"'))
    ptc = [(X(t), Y(v)) for t, v in zip(S["t"][::30], S["xc"][::30])]
    ptp = [(X(t), Y(v)) for t, v in zip(S["t"][::30], S["xp"][::30])]
    o.append(poly(s, ptc, I["primary"], "curve_multi"))
    o.append(poly(s, ptp, O["geometry"], "curve_multi"))
    o.append(H.label(s, box[0], box[1] - 30, "COP (blue) and COM projection (black)", "label2"))
    o.append(H.label(s, box[0], box[1] - 14, f"at Δ = Δ{H.sub('crit', s, 'label2')} = {S['dc']:.3f} s, "
                     f"{it('f')} = {S['wc'] / (2 * math.pi):.2f} Hz", "label2", I["secondary"]))
    hv = [[X(t), [Y(a), Y(b)], f"t {t:.2f} s: COM {a * 100:+.1f} cm, COP {b * 100:+.1f} cm".replace("-", "−")]
          for t, a, b in zip(S["t"][::10], S["xc"][::10], S["xp"][::10])]
    frames = []
    dft = int(np.argmax(S["xc"][S["idx"]]))                    # the still frame: maximum forward lean
    body0, J0 = lean(s, 0.0, hx, fy, hgt, p=p)                 # rigid about the ankle: one body, rotated per frame
    wrap = body0.split(">", 1)[0] + ">"
    foot = [u for u in J0["_uses"] if "lat_foot" in u]
    upper = [u for u in J0["_uses"] if "lat_foot" not in u]
    o.insert(1, f'<defs><g id="{p}up">{wrap}{"".join(upper)}</g></g></defs>')
    o.append(wrap + "".join(foot) + "</g>")
    c0 = J0["comT"]
    for kf, i in enumerate(S["idx"]):
        thd = float(S["th"][i])
        r = rot((c0[0] - ax, c0[1] - ay), thd)
        c = (ax + r[0], ay + r[1])
        xc = ax + S["xc"][i] * um
        xp = ax + S["xp"][i] * um
        g = [f'<use href="#{p}up" transform="rotate({thd:.3f} {ax:.2f} {ay:.2f})"/>',
             vline(s, xc, c[1] + 9, fy, O["dim"]), H.com_mark(s, *c), dot(s, xc, fy, I["primary"], 4),
             cop_mark(s, xp, fy), H.line(s, X(S["t"][i]), box[1], X(S["t"][i]), box[3], O["flag"], "ref"),
             dot(s, X(S["t"][i]), Y(S["xc"][i]), I["primary"], 4), dot(s, X(S["t"][i]), Y(S["xp"][i]), O["geometry"], 4),
             H.label(s, 40, 26, f"lean {thd:+.1f}°".replace("-", "−"), "label2", I["secondary"])]
        frames.append(H.frame(kf, dft, "".join(g)))
    o += frames
    o.append(H.joint_centre(s, ax, ay))
    o.append(cop_mark(s, 476, 470))
    o.append(H.label(s, 490, 475, "centre of pressure (COP)", "label2"))
    o.append(dot(s, 476, 494, I["primary"], 4))
    o.append(H.label(s, 490, 499, "COM projection on the floor", "label2"))
    o.append(H.label(s, 470, 530, f"lean amplitude drawn at {SWAY_AMP:.0f}° (the model is linear)", "label2",
                     I["secondary"]))
    o.append(LB.credit(s, 40, fy + 46, width=680))
    vals = [f"{v:.2f} s" for v in S["tf"]]
    extra = H.frames_attr("time in the sway cycle", vals, dft) + " " + H.hover_attr(list(box), hv)
    aria = ("Animated: a skeleton sways about the ankle at the stability margin, 0.35 Hz, the frames taken from the "
            "Lab 1 delayed-feedback simulation at the critical delay of 0.130 s. A blue centre-of-pressure marker on "
            "the floor swings 1.5 times as far as the black point under the centre of mass, in step with it, so it "
            "lies beyond the COM on each side; a trace at the right shows both over one cycle. Without the slider the "
            "figure shows the instant of largest forward lean.")
    return finish(VB, aria, s, o, extra=extra)


# ================================================================ svg #16  Fig. 15: ankle vs hip strategy
HIP_POSE = dict(pelvis=50.0, trunk=0.0, thigh=-10.0)


def fig16():
    p = "m7f16_"
    VB = (0, 0, 760, 590)
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    hgt, fy = 420.0, 500.0
    o = [defs(p, s), H.line(s, 380, 20, 380, 580, GRID, "axis")]
    # ---- left: ankle strategy
    th = 4.0
    body, J = lean(s, th, 150.0, fy, hgt, p=p)
    ax, ay = J["ankle"]
    um = m2u(J, 1.0)
    c = J["comT"]
    o += [body, floor(s, 30, 350, fy)]
    o.append(f'<rect x="{ax - D_HEEL * um:.2f}" y="{fy + 2:.2f}" width="{(D_HEEL + D_TOE) * um:.2f}" height="7" '
             f'fill="{BOXFILL}" stroke="{I["secondary"]}" stroke-width="{s(1):.2f}"/>')
    xcop = ax + 0.09 * um
    o.append(H.com_mark(s, *c))
    o.append(vline(s, c[0], c[1] + 9, fy, O["dim"]))
    o.append(cop_mark(s, xcop, fy))
    o.append(H.arrow(s, p, ax - 0.03 * um, fy + 24, ax + 0.10 * um, fy + 24, "geometry", both=True))
    o.append(H.label(s, ax + 0.035 * um, fy + 44, "COP moves within the foot", "label2", O["geometry"], "middle"))
    o.append(arc_arrow(s, p, ax, ay, 300, -90, -76, "geometry", both=True))
    o.append(H.label(s, c[0] + 40, c[1] - 150, "the body rotates as one", "label2", O["geometry"]))
    o.append(H.label(s, c[0] + 40, c[1] - 134, "segment about the ankle", "label2", O["geometry"]))
    o.append(H.joint_centre(s, ax, ay))
    o.append(H.label(s, 190, 26, "ankle strategy", anchor="middle"))
    o.append(H.label(s, 190, 44, "small, slow disturbance", "label2", I["secondary"], "middle"))
    # ---- right: hip strategy (kit Winter COM: the text states none for this pose)
    hp = HIP_POSE
    arm = dict(hip=hp["pelvis"] - hp["thigh"], shoulder=hp["pelvis"] + hp["trunk"])     # arms hang vertically
    P = LB.pose(pelvis=hp["pelvis"], trunk=hp["trunk"], near=arm, far=arm)
    body, J2 = LB.draw(p, s, P, 520.0, fy, hgt)
    ax2 = J2["ankle"][0]
    c2 = J2["com"]
    o += [body, floor(s, 400, 740, fy)]
    o.append(f'<rect x="{ax2 - D_HEEL * um:.2f}" y="{fy + 2:.2f}" width="{(D_HEEL + D_TOE) * um:.2f}" height="7" '
             f'fill="{BOXFILL}" stroke="{I["secondary"]}" stroke-width="{s(1):.2f}"/>')
    xt = ax2 + D_TOE * um
    o.append(H.com_mark(s, *c2))
    o.append(vline(s, c2[0], c2[1] + 9, fy, O["dim"]))
    o.append(H.arrow(s, p, xt, fy - 8, xt - 90, fy - 8, "reaction"))
    o.append(H.label(s, xt - 96, fy - 16, f"{it('H')}: backward shear", "label2", anchor="end"))
    o.append(cop_mark(s, xt, fy))
    o.append(H.label(s, xt + 10, fy + 26, "COP pinned at the toe edge", "label2", O["geometry"], "middle"))
    hipj = J2["hip"]
    o.append(arc_arrow(s, p, hipj[0], hipj[1], 70, -150, -70, "geometry"))
    o.append(H.label(s, hipj[0] - 30, hipj[1] - 82, "trunk counter-rotates", "label2", O["geometry"], "end"))
    o.append(H.label(s, hipj[0] - 30, hipj[1] - 66, "about the hip", "label2", O["geometry"], "end"))
    o.append(H.joint_centre(s, *hipj))
    o.append(H.joint_centre(s, *J2["ankle"]))
    o.append(H.label(s, 570, 26, "hip strategy", anchor="middle"))
    o.append(H.label(s, 570, 44, "large or fast disturbance", "label2", I["secondary"], "middle"))
    o.append(LB.credit(s, 30, fy + 64, width=700))
    aria = ("Two skeletons. Left, ankle strategy: the body leans 4 degrees as one rigid segment about the ankle and "
            "the centre of pressure moves within the foot. Right, hip strategy: the body flexes at the hip, trunk "
            "forward and hips back; the centre of pressure is pinned at the toe edge and a backward horizontal ground "
            "reaction H acts at the floor.")
    return finish(VB, aria, s, o)


# ================================================================ svg #17  Fig. 16: co-contraction, knee locking
TAU0 = M_KG * G * COM_AHEAD          # held ankle torque at upright: Mg x 0.02 m = 13.7 N m (line 176)
K_LOW, K_HIGH = 0.9 * MGL, KP        # 556 (intrinsic, line 425) and 900 N m/rad (line 493)
LOCK = dict(pelvis=1.16, knee=-5.0)                     # 5 deg hyperextension at the stop (as svg 34); the 1.16 deg
# lean puts the COM 2.0 cm ahead of the ankle (the text value, line 176), which leaves the knee centre 1.0 cm behind the line
CROUCH = dict(pelvis=20.0, hip=45.0, knee=40.0)


def fig17():
    p = "m7f17_"
    VB = (0, 0, 760, 520)
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    o = [defs(p, s), H.line(s, 392, 20, 392, 470, GRID, "axis")]
    # ---- left: torque-angle lines
    x0, top, x1, y0 = 80.0, 100.0, 350.0, 390.0
    tr, yr = (-3.0, 3.0), (-40.0, 60.0)
    X = lambda v: x0 + (v - tr[0]) / (tr[1] - tr[0]) * (x1 - x0)       # noqa: E731
    Y = lambda v: y0 - (v - yr[0]) / (yr[1] - yr[0]) * (y0 - top)      # noqa: E731
    for v in (-40, -20, 0, 20, 40, 60):
        o.append(H.line(s, x0, Y(v), x1, Y(v), GRID if v else I["rule"], "leader"))
        o.append(H.line(s, x0 - 5, Y(v), x0, Y(v), I["axis"], "leader"))
        o.append(H.label(s, x0 - 9, Y(v) + 4.5, f"{v}".replace("-", "−"), "tick", I["secondary"], "end"))
    for v in (-3, -2, -1, 0, 1, 2, 3):
        o.append(H.line(s, X(v), y0, X(v), y0 + 5, I["axis"], "leader"))
        o.append(H.label(s, X(v), y0 + 20, f"{v}".replace("-", "−"), "tick", I["secondary"], "middle"))
    o.append(H.line(s, x0, y0, x1, y0, I["axis"], "axis"))
    o.append(H.line(s, x0, top, x0, y0, I["axis"], "axis"))
    o.append(H.label(s, (x0 + x1) / 2, y0 + 44, f"lean {it('θ')} (degrees, forward +)", anchor="middle"))
    ym = (top + y0) / 2
    o.append(H.label(s, x0 - 48, ym, "ankle torque τ (N·m)", anchor="middle",
                     extra=f'transform="rotate(-90 {x0 - 48:.2f} {ym:.2f})"'))
    th = np.linspace(tr[0], tr[1], 121)
    lines = [(K_LOW, H.SERIES[0], "low co-contraction"), (K_HIGH, H.SERIES[1], "high co-contraction")]
    o.append(H.line(s, x0, Y(TAU0), x1, Y(TAU0), I["secondary"], "ref", dash=H.DASH_REF))
    for K, col, _ in lines:
        o.append(poly(s, [(X(t), Y(TAU0 + K * math.radians(t))) for t in th[::6]], col, "curve_multi"))
    o.append(dot(s, X(0), Y(TAU0), I["primary"], 4.5))
    o.append(H.label(s, X(-1.4), Y(-30), f"slope {K_HIGH:.0f} N·m/rad", "label2", H.SERIES[1]))
    o.append(H.label(s, X(-2.9), Y(5), f"slope {K_LOW:.0f}", "label2", H.SERIES[0]))
    o.append(H.label(s, X(-2.9), Y(46), "dashed: the same net torque", "label2", I["secondary"]))
    o.append(H.label(s, X(-2.9), Y(46) + 16, f"at upright, {TAU0:.1f} N·m (Mg × 0.02 m)", "label2", I["secondary"]))
    lx, ly = x0 - 40, top - 52
    for i, (K, col, name) in enumerate(lines):
        o.append(H.line(s, lx, ly + 18 * i - 4, lx + 24, ly + 18 * i - 4, col, "curve_multi"))
        note = " (0.9 Mgℓ, below Mgℓ = 618)" if K < MGL else ""
        o.append(H.label(s, lx + 31, ly + 18 * i, f"{name}, {it('K')}{H.sub('p', s, 'label2')} = {K:.0f}{note}",
                         "label2"))
    o.append(H.label(s, lx, ly + 36, f"{it('K')}{H.sub('p', s, 'label2')} = {it('k')}{H.sub('a', s, 'label2')} + "
                     f"{it('k')}{H.sub('b', s, 'label2')}: the stiffnesses add, the torques subtract", "label2",
                     I["secondary"]))
    o.append(H.label(s, 200, 26, "co-contraction steepens the slope", anchor="middle"))
    hv = [[X(t), [Y(TAU0 + K_LOW * math.radians(t)), Y(TAU0 + K_HIGH * math.radians(t))],
           f"θ {t:+.2f}°: low {TAU0 + K_LOW * math.radians(t):.1f}, high {TAU0 + K_HIGH * math.radians(t):.1f} N·m"
           .replace("-", "−")] for t in th]
    # ---- right: knee locked vs crouched (kit Winter COM: the text states none for these poses)
    hgt, fy = 360.0, 430.0
    P1 = LB.pose(pelvis=LOCK["pelvis"], near=dict(hip=0.0, knee=LOCK["knee"]), far=dict(hip=0.0, knee=LOCK["knee"]))
    P2 = LB.pose(pelvis=CROUCH["pelvis"], near=dict(hip=CROUCH["hip"], knee=CROUCH["knee"]),
                 far=dict(hip=CROUCH["hip"], knee=CROUCH["knee"]))
    o.append(floor(s, 410, 750, fy))
    arms = []
    for P, hx, name in ((P1, 450.0, "locked"), (P2, 610.0, "crouched")):
        body, J = LB.draw(p, s, P, hx, fy, hgt)
        um = m2u(J, 1.0)
        c, kn = J["com"], J["knee"]
        arm = (c[0] - kn[0]) / um
        arms.append(arm)
        o.append(body)
        o.append(H.com_mark(s, *c))
        o.append(vline(s, c[0], c[1] + 9, fy, O["load"]))
        o.append(H.joint_centre(s, *kn))
        yd = kn[1] + (22 if name == "locked" else -26)
        o.append(dim_h(s, p, kn[0], c[0], yd, tick=4))
        if name == "locked":
            o.append(H.label(s, c[0] + 12, kn[1] - 6, f"weight line {arm * 100:.1f} cm", "label2", O["load"]))
            o.append(H.label(s, c[0] + 12, kn[1] + 10, "in front of the knee", "label2", O["load"]))
            o.append(H.label(s, hx + 20, fy + 24, "extended, locked", "label2", anchor="middle"))
            o.append(H.label(s, hx + 20, fy + 40, "passive stop holds it", "label2", I["secondary"], "middle"))
        else:
            o.append(H.label(s, c[0] - 8, yd - 22, f"weight line {-arm * 100:.1f} cm", "label2", O["load"], "end"))
            o.append(H.label(s, c[0] - 8, yd - 6, "behind the knee", "label2", O["load"], "end"))
            hip = J["hip"]
            d = (hip[0] - kn[0], hip[1] - kn[1])
            L = math.hypot(*d)
            u, n = (d[0] / L, d[1] / L), (-d[1] / L, d[0] / L)              # n: anterior side of the thigh
            a0 = (kn[0] + 0.07 * L * u[0] + 16 * n[0], kn[1] + 0.07 * L * u[1] + 16 * n[1])
            a1 = (kn[0] + 0.55 * L * u[0] + 16 * n[0], kn[1] + 0.55 * L * u[1] + 16 * n[1])
            o.append(H.arrow(s, p, a0[0], a0[1], a1[0], a1[1], "force"))
            o.append(H.label(s, a1[0] + 10, a1[1] - 4, "quadriceps", "label2", O["force"]))
            o.append(H.label(s, a1[0] + 10, a1[1] + 12, "must pull", "label2", O["force"]))
            o.append(H.label(s, hx + 30, fy + 24, "flexed (crouched)", "label2", anchor="middle"))
            o.append(H.label(s, hx + 30, fy + 40, "quadriceps hold it", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 580, 26, "knee locking saves effort", anchor="middle"))
    o.append(LB.credit(s, 8, fy + 62, width=744))
    aria = ("Left: plot of ankle torque against lean angle from minus 3 to 3 degrees for low co-contraction (slope "
            "556 N m per rad) and high co-contraction (slope 900 N m per rad); both lines pass through the same net "
            "torque at upright, 13.7 N m, drawn dashed, while the slope, the stiffness, steepens. Right: two "
            "skeletons. An extended locked knee with the weight line 1 cm in front of the knee, held by the passive "
            "stop; a crouched knee with the weight line 8 cm behind it, held by the quadriceps.")
    return finish(VB, aria, s, o, extra=H.hover_attr([x0, top, x1, y0], hv))


# ================================================================ svg #18  Fig. 17: lumbar vertebrae and discs
NUM = r'[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?'
LUM_WIN = (34.0, -658.0, 104.0, 72.0)        # body units: x, y, w, h (L3 to the iliac crest, lateral view)


def _subpaths(d):
    """Kit path data (M, m, l, z only) -> [(closed, [(x, y)])] absolute."""
    toks = re.findall(NUM + r'|[A-Za-z]', d)
    subs, cur, cmd, x, y, sx, sy, k = [], None, None, 0.0, 0.0, 0.0, 0.0, 0
    while k < len(toks):
        t = toks[k]
        if t.isalpha():
            cmd, k = t, k + 1
            if cmd in "zZ":
                subs.append((True, cur))
                cur, x, y = None, sx, sy
            continue
        a, b = float(toks[k]), float(toks[k + 1])
        k += 2
        if cmd in "Mm":
            if cur:
                subs.append((False, cur))
            x, y = (a, b) if cmd == "M" else (x + a, y + b)
            sx, sy, cur = x, y, [(x, y)]
            cmd = "l" if cmd == "m" else "L"
        else:
            x, y = (x + a, y + b) if cmd == "l" else (a, b)
            cur.append((x, y))
    if cur:
        subs.append((False, cur))
    return subs


def _kit_paths(seg):
    t = (LB.SVG_DIR / "lynch_lat_body.svg").read_text(encoding="utf-8")
    g = re.search(r'<g id="hbody_' + seg + r'" data-bbox="[^"]+">(.*?)</g><!--/' + seg + '-->', t, re.S).group(1)
    return re.findall(r'<path d="([^"]*)"([^>]*)/>', g)


# Disc bands: quadrilaterals between the paired disc lines Lynch drew, read off a 1-unit grid render of the kit's
# hbody_lat_trunk art (body units). Upper = L3/L4, lower = L4/L5; the body between them is L4. L5 and the L5/S1
# junction (kit landmark LJ["l5s1"]) lie behind the iliac crest in this lateral art.
DISCS = [[(84.0, -639.2), (103.2, -640.2), (104.0, -634.5), (84.0, -634.8)],
         [(86.5, -620.0), (104.5, -620.4), (103.5, -615.6), (86.5, -616.4)]]


def lumbar_art():
    """The lumbar window of the kit's lateral trunk + pelvis art (body units); subpaths outside the window dropped."""
    wx, wy, ww, wh = LUM_WIN
    out = []
    for seg, off in (("lat_trunk", LB.LJ["l5s1"]), ("lat_pelvis", LB.LJ["hip"])):
        for d, attrs in _kit_paths(seg):
            keep = []
            for closed, pts in _subpaths(d):
                P = [(x + off[0], y + off[1]) for x, y in pts]
                xs, ys = [q[0] for q in P], [q[1] for q in P]
                if max(xs) < wx or min(xs) > wx + ww or max(ys) < wy or min(ys) > wy + wh:
                    continue
                keep.append(path_d(P, closed))
            if keep:
                out.append((seg, attrs, "".join(keep)))
    return out


def fig18():
    p = "m7f18_"
    VB = (0, 0, 760, 436)
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    wx, wy, ww, wh = LUM_WIN
    f = 4.0                                                       # figure units per body unit in the window
    X0, Y0 = 190.0, 40.0
    B = lambda x, y: (X0 + (x - wx) * f, Y0 + (y - wy) * f)       # noqa: E731
    art, discs = lumbar_art(), DISCS
    # the window document: bone fills, disc bands, then the trunk detail lines; pelvis on top (kit draw order)
    body = []
    for seg in ("lat_trunk", "lat_pelvis"):
        for sg, attrs, d in art:
            if sg != seg:
                continue
            body.append(f'<path d="{d}"{H.recolour(attrs, "lynch")}/>')
            if seg == "lat_trunk" and "828487" in attrs and not any("fibrocart" in x for x in body[-3:]):
                body += [f'<path d="{path_d(q)}" fill="{T["fibrocart"][0]}"/><!--fibrocart-->' for q in discs]
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{wx} {wy} {ww} {wh}" width="{ww}" height="{wh}">'
           + "".join(body) + "</svg>")
    doc = re.sub(r'="([^"\']*)"', r"='\1'", doc)
    b64 = "data:image/svg+xml;base64," + base64.b64encode(doc.encode("utf-8")).decode("ascii")
    pct = "data:image/svg+xml," + quote(doc, safe=" !$'()*+,-./:;=?@_~[]{}|")
    o = [defs(p, s)]
    o.append(f'<image x="{X0}" y="{Y0}" width="{ww * f:.2f}" height="{wh * f:.2f}" preserveAspectRatio="none" '
             f'href="{min(b64, pct, key=len)}"/>')
    o.append(f'<rect x="{X0}" y="{Y0}" width="{ww * f:.2f}" height="{wh * f:.2f}" fill="none" '
             f'stroke="{I["rule"]}" stroke-width="{s(1):.2f}"/>')
    # locator: the standing body with the window marked
    hgt, fy = 320.0, 360.0
    body_svg, J = LB.standing_full(p, s, 50.0, fy, hgt)
    k = J["scale"]
    L = lambda x, y: (J["heel"][0] + (x - LB.LAT["heel_x"]) * k, fy + y * k)   # noqa: E731
    o.append(body_svg)
    a, b = L(wx, wy), L(wx + ww, wy + wh)
    o.append(f'<rect x="{a[0]:.2f}" y="{a[1]:.2f}" width="{b[0] - a[0]:.2f}" height="{b[1] - a[1]:.2f}" fill="none" '
             f'stroke="{I["primary"]}" stroke-width="{s(1.2):.2f}"/>')
    o.append(H.line(s, b[0], a[1], X0, Y0, I["rule"], "leader", dash=(3, 3)))
    o.append(H.line(s, b[0], b[1], X0, Y0 + wh * f, I["rule"], "leader", dash=(3, 3)))
    o.append(floor(s, 10, 170, fy))
    # overlays in the window
    l5 = B(*LB.LJ["l5s1"])
    xe = LB.LJ["l5s1"][0] - 0.05 * UM
    e0, e1 = B(xe, wy + 2), B(xe, wy + wh - 2)
    o.append(white_under(s, *e0, *e1) + H.line(s, *e0, *e1, O["force"], "force", dash=H.DASH_LOA))
    o.append(H.label(s, e0[0] - 8, Y0 + 20, "erector spinae", "label2", O["force"], "end"))
    o.append(H.label(s, e0[0] - 8, Y0 + 36, "line of pull", "label2", O["force"], "end"))
    o.append(dim_h(s, p, B(xe, 0)[0], l5[0], l5[1] + 36))
    o.append(H.line(s, l5[0], l5[1] + 6, l5[0], l5[1] + 44, I["rule"], "leader"))
    o.append(H.label(s, (B(xe, 0)[0] + l5[0]) / 2, l5[1] + 58, f"{it('d')} ≈ 5 cm", fill=O["geometry"], anchor="middle"))
    o.append(H.joint_centre(s, *l5))
    xr = X0 + ww * f + 14
    o.append(leader(s, l5[0] + 8, l5[1], xr - 4, l5[1] + 30, I["primary"]))
    o.append(H.label(s, xr, l5[1] + 35, "L5/S1, the pivot", "label2"))
    o.append(H.label(s, xr, l5[1] + 51, "(hidden behind", "label2", I["secondary"]))
    o.append(H.label(s, xr, l5[1] + 67, "the iliac crest)", "label2", I["secondary"]))
    dh = []
    for q in discs:
        cx = sum(v[0] for v in q) / len(q)
        cy = sum(v[1] for v in q) / len(q)
        P = B(max(v[0] for v in q) - 3, cy)
        dh.append((max(v[1] for v in q) - min(v[1] for v in q)) / UM)
        o.append(leader(s, P[0] + 4, P[1], xr - 4, P[1]))
    if discs:
        o.append(H.label(s, xr, B(0, sum(v[1] for v in discs[0]) / len(discs[0]))[1] + 5, "L3/L4 disc", "label2"))
        o.append(H.label(s, xr, B(0, sum(v[1] for v in discs[-1]) / len(discs[-1]))[1] + 5, "L4/L5 disc", "label2"))
    vb_y = (sum(v[1] for v in discs[0]) / len(discs[0]) + sum(v[1] for v in discs[-1]) / len(discs[-1])) / 2
    vb_h = (min(v[1] for v in discs[-1]) - max(v[1] for v in discs[0])) / UM
    P = B(102, vb_y)
    o.append(leader(s, P[0], P[1], xr - 4, P[1]))
    o.append(H.label(s, xr, P[1] + 5, "L4 vertebral body", "label2"))
    sp = B(52, -630)
    o.append(H.label(s, sp[0] - 6, sp[1] + 60, "spinous", "label2", anchor="middle"))
    o.append(H.label(s, sp[0] - 6, sp[1] + 76, "processes", "label2", anchor="middle"))
    sa = B(108, -592)
    o.append(H.label(s, sa[0], sa[1] + 4, "iliac crest (pelvis)", "label2", anchor="middle"))
    o.append(H.label(s, X0, Y0 + wh * f + 20, f"as drawn: disc ≈ {sum(dh) / len(dh) * 100:.1f} cm tall, "
                     f"vertebral body ≈ {vb_h * 100:.1f} cm; the extensors pull {it('d')} ≈ 5 cm behind the pivot",
                     "label2", I["secondary"]))
    o.append(H.label(s, X0, 24, "lower lumbar spine, side view (front = right)", "label2", I["secondary"]))
    o.append(LB.credit(s, 8, fy + 34, width=744,
                       extra=" Lumbar window magnified; disc bands filled between the disc lines of the art."))
    aria = ("A small standing skeleton with a box around the low back, and that box magnified: the lower lumbar "
            "vertebral bodies seen from the side with thin blue intervertebral discs between them, the spinous "
            "processes behind and the iliac crest below. The L5/S1 junction, behind the crest, is marked as the pivot; a dashed red line 5 cm "
            "behind it is the line of pull of the erector spinae, so the extensors act on a moment arm d of about 5 cm.")
    return finish(VB, aria, s, o)


# ================================================================ svg #19  Fig. 18: stooped lift about L5/S1
PHI = 90.0                                   # the worked lift (line 601): L5/S1 to C7/T1 chord horizontal
M_T, R_T, M_L, R_L, D_E = 35.0, 0.30, 20.0, 0.40, 0.05
PEL19 = 55.0                                 # pelvis tilt; lumbar flexion = the rest of phi (as body_c.py C10)
CHORD0 = math.degrees(math.atan2(LB.LJ["neck"][0] - LB.LJ["l5s1"][0], LB.LJ["l5s1"][1] - LB.LJ["neck"][1]))


def _bisect(fn, lo, hi, n=50):
    flo = fn(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        if (fn(mid) > 0) == (flo > 0):
            lo, flo = mid, fn(mid)
        else:
            hi = mid
    return (lo + hi) / 2


def lift_pose():
    """Pelvis 55 deg + lumbar flexion so the L5/S1-C7 chord is PHI from vertical, knees straight. Shoulder flexion
    solved so the grip (mid-hand) sits r_L sin(phi) ahead of L5/S1 (Prop. 8.1's load arm); thigh angle solved so
    the COM of body (70 kg, Winter) + load (20 kg at the grip) is 0.04 m ahead of the ankle, over the mid-foot."""
    tot = PHI - CHORD0

    def build(thigh, sh):
        P = LB.pose(pelvis=PEL19, trunk=tot - PEL19, near=dict(hip=PEL19 - thigh, shoulder=sh),
                    far=dict(hip=PEL19 - thigh, shoulder=sh))
        J = LB.draw("", None, P, 0, 0, LB.H_U)[1]
        return P, J, LB.lerp(J["wrist"], J["fingertip"], 0.5)

    def shoulder(thigh):
        return _bisect(lambda sh: (build(thigh, sh)[2][0] - build(thigh, sh)[1]["l5s1"][0]) / UM
                       - R_L * math.sin(math.radians(PHI)), 40.0, 140.0, 40)

    def com_err(thigh):
        P, J, g = build(thigh, shoulder(thigh))
        return ((M_KG * J["com"][0] + M_L * g[0]) / (M_KG + M_L) - J["ankle"][0]) / UM - 0.04
    thigh = _bisect(com_err, -40.0, 0.0, 30)
    sh = shoulder(thigh)
    return build(thigh, sh)[0], sh


def fig19():
    p = "m7f19_"
    VB = (0, 0, 760, 640)
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    P, sh = lift_pose()
    hgt, fy = 640.0, 580.0
    body, J = LB.draw(p, s, P, 230.0, fy, hgt)
    um = m2u(J, 1.0)
    l5, nk = J["l5s1"], J["neck"]
    ph = math.radians(PHI)
    u, n = (math.sin(ph), -math.cos(ph)), (-math.cos(ph), -math.sin(ph))       # along the trunk; dorsal normal
    grip = LB.lerp(J["wrist"], J["fingertip"], 0.5)
    bw, bh = 0.32 * um, 0.26 * um
    o = [defs(p, s)]
    o.append(f'<rect x="{grip[0] - bw / 2:.2f}" y="{grip[1] - s(4):.2f}" width="{bw:.2f}" height="{bh:.2f}" '
             f'fill="{BOXFILL}" stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
    o.append(body)
    o.append(floor(s, 30, 740, fy))
    tc = (l5[0] + R_T * um * u[0], l5[1] + R_T * um * u[1])
    ce = (l5[0] + 0.62 * um * u[0], l5[1] + 0.62 * um * u[1])
    o.append(white_under(s, *l5, *ce) + H.line(s, *l5, *ce, O["dim"], "ref", dash=H.DASH_REF))
    o.append(vline(s, l5[0], l5[1], l5[1] - 0.30 * um, O["dim"]))
    o.append(angle_arc(s, l5[0], l5[1], 0.22 * um, -90, -90 + PHI))
    o.append(H.label(s, l5[0] + 0.07 * um, l5[1] - 0.25 * um, f"{it('φ')} = {PHI:.0f}°", fill=O["geometry"]))
    # erector spinae: d dorsal of the joint, pulling toward the pelvis
    e0 = (l5[0] + D_E * um * n[0] + 0.26 * um * u[0], l5[1] + D_E * um * n[1] + 0.26 * um * u[1])
    e1 = (l5[0] + D_E * um * n[0] + 0.03 * um * u[0], l5[1] + D_E * um * n[1] + 0.03 * um * u[1])
    o.append(H.arrow(s, p, *e0, *e1, "force"))
    em = ((e0[0] + e1[0]) / 2, (e0[1] + e1[1]) / 2)
    o.append(leader(s, l5[0] - 8, l5[1] - 48, em[0] - 4, em[1] - 4, O["force"]))
    o.append(H.label(s, l5[0] - 10, l5[1] - 58, f"{it('F')}{H.sub('e', s)}", fill=O["force"], anchor="end"))
    o.append(H.label(s, l5[0] - 10, l5[1] - 42, "erector spinae", "label2", O["force"], "end"))
    o.append(H.arrow(s, p, l5[0] + 0.12 * um * u[0] - 9 * n[0], l5[1] + 0.12 * um * u[1] - 9 * n[1],
                     l5[0] - 9 * n[0], l5[1] - 9 * n[1], "reaction"))
    fs0 = (l5[0] + 0.06 * um * u[0] - 9 * n[0], l5[1] + 0.06 * um * u[1] - 9 * n[1])
    o.append(leader(s, fs0[0] - 2, fs0[1] + 4, l5[0] - 14, l5[1] + 40))
    o.append(H.label(s, l5[0] - 16, l5[1] + 52, f"{it('F')}{H.sub('spine', s, 'label2')}: compression", "label2",
                     anchor="end"))
    dd = (l5[0] + D_E * um * n[0], l5[1] + D_E * um * n[1])
    o.append(H.line(s, *l5, *dd, O["geometry"], "geom"))
    o.append(H.label(s, dd[0] - 8, dd[1] + 10, f"{it('d')} = 5 cm", "label2", O["geometry"], "end"))
    o.append(H.joint_centre(s, *l5))
    o.append(H.label(s, l5[0] - 12, l5[1] + 26, "L5/S1", anchor="end"))
    o.append(H.com_mark(s, *tc))
    o.append(H.arrow(s, p, tc[0], tc[1] + 9, tc[0], tc[1] + 100, "load"))
    o.append(H.label(s, tc[0] + 7, tc[1] + 80, f"{it('m')}{H.sub('t', s)}{it('g')}", fill=O["load"]))
    o.append(leader(s, tc[0] + 6, tc[1] - 7, tc[0] + 30, tc[1] - 50, I["primary"]))
    o.append(H.label(s, tc[0] + 32, tc[1] - 54, f"trunk COM, {it('r')}{H.sub('t', s, 'label2')} = 0.30 m along the trunk",
                     "label2"))
    bc = (grip[0], grip[1] - s(4) + bh / 2)
    o.append(H.arrow(s, p, bc[0], bc[1], bc[0], fy - 4, "load"))
    o.append(H.label(s, bc[0] + 8, fy - 14, f"{it('m')}{H.sub('L', s)}{it('g')}", fill=O["load"]))
    y1, y2 = l5[1] + 0.16 * um, l5[1] + 0.26 * um
    for xx, yy in ((l5[0], y2 + 6), (tc[0], y1 + 6), (bc[0], y2 + 6)):
        o.append(H.line(s, xx, min(yy - 12, y1 - 8), xx, yy, I["rule"], "leader"))
    o.append(dim_h(s, p, l5[0], tc[0], y1, tick=4))
    o.append(H.label(s, (l5[0] + tc[0]) / 2, y1 - 8, f"{it('r')}{H.sub('t', s)} sin {it('φ')}", "label2",
                     O["geometry"], "middle"))
    o.append(dim_h(s, p, l5[0], bc[0], y2, tick=4))
    o.append(H.label(s, (l5[0] + bc[0]) / 2, y2 + 20, f"{it('r')}{H.sub('L', s)} sin {it('φ')}", "label2",
                     O["geometry"], "middle"))
    Mm = G * (M_T * R_T + M_L * R_L) * math.sin(ph)
    Fe = Mm / D_E
    Fs = Fe + (M_T + M_L) * G * math.cos(ph)
    tx = 480
    rows = [f"at {it('φ')} = {PHI:.0f}°, {it('m')}{H.sub('t', s, 'label2')} = 35 kg, {it('r')}{H.sub('t', s, 'label2')} = 0.30 m,",
            f"{it('m')}{H.sub('L', s, 'label2')} = 20 kg, {it('r')}{H.sub('L', s, 'label2')} = 0.40 m, {it('d')} = 0.05 m:",
            f"{it('M')}{H.sub('L5/S1', s, 'label2')} = {it('g')}({it('m')}{H.sub('t', s, 'label2')}{it('r')}{H.sub('t', s, 'label2')} + {it('m')}{H.sub('L', s, 'label2')}{it('r')}{H.sub('L', s, 'label2')}) sin {it('φ')} = {Mm:.0f} N·m",
            f"{it('F')}{H.sub('e', s, 'label2')} = {it('M')}/{it('d')} = {Fe / 1000:.2f} kN",
            f"{it('F')}{H.sub('spine', s, 'label2')} ≈ {it('M')}/{it('d')} + ({it('m')}{H.sub('t', s, 'label2')} + {it('m')}{H.sub('L', s, 'label2')}){it('g')} cos {it('φ')} = {Fs / 1000:.2f} kN"]
    for i, r in enumerate(rows):
        o.append(H.label(s, tx, 360 + 18 * i, r, "label2", I["primary"] if i > 1 else I["secondary"]))
    o.append(LB.credit(s, 8, fy + 24, width=744))
    aria = ("A skeleton stoop-lifting with straight knees, the trunk horizontal (phi = 90 degrees), holding a box "
            "in hanging hands. At the L5/S1 pivot the upper-body weight mt g acts at the trunk centre of mass, "
            "rt sin phi = 0.30 m ahead, and the box weight mL g rL sin phi = 0.40 m ahead; the erector spinae pull "
            "F e on a 5 cm moment arm d behind the joint, and F spine is the compression. The moment is 181 N m and "
            "the compression about 3.6 kN, the worked lift of the text.")
    return finish(VB, aria, s, o)


FIGS = {
    2: ("Left: a mass hanging below a pivot, displaced, with gravity ", fig2),
    3: ("Winter-proportion standing body with COM and base of support", fig3),
    4: ("Two panels. In each, a horizontal bar shows the base of supp", fig4),
    5: ("Left: top view of a foot sole with pressure concentrated und", fig5),
    7: ("Free-body diagram of the inverted pendulum: a rigid rod hing", fig7),
    8: ("The body leans and its centre of mass accelerates forward. T", fig8),
    15: ("Animated: a standing body gently oscillating about the ankle", fig15),
    16: ("Left: ankle strategy, the body rotating as one rigid segment", fig16),
    17: ("Left: torque versus joint angle for two co-contraction level", fig17),
    18: ("Lumbar vertebral bodies stacked with intervertebral discs.", fig18),
    19: ("A person bent forward lifting a box. The pivot at L5/S1 has ", fig19),
}
