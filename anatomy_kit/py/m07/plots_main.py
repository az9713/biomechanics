"""Module 7 main-text plots and block diagrams in the house style (group `plots_main`).

svg #6 (force plate + stabilogram), #9 (saddle phase portrait), #10 (toppling clock), #11 (feedback loop),
#12 (delay-free stability region), #13 (delay island), #14 (DDE traces), #20 (L5/S1 compression),
#22 (critical delay vs gain), #24 (safe-load envelope), #25 (repayment hub).
Every plotted number is computed here from what module07.html states: the reference body (M = 70 kg,
l = 0.90 m, I = 66 kg m^2, lines 263 and 357-360), Props 4.1, 5.1, 6.2, 6.3, 8.1, 8.2, the Lab 1 code
(lines 620-663, ported line for line) and the Lab 2 code (lines 679-697, ported line for line).
All figures use a 760-unit-wide viewBox, so one user unit is one rendered px.
"""
import math
from functools import lru_cache

import numpy as np

import house as H
from m05.plots_main import (DASH_SER, GRID, Ax, axes, curve, dot, hover, it, lead, legend, mn, poly, pts_str,
                            svg)
from m05.schematic import box

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES

# ---------------------------------------------------------------- reference body and Lab 1 (text lines 263, 357-360, 620-663)
M_B, G, ELL = 70.0, 9.81, 0.9                 # kg, m/s^2, m
I_B, MGL = 66.0, 618.0                        # kg m^2, N m/rad (the Lab 1 constants)
W0 = math.sqrt(M_B * G * ELL / I_B)           # 3.06 1/s (line 360)


def simulate(Kp, Kd, D, T=25.0, dt=1e-3, th0=0.6):
    """Lab 1 method-of-steps integrator, verbatim (Python lists instead of numpy arrays: same float64 steps)."""
    n, nd = int(T / dt), int(round(D / dt))
    th, w = [0.0] * n, [0.0] * n
    th[0] = th0
    for k in range(n - 1):
        j = k - nd
        thd = th[j] if j >= 0 else th0
        wd = w[j] if j >= 0 else 0.0
        acc = (MGL * th[k] - Kp * thd - Kd * wd) / I_B
        w[k + 1] = w[k] + dt * acc
        th[k + 1] = th[k] + dt * w[k + 1]
    return np.arange(n) * dt, np.array(th)


def diverges(th, t):
    late = np.abs(th[t > 0.8 * t[-1]]).max()
    mid = np.abs(th[(t > 0.4 * t[-1]) & (t < 0.6 * t[-1])]).max()
    return late > 1.02 * mid


@lru_cache(maxsize=None)
def bisect_delay(Kp, Kd):
    """Lab 1 bisection: returns (Dcrit, the 26 trial delays)."""
    lo, hi, mids = 0.05, 0.25, []
    for _ in range(26):
        mid = 0.5 * (lo + hi)
        mids.append(mid)
        t, th = simulate(Kp, Kd, mid)
        hi, lo = (mid, lo) if diverges(th, t) else (hi, mid)
    return 0.5 * (lo + hi), tuple(mids)


def theory(Kp, Kd):
    """Prop 6.3 quartic, as in Lab 1: (Delta_crit, omega_c)."""
    a, b, c = I_B * I_B, 2 * I_B * MGL - Kd ** 2, MGL ** 2 - Kp ** 2
    wc = math.sqrt((-b + math.sqrt(b * b - 4 * a * c)) / (2 * a))
    return math.atan(Kd * wc / Kp) / wc, wc


assert abs(bisect_delay(900.0, 120.0)[0] - 0.1295) < 5e-5 and abs(theory(900.0, 120.0)[0] - 0.1297) < 5e-5  # line 666


@lru_cache(maxsize=None)
def hopf(D, n=600):
    """Prop 6.2 Hopf boundary from omega = 0 (Kp = Mgl, Kd = Mgl D) to the first return to Kp = Mgl."""
    lo, hi = 1e-3, math.pi / (2 * D)
    f = lambda w: (I_B * w * w + MGL) * math.cos(w * D) - MGL   # noqa: E731
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if f(mid) > 0 else (lo, mid)
    ws = np.linspace(0.0, 0.5 * (lo + hi), n)
    kp = (I_B * ws ** 2 + MGL) * np.cos(ws * D)
    kd = np.empty_like(ws)
    kd[0] = MGL * D
    kd[1:] = (I_B * ws[1:] ** 2 + MGL) * np.sin(ws[1:] * D) / ws[1:]
    return kp, kd


def island_area(D):
    """Area enclosed by the Hopf curve and the divergence line (shoelace = Green's theorem)."""
    kp, kd = hopf(D, 4000)
    x, y = np.append(kp, MGL), np.append(kd, kd[0])
    return 0.5 * abs(float(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1))))


def island_kd(D, Kp):
    """Lower and upper Kd of the island at one Kp (None outside)."""
    kp, kd = hopf(D)
    k = int(kp.argmax())
    if not (MGL < Kp < kp[k]):
        return None
    lo = float(np.interp(Kp, kp[:k + 1], kd[:k + 1]))
    hi = float(np.interp(Kp, kp[k:][::-1], kd[k:][::-1]))
    return lo, hi


# ---------------------------------------------------------------- K7 sway run (line 874), reused by Fig. 5
@lru_cache(maxsize=None)
def sway(seed, Kp=900.0, Kd=120.0, D=0.12, q=0.35, T=600.0, dt=1e-3):
    """Prop 6.1 closed loop with a white ankle-torque disturbance of intensity q (N m s^1/2), Lab 1's integrator.
    Returns t, x_com = l theta, x_cop = tau / (M g) (Prop 3.2), first 30 s discarded."""
    rng = np.random.default_rng(seed)
    n, nd = int(T / dt), int(round(D / dt))
    nz = ((q / math.sqrt(dt)) * rng.standard_normal(n)).tolist()
    th, w, tau = [0.0] * n, [0.0] * n, [0.0] * n
    for k in range(n - 1):
        j = k - nd
        thd = th[j] if j >= 0 else 0.0
        wd = w[j] if j >= 0 else 0.0
        tau[k] = Kp * thd + Kd * wd
        acc = (MGL * th[k] - tau[k] + nz[k]) / I_B
        w[k + 1] = w[k] + dt * acc
        th[k + 1] = th[k] + dt * w[k + 1]
    tau[n - 1] = Kp * th[n - 1 - nd] + Kd * w[n - 1 - nd]
    t = np.arange(n) * dt
    keep = t >= 30.0
    return t[keep], ELL * np.array(th)[keep], np.array(tau)[keep] / (M_B * G)


K7_SEED = 7          # the realisation whose RMS values are the ones K7 quotes (4.5 mm, 6.8 mm)


def rms_mm(x):
    return float(np.sqrt(np.mean(x ** 2)) * 1e3)


# ---------------------------------------------------------------- Lab 2 (lines 679-697) and Props 8.1-8.2
MT, RT, D_E, LIMIT = 35.0, 0.30, 0.05, 3400.0


def peak_compression(mL, rL):
    phi = np.linspace(0, np.pi / 2, 400)
    M = G * (MT * RT + mL * rL) * np.sin(phi)
    return (M / D_E + (MT + mL) * G * np.cos(phi)).max()


@lru_cache(maxsize=None)
def lab2_grid():
    """Lab 2's printed table: 0.5 kg grid, strict <."""
    out = []
    for rL in np.linspace(0.15, 0.50, 8):
        loads = np.arange(0, 60, 0.5)
        out.append((float(rL), float(max(m for m in loads if peak_compression(m, rL) < LIMIT))))
    return tuple(out)


