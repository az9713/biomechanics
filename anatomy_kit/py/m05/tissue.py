"""Module 5, group `tissue`: muscle tissue, sarcomere and cell-biology figures in the house style.

Main text (760 px): svg 2, 5, 6, 7, 9, 11, 12, 14, 17, 24, 28.  Problems (400 px): svg 42, 43, 44, 45, 52.
Geometry from the module 5 notation table (line 570-573): thick A = 1.60 um, thin a_thin = 1.30 um,
bare zone B = 0.10 um. f_L as in the approved style-guide example (ex_tissue / ex_plot).
"""
import html
import math

import house as H

T, O, I = H.TISSUE, H.OVERLAY, H.INK
BOX, GRID = "#f7f4ef", "#e6e6e6"
A_THICK, A_THIN, BARE = 1.60, 1.30, 0.10       # module05 notation table (um)


def f_L(l):
    """Approved example law: ascending 1.27 -> 1.6 (0.8) -> 2.6, plateau 2.6-2.7, descending to 4.2."""
    pts = [(1.27, 0.0), (1.60, 0.8), (2.60, 1.0), (2.70, 1.0), (4.20, 0.0)]
    if l <= pts[0][0] or l >= pts[-1][0]:
        return 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= l <= x1:
            return y0 + (y1 - y0) * (l - x0) / (x1 - x0)


def f_V(x, c=0.25):
    """Concentric Hill branch (line 1240), x = v / v_max."""
    return (1 - x) / (1 + x / c)


def esc(t):
    return html.escape(t)


def rect(x, y, w, h, fill, stroke=None, sw=0.8, rx=0, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{st} {extra}/>'


def circ(x, y, r, fill, stroke=None, sw=0.8, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}"{st} {extra}/>'


def path(d, stroke, sw, fill="none", extra=""):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw:.2f}" {extra}/>'


def legend(s, x, y, items, size="label2", gap=22, cw=6.6):
    """One legend row. items = [(swatch_svg_fn(x, y), text)]; swatch drawn in a 14 x 10 box at (x, y-10)."""
    o = []
    for sw, txt in items:
        o.append(sw(x, y))
        o.append(H.label(s, x + 19, y, txt, size, I["secondary"]))
        x += 19 + len(txt) * cw + gap
    return "".join(o), x


def sw_rect(fill, stroke=None, op=1):
    return lambda x, y: rect(x, y - 10, 14, 10, fill, stroke, 0.8, 0, f'opacity="{op}"')


def sw_dot(fill, stroke=None):
    return lambda x, y: circ(x + 7, y - 5, 4.5, fill, stroke, 1.0)


def sw_line(col, w=2.5, dash=None):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return lambda x, y: f'<line x1="{x}" y1="{y-5}" x2="{x+14}" y2="{y-5}" stroke="{col}" stroke-width="{w}"{da}/>'


# ---------------------------------------------------------------- sarcomere (lifted from ex_tissue)
def sarcomere(cx, y, l, S, shade=True, heads=True, thick=True, row=13, th=6, kh=10, zh=48):
    """One sarcomere of length l (um) centred at (cx, y), S px per um. Returns (svg, Z x positions)."""
    X = lambda u: cx + u * S                         # noqa: E731
    zl, zr = -l / 2, l / 2
    tk = min(A_THICK, l)                             # below 1.6 um the thick filament is compressed
    heads_l, heads_r = (-tk / 2, -BARE / 2), (BARE / 2, tk / 2)
    thin_l, thin_r = (zl, zl + A_THIN), (zr - A_THIN, zr)
    band = row * 2
    o = []
    if shade:
        dbl = [(a0, a1) for a0, a1 in ((0, thin_l[1]), (thin_r[0], 0)) if a1 > a0]
        for (a0, a1), (h0, h1) in ((thin_l, heads_l), (thin_r, heads_r)):
            g0, g1 = max(a0, h0), min(a1, h1)
            for d0, d1 in dbl:
                if d0 <= g0 < d1:
                    g0 = d1
                if d0 < g1 <= d1:
                    g1 = d0
            if g1 > g0:
                o.append(rect(X(g0), y - band, (g1 - g0) * S, 2 * band, O["neural"], extra='opacity="0.16"'))
        for a0, a1 in dbl:
            o.append(rect(X(a0), y - band, (a1 - a0) * S, 2 * band, O["flag"], extra='opacity="0.35"'))
    for yy in (y - row, y + row):
        for a0, a1 in (thin_l, thin_r):
            o.append(rect(X(a0), yy - th / 2, (a1 - a0) * S, th, T["actin"][0], T["actin"][1], 0.8, th / 2))
    if thick:
        o.append(rect(X(-tk / 2), y - kh / 2, tk * S, kh, T["myosin"][0], T["myosin"][1], 0.8, kh / 2))
        if heads:
            for h0, h1 in (heads_l, heads_r):
                n = max(1, int((h1 - h0) / 0.06))
                for j in range(n + 1):
                    xx = X(h0 + j * (h1 - h0) / n)
                    sg = -1 if h1 <= 0 else 1                # heads lean away from the centre
                    o.append(f'<path d="M{xx:.1f},{y-kh/2:.1f} l{2.5*sg:.1f},-4 M{xx:.1f},{y+kh/2:.1f} l{2.5*sg:.1f},4" '
                             f'stroke="{T["myosin"][1]}" stroke-width="0.9"/>')
    zw = max(3.0, min(5.0, S * 0.04))
    for z in (zl, zr):
        o.append(rect(X(z) - zw / 2, y - zh / 2, zw, zh, T["zdisc"][0]))
    return "".join(o), (X(zl), X(zr))


def fmt_l(l):
    return f"{l:.2f}".rstrip("0").rstrip(".") if abs(l * 10 - round(l * 10)) > 1e-9 else f"{l:.1f}"


# ---------------------------------------------------------------- svg 9: overlap panels (port of ex_tissue)
def fig9():
    VB = (0, 0, 760, 500)
    s = H.Scale(VB[2], VB[3])
    S, cx = 128.0, 400.0
    panels = [(1.4, "① too short"), (2.7, "② optimal"), (3.45, "③ stretched"), (4.2, "④ too long")]
    o = []
    for i, (l, name) in enumerate(panels):
        y = 60 + i * 112
        body, (xl, xr) = sarcomere(cx, y, l, S)
        o.append(body)
        for z in (xl, xr):
            o.append(H.label(s, z, y + 40, "Z", "label2", I["secondary"], "middle"))
        o.append(H.label(s, 10, y - 4, name, "label"))
        o.append(H.label(s, 10, y + 15, f"ℓ = {fmt_l(l)} µm", "label2", I["secondary"]))
        o.append(H.label(s, 750, y + 5, f'f{H.sub("L", s)} = {f_L(l):.2f}', anchor="end"))
    ly = 488
    items = [(T["actin"][0], "thin filament (actin)"), (T["myosin"][0], "thick filament (myosin), heads as ticks"),
             (O["neural"], "productive overlap"), (O["flag"], "double overlap")]
    x = 10
    for col, txt in items:
        op = {O["neural"]: 0.35, O["flag"]: 0.6}.get(col, 1)
        o.append(f'<rect x="{x}" y="{ly-10}" width="14" height="10" fill="{col}" opacity="{op}"/>')
        o.append(H.label(s, x + 19, ly, txt, "label2", I["secondary"]))
        x += 26 + len(txt) * 6.6
    aria = ("Four sarcomere panels at 1.4, 2.7, 3.45 and 4.2 micrometres, drawn to scale. Thin filaments run 1.3 "
            "micrometres in from each Z-disc; the 1.6 micrometre thick filament sits at the centre with heads except in "
            "a 0.1 micrometre bare zone. At 1.4 micrometres the thick filament is compressed between the Z-discs. Green "
            "shading marks thin filament beside heads, orange marks thin filament past the centre. Length factor: 0.32, "
            "1.00, 0.50, 0.00.")
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


