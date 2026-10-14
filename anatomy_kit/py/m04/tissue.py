"""Module 4, group `tissue`: cartilage, joint and schematic figures in the house style.

Main text (760 px): svg 1 (Fig. 1 osteochondral unit), 2 (Fig. 2 synovial joint), 4 (Fig. 3 microstructure),
5 (Fig. 4 Donnan), 7 (Fig. 6 confined compression), 8 (Fig. 7 effective stress), 12 (Fig. 11 loaded plug,
slider + Play), 13 (Fig. 12 finite-difference grid), 17 (Fig. 15 condyle on plateau), 19 (Fig. 17 lubrication
regimes), 24 (Fig. 20 osteoarthritis loop), 27 (Fig. 23 hub).
Every number is computed here from a value module04.html states (line numbers beside each constant).
Art: DBCLS "202108 Sagittal section through knee joint" (CC BY 4.0), cropped once by crop_art.py and put on the
page once (SHARED_DEFS); svg 1, 2 and 17 <use> it.
"""
import html
import math
import re

import house as H
from m05.body import _read, art_image, finish, inner_svg, wrap
from m05.schematic import box as sbox
from m05.tissue import ca_arrow as fluid_arrow
from m05.tissue import ca_marker as fluid_marker
from m05.tissue import circ, ellipse, legend, path, rect, sw_dot, sw_line, sw_rect

T, O, I = H.TISSUE, H.OVERLAY, H.INK
BOX, GRID = "#f7f4ef", "#e6e6e6"
SOLID = T["bone"][1]                                  # solid-matrix spring and share bar

# ---------------------------------------------------------------- constants the module states (module04.html line)
H_M, HA, K_PERM = 2e-3, 0.6e6, 1e-15                 # 604-606: h, aggregate modulus, permeability
D = HA * K_PERM                                      # 607: 6e-10 m^2/s
TAU = H_M ** 2 / D                                   # 608: 6667 s
C0, CF = 0.15, 0.20                                  # 302, 367 (M)
RG, THETA = 8.314, 310.0                             # 363, 367
R_JOINT, AC_CM2 = 1715.0, 10.0                       # 105, 940
R_EFF, E_INST, NU = 0.030, 10e6, 0.5                 # 941, 942
MU_EQ = 0.15                                         # 1076 (= mu_bl, 1036)
MU_BL, S0, ALPHA = 0.15, 0.5, 0.012                  # 1067
N_LAB, R_LAB = 50, 0.4                               # 774, 776
E_STAR = E_INST / (2 * (1 - NU ** 2))                # 908: 6.67 MPa
A_C = (3 * R_JOINT * R_EFF / (4 * E_STAR)) ** (1 / 3)   # 911: 18 mm
P0_HERTZ = 3 * R_JOINT / (2 * math.pi * A_C ** 2)    # 911, 947: 2.5 MPa
P_BIPH = 2 * R_JOINT / (math.pi * (1.3 * A_C) ** 2)  # 968: 2.0 MPa
P0_OA = 3 * R_JOINT / (2 * math.pi * 0.016 ** 2)     # 1293: 3.2 MPa


def lam(n):
    return (2 * n + 1) * math.pi / 2


def F_T(T_, n=1500):
    """Fluid load support, section 4 eq. (1), line 635."""
    return sum(2 / lam(i) ** 2 * math.exp(-lam(i) ** 2 * T_) for i in range(n))


def p_ZT(Z, T_, n=400):
    """Terzaghi pore pressure p / sigma0, Proposition 3.1 (line 560)."""
    if T_ <= 0:
        return 1.0 if Z < 1 else 0.0
    return sum(2 * (-1) ** i / lam(i) * math.cos(lam(i) * Z) * math.exp(-lam(i) ** 2 * T_) for i in range(n))


def F_t(t, k=K_PERM):
    return F_T(HA * k * t / H_M ** 2)


PI_SW = RG * THETA * (math.sqrt((CF * 1e3) ** 2 + 4 * (C0 * 1e3) ** 2) - 2 * C0 * 1e3)   # 362, 369: Pa
CP = 0.5 * (CF + math.sqrt(CF ** 2 + 4 * C0 ** 2))   # 352: c+ (M)
CM = CP - CF                                          # 341
F1 = F_t(1.0)                                         # 670: 0.986
F1_OA = F_t(1.0, 1000 * K_PERM)                       # 1276, 1315: k x 1000
MU_FOOT, MU_OA = MU_EQ * (1 - F1), MU_EQ * (1 - F1_OA)   # 1061, 1305
MU_MIN = min(MU_BL / (1 + (10 ** (-4 + 5 * i / 2999) / S0) ** 2) + ALPHA * 10 ** (-4 + 5 * i / 2999) for i in range(3000))
assert abs(TAU - 6667) < 1 and abs(PI_SW / 1e6 - 0.156) < 0.001 and abs(F1 - 0.986) < 0.0005
assert abs(A_C * 1e3 - 18) < 0.1 and abs(A_C / H_M - 9) < 0.05 and abs(P0_HERTZ / 1e6 - 2.54) < 0.01
assert abs(P_BIPH / 1e6 - 2.0) < 0.02 and abs(P0_OA / 1e6 - 3.2) < 0.01 and abs(1 - F1_OA - 0.4369) < 0.0005
assert abs(MU_FOOT - 0.0021) < 0.0001 and abs(MU_MIN - 0.032) < 0.001 and abs(CP - 0.280) < 0.001


def it(t):
    return f'<tspan font-style="italic">{t}</tspan>'


def sup(t, s, size="label"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size]*0.7):.2f}">{t}</tspan>'


def esc(t):
    return html.escape(t)


def dpath(pts, close=False):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + (" Z" if close else "")


def lead(s, x1, y1, x2, y2, col=None):
    """Leader with a dot on the thing it names."""
    return (f'<circle cx="{x1:.1f}" cy="{y1:.1f}" r="{s(2.5):.1f}" fill="{I["primary"]}"/>'
            + H.line(s, x1, y1, x2, y2, col or I["secondary"], "leader"))


# ---------------------------------------------------------------- the knee art (DBCLS, CC BY 4.0)
# python -I crop_art.py ../../../art_sources/D_knee-sagittal-dbcls/202108_Sagittal_section_through_knee_joint.svg
#   m04knee 126 136 300 392 --drop "foreignObject, aipgf"      (then moved into ../svg_paths/)
KNEE = (126, 136, 174, 256)                          # crop window, source user units (anterior is RIGHT)
KNEE_ID = "m4art_knee"
# The DBCLS knee uses its light blue for cartilage and menisci and its navy for the joint cavity, so the house
# "dbcls" map (elbow: light blue = cavity) does not fit; this local map does.
KNEE_RECOLOUR = {
    "#e2dacf": T["bone"][0], "#aaa59f": T["marrow"][0], "#84755d": T["bone"][1],
    "#adbcf2": T["cartilage"][0], "#29426d": T["fluid"][0], "#6079b2": T["fluid"][1],
    "#ffd664": T["fat"][0], "#f28b8b": T["muscle"][0], "#fdd6d8": T["skin"][0], "#fff3f3": T["tendon"][0],
}
# Landmarks measured once in Chrome (getPointAtLength, 600 samples per path) on the crop, source units.
KA = dict(
    contact=(196.0, 271.3),     # narrowest femoral-tibial cartilage gap: path 6 low edge 268.3 / path 16 top 274.2
    fem_cart=(157.2, 257.0),    # path 6 (femoral cartilage) outer 154.5,259.0 / path 8 (bone) 159.8,254.8: mid-band
    tib_cart=(180.0, 281.2),    # path 16 (tibial cartilage) top 277.7 / low 284.7 at x 180: mid-band
    meniscus=(221.5, 266.5),    # path 32 (anterior meniscus horn) centre
    cavity=(247.0, 247.0),      # path 3 (joint cavity) behind the patella
    patella=(266.0, 202.0),     # path 43 (patella, cancellous) centre
    femur=(200.0, 225.0),       # path 9 (femur, medullary) inside the condyle
    tibia=(208.0, 340.0),       # path 14 (tibia, medullary)
    lig=(271.0, 330.0),         # path 2 (patellar ligament)
    fat=(252.0, 300.0),         # path 4 (infrapatellar fat pad)
    quad=(226.0, 150.0),        # path 26 (quadriceps)
    tib_axis=((208.5, 350.0), (208.5, 385.0)),   # path 13 edges: 160.6/256.4 at y 350 (vertical shaft)
)


def knee_art():
    src = _read("202108_Sagittal_section_through_knee_joint_crop_m04knee.svg")
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


def SHARED_DEFS():
    """The knee crop once per page as #m4art_knee (svg 1, 2 and 17 <use> it)."""
    return f'<g id="{KNEE_ID}">{art_image("<svg>" + knee_art() + "</svg>", KNEE)}</g>'


class Knee:
    """The knee crop placed at (x, y) (top-left of the crop window) with scale k."""

    def __init__(self, x, y, k):
        self.x, self.y, self.k = x, y, k

    def use(self):
        return (f'<use href="#{KNEE_ID}" transform="translate({self.x - KNEE[0] * self.k:.2f} '
                f'{self.y - KNEE[1] * self.k:.2f}) scale({self.k})"/>')

    def M(self, pt):
        return (self.x + (pt[0] - KNEE[0]) * self.k, self.y + (pt[1] - KNEE[1]) * self.k)

    def box(self):
        return self.x, self.y, self.x + KNEE[2] * self.k, self.y + KNEE[3] * self.k


def knee_credit(what):
    return H.ATTRIBUTION["by"].format(author="DataBase Center for Life Science (DBCLS)",
                                      title="202108 Sagittal section through knee joint", licence="CC BY 4.0",
                                      changes=f"Recoloured, cropped. {what}")


def halo(s, x1, y1, x2, y2, w=6):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#fff" stroke-width="{s(w):.2f}"/>'


