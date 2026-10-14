"""Module 3, group `joints`: joint close-ups in the house style.

Main text (760 px): svg #1 (hip socket + sagittal knee), #2 (knee hinge vs shoulder), #6 (six synovial types),
#8 (four joint types in one hand), #15 (Hertz domes), #18 (deep vs shallow socket), #20 (stability cone, animated).
Problems (400 px): #31 (C4), #32 (C5), #33 (C6), #34 (C7), #36 (C9), #37 (C10), #44 (D7), #45 (D8).

Art (anatomy_kit/svg_paths, rows in ATTRIBUTIONS.md), each a crop made once by crop_art.py:
  Lynch, "Skeleton whole body ant lat views.svg" (CC BY 2.5), anterior view, subject's left side:
    ..._crop_m03hip (hip and pelvis), _m03shoulder, _m03hand, and the joint windows _m03mcp, _m03cmc, _m03carp.
    (Tighter head-only windows were tried: at joint scale they lose the pelvis and scapula and stop reading as a
    hip or a shoulder.)
  DBCLS, "202108 Sagittal section through knee joint.svg" (CC BY 4.0): ..._crop_m03knee.
  DBCLS elbow section (CC BY 4.0) and NIH BioArt 208 arm bones (PD), through m05.body (crops made for Module 5).
Landmarks were measured once in Chrome (getPointAtLength on the source paths, or a grid over the rendered
crop); each constant names its source. Every number is computed here from module03.html (line numbers beside
each constant).
"""
import math
import re
from pathlib import Path

import house as H
from m05.body import ARM, DB, Arm, Inset, art_image, finish, fit_circle, inner_svg, it, wrap
from m05.body import dbcls_art as elbow_art
from m05.plots_main import Ax, axes, dot

T, O, I = H.TISSUE, H.OVERLAY, H.INK
KIT = Path(__file__).resolve().parents[2] / "svg_paths"
DOF = "geometry"                      # a freedom is an angle or a length: geometry blue (green = neural only)

# ---------------------------------------------------------------- numbers module03.html states
R_HIP = 1715.0                        # N, single-leg-stance hip reaction, 2.5 W (line 963)
A_HIP = 10e-4                         # m², loaded hip contact area (line 963)
A_WIDE, A_NARROW = 20e-3, 7e-3        # m, contact radius at the two ends of the svg #16 sweep (line 1061)
BETA_HIP, BETA_SH = 55.0, 22.0        # deg, coverage angles (line 1123)


def p0_hertz(F, a):
    """Peak Hertz pressure p0 = 3F / (2 pi a^2), (5.2) line 978."""
    return 3 * F / (2 * math.pi * a * a)


# ---------------------------------------------------------------- art landmarks (source user units)
LYNCH = "Skeleton_whole_body_ant_lat_views_crop_m03{}.svg"
# Lynch root frame, about 49 units per cm (stature: crown y -10 to sole y 8560 = 1.75 m).
# Femur fill outline above the neck (path 3 of the m03hip crop, getPointAtLength, every 6th sample).
HIP_HEAD = [(490.9, 3937.0), (509.0, 3924.0), (529.2, 3914.6), (550.9, 3909.3), (573.1, 3908.3), (595.1, 3912.0),
            (615.9, 3920.1), (634.3, 3932.6), (647.7, 3950.3), (657.1, 3970.6), (665.9, 3991.1), (672.5, 4012.4),
            (674.6, 4034.6)]
# Humerus fill outline around the head (path 2 of the m03shoulder crop, every 5th sample; tubercle excluded).
HUM_HEAD = [(819, 1623), (825, 1612), (833, 1602), (842, 1594), (852, 1586), (864, 1581), (876, 1576), (888, 1574),
            (900, 1572), (912, 1570), (925, 1570), (937, 1573), (950, 1574), (961, 1578), (857, 1779), (848, 1771),
            (838, 1763), (829, 1754), (821, 1744), (815, 1733), (810, 1722), (806, 1710), (804, 1697), (803, 1685),
            (803, 1672), (805, 1660), (807, 1648), (812, 1636), (818, 1625)]
HUM_SHAFT = ((1007.7, 2000.0), (1047.3, 2300.0))     # humerus fill edge midpoints at y 2000 and 2300
# Hand joints (grid over the rendered m03ip / m03mcp / m03cmc / m03carp crops, 10-unit grid):
HAND = dict(
    pip=(1901.0, 4894.0),     # index proximal interphalangeal joint line, middle of its width
    pip_ax=((1878.0, 4860.0), (1930.0, 4970.0)),   # index finger axis through the PIP (phalanx midlines)
    mcp=(1806.0, 4733.0),     # index metacarpal head, centre of its rounded outline
    mcp_ax=((1790.0, 4660.0), (1835.0, 4820.0)),   # index metacarpal -> proximal phalanx midlines
    cmc=(1757.0, 4415.0),     # trapezium / first metacarpal joint line, middle
    cmc_ax=((1757.0, 4415.0), (1880.0, 4500.0)),   # first metacarpal midline
    carp=(1600.0, 4362.0),    # a capitate / trapezoid joint line, middle
)
# DBCLS knee (source viewBox 0 0 400 400; anterior is RIGHT): femur cortex = path 8, femoral cartilage = 6,
# tibial cartilage = 16 (getPointAtLength, 1200 / 800 / 600 samples).
KNEE = dict(
    distal=(190.7, 201.6, 63.4),   # circle fit to the femoral cortex outline, 172 < x < 233, y > 245 (130 samples)
    post=(176.7, 238.6, 23.4),     # circle fit to the posterior condyle, 150 < x < 172, 222 < y < 262 (99 samples)
    contact=(187.0, 205.0, 271.3),  # x range where the cartilage gap is < 7 units (min 5.7 at x 196), mid-gap y
    fem_axis=((135.5, 60.0), (167.7, 120.0)),     # femur cortex edge midpoints
    tib_axis=((221.7, 330.0), (230.6, 380.0)),    # tibia cortex edge midpoints
    patella=(263.0, 205.0),        # centre of the patella cortex bbox (243.7-282, 173.6-237.1)
)
# NIH BioArt 208 (left arm, anterior view): radius = path 6, x 36.6-43.8 at y 172 (m05.body ARM); its distal end
# near x 15 at the wrist line y 291 (ARM["wrist"]).
NIH_RADIUS = ((40.2, 172.0), (15.0, 290.0))


def _read(name):
    return (KIT / name).read_text(encoding="utf-8")


def lynch(name):
    """A Lynch crop recoloured. The 329 light-grey detail shapes become the bone line colour (not the shade
    colour lynch_body uses on whole bodies): at joint scale the outlines must separate ball from socket."""
    t = re.sub("#d1d3d4", T["bone"][1], inner_svg(_read(LYNCH.format(name))), flags=re.I)
    return H.recolour(t, "lynch")


# The DBCLS knee uses its light blue for cartilage and menisci and its navy for the joint cavity, so the house
# "dbcls" map (made for the elbow) does not fit; this is the same local map as m04/tissue.py KNEE_RECOLOUR.
KNEE_RECOLOUR = {
    "#e2dacf": T["bone"][0], "#aaa59f": T["marrow"][0], "#84755d": T["bone"][1],
    "#adbcf2": T["cartilage"][0], "#29426d": T["fluid"][0], "#6079b2": T["fluid"][1],
    "#ffd664": T["fat"][0], "#f28b8b": T["muscle"][0], "#fdd6d8": T["skin"][0], "#fff3f3": T["tendon"][0],
}


def knee_art():
    src = _read("202108_Sagittal_section_through_knee_joint_crop_m03knee.svg")
    style = re.search(r'<style>.*?</style>', src, re.S).group(0)
    body = src[src.index('<g i:extraneous="self">'):src.index('</switch>')]
    body = re.sub(r'\si:[\w-]+="[^"]*"', '', body)
    assert "<text" not in body and body.count('class="st5"') == 5
    k = [0]

    def menisci(m):                    # st5 paths in order: femoral, tibial, meniscus, meniscus, patellar cartilage
        k[0] += 1
        return 'class="stm"' if k[0] in (3, 4) else m.group(0)
    body = re.sub(r'class="st5"', menisci, body)
    style = style.replace("</style>", f".stm{{fill:{T['fibrocart'][0]};}}</style>")
    pat = re.compile("|".join(re.escape(c) for c in KNEE_RECOLOUR), re.I)
    return pat.sub(lambda m: KNEE_RECOLOUR[m.group(0).lower()], style + body)


def nih_elbow():
    """NIH arm bones (left arm, anterior view): humerus, ulna, radius fills (paths 4, 5, 6)."""
    src = H.recolour(_read("nih_arm_bones.svg"), "nih")
    ds = re.findall(r'<path\b[^>]*?\bd="([^"]+)"[^>]*/>', src)
    assert len(ds) == 24, len(ds)
    st = f'fill="{T["bone"][0]}" stroke="{T["bone"][1]}" stroke-width="0.6" stroke-linejoin="round"'
    return "".join(f'<path d="{ds[i - 1]}" {st}/>' for i in (4, 5, 6))


HIP_C = fit_circle(HIP_HEAD)          # (562.7, 4020.5, 111.4): 2.3 cm at 49 units per cm
HUM_C = fit_circle(HUM_HEAD)          # (914.4, 1681.2, 112.1)


class Place:
    """Art -> figure: P = d + k Rot(rot) diag(m, 1) (q - c); m = -1 mirrors left-right."""

    def __init__(self, c, d, k, rot=0.0, mirror=False):
        self.c, self.d, self.k, self.rot, self.m = c, d, k, rot, (-1 if mirror else 1)

    def __call__(self, q):
        x, y = (q[0] - self.c[0]) * self.m * self.k, (q[1] - self.c[1]) * self.k
        r = math.radians(self.rot)
        return (self.d[0] + x * math.cos(r) - y * math.sin(r), self.d[1] + x * math.sin(r) + y * math.cos(r))

    def tf(self):
        return (f'translate({self.d[0]:.2f} {self.d[1]:.2f}) rotate({self.rot:.3f}) scale({self.m * self.k:.4f} '
                f'{self.k:.4f}) translate({-self.c[0]:.2f} {-self.c[1]:.2f})')

    def box(self, x0, y0, x1, y1):
        pts = [self((x, y)) for x in (x0, x1) for y in (y0, y1)]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        return (round(min(xs), 2), round(min(ys), 2), round(max(xs) - min(xs), 2), round(max(ys) - min(ys), 2))

    def image(self, art, src_box, p=None):
        """art = a key of ART (shared once per page, shown through a window) or an art string (embedded here)."""
        if art in ART:
            return window(f"{p}w_{art}", art, self.tf(), self.box(*src_box))
        return art_image(f'<svg><g transform="{self.tf()}">{art}</g></svg>', self.box(*src_box))


