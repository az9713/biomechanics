"""Module 3 constrained-mechanics figures (group `linkage`).

svg #4 two-link arm + configuration loop (animated), #10 / #11 / #38 / #47 pendulums (#11 animated), #21 / #24 the
§7 lab limb on its rail (#24 animated), #25 ideal hinge vs real knee, #35 two-force bone, #39 elbow free body (D2),
#43 standing four-bar (D6), #46 joint angles (D9), #50 / #52 / #62 / #68 lab variants (K1, K2, K7, K10).

Every pose, force and period is computed here from the module text (module03.html): the §7.4 lab script
(lines 1305-1374), the K10 script (lines 2165-2224), T = mg(3 cos θ − 2 cos θ0) (line 735), the D2 givens (line 1955).
Art: NIH BioArt 208 arm bones and 244 upper-leg bones (public domain), DBCLS lateral knee (CC BY 4.0).
Colours: joint and contact reactions (λ, T, R) = OVERLAY reaction, weights = load, muscle = force,
lengths and angles = geometry.
"""
import functools
import math
import re

import numpy as np

import house as H
from crop_art import absolute
from m00.tissue import femur_d
from m05.body import ARM, Arm, FOREARM_FRAC, H_REF_M, _read, art_image, finish, fit_circle, it, wrap

T, O, I = H.TISSUE, H.OVERLAY, H.INK
BLK, BRN, RED, BLU = O["reaction"], O["load"], O["force"], O["geometry"]


# ================================================================ the §7.4 lab (lines 1305-1374), as a function
LAB = dict(L1=0.30, L2=0.30, m1=2.0, m2=1.5, g=9.81, yh=-0.48, gd=40.0, gp=40.0, dt=5e-5, nstep=40000, xw=0.30)


def lab_start(amp=40.0, wall=False):
    d = LAB
    th = math.radians(-90.0 + amp)
    x1, y1 = d["L1"] * math.cos(th), d["L1"] * math.sin(th)
    if wall:                                             # K2: hand on the wall x = xw, below the elbow
        x2 = d["xw"]
        return np.array([x1, y1, x2, y1 - math.sqrt(d["L2"] ** 2 - (x2 - x1) ** 2)])
    return np.array([x1, y1, x1 + math.sqrt(d["L2"] ** 2 - (d["yh"] - y1) ** 2), d["yh"]])


def lab_solve(q, dq, mL=0.0, wall=False):
    """One KKT solve of eq. (7.6) + Baumgarte, exactly as the lab loop. Returns (ddq, lam, gv)."""
    d = LAB
    M = np.diag([d["m1"], d["m1"], d["m2"], d["m2"]])
    Q = np.array([0, -d["m1"] * d["g"], 0, -(d["m2"] + mL) * d["g"]])
    x1, y1, x2, y2 = q
    dx1, dy1, dx2, dy2 = dq
    J = np.array([[x1, y1, 0., 0.], [-(x2 - x1), -(y2 - y1), x2 - x1, y2 - y1],
                  [0., 0., 1., 0.] if wall else [0., 0., 0., 1.]])
    dJ = np.array([[dx1, dy1, 0., 0.], [-(dx2 - dx1), -(dy2 - dy1), dx2 - dx1, dy2 - dy1], [0., 0., 0., 0.]])
    gv = np.array([0.5 * (x1 * x1 + y1 * y1 - d["L1"] ** 2), 0.5 * ((x2 - x1) ** 2 + (y2 - y1) ** 2 - d["L2"] ** 2),
                   x2 - d["xw"] if wall else y2 - d["yh"]])
    A = np.block([[M, J.T], [J, np.zeros((3, 3))]])
    rhs = np.concatenate([Q, -(dJ @ dq) - 2 * d["gd"] * (J @ dq) - d["gp"] ** 2 * gv])
    sol = np.linalg.solve(A, rhs)
    return sol[:4], -sol[4:], gv


@functools.lru_cache(maxsize=None)
def lab_run():
    """The default lab run (amp 40°, rail). Returns arrays t, q (n x 4), lam (n x 3), Rs, Re, Nc, gerr."""
    d = LAB
    q, dq = lab_start(), np.zeros(4)
    t, qs, lams, gerr = [], [], [], []
    for step in range(d["nstep"]):
        ddq, lam, gv = lab_solve(q, dq)
        t.append(step * d["dt"])
        qs.append(q.copy())
        lams.append(lam)
        gerr.append(np.abs(gv).max())
        dq = dq + d["dt"] * ddq
        q = q + d["dt"] * dq                       # semi-implicit Euler
    lam = np.array(lams)
    return dict(t=np.array(t), q=np.array(qs), lam=lam, Rs=np.abs(lam[:, 0]) * d["L1"],
                Re=np.abs(lam[:, 1]) * d["L2"], Nc=lam[:, 2], gerr=np.array(gerr))


def turning_index(h):
    """K7: the first MINIMUM of x2 (hand velocity flips negative -> positive), lines 2111-2117."""
    v = np.diff(h["q"][:, 2])
    return int(np.flatnonzero((v[:-1] < 0) & (v[1:] >= 0))[0] + 1)


def joint_forces(q, lam):
    """Forces drawn at the joints (N, lab frame, y up): bone 1 on the shoulder pin, bone 2 on the elbow,
    the third constraint on the hand. J_c^T lam gives the force on each mass; a massless bone passes it on."""
    x1, y1, x2, y2 = q
    f_sh = (-lam[0] * x1, -lam[0] * y1)                   # = minus (bone 1 on m1) = lam1 * grad g1, reversed
    f_el = (-lam[1] * (x2 - x1), -lam[1] * (y2 - y1))     # bone 2 on m1 = lam2 * d g2 / d p1
    return f_sh, f_el, lam[2]


# ================================================================ the K10 three-link script (lines 2165-2224), release solve
K10 = dict(L=(0.30, 0.30, 0.25), m=(2.0, 1.5, 1.0), g=9.81, yh=-0.68)


def k10_release():
    L1, L2, L3 = K10["L"]
    m1, m2, m3 = K10["m"]
    g, yh = K10["g"], K10["yh"]
    th = math.radians(-90.0 + 40.0)
    x1, y1 = L1 * math.cos(th), L1 * math.sin(th)
    x2, y2 = x1, y1 - L2
    x3 = x2 + math.sqrt(L3 * L3 - (yh - y2) ** 2)
    q = np.array([x1, y1, x2, y2, x3, yh])
    M = np.diag([m1, m1, m2, m2, m3, m3])
    Q = np.array([0, -m1 * g, 0, -m2 * g, 0, -m3 * g], float)
    J = np.array([[x1, y1, 0, 0, 0, 0], [-(x2 - x1), -(y2 - y1), x2 - x1, y2 - y1, 0, 0],
                  [0, 0, -(x3 - x2), -(yh - y2), x3 - x2, yh - y2], [0, 0, 0, 0, 0, 1.]], float)
    A = np.block([[M, J.T], [J, np.zeros((4, 4))]])
    lam = -np.linalg.solve(A, np.concatenate([Q, np.zeros(4)]))[6:]     # at rest: dq = 0, g(q) = 0
    R = (abs(lam[0]) * L1, abs(lam[1]) * L2, abs(lam[2]) * L3, lam[3])
    return q, lam, R


# ================================================================ drawing helpers
def mark(s, x, y, col=I["primary"], r=3.0):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{col}" stroke="#fff" stroke-width="{s(1.2):.2f}"/>'


def hatch(s, x0, x1, y, side=1, step=12.0, ink=I["secondary"]):
    """A fixed support: a solid line with short ticks on the side away from the body (side=1: below)."""
    o = [H.line(s, x0, y, x1, y, I["primary"], "axis")]
    n = int((x1 - x0) / step)
    for i in range(n + 1):
        x = x0 + i * step
        o.append(H.line(s, x, y, x - 7, y + side * 8, ink, "leader"))
    return "".join(o)


def vhatch(s, x, y0, y1, side=1, step=12.0):
    """A vertical wall: solid line, ticks on side (1 = right)."""
    o = [H.line(s, x, y0, x, y1, I["primary"], "axis")]
    for i in range(int((y1 - y0) / step) + 1):
        y = y0 + i * step
        o.append(H.line(s, x, y, x + side * 8, y - 7, I["secondary"], "leader"))
    return "".join(o)


def arc(s, p, cx, cy, r, a0, a1, col, meaning=None, w="geom"):
    """Circular arc on screen (angles in degrees, counter-clockwise positive, y up), head at a1 if meaning."""
    P = [(cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a))) for a in (a0, a1)]
    large = 1 if abs(a1 - a0) > 180 else 0
    sweep = 0 if a1 > a0 else 1
    mk = f' marker-end="url(#{p}a_{meaning})"' if meaning else ""
    return (f'<path d="M{P[0][0]:.2f},{P[0][1]:.2f} A{r:.2f},{r:.2f} 0 {large} {sweep} {P[1][0]:.2f},{P[1][1]:.2f}" '
            f'fill="none" stroke="{col}" stroke-width="{s(H.PX[w]):.2f}"{mk}/>')


def mark_defs(p, s):
    """Joint centre and point-mass marks at the origin, for <use> in animation frames."""
    return f'<g id="{p}jc">{H.joint_centre(s, 0, 0)}</g><g id="{p}cm">{H.com_mark(s, 0, 0)}</g>'


def use(p, name, P_):
    return f'<use href="#{p}{name}" x="{P_[0]:.1f}" y="{P_[1]:.1f}"/>'


NIH_ARM_CREDIT = H.ATTRIBUTION["pd"].format(
    author="NIH NIAID BioArt 208", title="Human Arm Bones",
    changes="Recoloured; humerus and forearm (no hand) reposed and stretched along their axes to the link lengths.")


# ================================================================ the limb: NIH arm bones posed as the lab's links
class Limb:
    """NIH arm bones (BioArt 208) posed as a two-link limb. Humerus: its cut top (the shoulder pin; the art has
    no humeral head) to the elbow axis ARM["E"]; forearm: the elbow axis to the wrist, which is the lab's hand
    point (the hand bones are not drawn, so nothing crosses the rail). Each bone is stretched along its axis to
    its link length; across the axis every bone keeps the art's own scale at `cm` canvas units per cm.
    The bones go once into <defs> and each pose is two <use>, so an animation costs a few bytes per frame."""

    def __init__(self, p, s, cm):
        self.p = p
        src = H.recolour(_read("nih_arm_bones.svg"), "nih")
        paths = re.findall(r'<path\b[^>]*?\bd="([^"]+)"[^>]*/>', src)
        assert len(paths) == 24, len(paths)
        k_art = math.dist(ARM["E"], ARM["wrist"]) / (FOREARM_FRAC * H_REF_M * 100)    # art units per cm
        self.sw = cm / k_art
        st = (f'fill="{T["bone"][0]}" stroke="{T["bone"][1]}" stroke-width="{s(H.PX["art_line"]) / self.sw:.3f}" '
              f'stroke-linejoin="round"')
        self.defs = (f'<g id="{p}hum"><path d="{absolute(paths[3])}" {st}/></g>'
                     f'<g id="{p}fore">' + "".join(f'<path d="{absolute(paths[i])}" {st}/>' for i in (5, 4)) + '</g>')

    def bone(self, name, A0, A1, P0, P1):
        a = math.degrees(math.atan2(A1[1] - A0[1], A1[0] - A0[0]))
        f = math.degrees(math.atan2(P1[1] - P0[1], P1[0] - P0[0]))
        sx = math.dist(P0, P1) / math.dist(A0, A1)
        return (f'<use href="#{self.p}{name}" transform="translate({P0[0]:.2f} {P0[1]:.2f}) rotate({f:.2f}) '
                f'scale({sx:.4f} {self.sw:.4f}) rotate({-a:.2f}) translate({-A0[0]} {-A0[1]})"/>')

    def pose(self, S, E, W):
        return self.bone("fore", ARM["E"], ARM["wrist"], E, W) + self.bone("hum", ARM["hum_top"], ARM["E"], S, E)


