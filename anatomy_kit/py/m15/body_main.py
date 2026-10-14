"""Module 15 whole-body figures (main text). Exposes the Lynch body kit once per page.

svg #2 (Fig. 1 measurement chain on a standing body), #3 (pipeline), #4 (five instruments on a squat), #6 (planar
marker model), #10 (free-body diagram of the shank), #23 (C1), #24 (C2), #28 (C6).

Numbers (module15.html line numbers):
  Shank instance (448): m = 3.3 kg, I = 0.048 kg m^2, length 0.40 m, a_c = (0.4, 1.2) m/s^2, alpha = 3.0 rad/s^2,
  F_d = (15, 690) N, M_d = -8 N m, shank at 75 deg to the horizontal (knee up and forward), COM 0.433 of the length from
  the knee (r_p 0.173 m, r_d 0.227 m): F_p = (-13.7, -653.7) N, r_d x F_d = -37.22, r_p x F_p = -27.00, M_p = 72.4 N m.
  Pipeline panel (#3): tau = I q'' + m g l sin q, I 0.05, m 4, l 0.25, q = 0.40 sin(2 pi 0.8 t), sigma 0.006 rad,
  15 % body-segment-parameter draw, 6 Hz zero-lag filter (lines 464-500 and Lab C, 636-670): per-sample mean and one
  standard deviation of 2000 pipeline runs, seed 15 (the Lab C draw).
  Joint angles of #6: from Definition 2.1 (line 289-293), computed from the marker points of the drawn pose.
Stature: the module states none; the kit's Winter proportions are used throughout (COM 0.58 H where drawn; the text
  states no COM height).
Body art: lynch_body.py (Patrick J. Lynch, CC BY 2.5).
"""
import math
import re

import numpy as np

import house as H
import lynch_body as LB
from m05.body import finish, it, wrap

SHARED_DEFS = LB.SHARED_DEFS
O, I, T, S = H.OVERLAY, H.INK, H.TISSUE, H.SERIES
BOXFILL, GRID = "#f7f4ef", "#e6e6e6"
BODY = H.MAX_DISPLAY_H_BODY
MARK = O["geometry"]                    # skin markers: one blue in every figure of the group
PURPLE = "#7b4a9e"                      # IMU (green is neural drive; module 10 used the same purple)


# ---------------------------------------------------------------- small helpers
def defs(p, s):
    return f"<defs>{H.markers(p, s)}</defs>"


def poly(s, pts, col, w="curve", dash=None, extra="", fill="none"):
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    return (f'<polyline points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in pts)}" fill="{fill}" stroke="{col}" '
            f'stroke-width="{s(H.PX[w]):.2f}" stroke-linejoin="round"{da} {extra}/>')


def white_under(s, x1, y1, x2, y2, w=4):
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#fff" '
            f'stroke-width="{s(w):.2f}" opacity="0.85"/>')


def dline(s, x1, y1, x2, y2, col=None, w="ref", dash=H.DASH_REF):
    return white_under(s, x1, y1, x2, y2) + H.line(s, x1, y1, x2, y2, col or O["dim"], w, dash=dash)


def leader(s, x1, y1, x2, y2, col=None):
    return H.line(s, x1, y1, x2, y2, col or I["secondary"], "leader")


def floor(s, x0, x1, y):
    return H.line(s, x0, y, x1, y, I["rule"], "axis")


def box(s, x, y, w, h, fill=BOXFILL, stroke=None, extra="", rx=4.0, sw=1.0):
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{s(rx):.2f}" fill="{fill}" '
            f'stroke="{stroke or I["secondary"]}" stroke-width="{s(sw):.2f}" {extra}/>')


def mark(s, x, y, col=MARK, r=5.0):
    """A skin marker: filled disc with a white rim (a mark, not anatomy)."""
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{col}" stroke="#fff" '
            f'stroke-width="{s(1.5):.2f}"/>')


def cop_mark(s, x, y):
    """Centre of pressure: blue cross-hair circle (module 7 idiom)."""
    r, c = s(5.5), O["geometry"]
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="#fff" stroke="{c}" stroke-width="{s(2):.2f}"/>'
            f'<path d="M{x - r * 1.7:.2f},{y:.2f}h{r * 3.4:.2f}M{x:.2f},{y - r * 1.7:.2f}v{r * 3.4:.2f}" '
            f'stroke="{c}" stroke-width="{s(1.4):.2f}"/>')


def path_d(pts):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def arc_pts(cx, cy, r, a0, a1, n=28):
    """Screen angles in degrees: 0 = +x, + = clockwise (y down)."""
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def arc_arrow(s, p, cx, cy, r, a0, a1, meaning, w=None):
    w = w or {"geometry": "geom", "dim": "ref"}.get(meaning, "force")
    return (f'<path d="{path_d(arc_pts(cx, cy, r, a0, a1))}" fill="none" stroke="{O[meaning]}" '
            f'stroke-width="{s(H.PX[w]):.2f}" marker-end="url(#{p}a_{meaning})"/>')


def arc_plain(s, cx, cy, r, a0, a1, col, w="geom"):
    return (f'<path d="{path_d(arc_pts(cx, cy, r, a0, a1))}" fill="none" stroke="{col}" '
            f'stroke-width="{s(H.PX[w]):.2f}"/>')


def lines(s, x, y, rows, size="label2", fill=None, anchor="start", dy=None):
    dy = dy or s(H.PX[size] * 1.3)
    return "".join(H.label(s, x, y + i * dy, t, size, fill or I["primary"], anchor) for i, t in enumerate(rows))


def badge(s, x, y, n, col=None):
    """Numbered disc."""
    r = s(9)
    col = col or I["secondary"]
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="#fff" stroke="{col}" stroke-width="{s(1.6):.2f}"/>'
            + H.label(s, x, y + s(5), str(n), "label2", I["primary"], "middle", 'stroke="none"'))


def rot_pt(c, v, deg):
    """Point c + v turned by SVG rotate(deg)."""
    r = LB.rot(v, deg)
    return (c[0] + r[0], c[1] + r[1])


def plate(s, x0, x1, y, h=12.0):
    return box(s, x0, y, x1 - x0, s(h), fill=GRID, stroke=I["secondary"], rx=1.5)


def grf_arrow(s, p, x, y, length):
    """Ground reaction on the plate: tail at the centre of pressure (x, y), head up."""
    return (white_under(s, x, y, x, y - length, 5) + H.arrow(s, p, x, y, x, y - length, "force"))


def camera(s, x, y, w=44.0, h=30.0, col=None):
    """Camera glyph, lens facing left (schematic)."""
    col = col or I["secondary"]
    return (box(s, x, y, s(w), s(h), fill=col, stroke=col, rx=4)
            + f'<circle cx="{x + s(w * 0.3):.2f}" cy="{y + s(h / 2):.2f}" r="{s(h * 0.3):.2f}" fill="#fff" stroke="{I["primary"]}" '
              f'stroke-width="{s(1):.2f}"/>'
            + f'<circle cx="{x + s(w * 0.3):.2f}" cy="{y + s(h / 2):.2f}" r="{s(h * 0.14):.2f}" fill="{I["primary"]}"/>')


