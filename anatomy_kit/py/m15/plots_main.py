"""Module 15 main-text and lab plots in the house style (group `plots_main`; svg #5 7 8 9 11 13 14 16 18 20 22).

Every plotted number is computed here from the module's own text and code (module15.html):
  #5   Lemma 1.1 and Prop. 1.2: CV_tot = sqrt(bio^2 + assay^2 + count^2), LSC = 1.96 sqrt(2) CV_tot; N from the stated
       concentrations, volumes and molar masses (lines 141-144)
  #7   Prop. 3.1 set-up (line 187): sigma 0.006 rad, fs 100 Hz, 1 Hz, 0.30 rad
  #8   Prop. 4.1 for the 0.8 Hz, 0.40 rad test joint (line 237): 2nd-order Butterworth, zero lag, np.gradient;
       bias = noise-free filter error, variance = noise passed (400 draws)
  #11  the Section 7 listing (seed 15), #13 Section 8 Monte Carlo (20 000 draws), #14 and #22 Lab D listing,
  #16  Lab A listing, #18 Lab B listing, #20 Lab C listing.
This file does NOT expose SHARED_DEFS: the Lynch body kit art comes from m15/body_main.py.
One user unit is one rendered px (760-unit viewBoxes), so sizes pass through H.Scale.
"""
import html
import math
from functools import lru_cache

import numpy as np
from scipy.signal import butter, filtfilt

import house as H
import lynch_body as LB
from m05.plots_main import Ax, axes, curve, dot, legend, poly, pts_str, tw

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
GRID = "#e6e6e6"
RED, BLUE, ORANGE = SER[0], SER[1], SER[2]

# ---------------------------------------------------------------- the synthetic joint of Section 7 (listing, lines 301-355)
FS, DT, SIG, G = 100.0, 0.01, 0.006, 9.81
IZ, MZ, LL = 0.05, 4.0, 0.25
A0, F0 = 0.40, 0.8
TT = np.arange(0, 2, DT)
TRIM = slice(8, -8)
Q_TRUE = A0 * np.sin(2 * np.pi * F0 * TT)
QDD_TRUE = -A0 * (2 * np.pi * F0) ** 2 * np.sin(2 * np.pi * F0 * TT)
TAU_TRUE = IZ * QDD_TRUE + MZ * G * LL * np.sin(Q_TRUE)


def smooth(x, fc):
    b, a = butter(2, fc / (FS / 2))
    return filtfilt(b, a, x, axis=-1)


def pipeline(q, fc, Iz=IZ, m=MZ):
    qf = q if fc is None else smooth(q, fc)
    return Iz * np.gradient(np.gradient(qf, DT, axis=-1), DT, axis=-1) + m * G * LL * np.sin(qf)


def rmse(a, b):
    return float(np.sqrt(np.mean((a[..., TRIM] - b[TRIM]) ** 2)))