class Frame:
    """Lab metres (y up) -> canvas: origin at the shoulder pin (ox, oy), K canvas units per metre."""

    def __init__(self, ox, oy, K):
        self.ox, self.oy, self.K = ox, oy, K

    def __call__(self, x, y):
        return (self.ox + self.K * x, self.oy - self.K * y)


def limb_scene(s, p, F, limb, q, rail=True, wall=False, sup=(60, 60), rail_x=(-0.12, 0.48)):
    """Supports, bones, joint and mass marks for one lab pose q = (x1, y1, x2, y2). Returns (svg, S, E, W)."""
    S, E, W = F(0, 0), F(q[0], q[1]), F(q[2], q[3])
    o = [hatch(s, S[0] - sup[0], S[0] + sup[1], S[1] - s(4), side=-1)]
    if rail:
        o.append(hatch(s, F(rail_x[0], 0)[0], F(rail_x[1], 0)[0], F(0, LAB["yh"])[1] + s(4)))
    if wall:
        o.append(vhatch(s, F(LAB["xw"], 0)[0] + s(4), F(0, -0.30)[1], F(0, -0.66)[1]))
    o.append(limb.pose(S, E, W))
    o.append(H.joint_centre(s, *S))
    o.append(H.com_mark(s, *E))
    o.append(H.com_mark(s, *W))
    return "".join(o), S, E, W


# ================================================================ svg #21  the constrained two-link limb (§7.1)
def unit(v):
    n = math.hypot(*v)
    return (v[0] / n, v[1] / n)


def side_label(s, A_, B_, text, off, col=BLU, size="label"):
    """Label at the middle of segment A-B, offset `off` units along its left normal (screen)."""
    ux, uy = unit((B_[0] - A_[0], B_[1] - A_[1]))
    nx, ny = uy, -ux
    x, y = (A_[0] + B_[0]) / 2 + nx * off, (A_[1] + B_[1]) / 2 + ny * off
    return H.label(s, x, y + s(5), text, size, col, "middle")


def fig21():
    p = "m3f21_"
    VB = (0, 0, 600, 384)
    s = H.Scale(VB[2], VB[3])
    K = 520.0                                   # canvas units per metre
    F = Frame(232, 50, K)
    limb = Limb(p, s, K / 100)
    q = lab_start()
    _, lam, _ = lab_solve(q, np.zeros(4))
    f_sh, f_el, nc = joint_forces(q, lam)
    A = 56.0                                    # every arrow: direction at release, one length (not to force scale)
    o = [f'<defs>{H.markers(p, s)}{limb.defs}</defs>']
    sc, S, E, W = limb_scene(s, p, F, limb, q)
    o.append(sc)
    r = s(8)
    # weights: m1 g down from the elbow; m2 g ends on the hand from above (the rail is below it)
    o.append(H.arrow(s, p, E[0] - 4, E[1] + r, E[0] - 4, E[1] + r + A, "load"))
    o.append(H.label(s, E[0] - 12, E[1] + r + A - 4, f'{it("m")}{H.sub("1", s)}{it("g")}', fill=BRN, anchor="end"))
    o.append(H.arrow(s, p, W[0] + 36, W[1] - r - A, W[0] + 36, W[1] - r, "load"))
    o.append(H.label(s, W[0] + 44, W[1] - r - 10, f'{it("m")}{H.sub("2", s)}{it("g")}', fill=BRN))
    # the three multipliers, each along its own constraint gradient, with its sign at release
    for P_, f, sub, sd in ((S, f_sh, "1", 1), (E, f_el, "2", -1)):
        ux, uy = unit(f)                                       # screen direction (ux, -uy); drawn beside the bone
        nx, ny = -uy * sd, -ux * sd
        b0 = (P_[0] + nx * 20 + ux * r, P_[1] + ny * 20 - uy * r)
        o.append(H.arrow(s, p, b0[0], b0[1], b0[0] + ux * A, b0[1] - uy * A, "reaction"))
        o.append(H.label(s, b0[0] + ux * A * 0.5 + nx * 16, b0[1] - uy * A * 0.5 + ny * 16 + 5, f'λ{H.sub(sub, s)}',
                         fill=BLK, anchor="middle"))
    o.append(H.arrow(s, p, W[0] + 12, W[1] - r, W[0] + 12, W[1] - r - A, "reaction"))
    o.append(H.label(s, W[0] + 20, W[1] - r - A - 8, f'λ{H.sub("3", s)} (rail)', fill=BLK))
    # names
    o.append(H.label(s, S[0] - 46, S[1] - 18, "shoulder pin (0, 0)", "label2", I["primary"], "end"))
    o.append(H.label(s, E[0] + 22, E[1] + 5, f'elbow: {it("m")}{H.sub("1", s, "label2")} at ({it("x")}{H.sub("1", s, "label2")}, '
                     f'{it("y")}{H.sub("1", s, "label2")})', "label2"))
    o.append(H.label(s, W[0] + 20, W[1] + 34, f'hand: {it("m")}{H.sub("2", s, "label2")} at ({it("x")}{H.sub("2", s, "label2")}, '
                     f'{it("y")}{H.sub("2", s, "label2")})', "label2"))
    o.append(side_label(s, S, E, f'{it("L")}{H.sub("1", s)}', -26))
    o.append(side_label(s, E, W, f'{it("L")}{H.sub("2", s)}', -26))
    d = LAB
    yr = F(0, d["yh"])[1]
    o.append(H.label(s, F(-0.12, 0)[0], yr - 9, f'frictionless rail {it("y")} = {it("y")}{H.sub("h", s, "label2")}', "label2", I["secondary"]))
    o.append(H.label(s, VB[2] - 8, 22, "pose and arrow senses at release (40°);", "label2", I["muted"], "end"))
    o.append(H.label(s, VB[2] - 8, 22 + s(16), "arrows not to force scale", "label2", I["muted"], "end"))
    lines = wrap(NIH_ARM_CREDIT, 104)
    o.append(H.credit(s, 8, VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines))
    aria = ("A two-link limb drawn with NIH arm bones: the humerus hangs from a shoulder pin on a hatched support at "
            "the origin, the forearm runs from the elbow, where the point mass m1 sits, to the hand point, where m2 "
            "sits on a hatched frictionless rail at height y h. Bone lengths L1 and L2. Both masses carry a weight "
            "arrow. The three constraint forces, with their senses at the release pose: lambda 1 along the upper arm at "
            "the shoulder, lambda 2 along the forearm at the elbow, lambda 3 vertically up from the rail at the hand.")
    return finish(VB, aria, s, o)


# ================================================================ svg #4  one pose = one point (§1), animated
def arm_angles(k, n=24):
    """The old figure's keyframes, written as the circle they are: theta1 (upper arm from the horizontal) and
    theta2 (elbow, relative to the upper arm), degrees, counter-clockwise positive."""
    a = 2 * math.pi * k / n
    return -20.0 + 35.0 * math.sin(a), 55.0 + 35.0 * math.cos(a)


def fig4():
    p = "m3f4_"
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    n, L1, L2, K = 24, 0.30, 0.30, 400.0
    F = Frame(70, 196, K)
    limb = Limb(p, s, K / 100)
    S = F(0, 0)
    red = H.SERIES[0]
    pd = mark_defs(p, s)

    def pose(t1, t2):
        a1, a2 = math.radians(t1), math.radians(t1 + t2)
        e = (L1 * math.cos(a1), L1 * math.sin(a1))
        return e, (e[0] + L2 * math.cos(a2), e[1] + L2 * math.sin(a2))
    # configuration plane
    x0, x1, y0, y1 = 470.0, 710.0, 318.0, 48.0           # plot box: theta1 -60..20, theta2 10..100
    X = lambda v: x0 + (v + 60) / 80 * (x1 - x0)         # noqa: E731
    Y = lambda v: y0 - (v - 10) / 90 * (y0 - y1)         # noqa: E731
    o = [f'<defs>{H.markers(p, s)}{limb.defs}{pd}</defs>']
    o.append(H.label(s, 150, 22, "the arm (physical space)", "label", I["primary"], "middle", 'font-weight="bold"'))
    o.append(H.label(s, (x0 + x1) / 2, 22, f"configuration space (θ{H.sub('1', s)}, θ{H.sub('2', s)})", "label",
                     I["primary"], "middle", 'font-weight="bold"'))
    for v in (-40, -20, 0):
        o.append(H.line(s, X(v), y0, X(v), y1, "#e6e6e6", "leader"))
    for v in (40, 70):
        o.append(H.line(s, x0, Y(v), x1, Y(v), "#e6e6e6", "leader"))
    o.append(H.line(s, x0, y0, x1, y0, I["axis"], "axis") + H.line(s, x0, y0, x0, y1, I["axis"], "axis"))
    for v in (-60, -40, -20, 0, 20):
        o.append(H.line(s, X(v), y0, X(v), y0 + 4, I["axis"], "leader"))
        o.append(H.label(s, X(v), y0 + 18, f"{v}°".replace("-", "−"), "tick", I["secondary"], "middle"))
    for v in (10, 40, 70, 100):
        o.append(H.line(s, x0 - 4, Y(v), x0, Y(v), I["axis"], "leader"))
        o.append(H.label(s, x0 - 7, Y(v) + 4.5, f"{v}°", "tick", I["secondary"], "end"))
    o.append(H.label(s, x1 + 6, y0 - 8, f'θ{H.sub("1", s)}', "label", I["primary"]))
    o.append(H.label(s, x0 - 8, y1 - 10, f'θ{H.sub("2", s)}', "label", I["primary"], "end"))
    loop = [arm_angles(i, 96) for i in range(97)]
    o.append(f'<polyline points="{" ".join(f"{X(a):.2f},{Y(b):.2f}" for a, b in loop)}" fill="none" stroke="{red}" '
             f'stroke-width="{s(H.PX["curve_multi"]):.2f}" stroke-dasharray="{s(5):.2f} {s(4):.2f}"/>')
    # the hand's path in physical space, the same motion
    hand = [F(*pose(*arm_angles(i, 96))[1]) for i in range(97)]
    o.append(f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in hand)}" fill="none" stroke="{red}" '
             f'stroke-width="{s(H.PX["curve_multi"]):.2f}" stroke-dasharray="{s(5):.2f} {s(4):.2f}"/>')
    o.append(vhatch(s, S[0] - s(10), S[1] - 26, S[1] + 26, side=-1, step=10))
    o.append(H.label(s, S[0] - 6, S[1] + 52, "shoulder", "label2", I["secondary"], "middle"))
    vals = []
    for k in range(n):
        t1, t2 = arm_angles(k, n)
        e, w = pose(t1, t2)
        E, W = F(*e), F(*w)
        g = [limb.pose(S, E, W)]
        g.append(H.line(s, S[0], S[1], S[0] + 46, S[1], O["dim"], "ref", H.DASH_REF))
        g.append(arc(s, p, S[0], S[1], 34, 0, t1, BLU))
        g.append(H.label(s, S[0] + 46, S[1] + (16 if t1 < 0 else -6), f'θ{H.sub("1", s)}', fill=BLU))
        ex = (E[0] + (E[0] - S[0]) * 0.3, E[1] + (E[1] - S[1]) * 0.3)
        g.append(H.line(s, E[0], E[1], ex[0], ex[1], O["dim"], "ref", H.DASH_REF))
        g.append(arc(s, p, E[0], E[1], 26, t1, t1 + t2, BLU))
        am = math.radians(t1 + t2 / 2)
        g.append(H.label(s, E[0] + 50 * math.cos(am) + 8, E[1] - 50 * math.sin(am) + 5, f'θ{H.sub("2", s)}', fill=BLU, anchor="middle"))
        g.append(use(p, "jc", E))
        g.append(mark(s, *W, red, 5))
        g.append(H.line(s, X(t1), Y(t2), X(t1), y0, O["dim"], "leader", H.DASH_REF))
        g.append(H.line(s, X(t1), Y(t2), x0, Y(t2), O["dim"], "leader", H.DASH_REF))
        g.append(mark(s, X(t1), Y(t2), red, 5))
        o.append(H.frame(k, 0, "".join(g)))
        vals.append(f"θ₁ {t1:.0f}°, θ₂ {t2:.0f}°".replace("-", "−"))
    o.append(H.joint_centre(s, *S))
    hx = max(hand)
    o.append(H.label(s, hx[0] + 10, hx[1] + 5, "hand path", "label2", I["primary"]))
    lines = wrap(NIH_ARM_CREDIT, 120)
    o.append(H.credit(s, 8, VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines))
    hv = []
    for i in range(71):
        t1 = -55.0 + i * 1.0
        c = math.sqrt(max(0.0, 1 - ((t1 + 20) / 35) ** 2))
        hv.append([X(t1), [Y(55 + 35 * c), Y(55 - 35 * c)], f"θ₁ = {t1:.1f}°: θ₂ = {55 + 35 * c:.1f}° or {55 - 35 * c:.1f}°".replace("-", "−")])
    aria = ("Animation, slider and Play button. Left: a two-link arm drawn with NIH arm bones, the shoulder fixed, moving "
            "through a cycle of poses; theta 1 is the upper-arm angle from the horizontal and theta 2 the elbow angle "
            "relative to the upper arm, both marked. The red hand traces a dashed closed path. Right: the configuration "
            "plane, theta 1 from minus 60 to 20 degrees against theta 2 from 10 to 100 degrees; the red point at (theta 1, "
            "theta 2) moves in step with the arm round a dashed circle, theta 1 = minus 20 + 35 sin, theta 2 = 55 + 35 cos.")
    return finish(VB, aria, s, o, H.frames_attr("pose", vals, 0) + " " + H.hover_attr([x0, y1, x1, y0], hv))