assert [round(m, 1) for r, m in lab2_grid() if round(r, 2) in (0.15, 0.30, 0.45, 0.50)] == [42.5, 21.5, 14.5, 13.0]


@lru_cache(maxsize=None)
def safe_load(rL):
    """Continuous inverse of Lab 2 (bisection on load), as K9 does: 18.9 kg at 0.35 m."""
    lo, hi = 0.0, 150.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if peak_compression(mid, rL) < LIMIT else (lo, mid)
    return 0.5 * (lo + hi)


def compression(phi_deg, mL, rL):
    """Prop 8.2, full form (N)."""
    p = math.radians(phi_deg)
    return G * (MT * RT + mL * rL) * math.sin(p) / D_E + (MT + mL) * G * math.cos(p)


def sub(t, s):
    return H.sub(t, s, "label2")


def sup(t, s):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX["label2"] * 0.7):.2f}">{t}</tspan>'


def ticks(vals, f="{:g}"):
    return [(v, mn(v, f)) for v in vals]


# ================================================================ svg #6: force plate + stabilogram (Fig. 5)
def fig6():
    VB = (0, 0, 760, 360)
    s = H.Scale(VB[2], VB[3])
    p = "m7f6_"
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    # --- left: the plate in an oblique view; plate frame x forward (AP), y to the left (ML), z up, metres
    SC, CX, CY = 430.0, 185.0, 238.0

    def P(x, y, z=0.0):
        return CX + SC * (x + 0.45 * y), CY - SC * (0.30 * y + z)
    LX, LY, TH = 0.30, 0.20, 0.035
    top = [P(-LX, -LY), P(LX, -LY), P(LX, LY), P(-LX, LY)]
    for cx_, cy_ in ((-LX + 0.04, LY - 0.04), (LX - 0.04, LY - 0.04), (-LX + 0.04, -LY + 0.04), (LX - 0.04, -LY + 0.04)):
        bx, by = P(cx_, cy_, -TH)
        o.append(f'<rect x="{bx-9:.2f}" y="{by:.2f}" width="18" height="13" fill="{T["bone_shade"][0]}" '
                 f'stroke="{I["secondary"]}" stroke-width="1"/>'
                 f'<ellipse cx="{bx:.2f}" cy="{by+13:.2f}" rx="9" ry="3" fill="{T["bone_shade"][0]}" stroke="{I["secondary"]}" stroke-width="1"/>'
                 f'<ellipse cx="{bx:.2f}" cy="{by:.2f}" rx="9" ry="3" fill="{T["bone"][0]}" stroke="{I["secondary"]}" stroke-width="1"/>')
    front = [P(-LX, -LY), P(LX, -LY), P(LX, -LY, -TH), P(-LX, -LY, -TH)]
    side = [P(LX, -LY), P(LX, LY), P(LX, LY, -TH), P(LX, -LY, -TH)]
    for poly_, fill in ((front, "#e3ddd0"), (side, "#d6cfc0"), (top, "#f7f4ef")):
        o.append(f'<polygon points="{pts_str(poly_)}" fill="{fill}" stroke="{I["secondary"]}" stroke-width="1.2" '
                 f'stroke-linejoin="round"/>')
    ox, oy = P(0, 0)
    xc, yc = 0.12, 0.0                                      # an illustrative COP on the plate (m)
    cx, cy = P(xc, yc)
    # x_cop: from O along x (forward) to the COP's x, then the y offset (construction); x axis continues
    xa, ya = P(xc, 0)
    x2, y2 = P(0.22, 0)
    o.append(H.arrow(s, p, xa + 4, ya, x2, y2, "dim", w="ref"))
    o.append(H.label(s, x2 + 5, y2 + 5, f'{it("x")} (forward)', "label2", I["secondary"]))
    o.append(H.line(s, xa, ya, cx, cy, I["rule"], "leader", (3, 3)))
    o.append(H.line(s, ox, oy, xa, ya, O["geometry"], "geom"))
    o.append(H.label(s, (ox + xa) / 2, oy + 19, f'x{sub("cop", s)}', "label2", I["primary"], "middle"))
    o.append(H.joint_centre(s, ox, oy))
    o.append(H.label(s, ox - 14, oy + 18, "O", "label2", I["primary"], "end"))
    # GRF up from the COP
    o.append(H.arrow(s, p, cx, cy, cx, cy - 150, "reaction"))
    o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="4" fill="{SER[1]}" stroke="#fff" stroke-width="1.5"/>')
    o.append(H.label(s, cx + 8, cy - 140, f'F{sub("z", s)} (vertical GRF)', "label2", I["primary"]))
    o.append(H.label(s, cx - 8, cy - 8, "COP", "label2", I["primary"], "end"))
    bl, bly = P(-LX + 0.04, -LY + 0.04, -TH)
    o.append(H.line(s, bl + 10, bly + 10, bl + 34, bly + 26, I["rule"], "leader"))
    o.append(H.label(s, bl + 37, bly + 31, "load cell (one of four)", "label2", I["secondary"]))
    o.append(H.label(s, 20, 34, "force plate", "label", I["primary"]))
    o.append(H.label(s, 20, 52, "reports F and M at its origin O", "label2", I["secondary"]))
    o.append(H.label(s, 20, 334, f'x{sub("cop", s)} = −M{sub("y", s)} / F{sub("z", s)},   '
                     f'y{sub("cop", s)} = M{sub("x", s)} / F{sub("z", s)}', "label", I["primary"]))
    o.append(H.label(s, 20, 352, "(Proposition 2.2, moments about O)", "label2", I["secondary"]))
    # --- right: computed stabilogram, the K7 closed loop; AP and ML from two independent runs
    _, com_ap, cop_ap = sway(K7_SEED)
    _, com_ml, cop_ml = sway(K7_SEED + 1)
    win = slice(0, 20000, 40)                               # t = 30-50 s, sampled every 40 ms
    tt = np.arange(30.0, 50.0, 0.04)
    pa, pm, ca, cm = (1e3 * v[win] for v in (cop_ap, cop_ml, com_ap, com_ml))
    lim = 20.0
    assert max(abs(pa).max(), abs(pm).max()) < lim
    ax = Ax((452, 76, 660, 296), (-lim, lim), (-lim, lim))
    o += axes(s, ax, ticks((-20, -10, 0, 10, 20)), ticks((-20, -10, 0, 10, 20)), "medio-lateral (mm)",
              "anterior-posterior (mm)", ylab_x=ax.x0 - 46, xlab_dy=42)
    o.append(poly(s, [(ax.X(a), ax.Y(b)) for a, b in zip(pm, pa)], SER[1], "curve_multi", extra='opacity="0.9"'))
    o.append(poly(s, [(ax.X(a), ax.Y(b)) for a, b in zip(cm, ca)], I["primary"], "curve_multi"))
    o.append(H.label(s, 404, 24, "stabilogram (computed, 20 s)", "label", I["primary"]))
    o += legend(s, 404, 52, [(SER[1], None, "centre of pressure"), (I["primary"], None, "centre of mass")], gap=14)
    kp_, kc_ = int(np.argmax(pa)), int(np.argmax(cm))
    o.append(lead(s, ax.X(pm[kp_]) + 3, ax.Y(pa[kp_]) - 2, 672, 96, I["rule"]))
    o.append(H.label(s, 676, 100, "COP", "label2", I["primary"]))
    o.append(lead(s, ax.X(cm[kc_]) + 3, ax.Y(ca[kc_]), 672, 166, I["rule"]))
    o.append(H.label(s, 676, 170, "COM", "label2", I["primary"]))
    o.append(H.label(s, 672, 232, "RMS (AP),", "label2", I["secondary"]))
    o.append(H.label(s, 672, 249, "600 s run:", "label2", I["secondary"]))
    o.append(H.label(s, 672, 266, f"COP {rms_mm(cop_ap):.1f} mm", "label2", I["primary"]))
    o.append(H.label(s, 672, 283, f"COM {rms_mm(com_ap):.1f} mm", "label2", I["primary"]))
    aria = ("Two panels. Left: a force plate drawn in an oblique view, standing on four load cells, with its origin O at "
            "the centre of the top surface, the forward x axis, the distance x-cop, the centre of pressure as a blue dot, the vertical ground "
            "reaction Fz rising from it, and the formula x-cop = minus My over Fz, y-cop = Mx over Fz. Right: a computed "
            "20-second stabilogram from the module's delayed PD model with a random ankle-torque disturbance: the blue "
            f"centre-of-pressure path wanders over a wider range than the black centre-of-mass path it surrounds. "
            f"RMS anterior-posterior excursion over the 600-second run: COP {rms_mm(cop_ap):.1f} mm, COM {rms_mm(com_ap):.1f} mm.")
    order = np.argsort(pm)
    hv = hover(ax, [ax.X(pm[k]) for k in order], [[ax.Y(pa[k]), ax.Y(ca[k])] for k in order],
               [f"t = {tt[k]:.2f} s: COP ({pm[k]:.1f}, {pa[k]:.1f}) mm, COM ({cm[k]:.1f}, {ca[k]:.1f}) mm" for k in order])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #9: the saddle (Fig. 8)
