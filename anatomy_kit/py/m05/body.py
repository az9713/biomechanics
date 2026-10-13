"""Module 5 body figures: svg #1 (Fig. 21 calf), #3 (Fig. 22 arm + bag), #34 (Fig. 28 elbow at 90 deg),
and the problem figures #53 (D2), #59 (D8), #72 (K6).

Art comes only from anatomy_kit/svg_paths/ (see ATTRIBUTIONS.md):
  Lower_leg_muscles.svg (InjuryMap, CC BY-SA 4.0), nih_arm_bones.svg (NIH BioArt 208, PD),
  202107_Sagittal_section_through_the_elbow_joint.svg (DBCLS, CC BY 4.0).
Landmark constants were measured once in Chrome (getPointAtLength on the source paths, or a
coordinate grid over the rendered art). Each constant names its source.
"""
import base64
from urllib.parse import quote
import html
import math
import re
from pathlib import Path

import house as H
from crop_art import absolute

KIT = Path(__file__).resolve().parents[2] / "svg_paths"
T, O, I = H.TISSUE, H.OVERLAY, H.INK
H_REF_M = 1.75            # reference stature used by the course
SHANK_FRAC = 0.246        # Winter: knee to ankle
FOREARM_FRAC = 0.146      # Winter: elbow to wrist


# ---------------------------------------------------------------- local helpers (not in house.py)
def _read(name):
    return (KIT / name).read_text(encoding="utf-8")


def inner_svg(s):
    a = re.search(r'<svg\b[^>]*>', s)
    return s[a.end():s.rfind("</svg>")]


def prefix_svg(s, p):
    """Prefix every id, url(#id), href="#id" and class name so inline SVGs cannot collide."""
    s = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{p}{m.group(1)}"', s)
    s = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{p}{m.group(1)})', s)
    s = re.sub(r'((?:xlink:)?href)="#([^"]+)"', lambda m: f'{m.group(1)}="#{p}{m.group(2)}"', s)
    s = re.sub(r'class="([^"]+)"', lambda m: 'class="' + " ".join(p + c for c in m.group(1).split()) + '"', s)
    s = re.sub(r'\.(cls-\d+)', lambda m: f'.{p}{m.group(1)}', s)
    return s


def fit_circle(pts):
    """Least-squares (Kasa) circle fit. Returns (cx, cy, r)."""
    S = [[0.0] * 4 for _ in range(3)]
    for x, y in pts:
        row, rhs = (x, y, 1.0), -(x * x + y * y)
        for i in range(3):
            for j in range(3):
                S[i][j] += row[i] * row[j]
            S[i][3] += row[i] * rhs
    for i in range(3):
        piv = S[i][i]
        S[i] = [v / piv for v in S[i]]
        for k in range(3):
            if k != i:
                f = S[k][i]
                S[k] = [a - f * b for a, b in zip(S[k], S[i])]
    D, E, F = S[0][3], S[1][3], S[2][3]
    cx, cy = -D / 2, -E / 2
    return cx, cy, math.sqrt(cx * cx + cy * cy - F)


def foot_of_perp(p, a, b):
    """Foot of the perpendicular from p to line a-b, and the distance."""
    (ax, ay), (bx, by), (px, py) = a, b, p
    dx, dy = bx - ax, by - ay
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    fx, fy = ax + t * dx, ay + t * dy
    return (fx, fy), math.hypot(px - fx, py - fy)


def wrap(text, n):
    out, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return out + [cur]


def it(v):
    return f'<tspan font-style="italic">{v}</tspan>'


def poly(pts, col, w, extra=""):
    return (f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="none" stroke="{col}" '
            f'stroke-width="{w:.2f}" stroke-linejoin="round" {extra}/>')


def art_image(doc, box, extra=""):
    """Embed a cropped art document as <image> (vector, ids isolated). Its bounding box is the crop box,
    so check_frame sees the crop and not the whole source sheet."""
    x, y, w, h = box
    a = re.search(r'<svg\b[^>]*>', doc)
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
           f'viewBox="{x} {y} {w} {h}" width="{w}" height="{h}">' + doc[a.end():])
    doc = re.sub(r'="([^"\']*)"', r"='\1'", doc)          # single quotes need no escape in the URI
    b64 = "data:image/svg+xml;base64," + base64.b64encode(doc.encode("utf-8")).decode("ascii")
    pct = "data:image/svg+xml," + quote(doc, safe=" !$'()*+,-./:;=?@_~[]{}|")
    return (f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none" '
            f'href="{min(b64, pct, key=len)}" {extra}/>')


def finish(vb, aria, s, body, extra=""):
    body = re.sub(r'<marker id="([^"]+)".*?</marker>',                  # drop arrowheads the figure never uses
                  lambda m: m.group(0) if f"url(#{m.group(1)})" in "".join(body) else "", "".join(body))
    body = [body.replace("<defs></defs>", "")]
    return H.svg_open(vb, html.escape(aria), s, extra) + "".join(body) + "</svg>"


# ================================================================ svg #1  Fig. 21 calf (approved sample, ported)
# Source user space of Lower_leg_muscles.svg (no root transform).
F21 = dict(
    # path 40 (talus) upper outline, getPointAtLength samples 29..43 of 60: the trochlear dome
    dome=[(324.0, 988.0), (326.0, 984.3), (329.8, 982.2), (334.1, 981.2), (338.4, 980.5), (342.7, 980.0),
          (347.0, 979.6), (351.4, 979.5), (355.7, 979.9), (360.0, 980.7), (364.1, 982.2), (367.9, 984.3),
          (371.3, 987.0), (374.2, 990.2), (377.1, 993.5)],
    femur_low=415.2,              # path 80 (femoral articular cartilage), lowest point
    plateau=431.6,                # path 82 (meniscus) lower edge under the same x = tibial plateau
    tendon_c=(414.65, 960.0),     # path 197 (Achilles) centreline at y 960: edges x 409.9 / 419.4
    insertion=(425.05, 1057.65),  # path 204 (calcaneal insertion) bbox centre
)


def fig1():
    idx, p = 1, "m5f1_"
    VB = (20, 290, 740, 935)
    s = H.Scale(VB[2], VB[3])
    # crop_art.py ../svg_paths/Lower_leg_muscles.svg fig21 20 290 760 1195 --drop "#Names, text" --png 0.4
    art = inner_svg(_read("Lower_leg_muscles_crop_fig21.svg"))
    assert 'id="Names"' not in art and "<text" not in art
    art = art_image("<svg>" + H.recolour(art, "injurymap") + "</svg>", (20, 290, 740, 905))

    d = F21
    ax, ay, ar = fit_circle(d["dome"])
    knee_y = (d["femur_low"] + d["plateau"]) / 2
    shank = ay - knee_y
    Tc, In = d["tendon_c"], d["insertion"]
    P, dist = foot_of_perp((ax, ay), Tc, In)
    ucm = shank / (SHANK_FRAC * H_REF_M * 100)          # units per cm, shank = 43 cm
    d_cm = dist / ucm
    red, blu = O["force"], O["geometry"]
    lx = 488                                            # label column
    o = [f'<defs>{H.markers(p, s)}</defs>', art]
    # knee joint line and shank dimension
    o.append(H.line(s, 190, knee_y, 385, knee_y, O["dim"], "ref", H.DASH_REF))
    o.append(H.label(s, 222, knee_y - 12, "knee joint line", "label", I["secondary"], "end"))
    o.append(H.line(s, 190, ay, ax - 8, ay, O["dim"], "leader", H.DASH_REF))
    o.append(H.line(s, 190, knee_y, 190, ay, O["dim"], "ref",
                    extra=f'marker-start="url(#{p}a_dim)" marker-end="url(#{p}a_dim)"'))
    my = (knee_y + ay) / 2
    o.append(H.label(s, 174, my, "shank ≈ 43 cm (0.246 H)", "label", I["secondary"], "middle",
                     f'transform="rotate(-90 174 {my:.1f})"'))
    # Achilles line of action: from the insertion up along the distal tendon (pull on the calcaneus)
    ux, uy = Tc[0] - In[0], Tc[1] - In[1]
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    top = (In[0] + ux * 175, In[1] + uy * 175)
    o.append(H.arrow(s, p, In[0], In[1], top[0], top[1], "force"))
    o.append(f'<circle cx="{In[0]:.1f}" cy="{In[1]:.1f}" r="{s(4):.1f}" fill="{red}" stroke="#fff" stroke-width="{s(1.2):.1f}"/>')
    o.append(H.line(s, top[0] + 5, top[1] + 30, lx - 4, top[1] + 2, red))
    o.append(H.label(s, lx, top[1] + 8, "Achilles line of action", fill=red))
    # moment arm: perpendicular from the ankle centre to the line of action
    o.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{P[0]:.1f}" y2="{P[1]:.1f}" stroke="#fff" stroke-width="{s(4.5):.1f}"/>')
    o.append(H.arrow(s, p, ax, ay, P[0], P[1], "geometry", both=True))
    o.append(H.label(s, (ax + P[0]) / 2, ay - 10, f'{it("d")}{H.sub("m", s)}', fill=blu, anchor="middle"))
    o.append(H.line(s, P[0] + 5, P[1] - 3, lx - 4, 984, blu))
    o.append(H.label(s, lx, 990, f'moment arm {it("d")}{H.sub("m", s)} ≈ {d_cm:.0f} cm', fill=blu))
    o.append(H.joint_centre(s, ax, ay))
    o.append(f'<path d="M{ax+6:.1f},{ay+6:.1f} L470,1118 L{lx-4},1118" fill="none" stroke="{I["primary"]}" stroke-width="{s(1):.2f}"/>')
    o.append(H.label(s, lx, 1124, "ankle joint centre"))
    o.append(H.label(s, lx, 1124 + s(17), "(centre of the talar dome)", "label2", I["secondary"]))
    o.append(H.line(s, In[0] + 6, In[1], lx - 4, In[1], O["load"]))
    o.append(H.label(s, lx, In[1] + 7, "Achilles to calcaneus", fill=O["load"]))
    o.append(H.line(s, 452, 600, lx - 4, 600, T["muscle"][1]))
    o.append(f'<circle cx="450" cy="600" r="{s(2.5):.1f}" fill="{T["muscle"][1]}"/>')
    o.append(H.label(s, lx, 607, "triceps surae", fill=T["muscle"][1]))
    cr = H.ATTRIBUTION["by-sa"].format(author="InjuryMap", title="Lower leg muscles.svg",
                                       changes="Lateral leg only; labels removed, cropped, overlays added.")
    o.append(H.credit(s, 30, 1166, wrap(cr, 92)))
    aria = ("Lateral view of the right lower leg (InjuryMap art): tibia, fibula, ankle and foot bones, gastrocnemius "
            "and soleus (triceps surae) narrowing into the Achilles tendon, which inserts on the calcaneus behind the "
            "ankle. Marked: the knee joint line, the shank length of about 43 cm, the ankle joint centre at the centre "
            f"of the talar dome, the Achilles line of action, and the perpendicular moment arm of about {d_cm:.0f} cm "
            "from the ankle centre to that line.")
    return finish(VB, aria, s, o)


