"""Module 3, group `plots`: the main-text plots and the K-problem plots in the house style.

svg #3 (constraint ledger), #13 (hip reaction vs b), #16 (Hertz p0 vs E*), #17 (shrinking contact, frames),
#19 (stability vs mobility), #23 (lab forces over a half-swing) are main-text figures (760 px);
#54 (K3), #56 (K4), #58 (K5), #60 (K6), #64 (K8), #66 (K9) are problem figures (400 px).
Every plotted number is computed here: (4.1) for #13, (5.2) for #16 and #17, (6.1) and ROM = 180 - beta - 30 deg
for #19, and the section 7.4 lab script (ported line for line in run()) for #23 and every K plot. The numbers the
module prints are asserted against these computations.
"""
import html
import math
from functools import lru_cache

import numpy as np

import house as H
from m05.plots_main import Ax, axes, curve, dot, legend, tw
from m05.plots_prob import Plot, label as plabel, legend as plegend

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
GRID = "#e6e6e6"
DASH_SER = (7, 4)
W = 400                       # problem figures: viewBox width = rendered width


def it(t):
    return f'<tspan font-style="italic">{t}</tspan>'


def sub(t, s, size="label"):
    return H.sub(t, s, size)


def sup(t, s, size="label"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def mn(v, f="{:.2f}"):
    t = f.format(v)
    return "−" + t[1:] if t.startswith("-") else t


def svg(vb, aria, s, body, extra=""):
    return H.svg_open(vb, html.escape(aria), s, extra=extra) + "".join(body) + "</svg>"


def poly(s, pts, col, w="curve", dash=None, extra=""):
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    return (f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{col}" '
            f'stroke-width="{s(H.PX[w]):.2f}" stroke-linejoin="round"{da} {extra}/>')


def thin(n, nmax=250):
    """Indices that keep at most nmax samples (first and last kept)."""
    k = max(1, -(-n // nmax))
    idx = list(range(0, n, k))
    return idx if idx[-1] == n - 1 else idx + [n - 1]


# ================================================================ section 7.4 lab, ported line for line
LAB = dict(L1=0.30, L2=0.30, m1=2.0, m2=1.5, yh=-0.48, amp=40.0, gd=40.0, gp=40.0)


def run(**kw):
    """module03.html:1305-1374 with its parameters as arguments (as `from lab import run` in K2-K9). Each run takes
    about 3 s, so runs are cached by their full parameter set (run() and run(amp=40) are one run)."""
    q = {**LAB, **{k: float(v) for k, v in kw.items()}}
    return _run(*(q[k] for k in LAB))


@lru_cache(maxsize=None)
def _run(L1, L2, m1, m2, yh, amp, gd, gp):
    g, dt, nstep = 9.81, 5e-5, 40000
    M = np.diag([m1, m1, m2, m2])
    Q = np.array([0, -m1*g, 0, -m2*g])

    def constraints(q):
        x1, y1, x2, y2 = q
        return np.array([0.5*(x1*x1 + y1*y1 - L1*L1), 0.5*((x2-x1)**2 + (y2-y1)**2 - L2*L2), y2 - yh])

    def Jc(q):
        x1, y1, x2, y2 = q
        return np.array([[x1, y1, 0., 0.], [-(x2-x1), -(y2-y1), x2-x1, y2-y1], [0., 0., 0., 1.]])

    def dJc(q, dq):
        dx1, dy1, dx2, dy2 = dq
        return np.array([[dx1, dy1, 0., 0.], [-(dx2-dx1), -(dy2-dy1), dx2-dx1, dy2-dy1], [0., 0., 0., 0.]])

    th = np.radians(-90.0 + amp)
    x1, y1 = L1*np.cos(th), L1*np.sin(th)
    x2 = x1 + np.sqrt(L2*L2 - (yh - y1)**2)
    q = np.array([x1, y1, x2, yh])
    dq = np.zeros(4)
    hist = {"t": [], "Rs": [], "Re": [], "Nc": [], "x2": [], "gerr": []}
    for step in range(nstep):
        J, dJ, gv = Jc(q), dJc(q, dq), constraints(q)
        A = np.block([[M, J.T], [J, np.zeros((3, 3))]])
        rhs = np.concatenate([Q, -(dJ@dq) - 2*gd*(J@dq) - gp*gp*gv])
        sol = np.linalg.solve(A, rhs)
        ddq, lam = sol[:4], -sol[4:]
        Rs, Re, Nc = abs(lam[0])*L1, abs(lam[1])*L2, lam[2]
        for key, val in zip(hist, (step*dt, Rs, Re, Nc, q[2], np.abs(gv).max())):
            hist[key].append(val)
        dq = dq + dt*ddq
        q = q + dt*dq
    return {k: np.array(v) for k, v in hist.items()}


WL = (2.0 + 1.5) * 9.81                      # limb weight, N


def turn(h):
    """K7: index of the first MINIMUM of x2 (the inner turning point; the hand first moves outward)."""
    v = np.diff(h["x2"])
    return int(np.flatnonzero((v[:-1] < 0) & (v[1:] >= 0))[0] + 1)


def close(v, ref, tol):
    assert abs(v - ref) <= tol * 1.0001, (v, ref)


@lru_cache(maxsize=None)
def lab_checked():
    """The base run, checked against the printed output at module03.html:1369-1374 and K5, K7 (2083-2085, 2124)."""
    h = run()
    close(WL, 34.34, 0.005)
    close(h["Rs"][0], 11.64, 0.005)
    close(h["Rs"].max(), 32.61, 0.005)
    close(h["Re"].max(), 11.61, 0.005)
    close(h["Nc"].max(), 22.32, 0.005)
    close(h["Nc"].min(), 6.21, 0.005)
    close(h["gerr"].max(), 1.03e-6, 0.005e-6)
    close(h["t"][turn(h)], 0.756, 0.0005)
    return h


# ================================================================ svg #3: the constraint ledger
def fig3():
    VB = (0, 0, 760, 300)
    s = H.Scale(VB[2], VB[3])
    x0, x1 = 100, 520
    u = (x1 - x0) / 6
    rows = [("shoulder", 3, "3 rotations", "3 translations"), ("hip", 3, "3 rotations", "3 translations"),
            ("knee", 1, "flex–ext", "3 translations + 2 rotations"), ("elbow", 1, "flex–ext", "3 translations + 2 rotations")]
    top, bh, gap = 56, 34, 18
    grey = I["rule"]
    o = []
    lx = x0
    for col, op, txt in ((SER[1], 0.85, f"degrees of freedom kept (mobility), {it('f')}"),
                         (grey, 0.35, f"freedoms removed = constraints (stability), 6 − {it('f')}")):
        o.append(f'<rect x="{lx}" y="12" width="22" height="12" fill="{col}" fill-opacity="{op}"/>')
        o.append(H.label(s, lx + 29, 23, txt, "label2", I["primary"]))
        lx += 29 + tw(txt) + 30
    for v in range(7):
        x = x0 + v * u
        o.append(H.line(s, x, top - 6, x, top + 4 * (bh + gap) - gap + 6, GRID, "leader"))
    panels = []
    for k, (name, f, kept, rem) in enumerate(rows):
        y = top + k * (bh + gap)
        o.append(H.label(s, x0 - 12, y + bh / 2 + 5, name, "label", I["primary"], "end"))
        o.append(f'<rect x="{x0:.2f}" y="{y}" width="{f * u:.2f}" height="{bh}" fill="{SER[1]}" fill-opacity="0.85"/>')
        o.append(f'<rect x="{x0 + f * u:.2f}" y="{y}" width="{(6 - f) * u:.2f}" height="{bh}" fill="{grey}" fill-opacity="0.35"/>')
        fs = s(H.PX["label2"])
        o.append(f'<text x="{x0 + f * u / 2:.2f}" y="{y + bh / 2 + 4.5:.2f}" font-size="{fs:.2f}" fill="#fff" '
                 f'text-anchor="middle">{kept}</text>')
        o.append(H.label(s, x0 + (f + 6) * u / 2, y + bh / 2 + 4.5, rem, "label2", I["primary"], "middle"))
        o.append(H.label(s, x1 + 10, y + bh / 2 + 5, f"{f} + {6 - f} = 6", "label2", I["secondary"]))
        box = [x0, y - gap / 2, x1, y + bh + gap / 2]
        panels.append((box, [[x0 + f * u / 2, y + bh / 2, f"{name}: f = {f} kept ({kept})"],
                             [x0 + (f + 6) * u / 2, y + bh / 2, f"{name}: 6 − f = {6 - f} removed ({rem})"]]))
    yb = top + 4 * (bh + gap) - gap
    o.append(H.line(s, x0, yb + 6, x1, yb + 6, I["axis"], "axis"))
    for v in range(7):
        o.append(H.line(s, x0 + v * u, yb + 6, x0 + v * u, yb + 11, I["axis"], "leader"))
        o.append(H.label(s, x0 + v * u, yb + 26, f"{v}", "tick", I["secondary"], "middle"))
    o.append(H.label(s, (x0 + x1) / 2, yb + 48, "freedoms of a rigid body (6 in all)", "label", I["primary"], "middle"))
    # shoulder and hip: same ledger, different stiffness (section 6)
    bx = 606
    ya, yb2 = top + 2, top + bh + gap + bh - 2
    o.append(f'<path d="M{bx - 6},{ya} h6 V{yb2} h-6" fill="none" stroke="{I["secondary"]}" stroke-width="{s(1):.2f}"/>')
    ym = (ya + yb2) / 2
    lines = ["same ledger, but", "the hip’s deeper", f"socket ({it('β')} ≈ 55°", "against 22°) makes", "each constraint",
             "stiffer (§6)"]
    for i, t in enumerate(lines):
        o.append(H.label(s, bx + 8, ym - 37 + i * 16, t, "label2", I["secondary"]))
    aria = ("Constraint ledger as stacked horizontal bars, one per joint, each six unit freedoms long. Shoulder and hip keep "
            "3 freedoms, their 3 rotations, and remove 3, the 3 translations. Knee and elbow keep 1, flexion-extension, and "
            "remove 5, three translations and two rotations. Blue is the freedoms kept for mobility, grey the constraints kept "
            "for stability. A bracket notes that shoulder and hip have the same ledger, but the hip's deep socket "
            "(coverage about 55 degrees against 22) makes each constraint stiffer.")
    return svg(VB, aria, s, o, H.hover_attr(panels))


# ================================================================ svg #13: hip reaction and abductor force vs b
def fig13():
    VB = (0, 0, 760, 392)
    s = H.Scale(VB[2], VB[3])
    a, Ws = 5.0, 5.0 / 6.0                                  # cm, W  (module03.html:807, 850)
    R = lambda b: Ws * (1 + b / a)                          # noqa: E731  (4.1)
    F = lambda b: Ws * b / a                                # noqa: E731
    close(R(10), 2.5, 1e-9)
    close(R(2.8), 1.30, 0.005)                              # the lean of svg #14's caption (module03.html:939)
    close(R(12), 2.83, 0.005)                               # old aria: "rises from about 0.8 to 2.8"
    ax = Ax((80, 50, 700, 320), (0, 12), (0, 3.2))
    o = axes(s, ax, [(v, f"{v}") for v in (0, 2, 4, 6, 8, 10, 12)], [(v, f"{v}") for v in (0, 1, 2, 3)],
             f"centre-of-mass offset {it('b')} (cm), abductor arm {it('a')} = 5 cm",
             f"force (× body weight {it('W')})", ylab_x=30)
    bs = np.linspace(0, 12, 241)
    o.append(H.line(s, ax.X(0), ax.Y(Ws), ax.X(12), ax.Y(Ws), O["dim"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(7.6), ax.Y(Ws) + 18, f"supported weight {it('W')}{sub('s', s)} = 5/6 {it('W')} ≈ 0.83 {it('W')}",
                     "label2", I["secondary"], "middle"))
    o.append(curve(s, ax, [0, 12], [F(0), F(12)], SER[1], "curve_multi"))      # both are straight lines in b
    o.append(curve(s, ax, [0, 12], [R(0), R(12)], SER[0], "curve_multi"))
    # the gap between the two lines is W_s at every b: R = W_s + F_ab
    xg = ax.X(11.2)
    o.append(H.line(s, xg, ax.Y(F(11.2)) - 4, xg, ax.Y(R(11.2)) + 4, O["dim"], "ref",
                    extra=f'marker-start="url(#m3f13_a_dim)" marker-end="url(#m3f13_a_dim)"'))
    o.append(H.label(s, xg + 8, (ax.Y(F(11.2)) + ax.Y(R(11.2))) / 2 + 5, f"{it('W')}{sub('s', s)}", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(8.1), ax.Y(R(8.1)) - 14, f"hip reaction {it('R')} = {it('W')}{sub('s', s)}(1 + {it('b')}/{it('a')})",
                     "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(8.6), ax.Y(F(8.6)) + 22, f"abductor force {it('F')}{sub('ab', s)} = {it('W')}{sub('s', s)} {it('b')}/{it('a')}",
                     "label2", I["primary"], "start"))
    for b, lines, dx, dy, anc in ((10.0, ["upright: b = 10 cm, R = 2.50 W"], -8, -14, "end"),
                                  (2.8, ["lean: b = 2.8 cm,", "R = 1.30 W"], 10, 19, "start")):
        o.append(dot(s, ax.X(b), ax.Y(R(b)), SER[0]))
        for i, txt in enumerate(lines):
            o.append(H.label(s, ax.X(b) + dx, ax.Y(R(b)) + dy + 16 * i, txt, "label2", I["primary"], anc))
    o += legend(s, ax.x0 + 14, 30, [(SER[0], None, "hip reaction R"), (SER[1], None, "abductor force Fab"),
                                    (O["dim"], H.DASH_REF, "supported weight Ws")])
    aria = ("Plot of the hip joint reaction R and the abductor force F ab, in units of body weight W, against the "
            "centre-of-mass offset b from 0 to 12 centimetres, from equation 4.1 with abductor arm a = 5 cm and supported "
            "weight Ws = 5/6 W. The abductor force rises from 0 to 2.0 W; the reaction runs parallel to it, a constant Ws = "
            "0.83 W higher, from 0.83 to 2.83 W. Two points are marked: upright, b = 10 cm, R = 2.50 W; leaning, b = 2.8 cm, "
            "R = 1.30 W.")
    hv = [[ax.X(b), [ax.Y(R(b)), ax.Y(F(b))], f"b = {b:.1f} cm: R = {R(b):.2f} W, Fab = {F(b):.2f} W"] for b in bs[::2]]
    return svg(VB, aria, s, [f"<defs>{H.markers('m3f13_', s)}</defs>"] + o, H.hover_attr(ax.box, hv))


# ================================================================ svg #16: Hertz peak pressure vs E*
F_HIP, R_EFF = 1715.0, 0.030                     # N, m  (module03.html:963, 1033)


def p0_hertz(E, F=F_HIP, R=R_EFF):
    return (6 * F * E**2 / (math.pi**3 * R**2)) ** (1 / 3)          # (5.2), Pa


def a_hertz(E, F=F_HIP, R=R_EFF):
    return (3 * F * R / (4 * E)) ** (1 / 3)                          # (5.2), m


def fig16():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    # module03.html:1004: E* = 10/(2 x 0.75) = 6.67 MPa and 17 000/(2 x 0.91) = 9.34 GPa. The caption (1033) gives
    # a = 17.9 mm, which needs the rounded 6.7 MPa; the exact 6.67 MPa gives 17.95 mm (reported as a text note)
    E_c, E_b = 10e6 / (2 * (1 - 0.5**2)), 17e9 / (2 * (1 - 0.3**2))
    pc, pb, ac = p0_hertz(E_c) / 1e6, p0_hertz(E_b) / 1e6, a_hertz(E_c)
    close(E_c / 1e6, 6.7, 0.05)
    close(E_b / 1e9, 9.3, 0.05)
    close(pc, 2.5, 0.05)
    close(pb, 320, 5)
    close(pb / pc, 125, 1)
    close(ac * 1e3, 17.95, 0.005)
    close(math.pi * ac**2 * 1e4, 10.1, 0.05)
    ax = Ax((90, 30, 720, 310), (1e6, 1e11), (0.1, 1000), xlog=True, ylog=True)
    xt = [(1e6, "1 MPa"), (1e7, "10 MPa"), (1e8, "100 MPa"), (1e9, "1 GPa"), (1e10, "10 GPa"), (1e11, "100 GPa")]
    yt = [(0.1, "0.1"), (1, "1"), (10, "10"), (100, "100"), (1000, "1000")]
    o = [f'<rect x="{ax.x0}" y="{ax.Y(25):.2f}" width="{ax.x1 - ax.x0}" height="{ax.Y(15) - ax.Y(25):.2f}" fill="{O["flag"]}" '
         f'opacity="0.22"/>']
    o += axes(s, ax, xt, yt, f"effective modulus {it('E')}* (log scale)", f"peak pressure {it('p')}{sub('0', s)} (MPa, log scale)",
              ylab_x=30)
    o.append(H.label(s, ax.X(2.2e10), ax.Y(25) - 7, "cartilage damage ≈ 15–25 MPa", "label2", I["primary"], "end"))
    Es = np.logspace(6, 11, 201)
    ps = [p0_hertz(E) / 1e6 for E in Es]
    o.append(curve(s, ax, Es, ps, SER[0]))
    o.append(dot(s, ax.X(E_c), ax.Y(pc), SER[0], r=5))
    o.append(dot(s, ax.X(E_b), ax.Y(pb), SER[0], r=5))
    xc, yc = ax.X(E_c) + 12, ax.Y(pc) + 14
    o.append(H.label(s, xc, yc, f"cartilage on cartilage: {it('E')}* = {E_c / 1e6:.2f} MPa, {it('p')}{sub('0', s, 'label2')} ≈ {pc:.1f} MPa", "label2"))
    o.append(H.label(s, xc, yc + 17, f"contact radius {it('a')} = {ac * 1e3:.2f} mm, area π{it('a')}² = {math.pi * ac**2 * 1e4:.1f} cm²",
                     "label2", I["secondary"]))
    o.append(H.label(s, ax.X(E_b) - 12, ax.Y(pb) - 10, f"bone on bone: {it('E')}* = {E_b / 1e9:.1f} GPa, {it('p')}{sub('0', s, 'label2')} ≈ {pb:.0f} MPa "
                     f"({pb / pc:.0f}× higher)", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.x0 + 10, ax.top + 34,
                     f"slope 2/3: {it('p')}{sub('0', s, 'label2')} ∝ {it('E')}*{sup('2/3', s, 'label2')}", "label2", I["secondary"], "start"))
    o.append(H.label(s, ax.x0 + 10, ax.top + 16,
                     f"{it('F')} = 1715 N, {it('R')}{sub('eff', s, 'label2')} = 30 mm", "label2", I["secondary"]))
    aria = ("Log-log plot of the Hertz peak contact pressure p0 against the effective modulus E*, for a joint force of "
            "1715 N and an effective radius of 30 mm. The line has slope two thirds. Cartilage on cartilage, E* = "
            f"{E_c / 1e6:.1f} MPa, gives p0 of about {pc:.1f} MPa with a contact radius of {ac * 1e3:.1f} mm, area "
            f"{math.pi * ac**2 * 1e4:.1f} square centimetres, well below the shaded cartilage-damage band at 15 to 25 MPa. "
            f"Bone on bone, E* = {E_b / 1e9:.1f} GPa, gives about {pb:.0f} MPa, {pb / pc:.0f} times higher.")
    hv = [[ax.X(E), ax.Y(p), f"E* = {E / 1e6:.3g} MPa: p0 = {p:.3g} MPa, a = {a_hertz(E) * 1e3:.3g} mm"]
          for E, p in zip(Es, ps)]
    return svg(VB, aria, s, o, H.hover_attr(ax.box, hv))


# ================================================================ svg #17: fixed force, shrinking contact (frames)
def fig17():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    p = "m3f17_"
    radii = list(range(20, 6, -1))                    # mm: 20 .. 7 (caption, module03.html:1061)
    p0 = {a: 3 * F_HIP / (2 * math.pi * (a / 1e3) ** 2) / 1e6 for a in radii}
    close(p0[20], 2.05, 0.01)                         # "from about 2 MPa"
    close(p0[7], 16.7, 0.05)                          # "to about 17 MPa"
    close((20 / 19) ** 2 - 1, 0.11, 0.005)   # 11 % per mm at 20 mm (module03.html:1042)
    close((7 / 6) ** 2 - 1, 0.36, 0.005)              # 36 % per mm at 7 mm
    ax = Ax((90, 40, 720, 300), (-24, 24), (0, 27))
    o = [f"<defs>{H.markers(p, s)}</defs>",
         f'<rect x="{ax.x0}" y="{ax.Y(25):.2f}" width="{ax.x1 - ax.x0}" height="{ax.Y(15) - ax.Y(25):.2f}" fill="{O["flag"]}" '
         f'opacity="0.22"/>']
    o += axes(s, ax, [(v, f"{v}" if v >= 0 else f"−{-v}") for v in (-20, -10, 0, 10, 20)],
              [(v, f"{v}") for v in (0, 5, 10, 15, 20, 25)], f"distance from the contact centre {it('r')} (mm)",
              f"contact pressure {it('p')} (MPa)", ylab_x=30, xlab_dy=84)
    o.append(H.label(s, ax.x1 - 6, ax.Y(25) + 17, "cartilage damage ≈ 15–25 MPa", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.x0 + 8, ax.top + 2, f"fixed joint force {it('F')} = 1715 N;  {it('p')}{sub('0', s, 'label2')} = 3{it('F')}/(2π{it('a')}²) ∝ 1/{it('a')}²",
                     "label2", I["secondary"]))

    def dome(a, n=41):
        """p(r) = p0 sqrt(1 - (r/a)^2), sampled as r = a sin(phi), p = p0 cos(phi): dense where the dome is steep."""
        ph = np.linspace(-math.pi / 2, math.pi / 2, n)
        return [(ax.X(a * math.sin(f)), ax.Y(p0[a] * math.cos(f))) for f in ph]

    for a in radii:                                   # every frame carries F: the integral of p 2 pi r dr
        rr = np.linspace(0, a / 1e3, 4001)
        load = np.trapezoid(p0[a] * 1e6 * np.sqrt(np.clip(1 - (rr / (a / 1e3)) ** 2, 0, None)) * 2 * np.pi * rr, rr)
        close(load, F_HIP, 1.0)
        assert ax.Y(p0[a]) > VB[1] + 20                # the tallest dome stays inside the plot
    ghost = dome(20)
    o.append(poly(s, ghost, I["rule"], "curve_multi", DASH_SER))
    o.append(H.label(s, ax.X(-14), ax.Y(0.9 * p0[20]) - 12, f"start: {it('a')} = 20 mm", "label2", I["muted"], "end"))
    frames, last = [], len(radii) - 1
    for k, a in enumerate(radii):
        d = dome(a)
        fill = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in d) + " Z"
        nxt = (a / (a - 1)) ** 2 - 1
        body = [f'<path d="{fill}" fill="{SER[0]}" fill-opacity="0.18"/>', poly(s, d, SER[0]),
                dot(s, ax.X(0), ax.Y(p0[a]), SER[0]),
                H.line(s, ax.X(-a), ax.y0 + 34, ax.X(a), ax.y0 + 34, O["geometry"], "geom",
                       extra=f'marker-start="url(#{p}a_geometry)" marker-end="url(#{p}a_geometry)"'),
                H.label(s, ax.X(0), ax.y0 + 54, f"contact patch 2{it('a')} = {2 * a} mm", "label2", I["primary"], "middle"),
                H.label(s, ax.X(0) + 12, ax.Y(p0[a]) - 8, f"{it('p')}{sub('0', s)} = {p0[a]:.1f} MPa", "label", I["primary"]),
                H.label(s, ax.x0 + 12, ax.Y(13), f"{it('a')} = {a} mm", "label", I["primary"]),
                H.label(s, ax.x0 + 12, ax.Y(13) + 18, f"losing 1 mm more: +{nxt * 100:.0f} %", "label2", I["secondary"])]
        frames.append(H.frame(k, last, "".join(body)))
    o += frames
    aria = ("Hertz pressure dome p(r) = p0 times the square root of 1 minus (r/a) squared under a fixed joint force of 1715 N, "
            "drawn to scale as the contact radius a shrinks from 20 mm to 7 mm, one frame per millimetre. The peak p0 = "
            f"3F/(2 pi a squared) rises from {p0[20]:.1f} MPa at a = 20 mm to {p0[7]:.1f} MPa at a = 7 mm, into the shaded "
            "cartilage-damage band at 15 to 25 MPa. Each frame states how much one more millimetre of lost radius would raise "
            "the peak: 11 percent at 20 mm, 36 percent at 7 mm. A dashed outline keeps the starting 20 mm dome. The still "
            "frame shows a = 7 mm.")
    return svg(VB, aria, s, o, H.frames_attr("contact radius a", [f"{a} mm" for a in radii], last))


# ================================================================ svg #19: stability vs mobility along beta
def fig19():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    TH_N = 30.0
    rom = lambda b: 180.0 - b - TH_N                  # noqa: E731  (module03.html:1161)
    mob = lambda b: rom(b) / rom(10.0)                # noqa: E731
    S = lambda b: math.tan(math.radians(b))           # noqa: E731  (6.1)
    close(S(55), 1.43, 0.005)
    close(S(22), 0.40, 0.005)
    close(S(55) / S(22), 3.5, 0.05)                   # "about 3.5x harder" (module03.html:1123)
    ax = Ax((80, 62, 680, 330), (10, 70), (0, 3))
    yr = lambda m: ax.y0 - m * (ax.y0 - ax.top)       # noqa: E731  right axis: mobility 0..1 on the same box
    o = axes(s, ax, [(v, f"{v}°") for v in (10, 20, 30, 40, 50, 60, 70)], [(v, f"{v}") for v in (0, 1, 2, 3)],
             f"socket coverage angle {it('β')}", None)
    o.append(H.line(s, ax.x1, ax.y0, ax.x1, ax.top, I["axis"], "axis"))
    for m in (0, 0.5, 1.0):
        o.append(H.line(s, ax.x1, yr(m), ax.x1 + 5, yr(m), I["axis"], "leader"))
        o.append(H.label(s, ax.x1 + 9, yr(m) + 4.5, f"{m:g}", "tick", I["secondary"]))
    # axis titles in ink; the legend ties each series to its axis
    ym = (ax.y0 + ax.top) / 2
    o.append(H.label(s, 30, ym, f"stability ratio {it('S')} = tan {it('β')}", "label", I["primary"], "middle",
                     f'transform="rotate(-90 30 {ym:.2f})"'))
    o.append(H.label(s, 735, ym, "mobility (ROM, normalised)", "label", I["primary"], "middle",
                     f'transform="rotate(90 735 {ym:.2f})"'))
    o += legend(s, ax.x0 + 6, 22, [(SER[0], None, "stability S = tan β (left axis)"),
                                   (SER[1], None, "mobility ROM(β)/ROM(10°) (right axis)")])
    bs = np.linspace(10, 70, 121)
    for bj, name in ((22.0, "shoulder"), (55.0, "hip")):
        o.append(H.line(s, ax.X(bj), ax.y0, ax.X(bj), ax.top, I["rule"], "leader", H.DASH_REF))
        o.append(H.label(s, ax.X(bj), ax.top - 8, f"{name}, {it('β')} ≈ {bj:.0f}°", "label2", I["primary"], "middle"))
    o.append(curve(s, ax, bs, [S(b) for b in bs], SER[0], "curve_multi"))
    o.append(poly(s, [(ax.X(b), yr(mob(b))) for b in bs], SER[1], "curve_multi"))
    for bj in (22.0, 55.0):
        o.append(dot(s, ax.X(bj), ax.Y(S(bj)), SER[0]))
        o.append(H.label(s, ax.X(bj) + 9, ax.Y(S(bj)) + 18, f"{it('S')} = {S(bj):.2f}", "label2", I["primary"]))
        o.append(dot(s, ax.X(bj), yr(mob(bj)), SER[1]))
        o.append(H.label(s, ax.X(bj) + 9, yr(mob(bj)) - 16, f"ROM {rom(bj):.0f}° ({mob(bj):.2f})", "label2", I["primary"]))
    o.append(H.label(s, ax.X(40), ax.Y(S(40)) + 22, "stability", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(40), yr(mob(40)) - 12, "mobility", "label2", I["primary"], "middle"))
    # slopes: the trade's shape (mobility linear, stability faster than linear)
    k = math.pi / 180
    d22, d55 = k / math.cos(math.radians(22)) ** 2, k / math.cos(math.radians(55)) ** 2
    nx, ny = ax.X(25), ax.Y(1.85)
    for i, t in enumerate(["per degree of coverage:", f"mobility −{1 / rom(10.0):.4f} everywhere;",
                           f"{it('S')} +{d22:.3f} at 22°, +{d55:.3f} at 55°"]):
        o.append(H.label(s, nx, ny + i * 17, t, "label2", I["secondary"]))
    aria = ("Plot against socket coverage angle beta from 10 to 70 degrees, with two y-axes. Left: the stability ratio "
            "S = tan beta rises faster than linearly, from 0.18 to 2.75. Right: mobility, the range of motion 180 - beta - 30 "
            "degrees normalised by its value at 10 degrees, falls linearly from 1 to 0.57. The shoulder, beta about 22 "
            "degrees, has S = 0.40 and range 128 degrees (0.91); the hip, beta about 55 degrees, has S = 1.43 and range "
            "95 degrees (0.68). Per degree of coverage mobility always drops by 0.0071, while S gains 0.020 at 22 degrees "
            "and 0.053 at 55 degrees.")
    hv = [[ax.X(b), [ax.Y(S(b)), yr(mob(b))], f"β = {b:.1f}°: S = {S(b):.2f}, ROM = {rom(b):.0f}° ({mob(b):.2f})"]
          for b in bs]
    return svg(VB, aria, s, o, H.hover_attr(ax.box, hv))


# ================================================================ svg #23: Plot B, the three forces over a half-swing
def fig23():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    h = lab_checked()
    i1 = turn(h)
    x, Rs, Re, Nc, t = (h[k][:i1 + 1] for k in ("x2", "Rs", "Re", "Nc", "t"))
    ipk = int(np.argmax(Rs))
    iout = int(np.argmax(x))
    close(Rs[0] / WL, 0.34, 0.005)
    close(Rs[ipk] / WL, 0.95, 0.005)
    assert np.all(Rs >= Re)                           # "the proximal joint always carries more" (module03.html:1414)
    ax = Ax((80, 50, 630, 320), (-0.05, 0.40), (0, 1.0))
    o = axes(s, ax, [(v, f"{v:.1f}") for v in (0.0, 0.1, 0.2, 0.3, 0.4)], [(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1.0)],
             f"hand position {it('x')} along the rail (m)", f"force / limb weight {it('W')}{sub('L', s)}", ylab_x=30)
    ix = thin(len(x))
    for ys, col, dash in ((Nc, SER[2], DASH_SER), (Re, SER[1], None), (Rs, SER[0], None)):
        o.append(poly(s, [(ax.X(x[i]), ax.Y(ys[i] / WL)) for i in ix], col, "curve_multi", dash))
    o.append(dot(s, ax.X(x[0]), ax.Y(Rs[0] / WL), SER[0]))
    yr0 = ax.Y(Rs[0] / WL)
    o.append(H.line(s, ax.X(x[0]) + 6, yr0, ax.x1 + 14, yr0, I["secondary"], "leader"))
    o.append(H.label(s, ax.x1 + 18, yr0 + 4.5, "release, at rest:", "label2", I["primary"]))
    o.append(H.label(s, ax.x1 + 18, yr0 + 21, f"{it('R')}{sub('s', s, 'label2')} = {Rs[0] / WL:.2f}", "label2", I["primary"]))
    o.append(dot(s, ax.X(x[ipk]), ax.Y(Rs[ipk] / WL), SER[0]))
    o.append(H.label(s, ax.X(x[ipk]) - 10, ax.Y(Rs[ipk] / WL) - 8,
                     f"peak {Rs[ipk] / WL:.2f} at {it('x')} = {x[ipk]:.3f} m, {it('t')} = {t[ipk]:.2f} s", "label2", I["primary"], "end"))
    o.append(dot(s, ax.X(x[-1]), ax.Y(Rs[-1] / WL), SER[0]))
    o.append(H.label(s, ax.X(x[-1]) + 10, ax.Y(Rs[-1] / WL) + 16, f"turning point: {Rs[-1] / WL:.2f}", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.205), ax.Y(0.68) + 20, f"shoulder {it('R')}{sub('s', s, 'label2')}", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(0.22), ax.Y(0.465), f"contact λ{sub('3', s, 'label2')}", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(0.05), ax.Y(0.07), f"elbow {it('R')}{sub('e', s, 'label2')}", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.x1 + 120, ax.y0 + 62,
                     f"the hand first moves out, {x[0]:.4f} → {x[iout]:.4f} m (to {it('t')} = {t[iout]:.3f} s), then in to "
                     f"{mn(x[-1], '{:.3f}')} m at {it('t')} = {t[-1]:.3f} s", "label2", I["secondary"], "end"))
    o += legend(s, ax.x0 + 14, 30, [(SER[0], None, "shoulder Rs"), (SER[1], None, "elbow Re"), (SER[2], DASH_SER, f"contact λ{sub('3', s, 'label2')}")])
    aria = ("Plot of the three constraint forces of the lab limb, in units of the limb weight WL = 34.3 N, against the hand "
            "position x along the rail over one half-swing, computed by the section 7.4 code. Released at rest at x = 0.358 m, "
            "the hand first moves out to 0.360 m, then sweeps in to x = -0.027 m at t = 0.756 s. The shoulder reaction Rs "
            f"starts at {Rs[0] / WL:.2f}, peaks at {Rs[ipk] / WL:.2f} at x = {x[ipk]:.3f} m (t = {t[ipk]:.2f} s), and eases to "
            f"{Rs[-1] / WL:.2f} at the turning point. The elbow reaction Re stays below Rs throughout, between 0 and "
            f"{Re.max() / WL:.2f}. The dashed contact force lambda 3 runs from {Nc.min() / WL:.2f} to {Nc.max() / WL:.2f}.")
    sel = [i for i in ix if t[i] >= t[iout]]                 # hover on the single-valued inward sweep only
    hv = [[ax.X(x[i]), [ax.Y(Rs[i] / WL), ax.Y(Re[i] / WL), ax.Y(Nc[i] / WL)],
           f"x = {x[i]:.3f} m, t = {t[i]:.2f} s: Rs {Rs[i] / WL:.2f}, Re {Re[i] / WL:.2f}, λ3 {Nc[i] / WL:.2f} WL"] for i in sel]
    hv.sort(key=lambda q: q[0])
    return svg(VB, aria, s, o, H.hover_attr(ax.box, hv))


# ================================================================ problem plots (400 px)
def sci(v):
    """2.16e-05 -> 2.16×10⁻⁵ (Unicode superscripts; SVG text has no MathJax)."""
    m, e = f"{v:.2e}".split("e")
    return f"{m}×10" + str(int(e)).translate(str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹"))


def ps(h):
    return H.Scale(W, h, display_w=400)


# ---------------------------------------------------------------- #54 K3: scale every mass
def fig54():
    VB = (0, 0, W, 262)
    s = ps(VB[3])
    ks = (0.5, 1.0, 2.0)
    runs = {k: run(m1=2.0 * k, m2=1.5 * k) for k in ks}
    pk = {k: runs[k]["Rs"].max() for k in ks}
    for k, ref in zip(ks, (16.3, 32.6, 65.2)):
        close(pk[k], ref, 0.05)
    xa = {k: (runs[k]["x2"][0], runs[k]["x2"][turn(runs[k])]) for k in ks}
    for k in ks:
        close(xa[k][0], 0.358, 0.0005)
        close(xa[k][1], -0.027, 0.0005)
    P = Plot(s, (58, 46, 388, 206), (0, 2.2), (0, 75))
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2)], [(v, f"{v}") for v in (0, 20, 40, 60)],
                f"mass-scale factor {it('k')}", f"peak {it('R')}{sub('s', s)} (N)", grid=(20, 40, 60))]
    o.append(P.curve([0, 2.2], [0, pk[1.0] * 2.2], I["rule"], dash=H.DASH_REF))
    o.append(P.curve(list(ks), [pk[k] for k in ks], SER[0]))
    for k in ks:
        o.append(P.dot(k, pk[k], SER[0]))
        dx, dy, anc = (-8, -7, "end") if k == 2.0 else (8, 17, "start")
        o.append(plabel(s, P.X(k) + dx, P.Y(pk[k]) + dy, f"{pk[k]:.1f} N", "label2", I["primary"], anc))
    o.append(plabel(s, P.X(1.25), P.Y(pk[1.0] * 2.2) + 2, f"{it('R')}{sub('s', s, 'label2')} = {pk[1.0]:.1f} {it('k')} N",
                    "label2", I["secondary"], "end"))
    o.append(plabel(s, 58, 18, f"for every {it('k')}: hand sweeps {xa[1.0][0]:.3f} → {mn(xa[1.0][1], '{:.3f}')} m", "label2",
                    I["secondary"]))
    o.append(plabel(s, 58, 34, "(trajectory unchanged)", "label2", I["muted"]))
    aria = ("Problem K3 plot: peak shoulder reaction against the mass-scale factor k, from three runs of the lab with "
            f"every mass multiplied by k: {pk[0.5]:.1f} N at k = 0.5, {pk[1.0]:.1f} N at k = 1 and {pk[2.0]:.1f} N at k = 2. "
            "The points lie on a straight line through the origin, Rs = 32.6 k newtons. In every run the hand sweeps the "
            "same path, from 0.358 m to -0.027 m.")
    hv = [[P.X(k), P.Y(pk[k]), f"k = {k:g}: peak Rs = {pk[k]:.1f} N, hand {xa[k][0]:.3f} → {xa[k][1]:.3f} m"] for k in ks]
    return svg(VB, aria, s, o, H.hover_attr(P.box, hv))


