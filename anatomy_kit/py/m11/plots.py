"""Module 11 plots (group `plots`): main-text #9, #12, #16, #18 and problem figures #25 (C5), #35 (D5),
#41 (K1), #42 (K2), #48 (K8), #49 (K9), #50 (K10).

Every plotted number is computed here from the formula or the lab code module11.html states (line numbers of
module11.html in brackets); the printed values of the text are asserted where they are computed:
  Lab B   (lines 327-357)  two-link elbow torque of a wave, Prop 6.1 with the Appendix masses; theta1 = 100 deg,
          theta2 = -1.0 + 0.5 sin(2 pi f t); inertial peak 4.7, gravity peak 3.5, total 8.1 (1.5 Hz), 22.1 (3 Hz);
  Lab C   (lines 372-397)  F_g = (1 + s) L / (2 mu), s = 0.30, m = 0.5 kg, lift pulse 4 exp(-((t - 0.6)/0.12)^2);
          5.31 / 15.9 / 31.9 N per pad at mu = 0.6 / 0.2 / 0.1;
  Lab D   (lines 409-430)  Jacobian ellipses (D5): velocity = J on the unit circle, force = J^-T on it;
  K1      (line 537)       straight reach, N = 400, T = 0.6 s, start (0.10, -0.30), goal y = 0.10;
  K2      (line 541)       M22 A (2 pi f)^2 against m2 lc2 g, crossover 1.31 Hz;
  K8      (line 565)       true peak 9 m/s^2, predicted 1.5, s = 0.30, 70 ms reflex;
  K9      (line 569)       w = l1 l2 |sin th2| at r = 0.6 l_tot, l_tot = 0.75 m;
  K10     (line 573)       pinch 2 mu F_g, power 2 mu F_g exp(mu beta), F_g = 30 N, beta = pi.
The whole bodies (seated person) are the Lynch body kit (lynch_body.py); m11/body_main.py puts the defs on the page,
this group only <use>s them.  Pose angles, stature and the chair are design values (marked in the code).
"""
import html
import math

import numpy as np

import house as H
import lynch_body as LB
from m05 import plots_main as PM
from m05.plots_prob import Plot, label, legend, hov, svg, sub

O, I, SER, T = H.OVERLAY, H.INK, H.SERIES, H.TISSUE
GRID = "#e6e6e6"
BOX = "#f7f4ef"
DASH = PM.DASH_SER
W = 400                                                  # problem figures: viewBox width = rendered width

# ---------------------------------------------------------------- the module's arm (Lab B, Appendix; line 333-336)
G = 9.81
M1, M2, L1, L2 = 2.1, 1.65, 0.30, 0.45
LC1, LC2, I1, I2 = 0.15, 0.22, 0.016, 0.025
M22 = I2 + M2 * LC2 ** 2
TH1, A_W, TH20 = math.radians(100), 0.5, -1.0
G_ELBOW = M2 * LC2 * G                                   # m2 lc2 g = 3.56 N m (line 173, line 541)


def close(v, ref, tol):
    assert abs(v - ref) <= tol * 1.0001, (v, ref)


def wave(f, t):
    """Lab B's tau(): total, inertial and gravity elbow torque (shoulder held, so the Coriolis term is zero)."""
    w = 2 * np.pi * f
    th2 = TH20 + A_W * np.sin(w * t)
    inert = M22 * (-A_W * w * w * np.sin(w * t))
    grav = G_ELBOW * np.cos(TH1 + th2)
    return inert + grav, inert, grav


def lab_b_peaks(f):
    t = np.linspace(0, 2.0, 400)                         # Lab B's grid
    tot, inert, grav = wave(f, t)
    return float(np.abs(tot).max()), float(np.abs(inert).max()), float(np.abs(grav).max())


close(M22, 0.10486, 1e-4)
_p15, _p3 = lab_b_peaks(1.5), lab_b_peaks(3.0)
assert [round(v, 1) for v in (_p15[1], _p15[2], _p15[0])] == [4.7, 3.5, 8.1]        # lines 355, 367, 369
assert [round(_p3[1]), round(_p3[0])] == [19, 22]                                   # line 367


def sw(s, x, y, txt, col, dash=None, w="curve_multi"):
    return H.line(s, x, y - 4.5, x + 20, y - 4.5, col, w, dash) + label(s, x + 25, y, txt, "label2", I["secondary"])


def end_labels(s, x, items, spacing=16):
    """Direct labels right of a plot: items (y, colour, text, dash) at the curve-end heights, pushed apart to
    `spacing`; a leader joins a moved label to its curve end.  Identity = the coloured mark, text stays ink."""
    items = sorted(items, key=lambda q: q[0])
    ys = [q[0] for q in items]
    for i in range(1, len(ys)):
        ys[i] = max(ys[i], ys[i - 1] + spacing)
    o = []
    for (y0, col, txt, dash), y in zip(items, ys):
        if abs(y - y0) > 1:
            o.append(H.line(s, x - 6, y0, x + 2, y - 4.5, col, "leader"))
        o.append(H.line(s, x + 2, y - 4.5, x + 18, y - 4.5, col, "curve_multi", dash))
        o.append(label(s, x + 23, y, txt, "label2", I["primary"]))
    return "".join(o)


def svg_main(vb, aria, s, o, hv):
    return svg(vb, aria, s, "".join(o), hv)


# ---------------------------------------------------------------- body kit helpers
def fit(P, s, box, facing="right"):
    """Draw pose P so its art bbox fits box (x0, y0, x1, y1), centred, bottom-aligned.  Returns (svg, J, (x, y, h))."""
    _, J0 = LB.draw("m11", s, P, 0, 0, 100, facing=facing)
    x0, y0, x1, y1 = J0["bbox"]
    k = min((box[2] - box[0]) / (x1 - x0), (box[3] - box[1]) / (y1 - y0))
    x = (box[0] + box[2]) / 2 - k * (x0 + x1) / 2
    y = box[3] - k * y1
    sv, J = LB.draw("m11", s, P, x, y, 100 * k, facing=facing)
    return sv, J, (x, y, 100 * k)


def ghost_arm(P, s, place, facing="right", op=0.35):
    """Only the near forearm and hand of pose P (a faint earlier or later position of the wave)."""
    P2 = LB.Pose(P.view)
    P2.segs = [q for q in P.segs if q[0] in ("arm_fore", "arm_hand") and not q[5]]
    P2.j, P2.com, P2.anchor, P2.floor_y = P.j, P.com, P.anchor, P.floor_y
    sv, _ = LB.draw("m11", s, P2, place[0], place[1], place[2], facing=facing)
    return f'<g opacity="{op}">{sv}</g>'