# ---------------------------------------------------------------- small tissue pieces
def brush(x, y, L=30, ang=90, n=6, charges=True, col=None):
    """Proteoglycan bottle-brush: core with GAG side chains, a fixed minus at alternate chain tips."""
    col = col or I["secondary"]
    a = math.radians(ang)
    ux, uy = math.cos(a), -math.sin(a)
    nx, ny = -uy, ux
    o = [f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+L*ux:.1f}" y2="{y+L*uy:.1f}" stroke="{col}" stroke-width="1.6"/>']
    for j in range(n):
        t = (j + 0.5) / n * L
        cx, cy = x + t * ux, y + t * uy
        for sg in (-1, 1):
            ex, ey = cx + sg * 6 * nx + 2 * ux, cy + sg * 6 * ny + 2 * uy
            o.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="{col}" stroke-width="1"/>')
            if charges and (j + (sg > 0)) % 2 == 0:
                mx, my = cx + sg * 9.5 * nx + 2.5 * ux, cy + sg * 9.5 * ny + 2.5 * uy
                o.append(f'<line x1="{mx-2.4:.1f}" y1="{my:.1f}" x2="{mx+2.4:.1f}" y2="{my:.1f}" stroke="{I["primary"]}" '
                         f'stroke-width="1.3"/>')
    return "".join(o)


def chondrocyte(x, y, rx, ry, rot=0):
    tf = f' transform="rotate({rot} {x:.1f} {y:.1f})"' if rot else ""
    return (f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx}" ry="{ry}" fill="{T["skin"][0]}" stroke="{T["skin"][1]}" '
            f'stroke-width="1"{tf}/>' + circ(x, y, min(rx, ry) * 0.42, T["bone"][1]))


def na_ion(x, y, r=7.5):
    return (circ(x, y, r, T["fluid"][0], T["fluid"][1], 1.2) +
            f'<path d="M{x-3.6:.1f},{y:.1f}h7.2M{x:.1f},{y-3.6:.1f}v7.2" stroke="{I["primary"]}" stroke-width="1.4"/>')


def cl_ion(x, y, r=7.5):
    return (circ(x, y, r, "#fff", T["fluid"][1], 1.4) +
            f'<path d="M{x-3.6:.1f},{y:.1f}h7.2" stroke="{I["primary"]}" stroke-width="1.4"/>')


def hatch(x0, y0, x1, y1, step=9, col=None):
    """Ground hatch under a rigid support."""
    col = col or I["rule"]
    o, x = [], x0
    while x < x1:
        o.append(f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x+(y1-y0):.1f}" y2="{y0:.1f}" stroke="{col}" stroke-width="1"/>')
        x += step
    return "".join(o)


def spring_d(x, y0, y1, n=7, amp=11.0, lead_=10.0):
    pts = [(x, y0), (x, y0 + lead_)]
    w = (y1 - y0 - 2 * lead_) / n
    for i in range(n):
        pts.append((x + (amp if i % 2 else -amp), y0 + lead_ + (i + 0.5) * w))
    pts += [(x, y1 - lead_), (x, y1)]
    return dpath(pts)


def trabecular(x0, y0, x1, y1, seed=4, n=26, r=(7, 15)):
    """Cancellous bone: bone fill with marrow spaces (deterministic placement, schematic)."""
    import random
    rnd = random.Random(seed)
    o = [rect(x0, y0, x1 - x0, y1 - y0, T["bone"][0], T["bone"][1], 1.0)]
    placed = []
    tries = 0
    while len(placed) < n and tries < 4000:
        tries += 1
        rx, ry = rnd.uniform(*r), rnd.uniform(r[0] * 0.7, r[1] * 0.8)
        cx, cy = rnd.uniform(x0 + rx + 3, x1 - rx - 3), rnd.uniform(y0 + ry + 3, y1 - ry - 3)
        if all(((cx - a) / (rx + c + 4)) ** 2 + ((cy - b) / (ry + d_ + 4)) ** 2 > 1 for a, b, c, d_ in placed):
            placed.append((cx, cy, rx, ry))
    for cx, cy, rx, ry in placed:
        o.append(ellipse(cx, cy, f"{rx:.1f}", f"{ry:.1f}", T["marrow"][0], T["bone"][1], 0.8))
    return "".join(o)


# ================================================================ svg 1 (Fig. 1): osteochondral unit
def fig1():
    p = "m4f1_"
    VB = (0, 0, 760, 364)
    s = H.Scale(VB[2], VB[3])
    kn = Knee(18, 24, 1.12)
    o = [f'<defs>{H.markers(p, s)}</defs>', kn.use()]
    # zoom window on the tibial plateau, where cartilage sits on bone
    zc = kn.M((200.0, 280.5))
    zw = 22.0
    o.append(f'<rect x="{zc[0]-zw/2:.1f}" y="{zc[1]-zw/2:.1f}" width="{zw}" height="{zw}" fill="none" '
             f'stroke="{I["axis"]}" stroke-width="{s(1.4):.2f}"/>')
    o.append(H.label(s, kn.M(KA["femur"])[0], kn.M(KA["femur"])[1], "femur", "label2", I["secondary"], "middle"))
    o.append(H.label(s, kn.M(KA["tibia"])[0], kn.M(KA["tibia"])[1], "tibia", "label2", I["secondary"], "middle"))
    # ---- the slice: hyaline layer to scale (h = 2 mm, line 604), the rest not to scale
    x0, x1 = 300.0, 520.0
    mm = 70.0                                          # px per mm in the hyaline layer
    yf, yc = 34.0, 64.0                                # fluid film top, articular surface
    yt = yc + H_M * 1e3 * mm                           # tidemark
    ycc = yt + 14.0                                    # cement line (calcified cartilage below the tidemark)
    ypl = ycc + 30.0                                   # end of the subchondral plate
    yb = 318.0
    o.append(rect(x0, yf, x1 - x0, yc - yf, T["fluid"][0], T["fluid"][1], 1.0))
    o.append(rect(x0, yc, x1 - x0, yt - yc, T["cartilage"][0], T["cartilage"][1], 1.0))
    o.append(trabecular(x0, ypl, x1, yb, seed=7, n=14, r=(9, 18)))
    o.append(rect(x0, ycc, x1 - x0, ypl - ycc, T["bone"][0], T["bone"][1], 1.0))
    o.append(rect(x0, yt, x1 - x0, ycc - yt, T["bone_shade"][0], T["bone"][1], 1.0, extra='fill-opacity="0.55"'))
    wave = [(x0 + i * (x1 - x0) / 44, yt + 1.6 * math.sin(i * 1.3)) for i in range(45)]
    o.append(path(dpath(wave), T["bone"][1], 1.8))
    # the physics lives in the hyaline layer
    o.append(H.label(s, (x0 + x1) / 2, yc + 60, "hyaline cartilage", "label", I["primary"], "middle"))
    o.append(H.label(s, (x0 + x1) / 2, yc + 80, "porous, charged, 65–80 % water", "label2", I["secondary"], "middle"))
    o.append(H.label(s, (x0 + x1) / 2, yc + 100, "biphasic and Donnan physics (§2–§5)", "label2", I["secondary"],
                     "middle"))
    # thickness of the hyaline layer
    xd = x0 - 18
    for y in (yc, yt):
        o.append(H.line(s, xd - 6, y, x0, y, O["geometry"], "leader"))
    o.append(H.arrow(s, p, xd, yc, xd, yt, "geometry", both=True))
    o.append(H.label(s, xd - 8, (yc + yt) / 2 - 2, f'{it("h")} ≈ 2 mm', "label", I["primary"], "end"))
    o.append(H.label(s, xd - 8, (yc + yt) / 2 + 16, "(2–4 mm)", "label2", I["secondary"], "end"))
    # load path
    o.append(H.arrow(s, p, x1 - 30, yf - 30, x1 - 30, yf - 2, "load"))
    o.append(H.label(s, x1 - 38, yf - 14, "joint load", "label2", I["primary"], "end"))
    # layer names, right, in load-bearing order
    lx = x1 + 24
    rows = [((yf + yc) / 2, "synovial fluid", "lubricant film (not to scale)"),
            ((yc + yt) / 2, "hyaline (articular) cartilage", "the load-bearing layer"),
            (yt, "tidemark (calcification front)", ""),
            ((yt + ycc) / 2 + 4, "calcified cartilage", ""),
            ((ycc + ypl) / 2, "subchondral bone plate", ""),
            ((ypl + yb) / 2 + 20, "cancellous (trabecular) bone", "marrow between the struts")]
    ys = [52, 150, 214, 238, 262, 290]
    for (ya, t1, t2), yl in zip(rows, ys):
        o.append(lead(s, x1 - 6, ya, lx - 4, yl - 4))
        o.append(H.label(s, lx, yl, t1, "label2", I["primary"]))
        if t2:
            o.append(H.label(s, lx, yl + 15, t2, "label2", I["muted"]))
    # zoom guides
    da = f'stroke-dasharray="{s(5):.1f} {s(3):.1f}"'
    o.append(path(f"M{zc[0]+zw/2:.1f},{zc[1]-zw/2:.1f} L{x0-4:.1f},{yf:.1f} M{zc[0]+zw/2:.1f},{zc[1]+zw/2:.1f} "
                  f"L{x0-4:.1f},{yb:.1f}", I["rule"], s(1.1), extra=da))
    cr = knee_credit("Slice drawn for this course; only the hyaline layer is to scale.")
    o.append(H.credit(s, 10, 342, wrap(cr, 128)))
    aria = ("Osteochondral unit. Left: a sagittal section of the knee with a small box on the tibial plateau. Right: the "
            "boxed slice enlarged, in load-bearing order from the top: synovial fluid film, hyaline articular cartilage "
            "about 2 millimetres thick (drawn to scale, 2 to 4 millimetres in life), the wavy tidemark, calcified "
            "cartilage, the subchondral bone plate and cancellous bone with marrow spaces. The biphasic and Donnan "
            "physics of sections 2 to 5 live in the hyaline layer.")
    return finish(VB, aria, s, o)


