"""Module 3, group `body`: whole-body figures from the posable Lynch skeleton (lynch_body.py), house style.

Main text (760 px): svg #7 (front-view joint map), #12 (single-leg-stance free body), #14 (trunk lean over the
stance hip, animated: slider + Play).  Problems (400 px): #28 (C1 rail vs wall), #29 (C2 cane), #30 (C3 upright vs
lean), #40 (D3 pelvis free body).

Numbers from module03.html (line numbers beside each constant): W_s = 5/6 W, a = 5 cm, b = 10 cm upright and 2.8 cm
leaning; R = W_s (1 + b/a) (4.1), F_ab = W_s b / a.  The text gives no stature: the figures assume 1.75 m, so 1 cm
= LB.H_U / 175 body units.  The COM mark sits at the text's b (the kit's own W_s centre of mass is 12.1 cm medial of
the upright stance hip); the lean frames move it by the kit's computed shift, and the trunk lean that gives
b = 2.8 cm is solved here.  The stance-hip adduction of every frame is solved so the whole-body COM is over the
stance sole.  The pelvis is held level (line 805).
"""
import copy
import math

import house as H
import lynch_body as LB
from m03.joints import HAND
from m05.body import finish, it

SHARED_DEFS = LB.SHARED_DEFS

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
CM = LB.H_U / 175.0                     # body units per cm (assumed stature 1.75 m; the text states none)

# ---------------------------------------------------------------- numbers module03.html states
WS = 5.0 / 6.0                          # supported weight, W (lines 807, 850)
A_AB = 5.0                              # abductor lever a, cm (lines 841, 850)
B_UP, B_LEAN = 10.0, 2.8                # weight lever b upright and leaning, cm (lines 850, 939)


def R_hip(b):
    return WS * (1 + b / A_AB)          # (4.1)


def F_ab(b):
    return WS * b / A_AB


def close(v, ref, tol):
    assert abs(v - ref) <= tol * 1.0001, (v, ref)


close(R_hip(B_UP), 2.50, 0.005)         # line 850
close(R_hip(B_LEAN), 1.30, 0.005)       # line 939
close(R_hip(B_UP) / R_hip(B_LEAN), 1.9, 0.05)   # "a factor 1.9", line 939
close(F_ab(B_UP), 1.67, 0.005)          # line 942
close(WS, 0.83, 0.005)                  # "R = W_s = 0.83 W", line 939

# Greater trochanter: lateral-most point of the anterior femur art (hbody_ant_thigh, local, hip at the origin),
# read from the path data: x 32.0 U at y 30.1 U = 5.6 cm lateral of the femoral-head centre (a = 5 cm is the lever).
TROCH = (32.0, 30.1)
ARMS = LB._ANT_ARMS                     # the art's own arm angles (hanging, palms forward)


def sub(t, s, size="label"):
    return H.sub(t, s, size)


def Ws(s, size="label"):
    return f'{it("W")}{sub("s", s, size)}'


def Fab(s, size="label"):
    return f'{it("F")}{sub("ab", s, size)}'


# ================================================================ the frontal single-leg stance
def _ant(trunk, hl):
    """Pelvis level; the shoulders are counter-rotated by the trunk lean so both arms hang as in standing."""
    arm_r = dict(ARMS, shoulder=ARMS["shoulder"] - trunk)
    arm_l = dict(ARMS, shoulder=ARMS["shoulder"] + trunk)
    return LB.pose_ant(pelvis=0.0, trunk=trunk, l=dict(hip=hl, **arm_l),
                       r=dict(hip=4.0, hip_flex=40.0, knee_flex=70.0, **arm_r), anchor=("sole", "l"))


STANCE = ("thigh_l", "shank_l", "foot_l")


def _com(P, skip=()):
    m = sum(v[1] for k, v in P.com.items() if k not in skip)
    return (sum(v[0][0] * v[1] for k, v in P.com.items() if k not in skip) / m,
            sum(v[0][1] * v[1] for k, v in P.com.items() if k not in skip) / m)


def _bisect(f, lo, hi, n=60):
    """Root of f on [lo, hi] (f changes sign there, or is zero at an end)."""
    flo = f(lo)
    if flo == 0:
        return lo
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def b_kit(trunk):
    """Horizontal distance (cm) from the stance (left) hip to the COM of everything but the stance leg."""
    P = _ant(trunk, 0.0)
    return (P.j["hip_l"][0] - _com(P, STANCE)[0]) / CM


