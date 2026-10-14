"""Module 16, group `body_main`: 14 problem figures in the house style (400 px, class f).

svg 19, 20, 22, 23, 24 (C1, C2, C4, C5, C6), 29, 31, 32, 35, 36, 37 (D1, D3, D4, D7, D8, D9),
42, 43, 51 (K3, K4, K9).

No Module 16 figure is a whole body, so the Lynch kit is not used and SHARED_DEFS() carries one thing only:
the NIH BioArt femur fill path (public domain, the m00 crop `svg_paths/nih_upper_leg_crop_m00femur.svg`) as
#m16art_femur, <use>d by C1 (#19) and C5 (#23). Any other Module 16 group may <use> the same id.
Tendon is drawn as a tissue strip with collagen lines (the m02/beam.py, m04/tissue_prob.py idiom); the 52 KB
InjuryMap Achilles crop is too heavy for a 400 px figure. Continuum objects (stress element, tetrahedron,
bar element, series bars) are schematic blocks, not anatomy.

Colour meanings (as the main-text Fig. of Section 2, module16.html line 162): normal stress and traction
= force red, shear stress = geometry blue, cut normal n = dim grey, body force = load brown. Stiff and soft
materials of K3, K9 and element 1 and 2 of D8 use the marrow and cartilage tokens, named in a legend.

Every plotted number is computed here from the formula or the K-problem script the page states; the printed
numbers of the page are asserted (line numbers beside each constant).
"""
import math
import random

import numpy as np

import house as H
from m00.tissue import FEMUR_ART, femur_d
from m02.bone import edges as femur_edges
from m05.body import finish, wrap
from m05.plots_prob import Plot, hov
from m05.plots_prob import label as plabel
from m05.plots_prob import legend as plegend
from m05.schematic import it
from m05.tissue import circ, path, rect

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
BOX, GRID = "#f7f4ef", "#e6e6e6"
RED, BLUE, BROWN, GREY = O["force"], O["geometry"], O["load"], O["dim"]
STIFF, SOFT = T["marrow"], T["cartilage"]            # stiff = darker warm token, soft = pale blue token
BONE, BONE_L = T["bone"]
COLL = T["tendon"][1]
FEMUR_ID = "m16art_femur"
ART_L = FEMUR_ART[3] - FEMUR_ART[1]
CREDIT = ("Art: NIH NIAID BioArt (R. Kissinger), “Human Upper Leg Bones”, public domain (U.S. Government work). "
          "One femur, recoloured.")


def SHARED_DEFS():  # noqa: N802 (apply_figs calls this name)
    """The femur fill path, once per page (no fill or stroke: each <use> sets them)."""
    return f'<path id="{FEMUR_ID}" d="{femur_d()}"/>'


# ---------------------------------------------------------------- small helpers
def lab(s, x, y, t, size="label2", fill=I["primary"], anchor="start", extra=""):
    return H.label(s, x, y, t, size, fill, anchor, extra)


def sub(t, s, size="label2"):
    return H.sub(t, s, size)