def fig9():
    VB = (0, 0, 760, 430)
    s = H.Scale(VB[2], VB[3])
    p = "m7f9_"
    th_r, wd_r = 2.0, 6.5                                   # deg, deg/s
    ax = Ax((80, 48, 560, 380), (-th_r, th_r), (-wd_r, wd_r))
    o = [f'<defs>{H.markers(p, s)}<marker id="{p}a_traj" markerUnits="userSpaceOnUse" markerWidth="9.6" markerHeight="6.4" '
         f'refX="7.6" refY="3.2" orient="auto"><path d="M0,0 L8,3.2 L0,6.4 Z" fill="{I["rule"]}"/></marker></defs>']
    o += axes(s, ax, ticks((-2, -1, 0, 1, 2)), ticks((-6, -3, 0, 3, 6)), "lean angle θ (degrees)",
              "lean rate dθ/dt (degrees per second)", grid=False, ylab_x=ax.x0 - 50)
    o.append(H.line(s, ax.X(0), ax.top, ax.X(0), ax.y0, I["rule"], "leader"))
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["rule"], "leader"))

    def inside(a, b):
        return abs(a) <= th_r and abs(b) <= wd_r
    # trajectories theta(t) = A e^{w0 t} + B e^{-w0 t}: hyperbolae, time runs with u
    us = np.linspace(-3.5, 3.5, 141)
    for c in (1.2, 2.4, 3.6):                             # sqrt|c| in deg/s
        fams = [(c / W0 * np.sinh(us), c * np.cosh(us)), (-c / W0 * np.sinh(us), -c * np.cosh(us)),
                (c / W0 * np.cosh(us), c * np.sinh(us)), (-c / W0 * np.cosh(us), -c * np.sinh(us))]
        for a, b in fams:
            keep = [(x, y) for x, y in zip(a, b) if inside(x, y)]
            o.append(poly(s, [(ax.X(x), ax.Y(y)) for x, y in keep], I["rule"], "leader", extra='opacity="0.9"'))
            k = int(np.argmin(np.abs(us - 0.35)))
            x1, y1, x2, y2 = a[k - 6], b[k - 6], a[k], b[k]
            o.append(H.line(s, ax.X(x1), ax.Y(y1), ax.X(x2), ax.Y(y2), I["rule"], "leader", extra=f'marker-end="url(#{p}a_traj)"'))
    xs = np.linspace(-th_r, th_r, 81)
    o.append(curve(s, ax, xs, -W0 * xs, SER[1], "curve", DASH_SER))
    o.append(curve(s, ax, xs, W0 * xs, SER[0], "curve"))
    for x0_, x1_, col, mean in ((1.6, 1.15, SER[1], "geometry"), (-1.6, -1.15, SER[1], "geometry"),
                                (0.55, 1.0, SER[0], "force"), (-0.55, -1.0, SER[0], "force")):
        sg = -1 if col == SER[1] else 1
        o.append(H.arrow(s, p, ax.X(x0_), ax.Y(sg * W0 * x0_), ax.X(x1_), ax.Y(sg * W0 * x1_), mean))
    o.append(dot(s, ax.X(0), ax.Y(0), I["primary"], r=5))
    o.append(H.label(s, 574, ax.Y(W0 * 2) + 5, "unstable manifold", "label", I["primary"]))
    o.append(H.label(s, 574, ax.Y(W0 * 2) + 24, f"dθ/dt = +ω{sub('0', s)}θ: every state", "label2", I["secondary"]))
    o.append(H.label(s, 574, ax.Y(W0 * 2) + 41, "off the blue line ends", "label2", I["secondary"]))
    o.append(H.label(s, 574, ax.Y(W0 * 2) + 58, "here and topples", "label2", I["secondary"]))
    o.append(H.label(s, 574, ax.Y(-W0 * 2) - 40, "stable manifold", "label", I["primary"]))
    o.append(H.label(s, 574, ax.Y(-W0 * 2) - 21, f"dθ/dt = −ω{sub('0', s)}θ: the only", "label2", I["secondary"]))
    o.append(H.label(s, 574, ax.Y(-W0 * 2) - 4, "states that fall to upright", "label2", I["secondary"]))
    o.append(H.label(s, 574, ax.Y(0) - 18, "saddle at the origin:", "label2", I["primary"]))
    o.append(H.label(s, 574, ax.Y(0) - 1, "upright, θ = dθ/dt = 0", "label2", I["primary"]))
    o.append(H.label(s, 574, ax.Y(0) + 24, f"ω{sub('0', s)} = √(Mgℓ/I) = {W0:.2f} s⁻¹", "label2", I["secondary"]))
    o.append(H.label(s, 574, ax.Y(0) + 42, "grey: trajectories,", "label2", I["secondary"]))
    o.append(H.label(s, 574, ax.Y(0) + 58, "(dθ/dt)² − ω₀²θ² constant", "label2", I["secondary"]))
    o += legend(s, ax.x0, 26, [(SER[0], None, "unstable manifold"), (SER[1], DASH_SER, "stable manifold"),
                                (I["rule"], None, "trajectory")])
    aria = ("Phase portrait of the uncontrolled inverted pendulum, lean angle theta from minus 2 to 2 degrees against "
            f"lean rate from minus 6.5 to 6.5 degrees per second, with omega-zero = {W0:.2f} per second. The origin "
            "(upright) is a saddle. Grey hyperbolic trajectories, with arrows, sweep in along the dashed blue stable "
            "manifold theta-dot = minus omega-zero theta and out along the red unstable manifold theta-dot = plus "
            "omega-zero theta; only states on the blue line fall to upright.")
    hx = np.linspace(-th_r, th_r, 161)
    hv = hover(ax, [ax.X(x) for x in hx], [[ax.Y(-W0 * x), ax.Y(W0 * x)] for x in hx],
               [f"θ = {mn(x, '{:.2f}')}°: stable dθ/dt = {mn(-W0 * x, '{:.2f}')} °/s, unstable {mn(W0 * x, '{:.2f}')} °/s" for x in hx])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #10: the toppling clock (Fig. 9)