def chair(s, J, facing="right", span=(-0.16, 0.20)):
    """Seat and legs under the hip: a schematic stool (design value), not anatomy."""
    hx, hy = J["hip"]
    h = J["floor_y"] - J["vertex"][1]
    sg = -1 if facing == "left" else 1
    y = hy + 0.075 * h
    xa, xb = hx + sg * span[0] * h, hx + sg * span[1] * h
    o = [H.line(s, xa, y, xb, y, I["rule"], "axis", extra='stroke-linecap="round"')]
    for xx in (xa + (xb - xa) * 0.06, xa + (xb - xa) * 0.94):
        o.append(H.line(s, xx, y, xx, J["floor_y"], I["rule"], "axis"))
    return "".join(o)


def floor(s, x0, x1, y):
    return H.line(s, x0, y, x1, y, I["axis"], "axis")


def cup(s, x, y, w):
    """A mug (schematic, fluid-blue tissue tokens) with its base centre at (x, y)."""
    h = w * 1.15
    f, ln = T["fluid"]
    return (f'<path d="M{x + w / 2:.2f},{y - h * 0.72:.2f} q{w * 0.45:.2f},{h * 0.02:.2f} {w * 0.04:.2f},{h * 0.42:.2f}" '
            f'fill="none" stroke="{ln}" stroke-width="{s(1.6):.2f}"/>'
            f'<rect x="{x - w / 2:.2f}" y="{y - h:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{w * 0.08:.2f}" fill="{f}" '
            f'stroke="{ln}" stroke-width="{s(1.2):.2f}"/>')


# ================================================================ svg #9: elbow torque of a wave (Lab B, 1.5 Hz)
def fig9():
    VB = (0, 0, 760, 416)
    s = H.Scale(VB[2], VB[3])
    P = Plot(s, (336, 66, 590, 316), (0, 2.0), (-6, 9))
    t = np.linspace(0, 2.0, 241)
    tot, inert, grav = wave(1.5, t)
    assert [round(v, 1) for v in (tot.max(), inert.max(), grav.max())] == [8.1, 4.7, 3.5]
    o = [P.axes([(x, f"{x:.1f}") for x in (0, 0.5, 1.0, 1.5, 2.0)],
                [(y, PM.mn(y, "{:.0f}")) for y in (-6, -3, 0, 3, 6, 9)], "time t (s)", "elbow torque (N m)",
                grid=(-6, -3, 3, 6, 9), ytx=286)]
    o.append(H.line(s, P.x0, P.Y(0), P.x1, P.Y(0), I["rule"], "ref"))
    o.append(P.curve(t, grav, O["load"], multi=True, dash=DASH))
    o.append(P.curve(t, inert, SER[1], multi=True))
    o.append(P.curve(t, tot, I["primary"]))
    o.append(end_labels(s, P.x1 + 8, [
        (P.Y(tot[-1]), I["primary"], f"total, peak {tot.max():.1f}", None),
        (P.Y(grav[-1]), O["load"], f"gravity, {grav.min():.1f} to {grav.max():.1f}", DASH),
        (P.Y(inert[-1]), SER[1], f"inertial, peak {inert.max():.1f}", None)]))
    o.append(legend(s, 336, 28, [(I["primary"], "total τ₂", None), (SER[1], "inertial", None), (O["load"], "gravity", DASH)]))
    # inset: a seated skeleton waving.  Sketch in the kit's clinical angles (shoulder flexion 100 deg, elbow flexion
    # 57 deg +- 29 deg = the model's theta1 and theta2^0 +- A in size); the plot carries the model's own geometry.
    bx = (10, 92, 280, 330)
    el0 = math.degrees(-TH20)
    kw = dict(near=dict(hip=90, knee=90, shoulder=100, elbow=el0), far=dict(hip=90, knee=90))
    sv, J, place = fit(LB.pose(**kw), s, bx, "right")
    gh = "".join(ghost_arm(LB.pose(near=dict(kw["near"], elbow=el0 + d), far=kw["far"]), s, place, "right")
                 for d in (-math.degrees(A_W), math.degrees(A_W)))
    o += [chair(s, J), floor(s, bx[0], bx[2], J["floor_y"]), sv, gh]
    o.append(label(s, bx[0] + 4, 56, f"the wave: shoulder 100°, elbow {el0:.0f}° ± {math.degrees(A_W):.0f}°", "label2",
                   I["primary"]))
    o.append(label(s, bx[0] + 4, 72, "faint forearms: the two ends of the swing", "label2", I["secondary"]))
    o.append(LB.credit(s, 10, 382, width=740))
    aria = ("Elbow torque over two seconds of a 1.5 hertz wave, split into an inertial part, a gravitational part and "
            f"their sum. The total peaks at {tot.max():.1f} newton metres and falls to {tot.min():.1f}; the inertial part "
            f"peaks at {inert.max():.1f}; the gravitational part stays between {grav.min():.1f} and {grav.max():.1f}. "
            "At left a seated skeleton raises the arm, with faint forearms at the two ends of the swing.")
    hvp = hov(P, t, [tot, inert, grav], lambda i: f"t = {t[i]:.2f} s: total {PM.mn(tot[i])}, inertial {PM.mn(inert[i])}, "
                                                  f"gravity {PM.mn(grav[i])} N m")
    return svg_main(VB, aria, s, o, (P.box, hvp))


# ================================================================ svg #12 and #18 right: the grip-load loop (Lab C)
MG, S_MARGIN, MU_REF = 0.5, 0.30, 0.6                    # kg, safety margin, friction during the lift (lines 372, 377)


def lift(t, mu=MU_REF):
    a = 4.0 * np.exp(-((t - 0.6) / 0.12) ** 2)           # Lab C's acceleration pulse (line 383)
    load = MG * (G + a)
    return load, (1 + S_MARGIN) * load / (2 * mu), load / (2 * mu)


