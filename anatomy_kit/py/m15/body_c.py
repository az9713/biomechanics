"""Module 15 problem figures, group `body_c` (svg #29 30 31 32 33 37 38 39 40 41 48 50 53), 400 px wide.

Numbers (module15.html line numbers):
  #29 C7   Lab D data (lines 679-685, seed 15): cameras = a_true + N(0, 0.12), plate = F_y/70 - g, F_y noise 2.5 N.
  #30 C8   marker noise: 1.70 N m unfiltered, 0.07 filtered (K4, seed 15, line 886); parameter error: the linearised pooled
           RMS u sqrt(<(I q'')^2 + (m g l sin q)^2>) at u = 15 % (line 537), on the raw and on the 6 Hz filtered angle.
  #31 C9   the synthetic joint of Section 7 (line 464); the EMG trace is illustrative (the text gives no EMG numbers).
  #32 C10  static hold: tau = m g l (line 759); arm COM from the Winter fractions of the kit.
  #33 D1   Definition 2.1 angles computed from the drawn pose; delta theta = eps / d (line 765).
  #37 D5   Winter mass fractions of the kit (head 0.081, trunk 0.497, arm 0.050, thigh 0.100, shank 0.0465, foot 0.0145).
  #38 D6   Proposition 5.1, a mid-squat pose.
  #39 D7, #40 D8  the shank instance of line 448 (m 3.3 kg, I 0.048, 0.40 m, a_c (0.4, 1.2), alpha 3.0, F_d (15, 690),
           M_d -8, shank at 75 deg): F_p (-13.7, -653.7) N, M_p = 72.4 N m.
  #41 D9   Proposition 8.1 terms for the synthetic joint at 15 % parameter error and 0.006 rad marker noise, 6 Hz filter.
  #48 K4   Section 7 listing: 0.07, 1.70, 3.31 and 6.68 N m (lines 468, 886).
  #50 K6   Proposition 6.1 for foot and shank (symbols; the text gives no foot numbers).
  #53 K8   Lab D listing (lines 679-701): 70.03 kg at N = 20, 70.00 at 200, s.e. 0.19 to 0.06 kg.
This file does NOT expose SHARED_DEFS: the Lynch kit art comes from m15/body_main.py (`<use href="#hbody_...">`).
"""
import html
import math

import numpy as np

import house as H
import lynch_body as LB
from m05.body import it
from m05.plots_prob import Plot, hov, label, legend
from m15.plots_main import (DT, G, IZ, LL, MZ, Q_TRUE, QDD_TRUE, SIG, TAU_TRUE, TRIM, TT, identify, lab_d_data,
                            pipeline_run, rmse, smooth)

O, I, T, SER = H.OVERLAY, H.INK, H.TISSUE, H.SERIES
RED, BLUE, ORANGE, GREEN = SER
GRID, BOX = "#e6e6e6", "#f7f4ef"
W = 400
BODY = H.MAX_DISPLAY_H_BODY


def mn(v, f="{:.2f}"):
    t = f.format(v)
    return "−" + t[1:] if t.startswith("-") else t


def sc(w, h, body=False):
    return H.Scale(w, h, display_w=400, max_h=BODY if body else H.MAX_DISPLAY_H)


def done(vb, aria, s, body, hover=None):
    """Close a figure: H.svg_open + body + hover. Unused arrow markers are dropped."""
    import re
    b = "".join(body)
    b = re.sub(r'<marker id="([^"]+)".*?</marker>', lambda m: m.group(0) if f"url(#{m.group(1)})" in b else "", b)
    b = b.replace("<defs></defs>", "")
    ex = H.hover_attr(*hover) if hover else ""
    return H.svg_open(vb, html.escape(aria), s, extra=ex) + b + "</svg>"


# ================================================================ svg #29  C7: two instruments, one acceleration
def fig29():
    VB = (0, 0, W, 318)
    s = sc(W, VB[3])
    t, a_true, fy, a_kin = lab_d_data()
    a_plate = fy / 70.0 - G
    res = float(np.sqrt(np.mean((a_kin - a_plate) ** 2)))
    assert abs(res - 0.129) < 0.002 and abs(np.abs(a_true).max() - 1.7) < 0.05                    # Lab D, Section 5 (line 405)
    P = Plot(s, (58, 66, 388, 232), (0, 2), (-2, 2))
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2)], [(-2, "−2"), (-1, "−1"), (0, "0"), (1, "1"), (2, "2")],
                "time (s)", "COM acceleration (m/s²)", grid=(-1, 0, 1))]
    o.append(P.curve(t, a_kin, RED, multi=True, nmax=400))
    o.append(P.curve(t, a_plate, BLUE, multi=True, nmax=400))
    o.append(legend(s, 58, 20, [(RED, "cameras: twice-differentiated segment COM", None)]))
    o.append(legend(s, 58, 40, [(BLUE, "force plate: F" + H.sub("y", s, "label2") + "/M − g", None)]))
    o.append(label(s, 58, 294, "two independent instruments:", "label2", I["secondary"]))
    o.append(label(s, 58, 310, f"RMS gap {res:.3f} m/s² on a peak of {np.abs(a_true).max():.1f} m/s²", "label2", I["secondary"]))
    hv = hov(P, t, [a_kin, a_plate], lambda i: f"t = {t[i]:.2f} s: cameras {mn(a_kin[i])}, force plate {mn(a_plate[i])} m/s²")
    aria = ("Problem C7 plot. The vertical acceleration of the body centre of mass during a two-second squat, found two ways: from "
            "the cameras (twice-differentiated segment centres, red) and from the force plate as Fy over M minus g (blue). The "
            f"two curves overlay between minus 1.7 and plus 1.7 metres per second squared, with an RMS gap of {res:.2f}.")
    return done(VB, aria, s, o, (P.box, hv))