# ---------------------------------------------------------------- #56 K4: lengthen the forearm
def fig56():
    VB = (0, 0, W, 252)
    s = ps(VB[3])
    L2s = (0.20, 0.30, 0.40)
    pk = {L: run(L2=L, yh=-(0.30 + L) * 0.8)["Rs"].max() for L in L2s}
    for L, ref in zip(L2s, (31.7, 32.6, 33.3)):
        close(pk[L], ref, 0.05)
    P = Plot(s, (58, 30, 388, 196), (0.15, 0.45), (0, 40))
    o = [P.axes([(v, f"{v:.2f}") for v in (0.2, 0.3, 0.4)], [(v, f"{v}") for v in (0, 10, 20, 30, 40)],
                f"forearm length {it('L')}{sub('2', s)} (m)", f"peak {it('R')}{sub('s', s)} (N)", grid=(10, 20, 30, 40))]
    o.append(P.curve(list(L2s), [pk[L] for L in L2s], SER[0]))
    for L in L2s:
        o.append(P.dot(L, pk[L], SER[0]))
        o.append(plabel(s, P.X(L), P.Y(pk[L]) + 20, f"{pk[L]:.1f}", "label2", I["primary"], "middle"))
    ch = pk[0.40] / pk[0.20] - 1
    o.append(plabel(s, P.X(0.30), P.Y(14), f"doubling {it('L')}{sub('2', s, 'label2')}: +{ch * 100:.0f} %", "label2", I["secondary"], "middle"))
    o.append(plabel(s, P.X(0.30), P.Y(14) + 17, "rail kept at 80 % of full reach", "label2", I["muted"], "middle"))
    aria = ("Problem K4 plot: peak shoulder reaction against forearm length L2, with the rail lowered to keep the hand at "
            f"80 percent of full reach: {pk[0.20]:.1f} N at 0.20 m, {pk[0.30]:.1f} N at 0.30 m and {pk[0.40]:.1f} N at 0.40 m. "
            f"On an axis from zero the line is nearly flat: doubling L2 raises the peak by {ch * 100:.0f} percent.")
    hv = [[P.X(L), P.Y(pk[L]), f"L2 = {L:.2f} m (rail y = {-(0.30 + L) * 0.8:.2f} m): peak Rs = {pk[L]:.1f} N"] for L in L2s]
    return svg(VB, aria, s, o, H.hover_attr(P.box, hv))