def fig12():
    VB = (0, 0, 760, 416)
    s = H.Scale(VB[2], VB[3])
    P = Plot(s, (336, 66, 590, 316), (0, 1.5), (0, 12))
    t = np.linspace(0, 1.5, 181)
    load, grip, floor_ = lift(t)
    assert round(float(grip[0]), 2) == 5.31
    band = (f'<polygon points="{" ".join(f"{P.X(a):.1f},{P.Y(b):.1f}" for a, b in zip(t, grip))} '
            f'{" ".join(f"{P.X(a):.1f},{P.Y(b):.1f}" for a, b in zip(t[::-1], floor_[::-1]))}" fill="{SER[1]}" opacity="0.14"/>')
    o = [band, P.axes([(x, f"{x:.1f}") for x in (0, 0.5, 1.0, 1.5)], [(y, f"{y}") for y in (0, 3, 6, 9, 12)],
                      "time t (s)", "force (N)", grid=(3, 6, 9, 12), ytx=292)]
    o.append(P.curve(t, floor_, I["secondary"], multi=True, dash=DASH))
    o.append(P.curve(t, load, SER[0], multi=True))
    o.append(P.curve(t, grip, SER[1], multi=True))
    j = int(np.argmax(grip))
    o.append(label(s, P.X(0.64), P.Y(grip[j]) - 6, f"grip peak {grip[j]:.1f} N", "label2", I["primary"]))
    o.append(label(s, P.X(0.04), P.Y(10.6), "safety margin s = 0.3: the shaded band", "label2", I["secondary"]))
    o.append(label(s, P.X(0.04), P.Y(10.6) + 16, "between grip and slip floor", "label2", I["secondary"]))
    o.append(end_labels(s, P.x1 + 8, [
        (P.Y(grip[-1]), SER[1], f"grip {grip[-1]:.2f} N", None),
        (P.Y(load[-1]), SER[0], f"load {load[-1]:.2f} N", None),
        (P.Y(floor_[-1]), I["secondary"], f"slip floor {floor_[-1]:.2f} N", DASH)]))
    o.append(label(s, P.x1 + 8, P.Y(1.6), "at rest; μ = 0.6, m = 0.5 kg", "label2", I["secondary"]))
    o.append(label(s, P.x1 + 8, P.Y(1.6) + 16, "grip F_g = (1 + s) L / 2μ".replace("F_g", "F" + sub("g", s, "label2")),
                   "label2", I["secondary"]))
    o += [legend(s, 336, 28, [(SER[1], "grip force per pad", None), (SER[0], "load force L", None),
                              (I["secondary"], "slip floor L/2μ", DASH)])]
    bx = (10, 92, 300, 330)
    Pm = LB.pose(near=dict(hip=90, knee=90, shoulder=30, elbow=60), far=dict(hip=90, knee=90, shoulder=30, elbow=60))
    sv, J, _ = fit(Pm, s, bx, "right")
    o += [chair(s, J), floor(s, bx[0], bx[2], J["floor_y"]), sv,
          cup(s, J["fingertip"][0] + 14, J["fingertip"][1] + 14, 24)]
    o.append(label(s, bx[0] + 4, 72, "lifting a familiar cup", "label2", I["secondary"]))
    o.append(LB.credit(s, 10, 382, width=740))
    aria = ("The grip-load loop over a 1.5 second lift: grip force per pad and load force rise together in parallel "
            f"from {grip[0]:.2f} and {load[0]:.2f} newtons at rest to {grip[j]:.1f} and {load.max():.1f} at the acceleration "
            f"peak, with grip held a 30 percent safety margin above the dashed slip floor L over 2 mu ({floor_.max():.2f} N "
            "at the peak). At left a seated skeleton lifts a cup.")
    hvp = hov(P, t, [grip, load, floor_], lambda i: f"t = {t[i]:.2f} s: grip {grip[i]:.2f}, load {load[i]:.2f}, "
                                                    f"slip floor {floor_[i]:.2f} N")
    return svg_main(VB, aria, s, o, (P.box, hvp))


# ================================================================ svg #16: Lab B at 1.5 and 3 Hz
def fig16():
    VB = (0, 0, 760, 396)
    s = H.Scale(VB[2], VB[3])
    P = Plot(s, (84, 60, 560, 330), (0, 2.0), (-24, 24))
    t = np.linspace(0, 2.0, 241)
    t15, i15, g15 = wave(1.5, t)
    t3, i3, g3 = wave(3.0, t)
    assert [round(float(t15.max()), 1), round(float(t3.max()), 1), round(float(i3.max()), 1)] == [8.1, 22.1, 18.6]
    o = [P.axes([(x, f"{x:.1f}") for x in (0, 0.5, 1.0, 1.5, 2.0)],
                [(y, PM.mn(y, "{:.0f}")) for y in (-24, -12, 0, 12, 24)], "time t (s)", "elbow torque (N m)",
                grid=(-24, -12, 12, 24), ytx=26)]
    o.append(H.line(s, P.x0, P.Y(0), P.x1, P.Y(0), I["rule"], "ref"))
    o.append(P.curve(t, g15, O["load"], multi=True, dash=DASH))
    o.append(P.curve(t, i15, SER[1], multi=True))
    o.append(P.curve(t, t3, SER[0], multi=True, nmax=181))
    o.append(P.curve(t, t15, I["primary"], multi=True))
    o.append(end_labels(s, P.x1 + 8, [
        (P.Y(t3[-1]), SER[0], f"total, 3 Hz: peak {t3.max():.1f}", None),
        (P.Y(t15[-1]), I["primary"], f"total, 1.5 Hz: peak {t15.max():.1f}", None),
        (P.Y(i15[-1]), SER[1], f"inertial, 1.5 Hz: peak {i15.max():.1f}", None),
        (P.Y(g15[-1]), O["load"], f"gravity: peak {g15.max():.1f}", DASH)], spacing=18))
    o += [legend(s, 84, 24, [(SER[0], "total, 3 Hz", None), (I["primary"], "total, 1.5 Hz", None),
                             (SER[1], "inertial, 1.5 Hz", None), (O["load"], "gravity", DASH)])]
    aria = ("Elbow torque over two seconds of waving at 1.5 and 3 hertz. At 1.5 hertz the inertial part peaks at "
            f"{i15.max():.1f} and the gravitational part at {g15.max():.1f} newton metres, so the total peaks at "
            f"{t15.max():.1f}. At 3 hertz the inertial part quadruples to {i3.max():.1f} and the total peaks at "
            f"{t3.max():.1f}, about 2.7 times the 1.5 hertz total, for the same hand travel.")
    hvp = hov(P, t, [t3, t15, i15, g15], lambda i: f"t = {t[i]:.2f} s: total 3 Hz {PM.mn(t3[i])}; 1.5 Hz total "
                                                   f"{PM.mn(t15[i])}, inertial {PM.mn(i15[i])}, gravity {PM.mn(g15[i])} N m")
    return svg_main(VB, aria, s, o, (P.box, hvp))