def sup(t, s, size="tick"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def tag(s, x, y, col, text, size="label2", anchor="start", dashed=False):
    """Direct label: a short coloured mark, then ink text (text is never the series colour)."""
    w = tw(text, H.PX[size])
    x0 = x - w - 30 if anchor == "end" else x
    da = f' stroke-dasharray="{s(5):.2f} {s(3):.2f}"' if dashed else ""
    return [f'<line x1="{x0:.2f}" y1="{y - 4:.2f}" x2="{x0 + 20:.2f}" y2="{y - 4:.2f}" stroke="{col}" '
            f'stroke-width="{s(H.PX["curve_multi"]):.2f}"{da}/>',
            H.label(s, x0 + 25, y, text, size, I["primary"])]


def hover_pts(ax, xs, ys, texts):
    """ys: list of series (each a list), one tooltip per x."""
    out = []
    for k, x in enumerate(xs):
        yy = [round(ax.Y(ser[k]), 2) for ser in ys]
        out.append([round(ax.X(x), 2), yy if len(yy) > 1 else yy[0], texts[k]])
    return out


def mn(v, f="{:.2f}"):
    t = f.format(v)
    return "−" + t[1:] if t.startswith("-") else t


def finish(vb, aria, s, body, hv=None):
    return H.svg_open(vb, html.escape(aria), s, extra=hv or "") + "".join(body) + "</svg>"


# ================================================================ svg #5: the three CVs of the biochemical markers
def cv_numbers():
    NA = 6.022e23
    n = {"CTX": 0.30e-9 * 0.025 / 869 * NA, "P1NP": 40e-9 * 0.025 / 35000 * NA, "lactate": 1e-3 * 1e-6 * 1.0 * NA}
    bio = {"CTX": 25.0, "P1NP": 8.0, "lactate": 12.0}       # line 197 and caption (CV_bio, %)
    assay = {"CTX": 6.0, "P1NP": 3.0, "lactate": 3.0}        # line 200 (%)
    out = {}
    for k in n:
        cnt = 100 / math.sqrt(n[k])
        tot = math.sqrt(bio[k] ** 2 + assay[k] ** 2 + cnt ** 2)
        out[k] = dict(N=n[k], bio=bio[k], assay=assay[k], cnt=cnt, tot=tot, lsc=1.96 * math.sqrt(2) * tot)
    return out


def fig5():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    d = cv_numbers()
    # text checks (lines 205-211): N, counting CVs, CV_tot, LSC
    assert abs(d["CTX"]["N"] / 5.2e9 - 1) < 0.02 and abs(d["P1NP"]["N"] / 1.7e10 - 1) < 0.02
    assert abs(d["lactate"]["N"] / 6.0e14 - 1) < 0.01
    assert [round(d[k]["lsc"]) for k in d] == [71, 24, 34], [d[k]["lsc"] for k in d]
    assert abs(d["CTX"]["tot"] - 25.71) < 0.01 and abs(d["lactate"]["cnt"] - 4.1e-6) < 0.05e-6
    ax = Ax((90, 70, 735, 320), (0, 1), (1e-6, 1e2), ylog=True)
    o = []
    yt = [(10.0 ** e, "10" + sup(f"−{-e}" if e < 0 else str(e), s)) for e in range(-6, 3)]
    yt = [(v, ("1" if v == 1 else t)) for v, t in yt]
    o += axes(s, ax, [], yt, "", "coefficient of variation CV (%, log scale)", ylab_x=24)
    gw = (ax.x1 - ax.x0) / 3
    bw = 36
    cols = [RED, BLUE, ORANGE]
    pts = []
    for g, k in enumerate(d):
        cx = ax.x0 + gw * (g + 0.5) - 20
        for j, key in enumerate(("bio", "assay", "cnt")):
            v = d[k][key]
            bx = cx - 1.5 * bw - 6 + j * (bw + 6)
            o.append(f'<rect x="{bx:.2f}" y="{ax.Y(v):.2f}" width="{bw}" height="{ax.y0 - ax.Y(v):.2f}" fill="{cols[j]}"/>')
            txt = f"{v:g}" if v >= 1 else f"{v:.{math.ceil(-math.log10(v)) + 1}f}".rstrip("0")
            o.append(H.label(s, bx + bw / 2, ax.Y(v) - 6, txt, "tick", I["primary"], "middle"))
            pts.append([bx + bw / 2, ax.Y(v), f"{k}, {['biological', 'assay', 'counting floor'][j]} CV = {txt} %"])
        # diamond: quadrature total
        dx, dy, r = cx + 1.5 * bw + 22, ax.Y(d[k]["tot"]), 8
        o.append(f'<path d="M{dx:.2f},{dy - r:.2f} L{dx + r:.2f},{dy:.2f} L{dx:.2f},{dy + r:.2f} L{dx - r:.2f},{dy:.2f} Z" '
                 f'fill="{I["primary"]}" stroke="#fff" stroke-width="{s(1.5):.2f}"/>')
        o.append(H.label(s, dx + 12, dy + 5, f"{d[k]['tot']:.1f}", "tick", I["primary"]))
        pts.append([dx, dy, f"{k}, total CV = {d[k]['tot']:.2f} %, LSC = {d[k]['lsc']:.0f} %"])
        o.append(H.label(s, cx, ax.y0 + 24, k, "label", I["primary"], "middle"))
        o.append(H.label(s, cx, ax.y0 + 43, f"LSC {d[k]['lsc']:.0f}%", "label2", I["secondary"], "middle"))
    o += legend(s, ax.x0, 38, [(RED, None, "biological CV"), (BLUE, None, "assay CV"), (ORANGE, None, "counting floor 1/√N")], gap=22) \
        if False else []
    lx = 90
    for col, txt in ((RED, "biological CV"), (BLUE, "assay CV"), (ORANGE, "counting floor, 1/√N")):
        o.append(f'<rect x="{lx}" y="22" width="14" height="14" fill="{col}"/>')
        o.append(H.label(s, lx + 20, 34, txt, "label2", I["primary"]))
        lx += 20 + tw(txt) + 26
    o.append(f'<path d="M{lx + 8:.2f},21 L{lx + 16:.2f},29 L{lx + 8:.2f},37 L{lx:.2f},29 Z" fill="{I["primary"]}"/>')
    o.append(H.label(s, lx + 24, 34, "total CV (quadrature), %", "label2", I["primary"]))
    pts.sort(key=lambda p: p[0])
    aria = ("Grouped log-scale bar chart of three coefficients of variation for CTX, P1NP and lactate: biological CV 25, 8 and "
            "12 percent (red), assay CV 6, 3 and 3 percent (blue), and the counting floor 0.0014, 0.00076 and 0.0000041 "
            "percent (orange). A black diamond marks each marker's quadrature-summed total CV, 25.7, 8.5 and 12.4 percent, "
            "and the label under each group gives its least significant change, 71, 24 and 34 percent.")
    return finish(VB, aria, s, o, H.hover_attr([ax.x0, ax.top, ax.x1, ax.y0], [[round(a, 1), round(b, 1), t] for a, b, t in pts]))


# ================================================================ svg #7: differentiation amplifies noise
@lru_cache(None)
def noise_demo():
    """Line 187: sigma 0.006 rad, fs 100 Hz, 1 Hz, 0.30 rad. Record -1..2 s, shown 0..1 s (no filter edge)."""
    t = np.arange(-1, 2, DT)
    a, f0 = 0.30, 1.0
    q = a * np.sin(2 * np.pi * f0 * t)
    v = a * 2 * np.pi * f0 * np.cos(2 * np.pi * f0 * t)
    qm = q + np.random.default_rng(15).normal(0, SIG, t.size)
    # cutoff: the one that minimises the RMS velocity error for this motion (the text states none for this figure)
    best = None
    for fc in np.geomspace(1.5, 12, 60):
        e = np.sqrt(np.mean((np.gradient(smooth(qm, fc), DT) - v) ** 2))
        if best is None or e < best[0]:
            best = (e, fc)
    fc = round(best[1] * 2) / 2
    return t, q, v, qm, np.gradient(qm, DT), np.gradient(smooth(qm, fc), DT), fc


def fig7():
    VB = (0, 0, 760, 358)
    s = H.Scale(VB[2], VB[3])
    t, q, v, qm, vraw, vfil, fc = noise_demo()
    assert abs(0.30 * 2 * np.pi - 1.9) < 0.02 and abs(SIG / (math.sqrt(2) * DT) - 0.42) < 0.005      # lines 187-189
    m = (t >= 0) & (t <= 1)
    A = Ax((78, 66, 345, 270), (0, 1), (-0.35, 0.35))
    B = Ax((468, 66, 735, 270), (0, 1), (-2.6, 2.6))
    o = axes(s, A, [(0, "0"), (0.5, "0.5"), (1, "1")], [(-0.3, "−0.3"), (0, "0"), (0.3, "0.3")], "time (s)", "joint angle q (rad)", ylab_x=22)
    o += axes(s, B, [(0, "0"), (0.5, "0.5"), (1, "1")], [(-2, "−2"), (0, "0"), (2, "2")], "time (s)", "velocity (rad/s)", ylab_x=412)
    o.append(curve(s, A, t[m], q[m], RED))
    for x, y in zip(t[m][::2], qm[m][::2]):
        o.append(dot(s, A.X(x), A.Y(y), ORANGE, r=2.6))
    o.append(poly(s, [(B.X(x), B.Y(y)) for x, y in zip(t[m], vraw[m])], ORANGE, "curve_multi"))
    o.append(curve(s, B, t[m], vfil[m], BLUE))
    o.append(curve(s, B, t[m], v[m], RED, "curve_multi", dash=(7, 4)))
    # legends above each panel
    lx = 78
    o += tag(s, lx, 44, RED, "true angle")
    o.append(dot(s, lx + 130 + 10, 40, ORANGE, r=2.6))
    o.append(H.label(s, lx + 130 + 24, 44, "measured, σ = 0.006 rad", "label2", I["primary"]))
    lx = 468
    o += tag(s, lx, 44, ORANGE, "raw")
    o += tag(s, lx + 70, 44, BLUE, f"filtered, {fc:g} Hz")
    o += tag(s, lx + 215, 44, RED, "true", dashed=True)
    o.append(H.label(s, 78, 344, "noise 0.006 rad is 2% of the 0.30 rad amplitude", "label2", I["secondary"]))
    o.append(H.label(s, 468, 344, "raw velocity noise 0.42 rad/s, true peak 1.9 rad/s", "label2", I["secondary"]))
    hv = H.hover_attr([
        (A.box, hover_pts(A, t[m], [q[m], qm[m]], [f"t = {x:.2f} s, true {a:.3f} rad, measured {b:.3f} rad" for x, a, b in zip(t[m], q[m], qm[m])])),
        (B.box, hover_pts(B, t[m], [v[m], vraw[m], vfil[m]], [f"t = {x:.2f} s, true {mn(a)} rad/s, raw {mn(b)}, filtered {mn(c)}" for x, a, b, c in zip(t[m], v[m], vraw[m], vfil[m])]))])
    aria = ("Left: a joint angle, a 0.30 rad, 1 Hz sine, measured with 0.006 rad noise over one second; the orange samples lie "
            "almost on the red true curve. Right: its central-difference velocity: the raw velocity in orange swings about 0.4 "
            f"rad per second either side of the red true velocity, which peaks at 1.9 rad per second; filtering the angle at {fc:g} "
            "hertz before differentiating gives the blue curve, close to the truth.")
    return finish(VB, aria, s, o, hv)


# ================================================================ svg #8: bias and variance against the cutoff
@lru_cache(None)
def bias_variance():
    v_true = A0 * 2 * np.pi * F0 * np.cos(2 * np.pi * F0 * TT)
    fcs = np.geomspace(1.2, 45, 70)
    noise = np.random.default_rng(1).normal(0, SIG, (400, TT.size))
    rows = []
    for fc in fcs:
        vb = np.gradient(smooth(Q_TRUE, fc), DT)
        bias = float(np.sqrt(np.mean((vb - v_true)[TRIM] ** 2)))
        vs = np.gradient(smooth(Q_TRUE[None, :] + noise, fc), DT, axis=-1)
        sd = float(np.sqrt(np.mean((vs - vb)[:, TRIM] ** 2)))
        rows.append((fc, bias, sd, math.hypot(bias, sd)))
    return np.array(rows)


def fig8():
    VB = (0, 0, 760, 410)
    s = H.Scale(VB[2], VB[3])
    r = bias_variance()
    j = int(r[:, 3].argmin())
    i7 = int(np.abs(r[:, 0] - 7.0).argmin())
    assert abs(r[j, 0] - 3.0) < 0.1 and abs(r[j, 3] - 0.021) < 0.001 and abs(r[j, 1] - 0.013) < 0.001   # lines 252-253
    assert abs(r[j, 2] - 0.016) < 0.001 and abs(r[i7, 3] - 0.050) < 0.002
    ax = Ax((84, 60, 735, 330), (1, 50), (0, 0.45), xlog=True)
    xt = [(v, str(v)) for v in (1, 2, 5, 10, 20, 50)]
    yt = [(0, "0"), (0.15, "0.15"), (0.30, "0.30"), (0.45, "0.45")]
    o = axes(s, ax, xt, yt, "filter cutoff f" + H.sub("c", s) + " (Hz)", "RMS velocity error (rad/s)", ylab_x=24)
    xo = ax.X(r[j, 0])
    o.append(H.line(s, xo, ax.Y(r[j, 3]), xo, ax.y0, O["dim"], "ref", dash=H.DASH_REF))
    o.append(curve(s, ax, r[:, 0], r[:, 2], ORANGE, "curve_multi", dash=(7, 4)))
    o.append(curve(s, ax, r[:, 0], r[:, 1], BLUE, "curve_multi", dash=(7, 4)))
    o.append(curve(s, ax, r[:, 0], r[:, 3], RED))
    o.append(dot(s, xo, ax.Y(r[j, 3]), I["primary"]))
    o.append(dot(s, ax.X(r[i7, 0]), ax.Y(r[i7, 3]), I["primary"], hollow=True))
    o.append(H.label(s, xo + 14, ax.Y(0.21), "minimum 0.021 rad/s", "label2", I["primary"]))
    o.append(H.label(s, xo + 14, ax.Y(0.21) + 17, "at f" + H.sub("c", s) + " = 3.0 Hz", "label2", I["primary"]))
    o.append(H.label(s, ax.X(7.0) - 10, ax.Y(0.050) - 12, "7 Hz: 0.050 rad/s", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(1.4), ax.Y(0.42), "bias dominates: signal removed", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(7.5), ax.Y(0.31), "noise dominates: noise passed", "label2", I["secondary"]))
    o += tag(s, 84, 38, RED, "total RMS error")
    o += tag(s, 84 + 175, 38, BLUE, "bias", dashed=True)
    o += tag(s, 84 + 270, 38, ORANGE, "noise standard deviation", dashed=True)
    hv = H.hover_attr(ax.box, hover_pts(ax, r[:, 0], [r[:, 3], r[:, 1], r[:, 2]],
                                        [f"fc = {a:.2f} Hz: total {d:.3f}, bias {b:.3f}, noise {c:.3f} rad/s" for a, b, c, d in r]))
    aria = ("RMS velocity-estimate error against filter cutoff frequency on a log axis from 1 to 50 hertz, for a 0.8 hertz, 0.40 "
            "radian test motion with 0.006 radian noise. The blue bias falls from 0.39 rad per second at 1.2 hertz to zero; the "
            "orange passed-noise standard deviation rises to 0.42 at 45 hertz; the red total is U-shaped with a minimum of 0.021 "
            "rad per second at 3.0 hertz, where bias is 0.013 and noise 0.016. A hollow dot marks 0.050 at 7 hertz.")
    return finish(VB, aria, s, o, hv)


# ================================================================ svg #9: the body COM and the force-plate check
@lru_cache(None)
def lab_d_data():
    """Lab D listing (lines 520-540): 2 s squat, plate noise 2.5 N, kinematic noise 0.12 m/s^2, seed 15."""
    t = np.arange(0, 2, DT)
    a_true = -0.35 * np.pi ** 2 * np.cos(np.pi * t) / 2.0
    rng = np.random.default_rng(15)
    fy = 70.0 * (G + a_true) + rng.normal(0, 2.5, t.size)
    a_kin = a_true + rng.normal(0, 0.12, t.size)
    return t, a_true, fy, a_kin


def identify(a_kin, fy, ms=None):
    ms = np.linspace(60, 80, 801) if ms is None else ms
    res = [np.sqrt(np.mean((a_kin - (fy / m - G)) ** 2)) for m in ms]
    return ms[int(np.argmin(res))]


def squat_pose(lean):
    leg = dict(hip=78.0, knee=92.0, shoulder=35.0, elbow=15.0)
    return LB.pose(pelvis=lean * 0.55, trunk=lean * 0.45, near=dict(leg), far=dict(leg), anchor=("heel", "near"))


def fig9():
    VB = (0, 0, 760, 432)
    s = H.Scale(VB[2], VB[3])
    t, a_true, fy, a_kin = lab_d_data()
    a_plate = fy / 70.0 - G
    res = float(np.sqrt(np.mean((a_kin - a_plate) ** 2)))
    assert abs(res - 0.12) < 0.01 and abs(np.abs(a_true).max() - 1.7) < 0.05 and abs(res / np.abs(a_true).max() - 0.07) < 0.01
    # body, left panel
    S0 = H.Scale(300, 420)
    lean = 28.0
    P = squat_pose(lean)
    height = 290.0
    fx, fy0 = 118.0, 342.0
    body, J = LB.draw("m15f9_", s, P, fx, fy0, height)
    midfoot = (J["heel"][0] + J["toe"][0]) / 2
    o = []
    o.append(f'<rect x="20" y="{fy0:.2f}" width="236" height="16" fill="#cfcfcf" stroke="{I["axis"]}" stroke-width="{s(1.2):.2f}"/>')
    o.append(body)
    for key in ("com_head", "com_trunk", "com_upper_arm", "com_forearm", "com_hand", "com_thigh", "com_shank", "com_foot"):
        x, y = J[key]
        o.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(3.2):.2f}" fill="{I["secondary"]}" stroke="#fff" stroke-width="{s(1.2):.2f}"/>')
    cx, cy = J["com"]
    o.append(H.com_mark(s, cx, cy))
    # Mg down from the COM, F_y up from the plate (arrows are drawn, not to scale)
    o.append(f'<defs>{H.markers("m9", s)}</defs>')
    o.append(H.arrow(s, "m9", cx + 26, cy, cx + 26, cy + 70, "load"))
    o.append(H.label(s, cx + 32, cy + 52, "Mg", "label", O["load"] and I["primary"]))
    o.append(H.arrow(s, "m9", midfoot + 30, fy0, midfoot + 30, fy0 - 82, "reaction"))
    o.append(H.label(s, midfoot + 36, fy0 - 52, "F" + H.sub("y", s), "label", I["primary"]))
    o.append(H.line(s, cx - 8, cy - 4, cx - 44, cy - 30, I["rule"], "leader"))
    o.append(H.label(s, cx - 46, cy - 30, "COM", "label2", I["primary"], "end"))
    o.append(H.label(s, 138, fy0 + 36, "force plate", "label2", I["primary"], "middle"))
    # right panel: plot
    ax = Ax((372, 84, 735, 306), (0, 2), (-2, 2))
    o += axes(s, ax, [(0, "0"), (0.5, "0.5"), (1, "1"), (1.5, "1.5"), (2, "2")], [(-2, "−2"), (-1, "−1"), (0, "0"), (1, "1"), (2, "2")],
              "time (s)", "vertical COM acceleration (m/s²)", ylab_x=318)
    o.append(curve(s, ax, t, a_kin, RED, "curve_multi"))
    o.append(curve(s, ax, t, a_plate, BLUE))
    o += tag(s, 372, 34, BLUE, "force plate: F" + H.sub("y", s) + "/M − g")
    o += tag(s, 372, 56, RED, "cameras: twice-differentiated segment COM")
    o.append(H.label(s, 372, 374, f"RMS residual {res:.3f} m/s² on a peak of {np.abs(a_true).max():.1f} m/s²", "label2", I["secondary"]))
    o.append(LB.credit(s, 20, 410))
    ix = [k for k in range(0, t.size, 1)]
    hv = H.hover_attr(ax.box, hover_pts(ax, t[ix], [a_kin[ix], a_plate[ix]],
                                        [f"t = {t[k]:.2f} s: cameras {mn(a_kin[k])}, force plate {mn(a_plate[k])} m/s²" for k in ix]))
    aria = ("A person in a mid-squat, drawn as a skeleton, on a grey force plate; grey dots mark the segment centres of mass, "
            "the black-and-white mark is the whole-body centre of mass, a brown arrow shows the weight Mg down from it and a "
            "black arrow the plate force Fy up. Right: the vertical COM acceleration over two seconds estimated two ways, "
            "from the cameras (red) and from the force plate as Fy over M minus g (blue); the two curves overlay, "
            "with an RMS gap of 0.13 metres per second squared on a peak of 1.7.")
    return finish(VB, aria, s, o, hv), J, midfoot


