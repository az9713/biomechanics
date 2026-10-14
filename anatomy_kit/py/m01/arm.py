"""Module 1 arm / lever figures: svg #1 (Fig. 1 moment arm), #2 (Fig. 2 forearm free body), #3 (Fig. 3 animated
forearm rotation), #4 (Fig. 4 mechanical disadvantage), and the problem figures #11 (C1), #13 (C3), #14 (C4),
#19 (C9), #20 (C10), #21 (D1), #22 (D2), #23 (D3), #24 (D4), #28 (D8).

Art: nih_arm_bones.svg (NIH BioArt 208, public domain) reposed with m05/body.py `Arm` (approved, Module 5 Fig. 22);
Lower_leg_muscles_crop_m01foot.svg (InjuryMap, CC BY-SA 4.0) for the C4 ankle lever. Numbers: module01.html §8
(lines 411-418) and the Appendix parameter table (lines 876-879).
"""
import math

import house as H
from m05.body import ARM, F21, Arm, art_image, finish, fit_circle, foot_of_perp, inner_svg, it, wrap, _read

T, O, I = H.TISSUE, H.OVERLAY, H.INK
M_S, R_S, R_L, D_M, G = 0.022 * 70.0, 0.116, 0.35, 0.03, 9.81    # Appendix lines 876-879, 892
UPPER_CM = 0.186 * 175.0           # Winter: shoulder to elbow, 0.186 H (H = 1.75 m as m05/body.py), drawing only
UPPER_COM = 0.436                  # Winter: upper-arm COM from the shoulder, fraction of its length, drawing only
NIH = H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt 208", title="Human Arm Bones",
                                 changes="Recoloured; reposed.")


# ---------------------------------------------------------------- the NIH arm in any sagittal pose
class Posed(Arm):
    """m05 Arm with free angles. th = forearm direction (deg, clockwise from +x = angle below horizontal);
    hum = direction elbow -> shoulder (deg, -90 = humerus vertical above the elbow, 180 = shoulder on the left).
    C() maps humerus-frame cm (m05 frame: x anterior, y down, humerus vertical); F() maps forearm-frame cm
    (x along the forearm from the elbow, y 90 deg clockwise of it)."""

    def __init__(self, p, s, Ec, K, th=0.0, hum=-90.0, r_ins=3.0):
        self.th, self.hum = th, hum
        super().__init__(p, s, Ec, K, r_ins)
        self.I = self.F((r_ins, 0.4))
        self.B = self.C(ARM["belly"][2])
        self.P, dist = foot_of_perp(Ec, self.B, self.I)
        self.d_cm = dist / K

    @staticmethod
    def _rot(v, deg):
        c, s_ = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        return v[0] * c - v[1] * s_, v[0] * s_ + v[1] * c

    def C(self, v):
        x, y = self._rot(v, self.hum + 90.0)
        return self.Ec[0] + x * self.K, self.Ec[1] + y * self.K

    def F(self, v):
        x, y = self._rot(v, self.th)
        return self.Ec[0] + x * self.K, self.Ec[1] + y * self.K

    def _st(self):
        sc = self.K / self.k_art
        return sc, (f'fill="{T["bone"][0]}" stroke="{T["bone"][1]}" stroke-width="{self.s(H.PX["art_line"]) / sc:.3f}" '
                    f'stroke-linejoin="round"')

    def fore_paths(self):
        from crop_art import absolute
        _, st = self._st()
        return "".join(f'<path d="{absolute(self.paths[i - 1])}" {st}/>' for i in [6, 5] + list(range(7, 16)))

    def fore_tf(self, th=None):
        E, sc = ARM["E"], self.K / self.k_art
        th = self.th if th is None else th
        return (f'translate({self.Ec[0]:.2f} {self.Ec[1]:.2f}) scale({sc:.4f}) rotate({self.a_f - 90.0 + th:.3f}) '
                f'translate({-E[0]} {-E[1]})')

    def bones(self, hand=True, upper=True):
        from crop_art import absolute
        E, (sc, st) = ARM["E"], self._st()
        out = f'<g transform="{self.fore_tf()}">{self.fore_paths()}</g>'
        if upper:
            out += (f'<g transform="translate({self.Ec[0]:.2f} {self.Ec[1]:.2f}) scale({sc:.4f}) '
                    f'rotate({self.a_h + self.hum + 90.0:.3f}) translate({-E[0]} {-E[1]})">'
                    f'<path d="{absolute(self.paths[3])}" {st}/></g>')
        return out