def stance(trunk):
    """Frontal single-leg stance on the left leg: pelvis level, trunk leaned `trunk` deg toward the stance side,
    stance hip adducted so that the whole-body COM is over the stance sole."""
    hl = _bisect(lambda h: (lambda P: P.j["sole_l"][0] - _com(P)[0])(_ant(trunk, h)), -20.0, 10.0)
    return _ant(trunk, hl)


B_KIT0 = b_kit(0.0)


def trunk_for(b):
    """Trunk lean that moves the kit COM by b - B_UP (the mark is drawn at the text's b)."""
    return _bisect(lambda t: b_kit(t) - (B_KIT0 - (B_UP - b)), 0.0, 45.0)


def ws_com(J, P):
    """Figure point of the COM of the supported mass (all but the stance leg)."""
    m = sum(v[1] for k, v in P.com.items() if k not in STANCE)
    return (sum(J["com_" + k][0] * v[1] for k, v in P.com.items() if k not in STANCE) / m,
            sum(J["com_" + k][1] * v[1] for k, v in P.com.items() if k not in STANCE) / m)


# ================================================================ drawing helpers
def dim(s, p, x0, x1, y, text, below=False, size="label"):
    """Horizontal dimension (geometry blue, two heads) with its label above (or below) the middle."""
    if abs(x1 - x0) > s(24):
        o = [H.arrow(s, p, x0, y, x1, y, "geometry", both=True)]
    else:                                                      # too short for two heads: a bar with end ticks
        c = O["geometry"]
        o = [H.line(s, x0, y, x1, y, c, "geom"), H.line(s, x0, y - s(5), x0, y + s(5), c, "geom"),
             H.line(s, x1, y - s(5), x1, y + s(5), c, "geom")]
    ty = y + s(H.PX[size]) + s(4) if below else y - s(5)
    o.append(H.label(s, (x0 + x1) / 2, ty, text, size, anchor="middle"))
    return "".join(o)


def ext(s, x, y0, y1):
    """Dashed extension line (reference grey)."""
    return H.line(s, x, y0, x, y1, O["dim"], "ref", H.DASH_REF)


def floor(s, x0, x1, y, hatch=True):
    o = [H.line(s, x0, y, x1, y, I["axis"], "axis")]
    if hatch:
        n = int((x1 - x0) / s(10))
        o += [H.line(s, x0 + s(10) * i + s(8), y + s(1), x0 + s(10) * i, y + s(7), I["rule"], "leader")
              for i in range(n)]
    return "".join(o)


def _credit_text(extra=""):
    return H.ATTRIBUTION["by"].format(
        author="Patrick J. Lynch, medical illustrator",
        title="Skeleton lateral.svg” and “Skeleton whole body ant lat views.svg", licence="CC BY 2.5",
        changes="Recoloured, split into segments and reposed; arms from the anterior view." + extra)


def credit(s, vb, extra=""):
    """Lynch credit (lynch_body.credit) at the bottom of the viewBox, wrapped to its width."""
    w = vb[2] - s(12)
    n = max(20, int(w / (s(H.PX["credit"]) * 0.47)))          # the wrap rule of lynch_body.credit
    lines, cur = 0, ""
    for wd in _credit_text(extra).split():
        if cur and len(cur) + 1 + len(wd) > n:
            lines, cur = lines + 1, wd
        else:
            cur = (cur + " " + wd).strip()
    y = vb[1] + vb[3] - s(6) - lines * s(H.PX["credit"]) * 1.25
    return LB.credit(s, vb[0] + s(6), y, width=w, extra=extra)


def only(P, keep):
    """A copy of pose P that draws only the segments `keep(seg)` accepts (joints and masses unchanged)."""
    Q = copy.copy(P)
    Q.segs = [g for g in P.segs if keep(g)]
    return Q


# ================================================================ svg #7  joint map (front view)
DOF_COL = {1: SER[0], 2: SER[1], 3: SER[2], 0: I["secondary"]}


def badge(s, x, y, n):
    r = s(7.5)
    out = (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{DOF_COL[n]}" stroke="#fff" '
           f'stroke-width="{s(1.6):.2f}"/>')
    if n:
        out += (f'<text x="{x:.2f}" y="{y + s(4):.2f}" font-size="{s(11.5):.2f}" font-weight="bold" fill="#fff" '
                f'text-anchor="middle">{n}</text>')
    return out


def root_pt(J, q):
    """A point of the anterior art (Lynch root frame, the subject's left side) in figure units, standing pose."""
    b = LB.ant_body(q)
    k = J["scale"]
    return (J["hip_mid"][0] + k * (b[0] - LB.AJ["hip_mid"][0]), J["hip_mid"][1] + k * (b[1] - LB.AJ["hip_mid"][1]))


