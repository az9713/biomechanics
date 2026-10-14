"""Module 6 main-text plots in the house style (group `plots_main`).

Every plotted number is computed here from the formula or the code the module states:
  sigma(eps) (Prop. 1, Eq. 1.2), F(x) and k(x) (Prop. 2, Eqs. 2.2-2.3), U(x) (Prop. 3, Eq. 3.3),
  the prescribed fibre/tendon split of Fig. 9 (Eq. 4.4), the SLS step responses (Prop. 7), the SLS
  steady cycle and tan delta (Prop. 9, Eq. 7.3), the one-sided ligament torque (Lemma 1, Eq. 8.1)
  and Labs 1-3 (their code, unchanged).
All figures use a 760-unit-wide viewBox, so one user unit is one rendered px.
"""
import math
from functools import lru_cache

import numpy as np

import house as H
from m05.plots_main import (Ax, axes, curve, dot, legend, lead, hover, svg, mn, tw, pts_str, sub,
                            DASH_SER, GRID, BOXFILL)

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES


def raxis(s, ax, ticks, title, title_dx=58):
    """Right-hand axis on the same box: ticks [(y in ax units, text)], rotated title (ink)."""
    o = [H.line(s, ax.x1, ax.y0, ax.x1, ax.top, I["axis"], "axis")]
    for v, txt in ticks:
        o.append(H.line(s, ax.x1, ax.Y(v), ax.x1 + 5, ax.Y(v), I["axis"], "leader"))
        o.append(H.label(s, ax.x1 + 9, ax.Y(v) + 4.5, txt, "tick", I["secondary"], "start"))
    yx, ym = ax.x1 + title_dx, (ax.y0 + ax.top) / 2
    o.append(H.label(s, yx, ym, title, "label", I["primary"], "middle", f'transform="rotate(90 {yx:.2f} {ym:.2f})"'))
    return o


def band(ax, xa, xb, ya=None, yb=None):
    ya = ax.top if ya is None else ya
    yb = ax.y0 if yb is None else yb
    return f'<rect x="{ax.X(xa):.2f}" y="{ya:.2f}" width="{ax.X(xb) - ax.X(xa):.2f}" height="{yb - ya:.2f}" fill="{BOXFILL}"/>'


def area(xy_top, y_base):
    """Closed polygon under a curve given in user units."""
    pts = list(xy_top) + [(xy_top[-1][0], y_base), (xy_top[0][0], y_base)]
    return f'<polygon points="{pts_str(pts)}" fill="{SER[0]}" opacity="0.13"/>'


# ================================================================ tendon constants (secs. 1-3)
E_LIN, EPS_T, EPS_F = 1300.0, 3.0, 9.0          # MPa, toe end (%), rupture (%)   lines 147, 178
A0, L0 = 80.0, 250.0                            # mm^2, mm                          line 264
K_LIN = A0 * E_LIN / L0                         # 416 N/mm                          line 265
X_T, X_F = EPS_T / 100 * L0, EPS_F / 100 * L0   # 7.5 mm, 22.5 mm                   line 266


def sigma(e):
    """Eq. 1.2, e in %, MPa."""
    e = e / 100
    et = EPS_T / 100
    return E_LIN / (2 * et) * e * e if e <= et else E_LIN * et / 2 + E_LIN * (e - et)


def phi(e):
    return min(e / EPS_T, 1.0)


def F_x(x):
    """Eq. 2.3, x in mm, N."""
    return K_LIN / (2 * X_T) * x * x if x <= X_T else K_LIN * (x - X_T / 2)


def k_x(x):
    return K_LIN * min(x / X_T, 1.0)


def U_x(x):
    """Eq. 3.3, x in mm, J (N mm / 1000)."""
    if x <= X_T:
        return K_LIN / (6 * X_T) * x ** 3 / 1000
    return K_LIN * (x * x / 2 - X_T * x / 2 + X_T ** 2 / 6) / 1000


# ================================================================ svg #5: the J-shaped law (Fig. 3)
def fig5():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 50, 670, 330), (0, 10.5), (0, 110))
    es = [round(i * 0.1, 6) for i in range(int(round(EPS_F / 0.1)) + 1)]
    sf, st = sigma(EPS_F), sigma(EPS_T)
    o = [band(ax, 0, EPS_T)]
    o += axes(s, ax, [(v, f"{v:g}") for v in (0, 2, 3, 4, 6, 8, 9, 10)], [(v, f"{v}") for v in range(0, 101, 20)],
              "strain ε (%)", "stress σ (MPa)")
    o += raxis(s, ax, [(0, "0"), (50, "0.5"), (100, "1")], "recruited fraction Φ")
    o.append(curve(s, ax, es, [100 * phi(e) for e in es], SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, ax, es, [sigma(e) for e in es], SER[0]))
    o.append(H.label(s, ax.X(1.5), ax.Y(88), "toe:", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, ax.X(1.5), ax.Y(88) + 16, "crimp", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.X(1.5), ax.Y(88) + 32, "straightens", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.X(5.0), ax.Y(100) - 9, "Φ = 1: every fibril recruited from ε* = 3 % on", "label2", I["primary"]))
    o.append(dot(s, ax.X(EPS_T), ax.Y(st), O["flag"]))
    o.append(H.label(s, ax.X(EPS_T) + 10, ax.Y(st) + 18, f"toe ends: ε* = 3 %, σ = {st:.1f} MPa", "label2", I["primary"]))
    o.append(H.label(s, ax.X(6.3), ax.Y(38), f"linear: slope E{sub('lin', s)} = 1.3 GPa", "label2", I["primary"]))
    o.append(H.label(s, ax.X(6.3), ax.Y(38) + 16, "(straight collagen)", "label2", I["secondary"]))
    o.append(dot(s, ax.X(EPS_F), ax.Y(sf), O["flag"]))
    o.append(H.label(s, ax.X(EPS_F) + 9, ax.Y(sf) - 2, "rupture", "label2", I["primary"]))
    o.append(H.label(s, ax.X(EPS_F) + 9, ax.Y(sf) + 14, f"{sf:.1f} MPa", "label2", I["secondary"]))
    o += legend(s, ax.x0, 30, [(SER[0], None, "stress σ (left axis)"), (SER[1], DASH_SER, "recruited fraction Φ (right axis)")])
    aria = ("The J-shaped stress-strain law of tendon from Proposition 1 with E_lin 1.3 GPa and a uniform crimp "
            f"distribution ending at 3 percent strain. Red: stress rises as a parabola through the shaded toe to {st:.1f} MPa "
            f"at 3 percent, then linearly with slope 1.3 GPa to rupture at 9 percent and {sf:.1f} MPa. Blue dashed, right "
            "axis: the recruited fraction Phi rises linearly from 0 and reaches 1 exactly where the toe ends.").replace("_", " ")
    hv = hover(ax, [ax.X(e) for e in es], [[ax.Y(sigma(e)), ax.Y(100 * phi(e))] for e in es],
               [f"ε = {e:.2f} %: σ = {sigma(e):.1f} MPa, Φ = {phi(e):.2f}, E = {1.3 * phi(e):.2f} GPa" for e in es])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #8: force-elongation and stiffness (Fig. 5)