def fig10():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    th0, tc, dl = 0.5, 1 / W0, 0.15                        # deg (line 361), s, s
    ax = Ax((80, 30, 730, 300), (0, 0.9), (0, 8))
    o = [f'<rect x="{ax.X(0):.2f}" y="{ax.top}" width="{ax.X(dl)-ax.X(0):.2f}" height="{ax.y0-ax.top}" '
         f'fill="{O["neural"]}" opacity="0.12"/>']
    o += axes(s, ax, [(v, f"{v:.2f}") for v in (0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9)], ticks((0, 2, 4, 6, 8)),
              "time after the lean begins, t (s)", "lean θ (degrees)")
    ts = np.linspace(0, 0.9, 181)
    o.append(curve(s, ax, ts, th0 * np.exp(ts / tc), SER[0]))
    t5 = tc * math.log(5 / th0)
    for tq, thq in ((tc, th0 * math.e), (t5, 5.0)):
        o.append(H.line(s, ax.X(tq), ax.Y(thq), ax.X(tq), ax.y0, I["rule"], "leader", H.DASH_REF))
        o.append(H.line(s, ax.x0, ax.Y(thq), ax.X(tq), ax.Y(thq), I["rule"], "leader", H.DASH_REF))
    g = math.exp(dl / tc)
    o.append(dot(s, ax.X(dl), ax.Y(th0 * g), O["neural"]))
    o.append(dot(s, ax.X(tc), ax.Y(th0 * math.e), O["flag"]))
    o.append(dot(s, ax.X(t5), ax.Y(5.0), O["flag"]))
    o.append(H.label(s, ax.X(0) + 8, ax.top + 20, f"neural delay Δ = {dl:.2f} s:", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0) + 8, ax.top + 37, f"the lean grows ×{g:.2f}", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0) + 8, ax.top + 54, f"(+{100*(g-1):.0f} %) before any", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0) + 8, ax.top + 71, "correction arrives", "label2", I["primary"]))
    o.append(H.label(s, ax.X(tc) + 10, ax.Y(th0 * math.e) + 22, f"one e-fold: τ{sub('c', s)} = 1/ω₀ = {tc:.2f} s,",
                     "label2", I["primary"]))
    o.append(H.label(s, ax.X(tc) + 10, ax.Y(th0 * math.e) + 39, f"θ = e·θ₀ = {th0*math.e:.2f}°", "label2", I["primary"]))
    o.append(H.label(s, ax.X(t5) - 10, ax.Y(5.0) - 10, f"5° at t = ln 10 · τ{sub('c', s)} = {t5:.2f} s", "label2",
                     I["primary"], "end"))
    o.append(H.label(s, ax.X(0.30), ax.Y(6.6), f"θ(t) = θ₀ e{sup('t/τc', s)}, θ₀ = {th0}°, no control (τ = 0)",
                     "label2", I["secondary"]))
    aria = (f"Lean angle against time for the uncontrolled body, theta = theta-zero times e to the t over tau-c, starting "
            f"at 0.5 degrees. The curve passes one e-fold, {th0*math.e:.2f} degrees, at the toppling time constant "
            f"tau-c = {tc:.2f} s and reaches 5 degrees at {t5:.2f} s. A green band marks the neural delay of 0.15 s, "
            f"within which the lean already grows by a factor {g:.2f}.")
    hts = np.linspace(0, 0.9, 181)
    hv = hover(ax, [ax.X(x) for x in hts], [ax.Y(th0 * math.exp(x / tc)) for x in hts],
               [f"t = {x:.3f} s: θ = {th0*math.exp(x/tc):.2f}°" for x in hts])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #11: the postural feedback loop (Fig. 10)
def fig11():
    VB = (0, 0, 760, 330)
    s = H.Scale(VB[2], VB[3])
    p = "m7f11_"
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    bw, bh = 226, 74
    B = {"body": (267, 46), "spin": (520, 136), "ns": (267, 228), "pf": (14, 136)}
    rows = {"body": ("body (the plant, §4)", "I d²θ/dt² = Mgℓθ − τ  (unstable)", I["rule"]),
            "spin": ("calf muscle spindles", "length ∝ θ (P),  rate ∝ dθ/dt (D)", O["neural"]),
            "ns": ("nervous system", f"τ = K{H.sub('p', s, 'label2')}θ + K{H.sub('d', s, 'label2')} dθ/dt", O["neural"]),
            "pf": ("plantarflexors (calf)", f"apply τ: COP moves to τ/Mg", O["force"])}
    for k, (x, y) in B.items():
        name, eq, acc = rows[k]
        o.append(box(s, x, y, bw, bh, acc))
        o.append(H.label(s, x + bw / 2 + 2, y + 30, name, "label", I["primary"], "middle"))
        o.append(H.label(s, x + bw / 2 + 2, y + 54, eq, "label2", I["primary"], "middle"))
    xb, yb = B["body"]
    xs_, ys_ = B["spin"]
    xn, yn = B["ns"]
    xp, yp = B["pf"]
    o.append(H.arrow(s, p, xb + bw + 4, yb + bh / 2, xs_ + bw / 2, ys_ - 6, "dim", w="ref"))
    o.append(H.label(s, xb + bw + 70, yb + bh / 2 + 4, "lean θ, dθ/dt", "label2", I["primary"]))
    o.append(H.arrow(s, p, xs_ + bw / 2, ys_ + bh + 4, xn + bw + 6, yn + bh / 2, "neural"))
    o.append(H.label(s, xs_ + bw / 2 + 10, ys_ + bh + 40, "afferent signals", "label2", I["primary"]))
    o.append(H.arrow(s, p, xn - 6, yn + bh / 2, xp + bw / 2, yp + bh + 4, "neural"))
    o.append(H.label(s, xp + bw / 2 - 10, yp + bh + 40, "motor command", "label2", I["primary"], "end"))
    o.append(H.arrow(s, p, xp + bw / 2, yp - 6, xb - 4, yb + bh / 2, "force"))
    o.append(H.label(s, xp + bw / 2 - 10, yb + bh / 2 + 4, "ankle torque τ", "label2", I["primary"], "end"))
    o.append(H.label(s, xp + bw / 2 - 10, yb + bh / 2 + 21, "(through the COP)", "label2", I["secondary"], "end"))
    o.append(H.arrow(s, p, xb + bw / 2, 4, xb + bw / 2, yb - 3, "load"))
    o.append(H.label(s, xb + bw / 2 + 10, 18, "disturbance", "label2", I["secondary"]))
    o.append(H.label(s, 380, 172, "one trip round the loop", "label2", I["secondary"], "middle"))
    o.append(H.label(s, 380, 190, "takes Δ ≈ 0.15 s (§6)", "label2", I["secondary"], "middle"))
    aria = ("Block diagram of the postural feedback loop. The body, an unstable plant obeying I theta-double-dot = Mgl "
            "theta minus tau, leans by theta. The calf muscle spindles sense length, proportional to theta (the "
            "proportional term), and rate, proportional to theta-dot (the derivative term). Green afferent signals go "
            "to the nervous system, which forms tau = Kp theta + Kd theta-dot; a green motor command goes to the "
            "plantarflexors, which apply the ankle torque by moving the centre of pressure to tau over Mg, and the red "
            "torque arrow returns to the body. A disturbance enters at the body. One trip round the loop takes about 0.15 s.")
    return svg(VB, aria, s, o)


