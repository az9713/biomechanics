"""Module 7, group `body_dk`: derivational problems D1-D10 (svg #36-#45) and K10 (svg #55), house style, 400 px.

Bodies are the posable Lynch skeleton (lynch_body.py); body_main.py puts its defs on the page, this group only
<use>s them.  Conventions of body_c.py: stature 1.75 m, the text's COM 0.55 H up and 0.02 m ahead of the ankle
(module07.html lines 144, 176), ink labels, Lynch credit at the foot of every body figure.  D2, D5, D6 and D7 are
not about the body: they are a phase plane, a gain plane, a phasor diagram and a crossing-frequency plot.
Every number on a figure is computed here from the constants the module states (line numbers beside them).
"""
import math

import numpy as np

import house as H
import lynch_body as LB
from m05.body import finish, it
from m05.plots_prob import Plot, label as plabel, legend
from m07.body_c import (CM, D_HEEL, D_TOE, DE, ELL, G, I_A, KD, KP, LIMIT, MGL, ML, MT, RL, RT, W0, M, bisect,
                        close, cmu, credit, ext, floor, lab, quartic, rect, sub, whole_com, VBs)
from m07.body_main import angle_arc, arc_arrow, cop_mark, lean, vline, xcom_mark

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
BOX = "#f7f4ef"
GRID = "#e6e6e6"
MGN = M * G                              # N, body weight (line 357: M = 70 kg); the text rounds it to 690 (522)
WC, DCRIT = quartic(KP, KD)              # Prop 6.3 at the representative gains (line 493)
close(WC, 2.2, 0.05)                     # line 494
close(WC / (2 * math.pi), 0.35, 0.005)   # line 494
close(DCRIT, 0.13, 0.005)                # line 494
close(1 / W0, 0.33, 0.005)               # line 360
close(MGN * D_TOE, 80, 3)                # "near 80 N m" (lines 522, 835)