# ================================================================ svg 2 (Fig. 2): the impossible bearing
def fig2():
    p = "m4f2_"
    VB = (0, 0, 760, 478)
    s = H.Scale(VB[2], VB[3])
    kn = Knee(250, 8, 1.55)
    o = [f'<defs>{H.markers(p, s)}</defs>', kn.use()]
    M = kn.M
    # joint reaction pressing the femur onto the tibia, tip on the contact
    cx, cy = M(KA["contact"])
    o.append(halo(s, cx, cy - 112, cx, cy - 6, 7))
    o.append(H.arrow(s, p, cx, cy - 112, cx, cy - 6, "reaction"))
    o.append(H.label(s, cx + 9, cy - 92, f'{it("R")} ≈ {R_JOINT:.0f} N', "label", I["primary"]))
    o.append(H.label(s, cx + 9, cy - 75, "joint reaction (Module 3)", "label2", I["secondary"]))
    # sliding at the contact, drawn just above it on the femoral side
    o.append(halo(s, cx - 34, cy - 18, cx + 34, cy - 18, 6))
    o.append(H.arrow(s, p, cx - 34, cy - 18, cx + 34, cy - 18, "dim", w="geom", both=True))
    # labels, posterior (left) side
    lx = 236
    left = [(KA["fem_cart"], 238, "articular cartilage", "2–4 mm on each bone end"),
            (KA["tib_cart"], 238, None, None),
            ((166.0, 276.0), 326, "meniscus", "fibrocartilage wedge"),
            (KA["tibia"], 396, "tibia", ""),
            (KA["femur"], 120, "femur", "")]
    for pt, ly, t1, t2 in left:
        ax, ay = M(pt)
        o.append(lead(s, ax, ay, lx + 4, ly - 4))
        if t1:
            o.append(H.label(s, lx, ly, t1, "label", I["primary"], "end"))
        if t2:
            o.append(H.label(s, lx, ly + 17, t2, "label2", I["secondary"], "end"))
    # labels, anterior (right) side
    rx = 540
    right = [(KA["patella"], 150, "patella", ""),
             (KA["cavity"], 246, "synovial fluid", "fills the joint cavity"),
             ((cx + 2, cy), 300, None, None)]
    for pt, ly, t1, t2 in right:
        ax, ay = pt if t1 is None else M(pt)
        o.append(lead(s, ax, ay, rx - 4, ly - 4))
        if t1:
            o.append(H.label(s, rx, ly, t1, "label", I["primary"]))
        if t2:
            o.append(H.label(s, rx, ly + 17, t2, "label2", I["secondary"]))
    o.append(H.label(s, rx, 300, "contact: surfaces slide", "label", I["primary"]))
    o.append(H.label(s, rx, 317, f'at {it("μ")} ≈ 0.005 (ice on ice: 0.03)', "label2", I["secondary"]))
    pbar = R_JOINT / (AC_CM2 * 1e-4) / 1e6
    o.append(H.label(s, 380, 428, f'mean contact pressure {it("p")} = {it("R")} / {it("A")}{H.sub("c", s)} ≈ {pbar:.1f} MPa  ·  '
                     f'≈ 10⁶ cycles a year  ·  decades, no replacement', "label2", I["primary"], "middle"))
    o.append(H.label(s, 380, 448, "How does 2–4 mm of soft, water-filled gel do this?", "label", I["primary"], "middle",
                     'font-style="italic"'))
    o.append(H.credit(s, 10, 462, wrap(knee_credit("Arrows and labels drawn for this course; arrows not to force scale."), 128)))
    aria = ("The impossible bearing: a sagittal section of the knee, a synovial joint. The femur and tibia each end in a "
            "thin layer of articular cartilage, 2 to 4 millimetres thick; a meniscus sits between them and synovial fluid "
            "fills the joint cavity in front, behind the patella. A dark arrow, the joint reaction R of about 1715 newtons, "
            "presses the femur onto the tibia at the contact; a double arrow at the contact marks sliding at a friction "
            "coefficient of about 0.005. Mean contact pressure about 1.7 megapascals, about a million cycles a year, for "
            "decades.")
    return finish(VB, aria, s, o)


# ================================================================ svg 17 (Fig. 15): condyle on the plateau
def fig17():
    p = "m4f17_"
    VB = (0, 0, 760, 452)
    s = H.Scale(VB[2], VB[3])
    kn = Knee(14, 56, 1.22)
    o = [f'<defs>{H.markers(p, s)}</defs>', kn.use()]
    cx, cy = kn.M(KA["contact"])
    o.append(halo(s, cx, cy - 96, cx, cy - 5, 7))
    o.append(H.arrow(s, p, cx, cy - 96, cx, cy - 5, "reaction"))
    o.append(H.label(s, cx + 8, cy - 80, it("R"), "label", I["primary"]))
    zw, zh = 40.0, 26.0
    o.append(f'<rect x="{cx-zw/2:.1f}" y="{cy-zh/2:.1f}" width="{zw}" height="{zh}" fill="none" stroke="{I["axis"]}" '
             f'stroke-width="{s(1.4):.2f}"/>')
    o.append(H.label(s, kn.M(KA["tibia"])[0], kn.M(KA["tibia"])[1], "tibia", "label2", I["secondary"], "middle"))
    o.append(H.label(s, kn.M((178.0, 205.0))[0], kn.M((178.0, 205.0))[1], "femur", "label2", I["secondary"], "middle"))
    # ---- zoom: cartilage thickness and contact width to one mm scale; condyle curvature schematic
    mm = 9.0
    xc, yt, ytop = 520.0, 250.0, 80.0               # contact centre, tibial cartilage surface, top cut of the condyle
    hh, a = H_M * 1e3 * mm, A_C * 1e3 * mm          # 18 px, 162 px
    xl, xr = 298.0, 744.0
    rp = R_EFF * 1e3 * mm                            # condyle radius to the same scale (30 mm, line 941)
    o.append(trabecular(xl, yt + hh + 12, xr, yt + hh + 54, seed=3, n=16, r=(7, 13)))
    o.append(rect(xl, yt + hh, xr - xl, 12, T["bone"][0], T["bone"][1], 1.0))
    o.append(rect(xl, yt, xr - xl, hh, T["cartilage"][0], T["cartilage"][1], 1.0))

    def surf(x):
        """Loaded femoral surface: flat over the patch, then the condyle's own curvature (gap (x^2 - a^2) / 2R)."""
        d = abs(x - xc)
        return yt - (d * d - a * a) / (2 * rp) if d > a else yt
    xs = [xl + (xr - xl) * i / 120 for i in range(121)]
    out = [(x, surf(x)) for x in xs]
    inn = [(x, y - hh) for x, y in out]
    o.append(path(dpath(out + inn[::-1], True), T["cartilage"][1], 1.0, T["cartilage"][0]))
    o.append(path(dpath([(xl, ytop)] + inn + [(xr, ytop)], True), T["bone"][1], 1.0, T["bone"][0]))
    cut = [(xl - 3 + i * (xr - xl + 6) / 40, ytop + 2.2 * math.sin(i * 1.7)) for i in range(41)]
    o.append(path(dpath(cut), "#fff", 5))
    o.append(H.arrow(s, p, xc, 20, xc, ytop + 40, "reaction"))
    o.append(H.label(s, xc + 9, 40, f'{it("R")} ≈ {R_JOINT:.0f} N', "label", I["primary"]))
    o.append(H.label(s, xc, 150, "femoral condyle", "label", I["primary"], "middle"))
    o.append(H.label(s, xc, 168, "(bone)", "label2", I["secondary"], "middle"))
    # cartilage labels with leaders
    xq = xc + a + 40
    o.append(lead(s, xq, surf(xq) - hh / 2, xq - 20, 186))
    o.append(H.label(s, xq - 24, 182, "femoral cartilage", "label2", I["primary"], "end"))
    o.append(lead(s, 326, yt + hh / 2, 326, yt + hh + 27))
    o.append(H.label(s, 306, yt + hh + 42, "tibial cartilage", "label2", I["primary"]))
    # thickness h on the tibial layer, right end
    xh = 732.0
    o.append(H.arrow(s, p, xh, yt - 22, xh, yt, "geometry"))
    o.append(H.arrow(s, p, xh, yt + hh + 22, xh, yt + hh, "geometry"))
    o.append(H.label(s, xh - 8, yt + hh + 42, f'{it("h")} ≈ 2 mm', "label", I["primary"], "end"))
    o.append(H.label(s, xc, yt + hh + 42, "rigid subchondral bone", "label2", I["primary"], "middle"))
    # contact patch 2a
    yd = yt + hh + 78
    for x in (xc - a, xc + a):
        o.append(H.line(s, x, yt, x, yd + 6, O["geometry"], "leader"))
    o.append(H.arrow(s, p, xc - a, yd, xc + a, yd, "geometry", both=True))
    o.append(H.label(s, xc, yd + 20, f'contact width 2{it("a")} ≈ {2 * A_C * 1e3:.0f} mm  ({it("a")} ≈ {A_C * 1e3:.0f} mm)',
                     "label", I["primary"], "middle"))
    o.append(H.label(s, xc, yd + 40, f'{it("a")} / {it("h")} ≈ {A_C / H_M:.0f}: a thin layer, not the deep half-space Hertz '
                     f'assumes', "label2", I["secondary"], "middle"))
    # scale bar
    ys_ = yd + 64
    o.append(H.line(s, xl + 4, ys_, xl + 4 + 10 * mm, ys_, I["axis"], "axis"))
    for x in (xl + 4, xl + 4 + 10 * mm):
        o.append(H.line(s, x, ys_ - 5, x, ys_ + 5, I["axis"], "leader"))
    o.append(H.label(s, xl + 14 + 10 * mm, ys_ + 5, "10 mm: h, 2a and the 30 mm condyle radius all to this scale",
                     "label2", I["muted"]))
    # zoom guides
    da = f'stroke-dasharray="{s(5):.1f} {s(3):.1f}"'
    o.append(path(f"M{cx+zw/2:.1f},{cy-zh/2:.1f} L{xl-4:.1f},{ytop:.1f} M{cx+zw/2:.1f},{cy+zh/2:.1f} L{xl-4:.1f},"
                  f"{yt+hh+54:.1f}", I["rule"], s(1.1), extra=da))
    o.append(H.credit(s, 10, 434, wrap(knee_credit("Zoom and overlays drawn for this course."), 128)))
    aria = ("The contact. Left: a sagittal section of the knee; a dark arrow, the joint reaction R, presses the femoral "
            "condyle onto the tibial plateau, and a box marks the contact. Right: the boxed region enlarged, with the "
            "cartilage thickness and the contact width drawn to one millimetre scale: the condyle, capped with cartilage, "
            "bears on a 2 millimetre tibial cartilage layer over rigid subchondral bone; R about 1715 newtons, contact "
            "patch 2a about 36 millimetres wide (a about 18 millimetres), so a over h is about 9: a thin layer, not the "
            "deep half-space that Hertz contact assumes. The 30 millimetre condyle radius is drawn to the same scale.")
    return finish(VB, aria, s, o)