def phone(s, x, y, col, w=34.0, h=62.0):
    """Phone glyph, held landscape-free: portrait rounded rectangle with a lens dot at the top-left."""
    return (box(s, x, y, s(w), s(h), fill=I["secondary"], stroke=col, rx=6, sw=2.2)
            + f'<circle cx="{x + s(w * 0.3):.2f}" cy="{y + s(h * 0.14):.2f}" r="{s(4.5):.2f}" fill="#fff" '
              f'stroke="{I["primary"]}" stroke-width="{s(1):.2f}"/>')


def ang_deg(v):
    """Lab angle of a vector given in SCREEN coordinates (y down): atan2(y up, x), degrees."""
    return math.degrees(math.atan2(-v[1], v[0]))


def dots(base, n=1):
    """Italic letter with one (q̇) or two (q̈) dots above it: Georgia has no combining marks in SVG text, so the spacing
    modifier is placed by dx/dy and the baseline is restored after it (module 10 idiom)."""
    mark_, dx = ("˙", -0.45) if n == 1 else ("¨", -0.55)
    return (f'<tspan font-style="italic">{base}</tspan><tspan dx="{dx}em" dy="-0.1em" font-style="normal">{mark_}</tspan>'
            f'<tspan dy="0.1em"> </tspan>')


def fmt(v, n=0):
    t = f"{v:.{n}f}"
    return t.replace("-", "−")


# ================================================================ svg #2  Fig. 1 measurement chain on a standing body
# foot_plantar.py plantar_outline_path: right foot, u heel -> toe (0..0.98 of the length), v < 0 lateral (copy used by
# modules 1 and 8).
PLANTAR = [(0.00, 0.08), (0.02, -0.10), (0.08, -0.16), (0.18, -0.14), (0.32, -0.12), (0.50, -0.14), (0.68, -0.16),
           (0.82, -0.12), (0.94, -0.04), (0.98, 0.04), (0.96, 0.12), (0.88, 0.16), (0.72, 0.14), (0.55, 0.10),
           (0.40, 0.06), (0.25, 0.04), (0.12, 0.06), (0.04, 0.10)]


def smooth_closed(pts):
    """Closed Catmull-Rom spline through pts as cubic Beziers."""
    n, d = len(pts), [f"M{pts[0][0]:.2f},{pts[0][1]:.2f}"]
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d.append(f"C{c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {p2[0]:.2f},{p2[1]:.2f}")
    return "".join(d) + "Z"


def fig2():
    p = "m15f2_"
    hgt, fy = 470.0, 505.0
    VB = (0, 0, 760, 650)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    body, J = LB.standing_full(p, s, 250.0, fy, hgt)
    o = [defs(p, s), body]
    hx, tx = J["heel"][0], J["toe"][0]
    px0, px1 = hx - s(60), tx + s(60)
    o.append(floor(s, 20, 460, fy))
    o.append(plate(s, px0, px1, fy))
    com = J["com"]
    # markers at five joint centres (blue discs) with names on the right
    names = [("shoulder", J["shoulder"]), ("hip", J["hip"]), ("wrist", J["wrist"]), ("knee", J["knee"]),
             ("ankle", J["ankle"])]
    xl = 430.0
    label_y = [J["shoulder"][1] - s(2), J["hip"][1] - s(14), J["wrist"][1] + s(18), J["knee"][1], J["ankle"][1] + s(2)]
    for (nm, (mx, my)), ly in zip(names, label_y):
        o.append(leader(s, mx + s(7), my, xl - s(8), ly - s(5)))
    for nm, (mx, my) in names:
        o.append(mark(s, mx, my))
    for (nm, _), ly in zip(names, label_y):
        o.append(H.label(s, xl, ly, nm))
    o.append(H.label(s, xl, J["shoulder"][1] - s(46), "markers on the skin, at the joint centres", "label2", MARK))
    o.append(H.label(s, xl, J["shoulder"][1] - s(28), "(blue discs: positions, 100-250 Hz)", "label2", I["secondary"]))
    # COM (left)
    o.append(H.com_mark(s, *com))
    lx = hx - s(40)
    o.append(leader(s, com[0] - s(9), com[1], lx + s(6), com[1]))
    o.append(H.label(s, lx, com[1] + s(5), "centre of mass (COM)", anchor="end"))
    # GRF and COP under the foot
    cx_ = com[0]                                        # quiet stance: the ground reaction passes through the COM
    glen = 0.24 * hgt
    o.append(grf_arrow(s, p, cx_, fy, glen))
    o.append(cop_mark(s, cx_, fy))
    o.append(leader(s, cx_ - s(4), fy - glen * 0.62, lx + s(6), fy - glen * 0.62, O["force"]))
    o.append(H.label(s, lx, fy - glen * 0.62 + s(5), "ground reaction force (GRF)", anchor="end", fill=O["force"]))
    o.append(leader(s, cx_ - s(8), fy + s(1), lx + s(6), fy + s(30), O["geometry"]))
    o.append(H.label(s, lx, fy + s(35), "centre of pressure (COP)", anchor="end", fill=O["geometry"]))
    o.append(H.label(s, px1 + s(8), fy + s(16), "force plate", "label2", I["secondary"]))
    # plate seen from above: the foot outline and the COP
    fx0, fy0, Lf = 520.0, 520.0, 150.0
    ux = (cx_ - hx) / (tx - hx)                         # COP along the foot, heel 0 -> toe 1
    o.append(box(s, fx0 - s(14), fy0 - s(40), Lf + s(28), s(100), fill=GRID, stroke=I["secondary"], rx=2))
    F = lambda u, v: (fx0 + u * Lf, fy0 + v * Lf)   # noqa: E731
    o.append(f'<path d="{smooth_closed([F(u, v) for u, v in PLANTAR])}" fill="{T["skin"][0]}" stroke="{T["skin"][1]}" '
             f'stroke-width="{s(1.6):.2f}"/>')
    cpx, cpy = F(min(max(ux * 0.98, 0.0), 0.98), 0.0)
    o.append(cop_mark(s, cpx, cpy))
    o.append(H.label(s, fx0 + Lf / 2, fy0 - s(52), "plate seen from above", "label2", I["secondary"], "middle"))
    o.append(H.label(s, fx0 + Lf / 2, fy0 + s(86), "foot outline and COP", "label2", I["secondary"], "middle"))
    o.append(H.label(s, xl, fy - s(100), "inverse dynamics joins the marker motion", "label2", I["primary"]))
    o.append(H.label(s, xl, fy - s(82), "to the ground reaction and returns the torque", "label2", I["primary"]))
    o.append(LB.credit(s, 20, fy + s(86), width=470))
    o.append(H.credit(s, fx0 - s(14), fy0 + s(112), ["Footprint: schematic plantar outline,", "drawn for this course."]))
    aria = ("Lateral view of a standing human skeleton inside its body outline, facing right, on a force plate. Blue "
            "discs mark the shoulder, hip, wrist, knee and ankle joint centres; a mark shows the centre of mass. "
            "Under the foot the plate supplies the ground reaction force, a red upward arrow, at the centre of "
            "pressure, a blue cross-hair. A small view of the plate from above shows the foot outline with the "
            "centre of pressure on it. Inverse dynamics joins the marker motion to the ground reaction.")
    return finish(VB, aria, s, o)