# ================================================================ the arm (NIH BioArt 208, anterior view, reposed)
# nih_arm_bones.svg path order: 1 = dark under-shape of the left arm (dropped), 4 = left humerus fill,
# 5-6 = left radius / ulna fills, 7-15 = left hand fills, 2-3 + 16-24 = right arm (dropped).
ARM = dict(
    E=(49.5, 156.0),        # ESTIMATE: elbow flexion centre, ~1 cm above the distal humeral joint outline (y 160-163)
    hum_top=(76.8, 2.2),    # centre of the cut top of the humerus fill (path 4 points x 69.9..83.7 at y 2)
    wrist=(19.5, 291.5),    # between the distal ends of paths 5 and 6
    origin=(0.6, -34.5),    # cm, humerus frame (x anterior, y down): supraglenoid tubercle (long head)
    belly=((1.9, -25.0), (3.9, -16.0), (2.8, -7.5)),   # cm: biceps belly top, bezier control, belly bottom
    half_w=2.2,             # cm, biceps max half-thickness
    tri=((-3.0, -24.0), (-4.6, -15.0), (-2.9, -5.5)),  # cm: triceps belly (posterior), same construction
    tri_half_w=2.0,
    # cm: olecranon tip at 90 deg flexion, posterior and slightly distal to the axis. The anterior-view NIH ulna
    # ends 0.74 cm DISTAL to the axis (path 5 outline), so this art has no olecranon here; the #34 inset shows it.
    tri_ins=(-1.6, 0.9),
)


class Arm:
    """The reposed NIH arm at 90 deg flexion. Canvas = Ec + cm * K."""

    def __init__(self, p, s, Ec, K, r_ins=3.0):
        self.p, self.s, self.Ec, self.K = p, s, Ec, K
        src = H.recolour(_read("nih_arm_bones.svg"), "nih")
        self.paths = re.findall(r'<path\b[^>]*?\bd="([^"]+)"[^>]*/>', src)
        assert len(self.paths) == 24, len(self.paths)
        d = ARM
        E, Tp, W = d["E"], d["hum_top"], d["wrist"]
        self.a_h = math.degrees(math.atan2(E[0] - Tp[0], E[1] - Tp[1]))
        self.a_f = math.degrees(math.atan2(W[0] - E[0], W[1] - E[1]))
        self.k_art = math.hypot(W[0] - E[0], W[1] - E[1]) / (FOREARM_FRAC * H_REF_M * 100)   # art units / cm
        self.hum_cm = math.hypot(E[0] - Tp[0], E[1] - Tp[1]) / self.k_art
        # insertion at 90 deg: r_ins along the forearm, 0.4 cm off the axis onto the ulnar-facing edge of the radius
        # (art: radius = path 6, x 36.6-43.8 at y 172; ulna = path 5, x 45.4-57.5; the axis point x 46.0 is on the ulna)
        self.I = self.C((r_ins, 0.4))
        self.B = self.C(d["belly"][2])
        self.P, dist = foot_of_perp(Ec, self.B, self.I)
        self.d_cm = dist / K

    def C(self, v):
        return (self.Ec[0] + v[0] * self.K, self.Ec[1] + v[1] * self.K)

    def bones(self, hand=True):
        s, E, sc = self.s, ARM["E"], self.K / self.k_art
        st = (f'fill="{T["bone"][0]}" stroke="{T["bone"][1]}" stroke-width="{s(H.PX["art_line"]) / sc:.3f}" '
              f'stroke-linejoin="round"')
        hum = f'<path d="{absolute(self.paths[3])}" {st}/>'           # path points rounded to 0.1 art unit
        fore = "".join(f'<path d="{absolute(self.paths[i - 1])}" {st}/>' for i in [6, 5] + list(range(7, 16) if hand else []))
        g = lambda ang, body: (f'<g transform="translate({self.Ec[0]:.2f} {self.Ec[1]:.2f}) scale({sc:.4f}) '   # noqa: E731
                               f'rotate({ang:.3f}) translate({-E[0]} {-E[1]})">{body}</g>')
        return g(self.a_f - 90.0, fore) + g(self.a_h, hum)

    def belly(self, ctrl, half_w, fibre_col):
        P1, PC, B = (self.C(v) for v in ctrl)
        hw = half_w * self.K

        def bez(t):
            x = (1 - t) ** 2 * P1[0] + 2 * (1 - t) * t * PC[0] + t * t * B[0]
            y = (1 - t) ** 2 * P1[1] + 2 * (1 - t) * t * PC[1] + t * t * B[1]
            dx = 2 * (1 - t) * (PC[0] - P1[0]) + 2 * t * (B[0] - PC[0])
            dy = 2 * (1 - t) * (PC[1] - P1[1]) + 2 * t * (B[1] - PC[1])
            L = math.hypot(dx, dy)
            return x, y, -dy / L, dx / L

        def width(t):
            return hw * math.sin(math.pi * t) ** 0.85

        N = 36
        left, right = [], []
        for i in range(N + 1):
            x, y, nx, ny = bez(i / N)
            w = width(i / N)
            left.append((x + nx * w, y + ny * w))
            right.append((x - nx * w, y - ny * w))
        out = [f'<path d="{absolute("M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in left + right[::-1]) + " Z")}" '
               f'fill="{T["muscle"][0]}" stroke="{T["muscle"][1]}" stroke-width="{self.s(1):.2f}"/>']
        for f in [-0.75, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75]:    # fibre lines as <path> (not <polyline>)
            pts = []
            for i in range(2, N - 1, 3):
                x, y, nx, ny = bez(i / N)
                w = width(i / N) * f
                pts.append(f"{x + nx * w:.2f},{y + ny * w:.2f}")
            out.append(f'<path d="{absolute("M" + " L".join(pts))}" fill="none" stroke="{fibre_col}" stroke-width="{self.s(0.6):.2f}" opacity="0.5"/>')
        return "".join(out), bez, width

    def tendon(self, a, b, w):
        s = self.s
        return (f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{T["tendon"][1]}" '
                f'stroke-width="{s(w + 1.4):.2f}" stroke-linecap="round"/>'
                f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{T["tendon"][0]}" '
                f'stroke-width="{s(w):.2f}" stroke-linecap="round"/>')

    def biceps(self):
        """Tendons + belly + insertion dot. Returns (svg, bez, width)."""
        d = ARM
        belly, bez, width = self.belly(d["belly"], d["half_w"], T["muscle_dk"][1])
        O_ = self.C(d["origin"])
        P1 = self.C(d["belly"][0])
        return (self.tendon(O_, P1, 2.4) + self.tendon(self.B, self.I, 3.0) + belly +
                f'<circle cx="{self.I[0]:.1f}" cy="{self.I[1]:.1f}" r="{self.s(2.8):.2f}" fill="{O["force"]}" '
                f'stroke="#fff" stroke-width="{self.s(1):.2f}"/>'), bez, width

    def loa(self, ext=4.0):
        """Biceps line of action: through the belly bottom B and the insertion I, extended past I by ext cm."""
        ux, uy = self.I[0] - self.B[0], self.I[1] - self.B[1]
        L = math.hypot(ux, uy)
        ux, uy = ux / L, uy / L
        X = (self.I[0] + ux * ext * self.K, self.I[1] + uy * ext * self.K)
        return H.line(self.s, self.B[0], self.B[1], X[0], X[1], O["force"], "leader", H.DASH_LOA), (ux, uy)


