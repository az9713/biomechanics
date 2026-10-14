"""Module 2, group `bone`: the figures that show a real femur, in the house style.

Main text (760 px): svg #1 (Fig. 1 femur landmarks, neck-shaft angle), #6 (Fig. 5 torsion, spiral crack).
Problem figures (400 px): #15 C4, #20 C9, #21 C10, #32 K1, #48 K9, #50 K10.
Art: NIH NIAID BioArt 244 (public domain). One femur fill path (the m00 crop, crop_art.py ... m00femur) is put on
the page once by SHARED_DEFS() as #m2art_femur and <use>d; #1 draws its proximal end cut from the same path, #50
the same path bent by the computed deflection, #21 a crop of the hip (crop_art.py ../svg_paths/nih_upper_leg.svg
m02hip 0 25 112 118). #15 (C4 names the tibia) draws the InjuryMap tibia (CC BY-SA 4.0, crop m02tibia). Colours, one meaning each (as m02/beam.py): tension = SERIES[0] red, compression = SERIES[1]
blue, applied load or torque = load brown, axes and angles = geometry blue, joint force = reaction black.
Every plotted number is computed here from the value or the K-problem script module02.html states (line numbers
beside each constant; the scripts are ported line for line and their printed numbers asserted).
"""
import math
import re

import numpy as np
from scipy.optimize import minimize

import house as H
from m00.tissue import FEMUR_ART, femur_d
from m05.body import KIT, _read, art_image, finish, fit_circle, inner_svg, wrap
from m05.plots_prob import Plot, hov
from m05.plots_prob import label as plabel
from m05.plots_prob import legend as plegend
from m05.tissue import circ, path, rect

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
TEN, COM = SER[0], SER[1]
BONE, BONE_L = T["bone"]
GRID, BOX = "#e6e6e6", "#f7f4ef"
FEMUR_ID = "m2art_femur"                       # page-global id: the femur path is on the page once
NSA = 125.0                                    # neck-shaft angle, deg (line 105: assumed adult value)


def it(t):
    return f'<tspan font-style="italic">{t}</tspan>'


def sup(t, s, size="label2"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def credit(s, vb, n, changes):
    cr = H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt (Ryan Kissinger)", title="Human Upper Leg Bones (BioArt 244)",
                                    changes=changes)
    lines = wrap(cr, n)
    return H.credit(s, 8, vb[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines)


# ---------------------------------------------------------------- the femur path: parse, sample, measure
NUM = re.compile(r'[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?')
NARG = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "A": 7}


def segments(d):
    """Path data -> [('M'|'L', [p]) | ('C', [c1, c2, p]) | ('Z', [])] in absolute coordinates.
    Q becomes the equal cubic; an arc A becomes a line to its end point (used to measure, never to draw)."""
    tok, out, i, cmd = re.findall(r'[A-Za-z]|' + NUM.pattern, d), [], 0, None
    cx = cy = sx = sy = 0.0
    while i < len(tok):
        if tok[i].isalpha():
            cmd, i = tok[i], i + 1
            if cmd in "Zz":
                out.append(("Z", []))
                cx, cy = sx, sy
                continue
        C, n = cmd.upper(), NARG[cmd.upper()]
        a = [float(v) for v in tok[i:i + n]]
        i += n
        ox, oy = (cx, cy) if cmd.islower() else (0.0, 0.0)
        if C == "M":
            cx, cy = sx, sy = a[0] + ox, a[1] + oy
            out.append(("M", [(cx, cy)]))
            cmd = "l" if cmd.islower() else "L"
        elif C in "LHVA":
            cx = a[-2 if C == "A" else 0] + ox if C in "LHA" else cx
            cy = a[-1] + oy if C in "LVA" else cy
            out.append(("L", [(cx, cy)]))
        elif C == "Q":
            q, e = (a[0] + ox, a[1] + oy), (a[2] + ox, a[3] + oy)
            out.append(("C", [(cx + 2 / 3 * (q[0] - cx), cy + 2 / 3 * (q[1] - cy)),
                              (e[0] + 2 / 3 * (q[0] - e[0]), e[1] + 2 / 3 * (q[1] - e[1])), e]))
            cx, cy = e
        else:
            if C == "S":
                pc = out[-1][1][1] if out[-1][0] == "C" else (cx, cy)
                c1, a = (2 * cx - pc[0], 2 * cy - pc[1]), [0, 0] + a
            else:
                c1 = (a[0] + ox, a[1] + oy)
            c2 = (a[2] + ox, a[3] + oy)
            cx, cy = a[4] + ox, a[5] + oy
            out.append(("C", [c1, c2, (cx, cy)]))
    return out


def emit(segs, f):
    """Segments -> path data, every point mapped by f (a smooth map keeps Bezier control points valid)."""
    o = []
    for k, ps in segs:
        o.append(k + " ".join(f"{x:.1f},{y:.1f}" for x, y in map(f, ps)) if ps else "Z")
    return "".join(o)


def sample(segs, n=8):
    pts, cur = [], None
    for k, ps in segs:
        if k in "ML":
            cur = ps[0]
            pts.append(cur)
        elif k == "C":
            p0, (c1, c2, p3) = cur, ps
            for i in range(1, n + 1):
                t = i / n
                m = 1 - t
                pts.append(tuple(m ** 3 * a + 3 * m * m * t * b + 3 * m * t * t * c + t ** 3 * e
                                 for a, b, c, e in zip(p0, c1, c2, p3)))
            cur = p3
    return pts


SEGS = segments(femur_d())
OUT = sample(SEGS)                              # 425 outline points, art units


def edges(ay):
    """Lateral and medial outline x of the art at height ay (first and last crossing)."""
    xs = sorted(a[0] + (ay - a[1]) / (b[1] - a[1]) * (b[0] - a[0])
                for a, b in zip(OUT, OUT[1:] + OUT[:1]) if (a[1] - ay) * (b[1] - ay) < 0)
    return xs[0], xs[-1]


HEAD = fit_circle(OUT[14:50])                   # head arc of the art: centre (45.8, 57.2), r 15.05 art units
SHAFT_A = (sum(edges(110)) / 2, 110.0)          # shaft axis through the mid-shaft at two levels (art units)
SHAFT_B = (sum(edges(200)) / 2, 200.0)
ART_L = FEMUR_ART[3] - FEMUR_ART[1]             # femur length in art units (head top to condyles)
assert abs(HEAD[2] - 15.05) < 0.05 and abs(SHAFT_A[0] - 29.06) < 0.02


class Femur:
    """Vertical femur placed by its art bbox: top-left (x0, y0) and height h (or scale k)."""

    ed = staticmethod(edges)

    def __init__(self, x0, y0, h=None, k=None, kx=None):
        self.k = k or h / ART_L
        self.kx = kx or self.k
        self.tx, self.ty = x0 - FEMUR_ART[0] * self.kx, y0 - FEMUR_ART[1] * self.k

    def P(self, ax, ay):
        return self.tx + ax * self.kx, self.ty + ay * self.k

    def use(self, s, fill=BONE, stroke=BONE_L, extra=""):
        sw = s(H.PX["art_line"]) / min(self.k, self.kx)
        return (f'<use href="#{FEMUR_ID}" transform="translate({self.tx:.2f} {self.ty:.2f}) scale({self.kx:.4f} {self.k:.4f})" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="{sw:.2f}" stroke-linejoin="round" {extra}/>')

    def shaft(self, ay):
        """Screen centre x and half-width of the shaft at art height ay."""
        a, b = self.ed(ay)
        return self.tx + (a + b) / 2 * self.kx, (b - a) / 2 * self.kx