# ================================================================ svg #18: Lab C, floor against friction and lift
def fig18():
    VB = (0, 0, 760, 340)
    s = H.Scale(VB[2], VB[3])
    PL = Plot(s, (84, 60, 350, 280), (0.1, 0.8), (0, 35))
    PR = Plot(s, (456, 60, 740, 280), (0, 1.5), (0, 12))
    mu = np.linspace(0.1, 0.8, 100)
    fs = (1 + S_MARGIN) * MG * G / (2 * mu)
    dots = [(m_, (1 + S_MARGIN) * MG * G / (2 * m_)) for m_ in (0.6, 0.2, 0.1)]
    assert [round(d[1], 2) for d in dots] == [5.31, 15.94, 31.88] and round(dots[2][1], 1) == 31.9
    o = [PL.axes([(x, f"{x:.1f}") for x in (0.1, 0.2, 0.4, 0.6, 0.8)], [(y, f"{y}") for y in (0, 10, 20, 30)],
                 "friction coefficient μ", "grip force per pad (N)", grid=(10, 20, 30), ytx=26)]
    o.append(PL.curve(mu, fs, SER[1]))
    for m_, f_ in dots:
        o.append(PL.dot(m_, f_, SER[1]))
    o.append(label(s, PL.X(0.1) + 10, PL.Y(dots[2][1]) + 4, f"{dots[2][1]:.1f} N at μ = 0.1", "label2", I["primary"]))
    o.append(label(s, PL.X(0.2) + 10, PL.Y(dots[1][1]) - 6, f"{dots[1][1]:.1f} N at 0.2", "label2", I["primary"]))
    o.append(label(s, PL.X(0.6), PL.Y(dots[0][1]) - 12, f"{dots[0][1]:.1f} N at 0.6", "label2", I["primary"], "middle"))
    o.append(label(s, PL.X(0.8), PL.Y(24), "F_g = 1.3 m g / 2μ".replace("F_g", f"F{sub('g', s, 'label2')}"),
                   "label2", I["secondary"], "end"))
    o.append(label(s, PL.X(0.8), PL.Y(24) + 16, "(m = 0.5 kg, s = 0.3)", "label2", I["secondary"], "end"))
    t = np.linspace(0, 1.5, 181)
    load, grip, _ = lift(t)
    o.append(PR.axes([(x, f"{x:.1f}") for x in (0, 0.5, 1.0, 1.5)], [(y, f"{y}") for y in (0, 4, 8, 12)],
                     "time t (s)", "force (N)", grid=(4, 8, 12), ytx=412))
    o.append(PR.curve(t, load, SER[0], multi=True))
    o.append(PR.curve(t, grip, SER[1], multi=True))
    o.append(label(s, PR.X(0.05), PR.Y(grip[0]) - 10, "grip", "label2", I["primary"]))
    o.append(label(s, PR.X(0.05), PR.Y(load[0]) + 20, "load", "label2", I["primary"]))
    o.append(label(s, PR.X(0.72), PR.Y(grip.max()) - 8, f"peak {grip.max():.1f} and {load.max():.1f} N", "label2",
                   I["secondary"]))
    o += [legend(s, 84, 28, [(SER[1], "grip force per pad, static", None)]),
          legend(s, 456, 28, [(SER[1], "grip, lifting", None), (SER[0], "load", None)]),
          label(s, 740, 46, "μ = 0.6 during the lift", "label2", I["secondary"], "end")]
    aria = ("Left: the grip-force floor per pad with a 30 percent margin against the friction coefficient, a "
            f"hyperbola: {dots[0][1]:.1f} newtons at 0.6, {dots[1][1]:.1f} at 0.2 and {dots[2][1]:.1f} at 0.1. Right: "
            "grip force and load force over a 1.5 second lift, rising together.")
    ptl = hov(PL, mu, [fs], lambda i: f"μ = {mu[i]:.3f}: grip floor {fs[i]:.2f} N per pad")
    ptr = hov(PR, t, [grip, load], lambda i: f"t = {t[i]:.2f} s: grip {grip[i]:.2f}, load {load[i]:.2f} N")
    return H.svg_open(VB, html.escape(aria), s, extra=H.hover_attr([(PL.box, ptl), (PR.box, ptr)])) + "".join(o) + "</svg>"


# ================================================================ svg #25 C5: the taped thumb (force closure)
def fig25():
    VB = (0, 0, W, 366)
    s = H.Scale(W, VB[3], display_w=400)
    mu = 0.6                                              # design value: the Lab C reference friction
    phi = math.degrees(math.atan(mu))
    o = []
    bx = (4, 52, 168, 258)
    Pm = LB.pose(near=dict(hip=90, knee=90, shoulder=30, elbow=60), far=dict(hip=90, knee=90, shoulder=30, elbow=60))
    sv, J, _ = fit(Pm, s, bx, "right")
    fx, fy = J["fingertip"]
    cx, cy = fx + 12, fy + 4
    o += [chair(s, J), floor(s, bx[0], bx[2], J["floor_y"]), sv, cup(s, cx, cy + 12, 20)]
    # the detail box: two top views of the cup, friction cones at the two contacts
    X0, Y0, X1, Y1 = 176, 76, 396, 276
    o.append(f'<rect x="{X0}" y="{Y0}" width="{X1 - X0}" height="{Y1 - Y0}" rx="6" fill="{BOX}" stroke="{I["rule"]}" '
             f'stroke-width="{s(1):.2f}"/>')
    o.append(H.line(s, cx + 11, cy - 10, X0, Y0 + 40, I["rule"], "ref", H.DASH_REF))
    o.append(label(s, (X0 + X1) / 2, Y0 - 8, "detail: two pads on the cup, top view", "label2", I["secondary"], "middle"))
    R, CL = 34, 46

    def case(ccx, ccy, ang_a, ang_b, name, verdict, ok):
        pa = (ccx + R * math.cos(math.radians(ang_a)), ccy - R * math.sin(math.radians(ang_a)))
        pb = (ccx + R * math.cos(math.radians(ang_b)), ccy - R * math.sin(math.radians(ang_b)))
        out = [f'<circle cx="{ccx}" cy="{ccy}" r="{R}" fill="{T["fluid"][0]}" stroke="{T["fluid"][1]}" '
               f'stroke-width="{s(1.2):.2f}"/>']
        gam = []
        for p, q in ((pa, pb), (pb, pa)):
            nx, ny = ccx - p[0], ccy - p[1]                                          # inward normal (to the centre)
            n = math.hypot(nx, ny)
            nx, ny = nx / n, ny / n
            jx, jy = q[0] - p[0], q[1] - p[1]
            jn = math.hypot(jx, jy)
            g = math.degrees(math.acos(max(-1, min(1, (nx * jx + ny * jy) / jn))))
            gam.append(g)
            col = O["neural"] if g < phi else SER[0]
            for sg in (-1, 1):
                a = math.atan2(ny, nx) + sg * math.radians(phi)
                out.append(H.line(s, p[0], p[1], p[0] + CL * math.cos(a), p[1] + CL * math.sin(a), col, "geom",
                                  H.DASH_REF))
        out.append(H.line(s, pa[0], pa[1], pb[0], pb[1], I["primary"], "geom"))      # the joining line
        for p in (pa, pb):
            out.append(f'<circle cx="{p[0]:.2f}" cy="{p[1]:.2f}" r="{s(5):.2f}" fill="{T["skin"][0]}" '
                       f'stroke="{T["skin"][1]}" stroke-width="{s(1.5):.2f}"/>')
        out.append(label(s, ccx, ccy + R + 22, name, "label2", I["primary"], "middle"))
        out.append(label(s, ccx, ccy + R + 39, f"γ = {gam[0]:.0f}°, {gam[1]:.0f}° {'<' if ok else '≥'} φ".replace("<", "&lt;"),
                         "label2", I["secondary"], "middle"))
        out.append(label(s, ccx, ccy + R + 56, verdict, "label2", I["primary"], "middle"))
        return "".join(out), gam

    c1, g1 = case(236, 150, 180, 0, "thumb opposed", "force-closed", True)
    c2, g2 = case(346, 150, 195, 125, "thumb taped flat", "not closed", False)
    assert max(g1) < phi < min(g2)
    o += [c1, c2]
    o.append(label(s, (X0 + X1) / 2, Y0 + 16, f"φ = arctan μ = {phi:.0f}° (μ = {mu})", "label2", I["secondary"], "middle"))
    o.append(label(s, 4, 296, "dashed lines: the friction-cone edges at each pad; green = the", "label2", I["secondary"]))
    o.append(label(s, 4, 312, "joining line (solid) lies inside the cone, red = outside it", "label2", I["secondary"]))
    o.append(LB.credit(s, 4, 332, width=392))
    aria = ("C5: the taped thumb, force closure of a two-pad pinch. At left a seated skeleton holds a cup; at right two "
            f"top views of the cup with the friction cone, half-angle {phi:.0f} degrees, at each pad. With the thumb "
            f"opposed the joining line is inside both cones (angles {g1[0]:.0f} and {g1[1]:.0f} degrees) and the grasp is "
            f"force-closed; with the thumb flat the angles are {g2[0]:.0f} and {g2[1]:.0f} degrees, outside the cone, "
            "and closure is lost.")
    return H.svg_open(VB, html.escape(aria), s) + "".join(o) + "</svg>"