def fig9_build():
    return fig9()[0]


# ================================================================ svg #11: the pipeline recovers the torque
@lru_cache(None)
def pipeline_run():
    q_meas = Q_TRUE + np.random.default_rng(15).normal(0, SIG, TT.size)
    return (pipeline(q_meas, 6.0), pipeline(q_meas, None))


def fig11():
    VB = (0, 0, 760, 410)
    s = H.Scale(VB[2], VB[3])
    filt, raw = pipeline_run()
    e_f, e_r = rmse(filt, TAU_TRUE), rmse(raw, TAU_TRUE)
    assert abs(np.abs(TAU_TRUE).max() - 3.31) < 0.005 and abs(e_f - 0.07) < 0.005 and abs(e_r - 1.70) < 0.005, (e_f, e_r)   # line 462
    sl = TRIM
    t = TT[sl]
    ax = Ax((84, 66, 735, 330), (0, 2), (-6.5, 6.5))
    o = axes(s, ax, [(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2)], [(-5, "−5"), (0, "0"), (5, "5")], "time (s)", "joint torque (N m)", ylab_x=26)
    o.append(poly(s, [(ax.X(x), ax.Y(y)) for x, y in zip(t, raw[sl])], ORANGE, "curve_multi"))
    o.append(curve(s, ax, t, filt[sl], BLUE))
    o.append(curve(s, ax, t, TAU_TRUE[sl], RED, "curve_multi", dash=(7, 4)))
    o += tag(s, 84, 40, RED, "true torque", dashed=True)
    o += tag(s, 84 + 150, 40, BLUE, f"filtered, 6 Hz: RMSE {e_f:.2f} N m")
    o += tag(s, 84 + 420, 40, ORANGE, f"unfiltered: RMSE {e_r:.2f} N m")
    hv = H.hover_attr(ax.box, hover_pts(ax, t, [TAU_TRUE[sl], filt[sl], raw[sl]],
                                        [f"t = {x:.2f} s: true {mn(a)}, filtered {mn(b)}, unfiltered {mn(c)} N m"
                                         for x, a, b, c in zip(t, TAU_TRUE[sl], filt[sl], raw[sl])]))
    aria = ("Recovered joint torque over two seconds for the synthetic joint: the true torque as a red dashed curve peaking "
            "at 3.31 newton metres, the blue estimate from the filtered pipeline lying on it with 0.07 newton metre RMS error, "
            "and the orange unfiltered estimate swinging about 1.7 newton metres RMS off it.")
    return finish(VB, aria, s, o, hv)