# ================================================================ svg 4 (Fig. 3): inside the layer
def fig4():
    p = "m4f4_"
    VB = (0, 0, 760, 452)
    s = H.Scale(VB[2], VB[3])
    x0, x1 = 214.0, 554.0
    ys, yz1, yz2, yt = 52.0, 52 + 0.15 * 290, 52 + 0.65 * 290, 342.0   # surface, zone bounds, tidemark (2 mm = 290 px)
    ycc, yb = yt + 16, 404.0
    col = T["tendon"][1]
    o = [f'<defs>{H.markers(p, s)}<clipPath id="{p}clip"><rect x="{x0}" y="{ys}" width="{x1-x0}" height="{ycc-ys}"/>'
         f'</clipPath></defs>']
    o.append(rect(x0, ys - 16, x1 - x0, 16, T["fluid"][0], T["fluid"][1], 1.0))
    o.append(rect(x0, ys, x1 - x0, yt - ys, T["cartilage"][0], T["cartilage"][1], 1.0))
    o.append(rect(x0, yt, x1 - x0, ycc - yt, T["bone_shade"][0], T["bone"][1], 1.0, extra='fill-opacity="0.55"'))
    o.append(trabecular(x0, ycc, x1, yb, seed=11, n=10, r=(9, 16)))
    for y in (yz1, yz2):
        o.append(H.line(s, x0, y, x1, y, I["rule"], "leader", (2, 3)))
    # interstitial water: sparse fluid dots
    import random
    rnd = random.Random(5)
    for _ in range(46):
        o.append(circ(rnd.uniform(x0 + 6, x1 - 6), rnd.uniform(ys + 6, yt - 6), 1.8, T["fluid"][0], T["fluid"][1], 0.6))
    # collagen: Benninghoff arcades (radial in the deep zone, arching in the middle, tangential at the surface)
    fib = []
    n_arc, wa = 4, (x1 - x0) / 4
    for k in range(n_arc + 1):
        xa = x0 + k * wa
        for j, (dx, ytop) in enumerate(((10, ys + 9), (20, ys + 17), (30, ys + 25))):
            xl, xr = xa - wa / 2 + dx, xa + wa / 2 - dx
            fib.append(f"M{xl:.1f},{ycc-4:.1f} L{xl:.1f},{yz2:.1f} C{xl:.1f},{ytop+30:.1f} {xa-wa*0.18:.1f},{ytop:.1f} "
                       f"{xa:.1f},{ytop:.1f} C{xa+wa*0.18:.1f},{ytop:.1f} {xr:.1f},{ytop+30:.1f} {xr:.1f},{yz2:.1f} "
                       f"L{xr:.1f},{ycc-4:.1f}")
    for y in (ys + 4, ys + 7.5):
        fib.append(f"M{x0:.1f},{y:.1f} L{x1:.1f},{y:.1f}")
    o.append(f'<g clip-path="url(#{p}clip)">' + "".join(path(d, col, 1.5) for d in fib) + "</g>")
    wave = [(x0 + i * (x1 - x0) / 60, yt + 1.6 * math.sin(i * 1.25)) for i in range(61)]
    o.append(path(dpath(wave), T["bone"][1], 1.8))
    # chondrocytes: flat at the surface, round in the middle, in columns in the deep zone
    for x in (262, 352, 450, 520):
        o.append(chondrocyte(x, ys + 32, 10, 3.6))
    for x, y in ((250, 140), (330, 186), (414, 128), (500, 176), (300, 222)):
        o.append(chondrocyte(x, y, 6.5, 6.0))
    for x in (x0 + wa * 0.5 + 2, x0 + wa * 1.5 - 2, x0 + wa * 2.5 + 2, x0 + wa * 3.5 - 2):
        for y in (268, 284, 300, 316):
            o.append(chondrocyte(x, y, 5.2, 4.6))
    # proteoglycan aggregates (fixed negative charge)
    for x, y in ((236, 214), (290, 160), (372, 200), (458, 222), (530, 150)):
        o.append(brush(x, y, 34, 90, 5))
    # zone names (right)
    lx = x1 + 12
    for y0_, y1_, t1, t2 in ((ys, yz1, "superficial zone", "fibres tangential"), (yz1, yz2, "middle zone", "fibres arch"),
                             (yz2, yt, "deep zone", "fibres radial")):
        o.append(H.line(s, x1 + 4, y0_ + 2, x1 + 4, y1_ - 2, I["rule"], "leader"))
        o.append(H.label(s, lx, (y0_ + y1_) / 2 - 2, t1, "label2", I["primary"]))
        o.append(H.label(s, lx, (y0_ + y1_) / 2 + 14, t2, "label2", I["muted"]))
    o.append(lead(s, x1 - 8, yt + 1, lx - 4, yt + 2))
    o.append(H.label(s, lx, yt + 6, "tidemark", "label2", I["primary"]))
    o.append(lead(s, x1 - 8, (yt + ycc) / 2, lx - 4, yt + 24))
    o.append(H.label(s, lx, yt + 28, "calcified cartilage", "label2", I["primary"]))
    o.append(H.label(s, lx, yb - 8, "subchondral bone", "label2", I["primary"]))
    o.append(H.label(s, lx, ys - 4, "articular surface", "label2", I["primary"]))
    # constituents (left), each with a leader to one example
    rx = x0 - 52
    o.append(circ(x0 + 14, 296, 1.8, T["fluid"][0], T["fluid"][1], 0.6))
    rows = [((262 - 10, ys + 32), 52, "chondrocyte", "< 10 % of volume, no load"),
            ((290, 164), 128, "proteoglycan aggregate", f'fixed negative charge {it("c")}{H.sub("F", s, "label2")}'),
            ((x0 + wa / 2 - 10, 226), 204, "collagen fibre (type II)", "carries tension"),
            ((x0 + 14, 296), 280, "interstitial water", "65–80 % of wet weight")]
    for (ax, ay), ly, t1, t2 in rows:
        o.append(lead(s, ax, ay, rx + 4, ly - 4))
        if t1:
            o.append(H.label(s, rx, ly, t1, "label2", I["primary"], "end"))
            o.append(H.label(s, rx, ly + 15, t2, "label2", I["muted"], "end"))
    # depth
    xd = x0 - 14
    o.append(H.arrow(s, p, xd, ys, xd, yt, "dim", both=True))
    o.append(H.label(s, xd - 6, 252, "2–4 mm", "label2", I["secondary"], "end"))
    lg, _ = legend(s, 20, 442, [(sw_line(col, 1.5), "collagen fibre"), (sw_line(I["secondary"], 1.6), "proteoglycan (− = fixed charge)"),
                                (sw_dot(T["skin"][0], T["skin"][1]), "chondrocyte"), (sw_dot(T["fluid"][0], T["fluid"][1]), "water"),
                                (sw_rect(T["cartilage"][0], T["cartilage"][1]), "cartilage matrix")], gap=14, cw=6.3)
    o.append(lg)
    aria = ("Schematic slice of articular cartilage about 2 to 4 millimetres deep, on calcified cartilage and subchondral "
            "bone. Collagen fibres rise radially in the deep zone, anchored across the wavy tidemark into calcified "
            "cartilage, arch in the middle zone and run tangential to the articular surface in the superficial zone: "
            "Benninghoff arcades. Bottle-brush proteoglycan aggregates with fixed negative charges sit in the mesh; "
            "sparse chondrocytes are flat at the surface, round in the middle zone and stacked in columns in the deep "
            "zone; dots mark the interstitial water, 65 to 80 percent of wet weight.")
    return finish(VB, aria, s, o)