def SHARED_DEFS():
    """The femur fill path, once per page (no fill or stroke: each <use> sets them)."""
    return f'<path id="{FEMUR_ID}" d="{femur_d()}"/>'


# ---------------------------------------------------------------- torsion marks
def torque(s, p, cx, cy, rx, front_left, lab, lab_side=1):
    """A torque about a vertical shaft axis, drawn as an ellipse arc round the shaft (front half in front of it).
    front_left: the front of the arc moves to the left. Head at the back edge; label beside it."""
    ry = rx * 0.32
    ths = np.radians(np.linspace(-40, 195, 48) if front_left else np.linspace(220, -15, 48))
    pts = [(cx + rx * math.cos(t), cy + ry * math.sin(t)) for t in ths]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    o = path(d, O["load"], s(H.PX["load"]), extra=f'marker-end="url(#{p}a_load)" stroke-linecap="round"')
    lx = cx + lab_side * (rx + s(10))
    return o + H.label(s, lx, cy + s(5), lab, "label", I["primary"], "start" if lab_side > 0 else "end")


def helix(s, F, ay0, ay1, phi0=0.0):
    """A 45-degree helical crack on the shaft, from art height ay0 up to ay1 (ay1 < ay0). On a cylinder of radius R
    the helix advances R per radian along the axis, so its trace crosses the front centre line at 45 degrees.
    Returns (front path, back path, front-centre crossings in screen units)."""
    R = np.mean([(lambda e: (e[1] - e[0]) / 2)(F.ed(a)) for a in np.linspace(ay1, ay0, 9)])
    n = int((ay0 - ay1) / R / 0.04)
    front, back, runs, cross = [], [], [], []
    for i in range(n + 1):
        phi = phi0 + i * 0.04
        ay = ay0 - R * (phi - phi0)
        a, b = F.ed(ay)
        c, r = (a + b) / 2, (b - a) / 2
        pt = F.P(c + r * math.sin(phi), ay)
        vis = math.cos(phi) > 0
        if not runs or runs[-1][0] != vis:
            runs.append((vis, [runs[-1][1][-1]] if runs else []))
        runs[-1][1].append(pt)
        if i and math.floor(phi / (2 * math.pi)) != math.floor((phi - 0.04) / (2 * math.pi)):
            cross.append(pt)
    for vis, q in runs:
        (front if vis else back).append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in q))
    return "".join(front), "".join(back), cross


def crack(s, F, ay0, ay1, phi0=0.0):
    f, b, cross = helix(s, F, ay0, ay1, phi0)
    return (path(b, I["muted"], s(1.2), extra=f'stroke-dasharray="{s(3):.1f} {s(2.5):.1f}" stroke-linecap="round"')
            + path(f, I["primary"], s(2.4), extra='stroke-linecap="round" stroke-linejoin="round"')), cross


def angle_mark(s, x, y, r, a0, a1, col):
    """Arc of radius r about (x, y) from screen angle a0 to a1 (deg, y down), short way."""
    p0 = (x + r * math.cos(math.radians(a0)), y + r * math.sin(math.radians(a0)))
    p1 = (x + r * math.cos(math.radians(a1)), y + r * math.sin(math.radians(a1)))
    sweep = 1 if (a1 - a0) % 360 < 180 else 0
    return path(f"M{p0[0]:.1f},{p0[1]:.1f} A{r:.1f},{r:.1f} 0 0 {sweep} {p1[0]:.1f},{p1[1]:.1f}", col, s(H.PX["geom"]))


# ================================================================ svg #1  Fig. 1: femur landmarks and neck-shaft angle
def neck_geometry():
    """Neck axis through the fitted head centre at NSA to the distal shaft axis; returns (P on shaft axis, unit
    vectors toward the head and down the shaft) in art units."""
    dx, dy = SHAFT_B[0] - SHAFT_A[0], SHAFT_B[1] - SHAFT_A[1]
    a_sh = math.atan2(dy, dx)                                  # screen angle of the distal shaft direction
    a_nk = a_sh - math.radians(NSA)                            # rotate toward the medial side (right, up)
    un, us = (math.cos(a_nk), math.sin(a_nk)), (math.cos(a_sh), math.sin(a_sh))
    # P = HEAD - t un lies on the shaft axis A + u us
    hx, hy = HEAD[0] - SHAFT_A[0], HEAD[1] - SHAFT_A[1]
    det = -un[0] * us[1] + un[1] * us[0]
    t = (-hx * us[1] + hy * us[0]) / det
    return (HEAD[0] - t * un[0], HEAD[1] - t * un[1]), un, us, math.degrees(a_sh), math.degrees(a_nk)


def proximal_d(f, ycut=150.0):
    """The art outline above ycut (the femur cut across the shaft), points mapped by f."""
    pts = sample(SEGS, 12)                                    # denser, so the enlarged outline stays smooth
    i1 = next(i for i, q in enumerate(pts) if q[1] > ycut)     # medial edge leaves the window
    i2 = max(i for i, q in enumerate(pts) if q[1] > ycut) + 1  # lateral edge re-enters it
    ea, eb = edges(ycut)
    q = pts[:i1] + [(eb, ycut), (ea, ycut)] + pts[i2:]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in map(f, q)) + "Z"


