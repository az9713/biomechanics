"""Module 14 body group `body_main`: femur and body figures, in the house style.

Main text (760 px): svg #2 (Fig. 1 hip: neck fracture, cartilage loss), #3 (Fig. 2 six drifting parameters),
#6 (Fig. 5 sideways fall: impact against bone strength), #12 (Fig. 10 coupled-drift network).
Problem figures (400 px): #23 C3, #24 C4, #33 D3, #38 D8.
Art: NIH NIAID BioArt 244 (public domain). The m02 hip crop (pelvis above, upper femur below) is put on the page
once by SHARED_DEFS() as the <image> #m14art_hip and <use>d by #2 (twice), #6, #23, #24, #38. No Lynch body kit: no m14 figure uses it.
Every plotted number is computed here from a value or formula module14.html states (line numbers beside each constant).
Colours, one meaning each: external load / impact force = load brown, bone strength = bone fill, margin and
density curves = SERIES red / blue, dimensions = geometry blue, load that maintains tissue = load brown,
causal links = dim grey, muscle pull on bone = force red.
"""
import html
import math
import re

import numpy as np

import house as H
from m02.bone import HEAD, HIP, hip_art
from m05.body import art_image, wrap
from m05.plots_prob import Plot, hov
from m05.plots_prob import label as plabel
from m05.plots_prob import legend as plegend
from m05.tissue import circ, legend, path, rect, sw_line

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
BOX, GRID = "#f7f4ef", "#e6e6e6"
HIP_ID = "m14art_hip"
NECK = (39.2, 67.2)                                     # art units: centre of the femoral neck, measured on the crop
TROCH = (8.5, 62.0)                                     # art units: lateral surface of the greater trochanter
CART = "#8cc4e4"                                        # cartilage layer fill (a strengthened T["cartilage"], too pale on bone)
HIP_IMG = art_image("<svg>" + hip_art() + "</svg>", HIP).replace("<image ", f'<image id="{HIP_ID}" ', 1)

# ---------------------------------------------------------------- numbers the module states
G, HF, M_EFF, K_SPR = 9.81, 0.70, 35.0, 40000.0          # line 145: h_f 0.70 m, m_eff 35 kg, k 40 kN/m
V_IMP = math.sqrt(2 * G * HF)                             # line 144: v = sqrt(2 g h_f) = 3.7 m/s
F_PEAK = V_IMP * math.sqrt(M_EFF * K_SPR)                 # line 144: F = v sqrt(m_eff k), 4385 N (line 147)
X_MAX = V_IMP * math.sqrt(M_EFF / K_SPR)                  # line 147: x_max = v sqrt(m_eff / k) = 11.0 cm
S0 = 7000.0                                               # line 151, 454: young femoral neck, 7 kN
assert abs(V_IMP - 3.7) < 0.01 and round(F_PEAK) == 4385 and abs(X_MAX * 100 - 11.0) < 0.05
assert abs(0.8 ** 2 * S0 - 4480) < 1e-6 and abs(0.6 ** 2 * S0 - 2520) < 1e-6      # lines 137, 151: 0.64 S0, 0.36 S0 ~ 2.5 kN
assert abs(math.sqrt(F_PEAK / S0) - 0.79) < 0.005                                  # line 454: critical density 0.79
assert abs(math.sqrt(F_PEAK / math.sqrt(2) / S0) - 0.67) < 0.005                   # line 454: halved k, 0.67
E_KIN = 0.5 * M_EFF * V_IMP ** 2                                                   # J; equals 1/2 k x_max^2
assert abs(E_KIN - 0.5 * K_SPR * X_MAX ** 2) < 1e-6


def SHARED_DEFS():
    return HIP_IMG


# ---------------------------------------------------------------- helpers
def it(v):
    return f'<tspan font-style="italic">{v}</tspan>'


def esc(t):
    return html.escape(t)


def lab(s, x, y, text, size="label2", col=None, anchor="start", extra=""):
    return H.label(s, x, y, text, size, col or I["primary"], anchor, extra)


def finish(vb, aria, s, body, extra=""):
    body = "".join(body)
    body = re.sub(r'<marker id="([^"]+)".*?</marker>',
                  lambda m: m.group(0) if f"url(#{m.group(1)})" in body else "", body)
    return H.svg_open(vb, esc(aria), s, extra) + body.replace("<defs></defs>", "") + "</svg>"