# ================================================================ svg #13: Monte Carlo error bars and the error budget
@lru_cache(None)
def mc_budget():
    n = 20000
    rb = np.random.default_rng(17)                      # the 15% parameter draws (the text's seed is not stated)
    z1, z2 = rb.normal(0, 0.15, n), rb.normal(0, 0.15, n)
    rng = np.random.default_rng(15)
    qf6 = smooth(Q_TRUE, 6.0)
    qdd6 = np.gradient(np.gradient(qf6, DT), DT)
    a, b = qdd6, G * LL * np.sin(qf6)
    # BSP only: noise off, inertia and mass drawn (linear in the draws, so the 20 000-draw pool is cheap)
    tau_b = (IZ * (1 + z1))[:, None] * a[None, :] + (MZ * (1 + z2))[:, None] * b[None, :]
    bsp = float(np.sqrt(np.mean((tau_b[:, TRIM] - TAU_TRUE[TRIM]) ** 2)))
    lin = 0.15 * float(np.sqrt(np.mean(((IZ * a) ** 2 + (MZ * b) ** 2)[TRIM])))
    noise = rng.normal(0, SIG, (n, TT.size))
    mark = rmse(pipeline(Q_TRUE[None, :] + noise, 6.0), TAU_TRUE)
    cutoff = rmse(pipeline(Q_TRUE, 1.5), TAU_TRUE)
    bias = rmse(pipeline(Q_TRUE, 6.0), TAU_TRUE)
    # the band: 2000 draws with marker noise and the 15% BSP together, 6 Hz
    m2 = 2000
    qm = Q_TRUE[None, :] + noise[:m2]
    qf = smooth(qm, 6.0)
    qdd = np.gradient(np.gradient(qf, DT, axis=-1), DT, axis=-1)
    tau = (IZ * (1 + z1[:m2]))[:, None] * qdd + (MZ * (1 + z2[:m2]))[:, None] * G * LL * np.sin(qf)
    return dict(bsp=bsp, lin=lin, mark=mark, cutoff=cutoff, bias=bias, mean=tau.mean(0), sd=tau.std(0))