def fig8():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 50, 670, 330), (0, 26), (0, 8.8))         # right axis: k = 50 x F (kN), so 2 kN <-> 100 N/mm
    xs = sorted(set([round(i * 0.2, 6) for i in range(int(round(X_F / 0.2)) + 1)] + [X_T]))
    ft, ff = F_x(X_T) / 1000, F_x(X_F) / 1000
    o = [band(ax, 5, 12.5)]
    o += axes(s, ax, [(v, f"{v}") for v in range(0, 25, 4)], [(v, f"{v}") for v in range(0, 9, 2)],
              "elongation x (mm)", "force F (kN)")
    o += raxis(s, ax, [(v / 50, f"{v}") for v in range(0, 401, 100)], "stiffness k (N/mm)")
    o.append(H.label(s, ax.X(10.2), ax.Y(7.2), "walk–run", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, ax.X(10.2), ax.Y(7.2) + 16, "x ≈ 5–12 mm", "label2", I["secondary"], "middle"))
    o.append(curve(s, ax, xs, [k_x(x) / 50 for x in xs], SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, ax, xs, [F_x(x) / 1000 for x in xs], SER[0]))
    o.append(H.label(s, ax.X(13.5), ax.Y(K_LIN / 50) - 9, f"plateau k{sub('lin', s)} = A{sub('0', s)}E{sub('lin', s)}/L{sub('0', s)} = {K_LIN:.0f} N/mm",
                     "label2", I["primary"]))
    o.append(dot(s, ax.X(X_T), ax.Y(ft), O["flag"]))
    o.append(dot(s, ax.X(X_T), ax.Y(K_LIN / 50), O["flag"]))
    o.append(H.label(s, ax.X(X_T) + 10, ax.Y(ft) + 18, f"toe ends: x* = {X_T:.1f} mm, F = {ft:.2f} kN", "label2", I["primary"]))
    o.append(H.label(s, ax.X(13.2), ax.Y(2.6), f"linear: F = k{sub('lin', s)}(x − x*/2)", "label2", I["secondary"]))
    o.append(dot(s, ax.X(X_F), ax.Y(ff), O["flag"]))
    o.append(H.label(s, ax.X(X_F) + 9, ax.Y(ff) + 2, "rupture", "label2", I["primary"]))
    o.append(H.label(s, ax.X(X_F) + 9, ax.Y(ff) + 18, f"{ff:.1f} kN", "label2", I["secondary"]))
    o += legend(s, ax.x0, 30, [(SER[0], None, "force F (left axis)"), (SER[1], DASH_SER, "stiffness k = dF/dx (right axis)")])
    aria = (f"Structural force-elongation curve of an Achilles tendon from Eq. 2.3 with A0 80 mm2, L0 250 mm and E_lin "
            f"1.3 GPa. Red: force rises as a parabola through the toe to {ft:.2f} kN at x* = 7.5 mm, then linearly to "
            f"rupture at 22.5 mm and {ff:.1f} kN. Blue dashed, right axis: the stiffness dF/dx climbs linearly through the toe "
            f"and plateaus at k_lin = {K_LIN:.0f} N/mm. A shaded band marks the walking-to-running range, 5 to 12 mm.").replace("_", " ")
    hv = hover(ax, [ax.X(x) for x in xs], [[ax.Y(F_x(x) / 1000), ax.Y(k_x(x) / 50)] for x in xs],
               [f"x = {x:.1f} mm: F = {F_x(x) / 1000:.2f} kN, k = {k_x(x):.0f} N/mm" for x in xs])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #9: stored energy (Fig. 6)
def fig9():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    p = "m6f9_"
    ax = Ax((80, 50, 670, 330), (0, 26), (0, 10))          # right axis: U = 10 x F, so 2 kN <-> 20 J
    XP = 16.0                                               # running push-off (line 312)
    xs = sorted(set([round(i * 0.2, 6) for i in range(int(round(X_F / 0.2)) + 1)] + [X_T]))
    xa = [x for x in xs if x <= XP + 1e-9]
    up, ut, fp = U_x(XP), U_x(X_T), F_x(XP) / 1000
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o.append(area([(ax.X(x), ax.Y(F_x(x) / 1000)) for x in xa], ax.y0))
    o += axes(s, ax, [(v, f"{v}") for v in range(0, 25, 4)], [(v, f"{v}") for v in range(0, 11, 2)],
              "elongation x (mm)", "force F (kN)")
    o += raxis(s, ax, [(v / 10, f"{v}") for v in range(0, 101, 20)], "stored energy U (J)")
    o.append(H.line(s, ax.X(XP), ax.y0, ax.X(XP), ax.top + 14, I["rule"], "leader", H.DASH_REF))
    o.append(H.label(s, ax.X(XP), ax.top + 8, "running push-off, x ≈ 16 mm", "label2", I["primary"], "middle"))
    o.append(H.line(s, ax.X(X_T), ax.y0, ax.X(X_T), ax.Y(F_x(X_T) / 1000), I["rule"], "leader"))
    o.append(curve(s, ax, xs, [U_x(x) / 10 for x in xs], SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, ax, xs, [F_x(x) / 1000 for x in xs], SER[0]))
    o.append(H.label(s, ax.X(12.6), ax.Y(0.4), f"linear region: {up - ut:.1f} J", "label2", I["primary"], "middle"))
    o.append(H.line(s, ax.X(5.4), ax.Y(0.12), ax.X(4.2), ax.Y(1.55) + 4, I["rule"], "leader"))
    o.append(H.label(s, ax.X(4.2), ax.Y(1.55), f"toe: {ut:.1f} J ({100 * ut / up:.0f} %)", "label2", I["primary"], "end"))
    o.append(dot(s, ax.X(XP), ax.Y(up / 10), SER[1]))
    o.append(H.label(s, ax.X(XP) + 10, ax.Y(up / 10) + 18, f"U(16 mm) = {up:.1f} J", "label2", I["primary"]))
    o.append(dot(s, ax.X(XP), ax.Y(fp), SER[0]))
    o.append(H.label(s, ax.X(XP) - 10, ax.Y(fp) - 8, f"F = {fp:.1f} kN", "label2", I["primary"], "end"))
    o += legend(s, ax.x0, 30, [(SER[0], None, "force F (left axis)"), (SER[1], DASH_SER, "stored energy U(x) (right axis)"),
                               (SER[0], None, "U = area under F", "band")])
    aria = (f"Force-elongation curve of the Achilles tendon (red, left axis) with the area beneath it shaded up to a running "
            f"push-off at 16 mm, where the force is {fp:.1f} kN: that area is the stored elastic energy, {up:.1f} J by Eq. 3.3. "
            f"Only {ut:.1f} J of it lies in the toe, below x* = 7.5 mm; {up - ut:.1f} J lies in the linear region. The blue "
            "dashed curve on the right axis is the running total U(x), steepest where the force is largest.")
    hv = hover(ax, [ax.X(x) for x in xs], [[ax.Y(F_x(x) / 1000), ax.Y(U_x(x) / 10)] for x in xs],
               [f"x = {x:.1f} mm: F = {F_x(x) / 1000:.2f} kN, U = {U_x(x):.1f} J" for x in xs])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #12: the prescribed split (Fig. 9)