def credit(s, vb, n, text):
    cr = H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt (Ryan Kissinger)", title="Human Upper Leg Bones (BioArt 244)",
                                    changes=text)
    lines = wrap(cr, n)
    return H.credit(s, 8, vb[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines)


class Hip:
    """The hip crop (pelvis above, upper femur below), placed at screen (X0, Y0) with K screen units per art unit."""

    def __init__(self, X0, Y0, K):
        self.X0, self.Y0, self.K = X0, Y0, K
        self.w, self.h = HIP[2] * K, HIP[3] * K

    def f(self, q):
        return self.X0 + (q[0] - HIP[0]) * self.K, self.Y0 + (q[1] - HIP[1]) * self.K

    def use(self):
        return (f'<use href="#{HIP_ID}" transform="translate({self.X0 - HIP[0] * self.K:.2f} '
                f'{self.Y0 - HIP[1] * self.K:.2f}) scale({self.K})"/>')

    def neck_ring(self, s, r=22, col=None):
        c = self.f(NECK)
        col = col or O["flag"]
        return (f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{s(r):.2f}" fill="none" stroke="#fff" stroke-width="{s(4.5):.2f}"/>'
                f'<circle cx="{c[0]:.2f}" cy="{c[1]:.2f}" r="{s(r):.2f}" fill="none" stroke="{col}" stroke-width="{s(2.5):.2f}"/>')


def strength_bars(s, P, items, fkn, flab):
    """Bars of bone strength S (kN) against the dashed fall-impact line F. items = [(name, S_N)]."""
    o = []
    x0, y1, x1, y0 = P.box
    o.append(H.line(s, x0, y0, x1, y0, I["axis"], "axis"))
    o.append(H.line(s, x0, y0, x0, y1, I["axis"], "axis"))
    for v in range(0, 9, 2):
        o.append(H.line(s, x0 - 5, P.Y(v), x0, P.Y(v), I["axis"], "leader"))
        o.append(plabel(s, x0 - 8, P.Y(v) + 4.5, f"{v}", "tick", I["secondary"], "end"))
    pts = []
    n = len(items)
    for i, (name, S) in enumerate(items):
        cx = P.X((i + 0.5) * 3.0 / n)
        bw = (x1 - x0) / n * 0.5
        o.append(rect(cx - bw / 2, P.Y(S / 1000), bw, P.y0 - P.Y(S / 1000), T["bone"][0], T["bone"][1], 1.2))
        o.append(plabel(s, cx, P.Y(S / 1000) - 7, f"{S / 1000:.1f} kN", "label2", I["primary"], "middle"))
        m = S / F_PEAK
        o.append(plabel(s, cx, y0 + 19, name, "label2", I["primary"], "middle"))
        o.append(plabel(s, cx, y0 + 36, f"S/F {m:.2f}", "label2", I["secondary"], "middle"))
        o.append(plabel(s, cx, y0 + 53, "bruise" if m > 1.04 else ("just holds" if m >= 1 else "fracture"), "label2",
                        I["secondary"], "middle"))
        pts.append([cx, P.Y(S / 1000), f"{name}: S = {S / 1000:.2f} kN, F = {fkn:.2f} kN, S/F = {m:.2f}"])
    o.append(H.line(s, x0, P.Y(fkn), x1, P.Y(fkn), O["load"], "load", H.DASH_REF))
    for k, txt in enumerate(flab):
        o.append(plabel(s, x1 + 8, P.Y(fkn) - 3 + 16 * k, txt, "label2", I["primary"], "start"))
    return "".join(o), pts


# ================================================================ svg #2  Fig. 1: where aging shows on the hip
def fig2():
    p, idx = "m14f2_", 2
    VB = (0, 0, 760, 396)
    s = H.Scale(VB[2], VB[3])
    A, B = Hip(20, 44, 3.05), Hip(400, 44, 3.05)
    o = [f"<defs>{H.markers(p, s)}</defs>", A.use(), B.use()]
    o.append(lab(s, 20, 24, "① osteoporosis: the femoral neck", "label", I["primary"]))
    o.append(lab(s, 400, 24, "② osteoarthritis: the hip cartilage", "label", I["primary"]))
    # ---- panel 1: the neck fracture site (a dashed line across the neck, perpendicular to the neck axis)
    a, b = A.f((28.5, 58.5)), A.f((50.0, 76.0))
    o.append(H.line(s, a[0], a[1], b[0], b[1], O["flag"], "geom", H.DASH_LOA))
    o.append(A.neck_ring(s, 30))
    c = A.f(NECK)
    o.append(H.line(s, c[0] + 21, c[1] + 21, 232, 252, I["secondary"], "leader"))
    o.append(lab(s, 236, 247, "neck fracture site", "label", I["primary"]))
    o.append(lab(s, 236, 266, "S ≈ 7 kN young,", "label2", I["secondary"]))
    o.append(lab(s, 236, 282, "S ≈ 2.5 kN at", "label2", I["secondary"]))
    o.append(lab(s, 236, 298, "40 % density loss", "label2", I["secondary"]))
    gt = A.f((16, 34))
    o.append(lab(s, gt[0] - 4, gt[1] - 8, "greater trochanter", "label2", I["secondary"]))
    # ---- panel 2: cartilage on the head, 2 mm at the rim and worn to 0.6 mm under the load (thickness not to bone scale)
    hx, hy, hr = HEAD
    Hc = B.f((hx, hy))
    rh = hr * B.K
    t_h, t_w = s(5.2), s(1.6)                               # healthy 2 mm and worn 0.6 mm (line 161): ratio 3.3

    def thick(deg):                                         # worn zone centred at -60 deg, smooth edges
        w = 0.5 - 0.5 * math.cos(math.pi * max(0.0, 1 - abs(deg + 60) / 45))
        return t_h + (t_w - t_h) * w

    degs = np.linspace(-100, 8, 90)
    xy = lambda r, d: (Hc[0] + r * math.cos(math.radians(d)), Hc[1] + r * math.sin(math.radians(d)))  # noqa: E731
    poly = [xy(rh, d) for d in degs] + [xy(rh - thick(d), d) for d in degs[::-1]]
    o.append(f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in poly)}" fill="{CART}" '
             f'stroke="{T["fluid"][1]}" stroke-width="{s(0.8):.2f}" stroke-linejoin="round"/>')
    o.append(circ(Hc[0], Hc[1], rh, "none", I["rule"], s(1.0), f'stroke-dasharray="{s(4):.1f} {s(3):.1f}"'))
    tip = xy(rh, -60)
    o.append(H.arrow(s, p, tip[0] - 14, tip[1] - 44, tip[0] - 1, tip[1] - 3, "load"))
    o.append(lab(s, tip[0] - 18, tip[1] - 38, "joint load", "label2", I["primary"], "end"))
    wz = xy(rh - 3, -60)
    o.append(H.line(s, wz[0] + 2, wz[1], 610, 66, I["secondary"], "leader"))
    o.append(lab(s, 614, 62, "worn: 0.6 mm,", "label2", I["primary"]))
    o.append(lab(s, 614, 78, "peak stress ≈ 7 MPa", "label2", I["primary"]))
    rim = xy(rh - 3, 3)
    o.append(H.line(s, rim[0] + 1, rim[1] + 2, 612, 150, I["secondary"], "leader"))
    o.append(lab(s, 616, 150, "rim: 2 mm,", "label2", I["primary"]))
    o.append(lab(s, 616, 166, "3 MPa", "label2", I["primary"]))
    lg, _ = legend(s, 20, 342, [(lambda x, y: rect(x, y - 10, 14, 10, CART, T["fluid"][1], 0.8), "articular cartilage"),
                                (sw_line(O["load"], 2.5), "joint load"),
                                (sw_line(O["flag"], 2.5, "6 3"), "fracture line")], gap=14)
    o.append(lg)
    o.append(lab(s, 400, 342, "a thinner layer carries less of the", "label2", I["secondary"]))
    o.append(lab(s, 400, 358, "load by fluid pressure (Module 4)", "label2", I["secondary"]))
    o.append(credit(s, VB, 135, "Hip region cropped and recoloured; the marks, the cartilage layer (thickness not to bone scale) "
                                "and the labels are drawn for this course."))
    aria = ("Two views of the same hip, the pelvis above and the upper femur below. Left: the narrow neck of the femur, "
            "between the ball-shaped head and the shaft, is ringed and crossed by a dashed fracture line, the site of "
            "osteoporotic fracture; the neck fails at about 7 kilonewtons in a young adult and about 2.5 kilonewtons "
            "after 40 percent density loss. Right: a blue cartilage layer covers the head, 2 millimetres thick at the "
            "rim and worn to 0.6 millimetres under the joint load, where the peak contact stress rises from 3 to about 7 megapascals.")
    return finish(VB, aria, s, o)