def fig13():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    r = mc_budget()
    assert abs(r["bsp"] - 0.414) < 0.001 and abs(r["lin"] - 0.415) < 0.005 and abs(r["mark"] - 0.059) < 0.004   # line 489
    assert abs(r["cutoff"] - 0.228) < 0.004 and abs(r["bias"] - 0.004) < 0.002
    t = TT[TRIM]
    A = Ax((76, 66, 360, 300), (0, 2), (-5, 5))
    o = axes(s, A, [(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2)], [(-4, "−4"), (0, "0"), (4, "4")], "time (s)", "torque (N m)", ylab_x=22)
    hi, lo = r["mean"][TRIM] + 2 * r["sd"][TRIM], r["mean"][TRIM] - 2 * r["sd"][TRIM]
    band = [(A.X(x), A.Y(y)) for x, y in zip(t, hi)] + [(A.X(x), A.Y(y)) for x, y in zip(t[::-1], lo[::-1])]
    o.append(f'<polygon points="{pts_str(band)}" fill="{BLUE}" opacity="0.2"/>')
    o.append(curve(s, A, t, r["mean"][TRIM], BLUE))
    o.append(curve(s, A, t, TAU_TRUE[TRIM], RED, "curve_multi", dash=(7, 4)))
    o += tag(s, 76, 40, BLUE, "mean")
    o.append(f'<rect x="{76 + 78}" y="30" width="22" height="10" fill="{BLUE}" opacity="0.25"/>')
    o.append(H.label(s, 76 + 106, 40, "±2σ band", "label2", I["primary"]))
    o += tag(s, 76 + 190, 40, RED, "true", dashed=True)
    # bars
    names = [("BSP error", r["bsp"]), ("marker noise", r["mark"]), ("cutoff 1.5 Hz", r["cutoff"]), ("filter bias", r["bias"])]
    B = Ax((470, 66, 735, 300), (0, 4), (0, 0.5))
    o += axes(s, B, [], [(0, "0"), (0.25, "0.25"), (0.5, "0.5")], "", "RMS torque error (N m)", ylab_x=414)
    pts = []
    for k, (nm, v) in enumerate(names):
        cx = B.x0 + (k + 0.5) * (B.x1 - B.x0) / 4
        o.append(f'<rect x="{cx - 24:.2f}" y="{B.Y(v):.2f}" width="48" height="{B.y0 - B.Y(v):.2f}" fill="{SER[1]}" opacity="0.85"/>')
        o.append(H.label(s, cx, B.Y(v) - 6, f"{v:.3f}", "tick", I["primary"], "middle"))
        parts = nm.split(" ")
        o.append(H.label(s, cx, B.y0 + 20, parts[0], "tick", I["primary"], "middle"))
        o.append(H.label(s, cx, B.y0 + 36, " ".join(parts[1:]), "tick", I["primary"], "middle"))
        pts.append([cx, B.Y(v), f"{nm}: RMS torque error {v:.3f} N m"])
    o.append(H.label(s, B.x0, 40, "error budget, each source alone", "label2", I["primary"]))
    hv = H.hover_attr([(A.box, hover_pts(A, t, [r["mean"][TRIM], hi, lo, TAU_TRUE[TRIM]],
                                         [f"t = {x:.2f} s: mean {mn(a)}, band {mn(l)} to {mn(h)}, true {mn(c)} N m"
                                          for x, a, h, l, c in zip(t, r["mean"][TRIM], hi, lo, TAU_TRUE[TRIM])])),
                       (B.box, pts)])
    aria = ("Left: the recovered torque as a blue mean curve inside a shaded plus or minus two sigma band from Monte Carlo "
            "sampling of marker noise and 15 percent body-segment-parameter error, with the red dashed true torque. Right: "
            "bars of the RMS torque error each source contributes alone: body-segment parameters 0.414 newton metres, marker "
            "noise 0.059, a 1.5 hertz cutoff 0.228, filter bias at 6 hertz 0.004.")
    return finish(VB, aria, s, o, hv)