# ================================================================ svg #35 D5: force ellipse against velocity ellipse
def jac(th1, th2):
    s1, s12, c1, c12 = np.sin(th1), np.sin(th1 + th2), np.cos(th1), np.cos(th1 + th2)
    return np.array([[-L1 * s1 - L2 * s12, -L2 * s12], [L1 * c1 + L2 * c12, L2 * c12]])


def fig35():
    VB = (0, 0, W, 336)
    s = H.Scale(W, VB[3], display_w=400)
    Jm = jac(math.radians(30), 0.6)                       # Lab D's shoulder angle, elbow 0.6 rad (design value)
    U, sig, Vt = np.linalg.svd(Jm)
    w = abs(np.linalg.det(Jm))
    close(sig[0] * sig[1], w, 1e-9)
    close(w, L1 * L2 * math.sin(0.6), 1e-9)               # Lab D: w = l1 l2 |sin th2|
    ph = np.linspace(0, 2 * np.pi, 121)
    circle = np.array([np.cos(ph), np.sin(ph)])
    vel = Jm @ circle
    frc = np.linalg.inv(Jm).T @ circle
    # same principal axes, reciprocal lengths: the SVD statement of the solution
    assert np.allclose(np.abs(U.T @ vel).max(axis=1), sig, rtol=1e-2) and \
        np.allclose(np.abs(U.T @ frc).max(axis=1), 1 / sig, rtol=1e-2)
    kpx = 110 / sig[0]
    ccx, ccy = 200, 150

    def pts(M, scale):                                    # screen y is down: flip the vertical component
        return " ".join(f"{ccx + scale * x:.1f},{ccy - scale * y:.1f}" for x, y in M.T)
    fscale = kpx * w                                      # force ellipse drawn x w, so its axes are sigma2, sigma1
    o = [f'<polygon points="{pts(vel, kpx)}" fill="{SER[1]}" opacity="0.12"/>',
         f'<polyline points="{pts(vel, kpx)}" fill="none" stroke="{SER[1]}" stroke-width="{s(H.PX["curve"]):.2f}"/>',
         f'<polyline points="{pts(frc, fscale)}" fill="none" stroke="{SER[0]}" stroke-width="{s(H.PX["curve"]):.2f}" '
         f'stroke-dasharray="{s(7):.1f} {s(4):.1f}"/>']
    u1, u2 = (U[0, 0], -U[1, 0]), (U[0, 1], -U[1, 1])
    for u, L in ((u1, 124), (u2, 96)):
        o.append(H.line(s, ccx - L * u[0], ccy - L * u[1], ccx + L * u[0], ccy + L * u[1], I["rule"], "ref", H.DASH_REF))
    o.append(label(s, ccx + 132 * u1[0], ccy + 132 * u1[1] + 4, "u₁", "label", I["primary"],
                   "start" if u1[0] > 0 else "end"))
    sg = 1 if u2[1] < 0 else -1                           # the end of u2 that points up the page
    o.append(label(s, ccx + sg * 112 * u2[0], ccy + sg * 112 * u2[1] - 4, "u₂", "label", I["primary"],
                   "start" if sg * u2[0] > 0 else "end"))
    o.append(f'<circle cx="{ccx}" cy="{ccy}" r="{s(H.PX["dot"]):.2f}" fill="{I["primary"]}"/>')
    o.append(label(s, 200, 22, "same axes u₁, u₂ (columns of U), reciprocal lengths", "label", I["primary"], "middle"))
    o.append(H.line(s, 14, 262, 38, 262, SER[1], "curve"))
    o.append(label(s, 44, 266, f"velocity ellipse: σ₁ = {sig[0]:.3f} on u₁, σ₂ = {sig[1]:.3f} on u₂", "label2",
                   I["primary"]))
    o.append(H.line(s, 14, 284, 38, 284, SER[0], "curve", H.DASH_REF))
    o.append(label(s, 44, 288, f"force ellipse: 1/σ₁ = {1 / sig[0]:.1f} on u₁, 1/σ₂ = {1 / sig[1]:.1f} on u₂", "label2",
                   I["primary"]))
    o.append(label(s, 14, 308, f"force ellipse drawn × σ₁σ₂ = {w:.4f}; σ in m, 1/σ in m⁻¹", "label2", I["secondary"]))
    o.append(label(s, 14, 324, "the long axis of one is the short axis of the other", "label2", I["secondary"]))
    aria = ("D5: the velocity ellipse, the image of the unit joint-rate circle under the Jacobian J, and the force "
            "ellipse, the image of the unit torque circle under J inverse transpose, for the two-link arm at a shoulder "
            f"angle of 30 degrees and an elbow angle of 0.6 radians. Both have their principal axes along the columns "
            f"of U; the velocity semi-axes are {sig[0]:.3f} and {sig[1]:.3f}, the force semi-axes are the reciprocals "
            f"{1 / sig[0]:.1f} and {1 / sig[1]:.1f}, drawn scaled by the manipulability {w:.4f} so the force ellipse is "
            "the velocity ellipse turned through 90 degrees.")
    return H.svg_open(VB, html.escape(aria), s) + "".join(o) + "</svg>"


# ================================================================ svg #41 K1: peak elbow rate against reach
def ik_peak(gx, n=400, T_=0.6):
    s_ = np.linspace(0, 1, n)
    x, y = 0.10 + (gx - 0.10) * s_, -0.30 + 0.40 * s_
    c = (x * x + y * y - L1 ** 2 - L2 ** 2) / (2 * L1 * L2)
    return float(np.abs(np.gradient(np.arccos(np.clip(c, -1, 1)), T_ / (n - 1))).max())