# ================================================================ DBCLS sagittal elbow (inset)
# Source user space of 202107_Sagittal_section_through_the_elbow_joint.svg (viewBox 0 0 400 400).
# Anterior is LEFT in the source; the inset mirrors it so anterior is RIGHT, as in the arm drawing.
DB = dict(
    # path 0 (humerus cortex) lower outline, getPointAtLength samples with y > 205: the trochlea
    trochlea=[(169.2, 210.8), (168.3, 217.9), (168.8, 225.1), (170.9, 231.9), (174.4, 238.2), (179.4, 243.4), (185.5, 247.2),
              (192.3, 249.3), (199.5, 249.6), (206.5, 248.1), (213.0, 245.1), (218.8, 240.8), (223.4, 235.3),
              (226.5, 228.9), (228.2, 221.9), (229.1, 214.8), (228.9, 207.6)],
    # humerus shaft centre: path 0 edges at y 40 (137.7 / 201.7) and y 140 (161.2 / 217.9)
    hum_axis=((169.7, 40.0), (189.55, 140.0)),
    # radius shaft centre: path 4 edges at y 290 (155.9 / 193.3) and y 370 (127.9 / 161.6)
    rad_axis=((174.6, 290.0), (144.75, 370.0)),
    # anterior muscle (path 8): terminal tendon centreline, midpoints of its two edges near the tip;
    # the tip lands on the proximal radius (path 4 top, y 259-278), so it is the biceps tendon
    tendon=((159.85, 262.45), (174.85, 274.0)),
    # posterior muscle (path 2) = triceps: tip on the olecranon (path 2 lowest points ~(277.9, 216.4..218.8))
    # and its centreline at y 170 (edges 237.6 / 269.0)
    triceps=((277.8, 218.8), (253.3, 170.0)),
    troch_r_cm=1.0,          # literature: sagittal radius of the trochlea, about 1.0 cm (scale basis 1)
    shaft_ap_cm=2.0,         # literature: humeral shaft AP depth ~6 cm above the joint, about 2.0 cm (basis 2)
)


def dbcls_art(p):
    """The cropped DBCLS section, recoloured. It is embedded through art_image (its own document), so the
    st* classes and ids cannot collide with the page and need no prefix (p is kept for the call sites)."""
    # python -I crop_art.py ../svg_paths/202107_Sagittal_section_through_the_elbow_joint.svg fig22
    #   52.1 105.3 330.8 337.1 --drop "foreignObject, aipgf" --rot 11.23 198.41 218.64
    # (box = the union of the #3 and #34 inset windows, in the source frame turned by Inset.rot about the trochlea)
    src = _read("202107_Sagittal_section_through_the_elbow_joint_crop_fig22.svg")
    style = re.search(r'<style>.*?</style>', src, re.S).group(0)
    body = src[src.index('<g i:extraneous="self">'):src.index('</switch>')]
    body = re.sub(r'\si:[\w-]+="[^"]*"', '', body)
    assert "<text" not in body
    return H.recolour(style + body, "dbcls")


class Inset:
    """DBCLS elbow mirrored (anterior right) and rotated so the humerus shaft is vertical."""

    def __init__(self, p, s, centre, sc):
        d = DB
        self.p, self.s, self.sc, self.centre = p, s, sc, centre
        self.tc = fit_circle(d["trochlea"])
        (hx0, hy0), (hx1, hy1) = d["hum_axis"]
        (rx0, ry0), (rx1, ry1) = d["rad_axis"]
        self.rot = math.degrees(math.atan2(hx1 - hx0, hy1 - hy0))   # rotate(+rot) makes the shaft vertical
        rad_dev = math.degrees(math.atan2(rx0 - rx1, ry1 - ry0))
        self.flex = self.rot + rad_dev                                 # inset flexion from full extension
        self.u_cm = (self.tc[2] / d["troch_r_cm"], (201.7 - 137.7) / d["shaft_ap_cm"])
        self.k = sum(self.u_cm) / 2                                    # art units per cm (mean of the two bases)
        a, b = d["tendon"]
        self.tip = b
        self.foot, dist = foot_of_perp(self.tc[:2], a, b)
        self.d_cm = dist / self.k

    def M(self, pt):
        """Source point -> canvas."""
        r = math.radians(self.rot)
        x, y = pt[0] - self.tc[0], pt[1] - self.tc[1]
        x, y = x * math.cos(r) - y * math.sin(r), x * math.sin(r) + y * math.cos(r)
        return (self.centre[0] - x * self.sc, self.centre[1] + y * self.sc)

    def group(self, clip_id, box):
        x, y, w, h = box
        return (f'<clipPath id="{clip_id}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{self.s(6):.1f}"/></clipPath>'
                f'<g clip-path="url(#{clip_id})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff"/>' +
                art_image(f'<svg><g transform="translate({self.centre[0]:.2f} {self.centre[1]:.2f}) scale({-self.sc:.4f} {self.sc:.4f}) '
                          f'rotate({self.rot:.3f}) translate({-self.tc[0]:.2f} {-self.tc[1]:.2f})">{dbcls_art(self.p)}</g></svg>', box) +
                '</g>'
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{self.s(6):.1f}" fill="none" stroke="{I["rule"]}" '
                f'stroke-width="{self.s(1.2):.2f}"/>')


