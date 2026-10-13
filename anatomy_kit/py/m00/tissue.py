"""Module 0, group `tissue`: tissue / molecular schematics and logarithmic ladders in the house style.

Main text (760 px): svg 2 (Fig. 1 zoom), 9 (Fig. 8 collagen load path), 12 (Fig. 11 SERCA + ledger),
13 (Fig. 12 chain + force laws), 23 (Fig. 21 Gly-X-Y), 25 (Fig. 23 bilayer capacitor); ladders 3 (Fig. 2
concentration), 4 (Fig. 3 energy), 8 (Fig. 7 modulus descent).
Every plotted number is computed here from a constant or a value module00.html states (line numbers beside
each constant). Art: NIH NIAID BioArt 244 (public domain), cropped by crop_art.py to one femur.
"""
import math
import random
import re
from pathlib import Path

import house as H
from m05.body import finish, wrap
from m05.plots_main import Ax, axes, dot
from m05.plots_main import legend as plegend
from m05.tissue import ca, ca_arrow, ca_dot, ca_marker, circ, legend, path, rect, sw_ca, sw_dot, sw_line, sw_rect

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
BOX, GRID = "#f7f4ef", "#e6e6e6"
KIT = Path(__file__).resolve().parents[2] / "svg_paths"

# ---------------------------------------------------------------- constants the module states
K_B, T_BODY, N_A = 1.381e-23, 310.15, 6.022e23      # line 163
KBT = K_B * T_BODY                                   # 4.28e-21 J (line 165)
RG = 8.314                                           # line 632
RGT = RG * T_BODY / 1000                             # 2.58 kJ/mol (line 165, 316)
E_CHG, EPS0 = 1.602e-19, 8.854e-12                   # line 167, line 1376


def it(t):
    return f'<tspan font-style="italic">{t}</tspan>'


def kbt(s, size="label2"):
    return f'k{H.sub("B", s, size)}T'