def fig7():
    p = "m3f7_"
    HF, top, xc = 690.0, 16.0, 300.0
    P = LB.pose_ant(**LB.POSES_ANT["standing"])
    k = HF / LB.H_U
    yh = top + (LB.H_U + LB.AJ["hip_mid"][1]) * k
    body, J = LB.draw(p, None, P, xc, yh, HF)
    fy = J["floor_y"]
    VB = (0, 0, 760, round(fy + 78))
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    o = [body]
    lerp = LB.lerp
    c12 = lerp(J["neck"], J["vertex"], 0.30)                 # C1-C2: no landmark in the art; estimated (report)
    facet = lerp(J["l5s1"], J["neck"], 0.16)
    facet = (facet[0] + 2.0 * CM * k, facet[1])               # a lumbar facet, 2 cm lateral of the midline
    e = J["elbow_r"]
    pru = lerp(J["elbow_l"], J["wrist_l"], 0.10)
    pru = (pru[0] + 1.2 * CM * k, pru[1])                     # radial head: lateral (subject's left = image right)
    left = [("atlanto-axial (C1–C2)", "pivot · 1 DOF", 1, c12),
            ("shoulder", "ball and socket · 3 DOF", 3, J["shoulder_r"]),
            ("elbow (humero-ulnar)", "hinge · 1 DOF", 1, e),
            ("hip", "ball and socket · 3 DOF", 3, J["hip_r"]),
            ("knee", "hinge · 1 DOF", 1, J["knee_r"]),
            ("ankle (talocrural)", "hinge, oblique axis · 1 DOF", 1, J["ankle_r"])]
    gap = s(40)

    def column(items, x, anc, lo, size="label"):
        last = lo - gap
        sx = 1 if anc == "end" else -1
        for name, kind, n, q in items:
            last = max(q[1], last + gap)
            o.append(H.line(s, q[0], q[1], x + sx * s(4), last - s(4), I["rule"], "leader"))
            o.append(H.label(s, x, last - s(2), name, size, anchor=anc))
            o.append(H.label(s, x, last + s(13), kind, "label2", I["secondary"], anc))
        return [q for _, _, _, q in items]

    marks = column(left, 196.0, "end", s(40))
    mid = [("spinal facet (zygapophyseal)", "plane · small glides", 0, facet),
           ("proximal radio-ulnar", "pivot · 1 DOF", 1, pru)]
    marks += column(mid, 470.0, "start", 0)
    # inset: the subject's left hand, enlarged 3.1 times
    hb = only(P, lambda g: g[0] == "arm_hand" and not g[4])
    hb.anchor = P.j["wrist_l"]
    ki = 2.6 * k
    wx, wy = 462.0, 462.0
    hand_svg, JH = LB.draw(p, s, hb, wx, wy, ki * LB.H_U)
    x0, y0, x1, y1 = JH["bbox"]
    ib = (x0 - s(10), y0 - s(12), 760 - s(2) - (x0 - s(10)), y1 - y0 + s(22))
    o.append(f'<rect x="{ib[0]:.2f}" y="{ib[1]:.2f}" width="{ib[2]:.2f}" height="{ib[3]:.2f}" fill="#fff" '
             f'stroke="{I["rule"]}" stroke-width="{s(1):.2f}"/>')
    hx0, hx1 = J["bbox"][2] - (x1 - x0) / 2.6 - s(4), J["bbox"][2] + s(3)       # the hand on the body
    hy0, hy1 = J["wrist_l"][1] - s(4), J["fingertip_l"][1] + s(6)
    o.append(f'<rect x="{hx0:.2f}" y="{hy0:.2f}" width="{hx1 - hx0:.2f}" height="{hy1 - hy0:.2f}" fill="none" '
             f'stroke="{I["rule"]}" stroke-width="{s(1):.2f}"/>')
    o.append(H.line(s, hx0, hy1, ib[0], ib[1] + ib[3], I["rule"], "leader"))
    o.append(H.line(s, hx1, hy0, ib[0] + ib[2] * 0.5, ib[1], I["rule"], "leader"))
    o.append(hand_svg)
    o.append(H.label(s, ib[0] + s(6), ib[1] + ib[3] - s(6), "left hand, enlarged", "label2", I["secondary"]))
    hand = {key: root_pt(JH, HAND[key]) for key in ("carp", "cmc", "mcp", "pip")}
    right = [("wrist (radiocarpal)", "condyloid · 2 DOF", 2, JH["wrist_l"]),
             ("intercarpal", "plane · small glides", 0, hand["carp"]),
             ("thumb carpometacarpal", "saddle · 2 DOF", 2, hand["cmc"]),
             ("knuckle (MCP)", "condyloid · 2 DOF", 2, hand["mcp"]),
             ("interphalangeal (finger)", "hinge · 1 DOF", 1, hand["pip"])]
    marks += column(right, x1 + s(16), "start", ib[1] + s(24), "label2")
    for (_, _, n, q) in left + mid + right:
        o.append(badge(s, q[0], q[1], n))
    # legend
    ly = fy + s(28)
    x = 24.0
    for n, t in ((1, "1 DOF (hinge, pivot)"), (2, "2 DOF (condyloid, saddle)"), (3, "3 DOF (ball and socket)"),
                 (0, "plane joint: small glides")):
        o.append(badge(s, x, ly - s(4), n))
        o.append(H.label(s, x + s(12), ly, t, "label2"))
        x += s(12) + len(t) * s(H.PX["label2"]) * 0.5 + s(22)
    o.append(credit(s, VB))
    del marks
    aria = ("Front-view skeleton (Lynch art) with the table's twelve example joints and the knee marked by "
            "numbered dots coloured by degrees of freedom: red 1, blue 2, orange 3, grey for the gliding plane "
            "joints. Subject's right side: atlanto-axial C1–C2 pivot, shoulder ball and socket, elbow hinge, hip ball "
            "and socket, knee hinge, ankle hinge with an oblique axis. Spine and subject's left arm: a lumbar facet "
            "plane joint, the proximal radio-ulnar pivot. An enlarged inset of the left hand: wrist radiocarpal "
            "condyloid, intercarpal plane joint, thumb carpometacarpal saddle, knuckle MCP condyloid, finger "
            "interphalangeal hinge.")
    return finish(VB, aria, s, o)