T_LOAD, T_PUSH = 0.15, 0.22               # s: loading 0-0.15, push-off 0.15-0.22 (the old figure's phases)
A_LOAD, SPLIT = 0.54, 6.0                 # fibre peak in loading (l0/s); tendon : fibre at push-off (line 382)
# push-off amplitude chosen so the tendon recoils exactly the stretch it stored in loading (integral of x' = 0)
A_PUSH = A_LOAD * T_LOAD * (SPLIT + 1) / ((T_PUSH - T_LOAD) * SPLIT)


def split(t):
    """(v_MTU, v_tendon, v_fibre) shortening velocities, l0/s, Eq. 4.4 with theta_p = 0."""
    if t <= T_LOAD:
        vf = A_LOAD * math.sin(math.pi * t / T_LOAD)
        return 0.0, -vf, vf
    if t <= T_PUSH:
        vm = A_PUSH * math.sin(math.pi * (t - T_LOAD) / (T_PUSH - T_LOAD))
        return vm, vm * SPLIT / (SPLIT + 1), vm / (SPLIT + 1)
    return 0.0, 0.0, 0.0


def fig12():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 50, 735, 320), (0, 0.25), (-0.8, 1.7))
    ts = [i * 0.002 for i in range(126)]
    V = [split(t) for t in ts]
    tm = (T_LOAD + T_PUSH) / 2
    vm, vt, vf = split(tm)
    o = [band(ax, T_LOAD, T_PUSH)]
    o += axes(s, ax, [(v, f"{v:g}") for v in (0, 0.05, 0.1, 0.15, 0.2, 0.25)], [(v, mn(v, "{:.1f}")) for v in (-0.5, 0, 0.5, 1.0, 1.5)],
              "time (s)", "shortening velocity (ℓ₀/s)")
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["rule"], "leader"))
    o.append(H.label(s, ax.X(tm), ax.top + 16, "push-off", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, ax.X(0.075), ax.Y(0.88), "loading: the fibre shortens and", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(0.075), ax.Y(0.88) + 16, "stretches the tendon (stores energy)", "label2", I["primary"], "middle"))
    o.append(curve(s, ax, ts, [v[2] for v in V], SER[0]))
    o.append(curve(s, ax, ts, [v[1] for v in V], SER[1]))
    o.append(curve(s, ax, ts, [v[0] for v in V], I["primary"], "curve_multi", DASH_SER))
    o.append(H.label(s, ax.X(0.075), ax.Y(0) + 18, f"whole unit isometric, L̇{sub('MTU', s)} = 0", "label2", I["secondary"], "middle"))
    for y, col in ((vm, I["primary"]), (vt, SER[1]), (vf, SER[0])):
        o.append(dot(s, ax.X(tm), ax.Y(y), col))
    o.append(H.label(s, ax.X(0.167), ax.Y(vm) + 4, f"L̇{sub('MTU', s)} = {vm:.2f}", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(0.165), ax.Y(vt) + 8, f"tendon ẋ = {vt:.2f}", "label2", I["primary"], "end"))
    o.append(lead(s, ax.X(tm), ax.Y(vf) + 6, ax.X(tm), ax.Y(-0.12) - 12, SER[0]))
    o.append(H.label(s, ax.X(tm), ax.Y(-0.12), f"fibre ℓ̇ = {vf:.2f}", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(tm), ax.Y(-0.12) + 16, f"recoil = {vt / vf:.0f} × fibre", "label2", I["secondary"], "middle"))
    o += legend(s, ax.x0, 30, [(I["primary"], DASH_SER, "whole unit L̇MTU (joint)".replace("MTU", sub("MTU", s))),
                               (SER[1], None, "tendon ẋ"), (SER[0], None, "fibre ℓ̇")])
    aria = ("Prescribed shortening velocities of a muscle-tendon unit through a stance phase, split by Eq. 4.4 with zero "
            "pennation. During loading, 0 to 0.15 s, the whole unit is isometric: the fibre (red) shortens at up to 0.54 "
            "optimal lengths per second while the tendon (blue) lengthens at the same rate, storing energy. During the shaded "
            f"push-off, 0.15 to 0.22 s, the whole-unit velocity (black dashed) peaks at {vm:.2f}; the tendon recoils at "
            f"{vt:.2f} and the fibre shortens at only {vf:.2f}, a 6 to 1 split. The tendon recoils exactly the stretch it "
            "stored.")
    hv = hover(ax, [ax.X(t) for t in ts], [[ax.Y(v[0]), ax.Y(v[1]), ax.Y(v[2])] for v in V],
               [f"t = {t:.3f} s: whole unit {v[0]:.2f}, tendon {v[1]:.2f}, fibre {v[2]:.2f} ℓ0/s" for t, v in zip(ts, V)])
    return svg(VB, aria, s, o, hv)


# ================================================================ SLS (Prop. 7), the illustrative E_inst = 1.8 E_R
R_SLS, TS, TE = 1.8, 0.05, 0.09           # E_inst/E_R (line 596), tau_sigma, tau_eps = tau_sigma x 1.8 (s; Lab 1)


def creep(t):
    """eps / (sigma0 / E_R) after a stress step at t = 0 (line 529)."""
    return 0.0 if t < 0 else 1 / R_SLS + (1 - 1 / R_SLS) * (1 - math.exp(-t / TE))


def relax(t):
    """sigma / (E_R eps0) after a strain step at t = 0 (line 528)."""
    return 0.0 if t < 0 else 1 + (R_SLS - 1) * math.exp(-t / TS)