# ================================================================ svg 5 (Fig. 4): Donnan equilibrium
def fig5():
    p = "m4f5_"
    VB = (0, 0, 760, 418)
    s = H.Scale(VB[2], VB[3])
    per = 0.025                                        # M per glyph: glyph count per compartment ∝ concentration
    n_fix, n_na, n_cl, n_b = round(CF / per), round(CP / per), round(CM / per), round(C0 / per)
    assert (n_fix, n_na, n_cl, n_b) == (8, 11, 3, 6) and n_na == n_cl + n_fix
    tx0, tx1, bx0, bx1, y0, y1 = 24.0, 334.0, 426.0, 736.0, 58.0, 282.0
    xb = (tx1 + bx0) / 2
    o = [f'<defs>{H.markers(p, s)}{fluid_marker(p, s)}</defs>']
    o.append(rect(tx0, y0, tx1 - tx0, y1 - y0, T["cartilage"][0], T["cartilage"][1], 1.2, 8))
    o.append(rect(bx0, y0, bx1 - bx0, y1 - y0, T["fluid"][0], T["fluid"][1], 1.2, 8, 'fill-opacity="0.45"'))
    o.append(H.label(s, (tx0 + tx1) / 2, 40, "tissue (cartilage)", "label", I["primary"], "middle"))
    o.append(H.label(s, (bx0 + bx1) / 2, 40, "salt bath (synovial fluid)", "label", I["primary"], "middle"))
    o.append(H.line(s, xb, 22, xb, y1 + 6, O["dim"], "ref", H.DASH_REF))
    # fixed charges on two proteoglycan brushes (4 each)
    o.append(brush(92, 236, 120, 72, 4))
    o.append(brush(232, 240, 120, 100, 4))
    na_t = [(60, 90), (128, 80), (200, 96), (288, 84), (162, 146), (300, 150), (70, 190), (254, 196), (120, 256),
            (304, 254), (190, 264)][:n_na]
    cl_t = [(176, 118), (292, 214), (44, 250)][:n_cl]
    na_b = [(500, 80), (580, 84), (668, 100), (520, 176), (620, 160), (700, 248)][:n_b]
    cl_b = [(512, 136), (610, 118), (494, 236), (568, 236), (668, 200), (720, 140)][:n_b]
    for x, y in na_t + na_b:
        o.append(na_ion(x, y))
    for x, y in cl_t + cl_b:
        o.append(cl_ion(x, y))
    # fluxes across the boundary
    o.append(fluid_arrow(s, p, bx0 + 50, 112, tx1 - 22, 112))
    o.append(H.label(s, xb + 8, 104, "Na⁺ drawn in", "label2", I["primary"]))
    o.append(fluid_arrow(s, p, tx1 - 22, 212, bx0 + 50, 212))
    o.append(H.label(s, xb + 8, 204, "Cl⁻ partly out", "label2", I["primary"]))
    o.append(fluid_arrow(s, p, bx0 + 50, 262, tx1 - 22, 262, w="geom"))
    o.append(H.label(s, xb + 8, 254, "water in", "label2", I["primary"]))
    # computed concentrations (section 2, eq. 3)
    yt = y1 + 26
    o.append(H.label(s, (tx0 + tx1) / 2, yt, f'{it("c")}₊ = {CP:.2f} M,  {it("c")}₋ = {CM:.2f} M,  {it("c")}{H.sub("F", s)} = {CF:.2f} M',
                     "label", I["primary"], "middle"))
    o.append(H.label(s, (tx0 + tx1) / 2, yt + 19, f'{it("c")}₊ = {it("c")}₋ + {it("c")}{H.sub("F", s, "label2")} (neutral),  '
                     f'{it("c")}₊{it("c")}₋ = {it("c")}₀² (Donnan)', "label2", I["secondary"], "middle"))
    o.append(H.label(s, (bx0 + bx1) / 2, yt, f'{it("c")}₊ = {it("c")}₋ = {it("c")}₀ = {C0:.2f} M', "label", I["primary"], "middle"))
    o.append(H.label(s, (bx0 + bx1) / 2, yt + 19, "neutral, no fixed charge", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 380, yt + 52, f'swelling pressure {it("π")} = {it("R")}{H.sub("g", s)}Θ (√({it("c")}{H.sub("F", s)}² + 4{it("c")}₀²) − 2{it("c")}₀) '
                     f'≈ {PI_SW / 1e6:.2f} MPa, held by collagen tension', "label", I["primary"], "middle"))
    o.append(H.label(s, xb, 16, "boundary: water, Na⁺, Cl⁻ pass; the fixed charge cannot", "label2", I["secondary"], "middle"))
    lg, _ = legend(s, 24, 404, [(lambda x, y: na_ion(x + 7, y - 5, 6), "Na⁺ (mobile)"),
                                (lambda x, y: cl_ion(x + 7, y - 5, 6), "Cl⁻ (mobile)"),
                                (sw_line(I["secondary"], 1.6), "proteoglycan, − = fixed charge (bound)"),
                                (lambda x, y: "", f"one symbol = {per} M")], gap=18, cw=6.3)
    o.append(lg)
    aria = ("Donnan equilibrium. Left, a cartilage compartment: two proteoglycan brushes carry 8 fixed negative charges, "
            "with 11 sodium and 3 chloride ions; right, a salt bath with 6 sodium and 6 chloride ions; one symbol is 0.025 "
            "molar, so the counts follow the computed concentrations. A dashed boundary passes water and small ions but "
            "not the fixed charge. Arrows: sodium drawn in, chloride partly out, water in. Inside, c plus 0.28 molar, c "
            "minus 0.08 molar, fixed charge 0.20 molar; outside, both 0.15 molar. Swelling pressure about 0.16 megapascals, "
            "held by collagen tension.")
    return finish(VB, aria, s, o)


# ================================================================ chamber pieces (svg 7, 8, 12)
def chamber(s, x0, x1, ytop, ybase, wall=20.0, base=18.0):
    """Rigid impermeable chamber: walls and base (grey), ground hatch."""
    o = [rect(x0 - wall, ytop, wall, ybase - ytop + base, GRID, I["rule"], 1.0),
         rect(x1, ytop, wall, ybase - ytop + base, GRID, I["rule"], 1.0),
         rect(x0, ybase, x1 - x0, base, GRID, I["rule"], 1.0)]
    o.append(hatch(x0 - wall, ybase + base, x1 + wall, ybase + base + 10))
    return "".join(o)


def platen(s, x0, x1, y, th=20.0, holes=6):
    o = [rect(x0, y, x1 - x0, th, GRID, I["axis"], 1.2)]
    for i in range(holes):
        o.append(circ(x0 + (i + 0.5) * (x1 - x0) / holes, y + th / 2, 3.2, "#fff", I["axis"], 1.0))
    return "".join(o)


# ================================================================ svg 7 (Fig. 6): confined compression
def fig7():
    p = "m4f7_"
    VB = (0, 0, 760, 456)
    s = H.Scale(VB[2], VB[3])
    x0, x1, yp, ybase = 250.0, 470.0, 150.0, 392.0
    o = [f'<defs>{H.markers(p, s)}{fluid_marker(p, s)}</defs>']
    o.append(chamber(s, x0, x1, yp - 26, ybase))
    o.append(rect(x0, yp, x1 - x0, ybase - yp, T["cartilage"][0], T["cartilage"][1], 1.0))
    import random
    rnd = random.Random(2)
    for _ in range(26):
        o.append(circ(rnd.uniform(x0 + 8, x1 - 8), rnd.uniform(yp + 8, ybase - 8), 1.8, T["fluid"][0], T["fluid"][1], 0.6))
    o.append(brush(284, 360, 40, 90, 5))
    o.append(brush(430, 300, 40, 90, 5))
    o.append(platen(s, x0, x1, yp - 22))
    for x in (300, 360, 420):
        o.append(H.arrow(s, p, x, 64, x, yp - 24, "load"))
    o.append(H.label(s, 360, 50, f'applied total stress {it("σ")}₀ (held)', "label", I["primary"], "middle"))
    for xh, dx in ((x0 + 18, -14), (x1 - 18, 14)):
        o.append(fluid_arrow(s, p, xh, yp - 26, xh + dx, yp - 72))
    o.append(H.label(s, x1 + 4, yp - 60, f'{it("q")}: fluid out', "label2", I["primary"]))
    # depth axis
    xa = 190.0
    o.append(H.arrow(s, p, xa, ybase, xa, yp - 6, "dim"))
    o.append(H.label(s, xa - 10, ybase + 5, f'{it("z")} = 0', "label", I["primary"], "end"))
    o.append(H.label(s, xa - 10, yp + 5, f'{it("z")} = {it("h")}', "label", I["primary"], "end"))
    o.append(H.label(s, xa - 10, (yp + ybase) / 2 + 5, it("z"), "label", I["primary"], "end"))
    for y in (yp, ybase):
        o.append(H.line(s, xa - 5, y, x0 - 22, y, O["dim"], "leader"))
    # field variables at one depth z
    yz = 262.0
    o.append(H.line(s, x0, yz, x1, yz, O["dim"], "ref", (3, 3)))
    o.append(H.arrow(s, p, 268, yz, 268, yz - 34, "geometry"))
    o.append(H.label(s, 276, yz - 18, f'{it("u")}({it("z")}, {it("t")}): solid displacement', "label2", I["primary"]))
    o.append(H.label(s, 360, yz + 34, f'{it("p")}({it("z")}, {it("t")}): pore pressure', "label", I["primary"], "middle"))
    o.append(H.label(s, 360, 196, "charged porous gel", "label2", I["secondary"], "middle"))
    # boundary conditions (right)
    lx = 520
    rows = [((x1 - 6, yp - 12), yp - 18, "porous platen: drains", f'{it("p")} = 0 at {it("z")} = {it("h")}; carries {it("σ")}₀'),
            ((x1 - 8, 220), 220, f'cartilage plug, thickness {it("h")}', "2 mm in the §3 table"),
            ((x1 + 10, 320), 316, "rigid side walls", "impermeable, frictionless"),
            ((x1 - 30, ybase + 9), ybase + 10, "impermeable rigid base", f'{it("u")} = 0 and {it("q")} = 0 at {it("z")} = 0')]
    for (ax, ay), ly, t1, t2 in rows:
        o.append(lead(s, ax, ay, lx - 4, ly - 4))
        o.append(H.label(s, lx, ly, t1, "label2", I["primary"]))
        o.append(H.label(s, lx, ly + 16, t2, "label2", I["secondary"]))
    o.append(H.label(s, 360, 446, f'deformation and flow only along {it("z")}', "label2", I["secondary"], "middle"))
    aria = ("Confined-compression test. A cartilage plug of thickness h sits in a rigid chamber with impermeable, "
            "frictionless walls and an impermeable rigid base at z equals 0. A porous platen at z equals h carries the "
            "held applied stress sigma nought, drawn as three brown arrows, and drains: p equals 0 there, and fluid flux q "
            "leaves upward. At a depth z the solid displacement u, upward positive, and the pore pressure p are marked. At "
            "the base, u equals 0 and q equals 0. Deformation and flow are only along z.")
    return finish(VB, aria, s, o)