# ---------------------------------------------------------------- svg 11: sliding sarcomere + operating point (frames)
def fig11():
    VB = (0, 0, 760, 500)
    s = H.Scale(VB[2], VB[3])
    S, cx, ys = 128.0, 380.0, 92.0
    x0, x1, y0, y1 = 90, 730, 440, 260               # plot box
    L0, L1 = 1.0, 4.4
    X = lambda l: x0 + (l - L0) / (L1 - L0) * (x1 - x0)   # noqa: E731  one scale for ticks, curve, dot
    Y = lambda f: y0 - f / 1.1 * (y0 - y1)                # noqa: E731
    lens = [round(4.2 - 0.1 * k, 2) for k in range(27)]   # 4.2 -> 1.6 um
    dflt = lens.index(2.7)
    o = [H.label(s, 380, 22, "one sarcomere: the filaments slide, they never shorten", "label", I["primary"], "middle")]
    # plot (static)
    o.append(f'<rect x="{X(2.6):.2f}" y="{y1}" width="{X(2.7)-X(2.6):.2f}" height="{y0-y1}" fill="{O["neural"]}" opacity="0.12"/>')
    for f in (0.5, 1.0):
        o.append(H.line(s, x0, Y(f), x1, Y(f), GRID, "leader"))
    o.append(H.line(s, x0, y0, x1, y0, I["axis"], "axis"))
    o.append(H.line(s, x0, y0, x0, y1, I["axis"], "axis"))
    for f in (0.0, 0.5, 1.0):
        o.append(H.line(s, x0 - 5, Y(f), x0, Y(f), I["axis"], "leader"))
        o.append(H.label(s, x0 - 9, Y(f) + 4.5, f"{f:.1f}", "tick", I["secondary"], "end"))
    for l, txt in ((1.27, "1.27"), (1.6, "1.6"), (2.0, "2"), (2.7, "2.7"), (3.0, "3"), (4.0, "4"), (4.2, "4.2")):
        o.append(H.line(s, X(l), y0, X(l), y0 + 5, I["axis"], "leader"))
        o.append(H.label(s, X(l), y0 + 20, txt, "tick", I["secondary"], "middle"))
    o.append(H.label(s, (x0 + x1) / 2, y0 + 44, "sarcomere length ℓ (µm)", "label", I["primary"], "middle"))
    o.append(H.label(s, 30, (y0 + y1) / 2, f'f{H.sub("L", s)}(ℓ)', "label", I["primary"], "middle",
                     f'transform="rotate(-90 30 {(y0 + y1) / 2})"'))
    brk = [(1.27, 0.0), (1.60, 0.8), (2.60, 1.0), (2.70, 1.0), (4.20, 0.0)]
    pts = [(X(L0), Y(0))] + [(X(l), Y(f)) for l, f in brk] + [(X(L1), Y(0))]
    o.append(f'<polyline points="{" ".join(f"{a:.2f},{b:.2f}" for a, b in pts)}" fill="none" '
             f'stroke="{H.SERIES[0]}" stroke-width="{s(H.PX["curve"]):.2f}" stroke-linejoin="round"/>')
    o.append(H.label(s, X(2.65), Y(1.0) - 12, "plateau", "label2", I["secondary"], "middle"))
    # frames: thin filaments + Z-discs + overlap shading + operating point; thick filament stays (drawn after, on top)
    for k, l in enumerate(lens):
        body, (xl, xr) = sarcomere(cx, ys, l, S, thick=False)
        fr = [body]
        for z in (xl, xr):
            fr.append(H.label(s, z, ys + 42, "Z", "label2", I["secondary"], "middle"))
        fr.append(H.label(s, 380, ys + 74, f'ℓ = {l:.1f} µm,  f{H.sub("L", s, "label")} = {f_L(l):.2f}', "label",
                          I["primary"], "middle"))
        fr.append(f'<circle cx="{X(l):.2f}" cy="{Y(f_L(l)):.2f}" r="{s(6):.2f}" fill="{O["flag"]}" stroke="#fff" '
                  f'stroke-width="{s(1.5):.2f}"/>')
        o.append(H.frame(k, dflt, "".join(fr)))
    tk = []                                        # thick filament + heads: static, drawn over the frames
    Xs = lambda u: cx + u * S                      # noqa: E731
    tk.append(rect(Xs(-A_THICK / 2), ys - 5, A_THICK * S, 10, T["myosin"][0], T["myosin"][1], 0.8, 5))
    for h0, h1 in ((-A_THICK / 2, -BARE / 2), (BARE / 2, A_THICK / 2)):
        n = int((h1 - h0) / 0.06)
        sg = -1 if h1 <= 0 else 1
        for j in range(n + 1):
            xx = Xs(h0 + j * (h1 - h0) / n)
            tk.append(f'<path d="M{xx:.1f},{ys-5:.1f} l{2.5*sg:.1f},-4 M{xx:.1f},{ys+5:.1f} l{2.5*sg:.1f},4" '
                      f'stroke="{T["myosin"][1]}" stroke-width="0.9"/>')
    o.append("".join(tk))
    # legend
    lg, _ = legend(s, 60, 200, [(sw_rect(T["actin"][0], T["actin"][1]), "thin (actin), slides"),
                                (sw_rect(T["myosin"][0], T["myosin"][1]), "thick (myosin), fixed"),
                                (sw_rect(T["zdisc"][0]), "Z-disc"),
                                (sw_rect(O["neural"], None, 0.35), "productive overlap"),
                                (sw_rect(O["flag"], None, 0.6), "double overlap")], gap=16)
    o.append(lg)
    o.append(legend(s, 60, 224, [(sw_dot(O["flag"], "#fff"), "operating point on the curve below")], gap=16)[0])
    hv = [[round(X(l), 2), round(Y(f_L(l)), 2), f"ℓ = {l:.2f} µm, f = {f_L(l):.2f}"]
          for l in (L0 + i * 0.02 for i in range(int(round((L1 - L0) / 0.02)) + 1))]
    aria = ("Sarcomere drawn to scale with a slider: the thin actin filaments and Z-discs slide over the fixed 1.6 "
            "micrometre thick myosin filament as sarcomere length goes from 4.2 down to 1.6 micrometres in 0.1 "
            "micrometre steps. Below, an orange dot marks the operating point on the active length-tension curve. "
            "The still frame is at the optimal length 2.7 micrometres, where the force factor is 1.")
    extra = H.hover_attr([x0, y1, x1, y0], hv) + " " + H.frames_attr("ℓ (µm)", [f"{l:.1f}" for l in lens], dflt)
    return H.svg_open(VB, esc(aria), s, extra=extra) + "".join(o) + "</svg>"


# ---------------------------------------------------------------- shared small pieces
def fibre_bar(x1, y1, x2, y2, w, fill=None, stroke=None, sw=0.8, op=1.0):
    """A muscle fibre as a rounded bar from (x1, y1) to (x2, y2)."""
    fill, stroke = fill or T["muscle"][0], stroke or T["muscle"][1]
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    L = math.hypot(x2 - x1, y2 - y1)
    a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return (f'<rect x="{cx-L/2:.1f}" y="{cy-w/2:.1f}" width="{L:.1f}" height="{w:.1f}" rx="{w/2:.1f}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}" fill-opacity="{op}" transform="rotate({a:.2f} {cx:.1f} {cy:.1f})"/>')


def angle_arc(s, x, y, r, a0, a1, col=None):
    """Arc at (x, y) from angle a0 to a1 (degrees, maths sense: counter-clockwise, y up)."""
    col = col or O["geometry"]
    p0 = (x + r * math.cos(math.radians(a0)), y - r * math.sin(math.radians(a0)))
    p1 = (x + r * math.cos(math.radians(a1)), y - r * math.sin(math.radians(a1)))
    sweep = 0 if a1 > a0 else 1
    return path(f"M{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 0 {sweep} {p1[0]:.1f},{p1[1]:.1f}", col, s(H.PX["geom"]))


def dashed_arrow(s, p, x1, y1, x2, y2, meaning):
    return H.line(s, x1, y1, x2, y2, O[meaning], "force", H.DASH_LOA, extra=f'marker-end="url(#{p}a_{meaning})"')


def halo_line(s, x1, y1, x2, y2, w=6):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#fff" stroke-width="{s(w):.2f}"/>'


def th_p(s, size="label"):
    return "θ" + H.sub("p", s, size)


def F_fib(s, size="label"):
    return "F" + H.sub("fibre", s, size)


def neck(x1, y1, x2, y2, w=5):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{T["myosin"][1]}" '
            f'stroke-width="{w}" stroke-linecap="round"/>')


def ca():
    return "Ca²⁺"


def ellipse(cx, cy, rx, ry, fill, stroke=None, sw=1.0, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx}" ry="{ry}" fill="{fill}"{st} {extra}/>'


# ---------------------------------------------------------------- muscle as tissue (svg #50 idiom) and the InjuryMap calf
# the author (2026-10-12): muscle is one filled tissue region with fibre lines, never capsules or bars.
from m05.body import _read, art_image, inner_svg, wrap   # noqa: E402

# crop_art.py ../svg_paths/Leg_muscles.svg m05calf 715 230 965 1065 --drop "#Names, #Shadow, text" --png 0.4
CALF = (715, 230, 250, 835)                               # crop window, source user units


CALF_ID = "m5art_calf"                                    # page-global id: the art is embedded once per page


def SHARED_DEFS():
    """Page-level defs (apply_figs / preview_figs put them once, before the figures): the calf crop as #m5art_calf.
    Three figures <use> it, so the 67 KB art is on the page once, not three times."""
    art = inner_svg(_read("Leg_muscles_crop_m05calf.svg"))
    assert 'id="Names"' not in art and "<text" not in art
    return f'<g id="{CALF_ID}">{art_image("<svg>" + art + "</svg>", CALF)}</g>'


def calf_use(tf):
    return f'<use href="#{CALF_ID}" transform="{tf}"/>'


def calf_credit(s, x, y, n, what="schematic"):
    cr = H.ATTRIBUTION["by-sa"].format(author="InjuryMap", title="Leg muscles.svg",
                                       changes=f"Cropped, labels removed; {what} drawn for this course.")
    return H.credit(s, x, y, wrap(cr, n))


def tissue(s, pts, fill=None, stroke=None, sw=1.0, extra=""):
    """A closed muscle-tissue region."""
    return (f'<path d="M{" L".join(f"{x:.1f},{y:.1f}" for x, y in pts)} Z" fill="{fill or T["muscle"][0]}" '
            f'stroke="{stroke or T["muscle"][1]}" stroke-width="{s(sw):.2f}" stroke-linejoin="round" {extra}/>')


def fibre_line(s, x1, y1, x2, y2, op=0.55, w=0.8):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{T["muscle_dk"][1]}" '
            f'stroke-width="{s(w):.2f}" opacity="{op}"/>')


def muscle_grad(gid, x1, y1, x2, y2):
    """Fill along the fibres, pale where they join tendon (as the InjuryMap art does). Iso-lines are
    perpendicular to (x1, y1) -> (x2, y2)."""
    pale = "#e3c4b8"
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" '
            f'y2="{y2:.1f}"><stop offset="0" stop-color="{pale}"/><stop offset="0.2" stop-color="{T["muscle"][0]}"/>'
            f'<stop offset="0.8" stop-color="{T["muscle"][0]}"/><stop offset="1" stop-color="{pale}"/></linearGradient>')


def pennate_sheet(s, x0, x1, yt, ya, th, p, pitch=18.0):
    """Unipennate tissue between a tendon edge (y = yt) and an aponeurosis edge (y = ya < yt): one region whose
    fibres leave the tendon at theta, from x0..x1 on the tendon. Uses the gradient #{p}mg (see muscle_grad)."""
    run = (yt - ya) / math.tan(th)
    o = [f'<defs>{muscle_grad(p + "mg", 0, yt, 0, ya)}</defs>',
         tissue(s, [(x0, yt), (x1, yt), (x1 + run, ya), (x0 + run, ya)], fill=f"url(#{p}mg)")]
    xb = x0 + pitch / 2
    while xb < x1:
        o.append(fibre_line(s, xb, yt, xb + run, ya))
        xb += pitch
    return "".join(o)