# ================================================================ svg #12: delay-free stability region + responses (Fig. 11)
def pd_response(Kp, Kd, t):
    """Delay-free closed loop I th'' + Kd th' + (Kp - Mgl) th = 0, th(0) = 1, th'(0) = 0 (exact)."""
    a, b, c = I_B, Kd, Kp - MGL
    disc = b * b - 4 * a * c
    if disc > 0:
        r1, r2 = (-b + math.sqrt(disc)) / (2 * a), (-b - math.sqrt(disc)) / (2 * a)
        return (r2 * np.exp(r1 * t) - r1 * np.exp(r2 * t)) / (r2 - r1)
    sg, wd = -b / (2 * a), math.sqrt(-disc) / (2 * a)
    return np.exp(sg * t) * (np.cos(wd * t) - sg / wd * np.sin(wd * t))


PD_CASES = [("lightly damped", 900.0, 180.0, SER[0]), ("overdamped", 900.0, 400.0, SER[1]),
            ("unstable: passive 0.9 Mgℓ", 0.9 * MGL, 120.0, SER[2])]


def fig12():
    VB = (0, 0, 760, 390)
    s = H.Scale(VB[2], VB[3])
    p = "m7f12_"
    a1 = Ax((70, 56, 340, 300), (0, 1500), (0, 500))
    a2 = Ax((440, 56, 735, 300), (0, 3), (-0.5, 3.0))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o.append(f'<rect x="{a1.X(MGL):.2f}" y="{a1.top}" width="{a1.x1-a1.X(MGL):.2f}" height="{a1.y0-a1.top}" '
             f'fill="{O["neural"]}" opacity="0.13"/>')
    o += axes(s, a1, ticks((0, 500, 1000, 1500)), ticks((0, 100, 200, 300, 400, 500)),
              f"K{H.sub('p', s)} (N·m/rad)", f"K{H.sub('d', s)} (N·m·s/rad)", ylab_x=a1.x0 - 52, xlab_dy=42)
    o.append(H.line(s, a1.X(MGL), a1.top, a1.X(MGL), a1.y0, I["axis"], "ref", H.DASH_REF))
    o.append(H.label(s, a1.X(MGL) + 6, a1.top - 8, f"K{sub('p', s)} = Mgℓ = {MGL:.0f}", "label2", I["primary"], "middle"))
    o.append(H.label(s, a1.X(1150), a1.Y(470), "stable", "label", I["primary"], "middle"))
    o.append(H.label(s, a1.X(1150), a1.Y(470) + 17, f"K{sub('p', s)} &gt; Mgℓ, K{sub('d', s)} &gt; 0", "label2", I["secondary"], "middle"))
    o.append(H.label(s, a1.X(300), a1.Y(470), "unstable", "label", I["primary"], "middle"))
    for name, kp, kd, col in PD_CASES:
        o.append(dot(s, a1.X(kp), a1.Y(kd), col, r=5))
    kp_i = 0.9 * MGL
    o.append(H.arrow(s, p, a1.X(kp_i) + 9, a1.Y(120), a1.X(kp_i) + 70, a1.Y(120), "dim", w="ref"))
    o.append(H.label(s, a1.X(MGL) - 8, a1.Y(120) + 24, "passive", "label2", I["primary"], "end"))
    o.append(H.label(s, a1.X(MGL) - 8, a1.Y(120) + 41, f"0.9 Mgℓ = {kp_i:.0f}", "label2", I["primary"], "end"))
    o.append(H.label(s, a1.X(kp_i) + 76, a1.Y(120) + 4, "active", "label2", I["secondary"]))
    o.append(H.label(s, a1.X(900) + 10, a1.Y(180) + 5, "(900, 180)", "label2", I["secondary"]))
    o.append(H.label(s, a1.X(900) + 10, a1.Y(400) + 5, "(900, 400)", "label2", I["secondary"]))
    o.append(H.label(s, a1.x0, 26, "stable gains, no delay", "label", I["primary"]))
    # right: responses
    o += axes(s, a2, ticks((0, 1, 2, 3)), [(v, f"{v:g}") for v in (0, 1, 2, 3)], "time (s)", "lean θ/θ₀",
              ylab_x=a2.x0 - 40, xlab_dy=42)
    o.append(H.line(s, a2.x0, a2.Y(0), a2.x1, a2.Y(0), I["rule"], "leader"))
    ts = np.linspace(0, 3, 241)
    resp = {}
    for name, kp, kd, col in PD_CASES:
        y = pd_response(kp, kd, ts)
        resp[name] = y
        o.append(curve(s, a2, ts, y, col, "curve_multi"))
    y_ld = resp["lightly damped"]
    ov = -y_ld.min()
    zeta = 180.0 / (2 * math.sqrt(I_B * (900.0 - MGL)))
    o.append(H.label(s, a2.x0 + 8, a2.Y(2.75), f"passive 0.9 Mgℓ: θ grows,", "label2", I["primary"]))
    o.append(H.label(s, a2.x0 + 8, a2.Y(2.75) + 17, f"×{resp[PD_CASES[2][0]][-1]:.2f} by 3 s", "label2", I["primary"]))
    o.append(H.label(s, a2.X(1.25), a2.Y(0.62), "overdamped (900, 400)", "label2", I["primary"]))
    o.append(H.label(s, a2.X(0.3), a2.Y(-0.33), f"lightly damped (900, 180): {100*ov:.0f} % overshoot", "label2", I["primary"]))
    o.append(H.label(s, a2.x0, 26, "return to upright after a small lean", "label", I["primary"]))
    o += legend(s, 70, 382, [(c, None, n) for n, _, _, c in PD_CASES], gap=18)
    aria = ("Two panels. Left: the plane of proportional gain Kp against derivative gain Kd. The delay-free closed loop is "
            f"stable in the green quadrant right of the dashed line Kp = Mgl = {MGL:.0f} N m per rad and above Kd = 0. "
            f"An orange dot at the passive ankle stiffness 0.9 Mgl = {kp_i:.0f} lies on the unstable side, with an arrow "
            "showing that active stiffness must push it right; a red dot at (900, 180) and a blue dot at (900, 400) lie in "
            "the stable quadrant. Right: the lean, as a fraction of the initial lean, against time for those three gain "
            f"pairs: the passive case (orange) grows, the overdamped case (blue) creeps back, the lightly damped case "
            f"(red, damping ratio {zeta:.2f}) returns within about a second with a {100*ov:.0f} percent overshoot.")
    k1 = np.linspace(0, 1500, 121)
    pts1 = [[a1.X(k), a1.Y(120), f"Kp = {k:.0f}: Kp − Mgℓ = {mn(k - MGL, '{:.0f}', True)} N·m/rad → "
             + ("stable for any Kd > 0" if k > MGL else "unstable for every Kd")] for k in k1]
    pts2 = [[a2.X(t), [a2.Y(min(resp[n][i], 3.0)) for n, *_ in PD_CASES],
             f"t = {t:.2f} s: " + ", ".join(f"{n.split(':')[0]} {resp[n][i]:.2f}" for n, *_ in PD_CASES)]
            for i, t in enumerate(ts)]
    return svg(VB, aria, s, o, H.hover_attr([(a1.box, pts1), (a2.box, pts2)]))


# ================================================================ svg #13: the delay island (Fig. 12)
ISL = [(0.10, SER[1]), (0.15, SER[2]), (0.20, SER[3])]