# ================================================================ svg #14: the V of the dynamic residual
def fig14():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    t, a_true, fy, a_kin = lab_d_data()
    ms = np.linspace(55, 85, 241)
    res = np.array([np.sqrt(np.mean((a_kin - (fy / m - G)) ** 2)) for m in ms])
    j = int(res.argmin())
    assert abs(ms[j] - 70.0) < 0.2 and abs(res[j] - 0.12) < 0.01
    ax = Ax((84, 50, 735, 320), (55, 85), (0, 2.8))
    o = axes(s, ax, [(v, str(v)) for v in range(55, 90, 5)], [(0, "0"), (1, "1"), (2, "2")], "assumed body mass M (kg)",
             "dynamic residual (m/s²)", ylab_x=26)
    o.append(H.line(s, ax.X(70), ax.top, ax.X(70), ax.y0, O["dim"], "ref", dash=H.DASH_REF))
    o.append(curve(s, ax, ms, res, RED))
    o.append(dot(s, ax.X(ms[j]), ax.Y(res[j]), I["primary"]))
    o.append(H.label(s, ax.X(70) + 14, ax.Y(2.3), f"minimum at M = {ms[j]:.1f} kg", "label2", I["primary"]))
    o.append(H.label(s, ax.X(70) + 14, ax.Y(2.3) + 17, f"residual {res[j]:.3f} m/s²", "label2", I["primary"]))
    o.append(H.label(s, ax.X(70) - 8, ax.top + 12, "true M = 70 kg", "label2", I["secondary"], "end"))
    o += tag(s, 84, 30, RED, "RMS(kinematic − force-plate COM acceleration)")
    hv = H.hover_attr(ax.box, hover_pts(ax, ms, [res], [f"M = {m:.2f} kg: residual {r_:.3f} m/s²" for m, r_ in zip(ms, res)]))
    aria = ("The dynamic residual, the RMS gap between the kinematic and force-plate vertical COM accelerations, against the assumed "
            "body mass from 55 to 85 kilograms: a V that falls from 2.7 metres per second squared at 55 kilograms to a minimum "
            "of 0.13 at 70 kilograms and rises to 1.75 at 85. A dashed line marks the true mass of 70 kilograms.")
    return finish(VB, aria, s, o, hv)


# ================================================================ Labs: svg #16, #18, #20, #22
LAB_FCS = np.geomspace(1.5, 30, 30)


@lru_cache(None)
def lab_a():
    rng = np.random.default_rng(15)
    knees, curves = [], []
    for _ in range(200):
        qm = Q_TRUE + rng.normal(0, SIG, TT.size)
        resid = np.array([np.sqrt(np.mean((qm - smooth(qm, fc)) ** 2)) for fc in LAB_FCS])
        tail = resid[LAB_FCS > 12].mean()
        knees.append(LAB_FCS[np.argmax(resid < 1.5 * tail)])
        curves.append(resid)
    return np.array(curves), np.array(knees)


def fig16():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    cur, knees = lab_a()
    med, p5, p95 = np.median(knees), *np.percentile(knees, [5, 95])
    assert abs(med - 3.1) < 0.1 and abs(p5 - 2.8) < 0.1 and abs(p95 - 3.8) < 0.1, (med, p5, p95)       # line 439
    mean = cur.mean(0)
    tail = float(mean[LAB_FCS > 12].mean())
    ymax = 0.06
    ax = Ax((84, 56, 735, 320), (1.5, 30), (0, ymax), xlog=True)
    xt = [(v, str(v)) for v in (2, 3, 5, 10, 20, 30)]
    o = [f'<rect x="{ax.X(p5):.2f}" y="{ax.top}" width="{ax.X(p95) - ax.X(p5):.2f}" height="{ax.y0 - ax.top}" fill="{BLUE}" opacity="0.14"/>']
    o += axes(s, ax, xt, [(0, "0"), (0.02, "0.02"), (0.04, "0.04"), (0.06, "0.06")], "cutoff f" + H.sub("c", s) + " (Hz)",
              "RMS(raw − filtered) angle (rad)", ylab_x=24)
    o.append(H.line(s, ax.x0, ax.Y(tail), ax.x1, ax.Y(tail), O["dim"], "ref", dash=H.DASH_REF))
    o.append(H.line(s, ax.X(med), ax.Y(float(np.interp(med, LAB_FCS, mean))), ax.X(med), ax.y0, O["dim"], "ref", dash=H.DASH_REF))
    o.append(curve(s, ax, LAB_FCS, mean, RED))
    o.append(dot(s, ax.X(med), ax.Y(float(np.interp(med, LAB_FCS, mean))), I["primary"]))
    o.append(H.label(s, ax.X(med) + 16, ax.Y(0.034), f"knee: median {med:.1f} Hz", "label2", I["primary"]))
    o.append(H.label(s, ax.X(med) + 16, ax.Y(0.034) + 17, f"5–95%: {p5:.1f} to {p95:.1f} Hz", "label2", I["primary"]))
    o.append(H.label(s, ax.X(1.6) + 14, ax.Y(0.052), "signal removed", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(13), ax.Y(tail) - 10, "noise floor", "label2", I["secondary"]))
    o += tag(s, 84, 32, RED, "mean residual over 200 noise draws")
    o.append(f'<rect x="{84 + 290}" y="23" width="22" height="10" fill="{BLUE}" opacity="0.25"/>')
    o.append(H.label(s, 84 + 318, 32, "5–95% range of the knee", "label2", I["primary"]))
    hv = H.hover_attr(ax.box, hover_pts(ax, LAB_FCS, [mean], [f"fc = {f:.2f} Hz: residual {r_:.4f} rad" for f, r_ in zip(LAB_FCS, mean)]))
    aria = ("Lab A residual analysis: the RMS difference between raw and filtered angle against cutoff on a log axis from 1.5 to "
            "30 hertz, averaged over 200 noise draws. The red curve is flat at the noise floor at high cutoff and climbs steeply "
            "below about 3 hertz; a dot marks the knee at a median of 3.1 hertz and a shaded band the 5 to 95 percent range of "
            "2.8 to 3.8 hertz.")
    return finish(VB, aria, s, o, hv)