# ================================================================ svg #3  Fig. 22 arm holding a bag
def fig3():
    idx, p = 3, "m5f3_"
    K = 10.0                                   # canvas units per cm
    Ec = (150.0, 440.0)
    VB = (0, 0, 630, 700)
    s = H.Scale(VB[2], VB[3])
    A = Arm(p, s, Ec, K, r_ins=3.0)
    r_L = 35.0
    G = A.C((r_L, 0.0))
    ratio = r_L / A.d_cm
    red, blu, brn, grn = O["force"], O["geometry"], O["load"], O["neural"]
    o = [f'<defs>{H.markers(p, s)}</defs>']

    # ---- inset (upper right): DBCLS sagittal elbow
    box = (300, 112, 316, 262)
    ins = Inset(p + "db_", s, (box[0] + 150, box[1] + 128), 1.15)
    o.append(ins.group(f"{p}clip", box))
    tcx, tcy = ins.M(ins.tc[:2])
    tip, foot = ins.M(ins.tip), ins.M(ins.foot)
    ux, uy = tip[0] - foot[0], tip[1] - foot[1]
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    far = (foot[0] - ux * 70, foot[1] - uy * 70)
    o.append(H.line(s, far[0], far[1], tip[0], tip[1], red, "leader", H.DASH_LOA))
    o.append(H.arrow(s, p, tip[0], tip[1], tip[0] - ux * 46, tip[1] - uy * 46, "force"))
    o.append(f'<line x1="{tcx:.1f}" y1="{tcy:.1f}" x2="{foot[0]:.1f}" y2="{foot[1]:.1f}" stroke="#fff" stroke-width="{s(4.5):.1f}"/>')
    o.append(H.arrow(s, p, tcx, tcy, foot[0], foot[1], "geometry", both=True))
    o.append(H.joint_centre(s, tcx, tcy))
    o.append(H.label(s, box[0] + 8, box[1] - 26, "Inset: sagittal section of the circled elbow", "label2", I["primary"]))
    o.append(H.label(s, box[0] + 8, box[1] - 10, f"(this section is flexed ≈ {ins.flex:.0f}°)", "label2", I["secondary"]))
    lab = box[0] + box[2] - 6
    o.append(H.label(s, tcx, box[1] + 22, "humerus", "label2", I["secondary"], "middle"))
    rad = ins.M((146.0, 342.0))                    # on the radius shaft (path 4, between its edges)
    uln = ins.M((215.0, 320.0))                    # on the ulna shaft (path 22/25)
    o.append(H.label(s, rad[0] + 6, rad[1] + 5, "radius", "label2", I["secondary"]))
    o.append(H.label(s, uln[0], uln[1] + 5, "ulna", "label2", I["secondary"], "middle"))
    o.append(H.line(s, tip[0] + 3, tip[1] + 3, lab - 30, box[1] + 186, red))
    o.append(H.label(s, lab, box[1] + 200, "biceps tendon", "label2", red, "end"))
    o.append(H.label(s, lab, box[1] + 216, "→ radius", "label2", red, "end"))
    o.append(H.line(s, tcx - 7, tcy - 6, box[0] + 64, box[1] + 62, I["primary"]))
    o.append(H.label(s, box[0] + 8, box[1] + 44, "trochlea centre", "label2", I["primary"]))
    o.append(H.label(s, box[0] + 8, box[1] + 59, "= elbow axis", "label2", I["primary"]))
    mx, my = (tcx + foot[0]) / 2, (tcy + foot[1]) / 2
    o.append(H.label(s, mx + 12, my - 4, f'{it("d")}{H.sub("m", s, "label2")}', "label", blu))

    # ---- bag (behind the hand)
    bw = 2.6 * K
    o.append(f'<g transform="translate({G[0]:.1f} {G[1]:.1f})">'
             f'<path d="M{-bw*0.6:.1f},{4*K:.1f} L0,0 L{bw*0.6:.1f},{4*K:.1f}" fill="none" stroke="{brn}" stroke-width="{s(1.6):.2f}"/>'
             f'<path d="M{-bw*0.75:.1f},{4*K:.1f} L{bw*0.75:.1f},{4*K:.1f} L{bw:.1f},{10*K:.1f} L{-bw:.1f},{10*K:.1f} Z" '
             f'fill="#f7f4ef" stroke="{brn}" stroke-width="{s(1.2):.2f}"/></g>')
    o.append(H.arrow(s, p, G[0], G[1] + 10.5 * K, G[0], G[1] + 15.5 * K, "load"))
    o.append(H.label(s, G[0] + 10, G[1] + 14 * K, f'{it("W")} (bag)', fill=brn))

    # ---- arm: bones, biceps, line of action
    o.append(A.bones())
    bic, bez, width = A.biceps()
    o.append(bic)
    loa, (lx, ly) = A.loa()
    o.append(loa)
    # F_m arrow beside the distal tendon, offset to the anterior side
    nx, ny = -ly, lx
    if nx < 0:
        nx, ny = -nx, -ny
    S0 = (A.I[0] + nx * 9, A.I[1] + ny * 9 - 6)
    o.append(H.arrow(s, p, S0[0], S0[1], S0[0] - lx * 62, S0[1] - ly * 62, "force"))
    o.append(H.label(s, S0[0] + 8, S0[1] - 34, f'F{H.sub("m", s)} ≈ {ratio:.0f}×{it("W")}', fill=red))
    # d_m at the elbow (horizontal, 3 cm)
    o.append(H.arrow(s, p, Ec[0], Ec[1], A.P[0], A.P[1], "geometry", both=True))
    o.append(H.line(s, (Ec[0] + A.P[0]) / 2, Ec[1] - 3, 108, Ec[1] - 46, blu))
    o.append(H.label(s, 104, Ec[1] - 46, f'{it("d")}{H.sub("m", s)} ≈ {A.d_cm:.1f} cm', fill=blu, anchor="end"))
    o.append(H.joint_centre(s, Ec[0], Ec[1]))
    o.append(H.label(s, Ec[0] - 14, Ec[1] + 26, "elbow centre", "label2", I["secondary"], "end"))
    # link: elbow -> inset
    o.append(f'<circle cx="{Ec[0]:.1f}" cy="{Ec[1]:.1f}" r="{3.6*K:.1f}" fill="none" stroke="{I["rule"]}" '
             f'stroke-width="{s(1):.2f}" stroke-dasharray="{s(4):.1f} {s(3):.1f}"/>')
    # r_L dimension
    yd = Ec[1] + 4.6 * K
    o.append(H.line(s, Ec[0], Ec[1] + 3.8 * K, Ec[0], yd + 6, O["dim"], "leader", H.DASH_REF))
    o.append(H.line(s, G[0], G[1] + 10.5 * K, G[0], yd + 6, O["dim"], "leader", H.DASH_REF))
    o.append(H.line(s, Ec[0], yd, G[0] - bw - 4, yd, brn, "ref",
                    extra=f'marker-start="url(#{p}a_load)"'))
    o.append(H.line(s, G[0] - bw - 4, yd, G[0], yd, brn, "ref", extra=f'marker-end="url(#{p}a_load)"'))
    o.append(H.label(s, (Ec[0] + G[0]) / 2 - 20, yd + 20, f'{it("r")}{H.sub("L", s)} ≈ {r_L:.0f} cm '
                     f'({ratio:.0f}× the muscle’s lever)', fill=brn, anchor="middle"))
    # shoulder, origin, biceps label, motor nerve
    top = A.C((0.0, -A.hum_cm))
    Og = A.C(ARM["origin"])
    o.append(f'<circle cx="{Og[0]:.1f}" cy="{Og[1]:.1f}" r="{s(2.5):.2f}" fill="{T["muscle"][1]}"/>')
    o.append(H.label(s, Og[0] + 9, Og[1] + 4, "long head → scapula", "label2", T["muscle"][1]))
    o.append(H.label(s, top[0] + 14, top[1] + 10, "humeral head", "label2", I["muted"]))
    o.append(H.label(s, top[0] + 14, top[1] + 25, "not drawn", "label2", I["muted"]))
    bx, by, bnx, bny = bez(0.6)
    e = (bx + abs(bnx) * width(0.6), by + bny * width(0.6) * (1 if bnx > 0 else -1))
    o.append(H.line(s, e[0] + 2, e[1], 212, e[1] + 10, T["muscle"][1]))
    o.append(H.label(s, 216, e[1] + 15, "biceps", fill=T["muscle"][1]))
    bt = bez(0.42)
    nerve_t = (bt[0] - abs(bt[2]) * width(0.42) * 0.55, bt[1] - bt[3] * width(0.42) * 0.55)
    o.append(f'<path d="M22,70 C30,170 70,{nerve_t[1]+20:.1f} {nerve_t[0]-4:.1f},{nerve_t[1]:.1f}" fill="none" '
             f'stroke="{grn}" stroke-width="{s(2):.2f}" marker-end="url(#{p}a_neural)"/>'
             f'<circle cx="22" cy="70" r="{s(3.5):.2f}" fill="{grn}"/>')
    o.append(H.label(s, 10, 52, f'motor nerve → neural drive {it("u")}({it("t")})', fill=grn))

    # ---- credit
    c1 = H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt 208", title="Human Arm Bones",
                                    changes="Recoloured; anterior-view bones reposed (humerus vertical, forearm turned about the elbow).")
    c2 = H.ATTRIBUTION["by"].format(author="DataBase Center for Life Science (DBCLS)",
                                    title="202107 Sagittal section through the elbow joint", licence="CC BY 4.0",
                                    changes="Recoloured, mirrored, rotated, cropped.").replace("Art:", "Inset:")
    lines = wrap(c1, 100) + wrap(c2, 100) + ["Biceps, nerve, bag and overlays drawn for this course. Arrows are not to force scale."]
    o.append(H.credit(s, 8, VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines))

    aria = ("Arm holding a bag, side view: the humerus is vertical and the forearm horizontal, flexed 90 degrees at the "
            "elbow. A biceps belly runs in front of the humerus from a tendon to the scapula down to a tendon on the "
            "radius 3 cm beyond the elbow centre. A green motor nerve carrying the neural drive u(t) enters the belly. "
            f"The muscle force F_m, about {ratio:.0f} times the bag weight, pulls up along the distal tendon at a moment arm "
            f"of {A.d_cm:.1f} cm; the bag's weight W hangs {r_L:.0f} cm from the elbow. An inset shows a sagittal section "
            f"of a real elbow, flexed about {ins.flex:.0f} degrees, with the trochlea centre as the elbow axis and the "
            "perpendicular from it to the biceps tendon line.").replace("F_m", "F m")
    return finish(VB, aria, s, o)