# ================================================================ single-leg stance free body (#12, #40)
def pelvis_fbd(s, p, P, ox, oy, kz, b, numbers=True, fs=None, ref=False):
    """Pelvis + stance femur of pose P with the hip (femoral head O) at (ox, oy), kz figure units per body unit.
    Draws W_s at the COM (b cm medial of O), F_ab at a = 5 cm lateral, R up through O, and the a, b dimensions.
    Labels that do not ride on an arrow sit left of the upright COM line, so the frames of #14 never put a label
    on another frame's dashed line."""
    Q = only(P, lambda g: g[0] == "ant_pelvis" or (g[0] == "ant_thigh" and not g[4]))
    Q.anchor = P.j["hip_l"]
    body, J = LB.draw(p, s, Q, ox, oy, kz * LB.H_U)
    cm = CM * kz
    fs = fs or s(62)                                           # figure units per body weight W
    o = [body]
    cy = ws_com(J, P)[1]
    cx = ox - b * cm                                           # the text's b (the kit's own is 12.1 cm upright)
    lx = ox - B_UP * cm - s(10)
    xa = ox + A_AB * cm
    tro = (ox + TROCH[0] * kz, oy + TROCH[1] * kz)
    dy = oy + 0.34 * (J["knee_l"][1] - oy)
    rv, fv, wv = R_hip(b) * fs, F_ab(b) * fs, WS * fs
    # extension lines first (under the arrows)
    o.append(ext(s, cx, cy + wv + s(3), dy + s(2)))
    o.append(ext(s, ox, oy + s(8), dy + s(2)))
    o.append(ext(s, xa, tro[1] - s(4), dy + s(2)))
    # forces
    o.append(H.arrow(s, p, cx, cy, cx, cy + wv, "load"))
    fa0 = tro[1] - s(4) - fv
    o.append(H.arrow(s, p, xa, fa0, xa, tro[1] - s(4), "force"))
    o.append(H.arrow(s, p, ox, oy, ox, oy - rv, "reaction"))
    if ref:                                                    # where R ends upright (b = 10 cm)
        ty = oy - R_hip(B_UP) * fs
        o.append(H.line(s, ox - s(10), ty, ox + s(10), ty, I["rule"], "axis"))
    o.append(H.com_mark(s, cx, cy))
    o.append(H.joint_centre(s, ox, oy))
    o.append(dim(s, p, cx, ox, dy, ""))
    o.append(dim(s, p, ox, xa, dy, ""))
    o.append(H.label(s, lx, dy + s(5), f'{it("b")} = {b:g} cm' if numbers else it("b"), anchor="end"))
    o.append(H.label(s, xa + s(8), dy + s(5), f'{it("a")} = {A_AB:g} cm' if numbers else it("a")))
    pts = dict(com=(cx, cy), O=(ox, oy), xa=xa, fa0=fa0, tro=tro, rtip=oy - rv, wtip=cy + wv, dy=dy, J=J, lx=lx)
    return "".join(o), pts