# ================================================================ svg 8 (Fig. 7): effective-stress partition
def fig8():
    p = "m4f8_"
    VB = (0, 0, 760, 342)
    s = H.Scale(VB[2], VB[3])
    x0, x1, yp, ybase = 110.0, 350.0, 118.0, 282.0
    o = [f'<defs>{H.markers(p, s)}{fluid_marker(p, s)}</defs>']
    o.append(chamber(s, x0, x1, yp - 24, ybase, wall=14, base=14))
    o.append(rect(x0, yp, x1 - x0, ybase - yp, T["fluid"][0], T["fluid"][1], 1.0))
    o.append(path(spring_d(178, yp, ybase, n=8, amp=14), SOLID, 3.0, extra='stroke-linejoin="round"'))
    o.append(platen(s, x0, x1, yp - 20, 20, 5))
    for x in (160, 230, 300):
        o.append(H.arrow(s, p, x, 34, x, yp - 22, "load"))
    o.append(H.label(s, 230, 22, f'total stress {it("σ")} from the platen', "label", I["primary"], "middle"))
    o.append(H.label(s, 270, 194, it("p"), "label", I["primary"], "middle"))
    # labels (right column)
    lx = 380
    o.append(H.label(s, lx, 92, "platen holes: fluid can leave only slowly", "label2", I["secondary"]))
    o.append(H.label(s, lx, 108, f'(low permeability {it("k")})', "label2", I["secondary"]))
    o.append(fluid_arrow(s, p, x0 + 24, yp - 21, x0 + 14, yp - 48, w="geom"))
    o.append(fluid_arrow(s, p, x1 - 24, yp - 21, x1 - 14, yp - 48, w="geom"))
    o.append(lead(s, 300, 152, lx - 4, 146))
    o.append(H.label(s, lx, 150, "interstitial fluid", "label2", I["primary"]))
    o.append(H.label(s, lx, 166, f'carries pore pressure {it("p")}', "label2", I["secondary"]))
    o.append(lead(s, 192, 236, lx - 4, 206))
    o.append(H.label(s, lx, 210, f'solid matrix: a spring of stiffness {it("H")}{H.sub("A", s, "label2")}', "label2", I["primary"]))
    o.append(H.label(s, lx, 226, f'carries {it("σ")}{H.sub("E", s, "label2")} = {it("H")}{H.sub("A", s, "label2")}{it("ε")}',
                     "label2", I["secondary"]))
    # the partition
    o.append(H.label(s, 560, 270, f'{it("σ")} = {it("σ")}{H.sub("E", s)} − {it("p")}', "label", I["primary"], "middle",
                     f'font-size="{s(22):.2f}"'))
    o.append(H.label(s, 560, 292, "tension positive (§3, eq. 4); compression positive (§4):", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 560, 310, f'{it("σ")}₀ = {it("σ")}{H.sub("E", s, "label2")} + {it("p")}.  Which phase carries how much '
                     'depends on time.', "label2", I["secondary"], "middle"))
    lg, _ = legend(s, 110, 334, [(sw_line(SOLID, 3), "solid matrix"), (sw_rect(T["fluid"][0], T["fluid"][1]), "interstitial fluid"),
                                 (sw_line(O["load"], 2.5), "applied stress")], gap=18, cw=6.3)
    o.append(lg)
    aria = ("Effective-stress partition, drawn as a spring in a fluid-filled cylinder under a porous platen. Brown arrows: "
            "the total stress sigma from the platen. The spring is the solid matrix, stiffness H A, carrying the effective "
            "stress sigma E equals H A epsilon; the fluid around it carries the pore pressure p; the platen holes let fluid "
            "leave only slowly, the low permeability k. Sigma equals sigma E minus p with tension positive; with "
            "compression positive, sigma nought equals sigma E plus p. Which phase carries how much depends on time.")
    return finish(VB, aria, s, o)


# ================================================================ svg 12 (Fig. 11): the loaded plug, frames
def fmt_t(t):
    if t == 0:
        return "0⁺"
    if t < 10:
        return f"{t:.1f} s"
    if t < 120:
        return f"{t:.0f} s"
    if t < 600:
        return f"{t / 60:.1f} min"
    if t < 7200:
        return f"{t / 60:.0f} min"
    return f"{t / 3600:.1f} h"


def fig12():
    p = "m4f12_"
    VB = (0, 0, 760, 420)
    s = H.Scale(VB[2], VB[3])
    x0, x1, yp0, ybase = 150.0, 330.0, 120.0, 350.0
    h0, n_st, eps_inf = ybase - yp0, 16, 0.10           # eps_inf = sigma0 / H_A, drawn at the 0.10 of the lab (line 769)
    ts = [0.0] + [10 ** (k * math.log10(20000) / 16) for k in range(17)]   # 1 s .. 20000 s, even in log t
    Ts = [D * t / H_M ** 2 for t in ts]
    Fs = [F_T(T_) if T_ > 0 else 1.0 for T_ in Ts]
    dU = [0.0] + [Fs[k - 1] - Fs[k] for k in range(1, len(ts))]
    dU[1] = 0.0                                          # 0+ -> 1 s is not a log step
    dmax = max(dU)
    dflt = min(range(len(ts)), key=lambda k: abs(Fs[k] - 0.5))
    fl = T["fluid"][1]
    pl = platen(s, x0, x1, -20, 20, 6) + "".join(H.arrow(s, p, x, -76, x, -22, "load") for x in (190, 240, 290))
    o = [f'<defs>{H.markers(p, s)}{fluid_marker(p, s)}<linearGradient id="{p}pg" x1="0" x2="1">'
         f'<stop offset="0" stop-color="{fl}" stop-opacity="0"/><stop offset="1" stop-color="{fl}" stop-opacity="0.62"/>'
         f'</linearGradient><g id="{p}pl">{pl}</g></defs>']
    o.append(chamber(s, x0, x1, yp0 - 46, ybase))
    o.append(H.label(s, (x0 + x1) / 2, 18, "held load", "label2", I["primary"], "middle"))
    o.append(H.label(s, 404, 136, "fluid pressure carries", "label2", I["primary"]))
    o.append(H.label(s, 404, 206, "solid matrix carries", "label2", I["primary"]))
    for k, (t, T_, F_) in enumerate(zip(ts, Ts, Fs)):
        fr = []
        pz = [p_ZT((i + 0.5) / n_st, T_) for i in range(n_st)]
        y = ybase
        strips = []
        for pi in pz:
            dz = h0 / n_st * (1 - eps_inf * (1 - pi))        # compressive strain eps_inf (1 - p / sigma0)
            strips.append((y - dz, dz, pi))
            y -= dz
        ytop = y
        fr.append(rect(x0, ytop, x1 - x0, ybase - ytop, T["cartilage"][0], T["cartilage"][1], 1.0))
        fr.append(f'<g fill="{fl}">' + "".join(f'<rect x="{x0:.0f}" y="{ys_:.1f}" width="{x1-x0:.0f}" height="{dz+0.3:.1f}" '
                                                 f'fill-opacity="{0.62 * max(0.0, pi):.2f}"/>' for ys_, dz, pi in strips) + "</g>")
        fr.append(f'<use href="#{p}pl" transform="translate(0 {ytop:.1f})"/>')
        if dU[k] > 0.004 * dmax:
            L = 10 + 44 * dU[k] / dmax
            for xh, dx in ((x0 + 15, -0.3), (x1 - 15, 0.3)):
                fr.append(fluid_arrow(s, p, xh, ytop - 22, xh + dx * L, ytop - 22 - L))
        # read-out (right)
        fr.append(H.label(s, 404, 70, f't = {fmt_t(t)}', "label", I["primary"]))
        fr.append(H.label(s, 404, 90, f'T = Dt / h² = {T_:.2g}' if T_ > 0 else "T = 0⁺ (load just applied)", "label2",
                          I["secondary"]))
        fr.append(rect(404, 144, 300 * F_, 18, fl, None, 0, 0, 'fill-opacity="0.62"'))
        fr.append(H.label(s, 704, 136, f'F = {F_:.3f}', "label2", I["primary"], "end"))
        fr.append(rect(404, 214, 300 * (1 - F_), 18, SOLID))
        fr.append(H.label(s, 704, 206, f'1 − F = {1 - F_:.3f}', "label2", I["primary"], "end"))
        msg = ("the fluid carries the load" if F_ > 0.9 else "the matrix carries the load" if F_ < 0.1
               else "fluid exudes; the matrix takes over")
        fr.append(H.label(s, 404, 262, msg, "label", I["primary"]))
        o.append(H.frame(k, dflt, "".join(fr)))
    o.append(H.label(s, 404, 282, "the platen settles by U = 1 − F", "label2", I["secondary"]))
    for y in (144, 214):
        o.append(rect(404, y, 300, 18, "none", I["rule"], 1.0))
    o.append(H.label(s, 404, 316, f'healthy cartilage: τ = h² / D ≈ {TAU:.0f} s ≈ {TAU / 3600:.1f} h', "label2", I["secondary"]))
    o.append(H.label(s, 404, 334, f'footstep, t = 1 s: F = {F1:.3f}', "label2", I["secondary"]))
    o.append(f'<rect x="20" y="{VB[3]-38}" width="60" height="10" fill="url(#{p}pg)" stroke="{I["rule"]}" stroke-width="0.8"/>')
    o.append(H.label(s, 86, VB[3] - 28, f'pore pressure {it("p")} / {it("σ")}₀ from 0 to 1 (Terzaghi series, §3); grey bar: porous platen', "label2", I["primary"]))
    o.append(H.label(s, 20, VB[3] - 8, f'settlement drawn for σ₀ / H{H.sub("A", s, "label2")} = {eps_inf:.2f};  '
                     "arrows: fluid leaving in each frame step (steps even in log t)", "label2", I["muted"]))
    vals = [fmt_t(t) for t in ts]
    aria = ("A cartilage plug in a rigid chamber under a held load, with a slider over time from 0 to 20000 seconds, in "
            "even steps of log time. Blue shading inside the plug is the computed pore pressure at each depth (Terzaghi "
            "series): at first uniform, then draining from the platen side, the base last. The plug compacts, the porous "
            "platen settles by U equals 1 minus F, and arrows show fluid leaving through the platen. Bars on the right give "
            "the share of the load carried by fluid pressure, F, and by the solid matrix, 1 minus F. Still frame: t about "
            f"{vals[dflt]}, F about {Fs[dflt]:.2f}.")
    extra = H.frames_attr("t", vals, dflt)
    return finish(VB, aria, s, o, extra)


# ================================================================ svg 13 (Fig. 12): finite-difference grid
def u_sym(s, i, n, size="label"):
    return f'{it("u")}{H.sub(i, s, size)}{sup(n, s, size)}'