# ================================================================ svg #13: creep and relaxation (Fig. 10)
def fig13():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    L = Ax((80, 116, 355, 316), (-0.05, 0.45), (0, 1.2))
    R = Ax((460, 116, 735, 316), (-0.05, 0.45), (0, 2.0))
    ts = [-0.05, -1e-9] + [i * 0.005 for i in range(91)]
    xt = [(v, f"{v:g}") for v in (0, 0.1, 0.2, 0.3, 0.4)]
    o = []
    o += axes(s, L, xt, [(v, f"{v:g}") for v in (0, 0.5, 1)], "time (s)", f"strain ε / (σ₀/E{H.sub('R', s)})", ylab_x=L.x0 - 50)
    o += axes(s, R, xt, [(v, f"{v:g}") for v in (0, 0.5, 1, 1.5, 2)], "time (s)", f"stress σ / (E{H.sub('R', s)}ε₀)",
              ylab_x=R.x0 - 50)
    for ax, title, held, fn, col in ((L, "Creep: hold the stress", "input: σ = σ₀ held from t = 0", creep, SER[0]),
                                     (R, "Stress relaxation: hold the strain", "input: ε = ε₀ held from t = 0", relax, SER[1])):
        o.append(H.label(s, (ax.x0 + ax.x1) / 2, 26, title, "label", I["primary"], "middle"))
        yh, yl = 56, 84
        o.append(H.line(s, ax.x0, yl, ax.X(0), yl, I["secondary"], "ref"))
        o.append(H.line(s, ax.X(0), yl, ax.X(0), yh, I["secondary"], "ref"))
        o.append(H.line(s, ax.X(0), yh, ax.x1, yh, I["secondary"], "ref"))
        o.append(H.label(s, ax.X(0) + 8, yl - 6, held, "label2", I["secondary"]))
        o.append(curve(s, ax, ts, [fn(t) for t in ts], col))
    # creep marks
    o.append(H.line(s, L.x0, L.Y(1), L.x1, L.Y(1), I["rule"], "ref", H.DASH_REF))
    o.append(H.label(s, L.x1 - 4, L.Y(1) - 8, "plateau σ₀/E" + sub("R", s), "label2", I["secondary"], "end"))
    o.append(dot(s, L.X(0), L.Y(creep(0)), O["flag"]))
    o.append(H.label(s, L.X(0) + 10, L.Y(creep(0)) + 18, f"instant jump σ₀/E{sub('inst', s)} = {creep(0):.2f}", "label2", I["primary"]))
    o.append(dot(s, L.X(TE), L.Y(creep(TE)), O["flag"]))
    o.append(H.label(s, L.X(TE) + 10, L.Y(creep(TE)) + 18, f"t = τ{sub('ε', s)} = {1000 * TE:.0f} ms: {creep(TE):.2f}", "label2",
                     I["primary"]))
    # relaxation marks
    o.append(H.line(s, R.x0, R.Y(1), R.x1, R.Y(1), I["rule"], "ref", H.DASH_REF))
    o.append(H.label(s, R.x1 - 4, R.Y(1) + 18, "plateau E" + sub("R", s) + "ε₀", "label2", I["secondary"], "end"))
    o.append(dot(s, R.X(0), R.Y(relax(0)), O["flag"]))
    o.append(H.label(s, R.X(0) + 10, R.Y(relax(0)) - 2, f"instant jump E{sub('inst', s)}ε₀ = {relax(0):.1f}", "label2", I["primary"]))
    o.append(dot(s, R.X(TS), R.Y(relax(TS)), O["flag"]))
    o.append(H.label(s, R.X(TS) + 10, R.Y(relax(TS)) - 8, f"t = τ{sub('σ', s)} = {1000 * TS:.0f} ms: {relax(TS):.2f}", "label2",
                     I["primary"]))
    aria = ("Creep and stress relaxation of the standard linear solid of Proposition 7, with an instantaneous modulus 1.8 "
            "times the relaxed one, relaxation time 50 ms and creep time 90 ms. Left, creep: a stress step is held from time "
            f"zero; the strain jumps at once to {creep(0):.2f} of its relaxed value, then creeps up, reaching {creep(TE):.2f} "
            "at 90 ms and the plateau 1 later. Right, relaxation: a strain step is held; the stress jumps to 1.8 times its "
            f"relaxed value, then decays, at {relax(TS):.2f} after 50 ms, toward the nonzero plateau 1.")
    hc = [i * 0.0025 for i in range(181)]
    hv = H.hover_attr([(L.box, [[L.X(t), L.Y(creep(t)), f"t = {1000 * t:.0f} ms: ε = {creep(t):.3f} σ0/ER"] for t in hc]),
                       (R.box, [[R.X(t), R.Y(relax(t)), f"t = {1000 * t:.0f} ms: σ = {relax(t):.3f} ER ε0"] for t in hc])])
    return svg(VB, aria, s, o, hv)


# ================================================================ SLS steady cycle (Prop. 9, Eq. 7.3)
def estar(x):
    """E*/E_R at x = omega tau_sigma: (|E*|, delta)."""
    z = complex(1, x * R_SLS) / complex(1, x)
    return abs(z), math.atan2(z.imag, z.real)


def tan_d(x):
    return x * (R_SLS - 1) / (1 + x * x * R_SLS)


RATES = [(0.1, SER[1], "slow"), (1 / math.sqrt(R_SLS), SER[0], "intermediate"), (10.0, SER[2], "fast")]


def loop(x, n=121):
    """eps = (eps0/2)(1 - cos wt), steady sigma; normalised by eps0 and E_R eps0."""
    m, d = estar(x)
    ph = [2 * math.pi * i / (n - 1) for i in range(n)]
    return [(0.5 * (1 - math.cos(p)), 0.5 - 0.5 * m * math.cos(p + d)) for p in ph]


def w_d(x):
    """Loop area / (E_R eps0^2) = pi |E*| (1/2)^2 sin(delta), Eq. 7.2 with amplitude eps0/2."""
    m, d = estar(x)
    return math.pi * m * 0.25 * math.sin(d)