def sup(t, s, size="label2"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def bf(t):
    return f'<tspan font-weight="700">{t}</tspan>'


def xdd(s, size="label2"):
    """x with a double dot (acceleration): Georgia has no combining dots, so a spacing diaeresis is placed by dx/dy."""
    return (f'x<tspan dx="{-s(6.5):.2f}" dy="{-s(5):.2f}">¨</tspan><tspan dx="{s(1):.2f}" dy="{s(5):.2f}"> </tspan>')


def dash_attr(s, a=5, b=3):
    return f'stroke-dasharray="{s(a):.2f} {s(b):.2f}"'


def credit(s, x, y, n=64):
    return H.credit(s, x, y, wrap(CREDIT, n))


def node(s, x, y, r=5.5):
    return circ(x, y, s(r), "#fff", I["axis"], s(1.4))


def bar(s, x1, x2, yc, hh=24, fill=BOX, stroke=I["rule"], dashed=False, sw=1.0):
    ex = dash_attr(s) if dashed else ""
    return rect(x1, yc - hh / 2, x2 - x1, hh, "none" if dashed else fill, stroke, s(sw), 3, ex)


def vec2(x, y, ang_deg, length):
    a = math.radians(ang_deg)
    return x + length * math.cos(a), y + length * math.sin(a)


def hatch_wall(s, x, yc, half=20, n=5):
    """Fixed support on the left of x: wall line and hatch ticks."""
    o = [H.line(s, x, yc - half, x, yc + half, I["axis"], "axis")]
    for i in range(n):
        y = yc - half + 4 + i * (2 * half - 8) / (n - 1)
        o.append(H.line(s, x, y, x - 8, y + 8, I["axis"], "leader"))
    return "".join(o)


class Femur:
    """Vertical femur placed by its art bbox: top-left (x0, y0) and height h (the m02/bone.py Femur idea)."""

    def __init__(self, x0, y0, h):
        self.k = h / ART_L
        self.tx, self.ty = x0 - FEMUR_ART[0] * self.k, y0 - FEMUR_ART[1] * self.k

    def P(self, ax, ay):
        return self.tx + ax * self.k, self.ty + ay * self.k

    def use(self, s):
        sw = s(H.PX["art_line"]) / self.k
        return (f'<use href="#{FEMUR_ID}" transform="translate({self.tx:.2f} {self.ty:.2f}) scale({self.k:.4f})" '
                f'fill="{BONE}" stroke="{BONE_L}" stroke-width="{sw:.2f}" stroke-linejoin="round"/>')


# ================================================================ svg #19  C1: traction depends on the cut
def fig19():
    p = "m16f19_"
    VB = (0, 0, 400, 346)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    F = Femur(30, 38, 200)
    o.append(F.use(s))
    hx, hy = F.P(45.8, FEMUR_ART[1])
    bx, by = F.P(38.0, FEMUR_ART[3])
    o.append(H.arrow(s, p, hx, hy - 2, hx, hy - 30, "load"))
    o.append(H.arrow(s, p, bx, by + 2, bx, by + 30, "load"))
    o.append(lab(s, hx + 8, hy - 14, "pull", "label2", BROWN))
    a, b = femur_edges(190.0)
    px, py = F.P((a + b) / 2, 190.0)
    o.append(circ(px, py, s(4), "#fff", I["primary"], s(1.5)))
    # three cuts through that point: n at angle theta from the pull direction e (up the page); uniaxial stress = sigma e (x) e,
    # so t = sigma n = sigma (e . n) e  (module16.html line 130; uniaxial bar, line 172)
    cxs, cy, r = (168.0, 258.0, 348.0), 116.0, 38.0
    o.append(H.line(s, px + 6, py - 2, cxs[0] - r - 2, cy + 6, I["rule"], "leader", H.DASH_REF))
    o.append(lab(s, 258, 30, "one point, one pull σ, three cuts", "label", I["primary"], "middle"))
    o.append(lab(s, 258, 46, "the point, magnified, cut at angle θ to the pull", "label2", I["secondary"], "middle"))
    n_len, t_scale = 24.0, r
    for cx, th in zip(cxs, (0.0, 45.0, 90.0)):
        c, sn = math.cos(math.radians(th)), math.sin(math.radians(th))
        n = (sn, -c)                                   # cut normal (screen coords, y down); 0 deg = up the page
        sv = (-c, -sn)                                 # unit vector along the cut with t . sv >= 0
        t_n, t_s = c * c, c * sn                       # normal and shear parts of t, in units of sigma
        A = (cx + r * sv[0], cy + r * sv[1])
        B = (cx - r * sv[0], cy - r * sv[1])
        o.append(circ(cx, cy, r, BONE, BONE_L, s(1.2)))
        o.append(f'<path d="M{A[0]:.2f},{A[1]:.2f} A{r},{r} 0 0 1 {B[0]:.2f},{B[1]:.2f} Z" fill="{T["bone_shade"][0]}" '
                 f'stroke="none"/>')
        o.append(circ(cx, cy, r, "none", BONE_L, s(1.2)))
        o.append(H.line(s, cx - (r + 7) * sv[0], cy - (r + 7) * sv[1], cx + (r + 7) * sv[0], cy + (r + 7) * sv[1],
                        I["axis"], "ref", H.DASH_REF))
        off = 6.0 if th == 0 else 0.0
        o.append(H.arrow(s, p, cx - off, cy, cx - off + n_len * n[0], cy + n_len * n[1], "dim", w="geom"))
        if c > 1e-9:
            o.append(H.arrow(s, p, cx + off, cy, cx + off, cy - t_scale * c, "force"))
        if th == 45.0:
            na = (cx + t_n * t_scale * n[0], cy + t_n * t_scale * n[1])
            ta = (cx + t_s * t_scale * sv[0], cy + t_s * t_scale * sv[1])
            tip = (cx, cy - t_scale * c)
            o.append(H.line(s, na[0], na[1], tip[0], tip[1], I["rule"], "leader", H.DASH_REF))
            o.append(H.line(s, ta[0], ta[1], tip[0], tip[1], I["rule"], "leader", H.DASH_REF))
            o.append(H.arrow(s, p, cx, cy, ta[0], ta[1], "geometry"))
        if th == 90.0:
            o.append(circ(cx, cy, s(3.2), RED, "#fff", s(1)))
        ly = cy + r + 22
        o.append(lab(s, cx, ly, f"θ = {th:.0f}°", "label", I["primary"], "middle"))
        if c > 1e-9:
            o.append(lab(s, cx, ly + 18, f"t = {c:.2f} σ", "label2", I["primary"], "middle"))
            o.append(lab(s, cx, ly + 34, f"normal {t_n:.2f} σ", "label2", I["secondary"], "middle"))
            o.append(lab(s, cx, ly + 50, f"shear {t_s:.2f} σ", "label2", I["secondary"], "middle"))
        else:
            o.append(lab(s, cx, ly + 18, "t = 0", "label2", I["primary"], "middle"))
            o.append(lab(s, cx, ly + 34, "no force across", "label2", I["secondary"], "middle"))
            o.append(lab(s, cx, ly + 50, "a parallel cut", "label2", I["secondary"], "middle"))
        o.append(lab(s, cx + (n_len + 8) * n[0] - off + (2 if th == 90 else 0), cy + (n_len + 8) * n[1] + (7 if th == 90 else 4),
                     it("n"), "label2", I["secondary"], "middle" if th == 0 else "start"))
    o.append(lab(s, 108, 272, "uniaxial pull σ: t = σ n = σ cos θ,", "label2", I["primary"]))
    o.append(lab(s, 108, 288, "always along the pull, but a different", "label2", I["primary"]))
    o.append(lab(s, 108, 304, "size and split on every cut", "label2", I["primary"]))
    o.append(credit(s, 10, 321, 66))
    aria = ("A femur in axial tension with one point on the shaft magnified three times. In each magnified disc the same "
            "pull sigma acts, and a dashed cut passes through the point with its normal n at angle theta to the pull. At "
            "0 degrees the traction t equals sigma in full along the pull. At 45 degrees t is 0.71 sigma along the pull, "
            "splitting into a normal part of 0.50 sigma and a shear part of 0.50 sigma. At 90 degrees, a cut parallel to "
            "the pull, t is zero. One stress, three different tractions: t depends on the cut, so a tensor is needed.")
    return finish(VB, aria, s, o)


# ================================================================ svg #20  C2: six, not nine
def fig20():
    p = "m16f20_"
    VB = (0, 0, 400, 300)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    x0, y0, a = 46.0, 70.0, 116.0
    cx, cy = x0 + a / 2, y0 + a / 2
    o.append(rect(x0, y0, a, a, BOX, I["rule"], s(1.2), 3))
    L1 = 32.0
    o.append(H.arrow(s, p, x0 + a, cy, x0 + a + L1, cy, "force"))
    o.append(H.arrow(s, p, x0, cy, x0 - L1, cy, "force"))
    o.append(H.arrow(s, p, cx, y0, cx, y0 - L1, "force"))
    o.append(H.arrow(s, p, cx, y0 + a, cx, y0 + a + L1, "force"))
    d, m = 11.0, 27.0
    o.append(H.arrow(s, p, x0 + a - d, cy + m, x0 + a - d, cy - m, "geometry"))        # tau_xy on the +x face, up
    o.append(H.arrow(s, p, x0 + d, cy - m, x0 + d, cy + m, "geometry"))                # tau_xy on the -x face, down
    o.append(H.arrow(s, p, cx - m, y0 + d, cx + m, y0 + d, "geometry"))                # tau_yx on the +y (top) face, right
    o.append(H.arrow(s, p, cx + m, y0 + a - d, cx - m, y0 + a - d, "geometry"))        # tau_yx on the bottom face, left
    o.append(lab(s, x0 + a + L1 + 4, cy + 5, f"σ{sub('xx', s)}", "label", I["primary"]))
    o.append(lab(s, cx + 8, y0 - L1 + 4, f"σ{sub('yy', s)}", "label", I["primary"]))
    o.append(lab(s, x0 + a - d - 6, cy + 5, f"τ{sub('xy', s)}", "label2", I["primary"], "end"))
    o.append(lab(s, cx, y0 + d + 22, f"τ{sub('yx', s)}", "label2", I["primary"], "middle"))
    o.append(lab(s, cx, y0 + a + L1 + 18, "stress element, x–y faces", "label2", I["secondary"], "middle"))
    o.append(lab(s, cx, y0 + a + L1 + 34, "(the z faces are not drawn)", "label2", I["muted"], "middle"))
    mx, my, cw, chh = 238.0, 70.0, 50.0, 38.0
    names = "xyz"
    o.append(lab(s, mx + 1.5 * cw, my - 14, f"σ{sub('ij', s, 'label')} = σ{sub('ji', s, 'label')}", "label", I["primary"], "middle"))
    for i in range(3):
        for j in range(3):
            x, y = mx + j * cw, my + i * chh
            sym = ("σ" if i == j else "τ") + sub(names[i] + names[j], s)
            if i == j:
                o.append(rect(x, y, cw, chh, RED, I["rule"], s(1.0), 0, 'fill-opacity="0.22"'))
                o.append(lab(s, x + cw / 2, y + chh / 2 + 5, sym, "label2", I["primary"], "middle"))
            elif j > i:
                o.append(rect(x, y, cw, chh, BLUE, I["rule"], s(1.0), 0, 'fill-opacity="0.22"'))
                o.append(lab(s, x + cw / 2, y + chh / 2 + 5, sym, "label2", I["primary"], "middle"))
            else:
                o.append(rect(x, y, cw, chh, "#fff", I["rule"], s(1.0), 0, dash_attr(s, 3, 2)))
                o.append(lab(s, x + cw / 2, y + chh / 2 + 5, sym, "label2", I["muted"], "middle"))
    yb = my + 3 * chh
    o.append(lab(s, mx, yb + 20, "3 normal + 3 shear", "label2", I["primary"]))
    o.append(lab(s, mx, yb + 36, "= 6 independent", "label2", I["primary"]))
    o.append(lab(s, mx, yb + 56, "dashed cells repeat the", "label2", I["secondary"]))
    o.append(lab(s, mx, yb + 72, "cells across the diagonal", "label2", I["secondary"]))
    ly = yb + 98
    o.append(rect(mx, ly - 10, 14, 10, RED, I["rule"], 0.8, 0, 'fill-opacity="0.22"'))
    o.append(lab(s, mx + 19, ly, "normal", "label2", I["secondary"]))
    o.append(rect(mx + 84, ly - 10, 14, 10, BLUE, I["rule"], 0.8, 0, 'fill-opacity="0.22"'))
    o.append(lab(s, mx + 103, ly, "shear", "label2", I["secondary"]))
    aria = ("A square stress element with normal stresses sigma x x and sigma y y drawn outward in red on its faces, and "
            "complementary shear stresses tau x y and tau y x drawn in blue along its faces so that the couples cancel. "
            "Beside it the three by three array of stress components: three red normal entries on the diagonal, three blue "
            "shear entries above it, and three dashed entries below it that repeat the upper ones because sigma i j "
            "equals sigma j i, leaving six independent components.")
    return finish(VB, aria, s, o)


# ================================================================ svg #22  C4: the zero eigenvalue
def fig22():
    p = "m16f22_"
    VB = (0, 0, 400, 282)
    s = H.Scale(VB[2], VB[3], display_w=400)
    ke = np.array([[1.0, -1.0], [-1.0, 1.0]])                  # k_e in units of EA/L (line 223)
    w, v = np.linalg.eigh(ke)
    assert abs(w[0]) < 1e-12 and abs(w[1] - 2.0) < 1e-12        # eigenvalues 0 and 2 EA/L (line 228)
    assert abs(abs(v[0, 0]) - abs(v[1, 0])) < 1e-12 and v[0, 0] * v[1, 0] > 0      # (1, 1)
    assert v[0, 1] * v[1, 1] < 0                                                    # (1, -1)
    assert abs(np.linalg.det(ke[1:, 1:]) - 1.0) < 1e-12                             # node 1 fixed: [1], det > 0
    o = [f'<defs>{H.markers(p, s)}</defs>']
    x1, x2, hh = 78.0, 178.0, 24.0
    rows = [(60.0, "rigid"), (150.0, "stretch"), (240.0, "fixed")]
    for yc, kind in rows:
        if kind == "rigid":
            sh = 50.0
            o.append(bar(s, x1, x2, yc, hh, dashed=True))
            o.append(bar(s, x1 + sh, x2 + sh, yc, hh))
            for xn in (x1, x2):
                o.append(H.arrow(s, p, xn, yc - 22, xn + sh, yc - 22, "geometry"))
            o.append(node(s, x1 + sh, yc))
            o.append(node(s, x2 + sh, yc))
            o.append(lab(s, x1 + sh / 2, yc - 32, f"u{sub('1', s)}", "label2", BLUE, "middle"))
            o.append(lab(s, x2 + sh / 2, yc - 32, f"u{sub('2', s)}", "label2", BLUE, "middle"))
            o.append(H.arrow(s, p, x1 + sh, yc + 24, x2 + sh, yc + 24, "dim", both=True))
            o.append(lab(s, (x1 + x2) / 2 + sh, yc + 40, it("L") + " unchanged", "label2", I["secondary"], "middle"))
            t1, t2, t3 = "(1, 1): rigid shift", "eigenvalue 0", "no stretch, no energy"
        elif kind == "stretch":
            sh = 24.0
            o.append(bar(s, x1, x2, yc, hh, dashed=True))
            o.append(bar(s, x1 - sh, x2 + sh, yc, hh))
            o.append(H.arrow(s, p, x1, yc - 22, x1 - sh, yc - 22, "geometry"))
            o.append(H.arrow(s, p, x2, yc - 22, x2 + sh, yc - 22, "geometry"))
            o.append(node(s, x1 - sh, yc))
            o.append(node(s, x2 + sh, yc))
            o.append(lab(s, x1 - sh / 2, yc - 32, f"u{sub('1', s)}", "label2", BLUE, "middle"))
            o.append(lab(s, x2 + sh / 2, yc - 32, f"u{sub('2', s)}", "label2", BLUE, "middle"))
            o.append(H.arrow(s, p, x1 - sh, yc + 24, x2 + sh, yc + 24, "dim", both=True))
            o.append(lab(s, (x1 + x2) / 2, yc + 40, f"{it('L')} + u{sub('2', s)} − u{sub('1', s)}", "label2",
                         I["secondary"], "middle"))
            t1, t2, t3 = "(1, −1): pure stretch", f"eigenvalue 2{it('EA')}/{it('L')}", "energy is stored"
        else:
            sh = 50.0
            o.append(bar(s, x1, x2, yc, hh, dashed=True))
            o.append(bar(s, x1, x2 + sh, yc, hh))
            o.append(hatch_wall(s, x1, yc, 20))
            o.append(node(s, x1, yc))
            o.append(node(s, x2 + sh, yc))
            o.append(H.arrow(s, p, x2, yc - 22, x2 + sh, yc - 22, "geometry"))
            o.append(lab(s, x2 + sh / 2, yc - 32, f"u{sub('2', s)}", "label2", BLUE, "middle"))
            o.append(lab(s, x1 - 12, yc + 40, "fixed", "label2", I["secondary"], "middle"))
            t1, t2, t3 = "node 1 fixed", f"reduced matrix = {it('EA')}/{it('L')}", "positive: u is unique"
        o.append(lab(s, 262, yc - 12, t1, "label2", I["primary"]))
        o.append(lab(s, 262, yc + 4, t2, "label2", I["primary"]))
        o.append(lab(s, 262, yc + 20, t3, "label2", I["secondary"]))
    aria = ("Three bar-element cases with dashed outlines for the start and solid bars for the end. Top: both nodes move "
            "the same distance, mode (1, 1), a rigid shift that does not change the length L, eigenvalue 0 of the "
            "stiffness matrix, no energy. Middle: the nodes move apart, mode (1, minus 1), a pure stretch, eigenvalue "
            "2 EA over L. Bottom: node 1 is fixed to a wall, so the rigid mode is removed, the reduced matrix is EA over "
            "L, which is positive, and the displacement is unique.")
    return finish(VB, aria, s, o)


# ================================================================ svg #23  C5: bone has one modulus, tendon has a direction
E_MAT, E_F = 0.12, 1.38          # GPa, tendon directional stiffness anchors (module16.html lines 888, 874)
E_BONE = (15.0, 20.0)            # GPa, cortical bone modulus range (line 884)


def tendon_E(th_deg):
    return E_MAT + E_F * math.cos(math.radians(th_deg)) ** 4


def fig23():
    p = "m16f23_"
    VB = (0, 0, 400, 404)
    s = H.Scale(VB[2], VB[3], display_w=400)
    assert abs(tendon_E(0) - 1.50) < 1e-9 and abs(tendon_E(90) - 0.12) < 1e-9
    assert abs(tendon_E(0) / tendon_E(90) - 12.5) < 1e-9                  # ratio 12.5 (lines 311, 885)
    th_half = math.degrees(math.acos(((tendon_E(0) / 2 - E_MAT) / E_F) ** 0.25))
    assert abs(th_half - 35.0) < 0.3                                       # halves by 35 degrees (line 311)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(lab(s, 100, 22, "bone: one modulus", "label", I["primary"], "middle"))
    o.append(lab(s, 300, 22, "tendon: a direction", "label", I["primary"], "middle"))
    # bone: femur icon and a magnified disc of mineralised matrix, rods at random angles
    F = Femur(24, 36, 106)
    o.append(F.use(s))
    dcx, dcy, dr = 122.0, 80.0, 36.0
    o.append(circ(dcx, dcy, dr, BONE, BONE_L, s(1.2)))
    rng = random.Random(16)
    d = ""
    n = 0
    while n < 30:
        x, y = rng.uniform(-1, 1) * (dr - 7), rng.uniform(-1, 1) * (dr - 7)
        if x * x + y * y > (dr - 8) ** 2:
            continue
        a = rng.uniform(0, math.pi)
        q = 5.0
        d += f"M{dcx + x - q * math.cos(a):.1f},{dcy + y - q * math.sin(a):.1f}l{2 * q * math.cos(a):.1f},{2 * q * math.sin(a):.1f}"
        n += 1
    o.append(path(d, BONE_L, s(1.6), extra='stroke-linecap="round"'))
    ax, ay = F.P(29.0, 150.0)
    o.append(H.line(s, ax + 4, ay, dcx - dr - 2, dcy + 8, I["rule"], "leader", H.DASH_REF))
    o.append(lab(s, 52, 158, "mineral rods at every angle", "label2", I["secondary"]))
    # tendon strip with collagen lines, fibre direction a
    tx0, ty0, tw, th_ = 218.0, 56.0, 164.0, 60.0
    o.append(rect(tx0, ty0, tw, th_, T["tendon"][0], T["tendon"][1], s(1.0), 6))
    for k in range(1, 7):
        yy = ty0 + k * th_ / 7
        o.append(H.line(s, tx0 + 6, yy, tx0 + tw - 6, yy, COLL, "leader", extra='stroke-opacity="0.85"'))
    o.append(H.arrow(s, p, tx0 + 36, ty0 - 12, tx0 + 116, ty0 - 12, "geometry"))
    o.append(lab(s, tx0 + 124, ty0 - 8, it("a"), "label", BLUE))
    o.append(lab(s, tx0 + tw / 2, ty0 + th_ + 18, "collagen fibres along a", "label2", I["secondary"], "middle"))
    # polar stiffness: radius = E(theta) / E(0), theta from the fibre direction a (horizontal)
    R, pcy = 58.0, 234.0
    pcx = (100.0, 300.0)
    pts_b, pts_t = [], []
    for th in range(0, 361, 5):
        c, sn = math.cos(math.radians(th)), math.sin(math.radians(th))
        pts_b.append((pcx[0] + R * c, pcy - R * sn))
        rt = tendon_E(th) / tendon_E(0)
        pts_t.append((pcx[1] + R * rt * c, pcy - R * rt * sn))
    for cxp in pcx:
        o.append(circ(cxp, pcy, R / 2, "none", GRID, s(1.0)))
        o.append(circ(cxp, pcy, R, "none", GRID, s(1.0)))
        o.append(H.line(s, cxp - R - 8, pcy, cxp + R + 8, pcy, I["axis"], "leader", H.DASH_REF))
    pl = lambda pts, col: (f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{col}" '  # noqa: E731
                           f'stroke-width="{s(H.PX["curve"]):.2f}" stroke-linejoin="round"/>')
    o.append(pl(pts_b, SER[1]))
    o.append(pl(pts_t, SER[0]))
    for cxp in pcx:
        o.append(lab(s, cxp + R + 10, pcy - 4, "a", "label2", I["secondary"], "start", 'font-style="italic"'))
    o.append(lab(s, pcx[0], pcy + R + 20, f"E ≈ {E_BONE[0]:.0f}–{E_BONE[1]:.0f} GPa", "label2", I["primary"], "middle"))
    o.append(lab(s, pcx[0], pcy + R + 36, "at every angle", "label2", I["primary"], "middle"))
    o.append(lab(s, pcx[1], pcy + R + 20, f"E = {tendon_E(0):.2f} GPa along a,", "label2", I["primary"], "middle"))
    o.append(lab(s, pcx[1], pcy + R + 36, f"{tendon_E(90):.2f} GPa across (ratio {tendon_E(0) / tendon_E(90):.1f})", "label2",
                 I["primary"], "middle"))
    o.append(lab(s, 200, 354, "polar plots: radius = E(θ) / E(0), θ measured from a", "label2", I["secondary"], "middle"))
    lg = plegend(s, 130, 372, [(SER[1], "bone", None), (SER[0], "tendon", None)])
    o.append(lg)

    def hv(cxp, fE, name):
        out = []
        for th in range(0, 181, 3):
            c, sn = math.cos(math.radians(th)), math.sin(math.radians(th))
            r_ = fE(th)
            out.append([cxp + R * r_ * c, [pcy - R * r_ * sn, pcy + R * r_ * sn],
                        f"{name}, θ = {th}° from a: E(θ)/E(0) = {r_:.2f}"])
        return sorted(out, key=lambda q: q[0])
    boxb = [pcx[0] - R, pcy - R, pcx[0] + R, pcy + R]
    boxt = [pcx[1] - R, pcy - R, pcx[1] + R, pcy + R]
    hvb = hv(pcx[0], lambda th: 1.0, "bone")
    hvt = hv(pcx[1], lambda th: tendon_E(th) / tendon_E(0), "tendon")
    aria = ("Left: a femur with one point magnified, showing short mineral rods at random angles, and below it a circular "
            "polar plot of stiffness against load direction: the same modulus, about 15 to 20 GPa, at every angle. Right: "
            "a tendon strip of aligned collagen fibres with the fibre direction a, and below it a peanut-shaped polar plot "
            "of stiffness E of theta, 1.50 GPa along the fibres and 0.12 GPa across them, a ratio of 12.5, falling to half "
            "by about 35 degrees from the fibres.")
    o.append(credit(s, 10, 389, 70))
    return finish(VB, aria, s, o, H.hover_attr([(boxb, hvb), (boxt, hvt)]))


# ================================================================ svg #24  C6: the toe
K_FIB = 48.0                    # fibre stiffening rate (Lab B, line 483)
EPS_MAX = 0.10                  # the 10 % stretch of Fig. 8 (line 329)


def toe_stress(eps):
    return (math.exp(K_FIB * eps) - 1.0) / (math.exp(K_FIB * EPS_MAX) - 1.0)


def crimp_pts(x0, x1, yc, arc_ratio, waves=3, n=60):
    """Sinusoidal fibre between chord ends x0, x1 whose arc length is arc_ratio times the chord."""
    ch = x1 - x0
    lo, hi = 0.0, 0.5 * ch

    def arc(a):
        pts = [(x0 + ch * i / n, yc + a * math.sin(2 * math.pi * waves * i / n)) for i in range(n + 1)]
        return sum(math.dist(pts[i], pts[i + 1]) for i in range(n)), pts

    for _ in range(50):
        mid = (lo + hi) / 2
        if arc(mid)[0] < arc_ratio * ch:
            lo = mid
        else:
            hi = mid
    return arc((lo + hi) / 2)[1]


def fig24():
    p = "m16f24_"
    VB = (0, 0, 400, 360)
    s = H.Scale(VB[2], VB[3], display_w=400)
    e_star = math.log((math.exp(K_FIB * EPS_MAX) - 1) / (K_FIB * EPS_MAX)) / K_FIB      # tangent = secant stiffness
    assert 0.066 < e_star < 0.068
    o = [f'<defs>{H.markers(p, s)}</defs>']
    P = Plot(s, (56, 156, 388, 296), (0, 10), (0, 1.0))
    o.append(P.axes([(0, "0"), (2, "2"), (4, "4"), (6, "6"), (8, "8"), (10, "10")],
                    [(0, "0"), (0.5, "0.5"), (1.0, "1")], "strain ε (%)", "σ / σ(10 %)", grid=[0.5, 1.0], ytx=16))
    xs = [i / 10 for i in range(0, 101)]
    ys = [toe_stress(x / 100) for x in xs]
    sec = [x / 10 for x in xs]
    o.append(P.curve(xs, sec, SER[1], dash=(6, 4)))
    o.append(P.curve(xs, ys, SER[0]))
    o.append(P.dot(e_star * 100, toe_stress(e_star), O["flag"]))
    # direct labels, leaders, legend
    o.append(lab(s, P.X(0.3), P.Y(0.92), f"tangent = secant at ε = {e_star * 100:.1f} % (orange)", "label2", I["secondary"]))
    o.append(H.line(s, P.X(5.9), P.Y(0.86), P.X(e_star * 100) - 3, P.Y(toe_stress(e_star)) - 6, I["rule"], "leader"))
    o.append(lab(s, P.X(0.3), P.Y(0.58), "single modulus", "label2", I["secondary"]))
    o.append(H.line(s, P.X(1.5), P.Y(0.52), P.X(1.5), P.Y(0.16), I["rule"], "leader"))
    o.append(lab(s, P.X(9.9), P.Y(0.17), "fibre law", "label2", I["secondary"], "end"))
    o.append(plegend(s, 56, 140, [(SER[0], "fibre law, k = 48", None), (SER[1], "single modulus (secant)", (6, 4))]))
    # crimp sketches above the plot, at the strains of the dots
    for eps_pct, name in ((1.0, "crimped"), (5.0, "straightening"), (9.0, "nearly taut")):
        cx = P.X(eps_pct)
        ratio = (1 + EPS_MAX) / (1 + eps_pct / 100)
        pts = crimp_pts(cx - 34, cx + 34, 48.0, ratio)
        o.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{COLL}" '
                 f'stroke-width="{s(2.4):.2f}" stroke-linejoin="round"/>')
        for xe in (cx - 34, cx + 34):
            o.append(rect(xe - 2, 48 - 9, 4, 18, T["zdisc"][0], None, 0, 1))
        o.append(lab(s, cx, 76, name, "label2", I["secondary"], "middle"))
        o.append(lab(s, cx, 92, f"ε = {eps_pct:.0f} %", "label2", I["primary"], "middle"))
        o.append(H.line(s, cx, 98, cx, 108, I["rule"], "leader"))
        o.append(P.dot(eps_pct, toe_stress(eps_pct / 100), SER[0]))
    o.append(lab(s, 222, 20, "a collagen fibre, schematic: crimped until stretched out", "label2", I["secondary"], "middle"))
    o.append(lab(s, 200, 352, "red curve: exp(kε) − 1 with k = 48 (Lab B), scaled to 1 at ε = 10 %", "label2", I["muted"], "middle"))
    hv_pts = [[round(P.X(x), 2), [round(P.Y(y), 2), round(P.Y(sc), 2)],
               f"ε = {x:.1f} %: fibre law {y:.3f}, single modulus {sc:.3f}"] for x, y, sc in zip(xs, ys, sec)]
    aria = ("Stress against strain for a tendon fibre law, normalised to its value at 10 per cent strain. The fibre "
            "exponential law e to the 48 epsilon minus one, in red, stays near zero out to about 5 per cent, the compliant "
            "toe, then climbs steeply; a single-modulus line to 10 per cent, in blue, is above it at low strain and below "
            f"it at high strain, and the two tangents match at {e_star * 100:.1f} per cent strain. Three sketches of a "
            "collagen fibre above the plot show it crimped at 1 per cent, straightening at 5 per cent and nearly taut at "
            "9 per cent.")
    return finish(VB, aria, s, o, H.hover_attr(P.box, hv_pts))


