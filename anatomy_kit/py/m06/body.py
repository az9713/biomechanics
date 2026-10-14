"""Module 6, group `body`: svg #2 (Fig. 1, Achilles and ACL paths), #3 (Fig. 2, a runner in mid-stance), #21 (Fig. 19,
the knee as a crossed four-bar, flexion slider), #23 (Fig. 21, the foot arch as a tension truss + windlass) and the
problem figures #40 (C10), #50 (D10), #67 (K9).

Art (see ATTRIBUTIONS.md):
  202108_Lateral_view_of_knee_joint_crop_m03f25.svg (DBCLS, CC BY 4.0): split by element into femur, tibia (with
    fibula and menisci) and patella; the ligament bands are left out.  SHARED_DEFS puts the three parts on the page
    once as #m6art_femur, #m6art_tibia, #m6art_patella; #2, #21, #40 and #67 <use> them.
  Lower_leg_muscles_crop_m06ach.svg (InjuryMap, CC BY-SA 4.0): the lateral calf, Achilles tendon and heel, #2 only.
  Lynch body kit (lynch_body.py, CC BY 2.5): the runner of #3 and the foot (#hbody_lat_foot) of #23 and #50.
Numbers: the K9 four-bar (module06.html lines 1170-1212) is solved here exactly as its code does (root find on the
ACL angle, cruciate-line intersection) and its printed results are asserted below; T = W b / (4 h) is lines 673-675
(Prop. 11); the energies in #2 and #3 are line 115 (35 J Achilles, 90-95 % returned; 17 J arch); the stance load of
2.5 body weights is lines 1213 / 1215 (K10); b and h stay symbols (Appendix line 1299 gives 0.15 m and 0.05 m; the
Lynch foot at a 1.75 m stature measures b = 16.4 cm heel to ball and h = 8.4 cm from the talar dome to the tie).
"""
import math
import re

import house as H
import lynch_body as LB
from m05.body import _read, art_image, finish, inner_svg, it, wrap
from m05.plots_main import Ax, axes
from m05.plots_main import poly as plot_poly

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
RED, BLU, BRN, BLK, ORA = O["force"], SER[1], O["load"], O["reaction"], O["flag"]


# ================================================================ the K9 four-bar (module06.html lines 1170-1212)
K9 = dict(Af=(0.0, 0.0), Pf=(-20.0, 0.0), acl=32.0, pcl=34.0, tib=28.0)   # mm; x posterior, y proximal