def sup(t, s, size="label2"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def lines(s, x, y, rows, size="label2", anchor="start", fill=None):
    L = s(H.PX[size]) * 1.35
    return "".join(lab(s, x, y + i * L, t, size, fill or I["primary"], anchor) for i, t in enumerate(rows))


def mn(v, f="{:g}"):
    return (v if isinstance(v, str) else f.format(v)).replace("-", "−")


def xs(t, s, size="label"):
    """x with a subscript (x_com, x_cop)."""
    return f'{it("x")}{sub(t, s, size)}'


def pvb(h):
    return (0, 0, 400, h), H.Scale(400, h, display_w=400)


# ================================================================ svg #36  D1 Euler's law about the ankle
TH36 = 10.0                              # deg, drawn lean (design value, as Fig. 6)


def fig36():
    p = "m7f36_"
    VB, s = VBs(410)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 300.0, 352.0
    body, J = lean(s, TH36, 140.0, fy, HF, p=p)
    ax, ay = J["ankle"]
    c = J["comT"]
    o.append(floor(s, 8, 236, fy))
    o.append(body)
    yd = c[1] - s(24)
    o.append(vline(s, ax, ay - s(8), yd + s(2), O["dim"]))
    o.append(ext(s, ax, ay, c[0], c[1]))
    o.append(angle_arc(s, ax, ay, s(74), -90, -90 + TH36))
    o.append(lab(s, ax + s(5), ay - s(80), it("θ"), "label2"))
    mid = LB.lerp((ax, ay), c, 0.62)
    o.append(H.line(s, mid[0] + s(3), mid[1], mid[0] + s(52), mid[1] - s(10), I["secondary"], "leader"))
    o.append(lab(s, mid[0] + s(55), mid[1] - s(6), f'{it("ℓ")} = 0.9 m', "label2"))
    o.append(H.arrow(s, p, ax, yd, c[0], yd, "geometry", both=True))
    o.append(lab(s, (ax + c[0]) / 2, yd - s(7), f'{it("ℓ")} sin {it("θ")}', "label2", anchor="middle"))
    o.append(H.arrow(s, p, c[0], c[1] + s(9), c[0], c[1] + s(78), "load"))
    o.append(lab(s, c[0] + s(7), c[1] + s(72), it("Mg"), "label2"))
    o.append(H.com_mark(s, *c))
    o.append(lab(s, c[0] + s(10), c[1] - s(7), "COM", "label2"))
    o.append(H.joint_centre(s, ax, ay))
    o.append(lab(s, ax - s(12), ay + s(4), it("O"), "label2", anchor="end"))
    o.append(arc_arrow(s, p, ax, ay, s(40), -25, -150, "force"))
    o.append(lines(s, ax - s(44), ay - s(40), [f'{it("τ")}: ankle torque,', "restoring"], anchor="end"))
    # the equation and its sign
    x0 = 226
    o.append(lab(s, x0, 26, "Euler’s law about the ankle O:", "label2"))
    o.append(lab(s, x0, 48, f'{it("I")} d²{it("θ")}/d{it("t")}² = {it("Mgℓ")} sin {it("θ")} − {it("τ")}', "label2"))
    o.append(lines(s, x0, 78, [f'+{it("Mgℓ")} sin {it("θ")} grows with {it("θ")}:',
                               "gravity drives the lean further,", "the destabilising term"]))
    # a hanging pendulum for contrast (schematic, not anatomy)
    px_, py_, Lp, a = 312.0, 168.0, 92.0, math.radians(22)
    bob = (px_ + Lp * math.sin(a), py_ + Lp * math.cos(a))
    o.append(rect(s, px_ - 22, py_ - 6, 44, 6, fill=GRID, stroke=I["rule"]))
    o.append(H.line(s, px_, py_, px_, py_ + Lp + 8, O["dim"], "ref", H.DASH_REF))
    o.append(H.line(s, px_, py_, *bob, I["secondary"], "force"))
    o.append(f'<circle cx="{bob[0]:.2f}" cy="{bob[1]:.2f}" r="{s(9):.2f}" fill="{GRID}" stroke="{I["secondary"]}" '
             f'stroke-width="{s(1.2):.2f}"/>')
    o.append(angle_arc(s, px_, py_, s(34), 90, 90 - 22))
    o.append(lab(s, px_ + s(5), py_ + s(48), it("θ"), "label2"))
    o.append(H.arrow(s, p, bob[0], bob[1] + s(10), bob[0], bob[1] + s(46), "load"))
    o.append(lab(s, bob[0] + s(7), bob[1] + s(42), it("Mg"), "label2"))
    o.append(arc_arrow(s, p, px_, py_, Lp + s(16), 90 - 30, 90 - 6, "force"))
    o.append(lines(s, 392, 314, ["hanging pendulum:", f'−{it("Mgℓ")} sin {it("θ")} pulls back'], anchor="end"))
    o.append(credit(s, VB))
    aria = ("Left: a skeleton (Lynch art) leaning 10 degrees forward as one rigid segment hinged at the ankle O. The "
            "line from O to the centre of mass has length l = 0.9 m at angle theta from the vertical, so the weight Mg "
            "has the horizontal moment arm l sin theta about O; a red curved arrow at the ankle is the restoring "
            "ankle torque tau. Euler's law about O gives I theta-double-dot = Mgl sin theta minus tau: the gravity term "
            "is positive and grows with theta, the destabilising term. Right: a hanging pendulum for contrast, whose "
            "gravity moment -Mgl sin theta pulls the bob back toward the vertical.")
    return finish(VB, aria, s, o)


# ================================================================ svg #37  D2 the saddle
def fig37():
    p = "m7f37_"
    VB, s = pvb(300)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    w = W0 * 1.0                                         # deg/s per deg
    pl = Plot(s, (52, 40, 236, 232), (-2, 2), (-7, 7))
    o.append(pl.axes([(v, mn(v)) for v in (-2, -1, 0, 1, 2)], [(v, mn(v)) for v in (-6, -3, 0, 3, 6)],
                     "lean θ (°)", "lean rate dθ/dt (°/s)", grid=(0,), ytx=13))
    o.append(H.line(s, pl.X(0), pl.Y(-7), pl.X(0), pl.Y(7), GRID, "leader"))
    # trajectories: (dθ/dt)² − ω0² θ² = c
    th = np.linspace(-2, 2, 161)
    for c in (2.5 ** 2, 5.0 ** 2):
        for sg in (1, -1):
            v = sg * np.sqrt(c + (w * th) ** 2)
            m = np.abs(v) <= 7
            o.append(pl.curve(th[m], v[m], I["rule"], multi=True, nmax=80))
    vv = np.linspace(-7, 7, 161)
    for c in (0.8, 1.6):
        for sg in (1, -1):
            t2 = sg * np.sqrt(c ** 2 + (vv / w) ** 2)
            m = np.abs(t2) <= 2
            o.append(pl.curve(t2[m], vv[m], I["rule"], multi=True, nmax=80))
    o.append(pl.curve(th, -w * th, SER[1], multi=True, dash=(6, 4)))
    o.append(pl.curve(th, w * th, SER[0], multi=True))
    for t0, sg in ((1.25, 1), (-1.25, -1)):
        o.append(H.arrow(s, p, pl.X(t0), pl.Y(w * t0), pl.X(t0 + sg * 0.3), pl.Y(w * (t0 + sg * 0.3)), "force"))
        o.append(H.arrow(s, p, pl.X(t0 + sg * 0.45), pl.Y(-w * (t0 + sg * 0.45)), pl.X(t0), pl.Y(-w * t0),
                         "geometry"))
    o.append(f'<circle cx="{pl.X(0):.2f}" cy="{pl.Y(0):.2f}" r="{s(4):.2f}" fill="{I["primary"]}"/>')
    o.append(legend(s, 12, 18, [(SER[0], "unstable, +ω₀θ", None), (SER[1], "stable, −ω₀θ", (6, 4)),
                                (I["rule"], "trajectory", None)], gap=22))
    # s-plane
    sp = Plot(s, (258, 96, 392, 156), (-5.5, 5.5), (-2, 2))
    y0 = sp.Y(0)
    o.append(H.line(s, sp.x0, y0, sp.x1, y0, I["axis"], "axis"))
    o.append(H.line(s, sp.X(0), sp.y1, sp.X(0), sp.y0, I["axis"], "axis"))
    o.append(plabel(s, sp.x1, y0 - s(5), "Re", "tick", I["secondary"], "end"))
    o.append(plabel(s, sp.X(0) + s(4), sp.y1 + s(8), "Im", "tick", I["secondary"]))
    o.append(sp.dot(-W0, 0, SER[1]))
    o.append(sp.dot(W0, 0, SER[0]))
    o.append(plabel(s, sp.X(-W0), y0 + s(20), f"−{W0:.2f}", "tick", anchor="middle"))
    o.append(plabel(s, sp.X(W0), y0 + s(20), f"+{W0:.2f}", "tick", anchor="middle"))
    o.append(lines(s, 258, 54, ["d²θ/dt² = ω₀²θ;", f"roots of {it('s')}² = ω₀² (s⁻¹):"]))
    o.append(lines(s, 258, 196, [f"{it('s')} = ±ω₀ = ±{W0:.2f} s⁻¹,", "real, opposite signs:", "a saddle;",
                                 f"τ{sub('c', s, 'label2')} = 1/ω₀ = {1 / W0:.2f} s"]))
    pts = [[pl.X(t), [pl.Y(w * t), pl.Y(-w * t)], f"θ {t:.2f}°: unstable {w * t:.2f}, stable {-w * t:.2f} °/s"]
           for t in np.linspace(-2, 2, 101)]
    pts2 = [[sp.X(-W0), sp.Y(0), f"s = −ω₀ = −{W0:.2f} 1/s: decaying mode"],
            [sp.X(W0), sp.Y(0), f"s = +ω₀ = +{W0:.2f} 1/s: growing mode"]]
    aria = ("Left: phase plane of the uncontrolled linearised body, lean angle theta against lean rate. Trajectories "
            "(grey) are hyperbolae; only states on the stable line dtheta/dt = -omega0 theta (blue, dashed) fall to "
            "upright, every other state leaves along the unstable line dtheta/dt = +omega0 theta (red). Right: the "
            "characteristic roots s = +-omega0 = +-3.06 per second on the real axis, real and of opposite sign: the "
            "upright equilibrium is a saddle, with growth rate 3.06 per second and toppling time 0.33 s.")
    return finish(VB, aria, s, o, extra=H.hover_attr([(pl.box, pts), (sp.box, pts2)]))


# ================================================================ svg #38  D3 the COP-COM law and its sign
X38, A38 = 0.06, 0.5                     # m, m/s^2: drawn COM offset and COM acceleration (design values)


def strip(s, x0, x1, lo, hi):
    """A cm scale for a magnified floor: returns X(cm)."""
    return lambda v: x0 + (v - lo) / (hi - lo) * (x1 - x0)  # noqa: E731


def bos_bar(s, X, y, ticks=True):
    o = [rect(s, X(-D_HEEL * 100), y - s(4), X(D_TOE * 100) - X(-D_HEEL * 100), s(8))]
    if ticks:
        for v, t in ((-D_HEEL * 100, "heel"), (0, "ankle"), (D_TOE * 100, "toe edge")):
            o.append(H.line(s, X(v), y + s(4), X(v), y + s(9), I["axis"], "leader"))
            o.append(plabel(s, X(v), y + s(22), t, "tick", I["secondary"], "middle"))
    return "".join(o)


def fig38():
    p = "m7f38_"
    VB, s = VBs(410)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 260.0, 330.0
    th = math.degrees(math.asin(X38 / ELL))
    body, J = lean(s, th, 26.0, fy, HF, p=p)
    ax, ay = J["ankle"]
    c = J["comT"]
    o.append(floor(s, 8, 150, fy))
    o.append(body)
    o.append(vline(s, c[0], c[1] + s(8), fy, O["dim"]))
    o.append(H.com_mark(s, *c))
    o.append(H.joint_centre(s, ax, ay))
    o.append(lab(s, c[0] - s(10), c[1] + s(4), "COM", "label2", anchor="end"))
    off = A38 / W0 ** 2 * 100                            # cm, Prop 3.3
    close(off, 5.34, 0.01)
    X = strip(s, 172, 388, -6, 14)
    o.append(lab(s, 172, 24, f'{xs("cop", s)} − {xs("com", s)} = −{it("a")}{sub("com", s)}/ω₀²'))
    o.append(lab(s, 172, 44, "(Prop. 3.3), ω₀ = 3.06 s⁻¹", "label2"))
    o.append(lab(s, 172, 64, "floor magnified, cm from the ankle", "label2", I["secondary"]))
    for k, (a, title) in enumerate(((A38, "speeding up"), (-A38, "braking"))):
        yb = 116 + k * 104
        xc, xp = X38 * 100, X38 * 100 - a / W0 ** 2 * 100
        o.append(lab(s, 172, yb - s(28), f'{title}: {it("a")}{sub("com", s, "label2")} = {mn(f"{a:+.1f}")} m/s²',
                     "label2"))
        o.append(bos_bar(s, X, yb))
        o.append(H.arrow(s, p, X(xc), yb - s(14), X(xc) + (s(30) if a > 0 else -s(30)), yb - s(14), "geometry"))
        o.append(H.com_mark(s, X(xc), yb))
        o.append(cop_mark(s, X(xp), yb))
        yd = yb + s(34)
        o.append(H.arrow(s, p, X(xc), yd, X(xp), yd, "dim"))
        o.append(lab(s, 388, yd + s(16), f"COP {off:.1f} cm {'behind' if a > 0 else 'ahead of'} the COM", "label2",
                     anchor="end"))
    o.append(lines(s, 172, 300, ["the COP sits opposite the COM’s", "acceleration: to push the COM",
                                 "forward, the COP goes behind it"]))
    o.append(credit(s, VB))
    aria = ("Left: a skeleton (Lynch art) leaning slightly forward about the ankle, its centre of mass 6 cm ahead of "
            "the ankle. Right: the floor under it magnified, from the heel edge (5 cm behind the ankle) to the toe edge "
            "(12 cm ahead), for two cases with the same COM position. Top: the COM speeding up forward at 0.5 m/s^2; "
            "the centre of pressure (blue cross-hair, ground force N) sits 5.3 cm behind the COM. Bottom: the COM "
            "braking at 0.5 m/s^2; the centre of pressure sits 5.3 cm ahead of it. Proposition 3.3, x_cop - x_com = "
            "-a_com / omega0^2 with omega0 = 3.06 per second: the COP is displaced opposite to the COM acceleration.")
    return finish(VB, aria, s, o)


# ================================================================ svg #39  D4 the extrapolated COM
V39 = (0.15, 0.25)                       # m/s, the two drawn COM velocities (design values)


def fig39():
    p = "m7f39_"
    VB, s = VBs(610)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 220.0, 250.0
    th = math.degrees(math.asin(X38 / ELL))
    body, J = lean(s, th, 40.0, fy, HF, p=p)
    c = J["comT"]
    o.append(floor(s, 8, 150, fy))
    o.append(body)
    o.append(H.com_mark(s, *c))
    o.append(H.arrow(s, p, c[0] + s(9), c[1], c[0] + s(48), c[1], "geometry"))
    o.append(lab(s, c[0] + s(52), c[1] + s(4), it("v"), "label2"))
    o.append(lab(s, 166, 26, f'ξ = {xs("com", s)} + {it("v")}/ω₀'))
    o.append(lines(s, 166, 48, ["ω₀ = 3.06 s⁻¹ (Prop. 4.2):", f'd{it("ξ")}/d{it("t")} = ω₀(ξ − {xs("cop", s, "label2")}).',
                                "ξ runs away from the COP unless", "the COP sits on it, which it can",
                                "only inside the base: captured", "if and only if ξ ∈ BoS"]))
    o.append(lines(s, 166, 170, [f'drawn: {xs("com", s, "label2")} = {X38 * 100:.0f} cm and',
                                 f'{it("v")} = {V39[0]:.2f} (A) or {V39[1]:.2f} m/s (B)']))
    # magnified floor
    X = strip(s, 30, 380, -6, 24)
    yb = 330.0
    o.append(lab(s, 30, 276, "floor magnified, cm from the ankle", "label2", I["secondary"]))
    hc, tcm = (J["heel"][0] - J["ankle"][0]) / cmu(J), (J["toe"][0] - J["ankle"][0]) / cmu(J)    # cm from the ankle
    o.append(H.line(s, J["heel"][0], fy + s(3), X(hc), 262, I["rule"], "leader"))
    o.append(H.line(s, J["toe"][0], fy + s(3), X(tcm), 262, I["rule"], "leader"))
    o.append(bos_bar(s, X, yb))
    xc = X38 * 100
    xi = [xc + v / W0 * 100 for v in V39]
    for k, (v, x_) in enumerate(zip(V39, xi)):
        yy = yb - s(16) - k * s(20)
        o.append(H.arrow(s, p, X(xc), yy, X(x_), yy, "geometry"))
        o.append(lab(s, X(xc) - s(8), yy + s(4), f"{'AB'[k]}: {it('v')}/ω₀ = {v / W0 * 100:.1f} cm", "label2",
                     anchor="end"))
        o.append(lab(s, X(x_) + s(10), yy + s(4), f"ξ{sub('AB'[k], s, 'label2')} = {x_:.1f} cm", "label2"))
    o.append(H.com_mark(s, X(xc), yb))
    for k, x_ in enumerate(xi):
        o.append(xcom_mark(s, X(x_), yb))
    # xi(t): A captured (COP placed on xi), B beyond the toe (COP pinned at the toe edge)
    t = np.linspace(0, 0.8, 161)
    xa = np.full_like(t, xi[0])
    xb = D_TOE * 100 + (xi[1] - D_TOE * 100) * np.exp(W0 * t)
    pl = Plot(s, (62, 412, 386, 520), (0, 0.8), (-5, 40))
    o.append(f'<rect x="{pl.x0:.2f}" y="{pl.Y(D_TOE * 100):.2f}" width="{pl.x1 - pl.x0:.2f}" '
             f'height="{pl.Y(-D_HEEL * 100) - pl.Y(D_TOE * 100):.2f}" fill="{BOX}"/>')
    o.append(pl.axes([(v, f"{v:g}") for v in (0, 0.2, 0.4, 0.6, 0.8)], [(v, mn(v)) for v in (0, 12, 20, 40)],
                     "time (s)", "ξ (cm)", grid=(20, 40), ytx=26))
    o.append(pl.curve(t, xa, SER[1], multi=True))
    o.append(pl.curve(t, xb, SER[0], multi=True))
    o.append(plabel(s, pl.X(0.02), pl.Y(-1.5), "base of support", "label2", I["secondary"]))
    o.append(plabel(s, pl.X(0.5), pl.Y(xi[0]) - s(6), "A: COP on ξ, captured", "label2"))
    o.append(plabel(s, pl.X(0.6), pl.Y(34), "B: COP pinned at", "label2", anchor="end"))
    o.append(plabel(s, pl.X(0.6), pl.Y(34) + s(15), "the toe, ξ runs off", "label2", anchor="end"))
    o.append(legend(s, 62, 400, [(SER[1], f"A, {it('v')} = {V39[0]:.2f} m/s", None),
                                 (SER[0], f"B, {it('v')} = {V39[1]:.2f} m/s", None)]))
    close(xb[-1], D_TOE * 100 + (xi[1] - D_TOE * 100) * math.exp(W0 * 0.8), 1e-9)
    pts = [[pl.X(t[i]), [pl.Y(xa[i]), pl.Y(min(xb[i], 40))], f"t {t[i]:.2f} s: ξ A {xa[i]:.1f} cm, ξ B {xb[i]:.1f} cm"]
           for i in range(len(t))]
    o.append(credit(s, VB))
    aria = ("Top: a skeleton (Lynch art) leaning slightly forward, its centre of mass 6 cm ahead of the ankle and "
            "moving forward at speed v. The extrapolated centre of mass xi = x_com + v/omega0 (omega0 = 3.06 per "
            "second) obeys dxi/dt = omega0 (xi - x_cop). Middle: the floor magnified; at v = 0.15 m/s xi lies 10.9 cm "
            "ahead of the ankle, inside the base of support that ends at the toe edge, 12 cm ahead; at v = 0.25 m/s it "
            "lies at 14.2 cm, beyond it. Bottom: xi against time. A (blue): the COP is placed on xi and xi stays put: "
            "captured. B (red): the COP is pinned at the toe edge and xi runs away exponentially at rate omega0.")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ svg #40  D5 delay-free PD stability
EX40 = ((900.0, 120.0), (400.0, 120.0), (900.0, -60.0))    # example gains (N m/rad, N m s/rad): design values


def roots(kp, kd):
    """Roots of I s^2 + Kd s + (Kp - Mgl) = 0 (Prop 5.1)."""
    return np.roots([I_A, kd, kp - MGL])


def fig40():
    p = "m7f40_"
    VB, s = pvb(330)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    pl = Plot(s, (66, 72, 372, 262), (0, 1500), (-100, 300))
    x0, y0, x1, y1 = pl.X(MGL), pl.Y(300), pl.X(1500), pl.Y(0)
    o.append(f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}" fill="{O["neural"]}" '
             f'fill-opacity="0.09"/>')
    o.append(pl.axes([(v, f"{v:g}") for v in (0, 500, 1000, 1500)], [(v, mn(v)) for v in (-100, 0, 100, 200, 300)],
                     f'{it("K")}{sub("p", s)} (N·m/rad)', f'{it("K")}{sub("d", s)} (N·m·s/rad)', grid=(100, 200, 300),
                     ytx=14))
    o.append(H.line(s, pl.x0, pl.Y(0), pl.x1, pl.Y(0), I["axis"], "leader"))
    o.append(H.line(s, x0, pl.y1, x0, pl.y0, I["secondary"], "ref", H.DASH_REF))
    o.append(plabel(s, x0 + s(5), pl.y1 - s(4), f"Mgℓ = {MGL:.0f}", "label2"))
    txt = []
    for (kp, kd), col in zip(EX40, (SER[1], SER[0], SER[2])):
        r = roots(kp, kd)
        o.append(pl.dot(kp, kd, col))
        if abs(r[0].imag) > 1e-9:
            txt.append(f"{r[0].real:+.2f} ± {abs(r[0].imag):.2f}i".replace("-", "−"))
        else:
            txt.append(f"s₊ = {max(r.real):+.2f}".replace("-", "−"))
    re0 = roots(*EX40[0])[0].real
    close(re0, -KD / (2 * I_A), 1e-9)
    o.append(plabel(s, pl.X(900) + s(8), pl.Y(120) - s(8), "stable: s =", "label2"))
    o.append(plabel(s, pl.X(900) + s(8), pl.Y(120) + s(7), txt[0], "label2"))
    o.append(plabel(s, pl.X(400) - s(8), pl.Y(120) - s(8), "falls: real", "label2", anchor="end"))
    o.append(plabel(s, pl.X(400) - s(8), pl.Y(120) + s(7), f"root {txt[1]}", "label2", anchor="end"))
    o.append(plabel(s, pl.X(900) + s(8), pl.Y(-60) - s(3), "growing sway:", "label2"))
    o.append(plabel(s, pl.X(900) + s(8), pl.Y(-60) + s(12), f"s = {txt[2]}", "label2"))
    o.append(plabel(s, pl.X(1480), pl.Y(270), "stable quadrant", "label2", anchor="end"))
    o.append(plabel(s, 12, 20, f'closed loop {it("I")}{it("s")}² + {it("K")}{sub("d", s, "label2")}{it("s")} + '
                    f'({it("K")}{sub("p", s, "label2")} − Mgℓ) = 0: both roots in the', "label2"))
    o.append(plabel(s, 12, 20 + s(17), f'left half-plane iff {it("K")}{sub("d", s, "label2")} &gt; 0 and '
                    f'{it("K")}{sub("p", s, "label2")} &gt; Mgℓ (Routh–Hurwitz)', "label2"))
    pts = []
    for kp in np.linspace(0, 1500, 121):
        t_ = (f"Kp {kp:.0f} N·m/rad: stable iff Kd &gt; 0" if kp > MGL else
              f"Kp {kp:.0f} N·m/rad: below Mgl, falls for every Kd")
        pts.append([pl.X(kp), pl.Y(0), t_.replace("&gt;", ">")])
    aria = ("Plane of the proportional gain K_p (horizontal) and the derivative gain K_d (vertical) for the delay-free "
            "closed loop I s^2 + K_d s + (K_p - Mgl) = 0. The shaded quadrant K_p > Mgl = 618 N m/rad (dashed line), "
            "K_d > 0 is stable. Three example points: (900, 120), blue, roots -0.91 +- 1.86i, stable; (400, 120), red, "
            "a real root +1.12 per second, the body falls; (900, -60), orange, roots +0.45 +- 2.02i, a growing sway.")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ svg #41  D6 s = i omega: the phasor picture