# ================================================================ svg #3  Fig. 2: six parameters drift together
PARAMS = ["muscle force", "bone density", "cartilage thickness", "reflex speed", "sensory acuity", "balance margin"]
R_DRIFT = 0.01                                    # line 426, 264: r = 0.01 per year, tau(a) = tau_p [1 - r (a - a0)]


def fig3():
    VB = (0, 0, 760, 388)
    s = H.Scale(VB[2], VB[3])
    o = []
    panels, hv = [], []
    t = np.arange(0, 40.01, 1.0)
    y = 100 * (1 - R_DRIFT * t)
    assert abs(y[-1] - 60.0) < 1e-9
    for i, name in enumerate(PARAMS):
        c, r = i % 3, i // 3
        x0, y1 = 72 + c * 235, 52 + r * 148
        P = Plot(s, (x0, y1, x0 + 165, y1 + 92), (0, 40), (50, 100))
        o.append(plabel(s, x0 + 82, y1 - 14, name, "label", I["primary"], "middle"))
        for g in (60, 80, 100):
            o.append(H.line(s, P.x0, P.Y(g), P.x1, P.Y(g), GRID, "leader"))
        o.append(H.line(s, P.x0, P.y0, P.x1, P.y0, I["axis"], "axis"))
        o.append(H.line(s, P.x0, P.y0, P.x0, P.y1, I["axis"], "axis"))
        for v in (60, 80, 100):
            o.append(H.line(s, P.x0 - 5, P.Y(v), P.x0, P.Y(v), I["axis"], "leader"))
            o.append(plabel(s, P.x0 - 8, P.Y(v) + 4.5, f"{v}", "tick", I["secondary"], "end"))
        for v in (0, 20, 40):
            o.append(H.line(s, P.X(v), P.y0, P.X(v), P.y0 + 5, I["axis"], "leader"))
            o.append(plabel(s, P.X(v), P.y0 + 19, f"{v}", "tick", I["secondary"], "middle"))
        o.append(P.curve(t, y, SER[0]))
        o.append(P.dot(40, 60, SER[0]))
        o.append(plabel(s, P.X(40) + 9, P.Y(60) + 4.5, "60 %", "label2", I["primary"]))
        panels.append((P.box, hov(P, t, [y], lambda k, n=name: f"{n}: {y[k]:.0f} % of midlife value, {t[k]:.0f} years past midlife")))
    for r in range(2):
        yc = 52 + r * 148 + 46
        o.append(plabel(s, 14, yc, "% of midlife value", "label", I["primary"], "middle", f'transform="rotate(-90 14 {yc})"'))
    o.append(plabel(s, 72 + 82, 52 + 148 + 92 + 40, "years past midlife", "label", I["primary"], "middle"))
    o.append(plabel(s, 72 + 235 + 82, 52 + 148 + 92 + 40, "years past midlife", "label", I["primary"], "middle"))
    o.append(plabel(s, 72 + 470 + 82, 52 + 148 + 92 + 40, "years past midlife", "label", I["primary"], "middle"))
    o.append(plabel(s, 380, 380, "each curve: 100 × (1 − 0.01 t), the linear drift of Proposition 2.1 (r = 0.01 per year)", "label2",
                    I["secondary"], "middle"))
    aria = ("Six small plots, one per mechanical parameter: muscle force, bone density, cartilage thickness, reflex speed, "
            "sensory acuity and balance margin. Each plots the percentage of its midlife value against years past midlife, "
            "from 0 to 40 years, and falls in a straight line at 1 percent of the midlife value per year, from 100 to 60 percent.")
    return finish(VB, aria, s, o, H.hover_attr(panels))