def fig13():
    p = "m4f13_"
    VB = (0, 0, 760, 374)
    s = H.Scale(VB[2], VB[3])
    N, dy, yb = 10, 24.0, 300.0
    Y = lambda i: yb - dy * i                      # noqa: E731
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # the layer, with its N + 1 nodes
    sx0, sx1 = 52.0, 92.0
    o.append(rect(sx0, Y(N), sx1 - sx0, yb - Y(N), T["cartilage"][0], T["cartilage"][1], 1.0))
    o.append(rect(sx0 - 6, Y(N) - 14, sx1 - sx0 + 12, 14, GRID, I["axis"], 1.0))
    o.append(rect(sx0 - 6, yb, sx1 - sx0 + 12, 12, GRID, I["rule"], 1.0))
    o.append(hatch(sx0 - 6, yb + 12, sx1 + 6, yb + 20))
    cols = {0: I["primary"], N: O["load"]}
    for i in range(N + 1):
        o.append(circ((sx0 + sx1) / 2, Y(i), 4.2, cols.get(i, I["rule"]), "#fff", 1.0))
    o.append(H.label(s, sx0 - 10, Y(N) - 22, f'platen, {it("z")} = {it("h")}: {u_sym(s, "N", "")} = {it("U")}({it("t")}), the ramp',
                     "label2", I["primary"]))
    o.append(H.label(s, sx0 - 10, yb + 38, f'base, {it("z")} = 0: {u_sym(s, "0", "")} = 0 (pinned)', "label2", I["primary"]))
    xd = sx0 - 14
    o.append(H.line(s, xd, Y(4), xd, Y(5), O["geometry"], "geom", extra=f'marker-start="url(#{p}a_geometry)" '
                    f'marker-end="url(#{p}a_geometry)"'))
    o.append(H.label(s, xd - 4, (Y(4) + Y(5)) / 2 + 5, "Δz", "label2", I["primary"], "end"))
    # space-time grid: three time levels
    cx = [230.0, 340.0, 450.0]
    for i in range(N + 1):
        o.append(H.line(s, sx1 + 16, Y(i), cx[-1] + 24, Y(i), GRID, "leader"))
    for x in cx:
        o.append(H.line(s, x, Y(N) - 8, x, yb + 8, GRID, "leader"))
    i0 = 5
    st = {(1, i0 - 1), (1, i0), (1, i0 + 1)}
    for j, x in enumerate(cx):
        for i in range(N + 1):
            if (j, i) == (2, i0):
                continue
            c = O["geometry"] if (j, i) in st else cols.get(i, I["rule"])
            o.append(circ(x, Y(i), 5.2 if (j, i) in st else 4.2, c, "#fff", 1.0))
    for i in (i0 - 1, i0, i0 + 1):
        o.append(H.arrow(s, p, cx[1] + 7, Y(i), cx[2] - 9, Y(i0) + (Y(i) - Y(i0)) * 0.08, "dim", w="geom"))
    o.append(circ(cx[2], Y(i0), 7.0, O["flag"], "#fff", 1.4))
    o.append(H.label(s, cx[1] - 10, Y(i0 + 1) + 5, u_sym(s, "i+1", "n"), "label", I["primary"], "end"))
    o.append(H.label(s, cx[1] - 10, Y(i0) + 5, u_sym(s, "i", "n"), "label", I["primary"], "end"))
    o.append(H.label(s, cx[1] - 10, Y(i0 - 1) + 5, u_sym(s, "i−1", "n"), "label", I["primary"], "end"))
    o.append(H.label(s, cx[2] + 12, Y(i0) - 8, u_sym(s, "i", "n+1"), "label", I["primary"]))
    for x, t in zip(cx, ("n − 1", "n", "n + 1")):
        o.append(H.label(s, x, yb + 30, t, "label2", I["secondary"], "middle"))
    o.append(H.arrow(s, p, cx[0], yb + 46, cx[2] + 20, yb + 46, "dim", w="ref"))
    o.append(H.label(s, (cx[0] + cx[2]) / 2, yb + 62, "time level, step Δt", "label2", I["secondary"], "middle"))
    # the update rule
    ex = 488
    o.append(H.label(s, ex, 96, f'{u_sym(s, "i", "n+1")} = {u_sym(s, "i", "n")} + {it("r")} ({u_sym(s, "i−1", "n")} − '
                     f'2{u_sym(s, "i", "n")} + {u_sym(s, "i+1", "n")})', "label", I["primary"]))
    o.append(H.label(s, ex, 126, f'{it("r")} = {it("D")}Δ{it("t")} / Δ{it("z")}² ≤ ½ for stability', "label", I["primary"]))
    dz = H_M / N_LAB
    dt = R_LAB * dz ** 2 / D
    assert abs(dz * 1e6 - 40) < 1e-6 and abs(dt - 1.07) < 0.01
    o.append(H.label(s, ex + 32, 214, f'drawn: {it("N")} = {N}; the §5 lab: {it("N")} = {N_LAB},', "label2", I["secondary"]))
    o.append(H.label(s, ex + 32, 232, f'Δz = {dz * 1e6:.0f} µm, Δt ≈ {dt:.1f} s, r = {R_LAB}', "label2", I["secondary"]))
    lx = ex + 32
    lg, _ = legend(s, lx, 266, [(sw_dot(O["geometry"], "#fff"), "stencil at step n")], gap=12, cw=6.3)
    o.append(lg)
    o.append(legend(s, lx, 288, [(sw_dot(O["flag"], "#fff"), "updated node at n + 1")], gap=12, cw=6.3)[0])
    o.append(legend(s, lx, 310, [(sw_dot(I["primary"], "#fff"), "pinned"), (sw_dot(O["load"], "#fff"), "driven by the ramp")],
                    gap=12, cw=6.3)[0])
    o.append(legend(s, lx, 332, [(sw_dot(I["rule"], "#fff"), "interior node")], gap=12, cw=6.3)[0])
    aria = ("Finite-difference grid. Left: the cartilage layer as N plus 1 nodes, spacing delta z: the base node at z "
            "equals 0 is pinned, u 0 equals 0; the platen node at z equals h is driven by the ramp, u N equals U of t. "
            "Right: the nodes at time levels n minus 1, n and n plus 1; the three blue nodes i minus 1, i and i plus 1 at "
            "step n feed the orange node i at step n plus 1, the explicit three-point stencil u i n plus 1 equals u i n "
            "plus r times the second difference, with r equals D delta t over delta z squared at most one half. Ten "
            "intervals are drawn; the lab uses 50, delta z 40 micrometres, delta t about 1.1 seconds, r 0.4.")
    return finish(VB, aria, s, o)


# ================================================================ svg 19 (Fig. 17): four lubrication regimes
def fig19():
    p = "m4f19_"
    VB = (0, 0, 760, 276)
    s = H.Scale(VB[2], VB[3])
    o = [f'<defs>{H.markers(p, s)}{fluid_marker(p, s)}</defs>']
    gaps = (5, 12, 26, 4)
    names = ("Boundary", "Mixed", "Fluid-film", "Biphasic")
    lines = (("μ ≈ 0.15", "adsorbed lubricin and", "hyaluronic acid bear the load"),
             (f"μ falls to ≈ {MU_MIN:.2f}", "film patches and contact", ""),
             ("μ ≈ αS rises with ηU/N", "a full film separates them;", "friction is viscous drag"),
             (f"μ = μ{H.sub('eq', s)}(1 − F) ≈ {MU_FOOT:.3f}", "pressurized interstitial fluid", "carries the load (§4)"))
    ys = 118.0
    for i in range(4):
        px = 8 + i * 188
        cxp = px + 90
        g = gaps[i]
        o.append(H.label(s, cxp, 44, names[i], "label", I["primary"], "middle", 'font-weight="bold"'))
        # moving upper body: bone + cartilage, sliding at U under load N
        o.append(rect(px, ys - 32, 180, 14, T["bone"][0], T["bone"][1], 1.0))
        o.append(rect(px, ys - 18, 180, 18, T["cartilage"][0], T["cartilage"][1], 1.0))
        o.append(H.arrow(s, p, px + 12, 66, px + 62, 66, "dim", w="geom"))
        o.append(H.label(s, px + 68, 71, it("U"), "label2", I["primary"]))
        o.append(H.arrow(s, p, px + 160, 54, px + 160, ys - 34, "load"))
        o.append(H.label(s, px + 152, 70, it("N"), "label2", I["primary"], "end"))
        yl = ys + g
        o.append(rect(px, yl, 180, g, T["fluid"][0], None, 0, 0, 'fill-opacity="0.9"') if False else "")
        o.append(rect(px, ys, 180, g, T["fluid"][0], T["fluid"][1], 0.6))
        o.append(rect(px, yl, 180, 22, T["cartilage"][0], T["cartilage"][1], 1.0))
        o.append(rect(px, yl + 22, 180, 14, T["bone"][0], T["bone"][1], 1.0))
        if i == 0:                                       # adsorbed molecular layers nearly touching
            for x in range(px + 4, px + 178, 5):
                o.append(f'<path d="M{x},{ys:.1f} v2.4 M{x+2.5},{yl:.1f} v-2.4" stroke="{I["secondary"]}" stroke-width="1.1"/>')
        if i == 1:                                       # two asperity contacts, fluid between
            for xa in (px + 52, px + 128):
                o.append(rect(xa - 9, ys - 1, 18, g + 2, T["cartilage"][0]))
                o.append(f'<path d="M{xa-11},{ys:.1f} Q{xa},{ys+g+2:.1f} {xa+11},{ys:.1f} M{xa-11},{yl:.1f} '
                         f'Q{xa},{ys-2:.1f} {xa+11},{yl:.1f}" fill="none" stroke="{T["cartilage"][1]}" stroke-width="1"/>')
        if i == 2:                                       # Couette profile in the film
            for f_ in (0.25, 0.5, 0.75):
                yy = yl - f_ * g
                o.append(H.arrow(s, p, cxp - 40 * f_, yy, cxp + 40 * f_, yy, "dim", w="leader"))
        if i == 3:                                       # pressurized interstitial fluid in the lower layer
            o.append(rect(px, yl, 180, 22, T["fluid"][1], None, 0, 0, 'fill-opacity="0.42"'))
            for x in (px + 40, px + 90, px + 140):
                o.append(fluid_arrow(s, p, x, yl + 20, x, yl + 3, w="geom"))
        for j, (txt, size, colr) in enumerate(zip(lines[i], ("label", "label2", "label2"),
                                                 (I["primary"], I["secondary"], I["secondary"]))):
            if txt:
                o.append(H.label(s, cxp, 196 + j * 18, txt, size, colr, "middle"))
    # classical vs cartilage
    o.append(H.line(s, 12, 18, 552, 18, I["rule"], "leader"))
    o.append(H.label(s, 282, 13, "classical bearing: set by the Stribeck number S = ηU / N (low S → high S)", "label2",
                     I["secondary"], "middle"))
    o.append(H.line(s, 572, 18, 748, 18, I["rule"], "leader"))
    o.append(H.label(s, 660, 13, "cartilage: any S, even U = 0", "label2", I["secondary"], "middle"))
    lg, _ = legend(s, 12, 270, [(sw_rect(T["bone"][0], T["bone"][1]), "bone"), (sw_rect(T["cartilage"][0], T["cartilage"][1]), "cartilage"),
                                (sw_rect(T["fluid"][0], T["fluid"][1]), "synovial fluid"),
                                (sw_rect(T["fluid"][1], None, 0.42), "pressurized interstitial fluid"),
                                (sw_line(I["secondary"], 1.1), "adsorbed layer")], gap=12, cw=6.3)
    o.append(lg)
    aria = ("Four lubrication regimes, each a cartilage-capped body sliding at speed U under load N over cartilage. "
            "Boundary: the surfaces nearly touch and adsorbed lubricin and hyaluronic acid layers bear the load, friction "
            "about 0.15. Mixed: film patches and asperity contacts, friction falls to about 0.03. Fluid-film: a full film "
            "separates the surfaces and friction is viscous drag, rising with eta U over N. Biphasic: the pressurized "
            "interstitial fluid inside the lower cartilage carries the load, so friction is mu eq times 1 minus F, about "
            "0.002 for a 1 second step, at any sliding speed.")
    return finish(VB, aria, s, o)