def fig41():
    p = "m7f41_"
    VB, s = pvb(300)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    A = I_A * WC ** 2 + MGL                             # N m/rad
    ph = WC * DCRIT                                     # rad
    kdw = KD * WC
    close(A * math.cos(ph), KP, 1e-6)                   # Prop 6.2, real part
    close(A * math.sin(ph), kdw, 1e-6)                  # Prop 6.2, imaginary part
    k = 0.33                                            # px per N m/rad, the same on both axes
    ox, oy = 40.0, 222.0
    P = lambda re, im: (ox + k * re, oy - k * im)       # noqa: E731
    o.append(H.line(s, 16, oy, 394, oy, I["axis"], "axis"))
    o.append(H.line(s, ox, oy + 12, ox, 124, I["axis"], "axis"))
    o.append(plabel(s, 394, oy - s(6), "Re", "tick", I["secondary"], "end"))
    o.append(plabel(s, ox + s(5), 132, "Im", "tick", I["secondary"]))
    kt, at = P(KP, kdw), P(A, 0)
    o.append(H.line(s, kt[0], kt[1] + s(6), kt[0], oy, O["dim"], "ref", H.DASH_REF))
    o.append(H.arrow(s, p, ox, oy, *at, "reaction"))
    o.append(H.arrow(s, p, ox, oy, *kt, "geometry"))
    # the rotation e^(-i omega Delta) that carries the gain phasor onto the real axis
    o.append(arc_arrow(s, p, ox, oy, k * A, -math.degrees(ph) + 1.5, -1.0, "dim"))
    o.append(angle_arc(s, ox, oy, s(118), 0, -math.degrees(ph)))
    o.append(lab(s, ox + s(124), oy - s(9), f"ω{it('Δ')} = {math.degrees(ph):.1f}°", "label2"))
    o.append(lab(s, 178, 164, f'{it("K")}{sub("p", s, "label2")} + {it("iK")}{sub("d", s, "label2")}ω', "label2",
                 anchor="middle", extra=f'transform="rotate({-math.degrees(ph):.2f} 178 164)"'))
    o.append(lab(s, kt[0] - s(6), (kt[1] + oy) / 2 + s(4), f'{it("K")}{sub("d", s, "label2")}ω = {kdw:.0f}', "label2",
                 anchor="end"))
    o.append(lab(s, 392, kt[1] - s(10), f"× e{sup('−iωΔ', s)} turns it back", "label2", anchor="end"))
    for yy, xe, t_ in ((oy + s(20), kt[0], f'{it("K")}{sub("p", s, "label2")} = {KP:.0f}'),
                       (oy + s(44), at[0], f'{it("I")}ω² + Mgℓ = {A:.0f}')):
        o.append(H.arrow(s, p, ox, yy, xe, yy, "dim", both=True))
        o.append(H.line(s, xe, oy + s(3), xe, yy + s(4), I["rule"], "leader"))
        o.append(lab(s, (ox + xe) / 2, yy - s(4), t_, "label2", anchor="middle"))
    o.append(lines(s, 12, 22, [f'{it("s")} = iω in {it("I")}{it("s")}² − Mgℓ + ({it("K")}{sub("p", s, "label2")} + '
                               f'{it("K")}{sub("d", s, "label2")}{it("s")})e{sup("−sΔ", s)} = 0 gives',
                               f'({it("K")}{sub("p", s, "label2")} + i{it("K")}{sub("d", s, "label2")}ω) '
                               f'e{sup("−iωΔ", s)} = {it("I")}ω² + Mgℓ, a positive real number:',
                               f'real part: {it("K")}{sub("p", s, "label2")} = ({it("I")}ω² + Mgℓ) cos ω{it("Δ")}',
                               f'imaginary part: {it("K")}{sub("d", s, "label2")}ω = ({it("I")}ω² + Mgℓ) '
                               f'sin ω{it("Δ")}']))
    o.append(lab(s, 392, 292, f"drawn at {it('K')}{sub('p', s, 'tick')} = 900, {it('K')}{sub('d', s, 'tick')} = 120: "
                 f"ω = {WC:.2f} s⁻¹, {it('Δ')} = {DCRIT:.3f} s (N·m/rad)", "tick", I["secondary"], "end"))
    aria = ("Complex-plane picture of the oscillatory stability boundary. With s = i omega the characteristic equation "
            "reads (K_p + i K_d omega) e^(-i omega Delta) = I omega^2 + Mgl, a positive real number. The gain phasor "
            "K_p + i K_d omega (blue) has the same length as I omega^2 + Mgl (black, on the real axis) and the delay "
            "turns it back by the angle omega Delta onto the real axis. Its real projection is K_p = (I omega^2 + Mgl) "
            f"cos omega Delta and its imaginary projection K_d omega = (I omega^2 + Mgl) sin omega Delta. Drawn at "
            f"K_p = 900, K_d = 120 N m/rad: omega = {WC:.2f} per second, Delta = {DCRIT:.3f} s, omega Delta = "
            f"{math.degrees(ph):.1f} degrees, K_d omega = {kdw:.0f}, I omega^2 + Mgl = {A:.0f}.")
    return finish(VB, aria, s, o)