# ================================================================ svg #6  Fig. 5: the fall against the bone
def fig6():
    p, idx = "m14f6_", 6
    VB = (0, 0, 760, 392)
    s = H.Scale(VB[2], VB[3])
    A = Hip(176, 44, 2.25)
    o = [f"<defs>{H.markers(p, s)}</defs>", A.use(), A.neck_ring(s, 22)]
    tx, ty = A.f(TROCH)
    o.append(H.arrow(s, p, tx - 96, ty, tx - 1, ty, "load"))
    o.append(lab(s, tx - 106, ty - 22, "impact force", "label", I["primary"], "end"))
    o.append(lab(s, tx - 106, ty - 4, "F ≈ 4.4 kN", "label", I["primary"], "end"))
    o.append(lab(s, tx - 106, ty + 18, "on the greater", "label2", I["secondary"], "end"))
    o.append(lab(s, tx - 106, ty + 34, "trochanter", "label2", I["secondary"], "end"))
    c = A.f(NECK)
    o.append(H.line(s, c[0] + 16, c[1] + 16, 262, 214, I["secondary"], "leader"))
    o.append(lab(s, 266, 210, "femoral neck:", "label2", I["primary"]))
    o.append(lab(s, 266, 226, "the weak link", "label2", I["primary"]))
    P = Plot(s, (484, 44, 690, 262), (0, 3), (0, 8))
    body, pts = strength_bars(s, P, [("young", S0), ("ρ −20 %", 0.8 ** 2 * S0), ("ρ −40 %", 0.6 ** 2 * S0)],
                              F_PEAK / 1000, ["impact F", "≈ 4.4 kN"])
    o.append(body)
    o.append(plabel(s, 452, (P.y0 + P.y1) / 2, "neck strength S, force F (kN)", "label", I["primary"], "middle",
                    f'transform="rotate(-90 452 {(P.y0 + P.y1) / 2})"'))
    o.append(plabel(s, (P.x0 + P.x1) / 2, P.y0 + 74, "ρ −20 % = bone density 20 % below young", "label2", I["secondary"], "middle"))
    o.append(credit(s, VB, 135, "Hip region cropped and recoloured; the ring, arrow, bars and labels are drawn for this course."))
    aria = ("A hip, the pelvis above and the upper femur below, with a horizontal arrow pressing on the greater trochanter, "
            "the sideways-fall impact force of about 4.4 kilonewtons, and a ring on the femoral neck. At right, bars of "
            "neck strength S in kilonewtons against a dashed line at the fall force F: 7.0 for young bone, 4.5 after 20 percent "
            "density loss and 2.5 after 40 percent loss, giving strength-to-force margins of 1.60, 1.02 and 0.57; only the "
            "last is below one and fractures.")
    return finish(VB, aria, s, o, H.hover_attr(P.box, pts))