# ================================================================ boxes (svg 24, 27)
def tbox(s, x, y, w, h, l1, l2="", l3="", accent=None):
    o = [sbox(s, x, y, w, h, accent)]
    n = 1 + bool(l2) + bool(l3)
    y0 = y + h / 2 - (n - 1) * 9 + 5
    o.append(H.label(s, x + w / 2, y0, l1, "label", I["primary"], "middle"))
    if l2:
        o.append(H.label(s, x + w / 2, y0 + 18, l2, "label2", I["secondary"], "middle"))
    if l3:
        o.append(H.label(s, x + w / 2, y0 + 36, l3, "label2", I["secondary"], "middle"))
    return "".join(o)


# ================================================================ svg 24 (Fig. 20): the osteoarthritis loop
def fig24():
    p = "m4f24_"
    VB = (0, 0, 760, 452)
    s = H.Scale(VB[2], VB[3])
    w, h = 236, 74
    pos = {"pg": (262, 10), "cf": (10, 118), "k": (514, 118), "F": (514, 262), "mu": (262, 368), "ov": (10, 262)}
    tau_oa = TAU / 1000
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(tbox(s, *pos["pg"], w, h, "proteoglycan loss", "aggrecanase, MMP cleave aggrecan"))
    o.append(tbox(s, *pos["cf"], w, h, f'↓ fixed charge {it("c")}{H.sub("F", s)}, ↓ swelling {it("π")}', "(§2) turgor lost,",
                  "collagen frays (fibrillation)"))
    o.append(tbox(s, *pos["k"], w, h, f'↑ permeability {it("k")}, ↓ gel time {it("τ")}', "(§3) k × 1000:",
                  f'τ = {TAU:.0f} s → {tau_oa:.1f} s'))
    o.append(tbox(s, *pos["F"], w, h, f'↓ fluid load support {it("F")}', f'(§4) F(1 s): {F1:.3f} → {F1_OA:.2f}'))
    o.append(tbox(s, *pos["mu"], w, h, f'↑ friction {it("μ")}, ↑ contact peak', f'(§7) μ: {MU_FOOT:.3f} → {MU_OA:.3f}',
                  f'(§6) peak: {P_BIPH / 1e6:.1f} → {P0_OA / 1e6:.1f} MPa'))
    o.append(tbox(s, *pos["ov"], w, h, "matrix overload + wear", "the weakened solid", "takes the stress"))

    def edge(a, b, fa, fb):
        (ax, ay), (bx, by) = pos[a], pos[b]
        return H.arrow(s, p, ax + fa[0] * w, ay + fa[1] * h, bx + fb[0] * w, by + fb[1] * h, "dim", w="geom")
    o.append(edge("pg", "cf", (0.05, 1.0), (0.85, -0.06)))
    o.append(edge("pg", "k", (0.95, 1.0), (0.15, -0.06)))
    o.append(edge("k", "F", (0.5, 1.0), (0.5, -0.08)))
    o.append(edge("F", "mu", (0.2, 1.06), (1.02, 0.25)))
    o.append(edge("mu", "ov", (-0.02, 0.25), (0.8, 1.06)))
    o.append(edge("cf", "ov", (0.5, 1.0), (0.5, -0.08)))
    o.append(edge("ov", "pg", (0.94, -0.02), (0.18, 1.06)))
    o.append(H.label(s, 386, 196, f'loop gain {it("G")}', "label", I["primary"], "middle", 'font-weight="bold"'))
    o.append(H.label(s, 386, 216, f'runs away only if {it("G")} > 1', "label2", I["primary"], "middle"))
    o.append(H.label(s, 386, 236, f'mechanical link: ∂ln {it("d")} / ∂ln {it("k")} = ½', "label2", I["secondary"], "middle"))
    o.append(H.label(s, 386, 254, f'({it("d")} = 1 − {it("F")}; the biological links:', "label2", I["secondary"], "middle"))
    o.append(H.label(s, 386, 272, "Module 14)", "label2", I["secondary"], "middle"))
    aria = ("The osteoarthritis loop, six boxes joined by arrows. Proteoglycan loss, by aggrecanase and MMP, branches two "
            "ways. One: fixed charge and swelling pressure fall (section 2), turgor is lost and collagen frays. Two: "
            "permeability rises and gel time falls (section 3), for a thousandfold k from 6667 to 6.7 seconds; fluid load "
            "support falls (section 4), F at 1 second from 0.986 to 0.56; friction rises from 0.002 to 0.066 (section 7) "
            "and the contact peak from 2.0 to 3.2 megapascals (section 6). Both branches end in matrix overload and wear, "
            "which drives more proteoglycan loss. Centre: the loop runs away only if its gain G exceeds 1; the mechanical "
            "link contributes the half power of d against k.")
    return finish(VB, aria, s, o)


# ================================================================ svg 27 (Fig. 23): one idea, six phenomena
def fig27():
    p = "m4f27_"
    VB = (0, 0, 760, 452)
    s = H.Scale(VB[2], VB[3])
    w, h = 220, 66
    sig_ratio = 2 * H_M / math.sqrt(math.pi * D * 200.0)            # line 861: peak / equilibrium, t0 = 200 s
    assert abs(sig_ratio - 6.515) < 0.001
    boxes = [((270, 6), "resting swelling pre-stress", f'(§2) π ≈ {PI_SW / 1e6:.2f} MPa, no load'),
             ((530, 92), "fluid carries the load", f'(§4) F(1 s) = {F1:.3f}'),
             ((530, 296), "stress relaxation and creep", f'(§5) peak ≈ {sig_ratio:.1f} σ∞, over τ ≈ {TAU / 3600:.1f} h'),
             ((270, 382), "flattened contact pressure", f'(§6) peak {P0_HERTZ / 1e6:.1f} → {P_BIPH / 1e6:.1f} MPa, same load'),
             ((10, 296), "sub-ice friction", f'(§7) μ = μ{H.sub("eq", s, "label2")}(1 − F) ≈ {MU_FOOT:.3f}'),
             ((10, 92), "osteoarthritis = lost support", f'(§8) k × 1000: F(1 s) → {F1_OA:.2f}')]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    cx, cy, rx, ry = 380.0, 226.0, 170.0, 66.0
    o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{T["cartilage"][0]}" stroke="{T["fluid"][1]}" '
             f'stroke-width="{s(1.6):.2f}"/>')
    o.append(H.label(s, cx, cy - 24, "a charged, fluid-filled porous solid", "label", I["primary"], "middle", 'font-weight="bold"'))
    o.append(H.label(s, cx, cy + 2, f'∂{it("u")}/∂{it("t")} = {it("H")}{H.sub("A", s)}{it("k")} ∂²{it("u")}/∂{it("z")}²  (§3)',
                     "label", I["primary"], "middle"))
    o.append(H.label(s, cx, cy + 26, f'drains over τ = h² / (H{H.sub("A", s, "label2")}k) ≈ {TAU:.0f} s', "label2",
                     I["secondary"], "middle"))
    for (x, y), t1, t2 in boxes:
        o.append(tbox(s, x, y, w, h, t1, t2))
        bx, by = x + w / 2, y + h / 2
        ang = math.atan2((by - cy) / ry, (bx - cx) / rx)
        sx_, sy_ = cx + rx * math.cos(ang), cy + ry * math.sin(ang)
        # end on the box edge nearest the ellipse
        ex = min(max(sx_, x), x + w) if abs(bx - cx) < 1 else (x + w + 4 if bx < cx else x - 4)
        ey = (y + h + 4 if by < cy else y - 4) if abs(bx - cx) < 1 else min(max(by + (sy_ - by) * 0.55, y + 8), y + h - 8)
        if abs(bx - cx) < 1:
            ex = cx
        o.append(H.arrow(s, p, sx_, sy_, ex, ey, "dim", w="geom"))
    aria = ("Hub diagram: at the centre, a charged, fluid-filled porous solid obeying the consolidation equation, partial "
            "u by partial t equals H A k times the second z derivative of u (section 3), draining over tau about 6667 "
            "seconds. Arrows lead to six phenomena: resting swelling pre-stress, about 0.16 megapascals (section 2); fluid "
            "carries the load, F at 1 second 0.986 (section 4); stress relaxation and creep, peak about 6.5 times the "
            "equilibrium stress, over about 1.9 hours (section 5); flattened contact pressure, peak 2.5 to 2.0 "
            "megapascals at the same load (section 6); sub-ice friction, about 0.002 (section 7); osteoarthritis as lost "
            "support, F at 1 second falling to 0.56 for a thousandfold permeability (section 8).")
    return finish(VB, aria, s, o)


FIGS = {
    1: ("Osteochondral unit: subchondral bone, calcified cartilage, h", fig1),
    2: ("Cross-section of a synovial joint: two bone ends each capped", fig2),
    4: ("Microstructure of articular cartilage: a hydrated layer on s", fig4),
    5: ("Donnan equilibrium schematic: a cartilage compartment holdin", fig5),
    7: ("Confined-compression test: a cartilage plug of thickness h i", fig7),
    8: ("Effective-stress partition: the total stress applied to a ti", fig8),
    12: ("Animation: a cartilage plug under a suddenly applied and hel", fig12),
    13: ("Finite-difference grid for the cartilage layer: nodes from t", fig13),
    17: ("A femoral condyle pressing on the cartilage-covered tibial p", fig17),
    19: ("Four lubrication regimes between a sliding surface and carti", fig19),
    24: ("The osteoarthritis feedback loop: proteoglycan loss lowers f", fig24),
    27: ("Hub diagram: a charged, fluid-filled porous solid governed b", fig27),
}