def fig1():
    p = "m2f1_"
    VB = (0, 0, 760, 520)
    s = H.Scale(VB[2], VB[3])
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # ---- left: the whole femur (anterior view)
    F = Femur(118.0, 34.0, h=440.0)
    o.append(F.use(s))
    lab = lambda x, y, t, a="start", c=I["primary"], z="label2": H.label(s, x, y, t, z, c, a)  # noqa: E731
    lead = lambda a, b: H.line(s, a[0], a[1], b[0], b[1], I["secondary"], "leader")  # noqa: E731
    hd = F.P(HEAD[0] + 6, HEAD[1] - 12)
    o += [lead(hd, (hd[0] + 30, hd[1] - 6)), lab(hd[0] + 33, hd[1] - 3, "head")]
    gt = F.P(17, 52)
    o += [lead(gt, (gt[0] - 30, gt[1] - 6)), lab(gt[0] - 33, gt[1] - 9, "greater", "end"),
          lab(gt[0] - 33, gt[1] + 6, "trochanter (GT)", "end")]
    lt = F.P(48.5, 84)
    o += [lead(lt, (lt[0] + 30, lt[1] + 4)), lab(lt[0] + 33, lt[1] + 2, "lesser"), lab(lt[0] + 33, lt[1] + 17, "trochanter")]
    sh = F.P(edges(220)[1], 220)
    o += [lead(sh, (sh[0] + 30, sh[1])), lab(sh[0] + 33, sh[1] + 5, "shaft (cortical tube)")]
    cd = F.P(66, 360)
    o += [lead(cd, (cd[0] + 26, cd[1] + 8)), lab(cd[0] + 29, cd[1] + 12, "condyles (knee)")]
    o.append(lab(F.P(29, 41)[0], 20, "anterior view", "middle", I["secondary"]))
    o.append(lab(F.P(7, 0)[0] - 8, F.P(0, 290)[1], "lateral", "end", I["muted"]))
    o.append(lab(F.P(56, 0)[0] + 8, F.P(0, 290)[1], "medial", "start", I["muted"]))
    # zoom window on the proximal end
    zx0, zy0 = F.P(4, 36)
    zx1, zy1 = F.P(66, 150)
    o.append(f'<rect x="{zx0:.1f}" y="{zy0:.1f}" width="{zx1 - zx0:.1f}" height="{zy1 - zy0:.1f}" fill="none" '
             f'stroke="{I["axis"]}" stroke-width="{s(1.2):.2f}"/>')
    # ---- right: the proximal end, 3.7 x larger, with the axes
    K, X0, Y0 = 3.7, 404.0, 38.0
    f = lambda q: (X0 + (q[0] - 4) * K, Y0 + (q[1] - 36) * K)  # noqa: E731
    o.append(path(proximal_d(f), BONE_L, s(H.PX["art_line"]), fill=BONE, extra='stroke-linejoin="round"'))
    da = f'stroke-dasharray="{s(5):.1f} {s(3):.1f}"'
    bx0, bx1 = f((4, 36))[0], f((66, 150))[0]
    o.append(path(f"M{zx1:.1f},{zy0:.1f} L{bx0 - 8:.1f},{Y0:.1f} M{zx1:.1f},{zy1:.1f} L{bx0 - 8:.1f},{f((0, 150))[1]:.1f}",
                  I["rule"], s(1.1), extra=da))
    Pq, un, us, a_sh, a_nk = neck_geometry()
    Pp, Hc = f(Pq), f(HEAD[:2])
    rh = HEAD[2] * K
    o.append(circ(Hc[0], Hc[1], rh, "none", BONE_L, s(1.2), f'stroke-dasharray="{s(4):.1f} {s(3):.1f}"'))
    shaft_end = f((SHAFT_A[0] + us[0] * (148 - SHAFT_A[1]) / us[1], 148))
    nk_end = (Hc[0] + un[0] * (rh + 34), Hc[1] + un[1] * (rh + 34))
    o.append(H.line(s, Pp[0], Pp[1], shaft_end[0], shaft_end[1], O["geometry"], "geom", H.DASH_REF))
    o.append(H.line(s, Pp[0], Pp[1], nk_end[0], nk_end[1], O["geometry"], "geom", H.DASH_REF))
    o.append(angle_mark(s, Pp[0], Pp[1], 46, a_sh, a_nk, O["geometry"]))
    o.append(H.joint_centre(s, Hc[0], Hc[1]))
    am = math.radians((a_sh + a_nk) / 2)
    o.append(H.label(s, Pp[0] + 56 * math.cos(am) + 4, Pp[1] + 56 * math.sin(am) + 8, f"{NSA:.0f}°", "label", I["primary"]))
    o.append(lab(nk_end[0] + 6, nk_end[1] - 4, "neck axis"))
    o.append(lab(shaft_end[0] + 8, shaft_end[1] - 6, "shaft axis"))
    o.append(lab(Hc[0] + 36, Hc[1] + rh + 34, "head centre (circle", "start", I["secondary"]))
    o.append(lab(Hc[0] + 36, Hc[1] + rh + 50, "fitted to the head outline)", "start", I["secondary"]))
    o.append(lead((Hc[0] + 6, Hc[1] + 6), (Hc[0] + 33, Hc[1] + rh + 30)))
    nq = f((38, 60))
    o += [lead(nq, (nq[0] - 40, Y0 - 4)), lab(nq[0] - 40, Y0 - 8, "neck", "middle")]
    gq = f((14, 64))
    o += [lab(gq[0], gq[1], "GT", "middle")]
    lq = f((48.6, 86))
    o += [lead(lq, (lq[0] + 26, lq[1] + 10)), lab(lq[0] + 29, lq[1] + 15, "lesser trochanter")]
    o.append(H.label(s, 604, 330, "neck-shaft angle", "label", I["primary"]))
    o.append(H.label(s, 604, 348, f"≈ {NSA:.0f}°, typical adult value", "label2", I["secondary"]))
    o.append(credit(s, VB, 130, "One femur, recoloured; proximal end enlarged. Axes, angle and head circle drawn for "
                                "this course."))
    aria = ("Anterior view of a femur (NIH BioArt, public domain). Left: the whole bone with its landmarks: the head at the "
            "top on the medial side, the neck, the greater trochanter on the lateral side, the lesser trochanter below the "
            "neck, the shaft (a cortical tube), and the condyles at the knee. A box on the upper end is enlarged on the "
            f"right, where a dashed circle fitted to the head outline marks the head centre, and two blue dashed lines, the "
            f"neck axis through the head centre and the shaft axis down the middle of the shaft, meet at the neck-shaft "
            f"angle of about {NSA:.0f} degrees, the typical adult value.")
    return finish(VB, aria, s, o)


# ================================================================ svg #6  Fig. 5: torsion of the femoral shaft
def element(s, p, cx, cy, a, sense=1):
    """Pure-shear surface element (side a) under the torque of fig6/fig15: top face shear to the left (sense=1).
    Principal tension sigma1 = +tau on the diagonal the shear arrows converge on, compression sigma2 = -tau on the
    other; the crack runs perpendicular to sigma1."""
    x0, y0 = cx - a / 2, cy - a / 2
    o = [rect(x0, y0, a, a, BONE, BONE_L, s(1.4))]
    g, e = s(9), a * 0.16
    sh = [((x0 + a - e, y0 - g), (x0 + e, y0 - g)), ((x0 + e, y0 + a + g), (x0 + a - e, y0 + a + g)),
          ((x0 - g, y0 + a - e), (x0 - g, y0 + e)), ((x0 + a + g, y0 + e), (x0 + a + g, y0 + a - e))]
    for (u, v) in sh:
        if sense < 0:
            u, v = v, u
        o.append(H.arrow(s, p, u[0], u[1], v[0], v[1], "dim", w="geom"))
    o.append(H.label(s, cx, y0 - g - 8, it("τ"), "label", I["primary"], "middle"))
    o.append(H.label(s, x0 + a + g + 7, cy + 5, it("τ"), "label", I["primary"]))
    q = 1 / math.sqrt(2)
    t1, t2 = (q, q), (q, -q)                  # tension along top-left -> bottom-right (screen), compression across
    r0, r1 = a * 0.28, a * 0.62
    for sg in (1, -1):
        o.append(H.arrow(s, p, cx + sg * t1[0] * r0, cy + sg * t1[1] * r0, cx + sg * t1[0] * r1, cy + sg * t1[1] * r1, "force"))
        o.append(H.line(s, cx + sg * t2[0] * r1, cy + sg * t2[1] * r1, cx + sg * t2[0] * (r0 + s(2)), cy + sg * t2[1] * (r0 + s(2)),
                        COM, "force", extra=f'marker-end="url(#{p}a_geometry)"'))
    c = a * 0.22
    o.append(H.line(s, cx - t2[0] * c, cy - t2[1] * c, cx + t2[0] * c, cy + t2[1] * c, I["primary"], "force",
                    extra='stroke-linecap="round"'))
    return "".join(o), (cx + t1[0] * r1, cy + t1[1] * r1), (cx + t2[0] * r1, cy + t2[1] * r1)