# ---------------------------------------------------------------- #58 K5: static versus moving
def fig58():
    VB = (0, 0, W, 268)
    s = ps(VB[3])
    h = lab_checked()
    i1 = turn(h)
    x, Rs, t = h["x2"][:i1 + 1], h["Rs"][:i1 + 1] / WL, h["t"][:i1 + 1]
    ipk, iout = int(np.argmax(Rs)), int(np.argmax(x))
    close(Rs[ipk] / Rs[0], 2.80, 0.005)
    P = Plot(s, (58, 46, 388, 212), (-0.05, 0.40), (0, 1.1))
    o = [P.axes([(v, f"{v:.1f}") for v in (0.0, 0.1, 0.2, 0.3, 0.4)], [(v, f"{v:g}") for v in (0, 0.5, 1.0)],
                f"hand position {it('x')} (m)", f"{it('R')}{sub('s', s)} / {it('W')}{sub('L', s)}", grid=(0.5, 1.0))]
    ix = thin(len(x))
    o.append(P.curve([x[i] for i in ix], [Rs[i] for i in ix], SER[0]))
    o.append(P.dot(x[0], Rs[0], SER[0]))
    o.append(plabel(s, P.X(x[0]) - 8, P.Y(Rs[0]) + 16, f"at rest (release): {Rs[0]:.2f}", "label2", I["primary"], "end"))
    o.append(P.dot(x[ipk], Rs[ipk], SER[0]))
    o.append(plabel(s, P.X(x[ipk]) - 8, P.Y(Rs[ipk]) - 7, f"peak {Rs[ipk]:.2f}, {it('t')} = {t[ipk]:.2f} s", "label2", I["primary"], "end"))
    o.append(P.dot(x[-1], Rs[-1], SER[0]))
    o.append(plabel(s, P.X(x[-1]) + 4, P.Y(Rs[-1]) + 19, f"turning point {Rs[-1]:.2f}", "label2", I["primary"]))
    o.append(plabel(s, 58, 18, f"dynamic amplification {Rs[ipk] / Rs[0]:.2f}×  (1 {it('W')}{sub('L', s, 'label2')} = 34.3 N)",
                    "label2", I["secondary"]))
    aria = ("Problem K5 plot: shoulder reaction in units of limb weight against hand position over one half-swing of the "
            f"lab run. At release, at rest, it is {Rs[0]:.2f} (11.6 N), the static value. It peaks at {Rs[ipk]:.2f} (32.6 N) "
            f"at x = {x[ipk]:.3f} m, t = {t[ipk]:.2f} s, early in the inward sweep, a dynamic amplification of "
            f"{Rs[ipk] / Rs[0]:.2f}, and falls to {Rs[-1]:.2f} at the inner turning point, x = {x[-1]:.3f} m.")
    sel = sorted((i for i in ix if t[i] >= t[iout]), key=lambda i: x[i])
    hv = [[P.X(x[i]), P.Y(Rs[i]), f"x = {x[i]:.3f} m, t = {t[i]:.2f} s: Rs = {Rs[i]:.2f} WL"] for i in sel]
    return svg(VB, aria, s, o, H.hover_attr(P.box, hv))