# ================================================================ svg #3  pipeline
_MC = {}


def torque_mc():
    """Lab C draw (line 636-670): 2000 runs of the 6 Hz pipeline, 15 % parameter draws, seed 15.
    Returns t, tau_true, mean, sd over the interior samples."""
    if _MC:
        return _MC["v"]
    from scipy.signal import butter, filtfilt
    FS, DT, SIG, G = 100.0, 0.01, 0.006, 9.81
    IZ, MZ, LL = 0.05, 4.0, 0.25
    Tt = np.arange(0, 2, DT)
    trim = slice(8, -8)
    q_true = 0.40 * np.sin(2 * np.pi * 0.8 * Tt)
    qdd = -0.40 * (2 * np.pi * 0.8) ** 2 * np.sin(2 * np.pi * 0.8 * Tt)
    tau_true = IZ * qdd + MZ * G * LL * np.sin(q_true)
    assert round(float(np.abs(tau_true).max()), 2) == 3.31                  # line 500, Lab C
    b, a = butter(2, 6.0 / (FS / 2))

    def pipe(q, Iz, m):
        qf = filtfilt(b, a, q)
        return Iz * np.gradient(np.gradient(qf, DT), DT) + m * G * LL * np.sin(qf)

    rng = np.random.default_rng(15)
    runs, peaks = [], []
    for _ in range(2000):
        qm = q_true + rng.normal(0, SIG, Tt.size)
        Iz = IZ * (1 + rng.normal(0, 0.15))
        mz = MZ * (1 + rng.normal(0, 0.15))
        tau = pipe(qm, Iz, mz)[trim]
        runs.append(tau)
        peaks.append(np.max(np.abs(tau)))
    runs = np.array(runs)
    assert abs(np.mean(peaks) - 3.41) < 0.06 and abs(np.std(peaks) - 0.58) < 0.06, (np.mean(peaks), np.std(peaks))
    _MC["v"] = (Tt[trim], tau_true[trim], runs.mean(0), runs.std(0))
    return _MC["v"]


def fig3():
    p = "m15f3_"
    VB = (0, 0, 760, 384)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    o = [defs(p, s)]
    ink2 = I["secondary"]
    # ---- panel 1: what you measure
    o.append(box(s, 10, 28, 180, 276, rx=7))
    o.append(H.label(s, 100, 52, "what you measure", anchor="middle"))
    fy, hgt = 262.0, 170.0
    body, J = LB.standing_full(p, s, 36.0, fy, hgt)
    o.append(body)
    o.append(plate(s, J["heel"][0] - s(16), J["toe"][0] + s(16), fy, 9.0))
    for k in ("shoulder", "hip", "knee", "ankle"):
        o.append(mark(s, *J[k], r=4.0))
    o.append(grf_arrow(s, p, J["com"][0], fy, 44.0))
    cam_x, cam_y = 134.0, 130.0
    o.append(camera(s, cam_x, cam_y))
    for tgt in ((J["shoulder"][0] + s(14), J["shoulder"][1]), (J["ankle"][0] + s(14), J["ankle"][1] - s(10))):
        o.append(dline(s, cam_x, cam_y + s(15), tgt[0], tgt[1], I["rule"]))
    o.append(H.label(s, cam_x + s(22), cam_y - s(6), "camera", "label2", ink2, "middle"))
    o.append(H.label(s, J["toe"][0] + s(24), fy + s(8), "force plate", "label2", ink2))
    o.append(H.label(s, 20, 76, "blue discs: markers", "label2", MARK))
    # ---- processing boxes
    bx, bw = 254.0, 112.0
    rows = [(58.0, "smooth (filter)"), (132.0, "differentiate"), (206.0, f"q, {dots('q')}, {dots('q', 2)}")]
    for y0, tx_ in rows:
        o.append(box(s, bx, y0, bw, 46.0, rx=7))
        o.append(H.label(s, bx + bw / 2, y0 + 28, tx_, anchor="middle"))
    for (y0, _), (y1, _) in zip(rows[:-1], rows[1:]):
        o.append(H.arrow(s, p, bx + bw / 2, y0 + 46, bx + bw / 2, y1 - s(2), "dim", w="geom"))
    o.append(H.arrow(s, p, 190, 81, bx - s(2), 81, "dim", w="geom"))
    o.append(H.label(s, 222, 68, "marker", "label2", ink2, "middle"))
    o.append(H.label(s, 222, 104, "positions", "label2", ink2, "middle"))
    # ---- inverse dynamics
    ix, iw, iy, ih = 424.0, 124.0, 126.0, 104.0
    o.append(box(s, ix, iy, iw, ih, rx=7))
    o.append(H.label(s, ix + iw / 2, iy + 36, "inverse", anchor="middle"))
    o.append(H.label(s, ix + iw / 2, iy + 56, "dynamics", anchor="middle"))
    o.append(H.label(s, ix + iw / 2, iy + 80, "(Newton-Euler)", "label2", ink2, "middle"))
    o.append(H.arrow(s, p, bx + bw, 229, ix - s(2), 229, "dim", w="geom"))
    # the ground reaction goes straight to the foot end of the recursion; the inertia comes from a table
    gy = 338.0
    o.append(poly(s, [(190, gy), (ix + iw / 2 + s(24), gy), (ix + iw / 2 + s(24), iy + ih + s(2))], O["force"], "force",
                  extra=f'marker-end="url(#{p}a_force)"'))
    o.append(H.label(s, 204, gy - s(7), "ground reaction (GRF)", "label2", O["force"]))
    o.append(H.arrow(s, p, ix + iw / 2 - s(24), 72, ix + iw / 2 - s(24), iy - s(2), "dim", w="geom"))
    o.append(H.label(s, ix + iw / 2 - s(24), 60, "body inertia (masses, ℓ, I)", "label2", ink2, "middle"))
    # ---- panel 3: the torque with its band
    px, pw = 572.0, 178.0
    o.append(box(s, px, 28, pw, 290, rx=7))
    o.append(H.label(s, px + pw / 2, 52, f"joint torque τ({it('t')}) ± σ", anchor="middle"))
    x0, x1, y0, y1 = px + 40.0, px + pw - 14.0, 84.0, 256.0
    t, truth, mean, sd = torque_mc()
    ymax = 4.4
    X = lambda tt: x0 + (x1 - x0) * tt / 2.0       # noqa: E731
    Y = lambda v: (y0 + y1) / 2 - (y1 - y0) / 2 * v / ymax   # noqa: E731
    o.append(H.line(s, x0, Y(0), x1, Y(0), GRID, "axis"))
    o.append(H.line(s, x0, y0, x0, y1, I["axis"], "axis"))
    o.append(H.line(s, x0, y1, x1, y1, I["axis"], "axis"))
    for v in (-4, 0, 4):
        o.append(H.line(s, x0 - s(4), Y(v), x0, Y(v), I["axis"], "leader"))
        o.append(H.label(s, x0 - s(7), Y(v) + s(4.5), fmt(v), "tick", I["secondary"], "end"))
    for tt in (0, 1, 2):
        o.append(H.line(s, X(tt), y1, X(tt), y1 + s(4), I["axis"], "leader"))
        o.append(H.label(s, X(tt), y1 + s(18), str(tt), "tick", I["secondary"], "middle"))
    band = ([(X(a), Y(m + d)) for a, m, d in zip(t, mean, sd)] + [(X(a), Y(m - d)) for a, m, d in
                                                                    list(zip(t, mean, sd))[::-1]])
    o.append(f'<polygon points="{" ".join(f"{x:.2f},{y:.2f}" for x, y in band)}" fill="{O["force"]}" fill-opacity="0.2" '
             f'stroke="none"/>')
    curve = [(X(a), Y(m)) for a, m in zip(t, mean)]
    o.append(poly(s, curve, O["force"], "curve"))
    o.append(H.label(s, x1, y1 + s(36), "time (s)", "label2", ink2, "end"))
    o.append(H.label(s, x0 - s(2), y0 - s(10), "N·m", "label2", ink2, "start"))
    o.append(H.label(s, px + pw / 2, 302, "mean ± 1 sd of 2000 runs", "label2", ink2, "middle"))
    pts = [[X(a), [Y(m)], f"t = {a:.2f} s: τ = {fmt(m, 2)} ± {sd_:.2f} N·m"] for a, m, sd_ in zip(t, mean, sd)]
    o.append(H.arrow(s, p, ix + iw, 178, px - s(2), 178, "dim", w="geom"))
    o.append(LB.credit(s, 10, 362, width=740))
    aria = ("The measurement-to-torque pipeline as a flow. Left panel, what you measure: a standing person with blue "
            "marker discs, filmed by a camera, standing on a force plate that supplies the ground reaction. The marker "
            "positions go through smoothing, then differentiation, giving the angle, its velocity and acceleration, "
            "which feed inverse dynamics (Newton-Euler). The ground reaction goes to inverse dynamics directly and "
            "body inertia enters from a table. Right panel: the output, a joint torque curve over two seconds "
            "between about minus 3.3 and plus 3.3 newton-metres, inside a shaded one standard deviation band from "
            "2000 Monte Carlo runs with marker noise and a 15 percent body-segment-parameter error.")
    return finish(VB, aria, s, o, H.hover_attr([x0, y0, x1, y1], pts))