# ---------------------------------------------------------------- art used by several figures: once per page
# key -> (loader, crop window x, y, w, h in source units). SHARED_DEFS puts each one on the page once as
# #m3art_<key>; a figure shows a window of it through a pattern fill (a clip-path would not bound check_frame).
ART = {
    "hip": (lambda: lynch("hip"), (150, 3550, 750, 1000)),
    "shoulder": (lambda: lynch("shoulder"), (650, 1420, 650, 680)),
    "hand": (lambda: lynch("hand"), (1380, 4150, 820, 1100)),
    "knee": (lambda: knee_art(), (125, 110, 170, 235)),
    "elbow": (lambda: elbow_art(""), (0, 0, 400, 400)),
}


def SHARED_DEFS():
    return "".join(f'<g id="m3art_{k}">{art_image("<svg>" + f() + "</svg>", b)}</g>' for k, (f, b) in ART.items())


def window(pid, key, tf, box):
    """The figure-space box (x, y, w, h) filled with #m3art_<key> mapped by tf (source -> figure)."""
    x, y, w, h = box
    return (f'<defs><pattern id="{pid}" patternUnits="userSpaceOnUse" x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" '
            f'height="{h:.2f}"><g transform="translate({-x:.2f} {-y:.2f}) {tf}"><use href="#m3art_{key}"/></g>'
            f'</pattern></defs><rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="url(#{pid})"/>')


def elbow_image(p, centre, sc, box):
    """The m05 DBCLS elbow (mirrored: anterior right; humerus shaft vertical), trochlea centre at `centre`.
    Returns (window, Inset) so ins.M maps source points."""
    ins = Inset("", None, centre, sc)
    tc = ins.tc
    tf = (f'translate({centre[0]:.2f} {centre[1]:.2f}) scale({-sc:.4f} {sc:.4f}) rotate({ins.rot:.3f}) '
          f'translate({-tc[0]:.2f} {-tc[1]:.2f})')
    return window(f"{p}w_elbow", "elbow", tf, box), ins