# ================================================================ svg #34  Fig. 28 force times moment arm
def fig34():
    idx, p = 34, "m5f34_"
    K = 10.0
    Ec = (190.0, 390.0)
    VB = (0, 0, 760, 610)
    s = H.Scale(VB[2], VB[3])
    A = Arm(p, s, Ec, K, r_ins=3.0)               # same art and geometry as svg #3
    r_L = 30.0                                     # the 2 kg dumbbell grip of the §8 worked case
    G = A.C((r_L, 0.0))
    red, blu, brn = O["force"], O["geometry"], O["load"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # dumbbell at the grip (behind the hand)
    o.append(f'<g fill="{I["rule"]}" stroke="{I["secondary"]}" stroke-width="{s(1):.2f}">'
             f'<rect x="{G[0]-0.6*K:.1f}" y="{G[1]-4.6*K:.1f}" width="{1.2*K:.1f}" height="{9.2*K:.1f}" rx="{s(2):.1f}"/>'
             f'<rect x="{G[0]-1.8*K:.1f}" y="{G[1]-5.2*K:.1f}" width="{3.6*K:.1f}" height="{1.6*K:.1f}" rx="{s(3):.1f}"/>'
             f'<rect x="{G[0]-1.8*K:.1f}" y="{G[1]+3.6*K:.1f}" width="{3.6*K:.1f}" height="{1.6*K:.1f}" rx="{s(3):.1f}"/></g>')
    # triceps (antagonist) behind the humerus, tendon to the olecranon
    tri, tbez, twidth = A.belly(ARM["tri"], ARM["tri_half_w"], T["muscle_dk"][1])
    Ti = A.C(ARM["tri_ins"])
    TB = A.C(ARM["tri"][2])
    o.append(A.bones())
    o.append(A.tendon(TB, Ti, 3.0) + tri)
    bic, bez, width = A.biceps()
    o.append(bic)
    loa, (lx, ly) = A.loa()
    o.append(loa)
    nx, ny = -ly, lx
    if nx < 0:
        nx, ny = -nx, -ny
    S0 = (A.I[0] + nx * 9, A.I[1] + ny * 9 - 6)
    o.append(H.arrow(s, p, S0[0], S0[1], S0[0] - lx * 62, S0[1] - ly * 62, "force"))
    o.append(H.label(s, S0[0] + 8, S0[1] - 34, f'F{H.sub("m", s)}', fill=red))
    # triceps pull (other rotational sense)
    tx, ty = TB[0] - Ti[0], TB[1] - Ti[1]
    tl = math.hypot(tx, ty)
    o.append(H.arrow(s, p, Ti[0] - 9, Ti[1] - 2, Ti[0] - 9 + tx / tl * 52, Ti[1] - 2 + ty / tl * 52, "force"))
    o.append(f'<circle cx="{Ti[0]:.1f}" cy="{Ti[1]:.1f}" r="{s(2.8):.2f}" fill="{red}" stroke="#fff" stroke-width="{s(1):.2f}"/>')
    # d_m
    o.append(H.arrow(s, p, Ec[0], Ec[1], A.P[0], A.P[1], "geometry", both=True))
    o.append(H.line(s, (Ec[0] + A.P[0]) / 2, Ec[1] - 3, Ec[0] + 52, Ec[1] - 70, blu))
    o.append(H.label(s, Ec[0] + 56, Ec[1] - 72, f'moment arm {it("d")}{H.sub("m", s)}', fill=blu))
    o.append(H.joint_centre(s, Ec[0], Ec[1]))
    o.append(H.label(s, Ec[0] - 30, Ec[1] + 34, "elbow axis", "label2", I["secondary"], "end"))
    # load
    o.append(H.arrow(s, p, G[0], G[1] + 5.6 * K, G[0], G[1] + 11.5 * K, "load"))
    o.append(H.label(s, G[0] + 10, G[1] + 10 * K, f'{it("W")} = {it("m")}{it("g")}', fill=brn))
    yd = Ec[1] + 7.0 * K
    o.append(H.line(s, Ec[0], Ec[1] + 3.8 * K, Ec[0], yd + 6, O["dim"], "leader", H.DASH_REF))
    o.append(H.line(s, G[0], G[1] + 11.5 * K, G[0], yd + 6, O["dim"], "leader", H.DASH_REF))
    o.append(H.line(s, Ec[0], yd, G[0], yd, brn, "ref",
                    extra=f'marker-start="url(#{p}a_load)" marker-end="url(#{p}a_load)"'))
    o.append(H.label(s, (Ec[0] + G[0]) / 2, yd + 20, f'load moment arm {it("r")}{H.sub("L", s)}', fill=brn, anchor="middle"))
    # muscle labels
    bx, by, bnx, bny = bez(0.55)
    e = (bx + abs(bnx) * width(0.55), by)
    o.append(H.line(s, e[0] + 2, e[1], 300, e[1] - 10, T["muscle"][1]))
    o.append(H.label(s, 304, e[1] - 12, "biceps", fill=T["muscle"][1]))
    o.append(H.label(s, 304, e[1] + 6, "agonist (flexes)", "label2", I["secondary"]))
    tbx, tby, tnx, tny = tbez(0.5)
    te = (tbx - abs(tnx) * twidth(0.5), tby)
    o.append(H.line(s, te[0] - 2, te[1], 92, te[1] - 10, T["muscle"][1]))
    o.append(H.label(s, 88, te[1] - 12, "triceps", fill=T["muscle"][1], anchor="end"))
    o.append(H.label(s, 88, te[1] + 6, "antagonist", "label2", I["secondary"], "end"))
    o.append(H.label(s, 88, te[1] + 21, "(extends)", "label2", I["secondary"], "end"))
    o.append(H.line(s, Ti[0] - 4, Ti[1] + 3, 96, Ec[1] + 20, T["muscle"][1]))
    o.append(H.label(s, 92, Ec[1] + 24, "→ olecranon", "label2", T["muscle"][1], "end"))
    o.append(H.label(s, 92, Ec[1] + 39, "(see inset)", "label2", T["muscle"][1], "end"))
    top = A.C((0.0, -A.hum_cm))
    o.append(H.label(s, top[0] - 16, top[1] + 30, "humerus", "label2", I["muted"], "end"))
    o.append(H.label(s, 10, 30, f'τ{H.sub("net", s)} = τ{H.sub("ago", s)} − τ{H.sub("anti", s)}'))
    o.append(H.label(s, 10, 50, "biceps flexes, triceps extends", "label2", I["secondary"]))
    # ---- inset: DBCLS sagittal elbow, both muscles and both moment arms
    o.append(f'<circle cx="{Ec[0]:.1f}" cy="{Ec[1]:.1f}" r="{3.6*K:.1f}" fill="none" stroke="{I["rule"]}" '
             f'stroke-width="{s(1):.2f}" stroke-dasharray="{s(4):.1f} {s(3):.1f}"/>')
    box = (440, 62, 310, 262)
    ins = Inset(p + "db_", s, (box[0] + 150, box[1] + 128), 1.15)
    o.append(ins.group(f"{p}clip", box))
    tcx, tcy = ins.M(ins.tc[:2])
    lab = box[0] + box[2] - 6
    for (src_tip, src_far), sym, sign in ((DB["tendon"][::-1], "m", 1), (DB["triceps"], "anti", -1)):
        tip, far0 = ins.M(src_tip), ins.M(src_far)
        foot, _ = foot_of_perp((tcx, tcy), tip, far0)
        ux, uy = far0[0] - tip[0], far0[1] - tip[1]
        L = math.hypot(ux, uy)
        ux, uy = ux / L, uy / L
        o.append(H.line(s, tip[0], tip[1], tip[0] + ux * 120, tip[1] + uy * 120, red, "leader", H.DASH_LOA))
        o.append(H.arrow(s, p, tip[0], tip[1], tip[0] + ux * 44, tip[1] + uy * 44, "force"))
        o.append(f'<line x1="{tcx:.1f}" y1="{tcy:.1f}" x2="{foot[0]:.1f}" y2="{foot[1]:.1f}" stroke="#fff" stroke-width="{s(4.5):.1f}"/>')
        o.append(H.arrow(s, p, tcx, tcy, foot[0], foot[1], "geometry", both=True))
        mx, my = (tcx + foot[0]) / 2, (tcy + foot[1]) / 2
        o.append(H.label(s, mx + (-8 if sign > 0 else -4), my + (20 if sign > 0 else -8),
                         f'{it("d")}{H.sub(sym, s, "label2")}', "label", blu, "end"))
    o.append(H.joint_centre(s, tcx, tcy))
    o.append(H.label(s, box[0] + 8, box[1] - 26, "Inset: sagittal section of the circled elbow", "label2", I["primary"]))
    o.append(H.label(s, box[0] + 8, box[1] - 10, f"(this section is flexed ≈ {ins.flex:.0f}°)", "label2", I["secondary"]))
    o.append(H.label(s, tcx, box[1] + 22, "humerus", "label2", I["secondary"], "middle"))
    o.append(H.label(s, lab, box[1] + 200, "biceps → radius", "label2", I["primary"], "end"))
    o.append(H.label(s, box[0] + 8, box[1] + 200, "triceps →", "label2", I["primary"]))
    o.append(H.label(s, box[0] + 8, box[1] + 215, "olecranon", "label2", I["primary"]))
    o.append(H.label(s, tcx, box[1] + box[3] - 10, "trochlea centre = elbow axis", "label2", I["primary"], "middle"))
    c1 = H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt 208", title="Human Arm Bones",
                                    changes="Recoloured; anterior-view bones reposed (humerus vertical, forearm turned about the elbow).")
    c2 = H.ATTRIBUTION["by"].format(author="DataBase Center for Life Science (DBCLS)",
                                    title="202107 Sagittal section through the elbow joint", licence="CC BY 4.0",
                                    changes="Recoloured, mirrored, rotated, cropped.").replace("Art:", "Inset:")
    lines = wrap(c1, 120) + wrap(c2, 120) + ["Biceps, triceps, dumbbell and overlays drawn for this course. Arrows are not to force scale."]
    o.append(H.credit(s, 8, VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines))
    aria = ("Side view of an arm with the elbow at 90 degrees, the same arm art as Fig. 22: the biceps (agonist) runs in "
            "front of the humerus to the radius and pulls up with force F m; the blue moment arm d m is the "
            "perpendicular from the elbow axis to its line of action. The triceps (antagonist) runs behind the humerus "
            "to the olecranon and pulls the other way. A dumbbell of weight W = m g hangs at the hand at the load "
            "moment arm r L. Net torque: tau net = tau ago minus tau anti. An inset shows a sagittal section of a real "
            "elbow, flexed about 32 degrees: the biceps tendon to the radius passes in front of the trochlea centre at "
            "moment arm d m and the triceps to the olecranon passes behind it at moment arm d anti.")
    return finish(VB, aria, s, o)