# ================================================================ svg #30  C8: the error filtering cannot touch
def fig30():
    VB = (0, 0, W, 300)
    s = sc(W, VB[3])
    qf = smooth(Q_TRUE, 6.0)
    qdd_f = np.gradient(np.gradient(qf, DT), DT)

    def bsp(q, qdd):                                   # line 537: u sqrt(<(I q'')^2 + (m g l sin q)^2>) at u = 15 %
        return 0.15 * float(np.sqrt(np.mean(((IZ * qdd) ** 2 + (MZ * G * LL * np.sin(q)) ** 2)[TRIM])))
    bsp_raw, bsp_fil = bsp(Q_TRUE, QDD_TRUE), bsp(qf, qdd_f)
    filt, raw = pipeline_run()
    mk_fil, mk_raw = rmse(filt, TAU_TRUE), rmse(raw, TAU_TRUE)
    assert abs(mk_fil - 0.07) < 0.005 and abs(mk_raw - 1.70) < 0.005 and abs(bsp_fil - 0.415) < 0.002 and abs(bsp_raw - 0.415) < 0.002
    P = Plot(s, (58, 82, 388, 232), (0, 4), (0, 2))
    o = [P.axes([], [(0, "0"), (0.5, "0.5"), (1, "1"), (1.5, "1.5"), (2, "2")], "", "RMS torque error (N m)", grid=(0.5, 1, 1.5, 2))]
    groups = (("marker noise", mk_raw, mk_fil), ("15% mass and inertia error", bsp_raw, bsp_fil))
    pts = []
    bw = 50
    for g, (nm, vr, vf) in enumerate(groups):
        cx = P.X(1 + 2 * g)
        for j, (v, col, what) in enumerate(((vr, ORANGE, "unfiltered"), (vf, BLUE, "filtered, 6 Hz"))):
            x0 = cx + (j - 1) * bw - (4 if j == 0 else -4)
            o.append(f'<rect x="{x0:.2f}" y="{P.Y(v):.2f}" width="{bw}" height="{P.y0 - P.Y(v):.2f}" fill="{col}"/>')
            o.append(label(s, x0 + bw / 2, P.Y(v) - 6, f"{v:.2f}", "label2", I["primary"], "middle"))
            pts.append([x0 + bw / 2, P.Y(v), f"{nm}, {what}: RMS torque error {v:.3f} N m"])
    o.append(label(s, P.X(1), P.y0 + 20, "marker noise", "label", I["primary"], "middle"))
    o.append(label(s, P.X(3), P.y0 + 20, "mass and inertia", "label", I["primary"], "middle"))
    o.append(label(s, P.X(3), P.y0 + 38, "error of 15%", "label", I["primary"], "middle"))
    o.append(legend(s, 58, 20, [(ORANGE, "unfiltered", None), (BLUE, "filtered, 6 Hz", None)]))
    o.append(label(s, 58, 40, "marker error falls 24-fold (1.70 to 0.07);", "label2", I["secondary"]))
    o.append(label(s, 58, 56, "the parameter error does not move", "label2", I["secondary"]))
    pts.sort(key=lambda p: p[0])
    hv = (P.box, [[a, b, c] for a, b, c in pts])
    aria = ("Problem C8 bar chart of RMS torque error for the synthetic joint, each source alone, unfiltered in orange and filtered at "
            f"6 hertz in blue. Marker noise: {mk_raw:.2f} newton metres unfiltered and {mk_fil:.2f} filtered. A 15 percent error in "
            f"segment mass and inertia: {bsp_raw:.2f} unfiltered and {bsp_fil:.2f} filtered, the same bar height.")
    return done(VB, aria, s, o, hv)


# ================================================================ svg #31  C9: EMG timing checks the torque
def fig31():
    VB = (0, 0, W, 356)
    s = sc(W, VB[3])
    t = TT[TRIM]
    tau = TAU_TRUE[TRIM]
    lead = 0.08                                           # illustrative lead of the EMG envelope, s (the text gives none)
    tt = np.arange(-1, 3, DT)
    q = 0.40 * np.sin(2 * np.pi * 0.8 * tt)
    tau_ext = IZ * (-0.40 * (2 * np.pi * 0.8) ** 2 * np.sin(2 * np.pi * 0.8 * tt)) + MZ * G * LL * np.sin(q)
    env = np.maximum(np.interp(t + lead, tt, tau_ext), 0.0) / TAU_TRUE.max()
    zc = [float(TT[k]) for k in np.where(np.diff(np.sign(TAU_TRUE)) != 0)[0]]      # 0.00, 0.62, 1.25, 1.87
    A = Plot(s, (58, 50, 388, 150), (0, 2), (-4.5, 4.5))
    B = Plot(s, (58, 186, 388, 266), (0, 2), (0, 1.15))
    xt = [(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2)]
    o = []
    for lo, hi in ((0.0, 0.62), (1.25, 1.87)):                           # tau > 0 : the extensors must act
        o.append(f'<rect x="{A.X(lo):.2f}" y="{A.y1}" width="{A.X(hi) - A.X(lo):.2f}" height="{B.y0 - A.y1}" fill="{BOX}"/>')
    o.append(A.axes([], [(-4, "−4"), (0, "0"), (4, "4")], "", "torque (N m)", grid=(0,)))
    o.append(B.axes(xt, [(0, "0"), (1, "1")], "time (s)", "EMG (a.u.)", grid=()))
    o.append(A.curve(t, tau, RED, multi=True))
    o.append(B.curve(t, env, GREEN, multi=True))
    o.append(legend(s, 58, 18, [(RED, "computed joint torque τ", None)]))
    o.append(legend(s, 58, 36, [(GREEN, "extensor EMG envelope (illustrative)", None)]))
    o.append(label(s, A.X(0.31), A.Y(0) - 10, "τ > 0", "label2", I["secondary"], "middle"))
    o.append(label(s, A.X(1.56), A.Y(0) - 10, "τ > 0", "label2", I["secondary"], "middle"))
    o.append(label(s, A.X(0.935), A.Y(0) + 22, "τ < 0", "label2", I["secondary"], "middle"))
    # EMG onset leads the torque onset (second burst)
    on = zc[2]
    o.append(H.line(s, A.X(on), A.y1, A.X(on), B.y0, I["rule"], "leader", H.DASH_REF))
    o.append(H.arrow(s, "m15f31_", B.X(on), B.Y(0.2), B.X(on - lead), B.Y(0.2), "dim", w="ref"))
    o.append(label(s, B.X(on - lead) - 6, B.Y(0.2) + 4, "EMG leads", "label2", I["primary"], "end"))
    o.append(label(s, 58, 330, "a computed extensor torque while the", "label2", I["secondary"]))
    o.append(label(s, 58, 346, "EMG is silent would be a contradiction", "label2", I["secondary"]))
    o.insert(0, f'<defs>{H.markers("m15f31_", s)}</defs>')
    pts = [[A.X(x), [A.Y(a), B.Y(b)], f"t = {x:.2f} s: torque {mn(a)} N m, EMG {b:.2f} (arbitrary units)"] for x, a, b in zip(t, tau, env)]
    hv = ([(A.box, [[a, b[0], c] for a, b, c in pts]), (B.box, [[a, b[1], c] for a, b, c in pts])])
    aria = ("Problem C9 plot, two panels over two seconds on one time axis. Top: the computed joint torque of the synthetic joint in "
            "red, positive from 0 to 0.62 seconds and from 1.25 to 1.87 seconds, negative between. Bottom: an illustrative rectified "
            "and smoothed extensor EMG envelope in green that bursts only while the torque is positive and begins slightly before "
            "it; an arrow marks the lead. The EMG is not a calibrated force, it is a timing and sign check.")
    return done(VB, aria, s, o, (hv,))