def fig13():
    VB = (0, 0, 760, 420)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 62, 720, 362), (0, 4200), (0, 1100))
    o = []
    for D, col in ISL:
        kp, kd = hopf(D)
        o.append(f'<polygon points="{pts_str([(ax.X(a), ax.Y(b)) for a, b in zip(kp, kd)])}" fill="{col}" opacity="0.10"/>')
    o += axes(s, ax, ticks((0, 1000, 2000, 3000, 4000)), ticks((0, 250, 500, 750, 1000)),
              f"proportional gain K{H.sub('p', s)} (N·m/rad)", f"derivative gain K{H.sub('d', s)} (N·m·s/rad)",
              ylab_x=ax.x0 - 58, xlab_dy=44)
    for D, col in ISL:
        kp, kd = hopf(D)
        o.append(curve(s, ax, kp[::3], kd[::3], col, "curve_multi"))
    o.append(curve(s, ax, [MGL, MGL], [0, 1100], SER[0], "curve_multi"))
    o.append(H.label(s, ax.X(MGL) - 4, ax.top - 8, f"divergence boundary K{sub('p', s)} = Mgℓ = {MGL:.0f}", "label2", I["primary"]))
    for D, col in ISL:
        kp, kd = hopf(D)
        k = int(kp.argmax())
        o.append(H.label(s, ax.X(kp[k]) + 8, ax.Y(kd[k]) + 5, f"Δ = {D:.2f} s", "label2", I["primary"]))
    o.append(H.label(s, ax.X(2600), ax.Y(1010), "each curve: Hopf boundary (Proposition 6.2);", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(2600), ax.Y(1010) + 17, "stable gains lie inside it", "label2", I["secondary"]))
    dc = theory(900.0, 120.0)[0]
    o.append(dot(s, ax.X(900), ax.Y(120), I["primary"], r=5))
    o.append(H.line(s, ax.X(900) + 6, ax.Y(120) + 3, ax.X(2180), ax.Y(120) - 4, I["rule"], "leader"))
    o.append(H.label(s, ax.X(2200), ax.Y(120), f"(900, 120): Δ{sub('crit', s)} = {dc:.2f} s, so it lies", "label2", I["primary"]))
    o.append(H.label(s, ax.X(2200), ax.Y(120) + 17, "inside the 0.10 s island, outside 0.15 s", "label2", I["primary"]))
    o += legend(s, ax.x0, 22, [(SER[0], None, "Kₚ = Mgℓ")] + [(c, None, f"Δ = {D:.2f} s") for D, c in ISL])
    areas = [island_area(D) for D, _ in ISL]
    aria = ("Stability islands of the delayed PD controller in the plane of proportional gain Kp (0 to 4200 N m per rad) "
            "and derivative gain Kd (0 to 1100 N m s per rad), from the closed-form boundaries of Proposition 6.2. Each "
            f"island lies between the red divergence line Kp = Mgl = {MGL:.0f} and a Hopf curve. For a delay of 0.10 s "
            f"(blue) the island reaches Kp = {hopf(0.10)[0].max():.0f}; for 0.15 s (orange) {hopf(0.15)[0].max():.0f}; "
            f"for 0.20 s (green) {hopf(0.20)[0].max():.0f}. Areas: {areas[0]/1e6:.2f}, {areas[1]/1e6:.2f} and "
            f"{areas[2]/1e6:.2f} million. A black dot at Kp = 900, Kd = 120 has critical delay {dc:.2f} s: inside the "
            "0.10 s island and outside the 0.15 s one.")
    hk = np.linspace(MGL + 5, 4100, 160)
    pts = []
    for k in hk:
        ys, parts = [], []
        for D, _ in ISL:
            r = island_kd(D, k)
            if r:
                ys += [ax.Y(r[0]), ax.Y(r[1])]
                parts.append(f"Δ {D:.2f}: Kd {r[0]:.0f}–{r[1]:.0f}")
        pts.append([ax.X(k), ys or ax.Y(0), f"Kp = {k:.0f}: " + ("; ".join(parts) if parts else "no stable Kd")])
    return svg(VB, aria, s, o, hover(ax, *zip(*pts)))


# ================================================================ svg #14: crossing the critical delay (Fig. 13)
DDE_CASES = [(0.18, "unstable", SER[0]), (0.13, "sway", SER[1]), (0.08, "stable", SER[2])]


def fig14():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    LIM = 1.6
    ax = Ax((80, 50, 730, 310), (0, 12), (-LIM, LIM))
    o = axes(s, ax, ticks(range(0, 13, 2)), [(v, mn(v, "{:.1f}")) for v in (-1.6, -0.8, 0, 0.8, 1.6)],
             "time (s)", "lean θ (degrees)")
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["rule"], "leader"))
    runs = {}
    for D, name, col in DDE_CASES:
        t, th = simulate(900.0, 120.0, D, T=12.0)
        runs[D] = (t, th)
        k = len(th) if np.abs(th).max() < LIM else int(np.argmax(np.abs(th) >= LIM))
        sel = list(range(0, k, 50)) + ([k] if k < len(th) else [])
        ys = [max(-LIM, min(LIM, th[i])) for i in sel]
        o.append(curve(s, ax, [t[i] for i in sel], ys, col, "curve_multi"))
    t, th = runs[0.13]
    pk = [i for i in range(1, len(th) - 1) if th[i] > th[i - 1] and th[i] >= th[i + 1] and t[i] > 1]
    per = (t[pk[-1]] - t[pk[0]]) / (len(pk) - 1)
    a_early, a_late = np.abs(th[(t > 2) & (t < 5)]).max(), np.abs(th[t > 9]).max()
    t18, th18 = runs[0.18]
    k18 = int(np.argmax(np.abs(th18) >= LIM))
    o.append(H.label(s, ax.X(t18[k18]) + 10, ax.top + 14, f"Δ = 0.18 s: the swing grows and leaves the plot at "
                     f"t = {t18[k18]:.1f} s", "label2", I["primary"]))
    o.append(H.label(s, ax.X(3.6), ax.Y(1.05), f"Δ = 0.13 s ≈ Δ{sub('crit', s)}: sustained sway at {1/per:.2f} Hz, "
                     f"amplitude {a_early:.2f}° → {a_late:.2f}° over 12 s", "label2", I["primary"]))
    o.append(H.label(s, ax.X(6.0), ax.Y(-0.85), "Δ = 0.08 s: the lean decays to 0", "label2", I["primary"]))
    o.append(H.label(s, ax.x1, ax.y0 - 10, f"K{sub('p', s)} = 900, K{sub('d', s)} = 120, start 0.6°", "label2",
                     I["secondary"], "end"))
    o += legend(s, ax.x0, 30, [(c, None, f"Δ = {D:.2f} s ({n})") for D, n, c in DDE_CASES])
    aria = ("Lean angle against time over 12 seconds from the Lab 1 integrator of the delay-differential equation, gains "
            "Kp = 900 and Kd = 120, starting at 0.6 degrees with a constant history. With delay 0.08 s (orange) the lean "
            f"decays to zero; at 0.13 s, the critical delay, (blue) it settles into a sustained oscillation at {1/per:.2f} Hz "
            f"whose amplitude goes only from {a_early:.2f} to {a_late:.2f} degrees; at 0.18 s (red) the oscillation grows "
            f"and leaves the plotted range at {t18[k18]:.1f} s.")
    hs = list(range(0, len(t), 100))
    pts = []
    for i in hs:
        ys = [ax.Y(runs[D][1][i]) for D, *_ in DDE_CASES if abs(runs[D][1][i]) <= 1.6]
        pts.append([ax.X(t[i]), ys, f"t = {t[i]:.1f} s: " + ", ".join(f"Δ {D:.2f}: {mn(runs[D][1][i], '{:.2f}')}°"
                                                                      for D, *_ in DDE_CASES)])
    return svg(VB, aria, s, o, hover(ax, *zip(*pts)))