def fbd_labels(s, d, numbers, b=B_UP):
    cx, cy = d["com"]
    ox, oy = d["O"]
    wy = (cy + d["wtip"]) / 2 + s(5)
    o = []
    if numbers:
        o.append(H.label(s, ox + s(8), d["rtip"] + s(12), f'{it("R")} = {R_hip(b):.2f} {it("W")}'))
        o.append(H.label(s, ox + s(8), d["rtip"] + s(30), "hip reaction", "label2", I["secondary"]))
        o.append(H.label(s, d["xa"] + s(8), d["fa0"] + s(12), f'{Fab(s)} = {F_ab(b):.2f} {it("W")}'))
        o.append(H.label(s, d["xa"] + s(8), d["fa0"] + s(33), "abductors", "label2", I["secondary"]))
        o.append(H.label(s, cx - s(9), wy, f'{Ws(s)} = {WS:.2f} {it("W")}', anchor="end"))
    else:
        o.append(H.label(s, ox + s(8), d["rtip"] + s(12), it("R")))
        o.append(H.label(s, d["xa"] + s(8), d["fa0"] + s(12), Fab(s)))
        o.append(H.label(s, d["xa"] + s(8), d["fa0"] + s(33), "abductors", "label2", I["secondary"]))
        o.append(H.label(s, cx - s(9), wy, Ws(s), anchor="end"))
    o.append(H.label(s, cx, cy - s(12), "COM", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ox + s(9), oy + s(22), it("O")))
    o.append(H.line(s, ox - s(5), oy + s(5), d["lx"] + s(2), oy + s(34), I["rule"], "leader"))
    o.append(H.label(s, d["lx"], oy + s(40), "femoral head", "label2", I["secondary"], "end"))
    return "".join(o)


def fig12():
    p = "m3f12_"
    P = stance(0.0)
    VB = (0, 0, 760, 590)
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # locator: the whole body
    HF = 430.0
    body, J = LB.draw(p, s, P, 150.0, 480.0, HF)
    o.append(body)
    o.append(floor(s, J["bbox"][0] - s(10), J["bbox"][2] + s(10), J["floor_y"]))
    kb = J["scale"]
    hl = J["hip_l"]
    bx0, bx1 = hl[0] - 140 * kb, hl[0] + 45 * kb
    by0, by1 = hl[1] - 100 * kb, J["knee_l"][1] + 18 * kb
    o.append(f'<rect x="{bx0:.2f}" y="{by0:.2f}" width="{bx1 - bx0:.2f}" height="{by1 - by0:.2f}" fill="none" '
             f'stroke="{O["dim"]}" stroke-width="{s(1.2):.2f}"/>')
    o.append(H.label(s, 150.0, J["bbox"][1] - s(10), "single-leg stance on the left leg", "label2", I["secondary"],
                     "middle"))
    # the free body, enlarged
    kz = 1.25
    ox, oy = 560.0, 205.0
    fb, d = pelvis_fbd(s, p, P, ox, oy, kz, B_UP, fs=s(58))
    o.append(H.line(s, bx1, by0, ox - 140 * kz, 40, O["dim"], "leader"))
    o.append(H.line(s, bx1, by1, ox - 140 * kz, 545, O["dim"], "leader"))
    o.append(fb)
    o.append(fbd_labels(s, d, True))
    tro = d["tro"]
    o.append(H.line(s, tro[0] + s(3), tro[1] + s(6), tro[0] + s(26), tro[1] + s(30), I["rule"], "leader"))
    o.append(H.label(s, tro[0] + s(28), tro[1] + s(40), "greater trochanter", "label2", I["secondary"]))
    kn = d["J"]["knee_l"]
    o.append(H.label(s, kn[0] + s(30), kn[1] - s(40), "stance femur", "label2", I["secondary"]))
    o.append(credit(s, VB))
    aria = ("Left: a whole skeleton in single-leg stance on its left leg, the pelvis and stance femur boxed. Right, "
            "enlarged: the pelvis on the femoral head O. The supported weight W_s = 0.83 W pulls down at the centre of "
            "mass, b = 10 cm medial of O; the abductors pull down with F_ab = 1.67 W at a = 5 cm lateral, near the "
            "greater trochanter; the femoral head pushes up with the reaction R = 2.50 W.")
    return finish(VB, aria, s, o)