# ================================================================ svg #24  the lab swing, animated (§7.5)
def fig24():
    p = "m3f24_"
    h = lab_run()
    i_turn = turning_index(h)
    per = 2 * h["t"][i_turn]                    # K7: 2 x 0.756 s = one full swing, back to the release pose
    n = 24
    K, kN = 430.0, 3.0                          # canvas units per metre, per newton
    d = LAB
    ks = [min(len(h["t"]) - 1, round(k * per / n / d["dt"])) for k in range(n)]
    F0 = Frame(0, 0, K)
    pts = [(0, 0)]
    for k in ks:
        q = h["q"][k]
        f_sh, f_el, _ = joint_forces(q, h["lam"][k])
        E = F0(q[0], q[1])
        pts += [E, F0(q[2], q[3]), (f_sh[0] * kN, -f_sh[1] * kN), (E[0] + f_el[0] * kN, E[1] - f_el[1] * kN)]
    xs, ys = [v[0] for v in pts], [v[1] for v in pts]
    ox, oy = 150 - min(xs), 62
    W0, H0 = math.ceil(max(xs) - min(xs) + 290), math.ceil(max(ys) - min(ys) + 132)
    s = H.Scale(W0, H0)
    lines = wrap(NIH_ARM_CREDIT, 120)            # art credit below the force scale bar
    VB = (0, 0, W0, H0 + math.ceil(len(lines) * s(H.PX["credit"]) * 1.25 + s(8)))
    s = H.Scale(VB[2], VB[3])
    F = Frame(ox, oy, K)
    limb = Limb(p, s, K / 100)
    o = [f'<defs>{H.markers(p, s)}{limb.defs}{mark_defs(p, s)}</defs>']
    S = F(0, 0)
    o.append(hatch(s, S[0] - 50, S[0] + 50, S[1] - s(4), side=-1))
    yr = F(0, d["yh"])[1]
    x2 = h["q"][:, 2]
    o.append(hatch(s, F(x2.min() - 0.08, 0)[0], F(x2.max() + 0.08, 0)[0], yr + s(4)))
    for xv in (x2.min(), x2.max()):
        X = F(xv, 0)[0]
        o.append(H.line(s, X, yr + s(14), X, yr + s(24), O["dim"], "ref"))
    o.append(H.label(s, F(x2.min(), 0)[0] - 6, yr + s(26), f'turning points {it("x")}{H.sub("2", s, "label2")} = '
                     f'{x2.min():.3f} m'.replace("-", "−"), "label2", I["secondary"], "end"))
    o.append(H.label(s, F(x2.max(), 0)[0] + 6, yr + s(26), f'{x2.max():.3f} m', "label2", I["secondary"]))
    vals = []
    for j, k in enumerate(ks):
        q, lam = h["q"][k], h["lam"][k]
        f_sh, f_el, _ = joint_forces(q, lam)
        E, W = F(q[0], q[1]), F(q[2], q[3])
        g = [limb.pose(S, E, W), use(p, "cm", E), use(p, "cm", W)]
        for P_, f, name in ((S, f_sh, "s"), (E, f_el, "e")):
            L_ = math.hypot(*f) * kN
            if L_ > s(8):
                g.append(H.arrow(s, p, P_[0], P_[1], P_[0] + f[0] * kN, P_[1] - f[1] * kN, "reaction"))
            ux, uy = unit(f)
            g.append(H.label(s, P_[0] + f[0] * kN + ux * 12 + 14, P_[1] - f[1] * kN - uy * 12 + 6, f'{it("R")}{H.sub(name, s)}', fill=BLK))
        for jj, txt in enumerate((f'{it("t")} = {h["t"][k]:.2f} s', f'{it("R")}{H.sub("s", s)} = {h["Rs"][k]:.1f} N',
                                  f'{it("R")}{H.sub("e", s)} = {h["Re"][k]:.1f} N')):
            g.append(H.label(s, VB[2] - 12, 30 + jj * s(20), txt, "label", anchor="end"))
        o.append(H.frame(j, 0, "".join(g)))
        vals.append(f'{h["t"][k]:.2f} s')
    o.append(H.joint_centre(s, *S))
    # force scale bar
    by = H0 - 16
    o.append(H.line(s, 12, by - 5, 12 + 10 * kN, by - 5, BLK, "force"))
    o.append(H.label(s, 18 + 10 * kN, by, f'10 N: black arrows = joint reactions to this scale (peak {it("R")}{H.sub("s", s, "label2")} '
                     f'{h["Rs"].max():.1f} N)', "label2", I["secondary"]))
    o.append(H.credit(s, 8, VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines))
    k_pk = int(np.argmax(h["Rs"][:i_turn]))
    aria = ("Animation, slider and Play button: the lab's two-link limb (NIH arm bones) swings once in "
            f"{per:.2f} s, its hand sliding along the rail between turning points at x2 = {x2.max():.3f} and minus "
            f"{-x2.min():.3f} m. Black arrows at the shoulder and the elbow are the joint reactions R s and R e, drawn to "
            f"one force scale, with their values in newtons. R s is {h['Rs'][0]:.1f} N at release (the still frame), "
            f"peaks at {h['Rs'][k_pk]:.1f} N {h['t'][k_pk]:.2f} s later with the hand at x2 = {h['q'][k_pk, 2]:.3f} m, and "
            f"falls to {h['Rs'][i_turn]:.1f} N at the inner turning point.")
    return finish(VB, aria, s, o, H.frames_attr("t", vals, 0))


# ================================================================ pendulums (schematic): #10, #11, #38, #47
def ceiling(s, x, y, half=34):
    return hatch(s, x - half, x + half, y - s(3), side=-1, step=10)


def bob(s, x, y, r):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{I["secondary"]}" stroke="#fff" stroke-width="{s(1.2):.2f}"/>'


def rod(s, P, B):
    return H.line(s, P[0], P[1], B[0], B[1], I["secondary"], "axis")


def swing_point(P, L, th):
    """Bob position for angle th (rad) from the downward vertical, positive to the right."""
    return (P[0] + L * math.sin(th), P[1] + L * math.cos(th))


def fig10():
    p = "m3f10_"
    VB = (0, 0, 520, 300)
    s = H.Scale(VB[2], VB[3])
    P, L, th = (230.0, 50.0), 200.0, math.radians(38.0)
    B = swing_point(P, L, th)
    ux, uy = math.sin(th), math.cos(th)                   # unit vector pivot -> bob (outward = +grad g)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(f'<path d="M{P[0] - L * math.sin(math.radians(62)):.2f},{P[1] + L * math.cos(math.radians(62)):.2f} '
             f'A{L},{L} 0 0 0 {P[0] + L * math.sin(math.radians(62)):.2f},{P[1] + L * math.cos(math.radians(62)):.2f}" '
             f'fill="none" stroke="{O["dim"]}" stroke-width="{s(H.PX["ref"]):.2f}" '
             f'stroke-dasharray="{s(H.DASH_REF[0]):.2f} {s(H.DASH_REF[1]):.2f}"/>')
    o.append(ceiling(s, *P))
    o.append(H.line(s, P[0], P[1], P[0], P[1] + L + 26, O["dim"], "ref", H.DASH_REF))
    # axes at the pivot: x right, y DOWN (line 676)
    o.append(H.arrow(s, p, P[0], P[1] + 1, P[0] + 70, P[1] + 1, "dim"))
    o.append(H.label(s, P[0] + 76, P[1] + 6, it("x"), "label2", I["secondary"]))
    o.append(H.arrow(s, p, P[0] - 40, P[1] + 4, P[0] - 40, P[1] + 50, "dim"))
    o.append(H.label(s, P[0] - 46, P[1] + 48, f'{it("y")} (down)', "label2", I["secondary"], "end"))
    o.append(rod(s, P, B))
    o.append(arc(s, p, P[0], P[1], 62, -90, -90 + 38, BLU))
    o.append(H.label(s, P[0] + 14, P[1] + 84, it("θ"), fill=BLU, anchor="middle"))
    o.append(H.label(s, (P[0] + B[0]) / 2 - 12, (P[1] + B[1]) / 2 + 2, it("L"), fill=BLU, anchor="end"))
    # forces on the bob: tension up the rod, gravity down; the gradient direction outward (dashed reference)
    o.append(H.line(s, B[0], B[1], B[0] + ux * 82, B[1] + uy * 82, O["dim"], "ref", H.DASH_REF,
                    extra=f'marker-end="url(#{p}a_dim)"'))
    o.append(H.label(s, B[0] + ux * 88 + 6, B[1] + uy * 88 + 8, f'∇{it("g")} = ({it("x")}, {it("y")})', "label2", I["secondary"]))
    o.append(H.arrow(s, p, B[0] - ux * s(9), B[1] - uy * s(9), B[0] - ux * 92, B[1] - uy * 92, "reaction"))
    o.append(H.label(s, B[0] - ux * 70 + 16, B[1] - uy * 70 + 4, it("T"), fill=BLK))
    o.append(H.arrow(s, p, B[0], B[1] + s(9), B[0], B[1] + 78, "load"))
    o.append(H.label(s, B[0] - 10, B[1] + 70, f'{it("m")}{it("g")}', fill=BRN, anchor="end"))
    o.append(bob(s, *B, s(9)))
    o.append(H.joint_centre(s, *P))
    o.append(H.label(s, P[0] - 40, P[1] - 18, "pivot (0, 0)", "label2", I["secondary"], "end"))
    o.append(H.label(s, P[0] + L * 0.88 + 8, P[1] + L * 0.47 - 14, "constraint circle", "label2", I["secondary"]))
    o.append(H.label(s, P[0] + L * 0.88 + 8, P[1] + L * 0.47 + 2, f'{it("g")}({it("x")}, {it("y")}) = 0', "label2", I["secondary"]))
    aria = ("A pendulum: a pivot on a hatched support at the origin, a rigid rod of length L to a bob at angle theta = 38 "
            "degrees from the downward vertical, on the dashed constraint circle g(x, y) = 0. Axes x and y, with y "
            "pointing down. On the bob: the weight m g points down, the rod tension T points up the rod to the pivot, "
            "and the dashed constraint gradient, grad g = (x, y), points radially outward along the same line.")
    return finish(VB, aria, s, o)