# ---------------------------------------------------------------- #60 K6: swing harder
def fig60():
    VB = (0, 0, W, 252)
    s = ps(VB[3])
    amps = (10, 20, 30, 40, 50)
    pk = {a: run(amp=float(a))["Rs"].max() for a in amps}
    for a, ref in zip(amps, (20.66, 22.37, 25.75, 32.61, 48.39)):
        close(pk[a], ref, 0.005)
    r = {a: pk[a] / WL for a in amps}
    for a, ref in zip(amps, (0.60, 0.65, 0.75, 0.95, 1.41)):
        close(r[a], ref, 0.005)
    P = Plot(s, (58, 24, 388, 196), (5, 55), (0, 1.6))
    o = [P.axes([(v, f"{v}°") for v in amps], [(v, f"{v:g}") for v in (0, 0.5, 1.0, 1.5)],
                "release amplitude", f"peak {it('R')}{sub('s', s)} / {it('W')}{sub('L', s)}", grid=(0.5, 1.0, 1.5))]
    o.append(P.curve(list(amps), [r[a] for a in amps], SER[0]))
    for a in amps:
        o.append(P.dot(a, r[a], SER[0]))
        dx, anc = {50: (-8, "end"), 40: (-7, "end")}.get(a, (0, "middle"))
        o.append(plabel(s, P.X(a) + dx, P.Y(r[a]) - 9, f"{r[a]:.2f}", "label2", I["primary"], anc))
    o.append(plabel(s, P.X(8), P.Y(1.33), "each 10° adds more than the last:", "label2", I["secondary"]))
    o.append(plabel(s, P.X(8), P.Y(1.33) + 16, " +".join([""] + [f"{r[b] - r[a]:.2f}" for a, b in zip(amps, amps[1:])])[1:],
                    "label2", I["secondary"]))
    aria = ("Problem K6 plot: peak shoulder reaction in limb weights against release amplitude, from five runs of the "
            "lab: 0.60 at 10 degrees, 0.65 at 20, 0.75 at 30, 0.95 at 40 and 1.41 at 50. Each 10 degree step adds more "
            "than the one before: 0.05, 0.10, 0.20, 0.46.")
    hv = [[P.X(a), P.Y(r[a]), f"release {a}°: peak Rs = {pk[a]:.2f} N = {r[a]:.2f} WL"] for a in amps]
    return svg(VB, aria, s, o, H.hover_attr(P.box, hv))


