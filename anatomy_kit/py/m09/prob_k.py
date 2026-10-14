"""Module 9 computational-problem plots (K1-K11): house-style redraws at 400 px (svg #39-#49).

Every plotted number is computed here from the K solutions of module09.html (lines 528-629) and the four labs
of section 10 (lines 333-428): the SLIP stance of (2.1) by RK4 (K1, K2), the Lab 2 push-off profile (K3-K5),
Proposition 8.1 (K6), Proposition 7.1 (K7), Proposition 9.1 (K8), the Basquin curve of K9, the K10 walking
cost Fr^2/(1 - 0.85 Fr), and the K11 script ported line for line. The numbers the solutions quote are asserted.
"""
import math
from functools import lru_cache

import numpy as np

import house as H
from m05.plots_prob import Plot, hov, label, legend, sub, svg

O, I, SER = H.OVERLAY, H.INK, H.SERIES
W = 400
BOX = "#f7f4ef"
GRID = "#e6e6e6"
trapz = getattr(np, "trapezoid", None) or np.trapz


def dot(P, x, y, col, r=None):
    r = r or P.s(H.PX["dot"])
    return f'<circle cx="{P.X(x):.2f}" cy="{P.Y(y):.2f}" r="{r:.2f}" fill="{col}" stroke="#fff" stroke-width="1.5"/>'


def tk(vals, f="{:g}"):
    return [(v, f.format(v).replace("-", "−")) for v in vals]


def href(s, P, y, col=None):
    return H.line(s, P.x0, P.Y(y), P.x1, P.Y(y), col or I["secondary"], "ref", H.DASH_REF)


def vref(s, P, x, col=None, y_top=None):
    return H.line(s, P.X(x), P.y1 if y_top is None else y_top, P.X(x), P.y0, col or I["secondary"], "ref", H.DASH_REF)


def bisect(f, lo, hi, tol=1e-7):
    flo = f(lo)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


# ================================================================ SLIP stance, (2.1) by RK4 (K1, K2)
M, G, L0 = 70.0, 9.81, 1.0                      # Lab 1 (line 361)
BW = M * G