# ================================================================ svg #4  Fig. 2 five instruments on a squat
SQUAT = dict(pelvis=25, trunk=20, near=dict(hip=105, knee=105, shoulder=85, elbow=5),
             far=dict(hip=105, knee=105, shoulder=85, elbow=5))

INSTR = [   # (title, two lines, colour)
    ("1 · optical markers", ("3-D positions of skin-mounted dots", "100–250 Hz, about 0.5–1 mm"), MARK),
    ("5 · EMG (thigh)", ("voltage that tracks muscle activation", "activation, not force"), O["neural"]),
    ("2 · phone video", ("2-D image-plane projection", "no depth"), O["flag"]),
    ("4 · IMU (shank)", ("acceleration and angular rate", "in its own tilting frame"), PURPLE),
    ("3 · force plate", ("ground-reaction force and its", "point of application (COP)"), O["force"]),
]


def fig4():
    p = "m15f4_"
    hgt, fy = 440.0, 500.0
    VB = (0, 60, 760, 560)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    P = LB.pose(**SQUAT)
    body, J = LB.draw(p, s, P, 140.0, fy, hgt)
    o = [defs(p, s), floor(s, 20, 400, fy), body]
    hx, tx = J["heel"][0], J["toe"][0]
    o.append(plate(s, hx - s(55), tx + s(55), fy))
    # phone on the right of the body, looking at it
    bx1 = J["bbox"][2]
    phx, phy = bx1 + 80.0, 285.0
    # optical markers: five discs on the near side
    # IMU on the shank, EMG discs on the thigh
    kx, ky = J["knee"]
    ax, ay = J["ankle"]
    hx_, hy_ = J["hip"]
    sh_dir = (ax - kx, ay - ky)
    sh_len = math.hypot(*sh_dir)
    sh_u = (sh_dir[0] / sh_len, sh_dir[1] / sh_len)
    sh_n = (sh_u[1], -sh_u[0])                       # normal toward the front of the shank (+x side)
    if sh_n[0] < 0:
        sh_n = (-sh_n[0], -sh_n[1])
    imu_c = (kx + 0.5 * sh_dir[0] + sh_n[0] * s(15), ky + 0.5 * sh_dir[1] + sh_n[1] * s(15))
    imu_ang = math.degrees(math.atan2(sh_u[1], sh_u[0])) - 90
    th_dir = (kx - hx_, ky - hy_)
    th_len = math.hypot(*th_dir)
    th_u = (th_dir[0] / th_len, th_dir[1] / th_len)
    th_n = (th_u[1], -th_u[0])                       # normal toward the anterior (upper) side of the thigh
    if th_n[1] > 0:
        th_n = (-th_n[0], -th_n[1])
    emg_c = [(hx_ + f * th_dir[0] + th_n[0] * s(14), hy_ + f * th_dir[1] + th_n[1] * s(14)) for f in (0.40, 0.62)]
    rows_y = [140.0, 228.0, 316.0, 404.0, 492.0]
    xl = 520.0
    sites = [J["shoulder"], emg_c[1], (phx + s(34), phy + s(31)), imu_c, (tx + s(55), fy + s(6))]
    for (title, desc, col), (sx, sy), ry in zip(INSTR, sites, rows_y):
        o.append(H.line(s, sx + s(8), sy, xl - s(8), ry - s(5), col, "leader"))
    # sight lines of the phone to the body
    for ty in (J["vertex"][1] + s(30), fy - s(6)):
        o.append(dline(s, phx, phy + s(20), bx1 - s(6), ty, I["rule"]))
    o.append(phone(s, phx, phy, O["flag"]))
    for k in ("shoulder", "hip", "knee", "ankle", "toe"):
        o.append(mark(s, *J[k], r=5.0))
    # IMU: a small box turned with the shank
    iw_, ih_ = s(15), s(26)
    o.append(f'<g transform="translate({imu_c[0]:.2f} {imu_c[1]:.2f}) rotate({imu_ang:.2f})">'
             f'<rect x="{-iw_ / 2:.2f}" y="{-ih_ / 2:.2f}" width="{iw_:.2f}" height="{ih_:.2f}" rx="{s(3):.2f}" fill="{PURPLE}" '
             f'stroke="#fff" stroke-width="{s(1.5):.2f}"/></g>')
    # EMG: two electrode discs and a lead
    o.append(H.line(s, emg_c[0][0], emg_c[0][1], emg_c[1][0], emg_c[1][1], O["neural"], "geom"))
    for c in emg_c:
        o.append(mark(s, *c, col=O["neural"], r=6.0))
    # GRF
    o.append(grf_arrow(s, p, J["com"][0], fy, 0.30 * hgt))
    o.append(cop_mark(s, J["com"][0], fy))
    for (title, desc, col), ry in zip(INSTR, rows_y):
        o.append(box(s, xl - s(2), ry - s(11), s(11), s(11), fill=col, stroke=col, rx=1))
        o.append(H.label(s, xl + s(16), ry, title))
        o.append(H.label(s, xl + s(16), ry + s(20), desc[0], "label2", I["secondary"]))
        o.append(H.label(s, xl + s(16), ry + s(37), desc[1], "label2", I["secondary"]))
    o.append(H.label(s, 20, VB[1] + 24, "one squat, five different readings of it", "label", I["primary"]))
    o.append(LB.credit(s, 20, fy + s(64), width=470))
    aria = ("A skeleton squatting side-on, facing right, on a force plate, read by five instruments. One, blue discs "
            "mark the shoulder, hip, knee, ankle and toe for optical motion capture. Two, a phone on the right films "
            "it from the side and gives a two-dimensional projection. Three, the force plate under the feet gives the "
            "ground reaction, a red upward arrow at the centre of pressure. Four, a purple inertial sensor sits on the "
            "shank. Five, two green electrode discs sit on the thigh for electromyography.")
    return finish(VB, aria, s, o)