def pendulum_frames(th0_deg=60.0, n=36):
    """theta'' = -(g/L) sin theta (line 780), released from rest at +th0, in units where g/L = 1 (RK4).
    Returns ([(time / period, theta), ...] for n equal time steps over one period, period)."""
    f = lambda y: (y[1], -math.sin(y[0]))     # noqa: E731
    y, t, h, ts, ys = (math.radians(th0_deg), 0.0), 0.0, 1e-3, [0.0], [math.radians(th0_deg)]
    while True:
        k1 = f(y)
        k2 = f((y[0] + h / 2 * k1[0], y[1] + h / 2 * k1[1]))
        k3 = f((y[0] + h / 2 * k2[0], y[1] + h / 2 * k2[1]))
        k4 = f((y[0] + h * k3[0], y[1] + h * k3[1]))
        yn = (y[0] + h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]), y[1] + h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]))
        if yn[1] >= 0:                            # the velocity turns: far turning point = half a period
            break
        y, t = yn, t + h
        ts.append(t)
        ys.append(y[0])
    half = t + h * (-y[1]) / (yn[1] - y[1])
    ts.append(half)
    ys.append(-math.radians(th0_deg))

    def theta(tt):                                # linear interpolation on the half swing
        i = max(1, min(len(ts) - 1, next((j for j, v in enumerate(ts) if v >= tt), len(ts) - 1)))
        w = (tt - ts[i - 1]) / (ts[i] - ts[i - 1])
        return ys[i - 1] + w * (ys[i] - ys[i - 1])
    P = 2 * half
    return [(k / n, theta(k * P / n if k * P / n <= half else P - k * P / n)) for k in range(n)], P


def fig11():
    p = "m3f11_"
    VB = (0, 0, 620, 340)
    s = H.Scale(VB[2], VB[3])
    P, L, th0 = (310.0, 58.0), 190.0, 60.0
    A = 46.0                                            # length of m g (canvas units)
    frames, _ = pendulum_frames(th0, 24)
    n = len(frames)
    dflt = n // 4                                       # quarter period: the bottom, T = 2 mg
    o = [f'<defs>{H.markers(p, s)}</defs>']
    a0 = math.radians(th0)
    E0, E1 = swing_point(P, L, -a0), swing_point(P, L, a0)
    o.append(f'<path d="M{E0[0]:.2f},{E0[1]:.2f} A{L},{L} 0 0 0 {E1[0]:.2f},{E1[1]:.2f}" fill="none" stroke="{O["dim"]}" '
             f'stroke-width="{s(H.PX["ref"]):.2f}" stroke-dasharray="{s(H.DASH_REF[0]):.2f} {s(H.DASH_REF[1]):.2f}"/>')
    o.append(ceiling(s, *P))
    o.append(H.line(s, P[0], P[1], P[0], P[1] + L + 18, O["dim"], "ref", H.DASH_REF))
    t_of = lambda th: 3 * math.cos(th) - 2 * math.cos(a0)    # noqa: E731  T / mg, line 735
    o.append(H.label(s, E0[0] - 14, E0[1] + 4, f'θ = −60°: {it("T")} = {t_of(a0):.1f} {it("m")}{it("g")}', "label2", I["secondary"], "end"))
    o.append(H.label(s, E1[0] + 14, E1[1] + 4, f'θ₀ = 60°: {it("T")} = {t_of(a0):.1f} {it("m")}{it("g")}', "label2", I["secondary"]))
    o.append(H.label(s, P[0] + 24, P[1] + L + 30, f'bottom: {it("T")} = {t_of(0):.0f} {it("m")}{it("g")}', "label2", I["secondary"]))
    vals = []
    for k, (ph, th) in enumerate(frames):
        B = swing_point(P, L, th)
        ux, uy = math.sin(th), math.cos(th)
        Tm = t_of(th)
        g = [rod(s, P, B)]
        g.append(H.arrow(s, p, B[0] - ux * s(9), B[1] - uy * s(9), B[0] - ux * (s(9) + A * Tm), B[1] - uy * (s(9) + A * Tm), "reaction"))
        g.append(H.arrow(s, p, B[0], B[1] + s(9), B[0], B[1] + s(9) + A, "load"))
        g.append(bob(s, *B, s(9)))
        deg = round(math.degrees(th)) or 0
        g.append(H.label(s, 14, 26, f'θ = {deg}°'.replace("-", "−"), "label"))
        g.append(H.label(s, 14, 26 + s(20), f'{it("T")} = {Tm:.2f} {it("m")}{it("g")}', "label"))
        o.append(H.frame(k, dflt, "".join(g)))
        vals.append(f"{ph:.2f}")
    o.append(H.joint_centre(s, *P))
    # legend
    ly = VB[3] - 16
    o.append(H.arrow(s, p, 16, ly - 5, 44, ly - 5, "reaction"))
    o.append(H.label(s, 50, ly, f'rod tension {it("T")} = |λ|{it("L")} (length ∝ {it("T")})', "label2"))
    o.append(H.arrow(s, p, 360, ly - 5, 388, ly - 5, "load"))
    o.append(H.label(s, 394, ly, f'weight {it("m")}{it("g")} (constant)', "label2"))
    aria = ("Animation, slider and Play button: a pendulum released from rest at 60 degrees swings through one period on "
            "a dashed arc below its pivot. A black tension arrow up the rod has length proportional to T = m g (3 cos "
            "theta minus 2 cos 60 degrees): 0.5 m g at the two turning points and 2 m g at the bottom. A brown weight "
            "arrow m g stays the same length. The still frame shows the bottom of the swing.")
    return finish(VB, aria, s, o, H.frames_attr("time / period", vals, dflt))


def fig38():
    p = "m3f38_"
    VB = (0, 0, 400, 320)
    s = H.Scale(VB[2], VB[3], display_w=400)
    P, L = (200.0, 50.0), 170.0
    B = (P[0], P[1] + L)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    o.append(f'<path d="M{P[0] - L:.2f},{P[1]:.2f} A{L},{L} 0 0 0 {P[0] + L:.2f},{P[1]:.2f}" fill="none" stroke="{O["dim"]}" '
             f'stroke-width="{s(H.PX["ref"]):.2f}" stroke-dasharray="{s(H.DASH_REF[0]):.2f} {s(H.DASH_REF[1]):.2f}"/>')
    o.append(ceiling(s, *P))
    # axes: x right, y UP (D1 statement)
    o.append(H.arrow(s, p, P[0], P[1], P[0] + 70, P[1], "dim"))
    o.append(H.label(s, P[0] + 76, P[1] + 5, it("x"), "label2", I["secondary"]))
    o.append(H.arrow(s, p, P[0] - 50, P[1] + 44, P[0] - 50, P[1] + 4, "dim"))
    o.append(H.label(s, P[0] - 56, P[1] + 16, f'{it("y")} (up)', "label2", I["secondary"], "end"))
    o.append(rod(s, P, B))
    A = 66.0
    o.append(H.arrow(s, p, B[0] + 16, B[1] - s(4), B[0] + 16, B[1] - s(4) - A, "reaction"))
    o.append(H.label(s, B[0] + 24, B[1] - A + 4, f'{it("T")} = |λ|{it("L")}', fill=BLK))
    o.append(H.arrow(s, p, B[0], B[1] + s(9), B[0], B[1] + s(9) + A, "load"))
    o.append(H.label(s, B[0] + 8, B[1] + A, f'{it("m")}{it("g")}', fill=BRN))
    o.append(bob(s, *B, s(9)))
    o.append(H.joint_centre(s, *P))
    o.append(H.label(s, P[0] - 26, P[1] + L / 2, it("L"), fill=BLU, anchor="end"))
    o.append(H.label(s, B[0] - 16, B[1] + 6, f'({it("x")}, {it("y")}) = (0, −{it("L")})', "label2", I["primary"], "end"))
    o.append(H.label(s, P[0] + L * 0.72 + 8, P[1] + L * 0.72 + 14, f'{it("g")}({it("q")}) = 0', "label2", I["secondary"]))
    aria = ("Problem D1 setup: a pendulum hanging straight down at rest. Pivot at the origin on a hatched support, axes x "
            "to the right and y up, a rigid rod of length L to a bob at (x, y) = (0, minus L) on the dashed constraint "
            "circle g(q) = 0. On the bob: the rod tension T = |lambda| L points up the rod and the weight m g points "
            "down, drawn the same length.")
    return finish(VB, aria, s, o)


def fig47():
    p = "m3f47_"
    VB = (0, 0, 400, 330)
    s = H.Scale(VB[2], VB[3], display_w=400)
    P, L = (120.0, 46.0), 200.0
    th0, th = math.radians(60.0), math.radians(25.0)
    B0, B = swing_point(P, L, th0), swing_point(P, L, th)
    ux, uy = math.sin(th), math.cos(th)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    lo = swing_point(P, L, -math.radians(20))
    o.append(f'<path d="M{lo[0]:.2f},{lo[1]:.2f} A{L},{L} 0 0 0 {B0[0]:.2f},{B0[1]:.2f}" fill="none" stroke="{O["dim"]}" '
             f'stroke-width="{s(H.PX["ref"]):.2f}" stroke-dasharray="{s(H.DASH_REF[0]):.2f} {s(H.DASH_REF[1]):.2f}"/>')
    o.append(ceiling(s, *P))
    o.append(H.line(s, P[0], P[1], P[0], P[1] + L + 20, O["dim"], "ref", H.DASH_REF))
    # release position, ghosted
    o.append(H.line(s, P[0], P[1], B0[0], B0[1], O["dim"], "ref", H.DASH_REF))
    o.append(f'<circle cx="{B0[0]:.2f}" cy="{B0[1]:.2f}" r="{s(9):.2f}" fill="#fff" stroke="{O["dim"]}" stroke-width="{s(1.2):.2f}" '
             f'stroke-dasharray="{s(3):.2f} {s(2):.2f}"/>')
    o.append(H.label(s, B0[0] + 16, B0[1] + 5, "release, at rest", "label2", I["secondary"]))
    o.append(arc(s, p, P[0], P[1], 54, -90, -90 + 60, BLU))
    o.append(H.label(s, P[0] + 24, P[1] + 42, f'θ{H.sub("0", s)}', fill=BLU))
    o.append(arc(s, p, P[0], P[1], 96, -90, -90 + 25, BLU))
    o.append(H.label(s, P[0] + 8, P[1] + 118, it("θ"), fill=BLU))
    o.append(rod(s, P, B))
    o.append(H.arrow(s, p, B[0] - ux * s(9), B[1] - uy * s(9), B[0] - ux * 84, B[1] - uy * 84, "reaction"))
    o.append(H.label(s, B[0] - ux * 64 - 12, B[1] - uy * 64 + 4, it("T"), fill=BLK, anchor="end"))
    o.append(H.arrow(s, p, B[0], B[1] + s(9), B[0], B[1] + 70, "load"))
    o.append(H.label(s, B[0] + 8, B[1] + 64, f'{it("m")}{it("g")}', fill=BRN))
    o.append(bob(s, *B, s(9)))
    # speed along the arc
    vx, vy = -uy, ux
    o.append(H.arrow(s, p, B[0] + vx * 14 - 6, B[1] + vy * 14 + 14, B[0] + vx * 54 - 6, B[1] + vy * 54 + 14, "geometry"))
    o.append(H.label(s, B[0] + vx * 54 - 12, B[1] + vy * 54 + 32, it("v"), fill=BLU, anchor="end"))
    o.append(H.joint_centre(s, *P))
    o.append(H.label(s, P[0] - 18, P[1] + L * 0.55, it("L"), fill=BLU, anchor="end"))
    aria = ("Problem D10 setup: a pendulum of length L released from rest at angle theta 0 (60 degrees, the dashed ghost "
            "position) and now at angle theta (25 degrees) from the downward vertical, moving with speed v along the dashed "
            "arc. On the bob: the rod tension T points up the rod and the weight m g points down.")
    return finish(VB, aria, s, o)