# ---------------------------------------------------------------- drawing helpers (local)
def arc(s, p, cx, cy, r, a0, a1, key=DOF, both=False, w="geom"):
    """Circular arc from a0 to a1 (deg, screen y down), head at a1 (and a0 if both)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    ms = f' marker-start="url(#{p}a_{key})"' if both else ""
    return (f'<path d="M{x0:.2f},{y0:.2f} A{r:.2f},{r:.2f} 0 {1 if abs(a1 - a0) > 180 else 0} {1 if a1 > a0 else 0} '
            f'{x1:.2f},{y1:.2f}" fill="none" stroke="{O[key]}" stroke-width="{s(H.PX[w]):.2f}" '
            f'marker-end="url(#{p}a_{key})"{ms}/>')


def ell(s, p, cx, cy, rx, ry, phi, t0, t1, key=DOF, both=False):
    """Elliptical arc (a rotation about an axis in the picture plane, seen obliquely): parameter t0 -> t1 (deg),
    major axis turned phi deg. Drawn as a sampled <path>, so the overlap gate does not treat it as a curve."""
    f = math.radians(phi)
    pts = []
    for i in range(41):
        t = math.radians(t0 + (t1 - t0) * i / 40)
        ex, ey = rx * math.cos(t), ry * math.sin(t)
        pts.append((cx + ex * math.cos(f) - ey * math.sin(f), cy + ex * math.sin(f) + ey * math.cos(f)))
    d = "M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    ms = f' marker-start="url(#{p}a_{key})"' if both else ""
    return (f'<path d="{d}" fill="none" stroke="{O[key]}" stroke-width="{s(H.PX["geom"]):.2f}" stroke-linejoin="round" '
            f'marker-end="url(#{p}a_{key})"{ms}/>')


def axis_line(s, c, deg, half):
    """A rotation axis lying in the picture plane: short dashed line through c."""
    dx, dy = half * math.cos(math.radians(deg)), half * math.sin(math.radians(deg))
    return H.line(s, c[0] - dx, c[1] - dy, c[0] + dx, c[1] + dy, O["dim"], "leader", (3, 2.5))


def axis_dot(s, c):
    """A rotation axis normal to the picture plane (seen end-on)."""
    return (f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{s(3.6):.2f}" fill="#fff" stroke="{O["dim"]}" '
            f'stroke-width="{s(1.1):.2f}"/><circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{s(1.2):.2f}" fill="{O["dim"]}"/>')


def lead(s, x1, y1, x2, y2, col=None):
    return H.line(s, x1, y1, x2, y2, col or I["muted"], "leader")


def ring(s, x, y, col=O["geometry"], r=5.5):
    """Joint mark: white-backed ring (a mark, not anatomy)."""
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="none" stroke="#fff" stroke-width="{s(3.2):.2f}"/>'
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="none" stroke="{col}" stroke-width="{s(1.6):.2f}"/>')


def pol(c, r, deg):
    return (c[0] + r * math.cos(math.radians(deg)), c[1] + r * math.sin(math.radians(deg)))


def cone(s, c, axis_deg, beta, L):
    """Stability cone: wedge of half-angle beta about the axis direction (deg, screen), rim lines dashed."""
    q0, q1 = pol(c, L, axis_deg - beta), pol(c, L, axis_deg + beta)
    return (f'<path d="M{c[0]:.2f},{c[1]:.2f} L{q0[0]:.2f},{q0[1]:.2f} A{L:.2f},{L:.2f} 0 0 1 {q1[0]:.2f},{q1[1]:.2f} Z" '
            f'fill="{O["geometry"]}" fill-opacity="0.10" stroke="none"/>' +
            H.line(s, c[0], c[1], q0[0], q0[1], O["geometry"], "ref", H.DASH_REF) +
            H.line(s, c[0], c[1], q1[0], q1[1], O["geometry"], "ref", H.DASH_REF))


def angle_arc(s, c, r, a0, a1, col=O["geometry"]):
    x0, y0 = pol(c, r, a0)
    x1, y1 = pol(c, r, a1)
    return (f'<path d="M{x0:.2f},{y0:.2f} A{r:.2f},{r:.2f} 0 0 {1 if a1 > a0 else 0} {x1:.2f},{y1:.2f}" fill="none" '
            f'stroke="{col}" stroke-width="{s(1.3):.2f}"/>')


def head_outline(s, c, r, col=O["dim"]):
    return (f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{r:.2f}" fill="none" stroke="{col}" stroke-width="{s(1.2):.2f}" '
            f'stroke-dasharray="{s(4):.1f} {s(3):.1f}"/>')


def deg(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


def credit_lynch(changes="Recoloured, cropped; overlays drawn for this course."):
    return H.ATTRIBUTION["by"].format(author="Patrick J. Lynch, medical illustrator",
                                      title="Skeleton whole body ant lat views.svg", licence="CC BY 2.5", changes=changes)


def credit_dbcls(title, changes="Recoloured, cropped; overlays drawn for this course."):
    return H.ATTRIBUTION["by"].format(author="DataBase Center for Life Science (DBCLS)", title=title,
                                      licence="CC BY 4.0", changes=changes)


def credit_nih(changes="Recoloured, cropped."):
    return H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt 208", title="Human Arm Bones", changes=changes)


KNEE_T = "202108 Sagittal section through knee joint"
ELBOW_T = "202107 Sagittal section through the elbow joint"


def credits(s, vb, lines, x=8, gap=6):
    return H.credit(s, x, vb[1] + vb[3] - gap - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines)


# ================================================================ svg #1  hip socket + sagittal knee
def fig1():
    p = "m3f1_"
    VB = (0, 0, 760, 452)
    s = H.Scale(VB[2], VB[3])
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # ---- hip (Lynch, subject's left hip, anterior view)
    hp = Place((150.0, 3550.0), (14.0, 12.0), 0.345)
    o.append(hp.image("hip", (150, 3550, 900, 4550), p))
    hc, hr = hp(HIP_C[:2]), HIP_C[2] * hp.k
    o.append(head_outline(s, hc, hr))
    o.append(H.joint_centre(s, *hc))
    # the acetabular roof: the head arc the socket covers about the load axis (vertical), half-angle 55 deg
    cov = [pol(hc, hr + s(2.5), -90 + BETA_HIP * (i / 10 - 1)) for i in range(21)]
    o.append(f'<path d="M{" L".join(f"{x:.2f},{y:.2f}" for x, y in cov)}" fill="none" stroke="{O["flag"]}" '
             f'stroke-width="{s(4):.2f}" stroke-linecap="round"/>')
    lx = 292
    il = hp((330.0, 3720.0))
    o.append(lead(s, il[0] + 4, il[1], lx - 4, il[1] + 2))
    o.append(H.label(s, lx, il[1] + 7, "ilium (pelvis)"))
    ac = pol(hc, hr + s(3), -90 + BETA_HIP)
    o.append(lead(s, ac[0] + 4, ac[1] - 2, lx - 4, ac[1] - 16))
    o.append(H.label(s, lx, ac[1] - 11, "acetabulum (socket)"))
    o.append(H.label(s, lx, ac[1] + 6, "wraps over the head", "label2", I["secondary"]))
    fh = (hc[0] + hr * 0.55, hc[1] + hr * 0.30)
    o.append(lead(s, fh[0] + 3, fh[1], lx - 4, fh[1] + 30))
    o.append(H.label(s, lx, fh[1] + 35, "femoral head (ball)"))
    o.append(H.label(s, 150, 378, "hip: deep socket", "label", I["primary"], "middle"))
    # ---- knee (DBCLS sagittal section, anterior right)
    kp = Place((130.0, 112.0), (474.0, 10.0), 1.40)
    o.append(kp.image("knee", (130, 112, 295, 345), p))
    x0c, x1c, yc = KNEE["contact"]
    c0, c1 = kp((x0c, yc)), kp((x1c, yc))
    o.append(H.line(s, c0[0], c0[1], c1[0], c1[1], O["flag"], "force", extra='stroke-linecap="round"'))
    rx = 714
    for q, t in (((150.0, 160.0), "femur"), ((KNEE["patella"][0] + 10, KNEE["patella"][1]), "patella"),
                 ((215.0, 335.0), "tibia")):
        a = kp(q)
        o.append(lead(s, a[0] + 3, a[1], rx - 4, a[1]))
        o.append(H.label(s, rx, a[1] + 5, t))
    lx2 = 462
    for q, t, t2, ty in (((156.0, 236.0), "femoral condyle", None, 200),
                         ((168.0, 277.0), "meniscus", None, 250),
                         ((None, None), "contact region", "(cartilage on cartilage)", 296),
                         ((166.0, 292.0), "tibial plateau", None, 350)):
        if q[0] is None:
            a = ((c0[0] + c1[0]) / 2, c0[1])
            o.append(H.line(s, a[0], a[1] + 3, lx2 + 4, ty - 4, I["primary"], "leader"))
        else:
            a = kp(q)
            o.append(lead(s, a[0] - 3, a[1], lx2 + 4, ty - 4))
        o.append(H.label(s, lx2, ty, t, anchor="end"))
        if t2:
            o.append(H.label(s, lx2, ty + 16, t2, "label2", I["secondary"], "end"))
    o.append(H.label(s, 590, 378, "knee: condyles + plateau", "label", I["primary"], "middle"))
    lines = wrap(credit_lynch("Hip: recoloured, cropped."), 125) + wrap(
        credit_dbcls(KNEE_T, "Recoloured, cropped. Overlays drawn for this course.").replace("Art:", "Knee:"), 125)
    o.append(credits(s, VB, lines))
    aria = ("Left: the left hip in front view (Lynch skeleton art): the femoral head, a ball about 2.3 cm in radius, "
            "sits under the acetabulum of the pelvis, which wraps over the top of the head; the covered arc is marked "
            "in orange and the head centre with a cross. Right: a sagittal section of the knee (DBCLS art) with the "
            "femur, its rounded condyle, the patella in front, the menisci, the tibial plateau and the tibia; an orange "
            "line marks the contact region where the femoral and tibial cartilage meet.")
    return finish(VB, aria, s, o)


# ================================================================ svg #2  knee hinge vs shoulder ball-and-socket
def fig2():
    p = "m3f2_"
    VB = (0, 0, 760, 452)
    s = H.Scale(VB[2], VB[3])
    blu = O["geometry"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(H.line(s, 380, 14, 380, 380, "#e6e6e6", "leader"))
    o.append(H.label(s, 190, 26, "Knee — hinge", "label", I["primary"], "middle", 'font-weight="bold"'))
    o.append(H.label(s, 570, 26, "Shoulder — ball and socket", "label", I["primary"], "middle", 'font-weight="bold"'))
    # ---- knee: DBCLS sagittal section; the flexion axis is the posterior-condyle centre of curvature
    kp = Place((130.0, 112.0), (104.0, 42.0), 1.25)
    o.append(kp.image("knee", (130, 112, 295, 345), p))
    ax_ = kp(KNEE["post"][:2])
    tib = kp(KNEE["tib_axis"][1])
    fem = kp((168.0, 140.0))
    a_t = deg(ax_, tib)
    o.append(axis_dot(s, ax_))
    o.append(arc(s, p, ax_[0], ax_[1], 118, a_t - 26, a_t + 20, both=True))
    e = pol(ax_, 128, a_t + 22)
    o.append(H.label(s, e[0] - 6, e[1] + 14, "flex / extend", fill=blu, anchor="end"))
    o.append(lead(s, ax_[0] - 6, ax_[1] - 4, 98, 150))
    o.append(H.label(s, 94, 140, "hinge axis", "label2", I["secondary"], "end"))
    o.append(H.label(s, 94, 155, "(normal to", "label2", I["secondary"], "end"))
    o.append(H.label(s, 94, 170, "the page)", "label2", I["secondary"], "end"))
    o.append(H.label(s, fem[0] + 8, fem[1] + 18, "femur", "label2", I["secondary"]))
    tb = kp((262.0, 330.0))
    o.append(H.label(s, tb[0] + 6, tb[1], "tibia", "label2", I["secondary"]))
    o.append(H.label(s, 190, 358, "1 rotational DOF · highly stable", "label", I["primary"], "middle"))
    o.append(H.label(s, 190, 376, "keeps 1 freedom, locks out 5", "label2", I["secondary"], "middle"))
    # ---- shoulder: Lynch, subject's left shoulder, anterior view
    sp = Place((700.0, 1450.0), (416.0, 40.0), 0.56)
    o.append(sp.image("shoulder", (700, 1450, 1250, 2000), p))
    hc, hr = sp(HUM_C[:2]), HUM_C[2] * sp.k
    o.append(H.joint_centre(s, *hc))
    sh = sp(HUM_SHAFT[0])
    a_s = deg(hc, sh)
    # 1: abduction / adduction, in the picture (coronal) plane, about the antero-posterior axis (end-on)
    o.append(arc(s, p, hc[0], hc[1], 150, a_s - 26, a_s + 20, both=True))
    q = pol(hc, 158, a_s - 28)
    o.append(H.label(s, q[0] + 8, q[1] + 2, "ab- / adduction", fill=blu))
    # 2: flexion / extension, about the medio-lateral axis (in the picture plane, horizontal)
    o.append(axis_line(s, hc, 0, hr + 26))
    o.append(ell(s, p, hc[0], hc[1], hr * 0.85, 13, 90, 200, 480))
    q = (hc[0] - hr - 30, hc[1] - hr + 4)
    o.append(H.label(s, q[0], q[1], "flexion /", fill=blu, anchor="end"))
    o.append(H.label(s, q[0], q[1] + 17, "extension", fill=blu, anchor="end"))
    # 3: axial rotation about the humerus long axis
    m = pol(hc, hr + 70, a_s)
    o.append(axis_line(s, m, a_s, 34))
    o.append(ell(s, p, m[0], m[1], 30, 9, a_s - 90, 200, 500))
    o.append(H.label(s, m[0] - 38, m[1] + 5, "axial rotation", fill=blu, anchor="end"))
    o.append(H.label(s, hc[0] - hr - 30, hc[1] + 46, "glenoid", "label2", I["secondary"], "end"))
    o.append(lead(s, hc[0] - hr - 26, hc[1] + 42, hc[0] - hr + 6, hc[1] + 30))
    o.append(H.label(s, 570, 358, "3 rotational DOF · easily dislocated", "label", I["primary"], "middle"))
    o.append(H.label(s, 570, 376, "keeps 3 freedoms, locks out 3", "label2", I["secondary"], "middle"))
    lines = wrap(credit_dbcls(KNEE_T, "Recoloured, cropped.").replace("Art:", "Knee:"), 125) + wrap(
        credit_lynch("Recoloured, cropped. Arrows drawn for this course: blue = a kept freedom.").replace(
            "Art:", "Shoulder:"), 125)
    o.append(credits(s, VB, lines))
    aria = ("Left, the knee as a hinge: a sagittal section of the knee (DBCLS art) with one blue double arrow, flexion "
            "and extension of the tibia about a single axis through the femoral condyle, normal to the page. The knee "
            "keeps 1 freedom and locks out 5: highly stable. Right, the shoulder as a ball and socket: the left shoulder "
            "in front view (Lynch skeleton art) with three blue arrows about the centre of the humeral head: "
            "abduction and adduction, flexion and extension, and axial rotation. It keeps 3 freedoms and locks out 3: "
            "easily dislocated.")
    return finish(VB, aria, s, o)


# ================================================================ svg #6  the six synovial joint types
def fig6():
    p = "m3f6_"
    VB = (0, 0, 760, 500)
    s = H.Scale(VB[2], VB[3])
    blu = O["geometry"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    CW, RH, Y2 = 253.3, 228.0, 0.0
    for k in (1, 2):
        o.append(H.line(s, CW * k, 12, CW * k, 2 * RH - 12, "#e6e6e6", "leader"))
    o.append(H.line(s, 12, RH, 760 - 12, RH, "#e6e6e6", "leader"))
    cells = [("Hinge", "1 DOF", "elbow (shown) · finger"), ("Pivot", "1 DOF", "radio-ulnar (shown) · C1–C2"),
             ("Condyloid", "2 DOF", "knuckle (shown) · wrist"), ("Saddle", "2 DOF", "thumb base (carpometacarpal)"),
             ("Ball and socket", "3 DOF", "hip (shown) · shoulder"), ("Plane (gliding)", "≈2 DOF, sliding",
                                                                       "wrist bones (shown) · facets")]
    for n, (t, dof, ex) in enumerate(cells):
        cx, y = CW * (n % 3 + 0.5), RH * (n // 3)
        o.append(H.label(s, cx, y + 26, t, "label", I["primary"], "middle", 'font-weight="bold"'))
        o.append(H.label(s, cx, y + 196, dof, "label", blu, "middle", 'font-weight="bold"'))
        o.append(H.label(s, cx, y + 214, ex, "label2", I["secondary"], "middle"))
    art_y0, art_h = 38.0, 140.0          # art window inside each cell: y + 38 .. y + 178

    def win(n, w=200.0):
        cx, y = CW * (n % 3 + 0.5), RH * (n // 3)
        return (round(cx - w / 2, 2), round(y + art_y0, 2), w, art_h)

    # ---- 1 hinge: DBCLS elbow, flexion in the picture plane about the trochlea centre (axis normal to the page)
    b = win(0)
    img, ins = elbow_image(p, (b[0] + 92, b[1] + 66), 0.62, b)
    o.append(img)
    tc = ins.M(ins.tc[:2])
    a_f = deg(ins.M(DB["rad_axis"][0]), ins.M(DB["rad_axis"][1]))
    o.append(axis_dot(s, tc))
    o.append(arc(s, p, tc[0], tc[1], 58, a_f - 30, a_f + 22, both=True))
    o.append(H.label(s, b[0] + 4, b[1] + 14, "humerus", "label2", I["secondary"]))
    o.append(H.label(s, b[0] + b[2] - 2, b[1] + b[3] - 6, "ulna", "label2", I["secondary"], "end"))
    # ---- 2 pivot: NIH arm, the radius turns about its own long axis against the ulna
    b = win(1)
    kn = 1.75
    npl = Place((-8.0, 112.0), (b[0], b[1]), kn)
    o.append(npl.image(nih_elbow(), (-8, 112, -8 + b[2] / kn, 112 + b[3] / kn)))
    r0, r1 = npl(NIH_RADIUS[0]), npl(NIH_RADIUS[1])
    a_r = deg(r0, r1)
    o.append(axis_line(s, pol(r0, 24, a_r), a_r, 26))
    o.append(ell(s, p, *pol(r0, 30, a_r), 22, 7, a_r + 90, 200, 520))
    o.append(H.label(s, r0[0] - 26, r0[1] + 36, "radius", "label2", I["secondary"], "end"))
    o.append(H.label(s, r0[0] + 44, r0[1] + 36, "ulna", "label2", I["secondary"]))
    hm = npl((60.0, 122.0))
    o.append(H.label(s, hm[0] + 10, hm[1] + 8, "humerus", "label2", I["secondary"]))
    # ---- 3 condyloid: Lynch index knuckle (MCP); ab-/adduction in the plane, flexion about a horizontal axis
    b = win(2, 150.0)
    mpl = Place((1745.0, 4645.0), (b[0], b[1]), b[2] / 170.0)
    o.append(mpl.image(lynch("mcp"), (1745, 4645, 1915, 4645 + 170.0 * art_h / b[2])))
    j = mpl(HAND["mcp"])
    a_m = deg(mpl(HAND["mcp_ax"][0]), mpl(HAND["mcp_ax"][1]))
    o.append(axis_dot(s, j))
    o.append(arc(s, p, j[0], j[1], 50, a_m - 30, a_m + 30, both=True))
    o.append(axis_line(s, j, a_m + 90, 46))
    o.append(ell(s, p, j[0], j[1], 32, 9, a_m, 200, 480))
    # ---- 4 saddle: Lynch thumb carpometacarpal; flexion in the palm plane, abduction out of it
    b = win(3, 200.0)
    cpl = Place((1645.0, 4320.0), (b[0], b[1]), b[2] / 235.0)
    o.append(cpl.image(lynch("cmc"), (1645, 4320, 1880, 4320 + 235.0 * art_h / b[2])))
    j = cpl(HAND["cmc"])
    a_c = deg(cpl(HAND["cmc_ax"][0]), cpl(HAND["cmc_ax"][1]))
    o.append(axis_dot(s, j))
    o.append(arc(s, p, j[0], j[1], 56, a_c - 30, a_c + 30, both=True))
    o.append(axis_line(s, pol(j, 10, a_c), a_c + 90, 44))
    o.append(ell(s, p, *pol(j, 10, a_c), 36, 10, a_c, 200, 480))
    o.append(H.label(s, b[0] + 6, b[1] + b[3] - 8, "trapezium", "label2", I["secondary"]))
    o.append(H.label(s, b[0] + b[2] - 4, b[1] + b[3] - 8, "1st metacarpal", "label2", I["secondary"], "end"))
    # ---- 5 ball and socket: Lynch hip; three rotations about the head centre
    b = win(4, 200.0)
    kh = 0.30
    hpl = Place((HIP_C[0] - 0.42 * b[2] / kh, HIP_C[1] - 0.40 * art_h / kh), (b[0], b[1]), kh)
    sx, sy = hpl.c
    o.append(hpl.image("hip", (sx, sy, sx + b[2] / kh, sy + art_h / kh), p))
    hc, hr = hpl(HIP_C[:2]), HIP_C[2] * hpl.k
    o.append(head_outline(s, hc, hr))
    o.append(axis_dot(s, hc))
    o.append(arc(s, p, hc[0], hc[1], hr + 14, 100, 160, both=True))
    o.append(axis_line(s, hc, 0, hr + 18))
    o.append(ell(s, p, hc[0], hc[1], hr * 0.8, 8, 90, 200, 480))
    fs = hpl((690.0, 4250.0))                         # femoral shaft, below the neck
    o.append(axis_line(s, fs, 80, 26))
    o.append(ell(s, p, fs[0], fs[1], 22, 6, -10, 200, 500))
    o.append(H.label(s, b[0] + 4, b[1] + 14, "pelvis", "label2", I["secondary"]))
    o.append(H.label(s, fs[0] + 26, fs[1] + 4, "femur", "label2", I["secondary"]))
    # ---- 6 plane: Lynch carpals; small sliding in two directions across a flat joint
    b = win(5, 220.0)
    qpl = Place((1420.0, 4230.0), (b[0], b[1]), b[2] / 340.0)
    o.append(qpl.image(lynch("carp"), (1420, 4230, 1760, 4230 + 340.0 * art_h / b[2])))
    j = qpl(HAND["carp"])
    o.append(H.arrow(s, p, j[0] - 30, j[1], j[0] + 30, j[1], DOF, both=True))
    o.append(H.arrow(s, p, j[0], j[1] - 26, j[0], j[1] + 26, DOF, both=True))
    o.append(H.label(s, j[0] + 36, j[1] + 5, "slide", "label2", blu))
    lines = wrap("Art: DBCLS, “" + ELBOW_T + "”, CC BY 4.0; NIH NIAID BioArt 208, “Human Arm Bones”, public domain; "
                 "Patrick J. Lynch, medical illustrator, “Skeleton whole body ant lat views.svg”, CC BY 2.5; via Wikimedia Commons. "
                 "Recoloured, cropped. Blue arrows drawn for this course: curved = rotation, straight = sliding; "
                 "a dashed line or a dot (seen end-on) marks the axis.", 140)
    o.append(credits(s, VB, lines))
    aria = ("A grid of the six synovial joint types, each drawn on a real joint with blue arrows for its freedoms "
            "(curved = rotation, straight = sliding). Hinge, 1 DOF: an elbow section turning about the trochlea. "
            "Pivot, 1 DOF: the radius turning about its own long axis beside the ulna. Condyloid, 2 DOF: a knuckle "
            "with flexion and side-to-side motion. Saddle, 2 DOF: the thumb base with two rotations. Ball and socket, "
            "3 DOF: the hip with three rotations about the head centre. Plane, about 2 DOF of small sliding: the "
            "wrist bones.")
    return finish(VB, aria, s, o)


# ================================================================ svg #8  four joint types in one hand
def fig8():
    p = "m3f8_"
    VB = (0, 0, 760, 420)
    s = H.Scale(VB[2], VB[3])
    o = [f'<defs>{H.markers(p, s)}</defs>']
    hp = Place((1390.0, 4160.0), (40.0, 8.0), 0.352)
    o.append(hp.image("hand", (1390, 4160, 2170, 5240), p))
    rows = [("carp", "wrist bones (intercarpal)", "plane · gliding, ≈2 DOF of small sliding", 62),
            ("cmc", "thumb base (carpometacarpal, CMC)", "saddle · 2 DOF", 138),
            ("mcp", "knuckle (metacarpophalangeal, MCP)", "condyloid · 2 DOF", 214),
            ("pip", "finger joint (interphalangeal)", "hinge · 1 DOF", 290)]
    lx = 400
    for key, t1, t2, ty in rows:
        j = hp(HAND[key])
        o.append(lead(s, j[0] + s(6), j[1], lx - 6, ty - 5, I["secondary"]))
        o.append(ring(s, *j))
        o.append(H.label(s, lx, ty, t1))
        o.append(H.label(s, lx, ty + 17, t2, "label2", O["geometry"]))
    lines = wrap(credit_lynch("Left hand, palm forward; recoloured, cropped. Joint rings and labels drawn for this "
                              "course."), 125)
    o.append(credits(s, VB, lines))
    aria = ("The bones of a left hand, palm forward (Lynch skeleton art), with four joints ringed in blue and labelled: "
            "the wrist bones (intercarpal joints, plane, gliding, about 2 DOF of small sliding), the thumb base "
            "(carpometacarpal, saddle, 2 DOF), the index knuckle (metacarpophalangeal, condyloid, 2 DOF), and the "
            "index finger joint (proximal interphalangeal, hinge, 1 DOF).")
    return finish(VB, aria, s, o)


# ================================================================ svg #15  Hertz domes (computed)
def fig15():
    p = "m3f15_"
    VB = (0, 0, 760, 348)
    s = H.Scale(VB[2], VB[3])
    red = H.SERIES[0]
    o = []
    panels = []
    for k, (a, name) in enumerate(((A_WIDE, "congruent"), (A_NARROW, "incongruent"))):
        x0 = 86 if k == 0 else 456
        ax = Ax((x0, 54, x0 + 280, 262), (-25.0, 25.0), (0.0, 18.0))
        p0 = p0_hertz(R_HIP, a) / 1e6
        pm = R_HIP / (math.pi * a * a) / 1e6
        n = 4000                                      # check: the dome carries R (int p 2 pi r dr = R)
        tot = sum(p0 * 1e6 * math.sqrt(max(0.0, 1 - ((i + 0.5) / n) ** 2)) * 2 * math.pi * ((i + 0.5) / n * a)
                  * (a / n) for i in range(n))
        assert abs(tot - R_HIP) / R_HIP < 1e-3 and abs(p0 / pm - 1.5) < 1e-9
        am = a * 1e3
        rs = [-25.0 + 0.5 * i for i in range(101)]
        ps = [p0 * math.sqrt(1 - (r / am) ** 2) if abs(r) < am else 0.0 for r in rs]
        fine = sorted(set([-25.0, 25.0] + [am * math.cos(math.pi * i / 48) for i in range(49)]))
        pf = [p0 * math.sqrt(max(0.0, 1 - (r / am) ** 2)) if abs(r) <= am else 0.0 for r in fine]
        o += axes(s, ax, [(v, f"{v:g}") for v in (-20, -10, 0, 10, 20)], [(v, f"{v:g}") for v in (0, 5, 10, 15)],
                  "r (mm) from the contact centre", "pressure p (MPa)" if k == 0 else None, xlab_dy=42, ylab_x=x0 - 50)
        xy = [(ax.X(r), ax.Y(v)) for r, v in zip(fine, pf)]
        o.append(f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in xy)}" fill="{red}" fill-opacity="0.13"/>')
        o.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in xy)}" fill="none" stroke="{red}" '
                 f'stroke-width="{s(H.PX["curve"]):.2f}" stroke-linejoin="round"/>')
        o.append(H.line(s, ax.X(-am), ax.Y(pm), ax.X(am), ax.Y(pm), O["dim"], "ref", H.DASH_REF))
        o.append(dot(s, ax.X(0), ax.Y(p0), red))
        o.append(H.label(s, (ax.x0 + ax.x1) / 2, 38, f'{name}: {it("a")} = {am:.0f} mm', "label", I["primary"], "middle",
                         'font-weight="bold"'))
        if k == 0:
            o.append(H.label(s, ax.X(0) + 8, ax.Y(p0) - 12, f'peak {it("p")}₀ = {p0:.1f} MPa', "label2"))
            o.append(lead(s, ax.X(-9), ax.Y(pm) - 2, ax.X(-14), ax.Y(5.2)))
            o.append(H.label(s, ax.X(-14), ax.Y(5.2) - 5, f"mean {pm:.1f} MPa (dashed)", "label2", I["secondary"],
                             "middle"))
        else:
            o.append(H.label(s, ax.X(0) + 12, ax.Y(p0) + 4, f'peak {it("p")}₀ = {p0:.1f} MPa', "label2"))
            o.append(H.label(s, ax.X(am) + 6, ax.Y(pm) + 4, f"mean {pm:.1f} MPa", "label2", I["secondary"]))
        for sg in (-1, 1):
            o.append(H.line(s, ax.X(sg * am), ax.y0 - 5, ax.X(sg * am), ax.y0 + 5, red, "ref"))
        o.append(H.label(s, ax.X(am) + 4, ax.y0 - 9, f'{it("a")}', "label2", I["primary"]))
        o.append(H.label(s, ax.X(-am) - 4, ax.y0 - 9, f'−{it("a")}', "label2", I["primary"], "end"))
        panels.append((ax.box, [[ax.X(r), ax.Y(v), f"r = {r:.2f} mm, p = {v:.2f} MPa"] for r, v in zip(rs, ps)]))
    o.append(H.label(s, 380, 334, f'Same joint force under both: {it("R")} = {R_HIP:.0f} N = ∫ {it("p")} 2π{it("r")} d{it("r")}'
                     f' over each patch. Peak = 1.5 × mean.', "label2", I["secondary"], "middle"))
    aria = ("Two computed Hertz pressure domes p = p0 times the square root of 1 minus (r over a) squared, on the same "
            f"axes (pressure 0 to 18 MPa against r from minus 25 to 25 mm), for the same joint force R = {R_HIP:.0f} N. "
            f"Left, congruent, contact radius 20 mm: a wide low dome, peak {p0_hertz(R_HIP, A_WIDE)/1e6:.1f} MPa, mean "
            f"{R_HIP/(math.pi*A_WIDE**2)/1e6:.1f} MPa. Right, incongruent, contact radius 7 mm: a narrow tall dome, "
            f"peak {p0_hertz(R_HIP, A_NARROW)/1e6:.1f} MPa, mean {R_HIP/(math.pi*A_NARROW**2)/1e6:.1f} MPa. The peak "
            "is 1.5 times the mean in both.")
    return finish(VB, aria, s, o, H.hover_attr(panels))


# ================================================================ sockets: shared drawing for #18 / #34 / #20
def socket_panel(s, p, which, win, d, k, beta, L, n_len, label_n=True):
    """Head in socket on art: (svg list, head centre, radius, axis deg). which = 'hip' (axis up into the acetabular
    roof) or 'sh' (axis medial, into the glenoid). win = source window (x0, y0, x1, y1), drawn at d with scale k."""
    pl = Place(win[:2], d, k)
    if which == "hip":
        img = pl.image("hip", win, p)
        c, r, ax = pl(HIP_C[:2]), HIP_C[2] * k, -90.0
    else:
        img = pl.image("shoulder", win, p)
        c, r, ax = pl(HUM_C[:2]), HUM_C[2] * k, 180.0
    o = [img, head_outline(s, c, r), cone(s, c, ax, beta, L)]
    tail, tip = pol(c, n_len, ax + 180), pol(c, r - s(4), ax)
    o.append(H.arrow(s, p, tail[0], tail[1], tip[0], tip[1], "reaction"))
    if label_n:
        q = pol(c, n_len * 0.62, ax + 180)
        o.append(H.label(s, q[0] + (10 if which == "hip" else 0), q[1] + (5 if which == "hip" else -10),
                         f'{it("N")}', "label", O["reaction"], "start" if which == "hip" else "middle"))
    o.append(H.joint_centre(s, *c))
    return o, c, r, ax


# ================================================================ svg #18  deep vs shallow socket
def fig18():
    p = "m3f18_"
    VB = (0, 0, 760, 452)
    s = H.Scale(VB[2], VB[3])
    blu = O["geometry"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(H.line(s, 380, 14, 380, 392, "#e6e6e6", "leader"))
    for x, t in ((190, "Hip — deep socket"), (570, "Shoulder — shallow socket")):
        o.append(H.label(s, x, 26, t, "label", I["primary"], "middle", 'font-weight="bold"'))
    # hip: axis up into the acetabular roof, beta = 55 deg
    k = 0.42
    Lh = 1.7 * HIP_C[2] * k
    q, c, r, ax = socket_panel(s, p, "hip", (300, 3640, 860, 4380), (72.0, 44.0), k, BETA_HIP, Lh, 76)
    o += q
    o.append(angle_arc(s, c, 34, ax, ax + BETA_HIP))
    m = pol(c, 46, ax + BETA_HIP / 2)
    o.append(H.label(s, m[0] + 2, m[1] + 4, "β", "label", blu, "start", 'font-style="italic"'))
    rim = pol(c, Lh, ax + BETA_HIP)
    o.append(H.label(s, rim[0] + 6, rim[1] + 4, "rim", "label2", blu))
    ac = pol(c, r + 6, ax - 40)
    o.append(lead(s, ac[0] - 3, ac[1] - 2, 70, 106))
    o.append(H.label(s, 8, 100, "acetabulum", "label2", I["secondary"]))
    fh = pol(c, r * 0.7, 150)
    o.append(lead(s, fh[0] - 3, fh[1], 64, 250))
    o.append(H.label(s, 60, 254, "femoral", "label2", I["secondary"], "end"))
    o.append(H.label(s, 60, 269, "head", "label2", I["secondary"], "end"))
    S_h = math.tan(math.radians(BETA_HIP))
    o.append(H.label(s, 190, 374, f"β ≈ {BETA_HIP:.0f}° · S = tan β ≈ {S_h:.2f}", "label", I["primary"], "middle"))
    o.append(H.label(s, 190, 392, "stable, limited range", "label2", I["secondary"], "middle"))
    # shoulder: axis medial (left) into the glenoid, beta = 22 deg
    q, c, r, ax = socket_panel(s, p, "sh", (660, 1430, 1240, 2040), (452.0, 60.0), k, BETA_SH, 118, 76)
    o += q
    o.append(angle_arc(s, c, 96, ax - BETA_SH, ax))
    m = pol(c, 108, ax - BETA_SH / 2)
    o.append(H.label(s, m[0] - 4, m[1] + 4, "β", "label", blu, "end", 'font-style="italic"'))
    g = pol(c, r, 180 + 30)
    o.append(lead(s, g[0] - 2, g[1] + 2, 430, 262))
    o.append(H.label(s, 426, 276, "glenoid", "label2", I["secondary"]))
    hh = pol(c, r * 0.6, -50)
    o.append(lead(s, hh[0] + 2, hh[1], 700, 82))
    o.append(H.label(s, 704, 86, "humeral", "label2", I["secondary"]))
    o.append(H.label(s, 704, 101, "head", "label2", I["secondary"]))
    S_s = math.tan(math.radians(BETA_SH))
    o.append(H.label(s, 570, 374, f"β ≈ {BETA_SH:.0f}° · S = tan β ≈ {S_s:.2f}", "label", I["primary"], "middle"))
    o.append(H.label(s, 570, 392, "mobile, easily dislocated", "label2", I["secondary"], "middle"))
    lines = wrap(credit_lynch("Left hip and left shoulder, front view; recoloured, cropped. Head outline (dashed), "
                              "stability cone (blue) and N drawn for this course; β is the text value, not measured "
                              "on the art."), 125)
    o.append(credits(s, VB, lines))
    aria = (f"Left, the hip (Lynch skeleton art): the acetabulum wraps over the femoral head; the compressive force N "
            f"presses the head up into the socket, and a blue stability cone of half-angle beta about {BETA_HIP:.0f} "
            f"degrees opens around it, so S = tan beta is about {S_h:.2f}: stable, limited range. Right, the shoulder: "
            f"the shallow glenoid holds only the medial side of the humeral head; the cone about N is narrow, beta "
            f"about {BETA_SH:.0f} degrees, so S is about {S_s:.2f}: mobile, easily dislocated.")
    return finish(VB, aria, s, o)


# ================================================================ svg #20  stability cone, animated (slider + Play)
PHI = list(range(0, 38, 2))            # deg, resultant tilt frames
PHI_DEF = PHI.index(14)


def fig20():
    p = "m3f20_"
    VB = (0, 0, 760, 392)
    s = H.Scale(VB[2], VB[3])
    blu = O["geometry"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    win = (650, 1420, 1300, 2100)
    pl = Place(win[:2], (252.0, 10.0), 0.48)
    o.append(pl.image("shoulder", win, p))
    c, r = pl(HUM_C[:2]), HUM_C[2] * pl.k
    Lc, Ln = 176.0, 112.0
    o.append(head_outline(s, c, r))
    o.append(cone(s, c, 180.0, BETA_SH, Lc))
    for sg in (-1, 1):
        q = pol(c, Lc + 6, 180 + sg * BETA_SH)
        o.append(H.label(s, q[0] - 4, q[1] + (14 if sg < 0 else -4), "rim", "label2", blu, "end"))
    o.append(angle_arc(s, c, 150, 180 - BETA_SH, 180))
    m = pol(c, 160, 180 - BETA_SH / 2)
    o.append(H.label(s, m[0] - 4, m[1] + 8, f"β = {BETA_SH:.0f}°", "label2", blu, "end"))
    o.append(H.joint_centre(s, *c))
    g = pol(c, r, 200)
    o.append(lead(s, g[0] - 2, g[1] + 2, 150, 268))
    o.append(H.label(s, 146, 272, "glenoid", "label2", I["secondary"], "end"))
    o.append(H.label(s, 146, 287, "(shallow socket)", "label2", I["secondary"], "end"))
    h = pol(c, r * 0.6, -40)
    o.append(lead(s, h[0] + 2, h[1], 584, 40))
    o.append(H.label(s, 588, 44, "humeral head", "label2", I["secondary"]))
    frames = []
    for k, ph in enumerate(PHI):
        t = math.tan(math.radians(ph))
        Nt = pol(c, Ln, 180.0)
        Ft = (Nt[0], Nt[1] + Ln * t)
        g = [H.arrow(s, p, c[0], c[1], Nt[0], Nt[1], "dim", w="geom")]
        if ph:
            g.append(H.arrow(s, p, Nt[0], Nt[1], Ft[0], Ft[1], "load", w="geom"))
            g.append(H.label(s, Ft[0] - 8, (Nt[1] + Ft[1]) / 2 + 6, f'{it("F")}ₜ', "label", O["load"], "end"))
            g.append(angle_arc(s, c, 70, 180 - ph, 180, I["primary"]))
        g.append(H.label(s, Nt[0] + 22, Nt[1] - 8, f'{it("N")}', "label", I["secondary"]))
        g.append(H.arrow(s, p, c[0], c[1], Ft[0], Ft[1], "reaction"))
        inside = ph < BETA_SH
        lines = [f"tilt φ = {ph}°", f"{it('F')}ₜ/{it('N')} = tan φ = {t:.2f}"]
        tx = 590
        for i, txt in enumerate(lines):
            g.append(H.label(s, tx, 112 + 20 * i, txt, "label2", I["primary"]))
        if inside:
            g.append(H.label(s, tx, 192, "φ < β: inside the cone,", "label2", I["primary"]))
            g.append(H.label(s, tx, 209, "the head stays seated", "label2", I["primary"]))
        else:
            gc = (c[0] - 0.30 * r, c[1] + 0.62 * r)
            g.append(f'<circle cx="{gc[0]:.2f}" cy="{gc[1]:.2f}" r="{r:.2f}" fill="none" stroke="{O["flag"]}" '
                     f'stroke-width="{s(2.2):.2f}" stroke-dasharray="{s(6):.1f} {s(4):.1f}"/>')
            g.append(f'<rect x="{tx}" y="{184 - s(5):.1f}" width="{s(16):.1f}" height="{s(4):.1f}" fill="{O["flag"]}"/>')
            g.append(H.label(s, tx + 22, 186, "φ > β: past the rim,", "label2", I["primary"]))
            g.append(H.label(s, tx, 203, "the head rides over it", "label2", I["primary"]))
            g.append(H.label(s, tx, 220, "and dislocates", "label2", I["primary"]))
        frames.append(H.frame(k, PHI_DEF, "".join(g)))
    o += frames
    o.append(H.label(s, tx, 152, f"rim: β = {BETA_SH:.0f}°, tan β = {math.tan(math.radians(BETA_SH)):.2f}", "label2",
                     I["primary"]))
    o.append(H.label(s, tx, 262, f'φ = arctan({it("F")}ₜ/{it("N")})', "label2", I["secondary"]))
    o.append(H.label(s, tx, 279, "black: resultant of N and Fₜ", "label2", I["secondary"]))
    lines = wrap(credit_lynch("Left shoulder, front view; recoloured, cropped. Cone, forces and the displaced head "
                              "(orange, dashed) drawn for this course; β = 22° is the text value (§6.2)."), 125)
    o.append(credits(s, VB, lines))
    aria = ("Animation with a slider: the left shoulder in front view (Lynch skeleton art), the humeral head against "
            "the shallow glenoid. A blue stability cone of half-angle beta = 22 degrees opens medially from the head "
            "centre. A compressive force N presses the head into the glenoid and a growing sideways force F t tilts "
            "their black resultant by phi = arctan(F t over N), from 0 to 36 degrees. While phi is below beta the "
            "resultant stays inside the cone and the head stays seated; past 22 degrees it points beyond the rim and "
            "an orange dashed outline shows the head riding over the rim and dislocating. The still frame shows "
            "phi = 14 degrees.")
    vals = [f"{v}°" for v in PHI]
    return finish(VB, aria, s, o, H.frames_attr("tilt φ", vals, PHI_DEF))


# ================================================================ svg #31  C4 hinge vs saddle in one hand
def fig31():
    p = "m3f31_"
    VB = (0, 0, 400, 330)
    s = H.Scale(VB[2], VB[3], display_w=400)
    blu = O["geometry"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    hp = Place((1390.0, 4160.0), (10.0, 6.0), 0.272)
    o.append(hp.image("hand", (1390, 4160, 2170, 5240), p))
    j = hp(HAND["pip"])
    a = deg(hp(HAND["pip_ax"][0]), hp(HAND["pip_ax"][1]))
    o.append(axis_line(s, j, a + 90, 26))
    o.append(ell(s, p, j[0], j[1], 22, 7, a, 200, 480))
    o.append(lead(s, j[0] + 18, j[1] + 4, 268, 252, I["secondary"]))
    o.append(H.label(s, 272, 250, "hinge (PIP): 1 DOF", "label2", I["primary"]))
    o.append(H.label(s, 272, 266, "one rotation", "label2", blu))
    j = hp(HAND["cmc"])
    a = deg(hp(HAND["cmc_ax"][0]), hp(HAND["cmc_ax"][1]))
    o.append(axis_dot(s, j))
    o.append(arc(s, p, j[0], j[1], 44, a - 26, a + 24, both=True))
    o.append(axis_line(s, pol(j, 8, a), a + 90, 30))
    o.append(ell(s, p, *pol(j, 8, a), 26, 7, a, 200, 480))
    o.append(lead(s, j[0] + 20, j[1] - 22, 268, 40, I["secondary"]))
    o.append(H.label(s, 272, 38, "saddle (thumb CMC):", "label2", I["primary"]))
    o.append(H.label(s, 272, 54, "2 DOF", "label2", I["primary"]))
    o.append(H.label(s, 272, 70, "two rotations", "label2", blu))
    lines = wrap(credit_lynch("Left hand, palm forward; recoloured, cropped. Arrows drawn for this course."), 72)
    o.append(credits(s, VB, lines))
    aria = ("Problem C4 setup: the bones of a left hand, palm forward (Lynch skeleton art). At the index finger's middle "
            "joint (proximal interphalangeal, a hinge) one blue arrow turns about one axis: 1 DOF. At the thumb base "
            "(carpometacarpal, a saddle) two blue arrows turn about two different axes: 2 DOF.")
    return finish(VB, aria, s, o)


# ================================================================ svg #32  C5 constraint force normal, motion tangent
def fig32():
    p = "m3f32_"
    VB = (0, 0, 400, 336)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    win = (300, 3700, 860, 4250)
    pl = Place(win[:2], (16.0, 36.0), 0.46)
    o.append(pl.image("hip", win, p))
    c, r = pl(HIP_C[:2]), HIP_C[2] * pl.k
    o.append(head_outline(s, c, r))
    o.append(H.joint_centre(s, *c))
    Tp = pol(c, r, -90)
    o.append(H.arrow(s, p, Tp[0], Tp[1], Tp[0], Tp[1] + 44, "reaction"))
    o.append(H.arrow(s, p, Tp[0] - 62, Tp[1], Tp[0] + 62, Tp[1], DOF, both=True))
    q = 8
    o.append(f'<path d="M{Tp[0] + q:.2f},{Tp[1]:.2f} l0,{q:.2f} l{-q:.2f},0" fill="none" stroke="{I["primary"]}" '
             f'stroke-width="{s(1.1):.2f}"/>')
    lx = 286
    o.append(lead(s, Tp[0] + 4, Tp[1] + 30, lx - 4, Tp[1] + 30, I["secondary"]))
    o.append(H.label(s, lx, Tp[1] + 35, f'{it("J")}{H.sub("c", s)}ᵀλ', "label", O["reaction"]))
    o.append(H.label(s, lx, Tp[1] + 52, "constraint force,", "label2", I["primary"]))
    o.append(H.label(s, lx, Tp[1] + 67, "along the normal", "label2", I["primary"]))
    o.append(H.label(s, lx, Tp[1] - 16, "allowed slide,", "label2", O["geometry"]))
    o.append(H.label(s, lx, Tp[1] - 1, "along the tangent", "label2", O["geometry"]))
    o.append(H.label(s, 200, 22, "force ⊥ motion → no work", "label", I["primary"], "middle"))
    fh = pol(c, r * 0.5, 30)
    o.append(lead(s, fh[0] + 3, fh[1], lx - 4, c[1] + 54, I["secondary"]))
    o.append(H.label(s, lx, c[1] + 58, "femoral head", "label2", I["secondary"]))
    o.append(H.label(s, lx, c[1] + 73, "(dashed outline)", "label2", I["secondary"]))
    lines = wrap(credit_lynch("Left hip, front view; recoloured, cropped. Vectors drawn for this course."), 72)
    o.append(credits(s, VB, lines))
    aria = ("Problem C5 setup: the femoral head in the acetabulum (Lynch skeleton art). At the contact on the "
            "acetabular roof the constraint force J c transpose lambda points along the surface normal, into the head "
            "towards its centre; the allowed sliding motion runs along the tangent, left and right. A right-angle mark "
            "shows the two are perpendicular: force perpendicular to motion, so no work.")
    return finish(VB, aria, s, o)


# ================================================================ svg #33  C6 ideal hinge vs rolling-gliding knee
def fig33():
    p = "m3f33_"
    VB = (0, 0, 400, 318)
    s = H.Scale(VB[2], VB[3], display_w=400)
    blu = O["geometry"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    b = (6.0, 22.0, 180.0, 188.0)
    img, ins = elbow_image(p, (b[0] + 84, b[1] + 82), 0.80, b)
    o.append(img)
    tc = ins.M(ins.tc[:2])
    a_f = deg(ins.M(DB["rad_axis"][0]), ins.M(DB["rad_axis"][1]))
    o.append(H.joint_centre(s, *tc))
    o.append(arc(s, p, tc[0], tc[1], 72, a_f - 34, a_f + 20, both=True))
    o.append(H.label(s, 96, 236, "ideal hinge:", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, 96, 252, "one fixed axis (the pin)", "label2", I["primary"], "middle", 'font-style="italic"'))
    # knee: two centres of curvature of the femoral condyle (distal = extension, posterior = flexion)
    kp = Place((138.0, 168.0), (210.0, 22.0), 1.18)
    o.append(kp.image("knee", (138, 168, 290, 328), p))
    cd, cp = kp(KNEE["distal"][:2]), kp(KNEE["post"][:2])
    ratio = KNEE["distal"][2] / KNEE["post"][2]
    for q in (cd, cp):
        o.append(f'<circle cx="{q[0]:.2f}" cy="{q[1]:.2f}" r="{s(4):.2f}" fill="{O["flag"]}" stroke="#fff" '
                 f'stroke-width="{s(1.2):.2f}"/>')
    o.append(f'<path d="M{cd[0]:.2f},{cd[1]:.2f} Q{cd[0] - 30:.2f},{(cd[1] + cp[1]) / 2:.2f} {cp[0]:.2f},{cp[1]:.2f}" '
             f'fill="none" stroke="{O["flag"]}" stroke-width="{s(1.6):.2f}" stroke-dasharray="{s(4):.1f} {s(3):.1f}" '
             f'marker-end="url(#{p}a_flag)"/>')
    o.append(H.label(s, cd[0] + 8, cd[1] + 4, "centres of", "label2", I["primary"]))
    o.append(H.label(s, cd[0] + 8, cd[1] + 19, "curvature", "label2", I["primary"]))
    o.append(arc(s, p, cp[0], cp[1], 34, 100, 160))
    o.append(H.label(s, cp[0] - 40, cp[1] + 40, "roll", "label2", blu, "end"))
    x0c, x1c, yc = KNEE["contact"]
    g0, g1 = kp((x0c - 8, yc + 1)), kp((x1c + 14, yc + 1))
    o.append(H.arrow(s, p, g0[0], g0[1] + 8, g1[0], g1[1] + 8, DOF))
    o.append(H.label(s, g1[0] + 4, g1[1] + 20, "glide", "label2", blu))
    o.append(H.label(s, 300, 236, "real knee: rolls and glides,", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, 300, 252, "so the axis migrates", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, 300, 268, f"(radius {ratio:.1f}× smaller behind)", "label2", I["secondary"], "middle"))
    lines = wrap("Art: DBCLS, “" + ELBOW_T + "” and “" + KNEE_T + "”, CC BY 4.0, via Wikimedia Commons. Recoloured, "
                 "cropped; overlays drawn for this course.", 72)
    o.append(credits(s, VB, lines))
    aria = ("Problem C6 setup. Left: a sagittal section of the elbow (DBCLS art) with a blue arrow turning the forearm "
            "about one fixed pin at the trochlea centre: the ideal hinge. Right: a sagittal section of the knee (DBCLS "
            "art). The femoral condyle rolls (blue curved arrow) and glides (blue straight arrow) on the tibial plateau; "
            "two orange dots mark the centres of curvature of the condyle outline, distal and posterior, whose radii "
            f"differ by {ratio:.1f} times, and a dashed orange arrow shows the axis migrating between them.")
    return finish(VB, aria, s, o)


# ================================================================ svg #34  C7 the same ball, two sockets
def fig34():
    p = "m3f34_"
    VB = (0, 0, 400, 300)
    s = H.Scale(VB[2], VB[3], display_w=400)
    blu = O["geometry"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    k = 0.32
    q, c, r, ax = socket_panel(s, p, "hip", (330, 3700, 820, 4300), (18.0, 36.0), k, BETA_HIP, 1.6 * HIP_C[2] * k,
                               50, label_n=False)
    o += q
    o.append(angle_arc(s, c, 24, ax, ax + BETA_HIP))
    m = pol(c, 34, ax + BETA_HIP / 2)
    o.append(H.label(s, m[0] + 2, m[1] + 4, "β", "label", blu, "start", 'font-style="italic"'))
    o.append(H.label(s, 96, 22, "hip: deep socket", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, 96, 248, "large β → stable", "label2", I["primary"], "middle"))
    q, c, r, ax = socket_panel(s, p, "sh", (680, 1450, 1230, 2050), (212.0, 36.0), k, BETA_SH, 86, 50, label_n=False)
    o += q
    o.append(angle_arc(s, c, 70, ax - BETA_SH, ax))
    m = pol(c, 80, ax - BETA_SH / 2)
    o.append(H.label(s, m[0] - 2, m[1] + 4, "β", "label", blu, "end", 'font-style="italic"'))
    o.append(H.label(s, 300, 22, "shoulder: shallow socket", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, 300, 248, "small β → loose", "label2", I["primary"], "middle"))
    lines = wrap(credit_lynch("Recoloured, cropped. Cones and N (black) drawn for this course."), 72)
    o.append(credits(s, VB, lines))
    aria = ("Problem C7 setup: two ball-and-socket joints with heads of the same size (Lynch skeleton art, front view). "
            "Left, the hip: the acetabulum wraps over the femoral head and the blue stability cone about the "
            "compressive force N has a large rim angle beta. Right, the shoulder: the shallow glenoid gives a narrow "
            "cone with a small beta.")
    return finish(VB, aria, s, o)


# ================================================================ svg #36  C9 same force, small vs large contact
def fig36():
    p = "m3f36_"
    VB = (0, 0, 400, 340)
    s = H.Scale(VB[2], VB[3], display_w=400)
    A_s, A_l = A_HIP / 2, A_HIP                  # "twice the contact area" (line 1919); the hip's 10 cm2 (line 963)
    p_s, p_l = R_HIP / A_s / 1e6, R_HIP / A_l / 1e6
    assert abs(p_l - 1.715) < 1e-3 and abs(p_s / p_l - 2) < 1e-9
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # incongruent: knee condyle on the plateau, small patch
    kp = Place((140.0, 170.0), (14.0, 50.0), 1.12)
    o.append(kp.image("knee", (140, 170, 292, 322), p))
    x0c, x1c, yc = KNEE["contact"]
    c0, c1 = kp((x0c, yc)), kp((x1c, yc))
    o.append(H.line(s, c0[0], c0[1], c1[0], c1[1], O["flag"], "force", extra='stroke-linecap="round"'))
    top = kp((168.0, 172.0))
    o.append(H.arrow(s, p, top[0], top[1] - 24, top[0], top[1] + 8, "load"))
    o.append(H.label(s, top[0] + 8, top[1] - 6, f'{it("F")}', "label", O["load"]))
    o.append(H.label(s, 96, 240, "incongruent: small area A", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, 96, 256, f"p = F/A ≈ {p_s:.1f} MPa (high)", "label2", I["primary"], "middle"))
    # congruent: femoral head in the acetabulum, the patch spans the roof
    win = (330, 3700, 820, 4300)
    pl = Place(win[:2], (222.0, 34.0), 0.33)
    o.append(pl.image("hip", win, p))
    c, r = pl(HIP_C[:2]), HIP_C[2] * pl.k
    o.append(head_outline(s, c, r))
    cov = [pol(c, r + s(2.5), -90 + 45 * (i / 10 - 1)) for i in range(21)]
    o.append(f'<path d="M{" L".join(f"{x:.2f},{y:.2f}" for x, y in cov)}" fill="none" stroke="{O["flag"]}" '
             f'stroke-width="{s(4):.2f}" stroke-linecap="round"/>')
    tp = pol(c, r + 30, -90)
    o.append(H.arrow(s, p, tp[0], tp[1] - 30, tp[0], tp[1] + 6, "load"))
    o.append(H.label(s, tp[0] + 8, tp[1] - 12, f'{it("F")}', "label", O["load"]))
    o.append(H.label(s, 304, 240, "congruent: area 2A", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, 304, 256, f"p = F/2A ≈ {p_l:.1f} MPa (low)", "label2", I["primary"], "middle"))
    o.append(H.label(s, 200, 22, f"same F = {R_HIP:.0f} N; A = {A_s*1e4:.0f} cm² vs 2A = {A_l*1e4:.0f} cm²", "label2",
                     I["secondary"], "middle"))
    lines = wrap("Art: DBCLS, “" + KNEE_T + "”, CC BY 4.0; Patrick J. Lynch, medical illustrator, “Skeleton whole body ant lat views.svg”, "
                 "CC BY 2.5; via Wikimedia Commons. Recoloured, cropped. Contact patches (orange) drawn for this course.", 72)
    o.append(credits(s, VB, lines))
    aria = (f"Problem C9 setup: the same force F = {R_HIP:.0f} N on two joints. Left, an incongruent contact: the knee's "
            f"rounded femoral condyle on the flatter tibial plateau (DBCLS art) touches over a small orange patch of area "
            f"A = {A_s*1e4:.0f} square cm, so the mean pressure F over A is about {p_s:.1f} MPa. Right, a congruent "
            f"contact: the femoral head in the acetabulum (Lynch art) shares the load over an orange patch twice as large, "
            f"{A_l*1e4:.0f} square cm, so the pressure is about {p_l:.1f} MPa.")
    return finish(VB, aria, s, o)


# ================================================================ svg #37  C10 two muscles span one joint
def fig37():
    """Same arm art and construction as m05 svg #50 (co-contraction), with the joint reaction added."""
    p = "m3f37_"
    K = 9.0
    Ec = (150.0, 318.0)
    VB = (0, 0, 440, 508)
    s = H.Scale(VB[2], VB[3], display_w=400)
    A = Arm(p, s, Ec, K, r_ins=3.0)
    red = O["force"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    tri, tbez, twidth = A.belly(ARM["tri"], ARM["tri_half_w"], T["muscle_dk"][1])
    Ti, TB = A.C(ARM["tri_ins"]), A.C(ARM["tri"][2])
    o.append(A.bones(hand=False))
    o.append(A.tendon(TB, Ti, 2.4) + tri)
    bic, bez, width = A.biceps()
    o.append(bic)
    o.append(f'<circle cx="{Ti[0]:.1f}" cy="{Ti[1]:.1f}" r="{s(2.8):.2f}" fill="{red}" stroke="#fff" stroke-width="{s(1):.2f}"/>')
    for a, b, sym, side in ((A.B, A.I, "flex", 1), (TB, Ti, "ext", -1)):
        ux, uy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(ux, uy)
        S0 = (b[0] + side * 8, b[1] - 4)
        o.append(H.arrow(s, p, S0[0], S0[1], S0[0] - ux / L * 52, S0[1] - uy / L * 52, "force"))
        o.append(H.label(s, S0[0] + side * 6, S0[1] - 40, f'{it("F")}{H.sub(sym, s)}', fill=red,
                         anchor="start" if side > 0 else "end"))
    # the joint reaction on the forearm: both muscles pull it up, the humerus pushes back down
    o.append(H.arrow(s, p, Ec[0], Ec[1] + 6, Ec[0], Ec[1] + 74, "reaction"))
    o.append(H.label(s, Ec[0] + 10, Ec[1] + 64, f'{it("R")} (joint reaction)', "label", O["reaction"]))
    o.append(H.joint_centre(s, Ec[0], Ec[1]))
    bx, by, bnx, bny = bez(0.5)
    e = (bx + abs(bnx) * width(0.5), by)
    o.append(H.line(s, e[0] + 2, e[1], 214, e[1] - 6, T["muscle"][1]))
    o.append(H.label(s, 218, e[1] - 8, "flexor (biceps)", "label2", I["primary"]))
    o.append(H.label(s, 218, e[1] + 8, "in front of the joint", "label2", I["secondary"]))
    tbx, tby, tnx, tny = tbez(0.5)
    te = (tbx - abs(tnx) * twidth(0.5), tby)
    lx = te[0] - 16
    o.append(H.line(s, te[0] - 2, te[1], lx + 4, te[1] - 6, T["muscle"][1]))
    o.append(H.label(s, lx, te[1] - 8, "extensor", "label2", I["primary"], "end"))
    o.append(H.label(s, lx, te[1] + 8, "(triceps)", "label2", I["primary"], "end"))
    o.append(H.label(s, lx, te[1] + 24, "behind", "label2", I["secondary"], "end"))
    o.append(H.label(s, 12, 424, "Both pull at once (co-contraction): the net torque", "label2", I["primary"]))
    o.append(H.label(s, 12, 441, f'can stay the same while {it("R")} grows.', "label2", I["primary"]))
    lines = wrap(credit_nih("Recoloured; reposed. Muscles and overlays drawn for this course. Arrows are not to "
                            "force scale."), 70)
    o.append(credits(s, VB, lines))
    aria = ("Problem C10 setup: side view of an upper arm and forearm (NIH arm-bone art, the same construction as the "
            "Module 5 co-contraction figure), elbow at 90 degrees. A flexor (biceps) in front of the humerus and an "
            "extensor (triceps) behind it both pull, with forces F flex on the radius and F ext on the olecranon. Both "
            "pull the forearm up against the humerus, so the joint reaction R on the forearm points down, and it grows "
            "with both muscle forces while the net torque can stay the same.")
    return finish(VB, aria, s, o)


# ================================================================ svg #44  D7 Hertz contact (schematic)
def fig44():
    p = "m3f44_"
    VB = (0, 0, 400, 334)
    s = H.Scale(VB[2], VB[3], display_w=400)
    R, a, ys = 64.0, 30.0, 190.0                 # drawn radius, half-width (exaggerated), surface level
    cy = ys - math.sqrt(R * R - a * a)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(f'<rect x="60" y="{ys:.1f}" width="280" height="22" fill="{T["cartilage"][0]}" stroke="{T["cartilage"][1]}" '
             f'stroke-width="{s(1):.2f}"/>')
    o.append(f'<rect x="60" y="{ys + 22:.1f}" width="280" height="14" fill="{T["bone"][0]}" stroke="{T["bone"][1]}" '
             f'stroke-width="{s(1):.2f}"/>')
    th = math.degrees(math.asin(a / R))
    l0, l1 = pol((200, cy), R, 90 + th), pol((200, cy), R, 90 - th)
    o.append(f'<path d="M{l1[0]:.2f},{l1[1]:.2f} A{R},{R} 0 1 0 {l0[0]:.2f},{l0[1]:.2f} Z" fill="{T["bone"][0]}" '
             f'stroke="{T["bone"][1]}" stroke-width="{s(1.2):.2f}"/>')
    o.append(H.arrow(s, p, 200, cy - R - 44, 200, cy - R - 4, "load"))
    o.append(H.label(s, 210, cy - R - 20, f'{it("F")}', "label", O["load"]))
    q = pol((200, cy), R, -140)
    o.append(H.arrow(s, p, 200, cy, q[0], q[1], "dim", w="ref"))
    o.append(H.label(s, (200 + q[0]) / 2 - 8, (cy + q[1]) / 2 + 2, f'{it("R")}', "label", I["primary"], "end"))
    o.append(dot(s, 200, cy, I["primary"], r=2.5))
    o.append(H.label(s, 330, ys + 16, f'elastic layer, {it("E")}*', "label2", I["secondary"], "end"))
    # the pressure the layer feels: p(r) = p0 sqrt(1 - (r/a)^2) on |r| < a (shape only)
    yb, hp_ = 284.0, 34.0
    xs = [200 - a + 2 * a * i / 80 for i in range(81)]
    pts = [(x, yb - hp_ * math.sqrt(max(0.0, 1 - ((x - 200) / a) ** 2))) for x in xs]
    o.append(H.line(s, 120, yb, 280, yb, I["axis"], "axis"))
    o.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="none" stroke="{H.SERIES[0]}" '
             f'stroke-width="{s(H.PX["curve"]):.2f}" stroke-linejoin="round"/>')
    for x in (200 - a, 200 + a):
        o.append(H.line(s, x, ys + 2, x, yb + 10, O["dim"], "leader", H.DASH_REF))
    o.append(H.arrow(s, p, 200 - a, yb + 16, 200 + a, yb + 16, "geometry", both=True))
    o.append(H.label(s, 200, yb + 34, f'2{it("a")}', "label", O["geometry"], "middle"))
    o.append(H.line(s, 200, yb - hp_ - 2, 200 + a + 12, yb - hp_ - 10, I["secondary"], "leader"))
    o.append(H.label(s, 200 + a + 16, yb - hp_ - 6, f'{it("p")}₀ at the centre', "label2", I["primary"]))
    o.append(H.label(s, 116, yb - 4, f'{it("p")}({it("r")})', "label2", I["secondary"], "end"))
    o.append(H.label(s, 390, 326, "patch width exaggerated", "label2", I["muted"], "end"))
    aria = ("Problem D7 setup (schematic): a sphere of radius R pressed by a force F onto a flat elastic layer of "
            "effective modulus E star flattens to a contact patch of width 2a. Below, the pressure the layer feels "
            "across the patch is a dome, p0 times the square root of 1 minus (r over a) squared, peaking at p0 in the "
            "centre and falling to zero at the edges.")
    return finish(VB, aria, s, o)