def fig40():
    p = "m3f40_"
    P = stance(0.0)
    VB = (0, 0, 400, 420)
    s = H.Scale(VB[2], VB[3], display_w=400, max_h=H.MAX_DISPLAY_H_BODY)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    kz = 0.92
    ox, oy = 236.0, 150.0
    fb, d = pelvis_fbd(s, p, P, ox, oy, kz, B_UP, numbers=False, fs=s(46))
    o.append(fb)
    o.append(fbd_labels(s, d, False))
    o.append(credit(s, VB))
    aria = ("Frontal free-body diagram of the pelvis on the stance femur (Lynch skeleton art): the femoral head O, "
            "the abductors F_ab pulling down on the short lever a lateral of O, the supported weight W_s pulling down "
            "at the centre of mass on the longer lever b medial of O, and the reaction R pushing up at the head.")
    return finish(VB, aria, s, o)


# ================================================================ svg #14  lean over the stance hip (animated)
N14 = 13
B14 = [B_UP + (B_LEAN - B_UP) * i / (N14 - 1) for i in range(N14)]
TR14 = [trunk_for(b) for b in B14]
close(R_hip(B14[-1]), 1.30, 0.005)
close(F_ab(B14[-1]), 0.47, 0.005)


def stance_frame(s, p, b, trunk, HF, sx, sy, fs):
    """Whole frontal single-leg stance with W_s at the COM and the lever b; stance sole at (sx, sy)."""
    P = stance(trunk)
    body, J = LB.draw(p, s, P, sx, sy, HF)
    cm = CM * J["scale"]
    ox, oy = J["hip_l"]
    cy = ws_com(J, P)[1]
    cx = ox - b * cm                                           # the text's b (the lean moves the kit COM by b - 10 cm)
    o = [body]
    dy = oy + 0.075 * HF
    o.append(ext(s, cx, cy + WS * fs + s(2), dy + s(2)))
    o.append(ext(s, ox, oy + s(8), dy + s(2)))
    o.append(H.arrow(s, p, cx, cy, cx, cy + WS * fs, "load"))
    o.append(H.com_mark(s, cx, cy))
    o.append(H.joint_centre(s, ox, oy))
    o.append(dim(s, p, cx, ox, dy, ""))
    return "".join(o), dict(J=J, com=(cx, cy), O=(ox, oy), dy=dy, cm=cm)


def fig14():
    p = "m3f14_"
    VB = (0, 0, 760, 590)
    s = H.Scale(VB[2], VB[3], max_h=H.MAX_DISPLAY_H_BODY)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, sx, sy = 430.0, 150.0, 480.0
    kz, ox, oy = 1.25, 560.0, 205.0
    o.append(floor(s, 20, 285, sy))
    frames = []
    for i, (b, tr) in enumerate(zip(B14, TR14)):
        P = stance(tr)
        body, J = LB.draw(p, s, P, sx, sy, HF)
        kb = J["scale"]
        hl = J["hip_l"]
        g = [body, H.com_mark(s, hl[0] - b * CM * kb, ws_com(J, P)[1])]
        bx0, bx1 = hl[0] - 140 * kb, hl[0] + 45 * kb
        by0, by1 = hl[1] - 100 * kb, J["knee_l"][1] + 18 * kb
        g.append(f'<rect x="{bx0:.2f}" y="{by0:.2f}" width="{bx1 - bx0:.2f}" height="{by1 - by0:.2f}" fill="none" '
                 f'stroke="{O["dim"]}" stroke-width="{s(1.2):.2f}"/>')
        g.append(H.line(s, bx1, by0, ox - 140 * kz, 40, O["dim"], "leader"))
        g.append(H.line(s, bx1, by1, ox - 140 * kz, 545, O["dim"], "leader"))
        fb, d = pelvis_fbd(s, p, P, ox, oy, kz, round(b, 1), fs=s(58), ref=True)
        g.append(fb)
        g.append(fbd_labels(s, d, True, b))
        if d["com"][0] - d["lx"] > s(14):                     # the b label stays put: a leader to the dimension
            g.append(H.line(s, d["lx"] + s(3), d["dy"], d["com"][0] - s(3), d["dy"], I["rule"], "leader"))
        g.append(H.label(s, ox + s(14), oy - R_hip(B_UP) * s(58) + s(5), "upright", "label2", I["secondary"])
                 if i else "")
        g.append(H.label(s, sx, s(18), f"trunk lean {tr:.0f}° over the stance hip", "label2", I["secondary"],
                         "middle"))
        frames.append(H.frame(i, N14 - 1, "".join(g)))
    o += frames
    o.append(credit(s, VB))
    vals = [f"{b:.1f} cm" for b in B14]
    aria = ("Animated: left, a front-view skeleton in single-leg stance on its left leg leaning its trunk over the "
            f"stance hip (0 to {TR14[-1]:.0f} degrees, slider and Play); right, the enlarged pelvis on the femoral "
            "head. As the trunk leans, the centre of mass slides toward the femoral head and the weight lever b "
            "shrinks from 10 to 2.8 cm; the red abductor force falls from 1.67 W to 0.47 W and the black hip "
            "reaction R from 2.50 W to 1.30 W, with a grey tick at the upright R. The still figure is the leaning "
            "end state.")
    return finish(VB, aria, s, o, extra=H.frames_attr("b", vals, N14 - 1))