# ================================================================ svg #29  D1: dx = F dX
F_DEF = np.array([[1.30, 0.35], [0.0, 1.15]])    # the F of the main-text Fig. 2 (grid cells 34 px -> 44.2 px, 11.9 px shear, 39.1 px)


def fig29():
    p = "m16f29_"
    VB = (0, 0, 400, 250)
    s = H.Scale(VB[2], VB[3], display_w=400)
    J = float(np.linalg.det(F_DEF))
    assert abs(J - 1.495) < 1e-9                                    # main-text Fig. 2 prints J = 1.49 (line 104)
    dX = np.array([0.40, 0.20])
    dx = F_DEF @ dX
    assert abs(dx[0] - 0.59) < 1e-12 and abs(dx[1] - 0.23) < 1e-12
    u = 100.0                                                       # px per unit of the reference patch side
    o = [f'<defs>{H.markers(p, s)}</defs>']

    def patch(ox, oy, M, stroke):
        """Patch X in [0,1]^2 mapped by M, origin bottom-left at (ox, oy), Y up the page."""
        f = lambda X, Y: (ox + u * (M[0, 0] * X + M[0, 1] * Y), oy - u * (M[1, 0] * X + M[1, 1] * Y))  # noqa: E731
        quad = [f(0, 0), f(1, 0), f(1, 1), f(0, 1)]
        out = [f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in quad)} Z" fill="{BOX}" stroke="{stroke}" '
               f'stroke-width="{s(1.4):.2f}" stroke-linejoin="round"/>']
        for k in (0.25, 0.5, 0.75):
            a, b = f(k, 0), f(k, 1)
            out.append(H.line(s, a[0], a[1], b[0], b[1], stroke, "leader", extra='stroke-opacity="0.55"'))
            a, b = f(0, k), f(1, k)
            out.append(H.line(s, a[0], a[1], b[0], b[1], stroke, "leader", extra='stroke-opacity="0.55"'))
        return out, f

    ref, fr = patch(34, 170, np.eye(2), T["bone"][1])
    dfm, fd = patch(212, 170, F_DEF, T["muscle"][1])
    o += ref + dfm
    X0 = np.array([0.15, 0.20])
    a0, a1 = fr(*X0), fr(*(X0 + dX))
    o.append(H.arrow(s, p, a0[0], a0[1], a1[0], a1[1], "geometry"))
    o.append(circ(a0[0], a0[1], s(3.2), "#fff", I["primary"], s(1.3)))
    o.append(lab(s, (a0[0] + a1[0]) / 2 + 4, (a0[1] + a1[1]) / 2 + 18, it("dX"), "label", BLUE, "middle"))
    b0, b1 = fd(*(F_DEF @ X0)), fd(*(F_DEF @ (X0 + dX)))
    o.append(H.arrow(s, p, b0[0], b0[1], b1[0], b1[1], "geometry"))
    o.append(circ(b0[0], b0[1], s(3.2), "#fff", I["primary"], s(1.3)))
    o.append(lab(s, (b0[0] + b1[0]) / 2 + 4, (b0[1] + b1[1]) / 2 + 18, it("dx"), "label", BLUE, "middle"))
    o.append(lab(s, fr(0.5, 0)[0], 196, "reference body, X", "label2", I["secondary"], "middle"))
    o.append(lab(s, fd(0.5, 0)[0] + 12, 196, "deformed body, x = χ(X)", "label2", I["secondary"], "middle"))
    o.append(H.arrow(s, p, 160, 124, 200, 124, "dim", w="geom"))
    o.append(lab(s, 180, 114, it("F"), "label", I["primary"], "middle"))
    o.append(lab(s, 200, 20, f"{bf('F')} = ∂x/∂X = {bf('I')} + ∂u/∂X", "label", I["primary"], "middle"))
    o.append(lab(s, 200, 38, f"here F = [[{F_DEF[0, 0]:.2f}, {F_DEF[0, 1]:.2f}], [{F_DEF[1, 0]:.0f}, {F_DEF[1, 1]:.2f}]], "
                 f"J = det F = {J:.3f}", "label2", I["secondary"], "middle"))
    o.append(lab(s, 200, 220, "χ(X + dX) = χ(X) + F dX + O(|dX|²), so dx = F dX", "label2", I["primary"], "middle"))
    o.append(lab(s, 200, 238, f"dX = ({dX[0]:.2f}, {dX[1]:.2f}) → dx = ({dx[0]:.2f}, {dx[1]:.2f}), patch side = 1", "label2",
                 I["secondary"], "middle"))
    aria = ("A square material patch with grid lines in the reference body on the left, and on the right the same patch "
            "after the deformation gradient F, a stretched and sheared parallelogram. A short blue material fibre dX in "
            "the reference patch, (0.40, 0.20), becomes the blue fibre dx, (0.59, 0.23), in the deformed patch: dx equals "
            "F dX, with F = [[1.30, 0.35], [0, 1.15]] and determinant J = 1.495.")
    return finish(VB, aria, s, o)