# ================================================================ svg #12  Fig. 10: the coupled network
def fig12():
    p, idx = "m14f12_", 12
    VB = (0, 0, 800, 428)
    s = H.Scale(VB[2], VB[3])
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    W, Hh = 176, 52
    cxs = {"muscle": 130, "bone": 390, "balance": 650}
    ya, yb, yc = 30, 160, 296

    def node(cx, y, text, key=None, sub=None):
        o.append(f'<rect x="{cx - W / 2:.1f}" y="{y}" width="{W}" height="{Hh}" rx="6" fill="{BOX}" '
                 f'stroke="{T[key][1] if key else O["dim"]}" stroke-width="{s(1.6):.2f}"/>')
        if key:
            o.append(rect(cx - W / 2 + 10, y + Hh / 2 - 8, 16, 16, T[key][0], T[key][1], 0.9, 3))
        o.append(lab(s, cx - W / 2 + 36 if key else cx, y + Hh / 2 + 5, text, "label", I["primary"], "start" if key else "middle"))

    node(cxs["muscle"], ya, "muscle", "muscle")
    node(cxs["bone"], ya, "bone", "bone")
    node(cxs["balance"], ya, "balance controller", "nerve")
    # the load bar
    bx0, bx1 = 40, 705
    o.append(f'<rect x="{bx0}" y="{yb}" width="{bx1 - bx0}" height="44" rx="6" fill="{BOX}" stroke="{O["load"]}" '
             f'stroke-width="{s(1.8):.2f}"/>')
    o.append(lab(s, (bx0 + bx1) / 2, yb + 27, "mechanical load: activity", "label", I["primary"], "middle"))
    # muscle -> bone: less pull
    o.append(H.arrow(s, p, cxs["muscle"] + W / 2 + 4, ya + 26, cxs["bone"] - W / 2 - 4, ya + 26, "force"))
    o.append(lab(s, (cxs["muscle"] + cxs["bone"]) / 2, ya + 19, "less pull", "label2", I["primary"], "middle"))
    o.append(lab(s, (cxs["muscle"] + cxs["bone"]) / 2, ya + 46, "on bone", "label2", I["primary"], "middle"))
    # load maintains each node
    for k, ax in (("muscle", cxs["muscle"]), ("bone", cxs["bone"]), ("balance", 585)):
        o.append(H.arrow(s, p, ax, yb - 2, ax, ya + Hh + 3, "load"))
    o.append(lab(s, cxs["muscle"] + 8, 128, "maintains", "label2", I["primary"]))
    o.append(lab(s, cxs["bone"] + 8, 128, "maintains", "label2", I["primary"]))
    o.append(lab(s, 577, 128, "maintains", "label2", I["primary"], "end"))
    # slow controller: moves less
    o.append(H.arrow(s, p, 690, ya + Hh + 3, 690, yb - 2, "dim"))
    o.append(lab(s, 698, 128, "moves", "label2", I["primary"]))
    o.append(lab(s, 698, 144, "less", "label2", I["primary"]))
    # the cascade: balance -> FALL -> fracture -> immobility -> load
    fx, bxm, ix = cxs["balance"], cxs["bone"], cxs["muscle"]
    node(fx, yc, "FALL")
    node(bxm, yc, "fracture")
    node(ix, yc, "immobility")
    gx = 776
    o.append(path(f"M{fx + W / 2 + 4:.1f},{ya + 26} L{gx},{ya + 26} L{gx},{yc + 26} L{fx + W / 2 + 4:.1f},{yc + 26}", O["dim"],
                  s(H.PX["ref"]) * 1.0, extra=f'marker-end="url(#{p}a_dim)" stroke-linejoin="round"'))
    o.append(lab(s, gx - 8, 262, "balance margin", "label2", I["primary"], "end"))
    o.append(lab(s, gx - 8, 278, "exceeded", "label2", I["primary"], "end"))
    o.append(H.arrow(s, p, fx - W / 2 - 4, yc + 26, bxm + W / 2 + 4, yc + 26, "dim"))
    o.append(lab(s, (fx + bxm) / 2, yc + 19, "bone margin", "label2", I["primary"], "middle"))
    o.append(lab(s, (fx + bxm) / 2, yc + 46, "exceeded", "label2", I["primary"], "middle"))
    o.append(H.arrow(s, p, bxm - W / 2 - 4, yc + 26, ix + W / 2 + 4, yc + 26, "dim"))
    o.append(lab(s, (bxm + ix) / 2, yc + 19, "forces", "label2", I["primary"], "middle"))
    o.append(H.arrow(s, p, ix, yc - 2, ix, yb + 44 + 3, "dim"))
    o.append(lab(s, ix + 8, 245, "load withdrawn:", "label2", I["primary"]))
    o.append(lab(s, ix + 8, 261, "deconditions", "label2", I["primary"]))
    o.append(lab(s, ix + 8, 277, "all three", "label2", I["primary"]))
    lg, _ = legend(s, 40, 400, [(sw_line(O["load"], 2.5), "load that maintains tissue"), (sw_line(O["force"], 2.5), "muscle pull on bone"),
                                (sw_line(O["dim"], 2.0), "causal link")], gap=18)
    o.append(lg)
    aria = ("A network of the frailty cascade. Top row: muscle, bone and the balance controller. A red arrow from muscle "
            "to bone: weak muscle pulls less on bone. A wide box below, mechanical load from activity, sends a brown "
            "arrow up into each of the three nodes: load maintains each tissue. A grey arrow from the balance controller "
            "down to the load box: a precarious controller moves less. Bottom row, right to left: balance margin exceeded "
            "gives a fall, the fall exceeds the bone margin and gives a fracture, the fracture forces immobility, and a "
            "grey arrow from immobility up to the load box closes the loop: load withdrawn deconditions muscle, bone "
            "and balance together.")
    return finish(VB, aria, s, o)