# ================================================================ svg #41  D9: the terms of Var(tau)
def fig41():
    VB = (0, 0, W, 330)
    s = sc(W, VB[3])
    qf = smooth(Q_TRUE, 6.0)
    qdd = np.gradient(np.gradient(qf, DT), DT)
    rng = np.random.default_rng(15)
    dq = np.array([np.gradient(np.gradient(smooth(Q_TRUE + rng.normal(0, SIG, TT.size), 6.0), DT), DT) - qdd for _ in range(400)])
    rms = lambda v: float(np.sqrt(np.mean(v[..., TRIM] ** 2)))                                  # noqa: E731
    terms = [("inertia", "∂τ/∂I", "= q″", 0.15 * IZ * rms(qdd)),
             ("mass", "∂τ/∂m", "= gℓ sin q", 0.15 * MZ * G * LL * rms(np.sin(qf))),
             ("acceleration", "∂τ/∂q″", "= I", IZ * rms(dq))]
    tot = math.sqrt(sum(v * v for *_, v in terms))
    assert abs(terms[1][3] - 0.411) < 0.003 and abs(tot - 0.42) < 0.005                         # lines 537, 489: 0.414 and 0.059 in quadrature
    P = Plot(s, (58, 60, 388, 232), (0, 4), (0, 0.5))
    o = [P.axes([], [(0, "0"), (0.25, "0.25"), (0.5, "0.5")], "", "RMS torque error (N m)", grid=(0.25, 0.5))]
    pts = []
    bw = 50
    for k, (nm, d1, d2, v) in enumerate(terms + [("total", "√(Σ terms²)", "", tot)]):
        cx = P.X(k + 0.5)
        col = BLUE if k < 3 else I["secondary"]
        o.append(f'<rect x="{cx - bw / 2:.2f}" y="{P.Y(v):.2f}" width="{bw}" height="{P.y0 - P.Y(v):.2f}" fill="{col}"/>')
        o.append(label(s, cx, P.Y(v) - 6, f"{v:.2f}", "label2", I["primary"], "middle"))
        o.append(label(s, cx, P.y0 + 19, nm, "label2", I["primary"], "middle"))
        o.append(label(s, cx, P.y0 + 36, d1, "label2", I["secondary"], "middle"))
        if d2:
            o.append(label(s, cx, P.y0 + 52, d2, "label2", I["secondary"], "middle"))
        pts.append([cx, P.Y(v), f"{nm}: {v:.3f} N m RMS" + ("" if k == 3 else f" ({d1} {d2})")])
    o.append(label(s, 58, 20, "each partial times its input error, RMS over the 2 s trial:", "label2", I["primary"]))
    o.append(label(s, 58, 38, "15% on I, 15% on m, 0.006 rad marker noise at 6 Hz", "label2", I["secondary"]))
    aria = ("Problem D9 bar chart of the terms of the torque variance for the synthetic joint, as RMS torque error in newton metres: "
            f"inertia error 0.15 times I times q-double-dot, {terms[0][3]:.2f}; mass error 0.15 times m g l sin q, {terms[1][3]:.2f}; "
            f"acceleration noise I times its standard deviation, {terms[2][3]:.2f}; quadrature total {tot:.2f}. The mass term dominates.")
    return done(VB, aria, s, o, (P.box, pts))


# ================================================================ svg #48  K4: recover the torque, with and without filtering
def fig48():
    VB = (0, 0, W, 320)
    s = sc(W, VB[3])
    filt, raw = pipeline_run()
    e_f, e_r = rmse(filt, TAU_TRUE), rmse(raw, TAU_TRUE)
    qm = Q_TRUE + np.random.default_rng(15).normal(0, SIG, TT.size)
    cmp_ = np.zeros_like(qm)
    cmp_[1:-1] = (qm[2:] - 2 * qm[1:-1] + qm[:-2]) / DT ** 2
    e_c = rmse(IZ * cmp_ + MZ * G * LL * np.sin(qm), TAU_TRUE)
    assert abs(np.abs(TAU_TRUE).max() - 3.31) < 0.005 and abs(e_f - 0.07) < 0.005 and abs(e_r - 1.70) < 0.005 and abs(e_c - 6.68) < 0.005
    t = TT[TRIM]
    P = Plot(s, (58, 76, 388, 250), (0, 2), (-7.5, 7.5))
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2)], [(-5, "−5"), (0, "0"), (5, "5")], "time (s)", "joint torque (N m)", grid=(0,))]
    o.append(P.curve(t, raw[TRIM], ORANGE, multi=True, nmax=400))
    o.append(P.curve(t, filt[TRIM], BLUE, multi=True, nmax=400))
    o.append(P.curve(t, TAU_TRUE[TRIM], RED, multi=True, dash=(5, 3), nmax=400))
    o.append(legend(s, 58, 18, [(RED, "true torque, peak 3.31 N m", (5, 3))]))
    o.append(legend(s, 58, 36, [(BLUE, f"filtered, 6 Hz: RMSE {e_f:.2f} N m", None)]))
    o.append(legend(s, 58, 54, [(ORANGE, f"unfiltered: RMSE {e_r:.2f} N m", None)]))
    o.append(label(s, 58, 308, f"compact stencil, same data: {e_c:.2f} N m (off scale)", "label2", I["secondary"]))
    hv = hov(P, t, [TAU_TRUE[TRIM], filt[TRIM], raw[TRIM]],
             lambda i: f"t = {t[i]:.2f} s: true {mn(TAU_TRUE[TRIM][i])}, filtered {mn(filt[TRIM][i])}, unfiltered {mn(raw[TRIM][i])} N m")
    aria = ("Problem K4 plot: recovered joint torque over two seconds for the synthetic joint. The true torque is a red dashed sine "
            f"peaking at 3.31 newton metres; the blue filtered estimate lies on it with an RMS error of {e_f:.2f}; the orange "
            f"unfiltered estimate swings between about minus 6 and plus 7, an RMS error of {e_r:.2f}. The compact stencil would give "
            f"{e_c:.2f}, off the scale.")
    return done(VB, aria, s, o, (P.box, hv))


# ================================================================ svg #53  K8: the identified mass converges
def fig53():
    VB = (0, 0, W, 312)
    s = sc(W, VB[3])
    t, a_true, fy, a_kin = lab_d_data()
    ns = list(range(20, 201, 10))
    est = [identify(a_kin[:n], fy[:n]) for n in ns]
    se = [0.12 * 70.0 ** 2 / (70.0 * G) / math.sqrt(n) for n in ns]
    assert abs(est[0] - 70.03) < 0.03 and abs(est[-1] - 70.0) < 0.03 and abs(se[0] - 0.19) < 0.005 and abs(se[-1] - 0.06) < 0.005
    P = Plot(s, (64, 66, 388, 232), (20, 200), (69.5, 70.5))
    o = [P.axes([(v, str(v)) for v in (20, 60, 100, 140, 180)], [(69.5, "69.5"), (70, "70"), (70.5, "70.5")],
                "frames of data used, N", "identified mass (kg)", grid=(), ytx=14)]
    band = [(P.X(n), P.Y(70 + e)) for n, e in zip(ns, se)] + [(P.X(n), P.Y(70 - e)) for n, e in zip(ns[::-1], se[::-1])]
    o.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in band)}" fill="{BLUE}" opacity="0.2"/>')
    o.append(H.line(s, P.x0, P.Y(70), P.x1, P.Y(70), O["dim"], "ref", H.DASH_REF))
    o.append(P.curve(ns, est, RED, multi=True))
    for n, e in zip(ns, est):
        o.append(P.dot(n, e, RED))
    o.append(label(s, P.X(198), P.Y(70) + 17, "true M = 70 kg", "label2", I["primary"], "end"))
    o.append(legend(s, 64, 18, [(RED, "identified mass", None)]))
    o.append(f'<rect x="64" y="26" width="20" height="10" fill="{BLUE}" opacity="0.25"/>')
    o.append(label(s, 89, 36, "±1 predicted s.e. σ" + H.sub("a", s, "label2") + "M/(g√N)", "label2", I["secondary"]))
    o.append(label(s, 64, 296, f"s.e. {se[0]:.2f} kg at N = 20, {se[-1]:.2f} kg at N = 200", "label2", I["secondary"]))
    hv = hov(P, ns, [est], lambda i: f"N = {ns[i]} frames: identified {est[i]:.2f} kg, s.e. {se[i]:.2f} kg")
    aria = ("Problem K8 plot: the identified body mass against the number of frames used, from 20 to 200. Red dots joined by a line "
            f"sit at {est[0]:.2f} kilograms at 20 frames and {est[-1]:.2f} at 200, inside a blue band of one predicted standard "
            "error that narrows from 0.19 to 0.06 kilogram. A dashed line marks the true 70 kilograms.")
    return done(VB, aria, s, o, (P.box, hv))