def one_fibre(s, xi, yt, ya, th, p, hw=11.0):
    """The fibre whose force is resolved: a strip of the sheet, outlined, half-width hw along the tendon."""
    run = (yt - ya) / math.tan(th)
    return tissue(s, [(xi - hw, yt), (xi + hw, yt), (xi + hw + run, ya), (xi - hw + run, ya)], fill=f"url(#{p}mg)",
                  stroke=T["muscle_dk"][1], sw=1.6, extra='fill-opacity="0.45"')


# ---------------------------------------------------------------- svg 2: pennate muscle, angle and PCSA (opening figure)
def fig2():
    VB = (0, 0, 760, 352)
    s = H.Scale(VB[2], VB[3])
    p = "m5f2_"
    th = math.radians(25)
    xa, xb, cy, ry = 225.0, 675.0, 165.0, 96.0             # schematic belly: spindle from xa to xb, half-width ry

    def half_w(x):
        return ry * math.sin(math.pi * (x - xa) / (xb - xa)) ** 1.3 if xa < x < xb else 0.0
    o = [f'<defs>{H.markers(p, s)}{muscle_grad(p + "mg", xa, 0, xb, 0)}</defs>']
    # left: the real muscle (InjuryMap calf), scaled k; anchors are the art's own label points
    k, ox, oy = 0.3234, 18.0, 22.0
    A = lambda x, y: (ox + (x - CALF[0]) * k, oy + (y - CALF[1]) * k)   # noqa: E731
    o.append(calf_use(f"translate({ox - CALF[0] * k:.2f} {oy - CALF[1] * k:.2f}) scale({k})"))
    for (ax, ay), ty, t1, t2 in ((A(830, 488), 100, "gastrocnemius", "a pennate calf muscle"),
                                 (A(767, 872), 226, "Achilles tendon", "")):
        o.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="{s(2.5):.1f}" fill="{I["primary"]}"/>')
        o.append(H.line(s, ax, ay, 107, ty - 4, I["primary"]))
        o.append(H.label(s, 110, ty, t1))
        if t2:
            o.append(H.label(s, 110, ty + 17, t2, "label2", I["secondary"]))
    # right: schematic bipennate belly, fibres leave the central tendon at theta_p (svg #50 idiom)
    top = [(x, cy - half_w(x)) for x in (xa + i * (xb - xa) / 48 for i in range(49))]
    o.append(tissue(s, top + [(x, 2 * cy - y) for x, y in top[::-1]], fill=f"url(#{p}mg)"))
    for side in (-1, 1):
        for x0 in range(int(xa) + 26, int(xb) - 10, 22):
            y0 = cy + side * 7
            t = 0.0
            while half_w(x0 - (t + 1) * math.cos(th)) > abs(y0 + side * (t + 1) * math.sin(th) - cy):
                t += 1
            if t > 8:
                o.append(fibre_line(s, x0, y0, x0 - t * math.cos(th), y0 + side * t * math.sin(th), 0.75, 1.0))
    o.append(rect(215, cy - 7, 530, 14, T["tendon"][0], T["tendon"][1], 1.0, 7))
    # anatomical cut (perpendicular to the tendon) and PCSA cut (perpendicular to the fibres)
    xc = 310.0
    o.append(H.line(s, xc, cy - half_w(xc) - 12, xc, cy + half_w(xc) + 12, O["dim"], "ref", H.DASH_REF))
    px, py = 435.0, 115.0
    nx, ny = math.sin(th), math.cos(th)                  # unit normal to the upper fibres
    o.append(H.line(s, px - 62 * nx, py - 62 * ny, px + 50 * nx, py + 50 * ny, O["geometry"], "geom", H.DASH_REF))
    # one fibre force and its tendon component (on the fibre that leaves the tendon at xi)
    xi = xa + 26 + 22 * 14
    yi, Lf = cy - 7, 130.0
    tip = (xi - Lf * math.cos(th), yi - Lf * math.sin(th))
    o.append(halo_line(s, xi, yi, *tip))
    o.append(H.arrow(s, p, xi, yi, *tip, "force"))
    o.append(halo_line(s, xi, cy, tip[0], cy))
    o.append(H.arrow(s, p, xi, cy, tip[0], cy, "force"))
    o.append(angle_arc(s, xi, yi, 52, 180, 155))
    o.append(H.label(s, xi - 64, yi - 9, th_p(s), fill=O["geometry"], anchor="end"))
    o.append(H.label(s, tip[0] + 8, tip[1] - 8, F_fib(s), fill=O["force"]))
    o.append(H.label(s, tip[0] + 8, cy + 28, F_fib(s) + " cos " + th_p(s), fill=O["force"]))
    o.append(H.label(s, 745, cy + 26, "tendon", anchor="end"))
    o.append(H.label(s, 745, cy + 43, "(line of action)", "label2", I["secondary"], "end"))
    o.append(H.label(s, 650, 52, "muscle fibres"))
    o.append(H.line(s, 648, 56, 545, 106, T["muscle_dk"][1], "leader"))
    o.append(H.label(s, px, 28, "PCSA: cut perpendicular to the fibres", fill=O["geometry"], anchor="middle"))
    o.append(H.label(s, xc, 282, "anatomical cut: perpendicular to the tendon", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 610, 282, "schematic of a bipennate muscle", "label2", I["secondary"], "middle"))
    lg, _ = legend(s, 18, 308, [(sw_rect(T["muscle"][0], T["muscle"][1]), "muscle fibres"),
                                (sw_rect(T["tendon"][0], T["tendon"][1]), "tendon"),
                                (sw_line(O["force"]), "fibre force and its tendon part"),
                                (sw_line(O["geometry"], 2, "6 4"), "PCSA cut")], gap=18)
    o.append(lg)
    o.append(calf_credit(s, 18, 328, 110))
    aria = ("Left: InjuryMap art of a calf, with the gastrocnemius, a pennate muscle, and the Achilles tendon marked. "
            "Right: a schematic bipennate muscle. Fibres leave a central tendon at the pennation angle theta p, 25 "
            "degrees here. One fibre force F fibre is drawn along its fibre, and its part along the tendon, F fibre cos "
            "theta p. A blue dashed cut perpendicular to the fibres marks the physiological cross-section (PCSA); a grey "
            "dashed cut perpendicular to the tendon marks the anatomical cross-section, which is not the PCSA.")
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