# ================================================================ svg #45  D8 climbing the rim
def fig45():
    p = "m3f45_"
    VB = (0, 0, 400, 352)
    s = H.Scale(VB[2], VB[3], display_w=400)
    blu = O["geometry"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    win = (300, 3700, 860, 4280)
    pl = Place(win[:2], (20.0, 22.0), 0.46)
    o.append(pl.image("hip", win, p))
    c, r = pl(HIP_C[:2]), HIP_C[2] * pl.k
    o.append(head_outline(s, c, r))
    o.append(H.line(s, c[0], c[1] + r + 6, c[0], c[1] - r - 26, O["dim"], "ref", H.DASH_REF))
    o.append(H.label(s, c[0] + 6, c[1] - r - 16, "socket axis", "label2", I["secondary"]))
    rim = pol(c, r, -90 + BETA_HIP)
    o.append(H.line(s, c[0], c[1], rim[0], rim[1], blu, "ref", H.DASH_REF))
    o.append(angle_arc(s, c, 36, -90, -90 + BETA_HIP))
    m = pol(c, 48, -90 + BETA_HIP / 2)
    o.append(H.label(s, m[0] + 2, m[1] + 4, "β", "label", blu, "start", 'font-style="italic"'))
    tng = (math.cos(math.radians(BETA_HIP)), math.sin(math.radians(BETA_HIP)))   # rim tangent, up the wall
    o.append(H.line(s, rim[0] - tng[0] * 30, rim[1] - tng[1] * 30, rim[0] + tng[0] * 30, rim[1] + tng[1] * 30,
                    O["dim"], "ref"))
    o.append(f'<circle cx="{rim[0]:.2f}" cy="{rim[1]:.2f}" r="{s(3.5):.2f}" fill="{blu}" stroke="#fff" '
             f'stroke-width="{s(1.2):.2f}"/>')
    o.append(H.label(s, rim[0] + 10, rim[1] - 8, "rim", "label2", blu))
    o.append(H.arrow(s, p, c[0], c[1] + 78, c[0], c[1] + 6, "reaction"))
    o.append(H.label(s, c[0] - 8, c[1] + 62, f'{it("N")}', "label", O["reaction"], "end"))
    o.append(H.arrow(s, p, c[0] + 6, c[1], c[0] + 72, c[1], "load"))
    o.append(H.label(s, c[0] + 76, c[1] + 5, f'{it("F")}ₜ', "label", O["load"]))
    o.append(H.joint_centre(s, *c))
    o.append(H.label(s, 200, 302, f'dislocate when {it("F")}ₜ = {it("N")} tan β', "label", I["primary"], "middle",
                     'font-style="italic"'))
    lines = wrap(credit_lynch("Left hip, front view; recoloured, cropped. Overlays drawn for this course."), 72)
    o.append(credits(s, VB, lines))
    aria = ("Problem D8 setup: the femoral head in its socket (Lynch skeleton art, left hip). A compressive force N acts "
            "along the socket axis, pressing the head into the socket, and a sideways force F t pushes it towards the "
            "rim. A dashed blue line from the head centre to the rim makes the angle beta with the axis; the rim "
            "surface is drawn as a short tangent line there. The head dislocates when F t = N tan beta.")
    return finish(VB, aria, s, o)


FIGS = {
    1: ("Left: hip ball-and-socket with deep acetabulum. Right: sagit", fig1),
    2: ("The knee as a one-axis hinge with a single flexion-extension", fig2),
    6: ("A grid of the six synovial joint types: hinge and pivot each", fig6),
    8: ("An anatomical hand skeleton showing four joint types: the ca", fig8),
    15: ("Two pressure domes: a congruent joint spreads the load over ", fig15),
    18: ("Left: the hip, a deep socket wrapping more than half the fem", fig18),
    20: ("Animation: in a shallow socket, a tilting joint-force result", fig20),
    31: ("A shaded hand. The index finger's middle joint is a hinge wi", fig31),
    32: ("A ball resting in a socket. At the contact the constraint fo", fig32),
    33: ("Left: an ideal hinge turning about one fixed pin. Right: a f", fig33),
    34: ("Two ball-and-socket joints with the same head. The hip's dee", fig34),
    36: ("The same downward force F pressed onto two joints. Left, an ", fig36),
    37: ("An elbow joint spanned by two muscles, a flexor in front and", fig37),
    44: ("A sphere pressed onto a curved surface under a force F, flat", fig44),
    45: ("A head in a socket: a compressive force N along the axis, a ", fig45),
}