# ================================================================ svg #23  C3: the squared penalty
def fig23():
    p, idx = "m14f23_", 23
    VB = (0, 0, 400, 336)
    s = H.Scale(VB[2], VB[3], display_w=400)
    A = Hip(12, 60, 1.5)
    o = [f"<defs>{H.markers(p, s)}</defs>", A.use(), A.neck_ring(s, 13)]
    o.append(lab(s, 12, 214, "femoral neck:", "label2", I["primary"]))
    o.append(lab(s, 12, 230, "strength S ∝ ρ²", "label2", I["primary"]))
    P = Plot(s, (232, 40, 384, 232), (50, 100), (0, 100))
    rho = np.linspace(50, 100, 101)
    S = rho ** 2 / 100                                                      # line 135: S/S0 = (rho/rho0)^2, in per cent
    o.append(P.axes([(v, f"{v}") for v in (50, 75, 100)], [(0, "0"), (50, "50"), (100, "100")], "bone density ρ (% of young)",
                    "strength S (% of young)", grid=(50, 100), ytx=202))
    o.append(P.curve([50, 100], [50, 100], I["rule"], dash=H.DASH_REF))
    o.append(P.curve(rho, S, SER[0]))
    o.append(P.dot(80, 64, SER[0]))
    o.append(H.line(s, P.X(80), P.Y(64) + 6, P.X(80), P.Y(18) - 16, I["secondary"], "leader"))
    o.append(plabel(s, P.X(100), P.Y(18), "ρ −20 % gives S −36 %", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(97), P.Y(52), "S ∝ ρ²", "label", I["primary"], "end"))
    o.append(plabel(s, P.X(61), P.Y(61) - 14, "S ∝ ρ", "label2", I["muted"], "middle"))
    o.append(credit(s, VB, 62, "Hip region cropped and recoloured; ring and plot drawn for this course."))
    aria = ("Problem C3 plot. At left, a hip with a ring on the femoral neck. At right, bone strength as a percentage of "
            "young strength against bone density as a percentage of young density, from 50 to 100 percent: the curve S "
            "proportional to density squared, falling below the dashed straight line of strength proportional to density. At "
            "80 percent density the strength is 64 percent, a 36 percent loss for a 20 percent density loss.")
    hv = hov(P, rho, [S], lambda i: f"ρ = {rho[i]:.0f} %: S = {S[i]:.0f} % of young")
    return finish(VB, aria, s, o, H.hover_attr(P.box, hv))


# ================================================================ svg #24  C4: the fall that breaks
def fig24():
    p, idx = "m14f24_", 24
    VB = (0, 0, 400, 508)
    s = H.Scale(VB[2], VB[3], display_w=400)
    A = Hip(110, 14, 1.9)
    o = [f"<defs>{H.markers(p, s)}</defs>", A.use(), A.neck_ring(s, 20)]
    tx, ty = A.f(TROCH)
    o.append(H.arrow(s, p, tx - 66, ty, tx - 1, ty, "load"))
    o.append(lab(s, 8, ty - 22, "impact", "label2", I["primary"]))
    o.append(lab(s, 8, ty - 6, "F ≈ 4.4 kN", "label2", I["primary"]))
    c = A.f(NECK)
    o.append(lab(s, 8, 214, "same impact, two femoral necks", "label2", I["secondary"]))
    P = Plot(s, (96, 232, 318, 380), (0, 3), (0, 8))
    body, pts = strength_bars(s, P, [("young", S0), ("osteoporotic", 0.6 ** 2 * S0)], F_PEAK / 1000, ["F ≈", "4.4 kN"])
    o.append(body)
    o.append(plabel(s, 54, (P.y0 + P.y1) / 2, "S and F (kN)", "label", I["primary"], "middle",
                    f'transform="rotate(-90 54 {(P.y0 + P.y1) / 2})"'))
    o.append(credit(s, VB, 66, "Hip region cropped and recoloured; ring, arrow, bars and labels drawn for this course."))
    aria = ("Problem C4 setup. A hip at left with an arrow pressing on the greater trochanter, the sideways-fall impact "
            "force of 4.4 kilonewtons, and a ring on the femoral neck. At right, two bars of neck strength against a dashed "
            "line at that force: young bone at 7.0 kilonewtons, above the line, margin 1.60, a bruise; osteoporotic bone at "
            "2.5 kilonewtons, below the line, margin 0.57, a fracture. The impact is the same; the capacity differs.")
    return finish(VB, aria, s, o, H.hover_attr(P.box, pts))