# ---------------------------------------------------------------- svg 5: hierarchy, whole muscle to sarcomere (Fig. 3)
def fig5():
    VB = (0, 0, 760, 300)
    s = H.Scale(VB[2], VB[3])
    p = "m5f5_"
    cy = 110
    cxs = [76 + 152 * i for i in range(5)]
    titles = ["whole muscle", "fascicles", "muscle fibre", "myofibril", "sarcomere"]
    notes = [("calf muscle:", "gastrocnemius"), ("bundles of fibres", "≈ 0.1–1 mm"),
             ("one cell, 10–100 µm", "across, striated"), ("sarcomeres", "end to end"),
             ("ℓ ≈ 2.7 µm: the", "contractile unit")]
    fib = (f'<linearGradient id="{p}fib" x1="0" y1="0" x2="0" y2="1">'
           + "".join(f'<stop offset="{o_}" stop-color="{c}"/>' for o_, c in
                     ((0, T["muscle_dk"][0]), (0.35, T["muscle"][0]), (0.5, "#d99a96"), (0.7, T["muscle"][0]),
                      (1, T["muscle_dk"][1])))
           + "</linearGradient>")
    # whole muscle: the InjuryMap calf, upright, scale k1; fascicles: art window `win` magnified k2 in a clipped box
    k1, oy = 164 / CALF[3], 28.0
    ox = cxs[0] - CALF[2] / 2 * k1
    win = (790, 870, 420, 540)                             # X0, X1, Y0, Y1 in art units
    k2 = 96 / (win[3] - win[2])
    bw2, bh2 = k2 * (win[1] - win[0]), 96.0
    bx2, by2 = cxs[1] - bw2 / 2, cy - bh2 / 2
    o = [f'<defs>{fib}</defs>']
    for cx, t, (n1, n2) in zip(cxs, titles, notes):
        o.append(H.label(s, cx, 20, t, "label", I["primary"], "middle"))
        o.append(H.label(s, cx, 214, n1, "label2", I["secondary"], "middle"))
        o.append(H.label(s, cx, 230, n2, "label2", I["secondary"], "middle"))
    o.append(calf_use(f"translate({ox - CALF[0] * k1:.2f} {oy - CALF[1] * k1:.2f}) scale({k1:.4f})"))
    # crop_art.py ../svg_paths/Leg_muscles.svg m05fasc 790 420 870 540 --drop "#Names, #Shadow, text" --png 0.4
    fasc = art_image("<svg>" + inner_svg(_read("Leg_muscles_crop_m05fasc.svg")) + "</svg>",
                     (win[0], win[2], win[1] - win[0], win[3] - win[2]))
    o.append(f'<g transform="translate({bx2 - win[0] * k2:.2f} {by2 - win[2] * k2:.2f}) scale({k2:.4f})">{fasc}</g>')
    o.append(rect(bx2, by2, bw2, bh2, "none", T["muscle"][1], 1.0))
    zoom = [(ox + (win[0] - CALF[0]) * k1, oy + (win[2] - CALF[1]) * k1, (win[1] - win[0]) * k1, (win[3] - win[2]) * k1)]
    zoom.append((cxs[1] + 4, cy - 6, 8, 12))
    c = cxs[2]                                            # fibre: a striated cylinder, nuclei at its surface, cut end
    o.append(rect(c - 52, cy - 16, 100, 32, f"url(#{p}fib)", T["muscle"][1], 1.0, 3))
    for k in range(-46, 44, 5):
        o.append(H.line(s, c + k, cy - 15, c + k, cy + 15, T["muscle_dk"][1], "leader", extra='opacity="0.45"'))
    for nx_ in (-30, 6):
        o.append(ellipse(c + nx_, cy - 10, 6, 2.6, "#7a3a44", None, extra='opacity="0.8"'))
    o.append(ellipse(c + 48, cy, 7, 16, "#e8b4ae", T["muscle"][1], 1.0))
    for j in range(-3, 4):                                # myofibrils seen end-on in the cut face
        o.append(circ(c + 48 + (1.6 if j % 2 else -1.6), cy + j * 4, 1.5, T["muscle_dk"][0]))
    zoom.append((c + 41, cy - 7, 14, 14))
    c = cxs[3]                                            # myofibril: three sarcomeres in series
    for k in (-1, 0, 1):
        body, _ = sarcomere(c + k * 40.5, cy, 2.7, 15.0, shade=False, heads=False, row=5, th=2.5, kh=4, zh=18)
        o.append(body)
    zoom.append((c - 21, cy - 12, 42, 24))
    c = cxs[4]                                            # sarcomere at rest length, to scale
    body, (xl, xr) = sarcomere(c, cy, 2.7, 50.0, shade=False, heads=True, row=11, th=5, kh=8, zh=40)
    o.append(body)
    for z in (xl, xr):
        o.append(H.label(s, z, cy + 38, "Z", "label2", I["secondary"], "middle"))
    nxt = [(bx2, by2, by2 + bh2), (cxs[2] - 52, cy - 16, cy + 16), (cxs[3] - 64, cy - 11, cy + 11),
           (cxs[4] - 70, cy - 24, cy + 24)]
    for (bx, by, bw, bh), (tx, ty0, ty1) in zip(zoom, nxt):
        o.append(rect(bx, by, bw, bh, "none", I["primary"], 1.0))
        o.append(H.line(s, bx + bw, by, tx, ty0, I["rule"], "leader", (3, 3)))
        o.append(H.line(s, bx + bw, by + bh, tx, ty1, I["rule"], "leader", (3, 3)))
    lg, _ = legend(s, 18, 260, [(sw_rect(T["muscle"][0], T["muscle"][1]), "muscle tissue"),
                                (sw_rect(T["actin"][0], T["actin"][1]), "thin filament (actin)"),
                                (sw_rect(T["myosin"][0], T["myosin"][1]), "thick filament (myosin)"),
                                (sw_rect(T["zdisc"][0]), "Z-disc")], gap=16)
    o.append(lg)
    o.append(calf_credit(s, 18, 280, 140, "fibre and filaments"))
    aria = ("Zoom cascade through the muscle hierarchy, left to right: a whole muscle, the calf's gastrocnemius (InjuryMap "
            "art); a magnified window of the same art showing its "
            "fascicles, bundles of fibres; one striated muscle fibre (10 to 100 micrometres across) with nuclei at its "
            "surface and myofibrils seen end-on in its cut face; a myofibril (sarcomeres end to end); and one sarcomere "
            "at 2.7 micrometres drawn to scale: thin actin filaments from the two Z-discs overlap the central thick "
            "myosin filament.")
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


# ---------------------------------------------------------------- svg 6: unipennate force triangle (Fig. 4)
def fig6():
    VB = (0, 0, 760, 330)
    s = H.Scale(VB[2], VB[3])
    p = "m5f6_"
    th = math.radians(25)
    yt, ya = 250.0, 62.0                                    # tendon top edge, aponeurosis bottom edge
    run = (yt - ya) / math.tan(th)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    xi = 300.0                                              # the last fibre: its force triangle sits in free space
    o.append(pennate_sheet(s, 40, xi - 11, yt, ya, th, p))
    o.append(one_fibre(s, xi, yt, ya, th, p))
    o.append(rect(30, yt, 700, 18, T["tendon"][0], T["tendon"][1], 1.0, 9))
    o.append(rect(40 + run - 20, ya - 16, 730 - (40 + run - 20), 16, T["tendon"][0], T["tendon"][1], 1.0, 8))
    Lf = 190.0
    tip = (xi + Lf * math.cos(th), yt - Lf * math.sin(th))
    o.append(H.arrow(s, p, xi, yt, *tip, "force"))
    o.append(H.arrow(s, p, xi, yt, tip[0], yt, "force"))
    o.append(dashed_arrow(s, p, tip[0], yt, tip[0], tip[1] + 2, "force"))
    o.append(angle_arc(s, xi, yt, 56, 0, 25))
    o.append(H.label(s, xi + 62, yt - 8, th_p(s), fill=O["geometry"]))
    o.append(H.label(s, xi + 108, 224, F_fib(s), fill=O["force"]))
    o.append(H.label(s, xi, yt + 42, F_fib(s) + " cos " + th_p(s) + ": pulls the bone", fill=O["force"]))
    o.append(H.label(s, tip[0] + 10, 214, F_fib(s) + " sin " + th_p(s), fill=O["force"]))
    o.append(H.label(s, tip[0] + 10, 232, "wasted against the casing", "label2", I["secondary"]))
    o.append(H.label(s, 730, yt + 42, "tendon (line of action)", anchor="end"))
    o.append(H.label(s, 730, ya - 24, "aponeurosis", anchor="end"))
    o.append(H.label(s, 30, 140, "muscle fibres", "label"))
    o.append(H.line(s, 130, 144, 219, 171, T["muscle_dk"][0], "leader"))
    o.append(H.label(s, 30, 30, f"at {th_p(s, 'label2')} = 25°, cos {th_p(s, 'label2')} = 0.91: each fibre delivers 9% less "
                     "along the tendon", "label2", I["secondary"]))
    lg, _ = legend(s, 30, 318, [(sw_rect(T["muscle"][0], T["muscle"][1]), "muscle fibres"),
                                (sw_rect(T["tendon"][0], T["tendon"][1]), "tendon and aponeurosis"),
                                (sw_line(O["force"]), "fibre force and its parts (dashed: wasted part)")], gap=18)
    o.append(lg)
    aria = ("A unipennate muscle: fibres run at the pennation angle theta p, 25 degrees, between the tendon along the "
            "bottom and the aponeurosis above. For one fibre, the fibre force is resolved into F fibre cos theta p along "
            "the tendon, which pulls the bone, and a dashed perpendicular part F fibre sin theta p, which is wasted. At "
            "25 degrees cos theta p is 0.91.")
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


# ---------------------------------------------------------------- svg 7: crossbridge cycle (Fig. 5)
def xb_panel(s, cx, cy, state):
    o = [rect(cx - 90, cy - 40, 180, 12, T["actin"][0], T["actin"][1], 0.8, 6),
         rect(cx - 90, cy + 22, 180, 14, T["myosin"][0], T["myosin"][1], 0.8, 7)]
    head = {"attached": (cx + 16, cy - 21), "detached": (cx + 18, cy - 4), "primed": (cx - 18, cy - 8),
            "stroke": (cx + 16, cy - 21)}[state]
    if state == "stroke":                                 # ghost of the primed head before the stroke
        o.append(ellipse(cx - 16, cy - 21, 11, 7.5, "none", T["myosin"][1], 1.0, 'stroke-dasharray="3 2"'))
        o.append(path(f"M{cx-10},{cy-6} Q{cx},{cy-12} {cx+8},{cy-8}", I["secondary"], 1.0,
                      extra='marker-end="url(#m5f7_a_dim)"'))
    o.append(neck(cx, cy + 22, head[0], head[1] + 5))
    o.append(ellipse(head[0], head[1], 11, 7.5, T["myosin"][0], T["myosin"][1], 1.0))
    tag = {"detached": "ATP", "primed": "ADP·Pᵢ", "stroke": "ADP"}.get(state)
    if tag:
        w = 12 + len(tag) * 7.2
        tx = head[0] + 16
        o.append(rect(tx, head[1] - 9, w, 18, BOX, I["rule"], 0.8, 4))
        o.append(H.label(s, tx + w / 2, head[1] + 4.5, tag, "label2", I["primary"], "middle"))
    return "".join(o)