@lru_cache(maxsize=None)
def stance(k, alpha_deg, vx0=4.0, vy0=-0.7, dt=1e-4):
    """RK4 through one stance, foot at the origin, touchdown at rest length L0 to takeoff (r back to L0,
    the crossing interpolated linearly). Returns (contact time, vx at takeoff, vy at takeoff, peak Fz in N)."""
    a = math.radians(alpha_deg)

    def f(x, y, vx, vy):
        r = math.hypot(x, y)
        F = k * (L0 - r) / (r * M)
        return vx, vy, F * x, F * y - G

    x, y, vx, vy = -L0 * math.cos(a), L0 * math.sin(a), vx0, vy0
    t, fz = 0.0, 0.0
    while True:
        k1 = f(x, y, vx, vy)
        k2 = f(x + dt / 2 * k1[0], y + dt / 2 * k1[1], vx + dt / 2 * k1[2], vy + dt / 2 * k1[3])
        k3 = f(x + dt / 2 * k2[0], y + dt / 2 * k2[1], vx + dt / 2 * k2[2], vy + dt / 2 * k2[3])
        k4 = f(x + dt * k3[0], y + dt * k3[1], vx + dt * k3[2], vy + dt * k3[3])
        n = [x, y, vx, vy]
        n = [n[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(4)]
        r0, r1 = math.hypot(x, y), math.hypot(n[0], n[1])
        t += dt
        if r1 >= L0 and t > 5 * dt:
            w = (L0 - r0) / (r1 - r0)
            return t - dt + w * dt, vx + w * (n[2] - vx), vy + w * (n[3] - vy), fz
        x, y, vx, vy = n
        fz = max(fz, k * (L0 - r1) * y / r1)
        if y <= 0 or t > 2.0:
            return t, vx, vy, fz


def flight_ms(k, alpha=70.0):
    return 2 * stance(k, alpha)[2] / G * 1e3


@lru_cache(maxsize=None)
def k1_data():
    k_fl = bisect(lambda k: stance(k * 1e3, 70.0)[2], 8.0, 15.0)
    ks = np.round(np.linspace(k_fl, 40.0, 117), 4)
    tf = np.array([flight_ms(k * 1e3) for k in ks])
    pk = np.array([stance(k * 1e3, 70.0)[3] / BW for k in ks])
    k_3 = bisect(lambda k: stance(k * 1e3, 70.0)[3] / BW - 3.0, 12.0, 30.0)
    return ks, tf, pk, k_fl, k_3


@lru_cache(maxsize=None)
def k2_data(k=15e3):
    al = np.round(np.linspace(58.0, 80.0, 89), 4)
    asym = np.array([stance(k, a)[2] - 0.7 for a in al])
    root = bisect(lambda a: stance(k, a)[2] - 0.7, 58.0, 80.0)
    tc = stance(k, root)[0]
    return al, asym, root, tc


# ================================================================ Lab 2 push-off (K3, K4, K5)
TP, FPK = 0.30, 2.5                              # Lab 2 (line 376)
TT = np.linspace(0, TP, 400)


def profile(front):
    """Lab 2: same-peak force shape in BW; front < 1 shifts force earlier."""
    return 1.0 + (FPK - 1.0) * np.sin(np.pi * (TT / TP) ** front) ** 1.55


def impulse(front):
    """Net impulse (N s) of the Lab 2 profile."""
    return trapz((profile(front) - 1.0) * M * G, TT)


def height(front):
    v0 = impulse(front) / M
    return v0 * v0 / (2 * G)


# ================================================================ #39 K1: flight time and peak GRF vs stiffness
def fig39():
    VB = (0, 0, W, 444)
    s = H.Scale(W, VB[3], display_w=400)
    ks, tf, pk, k_fl, k_3 = k1_data()
    sweep = {k: flight_ms(k * 1e3) for k in (12, 15, 20, 26, 40, 60)}
    # line 530 quotes 25.4, 93.2, 171.9, 234.5, 319.9 ms; converged RK4 (dt 1e-4 to 1e-5) gives 93.3 and 234.6
    assert all(abs(sweep[k] - v) < 0.15 for k, v in zip((12, 15, 20, 26, 40), (25.4, 93.2, 171.9, 234.5, 319.9))), sweep
    assert round(sweep[60]) == 383 and round(k_fl, 2) == 11.09 and round(k_3, 1) == 19.3, (sweep[60], k_fl, k_3)
    tf3 = flight_ms(k_3 * 1e3)
    assert round(tf3) == 163 and round(stance(12e3, 70)[1], 2) == 4.20 and round(stance(40e3, 70)[1], 2) == 3.60
    A = Plot(s, (62, 52, 388, 182), (10, 40), (0, 350))
    B = Plot(s, (62, 274, 388, 384), (10, 40), (2, 4.5))
    kt = tk((10, 15, 20, 25, 30, 35, 40))
    o = [A.axes(kt, tk((0, 100, 200, 300)), "leg stiffness k (kN/m)", "flight time (ms)", grid=(100, 200, 300))]
    o.append(B.axes(kt, tk((2, 3, 4)), "leg stiffness k (kN/m)", "peak F (BW)", grid=(3, 4)))
    o.append(vref(s, A, k_3, O["flag"]))
    o.append(vref(s, B, k_3, O["flag"]))
    o.append(href(s, B, 3.0))
    o.append(A.curve(ks, tf, SER[0]))
    o.append(B.curve(ks, pk, SER[1]))
    o.append(dot(A, k_fl, 0, SER[0]))
    o.append(dot(A, k_3, tf3, O["flag"]))
    o.append(dot(B, k_3, 3.0, O["flag"]))
    o.append(label(s, A.X(k_3) + 8, A.Y(tf3) + 18, f"{k_3:.1f} kN/m: {tf3:.0f} ms", "label2"))
    o.append(label(s, A.X(39.6), A.Y(70), "no interior maximum:", "label2", I["secondary"], "end"))
    o.append(label(s, A.X(39.6), A.Y(70) + 16, f"{sweep[40]:.0f} ms at 40, still rising", "label2",
                   I["secondary"], "end"))
    o.append(label(s, 62, 34, f"dot at {k_fl:.2f} kN/m: no flight below it (v" + sub("y", s, "label2")
                   + " at takeoff ≤ 0)", "label2", I["secondary"]))
    o.append(label(s, B.X(39.6), B.Y(3.0) + 18, "limit: 3 body weights", "label2", I["secondary"], "end"))
    o.append(label(s, 62, 18, "touchdown α₀ = 70°, v" + sub("x", s, "label2") + " = 4.0, v" + sub("y", s, "label2")
                   + " = −0.7 m/s", "label2", I["secondary"]))
    o.append(label(s, B.X(k_3) + 6, B.y1 + 14, f"{k_3:.1f} kN/m", "label2", I["primary"]))
    aria = (f"Problem K1, two panels against leg stiffness from 10 to 40 kilonewtons per metre at the fixed touchdown "
            f"state alpha 70 degrees, vx 4.0, vy minus 0.7 metres per second. Top: flight time, zero at the no-flight "
            f"bound {k_fl:.2f} kN/m, rising monotonically to {sweep[40]:.0f} ms at 40 with no interior maximum. "
            f"Bottom: peak vertical ground reaction in body weights, rising past the dashed 3 body-weight limit at "
            f"{k_3:.1f} kN/m, where flight time is {tf3:.0f} ms; an orange dashed line marks that stiffness on both panels.")
    pa = hov(A, ks, [tf], lambda i: f"k = {ks[i]:.2f} kN/m: flight {max(tf[i], 0):.0f} ms, peak {pk[i]:.2f} BW")
    pb = hov(B, ks, [pk], lambda i: f"k = {ks[i]:.2f} kN/m: peak {pk[i]:.2f} BW, flight {max(tf[i], 0):.0f} ms")
    return svg(VB, aria, s, "".join(o), ([(A.box, pa), (B.box, pb)],))


# ================================================================ #40 K2: stride asymmetry vs angle of attack
def fig40():
    VB = (0, 0, W, 282)
    s = H.Scale(W, VB[3], display_w=400)
    al, asym, root, tc = k2_data()
    tf = 2 * 0.7 / G
    beta = tc / (2 * (tc + tf))
    assert (round(asym[0], 2), round(asym[-1], 2), round(root, 1)) == (1.37, -1.47, 68.2), (asym[0], asym[-1], root)
    assert (round(tc, 3), round(tf, 3), round(beta, 2)) == (0.192, 0.143, 0.29), (tc, tf, beta)   # line 534
    P = Plot(s, (62, 46, 388, 216), (58, 80), (-1.8, 1.6))
    o = [P.axes(tk((60, 65, 70, 75, 80)), tk((-1, 0, 1)), "angle of attack α₀ (degrees)", "asymmetry (m/s)",
                grid=(-1, 1))]
    o.append(href(s, P, 0.0))
    o.append(P.curve(al, asym, SER[1]))
    o.append(dot(P, 58, asym[0], SER[1]))
    o.append(dot(P, 80, asym[-1], SER[1]))
    o.append(dot(P, root, 0.0, O["flag"]))
    o.append(label(s, P.X(58) + 8, P.Y(asym[0]) - 7, f"+{asym[0]:.2f} at 58°", "label2"))
    o.append(label(s, P.X(80) - 22, P.y0 - 4, f"−{-asym[-1]:.2f} at 80°", "label2", I["primary"], "end"))
    o.append(label(s, P.X(root) + 8, P.Y(0) - 10, f"root α₀ = {root:.1f}°: periodic stride", "label2"))
    o.append(label(s, P.X(58.4), P.Y(-1.0), f"t{sub('c', s, 'label2')} = {tc:.3f} s, t{sub('f', s, 'label2')} = "
                   f"{tf:.3f} s, β = {beta:.2f}", "label2", I["secondary"]))
    o.append(label(s, 62, 22, "asymmetry = v" + sub("y,to", s, "label2") + " − |v" + sub("y,td", s, "label2")
                   + "|,  k = 15 kN/m, v" + sub("x", s, "label2") + " = 4.0 m/s", "label2", I["secondary"]))
    aria = (f"Problem K2 plot: stride asymmetry, the takeoff vertical speed minus the 0.7 metre per second touchdown "
            f"speed, against angle of attack from 58 to 80 degrees at leg stiffness 15 kN/m. The curve falls "
            f"monotonically from plus {asym[0]:.2f} to minus {-asym[-1]:.2f} metres per second and crosses the dashed "
            f"zero line at {root:.1f} degrees, the periodic stride: contact {tc:.3f} s, flight {tf:.3f} s, "
            f"duty factor {beta:.2f}.")
    hv = hov(P, al, [asym], lambda i: f"α₀ = {al[i]:.2f}°: asymmetry {asym[i]:+.3f} m/s")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #41 K3: height error vs mass error
def fig41():
    VB = (0, 0, W, 290)
    s = H.Scale(W, VB[3], display_w=400)
    J = impulse(1.0)
    v0, h0 = J / M, height(1.0)
    e = np.linspace(-5, 5, 201)
    v = (J + M * G * TP) / (M * (1 + e / 100)) - G * TP          # same measured trace, assumed mass m(1 + e)
    dh = ((v / v0) ** 2 - 1) * 100
    slope = -2 * (1 + G * TP / v0)
    assert round(slope, 2) == -4.42 and round(v0, 2) == 2.43 and round(h0 * 100, 2) == 30.04, (slope, v0)   # line 538
    h5 = v[-1] ** 2 / (2 * G) * 100
    assert round(h5, 2) == 24.04 and round(dh[-1], 1) == -20.0, (h5, dh[-1])
    P = Plot(s, (62, 62, 388, 226), (-5, 5), (-25, 30))
    o = [P.axes(tk((-4, -2, 0, 2, 4)), tk((-20, -10, 0, 10, 20, 30)), "body-mass error δm/m (%)",
                "height error δh/h (%)", grid=(-20, -10, 10, 20, 30))]
    o.append(href(s, P, 0.0, I["rule"]))
    o.append(P.curve(e, slope * e, SER[1], multi=True, dash=H.DASH_REF))
    o.append(P.curve(e, dh, SER[0], multi=True))
    o.append(dot(P, 5, dh[-1], SER[0]))
    o.append(dot(P, -5, dh[0], SER[0]))
    o.append(legend(s, 62, 20, [(SER[0], "refit of the same force trace", None),
                                (SER[1], f"slope {slope:.2f}".replace("-", "−"), H.DASH_REF)]))
    o.append(label(s, P.X(-5) + 9, P.Y(dh[0]) - 6, f"+{dh[0]:.1f}%", "label2"))
    o.append(label(s, P.X(-0.8), P.Y(18), f"+5% mass: {h0*100:.2f} → {h5:.2f} cm,", "label2"))
    o.append(label(s, P.X(-0.8), P.Y(18) + 16, f"−{-dh[-1]:.1f}% (dot, right)", "label2"))
    o.append(label(s, P.X(-4.8), P.Y(-12), "force trace fixed (Lab 2, t" + sub("p", s, "label2") + " = 0.30 s);",
                   "label2", I["secondary"]))
    o.append(label(s, P.X(-4.8), P.Y(-12) + 16, "only the assumed mass changes", "label2", I["secondary"]))
    aria = (f"Problem K3 plot: error in the recovered jump height against error in the assumed body mass, from minus 5 "
            f"to plus 5 percent, for one fixed Lab 2 force trace. The red curve, the exact refit, falls through zero "
            f"with slope {slope:.2f}, the dashed blue tangent: plus 5 percent mass lowers the height from {h0*100:.2f} "
            f"to {h5:.2f} cm, minus {-dh[-1]:.1f} percent, and minus 5 percent mass raises it {dh[0]:.1f} percent.")
    hv = hov(P, e, [dh, slope * e], lambda i: f"δm/m = {e[i]:+.2f}%: δh/h = {dh[i]:+.1f}% (tangent {slope*e[i]:+.1f}%)")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #42 K4: push-off shape and jump height
def fig42():
    VB = (0, 0, W, 470)
    s = H.Scale(W, VB[3], display_w=400)
    sweep = {f: height(f) * 100 for f in (1.3, 1.0, 0.8, 0.7, 0.5, 0.3)}
    assert [round(sweep[f], 2) for f in sweep] == [25.95, 30.04, 32.05, 32.38, 30.04, 20.02], sweep   # line 542
    fs = np.round(np.linspace(0.3, 1.3, 201), 4)
    hs = np.array([height(f) * 100 for f in fs])
    fbest, hbest = fs[hs.argmax()], hs.max()
    assert round(fbest, 1) == 0.7 and round(hbest, 1) == 32.4, (fbest, hbest)
    A = Plot(s, (62, 48, 388, 172), (0, 300), (0, 2.9))
    B = Plot(s, (62, 296, 388, 410), (0.3, 1.3), (18, 34))
    tms = TT * 1e3
    o = [A.axes(tk((0, 100, 200, 300)), tk((0, 1, 2)), "time in push-off (ms)", "force (BW)", grid=(2,))]
    o.append(href(s, A, 1.0))
    o.append(href(s, A, 2.5))
    for f, col in ((0.3, SER[2]), (1.0, SER[1]), (0.7, SER[0])):
        o.append(A.curve(tms, profile(f), col, multi=True))
    for f in (0.3, 0.7, 1.0):
        tpk = TP * 0.5 ** (1 / f) * 1e3
        o.append(label(s, A.X(tpk), A.Y(2.5) - 6, f"{f:.1f}", "label2", I["primary"], "middle"))
    o.append(legend(s, 62, 22, [(SER[0], "0.7 (best)", None), (SER[1], "1.0 (symmetric)", None),
                                (SER[2], "0.3", None)]))
    o.append(label(s, A.X(298), A.Y(2.5) - 6, "same peak 2.5 BW", "label2", I["secondary"], "end"))
    o.append(label(s, A.X(298), A.Y(1.0) + 15, "body weight", "label2", I["secondary"], "end"))
    o.append(B.axes(tk((0.3, 0.5, 0.7, 0.9, 1.1, 1.3)), tk((20, 25, 30)), "front-loading exponent (smaller = earlier)",
                    "jump height (cm)", grid=(20, 25, 30)))
    o.append(B.curve(fs, hs, SER[0]))
    o += [dot(B, f, h, SER[0]) for f, h in sweep.items()]
    o.append(dot(B, fbest, hbest, O["flag"]))
    o.append(label(s, B.X(fbest), B.Y(hbest) - 10, f"maximum {hbest:.1f} cm at {fbest:.1f}", "label2", I["primary"],
                   "middle"))
    o.append(label(s, B.X(1.0) - 8, B.Y(sweep[1.0]) + 18, f"symmetric {sweep[1.0]:.1f}", "label2", I["primary"], "end"))
    o.append(label(s, B.X(0.3) + 9, B.Y(sweep[0.3]) + 4, f"{sweep[0.3]:.1f}", "label2"))
    o.append(label(s, 62, 270, "dots: the six profiles of the K4 sweep", "label2",
                   I["secondary"]))
    aria = (f"Problem K4, two panels. Top: three Lab 2 push-off force profiles with the same 2.5 body-weight peak over "
            f"300 ms, front-loading exponent 0.7 (red), 1.0 symmetric (blue) and 0.3 (orange); the smaller the exponent, "
            f"the earlier and narrower the pulse. Bottom: jump height against the exponent from 0.3 to 1.3, an interior "
            f"maximum of {hbest:.1f} cm at {fbest:.1f}, against {sweep[1.0]:.1f} cm symmetric and {sweep[0.3]:.1f} cm "
            f"at 0.3.")
    sub_i = list(range(0, len(TT), 4))
    pa = [[round(A.X(tms[i]), 2), [round(A.Y(profile(f)[i]), 2) for f in (0.7, 1.0, 0.3)],
           f"t = {tms[i]:.0f} ms: F = {profile(0.7)[i]:.2f} / {profile(1.0)[i]:.2f} / {profile(0.3)[i]:.2f} BW"]
          for i in sub_i]
    pb = hov(B, fs, [hs], lambda i: f"exponent {fs[i]:.3f}: h = {hs[i]:.2f} cm")
    return svg(VB, aria, s, "".join(o), ([(A.box, pa), (B.box, pb)],))


# ================================================================ #43 K5: impulse gain and height gain
def fig43():
    VB = (0, 0, W, 290)
    s = H.Scale(W, VB[3], display_w=400)
    J1, h1 = impulse(1.0), height(1.0)
    assert (round(J1, 1), round(impulse(0.8), 1)) == (169.9, 175.5)                       # line 546
    gj8, gh8 = (impulse(0.8) / J1 - 1) * 100, (height(0.8) / h1 - 1) * 100
    assert (round(gj8, 1), round(gh8, 1)) == (3.3, 6.7), (gj8, gh8)
    fs = np.round(np.linspace(0.5, 1.0, 101), 4)
    gj = np.array([(impulse(f) / J1 - 1) * 100 for f in fs])
    gh = np.array([(height(f) / h1 - 1) * 100 for f in fs])
    P = Plot(s, (62, 62, 388, 226), (0.5, 1.0), (-3.5, 9))
    o = [P.axes(tk((0.5, 0.6, 0.7, 0.8, 0.9, 1.0)), tk((0, 2, 4, 6, 8)), "front-loading exponent (1 = squat jump)",
                "gain over squat jump (%)", grid=(2, 4, 6, 8))]
    o.append(P.curve(fs, gh, SER[0], multi=True))
    o.append(P.curve(fs, gj, SER[1], multi=True))
    o.append(dot(P, 0.8, gh8, SER[0]))
    o.append(dot(P, 0.8, gj8, SER[1]))
    o.append(legend(s, 62, 20, [(SER[0], "jump height", None), (SER[1], "net impulse", None)]))
    o.append(label(s, P.X(0.53), P.Y(-1.4), f"at 0.8: height +{gh8:.1f}% ({h1*100:.2f} → {height(0.8)*100:.2f} cm)",
                   "label2"))
    o.append(label(s, P.X(0.53), P.Y(-1.4) + 16, f"impulse +{gj8:.1f}% ({J1:.1f} → {impulse(0.8):.1f} N·s)", "label2"))
    o.append(label(s, P.X(0.52), P.Y(8.2), "height gain ≈ 2 × impulse gain (h ∝ J²)", "label2", I["secondary"]))
    aria = (f"Problem K5 plot: gain of a front-loaded countermovement profile over the symmetric squat-jump profile, "
            f"at the same 2.5 body-weight peak, against the front-loading exponent from 0.5 to 1. The blue net-impulse "
            f"gain and the red jump-height gain both peak near 0.7, and the height gain is about twice the impulse "
            f"gain everywhere. At the Lab 2 countermovement exponent 0.8: impulse {J1:.1f} to {impulse(0.8):.1f} "
            f"newton seconds, plus {gj8:.1f} percent; height {h1*100:.2f} to {height(0.8)*100:.2f} cm, plus {gh8:.1f} percent.")
    hv = hov(P, fs, [gh, gj], lambda i: f"exponent {fs[i]:.3f}: height +{gh[i]:.2f}%, impulse +{gj[i]:.2f}%")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #44 K6: stopping distance vs drop height
def fig44():
    VB = (0, 0, W, 290)
    s = H.Scale(W, VB[3], display_w=400)
    h = np.linspace(0, 2.2, 111)
    ds = lambda hd: M * G * hd / (6 * M * G - M * G) * 100        # noqa: E731  cm, F_tol = 6 mg (line 550)
    pts = [(hd, ds(hd)) for hd in (0.2, 0.4, 0.6, 0.8, 1.0)]
    assert [round(d) for _, d in pts] == [4, 8, 12, 16, 20]
    hcap = 0.40 * (6 * M * G - M * G) / (M * G)                    # 40 cm of controllable give
    assert round(hcap, 1) == 2.0
    P = Plot(s, (62, 62, 388, 226), (0, 2.2), (0, 48))
    o = [P.axes(tk((0, 0.5, 1.0, 1.5, 2.0)), tk((0, 10, 20, 30, 40)), "drop height (m)",
                "minimum stop d" + sub("s", s) + " (cm)", grid=(10, 20, 30))]
    o.append(href(s, P, 40, I["secondary"]))
    o.append(P.curve(h, ds(h), SER[0]))
    o += [dot(P, a, b, SER[0]) for a, b in pts]
    o.append(dot(P, hcap, 40, O["flag"]))
    o.append(label(s, P.X(0.05), P.Y(40) + 17, "deepest controllable give ≈ 40 cm", "label2", I["secondary"]))
    o.append(label(s, P.X(hcap) + 4, P.Y(40) - 8, f"drop cap ≈ {hcap:.1f} m", "label2", I["primary"], "end"))
    o.append(label(s, P.X(1.0) + 9, P.Y(20) + 15, "20 cm at 1.0 m", "label2"))
    o.append(label(s, 62, 22, "d" + sub("s", s, "label2") + " = mgh/(F" + sub("tol", s, "label2") + " − mg) = h/5 "
                   "at F" + sub("tol", s, "label2") + " = 6mg (average force)", "label2", I["secondary"]))
    aria = ("Problem K6 plot: minimum stopping distance that keeps the average landing force below 6 body weights, "
            "against drop height. It is the straight line d = h/5: 4, 8, 12, 16 and 20 cm at drops of 0.2 to 1.0 m "
            f"(dots). A dashed line at 40 cm, the deepest controllable give, meets it at a drop cap of {hcap:.1f} m.")
    hv = hov(P, h, [ds(h)], lambda i: f"drop {h[i]:.2f} m: d = {ds(h[i]):.1f} cm")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #45 K7: economy factor and muscle work vs R
U_STEP = 31.0                                                   # Lab 4 (line 419)


def fig45():
    VB = (0, 0, W, 458)
    s = H.Scale(W, VB[3], display_w=400)
    R = np.linspace(0.5, 0.96, 185)
    fac, wm = 2 / (1 - R), (1 - R) * U_STEP
    lab = {r: 2 / (1 - r) for r in (0.80, 0.88, 0.92, 0.95)}
    assert [round(v, 1) for v in lab.values()] == [10.0, 16.7, 25.0, 40.0]                 # line 428
    sens = {r: 2 / (1 - r) ** 2 for r in (0.80, 0.92)}
    assert (round(sens[0.80], 1), round(sens[0.92], 1)) == (50.0, 312.5)                   # line 554
    w88, w92 = (1 - 0.88) * U_STEP, (1 - 0.92) * U_STEP
    assert (round(w92, 2), round(w88, 2), round(w88 / w92 - 1, 2)) == (2.48, 3.72, 0.5)
    A = Plot(s, (62, 40, 388, 176), (0.5, 0.96), (0, 52))
    B = Plot(s, (62, 288, 388, 398), (0.5, 0.96), (0, 17))
    rt = tk((0.5, 0.6, 0.7, 0.8, 0.9))
    o = [A.axes(rt, tk((0, 10, 20, 30, 40, 50)), "tendon resilience R", "economy 2/(1 − R)", grid=(10, 20, 30, 40, 50))]
    for r, dx in ((0.80, 0.08), (0.92, 0.025)):
        y0 = lab[r]
        o.append(H.line(s, A.X(r - dx), A.Y(y0 - sens[r] * dx), A.X(r + dx), A.Y(y0 + sens[r] * dx), I["secondary"],
                        "ref", H.DASH_REF))
    o.append(A.curve(R, fac, SER[0]))
    o += [dot(A, r, v, SER[0]) for r, v in lab.items()]
    for r, v in lab.items():
        o.append(label(s, A.X(r) - 6, A.Y(v) - 6, f"{v:.1f}", "label2", I["primary"], "end"))
    o.append(label(s, 62, 22, "tangent slope 2/(1 − R)², 50 at 0.80, 312.5 at 0.92", "label2", I["secondary"]))
    o.append(B.axes(rt, tk((0, 5, 10, 15)), "tendon resilience R", "muscle work (J)", grid=(5, 10, 15)))
    o.append(B.curve(R, wm, SER[1]))
    o.append(dot(B, 0.88, w88, SER[1]))
    o.append(dot(B, 0.92, w92, SER[1]))
    o.append(label(s, B.X(0.955), B.Y(12.5), f"R 0.92 → 0.88: {w92:.2f} → {w88:.2f} J, +50%", "label2",
                   I["primary"], "end"))
    o.append(label(s, 62, 266, f"muscle work per step = (1 − R) × {U_STEP:.0f} J", "label2", I["secondary"]))
    aria = ("Problem K7, two panels against tendon resilience R from 0.5 to 0.96. Top: the economy factor 2 over 1 "
            "minus R rising hyperbolically through 10.0, 16.7, 25.0 and 40.0 at R = 0.80, 0.88, 0.92 and 0.95; dashed "
            "tangents show its slope, 50 at 0.80 and 312.5 at 0.92. Bottom: muscle work per step, 1 minus R times 31 J, "
            f"falling linearly; dropping R from 0.92 to 0.88 raises it from {w92:.2f} to {w88:.2f} J, 50 percent more.")
    pa = hov(A, R, [fac], lambda i: f"R = {R[i]:.3f}: factor {fac[i]:.1f}, slope {2/(1-R[i])**2:.0f}")
    pb = hov(B, R, [wm], lambda i: f"R = {R[i]:.3f}: muscle work {wm[i]:.2f} J")
    return svg(VB, aria, s, "".join(o), ([(A.box, pa), (B.box, pb)],))


# ================================================================ #46 K8: loading rate and peak vs contact stiffness
M_IMP, V_IMP = 8.0, 1.0                                         # section 9 (line 314)


def fig46():
    VB = (0, 0, W, 458)
    s = H.Scale(W, VB[3], display_w=400)
    k = np.linspace(0, 250, 126)
    rate = 2 / math.pi * V_IMP * k * 1e3 / BW                       # (9.1), BW/s
    peak = V_IMP * np.sqrt(k * 1e3 * M_IMP) / BW
    kmax = math.pi / 2 * 100 * BW / V_IMP / 1e3
    pk = lambda kc: V_IMP * math.sqrt(kc * 1e3 * M_IMP) / BW       # noqa: E731
    rt = lambda kc: 2 / math.pi * V_IMP * kc * 1e3 / BW             # noqa: E731
    assert (round(kmax, 1), round(pk(kmax), 2), round(pk(200), 2), round(rt(200)), round(rt(40))) == (
        107.9, 1.35, 1.84, 185, 37)                                                       # lines 314, 558
    assert (round((1 - 100 / rt(200)) * 100), round((1 - pk(kmax) / pk(200)) * 100)) == (46, 27)
    A = Plot(s, (62, 40, 388, 176), (0, 250), (0, 250))
    B = Plot(s, (62, 288, 388, 398), (0, 250), (0, 2.2))
    kt = tk((0, 50, 100, 150, 200, 250))
    o = [A.axes(kt, tk((0, 100, 200)), "contact stiffness k" + sub("c", s) + " (kN/m)", "loading rate (BW/s)",
                grid=(100, 200))]
    o.append(href(s, A, 100, I["secondary"]))
    o.append(vref(s, A, kmax, O["flag"]))
    o.append(A.curve(k, rate, SER[0]))
    o.append(dot(A, kmax, 100, O["flag"]))
    o.append(dot(A, 200, rt(200), SER[0]))
    o.append(dot(A, 40, rt(40), SER[0]))
    o.append(label(s, A.X(248), A.Y(100) + 17, "tolerance 100 BW/s", "label2", I["secondary"], "end"))
    o.append(label(s, A.X(kmax) - 6, A.Y(212), "k" + sub("c", s, "label2") + f" ≤ {kmax:.1f}", "label2", I["primary"],
                   "end"))
    o.append(label(s, A.X(250) - 2, A.Y(rt(200)) + 30, f"200 kN/m: {rt(200):.0f}/s", "label2", I["primary"], "end"))
    o.append(label(s, A.X(40) + 8, A.Y(rt(40)) + 16, f"{rt(40):.0f}/s at 40", "label2"))
    o.append(B.axes(kt, tk((0, 1, 2)), "contact stiffness k" + sub("c", s) + " (kN/m)", "impact peak (BW)",
                    grid=(1, 2)))
    o.append(vref(s, B, kmax, O["flag"]))
    o.append(B.curve(k, peak, SER[1]))
    o.append(dot(B, kmax, pk(kmax), O["flag"]))
    o.append(dot(B, 200, pk(200), SER[1]))
    o.append(label(s, B.X(kmax) + 9, B.Y(pk(kmax)) + 18, f"{pk(kmax):.2f}", "label2"))
    o.append(label(s, B.X(200) + 2, B.Y(pk(200)) + 22, f"{pk(200):.2f}", "label2", I["primary"], "middle"))
    o.append(label(s, 62, 266, "rate ∝ k" + sub("c", s, "label2") + ", peak ∝ √k" + sub("c", s, "label2")
                   + ": rate −46%, peak −27%", "label2", I["secondary"]))
    aria = ("Problem K8, two panels against contact stiffness from 0 to 250 kN/m, impact mass 8 kg at 1.0 m/s. Top: "
            "loading rate, a straight line through 37 body weights per second at 40 kN/m and 185 at 200 kN/m (concrete); "
            f"it meets the dashed tolerance of 100 per second at {kmax:.1f} kN/m (orange). Bottom: impact peak rising "
            f"as the square root of stiffness, {pk(kmax):.2f} body weights at {kmax:.1f} and {pk(200):.2f} at 200: "
            "the rate falls 46 percent, the peak only 27.")
    pa = hov(A, k, [rate], lambda i: f"k = {k[i]:.0f} kN/m: rate {rate[i]:.0f} BW/s, peak {peak[i]:.2f} BW")
    pb = hov(B, k, [peak], lambda i: f"k = {k[i]:.0f} kN/m: peak {peak[i]:.2f} BW, rate {rate[i]:.0f} BW/s")
    return svg(VB, aria, s, "".join(o), ([(A.box, pa), (B.box, pb)],))


# ================================================================ #47 K9: Miner damage and safe mileage
N0, SIG0, B_EXP, CYC_KM, WEEKS = 1e4, 60.0, 0.12, 700.0, 4          # K9 solution (line 562)


def n_fail(sig):
    return N0 * (SIG0 / sig) ** (1 / B_EXP)


def fig47():
    VB = (0, 0, W, 470)
    s = H.Scale(W, VB[3], display_w=400)
    km = {sg: n_fail(sg) / CYC_KM for sg in (45.0, 50.0)}
    wk = {sg: v / WEEKS for sg, v in km.items()}
    assert (round(n_fail(45) / 1e5, 2), round(km[45]), round(wk[45]), round(n_fail(50) / 1e4, 1), round(km[50]),
            round(wk[50]), round(km[45] / km[50], 1)) == (1.10, 157, 39, 4.6, 65, 16, 2.4)
    A = Plot(s, (62, 62, 388, 190), (0, 50), (0, 1.5))
    x = np.linspace(0, 50, 101)
    D = {sg: WEEKS * x * CYC_KM / n_fail(sg) for sg in (45.0, 50.0)}
    o = [A.axes(tk((0, 10, 20, 30, 40, 50)), tk((0, 0.5, 1, 1.5)), "weekly mileage (km)", "damage D in 4 weeks",
                grid=(0.5, 1.5))]
    o.append(href(s, A, 1.0, I["secondary"]))
    x50 = np.linspace(0, 1.5 * n_fail(50.0) / (WEEKS * CYC_KM), 101)
    o.append(A.curve(x50, WEEKS * x50 * CYC_KM / n_fail(50.0), SER[0], multi=True))
    o.append(A.curve(x, D[45.0], SER[1], multi=True))
    o.append(dot(A, wk[50], 1.0, SER[0]))
    o.append(dot(A, wk[45], 1.0, SER[1]))
    o.append(legend(s, 62, 20, [(SER[0], "50 MPa per step", None), (SER[1], "45 MPa per step", None)]))
    o.append(label(s, 62, 40, "Miner D = 4 × 700 × km/week ÷ N(σ); fracture at D = 1", "label2", I["secondary"]))
    o.append(label(s, A.X(wk[50]) + 9, A.Y(1.0) + 18, f"{wk[50]:.0f} km/wk", "label2"))
    o.append(label(s, A.X(wk[45]) + 9, A.Y(1.0) + 18, f"{wk[45]:.0f} km/wk", "label2"))
    o.append(label(s, A.X(0.8), A.Y(1.0) - 6, "D = 1", "label2", I["secondary"]))
    B = Plot(s, (62, 300, 388, 410), (40, 60), (0, math.log10(200)))
    sg = np.linspace(40, 60, 101)
    safe = n_fail(sg) / CYC_KM / WEEKS
    o.append(B.axes(tk((40, 45, 50, 55, 60)), [(math.log10(v), f"{v:g}") for v in (1, 10, 100)],
                    "per-step bone stress σ (MPa)", "safe km/week", grid=(1, 2)))
    o.append(B.curve(sg, np.log10(safe), SER[2]))
    o.append(dot(B, 45, math.log10(wk[45]), SER[1]))
    o.append(dot(B, 50, math.log10(wk[50]), SER[0]))
    o.append(label(s, B.X(45) + 9, B.Y(math.log10(wk[45])) - 4, f"{wk[45]:.0f}", "label2"))
    o.append(label(s, B.X(50) + 9, B.Y(math.log10(wk[50])) - 4, f"{wk[50]:.0f}", "label2"))
    o.append(label(s, 62, 276, "N(σ) = 10⁴ (60/σ)" + '<tspan baseline-shift="super" font-size="9.1">1/0.12</tspan>'
                   f": +11% stress, ÷{km[45]/km[50]:.1f} mileage", "label2", I["secondary"]))
    aria = (f"Problem K9, two panels. Top: Miner damage accumulated in four weeks against weekly mileage, straight lines "
            f"for a per-step stress of 45 MPa (blue) and 50 MPa (red), reaching the dashed fracture line D = 1 at "
            f"{wk[45]:.0f} and {wk[50]:.0f} km per week. Bottom: the safe weekly mileage against per-step stress on a "
            f"log axis, from the Basquin curve N = 10 to the 4 times (60 over sigma) to the power 1/0.12, falling "
            f"steeply: an 11 percent rise in stress, 45 to 50 MPa, divides the safe mileage by {km[45]/km[50]:.1f}.")
    pa = hov(A, x, [D[50.0], D[45.0]],
             lambda i: f"{x[i]:.1f} km/week: D = {D[50.0][i]:.2f} (50 MPa), {D[45.0][i]:.2f} (45 MPa)")
    pb = hov(B, sg, [np.log10(safe)],
             lambda i: f"σ = {sg[i]:.1f} MPa: N = {n_fail(sg[i]):.3g}, safe {safe[i]:.1f} km/week")
    return svg(VB, aria, s, "".join(o), ([(A.box, pa), (B.box, pb)],))


# ================================================================ #48 K10: walking vs running cost
def fig48():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    fr = lambda v: v * v / (G * L0)                                  # noqa: E731  (4.2), L0 = 1.0 m
    walk = lambda f: f * f / (1 - 0.85 * f)                          # noqa: E731  K10 solution (line 566)
    run_a, run_b = walk(0.71), walk(0.5)                             # flat running levels: Fr 0.71 and Fr 1/2
    v_x, v_c, v_1 = math.sqrt(0.71 * G * L0), math.sqrt(0.5 * G * L0), math.sqrt(G * L0)
    assert round(v_x, 1) == 2.6
    P = Plot(s, (62, 70, 388, 232), (0.5, 3.5), (0, 2.6))
    vw = np.linspace(0.5, 2.92, 122)
    cw = walk(fr(vw))
    o = [P.axes(tk((1, 1.5, 2, 2.5, 3, 3.5)), tk((0, 1, 2)), "speed v (m/s)", "cost per distance (a.u.)", grid=(1, 2))]
    o.append(vref(s, P, v_1, I["secondary"]))
    o.append(P.curve([0.5, 3.5], [run_b, run_b], SER[0], multi=True, dash=H.DASH_REF))
    o.append(P.curve([0.5, 3.5], [run_a, run_a], SER[0], multi=True))
    o.append(P.curve(vw, cw, SER[1], multi=True))
    o.append(dot(P, v_x, run_a, O["flag"]))
    o.append(dot(P, v_c, run_b, SER[0]))
    o.append(legend(s, 62, 20, [(SER[1], "walk ∝ Fr²/(1 − 0.85 Fr)", None), (SER[0], "run, flat", None)]))
    o.append(label(s, 62, 40, "free run level: solid → Fr 0.71, dashed → Fr ½", "label2",
                   I["secondary"]))
    o.append(label(s, P.X(v_x) - 8, P.Y(run_a) - 10, f"v = {v_x:.1f} m/s, Fr = 0.71", "label2", I["primary"], "end"))
    o.append(label(s, P.X(v_c) - 8, P.Y(run_b) - 9, f"Fr = ½: {v_c:.1f} m/s", "label2", I["primary"], "end"))
    o.append(label(s, P.X(v_1) + 5, P.Y(2.35), "Fr = 1", "label2", I["secondary"]))
    o.append(label(s, P.X(v_1) + 5, P.Y(2.35) + 15, "ceiling", "label2", I["secondary"]))
    o.append(label(s, P.X(2.05), P.Y(walk(fr(2.05))) + 16, "walk", "label2", I["primary"], "start"))
    o.append(label(s, P.X(0.6), P.Y(run_a) - 7, "run", "label2", I["primary"], "start"))
    aria = (f"Problem K10 plot: metabolic cost per distance, arbitrary units, against speed from 0.5 to 3.5 metres per "
            f"second for a 1 m leg. Walking cost, proportional to Fr squared over 1 minus 0.85 Fr, rises steeply; running "
            f"cost is taken flat. With one plausible running level the curves cross at {v_x:.1f} m/s, Fr = 0.71 "
            f"(solid red line); the dashed red level calibrated to the observed Fr of one half crosses at {v_c:.1f} m/s. "
            f"Both crossings lie below the dashed Fr = 1 ceiling at {v_1:.2f} m/s.")
    hv = []
    for v in np.linspace(0.5, 3.5, 151):
        if v <= 2.92:
            hv.append([round(P.X(v), 2), [round(P.Y(walk(fr(v))), 2), round(P.Y(run_a), 2)],
                       f"v = {v:.2f} m/s, Fr = {fr(v):.2f}: walk {walk(fr(v)):.2f}, run {run_a:.2f}"])
        else:
            txt = "walk off scale" if v < v_1 else "walking not available (Fr > 1)"
            hv.append([round(P.X(v), 2), round(P.Y(run_a), 2), f"v = {v:.2f} m/s, Fr = {fr(v):.2f}: {txt}"])
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #49 K11: power-duration fit of six records
def k11():
    """The K11 script (lines 572-626), ported line for line."""
    CoT_run, m = 4.184, 70.0
    records = {"800 m": (800.0, 100.91), "1500 m": (1500.0, 206.00), "5000 m": (5000.0, 755.36),
               "10000 m": (10000.0, 1571.00), "half marathon": (21097.5, 3451.0), "marathon": (42195.0, 7235.0)}
    t = np.array([tt for _, tt in records.values()])
    speed = np.array([d / tt for d, tt in records.values()])
    power = CoT_run * speed * m

    def fit(t_pts, p_pts):
        x = 1.0 / t_pts
        a_mat = np.vstack([np.ones_like(x), x]).T
        (cp, wprime), *_ = np.linalg.lstsq(a_mat, p_pts, rcond=None)
        return cp, wprime

    cp, wp = fit(t, power)
    loo = [fit(t[np.arange(len(t)) != i], power[np.arange(len(t)) != i]) for i in range(len(t))]
    p_ox = 75.0 * m / 1000.0 / 60.0 * 20.9e3
    return list(records), t, power, cp, wp, loo, p_ox


def fig49():
    VB = (0, 0, W, 296)
    s = H.Scale(W, VB[3], display_w=400)
    names, t, p, cp, wp, loo, p_ox = k11()
    assert (round(p[0], 1), round(p[-1], 1), round(cp, 1), round(wp / 1e3, 2), round(p_ox)) == (
        2321.9, 1708.1, 1796.9, 56.84, 1829), (p, cp, wp)                                   # line 627
    assert (round(min(c for c, _ in loo)), round(max(c for c, _ in loo))) == (1774, 1832)
    lt = math.log10
    P = Plot(s, (62, 62, 388, 232), (lt(80), lt(9000)), (1600, 2450))
    tt = np.logspace(lt(80), lt(9000), 150)
    pf = cp + wp / tt
    o = [P.axes([(lt(v), f"{v:g}") for v in (100, 1000)] + [(lt(v), "") for v in (200, 500, 2000, 5000)],
                tk((1600, 1800, 2000, 2200, 2400)), "duration t (s, log scale)", "metabolic power (W)",
                grid=(1800, 2000, 2200, 2400))]
    o.append(href(s, P, p_ox, SER[2]))
    o.append(href(s, P, cp, SER[1]))
    o.append(P.curve(np.log10(tt), pf, SER[1]))
    o += [dot(P, lt(a), b, SER[0]) for a, b in zip(t, p)]
    o.append(legend(s, 62, 20, [(SER[1], "fit P = CP + W′/t", None), (SER[2], "structural CP", H.DASH_REF)]))
    o.append(label(s, 62, 40, f"fit: CP = {cp:.0f} W, W′ = {wp/1e3:.1f} kJ; dots: six world records", "label2",
                   I["secondary"]))
    o.append(label(s, P.x0 + 4, P.Y(p_ox) - 6, f"structural {p_ox:.0f} W", "label2"))
    o.append(label(s, P.x0 + 4, P.Y(cp) + 16, f"CP fit {cp:.0f} W", "label2"))
    o.append(label(s, P.X(lt(t[-1])) - 8, P.Y(p[-1]) + 5, "marathon", "label2", I["primary"], "end"))
    o.append(label(s, P.X(lt(700)), P.Y(2340), f"800 m (left dot): {p[0]/cp*100:.1f}% of CP", "label2"))
    o.append(label(s, P.X(lt(700)), P.Y(2340) + 16, f"marathon: {p[-1]/cp*100:.1f}% of CP", "label2"))
    aria = (f"Problem K11 plot: metabolic power against duration on a log axis from 80 to 9000 seconds for six world "
            f"running records, 800 m to the marathon (red dots), from {p[0]:.0f} W to {p[-1]:.0f} W. The fitted "
            f"hyperbola P = CP + W prime over t (blue) has CP = {cp:.0f} W (blue dashed asymptote) and W prime = "
            f"{wp/1e3:.1f} kJ; the orange dashed line is the structural CP of {p_ox:.0f} W from a VO2max of 75 mL/kg/min. "
            f"The 800 m sits at {p[0]/cp*100:.1f} percent of the fitted CP, the marathon at {p[-1]/cp*100:.1f} percent.")
    hv = [[round(P.X(lt(v)), 2), round(P.Y(cp + wp / v), 2), f"t = {v:.0f} s: fit P = {cp + wp / v:.0f} W"] for v in tt]
    return svg(VB, aria, s, "".join(o), (P.box, hv))


FIGS = {
    39: ("Flight time rising monotonically with leg stiffness across t", fig39),
    40: ("Stride asymmetry versus angle of attack, a monotone curve cr", fig40),
    41: ("Recovered jump-height error versus body-mass error, a linear", fig41),
    42: ("Jump height versus push-off profile, with an optimum.", fig42),
    43: ("Squat-jump versus countermovement-jump energy bars, the coun", fig43),
    44: ("Minimum stopping distance rising in proportion to drop heigh", fig44),
    45: ("Economy factor versus tendon resilience, rising steeply.", fig45),
    46: ("Loading rate versus contact stiffness, linear.", fig46),
    47: ("Cumulative bone damage versus weekly mileage, reaching the f", fig47),
    48: ("Walking cost rising steeply with speed and running cost risi", fig48),
    49: ("Metabolic power against duration on a log time axis for six ", fig49),
}