# ================================================================ svg #6  Fig. 3 planar marker model
POSE6 = dict(pelvis=5, trunk=5, near=dict(hip=45, knee=70, shoulder=20, elbow=15),
             far=dict(hip=45, knee=70, shoulder=20, elbow=15))


def fig6():
    p = "m15f6_"
    hgt, fy = 470.0, 560.0
    VB = (0, 40, 760, 612)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    P = LB.pose(**POSE6)
    body, J = LB.draw(p, s, P, 150.0, fy, hgt)
    o = [defs(p, s), floor(s, 20, 470, fy), body]
    hip, kn, an, toe = J["hip"], J["knee"], J["ankle"], J["toe"]
    th = [ang_deg((b[0] - a[0], b[1] - a[1])) for a, b in ((hip, kn), (kn, an), (an, toe))]   # Definition 2.1
    q = th[0] - th[1]
    sub = lambda n: H.sub(str(n), s)       # noqa: E731
    # horizontal references and the thigh extension at the knee
    ref = hgt * 0.20
    o.append(dline(s, kn[0], kn[1], kn[0] + ref, kn[1]))
    o.append(dline(s, hip[0], hip[1], hip[0] + ref, hip[1]))
    ext = hgt * 0.17
    tu = ((kn[0] - hip[0]), (kn[1] - hip[1]))
    tl = math.hypot(*tu)
    o.append(dline(s, kn[0], kn[1], kn[0] + tu[0] / tl * ext, kn[1] + tu[1] / tl * ext, O["dim"]))
    # segment vectors proximal -> distal (blue)
    for a, b in ((hip, kn), (kn, an), (an, toe)):
        d = (b[0] - a[0], b[1] - a[1])
        L = math.hypot(*d)
        u = (d[0] / L, d[1] / L)
        o.append(white_under(s, a[0], a[1], b[0], b[1], 5))
        o.append(H.arrow(s, p, a[0] + u[0] * s(7), a[1] + u[1] * s(7), b[0] - u[0] * s(8), b[1] - u[1] * s(8), "geometry"))
    # angle arcs from the horizontal (clockwise on screen = negative lab angle)
    s_th, s_sh = -th[0], -th[1]
    r1, r2, r3 = hgt * 0.15, hgt * 0.075, hgt * 0.12
    o.append(arc_plain(s, hip[0], hip[1], r1, 0, s_th, O["geometry"]))
    o.append(arc_plain(s, kn[0], kn[1], r2, 0, s_sh, O["geometry"]))
    o.append(arc_arrow(s, p, kn[0], kn[1], r3, s_th, s_sh, "force"))
    for nm, (mx, my) in (("hip", hip), ("knee", kn), ("ankle", an), ("toe", toe)):
        o.append(mark(s, mx, my, r=6.0))
    # marker names
    o.append(H.label(s, hip[0] - s(14), hip[1] - s(12), f"hip (m{sub(1)})", anchor="end"))
    o.append(H.label(s, kn[0] + s(16), kn[1] - s(9), f"knee (m{sub(2)})"))
    o.append(H.label(s, an[0] - s(16), an[1] + s(5), f"ankle (m{sub(3)})", anchor="end"))
    o.append(H.label(s, toe[0] + s(12), toe[1] - s(8), f"toe (m{sub(4)})"))
    # angle names (values are in the box)
    a1 = math.radians(s_th)
    o.append(H.label(s, hip[0] + r1 * math.cos(a1 / 2) + s(10), hip[1] + r1 * math.sin(a1 / 2) + s(14),
                     f"θ{sub('thigh')}", "label", O["geometry"]))
    a2 = math.radians(s_sh)
    o.append(leader(s, kn[0] + r2 * math.cos(a2), kn[1] + r2 * math.sin(a2), kn[0] - hgt * 0.30 + s(6), kn[1] + hgt * 0.10 - s(4), O["geometry"]))
    o.append(H.label(s, kn[0] - hgt * 0.30, kn[1] + hgt * 0.10, f"θ{sub('shank')}", "label", O["geometry"], "end"))
    qy = kn[1] + r3 * math.sin(a1)
    o.append(leader(s, kn[0] + r3 * math.cos(a1) + s(3), qy, kn[0] + hgt * 0.17, qy, O["force"]))
    o.append(H.label(s, kn[0] + hgt * 0.17 + s(4), qy + s(5), "q (knee)", "label", O["force"]))
    # box with the rule and the numbers
    bx, by, bw = 484.0, 140.0, 262.0
    o.append(box(s, bx, by, bw, s(206), rx=6))
    o.append(H.label(s, bx + s(14), by + s(26), "angles from markers", "label", I["primary"]))
    o.append(H.label(s, bx + s(14), by + s(44), "(Definition 2.1)", "label2", I["secondary"]))
    rows = [f"θ = atan2(Δy, Δx)",
            f"Δ = distal − proximal marker",
            f"θ{sub('thigh')} (m{sub(2)} − m{sub(1)}) = {fmt(th[0])}°",
            f"θ{sub('shank')} (m{sub(3)} − m{sub(2)}) = {fmt(th[1])}°",
            f"θ{sub('foot')} (m{sub(4)} − m{sub(3)}) = {fmt(th[2])}°",
            f"q = θ{sub('thigh')} − θ{sub('shank')} = {fmt(th[0])}° − ({fmt(th[1])}°) = {fmt(q)}°"]
    o.append(lines(s, bx + s(14), by + s(70), rows, "label2", I["primary"], dy=s(21)))
    # lab frame
    ox, oy = 560.0, 560.0
    o.append(H.arrow(s, p, ox, oy, ox + s(60), oy, "dim"))
    o.append(H.arrow(s, p, ox, oy, ox, oy - s(60), "dim"))
    o.append(H.label(s, ox + s(66), oy + s(5), "x", "label", I["primary"], extra='font-style="italic"'))
    o.append(H.label(s, ox - s(4), oy - s(68), "y", "label", I["primary"], "end", 'font-style="italic"'))
    o.append(H.label(s, ox + s(30), oy + s(26), "lab frame (y up)", "label2", I["secondary"], "middle"))
    o.append(LB.credit(s, 20, fy + s(56), width=470))
    aria = ("A person standing with the near knee bent, side-on and facing right, drawn as a skeleton. Four blue marker "
            "discs sit at the hip, knee, ankle and toe. Blue arrows run from each marker to the next along the "
            "thigh, shank and foot. Dashed horizontal lines at the hip and knee give the reference for the segment "
            "angles theta; a red arc at the knee between the thigh line extended and the shank is the knee angle q, "
            + f"{q:.0f}" + " degrees. A box states the rule theta = atan2 of delta y and delta x, distal minus proximal, "
            "with the thigh angle " + f"{th[0]:.0f}" + ", shank angle " + f"{th[1]:.0f}" + " and foot angle " + f"{th[2]:.0f}"
            + " degrees, and a small x-y frame shows the lab axes.")
    return finish(VB, aria, s, o)