# ================================================================ svg #18: hysteresis loops (Fig. 15)
def fig18():
    VB = (0, 0, 760, 420)
    s = H.Scale(VB[2], VB[3])
    p = "m6f18_"
    ax = Ax((90, 30, 470, 350), (0, 1.0), (-0.5, 1.5))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, ax, [(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1)], [(v, mn(v, "{:g}")) for v in (-0.5, 0, 0.5, 1, 1.5)],
              "strain ε / ε₀", f"stress σ / (E{H.sub('R', s)}ε₀)")
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["rule"], "leader"))
    xm = RATES[1][0]
    lm = loop(xm)
    o.append(f'<polygon points="{pts_str([(ax.X(a), ax.Y(b)) for a, b in lm])}" fill="{SER[0]}" opacity="0.13"/>')
    for x, col, _ in RATES:
        o.append(curve(s, ax, *zip(*loop(x)), col, "curve_multi"))
    # traversal on the intermediate loop: loading branch above (phase 0 -> pi), unloading below
    for k0, k1 in ((26, 35), (86, 95)):
        (a0, b0), (a1, b1) = lm[k0], lm[k1]
        dx, dy = ax.X(a1) - ax.X(a0), ax.Y(b1) - ax.Y(b0)
        nx, ny = -dy / math.hypot(dx, dy), dx / math.hypot(dx, dy)
        off = -16
        x0_, y0_, x1_, y1_ = ax.X(a0) + nx * off, ax.Y(b0) + ny * off, ax.X(a1) + nx * off, ax.Y(b1) + ny * off
        o.append(H.arrow(s, p, x0_, y0_, x1_, y1_, "dim"))
        if k0 < 60:
            o.append(H.label(s, x0_ - 6, y0_ - 4, "loading", "label2", I["primary"], "end"))
        else:
            o.append(H.label(s, x0_ + 8, y0_ + 14, "unloading", "label2", I["primary"]))
    o.append(H.line(s, ax.X(0.29), ax.Y(-0.30) - 4, ax.X(0.025), ax.Y(-0.385), I["rule"], "leader"))
    o.append(H.label(s, ax.X(0.30), ax.Y(-0.30), "dip below σ = 0 on unloading:", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(0.30), ax.Y(-0.30) + 16, "the linear model’s viscous push", "label2", I["secondary"]))
    # right-hand key: rate, modulus regime, loop area
    kx, ky = 500, 70
    o.append(H.label(s, kx, ky - 30, f"loop area W{sub('d', s)} per cycle (shaded:", "label2", I["primary"]))
    o.append(H.label(s, kx, ky - 14, "the intermediate loop), in E" + sub("R", s) + "ε₀²", "label2", I["primary"]))
    notes = {"slow": "near E" + sub("R", s) + ", relaxed", "intermediate": "at the loss peak", "fast": "near E" + sub("inst", s) + " = 1.8 E" + sub("R", s)}
    for k, (x, col, name) in enumerate(RATES):
        y = ky + 22 + 52 * k
        o += legend(s, kx, y, [(col, None, f"{name}, ωτ{sub('σ', s)} = {x:.3g}")])
        o.append(H.label(s, kx + 31, y + 17, f"W{sub('d', s)} = {w_d(x):.3f}, tan δ = {tan_d(x):.2f}", "label2", I["secondary"]))
        o.append(H.label(s, kx + 31, y + 33, notes[name], "label2", I["muted"]))
    aria = ("Steady-state stress-strain loops of the standard linear solid with an instantaneous modulus 1.8 times the "
            "relaxed one, strain cycled from 0 to its peak, at three loading rates. Slow (blue, omega tau 0.1) gives a thin "
            "loop along the relaxed modulus; fast (orange, omega tau 10) a thin loop along the stiffer instantaneous modulus; "
            f"the intermediate rate at the loss peak (red, omega tau {xm:.3f}) the fattest loop, shaded, area "
            f"{w_d(xm):.3f} against {w_d(0.1):.3f} and {w_d(10):.3f}. Loading runs along the upper branch, unloading along "
            "the lower; the faster loops dip below zero stress on unloading.")
    he = [i / 100 for i in range(101)]

    def branches(x):
        lp = loop(x, 2001)
        up, dn = lp[:1001], lp[1000:][::-1]
        return [np.interp(he, [a for a, _ in up], [b for _, b in up]), np.interp(he, [a for a, _ in dn], [b for _, b in dn])]
    br = [branches(x) for x, _, _ in RATES]
    hv = hover(ax, [ax.X(e) for e in he], [[ax.Y(b[j][i]) for b in br for j in (0, 1)] for i in range(len(he))],
               [f"ε/ε0 = {e:.2f}: " + ", ".join(f"{n} {b[0][i]:.2f}/{b[1][i]:.2f}" for (_, _, n), b in zip(RATES, br))
                + " (load/unload)" for i, e in enumerate(he)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #19: loss factor (Fig. 16)
def fig19():
    VB = (0, 0, 760, 390)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 40, 735, 310), (0.01, 100), (0, 0.4), xlog=True)
    xs = [10 ** (-2 + 4 * i / 110) for i in range(111)]
    xp = 1 / math.sqrt(R_SLS)
    o = [band(ax, 8, 90)]
    o += axes(s, ax, [(v, t) for v, t in ((0.01, "0.01"), (0.1, "0.1"), (1, "1"), (10, "10"), (100, "100"))],
              [(v, f"{v:.1f}") for v in (0, 0.1, 0.2, 0.3)], "loading frequency ωτ" + H.sub("σ", s) + " (log scale)",
              "loss factor tan δ")
    o.append(H.label(s, ax.X(27), ax.top + 18, "gait, slow modes", "label2", I["primary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, ax.X(27), ax.top + 34, f"(τ{sub('σ', s)} ≳ 1 s):", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.X(27), ax.top + 50, "ωτ" + sub("σ", s) + " ≈ 8–90", "label2", I["secondary"], "middle"))
    o.append(H.line(s, ax.X(xp), ax.Y(tan_d(xp)), ax.X(xp), ax.y0, I["rule"], "leader", H.DASH_REF))
    o.append(curve(s, ax, xs, [tan_d(x) for x in xs], SER[0]))
    o.append(dot(s, ax.X(xp), ax.Y(tan_d(xp)), O["flag"]))
    o.append(H.label(s, ax.X(xp), ax.Y(tan_d(xp)) - 28, f"peak tan δ = {tan_d(xp):.2f} at ωτ{sub('σ', s)} = {xp:.3f},",
                     "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(xp), ax.Y(tan_d(xp)) - 12, f"that is ω = ω* = 1/√(τ{sub('σ', s)}τ{sub('ε', s)})", "label2",
                     I["secondary"], "middle"))
    o.append(H.line(s, ax.X(0.8) + 2, ax.Y(tan_d(0.8)) + 3, ax.X(2.2), ax.Y(0.235) - 12, I["rule"], "leader"))
    o.append(H.label(s, ax.X(2.2), ax.Y(0.235), f"lab fast mode τ{sub('σ', s)} = 0.05 s at a", "label2", I["primary"]))
    o.append(H.label(s, ax.X(2.2), ax.Y(0.235) + 16, "few-hertz gait: ωτ" + sub("σ", s) + " ≈ 0.8, on the peak", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.012), ax.Y(0.13), "slow: elastic at E" + sub("R", s), "label2", I["primary"]))
    o.append(H.label(s, ax.X(9.0), ax.Y(0.13), "fast: elastic", "label2", I["primary"]))
    o.append(H.label(s, ax.X(9.0), ax.Y(0.13) + 16, "at E" + sub("inst", s) + " = 1.8 E" + sub("R", s), "label2", I["secondary"]))
    aria = ("Loss factor tan delta of the standard linear solid, Eq. 7.3, against the dimensionless loading frequency "
            "omega tau-sigma on a log axis from 0.01 to 100, for an instantaneous modulus 1.8 times the relaxed one. It is "
            f"near zero at both ends and peaks at {tan_d(xp):.2f} at omega tau-sigma = {xp:.3f}. The lab's fast mode at a "
            "few-hertz gait sits at about 0.8, on the peak; the shaded band from 8 to 90 is gait for slow modes of order a "
            "second, where the loss is small.")
    hx = [10 ** (-2 + 4 * i / 200) for i in range(201)]
    hv = hover(ax, [ax.X(x) for x in hx], [ax.Y(tan_d(x)) for x in hx], [f"ωτσ = {x:.3g}: tan δ = {tan_d(x):.3f}" for x in hx])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #20: one-sided restoring torque (Fig. 17)
TH_LO, TH_HI, P_TOE = 0.0, 140.0, 2      # free range (deg); Lab 3's toe exponent


def torque(th):
    """Eq. 8.1 with Lab 3's power-law toe, T = R k (theta - theta_hi)^2; scaled so T(theta_hi + 25 deg) = 1."""
    if th > TH_HI:
        return ((th - TH_HI) / 25) ** P_TOE
    if th < TH_LO:
        return -((TH_LO - th) / 25) ** P_TOE
    return 0.0


def fig20():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 40, 735, 320), (-25, 165), (-1.1, 1.1))
    ths = [-25 + 1.0 * i for i in range(191)]
    o = [band(ax, TH_LO, TH_HI)]
    o += axes(s, ax, [(v, f"{v:.0f}°".replace("-", "−")) for v in (-20, 0, 40, 80, 120, 140, 160)], [], "joint angle θ",
              "restoring torque T", grid=False, ylab_x=ax.x0 - 30)
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["axis"], "axis"))
    for th in (TH_LO, TH_HI):
        o.append(H.line(s, ax.X(th), ax.y0, ax.X(th), ax.top, I["rule"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(70), ax.Y(0.40), "free range: ligaments slack, T = 0", "label", I["primary"], "middle"))
    o.append(H.label(s, ax.X(70), ax.Y(0.40) + 18, f"θ{sub('lo', s)} = 0° to θ{sub('hi', s)} = 140°", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.X(70), ax.Y(-0.45), "dashed: Module 3’s rigid wall,", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.X(70), ax.Y(-0.45) + 16, "an infinitely stiff stop that stores nothing", "label2", I["secondary"], "middle"))
    shade = [th for th in ths if TH_HI <= th <= 157]
    o.append(area([(ax.X(th), ax.Y(torque(th))) for th in shade], ax.Y(0)))
    o.append(curve(s, ax, ths, [torque(th) for th in ths], SER[0]))
    o.append(H.label(s, ax.X(139), ax.Y(0.92), "over-flexion:", "label2", I["primary"], "end", 'font-style="italic"'))
    o.append(H.label(s, ax.X(139), ax.Y(0.92) + 16, f"T = R F{sub('lig', s)}(R(θ − θ{sub('hi', s)}))", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(139), ax.Y(0.92) + 32, "steep but finite, ∝ (θ − θ" + sub("hi", s) + ")²", "label2", I["secondary"], "end"))
    o.append(H.line(s, ax.X(139) + 4, ax.Y(0.92) + 12, ax.X(159) - 4, ax.Y(torque(159)) + 2, I["rule"], "leader"))
    o.append(H.line(s, ax.X(152), ax.Y(0.08), ax.X(150), ax.Y(-0.18) - 4, I["rule"], "leader"))
    o.append(H.label(s, ax.X(142), ax.Y(-0.18) + 10, "shaded: energy", "label2", I["primary"]))
    o.append(H.label(s, ax.X(142), ax.Y(-0.18) + 26, "stored, ∫T dθ", "label2", I["primary"]))
    o.append(H.label(s, ax.X(1), ax.Y(-0.80), "hyper-extension", "label2", I["primary"], extra='font-style="italic"'))
    o.append(H.label(s, ax.X(1), ax.Y(-0.80) + 16, "(mirror at θ" + sub("lo", s) + ")", "label2", I["secondary"]))
    aria = ("Restoring torque of a joint against its angle, Lemma 1 with the parabolic toe of Lab 3. Across the shaded free "
            "range from 0 to 140 degrees the ligaments are slack and the torque is zero. Past 140 degrees (over-flexion) and "
            "below 0 (hyper-extension) a ligament engages and the torque grows with the square of the angle past the limit, "
            "starting with zero value and zero slope: a steep but finite one-sided spring, not the rigid walls of Module 3 "
            "(dashed). The area under the over-flexion branch is the energy stored at end-range.")
    hv = hover(ax, [ax.X(th) for th in ths[::2]], [ax.Y(torque(th)) for th in ths[::2]],
               [f"θ = {th:.0f}°: " + ("slack, T = 0" if torque(th) == 0 else f"T = {torque(th):.2f} (scale: 1 at 25° past the limit)")
                for th in ths[::2]])
    return svg(VB, aria, s, o, hv)


# ================================================================ Lab 1 (its code, unchanged)
@lru_cache(maxsize=None)
def lab1():
    kR, kinst = 2.0e5, 3.6e5
    ts, te = 0.05, 0.09
    m, x0 = 1.0, 0.020

    def recoil(sls):
        dt = 2e-5
        x, v, F = x0, 0.0, kinst * x0
        Tm = np.arange(0, 0.08, dt)
        X = np.empty_like(Tm)
        for i in range(len(Tm)):
            X[i] = x
            F = F + dt * (kR * (x + te * v) - F) / ts if sls else kR * x
            v += (-F / m) * dt
            x += v * dt
        return Tm, X
    Tm, Xe = recoil(False)
    _, Xs = recoil(True)
    pk = [i for i in range(1, len(Xs) - 1) if Xs[i] > Xs[i - 1] and Xs[i] >= Xs[i + 1] and Xs[i] > 0.004]
    return Tm, Xe, Xs, pk


def fig25():
    VB = (0, 0, 760, 370)
    s = H.Scale(VB[2], VB[3])
    Tm, Xe, Xs, pk = lab1()
    ax = Ax((80, 50, 735, 290), (0, 80), (-22, 30))
    sel = list(range(0, len(Tm), 40)) + [len(Tm) - 1]
    o = axes(s, ax, [(v, f"{v}") for v in range(0, 81, 10)], [(v, mn(v, "{:.0f}")) for v in (-20, -10, 0, 10, 20)],
             "time (ms)", "stretch x (mm)")
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["rule"], "leader"))
    o.append(curve(s, ax, [1e3 * Tm[k] for k in sel], [1e3 * Xe[k] for k in sel], SER[1], "curve_multi"))
    o.append(curve(s, ax, [1e3 * Tm[k] for k in sel], [1e3 * Xs[k] for k in sel], SER[0], "curve_multi"))
    for i in pk:
        o.append(dot(s, ax.X(1e3 * Tm[i]), ax.Y(1e3 * Xs[i]), SER[0], r=3.5))
    p1, p2 = 1e3 * Xs[pk[0]], 1e3 * Xs[pk[1]]
    res = (p2 / p1) ** 2
    for i, dy in ((pk[0], -9), (pk[1], -9)):
        o.append(H.label(s, ax.X(1e3 * Tm[i]), ax.Y(1e3 * Xs[i]) + dy, f"{1e3 * Xs[i]:.2f}", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(28), ax.Y(26.5), f"resilience per cycle = (peak 2 / peak 1)² = ({p2:.2f}/{p1:.2f})² = {res:.3f}",
                     "label2", I["primary"]))
    pke = [i for i in range(1, len(Xe) - 1) if Xe[i] > Xe[i - 1] and Xe[i] >= Xe[i + 1]]
    pe = 1e3 * (Tm[pke[1]] - Tm[pke[0]])
    o += legend(s, ax.x0, 26, [(SER[1], None, f"elastic: peaks stay at 20.0 mm, period {pe:.1f} ms"),
                               (SER[0], None, f"viscoelastic (SLS): period {1e3 * (Tm[pk[1]] - Tm[pk[0]]):.1f} ms, damped")])
    aria = ("Lab 1, tendon recoil, from the lab's code: the stretch of a tendon released from 20 mm with a 1 kg mass, over 80 ms. "
            f"The elastic tendon (blue) oscillates undamped with period {pe:.1f} ms, every peak at 20.0 mm. The viscoelastic "
            f"standard-linear-solid tendon (red) oscillates faster, period {1e3 * (Tm[pk[1]] - Tm[pk[0]]):.1f} ms, and its peaks "
            f"fall from {p1:.2f} to {p2:.2f} mm and on to {1e3 * Xs[pk[-1]]:.2f} mm at {1e3 * Tm[pk[-1]]:.0f} ms: a resilience "
            f"per cycle of ({p2:.2f}/{p1:.2f}) squared = {res:.3f}.")
    hk = list(range(0, len(Tm), 25))
    hv = hover(ax, [ax.X(1e3 * Tm[k]) for k in hk], [[ax.Y(1e3 * Xe[k]), ax.Y(1e3 * Xs[k])] for k in hk],
               [f"t = {1e3 * Tm[k]:.1f} ms: elastic {1e3 * Xe[k]:.1f} mm, SLS {1e3 * Xs[k]:.1f} mm" for k in hk])
    return svg(VB, aria, s, o, hv)