def k9_pose(th_deg):
    """Tibial attachments (At, Pt) at tibial-link orientation th (deg), both cruciates rigid: the K9 root find
    (brentq on the ACL angle in [-160, -20] deg), here by bisection."""
    th = math.radians(th_deg)
    (ax, ay), (px, py), La, Lp, Lt = K9["Af"], K9["Pf"], K9["acl"], K9["pcl"], K9["tib"]

    def pts(sa):
        At = (ax + La * math.cos(sa), ay + La * math.sin(sa))
        return At, (At[0] + Lt * math.cos(th), At[1] + Lt * math.sin(th))

    def gap(sa):
        _, Pt = pts(sa)
        return math.hypot(Pt[0] - px, Pt[1] - py) - Lp
    lo, hi = math.radians(-160), math.radians(-20)
    assert gap(lo) * gap(hi) < 0
    for _ in range(80):
        mid = (lo + hi) / 2
        if gap(lo) * gap(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return pts((lo + hi) / 2)


def cross(p1, p2, p3, p4):
    """Intersection of lines p1p2 and p3p4 and both line parameters (the K9 `cross`)."""
    r, q = (p2[0] - p1[0], p2[1] - p1[1]), (p4[0] - p3[0], p4[1] - p3[1])
    d = r[0] * q[1] - r[1] * q[0]
    u = ((p3[0] - p1[0]) * q[1] - (p3[1] - p1[1]) * q[0]) / d
    v = ((p3[0] - p1[0]) * r[1] - (p3[1] - p1[1]) * r[0]) / d
    return (p1[0] + u * r[0], p1[1] + u * r[1]), u, v


def centre(th):
    At, Pt = k9_pose(th)
    return cross(K9["Af"], At, K9["Pf"], Pt)


CENTRODE = [centre(float(j))[0] for j in range(61)]            # 0..60 deg, 1 deg steps (K9: linspace(0, 60, 61))
ARC = sum(math.dist(a, b) for a, b in zip(CENTRODE, CENTRODE[1:]))
NET = math.dist(CENTRODE[0], CENTRODE[-1])
# the K9 solution text (line 1172): 42 % -> 15 % along the ACL, (-9.4, -9.4) -> (-0.1, -4.6) mm, arc 10.9, net 10.5
assert [round(centre(t)[1], 2) for t in (0.0, 60.0)] == [0.42, 0.15]
assert [tuple(round(v, 1) for v in CENTRODE[i]) for i in (0, -1)] == [(-9.4, -9.4), (-0.1, -4.6)]
assert (round(ARC, 1), round(NET, 1)) == (10.9, 10.5)
assert round(math.hypot(*K9["Pf"])) == 20                     # Appendix line 1306: femoral link 20 mm


# ================================================================ DBCLS lateral knee: parts and the K9 frame on it
# Path order of the crop (= the source, 71 paths, Chrome bbox listing): 0-5 patella; 6-8, 28-30, 43-46 femur (fill,
# shades, posterior and trochlear cartilage, outline); 9-13 tibia; 14, 15, 31, 42 fibula; 16-18 menisci;
# 19-27, 32-41, 47-70 ligament bands (collateral and capsular), left out so the cruciate lines read.
KNEE_RECOLOUR = {                       # DBCLS lateral knee (st0..st8) -> house tokens (same map as m03 svg #25)
    "#cec2b2": T["bone"][0], "#a59983": T["bone_shade"][0], "#84755d": T["bone"][1], "#eae4dc": "#f7f4ef",
    "#aec5ff": T["fibrocart"][0], "#e3ebff": T["cartilage"][0], "#93a3cc": T["fibrocart"][1],
    "#f4f4f4": T["tendon"][0], "#9e9e9e": T["tendon"][1],
}
KNEE_PARTS = {                          # id: (path indices in drawing order, window x, y, w, h in source units)
    "femur": ([6, 7, 8, 28, 29, 30, 43, 44, 45, 46], (150, 30, 116, 162)),
    "tibia": ([9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 31, 42], (156, 188, 110, 140)),
    "patella": ([0, 1, 2, 3, 4, 5], (260, 82, 48, 80)),
}
# femur path 6 shaft edges, Chrome getPointAtLength samples: y 25 -> x 161.30 / 221.58, y 80 -> 175.28 / 242.87
FEM_AXIS = ((191.44, 25.0), (209.08, 80.0))
PLATEAU = ((165.0, 201.66), (250.0, 195.84))   # tibia path 9 upper outline (lowest y) at x 165 and x 250
TIB_AXIS = ((214.43, 260.0), (215.85, 340.0))   # path 9 shaft edges: y 260 -> 168.10 / 260.76, y 340 -> 183.20 / 248.49
# The K9 frame on the art (a design choice; K9 states lengths only).  The tibial link is perpendicular to the tibial
# shaft, so K9's theta is the angle between the two shafts and theta = 0 is full extension; the PCL tibial end sits on
# the plateau line at x = PT_X; K_ART art units per mm.  K_ART = 2.2 (plateau depth 85 units = 39 mm) and PT_X = 174
# keep the femoral ends inside the femur and the moved meniscus 0.2-3 mm clear of the femoral outline at every
# 10 deg from 0 to 60 deg (searched over K 1.4-2.6, PT_X 165-204 against Chrome samples of paths 16 and 46).
K_ART, PT_X = 2.2, 174.0
ALPHA = math.degrees(math.atan2(FEM_AXIS[1][0] - FEM_AXIS[0][0], FEM_AXIS[1][1] - FEM_AXIS[0][1]))  # shaft tilt
_a = math.radians(ALPHA)
EX, EY = (-math.cos(_a), math.sin(_a)), (-math.sin(_a), -math.cos(_a))   # K9 +x (posterior), +y (proximal) in art
_ta = math.atan2(TIB_AXIS[1][0] - TIB_AXIS[0][0], TIB_AXIS[1][1] - TIB_AXIS[0][1])
_u = (-math.cos(_ta), math.sin(_ta))                                       # tibial link, anterior -> posterior
TH_ART = math.degrees(math.atan2(_u[0] * EY[0] + _u[1] * EY[1], _u[0] * EX[0] + _u[1] * EX[1]))  # the art's flexion
_At0, _Pt0 = k9_pose(TH_ART)
_t = (PT_X - PLATEAU[1][0]) / (PLATEAU[0][0] - PLATEAU[1][0])
_P_art = (PT_X, PLATEAU[1][1] + (PLATEAU[0][1] - PLATEAU[1][1]) * _t)
AF_ART = (_P_art[0] - K_ART * (_Pt0[0] * EX[0] + _Pt0[1] * EY[0]), _P_art[1] - K_ART * (_Pt0[0] * EX[1] + _Pt0[1] * EY[1]))


def knee_doc(idx):
    src = _read("202108_Lateral_view_of_knee_joint_crop_m03f25.svg")
    style = re.search(r'<style>.*?</style>', src, re.S).group(0)
    paths = re.findall(r'<path\b[^>]*/>', src)
    assert len(paths) == 71 and "<text" not in src
    pat = re.compile("|".join(re.escape(c) for c in KNEE_RECOLOUR), re.I)
    return pat.sub(lambda m: KNEE_RECOLOUR[m.group(0).lower()], style + "".join(paths[i] for i in idx))


def SHARED_DEFS():  # noqa: N802 (apply_figs calls this name)
    """The Lynch body kit once per page, plus the three DBCLS knee parts as #m6art_femur / _tibia / _patella."""
    return LB.SHARED_DEFS() + "".join(f'<g id="m6art_{k}">{art_image("<svg>" + knee_doc(i) + "</svg>", b)}</g>'
                                      for k, (i, b) in KNEE_PARTS.items())


def k9_art(v):
    return (AF_ART[0] + K_ART * (v[0] * EX[0] + v[1] * EY[0]), AF_ART[1] + K_ART * (v[0] * EX[1] + v[1] * EY[1]))


def art_k9(q):
    dx, dy = q[0] - AF_ART[0], q[1] - AF_ART[1]
    return ((dx * EX[0] + dy * EX[1]) / K_ART, (dx * EY[0] + dy * EY[1]) / K_ART)


def matrix(f):
    """SVG matrix() of the affine map f (a function of one point)."""
    e = f((0.0, 0.0))
    a, c = f((1.0, 0.0)), f((0.0, 1.0))
    return (f"matrix({a[0] - e[0]:.5f} {a[1] - e[1]:.5f} {c[0] - e[0]:.5f} {c[1] - e[1]:.5f} "
            f"{e[0]:.2f} {e[1]:.2f})")


class Knee:
    """The DBCLS knee on the canvas: A_f at C, z canvas units per art unit; upright = femoral shaft vertical."""

    def __init__(self, C, z, upright=True):
        self.C, self.z = C, z
        self.r = math.radians(ALPHA if upright else 0.0)

    def S(self, q):
        """Art point -> canvas."""
        dx, dy = q[0] - AF_ART[0], q[1] - AF_ART[1]
        c, s = math.cos(self.r), math.sin(self.r)
        return (self.C[0] + self.z * (dx * c - dy * s), self.C[1] + self.z * (dx * s + dy * c))

    def P(self, v):
        """K9 point (mm) -> canvas."""
        return self.S(k9_art(v))

    def tib_move(self, th):
        """Art point of the tibia as drawn -> art point at flexion th (the rigid K9 tibial-link motion)."""
        At, _ = k9_pose(th)
        d = math.radians(th - TH_ART)
        c, s = math.cos(d), math.sin(d)

        def f(q):
            x, y = art_k9(q)
            x, y = x - _At0[0], y - _At0[1]
            return k9_art((At[0] + x * c - y * s, At[1] + x * s + y * c))
        return f

    def femur(self, extra=""):
        return f'<use href="#m6art_femur" transform="{matrix(self.S)}"{extra}/>'

    def patella(self):
        return f'<use href="#m6art_patella" transform="{matrix(self.S)}"/>'

    def tibia(self, th, extra=""):
        m = self.tib_move(th)
        return f'<use href="#m6art_tibia" transform="{matrix(lambda q: self.S(m(q)))}"{extra}/>'

    def tibia_box(self, th):
        """Canvas corners of the tibia window at flexion th (for the frame check of hidden frames)."""
        x, y, w, h = KNEE_PARTS["tibia"][1]
        m = self.tib_move(th)
        return [self.S(m(q)) for q in ((x, y), (x + w, y), (x, y + h), (x + w, y + h))]

    def box(self, part):
        x, y, w, h = KNEE_PARTS[part][1]
        return [self.S(q) for q in ((x, y), (x + w, y), (x, y + h), (x + w, y + h))]


def knee_credit(what):
    return H.ATTRIBUTION["by"].format(author="DataBase Center for Life Science (DBCLS)",
                                      title="202108 Lateral view of knee joint", licence="CC BY 4.0",
                                      changes=f"Recoloured, cropped, ligament bands removed. {what}")


# ================================================================ small drawing helpers
def dot(s, x, y, col, r=3.2, ring="#fff"):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{col}" stroke="{ring}" '
            f'stroke-width="{s(1.2):.2f}"/>')


def pin(s, x, y):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(2.6):.2f}" fill="#fff" stroke="{I["primary"]}" stroke-width="{s(1.2):.2f}"/>'


def bar(s, a, b, col, w=4.0, op=1.0, dash=None):
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    return (f'<line x1="{a[0]:.2f}" y1="{a[1]:.2f}" x2="{b[0]:.2f}" y2="{b[1]:.2f}" stroke="{col}" '
            f'stroke-width="{s(w):.2f}" stroke-linecap="round" opacity="{op}"{da}/>')


def path_d(pts):
    return "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts)


def coil(s, a, b, n=9, amp=6.0, lead=0.12, col=RED, w=2.2):
    """A tension-spring symbol from a to b as a <path> (schematic: the tissue acts as a spring)."""
    L = math.dist(a, b)
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    nx, ny = -uy, ux
    pts = [a]
    t0, t1 = lead, 1 - lead
    for k in range(2 * n + 1):
        t = t0 + (t1 - t0) * k / (2 * n)
        side = 0 if k in (0, 2 * n) else (1 if k % 2 else -1)
        pts.append((a[0] + ux * L * t + nx * amp * side, a[1] + uy * L * t + ny * amp * side))
    pts.append(b)
    return (f'<path d="{path_d(pts)}" fill="none" stroke="{col}" stroke-width="{s(w):.2f}" '
            f'stroke-linejoin="round" stroke-linecap="round"/>')


def leader(s, a, b, col=I["secondary"]):
    return H.line(s, a[0], a[1], b[0], b[1], col)