def fig7():
    VB = (0, 0, 760, 470)
    s = H.Scale(VB[2], VB[3])
    p = "m5f7_"
    L, R, top, bot = 160, 580, 100, 300
    o = [f'<defs>{H.markers(p, s)}</defs>']
    panels = [(L, top, "attached", "① attached", "bound to actin, awaiting ATP"),
              (R, top, "detached", "② detached", "ATP bound, head released"),
              (R, bot, "primed", "③ primed", "head re-cocked"),
              (L, bot, "stroke", "④ power stroke", "head pivots: thin filament moves ≈ 10 nm →")]
    for cx, cy, st, name, sub_ in panels:
        o.append(xb_panel(s, cx, cy, st))
        o.append(H.label(s, cx, cy + 60, name, "label", I["primary"], "middle"))
        o.append(H.label(s, cx, cy + 78, sub_, "label2", I["secondary"], "middle"))
    o.append(H.arrow(s, p, 262, top - 6, 470, top - 6, "dim", w="ref"))
    o.append(H.label(s, 366, top - 16, "ATP binds", "label", I["primary"], "middle"))
    o.append(H.arrow(s, p, R, top + 92, R, bot - 50, "dim", w="ref"))
    o.append(H.label(s, R + 12, 214, "hydrolysis:", "label", I["primary"]))
    o.append(H.label(s, R + 12, 232, "ATP → ADP + Pᵢ", "label2", I["secondary"]))
    o.append(H.arrow(s, p, 470, bot - 6, 262, bot - 6, "dim", w="ref"))
    o.append(H.label(s, 366, bot - 16, "Pᵢ released: power stroke", "label", I["primary"], "middle"))
    o.append(H.arrow(s, p, L, bot - 50, L, top + 92, "dim", w="ref"))
    o.append(H.label(s, L + 12, 224, "ADP released", "label", I["primary"]))
    o.append(H.label(s, 370, 196, "1 ATP", "label", I["primary"], "middle", 'font-weight="bold"'))
    o.append(H.label(s, 370, 214, "per cycle", "label", I["primary"], "middle", 'font-weight="bold"'))
    o.append(H.label(s, 750, 22, "sarcomere centre →", "label2", I["secondary"], "end"))
    o.append(H.label(s, 380, 420, "No ATP: the heads cannot let go and stay in state ①. This is rigor mortis.", "label",
                     I["primary"], "middle", 'font-style="italic"'))
    lg, _ = legend(s, 110, 456, [(sw_rect(T["actin"][0], T["actin"][1]), "thin filament (actin)"),
                                 (sw_rect(T["myosin"][0], T["myosin"][1]), "thick filament and head (myosin)"),
                                 (sw_rect(BOX, I["rule"]), "bound nucleotide")], gap=18)
    o.append(lg)
    aria = ("The four-state crossbridge cycle as a ring. State 1, attached: myosin head bound to actin, awaiting ATP. "
            "ATP binds and the head releases (state 2, detached). Hydrolysis of ATP to ADP plus phosphate re-cocks the "
            "head (state 3, primed). Phosphate release drives the power stroke (state 4): the head pivots and moves the "
            "thin filament about 10 nanometres toward the sarcomere centre. ADP release returns it to state 1. One ATP "
            "per cycle; with no ATP the heads stay attached, which is rigor mortis.")
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


# ---------------------------------------------------------------- thin filament (actin beads) used by svg 12 and 14
def actin_beads(x0, x1, y, r=7.0):
    o = []
    n = int((x1 - x0) / (2 * r))
    for i in range(n):
        o.append(circ(x0 + i * 2 * r, y - r * 0.85, r, T["actin"][0], T["actin"][1], 0.8))
        o.append(circ(x0 + r + i * 2 * r, y + r * 0.85, r, T["actin"][0], T["actin"][1], 0.8))
    return "".join(o)


def ca_dot(x, y, r=3.6):
    """Ca2+ ion: fluid token (the author, 2026-10-12: ions are never neural green)."""
    return circ(x, y, r + 0.6, T["fluid"][0], T["fluid"][1], 1.0)


CA_COL = T["fluid"][1]                                    # Ca2+ flux arrows: fluid outline colour


def ca_marker(p, s):
    """Slim head for Ca2+ flux arrows (house.markers has no fluid meaning). Id: {p}a_ca."""
    sz = s(H.PX["head_force"])
    return (f'<marker id="{p}a_ca" markerUnits="userSpaceOnUse" markerWidth="{sz*1.2:.2f}" markerHeight="{sz*0.8:.2f}" '
            f'refX="{sz*0.95:.2f}" refY="{sz*0.4:.2f}" orient="auto-start-reverse">'
            f'<path d="M0,0 L{sz:.2f},{sz*0.4:.2f} L0,{sz*0.8:.2f} Z" fill="{CA_COL}"/></marker>')


def ca_arrow(s, p, x1, y1, x2, y2, w="force"):
    return H.line(s, x1, y1, x2, y2, CA_COL, w, extra=f'marker-end="url(#{p}a_ca)"')


def sw_ca(x, y):
    return ca_dot(x + 7, y - 5, 4)


# ---------------------------------------------------------------- svg 12: excitation-contraction coupling (Fig. 9)
def fig12():
    VB = (0, 0, 760, 500)
    s = H.Scale(VB[2], VB[3])
    p = "m5f12_"
    ym, tl, tr, tb = 112, 380, 396, 330                  # sarcolemma y, T-tubule walls, tubule bottom
    o = [f'<defs>{H.markers(p, s)}{ca_marker(p, s)}</defs>']
    # motor-neuron terminal (nerve tissue) with ACh in the cleft
    o.append(path("M20,14 C60,20 90,30 120,40", T["nerve"][1], 9.0))
    o.append(path("M20,14 C60,20 90,30 120,40", T["nerve"][0], 6.0))
    o.append(ellipse(160, 64, 56, 28, T["nerve"][0], T["nerve"][1], 1.2))
    for vx, vy in ((132, 58), (152, 70), (174, 56), (190, 72), (146, 50)):
        o.append(circ(vx, vy, 4, BOX, T["nerve"][1], 0.8))
    for k in range(6):
        o.append(circ(122 + k * 15, 100, 2.6, I["secondary"]))
    # sarcolemma dipping into the T-tubule
    o.append(path(f"M20,{ym} H{tl} V{tb} H{tr} V{ym} H740", I["rule"], 4.0))
    # SR sacs with stored calcium
    for x0 in (230, 428):
        o.append(rect(x0, 190, 118, 120, BOX, I["rule"], 1.2, 14))
    for cx_, cy_ in ((262, 220), (300, 246), (256, 276), (318, 288), (282, 300), (470, 222), (508, 252), (462, 282),
                     (520, 290), (486, 236)):
        o.append(ca_dot(cx_, cy_))
    # triad: DHPR in the tubule wall, tethered to RyR in the SR wall
    for dx, rx_ in ((tl - 15, 342), (tr + 4, 423)):
        o.append(H.line(s, min(dx, rx_) + 11, 206, max(dx, rx_), 206, I["primary"], "ref"))
        o.append(rect(dx, 198, 11, 16, I["primary"], None, 0, 2))
        o.append(rect(rx_, 196, 11, 20, "#fff", I["primary"], 1.2, 2))
    # action potential along the sarcolemma and down the tubule
    o.append(H.arrow(s, p, 236, ym + 14, 366, ym + 14, "dim", w="ref"))
    o.append(H.arrow(s, p, 410, ym + 14, 560, ym + 14, "dim", w="ref"))
    o.append(H.arrow(s, p, (tl + tr) / 2, ym + 10, (tl + tr) / 2, tb - 8, "dim", w="ref"))
    # calcium release (RyR) and re-uptake (SERCA)
    for k, (cx_, cy_) in enumerate(((340, 330), (318, 352), (346, 372), (300, 386), (330, 396))):
        o.append(ca_dot(cx_, cy_))
    o.append(ca_arrow(s, p, 362, 222, 362, 400))
    o.append(circ(500, 310, 11, "#fff", I["primary"], 1.2))
    o.append(path("M540,392 Q538,346 508,320", CA_COL, s(H.PX["leader"]) * 1.4,
                  extra=f'marker-end="url(#{p}a_ca)"'))
    # thin filament with troponin, calcium binding
    o.append(actin_beads(40, 720, 430))
    for tx in (150, 330, 510, 690):
        o.append(ellipse(tx, 418, 9, 6, I["secondary"], "#fff", 0.8))
        o.append(ca_dot(tx + 2, 408, 3.2))
    # numbered labels
    o.append(H.label(s, 226, 48, "① motor-neuron terminal", "label"))
    o.append(H.label(s, 226, 66, "releases acetylcholine (ACh)", "label2", I["secondary"]))
    o.append(H.label(s, 226, 98, "ACh onto the motor end-plate", "label2", I["secondary"]))
    o.append(H.label(s, 740, ym - 8, "sarcolemma", "label2", I["secondary"], "end"))
    o.append(H.label(s, 30, ym + 30, "② muscle action potential", "label"))
    o.append(H.label(s, 30, ym + 48, "along the sarcolemma, down the T-tubule", "label2", I["secondary"]))
    o.append(H.label(s, tr + 6, tb + 4, "T-tubule", "label2", I["secondary"]))
    o.append(H.label(s, 452, 160, "③ triad: DHPR (voltage sensor) pulls", "label"))
    o.append(H.label(s, 452, 178, "the RyR release channel open", "label"))
    o.append(H.line(s, 450, 165, tr + 10, 197, I["primary"], "leader"))
    o.append(H.label(s, 560, 214, "sarcoplasmic reticulum", "label2", I["secondary"]))
    o.append(H.label(s, 560, 230, f"(SR): {ca()} store", "label2", I["secondary"]))
    o.append(H.label(s, 290, 362, f"{ca()} floods", "label", I["primary"], "end"))
    o.append(H.label(s, 290, 380, "the cytosol", "label", I["primary"], "end"))
    o.append(H.label(s, 556, 346, "④ SERCA pump spends ATP", "label"))
    o.append(H.label(s, 556, 364, f"to return {ca()} to the SR", "label2", I["secondary"]))
    o.append(H.label(s, 40, 466, f"⑤ {ca()} binds troponin on the thin filament (next figure)", "label"))
    lg, _ = legend(s, 40, 492, [(sw_ca, f"{ca()} ion"), (sw_line(CA_COL, 1.4), f"{ca()} flow"),
                                (sw_rect(T["nerve"][0], T["nerve"][1]), "nerve"),
                                (sw_rect(BOX, I["rule"]), "SR"), (sw_rect(I["primary"]), "DHPR"),
                                (sw_rect("#fff", I["primary"]), "RyR, SERCA"),
                                (sw_rect(T["actin"][0], T["actin"][1]), "actin"),
                                (sw_rect(I["secondary"]), "troponin")], gap=14)
    o.append(lg)
    aria = ("Excitation-contraction coupling, numbered 1 to 5. 1: the motor-neuron terminal releases acetylcholine onto "
            "the motor end-plate. 2: a muscle action potential runs along the sarcolemma and down a T-tubule. 3: at the "
            "triad the voltage sensor DHPR, tethered to the RyR release channel of the sarcoplasmic reticulum, pulls it "
            "open and calcium floods the cytosol. 4: the SERCA pump spends ATP to return calcium to the SR. 5: calcium "
            "binds troponin on the thin filament.")
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