# ================================================================ svg #20: L5/S1 compression vs flexion (Fig. 19)
REACH = [(0.40, SER[0]), (0.30, SER[1]), (0.20, SER[2])]


def fig20():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 50, 556, 320), (0, 90), (0, 4.5))
    o = axes(s, ax, ticks(range(0, 91, 15)), [(v, f"{v:g}") for v in (0, 1, 2, 3, 4)],
             "trunk flexion φ (degrees from vertical)", "L5/S1 compression (kN)")
    o.append(H.line(s, ax.x0, ax.Y(LIMIT / 1e3), ax.x1, ax.Y(LIMIT / 1e3), O["flag"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.x0 + 8, ax.Y(LIMIT / 1e3) - 8, "3.4 kN injury-risk threshold", "label2", I["primary"]))
    ph = np.linspace(0, 90, 181)
    cur = {}
    for rL, col in REACH:
        F = np.array([compression(x, 20.0, rL) for x in ph]) / 1e3
        cur[rL] = F
        o.append(curve(s, ax, ph, F, col, "curve_multi"))
        k = int(F.argmax())
        o.append(dot(s, ax.X(ph[k]), ax.Y(F[k]), col))
        o.append(H.label(s, ax.x1 + 10, ax.Y(F[-1]) + 5, f"r{sub('L', s)} = {rL:.2f} m: peak {F[k]:.2f} kN", "label2", I["primary"]))
    F4 = cur[0.40]
    kx = int(np.argmax(F4 > LIMIT / 1e3))
    xc = ph[kx - 1] + (LIMIT / 1e3 - F4[kx - 1]) / (F4[kx] - F4[kx - 1]) * (ph[kx] - ph[kx - 1])
    o.append(dot(s, ax.X(xc), ax.Y(LIMIT / 1e3), O["flag"]))
    o.append(H.label(s, ax.X(xc) - 10, ax.Y(LIMIT / 1e3) - 8, f"crossed at φ = {xc:.0f}°", "label2", I["primary"], "end"))
    full = compression(90, 20.0, 0.40) / 1e3
    o.append(H.label(s, ax.X(90), ax.Y(cur[0.40].max()) - 12, f"full bend: {full:.2f} kN (§8 lift)", "label2", I["primary"], "end"))
    up = compression(0, 20.0, 0.40) / 1e3
    o.append(H.label(s, ax.X(3), ax.Y(up) + 22, f"upright: (m{sub('t', s)} + m{sub('L', s)})g = {up:.2f} kN", "label2", I["secondary"]))
    o.append(H.label(s, ax.x1 + 10, ax.Y(1.4), f"20 kg load, m{sub('t', s)} = 35 kg,", "label2", I["secondary"]))
    o.append(H.label(s, ax.x1 + 10, ax.Y(1.4) + 17, f"r{sub('t', s)} = 0.30 m, d = 0.05 m", "label2", I["secondary"]))
    o += legend(s, ax.x0, 30, [(c, None, f"r{sub('L', s)} = {r:.2f} m") for r, c in REACH])
    aria = ("L5/S1 compression from Proposition 8.2, muscle term plus axial weight term, against trunk flexion from 0 to 90 "
            "degrees, for a 20 kg load held at reaches of 0.40 m (red), 0.30 m (blue) and 0.20 m (orange). All three start "
            f"at {up:.2f} kN upright and peak near 80 degrees, at {cur[0.40].max():.2f}, {cur[0.30].max():.2f} and "
            f"{cur[0.20].max():.2f} kN. A dashed orange line marks the 3.4 kN injury-risk threshold: only the 0.40 m reach "
            f"crosses it, at {xc:.0f} degrees, and reaches {full:.2f} kN at full bend.")
    pts = [[ax.X(x), [ax.Y(cur[r][i]) for r, _ in REACH],
            f"φ = {x:.1f}°: " + ", ".join(f"rL {r:.2f} m {cur[r][i]:.2f} kN" for r, _ in REACH)] for i, x in enumerate(ph)]
    return svg(VB, aria, s, o, hover(ax, *zip(*pts)))


# ================================================================ svg #22: critical delay vs Kp (Fig. 20)
KP_SIM = (650.0, 700.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0, 1300.0, 1400.0, 1500.0, 1600.0)


def fig22():
    VB = (0, 0, 760, 390)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((90, 50, 730, 310), (600, 1650), (50, 200))
    o = axes(s, ax, ticks((700, 900, 1100, 1300, 1500)), ticks((50, 100, 150, 200)),
             f"proportional gain K{H.sub('p', s)} (N·m/rad), K{H.sub('d', s)} = 120", f"critical delay Δ{H.sub('crit', s)} (ms)")
    o.append(H.line(s, ax.x0, ax.Y(150), ax.x1, ax.Y(150), I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.x1 - 4, ax.Y(150) - 8, "neural delay ≈ 150 ms", "label2", I["primary"], "end"))
    ks = np.linspace(630, 1650, 205)
    th_ = [1e3 * theory(k, 120.0)[0] for k in ks]
    keep = [(k, v) for k, v in zip(ks, th_) if v <= 200]
    o.append(curve(s, ax, [k for k, _ in keep], [v for _, v in keep], SER[0]))
    sim = [(k, 1e3 * bisect_delay(k, 120.0)[0]) for k in KP_SIM]
    for k, v in sim:
        o.append(dot(s, ax.X(k), ax.Y(v), SER[1], hollow=True, r=5))
    lo, hi = 650.0, 1500.0
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if theory(mid, 120.0)[0] > 0.15 else (lo, mid)
    kx = 0.5 * (lo + hi)
    o.append(dot(s, ax.X(kx), ax.Y(150), O["flag"]))
    o.append(lead(s, ax.X(kx) - 2, ax.Y(150) + 5, ax.X(700), ax.Y(96), I["rule"]))
    o.append(H.label(s, ax.X(640), ax.Y(88), f"K{sub('p', s)} = {kx:.0f}: Δ{sub('crit', s)} = 150 ms;", "label2", I["primary"]))
    o.append(H.label(s, ax.X(640), ax.Y(88) + 17, "stiffer gains cannot stand", "label2", I["primary"]))
    o.append(H.label(s, ax.X(640), ax.Y(88) + 34, "without prediction", "label2", I["primary"]))
    d9 = theory(900.0, 120.0)[0] * 1e3
    o.append(lead(s, ax.X(900) + 4, ax.Y(d9) - 5, ax.X(1000), ax.Y(176), I["rule"]))
    o.append(H.label(s, ax.X(1005), ax.Y(176), f"Lab 1 at (900, 120): {bisect_delay(900.0, 120.0)[0]*1e3:.1f} ms "
                     f"simulated, {d9:.1f} ms theory", "label2", I["primary"]))
    o += legend(s, ax.x0, 30, [(SER[0], None, "theory, Proposition 6.3"), (SER[1], None, "Lab 1 bisection (DDE simulation)", "hdot")])
    err = max(abs(v - 1e3 * theory(k, 120.0)[0]) for k, v in sim)
    aria = ("Critical delay in milliseconds against proportional gain Kp from 650 to 1600 N m per rad, Kd = 120. A red "
            "curve is the closed form of Proposition 6.3; blue open circles are the Lab 1 bisection on the simulated "
            f"delay-differential equation, which agree with it to within {err:.1f} ms. Both fall from "
            f"{1e3*theory(650.0, 120.0)[0]:.0f} ms at Kp = 650 to {1e3*theory(1600.0, 120.0)[0]:.0f} ms at 1600. A dashed "
            f"line marks the 150 ms neural delay, crossed at Kp = {kx:.0f}.")
    simd = dict(sim)
    pts = [[ax.X(k), ax.Y(v), f"Kp = {k:.0f}: theory {v:.1f} ms" + (f", simulation {simd[k]:.1f} ms" if k in simd else "")]
           for k, v in keep[::2]] + [[ax.X(k), ax.Y(v), f"Kp = {k:.0f}: simulation {v:.1f} ms, theory "
                                      f"{1e3*theory(k, 120.0)[0]:.1f} ms"] for k, v in sim]
    pts.sort(key=lambda q: q[0])
    return svg(VB, aria, s, o, hover(ax, *zip(*pts)))


# ================================================================ svg #24: safe lifting envelope (Fig. 21)
def fig24():
    VB = (0, 0, 760, 390)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 50, 730, 310), (0.10, 0.55), (0, 65))
    rs = np.linspace(0.10, 0.55, 91)
    ms = [safe_load(r) for r in rs]
    o = [f'<polygon points="{pts_str([(ax.X(r), ax.Y(m)) for r, m in zip(rs, ms)] + [(ax.X(0.55), ax.y0), (ax.X(0.10), ax.y0)])}" '
         f'fill="{O["neural"]}" opacity="0.12"/>']
    o += axes(s, ax, [(v, f"{v:.1f}") for v in (0.1, 0.2, 0.3, 0.4, 0.5)], ticks((0, 10, 20, 30, 40, 50, 60)),
              f"reach r{H.sub('L', s)}, load to spine (m)", "maximum safe load (kg)")
    o.append(curve(s, ax, rs, ms, SER[0]))
    for r, m in lab2_grid():
        o.append(dot(s, ax.X(r), ax.Y(m), I["secondary"], hollow=True))
    o.append(dot(s, ax.X(0.40), ax.Y(20), O["flag"], r=5))
    m40 = safe_load(0.40)
    o.append(H.label(s, ax.X(0.40) + 10, ax.Y(20) - 22, "§8 lift: 20 kg at 0.40 m,", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.40) + 10, ax.Y(20) - 6, f"over the limit (safe: {m40:.1f} kg)", "label2", I["primary"]))
    g = lab2_grid()
    o.append(H.label(s, ax.X(0.16) + 8, ax.Y(g[0][1]) - 4, f"{g[0][1]:.1f} kg at 0.15 m", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.45), ax.Y(g[6][1]) + 26, f"{g[6][1]:.1f} kg at 0.45 m: ÷{g[0][1]/g[6][1]:.1f}", "label2",
                     I["primary"], "middle"))
    o.append(H.label(s, ax.X(0.22), ax.Y(8), "safe: worst-case compression below 3.4 kN", "label2", I["primary"]))
    o += legend(s, ax.x0, 30, [(SER[0], None, "safe-load limit (bisection on load)"),
                               (I["secondary"], None, "Lab 2 output (0.5 kg grid)", "hdot")])
    aria = ("Maximum safe load in kilograms against reach from 0.10 to 0.55 m, from the Lab 2 compression model with a 3.4 kN "
            f"limit: a red curve falling from {safe_load(0.10):.0f} kg at 0.10 m to {safe_load(0.55):.1f} kg at 0.55 m, the "
            "green region below it safe. Open circles are the Lab 2 table on its 0.5 kg grid, 42.5 kg at 0.15 m to 13.0 kg "
            f"at 0.50 m. An orange dot at 20 kg and 0.40 m, the section 8 lift, sits above the curve, whose value there is "
            f"{m40:.1f} kg.")
    pts = [[ax.X(r), ax.Y(m), f"rL = {r:.3f} m: max safe load {m:.1f} kg"] for r, m in zip(rs, ms)]
    return svg(VB, aria, s, o, hover(ax, *zip(*pts)))