# ---------------------------------------------------------------- small local helpers
def arc(s, cx, cy, r, a0, a1, col, w=1.2):
    """Plain circular arc from a0 to a1 (deg, screen, clockwise positive)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    return (f'<path d="M{x0:.2f},{y0:.2f} A{r:.2f},{r:.2f} 0 {1 if abs(a1 - a0) > 180 else 0} {1 if a1 > a0 else 0} '
            f'{x1:.2f},{y1:.2f}" fill="none" stroke="{col}" stroke-width="{s(w):.2f}"/>')


def bold(v):
    return f'<tspan font-weight="bold">{v}</tspan>'


def sym(v, sb, s, size="label"):
    return f'{it(v)}{H.sub(sb, s, size)}'


def dim(s, p, x0, x1, y, col, marker="dim"):
    """Horizontal two-headed dimension line."""
    return H.line(s, x0, y, x1, y, col, "ref", extra=f'marker-start="url(#{p}a_{marker})" marker-end="url(#{p}a_{marker})"')


def leader(s, x, y0, y1):
    return H.line(s, x, y0, x, y1, O["dim"], "leader", H.DASH_REF)


def plate(s, x, y, r):
    """Dumbbell seen end-on (the handle runs across the palm, out of the sagittal plane): plate and hub."""
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{I["rule"]}" stroke="{I["secondary"]}" stroke-width="{s(1):.2f}"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 0.35:.1f}" fill="{I["muted"]}" stroke="{I["secondary"]}" stroke-width="{s(0.8):.2f}"/>')


def bag(s, G, K):
    bw = 2.6 * K
    brn = O["load"]
    return (f'<g transform="translate({G[0]:.1f} {G[1]:.1f})">'
            f'<path d="M{-bw*0.6:.1f},{4*K:.1f} L0,0 L{bw*0.6:.1f},{4*K:.1f}" fill="none" stroke="{brn}" stroke-width="{s(1.6):.2f}"/>'
            f'<path d="M{-bw*0.75:.1f},{4*K:.1f} L{bw*0.75:.1f},{4*K:.1f} L{bw:.1f},{10*K:.1f} L{-bw:.1f},{10*K:.1f} Z" '
            f'fill="#f7f4ef" stroke="{brn}" stroke-width="{s(1.2):.2f}"/></g>')


def dot(s, x, y, col, r=2.8):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s(r):.2f}" fill="{col}" stroke="#fff" stroke-width="{s(1):.2f}"/>'


def ref_point(s, x, y):
    """A chosen reference point (not a joint): flag-orange ring."""
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s(5):.2f}" fill="#fff" stroke="{O["flag"]}" stroke-width="{s(2.2):.2f}"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{s(1.6):.2f}" fill="{O["flag"]}"/>')


def credit(s, VB, lines, x=8):
    return H.credit(s, x, VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines)


def f_m_arrow(s, p, A, L=62):
    """Biceps pull beside the distal tendon (m05 fig3 idiom). Returns (svg, start, unit)."""
    ux, uy = A.I[0] - A.B[0], A.I[1] - A.B[1]
    n = math.hypot(ux, uy)
    ux, uy = ux / n, uy / n
    nx, ny = -uy, ux
    if nx < 0:
        nx, ny = -nx, -ny
    S0 = (A.I[0] + nx * s(6), A.I[1] + ny * s(6) - s(4))
    return H.arrow(s, p, S0[0], S0[1], S0[0] - ux * L, S0[1] - uy * L, "force"), S0, (ux, uy)


def lever_icon(s, p, x0, y, w, pos, names):
    """Schematic lever: beam, pivot wedge, effort (up) and load (down) at fractions of w. names = 3 labels."""
    o = [H.line(s, x0, y, x0 + w, y, I["primary"], "axis")]
    X = {k: x0 + v * w for k, v in pos.items()}
    h = s(9)
    o.append(f'<path d="M{X["pivot"]:.1f},{y + s(1.5):.1f} l{-h * 0.7:.1f},{h:.1f} h{h * 1.4:.1f} Z" fill="{I["secondary"]}"/>')
    o.append(H.arrow(s, p, X["effort"], y - s(2), X["effort"], y - s(26), "force"))
    o.append(H.arrow(s, p, X["load"], y + s(2), X["load"], y + s(26), "load"))
    o.append(H.label(s, X["pivot"], y + h + s(14), names[0], "label2", I["secondary"], "middle"))
    o.append(H.label(s, X["effort"], y - s(30), names[1], "label2", I["primary"], "middle"))
    o.append(H.label(s, X["load"], y + s(40), names[2], "label2", I["primary"], "middle"))
    return "".join(o)


# ================================================================ svg #1  Fig. 1 moment of a force
def fig1():
    p = "m1f1_"
    VB = (0, 0, 760, 330)
    s = H.Scale(VB[2], VB[3])
    Ox, Oy, Px, Py = 110.0, 250.0, 560.0, 92.0
    red, blu = O["force"], O["geometry"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(H.label(s, 20, 34, f'‖{bold("M")}‖ = {it("d")} ‖{bold("F")}‖ = ‖{bold("r")}‖ ‖{bold("F")}‖ sin {it("φ")}'))
    # line of action of F (vertical through P)
    o.append(H.line(s, Px, 26, Px, 312, red, "leader", H.DASH_LOA))
    o.append(H.label(s, Px + 10, 40, f'line of action of {bold("F")}', "label2", I["secondary"]))
    # r extended past P (to show phi)
    ux, uy = (Px - Ox) / math.hypot(Px - Ox, Py - Oy), (Py - Oy) / math.hypot(Px - Ox, Py - Oy)
    o.append(H.line(s, Px, Py, Px + ux * 90, Py + uy * 90, O["dim"], "leader", H.DASH_REF))
    o.append(H.arrow(s, p, Ox, Oy, Px, Py, "dim", w="force"))
    o.append(H.label(s, (Ox + Px) / 2 - 14, (Oy + Py) / 2 - 14, bold(it("r")), "label", I["primary"], "middle"))
    o.append(H.label(s, (Ox + Px) / 2 + 30, (Oy + Py) / 2 + 6, "position of P from O", "label2", I["secondary"]))
    # phi: from the r direction to the F direction (down), at P
    a0 = math.degrees(math.atan2(uy, ux))
    o.append(arc(s, Px, Py, 34, a0, 90.0, I["secondary"]))
    am = math.radians((a0 + 90.0) / 2)
    o.append(H.label(s, Px + 50 * math.cos(am), Py + 50 * math.sin(am) + 5, it("φ"), "label", I["primary"], "middle"))
    # F
    o.append(H.arrow(s, p, Px, Py, Px, Py + 118, "force"))
    o.append(H.label(s, Px - 12, Py + 80, bold(it("F")), fill=red, anchor="end"))
    # d, with the right angle at its foot
    o.append(f'<line x1="{Ox:.1f}" y1="{Oy:.1f}" x2="{Px:.1f}" y2="{Oy:.1f}" stroke="#fff" stroke-width="{s(4.5):.1f}"/>')
    o.append(H.arrow(s, p, Ox, Oy, Px, Oy, "geometry", both=True))
    q = s(10)
    o.append(f'<path d="M{Px - q:.1f},{Oy:.1f} v{-q:.1f} h{q:.1f}" fill="none" stroke="{blu}" stroke-width="{s(1):.2f}"/>')
    o.append(H.label(s, (Ox + Px) / 2, Oy + 26, f'moment arm {it("d")} = ‖{bold("r")}‖ sin {it("φ")}', fill=blu, anchor="middle"))
    o.append(H.label(s, (Ox + Px) / 2, Oy + 46, f'perpendicular distance from O to the line of action', "label2",
                     I["secondary"], "middle"))
    o.append(H.joint_centre(s, Ox, Oy))
    o.append(H.label(s, Ox - 14, Oy + 5, "O", anchor="end"))
    o.append(H.label(s, Ox - 14, Oy + 23, "pivot", "label2", I["secondary"], "end"))
    o.append(f'<circle cx="{Px:.1f}" cy="{Py:.1f}" r="{s(4):.2f}" fill="{I["primary"]}" stroke="#fff" stroke-width="{s(1.2):.2f}"/>')
    o.append(H.label(s, Px - 12, Py - 10, "P", anchor="end"))
    aria = ("A force F acts straight down at point P. The position vector r runs from the pivot O to P, at angle phi to F. "
            "The dashed red line of action of F is vertical, and the blue moment arm d = |r| sin phi is the "
            "perpendicular distance from O to that line, with a right angle at its foot. Moment |M| = d |F|.")
    return finish(VB, aria, s, o)


# ================================================================ forearm free body (shared by #2, #13, #23)
def forearm_fbd(p, s, Ec, K):
    """Horizontal forearm + hand, isolated at the elbow. Returns (arm, body list, x of insertion / COM / grip)."""
    A = Posed(p, s, Ec, K, th=0.0)
    xi, xs, xw = Ec[0] + D_M * 100 * K, Ec[0] + R_S * 100 * K, Ec[0] + R_L * 100 * K
    o = [A.bones(upper=False)]
    return A, o, (xi, xs, xw)


# ================================================================ svg #2  Fig. 2 free-body diagram
def fig2():
    p = "m1f2_"
    VB = (0, 0, 760, 420)
    s = H.Scale(VB[2], VB[3])
    K, Ec = 14.0, (120.0, 162.0)
    A, o, (xi, xs, xw) = forearm_fbd(p, s, Ec, K)
    Ex, Ey = Ec
    red, blu, brn = O["force"], O["geometry"], O["load"]
    o = [f'<defs>{H.markers(p, s)}</defs>'] + o
    o.append(H.arrow(s, p, xi, Ey - 6, xi, Ey - 130, "force"))
    o.append(dot(s, xi, Ey - 2, red))
    o.append(H.label(s, xi + 10, Ey - 112, f'{sym("F", "m", s)} (muscle)', fill=red))
    o.append(H.label(s, xi + 10, Ey - 94, "pulls up at a short moment arm", "label2", I["secondary"]))
    o.append(H.com_mark(s, xs, Ey))
    o.append(H.arrow(s, p, xs, Ey + 9, xs, Ey + 78, "load"))
    o.append(H.label(s, xs + 10, Ey + 54, f'{sym("W", "s", s)} = {sym("m", "s", s)}{it("g")}', fill=brn))
    o.append(H.label(s, xs + 10, Ey + 72, "forearm + hand, at its COM", "label2", I["secondary"]))
    o.append(H.arrow(s, p, xw, Ey + 8, xw, Ey + 112, "load"))
    o.append(H.label(s, xw + 10, Ey + 88, f'{sym("W", "L", s)} = {sym("m", "L", s)}{it("g")}', fill=brn))
    o.append(H.label(s, xw + 10, Ey + 106, "load in the hand", "label2", I["secondary"]))
    o.append(H.joint_centre(s, Ex, Ey))
    o.append(H.label(s, Ex - 14, Ey - 10, "O", anchor="end"))
    o.append(H.label(s, Ex - 14, Ey + 8, "elbow axis", "label2", I["secondary"], "end"))
    # dimensions
    y1, y2, y3 = Ey + 40, Ey + 108, Ey + 150
    o.append(leader(s, Ex, Ey + 10, y3 + 6))
    o.append(leader(s, xi, Ey + 6, y1 + 6))
    o.append(leader(s, xs, Ey + 82, y2 + 6))
    o.append(leader(s, xw, Ey + 116, y3 + 6))
    o.append(dim(s, p, Ex, xi, y1, blu, "geometry"))
    o.append(H.label(s, xi + 8, y1 + 5, f'{sym("d", "m", s)} = 3 cm', fill=blu))
    o.append(dim(s, p, Ex, xs, y2, brn, "load"))
    o.append(H.label(s, (Ex + xs) / 2, y2 - 9, f'{sym("r", "s", s)} = {R_S * 100:.1f} cm', fill=brn, anchor="middle"))
    o.append(dim(s, p, Ex, xw, y3, brn, "load"))
    o.append(H.label(s, (Ex + xw) / 2, y3 - 9, f'{sym("r", "L", s)} = {R_L * 100:.0f} cm', fill=brn, anchor="middle"))
    lines = wrap(NIH + " Overlays drawn for this course.", 120) + [
        "Arrows are not to force scale. The joint force at O is not drawn: it has no moment about O."]
    o.append(credit(s, VB, lines))
    aria = ("Free-body diagram of the forearm and hand held horizontal (theta = 0), isolated at the elbow axis O. The "
            "muscle force F m pulls up 3 cm from O; the segment weight W s = m s g pulls down at the forearm-and-hand "
            f"centre of mass {R_S * 100:.1f} cm from O; the load weight W L = m L g pulls down at the grip {R_L * 100:.0f} cm "
            "from O. The joint force at O is not drawn because it has no moment about O.")
    return finish(VB, aria, s, o)


# ================================================================ svg #3  Fig. 3 animated forearm rotation
def fig3():
    p = "m1f3_"
    K, Ec = 6.0, (120.0, 210.0)
    VB = (0, 0, 600, 640)
    s = H.Scale(VB[2], VB[3])
    A = Posed(p, s, Ec, K, th=0.0)
    Ex, Ey = Ec
    W_L = 5.0 * G                                      # the §8 5 kg bag, line 411
    blu, brn = O["geometry"], O["load"]
    thetas = list(range(0, 91, 10))
    default = thetas.index(30)
    o = [f'<defs>{H.markers(p, s)}<g id="{p}fore">{A.fore_paths()}</g></defs>']
    # static: humerus, horizontal reference through the elbow
    E, sc = ARM["E"], K / A.k_art
    from crop_art import absolute
    o.append(f'<g transform="translate({Ex:.2f} {Ey:.2f}) scale({sc:.4f}) rotate({A.a_h:.3f}) translate({-E[0]} {-E[1]})">'
             f'<path d="{absolute(A.paths[3])}" {A._st()[1]}/></g>')
    o.append(H.line(s, Ex, Ey, Ex + 54 * K, Ey, O["dim"], "leader", H.DASH_REF))
    o.append(H.label(s, Ex + 54 * K + 6, Ey + 5, "horizontal", "label2", I["muted"]))
    o.append(H.label(s, 330, 150, f'{sym("r", "L", s)} = {R_L * 100:.0f} cm, {sym("W", "L", s)} = 5 kg × {G} m/s² = {W_L:.1f} N',
                     "label2", I["secondary"]))
    o.append(H.label(s, 330, 168, "the bag hangs straight down at every angle", "label2", I["secondary"]))
    frames = []
    for k, th in enumerate(thetas):
        c = math.cos(math.radians(th))
        A.th = th
        Gp = A.F((R_L * 100, 0.0))
        f = [bag(s, Gp, K), f'<g transform="{A.fore_tf(th)}"><use href="#{p}fore"/></g>']
        f.append(H.arrow(s, p, Gp[0], Gp[1] + 10.5 * K, Gp[0], Gp[1] + 16.5 * K, "load"))
        f.append(H.label(s, Gp[0] + 10, Gp[1] + 15 * K, sym("W", "L", s), fill=brn))
        # line of action, up to the elbow's horizontal
        f.append(H.line(s, Gp[0], Ey, Gp[0], Gp[1] + 4 * K, O["force"], "leader", H.DASH_LOA))
        # angle theta
        if th > 0:
            f.append(arc(s, Ex, Ey, 9 * K, 0.0, th, I["secondary"]))
            am = math.radians(th / 2)
            f.append(H.label(s, Ex + 11.5 * K * math.cos(am), Ey + 11.5 * K * math.sin(am) + 5, it("θ"), "label",
                             I["primary"], "middle"))
        # moment arm d = r_L cos theta (blue bar at the elbow's height)
        dcm = R_L * 100 * c
        if dcm > 0.5:
            f.append(f'<line x1="{Ex:.1f}" y1="{Ey:.1f}" x2="{Gp[0]:.1f}" y2="{Ey:.1f}" stroke="#fff" stroke-width="{s(5):.1f}"/>')
            f.append(H.arrow(s, p, Ex, Ey, Gp[0], Ey, "geometry", both=True))
        f.append(H.joint_centre(s, Ex, Ey))
        f.append(H.label(s, Ex + max(dcm * K / 2, 0) + (0 if dcm > 8 else 14), Ey - 12,
                         f'{it("d")}', fill=blu, anchor="middle" if dcm > 8 else "start"))
        # read-out
        tq = W_L * R_L * c
        f.append(H.label(s, 330, 40, f'θ = {th}°'))
        f.append(H.label(s, 330, 62, f'{it("d")} = {sym("r", "L", s)} cos θ = {dcm:.1f} cm', fill=blu))
        f.append(H.label(s, 330, 84, f'τ = {sym("W", "L", s)} {it("d")} = {tq:.1f} N·m'))
        f.append(H.label(s, 330, 102, f'({c * 100:.0f} % of the horizontal value)', "label2", I["secondary"]))
        frames.append(H.frame(k, default, "".join(f)))
    o += frames
    o.append(H.label(s, Ex - 14, Ey + 24, "elbow", "label2", I["secondary"], "end"))
    lines = wrap(NIH + " Bag and overlays drawn for this course.", 104)
    o.append(credit(s, VB, lines))
    aria = ("Side view of an arm, humerus vertical, with the forearm lowered about the elbow from horizontal (theta = 0) "
            "to hanging straight down (theta = 90 degrees); the still shows theta = 30 degrees. A 5 kg bag hangs from the "
            "hand 35 cm from the elbow and its weight W L always points straight down. The blue bar is the horizontal "
            "moment arm d = r L cos theta, 30.3 cm at 30 degrees and 0 at 90 degrees, and the torque W L d falls in step, "
            "from 17.2 to 0 N m. A slider steps theta from 0 to 90 degrees.")
    return finish(VB, aria, s, o, H.frames_attr("θ", [f"{t}°" for t in thetas], default))


# ================================================================ svg #4  Fig. 4 mechanical disadvantage
def fig4():
    p = "m1f4_"
    K, Ec = 10.0, (130.0, 354.0)
    VB = (0, 0, 760, 584)
    s = H.Scale(VB[2], VB[3])
    A = Posed(p, s, Ec, K, th=0.0)
    Ex, Ey = Ec
    Gp = A.F((R_L * 100, 0.0))
    ratio = R_L / D_M
    red, blu, brn = O["force"], O["geometry"], O["load"]
    o = [f'<defs>{H.markers(p, s)}</defs>', bag(s, Gp, K)]
    o.append(H.arrow(s, p, Gp[0], Gp[1] + 10.5 * K, Gp[0], Gp[1] + 15.5 * K, "load"))
    o.append(H.label(s, Gp[0] + 10, Gp[1] + 14 * K, f'load {sym("W", "L", s)}', fill=brn))
    o.append(H.label(s, Gp[0] + 10, Gp[1] + 14 * K + 18, "(small)", "label2", I["secondary"]))
    o.append(A.bones())
    bic, bez, width = A.biceps()
    o.append(bic)
    loa, _ = A.loa()
    o.append(loa)
    arr, S0, _ = f_m_arrow(s, p, A, 74)
    o.append(arr)
    o.append(H.label(s, S0[0] + 10, S0[1] - 50, f'effort {sym("F", "m", s)} ≈ {ratio:.0f} × {sym("W", "L", s)}', fill=red))
    o.append(H.label(s, S0[0] + 10, S0[1] - 32, "(large)", "label2", I["secondary"]))
    o.append(H.arrow(s, p, Ex, Ey, A.P[0], A.P[1], "geometry", both=True))
    o.append(H.joint_centre(s, Ex, Ey))
    o.append(H.label(s, Ex - 14, Ey - 8, "pivot", anchor="end"))
    o.append(H.label(s, Ex - 14, Ey + 10, "(elbow axis)", "label2", I["secondary"], "end"))
    bx, by, bnx, bny = bez(0.55)
    e = (bx + abs(bnx) * width(0.55), by)
    o.append(H.line(s, e[0] + 2, e[1], 212, e[1] - 6, T["muscle"][1]))
    o.append(H.label(s, 216, e[1] - 2, "flexor (biceps)", fill=T["muscle"][1]))
    # dimensions
    yd, yr = Ey + 5.0 * K, Ey + 11.0 * K
    o.append(leader(s, Ex, Ey + 3.5 * K, yr + 6))
    o.append(leader(s, A.P[0], Ey + 1.5 * K, yd + 6))
    o.append(leader(s, Gp[0], Gp[1] + 10 * K, yr + 6))
    o.append(dim(s, p, Ex, A.P[0], yd, blu, "geometry"))
    o.append(H.label(s, A.P[0] + 8, yd + 5, f'{sym("d", "m", s)} ≈ {A.d_cm:.0f} cm', fill=blu))
    o.append(dim(s, p, Ex, Gp[0], yr, brn, "load"))
    o.append(H.label(s, (Ex + Gp[0]) / 2 - 40, yr - 9, f'{sym("r", "L", s)} ≈ {R_L * 100:.0f} cm', fill=brn, anchor="middle"))
    # lever reading (upper right)
    x0 = 400
    o.append(H.label(s, x0, 60, "Third-class lever:"))
    o.append(H.label(s, x0, 80, "the effort acts between pivot and load", "label2", I["secondary"]))
    o.append(lever_icon(s, p, x0 + 10, 140, 300, {"pivot": 0.0, "effort": D_M / R_L, "load": 1.0},
                        ("pivot", "effort", "load")))
    o.append(H.label(s, x0, 222, f'{sym("F", "m", s)}{sym("d", "m", s)} = {sym("W", "L", s)}{sym("r", "L", s)}'))
    o.append(H.label(s, x0, 244, f'{sym("F", "m", s)} = ({sym("r", "L", s)}/{sym("d", "m", s)}) {sym("W", "L", s)} '
                     f'≈ (35/3) {sym("W", "L", s)} ≈ {ratio:.0f} {sym("W", "L", s)}'))
    lines = wrap(NIH, 120) + ["Biceps, bag and overlays drawn for this course. Arrows are not to force scale."]
    o.append(credit(s, VB, lines))
    aria = ("Side view of an arm with the humerus vertical and the forearm horizontal, holding a bag. The flexor (biceps) "
            f"inserts on the forearm with moment arm d m of about {A.d_cm:.0f} cm from the elbow axis (the pivot) and pulls "
            f"up with the effort F m; the bag's weight W L hangs about {R_L * 100:.0f} cm from the pivot. Torque balance "
            f"F m d m = W L r L gives F m about {ratio:.0f} times W L. A small lever sketch shows the third-class order: "
            "pivot, then effort, then load.")
    return finish(VB, aria, s, o)


# ================================================================ problem figures (display_w = 400)
def nih_credit(s, VB, n=70, extra=None):
    return credit(s, VB, wrap(NIH + " " + (extra or "Overlays drawn for this course."), n))


def arm_with_biceps(o, s, p, A, L=40):
    """Bones, biceps and its pull. Returns the F_m arrow start."""
    o.append(A.bones())
    bic, _, _ = A.biceps()
    o.append(bic)
    arr, S0, _ = f_m_arrow(s, p, A, L)
    o.append(arr)
    return S0


# ---------------------------------------------------------------- svg #11  C1 two poses, same load
def fig11():
    p = "m1f11_"
    VB = (0, 0, 440, 380)
    s = H.Scale(VB[2], VB[3], display_w=400)
    K = 3.6
    blu, brn, red = O["geometry"], O["load"], O["force"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    yd = 318
    for Ec, th in (((46.0, 165.0), 0.0), ((262.0, 165.0), 60.0)):
        A = Posed(p, s, Ec, K, th=th)
        Gp = A.F((R_L * 100, 0.0))
        r = 3.0 * K
        S0 = arm_with_biceps(o, s, p, A)
        o.append(plate(s, Gp[0], Gp[1], r))
        kx, ky = (Gp[0] - r - 4, Gp[1] + r + 14) if th == 0 else (Gp[0] - r - 6, Gp[1] + 5)
        o.append(H.label(s, kx, ky, "4 kg", "label2", I["secondary"], "end"))
        o.append(H.arrow(s, p, Gp[0], Gp[1] + r + 2, Gp[0], Gp[1] + r + 38, "load"))
        o.append(H.label(s, Gp[0] + 7, Gp[1] + r + 34, it("W"), fill=brn))
        o.append(H.label(s, S0[0] + 4, S0[1] - 30, sym("F", "m", s), fill=red))
        o.append(H.joint_centre(s, *Ec))
        # line of action of W down to the moment-arm row, and the elbow's own leader
        o.append(H.line(s, Gp[0], Gp[1] + r + 40, Gp[0], yd + 6, O["dim"], "leader", H.DASH_REF))
        o.append(leader(s, Ec[0], Ec[1] + 14, yd + 6))
        o.append(dim(s, p, Ec[0], Gp[0], yd, blu, "geometry"))
        o.append(H.label(s, (Ec[0] + Gp[0]) / 2, yd - 7, f'{it("d")}({th:.0f}°)', "label2", blu, "middle"))
        o.append(H.label(s, Ec[0] - 30, 22, f'θ = {th:.0f}°'))
        if th > 0:
            o.append(H.line(s, Ec[0], Ec[1], Ec[0] + 22 * K, Ec[1], O["dim"], "leader", H.DASH_REF))
            o.append(arc(s, Ec[0], Ec[1], 10 * K, 0.0, th, I["secondary"]))
            am = math.radians(th / 2)
            o.append(H.label(s, Ec[0] + 12.5 * K * math.cos(am) + 4, Ec[1] + 12.5 * K * math.sin(am) + 5, "60°",
                             "label2", I["primary"]))
    o.append(nih_credit(s, VB, 70, "Muscle, dumbbells and overlays drawn for this course."))
    aria = ("Problem C1 setup: two side views of the same arm, humerus vertical, each holding a 4 kg dumbbell. Left: "
            "forearm horizontal, theta = 0. Right: forearm 60 degrees below horizontal. In each the biceps pulls up with "
            "F m, the weight W hangs down, and a blue bar marks the horizontal distance d from the elbow axis to the "
            "weight's line of action.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- forearm free body for C3 and D3
def fbd_problem(p, s, Ec, K, o, J=True):
    A, body, (xi, xs, xw) = forearm_fbd(p, s, Ec, K)
    Ex, Ey = Ec
    red, brn = O["force"], O["load"]
    o += body
    o.append(H.arrow(s, p, xi, Ey - 5, xi, Ey - 78, "force"))
    o.append(dot(s, xi, Ey - 2, red))
    o.append(H.label(s, xi + 8, Ey - 60, sym("F", "m", s), fill=red))
    o.append(H.com_mark(s, xs, Ey))
    o.append(H.arrow(s, p, xs, Ey + 9, xs, Ey + 52, "load"))
    o.append(H.label(s, xs + 8, Ey + 44, sym("W", "s", s), fill=brn))
    o.append(H.arrow(s, p, xw, Ey + 8, xw, Ey + 72, "load"))
    o.append(H.label(s, xw + 8, Ey + 64, sym("W", "L", s), fill=brn))
    if J:
        o.append(H.arrow(s, p, Ex, Ey + 9, Ex, Ey + 70, "reaction"))
        o.append(H.label(s, Ex - 8, Ey + 62, bold(it("J")), anchor="end"))
    return xi, xs, xw


# ---------------------------------------------------------------- svg #13  C3 segment free body
def fig13():
    p = "m1f13_"
    VB = (0, 0, 440, 300)
    s = H.Scale(VB[2], VB[3], display_w=400)
    Ec = (48.0, 150.0)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(H.label(s, 8, 22, f'Σ{bold("M")} about O = 0 → {sym("F", "m", s)}   ({bold(it("J"))} has no moment about O)', "label2"))
    o.append(H.label(s, 8, 42, f'Σ{bold("F")} = 0 → {bold(it("J"))}', "label2"))
    fbd_problem(p, s, Ec, 8.0, o)
    o.append(H.joint_centre(s, *Ec))
    o.append(H.label(s, Ec[0] - 8, Ec[1] - 10, "O", anchor="end"))
    o.append(H.label(s, 8, 248, f'joint reaction {bold(it("J"))}: force of the humerus on the forearm', "label2", I["secondary"]))
    o.append(nih_credit(s, VB, 74))
    aria = ("Problem C3 setup: free body of the horizontal forearm and hand, isolated at the elbow O. The muscle force F m "
            "pulls up near the elbow, the segment weight W s and the load W L pull down, and the joint reaction J of the "
            "humerus on the forearm acts at O, drawn downward. Sum of moments about O = 0 gives F m (J has no moment "
            "about O); sum of forces = 0 gives J.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #23  D3 two reference points
def fig23():
    p = "m1f23_"
    VB = (0, 0, 440, 280)
    s = H.Scale(VB[2], VB[3], display_w=400)
    Ec = (48.0, 140.0)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(H.label(s, 8, 24, f'Σ{bold("F")} = 0 ⇒ the same net moment about A or B', "label2"))
    xi, xs, xw = fbd_problem(p, s, Ec, 8.0, o)
    o.append(ref_point(s, *Ec))
    o.append(H.label(s, Ec[0] - 9, Ec[1] - 10, "A", "label", I["primary"], "end"))
    o.append(H.label(s, Ec[0] - 9, Ec[1] + 8, "elbow", "label2", I["secondary"], "end"))
    o.append(ref_point(s, xw, Ec[1]))
    o.append(H.label(s, xw - 4, Ec[1] - 12, "B", "label", I["primary"], "end"))
    o.append(H.label(s, xw + 10, Ec[1] - 26, "hand", "label2", I["secondary"]))
    o.append(nih_credit(s, VB, 74))
    aria = ("Problem D3 setup: the same free body of the horizontal forearm and hand as C3, with muscle force F m, "
            "segment weight W s, load W L and joint reaction J, and two candidate reference points for moments: A at "
            "the elbow and B at the hand. Since the sum of forces is zero, the net moment is the same about A or B.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #14  C4 elbow vs ankle lever
FOOT = dict(
    # python -I crop_art.py ../svg_paths/Lower_leg_muscles.svg m01foot 20 840 480 1160 --drop "#Names, text" --png 0.4
    box=(20, 860, 460, 300),        # Lower_leg_muscles.svg user space shown in the figure
    ankle=fit_circle(F21["dome"]),  # talar dome centre (m05 F21 landmarks)
    heel=F21["insertion"],          # Achilles insertion on the calcaneus
    tendon=F21["tendon_c"],
    ball=(150.0, 1130.0),           # ESTIMATE: under the metatarsal heads, 0.73 of the heel-to-toe length (x 459 -> 40)
)                                   # from the heel; sole line y 1130, read off a coordinate grid over the crop


def fig14():
    p = "m1f14_"
    VB = (0, 0, 440, 668)
    s = H.Scale(VB[2], VB[3], display_w=400)
    red, blu, brn = O["force"], O["geometry"], O["load"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # ---- elbow (top)
    o.append(H.label(s, 8, 20, "Elbow flexion"))
    K, Ec = 4.0, (52.0, 172.0)
    A = Posed(p, s, Ec, K, th=0.0)
    Gp = A.F((R_L * 100, 0.0))
    S0 = arm_with_biceps(o, s, p, A)
    r = 2.6 * K
    o.append(plate(s, Gp[0], Gp[1], r))
    o.append(H.arrow(s, p, Gp[0], Gp[1] + r + 2, Gp[0], Gp[1] + r + 34, "load"))
    o.append(H.label(s, Gp[0] + 7, Gp[1] + r + 30, "load", "label2", brn))
    o.append(H.label(s, S0[0] + 5, S0[1] - 28, "effort", "label2", red))
    o.append(H.joint_centre(s, *Ec))
    o.append(H.label(s, Ec[0] - 8, Ec[1] + 22, "pivot", "label2", I["primary"], "middle"))
    yd = Ec[1] + 72
    o.append(leader(s, A.P[0], Ec[1] + 6, yd - 16 + 6))
    o.append(leader(s, Ec[0], Ec[1] + 28, yd + 6))
    o.append(leader(s, Gp[0], Gp[1] + r + 38, yd + 6))
    o.append(dim(s, p, Ec[0], A.P[0], yd - 16, blu, "geometry"))
    o.append(H.label(s, A.P[0] + 6, yd - 12, "effort arm", "label2", blu))
    o.append(dim(s, p, Ec[0], Gp[0], yd, blu, "geometry"))
    o.append(H.label(s, (Ec[0] + Gp[0]) / 2 + 30, yd + 16, "load arm", "label2", blu, "middle"))
    o.append(lever_icon(s, p, 282, 120, 140, {"pivot": 0.0, "effort": D_M / R_L, "load": 1.0}, ("pivot", "", "load")))
    o.append(H.label(s, 282 + 140 * D_M / R_L + 6, 120 - s(30), "effort", "label2", I["primary"]))
    # ---- ankle (bottom): InjuryMap lateral foot, toes left
    y0 = 300
    o.append(H.line(s, 8, y0 - 18, 432, y0 - 18, I["rule"], "leader"))
    o.append(H.label(s, 8, y0 + 4, "Ankle push-off (rising on the toes)"))
    bx, by, bw, bh = FOOT["box"]
    sc, X0, Y0 = 0.62, 6.0, y0 + 6
    M = lambda q: (X0 + (q[0] - bx) * sc, Y0 + (q[1] - by) * sc)   # noqa: E731
    art = inner_svg(_read("Lower_leg_muscles_crop_m01foot.svg"))
    assert 'id="Names"' not in art and "<text" not in art
    o.append(f'<g transform="translate({X0 - bx * sc:.2f} {Y0 - by * sc:.2f}) scale({sc})">'
             + art_image("<svg>" + art + "</svg>", FOOT["box"]) + "</g>")
    ank, heel, ball, ten = M(FOOT["ankle"][:2]), M(FOOT["heel"]), M(FOOT["ball"]), M(FOOT["tendon"])
    o.append(H.line(s, 6, ball[1], 330, ball[1], I["secondary"], "ref"))
    o.append(H.label(s, 336, ball[1] + 5, "ground", "label2", I["muted"]))
    ux, uy = ten[0] - heel[0], ten[1] - heel[1]
    n = math.hypot(ux, uy)
    o.append(H.arrow(s, p, heel[0], heel[1], heel[0] + ux / n * 70, heel[1] + uy / n * 70, "force"))
    o.append(dot(s, heel[0], heel[1], red))
    o.append(H.label(s, heel[0] + 12, heel[1] + 18, "effort", "label2", red))
    o.append(H.label(s, heel[0] + 12, heel[1] + 33, "(Achilles → heel)", "label2", I["secondary"]))
    o.append(H.arrow(s, p, ank[0], ank[1] - 74, ank[0], ank[1] - 8, "load"))
    lx = 146
    o.append(H.line(s, lx + 3, ank[1] - 64, ank[0] - 3, ank[1] - 64, brn))
    o.append(H.label(s, lx, ank[1] - 60, "load", "label2", brn, "end"))
    o.append(H.label(s, lx, ank[1] - 45, "(body weight", "label2", I["secondary"], "end"))
    o.append(H.label(s, lx, ank[1] - 30, "through the ankle)", "label2", I["secondary"], "end"))
    o.append(H.joint_centre(s, *ank))
    h = s(9)
    o.append(f'<path d="M{ball[0]:.1f},{ball[1]:.1f} l{-h * 0.7:.1f},{h:.1f} h{h * 1.4:.1f} Z" fill="{I["secondary"]}"/>')
    o.append(H.label(s, 8, ball[1] + 22, "pivot", "label2", I["primary"]))
    o.append(H.label(s, 8, ball[1] + 37, "(ball of foot)", "label2", I["secondary"]))
    yd = ball[1] + 54
    for x in (ball[0], ank[0], heel[0]):
        o.append(leader(s, x, ball[1] + (12 if x == ball[0] else 3), yd + 6 + (16 if x != ank[0] else 0)))
    o.append(dim(s, p, ball[0], ank[0], yd, blu, "geometry"))
    o.append(H.label(s, (ball[0] + ank[0]) / 2, yd - 5, "load arm", "label2", blu, "middle"))
    o.append(dim(s, p, ball[0], heel[0], yd + 16, blu, "geometry"))
    o.append(H.label(s, heel[0] + 6, yd + 20, "effort arm", "label2", blu))
    fl = (ank[0] - ball[0]) / (heel[0] - ball[0])
    o.append(lever_icon(s, p, 300, 350, 110, {"pivot": 0.0, "load": fl, "effort": 1.0}, ("pivot", "effort", "load")))
    c2 = H.ATTRIBUTION["by-sa"].format(author="InjuryMap", title="Lower leg muscles.svg",
                                       changes="Foot cropped, labels removed, overlays added.").replace("Art:", "Foot:")
    o.append(credit(s, VB, wrap(NIH.replace("Art:", "Arm:") + " Muscle, dumbbell and overlays drawn for this course.", 74)
                    + wrap(c2, 74)))
    aria = ("Problem C4 setup, two levers. Top: side view of an arm, humerus vertical, forearm horizontal, holding a "
            "dumbbell; the pivot is the elbow axis, the effort is the biceps pull 3 cm from it, and the load hangs at "
            "the hand, so the effort sits between pivot and load. Bottom: lateral view of the foot (InjuryMap art) at "
            "push-off; the pivot is the ball of the foot on the ground, body weight bears down through the ankle, and "
            "the Achilles tendon pulls up at the heel, so the load sits between pivot and effort. Blue bars mark each "
            "effort arm and load arm; a small lever sketch beside each shows the order.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #19 C9 / svg #28 D8  adult and half-scale limb
def similar(p, d8):
    VB = (0, 0, 440, 330)
    s = H.Scale(VB[2], VB[3], display_w=400)
    brn, blu = O["load"], O["geometry"]
    o = [f'<defs>{H.markers(p, s)}</defs>']
    if d8:
        o.append(H.label(s, 232, 26, f'mass ∝ {it("L")}³, moment arm ∝ {it("L")}', "label2"))
        o.append(H.label(s, 232, 44, f'⇒ holding torque τ ∝ {it("L")}⁴', "label2"))
    for K, Ec, name, rn, wn in ((4.0, (52.0, 160.0), "adult", "r", "W"),
                                (2.0, (300.0, 196.0), "half scale" if d8 else "child", "r/2" if d8 else "r′", "W′")):
        A = Posed(p, s, Ec, K, th=0.0)
        arm_with_biceps(o, s, p, A, 10 * K)
        xs = Ec[0] + R_S * 100 * K
        o.append(H.com_mark(s, xs, Ec[1]))
        o.append(H.arrow(s, p, xs, Ec[1] + 9, xs, Ec[1] + 9 + 10 * K, "load"))
        o.append(H.label(s, xs + 7, Ec[1] + 6 + 10 * K, it(wn), fill=brn))
        o.append(H.joint_centre(s, *Ec))
        yd = Ec[1] + 9 + 12 * K + 12
        o.append(leader(s, Ec[0], Ec[1] + 10, yd + 6))
        o.append(leader(s, xs, Ec[1] + 11 + 10 * K, yd + 6))
        o.append(dim(s, p, Ec[0], xs, yd, blu, "geometry"))
        o.append(H.label(s, xs + 6, yd + 5, it(rn), "label2", blu))
        size = (it("L") if K == 4.0 else f'{it("L")}/2') if d8 else ("size " + it("L") if K == 4.0 else f'size {it("L")}/2')
        o.append(H.label(s, Ec[0] + 90 * K / 4, 268, f'{name}, {size}', "label", I["primary"], "middle"))
    o.append(nih_credit(s, VB, 74, "Muscle and overlays drawn for this course; the half-scale arm is the same art scaled by 1/2."))
    if d8:
        aria = ("Problem D8 setup: the same arm art drawn at full size L and at half size L/2, each with the forearm "
                "horizontal, the biceps, and the forearm's own weight acting at its centre of mass a distance r (and r/2) "
                "from the elbow. Mass scales as L cubed and moment arm as L, so the holding torque scales as L to the "
                "fourth power.")
    else:
        aria = ("Problem C9 setup: an adult arm (size L) and a geometrically similar half-scale arm (size L/2), the same "
                "art scaled by one half, each with the forearm horizontal, the biceps, and the forearm's own weight W or "
                "W prime acting at its centre of mass a distance r or r prime from the elbow.")
    return finish(VB, aria, s, o)


def fig19():
    return similar("m1f19_", False)


def fig28():
    return similar("m1f28_", True)


# ---------------------------------------------------------------- svg #20  C10 door, top view
def fig20():
    p = "m1f20_"
    VB = (0, 0, 440, 250)
    s = H.Scale(VB[2], VB[3], display_w=400)
    red, blu = O["force"], O["geometry"]
    hx, y, L, t = 60.0, 120.0, 300.0, 14.0
    o = [f'<defs>{H.markers(p, s)}</defs>']
    for x0, x1 in ((8, hx - 6), (hx + L + 8, 432)):          # wall stubs either side of the doorway
        o.append(f'<rect x="{x0}" y="{y - t / 2 - 3:.1f}" width="{x1 - x0}" height="{t + 6}" fill="{I["rule"]}"/>')
    o.append(arc(s, hx, y, L, 3.0, 12.0, I["muted"]).replace(                       # swing of the free edge
        'stroke-width', f'stroke-dasharray="{s(4):.1f} {s(3):.1f}" marker-end="url(#{p}a_dim)" stroke-width'))
    o.append(f'<rect x="{hx:.1f}" y="{y - t / 2:.1f}" width="{L:.1f}" height="{t}" fill="#f7f4ef" '
             f'stroke="{I["primary"]}" stroke-width="{s(1.2):.2f}"/>')
    xh = hx + L - 18
    o.append(f'<rect x="{xh - 6:.1f}" y="{y + t / 2:.1f}" width="12" height="5" fill="{I["secondary"]}"/>')
    o.append(f'<circle cx="{hx:.1f}" cy="{y:.1f}" r="{s(5):.2f}" fill="{I["primary"]}"/>')
    o.append(H.label(s, hx, y + 32, "hinge", "label2", I["primary"], "middle"))
    o.append(H.label(s, xh, y + 32, "handle", "label2", I["primary"], "middle"))
    o.append(H.label(s, (hx + xh) / 2, y + 32, "door (top view)", "label2", I["secondary"], "middle"))
    for x, t1, t2 in ((hx, "push at the hinge:", "no turn"), (xh, "push at the handle:", "the door turns")):
        o.append(H.arrow(s, p, x, y - 70, x, y - t / 2 - 2, "force"))
        side, anc = (6, "start") if x == hx else (-6, "end")
        o.append(H.label(s, x + side, y - 92, t1, "label2", I["primary"], anc))
        o.append(H.label(s, x + side, y - 76, t2, "label2", I["secondary"], anc))
        o.append(H.label(s, x + 7, y - 44, bold(it("F")), fill=red))
    yd = 214
    o.append(leader(s, hx, y + 40, yd + 6))
    o.append(leader(s, xh, y + 40, yd + 6))
    o.append(dim(s, p, hx, xh, yd, blu, "geometry"))
    o.append(H.label(s, (hx + xh) / 2, yd + 20, f'moment arm of the handle push = ‖{bold("r")}‖', "label2", blu, "middle"))
    o.append(H.label(s, hx + 8, y - 20, f'{bold("r")} = 0', "label2", I["secondary"]))
    aria = ("Problem C10 setup: top view of a door hinged at the left. The same push F, perpendicular to the door, is "
            "applied at the hinge, where r = 0 and the door does not turn, and at the handle, where the moment arm is "
            "the full distance r from the hinge and the door swings along the dashed arc.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #21  D1 long-handled tool
def fig21():
    p = "m1f21_"
    VB = (0, 0, 440, 320)
    s = H.Scale(VB[2], VB[3], display_w=400)
    K, Ec = 4.4, (40.0, 150.0)
    S_CM = 22.0                                     # drawn reach s (D1 is symbolic)
    brn = O["load"]
    A = Posed(p, s, Ec, K, th=0.0)
    Gp = A.F((R_L * 100, 0.0))
    tip = A.F((R_L * 100 + S_CM, 0.0))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(f'<rect x="{Gp[0] - 2 * K:.1f}" y="{Gp[1] - 0.6 * K:.1f}" width="{tip[0] - Gp[0] + 2 * K:.1f}" '
             f'height="{1.2 * K:.1f}" rx="{0.6 * K:.1f}" fill="{I["rule"]}" stroke="{I["secondary"]}" stroke-width="{s(0.8):.2f}"/>')
    o.append(A.bones())
    o.append(plate(s, tip[0], tip[1], 2.4 * K))
    o.append(H.arrow(s, p, tip[0], tip[1] + 2.4 * K + 2, tip[0], tip[1] + 2.4 * K + 44, "load"))
    o.append(H.label(s, tip[0] + 7, tip[1] + 2.4 * K + 38, it("W"), fill=brn))
    o.append(H.label(s, tip[0], tip[1] - 3 * K - 4, "load at the tool tip", "label2", I["secondary"], "middle"))
    o.append(H.joint_centre(s, *Ec))
    o.append(H.label(s, Ec[0], Ec[1] + 24, "elbow", "label2", I["secondary"], "middle"))
    y1, y2 = Ec[1] + 74, Ec[1] + 104
    o.append(leader(s, Ec[0], Ec[1] + 30, y2 + 6))
    o.append(leader(s, Gp[0], Gp[1] + 10, y1 + 6))
    o.append(leader(s, tip[0], tip[1] + 2.4 * K + 48, y2 + 6))
    o.append(dim(s, p, Ec[0], Gp[0], y1, brn, "load"))
    o.append(H.label(s, (Ec[0] + Gp[0]) / 2, y1 - 6, f'{sym("r", "L", s, "label2")} (to the grip)', "label2", brn, "middle"))
    o.append(dim(s, p, Gp[0], tip[0], y1, brn, "load"))
    o.append(H.label(s, (Gp[0] + tip[0]) / 2, y1 - 6, it("s"), "label", brn, "middle"))
    o.append(dim(s, p, Ec[0], tip[0], y2, brn, "load"))
    o.append(H.label(s, (Ec[0] + tip[0]) / 2, y2 - 6, f'{sym("r", "L", s, "label2")} + {it("s")}', "label2", brn, "middle"))
    o.append(nih_credit(s, VB, 74, "Tool and overlays drawn for this course."))
    aria = ("Problem D1 setup: side view of an arm, humerus vertical and forearm horizontal, gripping a long-handled tool "
            "that extends along the forearm line. The load W sits at the tool tip, a distance s beyond the grip, so its "
            "horizontal moment arm about the elbow is r L + s.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #22  D2 whole upper limb at the shoulder
def fig22():
    p = "m1f22_"
    VB = (0, 0, 440, 310)
    s = H.Scale(VB[2], VB[3], display_w=400)
    K = 4.6
    Sh = (26.0, 104.0)
    Ec = (Sh[0] + UPPER_CM * K, Sh[1])
    brn = O["load"]
    A = Posed(p, s, Ec, K, th=0.0, hum=180.0)
    o = [f'<defs>{H.markers(p, s)}</defs>', A.bones()]
    xa, xs, xw = Sh[0] + UPPER_COM * UPPER_CM * K, Ec[0] + R_S * 100 * K, Ec[0] + R_L * 100 * K
    o.append(plate(s, xw, Sh[1], 2.4 * K))
    rows = []
    for x, m, top in ((xa, "a", 8), (xs, "s", 8), (xw, "L", 2.4 * K + 2)):
        if m != "L":
            o.append(H.com_mark(s, x, Sh[1]))
        o.append(H.arrow(s, p, x, Sh[1] + top + 1, x, Sh[1] + top + 46, "load"))
        o.append(H.label(s, x + 7, Sh[1] + top + 36, f'{sym("m", m, s)}{it("g")}', fill=brn))
        rows.append((x, Sh[1] + top + 50))
    o.append(H.joint_centre(s, *Sh))
    o.append(H.joint_centre(s, *Ec))
    o.append(H.label(s, Sh[0] - 4, Sh[1] - 16, "shoulder axis", "label2", I["primary"]))
    o.append(H.label(s, Sh[0] + 30, Sh[1] - 34, "(humeral head not drawn)", "label2", I["muted"]))
    o.append(H.label(s, Ec[0] + 6, Ec[1] - 14, "elbow", "label2", I["secondary"]))
    y0 = 196
    o.append(leader(s, Sh[0], Sh[1] + 10, y0 + 2 * 22 + 6))
    names = (sym("r", "a", s, "label2"), sym("r", "s", s, "label2") + "′", sym("r", "L", s, "label2") + "′")
    for k, ((x, ytop), name) in enumerate(zip(rows, names)):
        yy = y0 + k * 22
        o.append(leader(s, x, ytop, yy + 6))
        o.append(dim(s, p, Sh[0], x, yy, brn, "load"))
        o.append(H.label(s, x + 6, yy + 5, name, "label2", brn))
    o.append(H.label(s, 8, 24, "limb straight and horizontal (θ = 0)", "label2", I["secondary"]))
    o.append(nih_credit(s, VB, 74, "Dumbbell and overlays drawn for this course. Distances are from the shoulder axis."))
    aria = ("Problem D2 setup: the whole upper limb held straight and horizontal from the shoulder axis, the same arm art "
            "with the humerus and forearm in line. Three weights pull down: the upper arm m a g at its centre of mass r a "
            "from the shoulder, the forearm and hand m s g at r s prime, and the hand load m L g at r L prime.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #24  D4 inclined muscle line
def fig24():
    p = "m1f24_"
    VB = (0, 0, 440, 340)
    s = H.Scale(VB[2], VB[3], display_w=400)
    K, Ec = 8.0, (72.0, 160.0)
    R_M, PHI = 4.0, 55.0                       # drawn values (D4 is symbolic)
    red, blu, brn = O["force"], O["geometry"], O["load"]
    A, body, _ = forearm_fbd(p, s, Ec, K)
    Ex, Ey = Ec
    xi, xw = Ex + R_M * K, Ex + R_L * 100 * K
    o = [f'<defs>{H.markers(p, s)}</defs>'] + body
    ux, uy = -math.cos(math.radians(PHI)), -math.sin(math.radians(PHI))
    Ip = (xi, Ey - 2)
    o.append(H.line(s, Ip[0] - ux * 30, Ip[1] - uy * 30, Ip[0] + ux * 150, Ip[1] + uy * 150, red, "leader", H.DASH_LOA))
    o.append(H.arrow(s, p, Ip[0], Ip[1], Ip[0] + ux * 96, Ip[1] + uy * 96, "force"))
    o.append(dot(s, *Ip, red))
    o.append(H.label(s, Ip[0] + ux * 96 + 12, Ip[1] + uy * 96 + 4, sym("F", "m", s), fill=red))
    o.append(arc(s, Ip[0], Ip[1], 34, 180.0, 180.0 + PHI, I["secondary"]))
    am = math.radians(180.0 + PHI / 2)
    o.append(H.label(s, Ip[0] + 48 * math.cos(am), Ip[1] + 48 * math.sin(am) + 4, it("φ"), "label", I["primary"], "middle"))
    o.append(H.arrow(s, p, Ex, Ey + 9, Ex, Ey + 66, "reaction"))
    o.append(H.label(s, Ex - 8, Ey + 58, sym("J", "y", s), anchor="end"))
    o.append(H.arrow(s, p, Ex - 64, Ey, Ex - 9, Ey, "reaction"))
    o.append(H.label(s, Ex - 60, Ey - 10, sym("J", "x", s)))
    o.append(H.arrow(s, p, xw, Ey + 8, xw, Ey + 72, "load"))
    o.append(H.label(s, xw + 8, Ey + 64, sym("W", "L", s), fill=brn))
    o.append(H.joint_centre(s, Ex, Ey))
    o.append(H.label(s, Ex - 36, Ey + 22, "elbow", "label2", I["secondary"], "middle"))
    y1, y2 = Ey + 98, Ey + 122
    o.append(leader(s, Ex, Ey + 70, y2 + 6))
    o.append(leader(s, xi, Ey + 8, y1 + 6))
    o.append(leader(s, xw, Ey + 76, y2 + 6))
    o.append(dim(s, p, Ex, xi, y1, blu, "geometry"))
    o.append(H.label(s, xi + 6, y1 + 5, sym("r", "m", s, "label2"), "label2", blu))
    o.append(dim(s, p, Ex, xw, y2, brn, "load"))
    o.append(H.label(s, (Ex + xw) / 2, y2 - 6, sym("r", "L", s, "label2"), "label2", brn, "middle"))
    ax, ay = 350.0, 82.0                       # frame of the D4 solution
    o.append(H.arrow(s, p, ax, ay, ax + 40, ay, "dim"))
    o.append(H.arrow(s, p, ax, ay, ax, ay - 40, "dim"))
    o.append(H.label(s, ax + 44, ay + 5, it("x"), "label2", I["secondary"]))
    o.append(H.label(s, ax - 6, ay - 32, it("y"), "label2", I["secondary"], "end"))
    o.append(H.label(s, ax - 20, ay + 20, "x distal, y up", "label2", I["muted"]))
    o.append(H.label(s, 432, 24, f"drawn with φ = {PHI:.0f}°", "label2", I["muted"], "end"))
    o.append(nih_credit(s, VB, 74))
    aria = ("Problem D4 setup: free body of the horizontal forearm. The flexor inserts at distance r m from the elbow and "
            "pulls along a line at angle phi to the forearm, upward and back toward the upper arm (force F m). The load "
            "W L hangs at r L. The joint reaction at the elbow is resolved into J x along the bone (drawn pointing "
            "distally, toward the hand) and J y across it (drawn downward). Axes: x distal, y up.")
    return finish(VB, aria, s, o)


FIGS = {
    1: ("A force F applied at point P; the moment arm d is the perpen", fig1),
    2: ("Free-body diagram of the horizontal forearm: elbow pivot at ", fig2),
    3: ("Animation: the forearm rotates from horizontal all the way t", fig3),
    4: ("Lever view: muscle inserts a short distance d_m from the joi", fig4),
    11: ("Two elbow poses holding the same load: horizontal vs. 60 deg", fig11),
    13: ("Segment free body: muscle force F m, load W L, and joint rea", fig13),
    14: ("Third-class elbow lever (effort between pivot and load) vs. ", fig14),
    19: ("Geometrically similar adult and half-scale child limb.", fig19),
    20: ("Top view of a door: the same push at the hinge vs. at the ha", fig20),
    21: ("Forearm holding a long-handled tool whose load sits a horizo", fig21),
    22: ("Two-segment upper limb at the shoulder with a hand load.", fig22),
    23: ("Two candidate pivots A (elbow) and B (hand) for the same fre", fig23),
    24: ("Inclined muscle line at angle phi; joint reaction resolved i", fig24),
    28: ("Adult limb and a half-scale similar limb; torque scales as L", fig28),
}