# ================================================================ svg #50  C9 co-contraction (problem figure)
def arc_arrow(s, p, cx, cy, r, a0, a1, col_key):
    """Circular arc from angle a0 to a1 (deg, screen y down), head at a1."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    sweep = 1 if a1 > a0 else 0
    large = 1 if abs(a1 - a0) > 180 else 0
    return (f'<path d="M{x0:.2f},{y0:.2f} A{r},{r} 0 {large} {sweep} {x1:.2f},{y1:.2f}" fill="none" '
            f'stroke="{O[col_key]}" stroke-width="{s(H.PX["geom"]):.2f}" marker-end="url(#{p}a_{col_key})"/>')


def fig50():
    """Same arm art and construction as svg #34, both muscles active, no load: tau_net = 0."""
    p = "m5f50_"
    K = 9.0
    Ec = (150.0, 320.0)
    VB = (0, 0, 440, 520)
    s = H.Scale(VB[2], VB[3], display_w=400)
    A = Arm(p, s, Ec, K, r_ins=3.0)
    red, blu = O["force"], O["geometry"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    tri, tbez, twidth = A.belly(ARM["tri"], ARM["tri_half_w"], T["muscle_dk"][1])
    Ti, TB = A.C(ARM["tri_ins"]), A.C(ARM["tri"][2])
    o.append(A.bones(hand=False))                    # forearm only: no load in this problem
    o.append(A.tendon(TB, Ti, 2.4) + tri)
    bic, bez, width = A.biceps()
    o.append(bic)
    o.append(f'<circle cx="{Ti[0]:.1f}" cy="{Ti[1]:.1f}" r="{s(2.8):.2f}" fill="{red}" stroke="#fff" stroke-width="{s(1):.2f}"/>')
    # lines of action, extended below the forearm to the moment-arm dimension row
    yd = Ec[1] + 7.5 * K
    dims = []
    for a, b, sym, side in ((A.B, A.I, "ago", 1), (TB, Ti, "anti", -1)):
        ux, uy = b[0] - a[0], b[1] - a[1]
        t = (yd - a[1]) / uy
        X = (a[0] + ux * t, yd)
        o.append(H.line(s, a[0], a[1], X[0], X[1] + 4, red, "leader", H.DASH_LOA))
        L = math.hypot(ux, uy)
        S0 = (b[0] + side * 8, b[1] - 4)                        # force arrow beside the tendon, outside
        o.append(H.arrow(s, p, S0[0], S0[1], S0[0] - ux / L * 52, S0[1] - uy / L * 52, "force"))
        o.append(H.label(s, S0[0] + side * 6, S0[1] - 40, f'{it("F")}{H.sub(sym, s)}', fill=red,
                         anchor="start" if side > 0 else "end"))
        foot, dist = foot_of_perp(Ec, a, b)
        dims.append((sym, X[0], dist / K))
    o.append(H.joint_centre(s, Ec[0], Ec[1]))
    # opposite torques about the elbow axis (flexion turns the forearm up = counter-clockwise on screen)
    o.append(arc_arrow(s, p, Ec[0], Ec[1], 4.2 * K, 75, -5, "force"))
    o.append(arc_arrow(s, p, Ec[0], Ec[1], 4.2 * K, 105, 185, "force"))
    o.append(H.label(s, Ec[0] + 4.6 * K, Ec[1] + 4.4 * K, f'{it("τ")}{H.sub("ago", s)}', fill=red))
    o.append(H.label(s, Ec[0] - 4.6 * K, Ec[1] + 4.4 * K, f'{it("τ")}{H.sub("anti", s)}', fill=red, anchor="end"))
    # moment arms, measured horizontally at the dimension row (both lines of action are near vertical)
    o.append(H.line(s, Ec[0], Ec[1] + 4.6 * K, Ec[0], yd + 5, O["dim"], "leader", H.DASH_REF))
    for sym, x, _ in dims:
        o.append(H.arrow(s, p, Ec[0], yd, x, yd, "geometry", both=True))
        o.append(H.label(s, x + (8 if x > Ec[0] else -8), yd + 5, f'{it("d")}{H.sub(sym, s)}', fill=blu,
                         anchor="start" if x > Ec[0] else "end"))
    # muscle labels
    bx, by, bnx, bny = bez(0.5)
    e = (bx + abs(bnx) * width(0.5), by)
    o.append(H.line(s, e[0] + 2, e[1], 214, e[1] - 6, T["muscle"][1]))
    o.append(H.label(s, 218, e[1] - 8, "agonist (biceps)", "label2", I["primary"]))
    o.append(H.label(s, 218, e[1] + 8, "active", "label2", I["secondary"]))
    tbx, tby, tnx, tny = tbez(0.5)
    te = (tbx - abs(tnx) * twidth(0.5), tby)
    lx = te[0] - 16
    o.append(H.line(s, te[0] - 2, te[1], lx + 4, te[1] - 6, T["muscle"][1]))
    o.append(H.label(s, lx, te[1] - 8, "antagonist", "label2", I["primary"], "end"))
    o.append(H.label(s, lx, te[1] + 8, "(triceps)", "label2", I["primary"], "end"))
    o.append(H.label(s, lx, te[1] + 24, "active", "label2", I["secondary"], "end"))
    o.append(H.label(s, 12, yd + 40, f'{it("τ")}{H.sub("net", s)} = {it("τ")}{H.sub("ago", s)} − '
                     f'{it("τ")}{H.sub("anti", s)} = 0, yet both muscles burn ATP:'))
    o.append(H.label(s, 12, yd + 62, "what does the co-contraction buy?", "label", I["secondary"]))
    c1 = H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt 208", title="Human Arm Bones",
                                    changes="Recoloured; reposed. Muscles and overlays drawn for this course.")
    lines = wrap(c1, 64)
    o.append(H.credit(s, 8, VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines))
    aria = ("Problem C9 setup: side view of an upper arm and forearm, the same arm art as Fig. 28, with the elbow at 90 "
            "degrees and no load. "
            "The agonist (biceps) in front of the humerus and the antagonist (triceps) behind it are both active. The "
            "biceps pulls on the radius in front of the elbow axis at moment arm d ago; the triceps pulls on the "
            "olecranon behind the axis at moment arm d anti. Their torques tau ago and tau anti turn in opposite senses "
            "and cancel: tau net = tau ago minus tau anti = 0, yet both muscles burn ATP. Question: what does the "
            "co-contraction buy?")
    return finish(VB, aria, s, o)


# ================================================================ plots (problem figures, display_w = 400)
def _axes(s, x0, x1, y0, y1):
    return [H.line(s, x0, y0, x1, y0, I["axis"], "axis"), H.line(s, x0, y0, x0, y1, I["axis"], "axis")]


def f_L(l):
    """module05 Proposition 2.1 (breakpoints of the ascending limb as in the style guide)."""
    pts = [(1.27, 0.0), (1.60, 0.8), (2.60, 1.0), (2.70, 1.0), (4.20, 0.0)]
    if l <= pts[0][0] or l >= pts[-1][0]:
        return 0.0
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        if xa <= l <= xb:
            return ya + (yb - ya) * (l - xa) / (xb - xa)


# ---------------------------------------------------------------- svg #53  D2 descending limb
A_THICK, A_THIN, BARE = 1.60, 1.30, 0.10     # module05 §2 (µm)