def fig41():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    key = (0.45, 0.60, 0.70, 0.73)
    r_key = [math.hypot(x, 0.10) for x in key]
    p_key = [ik_peak(x) for x in key]
    assert [round(r, 3) for r in r_key] == [0.461, 0.608, 0.707, 0.737]
    assert [round(p, 2) for p in p_key] == [2.55, 4.37, 8.79, 16.00]                       # line 537
    assert [round(ik_peak(x, 60), 2) for x in key] == [2.53, 4.31, 8.37, 13.94]
    assert [round(ik_peak(x, 4000), 2) for x in key] == [2.55, 4.38, 8.87, 16.45]
    assert round(p_key[3] / p_key[2], 2) == 1.82                                           # "1.82x over the last 3 cm"
    gx = np.linspace(0.40, 0.7425, 110)
    gx = np.unique(np.concatenate([gx, key]))
    r = np.hypot(gx, 0.10)
    ymax = 24.0
    P = Plot(s, (56, 60, 386, 238), (0.42, 0.76), (0, ymax))
    curves = {n: np.array([ik_peak(x, n) for x in gx]) for n in (60, 400, 4000)}

    def cut(ys):
        k = int(np.argmax(ys > ymax)) if (ys > ymax).any() else len(ys)
        return r[:k], ys[:k]
    o = [P.axes([(x, f"{x:.1f}") for x in (0.5, 0.6, 0.7)], [(y, f"{y}") for y in (0, 6, 12, 18, 24)],
                "reach distance r (m)", "peak elbow rate (rad s⁻¹)", grid=(6, 12, 18, 24), ytx=14)]
    o.append(H.line(s, P.X(0.75), P.y0, P.X(0.75), P.y1, I["rule"], "ref", H.DASH_REF))
    o.append(P.curve(*cut(curves[60]), SER[2], multi=True, dash=DASH))
    o.append(P.curve(*cut(curves[4000]), SER[1], multi=True, dash=DASH))
    o.append(P.curve(*cut(curves[400]), SER[0]))
    for rr, pp in zip(r_key, p_key):
        o.append(P.dot(rr, pp, SER[0]))
    o.append(label(s, P.X(r_key[0]) + 6, P.Y(p_key[0]) - 10, f"{p_key[0]:.2f}", "label2", I["primary"]))
    o.append(label(s, P.X(r_key[1]) + 6, P.Y(p_key[1]) - 10, f"{p_key[1]:.2f}", "label2", I["primary"]))
    o.append(label(s, P.X(r_key[2]) - 8, P.Y(p_key[2]) - 6, f"{p_key[2]:.2f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(r_key[3]) - 8, P.Y(p_key[3]) - 4, f"{p_key[3]:.2f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.75) - 4, P.Y(2.4), "ℓ₁ + ℓ₂ = 0.75 m", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(0.43), P.Y(21), "×1.82 over the last 3 cm", "label2", I["secondary"]))
    o.append(label(s, P.X(0.43), P.Y(21) + 16, "(0.707 to 0.737 m, N = 400)", "label2", I["secondary"]))
    o.append(legend(s, 56, 18, [(SER[0], "N = 400", None), (SER[2], "N = 60", DASH), (SER[1], "N = 4000", DASH)]))
    aria = ("K1 plot: peak elbow angular velocity of a 0.6 second straight reach against the reach distance, up to the "
            "workspace boundary at 0.75 metres. With 400 samples the peak is 2.55, 4.37, 8.79 and 16.00 radians per "
            "second at reaches of 0.461, 0.608, 0.707 and 0.737 metres, a factor 1.82 over the last 3 centimetres. "
            "Dashed curves with 60 and 4000 samples agree at short reach and separate near the boundary, where the "
            "true peak is unbounded.")
    hvp = hov(P, r[::2], [curves[400][::2]], lambda i: f"r = {r[::2][i]:.3f} m: peak {curves[400][::2][i]:.2f} rad/s "
                                                      f"(N = 400); N = 60: {curves[60][::2][i]:.2f}; N = 4000: "
                                                      f"{curves[4000][::2][i]:.2f}")
    return svg(VB, aria, s, "".join(o), (P.box, hvp))


# ================================================================ svg #42 K2: inertial against gravity torque
def fig42():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    fc = math.sqrt(G_ELBOW / (M22 * A_W)) / (2 * math.pi)
    assert round(fc, 2) == 1.31 and round(G_ELBOW, 1) == 3.6
    f = np.linspace(0.3, 3.2, 117)
    inert = M22 * A_W * (2 * np.pi * f) ** 2
    tm = np.linspace(0, 1.0, 600)
    tot = np.array([float(np.abs(wave(ff, np.linspace(0, 1 / ff, 600))[0]).max()) for ff in f])
    t15, t3 = lab_b_peaks(1.5)[0], lab_b_peaks(3.0)[0]
    assert round(t15, 1) == 8.1 and round(t3, 1) == 22.1                                    # line 541
    P = Plot(s, (56, 58, 386, 236), (0.2, 3.3), (0, 24))
    o = [P.axes([(x, f"{x}") for x in (1, 2, 3)], [(y, f"{y}") for y in (0, 6, 12, 18, 24)], "wave frequency f (Hz)",
                "peak elbow torque (N m)", grid=(6, 12, 18, 24), ytx=14)]
    o.append(H.line(s, P.X(fc), P.y0, P.X(fc), P.Y(G_ELBOW), I["rule"], "ref", H.DASH_REF))
    o.append(P.curve(f, np.full_like(f, G_ELBOW), O["load"], multi=True, dash=DASH))
    o.append(P.curve(f, inert, SER[1], multi=True))
    o.append(P.curve(f, tot, I["primary"]))
    o.append(P.dot(fc, G_ELBOW, SER[2]))
    for ff, tt in ((1.5, t15), (3.0, t3)):
        o.append(P.dot(ff, tt, I["primary"]))
    o.append(label(s, P.X(fc) + 8, P.Y(G_ELBOW) + 18, f"crossover {fc:.2f} Hz", "label2", I["primary"]))
    o.append(label(s, P.X(1.5) - 8, P.Y(t15) - 8, f"{t15:.1f} at 1.5 Hz", "label2", I["primary"], "end"))
    o.append(label(s, P.X(3.0) - 8, P.Y(t3) - 4, f"{t3:.1f} at 3 Hz", "label2", I["primary"], "end"))
    o.append(label(s, P.X(3.25), P.Y(G_ELBOW) - 8, f"gravity {G_ELBOW:.2f}", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(3.25), P.Y(9), "inertial ∝ f²", "label2", I["secondary"], "end"))
    o.append(legend(s, 56, 18, [(I["primary"], "total", None), (SER[1], "inertial M₂₂A(2πf)²", None)]))
    o.append(legend(s, 56, 38, [(O["load"], "gravity m₂ℓc₂g", DASH)]))
    aria = ("K2 plot: peak elbow torque of the wave against its frequency from 0.3 to 3.2 hertz. The inertial part "
            f"grows as f squared and crosses the constant gravitational part, {G_ELBOW:.2f} newton metres, at "
            f"{fc:.2f} hertz. The total peaks at {t15:.1f} newton metres at 1.5 hertz and {t3:.1f} at 3 hertz.")
    hvp = hov(P, f, [tot, inert], lambda i: f"f = {f[i]:.2f} Hz: total {tot[i]:.2f}, inertial {inert[i]:.2f}, "
                                            f"gravity {G_ELBOW:.2f} N m")
    return svg(VB, aria, s, "".join(o), (P.box, hvp))