# ================================================================ svg #42  D7 the crossing frequency
def fig42():
    p = "m7f42_"
    VB, s = pvb(350)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    pl = Plot(s, (66, 44, 386, 214), (0, 3.5), (500, 1300))
    o.append(pl.axes([(v, f"{v:g}") for v in (0, 1, 2, 3)], [(v, f"{v:g}") for v in (600, 800, 1000, 1200)],
                     "crossing frequency ω (s⁻¹)", "N·m/rad", grid=(600, 800, 1000, 1200), ytx=14))
    w = np.linspace(0, 3.5, 351)
    gk = np.sqrt(KP ** 2 + (KD * w) ** 2)
    ga = I_A * w ** 2 + MGL
    m = ga <= 1300
    o.append(pl.curve(w, gk, SER[1], multi=True))
    o.append(pl.curve(w[m], ga[m], SER[0], multi=True))
    A = I_A * WC ** 2 + MGL
    close(A, math.hypot(KP, KD * WC), 1e-6)
    o.append(H.line(s, pl.X(WC), pl.Y(A) + s(6), pl.X(WC), pl.y0, I["secondary"], "ref", H.DASH_REF))
    o.append(pl.dot(WC, A, O["flag"]))
    o.append(plabel(s, pl.X(WC) + s(8), pl.Y(A) + s(16), f"ω{sub('c', s, 'label2')} = {WC:.2f} s⁻¹", "label2"))
    o.append(plabel(s, pl.X(WC) + s(8), pl.Y(A) + s(31), f"f{sub('c', s, 'label2')} = {WC / (2 * math.pi):.2f} Hz",
                    "label2"))
    o.append(plabel(s, pl.X(0.08), pl.Y(966), f"|{it('K')}{sub('p', s, 'label2')} + i{it('K')}{sub('d', s, 'label2')}ω|",
                    "label2"))
    o.append(plabel(s, pl.X(0.5), pl.Y(560), f"{it('I')}ω² + Mgℓ", "label2"))
    o.append(legend(s, 66, 22, [(SER[1], "gain magnitude", None), (SER[0], "plant term Iω² + Mgℓ", None)]))
    kp, kd = f'{it("K")}{sub("p", s, "label2")}', f'{it("K")}{sub("d", s, "label2")}'
    wc = f'ω{sub("c", s, "label2")}'
    o.append(lines(s, 12, 282, [f'square and add: {kp}² + {kd}²ω² = ({it("I")}ω² + Mgℓ)², that is',
                                f'{it("I")}²ω⁴ + (2{it("I")}Mgℓ − {kd}²)ω² + (Mgℓ)² − {kp}² = 0: no Δ;',
                                f'then Δ{sub("crit", s, "label2")} = arctan({kd}{wc}/{kp})/{wc} = {DCRIT:.3f} s',
                                f'({kp} = 900, {kd} = 120, {it("I")} = 66, Mgℓ = 618)']))
    pts = [[pl.X(w[i]), [pl.Y(gk[i]), pl.Y(min(ga[i], 1300))],
            f"ω {w[i]:.2f} 1/s: |Kp + iKdω| {gk[i]:.0f}, Iω² + Mgl {ga[i]:.0f} N·m/rad"] for i in range(0, len(w), 3)]
    aria = ("Two curves against frequency omega: the gain magnitude sqrt(K_p^2 + K_d^2 omega^2) (blue) and the plant "
            "term I omega^2 + Mgl (red), at K_p = 900 and K_d = 120. Squaring and adding the two boundary equations "
            "removes the delay: the crossing frequency is where the two curves meet, omega_c = 2.20 per second "
            "(f_c = 0.35 Hz, orange point), the positive root of the quartic I^2 omega^4 + (2 I Mgl - K_d^2) omega^2 + "
            "(Mgl)^2 - K_p^2 = 0. The delay is then recovered as Delta_crit = arctan(K_d omega_c / K_p) / omega_c = "
            "0.130 s.")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ svg #43  D8 ankle-torque saturation