# ================================================================ svg #31  D3: the stress tetrahedron
def fig31():
    p = "m16f31_"
    VB = (0, 0, 400, 412)
    s = H.Scale(VB[2], VB[3], display_w=400)
    a_, b_, c_ = 1.0, 1.25, 1.1                                      # intercepts on the three axes (x1, x2, x3)
    O3 = np.array([0.0, 0.0, 0.0])
    Av, Bv, Cv = np.array([a_, 0, 0.0]), np.array([0, b_, 0.0]), np.array([0, 0, c_])
    area_o = 0.5 * np.linalg.norm(np.cross(Bv - Av, Cv - Av))        # oblique face A
    n = np.cross(Bv - Av, Cv - Av) / (2 * area_o)
    if n.sum() < 0:
        n = -n
    vol = a_ * b_ * c_ / 6.0
    hp = 3 * vol / area_o                                            # h' = 3V/A  (line 133: V = A h'/3)
    assert abs(vol - area_o * hp / 3) < 1e-12 and hp <= max(a_, b_, c_)
    for j, (e1, e2) in enumerate(((Bv, Cv), (Av, Cv), (Av, Bv))):   # axis faces have area A n_j
        assert abs(0.5 * np.linalg.norm(np.cross(e1, e2)) - area_o * n[j]) < 1e-12
    ox, oy, k = 96.0, 204.0, 84.0
    ax1 = np.array([-0.60, 0.42])                                    # x1 toward the viewer: down-left
    ax2 = np.array([1.0, 0.0])                                       # x2 to the right
    ax3 = np.array([0.0, -1.0])                                      # x3 up

    def pj(v):
        return (ox + k * (v[0] * ax1[0] + v[1] * ax2[0] + v[2] * ax3[0]), oy + k * (v[0] * ax1[1] + v[1] * ax2[1] + v[2] * ax3[1]))

    P0, PA, PB, PC = pj(O3), pj(Av), pj(Bv), pj(Cv)
    o = [f'<defs>{H.markers(p, s)}</defs>']

    def face(pts, fill, op):
        return (f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in pts)} Z" fill="{fill}" fill-opacity="{op}" '
                f'stroke="{I["axis"]}" stroke-width="{s(1.3):.2f}" stroke-linejoin="round"/>')

    o.append(face([P0, PA, PB], BOX, 0.9))
    o.append(face([P0, PA, PC], BOX, 0.9))
    o.append(face([P0, PB, PC], BOX, 0.9))
    o.append(face([PA, PB, PC], RED, 0.18))
    cen = lambda *ps: (sum(q[0] for q in ps) / len(ps), sum(q[1] for q in ps) / len(ps))  # noqa: E731
    gO = cen(PA, PB, PC)
    gx = {0: cen(P0, PB, PC), 1: cen(P0, PA, PC), 2: cen(P0, PA, PB)}
    dirs = {0: ax1, 1: ax2, 2: ax3}
    for j in range(3):                                               # tractions on the axis faces: outward normal is -e_j
        d = -dirs[j] / np.linalg.norm(dirs[j])
        o.append(H.arrow(s, p, gx[j][0], gx[j][1], gx[j][0] + 24 * d[0], gx[j][1] + 24 * d[1], "force"))
    nv = n[0] * ax1 + n[1] * ax2 + n[2] * ax3
    nv = nv / np.linalg.norm(nv)
    o.append(H.arrow(s, p, gO[0], gO[1], gO[0] + 26 * nv[0], gO[1] + 26 * nv[1], "dim", w="geom"))
    tv = np.array([nv[0] + 0.5, nv[1] - 0.15])
    tv = tv / np.linalg.norm(tv)
    o.append(H.arrow(s, p, gO[0], gO[1], gO[0] + 44 * tv[0], gO[1] + 44 * tv[1], "force"))
    o.append(lab(s, gO[0] + 46 * tv[0] + 4, gO[1] + 46 * tv[1] + 4, "t(n)", "label2", I["primary"]))
    o.append(lab(s, gO[0] + 28 * nv[0] - 3, gO[1] + 28 * nv[1] - 4, it("n"), "label2", I["secondary"], "end"))
    gv = ((P0[0] + PA[0] + PB[0] + PC[0]) / 4, (P0[1] + PA[1] + PB[1] + PC[1]) / 4)
    o.append(H.arrow(s, p, gv[0] + 22, gv[1] - 6, gv[0] + 22, gv[1] + 24, "load"))
    o.append(lab(s, gv[0] + 28, gv[1] + 18, it("b"), "label2", BROWN))
    for v, nm, dx_, dy_, an in ((Av, "1", -6, 14, "end"), (Bv, "2", 7, 5, "start"), (Cv, "3", 6, -4, "start")):
        q = pj(v)
        o.append(lab(s, q[0] + dx_, q[1] + dy_, f"x{sub(nm, s)}", "label2", I["secondary"], an))
    o.append(lab(s, P0[0] - 9, P0[1] - 6, "O", "label2", I["secondary"], "end"))
    o.append(lab(s, 200, 20, "tetrahedron: longest edge h, V = ⅓ A h′, h′ ≤ h", "label", I["primary"], "middle"))
    o.append(lab(s, 200, 38, f"drawn with h′ = {hp:.2f}, A = {area_o:.2f}, V = {vol:.3f}", "label2", I["secondary"], "middle"))
    # key
    kx, ky = 236.0, 84.0
    items = [("dim", "n: normal of the", "oblique face, area A"),
             ("force", "t(n): traction on it", ""),
             ("force", "−t" + sup("(j)", s) + ": tractions on", "axis faces, area A n" + sub("j", s)),
             ("load", "b: body force on", "the volume V")]
    y = ky
    for meaning, l1, l2 in items:
        o.append(H.arrow(s, p, kx, y - 4, kx + 20, y - 4, meaning, w="geom" if meaning == "dim" else None))
        o.append(lab(s, kx + 26, y, l1, "label2", I["primary"]))
        if l2:
            o.append(lab(s, kx + 26, y + 16, l2, "label2", I["primary"]))
            y += 44
        else:
            y += 28
    # ledger of powers of h (Newton's second law, line 134)
    y0 = 290.0
    cols = (16.0, 132.0, 212.0, 330.0)
    for x, t in zip(cols, ("term", "scales as", "divide by A", "as h → 0")):
        o.append(lab(s, x, y0, t, "label2", I["muted"]))
    o.append(H.line(s, 10, y0 + 6, 392, y0 + 6, GRID, "leader"))
    rows = [("t(n) A", "h²", "h⁰", "stays", RED),
            ("−Σ t" + sup("(j)", s) + " A n" + sub("j", s), "h²", "h⁰", "stays", RED),
            ("b V", "h³", "⅓ b h′, h¹", "→ 0", BROWN),
            ("ρ V " + xdd(s), "h³", "⅓ ρ h′ " + xdd(s) + ", h¹", "→ 0", I["secondary"])]
    for i, (t1, t2, t3, t4, col) in enumerate(rows):
        y = y0 + 26 + i * 22
        o.append(circ(7, y - 4, s(3.6), col, "#fff", s(0.8)))
        o.append(lab(s, cols[0] + 2, y, t1, "label2"))
        o.append(lab(s, cols[1], y, t2, "label2"))
        o.append(lab(s, cols[2], y, t3, "label2"))
        o.append(lab(s, cols[3], y, t4, "label2", I["primary"]))
    o.append(lab(s, 200, 404, "area terms stay O(1); volume terms keep one h and vanish", "label2",
                 I["secondary"], "middle"))
    aria = ("A tetrahedron with three faces normal to the axes x1, x2, x3 meeting at the origin O and one oblique face of "
            "area A with outward normal n. The axis faces have areas A n1, A n2 and A n3, red tractions act on every face, "
            "and a brown body force b acts on the volume V, one third of A times h prime. A table lists Newton's second law "
            "term by term: the two traction terms scale as h squared and stay finite after division by A; the body force "
            "and inertia terms scale as h cubed, keep one factor h after division by A, and vanish as h goes to zero.")
    return finish(VB, aria, s, o)