# ---------------------------------------------------------------- svg 14: calcium switch on the thin filament (Fig. 10)
def tm_path(x0, x1, y, amp=1.0):
    pts = [(x, y + amp * math.sin((x - x0) / 28.0)) for x in range(int(x0), int(x1) + 1, 6)]
    return "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts)


def fig14():
    VB = (0, 0, 760, 440)
    s = H.Scale(VB[2], VB[3])
    p = "m5f14_"
    o = [f'<defs>{H.markers(p, s)}{ca_marker(p, s)}</defs>']
    tan = T["bone"][1]
    for k, cy in enumerate((110, 300)):
        on = k == 1
        o.append(actin_beads(60, 690, cy))
        sites = [96 + 70 * i for i in range(9)]
        for sx in sites:                                   # myosin-binding sites on the lower face
            o.append(rect(sx - 5, cy + 12, 10, 4, O["flag"], None, 0, 1))
        ytm = cy + 4 if on else cy + 14                    # tropomyosin: over the sites, or rolled into the groove
        o.append(path(tm_path(52, 694, ytm), tan, 6.0, extra='stroke-linecap="round"'))
        for tx in (201, 446, 621):
            o.append(ellipse(tx, ytm, 10, 7, I["secondary"], "#fff", 0.8))
            if on:
                o.append(ca_dot(tx - 5, ytm - 10, 3.4))
                o.append(ca_dot(tx + 6, ytm - 11, 3.4))
        hx = sites[4]
        o.append(rect(hx - 70, cy + 66, 140, 12, T["myosin"][0], T["myosin"][1], 0.8, 6))
        head_y = cy + 22 if on else cy + 36
        o.append(neck(hx - 10, cy + 66, hx, head_y + 6))
        o.append(ellipse(hx, head_y, 11, 7.5, T["myosin"][0], T["myosin"][1], 1.0))
        name = f"② activated: {ca()} bound" if on else f"① relaxed: no {ca()}"
        sub_ = ("tropomyosin rolls into the groove: the sites are exposed" if on
                else "tropomyosin lies over the binding sites: no force")
        o.append(H.label(s, 40, cy - 52, name, "label"))
        o.append(H.label(s, 40, cy - 34, sub_, "label2", I["secondary"]))
        o.append(H.label(s, hx + 80, cy + 46, "cross-bridge forms" if on else "myosin head blocked", "label",
                         I["primary"]))
        o.append(H.line(s, hx + 78, cy + 42, hx + 14, head_y + 2, I["primary"], "leader"))
    o.append(ca_arrow(s, p, 725, 150, 725, 240))
    o.append(H.label(s, 718, 200, f"+ {ca()}", "label", I["primary"], "end"))
    lg, _ = legend(s, 40, 428, [(sw_rect(T["actin"][0], T["actin"][1]), "actin"),
                                (sw_line(tan, 5), "tropomyosin"),
                                (sw_rect(I["secondary"]), "troponin"),
                                (sw_rect(O["flag"]), "binding site"),
                                (sw_ca, f"{ca()} ion"),
                                (sw_rect(T["myosin"][0], T["myosin"][1]), "myosin head")], gap=16)
    o.append(lg)
    aria = ("Two panels of the thin filament. Top, relaxed with no calcium: the tropomyosin strand lies over the "
            "myosin-binding sites on actin, held by troponin, so the myosin head is blocked. Bottom, activated: calcium "
            "binds troponin, tropomyosin rolls into the actin groove, the orange binding sites are exposed, and the "
            "myosin head forms a cross-bridge.")
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


# ---------------------------------------------------------------- svg 17: motor unit (Fig. 13)
def fig17():
    VB = (0, 0, 760, 340)
    s = H.Scale(VB[2], VB[3])
    small, large = H.SERIES[1], H.SERIES[0]
    rows = [62 + 27 * i for i in range(9)]
    own = {1: small, 4: small, 7: small}                   # interdigitated: small unit on rows 1, 4, 7
    o = [rect(30, 56, 120, 230, BOX, I["rule"], 1.2, 30)]
    o.append(H.label(s, 90, 46, "spinal cord", "label2", I["secondary"], "middle"))
    for i, y in enumerate(rows):
        o.append(rect(452, y - 10, 280, 20, T["muscle"][0], T["muscle"][1], 0.8, 10))
    o.append(H.label(s, 592, 44, "muscle fibres", "label2", I["secondary"], "middle"))
    for (sx, sy, r, col, bx, by) in ((90, 110, 9, small, 400, 196), (90, 222, 16, large, 400, 152)):
        for dy in (-1, 0, 1):
            o.append(H.line(s, sx - r, sy, sx - r - 14, sy + dy * 10, col, "geom"))
        o.append(path(f"M{sx+r},{sy} C{sx+150},{sy} {bx-130},{by} {bx},{by}", col, s(H.PX["curve"])))
        o.append(circ(sx, sy, r, T["nerve"][0], col, 2.0))
        for i, y in enumerate(rows):
            if own.get(i, large) == col:
                o.append(path(f"M{bx},{by} L{440},{y} L{452},{y}", col, s(1.6)))
                o.append(circ(456, y, 4, col, "#fff", 1.0))
    o.append(H.label(s, 120, 96, "small α-motoneuron", "label", small))
    o.append(H.label(s, 120, 270, "large α-motoneuron", "label", large))
    o.append(H.label(s, 236, 128, "one axon, 3 fibres", "label2", I["secondary"]))
    o.append(H.label(s, 236, 214, "one axon, 6 fibres", "label2", I["secondary"]))
    lg, _ = legend(s, 30, 328, [(sw_line(small), "small motor unit"), (sw_line(large), "large motor unit"),
                                (sw_rect(T["muscle"][0], T["muscle"][1]), "muscle fibre"),
                                (lambda x, y: circ(x + 4, y - 5, 4, small, "#fff", 1.0) + circ(x + 13, y - 5, 4, large, "#fff", 1.0),
                                 "  nerve terminal (end-plate)"),
                                (sw_rect(T["nerve"][0], T["nerve"][1]), "cell body")], gap=14)
    o.append(lg)
    aria = ("Two motor units. A small and a large alpha-motoneuron sit in the spinal cord. Each sends one axon that "
            "branches to its own fibres: the small unit to 3 fibres, the large unit to 6. Their fibres are interdigitated "
            "through the muscle, and each branch ends at a nerve terminal on its fibre.")
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


# ---------------------------------------------------------------- svg 24: calcium in fast, out slow (Fig. 20)
def fig24():
    VB = (0, 0, 760, 300)
    s = H.Scale(VB[2], VB[3])
    p = "m5f24_"
    o = [f'<defs>{H.markers(p, s)}{ca_marker(p, s)}</defs>']
    o.append(rect(30, 46, 220, 200, BOX, I["rule"], 1.2, 14))
    o.append(H.line(s, 250, 46, 250, 246, I["rule"], "axis"))
    for cx_, cy_ in ((70, 90), (120, 120), (90, 170), (160, 80), (180, 150), (70, 220), (140, 210), (210, 190),
                     (110, 70), (200, 110)):
        o.append(ca_dot(cx_, cy_))
    o.append(H.label(s, 140, 34, f"sarcoplasmic reticulum ({ca()} store)", "label2", I["secondary"], "middle"))
    # fast: open channel, thick shaft
    o.append(rect(243, 78, 14, 26, "#fff", I["primary"], 1.2, 3))
    o.append(f'<line x1="262" y1="91" x2="520" y2="91" stroke="{CA_COL}" stroke-width="{s(7):.2f}" '
             f'marker-end="url(#{p}a_ca)"/>')
    o.append(H.label(s, 268, 70, "release through the RyR channel: fast", "label"))
    o.append(H.label(s, 540, 88, "a rises with", "label2", I["secondary"]))
    o.append(H.label(s, 540, 106, f'τ{H.sub("act", s)} ≈ 10 ms', "label", I["primary"]))
    # slow: pump, thin shaft
    o.append(circ(250, 200, 11, "#fff", I["primary"], 1.2))
    o.append(H.label(s, 250, 204.5, "P", "label2", I["primary"], "middle"))
    o.append(ca_arrow(s, p, 520, 200, 266, 200, w="leader"))
    o.append(H.label(s, 268, 186, "re-uptake by the SERCA pump: slow", "label"))
    o.append(H.label(s, 268, 222, f"against the gradient, 2 {ca()} per ATP", "label2", I["secondary"]))
    o.append(H.label(s, 540, 198, "a falls with", "label2", I["secondary"]))
    o.append(H.label(s, 540, 216, f'τ{H.sub("deact", s)} ≈ 40 ms', "label", I["primary"]))
    for cx_, cy_ in ((600, 140), (640, 156), (690, 136), (720, 160), (660, 128)):
        o.append(ca_dot(cx_, cy_))
    o.append(H.label(s, 740, 34, "cytosol", "label2", I["secondary"], "end"))
    o.append(H.label(s, 268, 262, "SR membrane", "label2", I["secondary"]))
    lg, _ = legend(s, 30, 290, [(sw_ca, f"{ca()} ion"), (sw_line(CA_COL, 5), f"{ca()} flux"),
                                (sw_rect(BOX, I["rule"]), "SR lumen"),
                                (sw_rect("#fff", I["primary"]), "channel (RyR) and pump (SERCA, P)")], gap=16)
    o.append(lg)
    aria = ("Calcium handling. The sarcoplasmic reticulum on the left stores calcium. A thick arrow through the open RyR "
            "channel releases calcium into the cytosol fast, so activation rises with tau act about 10 ms. A thin arrow "
            "through the SERCA pump returns calcium slowly against its gradient, 2 calcium ions per ATP, so activation "
            "falls with tau deact about 40 ms.")
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