# ================================================================ svg #33  D3: the impact force
def fig33():
    p, idx = "m14f33_", 33
    VB = (0, 0, 400, 450)
    s = H.Scale(VB[2], VB[3], display_w=400)
    PXM = 214.0                                   # px per metre of the mass's travel
    R, fl, sp = 22.0, 330.0, 92.0                 # mass radius, floor y, free spring length
    top = fl - sp                                 # spring top at rest = mass bottom at impact
    cl, cr = 100.0, 285.0
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    yi = top - R                                  # mass centre at impact
    yg = yi - HF * PXM                            # mass centre at release
    xm = X_MAX * PXM

    def spring(cx, y_top, y_bot, n=7, amp=11.0):
        pts = [(cx, y_top)]
        seg = (y_bot - y_top - 16) / n
        for i in range(n):
            pts.append((cx + (amp if i % 2 else -amp), y_top + 8 + (i + 0.5) * seg))
        pts.append((cx, y_bot))
        return (f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{I["secondary"]}" '
                f'stroke-width="{s(2.0):.2f}" stroke-linejoin="round"/>')

    def mass(cx, cy, ghost=False):
        if ghost:
            return circ(cx, cy, R, "none", I["rule"], s(1.2), f'stroke-dasharray="{s(4):.1f} {s(3):.1f}"')
        return circ(cx, cy, R, T["skin"][0], T["skin"][1], s(1.6)) + lab(s, cx, cy + 4.5, "35 kg", "label2", I["primary"], "middle")

    for cx in (cl, cr):                           # floor
        o.append(H.line(s, cx - 60, fl, cx + 60, fl, I["axis"], "axis"))
        for k in range(-60, 60, 10):
            o.append(H.line(s, cx + k, fl, cx + k - 7, fl + 8, I["rule"], "leader"))
    o.append(lab(s, cl, 20, "① at impact", "label", I["primary"], "middle"))
    o.append(lab(s, cr, 20, "② at maximum compression", "label", I["primary"], "middle"))
    # ① release, drop, impact
    o.append(mass(cl, yg, True))
    o.append(lab(s, cl + 30, yg + 5, "released at rest", "label2", I["secondary"]))
    o.append(H.arrow(s, p, 40, yg, 40, yi, "geometry", both=True))
    o.append(lab(s, 48, (yg + yi) / 2 + 5, f"h{H.sub('f', s, 'label2')} = 0.70 m", "label2", I["primary"]))
    o.append(spring(cl, top, fl))
    o.append(mass(cl, yi))
    o.append(H.arrow(s, p, cl, yi - R - 38, cl, yi - R - 2, "dim"))
    o.append(lab(s, cl + 10, yi - R - 18, f"v = √(2g h{H.sub('f', s, 'label2')})", "label2", I["primary"]))
    o.append(lab(s, cl + 10, yi - R - 2, "= 3.7 m/s", "label2", I["primary"]))
    # ② compressed
    o.append(mass(cr, yi, True))
    o.append(spring(cr, top + xm, fl, n=7))
    o.append(mass(cr, yi + xm))
    o.append(H.arrow(s, p, cr + 38, top, cr + 38, top + xm, "geometry", both=True))
    o.append(lab(s, cr + 46, top + xm / 2 - 4, f"x{H.sub('max', s, 'label2')}", "label2", I["primary"]))
    o.append(lab(s, cr + 46, top + xm / 2 + 12, "= 11.0 cm", "label2", I["primary"]))
    o.append(H.arrow(s, p, cr - 40, top + xm + 2, cr - 40, top + xm - 62, "load"))
    o.append(lab(s, cr - 46, top + xm - 36, f"F = k x{H.sub('max', s, 'label2')}", "label2", I["primary"], "end"))
    o.append(lab(s, cr - 46, top + xm - 16, "≈ 4.4 kN", "label2", I["primary"], "end"))
    o.append(lab(s, cl, fl + 30, f"½ m v² = {E_KIN:.0f} J", "label2", I["primary"], "middle"))
    o.append(lab(s, cr, fl + 30, f"½ k x{H.sub('max', s, 'label2')}² = {0.5 * K_SPR * X_MAX ** 2:.0f} J", "label2", I["primary"], "middle"))
    o.append(lab(s, 200, fl + 56, f"F{H.sub('peak', s)} = k x{H.sub('max', s)} = v √(m{H.sub('eff', s)} k) ≈ 4.4 kN", "label",
                 I["primary"], "middle"))
    o.append(lab(s, 200, fl + 78, f"m{H.sub('eff', s, 'label2')} = 35 kg (circle), k = 40 kN/m (spring)", "label2", I["secondary"], "middle"))
    o.append(lab(s, 200, fl + 96, "gravity work during the stroke is dropped in this form:", "label2", I["muted"], "middle"))
    o.append(lab(s, 200, fl + 112, "the exact balance gives F = 4742 N, 8 % higher", "label2", I["muted"], "middle"))
    aria = ("Problem D3 setup, two panels of a mass falling onto a spring, drawn to one length scale. Left: a 35 kilogram "
            "mass released from rest 0.70 metres above the landing falls at 3.7 metres per second as it reaches the "
            "spring, which stands for the soft tissue and floor with stiffness 40 kilonewtons per metre; its kinetic "
            "energy is half m v squared, 240 joules. Right: at maximum compression, 11.0 centimetres, all of that energy is "
            "in the spring, half k x squared, and the spring pushes back with the peak force k x, about 4.4 kilonewtons.")
    return finish(VB, aria, s, o)