def foot_only(P):
    Q = LB.Pose("lat")
    Q.__dict__.update(P.__dict__)
    Q.segs = [g for g in P.segs if g[0] == "lat_foot" and not g[5]]
    return Q


def fig43():
    p = "m7f43_"
    VB, s = VBs(560)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 250.0, 300.0
    th = math.degrees(math.asin(D_TOE / ELL))            # static limit: the COM over the toe edge
    body, J = lean(s, th, 22.0, fy, HF, p=p)
    c = J["comT"]
    o.append(floor(s, 8, 136, fy))
    o.append(body)
    o.append(vline(s, c[0], c[1] + s(8), fy, O["dim"]))
    o.append(H.com_mark(s, *c))
    o.append(H.arrow(s, p, c[0] + s(14), c[1] + s(4), c[0] + s(14), c[1] + s(56), "load"))
    o.append(lab(s, c[0] + s(20), c[1] + s(50), it("Mg"), "label2"))
    zx0, zy0, zx1, zy1 = J["heel"][0] - s(4), fy - s(14), J["toe"][0] + s(4), fy + s(3)
    o.append(f'<rect x="{zx0:.2f}" y="{zy0:.2f}" width="{zx1 - zx0:.2f}" height="{zy1 - zy0:.2f}" fill="none" '
             f'stroke="{I["rule"]}" stroke-width="{s(1):.2f}"/>')
    # enlarged foot bones; the plot below shares its horizontal scale
    Q = foot_only(LB.pose())
    HB, fy2 = 1330.0, 236.0
    _, J0 = LB.draw(p, s, Q, 0, 0, HB)
    xa = 214.0
    footb, JF = LB.draw(p, s, Q, xa - (J0["ankle"][0] - J0["heel"][0]), fy2, HB)
    cmb = cmu(JF)
    ax, ay = JF["ankle"]
    X = lambda v: ax + v * cmb                           # noqa: E731  (cm from the ankle)
    o.append(H.line(s, zx1, zy0, JF["heel"][0] - s(4), JF["bbox"][1], I["rule"], "leader"))
    o.append(H.line(s, zx1, zy1, JF["heel"][0] - s(4), fy2 + s(3), I["rule"], "leader"))
    o.append(floor(s, JF["heel"][0] - s(12), 396, fy2))
    o.append(footb)
    o.append(H.joint_centre(s, ax, ay))
    o.append(lab(s, ax - s(32), ay + s(10), "ankle", "label2", anchor="end"))
    for v in (-D_HEEL * 100, D_TOE * 100):
        o.append(H.line(s, X(v), fy2 - s(10), X(v), fy2 + s(30), I["axis"], "axis"))
    o.append(H.arrow(s, p, X(D_TOE * 100), fy2 + s(46), X(D_TOE * 100), fy2 + s(7), "reaction"))
    o.append(cop_mark(s, X(D_TOE * 100), fy2))
    o.append(lab(s, X(D_TOE * 100) + s(7), fy2 + s(42), f'{it("N")} ≈ {it("Mg")}', "label2"))
    o.append(arc_arrow(s, p, ax, ay, s(30), -20, -150, "force"))
    o.append(lab(s, ax + s(14), ay - s(36), f'{it("τ")}{sub("max", s, "label2")}', "label2"))
    yd = fy2 + s(20)
    o.append(H.arrow(s, p, X(0), yd, X(D_TOE * 100), yd, "geometry", both=True))
    o.append(H.arrow(s, p, X(-D_HEEL * 100), yd, X(0), yd, "geometry", both=True))
    o.append(ext(s, X(0), ay + s(8), X(0), yd + s(5)))
    o.append(lab(s, (X(0) + X(D_TOE * 100)) / 2, yd + s(16), f'{it("d")}{sub("toe", s, "label2")} = 0.12 m', "label2",
                 anchor="middle"))
    o.append(lab(s, X(-D_HEEL * 100) - s(4), yd + s(16), f'{it("d")}{sub("heel", s, "label2")} = 0.05 m', "label2",
                 anchor="end"))
    # torque against COP position: linear inside the foot, impossible outside
    lo, hi = -6.0, (396 - ax) / cmb
    pl = Plot(s, (X(lo), 324, X(hi), 452), (lo, hi), (-60, 100))
    for a_, b_ in ((lo, -D_HEEL * 100), (D_TOE * 100, hi)):
        o.append(f'<rect x="{pl.X(a_):.2f}" y="{pl.y1:.2f}" width="{pl.X(b_) - pl.X(a_):.2f}" '
                 f'height="{pl.y0 - pl.y1:.2f}" fill="{GRID}" fill-opacity="0.6"/>')
    o.append(pl.axes([(v, mn(v)) for v in (-5, 0, 5, 10, 15, 20) if lo <= v <= hi],
                     [(v, mn(v)) for v in (-50, 0, 50, 100)], "COP position from the ankle (cm)", "", grid=(0,)))
    o.append(plabel(s, pl.x0 - s(36), pl.y1 - s(8), f'{it("τ")} (N·m)', "label2"))
    xx = np.linspace(-D_HEEL * 100, D_TOE * 100, 120)
    tau = MGN * xx / 100
    o.append(pl.curve(xx, tau, SER[0]))
    tmax, tmin = MGN * D_TOE, -MGN * D_HEEL
    o.append(pl.dot(D_TOE * 100, tmax, SER[0]))
    o.append(pl.dot(-D_HEEL * 100, tmin, SER[0]))
    o.append(plabel(s, pl.X(D_TOE * 100) + s(7), pl.Y(tmax) + s(4), f"{tmax:.0f} N·m", "label2"))
    o.append(plabel(s, pl.X(-D_HEEL * 100) + s(8), pl.Y(tmin) + s(15), f"{mn(f'{tmin:.0f}')} N·m", "label2"))
    o.append(plabel(s, pl.X(17.5), pl.Y(30), "COP cannot", "label2", I["secondary"], "middle"))
    o.append(plabel(s, pl.X(17.5), pl.Y(30) + s(15), "go here", "label2", I["secondary"], "middle"))
    o.append(lines(s, 150, 24, [f'{it("τ")} = {it("Mg")}({it("x")}{sub("cop", s, "label2")} − '
                                f'{it("x")}{sub("ankle", s, "label2")}) and the COP stays',
                                f'in the foot: |{it("τ")}| ≤ {it("Mg")}·{it("d")}{sub("foot", s, "label2")}',
                                f'forward: {it("Mg")} × 0.12 m = {tmax:.0f} N·m',
                                f'backward: {it("Mg")} × 0.05 m = {-tmin:.0f} N·m',
                                f'({it("M")} = 70 kg, {it("g")} = 9.81 m/s²)']))
    o.append(lines(s, 8, 352, ["drawn at the static", "limit: COM over the", f"toe edge, lean {th:.1f}°"]))
    pts = [[pl.X(v), pl.Y(t_), f"COP {v:.1f} cm ahead of the ankle: τ = {t_:.1f} N·m".replace("-", "−")]
           for v, t_ in zip(xx, tau)]
    o.append(credit(s, VB))
    aria = ("Left: a skeleton (Lynch art) leaning 7.7 degrees forward, the static limit at which its centre of mass is "
            "over the toe edge. Right: the foot bones enlarged. The centre of pressure (blue cross-hair), where the "
            "ground force N ~ Mg acts, can move from the heel edge, 0.05 m behind the ankle, to the toe edge, 0.12 m "
            "ahead. Below, on the same horizontal scale: the ankle torque tau = Mg (x_cop - x_ankle) is a straight "
            f"line in the COP position that stops at the edges of the foot (grey: the COP cannot go there), so "
            f"|tau| <= Mg d_foot: {tmax:.0f} N m forward (Mg x 0.12 m, M = 70 kg) and {-tmin:.0f} N m backward.")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ svg #44  D9 angular momentum about the COM