# ================================================================ svg #30  C3 upright vs lean
def fig30():
    p = "m3f30_"
    VB = (0, 0, 400, 520)
    s = H.Scale(VB[2], VB[3], display_w=400, max_h=H.MAX_DISPLAY_H_BODY)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, sy, fs = 400.0, 440.0, s(34)
    o.append(floor(s, 8, 392, sy))
    for sx, b, title in ((104.0, B_UP, "upright"), (286.0, B_LEAN, "lean over the hip")):
        g, d = stance_frame(s, p, b, trunk_for(b), HF, sx, sy, fs)
        o.append(g)
        ox, oy = d["O"]
        o.append(H.label(s, ox + s(8), d["dy"] + s(19), f'{it("b")} = {b:g} cm', anchor="end" if b > 5 else "start"))
        o.append(H.label(s, d["com"][0] - s(8), d["com"][1] + WS * fs - s(2), Ws(s), anchor="end"))
        o.append(H.label(s, ox + s(9), oy + s(16), "hip", "label2", I["secondary"]))
        o.append(H.label(s, sx - s(14), s(20), title, anchor="middle"))
    o.append(credit(s, VB))
    aria = ("Two front views of single-leg stance on the left leg (Lynch skeleton art). Left, upright: the supported "
            "weight W_s acts at the centre of mass, b = 10 cm medial of the stance hip. Right, the trunk leaned over "
            "the stance hip: the centre of mass sits b = 2.8 cm from the hip, a far shorter lever.")
    return finish(VB, aria, s, o)


# ================================================================ svg #28  C1 rail vs wall (side view)
def fig28():
    p = "m3f28_"
    VB = (0, 0, 400, 382)
    s = H.Scale(VB[2], VB[3], display_w=400, max_h=H.MAX_DISPLAY_H_BODY)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 270.0, 318.0
    o.append(floor(s, 6, 394, fy, hatch=False))
    # one static balance on the arm (illustrative units): hand load L = 1, arm weight w = 0.3, wall push 0.35.
    # Rail: the vertical rail reaction takes all of L, so the shoulder keeps only w.  Wall: the wall pushes only
    # horizontally, so the shoulder takes L + w upward and the wall push forward.
    Lh, wl, hw = 1.0, 0.3, 0.35
    fs = s(50)
    box = f'fill="#f7f4ef" stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}"'
    # ---- rail
    P = LB.pose(near=dict(shoulder=40, elbow=50, wrist=0), far=dict(shoulder=-5, elbow=10))
    body, J = LB.draw(p, s, P, 34.0, fy, HF)
    hd = LB.lerp(J["wrist"], J["fingertip"], 0.45)
    ry = hd[1] + s(5)
    o.append(f'<rect x="{hd[0] - s(46):.2f}" y="{ry:.2f}" width="{s(100):.2f}" height="{s(6):.2f}" {box}/>')
    o.append(body)
    o.append(H.arrow(s, p, hd[0], hd[1] - Lh * fs, hd[0], hd[1], "load"))
    o.append(H.label(s, hd[0] + s(5), hd[1] - Lh * fs + s(10), "load"))
    o.append(H.arrow(s, p, hd[0], ry + s(6) + Lh * fs, hd[0], ry + s(6), "reaction"))
    o.append(H.label(s, hd[0] + s(5), ry + s(6) + Lh * fs - s(2), "rail"))
    sh = J["shoulder"]
    o.append(H.arrow(s, p, sh[0], sh[1] + wl * fs, sh[0], sh[1], "reaction"))
    o.append(H.label(s, sh[0] - s(8), sh[1] - s(8), f'{it("R")}{sub("s", s)}', anchor="end"))
    o.append(H.label(s, sh[0] - s(8), sh[1] + s(8), "small", "label2", I["secondary"], "end"))
    o.append(H.label(s, 100, s(18), "rail: load → surface", anchor="middle"))
    # ---- wall
    P2 = LB.pose(near=dict(shoulder=80, elbow=10, wrist=88), far=dict(shoulder=-5, elbow=10))
    body2, J2 = LB.draw(p, s, P2, 222.0, fy, HF)
    hd2 = LB.lerp(J2["wrist"], J2["fingertip"], 0.45)
    wx = max(J2["fingertip"][0], J2["wrist"][0]) + s(4)
    o.append(f'<rect x="{wx:.2f}" y="{hd2[1] - s(70):.2f}" width="{s(7):.2f}" height="{s(150):.2f}" {box}/>')
    o.append(body2)
    o.append(H.arrow(s, p, hd2[0] - s(4), hd2[1] - Lh * fs, hd2[0] - s(4), hd2[1], "load"))
    o.append(H.label(s, hd2[0] - s(10), hd2[1] - Lh * fs + s(10), "load", anchor="end"))
    o.append(H.arrow(s, p, wx + s(7) + hw * fs + s(8), hd2[1] + s(4), wx + s(7) + s(2), hd2[1] + s(4), "reaction"))
    o.append(H.label(s, wx + s(10), hd2[1] + s(24), "wall"))
    sh2 = J2["shoulder"]
    o.append(H.arrow(s, p, sh2[0] - hw * fs, sh2[1] + (Lh + wl) * fs, sh2[0], sh2[1], "reaction"))
    o.append(H.label(s, sh2[0] - hw * fs - s(6), sh2[1] + (Lh + wl) * fs - s(4), f'{it("R")}{sub("s", s)}',
                     anchor="end"))
    o.append(H.label(s, 290, s(18), "wall: load → shoulder", anchor="middle"))
    o.append(credit(s, VB))
    aria = ("Two side views of a standing skeleton (Lynch art) bracing one hand. Left: the hand rests on a horizontal "
            "rail; the brown downward load at the hand is met by an equal black upward rail reaction, and the black "
            "shoulder reaction R_s stays small. Right: the hand presses on a vertical wall; the wall pushes only "
            "horizontally, so the same downward load is carried up the arm and a large black reaction R_s appears at "
            "the shoulder.")
    return finish(VB, aria, s, o)