# ================================================================ drawing helpers for the body figures
def white_under(s, x1, y1, x2, y2, w=4):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#fff" '
            f'stroke-width="{s(w):.2f}" opacity="0.85"/>')


def dline(s, x1, y1, x2, y2, col=None, w="ref", dash=H.DASH_REF):
    return white_under(s, x1, y1, x2, y2) + H.line(s, x1, y1, x2, y2, col or O["dim"], w, dash=dash)


def leader(s, x1, y1, x2, y2, col=None):
    return H.line(s, x1, y1, x2, y2, col or I["secondary"], "leader")


def mark(s, x, y, col=None, r=5.0):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{col or O["geometry"]}" stroke="#fff" '
            f'stroke-width="{s(1.5):.2f}"/>')


def arc_pts(cx, cy, r, a0, a1, n=28):
    """Screen angles in degrees: 0 = +x, + = clockwise (y down)."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def path_d(pts):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def arc_arrow(s, p, cx, cy, r, a0, a1, meaning, w=None):
    w = w or {"geometry": "geom", "dim": "ref"}.get(meaning, "force")
    return (f'<path d="{path_d(arc_pts(cx, cy, r, a0, a1))}" fill="none" stroke="{O[meaning]}" '
            f'stroke-width="{s(H.PX[w]):.2f}" marker-end="url(#{p}a_{meaning})"/>')


def arc_plain(s, cx, cy, r, a0, a1, col, w="geom"):
    return (f'<path d="{path_d(arc_pts(cx, cy, r, a0, a1))}" fill="none" stroke="{col}" stroke-width="{s(H.PX[w]):.2f}"/>')


def box(s, x, y, w, h, fill=BOX, stroke=None, rx=4.0):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{s(rx):.2f}" fill="{fill}" '
            f'stroke="{stroke or I["secondary"]}" stroke-width="{s(1.0):.2f}"/>')


def plate(s, x0, x1, y, h=12.0):
    return box(s, x0, y, x1 - x0, s(h), fill=GRID, stroke=I["secondary"], rx=1.5)


def grf_arrow(s, p, x, y, length):
    return white_under(s, x, y, x, y - length, 5) + H.arrow(s, p, x, y, x, y - length, "force")


def rows(s, x, y, texts, size="label2", fill=None, dy=None):
    dy = dy or s(H.PX[size] * 1.45)
    return "".join(H.label(s, x, y + i * dy, t, size, fill or I["primary"]) for i, t in enumerate(texts))


def ang_deg(v):
    """Lab angle of a vector given in SCREEN coordinates (y down): atan2(y up, x), degrees."""
    return math.degrees(math.atan2(-v[1], v[0]))


def fmt(v, n=0):
    return f"{v:.{n}f}".replace("-", "−")


def bodyscale(w, h):
    return sc(w, h, True)


# ================================================================ svg #32  C10: the static hold returns m g l
def fig32():
    p = "m15f32_"
    VB = (0, 0, 400, 500)
    s = bodyscale(VB[2], VB[3])
    fy, hgt = 410.0, 360.0
    P = LB.pose(near=dict(shoulder=90, elbow=0), anchor=("heel", "near"))
    body, J = LB.draw(p, s, P, 100.0, fy, hgt)
    segs = ("upper_arm", "forearm", "hand")
    ms = [LB.WINTER[k]["mass_frac"] for k in segs]
    cx = sum(m * J["com_" + k][0] for m, k in zip(ms, segs)) / sum(ms)
    cy = sum(m * J["com_" + k][1] for m, k in zip(ms, segs)) / sum(ms)
    sx, sy = J["shoulder"]
    o = [f"<defs>{H.markers(p, s)}</defs>", H.line(s, 20, fy, 250, fy, I["rule"], "axis"), body]
    o.append(H.joint_centre(s, sx, sy))
    # weight at the arm COM, dimension l below the arm, torque at the shoulder
    wl = 84.0
    o.append(white_under(s, cx, cy, cx, cy + wl, 5))
    o.append(H.arrow(s, p, cx, cy, cx, cy + wl, "load"))
    o.append(H.com_mark(s, cx, cy))
    o.append(H.label(s, cx + s(10), cy + wl - s(6), it("m g"), "label", I["primary"]))
    dy_ = cy + 62.0
    o.append(dline(s, sx, sy + s(8), sx, dy_ + s(6), O["geometry"]))
    o.append(H.arrow(s, p, sx + s(3), dy_, cx - s(2), dy_, "geometry", both=True))
    o.append(H.label(s, (sx + cx) / 2, dy_ - s(8), it("ℓ"), "label", I["primary"], "middle"))
    o.append(arc_arrow(s, p, sx, sy, s(34), -10, -115, "force"))
    o.append(H.label(s, sx + s(30), sy - s(44), f"{it('τ')} = {it('m g ℓ')}", "label", I["primary"]))
    o.append(H.label(s, cx + s(14), cy + s(22), "arm COM", "label2", I["primary"]))
    o.append(rows(s, 232, 30, ["static hold:", "a = 0 and α = 0,", "so τ = m g ℓ", "with no differentiation"]))
    o.append(LB.credit(s, 20, 448, width=370))
    aria = ("A person held still, drawn as a skeleton in side view facing right, with one arm stretched straight out forward and "
            "horizontal. A black-and-white mark shows the centre of mass of the arm; a brown arrow m g runs down from it. A blue "
            "dimension line ℓ runs along the arm from the shoulder joint to the point under the arm centre of mass, and a red "
            "arc at the shoulder is the muscle torque, τ = m g ℓ, that balances the weight. The notes say a = 0 and α = 0, so "
            "nothing is differentiated.")
    return done(VB, aria, s, o)


# ================================================================ svg #33  D1: a segment angle from two markers
def fig33():
    p = "m15f33_"
    VB = (0, 0, 400, 590)
    s = bodyscale(VB[2], VB[3])
    fy, hgt = 360.0, 340.0
    leg = dict(hip=40.0, knee=75.0)
    P = LB.pose(near=dict(leg), far=dict(leg), anchor=("heel", "near"))
    body, J = LB.draw(p, s, P, 64.0, fy, hgt)
    hip, kn, an = J["hip"], J["knee"], J["ankle"]
    th_sh = ang_deg((an[0] - kn[0], an[1] - kn[1]))
    th_th = ang_deg((kn[0] - hip[0], kn[1] - hip[1]))
    q = th_th - th_sh
    o = [f"<defs>{H.markers(p, s)}</defs>", body]
    # the shank vector (distal minus proximal) with its components, and the angle from +x
    o.append(dline(s, kn[0], kn[1], kn[0] + 90, kn[1], I["rule"]))
    o.append(dline(s, an[0], an[1], kn[0], an[1], O["dim"]))
    o.append(dline(s, kn[0], kn[1], kn[0], an[1], O["dim"]))
    o.append(white_under(s, kn[0], kn[1], an[0], an[1], 5))
    o.append(H.arrow(s, p, kn[0], kn[1], an[0], an[1], "geometry"))
    o.append(arc_plain(s, kn[0], kn[1], 40, 0, -th_sh, O["geometry"]))
    for pt in (kn, an, hip):
        o.append(mark(s, pt[0], pt[1], r=6.0))
    o.append(H.label(s, kn[0] + 46, kn[1] + 40, f"{it('θ')}{H.sub('shank', s)}", "label", I["primary"]))
    o.append(H.label(s, kn[0] + 12, kn[1] - 14, "proximal marker (knee)", "label2", I["primary"]))
    o.append(H.label(s, an[0] - 4, an[1] + 40, "distal marker (ankle)", "label2", I["primary"]))
    o.append(H.label(s, (an[0] + kn[0]) / 2, an[1] + 18, "Δx", "label2", I["secondary"], "middle"))
    o.append(H.label(s, kn[0] + 8, (an[1] + kn[1]) / 2 + 4, "Δy", "label2", I["secondary"]))
    o.append(H.label(s, kn[0] + 94, kn[1] + 4, "lab x", "label2", I["secondary"]))
    # right column
    xr = 232.0
    o.append(box(s, xr - 12, 24, 176, 128))
    o.append(rows(s, xr, 46, ["Δ = distal − proximal", f"{it('θ')} = atan2(Δy, Δx)",
                              f"{it('θ')}{H.sub('shank', s, 'label2')} = {fmt(th_sh)}°,  "
                              f"{it('θ')}{H.sub('thigh', s, 'label2')} = {fmt(th_th)}°",
                              f"knee {it('q')} = {it('θ')}{H.sub('thigh', s, 'label2')} − {it('θ')}{H.sub('shank', s, 'label2')}",
                              f"= {fmt(q)}°"], dy=s(21)))
    # ill-conditioning inset: the marker error eps becomes an angle error eps / d
    eps, iy0 = 7.0, 430.0
    o.append(H.label(s, 20, iy0 - 14, "when the markers are close, a marker error ε", "label2", I["primary"]))
    o.append(H.label(s, 20, iy0 + 3, "becomes a large angle error:  δθ ≈ ε/d", "label2", I["primary"]))
    for d, x0 in ((120.0, 40.0), (34.0, 250.0)):
        y0 = iy0 + 46
        a = math.asin(eps / d)
        o.append(f'<circle cx="{x0 + d:.2f}" cy="{y0:.2f}" r="{eps:.2f}" fill="{O["geometry"]}" fill-opacity="0.18" '
                 f'stroke="{O["geometry"]}" stroke-width="{s(1.0):.2f}"/>')
        for sg in (1, -1):
            o.append(H.line(s, x0, y0, x0 + 1.2 * d * math.cos(a), y0 - sg * 1.2 * d * math.sin(a), I["rule"], "leader"))
        o.append(mark(s, x0, y0, r=4.0))
        o.append(H.label(s, x0 + d / 2, y0 + 30, f"d = {d:.0f}:  δθ ≈ {math.degrees(eps / d):.0f}°", "label2", I["primary"], "middle"))
    o.append(LB.credit(s, 20, 530, width=370))
    aria = ("A person with the hips and knees flexed, drawn as a skeleton in side view facing right. Blue marker discs sit at the hip, "
            "knee and ankle. A blue arrow runs from the proximal knee marker to the distal ankle marker with dashed horizontal "
            f"and vertical legs Δx and Δy and an arc from the horizontal giving the shank angle, {fmt(th_sh)} degrees. A box states "
            f"θ = atan2(Δy, Δx), the thigh angle {fmt(th_th)} degrees and the knee angle q, the difference, {fmt(q)} degrees. "
            "Below, two marker pairs each with a marker error disc: the pair far apart has a small angle error and the "
            "close pair a large one, δθ ≈ ε/d.")
    return done(VB, aria, s, o)


# ================================================================ svg #37  D5: the COM is a mass-weighted mean
def fig37():
    p = "m15f37_"
    VB = (0, 0, 400, 560)
    s = bodyscale(VB[2], VB[3])
    fy, hgt = 440.0, 380.0
    body, J = LB.standing_full(p, s, 130.0, fy, hgt)
    Wn = {k: v["mass_frac"] for k, v in LB.WINTER.items()}
    # (label, kit key of the near segment, mass fraction represented: both sides for the limbs)
    parts = [("head", "head", Wn["head_neck"]), ("trunk", "trunk", Wn["pelvis_trunk"]),
             ("upper arms (2)", "upper_arm", 2 * Wn["upper_arm"]), ("forearms (2)", "forearm", 2 * Wn["forearm"]),
             ("hands (2)", "hand", 2 * Wn["hand"]), ("thighs (2)", "thigh", 2 * Wn["thigh"]),
             ("shanks (2)", "shank", 2 * Wn["shank"]), ("feet (2)", "foot", 2 * Wn["foot"])]
    total = sum(f for *_, f in parts)
    assert abs(total - 1.0) < 1e-9                                                         # sum f_i = 1
    o = [H.line(s, 20, fy, 250, fy, I["rule"], "axis"), body]
    rad = {k: s(30 * math.sqrt(f)) for _, k, f in parts}
    for _, k, f in parts:
        x, y = J["com_" + k]
        o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{rad[k]:.2f}" fill="{I["secondary"]}" fill-opacity="0.55" '
                 f'stroke="#fff" stroke-width="{s(1.2):.2f}"/>')
    cx, cy = J["com"]
    o.append(H.com_mark(s, cx, cy))
    o.append(leader(s, cx - s(9), cy + s(2), 62, cy + 26))
    o.append(H.label(s, 60, cy + 30, "COM", "label2", I["primary"], "end"))
    ly, last = {}, -99.0
    for nm, k, _ in sorted(parts, key=lambda a: J["com_" + a[1]][1]):
        y = max(J["com_" + k][1] + 4, last + 20)
        ly[nm], last = y, y
    for nm, k, f in parts:
        x, y = J["com_" + k]
        o.append(leader(s, x + rad[k] + s(2), y, 250, ly[nm] - 5))
        o.append(H.label(s, 256, ly[nm], f"{nm}  {f:.3f}", "label2", I["primary"]))
    yl = ly["feet (2)"] + 14
    o.append(H.line(s, 256, yl, 392, yl, I["rule"], "leader"))
    o.append(H.label(s, 256, yl + 18, f"Σ {it('f')}{H.sub('i', s, 'label2')} = {total:.3f}", "label2", I["primary"]))
    o.append(rows(s, 20, 32, [f"{it('r')}{H.sub('COM', s)} = Σ {it('f')}{H.sub('i', s)} {it('r')}{H.sub('c,i', s)}"], size="label"))
    o.append(rows(s, 20, 54, [f"disc area ∝ {it('f')}{H.sub('i', s, 'label2')}; the total mass M cancels"], size="label2", fill=I["secondary"]))
    o.append(LB.credit(s, 20, 492, width=370))
    aria = ("A standing person in side view facing right, drawn as a skeleton inside the body outline, standing on the floor. Grey "
            "discs, each with area proportional to its mass fraction, sit at the centres of the head, trunk, upper arms, forearms, "
            "hands, thighs, shanks and feet; the trunk disc is the largest. The black-and-white mark is the whole-body centre of "
            "mass. Labels give the mass fractions: head 0.081, trunk 0.497, upper arms 0.056, forearms 0.032, hands 0.012, thighs "
            "0.200, shanks 0.093, feet 0.029, summing to 1.000. The formula is r COM = sum of f i times r c,i; the total mass M cancels.")
    return done(VB, aria, s, o)


def part_art(P, x, y, height, names, shift=None):
    """Only the near segments in `names` of pose P (placed as LB.draw places them), each optionally moved down by shift[name]."""
    k = height / LB.H_U
    ax, ay = P.anchor
    out = [f'<g transform="translate({x:.2f} {y:.2f}) scale({k:.4f} {k:.4f}) translate({-ax:.2f} {-ay:.2f})" fill="none">']
    for name, o_, th, scl, mirror, far in P.segs:
        if far or name not in names:
            continue
        tr = f"translate({o_[0]:.2f} {o_[1]:.2f})" + (f" rotate({th:.2f})" if th else "")
        out.append(f'<g transform="translate(0 {(shift or {}).get(name, 0.0) / k:.2f})"><use href="#hbody_{name}" transform="{tr}"/></g>')
    out.append("</g>")
    return "".join(out)


# ================================================================ svg #38  D6: internal forces cancel, M a = F_GRF - M g
def fig38():
    p = "m15f38_"
    VB = (0, 0, 400, 560)
    s = bodyscale(VB[2], VB[3])
    fy, hgt = 366.0, 350.0
    leg = dict(hip=78.0, knee=92.0, shoulder=35.0, elbow=15.0)
    lean = 28.0
    P = LB.pose(pelvis=lean * 0.55, trunk=lean * 0.45, near=dict(leg), far=dict(leg), anchor=("heel", "near"))
    body, J = LB.draw(p, s, P, 64.0, fy, hgt)
    mid = (J["heel"][0] + J["toe"][0]) / 2
    o = [f"<defs>{H.markers(p, s)}</defs>", plate(s, J["heel"][0] - 40, J["toe"][0] + 40, fy, 14.0), body]
    for k in ("com_head", "com_trunk", "com_upper_arm", "com_forearm", "com_hand", "com_thigh", "com_shank", "com_foot"):
        x, y = J[k]
        o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(3.2):.2f}" fill="{I["secondary"]}" stroke="#fff" stroke-width="{s(1.2):.2f}"/>')
    cx, cy = J["com"]
    o.append(H.com_mark(s, cx, cy))
    o.append(white_under(s, cx + 24, cy, cx + 24, cy + 70, 5))
    o.append(H.arrow(s, p, cx + 24, cy, cx + 24, cy + 70, "load"))
    o.append(H.label(s, cx + 30, cy + 48, it("M g"), "label", I["primary"]))
    o.append(grf_arrow(s, p, mid, fy, 96.0))
    o.append(H.label(s, mid - 8, fy - 50, f"{it('F')}{H.sub('GRF', s)}", "label", I["primary"], "end"))
    o.append(leader(s, cx - 9, cy - 4, cx - 40, cy - 28))
    o.append(H.label(s, cx - 42, cy - 30, "COM", "label2", I["primary"], "end"))
    # inset: a thigh and a shank apart, with the internal force that appears twice (equal and opposite)
    P0 = LB.pose(anchor=("heel", "near"))
    y0, h0, gap = 319.0, 380.0, 44.0
    _, Jt = LB.draw(p, s, P0, 0.0, y0, h0)
    x0 = 292.0 - Jt["knee"][0]
    _, J0 = LB.draw(p, s, P0, x0, y0, h0)
    kx, ky = J0["knee"]
    o.append(part_art(P0, x0, y0, h0, ("lat_thigh", "lat_shank"), {"lat_shank": gap}))
    o.append(white_under(s, kx - 10, ky + 34, kx - 10, ky, 5))
    o.append(H.arrow(s, p, kx - 10, ky + 34, kx - 10, ky, "reaction"))
    o.append(white_under(s, kx + 10, ky + gap - 34, kx + 10, ky + gap, 5))
    o.append(H.arrow(s, p, kx + 10, ky + gap - 34, kx + 10, ky + gap, "reaction"))
    o.append(H.label(s, kx - 18, ky + 20, f"{it('F')} on thigh", "label2", I["primary"], "end"))
    o.append(H.label(s, kx + 18, ky + 32, f"−{it('F')} on shank", "label2", I["primary"]))
    o.append(rows(s, 232, 40, ["each internal force", "appears twice, equal", "and opposite:", "it cancels in the sum"]))
    o.append(box(s, 14, 392, 372, 62))
    o.append(rows(s, 26, 414, [f"Σ {it('m')}{H.sub('i', s, 'label2')} {it('a')}{H.sub('i', s, 'label2')} = {it('F')}{H.sub('GRF', s, 'label2')} − {it('M g')}",
                              f"{it('M a')}{H.sub('COM', s, 'label2')} = {it('F')}{H.sub('GRF', s, 'label2')} − {it('M g')}"], dy=s(22)))
    o.append(H.label(s, 386, 474, "arrows not to scale", "label2", I["secondary"], "end"))
    o.append(LB.credit(s, 14, 492, width=372))
    aria = ("A person in a mid-squat, drawn as a skeleton in side view facing right, on a grey force plate. Grey dots mark the segment "
            "centres of mass and the black-and-white mark is the whole-body centre of mass. A brown arrow M g runs down from it and "
            "a red arrow F GRF runs up from the plate, drawn longer. At top right a thigh and a shank, drawn apart, carry a pair of "
            "equal and opposite black arrows, F on the thigh and minus F on the shank: an internal force that appears twice and "
            "cancels in the sum. A box gives the sum over segments, sum of m i a i equals F GRF minus M g, and M a COM equals F GRF "
            "minus M g.")
    return done(VB, aria, s, o)


# ================================================================ the shank instance of line 448 (svg #39, #40)
M_SEG, I_SEG, L_SEG = 3.3, 0.048, 0.40
A_C, ALPHA = (0.4, 1.2), 3.0
F_D, M_D = (15.0, 690.0), -8.0
INCL, RHO = 75.0, 0.433
U_ = (math.cos(math.radians(INCL)), math.sin(math.radians(INCL)))          # ankle -> knee, lab frame (y up)
R_P = (RHO * L_SEG * U_[0], RHO * L_SEG * U_[1])
R_D = (-(1 - RHO) * L_SEG * U_[0], -(1 - RHO) * L_SEG * U_[1])
F_P = tuple(round(v, 1) for v in (M_SEG * A_C[0] - F_D[0], M_SEG * A_C[1] + M_SEG * G - F_D[1]))
cross = lambda r, f: r[0] * f[1] - r[1] * f[0]                              # noqa: E731
M_P = I_SEG * ALPHA - M_D - cross(R_D, F_D) - cross(R_P, F_P)
assert F_P == (-13.7, -653.7), F_P                                          # line 448
assert (round(cross(R_D, F_D), 2), round(cross(R_P, F_P), 2), round(M_P, 1)) == (-37.22, -27.01, 72.4)   # line 448 prints -27.00
assert (round(math.hypot(*R_P), 3), round(math.hypot(*R_D), 3)) == (0.173, 0.227)


def shank_fbd(knee, pxm):
    """The shank art inclined 75 deg (knee up and forward) with its knee at `knee` (figure units); returns art, ankle, COM."""
    Lpx = L_SEG * pxm
    d_s = (-U_[0], U_[1])
    ankle = (knee[0] + d_s[0] * Lpx, knee[1] + d_s[1] * Lpx)
    off = LB.OFF["lat_shank"]["ankle"]
    th_art = math.degrees(math.atan2(d_s[1], d_s[0]) - math.atan2(off[1], off[0]))
    art = (f'<g transform="translate({knee[0]:.2f} {knee[1]:.2f}) rotate({th_art:.2f}) scale({Lpx / math.hypot(*off):.4f})" '
           f'fill="none"><use href="#hbody_lat_shank"/></g>')
    com = (knee[0] + RHO * (ankle[0] - knee[0]), knee[1] + RHO * (ankle[1] - knee[1]))
    return art, ankle, com


def vec_arrow(s, p, head, F, kF, col="reaction"):
    """Arrow for the lab-frame vector F (N) ending at `head`; to scale kF px per N."""
    d = (F[0], -F[1])
    L = math.hypot(*d) * kF
    u = (d[0] / math.hypot(*d), d[1] / math.hypot(*d))
    tail = (head[0] - u[0] * L, head[1] - u[1] * L)
    return white_under(s, *tail, *head, 5) + H.arrow(s, p, tail[0], tail[1], head[0], head[1], col), tail


def sb(s, t, size="label2"):
    return H.sub(t, s, size)


# ================================================================ svg #39  D7: the Newton step
def fig39():
    p = "m15f39_"
    VB = (0, 0, 400, 702)
    s = bodyscale(VB[2], VB[3])
    knee = (235.0, 150.0)
    art, ankle, com = shank_fbd(knee, 620.0)
    o = [f"<defs>{H.markers(p, s)}</defs>", art, H.joint_centre(s, *knee), H.joint_centre(s, *ankle)]
    ap, tail_p = vec_arrow(s, p, knee, F_P, 0.15)
    ad, tail_d = vec_arrow(s, p, ankle, F_D, 0.15)
    o += [ap, ad]
    gl = 52.0
    o.append(white_under(s, com[0], com[1], com[0], com[1] + gl, 5))
    o.append(H.arrow(s, p, com[0], com[1], com[0], com[1] + gl, "load"))
    o.append(H.com_mark(s, *com))
    o.append(H.label(s, com[0] + 14, com[1] + gl - 2, f"{it('m g')} = {M_SEG * G:.0f} N", "label2", I["primary"]))
    o.append(H.label(s, com[0] + 14, com[1] - 8, "COM", "label2", I["primary"]))
    o.append(H.label(s, tail_p[0] - 10, tail_p[1] + 14, f"{it('F')}{sb(s, 'p', 'label')} = (−13.7, −653.7) N", "label", I["primary"], "end"))
    o.append(H.label(s, tail_p[0] - 10, tail_p[1] + 32, "unknown: the Newton step", "label2", I["secondary"], "end"))
    o.append(H.label(s, tail_d[0] + 14, tail_d[1] - 2, f"{it('F')}{sb(s, 'd', 'label')} = (15, 690) N", "label", I["primary"]))
    o.append(H.label(s, tail_d[0] + 14, tail_d[1] + 16, "known: handed up from the foot", "label2", I["secondary"]))
    o.append(H.label(s, knee[0] + 22, knee[1] + 4, "knee (proximal)", "label2", I["secondary"]))
    o.append(H.label(s, ankle[0] - 22, ankle[1] + 4, "ankle (distal)", "label2", I["secondary"], "end"))
    o.append(H.label(s, 392, 530, f"{it('F')}{sb(s, 'p')} and {it('F')}{sb(s, 'd')} to one scale;", "label2", I["secondary"], "end"))
    o.append(H.label(s, 392, 547, "m g drawn longer than its scale", "label2", I["secondary"], "end"))
    o.append(box(s, 14, 560, 372, 76))
    o.append(rows(s, 26, 582, [f"Σ{it('F')} = {it('m a')}{sb(s, 'c')}:  {it('F')}{sb(s, 'p')} + {it('F')}{sb(s, 'd')} + {it('m g')} = {it('m a')}{sb(s, 'c')}",
                               f"{it('F')}{sb(s, 'p')} = {it('m a')}{sb(s, 'c')} − {it('m g')} − {it('F')}{sb(s, 'd')}",
                               f"= (1.3, 36.3) − (15, 690) = ({fmt(F_P[0], 1)}, {fmt(F_P[1], 1)}) N"], dy=s(21)))
    o.append(LB.credit(s, 14, 650, width=372))
    aria = ("Free-body diagram of the shank for the Newton step, in a mid-squat: the shank bone drawn inclined 75 degrees to the "
            "horizontal with the knee up and forward. A black arrow F d of 15 and 690 newtons, known, points up into the ankle; a "
            "black arrow F p of minus 13.7 and minus 653.7 newtons, unknown, points down into the knee; a brown arrow m g of 32 "
            "newtons acts down at the centre of mass. A box writes the sum of forces equal to m a c, F p plus F d plus m g equals "
            "m a c, and solves F p = m a c minus m g minus F d.")
    return done(VB, aria, s, o)


# ================================================================ svg #40  D8: the Euler step
def fig40():
    p = "m15f40_"
    VB = (0, 0, 400, 760)
    s = bodyscale(VB[2], VB[3])
    knee = (240.0, 100.0)
    art, ankle, com = shank_fbd(knee, 620.0)
    o = [f"<defs>{H.markers(p, s)}</defs>", art]
    ap, tail_p = vec_arrow(s, p, knee, F_P, 0.1)
    ad, tail_d = vec_arrow(s, p, ankle, F_D, 0.1)
    o += [ap, ad]
    o.append(dline(s, com[0], com[1], knee[0], knee[1], O["geometry"]))
    o.append(dline(s, com[0], com[1], ankle[0], ankle[1], O["geometry"]))
    for c in (knee, ankle):
        o.append(H.joint_centre(s, *c))
    o.append(H.com_mark(s, *com))
    o.append(H.label(s, (com[0] + knee[0]) / 2 + 30, (com[1] + knee[1]) / 2 + 4, f"{it('r')}{sb(s, 'p')} = {math.hypot(*R_P):.3f} m", "label2", O["geometry"]))
    o.append(H.label(s, (com[0] + ankle[0]) / 2 + 30, (com[1] + ankle[1]) / 2 + 14, f"{it('r')}{sb(s, 'd')} = {math.hypot(*R_D):.3f} m", "label2", O["geometry"]))
    o.append(H.label(s, com[0] - 12, com[1] + 4, "COM", "label2", I["primary"], "end"))
    o.append(arc_arrow(s, p, knee[0], knee[1], 36, 50, -70, "force"))
    o.append(H.label(s, knee[0] + 44, knee[1] + 2, f"{it('M')}{sb(s, 'p', 'label')} = {M_P:.1f} N·m", "label", I["primary"]))
    o.append(H.label(s, knee[0] + 44, knee[1] + 19, "unknown", "label2", I["secondary"]))
    o.append(arc_arrow(s, p, ankle[0], ankle[1], 30, -90, 20, "force"))
    o.append(H.label(s, ankle[0] + 38, ankle[1] - 8, f"{it('M')}{sb(s, 'd')} = −8 N·m", "label2", I["primary"]))
    o.append(H.label(s, tail_p[0] - 8, tail_p[1] + 10, f"{it('F')}{sb(s, 'p')}", "label2", I["primary"], "end"))
    o.append(H.label(s, tail_d[0] + 10, tail_d[1] + 4, f"{it('F')}{sb(s, 'd')}", "label2", I["primary"]))
    # ledger: what makes up M_p, each term in N m
    terms = [(f"{it('I α')}", I_SEG * ALPHA), (f"− {it('M')}{sb(s, 'd')}", -M_D),
             (f"− {it('r')}{sb(s, 'd')} × {it('F')}{sb(s, 'd')}", -cross(R_D, F_D)),
             (f"− {it('r')}{sb(s, 'p')} × {it('F')}{sb(s, 'p')}", -cross(R_P, F_P))]
    assert abs(sum(v for _, v in terms) - 72.4) < 0.05
    y0 = 470.0
    o.append(H.label(s, 20, y0, f"what makes up {it('M')}{sb(s, 'p', 'label')} (N·m)", "label", I["primary"]))
    kb = 4.0
    for i, (t, v) in enumerate(terms):
        y = y0 + 28 + i * 26
        o.append(H.label(s, 20, y + 4, t, "label2", I["primary"]))
        o.append(f'<rect x="150" y="{y - 9:.2f}" width="{max(v * kb, 1.2):.2f}" height="14" fill="{O["force"]}"/>')
        o.append(H.label(s, 150 + max(v * kb, 1.2) + 6, y + 4, f"{v:.2f}", "label2", I["primary"]))
    o.append(H.label(s, 20, y0 + 28 + 4 * 26 + 6, f"{it('M')}{sb(s, 'p')} = {M_P:.1f} N·m: the force moments dominate", "label2", I["primary"]))
    o.append(LB.credit(s, 14, 700, width=372))
    aria = ("Free-body diagram of the shank for the Euler step, inclined 75 degrees with the knee up and forward. Thin black arrows "
            "F d and F p act at the ankle and knee; dashed blue moment arms r p of 0.173 metres and r d of 0.227 metres run from the "
            "centre of mass to the knee and ankle. A red arc at the knee is the unknown net moment M p of 72.4 newton metres; a red arc "
            "at the ankle is the known moment M d of minus 8. Below, horizontal bars give the terms that sum to M p: I alpha 0.14, "
            "minus M d 8.00, minus r d cross F d 37.22 and minus r p cross F p 27.00 newton metres.")
    return done(VB, aria, s, o)


# ================================================================ svg #50  K6: the two-segment recursion, foot then shank
def fig50():
    p = "m15f50_"
    VB = (0, 0, 400, 660)
    s = bodyscale(VB[2], VB[3])
    fy, hx, H0, lift = 440.0, 60.0, 975.0, 30.0
    P = LB.pose(anchor=("heel", "near"))
    _, J = LB.draw(p, s, P, hx, fy, H0)
    ax, ay = J["ankle"]
    kx, ky = J["knee"][0], J["knee"][1] - lift
    cop = J["heel"][0] + 0.55 * (J["toe"][0] - J["heel"][0])
    o = [f"<defs>{H.markers(p, s)}</defs>", plate(s, J["heel"][0] - 30, J["toe"][0] + 30, fy, 14.0),
         part_art(P, hx, fy, H0, ("lat_foot", "lat_shank"), {"lat_shank": -lift})]
    o.append(H.joint_centre(s, ax, ay))
    o.append(H.joint_centre(s, ax, ay - lift))
    o.append(H.joint_centre(s, kx, ky))
    o.append(grf_arrow(s, p, cop, fy, 100.0))
    o.append(H.label(s, cop + 10, fy - 46, f"{it('F')}{sb(s, 'GRF', 'label')}", "label", I["primary"]))
    # the third-law pair at the ankle
    o.append(white_under(s, ax - 14, ay - 34, ax - 14, ay, 5))
    o.append(H.arrow(s, p, ax - 14, ay - 34, ax - 14, ay, "reaction"))
    o.append(white_under(s, ax + 14, ay - lift + 34, ax + 14, ay - lift, 5))
    o.append(H.arrow(s, p, ax + 14, ay - lift + 34, ax + 14, ay - lift, "reaction"))
    o.append(H.label(s, ax + 34, ay - 88, "ankle pair:", "label2", I["primary"]))
    o.append(H.label(s, ax + 34, ay - 72, f"{it('F')}{sb(s, 'a')} down on the foot", "label2", I["primary"]))
    o.append(H.label(s, ax + 34, ay - 56, f"−{it('F')}{sb(s, 'a')} up on the shank", "label2", I["primary"]))
    # the knee load, unknown
    o.append(white_under(s, kx, ky - 80, kx, ky, 5))
    o.append(H.arrow(s, p, kx, ky - 80, kx, ky, "reaction"))
    o.append(arc_arrow(s, p, kx, ky, 34, 50, -70, "force"))
    o.append(H.label(s, kx + 46, ky - 6, f"{it('M')}{sb(s, 'k', 'label')}", "label", I["primary"]))
    o.append(H.label(s, kx + 12, ky - 62, f"{it('F')}{sb(s, 'k', 'label')}", "label", I["primary"]))
    o.append(H.label(s, 170, ky + 70, f"2  shank: handed −{it('F')}{sb(s, 'a')},", "label2", I["primary"]))
    o.append(H.label(s, 170, ky + 86, "solves for the knee load", "label2", I["secondary"]))
    o.append(H.label(s, 170, fy - 190, "1  foot: GRF is measured,", "label2", I["primary"]))
    o.append(H.label(s, 170, fy - 174, "solves for the ankle load", "label2", I["secondary"]))
    o.append(H.label(s, 392, 28, "arrows not to scale", "label2", I["secondary"], "end"))
    o.append(box(s, 14, 478, 372, 82))
    o.append(rows(s, 26, 500, [f"foot:   {it('F')}{sb(s, 'a')} = {it('m')}{sb(s, 'f')} {it('a')}{sb(s, 'f')} − {it('m')}{sb(s, 'f')} {it('g')} − {it('F')}{sb(s, 'GRF')}",
                               f"shank: {it('F')}{sb(s, 'k')} = {it('m')}{sb(s, 's')} {it('a')}{sb(s, 's')} − {it('m')}{sb(s, 's')} {it('g')} + {it('F')}{sb(s, 'a')}",
                               f"an error in the foot data reaches {it('F')}{sb(s, 'k')} and {it('M')}{sb(s, 'k')}"], dy=s(21)))
    o.append(LB.credit(s, 14, 584, width=372))
    aria = ("The lower leg drawn as two free bodies, a foot on a grey force plate and the shank above it, drawn slightly apart in side "
            "view. A red arrow F GRF, measured, points up into the foot. At the ankle a pair of equal and opposite black arrows, "
            "F a on the foot and minus F a on the shank, passes the load from the foot to the shank. At the knee a black arrow F k and "
            "a red arc M k are the unknown knee force and moment. Labels number the steps, 1 foot and 2 shank, and a box gives the "
            "two recursion equations, F a equals m f a f minus m f g minus F GRF, and F k equals m s a s minus m s g plus F a.")
    return done(VB, aria, s, o)


FIGS = {
    29: (r'C7: two instruments, one truth. Why does agreement between t', fig29),
    30: (r'C8: the error filtering cannot touch. Why does a $15\%$ erro', fig30),
    31: (r'C9: the instrument that stays outside. EMG measures the musc', fig31),
    32: (r'C10: the pose that checks everything. Holding a limb still a', fig32),
    33: (r'D1: segment angle from markers. From proximal and distal mar', fig33),
    37: (r'D5: the centre of mass. Derive the whole-body COM from the s', fig37),
    38: (r'D6: the force-plate identity. Derive $M\ddot{\mathbf r}_{\rm', fig38),
    39: (r'D7: the Newton step. Derive the proximal joint force on a se', fig39),
    40: (r'D8: the Euler step. Derive the net proximal joint moment abo', fig40),
    41: (r'D9: torque error bars. Derive the variance of the single-joi', fig41),
    48: (r'K4: recover the torque, with and without filtering (simulati', fig48),
    50: (r'K6: the two-segment recursion (simulation). Run the Newton-E', fig50),
    53: (r'K8: identify the mass (inverse). Recover total body mass fro', fig53),
}