# ---------------------------------------------------------------- #64 K8: make the floor one-sided
def fig64():
    VB = (0, 0, W, 270)
    s = ps(VB[3])
    amps = (50, 40, 30)
    lo = {}
    tr = {}
    for a in amps:
        h = run(amp=float(a))
        lo[a] = h["Nc"].min()
        i1 = turn(h)
        tr[a] = (h["t"][:i1 + 1], h["Nc"][:i1 + 1])
    for a, ref in zip((30, 40, 50), (10.71, 6.21, -5.88)):
        close(lo[a], ref, 0.005)
    tmax = max(tr[a][0][-1] for a in amps)
    P = Plot(s, (58, 46, 388, 220), (0, 0.9), (-10, 40))
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.2, 0.4, 0.6, 0.8)], [(v, mn(v, "{:.0f}")) for v in (-10, 0, 10, 20, 30, 40)],
                f"time {it('t')} (s), one half-swing", f"contact λ{sub('3', s)} (N)", grid=(10, 20, 30, 40))]
    o.insert(0, f'<rect x="{P.x0}" y="{P.Y(0):.2f}" width="{P.x1 - P.x0}" height="{P.Y(-10) - P.Y(0):.2f}" '
                f'fill="{O["flag"]}" opacity="0.16"/>')
    o.append(H.line(s, P.x0, P.Y(0), P.x1, P.Y(0), O["dim"], "ref", H.DASH_REF))
    cols = dict(zip(amps, SER))
    for a in amps:
        tt, nn = tr[a]
        ix = thin(len(tt), 300)
        o.append(P.curve([tt[i] for i in ix], [nn[i] for i in ix], cols[a], multi=True))
    t50, n50 = tr[50]
    im = int(np.argmin(n50))
    neg = n50 < 0
    o.append(P.dot(t50[im], n50[im], SER[0]))
    o.append(plabel(s, P.X(t50[im]) + 9, P.Y(n50[im]) + 4, f"{mn(lo[50])} N", "label2", I["primary"]))
    tn = t50[neg]
    l3 = f"λ{sub('3', s, 'label2')}"
    o.append(plabel(s, P.x1 - 4, P.Y(-6.2), f"{l3} &lt; 0: a one-sided floor lets go", "label2", I["primary"], "end"))
    o.append(plabel(s, P.x1 - 4, P.Y(6.5), f"minimum {l3}: 30° {lo[30]:.2f} N,", "label2", I["secondary"], "end"))
    o.append(plabel(s, P.x1 - 4, P.Y(6.5) + 16, f"40° {lo[40]:.2f} N, 50° {mn(lo[50])} N", "label2", I["secondary"], "end"))
    o.append(plegend(s, 58, 20, [(cols[50], "50° release", None), (cols[40], "40°", None), (cols[30], "30°", None)]))
    aria = ("Problem K8 plot: the contact force lambda 3 against time over one half-swing for release amplitudes of 30, 40 "
            f"and 50 degrees. All three dip in the first quarter of the swing and recover. The minimum is {lo[30]:.2f} N at "
            f"30 degrees and {lo[40]:.2f} N at 40 degrees, both pushing; at 50 degrees it reaches {lo[50]:.2f} N, below the "
            f"dashed zero line from t = {tn[0]:.2f} to {tn[-1]:.2f} s, where the two-sided rail pulls the hand down and a real "
            "floor would let it lift off.")
    ts = np.linspace(0, tmax, 181)
    hv = []
    for x in ts:
        vals = [(a, float(np.interp(x, *tr[a]))) for a in amps if x <= tr[a][0][-1]]
        hv.append([P.X(x), [P.Y(v) for _, v in vals], f"t = {x:.2f} s: " + ", ".join(f"{a}° {v:.1f} N" for a, v in vals)])
    return svg(VB, aria, s, o, H.hover_attr(P.box, hv))