def fig6():
    p = "m2f6_"
    VB = (0, 0, 760, 470)
    s = H.Scale(VB[2], VB[3])
    o = [f'<defs>{H.markers(p, s)}</defs>']
    F = Femur(150.0, 26.0, h=400.0)
    o.append(F.use(s))
    # torque pair: top of the shaft turned counter-clockwise seen from above (front moves left), bottom opposite
    for ay, fl, lab in ((100.0, True, f'{it("T")}'), (318.0, False, f'{it("T")}')):
        cx, hw = F.shaft(ay)
        cy = F.P(0, ay)[1]
        o.append(torque(s, p, cx, cy, hw * 2.1, fl, lab, 1))
    o.append(H.label(s, F.P(66, 0)[0] + 30, F.P(0, 104)[1] + 22, "torque", "label2", I["secondary"]))
    o.append(H.label(s, F.P(66, 0)[0] + 30, F.P(0, 322)[1] + 22, "equal and opposite", "label2", I["secondary"]))
    cr, cross = crack(s, F, 270.0, 150.0)
    o.append(cr)
    # 45 degrees between the crack trace and the shaft axis, at a front-centre crossing
    cx0, cy0 = cross[0]
    o.append(H.line(s, cx0, cy0 + 26, cx0, cy0 - 40, O["geometry"], "geom", H.DASH_REF))
    o.append(angle_mark(s, cx0, cy0, 24, -90, -45, O["geometry"]))
    o.append(H.label(s, cx0 + 8, cy0 - 30, "45°", "label", I["primary"]))
    lx = F.P(0, 0)[0] - 30
    o.append(H.line(s, cx0 - 12, cy0 + 26, lx + 4, cy0 + 40, I["secondary"], "leader"))
    o.append(H.label(s, lx, cy0 + 38, "spiral crack:", "label2", I["primary"], "end"))
    o.append(H.label(s, lx, cy0 + 54, "a 45° helix", "label2", I["primary"], "end"))
    o.append(H.label(s, lx, cy0 + 70, "(dashed: back face)", "label2", I["secondary"], "end"))
    # surface element on the front centre line, magnified on the right
    ex, ey = F.shaft(128.0)[0], F.P(0, 128.0)[1]
    ew = 9.0
    o.append(f'<rect x="{ex - ew / 2:.1f}" y="{ey - ew / 2:.1f}" width="{ew}" height="{ew}" fill="none" '
             f'stroke="{I["axis"]}" stroke-width="{s(1.2):.2f}"/>')
    A, CX, CY = 128.0, 556.0, 210.0
    da = f'stroke-dasharray="{s(5):.1f} {s(3):.1f}"'
    o.append(path(f"M{ex + ew / 2:.1f},{ey - ew / 2:.1f} L{CX - A / 2 - 30:.1f},{CY - A / 2:.1f} M{ex + ew / 2:.1f},{ey + ew / 2:.1f} "
                  f"L{CX - A / 2 - 30:.1f},{CY + A / 2:.1f}", I["rule"], s(1.1), extra=da))
    el, t_end, c_end = element(s, p, CX, CY, A)
    o.append(el)
    o.append(H.label(s, CX, CY - A / 2 - 40, "surface element: pure shear", "label", I["primary"], "middle"))
    o.append(H.label(s, t_end[0] + 8, t_end[1] + 18, f'{it("σ")}₁ = +{it("τ")}', "label", I["primary"]))
    o.append(H.label(s, t_end[0] + 8, t_end[1] + 34, "principal tension", "label2", I["secondary"]))
    o.append(H.label(s, c_end[0] + 8, c_end[1] - 16, f'{it("σ")}₂ = −{it("τ")}', "label", I["primary"]))
    o.append(H.label(s, c_end[0] + 8, c_end[1] - 32, "compression", "label2", I["secondary"]))
    ax_x = CX - A / 2 - 50
    o.append(H.arrow(s, p, ax_x, CY + 34, ax_x, CY - 34, "dim", w="ref"))
    o.append(H.label(s, ax_x - 6, CY + 5, "shaft", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax_x - 6, CY + 21, "axis", "label2", I["secondary"], "end"))
    o.append(H.label(s, CX, CY + A / 2 + 46, "the crack opens across σ₁, along the other diagonal:", "label2", I["primary"], "middle"))
    o.append(H.label(s, CX, CY + A / 2 + 64, "at 45° to the axis, which wraps the shaft as a helix", "label2", I["primary"], "middle"))
    from m05.tissue import legend, sw_line
    lg, _ = legend(s, 346, 412, [(sw_line(O["load"]), "torque"), (sw_line(I["secondary"], 2.0), "shear τ"),
                                 (sw_line(TEN), "tension"), (sw_line(COM), "compression"), (sw_line(I["primary"]), "crack")],
                   gap=12)
    o.append(lg)
    o.append(credit(s, VB, 130, "One femur, recoloured. Torque, crack and stress element drawn for this course."))
    aria = ("Left: a femur (NIH BioArt, anterior view) twisted by a torque T: brown arrows round the upper shaft turn it one "
            "way and equal and opposite arrows round the lower shaft turn it the other. A dark crack winds round the shaft "
            "as a 45-degree helix, solid on the front face and dashed on the back; a blue mark shows the crack trace at 45 "
            "degrees to the shaft axis. A small square on the shaft surface is enlarged on the right: a bone element in "
            "pure shear tau (grey arrows on its four faces). Along one diagonal the shear resolves into principal tension "
            "sigma 1 = plus tau (red arrows pointing out), along the other into compression sigma 2 = minus tau (blue "
            "arrows pointing in). The crack (dark line) opens across the tension direction, along the compression "
            "diagonal, at 45 degrees to the axis, and so wraps the shaft as a helix.")
    return finish(VB, aria, s, o)


# ================================================================ svg #15  C4: brittle bone spirals, ductile steel breaks flat
# The tibia of InjuryMap "Lower leg muscles.svg" (CC BY-SA 4.0): its fill path (class c51) from
# crop_art.py ../svg_paths/Lower_leg_muscles.svg m02tibia 255 405 412 978 --drop "#Names, text". Fill only, as the femur.
TIB_D = re.search(r'<path\b(?=[^>]*class="c51")[^>]*\bd="([^"]+)"',
                  _read("Lower_leg_muscles_crop_m02tibia.svg")).group(1)
_TP = sample(segments(TIB_D))


def _mid(pts, ay):
    xs = sorted(a[0] + (ay - a[1]) / (b[1] - a[1]) * (b[0] - a[0])
                for a, b in zip(pts, pts[1:] + pts[:1]) if (a[1] - ay) * (b[1] - ay) < 0)
    return (xs[0] + xs[-1]) / 2


TIB_C = (_mid(_TP, 650), 650.0)                          # shaft axis through the mid-shaft at two levels
TIB_ROT = math.degrees(math.atan2(_mid(_TP, 850) - TIB_C[0], 200.0))   # tilt of the art's shaft: rotate it upright


def _rot(q):
    c, s_ = math.cos(math.radians(TIB_ROT)), math.sin(math.radians(TIB_ROT))
    x, y = q[0] - TIB_C[0], q[1] - TIB_C[1]
    return TIB_C[0] + x * c - y * s_, TIB_C[1] + x * s_ + y * c       # the map SVG rotate(TIB_ROT cx cy) applies


TIB_OUT = [_rot(q) for q in _TP]
TIB_BOX = (min(q[0] for q in TIB_OUT), min(q[1] for q in TIB_OUT), max(q[0] for q in TIB_OUT), max(q[1] for q in TIB_OUT))


def tib_edges(ay):
    xs = sorted(a[0] + (ay - a[1]) / (b[1] - a[1]) * (b[0] - a[0])
                for a, b in zip(TIB_OUT, TIB_OUT[1:] + TIB_OUT[:1]) if (a[1] - ay) * (b[1] - ay) < 0)
    return xs[0], xs[-1]