# ================================================================ lab problem figures (display_w = 400)
def problem_credit(s, VB, o, n=72):
    lines = wrap(NIH_ARM_CREDIT, n)
    o.append(H.credit(s, 8, VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines))


def beside(s, p, P_, f, A, sd, gap, meaning="reaction"):
    """Arrow of length A along force f (lab frame), starting `gap` from P_, shifted 18 units to one side."""
    ux, uy = unit(f)
    nx, ny = -uy * sd, -ux * sd
    b0 = (P_[0] + nx * 18 + ux * gap, P_[1] + ny * 18 - uy * gap)
    b1 = (b0[0] + ux * A, b0[1] - uy * A)
    return H.arrow(s, p, b0[0], b0[1], b1[0], b1[1], meaning), b0, b1, (nx, ny)


# ---------------------------------------------------------------- svg #46  D9 joint-angle coordinates
def fig46():
    p = "m3f46_"
    VB = (0, 0, 400, 340)
    s = H.Scale(VB[2], VB[3], display_w=400)
    t1, t2, L1, L2, K = 30.0, 50.0, LAB["L1"], LAB["L2"], 370.0
    F = Frame(64, 252, K)
    limb = Limb(p, s, K / 100)
    a1, a2 = math.radians(t1), math.radians(t1 + t2)
    e = (L1 * math.cos(a1), L1 * math.sin(a1))
    S, E, W = F(0, 0), F(*e), F(e[0] + L2 * math.cos(a2), e[1] + L2 * math.sin(a2))
    o = [f'<defs>{H.markers(p, s)}{limb.defs}</defs>']
    o.append(vhatch(s, S[0] - s(10), S[1] - 24, S[1] + 24, side=-1, step=10))
    o.append(H.line(s, S[0], S[1], S[0] + 150, S[1], O["dim"], "ref", H.DASH_REF))
    o.append(H.label(s, S[0] + 154, S[1] + 4, "horizontal", "label2", I["secondary"]))
    ex = (E[0] + (E[0] - S[0]) * 0.55, E[1] + (E[1] - S[1]) * 0.55)
    o.append(H.line(s, E[0], E[1], ex[0], ex[1], O["dim"], "ref", H.DASH_REF))
    o.append(limb.pose(S, E, W))
    o.append(arc(s, p, S[0], S[1], 64, 0, t1, BLU, "geometry"))
    o.append(H.label(s, S[0] + 78 * math.cos(math.radians(t1 / 2)), S[1] - 78 * math.sin(math.radians(t1 / 2)) + 6, f'θ{H.sub("1", s)}', fill=BLU))
    o.append(arc(s, p, E[0], E[1], 46, t1, t1 + t2, BLU, "geometry"))
    am = math.radians(t1 + t2 * 0.45)
    o.append(H.label(s, E[0] + 62 * math.cos(am), E[1] - 62 * math.sin(am) + 6, f'θ{H.sub("2", s)}', fill=BLU))
    o.append(H.joint_centre(s, *S))
    o.append(H.com_mark(s, *E))
    o.append(H.com_mark(s, *W))
    o.append(H.label(s, E[0] + 12, E[1] + 24, f'{it("m")}{H.sub("1", s)}', anchor="start"))
    o.append(H.label(s, W[0] + 14, W[1] + 5, f'{it("m")}{H.sub("2", s)}'))
    o.append(side_label(s, S, E, f'{it("L")}{H.sub("1", s)}', 22))
    o.append(side_label(s, E, W, f'{it("L")}{H.sub("2", s)}', 24))
    o.append(H.label(s, VB[2] - 8, 30, "θ₁ from the horizontal;", "label2", I["secondary"], "end"))
    o.append(H.label(s, VB[2] - 8, 30 + s(16), "θ₂ relative to link 1", "label2", I["secondary"], "end"))
    o.append(H.label(s, VB[2] - 8, 30 + s(32), "(drawn: θ₁ = 30°, θ₂ = 50°)", "label2", I["muted"], "end"))
    problem_credit(s, VB, o)
    aria = ("Problem D9 setup: a two-link limb drawn with NIH arm bones, shoulder pinned at left. The upper link, length L1 "
            "with point mass m1 at the elbow, makes angle theta 1 with the dashed horizontal; the forearm, length L2 with "
            "point mass m2 at the hand, makes the relative angle theta 2 with the dashed extension of the upper link. "
            "Drawn with theta 1 = 30 and theta 2 = 50 degrees.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #50  K1 a held load on the rail
def held_box(s, x, y, w=26, h=20):
    return (f'<rect x="{x - w / 2:.2f}" y="{y - h:.2f}" width="{w}" height="{h}" rx="{s(2):.2f}" fill="#f7f4ef" '
            f'stroke="{BRN}" stroke-width="{s(1.2):.2f}"/>')


def fig50():
    p = "m3f50_"
    VB = (0, 0, 400, 420)
    s = H.Scale(VB[2], VB[3], display_w=400)
    K = 470.0
    F = Frame(118, 52, K)
    limb = Limb(p, s, K / 100)
    q = lab_start()
    _, lam, _ = lab_solve(q, np.zeros(4))
    f_sh, _, _ = joint_forces(q, lam)
    o = [f'<defs>{H.markers(p, s)}{limb.defs}</defs>']
    sc, S, E, W = limb_scene(s, p, F, limb, q, rail_x=(-0.16, 0.50))
    o.append(sc)
    yr = F(0, LAB["yh"])[1] + s(4)
    # held mass in the hand, its weight, and the rail's push from below
    bx, by = W[0] + 22, W[1] - s(6)
    o.append(held_box(s, bx, by))
    o.append(H.label(s, bx, by - 6, it("m") + H.sub("L", s, "label2"), "label2", BRN, "middle"))
    o.append(H.arrow(s, p, bx, by - 84, bx, by - 24, "load"))
    o.append(H.label(s, bx + 8, by - 62, f'{it("m")}{H.sub("L", s)}{it("g")}', fill=BRN))
    o.append(H.arrow(s, p, W[0] - 6, yr + 64, W[0] - 6, yr + 2, "reaction"))
    o.append(H.label(s, W[0] - 16, yr + 40, f'contact λ{H.sub("3", s)}:', fill=BLK, anchor="end"))
    o.append(H.label(s, W[0] - 16, yr + 40 + s(18), f'rises by exactly {it("m")}{H.sub("L", s, "label2")}{it("g")}', "label2", BLK, "end"))
    a, b0, b1, (nx, ny) = beside(s, p, S, f_sh, 62, 1, s(8))
    o.append(a)
    o.append(H.label(s, b1[0] + 10, b1[1] + 14, f'{it("R")}{H.sub("s", s)}: does not move', fill=BLK))
    o.append(H.label(s, 8, S[1] - 16, "shoulder pin", "label2", I["secondary"]))
    o.append(H.label(s, F(-0.16, 0)[0], yr - 13, "horizontal rail", "label2", I["secondary"]))
    o.append(H.label(s, VB[2] - 8, 30, "arrow senses at release (40°);", "label2", I["muted"], "end"))
    o.append(H.label(s, VB[2] - 8, 30 + s(16), "not to force scale", "label2", I["muted"], "end"))
    problem_credit(s, VB, o)
    aria = ("Problem K1 setup: the lab's two-link limb (NIH arm bones) at its release pose, hand on the horizontal rail, "
            "holding a mass m L whose weight m L g points down. The rail pushes up on the hand with the contact force "
            "lambda 3, which rises by exactly m L g; the shoulder reaction R s along the upper arm does not move.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #52  K2 the hand on a vertical wall
def fig52():
    p = "m3f52_"
    VB = (0, 0, 400, 450)
    s = H.Scale(VB[2], VB[3], display_w=400)
    K, kN, mL = 470.0, 1.1, 5.0
    F = Frame(110, 66, K)
    limb = Limb(p, s, K / 100)
    q = lab_start(wall=True)
    _, lam, _ = lab_solve(q, np.zeros(4), mL=mL, wall=True)
    f_sh, _, nc = joint_forces(q, lam)
    o = [f'<defs>{H.markers(p, s)}{limb.defs}</defs>']
    sc, S, E, W = limb_scene(s, p, F, limb, q, rail=False, wall=True)
    o.append(sc)
    # the held mass hangs from the hand; its weight; the wall's horizontal reaction on the hand
    bx, by = W[0] - 16, W[1] + 44
    o.append(H.line(s, W[0], W[1], bx, by - 20, BRN, "leader"))
    o.append(held_box(s, bx, by))
    o.append(H.label(s, bx - 18, by - 4, it("m") + H.sub("L", s, "label2"), "label2", BRN, "end"))
    o.append(H.arrow(s, p, bx, by + 2, bx, by + 48, "load"))
    o.append(H.label(s, bx + 10, by + 40, f'{it("m")}{H.sub("L", s)}{it("g")}', fill=BRN))
    o.append(H.arrow(s, p, W[0] - s(8) - nc * kN * 2, W[1] - 2, W[0] - s(8), W[1] - 2, "reaction"))
    o.append(H.label(s, W[0] - s(8) - nc * kN * 2 - 6, W[1] - 22, "wall reaction λ₃:", "label2", BLK, "end"))
    o.append(H.label(s, W[0] - s(8) - nc * kN * 2 - 6, W[1] - 22 + s(16), "horizontal only", "label2", BLK, "end"))
    a, b0, b1, (nx, ny) = beside(s, p, S, f_sh, math.hypot(*f_sh) * kN, 1, s(8))
    o.append(a)
    o.append(H.label(s, b1[0] + 12, b1[1] - 4, f'{it("R")}{H.sub("s", s)} carries', fill=BLK))
    o.append(H.label(s, b1[0] + 12, b1[1] - 4 + s(18), "the vertical load", fill=BLK))
    o.append(H.label(s, F(LAB["xw"], 0)[0] + 16, F(0, -0.30)[1] - 8, f'wall {it("x")} = {it("x")}{H.sub("w", s, "label2")} = {LAB["xw"]:.2f} m',
                     "label2", I["secondary"]))
    o.append(H.label(s, 8, S[1] - 16, "shoulder pin", "label2", I["secondary"]))
    o.append(H.label(s, VB[2] - 8, 18, f'arrows at release, {it("m")}{H.sub("L", s, "label2")} = {mL:.0f} kg, one force scale:',
                     "label2", I["muted"], "end"))
    o.append(H.label(s, VB[2] - 8, 18 + s(16), f'{it("R")}{H.sub("s", s, "label2")} = {abs(lam[0]) * LAB["L1"]:.1f} N, '
                     f'λ₃ = {nc:.1f} N (λ₃ drawn ×2)', "label2", I["muted"], "end"))
    problem_credit(s, VB, o)
    aria = ("Problem K2 setup: the lab's two-link limb (NIH arm bones) with its hand on a frictionless vertical wall at x w "
            f"= 0.30 m, holding a hanging mass m L whose weight points down. The wall's reaction on the hand is horizontal; "
            f"the vertical load goes up the bones, and the shoulder reaction R s along the upper arm is large: at release "
            f"with m L = 5 kg, R s = {abs(lam[0]) * LAB['L1']:.1f} N against a wall reaction of {nc:.1f} N.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #62  K7 limb versus simple pendulum
def fig62():
    p = "m3f62_"
    VB = (0, 0, 400, 340)
    s = H.Scale(VB[2], VB[3], display_w=400)
    d = LAB
    h = lab_run()
    t_turn = h["t"][turning_index(h)]
    L_com = (d["m1"] * d["L1"] + d["m2"] * (d["L1"] + d["L2"])) / (d["m1"] + d["m2"])
    T_simple = 2 * math.pi * math.sqrt(L_com / d["g"])
    K = 330.0
    F = Frame(52, 48, K)
    limb = Limb(p, s, K / 100)
    q = lab_start()
    o = [f'<defs>{H.markers(p, s)}{limb.defs}</defs>']
    sc, S, E, W = limb_scene(s, p, F, limb, q, sup=(40, 40), rail_x=(-0.06, 0.44))
    o.append(sc)
    # simple pendulum of length L_com, released from the same 40 degrees, same scale
    P = (268.0, 48.0)
    Lp = L_com * K
    th = math.radians(40.0)
    B = swing_point(P, Lp, th)
    o.append(f'<path d="M{swing_point(P, Lp, -th)[0]:.2f},{swing_point(P, Lp, -th)[1]:.2f} A{Lp:.2f},{Lp:.2f} 0 0 0 '
             f'{B[0]:.2f},{B[1]:.2f}" fill="none" stroke="{O["dim"]}" stroke-width="{s(H.PX["ref"]):.2f}" '
             f'stroke-dasharray="{s(H.DASH_REF[0]):.2f} {s(H.DASH_REF[1]):.2f}"/>')
    o.append(ceiling(s, *P))
    o.append(H.line(s, P[0], P[1], P[0], P[1] + Lp + 10, O["dim"], "ref", H.DASH_REF))
    o.append(rod(s, P, B))
    o.append(H.com_mark(s, *B))
    o.append(H.joint_centre(s, *P))
    o.append(side_label(s, P, B, f'{it("L")}{H.sub("com", s)} = {L_com:.2f} m', 30, BLU, "label2"))
    yb = F(0, d["yh"])[1] + 34
    o.append(H.label(s, S[0] + 60, yb, "constrained limb", "label2", I["primary"], "middle"))
    o.append(H.label(s, S[0] + 60, yb + s(17), f'{it("T")} = 2 × {t_turn:.3f} s = {2 * t_turn:.2f} s', "label2", I["primary"], "middle"))
    o.append(H.label(s, P[0], yb, "simple pendulum", "label2", I["primary"], "middle"))
    o.append(H.label(s, P[0], yb + s(17), f'{it("T")} = 2π√({it("L")}{H.sub("com", s, "label2")}/{it("g")}) = {T_simple:.2f} s',
                     "label2", I["primary"], "middle"))
    o.append(H.label(s, VB[2] - 8, yb + s(38), "both released at 40°, drawn to one length scale", "label2", I["muted"], "end"))
    problem_credit(s, VB, o)
    aria = (f"Problem K7 setup, two panels to one length scale. Left: the lab's constrained two-link limb (NIH arm bones) "
            f"at its 40 degree release pose, hand on the rail; its measured period is 2 x {t_turn:.3f} s = {2 * t_turn:.2f} s. "
            f"Right: a simple pendulum of the centre-of-mass length L com = {L_com:.2f} m, released from 40 degrees, with "
            f"period 2 pi root(L com / g) = {T_simple:.2f} s.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #68  K10 three bones and a rail
def fig68():
    p = "m3f68_"
    VB = (0, 0, 400, 440)
    s = H.Scale(VB[2], VB[3], display_w=400)
    q, lam, R = k10_release()
    L1, L2, L3 = K10["L"]
    K, kN = 410.0, 2.6
    F = Frame(108, 46, K)
    limb = Limb(p, s, K / 100)
    x1, y1, x2, y2, x3, y3 = q
    S, E, Wr, Tp = F(0, 0), F(x1, y1), F(x2, y2), F(x3, y3)
    # forces drawn at the joints: bone i on its proximal joint, the rail on the tip (as svg #21)
    f_sh = (-lam[0] * x1, -lam[0] * y1)
    f_el = (-lam[1] * (x2 - x1), -lam[1] * (y2 - y1))
    f_wr = (-lam[2] * (x3 - x2), -lam[2] * (y3 - y2))
    o = [f'<defs>{H.markers(p, s)}{limb.defs}</defs>']
    o.append(hatch(s, S[0] - 46, S[0] + 46, S[1] - s(4), side=-1))
    o.append(hatch(s, F(0.20, 0)[0], F(0.56, 0)[0], Tp[1] + s(4)))
    # bone 3: the hand-held tool (not anatomy), drawn as a rod
    ux, uy = unit((Tp[0] - Wr[0], Tp[1] - Wr[1]))
    w3 = s(5)
    o.append(f'<path d="M{Wr[0] - uy * w3:.2f},{Wr[1] + ux * w3:.2f} L{Tp[0] - uy * w3:.2f},{Tp[1] + ux * w3:.2f} '
             f'L{Tp[0] + uy * w3:.2f},{Tp[1] - ux * w3:.2f} L{Wr[0] + uy * w3:.2f},{Wr[1] - ux * w3:.2f} Z" fill="#f7f4ef" '
             f'stroke="{I["secondary"]}" stroke-width="{s(1.2):.2f}" stroke-linejoin="round"/>')
    o.append(limb.pose(S, E, Wr))
    o.append(H.joint_centre(s, *S))
    for P_ in (E, Wr, Tp):
        o.append(H.com_mark(s, *P_))
    names = (("shoulder", R[0], S, f_sh, 1), ("elbow", R[1], E, f_el, 1), ("wrist", R[2], Wr, f_wr, -1))
    for name, val, P_, f, sd in names:
        A = max(math.hypot(*f) * kN, s(12))
        a, b0, b1, (nx, ny) = beside(s, p, P_, f, A, sd, s(8))
        o.append(a)
        o.append(H.label(s, b1[0] + (12 if sd > 0 else -12), b1[1] + 5, f'{name} {val:.1f} N', "label2", BLK,
                         "start" if sd > 0 else "end"))
    o.append(H.arrow(s, p, Tp[0] + 14, Tp[1] + s(4) + R[3] * kN + 4, Tp[0] + 14, Tp[1] + s(5), "reaction"))
    o.append(H.label(s, Tp[0] + 22, Tp[1] + 30, f'contact {R[3]:.1f} N', "label2", BLK))
    o.append(side_label(s, Wr, Tp, f'tool, {it("L")}{H.sub("3", s, "label2")} = {L3:.2f} m', 24, I["secondary"], "label2"))
    o.append(H.label(s, Tp[0] + 12, Tp[1] - 12, f'{it("m")}{H.sub("3", s, "label2")} = 1.0 kg', "label2", I["secondary"]))
    o.append(H.label(s, F(0.20, 0)[0] - 6, Tp[1] + 8, f'rail {it("y")} = {K10["yh"]:.2f} m'.replace("-", "−"), "label2", I["secondary"], "end"))
    for j, txt in enumerate(("10 × 10 KKT system:", "one solve at release returns", "all four forces (one scale)")):
        o.append(H.label(s, VB[2] - 8, 20 + j * s(16), txt, "label2", I["primary"], "end"))
    problem_credit(s, VB, o)
    aria = (f"Problem K10 setup: a three-link limb at its release pose: NIH arm bones for the upper arm (40 degrees off "
            f"the hang) and the vertical forearm, then a hand-held tool of length 0.25 m with a 1.0 kg mass at its tip, which "
            f"rests on a rail at y = minus 0.68 m. Black arrows to one force scale give the four forces from one solve of "
            f"the 10 by 10 KKT system: shoulder {R[0]:.1f} N, elbow {R[1]:.1f} N, wrist {R[2]:.1f} N, contact {R[3]:.1f} N.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #39  D2 elbow free body (m05 arm at 90°)
D2 = dict(W=49.0, L=0.35, d=0.03, Wf=15.0, c=0.116)      # line 1955


def fig39():
    p = "m3f39_"
    VB = (0, 0, 400, 490)
    s = H.Scale(VB[2], VB[3], display_w=400)
    K = 7.4                                              # canvas units per cm
    Ec = (56.0, 272.0)
    A = Arm(p, s, Ec, K, r_ins=D2["d"] * 100)
    d = D2
    G, C = A.C((d["L"] * 100, 0.0)), A.C((d["c"] * 100, 0.0))
    o = [f'<defs>{H.markers(p, s)}</defs>']
    # held weight: a bag on a strap behind the hand
    o.append(H.line(s, G[0], G[1], G[0], G[1] + 18, BRN, "leader"))
    o.append(held_box(s, G[0], G[1] + 38, 28, 20))
    o.append(A.bones())
    bic, bez, width = A.biceps()
    o.append(bic)
    loa, (lx, ly) = A.loa()
    o.append(loa)
    nx, ny = -ly, lx
    if nx < 0:
        nx, ny = -nx, -ny
    S0 = (A.I[0] + nx * 9, A.I[1] + ny * 9 - 6)
    top = (S0[0] - lx * 70, S0[1] - ly * 70)
    o.append(H.arrow(s, p, S0[0], S0[1], top[0], top[1], "force"))
    o.append(H.label(s, top[0] + 10, top[1] + 12, f'{it("F")}{H.sub("m", s)} = ?', fill=RED))
    # joint reaction on the forearm (down), weights
    o.append(H.arrow(s, p, Ec[0] - 8, Ec[1] + s(8), Ec[0] - 8, Ec[1] + 74, "reaction"))
    o.append(H.label(s, Ec[0] - 16, Ec[1] + 66, f'{it("R")} = ?', fill=BLK, anchor="end"))
    o.append(H.com_mark(s, *C))
    o.append(H.arrow(s, p, C[0], C[1] + s(8), C[0], C[1] + 56, "load"))
    o.append(H.label(s, C[0] + 8, C[1] + 50, f'{it("W")}{H.sub("f", s)} = {d["Wf"]:.0f} N', fill=BRN))
    o.append(H.arrow(s, p, G[0], G[1] + 50, G[0], G[1] + 96, "load"))
    o.append(H.label(s, G[0] - 8, G[1] + 86, f'{it("W")}{H.sub("load", s)} = {d["W"]:.0f} N', fill=BRN, anchor="end"))
    o.append(H.joint_centre(s, *Ec))
    o.append(H.label(s, Ec[0] - 10, Ec[1] - 12, "elbow", "label2", I["secondary"], "end"))
    o.append(H.label(s, Ec[0] - 10, Ec[1] + 3, "axis", "label2", I["secondary"], "end"))
    # levers from the elbow axis, one row each under the arm
    rows = ((Ec[1] + 112, C[0], f'{it("c")} = {d["c"]:.3f} m', "dim", I["primary"]),
            (Ec[1] + 136, G[0], f'{it("L")} = {d["L"]:.2f} m', "dim", I["primary"]),
            (Ec[1] + 160, A.P[0], f'{it("d")} = {d["d"]:.2f} m', "geometry", BLU))
    o.append(H.line(s, Ec[0], Ec[1] + 78, Ec[0], Ec[1] + 166, O["dim"], "leader", H.DASH_REF))
    o.append(H.line(s, A.P[0], A.P[1] + s(6), A.P[0], Ec[1] + 166, O["dim"], "leader", H.DASH_REF))
    o.append(H.line(s, C[0], C[1] + 58, C[0], Ec[1] + 118, O["dim"], "leader", H.DASH_REF))
    o.append(H.line(s, G[0], G[1] + 100, G[0], Ec[1] + 142, O["dim"], "leader", H.DASH_REF))
    for y, X, txt, mean, col in rows:
        o.append(H.arrow(s, p, Ec[0], y, X, y, mean, both=True))
        o.append(H.label(s, X + 8, y + 5, txt, "label2", col))
    bx, by, bnx, bny = bez(0.55)
    e = (bx + abs(bnx) * width(0.55), by)
    o.append(H.line(s, e[0] + 2, e[1], 150, e[1] - 6, T["muscle"][1]))
    o.append(H.label(s, 154, e[1] - 2, "biceps", fill=T["muscle"][1]))
    lines = wrap(H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt 208", title="Human Arm Bones",
                                            changes="Recoloured; reposed (humerus vertical, forearm horizontal). "
                                                    "Biceps and overlays drawn for this course."), 72)
    o.append(H.credit(s, 8, VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines))
    aria = ("Problem D2 setup: free-body diagram of the forearm at the elbow, side view with NIH arm bones: humerus "
            "vertical, forearm and hand horizontal. The biceps inserts on the radius d = 0.03 m from the elbow axis and "
            "pulls up with the unknown force F m along its tendon. The forearm-plus-hand weight W f = 15 N acts at its "
            "centre of mass c = 0.116 m from the axis; the held load W load = 49 N hangs at L = 0.35 m. The unknown joint "
            "reaction R acts down on the forearm at the elbow axis.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #35  C8 two-force bone vs mid-shaft pull
FEM = dict(head=(47.36, 56.15),          # Kasa fit to the head arc of path 9 of nih_upper_leg.svg (Chrome samples)
           knee=(39.6, 372.5),           # mid-point of the condyles' lowest outline, same path (x 8.0..71.2, y 372.5)
           shaft_r=(40.0, 214.0))        # lateral (right) shaft edge at mid-height, same path (x 20.7 / 40.0 at y 214)
NIH_LEG_CREDIT = H.ATTRIBUTION["pd"].format(author="NIH NIAID BioArt 244", title="Human Upper Leg Bones",
                                            changes="Recoloured; overlays drawn for this course.")


def femur_at(s, ox, oy, k, d_path):
    st = (f'fill="{T["bone"][0]}" stroke="{T["bone"][1]}" stroke-width="{s(H.PX["art_line"]) / k:.3f}" stroke-linejoin="round"')
    return f'<g transform="translate({ox:.2f} {oy:.2f}) scale({k:.4f})"><path d="{d_path}" {st}/></g>'


def fig35():
    p = "m3f35_"
    VB = (0, 0, 400, 380)
    s = H.Scale(VB[2], VB[3], display_w=400)
    k, top = 0.62, 86.0
    dpath = femur_d()
    o = [f'<defs>{H.markers(p, s)}</defs>']
    belly = Arm(p, s, (0.0, 0.0), 1.0)            # only its belly() drawer, in canvas units
    for col, ox in ((0, 58.0), (1, 214.0)):
        ty = top - FEM["head"][1] * k
        o.append(femur_at(s, ox, ty, k, dpath))
        M = lambda q: (ox + q[0] * k, ty + q[1] * k)      # noqa: E731
        Hd, Kn = M(FEM["head"]), M(FEM["knee"])
        ux, uy = unit((Kn[0] - Hd[0], Kn[1] - Hd[1]))
        if col == 0:
            o.append(H.line(s, Hd[0] - ux * 30, Hd[1] - uy * 30, Kn[0] + ux * 30, Kn[1] + uy * 30, O["dim"], "ref", H.DASH_REF))
            o.append(H.arrow(s, p, Hd[0] - ux * 50, Hd[1] - uy * 50, Hd[0] - ux * 10, Hd[1] - uy * 10, "reaction"))
            o.append(H.arrow(s, p, Kn[0] + ux * 50, Kn[1] + uy * 50, Kn[0] + ux * 6, Kn[1] + uy * 6, "reaction"))
            o.append(H.label(s, Hd[0] + 10, Hd[1] - 32, it("R"), fill=BLK))
            o.append(H.label(s, Kn[0] + 10, Kn[1] + 40, it("R"), fill=BLK))
            mx = Hd[0] + 22
            for j, txt in enumerate(("line of action", "through both", "joint centres")):
                o.append(H.label(s, mx, (Hd[1] + Kn[1]) / 2 - 16 + j * s(16), txt, "label2", I["secondary"]))
        else:
            ins = M(FEM["shaft_r"])
            org = (ins[0] + 92, ins[1] - 54)
            sv, _, _ = belly.belly(((org[0] - 4, org[1] + 4), (ins[0] + 52, ins[1] - 36), (ins[0] + 14, ins[1] - 4)), 8.0,
                                   T["muscle_dk"][1])
            o.append(belly.tendon((ins[0] + 14, ins[1] - 4), ins, 2.0))
            o.append(sv)
            o.append(hatch(s, org[0] - 14, org[0] + 16, org[1] - s(4), side=-1, step=8))
            o.append(H.label(s, org[0], org[1] - 20, "origin", "label2", I["secondary"], "middle"))
            o.append(f'<circle cx="{ins[0]:.2f}" cy="{ins[1]:.2f}" r="{s(2.8):.2f}" fill="{RED}" stroke="#fff" stroke-width="{s(1):.2f}"/>')
            fx, fy = unit((org[0] - ins[0], org[1] - ins[1]))
            b0 = (ins[0] - fy * 14 + 4, ins[1] + fx * 14)
            o.append(H.arrow(s, p, b0[0], b0[1], b0[0] + fx * 56, b0[1] + fy * 56, "force"))
            o.append(H.label(s, b0[0] + fx * 30 + 6, b0[1] + fy * 30 + 26, f'{it("F")}{H.sub("m", s)}', fill=RED))
            # the end reactions now act across the bone, opposite the pull; the bone bends (exaggerated)
            for P_ in (Hd, Kn):
                o.append(H.arrow(s, p, P_[0] + 46, P_[1] + 2, P_[0] + 12, P_[1] + 2, "reaction"))
            o.append(H.label(s, Hd[0] + 52, Hd[1] + 7, it("R"), fill=BLK))
            o.append(H.label(s, Kn[0] + 52, Kn[1] + 7, it("R"), fill=BLK))
            bend = [(Hd[0] + (Kn[0] - Hd[0]) * t + 20 * math.sin(math.pi * t), Hd[1] + (Kn[1] - Hd[1]) * t) for t in
                    [i / 30 for i in range(31)]]
            o.append(f'<path d="M{" L".join(f"{x:.2f},{y:.2f}" for x, y in bend)}" fill="none" stroke="{O["dim"]}" '
                     f'stroke-width="{s(H.PX["ref"]):.2f}" stroke-dasharray="{s(H.DASH_REF[0]):.2f} {s(H.DASH_REF[1]):.2f}"/>')
            o.append(H.label(s, ins[0] + 40, ins[1] + 66, "the axis bends", "label2", I["secondary"]))
            o.append(H.label(s, ins[0] + 40, ins[1] + 66 + s(16), "(Module 2)", "label2", I["secondary"]))
    o.append(H.label(s, 100, 24, "ends only → axial", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, 290, 24, "mid-shaft pull → bending", "label2", I["primary"], "middle", 'font-style="italic"'))
    lines = wrap(NIH_LEG_CREDIT, 72)
    o.append(H.credit(s, 8, VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines))
    aria = ("Problem C8 setup, two femurs (NIH art). Left: a femur loaded only at its two joints, the hip and the knee; the "
            "two end forces R act along the dashed line through both joint centres, so the reaction is axial. Right: a "
            "muscle from a separate origin inserts mid-shaft and pulls with force F m; the end reactions R now act across "
            "the bone, and the dashed axis bends (exaggerated), the beam case of Module 2.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #43  D6 pelvis + two legs + ground = four-bar
LEG = dict(hipL=(47.36, 56.15), hipR=(203.91, 56.86),     # Kasa fits to the femoral-head arcs, paths 9 and 10
           kneeL=(39.6, 372.5), kneeR=(206.9, 373.5))     # condyle mid-points, lowest outline of the same paths
SHANK_OVER_THIGH = 0.246 / 0.245                          # Winter segment lengths (fraction of stature)


def fig43():
    p = "m3f43_"
    VB = (0, 0, 400, 536)
    s = H.Scale(VB[2], VB[3], display_w=400)
    src = H.recolour(_read("nih_upper_leg.svg"), "nih")
    ds = re.findall(r'<path\b[^>]*?\bd="([^"]+)"', src)
    k = 0.56
    ox, oy = 200 - 125.6 * k, 40 - 0.0 * k
    M = lambda q: (ox + q[0] * k, oy + q[1] * k)      # noqa: E731
    st = (f'fill="{T["bone"][0]}" stroke="{T["bone"][1]}" stroke-width="{s(H.PX["art_line"]) / k:.3f}" stroke-linejoin="round"')
    sh = f'fill="{T["bone_shade"][0]}" stroke="{T["bone"][1]}" stroke-width="{s(H.PX["art_line"]) / k:.3f}"'
    art = (f'<g transform="translate({ox:.2f} {oy:.2f}) scale({k})">' + f'<path d="{absolute(ds[1])}" {st} fill-rule="evenodd"/>'
           + "".join(f'<path d="{absolute(ds[i])}" {sh}/>' for i in (11, 12))
           + "".join(f'<path d="{absolute(ds[i])}" {st}/>' for i in (8, 9)) + '</g>')
    d = LEG
    hips = [M(d["hipL"]), M(d["hipR"])]
    knees = [M(d["kneeL"]), M(d["kneeR"])]
    ank = [(Kn[0] + (Kn[0] - Hp[0]) * SHANK_OVER_THIGH, Kn[1] + (Kn[1] - Hp[1]) * SHANK_OVER_THIGH) for Hp, Kn in zip(hips, knees)]
    yg = max(a[1] for a in ank)
    ank = [(a[0], yg) for a in ank]
    o = [f'<defs>{H.markers(p, s)}</defs>', art]
    o.append(hatch(s, ank[0][0] - 50, ank[1][0] + 50, yg + s(6)))
    for Hp, Kn, An in zip(hips, knees, ank):
        o.append(H.line(s, Hp[0], Hp[1], Kn[0], Kn[1], BLU, "geom"))
        o.append(H.line(s, Kn[0], Kn[1], An[0], An[1], BLU, "geom", H.DASH_REF))
    o.append(H.line(s, hips[0][0], hips[0][1], hips[1][0], hips[1][1], BLU, "geom"))
    for P_ in hips + ank:
        o.append(H.joint_centre(s, *P_))
    mx = (hips[0][0] + hips[1][0]) / 2
    o.append(H.label(s, mx, hips[0][1] - 26, "pelvis (link)", "label2", I["primary"], "middle"))
    o.append(H.label(s, hips[0][0] - 14, hips[0][1] + 4, "hip pin", "label2", I["primary"], "end"))
    o.append(H.label(s, hips[1][0] + 14, hips[1][1] + 4, "hip pin", "label2", I["primary"]))
    mid_y = (knees[0][1] + ank[0][1]) / 2
    o.append(H.label(s, ank[0][0] - 12, mid_y - 8, "shank (rigid,", "label2", I["secondary"], "end"))
    o.append(H.label(s, ank[0][0] - 12, mid_y + 8, "not drawn)", "label2", I["secondary"], "end"))
    o.append(H.label(s, hips[1][0] + 14, (hips[1][1] + knees[1][1]) / 2, "leg (link)", "label2", I["primary"]))
    o.append(H.label(s, ank[0][0] - 12, yg - 10, "foot pin", "label2", I["primary"], "end"))
    o.append(H.label(s, ank[1][0] + 12, yg - 10, "foot pin", "label2", I["primary"]))
    o.append(H.label(s, mx, yg + 34, "ground (the fixed link)", "label2", I["primary"], "middle"))
    o.append(H.label(s, mx, yg + 34 + s(17), "4 links, 4 pins, one closed loop", "label2", BLU, "middle"))
    lines = wrap(NIH_LEG_CREDIT.replace("Recoloured;", "Recoloured; pelvis and femurs only;"), 72)
    o.append(H.credit(s, 8, VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines))
    aria = ("Problem D6 setup, front view: the pelvis and both femurs from NIH art, standing. Blue links join the pins: the "
            "pelvis link between the two hip pins, a leg link on each side from the hip pin down the femur and the dashed, "
            "undrawn rigid shank to a foot pin on the hatched ground, and the ground as the fixed fourth link. Four links, "
            "four pins, one closed loop: a four-bar linkage.")
    return finish(VB, aria, s, o)


# ---------------------------------------------------------------- svg #25  ideal hinge vs real knee (DBCLS lateral view)
KNEE_RECOLOUR = {                       # DBCLS lateral knee (st0..st8) -> house tokens; not in house.RECOLOUR
    "#cec2b2": T["bone"][0], "#a59983": T["bone_shade"][0], "#84755d": T["bone"][1], "#eae4dc": "#f7f4ef",
    "#aec5ff": T["fibrocart"][0], "#e3ebff": T["cartilage"][0], "#93a3cc": T["fibrocart"][1],
    "#f4f4f4": T["tendon"][0], "#9e9e9e": T["tendon"][1],
}
KNEE = dict(
    box=(150, 60, 156, 240),           # the crop window (crop_art.py ... m03f25 150 60 306 300), source units
    # path 6 (femur fill) lowest outline, Chrome getPointAtLength samples: the lateral condyle
    condyle=[(152.57, 143.48), (151.79, 151.53), (152.86, 159.56), (155.65, 167.16), (160.09, 173.93), (165.93, 179.54),
             (172.77, 183.88), (180.28, 186.93), (188.19, 188.71), (196.27, 189.23), (204.35, 188.51), (212.25, 186.67),
             (219.86, 183.88), (227.12, 180.26), (233.99, 175.96), (240.47, 171.08)],
    fem_axis=((196.6, 62.0), (211.0, 90.0)),   # path 6 shaft mid-points (edges 166.8 / 226.5 at y 40, 176.3 / 246 at y 90)
    tib_axis=((214.5, 260.0), (215.6, 300.0)),  # path 9 shaft mid-points (edges 168.6 / 260.5 at y 260, 184.3 / 246.8 at y 355)
    plateau=((165.0, 201.6), (249.5, 196.0)),   # path 9 upper edge
    cartilage=(258.0, 118.0),                   # path 43 (articular cartilage of the femoral groove), on the layer
    meniscus=(246.0, 201.0),                    # path 16 (meniscus), on the band
    ligament=(180.0, 222.0),                    # path 60 (lateral ligament band), on the band
)


def knee_art(p):
    src = _read("202108_Lateral_view_of_knee_joint_crop_m03f25.svg")
    style = re.search(r'<style>.*?</style>', src, re.S).group(0)
    body = src[src.index('<g i:extraneous="self">'):src.index('</switch>')]
    body = re.sub(r'\si:[\w-]+="[^"]*"', '', body)
    assert "<text" not in body
    doc = style + body
    pat = re.compile("|".join(re.escape(c) for c in KNEE_RECOLOUR), re.I)
    doc = pat.sub(lambda m: KNEE_RECOLOUR[m.group(0).lower()], doc)
    return art_image(f"<svg>{doc}</svg>", KNEE["box"], f'id="{p}knee"')


def fig25():
    p = "m3f25_"
    VB = (0, 0, 760, 420)
    s = H.Scale(VB[2], VB[3])
    kz = 1.32
    cx, cy, cr = fit_circle(KNEE["condyle"])
    o = [f'<defs>{H.markers(p, s)}{knee_art(p)}</defs>']
    panels = ((120.0, "Ideal hinge (our model)"), (500.0, "Real knee"))
    for i, (x0, title) in enumerate(panels):
        tx, ty = x0 - KNEE["box"][0] * kz, 40 - KNEE["box"][1] * kz
        Mp = lambda q: (tx + q[0] * kz, ty + q[1] * kz)      # noqa: E731
        op = ' opacity="0.32"' if i == 0 else ""
        o.append(f'<use href="#{p}knee" transform="translate({tx:.2f} {ty:.2f}) scale({kz})"{op}/>')
        C = Mp((cx, cy))
        o.append(H.label(s, x0 + 78 * kz, 26, title, "label", I["primary"], "middle", 'font-weight="bold"'))
        if i == 0:
            F0, F1 = Mp(KNEE["fem_axis"][0]), C
            T1 = Mp(KNEE["tib_axis"][1])
            for A_, B_ in ((F0, F1), (C, T1)):
                for col, w in (("#fff", 9), (BLU, 6)):
                    o.append(f'<line x1="{A_[0]:.2f}" y1="{A_[1]:.2f}" x2="{B_[0]:.2f}" y2="{B_[1]:.2f}" stroke="{col}" '
                             f'stroke-width="{s(w):.2f}" stroke-linecap="round"/>')
            o.append(H.joint_centre(s, *C))
            o.append(arc(s, p, C[0], C[1], 44, -40, 40, BLU, "geometry"))
            o.append(H.label(s, C[0] + 50, C[1] - 40, "one rotation", "label2", BLU))
            o.append(H.label(s, C[0] - 34, C[1] - 70, "rigid link", "label2", I["primary"], "end"))
            o.append(H.label(s, C[0] - 34, C[1] + 80, "rigid link", "label2", I["primary"], "end"))
            o.append(H.line(s, C[0] + 8, C[1] + 8, C[0] + 40, C[1] + 44, I["primary"]))
            o.append(H.label(s, C[0] + 44, C[1] + 56, "one fixed,", "label2", I["primary"]))
            o.append(H.label(s, C[0] + 44, C[1] + 56 + s(16), "frictionless pin", "label2", I["primary"]))
            o.append(H.label(s, x0 + 78 * kz, VB[3] - 44, "one fixed, frictionless axis; rigid surfaces", "label2", I["secondary"],
                             "middle", 'font-style="italic"'))
        else:
            # roll (arc along the condyle) + glide (along the plateau); the contact point moves
            o.append(arc(s, p, C[0], C[1], cr * kz + 10, -150, -110, BLU, "geometry"))
            o.append(H.label(s, C[0] - cr * kz - 18, C[1] + cr * kz * 0.6, "roll", "label2", BLU, "end"))
            P0, P1 = Mp(KNEE["plateau"][0]), Mp(KNEE["plateau"][1])
            gy = (P0[1] + P1[1]) / 2 + 30
            o.append(H.arrow(s, p, C[0] - 6, gy + 10, C[0] + 44, gy + 10, "geometry"))
            o.append(H.label(s, C[0] + 50, gy + 15, "+ glide", "label2", BLU))
            o.append(H.label(s, C[0] - 2, gy + 64, "the contact point and the", "label2", I["secondary"], "middle"))
            o.append(H.label(s, C[0] - 2, gy + 64 + s(16), "rotation axis migrate", "label2", I["secondary"], "middle"))
            for key, txt, dx, anc in (("cartilage", "cartilage", 30, "start"), ("meniscus", "meniscus", 54, "start"),
                                      ("ligament", "ligament (compliant)", -86, "end")):
                Q = Mp(KNEE[key])
                Lx = Q[0] + dx
                o.append(H.line(s, Q[0], Q[1], Lx + (-4 if anc == "start" else 4), Q[1] - 10, I["primary"]))
                o.append(mark(s, *Q, I["primary"], 2.2))
                o.append(H.label(s, Lx, Q[1] - 6, txt, "label2", I["primary"], anc))
            o.append(H.label(s, x0 + 78 * kz, VB[3] - 44, "migrating axis, compliant, lubricated", "label2", I["secondary"],
                             "middle", 'font-style="italic"'))
    o.append(H.line(s, 380, 40, 380, VB[3] - 60, "#e6e6e6", "leader"))
    cr_txt = H.ATTRIBUTION["by"].format(author="DataBase Center for Life Science (DBCLS)", title="202108 Lateral view of knee joint",
                                        licence="CC BY 4.0", changes="Recoloured, cropped; drawn twice (left faded); overlays added.")
    lines = wrap(cr_txt, 120)
    o.append(H.credit(s, 8, VB[3] - 6 - (len(lines) - 1) * s(H.PX["credit"]) * 1.25, lines))
    aria = ("Two panels of the same lateral view of a knee (DBCLS art). Left, faded: our model, the femur and the "
            "tibia replaced by two blue rigid links meeting at one fixed, frictionless pin, with one rotation arrow. "
            "Right: the real knee: the rounded femoral condyle rolls (red arc) and glides (red arrow) on the tibial "
            "plateau, so the contact point and the rotation axis migrate; labels mark the blue articular cartilage, the "
            "meniscus and a compliant ligament.")
    return finish(VB, aria, s, o)


FIGS = {
    4: ("Left: a two-link arm swinging through poses. Right: the matc", fig4),
    10: ("A pendulum: pivot at top, rod to a bob at angle theta from v", fig10),
    11: ("Animation of a swinging pendulum; a red tension arrow along ", fig11),
    21: ("A two-link limb: shoulder pinned at top left on hatched grou", fig21),
    24: ("Animation of the two-link limb swinging with its hand slidin", fig24),
    25: ("Left: an ideal hinge — two rigid bars meeting at a single fi", fig25),
    35: ("Left: a bone loaded only at its two ends carries an axial fo", fig35),
    38: ("A pendulum: pivot at top, a rigid rod to a bob on a dashed c", fig38),
    39: ("Sagittal free-body diagram of the elbow: vertical upper arm,", fig39),
    43: ("A closed loop: a pelvis bar joined by two legs to the ground", fig43),
    46: ("A two-link limb with the first link at angle theta-1 from ho", fig46),
    47: ("A pendulum at angle theta from the vertical (released from t", fig47),
    50: ("A two-link limb with its hand on a horizontal rail and a hel", fig50),
    52: ("A two-link limb pressing its hand on a vertical wall with a ", fig52),
    62: ("Side by side: the two-link constrained limb with its measure", fig62),
    68: ("A three-link limb with its tip on a rail, labelled with the ", fig68),
}