# ================================================================ svg #32  D4: moment balance on a cube
def fig32():
    from fractions import Fraction
    p = "m16f32_"
    VB = (0, 0, 400, 422)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    x0, y0, a = 135.0, 56.0, 130.0
    cx, cy = x0 + a / 2, y0 + a / 2
    o.append(rect(x0, y0, a, a, BOX, I["rule"], s(1.2), 3))
    m = 32.0
    o.append(H.arrow(s, p, x0 + a + 18, cy + m, x0 + a + 18, cy - m, "geometry"))      # sigma_ij on the +x face (up)
    o.append(H.arrow(s, p, x0 - 18, cy - m, x0 - 18, cy + m, "geometry"))              # on the -x face (down)
    o.append(H.arrow(s, p, cx - m, y0 - 18, cx + m, y0 - 18, "geometry"))              # sigma_ji on the +y (top) face (right)
    o.append(H.arrow(s, p, cx + m, y0 + a + 18, cx - m, y0 + a + 18, "geometry"))      # on the bottom face (left)

    def arc(r, a0, a1):
        pt = lambda ang: (cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang)))  # noqa: E731
        (xa, ya), (xb, yb) = pt(a0), pt(a1)
        return path(f"M{xa:.2f},{ya:.2f} A{r},{r} 0 {1 if abs(a1 - a0) > 180 else 0} {1 if a1 > a0 else 0} {xb:.2f},{yb:.2f}",
                    BROWN, s(H.PX["load"]),
                    extra=f'marker-end="url(#{p}a_load)"')
    o.append(arc(28, 40, -230))                                        # x-face pair: anticlockwise on the page (inner arc)
    o.append(arc(50, 215, 325))                                        # y-face pair: clockwise on the page (outer arc)
    o.append(lab(s, x0 + a + 26, cy + 5, f"σ{sub('ij', s)}", "label2", I["primary"]))
    o.append(lab(s, x0 - 26, cy + 5, f"σ{sub('ij', s)}", "label2", I["primary"], "end"))
    o.append(lab(s, cx, y0 - 26, f"σ{sub('ji', s)}", "label2", I["primary"], "middle"))
    o.append(lab(s, cx + m + 8, y0 + a + 23, f"σ{sub('ji', s)}", "label2", I["primary"]))
    o.append(lab(s, cx, cy + 5, "side h", "label2", I["muted"], "middle"))
    o.append(lab(s, 200, 232, f"inner brown arc: couple σ{sub('ij', s)} h³, anticlockwise", "label2", I["primary"], "middle"))
    o.append(lab(s, 200, 250, f"outer brown arc: couple σ{sub('ji', s)} h³, clockwise", "label2", I["primary"], "middle"))
    o.append(lab(s, 200, 270, "rotational inertia: ρ h⁵ × angular acceleration α", "label2", I["primary"], "middle"))
    o.append(lab(s, 200, 288, f"moment balance: (σ{sub('ij', s)} − σ{sub('ji', s)}) h³ = ρ h⁵ α", "label2", I["primary"], "middle"))
    # the powers of h, exact fractions
    y1 = 314.0
    cols = (40.0, 112.0, 196.0, 292.0)
    for x, t in zip(cols, ("h", "h³", "h⁵", "h⁵ / h³ = h²")):
        o.append(lab(s, x, y1, t, "label2", I["muted"]))
    o.append(H.line(s, 30, y1 + 6, 380, y1 + 6, GRID, "leader"))
    for i in range(4):
        h = Fraction(1, 2 ** i)
        assert h ** 5 / h ** 3 == h ** 2
        vals = ("1" if i == 0 else f"1/{2 ** i}", "1" if i == 0 else f"1/{2 ** (3 * i)}",
                "1" if i == 0 else f"1/{2 ** (5 * i)}", "1" if i == 0 else f"1/{2 ** (2 * i)}")
        y = y1 + 24 + i * 18
        for x, t in zip(cols, vals):
            o.append(lab(s, x, y, t, "label2", I["primary"]))
    o.append(lab(s, 200, 414, f"÷ h³ and h → 0: σ{sub('ij', s)} − σ{sub('ji', s)} = ρ h² α → 0, so σ{sub('ij', s)} = σ{sub('ji', s)}",
                 "label2", I["primary"], "middle"))
    aria = ("A cube of side h with the shear stress sigma i j on its two faces normal to i and the complementary shear "
            "sigma j i on its two faces normal to j, all drawn in blue, and two brown arcs for the couples they form: "
            "sigma i j times h cubed anticlockwise and sigma j i times h cubed clockwise. Below, a table of h, h cubed, "
            "h to the fifth and their ratio h squared for h of 1, 1/2, 1/4 and 1/8: the couples scale as h cubed and the "
            "rotational inertia as h to the fifth, so dividing by h cubed leaves sigma i j minus sigma j i equal to zero "
            "as h goes to zero.")
    return finish(VB, aria, s, o)