def arc_arrow(s, p, cx, cy, r, a0, a1, key="geometry"):
    """Circular arc from a0 to a1 (deg, screen y down), head at a1."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    return (f'<path d="M{x0:.2f},{y0:.2f} A{r:.2f},{r:.2f} 0 {1 if abs(a1 - a0) > 180 else 0} {1 if a1 > a0 else 0} '
            f'{x1:.2f},{y1:.2f}" fill="none" stroke="{O[key]}" stroke-width="{s(H.PX["geom"]):.2f}" '
            f'marker-end="url(#{p}a_{key})"/>')


def credit_block(s, x, y_bottom, texts, width):
    """Credit lines wrapped to `width` user units (Georgia: about 0.47 em per character, as lynch_body.credit)."""
    n = int(width / (s(H.PX["credit"]) * 0.47))
    lines = [ln for t in texts for ln in wrap(t, n)]
    return H.credit(s, x, y_bottom - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines), len(lines)


# ================================================================ svg #2  Fig. 1: Achilles path and ACL path
# InjuryMap "Lower leg muscles.svg" source units (no root transform): the lateral leg, anterior LEFT.
ACH = dict(
    box=(255, 425, 240, 690),       # shown window of the m06ach crop (crop window 300 440 480 1100)
    # Achilles path: calf belly centre (gastrocnemius fill, grid read), musculotendinous junction (where the belly
    # fill ends, grid read), tendon centreline at y 960 (m05 F21: edges 409.9 / 419.4), calcaneal insertion (m05 F21)
    path=[(442.0, 560.0), (430.0, 735.0), (414.65, 960.0), (425.05, 1057.65)],
    calf=(452.0, 600.0), tendon=(417.0, 850.0), calc=(455.0, 1085.0),
)


def fig2():
    p = "m6f2_"
    VB = (0, 0, 760, 640)
    s = H.Scale(VB[2], VB[3])
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # ---- left: the calf and Achilles (InjuryMap), anterior to the LEFT as drawn
    z, X0, Y0 = 0.74, 178.0, 50.0
    bx, by, bw, bh = ACH["box"]
    # the art is mirrored so that anterior is to the right, as in the knee panel
    M = lambda q: (X0 + (bx + bw - q[0]) * z, Y0 + (q[1] - by) * z)  # noqa: E731
    art = inner_svg(_read("Lower_leg_muscles_crop_m06ach.svg"))
    assert 'id="Names"' not in art and "<text" not in art
    o.append(f'<g transform="translate({X0 + (bx + bw) * z:.2f} {Y0 - by * z:.2f}) scale({-z} {z})">'
             f'{art_image("<svg>" + art + "</svg>", ACH["box"])}</g>')
    pts = [M(q) for q in ACH["path"]]
    o.append(f'<path d="{path_d(pts)}" fill="none" stroke="{RED}" stroke-width="{s(2.0):.2f}" '
             f'stroke-dasharray="{s(H.DASH_LOA[0]):.2f} {s(H.DASH_LOA[1]):.2f}"/>')
    ins, up = pts[-1], pts[-2]
    L = math.dist(ins, up)
    o.append(H.arrow(s, p, ins[0], ins[1], ins[0] + (up[0] - ins[0]) / L * 70, ins[1] + (up[1] - ins[1]) / L * 70, "force"))
    o.append(dot(s, ins[0], ins[1], RED))
    lx = X0 - 14
    o.append(H.label(s, 10, 28, "Achilles tendon: calf → calcaneus", "label", I["primary"]))
    c = M(ACH["calf"])
    o.append(leader(s, (c[0] - 4, c[1]), (lx + 4, c[1] - 4)))
    o.append(H.label(s, lx, c[1], "calf muscles", "label2", I["primary"], "end"))
    o.append(H.label(s, lx, c[1] + s(16), "(gastrocnemius, soleus)", "label2", I["secondary"], "end"))
    t = M(ACH["tendon"])
    o.append(leader(s, (t[0] - 6, t[1]), (lx + 4, t[1]), RED))
    o.append(H.label(s, lx, t[1] + 5, "Achilles tendon", "label2", RED, "end"))
    o.append(H.label(s, lx, t[1] + 5 + s(16), "stores ≈ 35 J per running", "label2", I["secondary"], "end"))
    o.append(H.label(s, lx, t[1] + 5 + s(32), "step, returns 90–95 %", "label2", I["secondary"], "end"))
    o.append(H.label(s, ins[0] - 14, ins[1] - 40, "pull on the heel", "label2", RED, "end"))
    k = M(ACH["calc"])
    o.append(leader(s, (k[0] - 4, k[1]), (lx + 4, k[1] - 14)))
    o.append(H.label(s, lx, k[1] - 9, "calcaneus (heel bone)", "label2", I["primary"], "end"))
    o.append(H.label(s, X0 + bw * z - 6, Y0 + bh * z - 8, "anterior →", "label2", I["muted"], "end"))
    # ---- right: the knee (DBCLS, as drawn), ACL from the back of the femur to the front of the tibia
    zk = 1.5
    kn = Knee((0.0, 0.0), zk, upright=False)
    fx0, fy0 = min(q[0] for q in kn.box("femur")), min(q[1] for q in kn.box("femur"))
    kn = Knee((486.0 - fx0, 50.0 - fy0), zk, upright=False)
    o += [kn.tibia(TH_ART), kn.femur(), kn.patella()]
    Af, At = kn.P(K9["Af"]), kn.P(_At0)
    o.append(bar(s, Af, At, T["tendon"][0], 7.5))
    o.append(bar(s, Af, At, RED, 3.0))
    o += [pin(s, *Af), pin(s, *At)]
    o.append(H.label(s, 420, 28, "ACL: femur → tibia, inside the knee", "label", I["primary"]))
    o.append(leader(s, (Af[0] - 4, Af[1] - 3), (Af[0] - 40, Af[1] - 46)))
    o.append(H.label(s, Af[0] - 42, Af[1] - 52, "back of the femur", "label2", I["primary"], "end"))
    mid = ((Af[0] + At[0]) / 2, (Af[1] + At[1]) / 2)
    o.append(leader(s, (mid[0] + 2, mid[1] + 5), (mid[0] + 2, mid[1] + 40), RED))
    o.append(H.label(s, mid[0] + 2, mid[1] + 55, "ACL", "label", RED, "middle"))
    o.append(H.label(s, mid[0] + 2, mid[1] + 55 + s(15), "(seen through", "label2", I["secondary"], "middle"))
    o.append(H.label(s, mid[0] + 2, mid[1] + 55 + s(30), "the condyle)", "label2", I["secondary"], "middle"))
    o.append(leader(s, (At[0] + 3, At[1] + 4), (At[0] + 34, At[1] + 34)))
    o.append(H.label(s, At[0] + 36, At[1] + 48, "front of", "label2", I["primary"]))
    o.append(H.label(s, At[0] + 36, At[1] + 48 + s(15), "the tibia", "label2", I["primary"]))
    for part, xy in (("femur", (210.0, 70.0)), ("tibia", (234.0, 300.0)), ("patella", (286.0, 120.0))):
        q = kn.S(xy)
        o.append(H.label(s, q[0], q[1], part, "label2", I["secondary"], "middle"))
    # anterior tibial translation (the motion the ACL resists): arrow across the tibia, anterior = right in this art
    tb = kn.S((196.0, 262.0))
    o.append(H.arrow(s, p, tb[0], tb[1], tb[0] + 70, tb[1], "geometry"))
    yb = max(q[1] for q in kn.box("tibia")) + 22
    o.append(H.label(s, tb[0] + 35, yb, "anterior tibial translation:", "label2", O["geometry"], "middle"))
    o.append(H.label(s, tb[0] + 35, yb + s(15), "the ACL resists it", "label2", O["geometry"], "middle"))
    # ---- credits
    c1 = H.ATTRIBUTION["by-sa"].format(author="InjuryMap", title="Lower leg muscles.svg",
                                       changes="Lateral calf only; labels removed, cropped, mirrored, overlays added.")
    c2 = knee_credit("The ACL line joins the attachments of the Module 6 four-bar (K9).").replace("Art:", "Knee:")
    cb, _ = credit_block(s, 10, VB[3] - 8, [c1, c2], VB[2] - 2 * 10)
    o.append(cb)
    aria = ("Two elastic tissues on real anatomy, both drawn with anterior to the right. Left, a side view of the "
            "lower leg (InjuryMap art): the calf "
            "muscles, gastrocnemius and soleus, narrow into the Achilles tendon, which inserts on the calcaneus; a red "
            "dashed line marks the path from calf to heel and a red arrow the tendon's pull on the calcaneus; the tendon "
            "stores about 35 J per running step and returns 90 to 95 percent. Right, a lateral view of the knee (DBCLS "
            "art): the anterior cruciate ligament, drawn red as seen through the femoral condyle, runs from the "
            "back of the femur to the front of the tibia; a blue arrow marks anterior translation of the tibia, the "
            "motion the ACL resists.")
    return finish(VB, aria, s, o)


# ================================================================ svg #3  Fig. 2: a runner in mid-stance
# Running mid-stance (Novacheck 1998, rounded; the module states no angles): stance knee 40 deg, thigh 15 deg forward
# of vertical (pelvis 10 + hip 25), foot flat (ankle dorsiflexion = shank angle); swing knee 105 deg; arms 90 deg.
RUN = dict(pelvis=10, trunk=-2, near=dict(hip=25, knee=40, shoulder=-25, elbow=95),
           far=dict(hip=15, knee=105, contact=None, ankle=-15, shoulder=30, elbow=95), anchor=("heel", "near"))
FOOT = dict(heel=(-9.5, 26.0), ball=(83.4, 33.4), ach=(-19.5, 10.0), apex=(15.0, -19.5))   # foot-local U, grid read
SHANK_ACH = (-40.0, 150.0)          # shank-local U: 2.5 cm behind the fibula, 60 % down the shank (calf-tendon junction)


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


def fig3():
    p = "m6f3_"
    VB = (0, 0, 600, 640)
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    P = LB.pose(**RUN)
    hgt, x, y = 540.0, 250.0, 566.0
    svg, J = LB.draw(p, s, P, x, y, hgt)
    J["_xy"] = (x, y)
    floor = J["floor_y"]
    o.append(H.line(s, 20, floor, 580, floor, I["rule"], "axis"))
    o.append(svg)
    cx, cy = J["com"]
    heel, ball = seg_pt(J, P, "lat_foot", False, FOOT["heel"]), seg_pt(J, P, "lat_foot", False, FOOT["ball"])
    ach = seg_pt(J, P, "lat_foot", False, FOOT["ach"])
    calf = seg_pt(J, P, "lat_shank", False, SHANK_ACH)
    # springs: Achilles (calf-tendon junction -> calcaneus) and the plantar fascia under the arch
    o.append(coil(s, calf, ach, n=8, amp=5.0))
    o += [dot(s, *calf, RED, 2.6), dot(s, *ach, RED, 2.6)]
    a0, a1 = (heel[0] + 4, heel[1] + 3), (ball[0] - 2, ball[1] + 2)
    o.append(coil(s, a0, a1, n=9, amp=3.2))
    # forces: W at the COM (load); F_GRF at the centre of pressure under the COM (reaction), 2.5 W (K10 stance peak)
    Lw = 46.0
    o.append(H.arrow(s, p, cx, cy + 8, cx, cy + 8 + Lw, "load"))
    o.append(H.label(s, cx + 10, cy + 8 + Lw - 6, it("W"), fill=BRN))
    o.append(H.arrow(s, p, cx, floor + 0.5, cx, floor - 2.5 * Lw, "reaction"))
    o.append(H.label(s, cx + 9, floor - 2.5 * Lw + 26, f'{it("F")}{H.sub("GRF", s)}', fill=BLK))
    o.append(H.label(s, cx + 9, floor - 2.5 * Lw + 26 + s(17), "≈ 2.5 W", "label2", I["secondary"]))
    o.append(H.com_mark(s, cx, cy))
    o.append(H.label(s, cx + 14, cy - 10, "centre of mass", "label2", I["secondary"]))
    # labels: Achilles behind the leg (left), arch in front of the toes (right)
    lx = calf[0] - 70
    o.append(leader(s, (calf[0] - 6, calf[1] + 4), (lx + 4, calf[1] + 4), RED))
    o.append(H.label(s, lx, calf[1] + 9, "Achilles tendon", "label", RED, "end"))
    for j, txt in enumerate(("series spring behind the ankle,", "in line with the calf muscle;", "≈ 35 J stored per step")):
        o.append(H.label(s, lx, calf[1] + 9 + s(17) * (j + 1), txt, "label2", I["secondary"], "end"))
    rx = ball[0] + 74
    o.append(leader(s, (a1[0] - 6, a1[1] + 3), (rx - 4, floor - 34), RED))
    o.append(H.label(s, rx, floor - 44, "plantar fascia / arch", "label", RED))
    o.append(H.label(s, rx, floor - 44 + s(17), "≈ 17 J per step", "label2", I["secondary"]))
    o.append(H.label(s, rx, floor - 44 + s(33), "(the whole arch)", "label2", I["secondary"]))
    o.append(H.label(s, 580, 40, "mid-stance: the planted leg", "label", I["primary"], "end"))
    o.append(H.label(s, 580, 40 + s(18), "compresses, then rebounds", "label", I["primary"], "end"))
    o.append(LB.credit(s, 10, VB[3] - 36, width=VB[2] - 20,
                       extra=" Springs and arrows drawn for this course; F GRF drawn at 2.5 W, the stance peak of K10."))
    aria = ("A runner in mid-stance, side view, facing right (Lynch skeleton art): the planted near leg is under the "
            "body with the knee flexed about 40 degrees and the foot flat; the far leg swings behind with the knee "
            "bent. Two springs are drawn red on the planted leg: a coil on the Achilles tendon behind the ankle, from "
            "the calf to the heel bone, storing about 35 J per step, and a coil under the arch for the plantar fascia, "
            "about 17 J per step for the whole arch. Body weight W points down from the centre of mass; the ground "
            "reaction F GRF, about 2.5 W, points up from the foot under it.")
    return finish(VB, aria, s, o)


# ================================================================ the four-bar overlay (svg #21, #40, #67)
def fourbar(s, kn, th, lab=True, op=1.0, w=3.6):
    """Cruciates (ACL red, PCL blue), the femoral and tibial links (ink), the four pins and the instant centre."""
    At, Pt = k9_pose(th)
    A, Pp = kn.P(K9["Af"]), kn.P(K9["Pf"])
    a, pt = kn.P(At), kn.P(Pt)
    Ic = kn.P(centre(th)[0])
    o = [bar(s, A, Pp, I["primary"], 1.6, op, (5, 3)), bar(s, a, pt, I["primary"], 2.0, op),
         bar(s, A, a, RED, w, op), bar(s, Pp, pt, BLU, w, op)]
    if op == 1.0:
        o += [pin(s, *q) for q in (A, Pp, a, pt)]
        o.append(dot(s, Ic[0], Ic[1], ORA, 4.2))
    return "".join(o), dict(Af=A, Pf=Pp, At=a, Pt=pt, I=Ic)


def centrode_path(s, kn, w=2.4, ticks=True):
    pts = [kn.P(c) for c in CENTRODE]
    o = [f'<path d="{path_d(pts)}" fill="none" stroke="#fff" stroke-width="{s(w + 3):.2f}" stroke-linecap="round"/>',
         f'<path d="{path_d(pts)}" fill="none" stroke="{ORA}" stroke-width="{s(w):.2f}" stroke-linecap="round"/>']
    if ticks:
        o += [f'<circle cx="{pts[j][0]:.2f}" cy="{pts[j][1]:.2f}" r="{s(1.8):.2f}" fill="{ORA}"/>' for j in range(0, 61, 10)]
    return "".join(o), pts


# ================================================================ svg #21  Fig. 19: the knee as a crossed four-bar
def fig21():
    p = "m6f21_"
    z = 1.62
    ths = list(range(0, 61, 10))
    dflt = 3
    kn = Knee((0.0, 0.0), z)
    allq = [q for th in ths for q in kn.tibia_box(th)] + kn.box("femur")   # every frame, hidden ones too
    kn = Knee((24.0 - min(q[0] for q in allq), 30.0 - min(q[1] for q in allq)), z)
    allq = [q for th in ths for q in kn.tibia_box(th)] + kn.box("femur")
    VB = (0, 0, 760, round(max(q[1] for q in allq) + 46))
    s = H.Scale(VB[2], VB[3])
    rx = max(q[0] for q in allq) + 34
    # the enlarged joint (lower right): K9 window x -30..8 mm, y -33..6 mm, same orientation as the main knee
    wx, wy = (-30.0, 8.0), (-34.0, 9.0)
    ib = (rx - 4, 262.0, VB[2] - 8 - (rx - 4), VB[3] - 74 - 262.0)
    k2 = min(ib[2] / (wx[1] - wx[0]), ib[3] / (wy[1] - wy[0]))
    z2 = k2 / K_ART
    C2 = (ib[0] + ib[2] / 2 + k2 * (wx[0] + wx[1]) / 2, ib[1] + ib[3] / 2 + k2 * (wy[0] + wy[1]) / 2)
    kz = Knee(C2, z2)
    cpath, cpts = centrode_path(s, kn, 2.0, ticks=False)
    zpath, zpts = centrode_path(s, kz, 2.4)
    o = [f'<defs>{H.markers(p, s)}<g id="{p}cm">{cpath}</g><g id="{p}cz">{zpath}</g></defs>']   # one copy, every frame uses it
    cpath, zpath = f'<use href="#{p}cm"/>', f'<use href="#{p}cz"/>'
    frames = []
    for k, th in enumerate(ths):
        fb, P = fourbar(s, kn, th, w=2.6)
        fz, Q = fourbar(s, kz, th, w=3.4)
        body = [kn.tibia(th), kn.femur(), cpath, fb,
                window(f"{p}z{k}", kz.tibia(th) + kz.femur(), ib), zpath, fz]
        body.append(H.label(s, Q["At"][0] + 8, Q["At"][1] + 18, "ACL", "label2", RED))
        body.append(H.label(s, Q["Pt"][0] - 8, Q["Pt"][1] + 18, "PCL", "label2", BLU, "end"))
        tl = kn.S(kn.tib_move(th)((214.0, 300.0)))
        body.append(H.label(s, tl[0], tl[1], "tibia", "label2", I["secondary"], "middle"))
        body.append(H.label(s, rx, 34, f"knee flexion θ = {th}°", "label", I["primary"]))
        frames.append(H.frame(k, dflt, "".join(body)))
    o += frames
    o.append(f'<rect x="{ib[0]:.2f}" y="{ib[1]:.2f}" width="{ib[2]:.2f}" height="{ib[3]:.2f}" fill="none" '
             f'stroke="{I["rule"]}" stroke-width="{s(1.2):.2f}"/>')
    zq = [kn.P((wx[0], wy[0])), kn.P((wx[1], wy[1]))]
    zx, zy = min(q[0] for q in zq), min(q[1] for q in zq)
    o.append(f'<rect x="{zx:.2f}" y="{zy:.2f}" width="{abs(zq[1][0] - zq[0][0]):.2f}" height="{abs(zq[1][1] - zq[0][1]):.2f}" '
             f'fill="none" stroke="{I["primary"]}" stroke-width="{s(1):.2f}" stroke-dasharray="{s(3):.2f} {s(2):.2f}"/>')
    o.append(H.label(s, ib[0], ib[1] - 8, f"dashed box enlarged ×{z2 / z:.1f}", "label2", I["secondary"]))
    c0, c1 = zpts[0], zpts[-1]
    o.append(H.label(s, c0[0] + 6, c0[1] + 18, "0°", "label2", ORA))
    o.append(H.label(s, c1[0] - 8, c1[1] - 8, "60°", "label2", ORA, "end"))
    fl = kn.S((205.0, 70.0))
    o.append(H.label(s, fl[0], fl[1], "femur (fixed link)", "label2", I["secondary"], "middle"))
    o.append(H.label(s, rx, 34 + s(17), "anterior to the right", "label2", I["muted"]))
    y = 94.0
    for col, txt, w, dash in ((I["primary"], "femoral link (fixed)", 1.6, (5, 3)), (RED, "ACL", 3.0, None),
                              (I["primary"], "tibial link", 2.0, None), (BLU, "PCL", 3.0, None)):
        o.append(bar(s, (rx, y - 4), (rx + 22, y - 4), col, w, 1.0, dash))
        o.append(H.label(s, rx + 30, y, txt, "label2", I["primary"]))
        y += s(18)
    y += 4
    o.append(dot(s, rx + 11, y - 4, ORA, 4.2))
    o.append(H.label(s, rx + 30, y, "instant centre = the", "label2", I["primary"]))
    o.append(H.label(s, rx + 30, y + s(15), "cruciate crossing (Prop. 10)", "label2", I["primary"]))
    y += s(38)
    o.append(bar(s, (rx, y - 4), (rx + 22, y - 4), ORA, 2.4))
    o.append(H.label(s, rx + 30, y, f"centrode, 0–60°: arc {ARC:.1f} mm,", "label2", I["primary"]))
    o.append(H.label(s, rx + 30, y + s(15), f"net {NET:.1f} mm (K9 lengths)", "label2", I["primary"]))
    cb, _ = credit_block(s, 10, VB[3] - 8, [knee_credit("Femur held fixed; the tibia placed by the four-bar of K9 "
                                                        "(ACL 32, PCL 34, tibial link 28 mm). Overlays drawn for this course.")],
                         VB[2] - 2 * 10)
    o.append(cb)
    aria = ("The knee as a crossed four-bar linkage, on a lateral view of a real knee (DBCLS art), anterior to the "
            "right. The femur is held fixed with its shaft vertical; the tibia hangs below at 30 degrees of flexion "
            "(a slider steps it from 0 to 60 degrees), and the joint is enlarged at the lower right. The anterior "
            "cruciate ligament (red) runs from the back of the femur to the front of the tibia, the posterior cruciate "
            "(blue) from the front of the femur to the back of the tibia; with the femoral and tibial links they close "
            "a four-bar. Their crossing, an orange dot, is the instant centre of rotation; the orange curve traces it "
            f"from 0 to 60 degrees of flexion, the centrode, an arc of {ARC:.1f} mm and a net shift of {NET:.1f} mm, so "
            "the axis is not fixed.")
    extra = H.frames_attr("knee flexion θ", [f"{t}°" for t in ths], dflt)
    return finish(VB, aria, s, o, extra)


# ================================================================ svg #40  C10: the crossed four-bar and its instant centre
def fig40():
    p = "m6f40_"
    th, z = 40.0, 1.55
    kn = Knee((0.0, 0.0), z)
    q = kn.tibia_box(th) + kn.box("femur")
    kn = Knee((12.0 - min(v[0] for v in q), 34.0 - min(v[1] for v in q)), z)
    q = kn.tibia_box(th) + kn.box("femur")
    x1 = max(v[0] for v in q)
    VB = (0, 0, round(x1 + 140), round(max(v[1] for v in q) + 40))
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [f'<defs>{H.markers(p, s)}</defs>', kn.tibia(th), kn.femur()]
    cp, cpts = centrode_path(s, kn, 2.2, ticks=False)
    fb, P = fourbar(s, kn, th, w=3.2)
    o += [cp, fb]
    o.append(H.label(s, P["At"][0] + 8, P["At"][1] + 20, "ACL", "label2", RED))
    o.append(H.label(s, P["Pt"][0] - 8, P["Pt"][1] + 20, "PCL", "label2", BLU, "end"))
    lx = x1 + 8
    o.append(leader(s, (P["I"][0] + 5, P["I"][1] - 3), (lx - 4, P["I"][1] - 40)))
    o.append(H.label(s, lx, P["I"][1] - 44, "instant", "label2", I["primary"]))
    o.append(H.label(s, lx, P["I"][1] - 44 + s(15), "centre", "label2", I["primary"]))
    o.append(H.label(s, lx, P["I"][1] - 44 + s(30), "(crossing)", "label2", I["secondary"]))
    c1 = cpts[-1]
    o.append(H.label(s, lx, P["I"][1] + 24, "its path,", "label2", I["primary"]))
    o.append(H.label(s, lx, P["I"][1] + 24 + s(15), "0–60°", "label2", I["primary"]))
    o.append(leader(s, (c1[0] + 4, c1[1] + 2), (lx - 4, P["I"][1] + 20), ORA))
    y = P["I"][1] + 24 + s(48)
    for col, txt, w, dash in ((I["primary"], "femoral link", 1.6, (5, 3)), (I["primary"], "tibial link", 2.0, None)):
        o.append(bar(s, (lx, y - 4), (lx + 16, y - 4), col, w, 1.0, dash))
        o.append(H.label(s, lx + 22, y, txt, "label2", I["primary"]))
        y += s(16)
    fl = kn.S((205.0, 70.0))
    o.append(H.label(s, fl[0], fl[1], "femur (fixed)", "label2", I["secondary"], "middle"))
    tl = kn.S(kn.tib_move(th)((214.0, 300.0)))
    o.append(H.label(s, tl[0], tl[1], "tibia", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 8, 18, f"knee flexed {th:.0f}°; anterior to the right", "label2", I["secondary"]))
    cb, _ = credit_block(s, 6, VB[3] - 6, [knee_credit("Overlays drawn for this course.")], VB[2] - 2 * 6)
    o.append(cb)
    aria = ("Problem C10 setup, a lateral view of a real knee (DBCLS art) flexed 40 degrees, femur fixed above, tibia "
            "below. The anterior cruciate (red) runs from the back of the femur to the front of the tibia and the "
            "posterior cruciate (blue) from the front of the femur to the back of the tibia; with the femoral and "
            "tibial links (black) they form a crossed four-bar. The orange dot where the cruciates cross is the "
            "instant centre, and the short orange curve is its path over 0 to 60 degrees of flexion. Question: why "
            "does the flexion axis migrate, and what sets its path?")
    return finish(VB, aria, s, o)


# ================================================================ svg #67  K9: the centrode, computed
def window(pid, inner, box):
    """A canvas rect filled with `inner` (canvas coordinates) through a pattern: its box bounds getBBox."""
    x, y, w, h = box
    return (f'<defs><pattern id="{pid}" patternUnits="userSpaceOnUse" x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" '
            f'height="{h:.2f}"><g transform="translate({-x:.2f} {-y:.2f})">{inner}</g></pattern></defs>'
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="url(#{pid})"/>')


def mm(v):
    return f"{v:.1f}".replace("-", "−")


def fig67():
    p = "m6f67_"
    VB = (0, 0, 480, 352)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # ---- left: the knee in the K9 frame, the four-bar at 0 deg (faint) and 60 deg (solid, tibia drawn faint)
    z = 1.75
    lo, hi = (-28.0, -35.0), (16.0, 10.0)                       # K9 window (mm) with a margin
    kn = Knee((0.0, 0.0), z)
    c = [kn.P(v) for v in (lo, hi)]
    kn = Knee((8.0 - min(q[0] for q in c), 48.0 - min(q[1] for q in c)), z)
    c = [kn.P(v) for v in (lo, hi)]
    box = (min(q[0] for q in c), min(q[1] for q in c), abs(c[1][0] - c[0][0]), abs(c[1][1] - c[0][1]))
    o.append(window(p + "w", kn.tibia(60.0, ' opacity="0.5"') + kn.femur(), box))
    o.append(f'<rect x="{box[0]:.2f}" y="{box[1]:.2f}" width="{box[2]:.2f}" height="{box[3]:.2f}" fill="none" '
             f'stroke="{I["rule"]}" stroke-width="{s(1):.2f}"/>')
    f0, _ = fourbar(s, kn, 0.0, op=0.55, w=1.6)
    f6, P6 = fourbar(s, kn, 60.0, w=2.4)
    o += [f0, f6]
    cp, _ = centrode_path(s, kn, 2.0, ticks=False)
    o.append(cp)
    o.append(H.label(s, box[0], 20, "four-bar at 0° (faint)", "label2", I["secondary"]))
    o.append(H.label(s, box[0], 20 + s(15), "and at 60° (solid)", "label2", I["secondary"]))
    o.append(H.label(s, P6["At"][0] + 5, P6["At"][1] + 15, "ACL", "label2", RED))
    o.append(H.label(s, P6["Pt"][0] + 4, P6["Pt"][1] + 22, "PCL", "label2", BLU))
    # zoom window = the plot range at right
    xr, yr = (1.0, -11.0), (-11.0, -3.5)
    zq = [kn.P((xr[0], yr[0])), kn.P((xr[1], yr[1]))]
    o.append(f'<rect x="{min(q[0] for q in zq):.2f}" y="{min(q[1] for q in zq):.2f}" width="{abs(zq[1][0] - zq[0][0]):.2f}" '
             f'height="{abs(zq[1][1] - zq[0][1]):.2f}" fill="none" stroke="{I["primary"]}" stroke-width="{s(1):.2f}" '
             f'stroke-dasharray="{s(3):.2f} {s(2):.2f}"/>')
    # ---- right: the centrode in mm (K9 frame; x increases to the LEFT = posterior, as in the knee)
    x0 = box[0] + box[2] + 58
    w = VB[2] - 12 - x0
    hgt = w * (yr[1] - yr[0]) / (xr[0] - xr[1])                  # equal mm scale on both axes
    ax = Ax((x0, 64.0, x0 + w, 64.0 + hgt), xr, yr)
    tk = [(v, f"{v:.0f}".replace("-", "−")) for v in (0, -4, -8)]
    o += axes(s, ax, tk, [(v, f"{v:.0f}".replace("-", "−")) for v in (-4, -6, -8, -10)], None, None)
    o.append(H.label(s, (ax.x0 + ax.x1) / 2, ax.y0 + 38, "x (mm), posterior ←", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.x0 - 40, ax.top - 14, "y (mm), proximal ↑", "label2", I["primary"]))
    o.append(H.label(s, ax.x0 - 40, 20, "instant centre, dots every 10°", "label2", I["secondary"]))
    pts = [(ax.X(cx), ax.Y(cy)) for cx, cy in CENTRODE]
    o.append(plot_poly(s, pts, ORA))
    o.append(bar(s, pts[0], pts[-1], I["primary"], 1.2, 1.0, (4, 3)))
    for j in range(0, 61, 10):
        o.append(dot(s, pts[j][0], pts[j][1], ORA, 3.0))
    o.append(H.label(s, pts[0][0] + 2, pts[0][1] + 22, f"0°: ({mm(CENTRODE[0][0])}, {mm(CENTRODE[0][1])})",
                     "label2", I["primary"], "end"))
    o.append(H.label(s, pts[-1][0] - 2, pts[-1][1] - 12, f"60°: ({mm(CENTRODE[-1][0])}, {mm(CENTRODE[-1][1])})",
                     "label2", I["primary"]))
    o.append(H.label(s, ax.x0, ax.y0 + 60, f"arc {ARC:.1f} mm; net {NET:.1f} mm", "label2", I["primary"]))
    o.append(H.label(s, ax.x0, ax.y0 + 60 + s(15), "(dashed chord)", "label2", I["secondary"]))
    cb, _ = credit_block(s, 6, VB[3] - 6, [knee_credit("Overlays drawn for this course.")], VB[2] - 2 * 6)
    o.append(cb)
    hp = sorted(([q[0], q[1], f"θ = {j}°: centre ({mm(CENTRODE[j][0])}, {mm(CENTRODE[j][1])}) mm"]
                 for j, q in enumerate(pts)), key=lambda r: r[0])
    aria = ("Problem K9 setup and result. Left: a lateral view of a knee (DBCLS art), anterior to the right, with the "
            "crossed four-bar of K9 (ACL 32 mm red, PCL 34 mm blue, tibial link 28 mm black) at 0 degrees of flexion, "
            "faint, and at 60 degrees, solid; the orange curve is the cruciate crossing over the arc. Right: that "
            "centrode enlarged in the K9 frame (origin at the ACL femoral attachment, x posterior, y proximal, mm): it "
            "runs from (minus 9.4, minus 9.4) mm at 0 degrees to (minus 0.1, minus 4.6) mm at 60 degrees, an arc of "
            f"{ARC:.1f} mm and a net migration of {NET:.1f} mm, posteriorly and proximally.")
    return finish(VB, aria, s, o, H.hover_attr(ax.box, hp))


# ================================================================ the foot arch as a tension truss (svg #23, #50)
class Foot:
    """#hbody_lat_foot (foot-local units U: ankle at the origin, sole at y 38.3, toes to +x) at canvas (x, y), scale z."""

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    def M(self, q):
        return (self.x + q[0] * self.z, self.y + q[1] * self.z)

    def tf(self):
        return f"translate({self.x:.2f} {self.y:.2f}) scale({self.z:.4f})"

    def use(self):
        return f'<use href="#hbody_lat_foot" transform="{self.tf()}"/>'

    def split(self, pid, ang):
        """The foot cut at the metatarsophalangeal line, the toes turned up by ang deg about MTP (windlass pose).
        Each piece is a polygon filled through a pattern, so getBBox sees the polygon, not the whole foot."""
        (x0, y0), (x1, y1) = (-25.0, -21.0), (129.0, 40.0)
        ca, cb = MTP_CUT
        rear = [(x0, y0), ca, cb, (x0, y1)]
        toes = [ca, (x1, y0), (x1, y1), cb]

        def piece(k, poly):
            return (f'<pattern id="{pid}{k}" patternUnits="userSpaceOnUse" x="{x0}" y="{y0}" width="{x1 - x0}" '
                    f'height="{y1 - y0}"><use href="#hbody_lat_foot" transform="translate({-x0} {-y0})"/></pattern>'
                    f'<path d="{path_d(poly)} Z" fill="url(#{pid}{k})"/>')
        return (f'<g transform="{self.tf()}">{piece("r", rear)}'
                f'<g transform="rotate({-ang} {MTP[0]} {MTP[1]})">{piece("t", toes)}</g></g>')