class Tibia(Femur):
    """The tibia, upright (rotated by TIB_ROT), placed by its rotated bbox: top-left (x0, y0) and height h."""
    ed = staticmethod(tib_edges)

    def __init__(self, x0, y0, h):
        self.k = self.kx = h / (TIB_BOX[3] - TIB_BOX[1])
        self.tx, self.ty = x0 - TIB_BOX[0] * self.k, y0 - TIB_BOX[1] * self.k

    def use(self, s, fill=BONE, stroke=BONE_L, extra=""):
        return (f'<g transform="translate({self.tx:.2f} {self.ty:.2f}) scale({self.k:.4f}) '
                f'rotate({TIB_ROT:.3f} {TIB_C[0]:.2f} {TIB_C[1]:.2f})"><path d="{TIB_D}" fill="{fill}" stroke="{stroke}" '
                f'stroke-width="{s(H.PX["art_line"]) / self.k:.2f}" stroke-linejoin="round" {extra}/></g>')


def fig15():
    p = "m2f15_"
    VB = (0, 0, 400, 388)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    F = Tibia(70.0, 34.0, h=250.0)
    o.append(F.use(s))
    for ay, fl in ((560.0, True), (900.0, False)):
        cx, hw = F.shaft(ay)
        o.append(torque(s, p, cx, F.P(0, ay)[1], hw * 2.0, fl, it("T")))
    cr, cross = crack(s, F, 860.0, 600.0)
    o.append(cr)
    # steel rod, same torque, flat break across the axis
    rx0, rw, ry0, ry1 = 262.0, 30.0, 52.0, 272.0
    ym = (ry0 + ry1) / 2
    gap = 3.0
    for y_a, y_b in ((ry0, ym - gap), (ym + gap, ry1)):
        o.append(rect(rx0, y_a, rw, y_b - y_a, GRID, I["rule"], s(1.2), rx=3))
    o.append(H.line(s, rx0 - 12, ym, rx0 + rw + 12, ym, I["primary"], "force", extra='stroke-linecap="round"'))
    for y, fl in ((ry0 + 26, True), (ry1 - 26, False)):
        o.append(torque(s, p, rx0 + rw / 2, y, rw * 1.1, fl, it("T")))
    o.append(H.label(s, rx0 + rw + 18, ym + 5, "flat", "label2", I["primary"]))
    yb = 302.0
    o.append(H.label(s, 100, yb, "brittle bone (tibia): 45° helix", "label2", I["primary"], "middle"))
    o.append(H.label(s, 100, yb + 16, "(crack ⟂ principal tension)", "label2", I["secondary"], "middle"))
    o.append(H.label(s, rx0 + rw / 2, yb, "ductile steel: flat break", "label2", I["primary"], "middle"))
    o.append(H.label(s, rx0 + rw / 2, yb + 16, "(plane of maximum shear)", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 200, 18, "the same torque, two failure planes", "label2", I["secondary"], "middle"))
    cr = H.ATTRIBUTION["by-sa"].format(author="InjuryMap", title="Lower leg muscles.svg",
                                       changes="Tibia only, recoloured, turned upright; torque, crack and steel rod drawn "
                                               "for this course.")
    lines = wrap(cr, 74)
    o.append(H.credit(s, 8, VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines))
    aria = ("Problem C4 setup. Left: a tibia (InjuryMap art, side view) under a torque T, brown arrows turning the top and the "
            "bottom of the shaft in opposite senses; a dark crack winds round the shaft as a 45-degree helix, solid on "
            "the front face and dashed on the back, perpendicular to the principal tension. Right: a grey ductile steel "
            "rod under the same torque breaks flat across its axis, on the plane of maximum shear.")
    return finish(VB, aria, s, o)


# ================================================================ svg #20  C9: geometric versus stouter scaling
LAM = 2.0                                        # length scale factor drawn (C9, line 711: every length x lambda)


def fig20():
    p = "m2f20_"
    VB = (0, 0, 400, 360)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    h0, yb = 110.0, 268.0
    k0 = h0 / ART_L
    kel = k0 * LAM ** 1.5                        # elastic similarity: d proportional to L^(3/2) (line 711, K6 line 937)
    # sigma ~ M_b L / d^3 with M_b ~ L d^2 (K6 solution, line 940): sigma ~ L^2 / d
    sig_geo = LAM ** 2 / LAM
    sig_el = LAM ** 2 / LAM ** 1.5
    assert abs(sig_geo - 2) < 1e-9 and abs(sig_el - 2 ** 0.5) < 1e-9
    W = lambda k: (FEMUR_ART[2] - FEMUR_ART[0]) * k  # noqa: E731
    xs = [48.0, 140.0, 140.0 + W(k0 * LAM) + 46]
    bones = [(k0, k0, h0, "small animal", "length L, width d"),
             (k0 * LAM, k0 * LAM, h0 * LAM, "geometric ×2", "d ∝ L"),
             (k0 * LAM, kel, h0 * LAM, "stouter ×2", None)]
    for x, (k, kx, h, t1, t2) in zip(xs, bones):
        F = Femur(x, yb - h, k=k, kx=kx)
        o.append(F.use(s))
        cx = x + W(kx) / 2
        o.append(H.label(s, cx, yb - h - 26, t1, "label2", I["primary"], "middle"))
        o.append(H.label(s, cx, yb - h - 10, t2 if t2 else f'd ∝ L{sup("3/2", s)}', "label2", I["secondary"], "middle"))
    o.append(H.arrow(s, p, xs[0] + W(k0) + 10, yb - 40, xs[1] - 10, yb - 40, "dim", w="ref"))
    o.append(H.label(s, (xs[0] + W(k0) + xs[1]) / 2, yb - 48, f'{it("λ")} = 2', "label2", I["primary"], "middle"))
    rows = [(xs[0] + W(k0) / 2, "σ × 1"), (xs[1] + W(k0 * LAM) / 2, f"σ × {sig_geo:.0f}"),
            (xs[2] + W(kel) / 2, f"σ × {sig_el:.2f}")]
    for x, t in rows:
        o.append(H.label(s, x, yb + 22, t, "label", I["primary"], "middle"))
    o.append(H.label(s, 200, yb + 42, "peak bending stress σ ∝ L²/d (body mass ∝ L d²)", "label2", I["secondary"], "middle"))
    o.append(credit(s, VB, 74, "Femur recoloured and scaled (the stouter bone widened by 2 to the 3/2)."))
    aria = ("Problem C9 setup. Three femurs (NIH BioArt) standing side by side. Left: a small animal's bone, length L and "
            "width d. Middle: the same bone scaled geometrically by lambda = 2, every length doubled, d proportional to L: "
            "its peak bending stress doubles. Right: a bone of the same doubled length but stouter, its width scaled as L "
            "to the 3/2 (elastic similarity, 2.83 times wider): its stress rises only by 1.41. Below: peak bending stress "
            "is proportional to L squared over d when body mass is proportional to L d squared.")
    return finish(VB, aria, s, o)


# ================================================================ svg #21  C10: trabeculae of the femoral head
HIP = (0.0, 30.0, 112.0, 88.0)                  # window inside the m02hip crop (art units)


def hip_art():
    art = inner_svg(_read("nih_upper_leg_crop_m02hip.svg"))
    art = re.sub(r"\.c2\{\s*mask: url\(#i2\);\s*\}", "", art)     # no fade-out: the window ends at the femur
    return H.recolour(art, "nih")