# ---------------------------------------------------------------- #66 K9: why the stabilization term
def fig66():
    VB = (0, 0, W, 276)
    s = ps(VB[3])
    on, off = lab_checked(), run(gd=0.0, gp=0.0)
    close(on["gerr"][-1], 6.51e-7, 0.005e-7)
    close(off["gerr"].max(), 2.16e-5, 0.005e-5)
    close(off["gerr"][-1], 2.16e-5, 0.005e-5)
    close(off["gerr"].max() / on["gerr"].max(), 21, 0.5)
    assert int(np.argmax(off["gerr"])) == len(off["gerr"]) - 1           # "at its maximum on the last step"
    P = Plot(s, (58, 56, 388, 228), (0, 2.0), (-10, -4))
    o = [P.axes([(v, f"{v:g}") for v in (0, 0.5, 1.0, 1.5, 2.0)], [(v, "10" + str(v).replace("-", "⁻").translate(
        str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))) for v in (-10, -8, -6, -4)],
        f"time {it('t')} (s)", f"constraint error max|{it('g')}| (m)", grid=(-8, -6, -4))]

    def env(h, nb=400):
        """Per-bin maximum of max|g| (keeps every peak), floored at 1e-10 m for the log axis (g = 0 at t = 0)."""
        g, t = h["gerr"], h["t"]
        k = len(g) // nb
        return ([t[i * k:(i + 1) * k].mean() for i in range(nb)],
                [math.log10(max(g[i * k:(i + 1) * k].max(), 1e-10)) for i in range(nb)])
    eo, en = env(off), env(on)
    o.append(P.curve(*eo, SER[0], multi=True))
    o.append(P.curve(*en, SER[1], multi=True))
    o.append(P.dot(off["t"][-1], math.log10(off["gerr"][-1]), SER[0]))
    o.append(plabel(s, P.X(2.0) - 6, P.Y(math.log10(off["gerr"][-1])) - 9,
                    f"max {sci(off['gerr'].max())} m, on the last step", "label2", I["primary"], "end"))
    imo = int(np.argmax(on["gerr"]))
    o.append(P.dot(on["t"][imo], math.log10(on["gerr"][imo]), SER[1]))
    o.append(plabel(s, P.X(2.0) - 6, P.Y(-8.9), f"max {sci(on['gerr'].max())} m (at {it('t')} = {on['t'][imo]:.2f} s);",
                    "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(2.0) - 6, P.Y(-8.9) + 16, f"final {sci(on['gerr'][-1])} m, still falling", "label2", I["primary"], "end"))
    o.append(plabel(s, P.X(2.0) - 6, P.Y(-5.5) + 4, f"factor {off['gerr'].max() / on['gerr'].max():.0f} at the maxima",
                    "label2", I["secondary"], "end"))
    gg = f"γ{sub('d', s, 'label2')} = γ{sub('p', s, 'label2')}"
    o.append(plegend(s, 58, 16, [(SER[0], f"no Baumgarte ({gg} = 0)", None)]))
    o.append(plegend(s, 58, 34, [(SER[1], f"with Baumgarte ({gg} = 40)", None)]))
    aria = ("Problem K9 plot: the constraint error max|g| on a log scale against time over the whole 2 s run, with and "
            "without the Baumgarte term. With it (gains 40) the error peaks at 1.03e-6 m and is down to 6.5e-7 m at the end. "
            "Without it the error climbs to 2.16e-5 m and is at its maximum on the last step, 21 times the stabilized "
            "maximum. Each curve shows the largest error in each 5 ms bin.")
    hv = [[P.X(a), [P.Y(b), P.Y(c)], f"t = {a:.2f} s: no Baumgarte {10 ** b:.1e} m, with {10 ** c:.1e} m"]
          for a, b, c in zip(eo[0], eo[1], en[1])]
    return svg(VB, aria, s, o, H.hover_attr(P.box, hv))


FIGS = {
    3: ("Stacked bars for shoulder, hip, knee, and elbow. Each total ", fig3),
    13: ("Plot of hip joint reaction force and abductor force, in unit", fig13),
    16: ("Log-log plot of Hertz peak contact pressure versus effective", fig16),
    17: ("Animation: as the contact patch narrows, the pressure dome g", fig17),
    19: ("Plot versus socket coverage angle: the stability ratio rises", fig19),
    23: ("Plot of three forces versus hand position over one half-swin", fig23),
    54: ("A line plot of peak shoulder reaction against the mass-scale", fig54),
    56: ("A nearly flat line plot of peak shoulder reaction against fo", fig56),
    58: ("A plot of shoulder reaction in units of limb weight versus h", fig58),
    60: ("A rising curve of peak shoulder reaction in limb weights aga", fig60),
    64: ("A plot of the contact force against time over one half-swing", fig64),
    66: ("A log-scale plot of constraint drift against time for two ru", fig66),
}