@lru_cache(None)
def lab_b():
    def pooled(fc, n=300, seed=5):
        r = np.random.default_rng(seed)
        acc = 0.0
        for _ in range(n):
            qm = Q_TRUE + r.normal(0, SIG, TT.size)
            acc += np.mean((pipeline(qm, fc)[TRIM] - TAU_TRUE[TRIM]) ** 2)
        return math.sqrt(acc / n)
    return np.array([pooled(fc) for fc in LAB_FCS])


def fig18():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    errs = lab_b()
    j = int(errs.argmin())
    e15, e30 = float(np.interp(1.5, LAB_FCS, errs)), float(np.interp(30.0, LAB_FCS, errs))
    assert abs(LAB_FCS[j] - 3.4) < 0.1 and abs(errs[j] - 0.022) < 0.002 and abs(e15 - 0.23) < 0.01 and abs(e30 - 1.34) < 0.02  # 473-476
    ax = Ax((84, 56, 735, 320), (1.5, 30), (0, 1.4), xlog=True)
    o = axes(s, ax, [(v, str(v)) for v in (2, 3, 5, 10, 20, 30)], [(0, "0"), (0.7, "0.7"), (1.4, "1.4")], "cutoff f" + H.sub("c", s) + " (Hz)",
             "torque RMSE (N m)", ylab_x=26)
    o.append(H.line(s, ax.X(3.0), ax.top, ax.X(3.0), ax.y0, O["dim"], "ref", dash=H.DASH_REF))
    o.append(curve(s, ax, LAB_FCS, errs, RED))
    o.append(dot(s, ax.X(LAB_FCS[j]), ax.Y(errs[j]), I["primary"]))
    o.append(dot(s, ax.X(1.5), ax.Y(e15), I["primary"], hollow=True))
    o.append(dot(s, ax.X(30), ax.Y(e30), I["primary"], hollow=True))
    o.append(H.label(s, ax.X(LAB_FCS[j]) + 14, ax.Y(0.45), f"minimum {errs[j]:.3f} N m", "label2", I["primary"]))
    o.append(H.label(s, ax.X(LAB_FCS[j]) + 14, ax.Y(0.45) + 17, f"at {LAB_FCS[j]:.1f} Hz", "label2", I["primary"]))
    o.append(H.label(s, ax.X(3.0) - 8, ax.Y(1.0), "velocity optimum 3.0 Hz", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(1.5) + 12, ax.Y(e15) - 10, f"1.5 Hz: {e15:.2f}", "label2", I["primary"]))
    o.append(H.label(s, ax.X(30) - 10, ax.Y(e30) - 4, f"30 Hz: {e30:.2f}", "label2", I["primary"], "end"))
    o += tag(s, 84, 32, RED, "RMS error of the recovered torque, 300 noise draws per cutoff")
    hv = H.hover_attr(ax.box, hover_pts(ax, LAB_FCS, [errs], [f"fc = {f:.2f} Hz: torque RMSE {e:.3f} N m" for f, e in zip(LAB_FCS, errs)]))
    aria = ("Lab B torque error against cutoff on a log axis from 1.5 to 30 hertz: the RMS error of the recovered joint torque "
            "is U-shaped, 0.23 newton metres at 1.5 hertz, a minimum of 0.022 at 3.4 hertz, and 1.34 at 30 hertz. A dashed "
            "line marks the velocity optimum of 3.0 hertz just below the minimum.")
    return finish(VB, aria, s, o, hv)


@lru_cache(None)
def lab_c():
    rng = np.random.default_rng(15)
    peaks = []
    for _ in range(2000):
        qm = Q_TRUE + rng.normal(0, SIG, TT.size)
        iz = IZ * (1 + rng.normal(0, 0.15))
        mz = MZ * (1 + rng.normal(0, 0.15))
        peaks.append(np.max(np.abs(pipeline(qm, 6.0, iz, mz)[TRIM])))
    return np.array(peaks)