def fig21():
    p = "m2f21_"
    VB = (0, 0, 400, 382)
    s = H.Scale(VB[2], VB[3], display_w=400)
    K, X0, Y0 = 3.05, 30.0, 26.0
    f = lambda q: (X0 + (q[0] - HIP[0]) * K, Y0 + (q[1] - HIP[1]) * K)  # noqa: E731
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(f'<g transform="translate({X0 - HIP[0] * K:.2f} {Y0 - HIP[1] * K:.2f}) scale({K})">'
             f'{art_image("<svg>" + hip_art() + "</svg>", HIP)}</g>')
    Hc = f(HEAD[:2])
    rh = HEAD[2] * K
    o.append(circ(Hc[0], Hc[1], rh, "none", BONE_L, s(1.3), f'stroke-dasharray="{s(4):.1f} {s(3):.1f}"'))
    # compressive struts: superior head surface (under the joint load) down to the medial cortex (calcar)
    def bez(a, c, b):
        return f"M{a[0]:.1f},{a[1]:.1f} Q{c[0]:.1f},{c[1]:.1f} {b[0]:.1f},{b[1]:.1f}"
    comp, tens = [], []
    for i, th in enumerate(np.linspace(-140, -55, 6)):
        a = (HEAD[0] + HEAD[2] * 0.92 * math.cos(math.radians(th)), HEAD[1] + HEAD[2] * 0.92 * math.sin(math.radians(th)))
        b = (edges(92 + 3 * i)[1] - 1.5, 92 + 3 * i)
        c = ((a[0] + b[0]) / 2 + 2.0, (a[1] + b[1]) / 2)
        comp.append(bez(f(a), f(c), f(b)))
    # tensile arcade: lateral cortex below the GT, arching over the neck to the inferior head
    for i, th in enumerate(np.linspace(-10, 60, 5)):
        a = (edges(80 + 6 * i)[0] + 1.5, 80 + 6 * i)
        b = (HEAD[0] + HEAD[2] * 0.9 * math.cos(math.radians(th)), HEAD[1] + HEAD[2] * 0.9 * math.sin(math.radians(th)))
        c = ((a[0] + b[0]) / 2 - 2, min(a[1], b[1]) - 16 + 2 * i)
        tens.append(bez(f(a), f(c), f(b)))
    o.append(path("".join(tens), TEN, s(1.6), extra='stroke-linecap="round"'))
    o.append(path("".join(comp), COM, s(1.6), extra='stroke-linecap="round"'))
    # joint force on the head, along the compressive fan
    ang = math.radians(-74)
    tip = (Hc[0] + rh * 0.55 * math.cos(ang), Hc[1] + rh * 0.55 * math.sin(ang))
    o.append(H.arrow(s, p, tip[0] + 70 * math.cos(ang), tip[1] + 70 * math.sin(ang) - 0, tip[0], tip[1], "reaction"))
    lab = lambda x, y, t, a="start", c=I["primary"]: H.label(s, x, y, t, "label2", c, a)  # noqa: E731
    jx, jy = tip[0] + 70 * math.cos(ang), tip[1] + 70 * math.sin(ang)
    o.append(lab(jx + 8, jy + 12, "hip joint force"))
    cq = f((edges(112)[1] - 1, 112))
    o.append(H.line(s, cq[0] + 2, cq[1], cq[0] + 26, cq[1] + 18, I["secondary"], "leader"))
    o.append(lab(cq[0] + 29, cq[1] + 22, "compressive struts"))
    tq = f((edges(98)[0] + 1, 98))
    o.append(H.line(s, tq[0] - 2, tq[1] + 2, tq[0] - 14, tq[1] + 30, I["secondary"], "leader"))
    o.append(lab(tq[0] - 16, tq[1] + 44, "tensile arcade", "middle"))
    o.append(H.line(s, Hc[0] + rh * 0.74, Hc[1] + rh * 0.74, Hc[0] + rh + 6, Hc[1] + rh + 1, I["secondary"], "leader"))
    o.append(lab(Hc[0] + rh + 8, Hc[1] + rh + 6, "head (in its socket)"))
    o.append(lab(f((90, 0))[0], f((0, 34))[1] + 16, "pelvis", "middle", I["secondary"]))
    from m05.tissue import legend, sw_line
    lg, _ = legend(s, 30, 330, [(sw_line(COM, 1.6), "compression"), (sw_line(TEN, 1.6), "tension"),
                                (sw_line(O["reaction"]), "joint force")], gap=12)
    o.append(lg)
    o.append(credit(s, VB, 74, "Hip region cropped and recoloured; head circle, struts and force drawn for this course."))
    aria = ("Problem C10 setup. The hip region of the NIH BioArt upper-leg bones: the pelvis above, the upper femur below "
            "with its head in the socket, outlined by a dashed circle. A black arrow, the hip joint force, presses on "
            "the top of the head. Inside the bone, blue compressive struts fan from the top of the head down to the "
            "medial cortex, along the joint force, and red tensile struts arch from the lateral cortex below the "
            "greater trochanter over the neck to the lower head: the trabeculae follow the principal load lines.")
    return finish(VB, aria, s, o)


# ================================================================ svg #32  K1: step versus ramp loading (script, lines 790-811)
Z0, E_B, K_GAIN = 2.02e-6, 17e9, 80.0
EPS_LO, EPS_HI = 1000e-6, 1500e-6
M_REF = 1250e-6 * Z0 * E_B


def rate(Z, M, k=K_GAIN):
    e = M / (Z * E_B)
    if e > EPS_HI:
        return k * Z * (e - EPS_HI)
    if e < EPS_LO:
        return k * Z * (e - EPS_LO)
    return 0.0


def k1_run(load, ramp_days, days=200, dt=0.5):
    """K1's peak_strain(), keeping the trajectory: (t, load fraction, strain in microstrain)."""
    Z, emax, out = Z0, 0.0, []
    for i in range(int(days / dt) + 1):
        frac = min(i * dt / ramp_days, 1.0) if ramp_days else 1.0
        M = M_REF + (load - 1) * M_REF * frac
        emax = max(emax, M / (Z * E_B))
        out.append((i * dt, M / M_REF, M / (Z * E_B) * 1e6))
        Z = max(Z + rate(Z, M) * dt, 1e-9)
    return round(emax * 1e6), out


def icon(s, p, x0, y0, h, txt, arrow_len=0):
    """A small femur with an optional load arrow on the head and a caption under it."""
    F = Femur(x0, y0, h=h)
    o = [F.use(s)]
    hx, hy = F.P(HEAD[0] + 2, HEAD[1] - HEAD[2])
    if arrow_len:
        o.append(H.arrow(s, p, hx, hy - arrow_len, hx, hy - 1, "load"))
    cx = F.P(40, 0)[0]
    for i, t in enumerate(txt):
        o.append(plabel(s, cx, y0 + h + 18 + 15 * i, t, "label2", I["secondary"], "middle"))
    return "".join(o)