def fig53():
    p = "m5f53_"
    VB = (0, 0, 400, 400)
    s = H.Scale(VB[2], VB[3], display_w=400)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # half-sarcomere at l = 3.45 µm, measured from the centre (M-line) to the Z-disc
    l = 3.45
    S, xm, ym = 150.0, 40.0, 70.0                     # px per µm, M-line x, filament row y
    X = lambda u: xm + u * S                          # noqa: E731
    tip = l / 2 - A_THIN
    ov = A_THICK / 2 - tip
    o.append(f'<rect x="{X(tip):.1f}" y="{ym-22}" width="{ov*S:.1f}" height="44" fill="{O["neural"]}" opacity="0.16"/>')
    o.append(H.line(s, X(0), ym - 30, X(0), ym + 30, O["dim"], "ref", H.DASH_REF))
    o.append(H.label(s, X(0), ym - 36, "M-line", "label2", I["secondary"], "middle"))
    o.append(f'<rect x="{X(0):.1f}" y="{ym-5}" width="{A_THICK/2*S:.1f}" height="10" rx="5" fill="{T["myosin"][0]}" stroke="{T["myosin"][1]}" stroke-width="{s(0.8):.2f}"/>')
    n = 12
    for j in range(n + 1):
        xx = X(BARE / 2 + j * (A_THICK / 2 - BARE / 2) / n)
        o.append(f'<path d="M{xx:.1f},{ym-5} l-2.5,-4 M{xx:.1f},{ym+5} l-2.5,4" stroke="{T["myosin"][1]}" stroke-width="{s(0.9):.2f}"/>')
    for yy in (ym - 14, ym + 14):
        o.append(f'<rect x="{X(tip):.1f}" y="{yy-3}" width="{A_THIN*S:.1f}" height="6" rx="3" fill="{T["actin"][0]}" stroke="{T["actin"][1]}" stroke-width="{s(0.8):.2f}"/>')
    o.append(f'<rect x="{X(l/2)-2.5:.1f}" y="{ym-24}" width="5" height="48" fill="{T["zdisc"][0]}"/>')
    o.append(H.label(s, X(l / 2), ym - 30, "Z", "label2", I["secondary"], "middle"))
    # dimensions under the row
    yA, yt, yo = ym + 40, ym + 74, ym + 108
    o.append(H.arrow(s, p, X(0), yA, X(A_THICK / 2), yA, "dim", both=True))
    o.append(H.label(s, X(A_THICK / 2) + 6, yA + 5, f'{it("A")}/2', "label2", I["secondary"]))
    o.append(H.arrow(s, p, X(tip), yt, X(l / 2), yt, "dim", both=True))
    o.append(H.label(s, X(tip + A_THIN / 2), yt - 6, f'{it("a")}{H.sub("thin", s, "label2")}', "label2", I["secondary"], "middle"))
    o.append(H.line(s, X(tip), ym + 18, X(tip), yo + 6, O["dim"], "leader", H.DASH_REF))
    o.append(H.arrow(s, p, X(0), yo, X(tip), yo, "dim", both=True))
    o.append(H.label(s, X(0) + 4, yo + 20, f'{it("ℓ")}/2 − {it("a")}{H.sub("thin", s, "label2")}', "label2", I["secondary"]))
    o.append(H.label(s, X(tip + ov / 2), ym - 30, "overlap", "label2", O["neural"], "middle"))
    o.append(H.label(s, 390, ym + 40 + 0, f"ℓ = {l:.2f} µm", "label2", I["secondary"], "end"))
    # plot of f_L with the descending limb
    x0, x1, y0, y1 = 52, 384, 360, 218
    L0, L1 = 1.0, 4.4
    PX = lambda v: x0 + (v - L0) / (L1 - L0) * (x1 - x0)   # noqa: E731
    PY = lambda f: y0 - f / 1.15 * (y0 - y1)               # noqa: E731
    o.append(H.line(s, x0, PY(1), x1, PY(1), "#e6e6e6", "leader"))
    o += _axes(s, x0, x1, y0, y1)
    for f in (0.0, 0.5, 1.0):
        o.append(H.line(s, x0 - 4, PY(f), x0, PY(f), I["axis"], "leader"))
        o.append(H.label(s, x0 - 7, PY(f) + 4.5, f"{f:.1f}", "tick", I["secondary"], "end"))
    for v, t in ((2.0, "2"), (2.7, "2.7"), (3.45, "3.45"), (4.2, "4.2")):
        o.append(H.line(s, PX(v), y0, PX(v), y0 + 4, I["axis"], "leader"))
        o.append(H.label(s, PX(v), y0 + 18, t, "tick", I["secondary"], "middle"))
    o.append(H.label(s, (x0 + x1) / 2 + 40, y0 + 36, "sarcomere length ℓ (µm)", "label2", I["primary"], "middle"))
    o.append(H.label(s, 14, (y0 + y1) / 2, f'f{H.sub("L", s, "label2")}', "label2", I["primary"], "middle",
                     f'transform="rotate(-90 14 {(y0 + y1) / 2})"'))
    grid = [L0 + i * 0.02 for i in range(int(round((L1 - L0) / 0.02)) + 1)]
    curve = sorted(set([L0 + i * 0.1 for i in range(35)] + [1.27, 1.6, 2.6, 2.7, 4.2, L1]))
    o.append(poly([(PX(v), PY(f_L(v))) for v in curve], H.SERIES[0], s(H.PX["curve"])))
    for v in (2.7, 4.2):
        o.append(f'<circle cx="{PX(v):.2f}" cy="{PY(f_L(v)):.2f}" r="{s(H.PX["dot"]):.2f}" fill="{O["flag"]}" stroke="#fff" stroke-width="{s(1.5):.2f}"/>')
    o.append(f'<circle cx="{PX(l):.2f}" cy="{PY(f_L(l)):.2f}" r="{s(H.PX["dot"]):.2f}" fill="{O["neural"]}" stroke="#fff" stroke-width="{s(1.5):.2f}"/>')
    o.append(H.label(s, PX(l) + 10, PY(f_L(l)) - 6, f"f = {f_L(l):.2f}", "label2", I["secondary"]))
    o.append(H.label(s, PX(2.7) + 6, PY(1.0) - 8, "ℓ₀ = 2.70", "label2", I["secondary"]))
    o.append(H.label(s, PX(3.05), PY(0.42), "descending", "label2", I["secondary"], "end", 'font-style="italic"'))
    o.append(H.label(s, PX(3.05), PY(0.42) + 15, "limb", "label2", I["secondary"], "end", 'font-style="italic"'))
    hv = [[round(PX(v), 2), round(PY(f_L(v)), 2),
           f"ℓ = {v:.2f} µm, f = {f_L(v):.2f}" + (f", overlap = {A_THICK/2-(v/2-A_THIN):.2f} µm" if 2.7 <= v <= 4.2 else "")]
          for v in grid]
    aria = ("Top: one half-sarcomere at 3.45 micrometres, from the M-line to the Z-disc. The thick-filament half runs "
            "out to A/2 = 0.80, the thin filament of length a thin = 1.30 reaches in from the Z-disc to an inner tip at "
            "l/2 minus a thin from the centre, and the green overlap between them is 0.38 micrometres. Bottom: the "
            "active length-tension curve f L against sarcomere length; the straight descending limb falls from 1 at "
            "2.70 to 0 at 4.20 micrometres, and the 3.45 case sits at f = 0.50.")
    return finish(VB, aria, s, o, H.hover_attr([x0, y1, x1, y0], hv))