# ================================================================ Lab 2 (its code, unchanged)
@lru_cache(maxsize=None)
def lab2():
    M, g = 80.0, 9.81
    kT = 1.7e4
    Fmax = 2600.0
    l0 = 0.055
    vmax = 8 * l0
    a = 1.0

    def fL(x):
        return np.exp(-((x / l0 - 1) / 0.45) ** 2)

    def fVinv(fv):
        fv = min(max(fv, 0.0), 1.5)
        vn = (1 - fv) / (1 + fv / 0.25)
        return min(max(vn, -0.4), 1.0) * vmax
    dt = 2e-5
    s, sd, l, t = 0.0, 1.35, l0, 0.0
    V, tt = [], []
    while True:
        xT = s - (l0 - l)
        F = kT * max(xT, 0.0)
        vfib = fVinv(F / (a * Fmax * fL(l)) if F > 0 else 0.0)
        V.append((-sd, vfib, -sd - vfib))
        tt.append(t)
        if t > 0.02 and (s <= 0 or F <= 0):
            break
        sd += (g - F / M) * dt
        s += sd * dt
        l -= vfib * dt
        t += dt
    return np.array(tt), np.array(V)


def fig27():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    tt, V = lab2()
    tm = 1e3 * tt
    ax = Ax((80, 50, 735, 320), (0, 290), (-2.0, 2.0))
    i0 = int(np.where(V[:, 0] >= 0)[0][0])                  # whole unit stops lengthening: loading ends
    ir, iff = int(V[:, 2].argmax()), int(np.abs(V[:, 1]).argmax())
    rec, fib = V[ir, 2], abs(V[iff, 1])
    sel = sorted(set(list(range(0, len(tt), 100)) + [len(tt) - 1]))
    o = [band(ax, 0, tm[i0])]
    o += axes(s, ax, [(v, f"{v}") for v in range(0, 281, 40)], [(v, mn(v, "{:.0f}")) for v in (-2, -1, 0, 1, 2)],
              "time after touchdown (ms)", "shortening speed (m/s)")
    o.append(H.line(s, ax.x0, ax.Y(0), ax.x1, ax.Y(0), I["rule"], "leader"))
    o.append(H.label(s, ax.X(tm[i0] / 2), ax.top + 18, f"loading, 0–{tm[i0]:.0f} ms", "label2", I["primary"], "middle",
                     'font-style="italic"'))
    o.append(H.label(s, ax.X((tm[i0] + tm[-1]) / 2), ax.Y(-1.75), f"push-off, {tm[i0]:.0f}–{tm[-1]:.0f} ms", "label2",
                     I["primary"], "middle", 'font-style="italic"'))
    o.append(curve(s, ax, [tm[k] for k in sel], [V[k, 1] for k in sel], SER[0]))
    o.append(curve(s, ax, [tm[k] for k in sel], [V[k, 2] for k in sel], SER[1]))
    o.append(curve(s, ax, [tm[k] for k in sel], [V[k, 0] for k in sel], I["primary"], "curve_multi", DASH_SER))
    o.append(dot(s, ax.X(tm[ir]), ax.Y(rec), SER[1]))
    o.append(H.label(s, ax.X(tm[ir]) - 8, ax.Y(rec) - 26, f"spring recoil peak {rec:.2f} m/s at {tm[ir]:.0f} ms", "label2",
                     I["primary"], "end"))
    o.append(dot(s, ax.X(tm[ir]), ax.Y(V[ir, 1]), SER[0]))
    o.append(H.label(s, ax.X(tm[ir]) - 8, ax.Y(V[ir, 1]) + 20, f"fibre there: {V[ir, 1]:.2f} m/s", "label2", I["primary"], "end"))
    o.append(dot(s, ax.X(tm[iff]), ax.Y(V[iff, 1]), SER[0]))
    o.append(dot(s, ax.X(tm[-1]), ax.Y(V[-1, 1]), SER[0]))
    o.append(H.label(s, ax.X(12), ax.Y(V[iff, 1]) - 22, f"fibre peak {fib:.2f} m/s = v{sub('max', s)} at touchdown and take-off,",
                     "label2", I["primary"]))
    o.append(H.label(s, ax.X(12), ax.Y(V[iff, 1]) - 6, f"where the leg force is near zero; {rec:.2f}/{fib:.2f} = {rec / fib:.1f}×",
                     "label2", I["secondary"]))
    o += legend(s, ax.x0, 30, [(I["primary"], DASH_SER, "whole unit L̇" + sub("MTU", s)), (SER[1], None, "leg-spring recoil"),
                               (SER[0], None, "fibre")])
    aria = ("Lab 2, a hop on a muscle-tendon leg spring, from the lab's code: shortening speeds over the stance phase. During "
            f"the shaded loading, 0 to {tm[i0]:.0f} ms, the whole unit (black dashed) and the leg spring (blue) lengthen while "
            f"the fibre (red) shortens, slowing from {fib:.2f} m/s at touchdown to near zero. At push-off the spring recoil "
            f"tracks the whole unit and peaks at {rec:.2f} m/s at {tm[ir]:.0f} ms, when the fibre shortens at {V[ir, 1]:.2f} "
            f"m/s; the fibre's own peak, {fib:.2f} m/s, comes at touchdown and take-off where the force is near zero. Peak "
            f"against peak the spring is {rec / fib:.1f} times faster.")
    hk = list(range(0, len(tt), 125))
    hv = hover(ax, [ax.X(tm[k]) for k in hk], [[ax.Y(V[k, 0]), ax.Y(V[k, 2]), ax.Y(V[k, 1])] for k in hk],
               [f"t = {tm[k]:.0f} ms: whole unit {V[k, 0]:.2f}, spring {V[k, 2]:.2f}, fibre {V[k, 1]:.2f} m/s" for k in hk])
    return svg(VB, aria, s, o, hv)