def fig32():
    p = "m2f32_"
    VB = (0, 0, 400, 340)
    s = H.Scale(VB[2], VB[3], display_w=400)
    pk_s, st = k1_run(1.6, 0)
    pk_r, rp = k1_run(1.6, 50)
    assert (pk_s, pk_r) == (2000, 1602), (pk_s, pk_r)          # script output, line 811
    st, rp = [q for q in st if q[0] <= 100], [q for q in rp if q[0] <= 100]
    t = [q[0] for q in st]
    PL = Plot(s, (150, 50, 388, 96), (0, 100), (0.9, 1.7))
    PS = Plot(s, (150, 124, 388, 268), (0, 100), (1200, 2100))
    o = [f'<defs>{H.markers(p, s)}</defs>', icon(s, p, 18, 92, 150, ["femur, load", "+60 %"], arrow_len=30)]
    # load panel
    o.append(H.line(s, PL.x0, PL.y0, PL.x1, PL.y0, I["axis"], "axis"))
    o.append(H.line(s, PL.x0, PL.y0, PL.x0, PL.y1, I["axis"], "axis"))
    for v, tx in ((1.0, "1"), (1.6, "1.6")):
        o.append(H.line(s, PL.x0, PL.Y(v), PL.x1, PL.Y(v), GRID, "leader"))
        o.append(H.line(s, PL.x0 - 5, PL.Y(v), PL.x0, PL.Y(v), I["axis"], "leader"))
        o.append(plabel(s, PL.x0 - 8, PL.Y(v) + 4.5, tx, "tick", I["secondary"], "end"))
    o.append(plabel(s, PL.x0 - 34, (PL.y0 + PL.y1) / 2 + 4, f'{it("M")}/{it("M")}{H.sub("ref", s, "label2")}', "label2",
                    I["primary"], "end"))
    o.append(PL.curve(t, [q[1] for q in st], TEN, multi=True))
    o.append(PL.curve(t, [q[1] for q in rp], COM, multi=True))
    # strain panel
    o.append(PS.axes([(v, f"{v}") for v in (0, 25, 50, 75, 100)], [(1250, "1250"), (1500, "1500"), (2000, "2000")],
                     "time (days)", "peak strain (µε)", grid=(1250, 2000), ytx=100))
    o.append(H.line(s, PS.x0, PS.Y(1500), PS.x1, PS.Y(1500), I["rule"], "ref", H.DASH_REF))
    o.append(plabel(s, PS.x1 - 2, PS.Y(1500) + 15, f'formation setpoint {it("ε")}{H.sub("hi", s, "label2")}', "label2",
                    I["secondary"], "end"))
    o.append(PS.curve(t, [q[2] for q in st], TEN, multi=True))
    o.append(PS.curve(t, [q[2] for q in rp], COM, multi=True))
    ir = max(range(len(rp)), key=lambda i: rp[i][2])
    o.append(PS.dot(0, st[0][2], TEN))
    o.append(PS.dot(rp[ir][0], rp[ir][2], COM))
    o.append(plabel(s, PS.X(3), PS.Y(2000) + 4, f"step: peak {pk_s} µε at day 0", "label2", I["primary"]))
    o.append(plabel(s, PS.X(46), PS.Y(rp[ir][2]) - 10, f"ramp: peak {pk_r} µε, day {rp[ir][0]:.0f}", "label2",
                    I["primary"], "middle"))
    o.append(plegend(s, 150, 24, [(TEN, "step", None), (COM, "ramp over 50 days", None)]))
    pl = hov(PL, t[::4], [[q[1] for q in st][::4], [q[1] for q in rp][::4]],
             lambda i: f"day {t[::4][i]:.0f}: load step {st[::4][i][1]:.2f}, ramp {rp[::4][i][1]:.2f}")
    ps = hov(PS, t[::4], [[q[2] for q in st][::4], [q[2] for q in rp][::4]],
             lambda i: f"day {t[::4][i]:.0f}: step {st[::4][i][2]:.0f} µε, ramp {rp[::4][i][2]:.0f} µε")
    o.append(credit(s, VB, 74, "Femur recoloured."))
    aria = ("Problem K1 result, computed with the module's script. Left: a small femur (NIH BioArt) with a load arrow, "
            "load raised by 60 percent. Top panel: the load M over M ref against time, a red step to 1.6 at day 0 and a "
            "blue ramp reaching 1.6 at day 50. Bottom panel: peak bone strain against time over 100 days. The step "
            f"jumps the strain to {pk_s} microstrain at once and the bone, thickening over weeks, brings it back down to "
            f"the 1500 microstrain formation setpoint by about day 30. The ramp lets the bone keep up: its strain peaks "
            f"at {pk_r} microstrain on day {rp[ir][0]:.0f} and also settles at 1500.")
    return finish(VB, aria, s, o, extra=H.hover_attr([(PL.box, pl), (PS.box, ps)]))


# ================================================================ svg #48  K9: bed-rest fit (script, lines 990-1018)
def traj(k, sc, days=300):
    Z, out = Z0, []
    for _ in range(days + 1):
        out.append(Z)
        e = sc * M_REF / (Z * E_B)
        if e > EPS_HI:
            rr = k * Z * (e - EPS_HI)
        elif e < EPS_LO:
            rr = k * Z * (e - EPS_LO)
        else:
            rr = 0.0
        Z = max(Z + rr, 1e-9)
    return np.array(out)


def k9_fit():
    rng = np.random.default_rng(0)
    t = np.arange(0, 301, 20)
    data = traj(60, 0.5)[t] * (1 + 0.02 * rng.standard_normal(len(t)))
    res = minimize(lambda q: np.sum((traj(q[0], q[1])[t] - data) ** 2), [30, 0.7], method="Nelder-Mead")
    return t, data, res.x


def fig48():
    p = "m2f48_"
    VB = (0, 0, 400, 316)
    s = H.Scale(VB[2], VB[3], display_w=400)
    t, data, (kf, lf) = k9_fit()
    assert list(np.round([kf, lf], 1)) == [56.7, 0.5], (kf, lf)          # script output, line 1018 (56.67, 0.496)
    zeq = 0.5 * 1250e-6 / EPS_LO * 100                                    # Z_eq = load M_ref / (E eps_lo), line 1020
    days = np.arange(0, 301)
    fit = traj(kf, lf) / Z0 * 100
    true = traj(60, 0.5) / Z0 * 100
    assert abs(true[-1] - zeq) < 0.05 and abs(zeq - 62.5) < 1e-9
    P = Plot(s, (150, 56, 388, 232), (0, 300), (55, 105))
    o = [f'<defs>{H.markers(p, s)}</defs>', icon(s, p, 18, 76, 150, ["bed rest:", "load × 0.5"], arrow_len=16)]
    o.append(P.axes([(v, f"{v}") for v in (0, 100, 200, 300)], [(62.5, "62.5"), (75, "75"), (100, "100")],
                    "time (days)", "section modulus Z/Z₀ (%)", grid=(75, 100), ytx=100))
    o.append(H.line(s, P.x0, P.Y(zeq), P.x1, P.Y(zeq), I["rule"], "ref", H.DASH_REF))
    o.append(plabel(s, P.X(200), P.Y(69.5), f'dashed: plateau {it("Z")}{H.sub("eq", s, "label2")} = {zeq:.1f} %', "label2",
                    I["secondary"], "middle"))
    o.append(P.curve(days, fit, TEN, multi=True))
    for x, y in zip(t, data / Z0 * 100):
        o.append(P.dot(x, y, COM))
    o.append(plabel(s, P.X(120), P.Y(88), f'fit: {it("k")} = {kf:.1f}, load {lf:.2f}', "label2", I["primary"]))
    o.append(plabel(s, P.X(120), P.Y(88) + 16, f'(true {it("k")} = 60, load 0.50)', "label2", I["secondary"]))
    from m05.tissue import legend, sw_dot, sw_line
    o.append(legend(s, 150, 18, [(sw_dot(COM, "#fff"), "synthetic DXA points, 2 % noise")])[0])
    o.append(legend(s, 150, 36, [(sw_line(TEN, 2.0), "least-squares fit of the remodeling law")])[0])
    pts = [[P.X(d), [P.Y(fit[d])], f"day {d}: fit Z/Z0 = {fit[d]:.1f} %"] for d in days[::3]]
    for x, y in zip(t, data / Z0 * 100):
        pts.append([P.X(x), [P.Y(y)], f"day {x}: DXA point {y:.1f} %, fit {fit[x]:.1f} %"])
    pts.sort(key=lambda q: q[0])
    o.append(credit(s, VB, 74, "Femur recoloured."))
    aria = ("Problem K9 result, computed with the module's script. Left: a small femur (NIH BioArt) with a short load "
            "arrow, bed rest at half the habitual load. Right: section modulus Z over Z0 in percent against time over 300 "
            "days. Blue dots are 16 synthetic DXA points every 20 days, made with gain k = 60 and load fraction 0.5 plus 2 "
            f"percent noise; the red curve is the least-squares fit of the remodeling law, k = {kf:.1f} and load {lf:.2f}. "
            f"Both fall from 100 percent and level off on the dashed plateau Z eq = {zeq:.1f} percent within about 100 days.")
    return finish(VB, aria, s, o, extra=H.hover_attr(P.box, pts))


