"""Module 5, group `schematic`: block diagrams and schematic problem figures in the house style.

svg #4 (pipeline), #22 (size-principle onion), #31 (Hill model), #41 (roadmap) are main-text
figures (760 px); #46 (C5), #49 (C8), #50 (C9), #76 (K8) are problem figures (400 px).
Every number is computed here from the values module05.html states.
"""
import html
import math
import re
from pathlib import Path

import house as H

T, O, I = H.TISSUE, H.OVERLAY, H.INK
BOX = "#f7f4ef"
KIT = Path(__file__).resolve().parents[2]          # anatomy_kit/
NIH_ARM = KIT / "svg_paths" / "nih_arm_bones.svg"

# NIH BioArt 208 art landmarks (wrist and Winter fraction as in sample/build_samples.py F22)
ART_WRIST = (19.5, 291.5)      # wrist in the art
# Elbow axis ON the forearm bones (the author, pilot review): proximal tips measured on the art (Chrome getPointAtLength,
# 2000 samples): path 6 (ulna) top y 158.1 at x 35.4-46.4, path 5 (radius) top y 161.4 at x 46.8-60.4. Chosen point:
# mid-way across the two proximal ends (x 47.9, y 158), then 1.5 cm (8.2 art units at 5.43 units/cm) distal along the
# forearm axis, so the mark sits on bone in the trochlear-notch / radial-head region. A first try at 0.5 cm still sat on
# the bone tip. The art has no joint profile, so the exact depth is a choice.
ART_E = (46.2, 166.0)
FOREARM_FRAC, H_REF_M = 0.146, 1.75


def it(t):
    return f'<tspan font-style="italic">{t}</tspan>'


def box(s, x, y, w, h, accent=None):
    o = f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="6" fill="{BOX}" stroke="{I["rule"]}" stroke-width="1"/>'
    if accent:
        o += f'<rect x="{x:.2f}" y="{y:.2f}" width="5" height="{h:.2f}" rx="2" fill="{accent}"/>'
    return o


def node(s, x, y, r, sym):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{I["axis"]}" stroke-width="{s(1.4):.2f}"/>'
            + H.label(s, x, y + s(6), sym, "label", I["primary"], "middle"))


def finish(vb, aria, s, body, extra=""):
    return H.svg_open(vb, html.escape(aria), s, extra) + "".join(body) + "</svg>"