# ================================================================ svg #35  D7: the bar element from its energy
def fig35():
    p = "m16f35_"
    VB = (0, 0, 400, 350)
    s = H.Scale(VB[2], VB[3], display_w=400)
    ke = np.array([[1.0, -1.0], [-1.0, 1.0]])
    assert np.allclose(np.linalg.eigvalsh(ke), [0.0, 2.0])             # eigenvalues 0 and 2 EA/L (line 228)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    x1, x2, yc = 60.0, 180.0, 82.0
    o.append(bar(s, x1, x2, yc, 28))
    o.append(node(s, x1, yc))
    o.append(node(s, x2, yc))
    o.append(lab(s, x1, yc + 46, "node 1", "label2", I["secondary"], "middle"))
    o.append(lab(s, x2, yc + 46, "node 2", "label2", I["secondary"], "middle"))
    o.append(lab(s, (x1 + x2) / 2, yc + 5, f"{it('A')}, {it('E')}", "label2", I["primary"], "middle"))
    o.append(H.arrow(s, p, x1 - 6, yc, x1 - 40, yc, "force"))
    o.append(H.arrow(s, p, x2 + 6, yc, x2 + 40, yc, "force"))
    o.append(lab(s, x1 - 24, yc - 8, f"f{sub('1', s)}", "label2", RED, "middle", 'font-style="italic"'))
    o.append(lab(s, x2 + 24, yc - 8, f"f{sub('2', s)}", "label2", RED, "middle", 'font-style="italic"'))
    o.append(H.arrow(s, p, x1, yc + 28, x1 + 22, yc + 28, "geometry"))
    o.append(H.arrow(s, p, x2, yc + 28, x2 + 34, yc + 28, "geometry"))
    o.append(lab(s, x1 + 11, yc + 62, f"u{sub('1', s)}", "label2", BLUE, "middle"))
    o.append(lab(s, x2 + 17, yc + 62, f"u{sub('2', s)}", "label2", BLUE, "middle"))
    o.append(H.arrow(s, p, x1, yc - 32, x2, yc - 32, "dim", both=True))
    o.append(lab(s, (x1 + x2) / 2, yc - 38, it("L"), "label2", I["secondary"], "middle"))
    ex = 252.0
    o.append(lab(s, ex, 50, f"ε = (u{sub('2', s)} − u{sub('1', s)}) / L", "label2", I["primary"]))
    o.append(lab(s, ex, 70, f"W{sub('e', s)} = ½ E ε² × A L", "label2", I["primary"]))
    o.append(lab(s, ex, 90, f"= ½ (EA/L)(u{sub('2', s)} − u{sub('1', s)})²", "label2", I["primary"]))
    o.append(lab(s, ex, 112, f"f{sub('i', s)} = ∂W{sub('e', s)}/∂u{sub('i', s)}", "label2", I["secondary"]))
    # parabola W(D) and its tangent, k = EA/L = 1: W = (1/2) D^2, f2 = dW/dD = D, curvature = k
    P = Plot(s, (54, 176, 214, 278), (-2.0, 2.0), (0.0, 2.0))
    o.append(P.axes([(-2, "−2"), (-1, "−1"), (0, "0"), (1, "1"), (2, "2")], [(0, "0"), (1, "1"), (2, "2")],
                    "Δ = u₂ − u₁", "W", grid=[1.0], ytx=16))
    xs = [i / 40 for i in range(-80, 81)]
    ys = [0.5 * x * x for x in xs]
    o.append(P.curve(xs, ys, SER[0]))
    d0 = 1.2
    xa, xb = d0 - 0.75, d0 + 0.7
    o.append(f'<polyline points="{P.X(xa):.1f},{P.Y(0.5 * d0 * d0 + d0 * (xa - d0)):.1f} {P.X(xb):.1f},{P.Y(0.5 * d0 * d0 + d0 * (xb - d0)):.1f}" '
             f'fill="none" stroke="{SER[1]}" stroke-width="{s(H.PX["curve_multi"]):.2f}" stroke-dasharray="{s(6):.1f} {s(4):.1f}"/>')
    o.append(P.dot(d0, 0.5 * d0 * d0, O["flag"]))
    # element matrix and its eigenpairs
    mx, my = 244.0, 176.0
    o.append(lab(s, mx + 50, my, f"k{sub('e', s)} = (EA/L) ×", "label2", I["primary"], "middle"))
    for i, row in enumerate((("1", "−1"), ("−1", "1"))):
        for j, v in enumerate(row):
            o.append(rect(mx + j * 48, my + 10 + i * 32, 48, 32, BLUE if (i + j) % 2 == 0 else RED, I["rule"], s(1.0), 0,
                          'fill-opacity="0.2"'))
            o.append(lab(s, mx + j * 48 + 24, my + 10 + i * 32 + 21, v, "label2", I["primary"], "middle"))
    o.append(lab(s, mx, my + 96, "eigenvalue 0: (1, 1)", "label2", I["primary"]))
    o.append(lab(s, mx, my + 112, "eigenvalue 2EA/L: (1, −1)", "label2", I["primary"]))
    o.append(lab(s, mx, my + 134, "plot: k = EA/L = 1", "label2", I["secondary"]))
    o.append(lab(s, mx, my + 150, "orange dot: slope = f₂ = kΔ", "label2", I["secondary"]))
    o.append(lab(s, mx, my + 166, "curvature of W = k", "label2", I["secondary"]))
    hv_pts = [[round(P.X(x), 2), round(P.Y(y), 2), f"Δ = {x:.2f}: W = {y:.3f}, f₂ = kΔ = {x:.2f}"] for x, y in zip(xs, ys)]
    aria = ("A bar element of length L, area A and modulus E with nodes 1 and 2, end forces f1 and f2 in red and nodal "
            "displacements u1 and u2 in blue. Its strain is the elongation over L, so its energy is one half EA over L times "
            "the elongation squared. A parabola of that energy against the elongation, with k equal to 1, shows the force "
            "f2 as the slope of its tangent and k as its curvature, and the 2 by 2 element matrix EA over L times 1, minus 1, "
            "minus 1, 1 is its second derivative, with eigenvalues 0 and 2 EA over L.")
    return finish(VB, aria, s, o, H.hover_attr(P.box, hv_pts))