# ---------------------------------------------------------------- svg 28: attached heads vs sliding speed (Fig. 23)
def fig28():
    VB = (0, 0, 760, 250)
    s = H.Scale(VB[2], VB[3])
    p = "m5f28_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    cases = []
    for name, n in (("slow", 7), ("medium", 4), ("fast", 1)):
        fv = n / 8                                         # attached heads proportional to force (line 1250)
        x = (1 - fv) / (1 + fv / 0.25)                     # invert f_V = (1 - x) / (1 + x / c), c = 0.25
        assert abs(f_V(x) - fv) < 1e-12
        cases.append((name, n, x, fv))
    for k, (name, n, x, fv) in enumerate(cases):
        cx = 130 + 250 * k
        o.append(rect(cx - 105, 76, 210, 14, T["actin"][0], T["actin"][1], 0.8, 7))
        o.append(rect(cx - 105, 140, 210, 14, T["myosin"][0], T["myosin"][1], 0.8, 7))
        att = {round(j * 8 / n) for j in range(n)}
        for i in range(8):
            hx = cx - 84 + i * 24
            if i in att:
                o.append(f'<line x1="{hx}" y1="140" x2="{hx+8}" y2="96" stroke="{O["neural"]}" stroke-width="3" stroke-linecap="round"/>')
                o.append(ellipse(hx + 8, 95, 6, 4.5, O["neural"], "#fff", 0.8))
            else:
                o.append(f'<line x1="{hx}" y1="140" x2="{hx-7}" y2="124" stroke="{T["myosin"][1]}" stroke-width="3" stroke-linecap="round"/>')
                o.append(ellipse(hx - 8, 121, 5, 4, T["myosin"][0], T["myosin"][1], 0.8))
        L = max(10.0, 300 * x)                             # arrow length proportional to v (300 px per v_max)
        o.append(H.arrow(s, p, cx - 100, 62, cx - 100 + L, 62, "dim", w="geom"))
        o.append(H.label(s, cx - 100, 44, f'v = {x:.2f} v{H.sub("max", s)}', "label2", I["secondary"]))
        o.append(H.label(s, cx, 180, name, "label", I["primary"], "middle"))
        o.append(H.label(s, cx, 198, f'f{H.sub("V", s, "label2")} = {fv:.2f}: {n} of 8 heads attached', "label2",
                         I["secondary"], "middle"))
    o.append(H.label(s, 750, 18, "thin filament slides at speed v →", "label2", I["secondary"], "end"))
    lg, _ = legend(s, 30, 236, [(sw_rect(T["actin"][0], T["actin"][1]), "thin filament (actin)"),
                                (sw_rect(T["myosin"][0], T["myosin"][1]), "thick filament (myosin)"),
                                (sw_rect(O["neural"]), "attached head, pulling"),
                                (sw_rect(T["myosin"][0], T["myosin"][1]), "detached head")], gap=16)
    o.append(lg)
    aria = ("Three panels of a thick filament with eight myosin heads under a sliding thin filament. At v = 0.03, 0.17 "
            "and 0.58 times v max, Hill's relation with curvature 0.25 gives f V = 0.88, 0.50 and 0.12, so 7, 4 and 1 of "
            "8 heads are attached (green). Force falls with shortening speed because fewer heads are attached.")
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


# ---------------------------------------------------------------- problem figures (400 px)
def legend_rows(s, x, y, items, gap=12):
    return legend(s, x, y, items, gap=gap)[0]


def fig42():                                              # C1: the sarcomere as the contractile unit
    VB = (0, 0, 400, 160)
    s = H.Scale(VB[2], VB[3], display_w=400)
    p = "m5f42_"
    S, cy = 40.0, 76.0
    w = 2.7 * S
    o = [f'<defs>{H.markers(p, s)}</defs>']
    for k in (-1, 0, 1):
        body, _ = sarcomere(200 + k * w, cy, 2.7, S, shade=False, heads=False, row=9, th=4, kh=7, zh=34)
        o.append(body)
    o.append(rect(200 - w / 2, cy - 21, w, 42, "none", O["geometry"], 1.4, 3))
    o.append(H.arrow(s, p, 200 - w / 2, 40, 200 + w / 2, 40, "geometry", both=True))
    o.append(H.label(s, 200, 28, "one sarcomere, Z to Z: ℓ ≈ 2.7 µm", "label2", O["geometry"], "middle"))
    o.append(H.label(s, 200, 118, "myofibril: sarcomeres in series", "label2", I["secondary"], "middle"))
    o.append(legend_rows(s, 14, 150, [(sw_rect(T["actin"][0], T["actin"][1]), "actin"),
                                       (sw_rect(T["myosin"][0], T["myosin"][1]), "myosin"),
                                       (sw_rect(T["zdisc"][0]), "Z-disc")]))
    aria = "Part of a myofibril: three sarcomeres in series; the middle one, from Z-disc to Z-disc, about 2.7 micrometres, is marked."
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


def fig43():                                              # C2: sarcomere pulled long, no overlap
    VB = (0, 0, 400, 160)
    s = H.Scale(VB[2], VB[3], display_w=400)
    S, cy, l = 76.0, 76.0, 4.6
    o = []
    body, (xl, xr) = sarcomere(200, cy, l, S, shade=False, heads=True, row=11, th=5, kh=8, zh=40)
    o.append(body)
    gl = (200 + (-l / 2 + A_THIN) * S + 200 - A_THICK / 2 * S) / 2
    gr = 400 - gl
    o.append(H.label(s, 200, 30, "no overlap", "label2", I["primary"], "middle"))
    for g in (gl, gr):
        o.append(H.line(s, 200 + (g - 200) * 0.45, 34, g, cy - 16, I["primary"], "leader"))
    o.append(H.label(s, 200, 124, f"ℓ = {l} µm, Z to Z", "label2", I["secondary"], "middle"))
    for z in (xl, xr):
        o.append(H.label(s, z, cy + 36, "Z", "label2", I["secondary"], "middle"))
    o.append(legend_rows(s, 14, 152, [(sw_rect(T["actin"][0], T["actin"][1]), "actin"),
                                       (sw_rect(T["myosin"][0], T["myosin"][1]), "myosin"),
                                       (sw_rect(T["zdisc"][0]), "Z-disc")]))
    aria = ("A sarcomere pulled to 4.6 micrometres, drawn to scale: the thin filaments from the two Z-discs no longer "
            "reach the thick filament, so there is no overlap.")
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


def fig44():                                              # C3: pennate fibres packing
    VB = (0, 0, 400, 300)
    s = H.Scale(VB[2], VB[3], display_w=400)
    p = "m5f44_"
    th = math.radians(25)
    Lf = 150.0
    h = Lf / 2 * math.sin(th)                              # pennate fibres exactly L_f / 2 long: same box, same volume
    yb = 104.0                                             # bottom edge of both muscle blocks
    xp, xq = 66.0, 236.0                                   # left edge of the parallel and the pennate block
    o = [f'<defs>{H.markers(p, s)}{muscle_grad(p + "mh", xp, 0, xp + Lf, 0)}'
         f'{muscle_grad(p + "mg", 0, yb, 0, yb - h)}</defs>']
    # left: the calf (InjuryMap), a strongly pennate group (module text, section 1)
    k = 150 / CALF[3]
    ox = 28 - CALF[2] / 2 * k
    o.append(calf_use(f"translate({ox - CALF[0] * k:.2f} {26 - CALF[1] * k:.2f}) scale({k:.4f})"))
    o.append(H.label(s, 28, 192, "calf:", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 28, 207, "pennate", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 228, 30, "two muscles of the same volume", "label2", I["secondary"], "middle"))
    # parallel: fibres run the full length L_f between two tendons
    o.append(rect(xp - 8, yb - h, 8, h, T["tendon"][0], T["tendon"][1], 0.8, 2))
    o.append(rect(xp + Lf, yb - h, 8, h, T["tendon"][0], T["tendon"][1], 0.8, 2))
    o.append(tissue(s, [(xp, yb), (xp + Lf, yb), (xp + Lf, yb - h), (xp, yb - h)], fill=f"url(#{p}mh)"))
    for j in range(1, 6):
        y = yb - h * j / 6
        o.append(fibre_line(s, xp + 1, y, xp + Lf - 1, y, 0.6, 0.9))
    o.append(H.arrow(s, p, xp, yb + 18, xp + Lf, yb + 18, "geometry", both=True))
    o.append(H.label(s, xp + Lf / 2, yb + 38, "L" + H.sub("f", s, "label2"), "label2", O["geometry"], "middle"))
    o.append(H.label(s, xp + Lf / 2, yb + 68, "parallel", "label", I["primary"], "middle"))
    # pennate: fibres L_f / 2 long at theta_p between a tendon (bottom) and an aponeurosis (top), in the same box
    o.append(tissue(s, [(xq, yb), (xq + Lf, yb), (xq + Lf, yb - h), (xq, yb - h)], fill=f"url(#{p}mg)"))
    run = h / math.tan(th)
    xb = xq - run
    while xb < xq + Lf:                                    # each fibre clipped to the box x range
        xa, xe = max(xb, xq + 1), min(xb + run, xq + Lf - 1)
        if xe - xa > 4:
            o.append(fibre_line(s, xa, yb - (xa - xb) * math.tan(th), xe, yb - (xe - xb) * math.tan(th), 0.7, 0.9))
        xb += 12
    o.append(rect(xq - 4, yb - h - 7, Lf + 12, 7, T["tendon"][0], T["tendon"][1], 0.8, 3))
    o.append(rect(xq - 8, yb, Lf + 12, 7, T["tendon"][0], T["tendon"][1], 0.8, 3))
    o.append(H.label(s, xq + Lf / 2, yb + 38, f"fibres ≈ L{H.sub('f', s, 'label2')}/2 at {th_p(s, 'label2')} = 25°",
                     "label2", I["secondary"], "middle"))
    o.append(H.label(s, xq + Lf / 2, yb + 68, "pennate", "label", I["primary"], "middle"))
    o.append(legend_rows(s, 8, 232, [(sw_rect(T["muscle"][0], T["muscle"][1]), "muscle fibres"),
                                       (sw_rect(T["tendon"][0], T["tendon"][1]), "tendon, aponeurosis")]))
    o.append(calf_credit(s, 8, 254, 70))
    aria = ("Left: InjuryMap art of a calf, a strongly pennate muscle group. Right: two muscles of the same volume, drawn "
            "in the same box. Parallel: fibres run the full length L f between two tendons. Pennate: many shorter "
            "fibres, about L f over 2 long, attach at 25 degrees between a tendon and an aponeurosis.")
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