MTP = (90.0, 27.0)                      # foot-local: centre of the metatarsal heads (grid read of the kit foot)
MTP_CUT = ((97.0, -6.0), (84.0, 40.0))  # the cut between the metatarsal heads and the proximal phalanges
MT_R = 6.0                              # metatarsal head radius, U (head bottom at y 33)


def truss(s, p, F, half=False):
    """Struts (bones in compression), tie (plantar fascia, tension T), W at the apex, W/2 at the ends, b and h."""
    hl, bl, ap = F.M(FOOT["heel"]), F.M(FOOT["ball"]), F.M(FOOT["apex"])
    floor = F.M((0.0, 38.3))[1]
    o = [bar(s, hl, ap, I["secondary"], 1.6, 1.0, (6, 4)),
         bar(s, ap, bl, I["secondary"], 1.6, 1.0 if not half else 0.5, (6, 4))]
    o.append(bar(s, hl, bl, "#fff", 6.0))
    o.append(bar(s, hl, bl, RED, 3.0))
    o += [pin(s, *hl), pin(s, *bl), pin(s, *ap)]
    # W at the apex (load), W/2 at the two ends (ground reaction)
    o.append(H.arrow(s, p, ap[0], ap[1] - 62, ap[0], ap[1] - 6, "load"))
    o.append(H.label(s, ap[0] + 9, ap[1] - 40, it("W"), fill=BRN))
    for q in (hl, bl):
        o.append(H.arrow(s, p, q[0], floor + 52, q[0], floor + 2, "reaction"))
        o.append(H.label(s, q[0] + 8, floor + 40, f'{it("W")}/2', "label2", BLK))
    # T on the tie ends, pulling them together
    ux, uy = bl[0] - hl[0], bl[1] - hl[1]
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    o.append(H.arrow(s, p, hl[0] + ux * 6, hl[1] + uy * 6, hl[0] + ux * 46, hl[1] + uy * 46, "force"))
    o.append(H.arrow(s, p, bl[0] - ux * 6, bl[1] - uy * 6, bl[0] - ux * 46, bl[1] - uy * 46, "force"))
    # h: apex to the tie line (vertical), b (or b/2): the horizontal span between the ends
    ty = hl[1] + (ap[0] - hl[0]) / (bl[0] - hl[0]) * (bl[1] - hl[1])
    o.append(H.arrow(s, p, ap[0], ap[1] + 7, ap[0], ty - 3, "geometry", both=True))
    o.append(H.label(s, ap[0] + 7, (ap[1] + ty) / 2 + 5, it("h"), fill=O["geometry"]))
    yd = floor + 70
    xe = ap[0] if half else bl[0]
    o.append(H.line(s, hl[0], floor + 4, hl[0], yd + 6, O["dim"], "leader", H.DASH_REF))
    o.append(H.line(s, xe, floor + 4 if not half else ap[1] + 4, xe, yd + 6, O["dim"], "leader", H.DASH_REF))
    o.append(H.arrow(s, p, hl[0], yd, xe, yd, "dim", both=True))
    o.append(H.label(s, (hl[0] + xe) / 2, yd - 7, it("b") + ("/2" if half else ""), "label2", I["secondary"], "middle"))
    return "".join(o), dict(heel=hl, ball=bl, apex=ap, floor=floor, tie_y=ty, yd=yd)