# ================================================================ svg #36  D8: assembly adds energies
def fig36():
    p = "m16f36_"
    VB = (36, 0, 296, 340)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    xs_, yc = (66.0, 176.0, 286.0), 56.0
    o.append(bar(s, xs_[0], xs_[1], yc, 28, STIFF[0], STIFF[1]))
    o.append(bar(s, xs_[1], xs_[2], yc, 28, SOFT[0], SOFT[1]))
    for i, x in enumerate(xs_):
        o.append(node(s, x, yc))
        o.append(lab(s, x, yc - 24, f"node {i + 1}", "label2", I["secondary"], "middle"))
    o.append(lab(s, (xs_[0] + xs_[1]) / 2, yc + 5, f"k{sub('1', s)}", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(lab(s, (xs_[1] + xs_[2]) / 2, yc + 5, f"k{sub('2', s)}", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(circ(xs_[1], yc, s(10), "none", O["flag"], s(2.0)))
    o.append(lab(s, xs_[1], yc + 38, "shared node", "label2", I["secondary"], "middle"))
    # the global matrix K = sum L^T k L
    mx, my, cw, chh = 100.0, 142.0, 66.0, 34.0
    Le = sub("e", s)
    o.append(lab(s, mx + 1.5 * cw, my - 14, f"K = Σ L{Le}{sup('T', s)} k{Le} L{Le}", "label", I["primary"], "middle"))
    k1, k2 = f"k{sub('1', s)}", f"k{sub('2', s)}"
    cells = [[(k1, 1), (f"−{k1}", 1), ("0", 0)],
             [(f"−{k1}", 1), (f"{k1} + {k2}", 3), (f"−{k2}", 2)],
             [("0", 0), (f"−{k2}", 2), (k2, 2)]]
    for i in range(3):
        for j in range(3):
            x, y = mx + j * cw, my + i * chh
            txt, kind = cells[i][j]
            if kind == 0:
                o.append(rect(x, y, cw, chh, "#fff", I["rule"], s(1.0)))
            elif kind == 1:
                o.append(rect(x, y, cw, chh, STIFF[0], I["rule"], s(1.0)))
            elif kind == 2:
                o.append(rect(x, y, cw, chh, SOFT[0], I["rule"], s(1.0)))
            else:
                o.append(f'<path d="M{x:.1f},{y:.1f} L{x + cw:.1f},{y:.1f} L{x:.1f},{y + chh:.1f} Z" fill="{STIFF[0]}"/>'
                         f'<path d="M{x + cw:.1f},{y:.1f} L{x + cw:.1f},{y + chh:.1f} L{x:.1f},{y + chh:.1f} Z" fill="{SOFT[0]}"/>'
                         f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{chh:.1f}" fill="none" stroke="{O["flag"]}" '
                         f'stroke-width="{s(2.0):.2f}"/>')
            o.append(lab(s, x + cw / 2, y + chh / 2 + 5, txt, "label2", I["primary"] if kind else I["muted"], "middle"))
    for j in range(3):
        o.append(lab(s, mx + j * cw + cw / 2, my + 3 * chh + 17, f"u{sub(str(j + 1), s)}", "label2", I["secondary"], "middle"))
        o.append(lab(s, mx - 8, my + j * chh + chh / 2 + 5, f"f{sub(str(j + 1), s)}", "label2", I["secondary"], "end"))
    o.append(lab(s, 184, 292, f"energy adds: ½ u{sup('T', s)}K u = Σ ½ u{Le}{sup('T', s)}k{Le}u{Le}", "label2",
                 I["primary"], "middle"))
    o.append(lab(s, 184, 310, f"node 2 collects k{sub('1', s)} + k{sub('2', s)}", "label2", I["secondary"], "middle"))
    o.append(rect(100, 322, 14, 10, STIFF[0], STIFF[1], 0.8) + lab(s, 119, 331, "element 1", "label2", I["secondary"]))
    o.append(rect(204, 322, 14, 10, SOFT[0], SOFT[1], 0.8) + lab(s, 223, 331, "element 2", "label2", I["secondary"]))
    aria = ("Two bar elements in a chain, element 1 with stiffness k1 between nodes 1 and 2 and element 2 with stiffness k2 "
            "between nodes 2 and 3, node 2 shared and ringed in orange. Below, the 3 by 3 global stiffness matrix: the k1 "
            "block in the upper left and the k2 block in the lower right overlap in one cell, the node 2 diagonal entry, "
            "where they add to k1 plus k2. Total energy is the sum of element energies.")
    return finish(VB, aria, s, o)


# ================================================================ svg #37  D9: fibre stress acts only along a
def fig37():
    p = "m16f37_"
    VB = (0, 0, 400, 270)
    s = H.Scale(VB[2], VB[3], display_w=400)
    a = np.array([1.0, 0.0])
    aa = np.outer(a, a)
    assert (aa == np.array([[1.0, 0.0], [0.0, 0.0]])).all()
    for nv, expect in (((1.0, 0.0), 1.0), ((0.0, 1.0), 0.0)):
        assert abs(float(np.linalg.norm(aa @ np.array(nv))) - expect) < 1e-12        # sigma_fib n ~ (a . n) a (line 307)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(lab(s, 200, 20, "tendon: the fibre term carries stress along a only", "label", I["primary"], "middle"))
    tx0, ty0, tw, th_ = 48.0, 84.0, 170.0, 80.0
    o.append(rect(tx0, ty0, tw, th_, T["tendon"][0], T["tendon"][1], s(1.0), 6))
    for k in range(1, 8):
        yy = ty0 + k * th_ / 8
        o.append(H.line(s, tx0 + 6, yy, tx0 + tw - 6, yy, COLL, "leader", extra='stroke-opacity="0.85"'))
    o.append(H.arrow(s, p, tx0 + 20, ty0 - 16, tx0 + 90, ty0 - 16, "geometry"))
    o.append(lab(s, tx0 + 98, ty0 - 12, it("a"), "label", BLUE))
    o.append(lab(s, tx0 + 118, ty0 - 12, "fibre direction", "label2", I["secondary"]))
    cxv = tx0 + tw * 0.62
    o.append(H.line(s, cxv, ty0 - 6, cxv, ty0 + th_ + 6, I["axis"], "ref", H.DASH_REF))
    o.append(H.arrow(s, p, cxv, ty0 + th_ * 0.62, cxv + 44, ty0 + th_ * 0.62, "force"))
    o.append(lab(s, cxv + 48, ty0 + th_ * 0.62 + 5, "W′ a", "label2", RED))
    cyh = ty0 + th_ * 0.25
    o.append(H.line(s, tx0 - 8, cyh, tx0 + 62, cyh, I["axis"], "ref", H.DASH_REF))
    o.append(circ(tx0 + 28, cyh, s(3.4), RED, "#fff", s(1)))
    o.append(lab(s, tx0 + 36, cyh - 7, "0", "label2", RED, "start"))
    o.append(H.arrow(s, p, tx0 + tw + 4, ty0 + th_ / 2 + 20, tx0 + tw + 34, ty0 + th_ / 2 + 20, "force"))
    o.append(H.arrow(s, p, tx0 - 4, ty0 + th_ / 2 + 20, tx0 - 34, ty0 + th_ / 2 + 20, "force"))
    o.append(lab(s, tx0 + tw + 19, ty0 + th_ / 2 + 42, "σ" + sub("fib", s), "label2", I["primary"], "middle"))
    o.append(lab(s, tx0, ty0 + th_ + 22, "vertical cut, n ∥ a: t = W′ a", "label2", I["primary"]))
    o.append(lab(s, tx0, ty0 + th_ + 40, "horizontal cut, n ⟂ a: t = 0", "label2", I["primary"]))
    mx, my = 280.0, 78.0
    o.append(lab(s, mx + 40, my - 8, "a ⊗ a", "label", I["primary"], "middle", 'font-style="italic"'))
    for i in range(2):
        for j in range(2):
            v = aa[i, j]
            o.append(rect(mx + j * 40, my + i * 40, 40, 40, RED, I["rule"], s(1.0), 0, f'fill-opacity="{0.22 if v else 0.0}"'))
            o.append(lab(s, mx + j * 40 + 20, my + i * 40 + 25, f"{v:.0f}", "label", I["primary"], "middle"))
    o.append(lab(s, mx - 14, my + 104, "σ" + sub("fib", s) + " = W′ a ⊗ a", "label2", I["primary"]))
    o.append(lab(s, mx - 14, my + 122, "n = (1, 0): t = W′ a", "label2", I["primary"]))
    o.append(lab(s, mx - 14, my + 140, "n = (0, 1): t = 0", "label2", I["primary"]))
    o.append(lab(s, 200, 258, "σ" + sub("fib", s) + " n = W′ (a·n) a, which is zero for n ⟂ a", "label2", I["secondary"], "middle"))
    aria = ("A tendon strip of aligned collagen fibres with the fibre direction a in blue. A cut across the fibres, normal "
            "parallel to a, carries a red traction W prime times a along the fibres; a cut along the fibres, normal "
            "perpendicular to a, carries zero. Beside it the outer-product matrix a tensor a for a along the first axis, "
            "[[1, 0], [0, 0]], so sigma fibre equals W prime a tensor a and acts only along a.")
    return finish(VB, aria, s, o)


# ================================================================ svg #42  K3: the localisation sweep
def fig42():
    p = "m16f42_"
    VB = (0, 0, 400, 372)
    s = H.Scale(VB[2], VB[3], display_w=400)
    rs = [10 ** (3 * i / 120) for i in range(121)]
    frac = lambda r: r / (1 + r)  # noqa: E731
    assert [round(100 * frac(r), 1) for r in (1, 10, 100, 1000)] == [50.0, 90.9, 99.0, 99.9]      # line 671
    o = [f'<defs>{H.markers(p, s)}</defs>']
    r10 = 10.0
    xl, seg = 96.0, 96.0
    yc0, yc1 = 40.0, 98.0
    o.append(bar(s, xl, xl + seg, yc0, 28, STIFF[0], STIFF[1]))
    o.append(bar(s, xl + seg, xl + 2 * seg, yc0, 28, SOFT[0], SOFT[1]))
    tot = 44.0
    ds, dl = tot / (1 + r10), tot * r10 / (1 + r10)                 # series: same force, strain goes as 1/E
    o.append(bar(s, xl, xl + seg + ds, yc1, 28, STIFF[0], STIFF[1]))
    o.append(bar(s, xl + seg + ds, xl + 2 * seg + ds + dl, yc1, 28, SOFT[0], SOFT[1]))
    o.append(H.arrow(s, p, xl - 4, yc1, xl - 32, yc1, "force"))
    o.append(H.arrow(s, p, xl + 2 * seg + tot + 4, yc1, xl + 2 * seg + tot + 32, yc1, "force"))
    o.append(lab(s, xl - 36, yc1 - 6, "P", "label2", RED, "end", 'font-style="italic"'))
    o.append(lab(s, xl + 2 * seg + tot + 36, yc1 - 6, "P", "label2", RED, "start", 'font-style="italic"'))
    o.append(lab(s, xl - 10, yc0 + 5, "unloaded", "label2", I["secondary"], "end"))
    o.append(lab(s, xl - 10, yc1 + 36, f"loaded, r = {r10:.0f}: stiff takes {100 * ds / tot:.0f} %, soft {100 * dl / tot:.0f} % of the stretch",
                 "label2", I["secondary"], "start"))
    o.append(lab(s, xl + seg / 2, yc0 + 5, "stiff", "label2", I["primary"], "middle"))
    o.append(lab(s, xl + 1.5 * seg, yc0 + 5, "soft", "label2", I["primary"], "middle"))
    o.append(rect(100, 150, 14, 10, STIFF[0], STIFF[1], 0.8) + lab(s, 119, 159, "stiff, E" + sub("stiff", s), "label2", I["secondary"]))
    o.append(rect(212, 150, 14, 10, SOFT[0], SOFT[1], 0.8) + lab(s, 231, 159, "soft, E" + sub("soft", s), "label2", I["secondary"]))
    P = Plot(s, (62, 196, 380, 304), (0.0, 3.0), (40.0, 100.0))
    o.append(P.axes([(0, "1"), (1, "10"), (2, "100"), (3, "1000")], [(50, "50"), (75, "75"), (100, "100")],
                    "modulus ratio r", "soft share (%)", grid=[50, 75, 100], ytx=16))
    ys = [100 * frac(r) for r in rs]
    xs = [math.log10(r) for r in rs]
    o.append(P.curve(xs, ys, SER[0]))
    for r, dxl, dyl in ((1, 10, 4), (10, 8, 18), (100, 6, 18), (1000, -8, 18)):
        o.append(P.dot(math.log10(r), 100 * frac(r), O["flag"]))
        o.append(lab(s, P.X(math.log10(r)) + dxl, P.Y(100 * frac(r)) + dyl, f"{100 * frac(r):.1f} %".replace(".0 %", " %"),
                     "label2", I["primary"], "start" if dxl > 0 else "end"))
    o.append(lab(s, 221, 362, f"r = E{sub('stiff', s)} / E{sub('soft', s)}; soft share = r / (1 + r)", "label2", I["muted"], "middle"))
    hv_pts = [[round(P.X(x), 2), round(P.Y(y), 2), f"r = {r:.3g}: soft segment takes {y:.1f} %"] for x, y, r in zip(xs, ys, rs)]
    aria = ("A stiff and a soft segment of equal length in series, unloaded and then pulled by a force P at modulus ratio "
            "10, where the soft segment takes 91 per cent of the added length. Below, the share of the deformation taken "
            "by the soft segment, r over 1 plus r, against the ratio r from 1 to 1000 on a log axis, with marked values "
            "50, 90.9, 99.0 and 99.9 per cent.")
    return finish(VB, aria, s, o, H.hover_attr(P.box, hv_pts))


# ================================================================ svg #43  K4: the stress-concentration factor
def kt(rh):
    return 1.0 + 0.5 * math.sqrt(1.0 / rh)           # K_t = 1 + (1/2) sqrt(h/r), assumed handbook fit (line 675)


def fig43():
    p = "m16f43_"
    VB = (0, 0, 400, 392)
    s = H.Scale(VB[2], VB[3], display_w=400)
    assert [round(kt(v), 2) for v in (0.5, 0.25, 0.02)] == [1.71, 2.0, 4.54]
    assert round(kt(0.02) / kt(0.5), 1) == 2.7                                       # factor 2.7
    assert round(kt(0.02) * 2, 1) == 9.1                                             # nine times the thick-section stress
    assert round(100 * ((kt(0.25) - 1) / (kt(0.5) - 1) - 1)) == 41                   # excess +41 %
    assert round(100 * (kt(0.25) / kt(0.5) - 1)) == 17                               # peak +17 %
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # stepped bar, thick height 2h, thin height h, fillet radius r (drawn at r/h = 0.25)
    hh = 36.0
    yc = 100.0
    xl, xs_, xr = 62.0, 190.0, 330.0
    rr = 0.25 * hh
    top_thick, bot_thick = yc - hh, yc + hh
    top_thin, bot_thin = yc - hh / 2, yc + hh / 2
    d = (f"M{xl},{top_thick} L{xs_:.1f},{top_thick} L{xs_:.1f},{top_thin - rr:.1f} "
         f"A{rr:.1f},{rr:.1f} 0 0 0 {xs_ + rr:.1f},{top_thin:.1f} L{xr},{top_thin} L{xr},{bot_thin} L{xs_ + rr:.1f},{bot_thin} "
         f"A{rr:.1f},{rr:.1f} 0 0 0 {xs_:.1f},{bot_thin + rr:.1f} L{xs_:.1f},{bot_thick} L{xl},{bot_thick} Z")
    o.append(f'<path d="{d}" fill="{BOX}" stroke="{I["rule"]}" stroke-width="{s(1.4):.2f}" stroke-linejoin="round"/>')
    o.append(H.arrow(s, p, xl - 4, yc, xl - 36, yc, "force"))
    o.append(H.arrow(s, p, xr + 4, yc, xr + 36, yc, "force"))
    o.append(lab(s, xl - 38, yc - 8, "P", "label2", RED, "end", 'font-style="italic"'))
    o.append(lab(s, xr + 38, yc - 8, "P", "label2", RED, "start", 'font-style="italic"'))
    cxm, cym = xs_ + rr * (1 - math.cos(math.radians(45))), top_thin - rr * (1 - math.sin(math.radians(45)))
    o.append(circ(cxm, cym, s(4.4), O["flag"], "#fff", s(1.5)))
    o.append(lab(s, xl + 8, top_thick - 8, "thick part: σ", "label2", I["primary"]))
    o.append(lab(s, xs_ + 14, top_thin - 38, "peak at the re-entrant corner", "label2", I["secondary"]))
    o.append(H.line(s, xs_ + 28, top_thin - 34, cxm + 3, cym - 5, I["rule"], "leader"))
    o.append(lab(s, xr - 8, bot_thin + 18, "thin part: 2σ nominal", "label2", I["primary"], "end"))
    o.append(H.arrow(s, p, xr - 26, top_thin + 2, xr - 26, bot_thin - 2, "dim", both=True))
    o.append(lab(s, xr - 20, yc + 5, it("h"), "label2", I["secondary"], "start"))
    o.append(lab(s, xs_ - 12, bot_thin + 40, "fillet radius " + it("r"), "label2", I["secondary"], "end"))
    o.append(H.line(s, xs_ - 10, bot_thin + 33, xs_ + 3, bot_thin + 6, I["rule"], "leader"))
    o.append(lab(s, 200, 20, "stepped bar: area A, then A/2 (thin section h)", "label", I["primary"], "middle"))
    P = Plot(s, (62, 196, 380, 324), (0.0, 0.5), (1.0, 5.0))
    o.append(P.axes([(0, "0"), (0.1, "0.1"), (0.2, "0.2"), (0.3, "0.3"), (0.4, "0.4"), (0.5, "0.5")],
                    [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")], "fillet radius r / h (small = sharp)",
                    "Kt", grid=[2, 3, 4], ytx=16))
    xs = [0.02 + i * (0.5 - 0.02) / 120 for i in range(121)]
    ys = [kt(x) for x in xs]
    o.append(P.curve(xs, ys, SER[0]))
    for v, dx, dy, anch in ((0.02, 8, -8, "start"), (0.25, 10, -10, "start"), (0.5, -8, -12, "end")):
        o.append(P.dot(v, kt(v), O["flag"]))
        o.append(lab(s, P.X(v) + dx, P.Y(kt(v)) + dy, f"{kt(v):.2f}", "label2", I["primary"], anch))
    o.append(lab(s, P.X(0.13), P.Y(4.75), "Kt ≈ 1 + ½ √(h/r), assumed fit", "label2", I["secondary"]))
    o.append(lab(s, P.X(0.13), P.Y(4.75) + 16, f"sharpest: 4.54 × 2σ = {2 * kt(0.02):.1f} σ", "label2", I["secondary"]))
    o.append(lab(s, 221, 384, "the 1-D model reports 2σ; the fillet sets the peak", "label2", I["muted"], "middle"))
    hv_pts = [[round(P.X(x), 2), round(P.Y(y), 2), f"r/h = {x:.3f}: Kt = {y:.2f}, peak = {2 * y:.2f} σ"] for x, y in zip(xs, ys)]
    aria = ("A bar stepping from area A to A over 2 through a rounded fillet of radius r, pulled by a force P, with thick "
            "stress sigma, thin nominal stress 2 sigma, and an orange mark at the re-entrant corner where the peak occurs. "
            "Below, the assumed peak-stress factor K t equal to 1 plus half the square root of h over r against r over h "
            "from 0.02 to 0.5, marked at 4.54 for the sharpest fillet, 2.00 at 0.25 and 1.71 at 0.5.")
    return finish(VB, aria, s, o, H.hover_attr(P.box, hv_pts))


# ================================================================ svg #51  K9: design a composite bar
def fig51():
    import itertools
    p = "m16f51_"
    VB = (0, 0, 400, 470)
    s = H.Scale(VB[2], VB[3], display_w=400)
    L, P_, A0, nel = 0.10, 2000.0, 2e-4, 8                             # lines 793-794
    E_soft, E_stiff, budget = 5e9, 20e9, 4
    xn = np.linspace(0, L, nel + 1)
    Ael = A0 * (1 - 0.5 * (xn[:-1] + xn[1:]) / 2 / L)
    le = np.diff(xn)

    def tip(stiff):
        Ee = np.where(np.isin(np.arange(nel), stiff), E_stiff, E_soft)
        return float(np.sum(P_ * le / (Ee * Ael)))

    cases = list(itertools.combinations(range(nel), budget))
    best, worst = min(cases, key=tip), max(cases, key=tip)
    assert len(cases) == 70 and best == (4, 5, 6, 7) and worst == (0, 1, 2, 3)
    assert (round(tip([]) * 1e3, 4), round(tip(best) * 1e3, 4), round(tip(worst) * 1e3, 4)) == (0.2771, 0.1555, 0.1908)
    assert round(100 * (1 - tip(best) / tip(worst)), 1) == 18.5
    delta = P_ * le / Ael * (1 / E_soft - 1 / E_stiff)                 # sensitivity of each element (line 789)
    assert list(np.argsort(-delta)[:4]) == [7, 6, 5, 4]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    x0, bw, h0 = 62.0, 220.0, 40.0
    o.append(lab(s, 200, 20, "which four elements get the stiff material?", "label", I["primary"], "middle"))
    o.append(lab(s, 200, 40, "8 elements, 2 cm² tapering to 1 cm², tip load P = 2 kN", "label2", I["secondary"], "middle"))

    def tapered(yc, stiff):
        out = []
        for e in range(nel):
            xa, xb = x0 + e * bw / nel, x0 + (e + 1) * bw / nel
            ha, hb = h0 * (1 - 0.5 * e / nel), h0 * (1 - 0.5 * (e + 1) / nel)
            fill = STIFF if e in stiff else SOFT
            out.append(f'<path d="M{xa:.1f},{yc - ha / 2:.1f} L{xb:.1f},{yc - hb / 2:.1f} L{xb:.1f},{yc + hb / 2:.1f} '
                       f'L{xa:.1f},{yc + ha / 2:.1f} Z" fill="{fill[0]}" stroke="{I["rule"]}" stroke-width="{s(1.0):.2f}" '
                       f'stroke-linejoin="round"/>')
        out.append(hatch_wall(s, x0, yc, 22))
        out.append(H.arrow(s, p, x0 + bw + 3, yc, x0 + bw + 28, yc, "force"))
        return "".join(out)

    rows = [(82.0, (), "all soft", tip([])), (144.0, best, "best", tip(best)), (206.0, worst, "worst", tip(worst))]
    for yc, st, name, tv in rows:
        o.append(tapered(yc, st))
        o.append(lab(s, x0 + bw + 34, yc - 2, f"{tv * 1e3:.4f} mm", "label2", I["primary"]))
        o.append(lab(s, x0 + bw + 34, yc + 14, name, "label2", I["secondary"]))
    o.append(rect(100, 258, 14, 10, STIFF[0], STIFF[1], 0.8) + lab(s, 119, 267, "stiff, 20 GPa", "label2", I["secondary"]))
    o.append(rect(212, 258, 14, 10, SOFT[0], SOFT[1], 0.8) + lab(s, 231, 267, "soft, 5 GPa", "label2", I["secondary"]))
    PL = Plot(s, (62, 296, 380, 366), (-0.5, 7.5), (0.0, 40.0))
    o.append(PL.axes([(e, str(e)) for e in range(8)], [(0, "0"), (20, "20"), (40, "40")],
                     "element e (0 = fixed, wide end)", "Δ (µm)", grid=[20, 40], ytx=16))
    bwid = (PL.X(1) - PL.X(0)) * 0.62
    for e in range(8):
        yv = delta[e] * 1e6
        fill = STIFF if e in best else SOFT
        o.append(rect(PL.X(e) - bwid / 2, PL.Y(yv), bwid, PL.Y(0) - PL.Y(yv), fill[0], I["rule"], s(1.0)))
        o.append(lab(s, PL.X(e), PL.Y(yv) - 5, f"{yv:.1f}", "label2", I["primary"], "middle"))
    o.append(lab(s, 221, 430, f"Δ{sub('e', s)} = P ℓ{sub('e', s)}/A{sub('e', s)} × (1/E{sub('soft', s)} − 1/E{sub('stiff', s)})",
                 "label2", I["secondary"], "middle"))
    o.append(lab(s, 221, 446, "the gain from stiffening element e; geometry alone ranks it", "label2", I["secondary"], "middle"))
    o.append(lab(s, 221, 462, f"best beats worst by {100 * (1 - tip(best) / tip(worst)):.1f} % of the tip displacement", "label2",
                 I["secondary"], "middle"))
    hv_pts = [[round(PL.X(e), 2), round(PL.Y(delta[e] * 1e6), 2), f"element {e}: gain {delta[e] * 1e6:.1f} µm"] for e in range(8)]
    aria = ("Three tapered eight-element bars, wide end fixed on the left and a 2 kN tip load on the right, with four "
            "elements stiff, 20 GPa, and four soft, 5 GPa: all soft gives a tip displacement of 0.2771 mm, the best "
            "placement with elements 4 to 7 stiff, the thin half, gives 0.1555 mm, and the worst, elements 0 to 3 stiff, "
            "gives 0.1908 mm, so the best beats the worst by 18.5 per cent. Below, the gain from stiffening each element, "
            "which depends on geometry alone and rises from 19.4 micrometres at the wide end to 35.3 at the thin end.")
    return finish(VB, aria, s, o, H.hover_attr(PL.box, hv_pts))


FIGS = {
    19: (r"C1: why a tensor. Why can a single number not describe the s", fig19),
    20: (r"C2: six, not nine. The stress tensor has nine components but", fig20),
    22: (r"C4: why a structure needs a support. The bar element's stiff", fig22),
    23: (r"C5: isotropic bone, anisotropic tendon. Why model bone with ", fig23),
    24: (r"C6: the toe. Why is a tendon compliant at low load and stiff", fig24),
    29: (r"D1: the deformation gradient. From the deformation map, deri", fig29),
    31: (r"D3: which power of h kills which term. Redo the tetrahedron ", fig31),
    32: (r"D4: stress symmetry. Derive $\sigma_{ij}=\sigma_{ji}$ from m", fig32),
    35: (r"D7: the bar element. Derive the $2\times2$ bar stiffness mat", fig35),
    36: (r"D8: assembly. Show the global stiffness is the sum of elemen", fig36),
    37: (r"D9: fibre stress. Show the fibre reinforcement contributes s", fig37),
    42: (r"K3: the localisation sweep (sensitivity). Put a soft and a s", fig42),
    43: (r"K4: the stress-concentration factor (sweep). A bar steps fro", fig43),
    51: (r"K9: design a composite bar. Four of eight bar elements may b", fig51),
}