# ================================================================ svg #38  D8: the critical density
def fig38():
    p, idx = "m14f38_", 38
    VB = (0, 0, 400, 336)
    s = H.Scale(VB[2], VB[3], display_w=400)
    A = Hip(12, 60, 1.5)
    o = [f"<defs>{H.markers(p, s)}</defs>", A.use(), A.neck_ring(s, 13)]
    o.append(lab(s, 12, 214, "femoral neck:", "label2", I["primary"]))
    o.append(lab(s, 12, 230, "S = 7 kN (ρ/ρ₀)²", "label2", I["primary"]))
    P = Plot(s, (232, 40, 384, 232), (50, 100), (0, 2.5))
    rho = np.linspace(50, 100, 101)
    F2 = F_PEAK / math.sqrt(2)                                              # line 454: halving k cuts F by sqrt 2
    m1 = S0 * (rho / 100) ** 2 / F_PEAK                                     # line 454: margin S/F
    m2 = S0 * (rho / 100) ** 2 / F2
    c1, c2 = 100 * math.sqrt(F_PEAK / S0), 100 * math.sqrt(F2 / S0)
    o.append(P.axes([(v, f"{v}") for v in (50, 75, 100)], [(0, "0"), (1, "1"), (2, "2")], "bone density ρ (% of young)",
                    "margin S/F", grid=(), ytx=206))
    o.append(H.line(s, P.x0, P.Y(1), P.x1, P.Y(1), I["rule"], "ref", H.DASH_REF))
    o.append(P.curve(rho, m1, SER[0]))
    o.append(P.curve(rho, m2, SER[1]))
    o.append(P.dot(c1, 1, SER[0]))
    o.append(P.dot(c2, 1, SER[1]))
    o.append(plabel(s, P.X(c1) + 4, P.Y(1) + 22, f"{c1:.0f} %", "label2", I["primary"], "start"))
    o.append(plabel(s, P.X(c2) - 4, P.Y(1) - 10, f"{c2:.0f} %", "label2", I["primary"], "end"))
    o.append(plegend(s, P.x0 + 8, P.y1 + 16, [(SER[0], "k = 40 kN/m", None)]))
    o.append(plegend(s, P.x0 + 8, P.y1 + 34, [(SER[1], "k halved (F ÷ √2)", None)]))
    o.append(plegend(s, P.x0 + 8, P.y1 + 52, [(I["rule"], "S/F = 1", H.DASH_REF)]))
    o.append(credit(s, VB, 62, "Hip region cropped and recoloured; ring and plot drawn for this course."))
    aria = ("Problem D8 plot. At left, a hip with a ring on the femoral neck. At right, the margin S over F of the neck "
            "against bone density as a percentage of young density, from 50 to 100 percent, for two landing stiffnesses: the "
            "fall at 40 kilonewtons per metre crosses the fracture line S over F equal to 1 at 79 percent density; with the "
            "stiffness halved, which cuts the impact force by the square root of two, the crossing moves down to 67 percent.")
    hv = hov(P, rho, [m1, m2], lambda i: f"ρ = {rho[i]:.0f} %: S/F = {m1[i]:.2f} (k = 40 kN/m), {m2[i]:.2f} (k halved)")
    return finish(VB, aria, s, o, H.hover_attr(P.box, hv))


FIGS = {
    2: ("Left: femoral neck fracture site on lateral femur. Right: osteoarthritic joint with thinned cartilage.", fig2),
    3: ("Six mechanical parameters of the body - muscle force, bone density, cartilage thickness, reflex speed, sensory acuity, balance margin - each drifting down with age.", fig3),
    6: ("A femur struck in a sideways fall, with the impact force and the femoral strength for young and osteoporotic bone shown as bars.", fig6),
    12: ("A network linking muscle, bone, and the balance controller through load, with the fall-fracture-immobility cascade.", fig12),
    23: ("C3: the squared penalty. Why does a $20\\%$ loss of bone density cost far more than $20\\%$ of bone strength?", fig23),
    24: ("C4: the fall that breaks. Why does a sideways fall fracture an old hip but only bruise a young one, when the impact is the same?", fig24),
    33: ("D3: the impact force. Derive the peak force of a mass striking a spring-like landing at speed $v$.", fig33),
    38: ("D8: critical density. Derive the bone density below which a given fall fractures the hip.", fig38),
}
FIGS = {k: (v[0][:60], v[1]) for k, v in FIGS.items()}