def foot_credit(extra=""):
    return H.ATTRIBUTION["by"].format(author="Patrick J. Lynch, medical illustrator", title="Skeleton lateral.svg",
                                      licence="CC BY 2.5", changes="Foot only; recoloured." + extra)


# ================================================================ svg #23  Fig. 21: tension truss and windlass
def fig23():
    p = "m6f23_"
    VB = (0, 0, 760, 390)
    s = H.Scale(VB[2], VB[3])
    o = [f'<defs>{H.markers(p, s)}</defs>']
    F = Foot(30.0 + 24.0 * 2.5, 118.0 + 19.5 * 2.5, 2.5)
    o.append(H.line(s, 14, F.M((0, 38.3))[1], 440, F.M((0, 38.3))[1], I["rule"], "axis"))
    o.append(F.use())
    tr, G = truss(s, p, F)
    o.append(tr)
    hl, bl, ap = G["heel"], G["ball"], G["apex"]
    o.append(H.label(s, 30, 30, "Tension truss", "label", I["primary"]))
    o.append(H.label(s, ap[0] + 40, ap[1] - 52, "body weight from the tibia", "label2", BRN))
    sm = ((hl[0] + ap[0]) / 2, (hl[1] + ap[1]) / 2)
    o.append(H.label(s, sm[0] - 14, sm[1] - 10, "strut", "label2", I["secondary"], "end"))
    o.append(H.label(s, sm[0] - 14, sm[1] + 5, "(bones,", "label2", I["secondary"], "end"))
    o.append(H.label(s, sm[0] - 14, sm[1] + 20, "compression)", "label2", I["secondary"], "end"))
    tm = ((hl[0] + bl[0]) / 2 - 30, G["tie_y"] + 2)
    o.append(leader(s, (tm[0], tm[1] + 2), (tm[0] + 22, G["floor"] + 18), RED))
    o.append(H.label(s, tm[0] + 26, G["floor"] + 23, "tie: plantar fascia,", "label2", RED))
    o.append(H.label(s, tm[0] + 26, G["floor"] + 23 + s(15), f'tension {it("T")}', "label2", RED))
    o.append(H.label(s, 440, 54, f'{it("T")} = {it("W")}{it("b")} / (4{it("h")})', "label", I["primary"], "end"))
    o.append(H.label(s, 440, 54 + s(16), "(Prop. 11)", "label2", I["secondary"], "end"))
    o.append(H.label(s, hl[0] - 6, G["floor"] + 30, "heel", "label2", I["secondary"], "end"))
    o.append(H.label(s, bl[0] + 36, G["floor"] + 64, "ball", "label2", I["secondary"]))
    # ---- right: the windlass (toes dorsiflexed, fascia wraps the metatarsal head)
    z2, ang = 1.72, 30.0
    floor2 = F.M((0, 38.3))[1]
    F2 = Foot(476.0 + 24.0 * z2, floor2 - 38.3 * z2, z2)
    o.append(H.label(s, 486, 30, "Windlass at push-off", "label", I["primary"]))
    o.append(H.line(s, 474, floor2, 750, floor2, I["rule"], "axis"))
    o.append(F2.split(p + "ft", ang))
    # fascia: heel -> under the head -> around it -> along the turned proximal phalanx
    c = F2.M(MTP)
    r = MT_R * z2
    a1 = math.radians(90.0 - ang)
    hb = (c[0], c[1] + r)
    ea = (c[0] + r * math.cos(a1), c[1] + r * math.sin(a1))
    tip = (ea[0] + math.cos(math.radians(-ang)) * 24 * z2, ea[1] + math.sin(math.radians(-ang)) * 24 * z2)
    hl2 = F2.M(FOOT["heel"])
    fd = (f"M{hl2[0]:.2f},{hl2[1]:.2f} L{hb[0]:.2f},{hb[1]:.2f} A{r:.2f},{r:.2f} 0 0 0 {ea[0]:.2f},{ea[1]:.2f} "
          f"L{tip[0]:.2f},{tip[1]:.2f}")
    o.append(f'<path d="{fd}" fill="none" stroke="#fff" stroke-width="{s(6):.2f}" stroke-linecap="round"/>')
    o.append(f'<path d="{fd}" fill="none" stroke="{RED}" stroke-width="{s(3):.2f}" stroke-linecap="round"/>')
    o.append(arc_arrow(s, p, c[0], c[1], 30 * z2, -2.0, -2.0 - ang, "geometry"))
    o.append(f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{r:.2f}" fill="none" stroke="{O["dim"]}" '
             f'stroke-width="{s(1):.2f}" stroke-dasharray="{s(2):.2f} {s(2):.2f}"/>')
    o.append(H.label(s, 750, c[1] - 64, "toe dorsiflexed", "label2", O["geometry"], "end"))
    o.append(leader(s, (c[0] - 3, c[1] + r + 3), (c[0] - 26, floor2 + 26), RED))
    o.append(H.label(s, c[0] - 26, floor2 + 40, "fascia wraps the", "label2", RED, "middle"))
    o.append(H.label(s, c[0] - 26, floor2 + 40 + s(15), "metatarsal head:", "label2", RED, "middle"))
    o.append(H.label(s, c[0] - 26, floor2 + 40 + s(30), "the tie shortens", "label2", RED, "middle"))
    ap2 = F2.M(FOOT["apex"])
    o.append(H.arrow(s, p, ap2[0], ap2[1] - 6, ap2[0], ap2[1] - 46, "geometry"))
    o.append(H.label(s, ap2[0] + 8, ap2[1] - 30, "arch rises,", "label2", O["geometry"]))
    o.append(H.label(s, ap2[0] + 8, ap2[1] - 30 + s(15), "foot stiffens", "label2", O["geometry"]))
    cb, _ = credit_block(s, 10, VB[3] - 8, [foot_credit(" Windlass panel: toes turned up 30° about the metatarsal heads. "
                                                        "Truss lines, arrows and the fascia drawn for this course.")],
                         VB[2] - 2 * 10)
    o.append(cb)
    aria = ("Left: the foot skeleton in side view (Lynch art) as a tension truss. Dashed strut lines run through the bones "
            "from the heel up to the apex at the ankle and down to the ball of the foot; body weight W presses down at "
            "the apex and each end carries W/2 from the ground. The plantar fascia (red) is the tie between the ends, "
            "carrying tension T = W b / (4 h), with b the span and h the apex height above the tie (blue). Right: the "
            "windlass at push-off: the toes turned up 30 degrees, the fascia (red) wraps the metatarsal head, the tie "
            "shortens and the arch rises (blue arrow).")
    return finish(VB, aria, s, o)