# ---------------------------------------------------------------- svg #4: the module pipeline (ex_block, approved)
def fig4():
    VB = (0, 8, 760, 140)                          # ex_block 0 0 760 190, tightened to the content (u stays 1)
    s = H.Scale(VB[2], VB[3])
    p = "m5f4_"
    stages = [("neural drive", "u(t)", "electrical (nerve)", "§3–§4", O["neural"]),
              ("activation", "a(t)", "chemical (Ca²⁺)", "§5", I["rule"]),
              ("muscle force", "F", "mechanical", "§2, §6–§7", O["force"]),
              ("joint torque", "τ", "", "§8", I["rule"])]
    bw, bh, gap, y = 130, 74, 73, 40
    o = [f'<defs>{H.markers(p, s)}</defs>']
    for i, (name, sym, nature, sec, col) in enumerate(stages):
        x = 10 + i * (bw + gap)
        o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="6" fill="{BOX}" stroke="{I["rule"]}" stroke-width="1"/>')
        o.append(f'<rect x="{x}" y="{y}" width="5" height="{bh}" rx="2" fill="{col}"/>')
        o.append(H.label(s, x + bw / 2, y + 28, name, "label", I["primary"], "middle"))
        o.append(H.label(s, x + bw / 2, y + 54, sym, "label", col if col != I["rule"] else I["primary"], "middle", 'font-style="italic"'))
        if nature:
            o.append(H.label(s, x + bw / 2, y + bh + 22, nature, "label2", I["secondary"], "middle"))
        o.append(H.label(s, x + bw / 2, y - 12, sec, "label2", I["muted"], "middle"))
        if i < 3:
            o.append(H.arrow(s, p, x + bw + 4, y + bh / 2, x + bw + gap - 4, y + bh / 2, "dim", w="ref"))
    xm = 10 + 3 * (bw + gap) - gap / 2
    o.append(H.label(s, xm, y + bh / 2 - 22, "× moment", "label2", I["secondary"], "middle"))
    o.append(H.label(s, xm, y + bh / 2 - 8, "arm", "label2", I["secondary"], "middle"))
    aria = ("A four-stage pipeline: neural drive u(t) feeds activation a(t), which feeds muscle force F, which feeds joint "
            "torque tau through the moment arm. Stage natures: electrical (nerve), chemical (calcium), mechanical. "
            "Sections: 3 to 4, 5, 2 and 6 to 7, 8.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #22: size-principle onion + neural drive
def fig22():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    p = "m5f22_"
    cx, cy = 200, 182
    rS, rFR, rFF = 34, 82, 146                     # core, ring, shell: grows with unit size (qualitative)
    mus = T["muscle"][0]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # shading density = fibres per unit (few -> many), table at module05.html:1046-1048
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{rFF}" fill="{mus}" fill-opacity="0.62" stroke="{T["muscle"][1]}" stroke-width="1"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{rFR}" fill="#fff"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{rFR}" fill="{mus}" fill-opacity="0.36" stroke="{T["muscle"][1]}" stroke-width="1"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{rS}" fill="#fff"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{rS}" fill="{mus}" fill-opacity="0.14" stroke="{T["muscle"][1]}" stroke-width="1"/>')
    # recruitment order: neural drive sweeps outward
    o.append(H.arrow(s, p, cx, cy, cx, cy - rFF - 22, "neural", w="force"))
    o.append(H.label(s, cx + 10, cy - rFF - 10, f"recruitment order as drive {it('u')} rises", "label", O["neural"]))
    # direct labels with leaders (right column)
    lx = 410
    rows = [(rFF, -35, 92, "FF — fast, fatigable (IIx)", "largest units, many fibres: recruited last"),
            (rFR, -4, 172, "FR — fast, resistant (IIa)", "medium units: recruited next"),
            (rS, 30, 252, "S — slow, fatigue-resistant (I)", "smallest units, few fibres: recruited first")]
    for r_out, ang, ly, t1, t2 in rows:
        r_in = {rFF: rFR, rFR: rS, rS: 0}[r_out]
        rm = (r_out + r_in) / 2
        ax, ay = cx + rm * math.cos(math.radians(ang)), cy + rm * math.sin(math.radians(ang))
        o.append(f'<circle cx="{ax:.2f}" cy="{ay:.2f}" r="{s(2.5):.2f}" fill="{I["primary"]}"/>')
        o.append(H.line(s, ax, ay, lx - 8, ly - 5, I["secondary"], "leader"))
        o.append(H.label(s, lx, ly, t1, "label"))
        o.append(H.label(s, lx, ly + 18, t2, "label2", I["secondary"]))
    o.append(H.label(s, lx, 302, "Rings show recruitment order, not location:", "label2", I["muted"]))
    o.append(H.label(s, lx, 318, "each unit’s fibres are scattered through the muscle.", "label2", I["muted"]))
    # neural drive axis u = 0 -> 1 with an impulse comb that gets denser (rate coding)
    x0, x1, ya = 40, 720, 366
    o.append(H.arrow(s, p, x0, ya, x1 + 12, ya, "dim", w="ref"))
    for x in (x0, x1):
        o.append(H.line(s, x, ya - 5, x, ya + 5, I["axis"], "axis"))
    xs, x, gap = [], x0 + 30, 34.0
    while x < x1 - 4:
        xs.append(x)
        x += gap
        gap = max(5.0, gap * 0.86)
    for x in xs:
        o.append(H.line(s, x, ya - 16, x, ya - 4, O["neural"], "ref"))
    o.append(H.label(s, x0, ya + 22, f"{it('u')} = 0: silent", "label2", I["secondary"]))
    o.append(H.label(s, x1, ya + 22, f"{it('u')} = 1: every unit recruited, firing fast enough to fuse", "label2", I["secondary"], "end"))
    o.append(H.label(s, (x0 + x1) / 2, ya - 24, f"neural drive {it('u')} ∈ [0, 1]: recruitment and rate coding (impulses denser) in one number",
                     "label2", I["primary"], "middle"))
    aria = ("Size-principle onion of motor-unit types: a small slow S core, a fast-resistant FR ring and a large "
            "fast-fatigable FF shell, shaded darker as fibres per unit increase. A green arrow from the centre outward shows "
            "recruitment order as drive rises: S first, FR next, FF last. The rings show order, not location. Below, the "
            "neural drive axis runs from u = 0, silent, to u = 1, every unit recruited and firing fast enough to fuse, with a "
            "green impulse comb that gets denser to the right for rate coding.")
    return finish((VB[0], VB[1], VB[2], VB[3]), aria, s, o)


# ---------------------------------------------------------------- svg #31: Hill-type model signal flow
def fig31():
    VB = (0, 0, 760, 318)
    s = H.Scale(VB[2], VB[3])
    p = "m5f31_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    bx, bw, bh = 10, 124, 38
    facs = [(f'{it("a")}(t)', "activation · §5"),
            (f'{it("F")}{H.sub("max", s)}', "force ceiling · §1"),
            (f'{it("f")}{H.sub("L", s)}(ℓ)', "length · §2"),
            (f'{it("f")}{H.sub("V", s)}(v)', "velocity · §6")]
    mx, my, r = 300, 128, 18
    for i, (sym, name) in enumerate(facs):
        y = 12 + i * 62
        o.append(box(s, bx, y, bw, bh))
        o.append(H.label(s, bx + bw / 2, y + 25, sym, "label", I["primary"], "middle"))
        o.append(H.label(s, bx + bw / 2, y + bh + 15, name, "label2", I["secondary"], "middle"))
        yc = y + bh / 2
        ang = math.atan2(my - yc, mx - (bx + bw + 4))
        o.append(H.arrow(s, p, bx + bw + 4, yc, mx - (r + 4) * math.cos(ang), my - (r + 4) * math.sin(ang), "dim", w="ref"))
    o.append(node(s, mx, my, r, "×"))
    sx, sy = 470, my
    o.append(H.arrow(s, p, mx + r + 4, my, sx - r - 4, sy, "dim", w="ref"))
    o.append(H.label(s, (mx + sx) / 2, my - 10, f'{it("F")}{H.sub("CE", s)}', "label", O["force"], "middle"))
    o.append(H.label(s, (mx + sx) / 2, my + 22, "contractile", "label2", I["secondary"], "middle"))
    o.append(H.label(s, (mx + sx) / 2, my + 37, "element", "label2", I["secondary"], "middle"))
    o.append(node(s, sx, sy, r, "+"))
    # parallel elastic element (passive force) below the sum node
    pw, ph, px, py = 150, 40, sx - 75, 204
    o.append(box(s, px, py, pw, ph, accent=O["force"]))
    o.append(H.label(s, sx, py + 26, f'{it("F")}{H.sub("PE", s)}(ℓ)', "label", O["force"], "middle"))
    o.append(H.label(s, sx, py + ph + 16, "parallel elastic (passive) · §7", "label2", I["secondary"], "middle"))
    o.append(H.arrow(s, p, sx, py - 4, sx, sy + r + 4, "dim", w="ref"))
    # pennation projection, then the tendon force to section 8
    qx, qw = 540, 112
    o.append(H.arrow(s, p, sx + r + 4, sy, qx - 4, sy, "dim", w="ref"))
    o.append(box(s, qx, sy - 20, qw, 40))
    o.append(H.label(s, qx + qw / 2, sy + 6, f'× cos {it("θ")}{H.sub("p", s)}', "label", I["primary"], "middle"))
    o.append(H.label(s, qx + qw / 2, sy + 20 + 16, "pennation · §1", "label2", I["secondary"], "middle"))
    o.append(H.arrow(s, p, qx + qw + 4, sy, 750, sy, "force"))
    o.append(H.label(s, 703, sy - 12, f'{it("F")}{H.sub("tendon", s)}', "label", O["force"], "middle"))
    o.append(H.label(s, 703, sy + 22, "to torque", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 703, sy + 37, "§8", "label2", I["secondary"], "middle"))
    eq = (f'{it("F")}{H.sub("tendon", s)} = [ {it("a")} {it("F")}{H.sub("max", s)} {it("f")}{H.sub("L", s)}(ℓ) '
          f'{it("f")}{H.sub("V", s)}(v) + {it("F")}{H.sub("PE", s)}(ℓ) ] cos {it("θ")}{H.sub("p", s)}')
    o.append(H.label(s, 380, 304, eq, "label", I["primary"], "middle"))
    aria = ("Signal-flow diagram of the Hill-type muscle model. Four factor boxes, activation a(t) from section 5, the force "
            "ceiling F max from section 1, the length factor f L of l from section 2 and the velocity factor f V of v from "
            "section 6, feed a multiply node, the contractile element, whose output is the contractile force F CE. A sum "
            "node adds the passive parallel-elastic force F PE of l. A times cosine theta p box (pennation, section 1) "
            "turns the sum into the tendon force F tendon, which goes to torque in section 8. Below: F tendon = "
            "[a F max f L f V + F PE] cos theta p.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #41: idealisations and where they are repaid
def fig41():
    VB = (0, 0, 760, 336)
    s = H.Scale(VB[2], VB[3])
    p = "m5f41_"
    o = [f'<defs>{H.markers(p, s)}</defs>']
    rows = [("rigid tendon (Assumption 7.1)", "Module 6", "series-elastic tendon: energy storage, return"),
            (f"neural drive {it('u')} prescribed by hand (§5)", "Module 7", "reflexes, spindles, closed-loop control"),
            ("redundancy shown for two muscles (§8)", "Modules 7 and 12", "whole-limb load-sharing, cost function"),
            ("one lumped fatigue state (§9)", "Module 14", "fibre-type fatigue, recovery kinetics"),
            ("prescribed joint kinematics (§9)", "later dynamics module", "limb inertia: torque → motion")]
    lx, lw, rx, rw, top, pitch = 10, 318, 420, 330, 52, 58
    o.append(H.label(s, lx, 20, "The Module 5 Hill-type model idealises …", "label", I["primary"]))
    o.append(H.label(s, rx, 20, "… repaid in", "label", I["primary"]))
    o.append(box(s, lx, 32, lw, pitch * len(rows) + 8, accent=None))
    for i, (ideal, mod, what) in enumerate(rows):
        yc = top + 14 + i * pitch
        o.append(H.label(s, lx + 14, yc + 5, ideal, "label", I["primary"]))
        o.append(H.arrow(s, p, lx + lw + 6, yc, rx - 6, yc, "dim", w="ref"))
        o.append(box(s, rx, yc - 23, rw, 46))
        o.append(H.label(s, rx + 12, yc - 4, mod, "label", I["primary"]))
        o.append(H.label(s, rx + 12, yc + 14, what, "label2", I["secondary"]))
    aria = ("Roadmap of the idealisations of the Module 5 Hill-type model and where each is repaid: rigid tendon "
            "(Assumption 7.1) to Module 6, series-elastic tendon; neural drive u prescribed by hand (section 5) to "
            "Module 7, reflexes and closed-loop control; redundancy shown for two muscles (section 8) to Modules 7 and 12, "
            "whole-limb load-sharing; one lumped fatigue state (section 9) to Module 14; prescribed joint kinematics "
            "(section 9) to a later dynamics module, torque to motion.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #46 (C5): same current, two motoneurons
def fig46():
    VB = (0, 0, 420, 268)
    s = H.Scale(VB[2], VB[3], display_w=400)
    p = "m5f46_"
    nf, nl = T["nerve"]
    mf, ml = T["muscle"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    yI = 44
    o.append(H.line(s, 40, yI, 380, yI, O["neural"], "force"))
    o.append(H.label(s, 210, yI - 12, f"descending command: the same current {it('I')} to both", "label2", I["primary"], "middle"))
    cells = [(110, 10, 3, "small motoneuron", "few fibres"), (300, 28, 9, "large motoneuron", "many fibres")]
    yc = 120
    for x, r, n, t1, t2 in cells:
        o.append(H.arrow(s, p, x, yI + 2, x, yc - r - 3, "neural", w="force"))
        o.append(H.label(s, x + 8, yI + 30, it("I"), "label", O["neural"]))
        o.append(f'<circle cx="{x}" cy="{yc}" r="{r}" fill="{nf}" stroke="{nl}" stroke-width="{s(1.2):.2f}"/>')
        ya = 176
        o.append(H.line(s, x, yc + r, x, ya, nl, "force"))
        w = 20 * n / 3 + 30 if n > 3 else 50
        x0 = x - w / 2
        o.append(H.line(s, x0, ya, x0 + w, ya, nl, "geom"))
        for j in range(n):
            fx = x0 + (j + 0.5) * w / n
            o.append(H.line(s, fx, ya, fx, ya + 10, nl, "leader"))
            o.append(f'<rect x="{fx - 3:.2f}" y="{ya + 10}" width="6" height="34" rx="3" fill="{mf}" stroke="{ml}" stroke-width="0.8"/>')
        o.append(H.label(s, x, 244, t1, "label2", I["primary"], "middle"))
        o.append(H.label(s, x, 261, t2, "label2", I["secondary"], "middle"))
    o.append(H.label(s, 210, yc + 5, "which reaches", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 210, yc + 21, "threshold first?", "label2", I["secondary"], "middle"))
    aria = ("Problem C5 setup: one descending command delivers the same synaptic current I to a small motoneuron and a "
            "large motoneuron. The small cell drives a motor unit of few muscle fibres, the large cell a unit of many "
            "fibres. Question: which reaches threshold first?")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #49 (C8): two flexors share one torque
def nih_forearm():
    src = H.recolour(NIH_ARM.read_text(encoding="utf-8"), "nih")
    paths = re.findall(r'<path\b[^>]*?\bd="([^"]+)"[^>]*/>', src)
    assert len(paths) == 24, len(paths)
    bone = f'fill="{T["bone"][0]}" stroke="{T["bone"][1]}" stroke-width="0.5" stroke-linejoin="round"'
    return "".join(f'<path d="{paths[i-1]}" {bone}/>' for i in [6, 5] + list(range(7, 16)))


def place_forearm(Ex, Ey, cm):
    E, W = ART_E, ART_WRIST
    a = math.degrees(math.atan2(W[1] - E[1], W[0] - E[0]))
    k_art = math.hypot(W[0] - E[0], W[1] - E[1]) / (FOREARM_FRAC * H_REF_M * 100)
    return (f'<g transform="translate({Ex} {Ey}) scale({cm / k_art:.4f}) rotate({-a:.3f}) '
            f'translate({-E[0]} {-E[1]})">{nih_forearm()}</g>')


# module05.html line 1434 (Fig. 30 caption) and line 1408 (2 kg dumbbell at r_L = 0.30 m)
C8 = dict(d_bi=4.0, d_br=2.5, Fmax_bi=135, Fmax_br=210, m=2.0, r_L=30.0)


def fig49():
    VB = (0, 10, 560, 386)
    s = H.Scale(VB[2], VB[3], display_w=400)
    p = "m5f49_"
    d = C8
    tau = d["m"] * 9.81 * d["r_L"] / 100                       # 5.886 N m
    W = d["m"] * 9.81
    assert abs(tau - 5.89) < 0.005 and abs(W - 19.6) < 0.05
    cm, Ex, Ey = 11.0, 64.0, 196.0
    xbr, xbi, xw = Ex + d["d_br"] * cm, Ex + d["d_bi"] * cm, Ex + d["r_L"] * cm
    o = [f'<defs>{H.markers(p, s)}</defs>', place_forearm(Ex, Ey, cm)]
    # the two unknown muscle forces, both pulling up (not to force scale)
    o.append(H.arrow(s, p, xbr, Ey - 6, xbr, Ey - 170, "force"))
    o.append(H.arrow(s, p, xbi, Ey - 6, xbi, Ey - 112, "force"))
    o.append(H.label(s, xbr + 10, Ey - 156, f'{it("F")}{H.sub("br", s)} = ?', fill=O["force"]))
    o.append(H.label(s, xbr + 10, Ey - 128, f'brachialis, {it("F")}{H.sub("max", s, "label2")} 210 N', "label2", I["secondary"]))
    o.append(H.label(s, xbi + 10, Ey - 94, f'{it("F")}{H.sub("bi", s)} = ?', fill=O["force"]))
    o.append(H.label(s, xbi + 10, Ey - 66, f'biceps, {it("F")}{H.sub("max", s, "label2")} 135 N', "label2", I["secondary"]))
    # load
    o.append(H.arrow(s, p, xw, Ey + 6, xw, Ey + 86, "load"))
    o.append(H.label(s, xw - 10, Ey + 70, f'{it("W")} ≈ {W:.1f} N', fill=O["load"], anchor="end"))
    o.append(H.label(s, xw - 10, Ey + 88, "2 kg dumbbell", "label2", I["secondary"], "end"))
    o.append(H.joint_centre(s, Ex, Ey))
    o.append(H.label(s, Ex - 14, Ey + 5, "elbow", "label2", I["secondary"], "end"))
    # moment arms (geometry blue, heads at both ends) and the load arm (load brown)
    y1, y2, yr = Ey + 32, Ey + 62, Ey + 118
    for x, yy in ((Ex, y2), (xbr, y1), (xbi, y2)):
        o.append(H.line(s, x, Ey + 8, x, yy + 5, O["dim"], "leader", H.DASH_REF))
    o.append(H.arrow(s, p, Ex, y1, xbr, y1, "geometry", both=True))
    o.append(H.label(s, xbi + 8, y1 + 5, f'{it("d")}{H.sub("br", s)} = 2.5 cm', fill=O["geometry"]))
    o.append(H.arrow(s, p, Ex, y2, xbi, y2, "geometry", both=True))
    o.append(H.label(s, xbi + 8, y2 + 5, f'{it("d")}{H.sub("bi", s)} = 4.0 cm', fill=O["geometry"]))
    o.append(H.line(s, Ex, y2 + 5, Ex, yr + 5, O["dim"], "leader", H.DASH_REF))
    o.append(H.line(s, xw, Ey + 96, xw, yr + 5, O["dim"], "leader", H.DASH_REF))
    o.append(H.line(s, Ex, yr, xw, yr, O["load"], "ref", extra=f'marker-start="url(#{p}a_dim)" marker-end="url(#{p}a_dim)"'))
    o.append(H.label(s, (Ex + xw) / 2, yr - 9, f'{it("r")}{H.sub("L", s)} = 30 cm', fill=O["load"], anchor="middle"))
    o.append(H.label(s, VB[2] / 2, Ey + 154,f'{it("F")}{H.sub("bi", s)}{it("d")}{H.sub("bi", s)} + {it("F")}{H.sub("br", s)}{it("d")}{H.sub("br", s)} '
                     f'= {it("W r")}{H.sub("L", s)} = {tau:.2f} N·m: which pair?', anchor="middle"))
    o.append(H.credit(s, 10, Ey + 176, ["Bones: NIH NIAID BioArt 208 “Human Arm Bones”, public domain.",
                                        "Recoloured; forearm and hand only. Arrows are not to force scale."]))
    aria = ("Problem C8 setup: free-body view of the horizontal forearm and hand. Two elbow flexors pull up near the elbow: "
            "the brachialis at 2.5 cm (maximum force 210 N) and the biceps at 4.0 cm (maximum force 135 N); both forces "
            "are unknown. A 2 kg dumbbell, weight about 19.6 N, hangs 30 cm from the elbow. Any pair with F bi d bi plus "
            "F br d br equal to 5.89 newton metres holds it: which pair is chosen?")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #76 (K8): two cost functions, three flexors
K8 = dict(D=(0.04, 0.03, 0.02), FM=(500.0, 700.0, 900.0), TAU=10.0)   # module05.html, problem K8


def k8_solve():
    D, FM, TAU = K8["D"], K8["FM"], K8["TAU"]
    lam = TAU / sum(d * d * f * f for d, f in zip(D, FM))
    Fq = [lam * d * f * f for d, f in zip(D, FM)]
    # min sum F under sum F d = TAU: the LP vertex loads only the largest moment arm (within its F_max)
    i = max(range(3), key=lambda k: D[k])
    Fl = [0.0] * 3
    Fl[i] = TAU / D[i]
    assert Fl[i] <= FM[i]
    assert [round(f) for f in Fq] == [86, 126, 139] and [round(f) for f in Fl] == [250, 0, 0]
    assert abs(sum(f * d for f, d in zip(Fq, D)) - TAU) < 1e-9
    return Fq, Fl


def fig76():
    VB = (0, 0, 440, 330)
    s = H.Scale(VB[2], VB[3], display_w=400)
    Fq, Fl = k8_solve()
    D, FM = K8["D"], K8["FM"]
    x0, x1, y0, y1 = 64, 430, 250, 70
    Y = lambda f: y0 - f / 300 * (y0 - y1)              # noqa: E731
    o = []
    for f in (100, 200, 300):
        o.append(H.line(s, x0, Y(f), x1, Y(f), "#e6e6e6", "leader"))
    for f in (0, 100, 200, 300):
        o.append(H.line(s, x0 - 5, Y(f), x0, Y(f), I["axis"], "leader"))
        o.append(H.label(s, x0 - 9, Y(f) + 4.5, f"{f}", "tick", I["secondary"], "end"))
    o.append(H.label(s, 16, (y0 + y1) / 2, "muscle force (N)", "label2", I["primary"], "middle",
                     f'transform="rotate(-90 16 {(y0 + y1) / 2})"'))
    gw, bw = (x1 - x0) / 3, 34
    hv = []
    for k in range(3):
        gx = x0 + gw * (k + 0.5)
        for j, (F, col) in enumerate(((Fq[k], H.SERIES[0]), (Fl[k], H.SERIES[1]))):
            bx = gx - bw - 2 + j * (bw + 4)
            h = y0 - Y(F)
            if h > 0:
                o.append(f'<rect x="{bx:.2f}" y="{Y(F):.2f}" width="{bw}" height="{h:.2f}" fill="{col}" fill-opacity="0.85"/>')
            o.append(H.label(s, bx + bw / 2, Y(F) - 6, f"{F:.0f}", "tick", I["primary"], "middle"))
            how = "(a) min stress" if j == 0 else "(b) min effort"
            hv.append([round(bx + bw / 2, 2), round(Y(F), 2), f"M{k+1}, {how}: {F:.0f} N ({F/FM[k]:.2f} of its max)"])
        o.append(H.label(s, gx, y0 + 18, f"M{k+1}", "label2", I["primary"], "middle"))
        o.append(H.label(s, gx, y0 + 34, f"d = {D[k]*100:.0f} cm", "label2", I["secondary"], "middle"))
        o.append(H.label(s, gx, y0 + 50, f'{it("F")}{H.sub("max", s, "label2")} {FM[k]:.0f} N', "label2", I["secondary"], "middle"))
    o.append(H.line(s, x0, y0, x1, y0, I["axis"], "axis"))
    o.append(H.line(s, x0, y0, x0, y1 - 6, I["axis"], "axis"))
    # legend (two series), with totals
    ly = 20
    for j, (col, txt) in enumerate(((H.SERIES[0], f"(a) min Σ({it('F')}/{it('F')}{H.sub('max', s, 'label2')})²: total {sum(Fq):.0f} N"),
                                    (H.SERIES[1], f"(b) min Σ{it('F')}: total {sum(Fl):.0f} N"))):
        yy = ly + j * 20
        o.append(f'<rect x="{x0}" y="{yy - 10}" width="14" height="10" fill="{col}" fill-opacity="0.85"/>')
        o.append(H.label(s, x0 + 20, yy, txt, "label2", I["primary"]))
    o.append(H.label(s, x1, ly, f"{it('τ')} = 10 N·m", "label2", I["secondary"], "end"))
    aria = ("Grouped bars for problem K8: three elbow flexors M1, M2, M3 (moment arms 4, 3, 2 cm; maximum forces 500, 700, "
            "900 N) share 10 newton metres. Red bars, minimum summed squared relative stress: 86, 126 and 139 N, total "
            "351 N. Blue bars, minimum summed force: 250 N in M1 and 0 in M2 and M3, total 250 N.")
    svg = finish(VB, aria, s, o, extra=H.hover_attr([x0, y1, x1, y0], hv))
    assert not any(c.lower() in t.lower() for t in re.findall(r"<text[^>]*>", svg) for c in H.SERIES), "series colour in text"
    return svg


FIGS = {
    4: ("A four-stage pipeline: neural drive u(t) feeds activation a(", fig4),
    22: ("Concentric onion of motor-unit types: a small slow core, the", fig22),
    31: ("Signal-flow block diagram of the Hill model. Four factor box", fig31),
    41: ("Roadmap: a central Module 5 box with arrows to Module 6 (ser", fig41),
    46: ("recruitment small to large", fig46),
    49: ("two muscles share torque", fig49),
    76: ("two redundancy cost functions: L2 shares force across three ", fig76),
}