TRUNK44 = 40.0                           # deg, trunk flexed at the hip (design value)
A44 = 1.0                                # m/s^2, the braking deceleration of the worked line (design value)


def pose44(lean_):
    return LB.pose(pelvis=lean_ + TRUNK44, near=dict(hip=TRUNK44, shoulder=20, elbow=10),
                   far=dict(hip=TRUNK44, shoulder=20, elbow=10))


def fig44():
    p = "m7f44_"
    VB, s = VBs(500)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 300.0, 386.0

    def gap(lean_):
        _, Jq = LB.draw(p, s, pose44(lean_), 0, 0, HF)
        return Jq["com"][0] - (Jq["ankle"][0] + D_TOE * 100 * cmu(Jq))
    ln = bisect(gap, -20.0, 20.0)
    P = pose44(ln)
    _, J0 = LB.draw(p, s, P, 0, 0, HF)
    body, J = LB.draw(p, s, P, 150.0 - (J0["ankle"][0] - J0["heel"][0]), fy, HF)
    c = J["com"]
    xcop = J["ankle"][0] + D_TOE * 100 * cmu(J)
    close(c[0], xcop, 1e-3)
    h_com = (fy - c[1]) / cmu(J) / 100                    # m
    H_ = -M * A44                                         # N, Newton: H = M a_com
    Ldot = H_ * h_com                                     # N m, with the COM over the pinned COP
    o.append(floor(s, 8, 392, fy))
    o.append(body)
    o.append(vline(s, c[0], c[1] + s(8), fy, O["dim"]))
    o.append(H.com_mark(s, *c))
    o.append(arc_arrow(s, p, c[0], c[1], s(38), -150, -40, "force"))
    o.append(lines(s, 10, c[1] - s(58), ["trunk pitches forward:", f"d{it('L')}{sub('G', s, 'label2')}/d{it('t')} &lt; 0"]))
    o.append(H.arrow(s, p, xcop, fy + s(44), xcop, fy + s(7), "reaction"))
    o.append(cop_mark(s, xcop, fy))
    o.append(lab(s, xcop + s(7), fy + s(38), f'{it("N")}, at the COP pinned at the toe edge', "label2"))
    o.append(H.arrow(s, p, xcop - s(8), fy - s(6), xcop - s(58), fy - s(6), "reaction"))
    o.append(lab(s, xcop - s(60), fy - s(12), f'{it("H")} &lt; 0', "label2", anchor="end"))
    xh = c[0] + s(70)
    o.append(ext(s, c[0] + s(8), c[1], xh + s(5), c[1]))
    o.append(H.arrow(s, p, xh, fy, xh, c[1], "geometry", both=True))
    o.append(lab(s, xh + s(6), (fy + c[1]) / 2, f'{it("h")}{sub("com", s, "label2")} = {h_com:.2f} m', "label2"))
    G_, sc, cp, cm_ = sub("G", s, "label2"), sub("com", s, "label2"), sub("cop", s, "label2"), sub("com", s, "label2")
    dL = f'd{it("L")}{G_}/d{it("t")}'
    o.append(lines(s, 10, 22, ["Euler’s law about the COM (counter-clockwise +,",
                               f'{it("H")} forward +): {dL} = {it("N")}({it("x")}{cp} − {it("x")}{cm_}) + '
                               f'{it("Hh")}{sc},',
                               f'and Newton: {it("H")} = {it("Ma")}{sc}. With the COM over the',
                               f'pinned COP the {it("N")} term is zero, so a braking {it("H")} &lt; 0',
                               f'needs {dL} = {it("Hh")}{sc} &lt; 0. At {A44:.0f} m/s²: {it("H")} = {mn(f"{H_:.0f}")} N,',
                               f'{dL} = {mn(f"{Ldot:.0f}")} N·m.']))
    o.append(credit(s, VB))
    aria = ("Side view of a skeleton (Lynch art) in the hip strategy: legs leaning, trunk flexed 40 degrees at the hip, "
            "the centre of mass over the centre of pressure, which is pinned at the toe edge, 0.12 m ahead of the ankle. "
            "The ground force has a vertical part N at the COP and a horizontal shear H at the floor, pointing backward; "
            f"the COM is h_com = {h_com:.2f} m above the floor. Euler's law about the COM, counter-clockwise positive and "
            "H positive forward: dL_G/dt = N (x_cop - x_com) + H h_com, with H = M a_com. With the COM over the pinned "
            "COP the N term is zero, so a backward braking shear needs dL_G/dt = H h_com < 0: the trunk pitches forward "
            f"(red arc). Braking at 1 m/s^2 gives H = {H_:.0f} N and dL_G/dt = {Ldot:.0f} N m.")
    return finish(VB, aria, s, o)


# ================================================================ svg #45  D10 flexed trunk about L5/S1
PHI45 = 45.0                             # deg, the drawn trunk flexion (design value)
CHORD0 = math.degrees(math.atan2(LB.LJ["neck"][0] - LB.LJ["l5s1"][0], LB.LJ["l5s1"][1] - LB.LJ["neck"][1]))


def lift(phi, pel):
    """Pelvis `pel` + lumbar flexion so the L5/S1-C7 chord is phi from vertical, knees straight.  Shoulder solved so
    the grip sits r_L sin(phi) ahead of L5/S1 (Prop 8.1's load arm); thigh solved so body (70 kg) + load (20 kg at
    the grip) is 0.04 m ahead of the ankle, over the mid-foot (the rule of body_main.lift_pose)."""
    tot = phi - CHORD0
    um = LB.H_U / 1.75

    def build(thigh, sh):
        P = LB.pose(pelvis=pel, trunk=tot - pel, near=dict(hip=pel - thigh, shoulder=sh),
                    far=dict(hip=pel - thigh, shoulder=sh))
        J = LB.draw("", None, P, 0, 0, LB.H_U)[1]
        return P, J, LB.lerp(J["wrist"], J["fingertip"], 0.5)

    def shoulder(thigh):
        return bisect(lambda sh: (build(thigh, sh)[2][0] - build(thigh, sh)[1]["l5s1"][0]) / um
                      - RL * math.sin(math.radians(phi)), 0.0, 140.0, 40)

    def com_err(thigh):
        P, J, g = build(thigh, shoulder(thigh))
        return ((M * J["com"][0] + ML * g[0]) / (M + ML) - J["ankle"][0]) / um - 0.04
    thigh = bisect(com_err, -40.0, 10.0, 30)
    return build(thigh, shoulder(thigh))[0]


def spine_terms(phi_deg):
    """Prop 8.2: muscle term M/d and axial weight term (N)."""
    ph = math.radians(phi_deg)
    return G * (MT * RT + ML * RL) * math.sin(ph) / DE, (MT + ML) * G * math.cos(ph)