def fig20():
    VB = (0, 0, 760, 416)
    s = H.Scale(VB[2], VB[3])
    pk = lab_c()
    lo, hi = np.percentile(pk, [2.5, 97.5])
    mean, sd = pk.mean(), pk.std()
    true = float(np.abs(TAU_TRUE).max())
    assert abs(mean - 3.41) < 0.01 and abs(sd - 0.58) < 0.01 and abs(lo - 2.22) < 0.02 and abs(hi - 4.53) < 0.02   # line 515-518
    edges = np.linspace(1.5, 5.2, 25)
    cnt, _ = np.histogram(pk, bins=edges)
    ymax = 300
    assert cnt.max() < ymax
    ax = Ax((84, 122, 735, 336), (1.5, 5.2), (0, ymax))
    o = axes(s, ax, [(v, f"{v:g}") for v in (2, 3, 4, 5)], [(0, "0"), (100, "100"), (200, "200"), (300, "300")],
             "recovered peak torque (N m)", "runs per bin (of 2000)", ylab_x=26)
    pts = []
    for k, c in enumerate(cnt):
        x0, x1 = ax.X(edges[k]), ax.X(edges[k + 1])
        if c:
            o.append(f'<rect x="{x0:.2f}" y="{ax.Y(c):.2f}" width="{x1 - x0:.2f}" height="{ax.y0 - ax.Y(c):.2f}" fill="{BLUE}" '
                     f'opacity="0.75" stroke="#fff" stroke-width="{s(1):.2f}"/>')
        pts.append([(x0 + x1) / 2, ax.Y(c), f"{edges[k]:.2f} to {edges[k + 1]:.2f} N m: {int(c)} runs"])
    o.append(H.line(s, ax.X(true), ax.top - 6, ax.X(true), ax.y0, RED, "geom", dash=(6, 4)))
    o.append(H.line(s, ax.X(mean), ax.Y(cnt.max()) - 4, ax.X(mean), ax.y0, I["primary"], "ref"))
    o.append(H.label(s, ax.X(true) - 6, ax.top + 4, f"true {true:.2f}", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(mean) + 14, ax.top + 4, f"mean {mean:.2f}", "label2", I["primary"]))
    # intervals above the histogram
    for yy, a, b, txt in ((66, mean - sd, mean + sd, f"±1 standard deviation: {sd:.2f} N m, {100 * sd / mean:.0f}% of the mean"),
                          (100, lo, hi, f"95% interval: {lo:.2f} to {hi:.2f} N m, ±{100 * (hi - lo) / 2 / mean:.0f}% of the mean")):
        o.append(H.line(s, ax.X(a), yy, ax.X(b), yy, I["primary"], "geom"))
        for e in (a, b):
            o.append(H.line(s, ax.X(e), yy - 5, ax.X(e), yy + 5, I["primary"], "geom"))
        o.append(H.label(s, (ax.X(a) + ax.X(b)) / 2, yy - 10, txt, "label2", I["primary"], "middle"))
    o += tag(s, 84, 26, RED, "true peak torque", dashed=True)
    hv = H.hover_attr(ax.box, sorted(pts, key=lambda p: p[0]))
    aria = ("Lab C Monte Carlo histogram of the recovered peak torque over 2000 runs: a roughly bell-shaped spread with mean 3.41 "
            "newton metres and standard deviation 0.58 around the true 3.31, marked by a red dashed line. A short bracket "
            "shows plus or minus one standard deviation, 17 percent of the mean, and a long bracket the 95 percent interval "
            "from 2.22 to 4.53, plus or minus 34 percent.")
    return finish(VB, aria, s, o, hv)


def fig22():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    t, a_true, fy, a_kin = lab_d_data()
    ns = list(range(20, 201, 10))
    est = [identify(a_kin[:n], fy[:n]) for n in ns]
    se = [0.12 * 70.0 ** 2 / (70.0 * G) / math.sqrt(n) for n in ns]
    assert abs(se[0] - 0.19) < 0.005 and abs(se[-1] - 0.06) < 0.005 and abs(est[0] - 70.03) < 0.03 and abs(est[-1] - 70.0) < 0.03
    assert max(abs(e - 70) for e in est) < 0.5                                                             # "within half a kilogram"
    ax = Ax((84, 56, 735, 320), (20, 200), (69.5, 70.5))
    o = axes(s, ax, [(v, str(v)) for v in (20, 60, 100, 140, 180, 200)], [(69.5, "69.5"), (70, "70"), (70.5, "70.5")],
             "frames of data used, N", "identified mass (kg)", ylab_x=26)
    band = [(ax.X(n), ax.Y(70 + e)) for n, e in zip(ns, se)] + [(ax.X(n), ax.Y(70 - e)) for n, e in zip(ns[::-1], se[::-1])]
    o.append(f'<polygon points="{pts_str(band)}" fill="{BLUE}" opacity="0.2"/>')
    o.append(H.line(s, ax.x0, ax.Y(70), ax.x1, ax.Y(70), O["dim"], "ref", dash=H.DASH_REF))
    o.append(curve(s, ax, ns, est, RED))
    for n, e in zip(ns, est):
        o.append(dot(s, ax.X(n), ax.Y(e), RED))
    o.append(H.label(s, ax.X(200) - 4, ax.Y(70) + 18, "true M = 70 kg", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(68), ax.Y(70 + se[5]) - 10, f"s.e. {se[0]:.2f} kg at N = 20, {se[-1]:.2f} kg at N = 200", "label2", I["primary"]))
    o += tag(s, 84, 32, RED, "identified mass")
    o.append(f'<rect x="{84 + 170}" y="23" width="22" height="10" fill="{BLUE}" opacity="0.25"/>')
    o.append(H.label(s, 84 + 198, 32, "±1 predicted standard error σₐM/(g√N)", "label2", I["primary"]))
    hv = H.hover_attr(ax.box, hover_pts(ax, ns, [est], [f"N = {n} frames: identified {e:.2f} kg, s.e. {x:.2f} kg" for n, e, x in zip(ns, est, se)]))
    aria = ("Lab D identification convergence: the identified body mass, red dots joined by a line, sits at 70.03 kilograms from the "
            "first 20 frames and 70.00 from 200 frames, inside a blue band of one predicted standard error that narrows from "
            "0.19 kilogram at 20 frames to 0.06 at 200. A dashed line marks the true 70 kilograms.")
    return finish(VB, aria, s, o, hv)


def _fig9():
    return fig9()[0]


FIGS = {
    5: ('Grouped log-scale bar chart of the biological, assay, and co', fig5),
    7: ('Left: a barely-noisy measured joint angle over one second. R', fig7),
    8: ('RMS velocity-estimate error versus filter cutoff frequency: ', fig8),
    9: ('A person squatting on a force plate with the body centre of ', _fig9),
    11: ('Recovered knee-style joint torque over two seconds: the true', fig11),
    13: ('Left: the recovered torque as a mean curve inside a shaded u', fig13),
    14: ('The dynamic residual between the kinematic and force-plate c', fig14),
    16: ('Lab A residual analysis: the root-mean-square difference bet', fig16),
    18: ('Lab B torque error versus cutoff: the RMS error of the recov', fig18),
    20: ('Lab C Monte Carlo histogram of the recovered peak torque ove', fig20),
    22: ('Lab D identification convergence: the identified body mass f', fig22),
}