# ================================================================ svg #50  K10: cantilever femur (script, lines 1029-1045)
E_K, LB, P_TIP = 17e9, 0.40, 500.0


def cumtrapz(f, x):
    d = np.diff(x)
    return np.concatenate([[0], np.cumsum((f[:-1] + f[1:]) / 2 * d)])


def cantilever(R, r, n=400):
    Ii = np.pi / 4 * (R ** 4 - r ** 4)
    x = np.linspace(0, LB, n)
    kappa = P_TIP * (LB - x) / (E_K * Ii)
    w = cumtrapz(cumtrapz(kappa, x), x)
    return x, w, round(w[-1] * 1e3, 1), round(P_TIP * LB * R / Ii / 1e6, 1)


def fig50():
    p = "m2f50_"
    VB = (0, 0, 400, 418)
    s = H.Scale(VB[2], VB[3], display_w=400)
    x, w7, d7, s7 = cantilever(0.014, 0.007)
    _, w9, d9, s9 = cantilever(0.014, 0.009)
    assert (d7, s7, d9, s9) == (22.2, 99.0, 25.1, 111.9), (d7, s7, d9, s9)     # script output, lines 1044-1045
    # ---- the bone: art bent by the computed healthy deflection, at true scale (bone length = L = 0.40 m)
    XW, YA, LPX = 46.0, 96.0, 300.0
    k = LPX / ART_L
    ax_c = (SHAFT_A[0] + SHAFT_B[0]) / 2

    def bend(q, wv=w7):
        u = (FEMUR_ART[3] - q[1]) / ART_L                    # 0 at the fixed (knee) end, 1 at the free end
        return XW + u * LPX, YA - (q[0] - ax_c) * k + np.interp(u * LB, x, wv) / LB * LPX

    straight = emit(SEGS, lambda q: (XW + (FEMUR_ART[3] - q[1]) / ART_L * LPX, YA - (q[0] - ax_c) * k))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(path(straight, I["rule"], s(1.1), extra=f'stroke-dasharray="{s(4):.1f} {s(3):.1f}"'))
    o.append(path(emit(SEGS, bend), BONE_L, s(H.PX["art_line"]), fill=BONE, extra='stroke-linejoin="round"'))
    # wall
    o.append(rect(XW - 16, YA - 44, 16, 88, GRID, I["rule"], s(1.0)))
    o.append(path("".join(f"M{XW - 16:.1f},{YA - 36 + 12 * i:.1f} l16,-10" for i in range(8)), I["rule"], s(0.8)))
    o.append(plabel(s, XW - 8, YA + 62, "fixed end", "label2", I["secondary"], "middle"))
    tip = (XW + LPX, YA + d7 / 1e3 / LB * LPX)
    o.append(H.arrow(s, p, tip[0] - 8, tip[1] - 62, tip[0] - 8, tip[1] - 12, "load"))
    o.append(plabel(s, tip[0] - 14, tip[1] - 50, f'{it("P")} = {P_TIP:.0f} N', "label2", I["primary"], "end"))
    o.append(plabel(s, XW - 14, 18, f'peak stress at the fixed end: {s7:.0f} MPa', "label2", I["primary"]))
    o.append(plabel(s, XW - 14, 34, f'(thinner wall: {s9:.0f} MPa)', "label2", I["secondary"]))
    o.append(plabel(s, XW + LPX / 2 + 20, YA + 62, f'{it("L")} = {LB:.2f} m, true-scale sag; dashed: unloaded', "label2",
                    I["secondary"], "middle"))
    # ---- deflection plot
    P = Plot(s, (60, 196, 340, 326), (0, 0.4), (0, 30))
    o.append(P.axes([(v, f"{v:.1f}") for v in (0, 0.1, 0.2, 0.3, 0.4)], [(0, "0"), (10, "10"), (20, "20"), (30, "30")],
                    "distance from the fixed end (m)", "deflection w (mm)", grid=(10, 20, 30), ytx=18))
    o.append(P.curve(x, w7 * 1e3, TEN, multi=True))
    o.append(P.curve(x, w9 * 1e3, COM, multi=True, dash=(7, 4)))
    o.append(P.dot(0.4, d7, TEN))
    o.append(P.dot(0.4, d9, COM))
    o.append(plabel(s, P.X(0.4) + 8, P.Y(d9) - 1, f"{d9} mm", "label2", I["primary"]))
    o.append(plabel(s, P.X(0.4) + 8, P.Y(d7) + 12, f"{d7} mm", "label2", I["primary"]))
    o.append(plegend(s, 70, 210, [(TEN, "bore r = 7 mm", None), (COM, "r = 9 mm (thinner)", (7, 4))]))
    o.append(plabel(s, 70, 228, f'{it("R")} = 14 mm', "label2", I["secondary"]))
    pts = [[P.X(x[i]), [P.Y(w7[i] * 1e3), P.Y(w9[i] * 1e3)],
            f"x = {x[i]:.2f} m: w = {w7[i] * 1e3:.1f} mm (r 7), {w9[i] * 1e3:.1f} mm (r 9)"] for i in range(0, len(x), 4)]
    o.append(credit(s, VB, 74, "Femur recoloured and bent by the computed deflection (true scale)."))
    aria = ("Problem K10 result, computed with the module's script. Top: a femur (NIH BioArt) held horizontal as a "
            "cantilever, its knee end fixed in a wall, bent at true scale by a downward tip load P = 500 N at the hip end "
            f"(dashed outline: unloaded). Peak stress at the fixed end is {s7:.0f} MPa, or {s9:.0f} MPa with a thinner "
            "wall. Bottom: deflection w against distance from the fixed end, 0 to 0.40 m, for outer radius 14 mm: the red "
            f"curve (bore 7 mm) reaches {d7} mm at the tip, the dashed blue curve (bore 9 mm, thinner wall) {d9} mm.")
    return finish(VB, aria, s, o, extra=H.hover_attr(P.box, pts))


FIGS = {
    1: ("Left: NIH BioArt upper leg bones (public domain). Right: later", fig1),
    6: ("Left: lateral femur under torque T with 45-degree helical crac", fig6),
    15: ("Left: a bone twisted by a torque fails on a 45-degree helix. R", fig15),
    20: ("A slender small-animal bone beside a proportionally stouter la", fig20),
    21: ("Femoral head with trabecular struts along load lines and hip j", fig21),
    32: ("A femur under step versus ramp loading, with peak bone strain ", fig32),
    48: ("Bed-rest DXA section-modulus points falling over time with a l", fig48),
    50: ("A cantilever femur deflecting under a transverse tip load P, w", fig50),
}