# ================================================================ svg #50  D10: one strut's free body
def fig50():
    p = "m6f50_"
    z = 2.15
    VB = (0, 0, 440, 330)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    F = Foot(80.0 + 24.0 * z, 82.0 + 19.5 * z, z)
    o.append(H.line(s, 6, F.M((0, 38.3))[1], 434, F.M((0, 38.3))[1], I["rule"], "axis"))
    o.append(F.use())
    tr, G = truss(s, p, F, half=True)
    o.append(tr)
    hl, bl, ap = G["heel"], G["ball"], G["apex"]
    # the free body: the heel-side strut
    pad = 12
    fbx0, fbx1 = hl[0] - pad - 14, ap[0] + pad
    o.append(f'<rect x="{fbx0:.2f}" y="{ap[1] - 22:.2f}" width="{fbx1 - fbx0:.2f}" '
             f'height="{G["floor"] + 4 - ap[1] + 22:.2f}" rx="{s(5):.2f}" fill="none" stroke="{I["rule"]}" '
             f'stroke-width="{s(1.1):.2f}" stroke-dasharray="{s(4):.2f} {s(3):.2f}"/>')
    o.append(H.label(s, fbx0 - 4, G["floor"] + 20, "free body:", "label2", I["secondary"], "end"))
    o.append(H.label(s, fbx0 - 4, G["floor"] + 20 + s(15), "one strut", "label2", I["secondary"], "end"))
    o.append(H.label(s, hl[0] + 30, G["tie_y"] - 10, it("T"), fill=RED))
    o.append(H.label(s, 434, 20, "moments about the apex:", "label2", I["secondary"], "end"))
    o.append(H.label(s, 434, 20 + s(17), f'({it("W")}/2)({it("b")}/2) = {it("T")} {it("h")}', "label", I["primary"], "end"))
    o.append(H.label(s, (hl[0] + bl[0]) / 2 + 40, G["tie_y"] + 19, "plantar fascia", "label2", RED, "middle"))
    cb, _ = credit_block(s, 6, VB[3] - 6, [foot_credit(" Truss lines and arrows drawn for this course.")], VB[2] - 2 * 6)
    o.append(cb)
    aria = ("Problem D10 setup: the foot skeleton in side view (Lynch art) with the arch drawn as a tension truss: two "
            "dashed struts from the heel and the ball meet at the apex at the ankle, where body weight W presses down; "
            "the plantar fascia (red) ties the two ends and carries tension T; each end carries W/2 from the ground. "
            "A dashed box isolates the heel-side strut as a free body: W/2 acts a horizontal distance b/2 from the "
            "apex and T acts a vertical distance h below it, so (W/2)(b/2) = T h.")
    return finish(VB, aria, s, o)


FIGS = {
    2: ("Left: Achilles path from calf to calcaneus. Right: ACL path ", fig2),
    3: ("A runner in mid-stance drawn as a Tier-2 shaded figure. The ", fig3),
    21: ("The knee as a crossed four-bar linkage. A fixed femoral cond", fig21),
    23: ("The medial longitudinal foot arch as a tension truss. Shaded", fig23),
    40: ("knee crossed-cruciate four-bar and instant centre", fig40),
    50: ("foot arch tension truss", fig50),
    67: ("knee four-bar instant-centre locus (centrode)", fig67),
}