# ================================================================ svg #48 K8: a slip and its reflex
def fig48():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    a_true, a_pred, sm, delay = 9.0, 1.5, 0.30, 0.070
    t = np.linspace(0, 1.0, 801)
    p = np.exp(-((t - 0.6) / 0.12) ** 2)
    load = MG * (G + a_true * p)
    ff = (1 + sm) * MG * (G + a_pred * p)                  # feedforward grip: friction it can deliver 2 mu F_g
    margin = ff / load - 1
    k0 = int(np.argmax(margin < 0))
    t_slip = float(np.interp(0.0, -margin[k0 - 1:k0 + 1], t[k0 - 1:k0 + 1]))
    t_ref = t_slip + delay
    assert round(t_slip, 3) == 0.488 and round(t_ref, 3) == 0.558                          # line 565
    close(float(margin.min()), -0.218, 0.001)
    close(float(t[int(np.argmin(margin))]), 0.600, 0.001)
    cap = np.where(t >= t_ref, (1 + sm) * load, ff)        # after the reflex: 30 % above the instantaneous floor
    assert round(float(cap.max()), 2) == 12.23 and round(float(load.max()), 2) == 9.41
    P = Plot(s, (56, 52, 386, 238), (0, 1.0), (0, 16))
    o = [P.axes([(x, f"{x:.1f}") for x in (0, 0.5, 1.0)], [(y, f"{y}") for y in (0, 8, 16)], "time t (s)", "force (N)",
                grid=(8, 16), ytx=14)]
    o.append(f'<rect x="{P.X(t_slip):.2f}" y="{P.y1:.2f}" width="{P.X(t_ref) - P.X(t_slip):.2f}" height="{P.y0 - P.y1:.2f}" '
             f'fill="{BOX}"/>')
    o.append(H.line(s, P.X(t_slip), P.y0, P.X(t_slip), P.y1, I["rule"], "ref", H.DASH_REF))
    o.append(H.line(s, P.X(t_ref), P.y0, P.X(t_ref), P.y1, I["rule"], "ref", H.DASH_REF))
    o.append(P.curve(t[t >= t_ref - 0.005], ff[t >= t_ref - 0.005], I["secondary"], multi=True, dash=DASH))
    o.append(P.curve(t, load, SER[0], multi=True))
    o.append(P.curve(t, cap, SER[1], multi=True))
    o.append(P.dot(t_slip, float(np.interp(t_slip, t, load)), SER[2]))
    o.append(label(s, P.X(t_slip) - 6, P.Y(1.2) - 2, f"slip {t_slip:.3f} s", "label2", I["primary"], "end"))
    o.append(label(s, P.X(t_ref) + 6, P.Y(1.2) - 2, f"reflex {t_ref:.3f} s (+70 ms)", "label2", I["primary"]))
    o.append(label(s, P.X(0.99), P.Y(cap.max()) - 6, f"capacity peak {cap.max():.2f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.99), P.Y(3.2), f"load peak {load.max():.2f}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.02), P.Y(ff[0]) - 8, "grip capacity", "label2", I["primary"]))
    o.append(label(s, P.X(0.02), P.Y(load[0]) + 20, "load", "label2", I["primary"]))
    o.append(legend(s, 56, 18, [(SER[0], "load L", None), (SER[1], "grip capacity 2μF_g".replace("F_g", "F" + sub("g", s, "label2")), None)]))
    o.append(legend(s, 56, 40, [(I["secondary"], "no reflex: margin falls to −21.8 %", DASH)]))
    aria = ("K8 plot: force against time during a lift whose load peak, 9.41 newtons, the internal model "
            "under-predicts. The feedforward grip capacity, 2 mu F g, falls below the load at 0.488 seconds, the slip. The "
            "70 millisecond reflex lands at 0.558 seconds and resets the capacity to 30 percent above the instantaneous "
            f"load, peaking at {cap.max():.2f} newtons. A dashed curve shows the capacity without the reflex, "
            "21.8 percent short of the load at the peak.")
    hvp = hov(P, t[::8], [cap[::8], load[::8]], lambda i: f"t = {t[::8][i]:.3f} s: capacity {cap[::8][i]:.2f}, load "
                                                          f"{load[::8][i]:.2f} N, margin {margin[::8][i] * 100:.1f} % (no reflex)")
    return svg(VB, aria, s, "".join(o), (P.box, hvp))


# ================================================================ svg #49 K9: best link-length ratio
def fig49():
    VB = (0, 0, W, 290)
    s = H.Scale(W, VB[3], display_w=400)
    ltot = 0.75
    r_ = 0.6 * ltot

    def w_of(rho):
        l1 = ltot / (1 + rho)
        l2 = ltot - l1
        c = (r_ * r_ - l1 * l1 - l2 * l2) / (2 * l1 * l2)
        return l1 * l2 * math.sqrt(1 - c * c)
    rho = np.linspace(0.4, 3.0, 261)
    w = np.array([w_of(x) for x in rho])
    assert round(float(rho[int(np.argmax(w))]), 2) == 1.0 and round(w_of(1.0), 3) == 0.135
    assert round(w_of(1.5), 3) == 0.127 and round(100 * w_of(1.5) / w_of(1.0)) == 94       # line 569
    P = Plot(s, (62, 60, 386, 236), (0.4, 3.0), (0, 0.16))
    o = [P.axes([(x, f"{x:.1f}") for x in (0.5, 1.0, 1.5, 2.0, 3.0)], [(y, f"{y:.2f}") for y in (0, 0.05, 0.10, 0.15)],
                "length ratio ℓ₂/ℓ₁", "manipulability w (m²)", grid=(0.05, 0.10, 0.15), ytx=14)]
    o.append(H.line(s, P.X(1.5), P.y0, P.X(1.5), P.Y(w_of(1.5)), I["rule"], "ref", H.DASH_REF))
    o.append(P.curve(rho, w, SER[0]))
    o.append(P.dot(1.0, w_of(1.0), SER[0]))
    o.append(P.dot(1.5, w_of(1.5), SER[1]))
    o.append(label(s, P.X(0.45), P.Y(0.1505) - 16, "best ℓ₂/ℓ₁ = 1,", "label2", I["primary"]))
    o.append(label(s, P.X(0.45), P.Y(0.1505), f"w = {w_of(1.0):.3f}", "label2", I["primary"]))
    o.append(label(s, P.X(1.5) + 8, P.Y(0.1505), f"human 1.5: w = {w_of(1.5):.3f}", "label2", I["primary"]))
    o.append(label(s, P.X(1.5) + 8, P.Y(0.1505) + 16, f"{100 * w_of(1.5) / w_of(1.0):.0f} % of the optimum", "label2",
                   I["secondary"]))
    o.append(label(s, P.X(3.0), P.Y(0.045), "ℓ₁ + ℓ₂ = 0.75 m", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(3.0), P.Y(0.045) + 16, "r = 0.6 ℓtot = 0.45 m", "label2", I["secondary"], "end"))
    o.append(legend(s, 62, 24, [(SER[0], "w = ℓ₁ℓ₂ |sin θ₂|", None)]))
    aria = ("K9 plot: manipulability w against the link-length ratio at fixed total arm length 0.75 metres and a reach "
            f"of 0.45 metres. It peaks at a ratio of 1, equal links, with w = {w_of(1.0):.3f} square metres. The human "
            f"ratio of 1.5 gives {w_of(1.5):.3f}, {100 * w_of(1.5) / w_of(1.0):.0f} percent of the optimum.")
    hvp = hov(P, rho, [w], lambda i: f"ℓ₂/ℓ₁ = {rho[i]:.2f}: w = {w[i]:.4f} m²")
    return svg(VB, aria, s, "".join(o), (P.box, hvp))