# ================================================================ Lab 3 (its code, unchanged)
SLACKS = [(0, SER[0], "normal"), (8, SER[1], "lax +8°"), (16, SER[2], "very lax +16°")]


@lru_cache(maxsize=None)
def lab3(slack_deg):
    Ii, R, k, p = 0.20, 0.03, 4.5e6, 2
    th_hi = np.radians(140 + slack_deg)
    dt = 1e-4
    th, w = np.radians(110), np.radians(650)
    tr, w_hit = [], None
    for _ in range(3000):
        tr.append(np.degrees(th))
        over = th - th_hi
        if over > 0 and w_hit is None:
            w_hit = float(np.degrees(w))                       # angular velocity when the ligament engages
        T_ = R * k * over ** p if over > 0 else 0.0
        w += (-T_ / Ii) * dt
        th += w * dt
    tr = np.array(tr)
    return tr, float(tr.max()) - 140, w_hit


def fig29():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 50, 735, 320), (0, 200), (100, 170))
    tms = np.arange(3000) * 0.1
    o = [f'<rect x="{ax.x0:.2f}" y="{ax.top:.2f}" width="{ax.x1 - ax.x0:.2f}" height="{ax.Y(140) - ax.top:.2f}" fill="{BOXFILL}"/>']
    o += axes(s, ax, [(v, f"{v}") for v in range(0, 201, 25)], [(v, f"{v}") for v in range(100, 171, 10)],
              "time (ms)", "joint angle θ (°)")
    o.append(H.label(s, ax.X(198), ax.Y(140) - 8, "past the 140° normal limit (shaded)", "label2", I["secondary"], "end"))
    ldt, lth = 8, 103                                            # name labels: 8 ms right of each line at 103 deg
    for sl, col, name in SLACKS:
        tr, ov, _ = lab3(sl)
        keep = [i for i in range(0, 2001, 20) if tr[i] >= 100]
        o.append(curve(s, ax, [tms[i] for i in keep], [tr[i] for i in keep], col, "curve_multi"))
        if sl:
            o.append(H.line(s, ax.X(100), ax.Y(140 + sl), ax.x1, ax.Y(140 + sl), col, "leader", H.DASH_REF))
            o.append(H.label(s, ax.X(198), ax.Y(140 + sl) - 5, f"{name}: engages at {140 + sl}°", "label2", I["secondary"], "end"))
        ip = int(tr.argmax())
        o.append(dot(s, ax.X(tms[ip]), ax.Y(tr[ip]), col))
        o.append(H.label(s, ax.X(tms[ip] - 4), ax.Y(tr[ip] + 3.2), f"+{ov:.1f}°", "label2", I["primary"], "end"))
        td = tms[ip] + (tr[ip] - lth) / 0.65                     # descending branch reaches lth here
        o.append(H.label(s, ax.X(td + ldt), ax.Y(lth), name, "label2", I["primary"]))
    w_eng = [lab3(sl)[2] for sl, _, _ in SLACKS]
    o.append(H.label(s, ax.X(12), ax.Y(109), f"each ligament stops the limb {lab3(0)[1]:.1f}° past its own", "label2", I["primary"]))
    o.append(H.label(s, ax.X(12), ax.Y(109) + 16, "engagement angle: no torque acts in the free range,", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(12), ax.Y(109) + 32, f"so the limb reaches each one at the same {w_eng[0]:.0f}°/s", "label2",
                     I["secondary"]))
    o.append(H.label(s, ax.X(12), ax.Y(166), "peaks: degrees past 140°", "label2", I["secondary"]))
    o += legend(s, ax.x0, 30, [(c, None, n) for _, c, n in SLACKS])
    ovs = [lab3(sl)[1] for sl, _, _ in SLACKS]
    aria = ("Lab 3, a limb rotating at 650 degrees per second from 110 degrees toward over-flexion, from the lab's code: joint "
            "angle against time for a normal ligament engaging at 140 degrees and two laxer ones engaging at 148 and 156. "
            f"Each rises at the same constant rate, rebounds off its ligament and swings back. The peaks are {ovs[0]:.1f}, "
            f"{ovs[1]:.1f} and {ovs[2]:.1f} degrees past the 140 degree limit (shaded above): each ligament stops the limb "
            f"{ovs[0]:.1f} degrees past its own engagement angle.")
    hk = list(range(0, 2001, 20))
    trs = [lab3(sl)[0] for sl, _, _ in SLACKS]
    hv = hover(ax, [ax.X(tms[i]) for i in hk], [[ax.Y(min(max(tr[i], 100), 170)) for tr in trs] for i in hk],
               [f"t = {tms[i]:.0f} ms: " + ", ".join(f"{n} {tr[i]:.1f}°" for (_, _, n), tr in zip(SLACKS, trs)) for i in hk])
    return svg(VB, aria, s, o, hv)


FIGS = {
    5: ("Stress-strain curve of tendon collagen. A red curve rises wit", fig5),
    8: ("Structural force-elongation curve of a tendon. Red: force F i", fig8),
    9: ("Force-elongation curve with the area beneath it shaded: that ", fig9),
    12: ("Shortening-velocity traces of a muscle-tendon unit through lo", fig12),
    13: ("Two canonical viscoelastic tests. Left, creep: a step stress ", fig13),
    18: ("Stress-strain hysteresis loops of the standard linear solid a", fig18),
    19: ("Loss factor tan delta versus loading frequency on a log axis ", fig19),
    20: ("Restoring torque of a joint versus its angle. Across the free", fig20),
    25: ("Tendon recoil: the stretch of a released tendon versus time. ", fig25),
    27: ("A hop on a muscle-tendon leg spring. Shortening speeds over t", fig27),
    29: ("A limb rotating fast toward over-flexion rebounds off the lig", fig29),
}