def twitch_model(f_hz, T_ms=250.0, dt=0.1):
    """Module 5 K2 model (Modelling assumption 3.2 + saturating train): returns t (ms) and a(t)."""
    TR, TD, TAU_A = 3.6, 18.0, 41.0
    t_pk = TR * math.log(1 + TD / TR)
    norm = (1 - math.exp(-t_pk / TR)) * math.exp(-t_pk / TD)

    def pulse(t):
        return (1 - math.exp(-t / TR)) * math.exp(-t / TD) / norm if t > 0 else 0.0
    spikes = [0.0] if f_hz is None else [k * 1000.0 / f_hz for k in range(int(T_ms * f_hz / 1000.0) + 1)]
    ts, aa, a = [], [], 0.0
    n = int(T_ms / dt)
    for i in range(n + 1):
        t = i * dt
        prod = 1.0
        for ti in spikes:
            if ti < t:
                prod *= 1 - pulse(t - ti)
        c = 0.1 + 1.3 * (1 - prod)
        tgt = c ** 3 / (1 + c ** 3)
        ts.append(t)
        aa.append(a)
        a += dt * (tgt - a) / TAU_A
    return ts, aa


def fig45():                                              # C4: twitches sum toward the ceiling
    VB = (0, 0, 400, 240)
    s = H.Scale(VB[2], VB[3], display_w=400)
    x0, x1, y0, y1 = 52, 388, 176, 22
    TMAX, AMAX = 250.0, 0.8
    X = lambda t: x0 + t / TMAX * (x1 - x0)               # noqa: E731
    Y = lambda a: y0 - a / AMAX * (y0 - y1)               # noqa: E731
    t, a60 = twitch_model(60.0)
    _, a1 = twitch_model(None)
    a_inf = 1.4 ** 3 / (1 + 1.4 ** 3)
    pk = max(a1)
    mean60 = sum(v for tt, v in zip(t, a60) if tt > 150) / sum(1 for tt in t if tt > 150)
    o = []
    for v in (0.2, 0.4, 0.6):
        o.append(H.line(s, x0, Y(v), x1, Y(v), GRID, "leader"))
    o.append(H.line(s, x0, y0, x1, y0, I["axis"], "axis"))
    o.append(H.line(s, x0, y0, x0, y1, I["axis"], "axis"))
    for v in (0.0, 0.2, 0.4, 0.6):
        o.append(H.line(s, x0 - 4, Y(v), x0, Y(v), I["axis"], "leader"))
        o.append(H.label(s, x0 - 7, Y(v) + 4.5, f"{v:.1f}", "tick", I["secondary"], "end"))
    for tt in (0, 100, 200):
        o.append(H.line(s, X(tt), y0, X(tt), y0 + 4, I["axis"], "leader"))
        o.append(H.label(s, X(tt), y0 + 18, f"{tt}", "tick", I["secondary"], "middle"))
    o.append(H.label(s, (x0 + x1) / 2, y0 + 36, "time (ms)", "label2", I["primary"], "middle"))
    o.append(H.label(s, 16, (y0 + y1) / 2, "activation a", "label2", I["primary"], "middle",
                     f'transform="rotate(-90 16 {(y0 + y1) / 2})"'))
    o.append(H.line(s, x0, Y(a_inf), x1, Y(a_inf), O["dim"], "ref", H.DASH_REF))
    o.append(H.label(s, x1, Y(a_inf) - 7, f"ceiling a∞ ≈ {a_inf:.2f}", "label2", I["secondary"], "end"))
    step = 25                                              # every 2.5 ms
    for ser, col in ((a60, H.SERIES[0]), (a1, H.SERIES[1])):
        pts = " ".join(f"{X(t[i]):.2f},{Y(ser[i]):.2f}" for i in range(0, len(t), step))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{s(H.PX["curve_multi"]):.2f}" '
                 f'stroke-linejoin="round"/>')
    o.append(H.label(s, X(150), Y(0.52), "60 Hz train", "label2", I["primary"], "middle"))
    o.append(H.label(s, X(70), Y(0.26), f"one twitch, peak {pk:.2f}", "label2", I["primary"], "start"))
    o.append(legend_rows(s, 14, 232, [(sw_line(H.SERIES[0], 2), "60 Hz impulse train"),
                                       (sw_line(H.SERIES[1], 2), "single impulse"),
                                       (sw_line(O["dim"], 1.4, "6 4"), "a∞ ceiling")], gap=10))
    hv = []
    for i in range(0, len(t), 20):                         # every 2 ms
        hv.append([round(X(t[i]), 2), [round(Y(a60[i]), 2), round(Y(a1[i]), 2)],
                   f"t = {t[i]:.0f} ms: train a = {a60[i]:.2f}, twitch a = {a1[i]:.2f}"])
    aria = (f"Activation against time from the module's twitch model. One impulse gives a twitch peaking at {pk:.2f}. "
            f"A 60 Hz impulse train sums the twitches up to a mean of about {mean60:.2f}, just under the calcium ceiling "
            f"a-infinity of {a_inf:.2f}, drawn as a dashed line.")
    return H.svg_open(VB, esc(aria), s, extra=H.hover_attr([x0, y1, x1, y0], hv)) + "".join(o) + "</svg>"


def fig52():                                              # D1: resolve fibre force onto the tendon
    VB = (0, 0, 400, 250)
    s = H.Scale(VB[2], VB[3], display_w=400)
    p = "m5f52_"
    th = math.radians(25)
    yt = 178.0
    o = [f'<defs>{H.markers(p, s)}</defs>']
    ya, xi = yt - 100, 100.0                               # aponeurosis edge; the fibre whose force is resolved
    run = (yt - ya) / math.tan(th)
    o.append(pennate_sheet(s, 14, xi - 11, yt, ya, th, p))
    o.append(one_fibre(s, xi, yt, ya, th, p))
    o.append(rect(8, yt, 384, 12, T["tendon"][0], T["tendon"][1], 0.8, 6))
    o.append(rect(14 + run - 10, ya - 8, 392 - (14 + run - 10), 8, T["tendon"][0], T["tendon"][1], 0.8, 4))
    o.append(H.label(s, 332, 96, "one fibre", "label2", I["secondary"]))
    Lf = 170.0
    tip = (xi + Lf * math.cos(th), yt - Lf * math.sin(th))
    o.append(H.arrow(s, p, xi, yt, *tip, "force"))
    o.append(H.arrow(s, p, xi, yt, tip[0], yt, "force"))
    o.append(dashed_arrow(s, p, tip[0], yt, tip[0], tip[1] + 2, "force"))
    o.append(angle_arc(s, xi, yt, 44, 0, 25))
    o.append(H.label(s, xi + 50, yt - 6, th_p(s, "label2"), "label2", O["geometry"]))
    o.append(H.label(s, 30, 96, f"{F_fib(s, 'label2')} = σ·PCSA", "label2", O["force"]))
    o.append(H.label(s, xi, yt + 34, f"along the tendon: {F_fib(s, 'label2')} cos {th_p(s, 'label2')}", "label2",
                     O["force"]))
    o.append(H.label(s, tip[0] + 8, 130, f"{F_fib(s, 'label2')} sin {th_p(s, 'label2')}", "label2", O["force"]))
    o.append(H.label(s, 200, 22, f"derive F{H.sub('max', s)} = σ·PCSA·cos {th_p(s)}", "label", I["primary"], "middle"))
    o.append(legend_rows(s, 14, 242, [(sw_rect(T["muscle"][0], T["muscle"][1]), "muscle fibres"),
                                       (sw_rect(T["tendon"][0], T["tendon"][1]), "tendon, aponeurosis"),
                                       (sw_line(O["force"]), "force")]))
    aria = ("Resolve the fibre force onto the tendon: a pennate muscle sheet between a tendon and an aponeurosis, its "
            "fibres at the pennation angle theta p. One fibre, outlined, pulls with F fibre = sigma "
            "times PCSA; its part along the tendon is F fibre cos theta p and the dashed part across it is F fibre sin "
            "theta p. Goal: F max = sigma PCSA cos theta p.")
    return H.svg_open(VB, esc(aria), s) + "".join(o) + "</svg>"


FIGS = {
    2: ("Pennate muscle: fibers at pennation angle alpha to the tendo", fig2),
    5: ("A left-to-right zoom cascade through the muscle force-produc", fig5),
    6: ("A unipennate muscle: fibres attach at pennation angle theta_", fig6),
    7: ("The four-state crossbridge cycle drawn as a ring. State 1 at", fig7),
    9: ("Four sarcomere panels at increasing length showing how thin-", fig9),
    11: ("Animated sarcomere: thin actin filaments anchored to two Z-d", fig11),
    12: ("Excitation-contraction coupling pathway. A motor-neuron term", fig12),
    14: ("Two panels of the thin filament. Top, relaxed with no calciu", fig14),
    17: ("A motor unit: a small and a large alpha-motoneuron in the sp", fig17),
    24: ("Schematic of calcium handling: the sarcoplasmic reticulum on", fig24),
    28: ("Three panels of a thick filament with eight myosin heads and", fig28),
    42: ("sarcomere as the contractile unit", fig42),
    43: ("sarcomere pulled long, no overlap", fig43),
    44: ("pennate fibres packing", fig44),
    45: ("Activation climbing toward the fused-tetanus ceiling: succes", fig45),
    52: ("resolve fibre force onto tendon", fig52),
}