# ================================================================ svg #10  Fig. 6 free-body diagram of the shank
M_SEG, I_SEG, L_SEG = 3.3, 0.048, 0.40
A_C, ALPHA = (0.4, 1.2), 3.0
F_D, M_D = (15.0, 690.0), -8.0
INCL, RHO = 75.0, 0.433            # shank inclination to the horizontal; COM fraction from the knee
G_ = 9.81
u_ = (math.cos(math.radians(INCL)), math.sin(math.radians(INCL)))          # ankle -> knee, lab frame (y up)
R_P = (RHO * L_SEG * u_[0], RHO * L_SEG * u_[1])
R_D = (-(1 - RHO) * L_SEG * u_[0], -(1 - RHO) * L_SEG * u_[1])
F_P = tuple(round(v, 1) for v in (M_SEG * A_C[0] - F_D[0], M_SEG * A_C[1] + M_SEG * G_ - F_D[1]))   # as the text rounds it
cross = lambda r, f: r[0] * f[1] - r[1] * f[0]    # noqa: E731
M_P = I_SEG * ALPHA - M_D - cross(R_D, F_D) - cross(R_P, F_P)
assert (round(F_P[0], 1), round(F_P[1], 1)) == (-13.7, -653.7), F_P                         # line 448
assert (round(cross(R_D, F_D), 2), round(cross(R_P, F_P), 1), round(M_P, 1)) == (-37.22, -27.0, 72.4)   # text: -27.00 (rounds r first)
assert (round(math.hypot(*R_P), 3), round(math.hypot(*R_D), 3)) == (0.173, 0.227)