def lift_overlay(s, p, J, phi, o, load_box=True):
    """L5/S1 joint, trunk COM, load, the two weights, F_e on d and F_spine; returns (l5, trunk COM, load centre)."""
    um = LB.H_U / 1.75 * J["scale"]
    l5 = J["l5s1"]
    ph = math.radians(phi)
    u, n = (math.sin(ph), -math.cos(ph)), (-math.cos(ph), -math.sin(ph))       # along the trunk; dorsal normal
    grip = LB.lerp(J["wrist"], J["fingertip"], 0.5)
    bw, bh = 0.24 * um, 0.16 * um
    o.insert(1, rect(s, grip[0] - bw / 2, grip[1] - s(3), bw, bh))
    tc = (l5[0] + RT * um * u[0], l5[1] + RT * um * u[1])
    ce = (l5[0] + 0.55 * um * u[0], l5[1] + 0.55 * um * u[1])
    o.append(ext(s, *l5, *ce))
    e0 = (l5[0] + DE * um * n[0] + s(62) * u[0], l5[1] + DE * um * n[1] + s(62) * u[1])
    e1 = (l5[0] + DE * um * n[0] + s(4) * u[0], l5[1] + DE * um * n[1] + s(4) * u[1])
    o.append(H.arrow(s, p, *e0, *e1, "force"))
    o.append(H.arrow(s, p, l5[0] - s(46) * u[0], l5[1] - s(46) * u[1], l5[0] - s(7) * u[0], l5[1] - s(7) * u[1],
                     "reaction"))
    o.append(H.joint_centre(s, *l5))
    o.append(H.com_mark(s, *tc))
    o.append(H.arrow(s, p, tc[0], tc[1] + s(8), tc[0], tc[1] + s(40), "load"))
    bc = (grip[0], grip[1] - s(3) + bh / 2)
    o.append(H.arrow(s, p, bc[0], bc[1], bc[0], bc[1] + s(42), "load"))
    return l5, tc, bc, u, n, e0, um


def fig45():
    p = "m7f45_"
    P = lift(PHI45, 30.0)
    HF = 330.0
    _, J0 = LB.draw(p, None, P, 0, 0, HF)
    fy = 26.0 - J0["bbox"][1]
    h = round(fy + 404)
    VB, s = VBs(h)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    body, J = LB.draw(p, s, P, 70.0 - J0["bbox"][0], fy, HF)
    o.append(floor(s, 8, 392, fy))
    o.append(body)
    l5, tc, bc, u, n, e0, um = lift_overlay(s, p, J, PHI45, o)
    o.append(vline(s, l5[0], l5[1] - s(8), l5[1] - 0.24 * um, O["dim"]))
    o.append(angle_arc(s, l5[0], l5[1], 0.17 * um, -90, -90 + PHI45))
    o.append(lab(s, l5[0] - s(6), l5[1] - 0.17 * um, f"{it('φ')} = {PHI45:.0f}°", "label2", anchor="end"))
    fe = (e0[0] + n[0] * s(10), e0[1] + n[1] * s(10))
    o.append(lab(s, fe[0], fe[1], f'{it("F")}{sub("e", s, "label2")}', "label2", anchor="end"))
    tail = (l5[0] - s(46) * u[0], l5[1] - s(46) * u[1])
    o.append(lab(s, tail[0] - s(4), tail[1] + s(14), f'{it("F")}{sub("spine", s, "label2")}', "label2", anchor="end"))
    o.append(lab(s, l5[0] - s(11), l5[1] + s(4), "L5/S1", "label2", anchor="end"))
    o.append(lab(s, tc[0] + s(6), tc[1] + s(36), f'{it("m")}{sub("t", s, "label2")}{it("g")}', "label2"))
    o.append(lab(s, bc[0] + s(6), bc[1] + s(38), f'{it("m")}{sub("L", s, "label2")}{it("g")}', "label2"))
    y1, y2 = fy + s(18), fy + s(42)
    for xx, yy in ((l5[0], l5[1] + s(8)), (tc[0], tc[1] + s(44)), (bc[0], bc[1] + s(46))):
        o.append(ext(s, xx, yy, xx, fy))
        o.append(H.line(s, xx, fy + s(4), xx, y2 + s(4), I["rule"], "leader"))
    o.append(H.arrow(s, p, l5[0], y1, tc[0], y1, "geometry", both=True))
    o.append(lab(s, tc[0] + s(5), y1 + s(4), f'{it("r")}{sub("t", s, "label2")} sin {it("φ")}', "label2"))
    o.append(H.arrow(s, p, l5[0], y2, bc[0], y2, "geometry", both=True))
    o.append(lab(s, bc[0] + s(5), y2 + s(4), f'{it("r")}{sub("L", s, "label2")} sin {it("φ")}', "label2"))
    m45, a45 = spine_terms(PHI45)
    Mo = m45 * DE
    mt_, ml_, rt_, rl_ = (sub(k, s, "label2") for k in ("t", "L", "t", "L"))
    o.append(lines(s, 10, fy + s(72), [
        f'{it("M")} = {it("g")}({it("m")}{mt_}{it("r")}{rt_} + {it("m")}{ml_}{it("r")}{rl_}) sin {it("φ")} = {Mo:.0f} N·m,'
        ' held by the', f'erector spinae on an arm {it("d")} = 0.05 m:',
        f'{it("F")}{sub("spine", s, "label2")} ≈ {it("M")}/{it("d")} + ({it("m")}{mt_} + {it("m")}{ml_}){it("g")} cos '
        f'{it("φ")} = {m45 / 1e3:.2f} + {a45 / 1e3:.2f} = {(m45 + a45) / 1e3:.2f} kN',
        f'at {it("φ")} = {PHI45:.0f}°: the muscle term is {m45 / a45:.1f} × the weight term']))
    # both terms against phi
    ph = np.linspace(0, 90, 181)
    tm = np.array([spine_terms(v)[0] for v in ph]) / 1e3
    ta = np.array([spine_terms(v)[1] for v in ph]) / 1e3
    pc = math.degrees(math.atan((MT + ML) * DE / (MT * RT + ML * RL)))
    close(spine_terms(pc)[0], spine_terms(pc)[1], 1e-6)
    close(spine_terms(90)[0] / 1e3, 3.6, 0.05)            # line 602
    pl = Plot(s, (62, fy + 190, 386, fy + 318), (0, 90), (0, 4))
    o.append(pl.axes([(v, f"{v:g}") for v in (0, 30, 45, 60, 90)], [(v, f"{v:g}") for v in (0, 1, 2, 3, 4)],
                     "trunk flexion φ (°)", "kN", grid=(1, 2, 3, 4), ytx=26))
    o.append(H.line(s, pl.x0, pl.Y(LIMIT / 1e3), pl.x1, pl.Y(LIMIT / 1e3), O["flag"], "ref", H.DASH_REF))
    o.append(pl.curve(ph, tm, SER[0], multi=True))
    o.append(pl.curve(ph, ta, SER[1], multi=True))
    o.append(pl.dot(PHI45, m45 / 1e3, SER[0]))
    o.append(pl.dot(PHI45, a45 / 1e3, SER[1]))
    o.append(pl.dot(pc, spine_terms(pc)[0] / 1e3, I["primary"]))
    o.append(plabel(s, pl.X(64), pl.Y(spine_terms(64)[0] / 1e3) + s(20), f'muscle {it("M")}/{it("d")}', "label2"))
    o.append(plabel(s, pl.X(55), pl.Y(spine_terms(55)[1] / 1e3) - s(8), "weight term", "label2"))
    o.append(plabel(s, pl.X(2), pl.Y(LIMIT / 1e3) - s(6), f"{LIMIT / 1e3:.1f} kN risk threshold", "label2"))
    o.append(H.line(s, pl.X(pc) + s(3), pl.Y(spine_terms(pc)[0] / 1e3) - s(4), pl.X(6), pl.Y(1.45), I["secondary"],
                    "leader"))
    o.append(plabel(s, pl.X(1), pl.Y(1.5) - s(2), f"equal at {pc:.1f}°", "label2"))
    o.append(legend(s, 62, fy + 178, [(SER[0], "muscle term", None), (SER[1], "weight term", None),
                                      (O["flag"], "risk line", H.DASH_REF)], gap=22))
    pts = [[pl.X(ph[i]), [pl.Y(tm[i]), pl.Y(ta[i])], f"φ {ph[i]:.1f}°: M/d {tm[i]:.2f} kN, weight {ta[i]:.2f} kN"]
           for i in range(len(ph))]
    o.append(credit(s, VB))
    aria = ("Top: a skeleton (Lynch art) with knees straight and the trunk flexed 45 degrees from the vertical about "
            "the L5/S1 joint, a box in the hands. The trunk weight m_t g acts at the trunk COM, r_t sin phi ahead of "
            "L5/S1, the load m_L g at the hands, r_L sin phi ahead; the erector spinae force F_e (red) pulls along the "
            "back on an arm d = 0.05 m; F_spine (black) presses along the spine. With m_t = 35 kg, r_t = 0.30 m, "
            f"m_L = 20 kg, r_L = 0.40 m: M = {Mo:.0f} N m, F_spine = {m45 / 1e3:.2f} kN + {a45 / 1e3:.2f} kN = "
            f"{(m45 + a45) / 1e3:.2f} kN. Bottom: the two compression terms against trunk flexion: the muscle term "
            f"M/d (red) exceeds the weight term (m_t + m_L) g cos phi (blue) at every angle above {pc:.1f} degrees "
            "and reaches 3.6 kN at 90 degrees, above the 3.4 kN risk threshold (orange dashed).")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ svg #55  K10 elasticities of spinal compression