def sup(t):
    return t.translate(str.maketrans("0123456789-+", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺"))


def sci(v, n=1):
    """3.4 × 10⁷ in Unicode."""
    e = math.floor(math.log10(abs(v)))
    return f"{v / 10 ** e:.{n}f} × 10{sup(str(e))}"


def spread(ys, gap, lo=-1e9, hi=1e9):
    """Push sorted label rows apart to at least `gap`, keeping them as close to their marks as possible."""
    y = list(ys)
    for _ in range(200):
        moved = False
        for i in range(1, len(y)):
            d = y[i] - y[i - 1]
            if d < gap - 1e-6:
                m = (gap - d) / 2
                y[i - 1] -= m
                y[i] += m
                moved = True
        y = [min(max(v, lo), hi) for v in y]
        if not moved:
            break
    return y


def dpath(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def leader(s, x1, y1, x2, y2, col=None):
    """Bent leader: mark -> short horizontal -> label row."""
    col = col or I["muted"]
    return path(f"M{x1:.1f},{y1:.1f} L{x1 + 10:.1f},{y1:.1f} L{x2 - 6:.1f},{y2:.1f} L{x2 - 2:.1f},{y2:.1f}", col, s(1.0))


# ================================================================ svg #2  Fig. 1: femur -> fibril -> bond
F1 = dict(F=1717.0, A=4.62e-4, E=17e9, L=0.43,       # line 107: F, A, E, femur length
          k=25.0, r0=0.24e-9, D=67, mineral=60)       # line 120 (k), 128 (D-period, 60 %), 135 (r0)
FEMUR_ART = (7.9, 41.0, 71.5, 374.4)                  # bbox of the femur fill path in the art (Chrome getBBox)
ART_HEAD = (52.0, 43.5)                               # top of the femoral head on that path (grid render)


def femur_d():
    """The one femur path of the crop (crop_art.py ../svg_paths/nih_upper_leg.svg m00femur 4 37 76 379
    --drop "path:not(:nth-of-type(9))"). Drawn inline as m05.schematic.nih_forearm draws the arm bones:
    fill only, so the art's fade-out mask and its outline under-shape (which also outlines the pelvis) go."""
    src = (KIT / "nih_upper_leg_crop_m00femur.svg").read_text(encoding="utf-8")
    ds = re.findall(r'<path\b[^>]*?\bd="([^"]+)"', src)
    assert len(ds) == 1, len(ds)
    return ds[0]


def strand_paths(x0, x1, yc, amp, lam, phases, w_out, w_in, n=120):
    """Braided strands drawn as rope: a dark outer stroke under a light core (paths, not polylines)."""
    o_out, o_in = [], []
    for ph in phases:
        pts = [(x0 + (x1 - x0) * i / n, yc + amp * math.sin(2 * math.pi * (x1 - x0) * i / n / lam + ph)) for i in range(n + 1)]
        o_out.append(path(dpath(pts), T["tendon"][1], w_out, extra='stroke-linecap="round"'))
        o_in.append(path(dpath(pts), T["tendon"][0], w_in, extra='stroke-linecap="round"'))
    return "".join(a + b for a, b in zip(o_out, o_in))


def zigzag(x0, x1, y, n=8, amp=7.0, lead=10.0):
    pts = [(x0, y), (x0 + lead, y)]
    w = (x1 - x0 - 2 * lead) / n
    for i in range(n):
        pts.append((x0 + lead + (i + 0.5) * w, y + (amp if i % 2 else -amp)))
    pts += [(x1 - lead, y), (x1, y)]
    return dpath(pts)


def fig2():
    idx, p = 2, "m0f2_"
    VB = (0, 0, 760, 372)
    s = H.Scale(VB[2], VB[3])
    d = F1
    eps = d["F"] / d["A"] / d["E"]
    dL_mm = eps * d["L"] * 1e3
    E_bond = d["k"] / d["r0"] / 1e9
    assert abs(dL_mm - 0.094) < 0.0005 and abs(E_bond - 104) < 0.5
    o = [f'<defs>{H.markers(p, s)}</defs>']
    titles = [(108, "① whole bone: what you feel"), (366, "② mineralised fibril: which tissue"),
              (632, "③ one ionic bond: which molecule")]
    for x, t in titles:
        o.append(H.label(s, x, 18, t, "label", I["primary"], "middle"))
    # ---- panel 1: the femur (NIH art), body load, length; labels on the left so the zoom guides run clear
    fx0, fy0, fy1 = 96.0, 58.0, 300.0
    k = (fy1 - fy0) / (FEMUR_ART[3] - FEMUR_ART[1])
    tx, ty = fx0 - FEMUR_ART[0] * k, fy0 - FEMUR_ART[1] * k
    o.append(f'<g transform="translate({tx:.2f} {ty:.2f}) scale({k:.4f})"><path d="{femur_d()}" fill="{T["bone"][0]}" '
             f'stroke="{T["bone"][1]}" stroke-width="{1.2 / k:.2f}" stroke-linejoin="round"/></g>')
    hx, hy = tx + ART_HEAD[0] * k, ty + ART_HEAD[1] * k
    fx1 = tx + FEMUR_ART[2] * k
    o.append(H.arrow(s, p, hx, hy - 30, hx, hy - 2, "load"))
    o.append(H.label(s, hx + 8, hy - 18, f'body load {it("F")} ≈ {d["F"]:.0f} N', "label2", I["primary"]))
    xd = fx0 - 12
    o.append(H.line(s, xd - 4, fy0, xd + 4, fy0, O["dim"], "leader"))
    o.append(H.line(s, xd - 4, fy1, xd + 4, fy1, O["dim"], "leader"))
    o.append(H.line(s, xd, fy0, xd, fy1, O["dim"], "ref", extra=f'marker-start="url(#{p}a_dim)" marker-end="url(#{p}a_dim)"'))
    o.append(H.label(s, xd - 8, 104, f'{it("L")} = {d["L"]*100:.0f} cm', "label2", I["primary"], "end"))
    o.append(H.label(s, xd - 8, 122, "shortens by", "label2", I["secondary"], "end"))
    o.append(H.label(s, xd - 8, 138, f"{dL_mm:.3f} mm", "label2", I["secondary"], "end"))
    o.append(H.label(s, xd - 8, 236, f'{it("E")} ≈ {d["E"]/1e9:.0f} GPa', "label", I["primary"], "end"))
    o.append(H.label(s, xd - 8, 252, "(measured)", "label2", I["muted"], "end"))
    # zoom window on the cortical shaft
    zx, zy, zw = tx + 22 * k, ty + 205 * k, 12.0
    o.append(f'<rect x="{zx:.1f}" y="{zy:.1f}" width="{zw}" height="{zw}" fill="none" stroke="{I["axis"]}" stroke-width="{s(1.2):.2f}"/>')
    # ---- panel 2: the fibril (schematic)
    bx0, bx1, yc = 246.0, 486.0, 150.0
    Dpx = (bx1 - bx0) / 4.2                                  # four D-periods across the drawing
    plate_w, plate_h = 0.45 * Dpx, 9.0
    for i in range(4):
        for row, dy in ((0, -21), (1, 21)):
            px_ = bx0 + (i + 0.30 + 0.25 * row) * Dpx
            o.append(rect(px_, yc + dy - plate_h / 2, plate_w, plate_h, T["bone_shade"][0], T["bone"][1], 1.0, 2))
    o.append(strand_paths(bx0, bx1, yc, 12.0, Dpx * 0.98, (0, 2 * math.pi / 3, 4 * math.pi / 3), s(6.5), s(4.0)))
    pl = (bx0 + 1.30 * Dpx + plate_w / 2, yc - 21 - plate_h / 2)
    o.append(H.line(s, pl[0], pl[1] - 2, pl[0] + 26, 84, I["secondary"], "leader"))
    o.append(H.label(s, pl[0] + 29, 82, "apatite platelets (mineral)", "label2", I["primary"]))
    o.append(H.line(s, bx0 + 3.25 * Dpx, yc + 12, bx0 + 3.25 * Dpx + 6, 222, I["secondary"], "leader"))
    o.append(H.label(s, bx0 + 3.25 * Dpx + 9, 226, "collagen triple helices", "label2", I["primary"]))
    yD = 196
    a0, a1 = bx0 + 0.55 * Dpx, bx0 + 1.55 * Dpx
    for x in (a0, a1):
        o.append(H.line(s, x, yD - 7, x, yD + 7, O["geometry"], "leader"))
    o.append(H.arrow(s, p, a0, yD, a1, yD, "geometry", both=True))
    o.append(H.label(s, (a0 + a1) / 2, yD + 22, f'D-period {d["D"]} nm', "label2", I["primary"], "middle"))
    o.append(H.label(s, 366, 258, f'≈ {d["mineral"]} % mineral by mass', "label2", I["secondary"], "middle"))
    z2x, z2y = bx0 + 3.55 * Dpx, yc - 21 - plate_h / 2 - 3
    o.append(f'<rect x="{z2x:.1f}" y="{z2y:.1f}" width="{zw}" height="{zw}" fill="none" stroke="{I["axis"]}" stroke-width="{s(1.2):.2f}"/>')
    # ---- panel 3: one Ca-O bond as a spring
    cx1, cx2, yb, r1, r2 = 572.0, 692.0, 150.0, 25.0, 19.0
    o.append(path(zigzag(cx1 + r1, cx2 - r2, yb), I["axis"], s(2.0), extra='stroke-linejoin="round"'))
    o.append(circ(cx1, yb, r1, T["fluid"][0], T["fluid"][1], 1.4))
    o.append(H.label(s, cx1, yb + 5, "Ca²⁺", "label", I["primary"], "middle"))
    o.append(circ(cx2, yb, r2, BOX, I["axis"], 1.4))
    o.append(H.label(s, cx2, yb + 5, "O²⁻", "label", I["primary"], "middle"))
    o.append(H.label(s, (cx1 + cx2) / 2, 106, f'bond stiffness {it("k")} ≈ {d["k"]:.0f} N m⁻¹', "label2", I["primary"], "middle"))
    for x in (cx1, cx2):
        o.append(H.line(s, x, yb + r2 + 22, x, yb + r2 + 36, O["geometry"], "leader"))
    yr = yb + r2 + 29
    o.append(H.arrow(s, p, cx1, yr, cx2, yr, "geometry", both=True))
    o.append(H.label(s, (cx1 + cx2) / 2, yr + 22, f'{it("r")}₀ ≈ {d["r0"]*1e9:.2f} nm', "label2", I["primary"], "middle"))
    o.append(H.label(s, (cx1 + cx2) / 2, yr + 46, "the spring the whole leg stands on", "label2", I["secondary"], "middle",
                     'font-style="italic"'))
    # ---- zoom guides (dashed construction paths; text kept clear of them)
    da = f'stroke-dasharray="{s(5):.1f} {s(3):.1f}"'
    o.append(path(f"M{zx+zw:.1f},{zy:.1f} L{bx0-6:.1f},62 M{zx+zw:.1f},{zy+zw:.1f} L{bx0-6:.1f},240", I["rule"], s(1.1), extra=da))
    o.append(path(f"M{z2x+zw:.1f},{z2y:.1f} L{cx1-r1-16:.1f},104 M{z2x+zw:.1f},{z2y+zw:.1f} L{cx1-r1-16:.1f},196", I["rule"],
                  s(1.1), extra=da))
    # ---- the return trip: E ~ k / r0, back to the bone (grey: an argument, not a force)
    o.append(path(f"M{(cx1+cx2)/2:.1f},{yr+56:.1f} C{cx1:.1f},{yr+104:.1f} 330,{yr+108:.1f} {fx1+8:.1f},{fy1-6:.1f}", O["dim"],
                  s(H.PX["geom"]), extra=f'marker-end="url(#{p}a_dim)"'))
    o.append(H.label(s, 420, 328, f'{it("E")} ≈ {it("k")} / {it("r")}₀ = ({d["k"]:.0f} N m⁻¹) ÷ ({d["r0"]*1e9:.2f} nm) ≈ '
                     f'{E_bond:.0f} GPa: calibrated here, derived in §2', "label2", I["primary"], "middle"))
    cr = H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt (Ryan Kissinger)", title="Human Upper Leg Bones (BioArt 244)",
                                    changes="One femur only; recoloured. Fibril and bond are schematic, not to scale.")
    o.append(H.credit(s, 10, 352, wrap(cr, 120)))
    aria = ("Three-panel zoom. Left: a femur (NIH BioArt) under a body load F of about 1717 N, length 43 cm, shortening by "
            f"{dL_mm:.3f} mm, measured modulus E about 17 GPa. A small window on the shaft magnifies to the middle panel: a "
            "mineralised collagen fibril, three braided triple-helix strands with apatite platelets in the gap zones, "
            "D-period 67 nm, about 60 percent mineral by mass. A window on one platelet magnifies to the right panel: one "
            "calcium-oxygen ionic bond drawn as two spheres joined by a spring of stiffness k about 25 newton per metre at "
            "separation r-zero 0.24 nanometre. A grey return arrow runs from the bond back to the bone, carrying E about k "
            f"over r-zero, {E_bond:.0f} gigapascal, calibrated here and derived in section 2.")
    return finish(VB, aria, s, o)


# ================================================================ svg #3  Fig. 2: concentration ladder
C_MARKS = [                                         # table, lines 252-259 (Ca labels: lines 257-258)
    (55.5, "water, the solvent itself: 55.5 M"),
    (0.2, "cartilage fixed charge: 0.2 M (M4 §2)"),
    (0.145, "Na⁺ outside, 145 mM; K⁺ inside the cell, 140 mM"),
    (5e-3, "ATP, inside a muscle fibre: 5 mM"),
    (10e-6, "free Ca²⁺, top of the activation range: 10 µM"),
    (0.1e-6, "free Ca²⁺, resting cytosol: 0.1 µM (M5 §3)"),
    (1e-9, "a peptide hormone, in plasma: 1 nM"),
]
D_1M = (N_A * 1e3 * 1e-27) ** (-1 / 3)              # 1.184 nm (line 234)


def dbar(c):
    return D_1M / c ** (1 / 3)


def fig3():
    VB = (0, 0, 760, 480)
    s = H.Scale(VB[2], VB[3])
    xa, top, pitch = 300.0, 64.0, 36.0               # axis x, y of 100 M, px per decade
    Y = lambda c: top + (2 - math.log10(c)) * pitch  # noqa: E731
    assert abs(D_1M - 1.184) < 0.001
    o = []
    o.append(H.label(s, 150, 24, "mean spacing d̄", "label", I["primary"], "end"))
    o.append(H.label(s, 150, 42, "= 1.184 nm ÷ ∛(c / 1 M)", "label2", I["secondary"], "end"))
    o.append(H.label(s, xa - 12, 24, "concentration c", "label", I["primary"], "end"))
    o.append(H.label(s, xa + 34, 24, "where the body puts it", "label", I["primary"]))
    o.append(H.line(s, xa, Y(100) - 8, xa, Y(1e-9) + 8, I["axis"], "axis"))
    names = {2: "100 M", 1: "10 M", 0: "1 M", -1: "100 mM", -2: "10 mM", -3: "1 mM", -4: "100 µM", -5: "10 µM",
             -6: "1 µM", -7: "100 nM", -8: "10 nM", -9: "1 nM"}
    for e in range(-9, 3):
        y = Y(10.0 ** e)
        o.append(H.line(s, xa - 6, y, xa, y, I["axis"], "leader"))
        o.append(H.label(s, xa - 12, y + 4.5, names[e], "tick", I["secondary"], "end"))
        dv = dbar(10.0 ** e)
        txt = f"{dv:.0f} nm" if dv >= 100 else (f"{dv:.1f} nm" if dv >= 10 else f"{dv:.2f} nm" if dv >= 1 else f"{dv:.3f} nm")
        o.append(H.label(s, 150, y + 4.5, txt, "tick", I["secondary"], "end"))
        o.append(H.line(s, 158, y, xa - 50, y, GRID, "leader"))
    ys = [Y(c) for c, _ in C_MARKS]
    ly = spread(ys, 19)
    lx = xa + 34
    for (c, txt), y, yl in zip(C_MARKS, ys, ly):
        o.append(leader(s, xa + 4, y, lx, yl - 4.5))
        o.append(H.label(s, lx, yl, txt, "label2", I["primary"]))
    o.append(dot(s, xa, Y(0.140), SER[0]))           # K+ 140 mM sits 0.015 decades under Na+ (the two dots touch)
    for c, _ in C_MARKS:
        o.append(dot(s, xa, Y(c), SER[0]))
    # the calcium comparison the caption points at: 100-fold in c, 4.6-fold in spacing
    ya, yb = Y(10e-6), Y(0.1e-6)
    xb = 652
    o.append(path(f"M{xb-6:.1f},{ya:.1f} L{xb:.1f},{ya:.1f} L{xb:.1f},{yb:.1f} L{xb-6:.1f},{yb:.1f}", I["axis"], s(1.2)))
    ratio_d = dbar(0.1e-6) / dbar(10e-6)
    assert abs(ratio_d - 4.64) < 0.01
    o.append(H.label(s, xb + 8, (ya + yb) / 2 - 4, "c × 100", "label2", I["primary"]))
    o.append(H.label(s, xb + 8, (ya + yb) / 2 + 13, f"d̄ × {ratio_d:.1f}", "label2", I["primary"]))
    aria = ("Vertical logarithmic ladder of concentration in the body, eleven decades from 1 nanomolar at the foot to 100 molar "
            "at the head. The far-left column gives the mean spacing between molecules at each decade, from 1184 nm at 1 nM "
            "to 0.255 nm at 100 M; it shrinks only tenfold per three decades because it is a cube root. Marks: water at 55.5 M, "
            "cartilage fixed charge at 0.2 M, sodium outside at 145 mM and potassium inside at 140 mM, ATP at 5 mM, free calcium "
            "at 10 micromolar (top of the activation range) and 0.1 micromolar (resting), and a peptide hormone at 1 nM. A "
            f"bracket between the two calcium marks: 100 times in concentration, {ratio_d:.1f} times in spacing.")
    return finish(VB, aria, s, o)


# ================================================================ svg #4  Fig. 3: energy ladder in kBT and kJ/mol
def e_marks(s):
    q = kbt(s)
    x = 0.5 * 25.0 * (F1["F"] / F1["A"] / F1["E"] * F1["r0"]) ** 2 / KBT      # line 169-171: 8.0e-6
    xb_lo, xb_hi = 3e-12 * 10e-9 / KBT, 6e-12 * 10e-9 / KBT                    # line 339: 3-6 pN over 10 nm
    m = [(x, None, f"one Ca–O bond of a femur, standing on one leg: {sci(x)} {q}"),
         (1.0 / RGT, None, f"a van der Waals contact: {1/RGT:.2f} {q} (1 kJ mol⁻¹)"),
         (3.0, None, f"a hydrogen bond in water: a few {q} net (≈ 3)"),
         (xb_lo, xb_hi, f"work of one crossbridge stroke: {xb_lo:.0f}–{xb_hi:.0f} {q} (3–6 pN × 10 nm)"),
         (50.0 / RGT, None, f"one ATP hydrolysed in a working cell: {50/RGT:.1f} {q} (50 kJ mol⁻¹)"),
         (E_CHG / KBT, None, f"rearranging an ionic lattice: ≈ 1 eV = {E_CHG/KBT:.1f} {q}"),
         (348.0 / RGT, None, f"a covalent C–C bond: {348/RGT:.0f} {q} (348 kJ mol⁻¹)")]
    assert abs(x - 8.0e-6) < 0.1e-6 and abs(50 / RGT - 19.4) < 0.05 and abs(348 / RGT - 135) < 0.5
    return m


def fig4():
    VB = (0, 0, 760, 474)
    s = H.Scale(VB[2], VB[3])
    xa, top, pitch = 240.0, 72.0, 42.0               # axis x, y of 10^3 kBT, px per decade
    Y = lambda e: top + (3 - math.log10(e)) * pitch  # noqa: E731
    o = []
    # thermal band: 1 kBT (drawn first, under everything)
    o.append(f'<rect x="{xa-6:.1f}" y="{Y(1.0)-6:.1f}" width="{740-xa:.1f}" height="12" fill="{O["flag"]}" opacity="0.18"/>')
    o.append(H.label(s, 110, 26, "kJ mol⁻¹", "label", I["primary"], "end"))
    o.append(H.label(s, 110, 44, "per mole", "label2", I["secondary"], "end"))
    o.append(H.label(s, xa - 12, 26, kbt(s, "label"), "label", I["primary"], "end"))
    o.append(H.label(s, xa - 12, 44, "per molecule", "label2", I["secondary"], "end"))
    o.append(H.label(s, xa + 50, 26, "the energy of one event", "label", I["primary"]))
    o.append(H.line(s, xa, Y(1e3) - 8, xa, Y(1e-6) + 8, I["axis"], "axis"))
    for e in range(-6, 4):
        y = Y(10.0 ** e)
        o.append(H.line(s, xa - 6, y, xa, y, I["axis"], "leader"))
        o.append(H.label(s, xa - 12, y + 4.5, "1" if e == 0 else f"10{sup(str(e))}", "tick", I["secondary"], "end"))
    for e in range(-5, 4):                           # kJ/mol decades sit at 10^e / RgT on the kBT axis
        y = Y(10.0 ** e / RGT)
        if Y(1e3) - 1 <= y <= Y(1e-6) + 1:
            o.append(H.line(s, 118, y, xa, y, GRID, "leader"))
            o.append(H.line(s, xa, y, xa + 6, y, I["axis"], "leader"))
            o.append(H.label(s, 110, y + 4.5, "1" if e == 0 else f"10{sup(str(e))}", "tick", I["secondary"], "end"))
    marks = e_marks(s)
    rows = [(Y(math.sqrt(a * b)) if b else Y(a), txt) for a, b, txt in marks]
    rows.append((Y(1.0), f"thermal energy itself: 1 {kbt(s)}"))
    rows.sort(key=lambda r: r[0])
    ly = spread([r[0] for r in rows], 19)
    lx = xa + 50
    for (y, txt), yl in zip(rows, ly):
        if "thermal" not in txt:
            o.append(leader(s, xa + 6, y, lx, yl - 4.5))
        o.append(H.label(s, lx, yl, txt, "label2", I["primary"]))
    for a, b, _ in marks:
        if b:
            o.append(f'<rect x="{xa-4:.1f}" y="{Y(b):.1f}" width="8" height="{Y(a)-Y(b):.1f}" rx="4" fill="{SER[0]}" '
                     f'stroke="#fff" stroke-width="{s(1.2):.2f}"/>')
        else:
            o.append(dot(s, xa, Y(a), SER[0]))
    # the band the body's chemistry occupies (caption: about 0.4 to 40 kBT, two decades)
    xb, y1, y2 = 726, Y(40.0), Y(0.4)
    o.append(path(f"M{xb-6},{y1:.1f} L{xb},{y1:.1f} L{xb},{y2:.1f} L{xb-6},{y2:.1f}", I["axis"], s(1.2)))
    ym = (y1 + y2) / 2
    o.append(H.label(s, xb + 18, ym, f"body chemistry, 0.4–40 {kbt(s)}", "label2", I["primary"], "middle",
                     f'transform="rotate(-90 {xb+18} {ym:.1f})"'))
    aria = ("One vertical logarithmic energy axis from 10 to the minus 6 to 10 to the 3 kBT, read twice: kBT per molecule "
            "beside the axis and kilojoules per mole in the far-left column, the two offset everywhere by the factor 2.58 "
            "kJ per mol, so their decade marks interleave. A shaded band marks 1 kBT. From the bottom: one calcium-oxygen bond "
            "of a femur while standing on one leg, 8.0 times 10 to the minus 6 kBT; a van der Waals contact, 0.39 kBT; a "
            "hydrogen bond in water, a few kBT net; the work of one crossbridge stroke, 7 to 14 kBT; one ATP in a working "
            "cell, 19.4 kBT; rearranging an ionic lattice, about 1 eV or 37.4 kBT; a covalent C-C bond, 135 kBT. A bracket "
            "marks 0.4 to 40 kBT, where the body's chemistry lives.")
    return finish(VB, aria, s, o)


# ================================================================ svg #8  Fig. 7: where the factor of seventeen went
def ladder7():
    """Line 139 (k_pair, n = 8), 505 (K_apatite), 515 (E = 1.5 K, 114 measured), 525 (alpha_M / 12), 529 (0.51)."""
    e, C0 = 1.602176634e-19, 8.8541878128e-12
    Ce = 4 * e * e / (4 * math.pi * C0)                              # |z1 z2| = 4
    r0, n, aM = 0.24e-9, 8, 1.7476
    k_pair = (n - 1) * Ce / r0 ** 3
    E_naive = k_pair / r0 / 1e9
    E_lat = E_naive * aM / 12
    E_ap = 1.5 * 8 * (34191e3 / 6.02214076e23) / (9 * 5.279e-28) / 1e9
    E_meas, E_cal = 114.0, 25.0 / r0 / 1e9
    assert round(k_pair) == 467 and round(E_naive) == 1947 and round(E_lat) == 284 and round(E_ap) == 143
    assert abs(12 / aM - 6.87) < 0.005 and round(E_ap / E_lat, 2) == 0.51 and round(E_meas / E_ap, 3) == 0.795
    return E_naive, E_lat, E_ap, E_meas, E_cal, aM


def fig8():
    VB = (0, 0, 760, 488)
    s = H.Scale(VB[2], VB[3])
    p = "m0f8_"
    En, El, Ea, Em, Ec, aM = ladder7()
    xa, ytop, pitch = 190.0, 50.0, 300.0             # axis x, y of 2000 GPa, px per decade
    Y = lambda v: ytop + (math.log10(2000) - math.log10(v)) * pitch  # noqa: E731
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(H.label(s, xa - 12, 24, "E (GPa)", "label", I["primary"], "end"))
    o.append(H.label(s, xa + 16, 24, "the descent, read downward", "label", I["primary"]))
    o.append(H.line(s, xa, Y(2000) - 8, xa, Y(95) + 6, I["axis"], "axis"))
    for v in (100, 200, 500, 1000, 2000):
        o.append(H.line(s, xa - 6, Y(v), xa, Y(v), I["axis"], "leader"))
        o.append(H.label(s, xa - 12, Y(v) + 4.5, f"{v}", "tick", I["secondary"], "end"))
    rungs = [(En, f"bare Ca–O pair, {it('k')}{H.sub('pair', s, 'label2')} / {it('r')}₀: {En:.0f} GPa", False),
             (El, f"a real Ca–O lattice (CaO), predicted: {El:.0f} GPa", False),
             (Ea, f"apatite, predicted by Proposition 2.2: {Ea:.0f} GPa", False),
             (Em, f"apatite, measured: {Em:.0f} GPa", True)]
    lx = xa + 16
    for v, txt, meas in rungs:
        o.append(H.line(s, xa, Y(v), lx - 4, Y(v), I["muted"], "leader"))
        o.append(H.label(s, lx, Y(v) + 4.5, txt, "label2", I["primary"]))
    for v, _, meas in rungs:
        o.append(dot(s, xa, Y(v), I["primary"], hollow=meas))
    # the steps, as arrows whose length is the log of the factor
    xs, tx = 520.0, 534.0
    steps = [(En, El, f"× α{H.sub('M', s)}/12 = 1/{12/aM:.2f}",
              ["Madelung sum over the whole lattice,", "and the true cell volume"]),
             (El, Ea, f"× {Ea/El:.2f}", ["dilution: the same Ca–O chemistry", "over more volume, 204 → 108 GJ m⁻³"]),
             (Ea, Em, f"× {Em/Ea:.3f}", ["polarizable O²⁻ and partial covalency:",
                                                                     "the one step the model lacks"])]
    for k, (a, b, f, why) in enumerate(steps):
        o.append(H.line(s, xs - 5, Y(a), xs + 5, Y(a), I["axis"], "leader"))
        o.append(H.arrow(s, p, xs, Y(a) + 2, xs, Y(b) - 1, "dim", w="ref"))
        ym = (Y(a) + Y(b)) / 2 + (14 if k == 2 else 0)
        o.append(H.label(s, tx, ym - 14, f, "label", I["primary"]))
        for j, w in enumerate(why):
            o.append(H.label(s, tx, ym + 2 + 15 * j, w, "label2", I["secondary"]))
    o.append(H.line(s, xs - 5, Y(Em), xs + 5, Y(Em), I["axis"], "leader"))
    # the whole factor, 1947 -> 114
    xb = 60
    o.append(path(f"M{xb+6},{Y(En):.1f} L{xb},{Y(En):.1f} L{xb},{Y(Em):.1f} L{xb+6},{Y(Em):.1f}", I["axis"], s(1.2)))
    ym = (Y(En) + Y(Em)) / 2
    o.append(H.label(s, xb - 10, ym, f"{En:.0f} → {Em:.0f}: a factor of {En/Em:.1f}", "label2", I["primary"], "middle",
                     f'transform="rotate(-90 {xb-10} {ym:.1f})"'))
    # section 0's calibrated 104 GPa: dashed, OFF the ladder (no mark on the axis, set to the right of the rungs)
    yc = Y(Ec)
    o.append(H.line(s, 410, yc, 500, yc, SER[0], "curve_multi", (6, 4)))
    o.append(H.label(s, 500, yc + 22, f"§0 ladder, calibrated backwards: {Ec:.0f} GPa", "label2", I["primary"], "end"))
    o.append(H.label(s, 500, yc + 38, "not a step: Module 2 §5’s measurement handed back", "label2", I["secondary"], "end"))
    aria = (f"A vertical logarithmic ladder of Young's modulus in GPa, read downward: a bare calcium-oxygen pair through E ~ k/r0 "
            f"gives {En:.0f}; a real CaO lattice costs alpha M over 12, 1 over {12/aM:.2f}, and lands on {El:.0f}; dilution "
            f"through apatite's phosphate framework, times {Ea/El:.2f}, gives the {Ea:.0f} that Proposition 2.2 predicts; "
            f"polarizable oxygen and partial covalency, times {Em/Ea:.2f}, reach the measured {Em:.0f}. Arrow lengths are the "
            f"logarithms of the factors; overall a factor of {En/Em:.1f}. A red dashed line at {Ec:.0f} GPa, off the ladder, "
            "is section 0's calibrated value: Module 2 section 5's measurement handed back.")
    return finish(VB, aria, s, o)


# ================================================================ svg #9  Fig. 8: four stages of the collagen load path
def wave(x0, span, y, amp, waves, n=160):
    return [(x0 + span * i / n, y + amp * math.sin(2 * math.pi * waves * i / n)) for i in range(n + 1)]


def arclen(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def rope(pts, s, w_out=7.0, w_in=4.0):
    d = dpath(pts)
    return (path(d, T["tendon"][1], s(w_out), extra='stroke-linecap="round"')
            + path(d, T["tendon"][0], s(w_in), extra='stroke-linecap="round"'))


def fig9():
    VB = (0, 0, 760, 226)
    s = H.Scale(VB[2], VB[3])
    p = "m0f9_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    bw, gap, y0, bh = 178.0, 8.0, 8.0, 150.0
    xs = [6 + i * (bw + gap) for i in range(4)]
    caps = ["1. at rest: crimped", "2. crimp pulled straight", "3. supercoil unwinds", "4. molecules slide"]
    for x, c in zip(xs, caps):
        o.append(rect(x, y0, bw, bh, BOX, I["rule"], 1.0, 6))
        o.append(H.label(s, x + bw / 2, y0 + bh + 20, c, "label2", I["primary"], "middle"))
    yc = y0 + 78
    # 1: crimp. Its contour length L is measured, and panel 2 draws a straight band of exactly that length.
    crimp = wave(xs[0] + 32, 92, yc, 13, 1.5)
    L = arclen(crimp)
    o.append(rope(crimp, s))
    o.append(H.label(s, xs[0] + bw / 2, y0 + 24, f"contour length {it('L')}", "label2", I["secondary"], "middle"))
    # 2: the same L, straight, pulled at both ends
    x2 = xs[1] + (bw - L) / 2
    o.append(rope([(x2, yc), (x2 + L, yc)], s))
    o.append(H.arrow(s, p, x2 - 3, yc, x2 - 18, yc, "force"))
    o.append(H.arrow(s, p, x2 + L + 3, yc, x2 + L + 18, yc, "force"))
    o.append(H.label(s, xs[1] + bw / 2, y0 + 24, f"same {it('L')}, crimp gone", "label2", I["secondary"], "middle"))
    for x in (x2, x2 + L):
        o.append(H.line(s, x, yc + 12, x, yc + 26, O["geometry"], "leader"))
    o.append(H.arrow(s, p, x2, yc + 19, x2 + L, yc + 19, "geometry", both=True))
    o.append(H.label(s, xs[1] + bw / 2, yc + 38, it("L"), "label2", I["primary"], "middle"))
    o.append(H.label(s, xs[1] + bw / 2, yc + 52, "a shape change,", "label2", I["secondary"], "middle"))
    o.append(H.label(s, xs[1] + bw / 2, yc + 67, "not a bond stretch", "label2", I["secondary"], "middle"))
    # 3: three strands whose pitch grows left to right (turns traded for length)
    x3a, x3b = xs[2] + 22, xs[2] + bw - 22
    n = 200
    lam = lambda u: 16 + 34 * u            # noqa: E731  local pitch, px
    ph, phs = 0.0, []
    for i in range(n + 1):
        u = i / n
        phs.append(ph)
        ph += 2 * math.pi * (x3b - x3a) / n / lam(u)
    for k in range(3):
        pts = [(x3a + (x3b - x3a) * i / n, yc + 11 * math.sin(phs[i] + 2 * math.pi * k / 3)) for i in range(n + 1)]
        o.append(path(dpath(pts), T["tendon"][1], s(2.6), extra='stroke-linecap="round"'))
    o.append(H.arrow(s, p, x3a - 3, yc, x3a - 16, yc, "force"))
    o.append(H.arrow(s, p, x3b + 3, yc, x3b + 16, yc, "force"))
    o.append(H.label(s, xs[2] + bw / 2, y0 + 24, "turns traded for length", "label2", I["secondary"], "middle"))
    o.append(H.label(s, xs[2] + bw / 2, yc + 38, "tight turns → loose turns", "label2", I["secondary"], "middle"))
    # 4: staggered molecules sliding through water and cross-links
    x4 = xs[3] + 14
    rw, rh, Dp = 54.0, 9.0, 34.0           # rod length, height, D stagger (px)
    yt, yb = yc - 16, yc + 16
    for j in range(2):
        o.append(rect(x4 + j * (rw + 8), yt - rh / 2, rw, rh, T["tendon"][0], T["tendon"][1], 1.4, rh / 2))
        o.append(rect(x4 + Dp + j * (rw + 8), yb - rh / 2, rw, rh, T["tendon"][0], T["tendon"][1], 1.4, rh / 2))
    for i in range(10):
        o.append(ca_dot(x4 + 4 + i * 14.6, yc, 2.6))
    for xx in (x4 + 46, x4 + 104):
        o.append(H.line(s, xx, yt + rh / 2, xx, yb - rh / 2, I["primary"], "ref"))
    o.append(H.arrow(s, p, x4 + 2 * rw + 10, yt, x4 + 2 * rw + 26, yt, "force"))
    o.append(H.arrow(s, p, x4 + Dp - 2, yb, x4 + Dp - 18, yb, "force"))
    for x in (x4, x4 + Dp):
        o.append(H.line(s, x, yb + 10, x, yb + 22, O["geometry"], "leader"))
    o.append(H.arrow(s, p, x4, yb + 16, x4 + Dp, yb + 16, "geometry", both=True))
    o.append(H.label(s, x4 + Dp + 8, yb + 21, it("D") + " = 67 nm stagger", "label2", I["primary"]))
    o.append(H.label(s, xs[3] + bw / 2, y0 + 24, "slip through a shear layer", "label2", I["secondary"], "middle"))
    lg, _ = legend(s, 10, 220, [(sw_rect(T["tendon"][0], T["tendon"][1]), "collagen molecule"),
                                (lambda x, y: ca_dot(x + 7, y - 5, 3), "water"),
                                (sw_line(I["primary"], 1.4), "cross-link"),
                                (sw_line(O["force"], 2.5), "pull"),
                                (sw_line(O["geometry"], 2.0), "length")], gap=18)
    o.append(lg)
    aria = ("Four schematic panels of a collagen fibril under increasing tension. 1: a crimped wavy molecule at rest, contour "
            "length L. 2: the same molecule pulled straight by red end forces, drawn exactly as long as the crimp's contour, "
            "so the shape changed and no bond stretched. 3: three helical strands whose turns loosen from left to right as "
            "the supercoil unwinds, trading turns for length. 4: two rows of rod-shaped molecules offset by the 67 nanometre "
            "D stagger, sliding in opposite directions through a layer of water and cross-links between them.")
    return finish(VB, aria, s, o)


# ================================================================ svg #12  Fig. 11: SERCA and its ledger
def ledger():
    """Line 690 (dG0' at 310 K), 702-707 (concentrations, -62.5 / -52.7), 752 (climb +23.75 per ion), 760-765.
    The m-ion costs are m x 23.75, the per-ion value line 752 states: 3 x 23.75 = 71.25, which the table prints as 71.3
    (line 764). Unrounded, 3 RgT ln(1e4) = 71.249."""
    dg0 = -30.90
    q_rest, q_fat = 13e-6 * 2.0e-3 / 5.5e-3, 70e-6 * 15e-3 / 5.0e-3
    g_rest, g_fat = -(dg0 + RGT * math.log(q_rest)), -(dg0 + RGT * math.log(q_fat))
    climb = round(RGT * math.log(1e-3 / 0.1e-6), 2)
    assert round(g_rest, 1) == 62.5 and round(g_fat, 1) == 52.7 and climb == 23.75
    return g_rest, g_fat, 2 * climb, 3 * climb, climb


def f1(v):
    """One decimal, half up (71.25 -> 71.3, as the module prints it)."""
    from decimal import ROUND_HALF_UP, Decimal
    return str(Decimal(repr(round(v, 9))).quantize(Decimal("0.1"), ROUND_HALF_UP))


def fig12():
    VB = (0, 0, 760, 344)
    s = H.Scale(VB[2], VB[3])
    p = "m0f12_"
    g_rest, g_fat, c2, c3, climb = ledger()
    assert (f1(g_rest), f1(g_fat), f1(c2), f1(c3)) == ("62.5", "52.7", "47.5", "71.3")
    o = [f'<defs>{H.markers(p, s)}{ca_marker(p, s)}</defs>']
    # ---- left: the pump in the SR membrane
    o.append(H.label(s, 175, 20, "the pump, in place", "label", I["primary"], "middle"))
    L0, L1, ym0, ym1, yl = 14.0, 336.0, 150.0, 166.0, 284.0
    o.append(rect(L0, ym1, L1 - L0, yl - ym1, BOX, I["rule"], 1.0, 0))
    o.append(rect(L0, ym0, L1 - L0, ym1 - ym0, T["fat"][0], T["fat"][1], 1.0, 0))
    o.append(H.label(s, L0 + 8, 48, "cytosol", "label", I["primary"]))
    o.append(H.label(s, L0 + 8, 66, f"free [{ca()}] = 0.1 µM", "label2", I["secondary"]))
    o.append(H.label(s, L0 + 8, yl - 12, "SR lumen", "label", I["primary"]))
    o.append(H.label(s, L0 + 84, yl - 12, f"free [{ca()}] = 1 mM: 10⁴ times higher", "label2", I["secondary"]))
    o.append(H.label(s, L1 - 6, ym0 - 6, "SR membrane", "label2", I["secondary"], "end"))
    for cx_, cy_ in ((60, 112), (262, 70), (300, 124)):
        o.append(ca_dot(cx_, cy_))
    rnd = random.Random(7)
    for k in range(24):
        cx_ = L0 + 16 + (k % 12) * 26 + rnd.uniform(-5, 5)
        cy_ = ym1 + 20 + (k // 12) * 32 + rnd.uniform(-5, 5)
        if not 146 < cx_ < 204:
            o.append(ca_dot(cx_, cy_))
    px0, pw = 150.0, 50.0
    o.append(rect(px0, ym0 - 22, pw, ym1 - ym0 + 44, "#fff", I["primary"], 1.4, 10))
    o.append(H.label(s, px0 + pw / 2, (ym0 + ym1) / 2 + 5, "SERCA", "label2", I["primary"], "middle"))
    xm = px0 + pw / 2
    o.append(ca_arrow(s, p, xm, 70, xm, ym0 - 26))
    o.append(ca_arrow(s, p, xm, ym1 + 24, xm, ym1 + 62))
    o.append(H.label(s, xm - 10, 92, f"2 {ca()}", "label2", I["primary"], "end"))
    o.append(H.arrow(s, p, 262, 104, px0 + pw + 4, ym0 - 10, "dim", w="ref"))
    o.append(H.label(s, 266, 104, "ATP", "label2", I["primary"]))
    o.append(H.arrow(s, p, px0 + pw + 4, ym1 + 10, 240, 206, "dim", w="ref"))
    o.append(H.label(s, 246, 214, "ADP + Pᵢ", "label2", I["primary"]))
    lg, _ = legend(s, L0, 334, [(sw_ca, f"{ca()} ion"), (sw_line(T["fluid"][1], 2.5), f"{ca()} carried"),
                                (sw_rect(T["fat"][0], T["fat"][1]), "membrane"), (sw_rect(BOX, I["rule"]), "lumen")], gap=20)
    o.append(lg)
    # ---- right: the ledger, kJ per mole of ATP
    ax = Ax((440, 52, 744, 240), (0, 4), (0, 90))
    o += axes(s, ax, [], [(v, f"{v}") for v in (0, 20, 40, 60, 80)], None, "energy (kJ mol⁻¹)", ylab_x=398)
    o.append(H.label(s, 592, 20, "what it earns, what it costs", "label", I["primary"], "middle"))
    bars = [(g_rest, SER[3], "one ATP", "at rest"), (g_fat, SER[2], "one ATP", "fatigued"),
            (c2, T["fluid"][1], f"2 {ca()}", "the climb"), (c3, T["fluid"][1], f"3 {ca()}", "the climb")]
    hv = []
    for i, (v, col, a, b) in enumerate(bars):
        xc = ax.X(i + 0.5)
        o.append(f'<rect x="{xc-26:.2f}" y="{ax.Y(v):.2f}" width="52" height="{ax.y0-ax.Y(v):.2f}" fill="{col}" '
                 f'fill-opacity="{1.0 if i < 2 else 0.85}"/>')
        o.append(H.label(s, xc, ax.y0 + 18, a, "label2", I["primary"], "middle"))
        o.append(H.label(s, xc, ax.y0 + 34, b, "label2", I["secondary"], "middle"))
        o.append(H.label(s, xc, ax.y0 + 52, f1(v), "label", I["primary"], "middle"))
        hv.append([xc, ax.Y(v), f"{a} {b}: {f1(v)} kJ/mol"])
    for v, col, dash, i0 in ((g_rest, SER[3], (7, 4), 0), (g_fat, SER[2], (3, 3), 1)):
        o.append(H.line(s, ax.X(i0 + 0.5) + 26, ax.Y(v), ax.x1, ax.Y(v), col, "curve_multi", dash))
    o.append(H.label(s, ax.x1, ax.Y(c3) - 26, "above both budgets:", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.x1, ax.Y(c3) - 10, f"3 {ca()} cannot be paid for", "label2", I["primary"], "end"))
    o += plegend(s, 452, 316, [(SER[3], (7, 4), f"ATP at rest, {f1(g_rest)}"), (SER[2], (3, 3), f"ATP fatigued, {f1(g_fat)}")],
                 gap=14)
    o.append(f'<rect x="{454}" y="{326}" width="22" height="10" fill="{T["fluid"][1]}" fill-opacity="0.85"/>')
    o.append(H.label(s, 483, 336, f"cost of the {ca()} climb, {climb:.2f} per ion", "label2", I["primary"]))
    aria = ("Two panels. Left: the SERCA pump spans the sarcoplasmic-reticulum membrane and carries two calcium ions from the "
            "cytosol, free calcium 0.1 micromolar, into the lumen, free calcium 1 millimolar, ten thousand times higher, while "
            "one ATP is split to ADP and phosphate. Right: bars in kilojoules per mole. One ATP supplies 62.5 at rest and 52.7 "
            "when fatigued, drawn as green and orange dashed budget lines. Lifting two calcium ions costs 47.5, below both "
            "budgets; lifting three costs 71.3, above both, so three cannot be paid for.")
    return finish(VB, aria, s, o, H.hover_attr(ax.box, hv))


# ================================================================ svg #13  Fig. 12: one chain, three force laws
LP, LC = 14.5e-9, 300e-9                          # line 840
B_K = 2 * LP                                       # Kuhn length, line 840


def f_wlc(u):
    return KBT / LP * (u + 1 / (4 * (1 - u) ** 2) - 0.25) * 1e12        # line 858, pN


def f_gauss(u):
    return 3 * KBT / B_K * u * 1e12                                     # Prop. 4.2 with N b = L_c, pN


def f_fjc(u):
    """Invert the Langevin law x/L = coth(beta) - 1/beta (line 856) by bisection; f = beta kBT / b."""
    if u <= 0:
        return 0.0
    lo, hi = 1e-9, 1e4
    for _ in range(200):
        m = (lo + hi) / 2
        if 1 / math.tanh(m) - 1 / m < u:
            lo = m
        else:
            hi = m
    return lo * KBT / B_K * 1e12


def chain_coil(n=10, target=0.31):
    """A 2-D 10-segment walk with |R| / Lc within 0.005 of `target`, no two non-adjacent joints closer than 0.55 b."""
    rnd = random.Random(11)
    for _ in range(200000):
        pts, a = [(0.0, 0.0)], rnd.uniform(0, 2 * math.pi)
        for _ in range(n):
            a += rnd.uniform(-2.2, 2.2)
            x, y = pts[-1]
            pts.append((x + math.cos(a), y + math.sin(a)))
        R = math.hypot(*pts[-1]) / n
        if abs(R - target) > 0.005:
            continue
        if any(math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]) < 0.55 for i in range(n + 1) for j in range(i + 2, n + 1)):
            continue
        return pts
    raise RuntimeError("no coil found")


def chain_taut(n=10, frac=0.97):
    th = math.acos(frac)
    pts = [(0.0, 0.0)]
    for i in range(n):
        x, y = pts[-1]
        pts.append((x + math.sin(th) * (1 if i % 2 else -1), y + math.cos(th)))
    return pts


def place(pts, b, x0, y0):
    """Scale by b and rotate so the end-to-end vector points straight up from (x0, y0)."""
    ex, ey = pts[-1]
    a = math.atan2(ey, ex) - math.pi / 2
    ca_, sa = math.cos(-a), math.sin(-a)
    return [(x0 + b * (x * ca_ - y * sa), y0 - b * (x * sa + y * ca_)) for x, y in pts]


def draw_chain(s, q):
    o = [path(dpath(q), I["secondary"], s(2.6), extra='stroke-linejoin="round"')]
    for x, y in q:
        o.append(circ(x, y, 3.6, "#fff", I["primary"], 1.2))
    return "".join(o)


def fig13():
    VB = (0, 0, 760, 316)
    s = H.Scale(VB[2], VB[3])
    p = "m0f13_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # ---- left: one chain, two extensions (identical segment lengths)
    o.append(H.label(s, 180, 18, "the same chain, two extensions", "label", I["primary"], "middle"))
    b = 21.0
    coil, taut = chain_coil(), chain_taut()
    seg = lambda q: [math.hypot(q[i + 1][0] - q[i][0], q[i + 1][1] - q[i][1]) for i in range(len(q) - 1)]  # noqa: E731
    assert all(abs(v - 1) < 1e-9 for v in seg(coil) + seg(taut))
    Rc, Rt = math.hypot(*coil[-1]) / 10, math.hypot(*taut[-1]) / 10
    assert abs(Rc - 0.31) < 0.006 and abs(Rt - 0.97) < 1e-9
    yb = 250.0
    qc, qt = place(coil, b, 76, 218), place(taut, b, 236, yb)
    lc = f"{it('L')}{H.sub('c', s, 'label2')}"
    # coiled: the end-to-end vector R drawn from the first joint to the last, over the chain (white halo)
    (cx0, cy0), (cx1, cy1) = qc[0], qc[-1]
    o.append(draw_chain(s, qc))
    o.append(f'<line x1="{cx0:.1f}" y1="{cy0:.1f}" x2="{cx1:.1f}" y2="{cy1:.1f}" stroke="#fff" stroke-width="{s(5):.2f}"/>')
    o.append(H.arrow(s, p, cx0, cy0, cx1, cy1, "geometry"))
    xr = max(x for x, _ in qc) + 10
    o.append(H.label(s, xr, (cy0 + cy1) / 2 + 5, f"{it('R')} ≈ {Rc:.2f} {lc}", "label2", I["primary"]))
    o.append(H.label(s, 84, 262, "coiled: many shapes", "label2", I["primary"], "middle"))
    o.append(H.label(s, 84, 278, "high entropy", "label2", I["secondary"], "middle"))
    # taut: R offset beside the chain, with short guides
    o.append(draw_chain(s, qt))
    (tx0, ty0), (tx1, ty1) = qt[0], qt[-1]
    dx = 24
    o.append(H.line(s, tx0 + 6, ty0, tx0 + dx + 5, ty0, O["geometry"], "leader"))
    o.append(H.line(s, tx1 + 6, ty1, tx1 + dx + 5, ty1, O["geometry"], "leader"))
    o.append(H.arrow(s, p, tx0 + dx, ty0, tx1 + dx, ty1, "geometry"))
    o.append(H.label(s, tx0 + dx + 10, (ty0 + ty1) / 2 - 12, f"{it('R')} = {Rt:.2f} {lc}", "label2", I["primary"]))
    o.append(H.label(s, tx0 + dx + 10, (ty0 + ty1) / 2 + 12, "taut: few shapes", "label2", I["primary"]))
    o.append(H.label(s, tx0 + dx + 10, (ty0 + ty1) / 2 + 28, "low entropy", "label2", I["secondary"]))
    o.append(H.arrow(s, p, tx1, ty1 - 6, tx1, ty1 - 28, "force"))
    o.append(H.arrow(s, p, tx0, ty0 + 6, tx0, ty0 + 26, "force"))
    o.append(H.label(s, tx1 - 10, ty1 - 14, it("f"), "label", I["primary"], "end"))
    o.append(H.label(s, tx0 - 10, ty0 + 22, it("f"), "label", I["primary"], "end"))
    o.append(H.label(s, 180, 304, f"{it('f')} = −{it('T')} ∂{it('S')}/∂{it('x')}: the pull is the entropy it costs", "label2",
                     I["primary"], "middle"))
    o.append(H.label(s, 84, 60, "ten rigid segments,", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 84, 76, f"each one Kuhn length {it('b')}", "label2", I["secondary"], "middle"))
    # ---- right: f(x/L) for one tropocollagen molecule
    ax = Ax((440, 52, 744, 250), (0, 1), (0, 3))
    o.append(H.label(s, 592, 16, "three force laws, one chain", "label", I["primary"], "middle"))
    u10 = 0.001
    while f_gauss(u10) / f_wlc(u10) > 0.9:
        u10 += 0.0001
    assert abs(u10 - 0.17) < 0.005
    o.append(f'<rect x="{ax.x0:.2f}" y="{ax.top:.2f}" width="{ax.X(0.17)-ax.x0:.2f}" height="{ax.y0-ax.top:.2f}" '
             f'fill="{SER[2]}" opacity="0.14"/>')
    o += axes(s, ax, [(v, t) for v, t in ((0, "0"), (0.25, "0.25"), (0.5, "0.5"), (0.75, "0.75"), (1, "1"))],
              [(v, f"{v}") for v in (0, 1, 2, 3)], f"extension {it('x')} / {it('L')}{H.sub('c', s)}",
              f"force {it('f')} (pN)", ylab_x=408, xlab_dy=42)
    us = [i / 110 for i in range(0, 110)]
    laws = [("worm-like chain", f_wlc, SER[0], None), ("freely jointed", f_fjc, SER[1], None),
            ("Gaussian limit", f_gauss, SER[2], (7, 4))]
    for name, fn, col, dash in laws:
        pts = []
        for u in us:
            v = fn(u)
            if v > 3.0:
                lo, hi = pts and (u - 1 / 110) or 0.0, u          # close the curve exactly at the 3 pN frame
                for _ in range(60):
                    lo, hi = ((lo + hi) / 2, hi) if fn((lo + hi) / 2) < 3.0 else (lo, (lo + hi) / 2)
                pts.append((ax.X(lo), ax.Y(fn(lo))))
                break
            pts.append((ax.X(u), ax.Y(v)))
        da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
        o.append(f'<polyline points="{" ".join(f"{a:.2f},{c:.2f}" for a, c in pts)}" fill="none" stroke="{col}" '
                 f'stroke-width="{s(H.PX["curve_multi"]):.2f}" stroke-linejoin="round"{da}/>')
    # direct labels (ink), each with a leader in its series colour to its own curve
    xw = 0.80
    o.append(H.label(s, ax.X(xw) - 12, ax.Y(2.70) + 4, "worm-like chain", "label2", I["primary"], "end"))
    o.append(H.line(s, ax.X(xw) - 10, ax.Y(2.70), ax.X(xw) - 1, ax.Y(f_wlc(xw)) - 2, SER[0], "leader"))
    o.append(H.label(s, ax.X(1.0), ax.Y(0.80), "freely", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(1.0), ax.Y(0.80) + 15, "jointed", "label2", I["primary"], "end"))
    o.append(H.line(s, ax.X(0.90), ax.Y(0.80) - 12, ax.X(0.885), ax.Y(f_fjc(0.885)) + 2, SER[1], "leader"))
    o.append(H.label(s, ax.X(1.0), ax.Y(0.10), "Gaussian limit", "label2", I["primary"], "end"))
    fh = f_wlc(0.5)
    o.append(dot(s, ax.X(0.5), ax.Y(fh), SER[0]))
    o.append(H.line(s, ax.X(0.5), ax.Y(fh) - 6, ax.X(0.45), ax.Y(1.0), I["muted"], "leader"))
    o.append(H.label(s, ax.X(0.45), ax.Y(1.0) - 6, f"{fh:.2f} pN at half extension", "label2", I["primary"], "middle"))
    o += plegend(s, ax.x0 - 24, ax.top - 12, [(SER[0], None, "worm-like"), (SER[1], None, "freely jointed"),
                                             (SER[2], (7, 4), "Gaussian")], gap=10)
    o.append(H.label(s, ax.X(0.19), ax.Y(2.45), "← shaded: Gaussian law", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(0.19), ax.Y(2.45) + 16, "within 10 % of the WLC,", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(0.19), ax.Y(2.45) + 32, f"to {it('x')}/{it('L')}{H.sub('c', s, 'label2')} = 0.17",
                     "label2", I["secondary"]))
    hv = []
    for u in [i / 100 for i in range(0, 96)]:
        ys, parts = [], []
        for name, fn, _, _ in laws:
            v = fn(u)
            if v <= 3.0:
                ys.append(ax.Y(v))
                parts.append(f"{name.split()[0]} {v:.2f}")
        hv.append([ax.X(u), ys, f"x/L = {u:.2f}: " + ", ".join(parts) + " pN"])
    aria = ("Two panels. Left: one chain of ten rigid segments drawn twice with the same segment lengths. Coiled, its "
            f"end-to-end vector R is {Rc:.2f} of the contour length and many shapes achieve it: high entropy. Pulled taut by "
            f"forces f at both ends, R is {Rt:.2f} of the contour length and few shapes do: low entropy; f = -T dS/dx. Right: "
            "force against extension x/Lc for one tropocollagen molecule (Lc 300 nm, persistence length 14.5 nm): the "
            "worm-like chain and the freely jointed chain both diverge near full extension, the Gaussian line keeps a "
            "constant slope; the shaded band to x/Lc = 0.17 is where the Gaussian law is within 10 percent of the worm-like "
            f"chain. At half extension the worm-like chain needs {fh:.2f} pN.")
    return finish(VB, aria, s, o, H.hover_attr(ax.box, hv))


# ================================================================ svg #23  Fig. 21: Gly-X-Y and the 300 nm
def fig23():
    VB = (0, 0, 760, 262)
    s = H.Scale(VB[2], VB[3])
    p = "m0f23_"
    rise, n_res, tail = 0.286, 1014, 10.0           # line 1324, 1330, 1332
    L_helix = n_res * rise
    assert abs(L_helix - 290.0) < 0.01 and abs(3 * rise - 0.858) < 1e-9
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(H.label(s, 190, 18, "one chain: Gly-X-Y", "label", I["primary"], "middle"))
    S = 100.0                                        # px per nm along the axis
    x0, yc, A = 56.0, 140.0, 26.0
    cols = [(SER[1], "glycine, every third residue"), (I["secondary"], "X, usually proline"),
            (SER[0], "Y, usually hydroxyproline")]
    tilt = math.radians(25)                          # view slightly off the helix side, so X and Y separate
    pts = [(x0 + i * rise * S, yc + A * math.cos(2 * math.pi * i / 3 + tilt)) for i in range(10)]
    o.append(path(dpath(pts), I["muted"], s(3.0), extra='stroke-linejoin="round"'))
    ya = yc + A + 18                                 # the shared axis of the three chains, on the glycine side
    o.append(H.line(s, x0 - 30, ya, pts[-1][0] + 30, ya, O["dim"], "ref", H.DASH_REF))
    o.append(H.label(s, pts[-1][0] + 30, ya + 20, "the axis the three chains share", "label2", I["secondary"], "end"))
    for i, (x, y) in enumerate(pts):
        o.append(circ(x, y, 10, cols[i % 3][0], "#fff", 1.4))
    yd = ya + 30
    g0, g1 = pts[0][0], pts[3][0]
    for x in (g0, g1):
        o.append(H.line(s, x, pts[0][1] + 12, x, yd + 7, O["geometry"], "leader"))
    o.append(H.arrow(s, p, g0, yd, g1, yd, "geometry", both=True))
    o.append(H.label(s, (g0 + g1) / 2, yd + 22, f"3 residues = {3*rise:.3f} nm", "label2", I["primary"], "middle"))
    o.append(H.label(s, (g0 + g1) / 2, yd + 38, f"rise {rise} nm per residue", "label2", I["secondary"], "middle"))
    for i, t in ((0, "Gly"), (1, "X"), (2, "Y")):
        x, y = pts[i]
        if i == 0:
            o.append(H.label(s, x - 14, y + 5, t, "label2", I["primary"], "end"))
        else:
            o.append(H.label(s, x, y - 16, t, "label2", I["primary"], "middle"))
    lg = [sw_dot(c, "#fff")(16, 44 + 18 * k) + H.label(s, 35, 44 + 18 * k, t, "label2", I["secondary"]) for k, (c, t) in enumerate(cols)]
    o += lg
    # ---- right: the arithmetic
    rx, rw = 428.0, 318.0
    o.append(H.label(s, rx + rw / 2, 18, "§4’s contour length, rebuilt", "label", I["primary"], "middle"))
    o.append(rect(rx, 32, rw, 156, BOX, I["rule"], 1.0, 6))
    rows = [(f"{n_res} residues in the α chain", I["secondary"], False),
            (f"× {rise} nm rise per residue", I["secondary"], False),
            (f"= {L_helix:.1f} nm of triple helix", I["primary"], True),
            (f"+ {tail:.0f} nm of telopeptide tails", I["secondary"], False),
            (f"= {L_helix + tail:.0f} nm: the contour length §4 used", I["primary"], True)]
    for k, (t, col, rule) in enumerate(rows):
        y = 58 + 28 * k
        o.append(H.label(s, rx + 14, y, t, "label", col))
        if rule:
            o.append(H.line(s, rx + 12, y - 22, rx + rw - 12, y - 22, I["rule"], "leader"))
    o.append(H.label(s, rx, 216, "Gly-X-Y also predicts glycine = 1/3 = 33.3 % of residues;", "label2", I["primary"]))
    o.append(H.label(s, rx, 234, "amino-acid analysis measures 33 %.", "label2", I["primary"]))
    aria = ("Two panels. Left: ten residues of one collagen alpha chain on a helix of three residues per turn, coloured by "
            "position in the Gly-X-Y repeat: blue glycine every third residue, grey X (usually proline), red Y (usually "
            "hydroxyproline). All four glycines sit on the same side, next to the dashed axis the three chains share. Three "
            "residues span 0.858 nm; the rise is 0.286 nm per residue. Right: 1014 residues times 0.286 nm is 290.0 nm of "
            "triple helix; plus 10 nm of telopeptide tails is 300 nm, the contour length section 4 used. Gly-X-Y also "
            "predicts 33.3 percent glycine; analysis measures 33 percent.")
    return finish(VB, aria, s, o)


# ================================================================ svg #25  Fig. 23: the bilayer is a capacitor
def counts():
    """Line 1372-1376 (eps_r 2.2, d 2.5 nm), 1378 (measured 1.0), 1380 (r 25 um, -90 mV), 1384-1386 (table)."""
    ca_calc = EPS0 * 2.2 / 2.5e-9 * 100                 # uF per cm^2
    r, V, cK = 25e-6, 0.090, 0.140
    vol_L = 4 / 3 * math.pi * r ** 3 * 1e3
    nK = cK * vol_L * N_A
    q_meas = 1.0e-2 * V * 4 * math.pi * r ** 2 / E_CHG    # the table's count uses the MEASURED 1.0 uF/cm^2
    assert round(ca_calc, 2) == 0.78 and round(1 / ca_calc, 2) == 1.28 and round(vol_L * 1e12) == 65
    assert round(nK / 1e12, 1) == 5.5 and round(q_meas / 1e7, 1) == 4.4 and round(q_meas / nK * 1e6, 1) == 8.0
    return ca_calc, nK, q_meas


def fig25():
    VB = (0, 0, 760, 304)
    s = H.Scale(VB[2], VB[3])
    p = "m0f25_"
    ca_calc, nK, q = counts()
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # ---- left: the bilayer, drawn to scale (20 px per nm: core 2.5 nm, whole bilayer 5 nm)
    o.append(H.label(s, 170, 18, "the bilayer is a capacitor", "label", I["primary"], "middle"))
    S = 20.0
    x0, x1 = 16.0, 252.0
    yt = 82.0
    ycore0, ycore1, yb = yt + 1.25 * S, yt + 3.75 * S, yt + 5 * S
    o.append(rect(x0, 34, x1 - x0, yt - 34, T["fluid"][0], None, 0, 0, 'opacity="0.45"'))
    o.append(rect(x0, yb, x1 - x0, 50, T["fluid"][0], None, 0, 0, 'opacity="0.45"'))
    o.append(rect(x0, ycore0, x1 - x0, ycore1 - ycore0, T["fat"][0], None, 0, 0, 'opacity="0.55"'))
    n = 10
    for i in range(n):
        x = x0 + (i + 0.5) * (x1 - x0) / n
        for yh, sg in ((yt + 9, 1), (yb - 9, -1)):
            yend = (ycore0 + ycore1) / 2 - sg * 2
            for dx in (-3, 3):
                o.append(H.line(s, x + dx, yh + sg * 6, x + dx, yend, T["fat"][1], "ref"))
            o.append(circ(x, yh, 7, T["fat"][0], T["fat"][1], 1.2))
    for i in range(6):
        x = x0 + (i + 0.5) * (x1 - x0) / 6
        o.append(H.label(s, x, yt - 8, "+", "label", I["primary"], "middle"))
        o.append(H.label(s, x, yb + 20, "−", "label", I["primary"], "middle"))
    o.append(H.label(s, x0 + 6, 50, "outside", "label2", I["primary"]))
    o.append(H.label(s, x0 + 6, yb + 44, "inside (cytosol)", "label2", I["primary"]))
    xd = x1 + 12
    for y in (ycore0, ycore1):
        o.append(H.line(s, x1 - 4, y, xd + 5, y, O["geometry"], "leader"))
    o.append(H.arrow(s, p, xd, ycore0, xd, ycore1, "geometry", both=True))
    o.append(H.label(s, xd + 8, (ycore0 + ycore1) / 2 - 3, f"{it('d')} = 2.5 nm", "label2", I["primary"]))
    o.append(H.label(s, xd + 8, (ycore0 + ycore1) / 2 + 13, "hydrocarbon", "label2", I["secondary"]))
    o.append(H.label(s, xd + 8, (ycore0 + ycore1) / 2 + 29, "core", "label2", I["secondary"]))
    xd2 = xd + 98
    for y in (yt, yb):
        o.append(H.line(s, xd2 - 5, y, xd2 + 5, y, O["dim"], "leader"))
    o.append(H.line(s, xd2, yt, xd2, yb, O["dim"], "ref", extra=f'marker-start="url(#{p}a_dim)" marker-end="url(#{p}a_dim)"'))
    o.append(H.label(s, xd2 + 8, (yt + yb) / 2 + 5, "5 nm", "label2", I["secondary"]))
    o.append(H.label(s, 170, 256, f"{it('C')}/{it('A')} = ε₀ε{H.sub('r', s)}/{it('d')} = {ca_calc:.2f} µF cm⁻²", "label",
                     I["primary"], "middle"))
    o.append(H.label(s, 170, 274, f"ε{H.sub('r', s, 'label2')} = 2.2; measured 1.0, a factor {1/ca_calc:.2f}", "label2",
                     I["secondary"], "middle"))
    lg, _ = legend(s, 16, 296, [(sw_rect(T["fat"][0], T["fat"][1]), "lipid head and tails"),
                                (sw_rect(T["fluid"][0], None, 0.45), "water")], gap=16)
    o.append(lg)
    # ---- right: the two counts on a log axis
    o.append(H.label(s, 590, 18, "and how little charge it takes", "label", I["primary"], "middle"))
    ax = Ax((500, 40, 744, 236), (0, 2), (1e6, 1e13), ylog=True)
    o += axes(s, ax, [], [(10.0 ** e, f"10{sup(str(e))}") for e in range(6, 14)], None, "count of ions", ylab_x=448)
    pts = [(0.5, nK, "K⁺ inside the cell", "140 mM in 65 pL"), (1.5, q, "ions separated", "to hold −90 mV")]
    hv = []
    for xv, v, a, b in pts:
        xc, yv = ax.X(xv), ax.Y(v)
        o.append(H.line(s, ax.x0, yv, xc, yv, I["muted"], "leader", H.DASH_REF))
        o.append(dot(s, xc, yv, SER[0], r=5))
        o.append(H.label(s, xc, yv - 12, sci(v), "label2", I["primary"], "middle"))
        o.append(H.label(s, xc, ax.y0 + 20, a, "label2", I["primary"], "middle"))
        o.append(H.label(s, xc, ax.y0 + 36, b, "label2", I["secondary"], "middle"))
        hv.append([xc, yv, f"{a}: {sci(v)}"])
    xb = ax.x1 - 10
    y1, y2 = ax.Y(nK), ax.Y(q)
    o.append(path(f"M{xb-6},{y1:.1f} L{xb},{y1:.1f} L{xb},{y2:.1f} L{xb-6},{y2:.1f}", I["axis"], s(1.2)))
    ppm = q / nK * 1e6
    o.append(H.label(s, ax.X(1.5), (y1 + y2) / 2 - 4, f"ratio {ppm:.1f}", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(1.5), (y1 + y2) / 2 + 12, "parts per million", "label2", I["primary"], "middle"))
    aria = ("Two panels. Left: a lipid bilayer drawn to scale, two leaflets of head groups around a 2.5 nm hydrocarbon core, "
            "5 nm overall, with plus charges on the outside face and minus charges on the inside face: a capacitor, C over A "
            f"= epsilon zero epsilon r over d = {ca_calc:.2f} microfarad per square centimetre against a measured 1.0, a factor "
            f"{1/ca_calc:.2f}. Right: on a logarithmic axis, the cell holds {sci(nK)} potassium ions (140 mM in 65 pL) and "
            f"holding minus 90 mV separates {sci(q)} ions: a ratio of {ppm:.1f} parts per million.")
    return finish(VB, aria, s, o, H.hover_attr(ax.box, hv))


FIGS = {
    2: ("Three-panel zoom. Left: a shaded femur with head, neck and c", fig2),
    3: ("Vertical logarithmic ladder of concentration in the body, fr", fig3),
    4: ("One vertical logarithmic energy axis read twice: kilojoules ", fig4),
    8: ("A logarithmic ladder descending from 1947 gigapascals for a ", fig8),
    9: ("Four schematic panels of a collagen fibril under increasing ", fig9),
    12: ("Two panels. Left: a schematic of the sarcoplasmic reticulum ", fig12),
    13: ("Two panels. Left: the same polymer chain drawn twice - coile", fig13),
    23: ("Two panels. Left: ten residues of one collagen chain drawn a", fig23),
    25: ("Two panels. Left: a lipid bilayer drawn with its two leaflet", fig25),
}