# ---------------------------------------------------------------- svg #59  D8 moment-arm geometry
def fig59():
    p = "m5f59_"
    VB = (0, 0, 400, 300)
    s = H.Scale(VB[2], VB[3], display_w=400)
    J = (110.0, 210.0)
    r1, r2, gam = 190.0, 120.0, math.radians(100.0)     # drawn lengths (px) and enclosed angle
    a1 = math.radians(-95.0)                             # origin direction: up the upper-arm segment
    Op = (J[0] + r1 * math.cos(a1), J[1] + r1 * math.sin(a1))
    a2 = a1 + gam
    Ip = (J[0] + r2 * math.cos(a2), J[1] + r2 * math.sin(a2))
    F, dpx = foot_of_perp(J, Op, Ip)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(H.line(s, J[0], J[1], Op[0], Op[1], I["secondary"], "axis"))
    o.append(H.line(s, J[0], J[1], Ip[0], Ip[1], I["secondary"], "axis"))
    o.append(H.line(s, Op[0], Op[1], Ip[0], Ip[1], O["force"], "force"))
    # angle arc gamma
    ra = 30
    arc0 = (J[0] + ra * math.cos(a1), J[1] + ra * math.sin(a1))
    arc1 = (J[0] + ra * math.cos(a2), J[1] + ra * math.sin(a2))
    o.append(f'<path d="M{arc0[0]:.1f},{arc0[1]:.1f} A{ra},{ra} 0 0 1 {arc1[0]:.1f},{arc1[1]:.1f}" fill="none" '
             f'stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"/>')
    am = (a1 + a2) / 2
    o.append(H.label(s, J[0] + 44 * math.cos(am) - 4, J[1] + 44 * math.sin(am) + 5, "γ", "label", I["primary"], "middle", 'font-style="italic"'))
    # moment arm with right-angle mark
    o.append(H.arrow(s, p, J[0], J[1], F[0], F[1], "geometry", both=True))
    ux, uy = (Ip[0] - Op[0]) / math.dist(Op, Ip), (Ip[1] - Op[1]) / math.dist(Op, Ip)
    vx, vy = (J[0] - F[0]) / dpx, (J[1] - F[1]) / dpx
    q = 8
    o.append(f'<path d="M{F[0]+ux*q:.1f},{F[1]+uy*q:.1f} l{vx*q:.1f},{vy*q:.1f} l{-ux*q:.1f},{-uy*q:.1f}" fill="none" '
             f'stroke="{O["geometry"]}" stroke-width="{s(1):.2f}"/>')
    mx, my = (J[0] + F[0]) / 2, (J[1] + F[1]) / 2
    o.append(H.label(s, mx + 8, my + 16, f'{it("d")}{H.sub("m", s)}', fill=O["geometry"]))
    o.append(H.joint_centre(s, *J))
    for P_, t, anc, dx, dy in ((Op, "origin", "start", 9, 4), (Ip, "insertion", "start", 8, 18)):
        o.append(f'<circle cx="{P_[0]:.1f}" cy="{P_[1]:.1f}" r="{s(3.5):.2f}" fill="{O["force"]}" stroke="#fff" stroke-width="{s(1):.2f}"/>')
        o.append(H.label(s, P_[0] + dx, P_[1] + dy, t, "label2", I["secondary"], anc))
    o.append(H.label(s, J[0] - 12, J[1] + 26, "joint axis", "label2", I["secondary"], "middle"))
    m1 = ((J[0] + Op[0]) / 2, (J[1] + Op[1]) / 2)
    o.append(H.label(s, m1[0] - 10, m1[1], f'{it("r")}{H.sub("1", s)}', anchor="end"))
    m2 = ((J[0] + Ip[0]) / 2, (J[1] + Ip[1]) / 2)
    o.append(H.label(s, m2[0] + 4, m2[1] + 22, f'{it("r")}{H.sub("2", s)}'))
    mL = ((Op[0] + Ip[0]) / 2, (Op[1] + Ip[1]) / 2)
    o.append(H.label(s, mL[0] + 14, mL[1] - 4, f'muscle, length {it("L")}', fill=O["force"]))
    o.append(H.label(s, 390, 286, "drawn with γ = 100°", "label2", I["muted"], "end"))
    aria = ("Moment-arm geometry: from the joint axis, the muscle origin lies at distance r1 and the insertion at "
            "distance r2, with angle gamma between those two lines. The muscle runs straight from origin to insertion "
            "with length L, and the moment arm d m is the perpendicular from the joint axis to the muscle line.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #72  K6 joint strength
def k6_fL(x):
    """K6 solution script, verbatim: active length factor at normalised fibre length x."""
    if x <= 0.47 or x >= 1.556:
        return 0.0
    if x < 0.963:
        return (x - 0.47) / 0.493
    if x <= 1.0:
        return 1.0
    return (1.556 - x) / 0.556


def fig72():
    p = "m5f72_"
    VB = (0, 0, 400, 300)
    s = H.Scale(VB[2], VB[3], display_w=400)
    th = [30.0 + i * 0.1 for i in range(801)]
    ell = [1.0 - 0.003 * (t - 70.0) for t in th]
    dm = [1.8 + 2.2 * math.sin(math.radians(t)) for t in th]
    st = [k6_fL(e) * d for e, d in zip(ell, dm)]
    kpk = max(range(len(st)), key=st.__getitem__)
    plat = [t for t, e in zip(th, ell) if 0.963 <= e <= 1.0]
    p0, p1 = min(plat), max(plat)
    x0, x1, y0, y1 = 50, 384, 238, 40
    X = lambda t: x0 + (t - 30) / 80 * (x1 - x0)   # noqa: E731
    Y = lambda v: y0 - (v - 2.0) / 2.2 * (y0 - y1)   # noqa: E731  y from 2.0 to 4.2 cm
    o = [f'<rect x="{X(p0):.2f}" y="{y1}" width="{X(p1)-X(p0):.2f}" height="{y0-y1}" fill="{O["neural"]}" opacity="0.12"/>']
    for v in (3.0, 4.0):
        o.append(H.line(s, x0, Y(v), x1, Y(v), "#e6e6e6", "leader"))
    o += _axes(s, x0, x1, y0, y1)
    for v in (2.0, 2.5, 3.0, 3.5, 4.0):
        o.append(H.line(s, x0 - 4, Y(v), x0, Y(v), I["axis"], "leader"))
        o.append(H.label(s, x0 - 7, Y(v) + 4.5, f"{v:.1f}", "tick", I["secondary"], "end"))
    for t in (30, 50, 70, 90, 110):
        o.append(H.line(s, X(t), y0, X(t), y0 + 4, I["axis"], "leader"))
        o.append(H.label(s, X(t), y0 + 18, f"{t}", "tick", I["secondary"], "middle"))
    o.append(H.label(s, (x0 + x1) / 2, y0 + 38, "elbow angle θ (deg)", "label2", I["primary"], "middle"))
    o.append(H.label(s, 14, (y0 + y1) / 2, "cm", "label2", I["primary"], "middle", f'transform="rotate(-90 14 {(y0 + y1) / 2})"'))
    o.append(poly([(X(t), Y(v)) for t, v in zip(th[::16], dm[::16])], H.SERIES[1], s(H.PX["curve_multi"]), 'stroke-dasharray="1 0"'))
    o.append(poly([(X(t), Y(max(v, 1.95))) for t, v in zip(th[::8], st[::8])], H.SERIES[0], s(H.PX["curve_multi"])))
    tp, vp = th[kpk], st[kpk]
    o.append(f'<circle cx="{X(tp):.2f}" cy="{Y(vp):.2f}" r="{s(H.PX["dot"]):.2f}" fill="{O["flag"]}" stroke="#fff" stroke-width="{s(1.5):.2f}"/>')
    o.append(f'<circle cx="{X(90):.2f}" cy="{Y(4.0):.2f}" r="{s(3):.2f}" fill="{H.SERIES[1]}" stroke="#fff" stroke-width="{s(1.2):.2f}"/>')
    # direct labels
    o.append(H.line(s, X(tp) - 3, Y(vp) - 3, X(62), Y(4.1) + 3, I["secondary"]))
    o.append(H.label(s, X(62), Y(4.1), f"peak {tp:.1f}° ({vp:.2f} cm)", "label2", I["primary"], "end"))
    o.append(H.label(s, X(97), Y(4.0) - 10, f'{it("d")}{H.sub("m", s, "label2")} peak 90°', "label2", I["secondary"], "start"))
    o.append(H.label(s, X(108), Y(3.02), f'f{H.sub("L", s, "label2")}·{it("d")}{H.sub("m", s, "label2")}', "label2", I["secondary"], "end"))
    o.append(H.label(s, X(33), Y(3.42), f'{it("d")}{H.sub("m", s, "label2")}(θ)', "label2", I["secondary"], "start"))
    o.append(H.label(s, (X(p0) + X(p1)) / 2, Y(2.36), f'f{H.sub("L", s, "label2")} = 1', "label2", I["secondary"], "middle"))
    o.append(H.label(s, (X(p0) + X(p1)) / 2, Y(2.36) + 15, f"{p0:.0f}–{p1:.1f}°", "label2", I["secondary"], "middle"))
    # legend
    lgx, lgy = X(34), Y(2.32)
    for k, (col, t) in enumerate(((H.SERIES[0], f'strength f{H.sub("L", s, "label2")}·{it("d")}{H.sub("m", s, "label2")}'),
                                  (H.SERIES[1], f'moment arm {it("d")}{H.sub("m", s, "label2")}'))):
        yy = lgy + k * 16
        o.append(H.line(s, lgx, yy - 4, lgx + 18, yy - 4, col, "curve_multi"))
        o.append(H.label(s, lgx + 24, yy, t, "label2", I["secondary"]))
    hv = []
    for i in range(0, len(th), 4):
        hv.append([round(X(th[i]), 2), [round(Y(max(st[i], 1.95)), 2), round(Y(dm[i]), 2)],
                   f"θ = {th[i]:.1f}°, ℓ/ℓ0 = {ell[i]:.3f}, fL = {k6_fL(ell[i]):.2f}, dm = {dm[i]:.2f} cm, fL·dm = {st[i]:.2f} cm"])
    aria = (f"Joint strength f L times d m in cm against elbow angle from 30 to 110 degrees, with the moment arm "
            f"d m = 1.8 + 2.2 sin theta for comparison. A shaded band marks the length-tension plateau, f L = 1, from "
            f"{p0:.0f} to {p1:.1f} degrees, where the two curves coincide. Strength peaks at {tp:.1f} degrees "
            f"({vp:.2f} cm), the far edge of the plateau; the moment arm alone peaks at 90 degrees (4.00 cm).")
    return finish(VB, aria, s, o, H.hover_attr([x0, y1, x1, y0], hv))


FIGS = {
    1: ("Triceps surae on a lower limb: muscle belly, Achilles tendon", fig1),
    3: ("A Tier-2 shaded arm flexed at the elbow holding a bag: the h", fig3),
    34: ("A Tier-2 shaded elbow at 90 degrees: humerus and forearm bon", fig34),
    50: ("agonist and antagonist co-contraction", fig50),
    53: ("descending limb of fL", fig53),
    59: ("moment arm geometry", fig59),
    72: ("joint strength f_L times moment arm peaks at 82 degrees, bet", fig72),
}

if __name__ == "__main__":
    a = Arm("x", H.Scale(560, 690), (150.0, 440.0), 10.0)
    ins = Inset("y", H.Scale(560, 690), (0, 0), 1.0)
    print(f"arm: k_art {a.k_art:.3f} u/cm, humerus visible {a.hum_cm:.1f} cm, d_m(90) {a.d_cm:.3f} cm")
    print(f"inset: trochlea {ins.tc}, rot {ins.rot:.2f}, flex {ins.flex:.1f} deg, u/cm {ins.u_cm}, k {ins.k:.2f}, "
          f"d_m {ins.d_cm:.2f} cm, insertion dist {math.dist(ins.tc[:2], ins.tip)/ins.k:.2f} cm, "
          f"model 1.8+2.2 sin = {1.8+2.2*math.sin(math.radians(ins.flex)):.2f} cm")