# ================================================================ svg #29  C2 cane (side view)
def fig29():
    p = "m3f29_"
    VB = (0, 0, 400, 430)
    s = H.Scale(VB[2], VB[3], display_w=400, max_h=H.MAX_DISPLAY_H_BODY)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 290.0, 314.0
    P = LB.pose(pelvis=4, near=dict(hip=12, knee=4, shoulder=25, elbow=35, wrist=0),
                far=dict(hip=-10, knee=4, shoulder=-10, elbow=10), anchor=("heel", "far"))
    body, J = LB.draw(p, s, P, 120.0, fy, HF)
    hd = LB.lerp(J["wrist"], J["fingertip"], 0.4)
    tip = (hd[0] + s(30), fy)
    o.append(H.line(s, hd[0], hd[1], tip[0], tip[1], I["secondary"], "force", extra='stroke-linecap="round"'))
    o.append(body)
    o.append(floor(s, 20, 380, fy))
    fs = s(50)
    feet = [((J["heel_far"][0] + J["toe_far"][0]) / 2 - s(6), "1"), ((J["heel"][0] + J["toe"][0]) / 2 - s(6), "2"),
            (tip[0], "3")]
    for x, n in feet:
        o.append(H.arrow(s, p, x, fy + fs * 0.9, x, fy, "reaction"))
        o.append(H.label(s, x + s(5), fy + fs * 0.9 - s(2), f'{it("R")}{sub(n, s)}'))
    c = J["com"]
    o.append(H.arrow(s, p, c[0], c[1], c[0], c[1] + fs * 1.4, "load"))
    o.append(H.com_mark(s, *c))
    o.append(H.label(s, c[0] - s(10), c[1] + fs * 1.4 - s(4), it("W"), anchor="end"))
    o.append(credit(s, VB))
    aria = ("Side view of a standing skeleton (Lynch art) leaning on a cane held in front: the body weight W acts down "
            "at the centre of mass, and three black upward reactions act at the rear foot (R1), the front foot (R2) "
            "and the cane tip (R3).")
    return finish(VB, aria, s, o)


FIGS = {
    7: ("A simplified front-view skeleton with the example joints fro", fig7),
    12: ("Frontal-plane free body of single-leg stance: a pelvis beam ", fig12),
    14: ("Animation of a figure standing on one leg and leaning its tr", fig14),
    28: ("Two whole-body figures. Left: a person braces a hand on a ho", fig28),
    29: ("A standing human leans on a cane: the body weight W acts dow", fig29),
    30: ("Single-leg stance shown twice. Left, upright: the centre of ", fig30),
    40: ("Frontal free-body diagram of the pelvis on one leg: the femo", fig40),
}