def fig10():
    p = "m15f10_"
    VB = (0, 0, 760, 764)
    s = H.Scale(VB[2], VB[3], max_h=BODY)
    o = [defs(p, s)]
    # ---- recursion strip (top-left)
    o.append(box(s, 20, 18, 270, 112, rx=6))
    o.append(H.label(s, 155, 40, "recursion: distal → proximal", "label2", I["primary"], "middle"))
    for i, (nm, x) in enumerate((("foot", 36), ("shank", 120), ("thigh", 204))):
        hl = nm == "shank"
        o.append(box(s, x, 54, 62, 32, fill="#fff", stroke=O["geometry"] if hl else I["secondary"], rx=5,
                     sw=2.2 if hl else 1.0))
        o.append(H.label(s, x + 31, 75, nm, "label2", I["primary"], "middle"))
    for x in (98, 182):
        o.append(H.arrow(s, p, x + s(2), 70, x + s(20), 70, "dim", w="geom"))
    o.append(H.label(s, 36 + 31, 112, "GRF measured here", "label2", O["force"], "middle"))
    # ---- small person with the shank highlighted
    pfy, phgt = 620.0, 400.0
    body, J = LB.standing_full(p, s, 70.0, pfy, phgt)
    o.append(floor(s, 20, 220, pfy))
    o.append(body)
    kx, ky = J["knee"]
    ax, ay = J["ankle"]
    o.append(f'<line x1="{kx:.2f}" y1="{ky:.2f}" x2="{ax:.2f}" y2="{ay:.2f}" stroke="{O["geometry"]}" stroke-opacity="0.32" '
             f'stroke-width="{0.085 * phgt:.2f}" stroke-linecap="round"/>')
    o.append(H.label(s, 120, pfy + s(26), "the shank, isolated", "label", I["primary"], "middle"))
    # ---- the big shank
    pxm = 700.0                                           # figure units per metre
    Lpx = L_SEG * pxm
    knee = (520.0, 215.0)
    # screen unit vector knee -> ankle (down and back); the lab angle 75 deg is the ankle -> knee line
    d_s = (-u_[0], u_[1])
    ankle = (knee[0] + d_s[0] * Lpx, knee[1] + d_s[1] * Lpx)
    off = LB.OFF["lat_shank"]["ankle"]                    # local knee -> ankle of the art
    k_art = Lpx / math.hypot(*off)
    th_art = math.degrees(math.atan2(d_s[1], d_s[0]) - math.atan2(off[1], off[0]))
    o.append(f'<g transform="translate({knee[0]:.2f} {knee[1]:.2f}) rotate({th_art:.2f}) scale({k_art:.4f})" fill="none">'
             f'<use href="#hbody_lat_shank"/></g>')
    com = (knee[0] + RHO * (ankle[0] - knee[0]), knee[1] + RHO * (ankle[1] - knee[1]))
    # moment arms, blue dashed
    o.append(dline(s, com[0], com[1], knee[0], knee[1], O["geometry"]))
    o.append(dline(s, com[0], com[1], ankle[0], ankle[1], O["geometry"]))
    o.append(H.label(s, (com[0] + knee[0]) / 2 - s(16), (com[1] + knee[1]) / 2 + s(4), f"{it('r')}{H.sub('p', s)} = {math.hypot(*R_P):.3f} m",
                     "label2", O["geometry"], "end"))
    o.append(H.label(s, (com[0] + ankle[0]) / 2 - s(16), (com[1] + ankle[1]) / 2 + s(4),
                     f"{it('r')}{H.sub('d', s)} = {math.hypot(*R_D):.3f} m", "label2", O["geometry"], "end"))
    # joints
    for c in (knee, ankle):
        o.append(H.joint_centre(s, *c))
    o.append(H.label(s, knee[0] - s(26), knee[1] + s(4), "knee (proximal)", "label2", I["secondary"], "end"))
    o.append(H.label(s, ankle[0] - s(26), ankle[1] + s(4), "ankle (distal)", "label2", I["secondary"], "end"))
    # forces
    kF = 0.17                                             # px per N for F_d and F_p
    def vec_screen(F):
        return (F[0], -F[1])                              # lab -> screen
    dd = vec_screen(F_D)
    ld = math.hypot(*dd) * kF
    ud = (dd[0] / math.hypot(*dd), dd[1] / math.hypot(*dd))
    tail_d = (ankle[0] - ud[0] * ld, ankle[1] - ud[1] * ld)
    o.append(white_under(s, *tail_d, *ankle, 5))
    o.append(H.arrow(s, p, tail_d[0], tail_d[1], ankle[0], ankle[1], "reaction"))
    dp_ = vec_screen(F_P)
    lp = math.hypot(*dp_) * kF
    up_ = (dp_[0] / math.hypot(*dp_), dp_[1] / math.hypot(*dp_))
    tail_p = (knee[0] - up_[0] * lp, knee[1] - up_[1] * lp)
    o.append(white_under(s, *tail_p, *knee, 5))
    o.append(H.arrow(s, p, tail_p[0], tail_p[1], knee[0], knee[1], "reaction"))
    o.append(H.label(s, tail_d[0] - s(10), tail_d[1] + s(8), f"{it('F')}{H.sub('d', s)} = (15, 690) N", "label", I["primary"], "end"))
    o.append(H.label(s, tail_d[0] - s(10), tail_d[1] + s(28), "known: handed up from the foot", "label2", I["secondary"], "end"))
    o.append(H.label(s, tail_p[0] + s(12), tail_p[1] + s(8), f"{it('F')}{H.sub('p', s)} = (−13.7, −653.7) N", "label", I["primary"]))
    o.append(H.label(s, tail_p[0] + s(12), tail_p[1] + s(28), "unknown: the Newton step", "label2", I["secondary"]))
    # gravity at the COM (longer than its scale, see the note)
    gl = 52.0
    o.append(white_under(s, com[0], com[1], com[0], com[1] + gl, 5))
    o.append(H.arrow(s, p, com[0], com[1], com[0], com[1] + gl, "load"))
    o.append(H.com_mark(s, *com))
    o.append(H.label(s, com[0] + s(14), com[1] + gl - s(2), f"{it('m g')} = {M_SEG * G_:.0f} N", "label2", O["load"]))
    o.append(H.label(s, com[0] + s(14), com[1] - s(8), "COM", "label2", I["primary"]))
    # moments: M_p counter-clockwise at the knee (positive), M_d clockwise at the ankle (negative)
    o.append(arc_arrow(s, p, knee[0], knee[1], s(36), 50, -70, "force"))
    o.append(H.label(s, knee[0] + s(44), knee[1] + s(30), f"{it('M')}{H.sub('p', s)} = {M_P:.1f} N·m", "label", O["force"]))
    o.append(H.label(s, knee[0] + s(44), knee[1] + s(50), "unknown: the Euler step", "label2", I["secondary"]))
    o.append(arc_arrow(s, p, ankle[0], ankle[1], s(30), -80, 30, "force"))
    o.append(H.label(s, ankle[0] + s(38), ankle[1] - s(22), f"{it('M')}{H.sub('d', s)} = −8 N·m", "label2", O["force"]))
    # zoom line from the person
    o.append(dline(s, (kx + ax) / 2 + s(30), (ky + ay) / 2, com[0] - s(60), com[1] + s(10), I["rule"]))
    # numbers
    rows = [f"Newton: {it('F')}{H.sub('p', s, 'label2')} = {it('m a')}{H.sub('c', s, 'label2')} − {it('m g')} − {it('F')}{H.sub('d', s, 'label2')} "
            f"= ({fmt(F_P[0], 1)}, {fmt(F_P[1], 1)}) N",
            f"Euler: {it('M')}{H.sub('p', s, 'label2')} = {it('I α')} − {it('M')}{H.sub('d', s, 'label2')} − {it('r')}{H.sub('d', s, 'label2')} × "
            f"{it('F')}{H.sub('d', s, 'label2')} − {it('r')}{H.sub('p', s, 'label2')} × {it('F')}{H.sub('p', s, 'label2')}",
            f"= {I_SEG * ALPHA:.2f} + {-M_D:.0f} + {-cross(R_D, F_D):.2f} + {-cross(R_P, F_P):.2f} = {M_P:.1f} N·m"]
    o.append(box(s, 250, 650, 490, 70, rx=6))
    o.append(lines(s, 264, 672, rows, "label2", I["primary"], dy=s(21)))
    o.append(H.label(s, 740, 30, f"{it('F')}{H.sub('d', s, 'label2')} and {it('F')}{H.sub('p', s, 'label2')} to one scale;", "label2",
                     I["secondary"], "end"))
    o.append(H.label(s, 740, 48, f"{it('m g')} drawn longer than its scale", "label2", I["secondary"], "end"))
    o.append(LB.credit(s, 20, 744, width=720))
    aria = ("Free-body diagram of the shank in a mid-squat. At left a small standing person has the shank highlighted. "
            "At right the shank, a bone drawing inclined 75 degrees to the horizontal with the knee up and forward, "
            "carries the known ankle reaction F d of 15 and 690 newtons pointing up into the ankle, the unknown knee "
            "reaction F p of minus 13.7 and minus 653.7 newtons pointing down into the knee, the weight m g of 32 "
            "newtons at the centre of mass, and two moments: the ankle moment M d of minus 8 newton-metres and the net "
            "knee moment M p of 72.4 newton-metres. Dashed blue moment arms r p of 0.173 metres and r d of 0.227 "
            "metres run from the centre of mass to the knee and ankle. A strip at top-left shows the recursion from "
            "foot to shank to thigh. The Newton and Euler steps of the text are written below with their numbers.")
    return finish(VB, aria, s, o)


# ================================================================ problem figures (display width 400)
def prob_scale(w, h):
    return H.Scale(w, h, display_w=400, max_h=BODY)