# ================================================================ svg #50 K10: pinch against power grip
def fig50():
    VB = (0, 0, W, 412)
    s = H.Scale(W, VB[3], display_w=400)
    F = 30.0
    pinch = lambda m_: 2 * m_ * F                                            # noqa: E731
    power = lambda m_, b=math.pi: 2 * m_ * F * np.exp(m_ * b)               # noqa: E731
    vals = {m_: (pinch(m_), float(power(m_))) for m_ in (0.2, 0.5, 0.8)}
    assert [(round(a), round(b)) for a, b in vals.values()] == [(12, 22), (30, 144), (48, 593)]
    assert [round(math.exp(m_ * math.pi), 2) for m_ in vals][:2] == [1.87, 4.81] and round(math.exp(0.8 * math.pi), 1) == 12.3
    assert round(float(power(0.5, math.pi / 2))) == 66 and round(float(power(0.5, 1.5 * math.pi))) == 317
    assert round(float(power(0.2)), 1) == 22.5
    ymax = 800.0
    P = Plot(s, (56, 130, 386, 318), (0.1, 0.85), (0, ymax))
    mu = np.linspace(0.1, 0.85, 121)

    def clip(b):
        y = power(mu, b)
        k = int(np.argmax(y > ymax)) if (y > ymax).any() else len(mu)
        return mu[:k], y[:k]
    o = [P.axes([(x, f"{x}") for x in (0.2, 0.5, 0.8)], [(y, f"{y}") for y in (0, 200, 400, 600, 800)],
                "friction coefficient μ", "heaviest object held (N)", grid=(200, 400, 600, 800), ytx=14)]
    o.append(P.curve(*clip(math.pi / 2), SER[2], multi=True, dash=DASH))
    o.append(P.curve(*clip(1.5 * math.pi), I["secondary"], multi=True, dash=DASH))
    o.append(P.curve(mu, pinch(mu), SER[1]))
    o.append(P.curve(mu, power(mu), SER[0]))
    for m_, (a, b) in vals.items():
        o.append(P.dot(m_, a, SER[1]))
        o.append(P.dot(m_, b, SER[0]))
    o.append(P.dot(0.5, float(power(0.5, math.pi / 2)), SER[2]))
    o.append(P.dot(0.5, float(power(0.5, 1.5 * math.pi)), I["secondary"]))
    o.append(label(s, P.X(0.575) - 8, P.Y(785) + 4, "β = 3π/2", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.85), P.Y(float(power(0.85, math.pi / 2))) - 10, "β = π/2", "label2", I["primary"], "end"))
    o.append(legend(s, 56, 18, [(SER[0], "power grip, β = π", None), (SER[1], "pinch 2μF", None)]))
    o.append(legend(s, 56, 38, [(SER[2], "β = π/2", DASH), (I["secondary"], "β = 3π/2", DASH)]))
    o.append(label(s, 386, 18, "F = 30 N", "label2", I["secondary"], "end"))
    for k, txt in enumerate(("μ = 0.2: pinch 12 N, power 22.5 N (× 1.9)",
                             "μ = 0.5: pinch 30 N, power 144 N (× 4.8) at β = π;",
                             "   66 N at β = π/2, 317 N at β = 3π/2",
                             "μ = 0.8: pinch 48 N, power 593 N (× 12.3)")):
        o.append(label(s, 56, 58 + 16 * k, txt, "label2", I["secondary"]))
    # inset: the seated hand with a cup (Lynch body kit)
    bx = (62, 150, 186, 250)
    Pm = LB.pose(near=dict(hip=90, knee=90, shoulder=30, elbow=60), far=dict(hip=90, knee=90, shoulder=30, elbow=60))
    sv, J, _ = fit(Pm, s, bx, "right")
    o += [chair(s, J), floor(s, bx[0], bx[2], J["floor_y"]), sv, cup(s, J["fingertip"][0] + 8, J["fingertip"][1] + 8, 14)]
    o.append(LB.credit(s, 4, 380, width=392))
    aria = ("K10 plot: the heaviest object held against the friction coefficient for a maximum squeeze of 30 newtons. "
            "The pinch, 2 mu F, is a straight line: 12, 30 and 48 newtons at mu 0.2, 0.5 and 0.8. The power grip with a "
            "half-wrap of pi, 2 mu F exp(mu pi), rises exponentially: 22.5, 144 and 593 newtons. At mu 0.5 a wrap of "
            "pi over 2 gives 66 newtons and a wrap of 3 pi over 2 gives 317. A seated skeleton holding a cup sits at left.")
    hvp = hov(P, mu, [power(mu), pinch(mu)], lambda i: f"μ = {mu[i]:.2f}: power {power(mu[i]):.1f} N, pinch "
                                                       f"{pinch(mu[i]):.1f} N")
    return svg(VB, aria, s, "".join(o), (P.box, hvp))


FIGS = {
    9: ("Elbow torque during a wave over two seconds, split into its ", fig9),
    12: ("Grip force and load force over a lift, rising together in pa", fig12),
    16: ("Elbow torque over two seconds of waving, at 1.5 Hz and 3 Hz,", fig16),
    18: ("Left: grip force per pad versus friction coefficient, a hype", fig18),
    25: ("C5: the taped thumb. Tape a person's thumb flat against the ", fig25),
    35: ("D5: force ellipsoid $\\perp$ velocity ellipsoid. Show that th", fig35),
    41: ("K1: the cost of the last centimetre (sensitivity sweep). A s", fig41),
    42: ("K2: inertial vs gravitational torque (regime comparison + ro", fig42),
    48: ("K8: a slip and its reflex (event-driven simulation). Simulat", fig48),
    49: ("K9: the best link-length ratio (design optimisation). Holding", fig49),
    50: ("K10: pinch versus power grip (capstan-amplified regime compa", fig50),
}