def f_spine(mL, rL, mt):
    """Prop 8.2 at phi = 90 deg (the K10 solution, line 886)."""
    return G * (mt * RT + mL * rL) / DE


def elasticities(h=1e-4):
    base = (ML, RL, MT)
    F0 = f_spine(*base)
    out = []
    for i in range(3):
        up, dn = list(base), list(base)
        up[i] *= 1 + h
        dn[i] *= 1 - h
        out.append((f_spine(*up) - f_spine(*dn)) / (2 * h * F0))
    return out


def fig55():
    p = "m7f55_"
    VB, s = VBs(460)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    E = elasticities()
    tot = MT * RT + ML * RL
    close(E[0], ML * RL / tot, 1e-6)
    close(E[2], MT * RT / tot, 1e-6)
    close(E[0], 0.43, 0.005)                             # line 886
    close(E[2], 0.57, 0.005)                             # line 886
    close(MT * RT, 10.5, 1e-9)                           # line 886
    close(ML * RL, 8.0, 1e-9)                            # line 886
    P = lift(90.0, 55.0)
    HF, fy = 300.0, 300.0
    _, J0 = LB.draw(p, s, P, 0, 0, HF)
    body, J = LB.draw(p, s, P, 30.0 - J0["bbox"][0], fy, HF)
    o.append(floor(s, 8, 250, fy))
    o.append(body)
    l5, tc, bc, u, n, e0, um = lift_overlay(s, p, J, 90.0, o)
    o.append(lab(s, l5[0] - s(8), l5[1] + s(30), "L5/S1", "label2", anchor="end"))
    o.append(lab(s, e0[0] + s(4), e0[1] - s(6), f'{it("F")}{sub("e", s, "label2")}', "label2"))
    o.append(lab(s, l5[0] - s(28), l5[1] - s(8), f'{it("F")}{sub("spine", s, "label2")}', "label2", anchor="middle"))
    o.append(lab(s, tc[0] + s(6), tc[1] + s(36), f'{it("m")}{sub("t", s, "label2")}{it("g")}', "label2"))
    o.append(lab(s, bc[0] + s(6), bc[1] + s(38), f'{it("m")}{sub("L", s, "label2")}{it("g")}', "label2"))
    ytop = J["bbox"][1]
    r1, r2 = ytop - s(8), ytop - s(32)
    o.append(ext(s, l5[0], l5[1] - s(8), l5[0], r2 - s(5)))
    for xx in (tc[0], bc[0]):
        o.append(ext(s, xx, ytop + s(4), xx, r2 - s(5) if xx == bc[0] else r1 - s(5)))
    o.append(H.arrow(s, p, l5[0], r1, tc[0], r1, "geometry", both=True))
    o.append(H.arrow(s, p, l5[0], r2, bc[0], r2, "geometry", both=True))
    o.append(lab(s, l5[0] - s(5), r1 + s(4), f'{it("r")}{sub("t", s, "label2")} 0.30 m', "label2", anchor="end"))
    o.append(lab(s, l5[0] - s(5), r2 + s(4), f'{it("r")}{sub("L", s, "label2")} 0.40 m', "label2", anchor="end"))
    # elasticity bars
    pl = Plot(s, (286, 92, 392, 252), (0, 3), (0, 0.7))
    o.append(pl.axes([(0.5, ""), (1.5, ""), (2.5, "")], [(v, f"{v:g}") for v in (0, 0.2, 0.4, 0.6)], "", "", grid=(0.2, 0.4, 0.6)))
    pts = []
    names = [f'{it("m")}{sub("L", s, "tick")}', f'{it("r")}{sub("L", s, "tick")}', f'{it("m")}{sub("t", s, "tick")}']
    plain = ("load mass mL", "reach rL", "trunk mass mt")
    for i, e in enumerate(E):
        xc, bw = pl.X(0.5 + i), s(22)
        col = SER[0] if i == 2 else SER[1]
        o.append(f'<rect x="{xc - bw / 2:.2f}" y="{pl.Y(e):.2f}" width="{bw:.2f}" height="{pl.Y(0) - pl.Y(e):.2f}" '
                 f'fill="{col}"/>')
        o.append(plabel(s, xc, pl.Y(e) - s(5), f"{e:.2f}", "label2", anchor="middle"))
        o.append(plabel(s, xc, pl.y0 + s(19), names[i], "label2", anchor="middle"))
        pts.append([xc, pl.Y(e), f"{plain[i]}: elasticity {e:.3f}"])
    o.append(lines(s, 268, 24, ["elasticity of F:", "% change in F per", "% change in input"]))
    mt_, ml_, rt_, rl_ = (sub(k, s, "label2") for k in ("t", "L", "t", "L"))
    o.append(lines(s, 10, 340, [f'At {it("φ")} = 90°, {it("F")} = {it("g")}({it("m")}{mt_}{it("r")}{rt_} + {it("m")}{ml_}'
                                f'{it("r")}{rl_})/{it("d")} = {f_spine(ML, RL, MT) / 1e3:.2f} kN. Each elasticity is',
                                f'that term’s share of the moment: {it("m")}{ml_}{it("r")}{rl_} = {ML * RL:.1f} and '
                                f'{it("m")}{mt_}{it("r")}{rt_} = {MT * RT:.1f} kg·m,',
                                "so the trunk’s own weight moves F most (red bar;",
                                "blue: the two load inputs)."]))
    o.append(credit(s, VB))
    aria = ("Left: a skeleton (Lynch art) stoop-lifting with the trunk horizontal and a box in the hands; about the "
            "L5/S1 pivot the trunk weight acts r_t = 0.30 m ahead and the load r_L = 0.40 m ahead, and the erector "
            "spinae (red) pull on an arm of 0.05 m. Right: the elasticity of the spinal compression F = g (m_t r_t + "
            f"m_L r_L)/d = {f_spine(ML, RL, MT) / 1e3:.2f} kN with respect to load mass ({E[0]:.2f}), reach "
            f"({E[1]:.2f}) and trunk mass ({E[2]:.2f}), computed by central differences. Each elasticity is that "
            "input's share of the moment: m_L r_L = 8.0 against m_t r_t = 10.5 kg m, so the trunk mass (red bar) "
            "moves the compression most; the two load bars are blue.")
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


FIGS = {
    36: ("D1: From Euler's law about the ankle, derive the nonlinear e", fig36),
    37: ("D2: Linearise the equation of motion about upright and show ", fig37),
    38: ("D3: Derive the exact relationship between the centre of pres", fig38),
    39: ("D4 extrapolated centre of mass: a standing body modelled as ", fig39),
    40: ("D5: Close the loop with a PD controller and derive the exact", fig40),
    41: ("D6: Introduce the neural delay and derive the equations of t", fig41),
    42: ("D7: For fixed gains, eliminate the delay from the boundary e", fig42),
    43: ("D8 anatomical ankle saturation diagram. A standing body is s", fig43),
    44: ("D9: Taking angular momentum about the centre of mass, derive", fig44),
    45: ("D10 anatomical derivation diagram. A flexed trunk rotates ab", fig45),
    55: ("K10 anatomical spine loading diagram. A bent trunk rotates a", fig55),
}