def fig23():                                   # C1 the number you never measured
    p = "m15f23_"
    VB = (0, 0, 400, 392)
    s = prob_scale(VB[2], VB[3])
    o = [defs(p, s)]
    fy, hgt = 252.0, 200.0
    body, J = LB.standing_full(p, s, 30.0, fy, hgt)
    o += [floor(s, 6, 112, fy), body, plate(s, J["heel"][0] - s(10), J["toe"][0] + s(14), fy, 8.0)]
    for k in ("shoulder", "hip", "knee", "ankle"):
        o.append(mark(s, *J[k], r=4.5))
    o.append(grf_arrow(s, p, J["com"][0], fy, 50.0))
    o.append(H.label(s, 8, 22, "no sensor reads torque", "label", I["primary"]))
    o.append(H.label(s, 8, fy + s(36), "measured:", "label2", I["primary"]))
    o.append(H.label(s, 8, fy + s(52), "marker positions,", "label2", I["secondary"]))
    o.append(H.label(s, 8, fy + s(68), "ground reaction", "label2", I["secondary"]))
    bx, by, bw, bh = 146.0, 118.0, 120.0, 100.0
    o.append(H.arrow(s, p, 104, 168, bx - s(3), 168, "dim", w="geom"))
    o.append(box(s, bx, by, bw, bh, rx=7))
    o.append(H.label(s, bx + bw / 2, by + 34, "model", "label", I["primary"], "middle"))
    o.append(H.label(s, bx + bw / 2, by + 58, "equations of", "label2", I["secondary"], "middle"))
    o.append(H.label(s, bx + bw / 2, by + 74, "motion, run", "label2", I["secondary"], "middle"))
    o.append(H.label(s, bx + bw / 2, by + 90, "backwards", "label2", I["secondary"], "middle"))
    o.append(H.arrow(s, p, bx + bw, 168, 296, 168, "force"))
    o.append(H.label(s, 304, 160, "τ", "label", O["force"]))
    o.append(H.label(s, 304, 182, "inferred,", "label2", O["force"]))
    o.append(H.label(s, 304, 198, "never read", "label2", I["secondary"]))
    o.append(LB.credit(s, 8, 340, width=384))
    aria = ("C1. A standing person with blue marker discs on a force plate with a red ground-reaction arrow, labelled "
            "measured: marker positions, ground reaction. An arrow leads into a box, a model of the equations of "
            "motion run backwards, and out to the joint torque tau, labelled inferred, never read. The title says no "
            "sensor reads torque.")
    return finish(VB, aria, s, o)


def fig24():                                   # C2 the odd instrument out
    p = "m15f24_"
    VB = (0, 0, 400, 380)
    s = prob_scale(VB[2], VB[3])
    o = [defs(p, s)]
    fy, hgt = 252.0, 200.0
    b1, J1 = LB.standing_full(p, s, 40.0, fy, hgt)
    b2, J2 = LB.standing_full(p, s, 232.0, fy, hgt)
    o += [floor(s, 4, 192, fy), b1, plate(s, J1["heel"][0] - s(24), J1["toe"][0] + s(24), fy, 8.0)]
    o.append(grf_arrow(s, p, J1["com"][0], fy, 80.0))
    o.append(cop_mark(s, J1["com"][0], fy))
    o.append(H.label(s, J1["com"][0] + s(14), fy - s(54), "direct force", "label", O["force"]))
    o.append(H.label(s, 8, 22, "measured force vs measured position", "label", I["primary"]))
    o.append(H.label(s, 96, fy + s(36), "force plate", "label2", I["primary"], "middle"))
    o.append(H.label(s, 96, fy + s(52), "reads the force itself", "label2", I["secondary"], "middle"))
    o.append(floor(s, 208, 396, fy))
    o.append(b2)
    for k in ("shoulder", "hip", "knee", "ankle"):
        o.append(mark(s, *J2[k], r=4.5))
    cam_x, cam_y = 336.0, 120.0
    for tgt in ((J2["shoulder"][0] + s(12), J2["shoulder"][1]), (J2["ankle"][0] + s(14), J2["ankle"][1] - s(8))):
        o.append(dline(s, cam_x, cam_y + s(15), tgt[0], tgt[1], I["rule"]))
    o.append(camera(s, cam_x, cam_y))
    o.append(H.label(s, 300, fy + s(36), "camera", "label2", I["primary"], "middle"))
    o.append(H.label(s, 300, fy + s(52), "reads positions only", "label2", I["secondary"], "middle"))
    o.append(LB.credit(s, 8, 330, width=384))
    aria = ("C2. Two standing people side by side. At left one stands on a force plate, with a red upward arrow labelled "
            "direct force and the caption force plate reads the force itself. At right one wears blue marker discs "
            "and is filmed by a camera, with the caption camera reads positions only. The title contrasts measured "
            "force with measured position.")
    return finish(VB, aria, s, o)


def fig28():                                   # C6 why start at the foot
    p = "m15f28_"
    VB = (0, 70, 400, 576)
    s = prob_scale(VB[2], VB[3])
    o = [defs(p, s)]
    fy, hgt = 540.0, 420.0
    body, J = LB.standing_full(p, s, 30.0, fy, hgt)
    o += [floor(s, 6, 170, fy), body, plate(s, J["heel"][0] - s(18), J["toe"][0] + s(20), fy, 8.0)]
    o.append(H.label(s, 8, 94, "recursion starts at the foot", "label", I["primary"]))
    o.append(grf_arrow(s, p, J["com"][0], fy, 80.0))
    o.append(H.label(s, J["com"][0] + s(10), fy - s(62), "GRF (known)", "label2", O["force"]))
    o.append(cop_mark(s, J["com"][0], fy))
    sites = [(J["ankle"], "foot", ["GRF is measured:", "the ankle load follows"], O["force"]),
             (J["knee"], "shank", ["handed the ankle load:", "the knee load follows"], I["secondary"]),
             (J["hip"], "thigh", ["handed the knee load:", "the hip load follows"], I["secondary"])]
    xl = 206.0
    ys = []
    for i, ((jx, jy), nm, desc, col) in enumerate(sites):
        ly = jy - (s(4) if i == 0 else 0)
        ys.append(ly)
        o.append(leader(s, jx + s(10), jy, xl - s(12), ly))
        o.append(badge(s, xl, ly, i + 1, col))
        o.append(H.label(s, xl + s(18), ly + s(5), nm, "label", I["primary"]))
        o.append(H.label(s, xl + s(18), ly + s(23), desc[0], "label2", col if i == 0 else I["secondary"]))
        o.append(H.label(s, xl + s(18), ly + s(39), desc[1], "label2", I["secondary"]))
    for ya, yb in zip(ys[:-1], ys[1:]):
        o.append(H.arrow(s, p, xl, ya - s(13), xl, yb + s(14), "dim", w="geom"))
    o.append(LB.credit(s, 8, 590, width=384))
    aria = ("C6. A standing person on a force plate with a red upward ground-reaction arrow. Three numbered discs mark "
            "the steps up the chain: one, the foot, where the ground reaction is measured and the ankle load follows; "
            "two, the shank, handed the ankle load, giving the knee load; three, the thigh, handed the knee load, "
            "giving the hip load. Grey arrows run upward from disc to disc.")
    return finish(VB, aria, s, o)


FIGS = {
    2: ("Winter-proportion body with motion-capture markers and force", fig2),
    3: ("The measurement-to-torque pipeline: a person recorded by cam", fig3),
    4: ("Five measurement instruments around a squatting person: opti", fig4),
    6: ("A recognizable standing person: a planar leg of three shaded", fig6),
    10: ("A small standing person at left shows which segment is isola", fig10),
    23: ("C1: the number you never measured. The course spent fourteen", fig23),
    24: ("C2: the odd instrument out. Of the five mechanical instrumen", fig24),
    28: ("C6: why start at the foot. The Newton-Euler recursion runs d", fig28),
}