# ================================================================ svg #25: where each idealisation is repaid (Fig. 22)
def fig25():
    VB = (0, 0, 760, 360)
    s = H.Scale(VB[2], VB[3])
    p = "m7f25_"
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    cx, cy, cw, ch = 262, 128, 236, 92
    o.append(box(s, cx, cy, cw, ch, O["force"]))
    o.append(H.label(s, cx + cw / 2 + 2, cy + 32, "delayed-PD inverted pendulum", "label", I["primary"], "middle"))
    o.append(H.label(s, cx + cw / 2 + 2, cy + 54, "one rigid segment, sagittal plane,", "label2", I["secondary"], "middle"))
    o.append(H.label(s, cx + cw / 2 + 2, cy + 72, "reactive control (this module)", "label2", I["secondary"], "middle"))
    bw, bh = 214, 64
    L = [("Module 8 · walking", "multi-segment and frontal-plane", "balance, stepping", 10, 14),
         ("Module 9 · running, jumping", "large-angle and spring-mass", "dynamics, impact loading", 10, 141),
         ("Module 12 · whole limb", "muscle redundancy beyond", "one agonist-antagonist pair", 10, 268)]
    R = [("Module 13 · sensorimotor", "fusion of vision, vestibular", "and proprioceptive signals", 536, 60),
         ("Module 14 · tissue loading", "dynamic spinal loading,", "tissue fatigue and creep", 536, 222)]
    for title, l1, l2, x, y in L + R:
        o.append(box(s, x, y, bw, bh, O["geometry"]))
        o.append(H.label(s, x + bw / 2 + 2, y + 22, title, "label2", I["primary"], "middle", 'font-weight="bold"'))
        o.append(H.label(s, x + bw / 2 + 2, y + 39, l1, "label2", I["secondary"], "middle"))
        o.append(H.label(s, x + bw / 2 + 2, y + 55, l2, "label2", I["secondary"], "middle"))
        right = x > cx
        sx = cx + cw + 4 if right else cx - 4
        sy = cy + ch / 2 + (y + bh / 2 - (cy + ch / 2)) * 0.35
        ex = x - 6 if right else x + bw + 6
        o.append(H.arrow(s, p, sx, sy, ex, y + bh / 2, "dim", w="ref"))
    o.append(H.label(s, 380, 352, "Predictive (internal-model) control: beyond this course; §6 states what it must achieve.",
                     "label2", I["secondary"], "middle"))
    aria = ("Hub diagram. A central box, the delayed-PD inverted pendulum of this module (one rigid segment, sagittal plane, "
            "reactive control), sends arrows to the five modules that repay its idealisations: Module 8, walking "
            "(multi-segment and frontal-plane balance, stepping); Module 9, running and jumping (large-angle and "
            "spring-mass dynamics, impact loading); Module 12, whole-limb muscle redundancy; Module 13, sensorimotor "
            "fusion of vision, vestibular and proprioceptive signals; Module 14, dynamic spinal loading, tissue fatigue "
            "and creep. A footnote: predictive control is beyond this course.")
    return svg(VB, aria, s, o)


FIGS = {
    6: ("Left: a force plate in perspective with load cells at the co", fig6),
    9: ("Phase portrait in the plane of lean angle theta (horizontal)", fig9),
    10: ("Plot of lean angle versus time, growing exponentially. The t", fig10),
    11: ("Block diagram of the postural feedback loop. The body plant ", fig11),
    12: ("Left: stability region in the plane of proportional gain Kp ", fig12),
    13: ("Stability island in the plane of proportional gain Kp (horiz", fig13),
    14: ("Lean angle versus time from integrating the delay-differenti", fig14),
    20: ("L5/S1 compression versus trunk flexion angle for load reache", fig20),
    22: ("Critical delay in milliseconds versus proportional gain Kp. ", fig22),
    24: ("Maximum safe load in kilograms versus reach in metres, a ste", fig24),
    25: ("A central delayed-PD inverted pendulum box with arrows to th", fig25),
}
