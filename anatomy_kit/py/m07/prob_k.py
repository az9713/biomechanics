"""Module 7 computational-problem plots (K1-K9): house-style redraws at 400 px (svg #46-#54).

Every plotted number is computed here from the K solutions in module07.html (lines 848-882), with the Lab 1
and Lab 2 code and the reference body imported from m07.plots_main. K5 and K8 need the rightmost
characteristic root of I s^2 - Mgl + (Kp + Kd s) e^{-s Delta}: a Chebyshev collocation of the delay
equation's generator (24 nodes) gives the candidates, Newton on the quasi-polynomial refines them.
The numbers the solutions quote are asserted.
"""
import math
from functools import lru_cache

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.signal import welch

import house as H
from m05.plots_prob import Plot, hov, label, legend, sub, svg
from m07.plots_main import (ELL, G, I_B, M_B, MGL, W0, bisect_delay, hopf, island_area, island_kd, peak_compression,
                            rms_mm, safe_load, simulate, sway, theory, K7_SEED)

O, I, SER, T = H.OVERLAY, H.INK, H.SERIES, H.TISSUE
W = 400
BOX = "#f7f4ef"


def dot(P, x, y, col, hollow=False, r=None):
    r = r or P.s(H.PX["dot"])
    if hollow:
        return (f'<circle cx="{P.X(x):.2f}" cy="{P.Y(y):.2f}" r="{r:.2f}" fill="#fff" stroke="{col}" '
                f'stroke-width="1.8"/>')
    return f'<circle cx="{P.X(x):.2f}" cy="{P.Y(y):.2f}" r="{r:.2f}" fill="{col}" stroke="#fff" stroke-width="1.5"/>'


def tk(vals, f="{:g}"):
    return [(v, f.format(v).replace("-", "−")) for v in vals]


def ref(s, P, y, col=None):
    return H.line(s, P.x0, P.Y(y), P.x1, P.Y(y), col or I["secondary"], "ref", H.DASH_REF)


def vref(s, P, x, col=None):
    return H.line(s, P.X(x), P.y1, P.X(x), P.y0, col or I["secondary"], "ref", H.DASH_REF)


# ---------------------------------------------------------------- rightmost characteristic root (K5, K8)
def _cheb(N):
    x = np.cos(np.pi * np.arange(N + 1) / N)
    c = np.hstack([2, np.ones(N - 1), 2]) * (-1) ** np.arange(N + 1)
    X = np.tile(x, (N + 1, 1)).T
    D = np.outer(c, 1 / c) / (X - X.T + np.eye(N + 1))
    return D - np.diag(D.sum(1))


CHEB = _cheb(24)


def rightmost(Kp, Kd, D):
    """Real part of the rightmost root of I s^2 - Mgl + (Kp + Kd s) e^{-sD} (Prop 6.1)."""
    N = CHEB.shape[0] - 1
    A0 = np.array([[0.0, 1.0], [MGL / I_B, 0.0]])
    A1 = np.array([[0.0, 0.0], [-Kp / I_B, -Kd / I_B]])
    Gm = np.zeros((2 * (N + 1), 2 * (N + 1)))
    Gm[0:2, 0:2], Gm[0:2, 2 * N:] = A0, A1
    Gm[2:, :] = np.kron(CHEB[1:, :] * 2 / D, np.eye(2))
    ev = np.linalg.eigvals(Gm)
    best = -np.inf
    for z in ev[np.argsort(-ev.real)][:6]:
        for _ in range(30):
            e = np.exp(-z * D)
            f = I_B * z * z - MGL + (Kp + Kd * z) * e
            fp = 2 * I_B * z + Kd * e - D * (Kp + Kd * z) * e
            step = f / fp
            z = z - step
            if abs(step) < 1e-12:
                break
        best = max(best, z.real)
    return float(best)


D_TRUE = 0.15                                           # the true neural delay of K5 and K8


@lru_cache(maxsize=None)
def k5_opt():
    r = minimize(lambda p: rightmost(p[0], p[1], D_TRUE), [800.0, 250.0], method="Nelder-Mead",
                 options=dict(xatol=1e-4, fatol=1e-10, maxiter=4000))
    return float(r.x[0]), float(r.x[1]), float(-r.fun)


@lru_cache(maxsize=None)
def sigma_best(Kp):
    """Largest decay rate at one Kp with Kd optimised inside the island (K5, K8): (sigma, Kd)."""
    lo, hi = island_kd(D_TRUE, Kp)
    r = minimize_scalar(lambda kd: rightmost(Kp, kd, D_TRUE), bounds=(lo, hi), method="bounded", options=dict(xatol=1e-3))
    return float(-r.fun), float(r.x)


def cheapest_kp(sig):
    """K8: smallest Kp whose best decay rate reaches sig (sigma_best rises on (Mgl, Kp_opt])."""
    lo, hi = MGL + 0.5, k5_opt()[0]
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if sigma_best(round(mid, 6))[0] < sig else (lo, mid)
    return 0.5 * (lo + hi)


# ================================================================ #46 K1: bisection for the stiffer gains
def fig46():
    VB = (0, 0, W, 470)
    s = H.Scale(W, VB[3], display_w=400)
    dsim, mids = bisect_delay(1100.0, 150.0)
    dth, wc = theory(1100.0, 150.0)
    assert round(dsim * 1e3, 1) == 129.5 and round(dth * 1e3, 1) == 129.7 and round(wc, 2) == 2.93   # line 850
    A = Plot(s, (62, 44, 388, 186), (0, 27), (100, 200))
    steps = list(range(1, 27))
    ms = [1e3 * m for m in mids]
    o = [A.axes(tk((1, 5, 10, 15, 20, 25)), tk((100, 150, 200)), "bisection step", "trial Δ (ms)", grid=(150,))]
    o.append(ref(s, A, dth * 1e3, O["flag"]))
    o.append(A.curve(steps, ms, SER[0], multi=True))
    o += [dot(A, k, m, SER[0], r=2.6) for k, m in zip(steps, ms)]
    o.append(label(s, A.X(26), A.Y(dth * 1e3) - 8, f"closed form {dth*1e3:.1f} ms", "label2", I["primary"], "end"))
    o.append(label(s, A.X(26), A.Y(dth * 1e3) + 20, f"bisection → {dsim*1e3:.1f} ms", "label2", I["primary"], "end"))
    o.append(label(s, 62, 24, f"K{sub('p', s, 'label2')} = 1100, K{sub('d', s, 'label2')} = 150", "label2", I["secondary"]))
    # panel B: the DDE at the bisected delay
    B = Plot(s, (62, 290, 388, 410), (0, 12), (-0.8, 0.8))
    t, th = simulate(1100.0, 150.0, dsim, T=12.0)
    pk = [i for i in range(1, len(th) - 1) if th[i] > th[i - 1] and th[i] >= th[i + 1] and t[i] > 1]
    f_obs = (len(pk) - 1) / (t[pk[-1]] - t[pk[0]])
    assert round(f_obs, 2) == round(wc / (2 * math.pi), 2) == 0.47, f_obs
    o.append(B.axes(tk((0, 4, 8, 12)), tk((-0.6, 0, 0.6)), "time (s)", "θ (degrees)", grid=(0,)))
    o.append(B.curve(t[::25], th[::25], SER[1], multi=True, nmax=500))
    o.append(label(s, 62, 264, f"at Δ = {dsim*1e3:.1f} ms: sustained sway at {f_obs:.2f} Hz", "label2", I["primary"]))
    o.append(label(s, 62, 281, f"(ω{sub('c', s, 'label2')} = {wc:.2f} s⁻¹; 0.35 Hz at 900, 120)", "label2", I["secondary"]))
    aria = (f"Problem K1, two panels, gains Kp = 1100 and Kd = 150. Top: the 26 trial delays of the Lab 1 bisection, "
            f"starting at 150 ms and converging to {dsim*1e3:.1f} ms, against a dashed orange line at the closed-form "
            f"critical delay {dth*1e3:.1f} ms. Bottom: the lean simulated at that delay over 12 s, a sustained "
            f"oscillation at {f_obs:.2f} Hz (omega-c = {wc:.2f} per second).")
    p1 = hov(A, steps, [ms], lambda i: f"step {steps[i]}: trial Δ = {ms[i]:.2f} ms")
    tt, yy = t[::100], th[::100]
    p2 = hov(B, tt, [yy], lambda i: f"t = {tt[i]:.1f} s: θ = {yy[i]:.3f}°")
    return svg(VB, aria, s, "".join(o), ([(A.box, p1), (B.box, p2)],))


# ================================================================ #47 K2: two islands and their areas
def fig47():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    a12, a18 = island_area(0.12), island_area(0.18)
    assert (round(a12 / 1e6, 3), round(a18 / 1e5, 3), round(a12 / a18, 3)) == (1.189, 2.674, 4.446)   # line 854
    P = Plot(s, (62, 44, 262, 236), (0, 3000), (0, 950))
    o = []
    for D, col in ((0.12, SER[0]), (0.18, SER[1])):
        kp, kd = hopf(D)
        o.append(f'<polygon points="{" ".join(f"{P.X(a):.1f},{P.Y(b):.1f}" for a, b in zip(kp, kd))}" fill="{col}" '
                 f'opacity="0.12"/>')
    o.append(P.axes([(0, "0"), (MGL, "Mgℓ"), (1500, "1500"), (3000, "3000")], tk((0, 400, 800)), f"K{sub('p', s)} (N·m/rad)", f"K{sub('d', s)} (N·m·s/rad)"))
    for D, col in ((0.12, SER[0]), (0.18, SER[1])):
        kp, kd = hopf(D)
        o.append(P.curve(kp, kd, col, multi=True))
    o.append(H.line(s, P.X(MGL), P.y1, P.X(MGL), P.y0, I["axis"], "ref", H.DASH_REF))
    k12 = int(hopf(0.12)[0].argmax())
    o.append(label(s, P.X(2150), P.Y(hopf(0.12)[1][k12]) + 5, "0.12 s", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(1080), P.Y(380) + 5, "0.18 s", "label2", I["primary"], "middle"))
    o.append(legend(s, 62, 22, [(SER[0], "Δ = 0.12 s", None), (SER[1], "Δ = 0.18 s", None)]))
    # bars: island areas, one scale
    bx, by, hmax = 290, 236, 150
    for i, (a, col, txt) in enumerate(((a12, SER[0], f"{a12/1e6:.2f}"), (a18, SER[1], f"{a18/1e6:.2f}"))):
        h = hmax * a / a12
        o.append(f'<rect x="{bx + i*52:.2f}" y="{by - h:.2f}" width="40" height="{h:.2f}" fill="{col}" opacity="0.85"/>')
        o.append(label(s, bx + i * 52 + 20, by - h - 6, txt, "label2", I["primary"], "middle"))
        o.append(label(s, bx + i * 52 + 20, by + 16, ("0.12 s", "0.18 s")[i], "label2", I["secondary"], "middle"))
    o.append(H.line(s, bx - 6, by, bx + 98, by, I["axis"], "axis"))
    o.append(label(s, bx + 46, 54, "island area, ×10⁶", "label2", I["secondary"], "middle"))
    o.append(label(s, bx + 46, 280, f"ratio {a12/a18:.3f}", "label2", I["primary"], "middle"))
    o.append(label(s, bx + 46, 296, "(grid: 4.44)", "label2", I["secondary"], "middle"))
    aria = (f"Problem K2. Left: the stability islands for delays 0.12 s (red) and 0.18 s (blue) in the gain plane, "
            f"Kp from 0 to 3000 and Kd from 0 to 950, drawn from the Hopf boundary of Proposition 6.2 to one scale, with "
            f"the divergence line Kp = Mgl dashed. Right: bars of the island areas, {a12/1e6:.2f} and {a18/1e6:.3f} "
            f"million, a ratio of {a12/a18:.3f}; the grid simulation of the solution gives 4.44.")
    hk = np.linspace(MGL + 5, 2900, 120)
    pts = []
    for k in hk:
        ys, parts = [], []
        for D in (0.12, 0.18):
            r = island_kd(D, k)
            if r:
                ys += [P.Y(r[0]), P.Y(r[1])]
                parts.append(f"Δ {D:.2f}: Kd {r[0]:.0f}–{r[1]:.0f}")
        pts.append([P.X(k), ys or P.Y(0), f"Kp = {k:.0f}: " + ("; ".join(parts) if parts else "no stable Kd")])
    return svg(VB, aria, s, "".join(o), (P.box, pts))


# ================================================================ #48 K3: inverse Hopf from a sway frequency
def k3(f, Kd=100.0):
    w = 2 * math.pi * f
    Kp = math.sqrt(MGL ** 2 + I_B ** 2 * w ** 4 + (2 * I_B * MGL - Kd ** 2) * w ** 2)
    return Kp, math.atan(Kd * w / Kp) / w


def fig48():
    VB = (0, 0, W, 450)
    s = H.Scale(W, VB[3], display_w=400)
    kp4, d4 = k3(0.40)
    assert round(kp4) == 1004 and round(d4 * 1e3) == 98                  # line 858
    fs = np.linspace(0.20, 0.65, 91)
    kps = np.array([k3(f)[0] for f in fs])
    ds = np.array([1e3 * k3(f)[1] for f in fs])
    A = Plot(s, (66, 40, 388, 176), (0.2, 0.65), (600, 1800))
    B = Plot(s, (66, 252, 388, 388), (0.2, 0.65), (40, 150))
    o = [A.axes(tk((0.2, 0.3, 0.4, 0.5, 0.6)), tk((600, 1200, 1800)), "sway frequency f (Hz)", f"K{sub('p', s)} (N·m/rad)",
                grid=(1200,))]
    o.append(H.line(s, A.X(0.4), A.Y(kp4), A.X(0.4), A.y0, I["rule"], "leader", H.DASH_REF))
    o.append(A.curve(fs, kps, SER[0]))
    o.append(dot(A, 0.4, kp4, O["flag"]))
    o.append(label(s, A.X(0.4) - 8, A.Y(kp4) - 10, f"0.40 Hz → K{sub('p', s, 'label2')} ≈ {kp4:.0f}", "label2", I["primary"], "end"))
    o.append(label(s, A.x0 + 6, A.y1 + 14, f"marginal Hopf, K{sub('d', s, 'label2')} = 100", "label2", I["secondary"]))
    o.append(B.axes(tk((0.2, 0.3, 0.4, 0.5, 0.6)), tk((40, 80, 120)), "sway frequency f (Hz)", "loop delay Δ (ms)",
                    grid=(80, 120)))
    o.append(H.line(s, B.X(0.4), B.Y(d4 * 1e3), B.X(0.4), B.y0, I["rule"], "leader", H.DASH_REF))
    o.append(B.curve(fs, ds, SER[1]))
    o.append(dot(B, 0.4, d4 * 1e3, O["flag"]))
    o.append(label(s, B.X(0.4) + 8, B.Y(d4 * 1e3) - 10, f"Δ ≈ {d4*1e3:.1f} ms", "label2", I["primary"]))
    aria = (f"Problem K3, two panels against the observed sway frequency from 0.2 to 0.65 Hz, derivative gain fixed at 100. "
            f"Top: the proportional gain that puts the body on the Hopf boundary at that frequency, rising from "
            f"{kps[0]:.0f} to {kps[-1]:.0f}; at 0.40 Hz it is {kp4:.0f} N m per rad. Bottom: the matching loop delay, "
            f"falling from {ds[0]:.0f} to {ds[-1]:.0f} ms; at 0.40 Hz it is {d4*1e3:.1f} ms.")
    pa = hov(A, fs, [kps], lambda i: f"f = {fs[i]:.3f} Hz: Kp = {kps[i]:.0f} N·m/rad")
    pb = hov(B, fs, [ds], lambda i: f"f = {fs[i]:.3f} Hz: Δ = {ds[i]:.1f} ms")
    return svg(VB, aria, s, "".join(o), ([(A.box, pa), (B.box, pb)],))


# ================================================================ #49 K4: body scale and delay tolerance
def fig49():
    VB = (0, 0, W, 450)
    s = H.Scale(W, VB[3], display_w=400)
    hs = np.linspace(1.6, 1.9, 61)
    w0 = np.sqrt(G / (0.55 * hs - 0.06))
    w0_n = np.sqrt(G / (0.55 * hs))
    clk = 100 * (w0[0] / w0 - 1)                       # % change of 1/w0 against the 1.6 m person
    clk_n = 100 * (w0_n[0] / w0_n - 1)
    assert (round(w0[0], 2), round(w0[-1], 2), round(100 * (1 - w0[-1] / w0[0]), 1), round(clk[-1], 1),
            round(clk_n[-1], 1)) == (3.46, 3.16, 8.8, 9.6, 9.0)                          # line 862
    A = Plot(s, (66, 40, 296, 176), (1.6, 1.9), (3.1, 3.5))
    B = Plot(s, (66, 262, 296, 398), (1.6, 1.9), (0, 10))
    o = [A.axes(tk((1.6, 1.7, 1.8, 1.9)), tk((3.1, 3.3, 3.5)), "height h (m)", "ω₀ (s⁻¹)", grid=(3.3,))]
    o.append(A.curve(hs, w0, SER[0]))
    o.append(dot(A, 1.6, w0[0], O["flag"]))
    o.append(dot(A, 1.9, w0[-1], O["flag"]))
    o.append(label(s, A.X(1.6) + 10, A.Y(w0[0]) - 6, f"1.6 m: {w0[0]:.2f} s⁻¹", "label2", I["primary"]))
    o.append(label(s, A.X(1.9) + 8, A.Y(w0[-1]) + 4, f"1.9 m: {w0[-1]:.2f} s⁻¹", "label2", I["primary"]))
    o.append(label(s, A.X(1.9) + 8, A.Y(w0[-1]) + 20, f"(−{100*(1-w0[-1]/w0[0]):.1f} %)", "label2", I["primary"]))
    o.append(label(s, A.X(1.9) + 8, A.y1 + 40, "ω₀ = √(g/ℓ),", "label2", I["secondary"]))
    o.append(label(s, A.X(1.9) + 8, A.y1 + 56, "ℓ = 0.55h − 0.06", "label2", I["secondary"]))
    o.append(B.axes(tk((1.6, 1.7, 1.8, 1.9)), tk((0, 5, 10)), "height h (m)", "1/ω₀ vs 1.6 m (%)", grid=(5,)))
    o.append(B.curve(hs, clk, SER[0]))
    o.append(B.curve(hs, clk_n, SER[1], multi=True, dash=(7, 4)))
    o.append(dot(B, 1.9, clk[-1], O["flag"]))
    o.append(label(s, B.X(1.9) + 8, B.Y(clk[-1]) - 2, f"+{clk[-1]:.1f} %", "label2", I["primary"]))
    o.append(label(s, B.X(1.9) + 8, B.Y(clk_n[-1]) + 14, f"+{clk_n[-1]:.1f} % (√h)", "label2", I["primary"]))
    o.append(legend(s, 66, 246, [(SER[0], "ℓ = 0.55h − 0.06", None), (SER[1], "ℓ = 0.55h", (7, 4))]))
    aria = (f"Problem K4, two panels against height from 1.6 to 1.9 m. Top: the toppling rate omega-zero = root of g over "
            f"l with l = 0.55 h minus 0.06 m, falling from {w0[0]:.2f} to {w0[-1]:.2f} per second, an "
            f"{100*(1-w0[-1]/w0[0]):.1f} percent drop. Bottom: the toppling clock 1 over omega-zero, and with it the "
            f"tolerable delay, relative to the 1.6 m person: {clk[-1]:.1f} percent longer at 1.9 m (red), against "
            f"{clk_n[-1]:.1f} percent if l were 0.55 h (blue dashed, the root-h scaling).")
    pa = hov(A, hs, [w0], lambda i: f"h = {hs[i]:.3f} m: ω₀ = {w0[i]:.3f} s⁻¹")
    pb = hov(B, hs, [clk, clk_n], lambda i: f"h = {hs[i]:.3f} m: +{clk[i]:.2f} % (ankle offset), +{clk_n[i]:.2f} % (√h)")
    return svg(VB, aria, s, "".join(o), ([(A.box, pa), (B.box, pb)],))


# ================================================================ #50 K5: fastest recovery inside the island
def fig50():
    VB = (0, 0, W, 490)
    s = H.Scale(W, VB[3], display_w=400)
    kpo, kdo, smax = k5_opt()
    s940 = -rightmost(940.0, 260.0, D_TRUE)
    assert (round(kpo), round(kdo), round(smax, 2), round(kpo / MGL, 2), round(s940, 2)) == (785, 256, 3.42, 1.27, 1.46)
    A = Plot(s, (66, 40, 376, 216), (500, 2000), (0, 750))                 # line 866
    kp, kd = hopf(D_TRUE)
    o = [f'<polygon points="{" ".join(f"{A.X(a):.1f},{A.Y(b):.1f}" for a, b in zip(kp, kd))}" fill="{O["neural"]}" '
         f'opacity="0.12"/>']
    o.append(A.axes(tk((500, 1000, 1500, 2000)), tk((0, 250, 500, 750)), f"K{sub('p', s)} (N·m/rad)",
                    f"K{sub('d', s)} (N·m·s/rad)"))
    o.append(A.curve(kp, kd, O["neural"], multi=True))
    o.append(H.line(s, A.X(MGL), A.y1, A.X(MGL), A.y0, I["axis"], "ref", H.DASH_REF))
    o.append(dot(A, kpo, kdo, O["flag"], r=5))
    o.append(dot(A, 940, 260, SER[1], r=5))
    o.append(H.line(s, A.X(kpo) - 2, A.Y(kdo) - 6, A.X(700), A.Y(520) + 4, I["rule"], "leader"))
    o.append(label(s, A.X(660), A.Y(520), f"optimum ({kpo:.0f}, {kdo:.0f})", "label2", I["primary"]))
    o.append(label(s, A.X(940) + 4, A.Y(260) - 10, f"(940, 260): σ = {s940:.2f}", "label2", I["primary"]))
    o.append(label(s, A.X(1500), A.y1 + 14, "island, Δ = 0.15 s", "label2", I["secondary"]))
    B = Plot(s, (66, 290, 376, 426), (500, 2000), (0, 3.6))
    ks = sorted(set(np.round(np.linspace(MGL + 2, kp.max() - 2, 70), 3).tolist()
                    + np.round(np.linspace(750, 800, 26), 3).tolist() + [round(kpo, 3)]))
    sb = [smax if k == round(kpo, 3) else sigma_best(k)[0] for k in ks]
    o.append(B.axes(tk((500, 1000, 1500, 2000)), tk((0, 1, 2, 3)), f"K{sub('p', s)} (N·m/rad), K{sub('d', s)} best",
                    "decay rate σ (s⁻¹)", grid=(1, 2, 3)))
    o.append(B.curve(ks, sb, SER[0]))
    o.append(dot(B, kpo, smax, O["flag"]))
    o.append(H.line(s, B.X(kpo) + 5, B.Y(smax) - 2, B.X(1140) - 4, B.Y(3.25) - 4, I["rule"], "leader"))
    o.append(label(s, B.X(1140), B.Y(3.25), f"σ{sub('max', s, 'label2')} = {smax:.2f} s⁻¹ at {kpo/MGL:.2f} Mgℓ", "label2",
                   I["primary"]))
    o.append(label(s, B.X(1140), B.Y(3.25) + 17, f"recovery time 1/σ = {1/smax:.2f} s", "label2", I["primary"]))
    aria = (f"Problem K5, delay 0.15 s, two panels. Top: the green stable island in the gain plane with the optimum gain "
            f"pair Kp = {kpo:.0f}, Kd = {kdo:.0f} (orange dot) well inside it and the softer pair (940, 260) (blue dot), "
            f"which recovers at {s940:.2f} per second. Bottom: the best decay rate at each Kp with Kd optimised, rising "
            f"from 0 at Kp = Mgl to a peak of {smax:.2f} per second at Kp = {kpo:.0f} ({kpo/MGL:.2f} Mgl) and falling to "
            "0 at the island's right tip.")
    pa_k = np.linspace(MGL + 5, kp.max() - 5, 100)
    pa = []
    for k in pa_k:
        lo, hi = island_kd(D_TRUE, k)
        pa.append([A.X(k), [A.Y(lo), A.Y(hi)], f"Kp = {k:.0f}: stable for Kd {lo:.0f}–{hi:.0f}"])
    pb = hov(B, ks, [sb], lambda i: f"Kp = {ks[i]:.0f}: best σ = {sb[i]:.2f} s⁻¹")
    return svg(VB, aria, s, "".join(o), ([(A.box, pa), (B.box, pb)],))


# ================================================================ #51 K6: largest recoverable shove
D_TOE, D_HEEL, X_COM0 = 0.12, 0.05, 0.02       # m (line 176)


def fig51():
    VB = (0, 0, W, 420)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m7f51_"
    m_toe = D_TOE - X_COM0
    jmax = M_B * W0 * m_toe
    assert (round(m_toe, 2), round(W0, 2), round(jmax / M_B, 2), round(jmax, 1), round(M_B * W0)) == (0.10, 3.06, 0.31, 21.4, 214)
    A = Plot(s, (66, 40, 388, 196), (0, 32), (0, 0.15))                                       # line 870
    js = np.linspace(0, 32, 65)
    o = [f"<defs>{H.markers(p, s)}</defs>",
         f'<rect x="{A.X(jmax):.2f}" y="{A.y1}" width="{A.x1 - A.X(jmax):.2f}" height="{A.y0 - A.y1}" fill="{O["force"]}" opacity="0.08"/>']
    o.append(A.axes(tk((0, 10, 20, 30)), tk((0, 0.05, 0.10, 0.15), "{:.2f}"), "shove impulse J (N·s)", "ξ − x_com (m)"
                    .replace("x_com", f"x{sub('com', s)}"), grid=(0.05,)))
    o.append(ref(s, A, m_toe, O["flag"]))
    o.append(A.curve(js, js / (M_B * W0), SER[0]))
    o.append(dot(A, jmax, m_toe, O["flag"], r=5))
    o.append(label(s, A.x0 + 6, A.Y(m_toe) - 8, f"toe margin m{sub('toe', s, 'label2')} = {m_toe:.2f} m", "label2", I["primary"]))
    o.append(label(s, A.X(jmax) + 8, A.Y(0.03), "step", "label2", I["primary"]))
    o.append(label(s, A.X(jmax) + 8, A.Y(0.03) + 16, "required", "label2", I["primary"]))
    o.append(label(s, A.X(jmax) + 8, A.Y(m_toe) + 22, f"J{sub('max', s, 'label2')} = {jmax:.1f} N·s", "label2", I["primary"]))
    o.append(label(s, A.X(3), A.Y(0.13), f"slope 1/(Mω₀) = 1/{M_B*W0:.0f} m per N·s", "label2", I["secondary"]))
    # panel B: the base of support at J = Jmax (sagittal, metres)
    X = lambda x: 70 + (x + 0.07) / 0.22 * 300                     # noqa: E731
    yc, yb = 318, 356                                              # COM row, top of the base-of-support bar
    o.append(label(s, 30, 268, f"at J{sub('max', s, 'label2')} the extrapolated COM ξ reaches the toe edge", "label2",
                   I["primary"]))
    o.append(f'<rect x="{X(-D_HEEL):.2f}" y="{yb:.2f}" width="{X(D_TOE) - X(-D_HEEL):.2f}" height="12" fill="{BOX}" '
             f'stroke="{I["rule"]}" stroke-width="1"/>')
    o.append(H.line(s, 30, yb + 12, 390, yb + 12, I["axis"], "axis"))
    for x in (-D_HEEL, D_TOE):
        o.append(H.line(s, X(x), yc - 18, X(x), yb, I["rule"], "leader", H.DASH_REF))
    o.append(label(s, X(-D_HEEL), yb + 30, "heel", "label2", I["secondary"], "middle"))
    o.append(label(s, X(D_TOE), yb + 30, "toe", "label2", I["secondary"], "middle"))
    o.append(label(s, (X(0) + X(D_TOE)) / 2, yb + 30, "base of support", "label2", I["secondary"], "middle"))
    o.append(label(s, 200, yb + 50, f"heel {D_HEEL:.2f} m behind the ankle, toe {D_TOE:.2f} m ahead", "label2",
                   I["secondary"], "middle"))
    o.append(H.joint_centre(s, X(0), yb - 8))
    o.append(label(s, X(0) - 10, yb - 4, "ankle", "label2", I["secondary"], "end"))
    o.append(H.com_mark(s, X(X_COM0), yc))
    o.append(f'<circle cx="{X(D_TOE):.2f}" cy="{yc:.2f}" r="6" fill="#fff" stroke="{O["flag"]}" stroke-width="2"/>')
    o.append(label(s, X(D_TOE) + 10, yc + 5, "ξ", "label", I["primary"]))
    o.append(H.arrow(s, p, X(X_COM0) + 9, yc, X(D_TOE) - 8, yc, "geometry"))
    o.append(label(s, (X(X_COM0) + X(D_TOE)) / 2, yc - 9, f"J/(Mω₀) = {m_toe:.2f} m", "label2", I["primary"], "middle"))
    o.append(H.arrow(s, p, X(X_COM0) - 80, yc, X(X_COM0) - 10, yc, "load"))
    o.append(label(s, X(X_COM0) - 80, yc - 9, "shove J", "label2", I["primary"]))
    o.append(label(s, X(X_COM0), yc + 24, "COM", "label2", I["primary"], "middle"))
    aria = (f"Problem K6, two panels. Top: the jump of the extrapolated centre of mass, J over M omega-zero, against the "
            f"shove impulse J from 0 to 32 N s, a straight line of slope 1 over {M_B*W0:.0f}; it meets the dashed toe "
            f"margin of {m_toe:.2f} m at J = {jmax:.1f} N s, beyond which (shaded) a step is required. Bottom: the base "
            f"of support from the heel, {D_HEEL:.2f} m behind the ankle, to the toe, {D_TOE:.2f} m ahead; the COM sits "
            f"{X_COM0:.2f} m ahead of the ankle and, at the largest shove, the extrapolated COM (open orange circle) lies "
            f"{m_toe:.2f} m further forward, on the toe edge.")
    pa = hov(A, js, [js / (M_B * W0)], lambda i: f"J = {js[i]:.1f} N·s: ξ − x = {js[i]/(M_B*W0):.3f} m"
             + (" (step needed)" if js[i] > jmax else ""))
    return svg(VB, aria, s, "".join(o), (A.box, pa))


# ================================================================ #52 K7: COP swings wider than COM
def fig52():
    VB = (0, 0, W, 440)
    s = H.Scale(W, VB[3], display_w=400)
    t, com, cop = sway(K7_SEED)
    rc, rp = rms_mm(com), rms_mm(cop)
    fr, F = welch(com, fs=1000.0, nperseg=2 ** 16)             # COM spectrum, 65.5 s segments
    fpk = float(fr[int(F.argmax())])
    amp = 1 + (2 * math.pi * fpk) ** 2 / W0 ** 2
    assert (round(rc, 1), round(rp, 1), round(rp / rc, 2), round(fpk, 2), round(amp, 2)) == (4.5, 6.8, 1.52, 0.35, 1.52), \
        (rc, rp, fpk, amp)                                                                     # line 874
    A = Plot(s, (66, 44, 346, 210), (30, 50), (-20, 20))
    k = slice(0, 20000, 20)
    tt, cc, pp = t[k], 1e3 * com[k], 1e3 * cop[k]
    o = [A.axes(tk((30, 35, 40, 45, 50)), tk((-20, 0, 20)), "time (s)", "AP position (mm)", grid=(0,))]
    o.append(A.curve(tt, pp, SER[1], multi=True, nmax=1000))
    o.append(A.curve(tt, cc, I["primary"], multi=True, nmax=1000))
    last = tt > 47.0                                           # direct labels at the last swing's peaks
    kp_, kc_ = int(np.argmax(np.where(last, pp, -1e9))), int(np.argmax(np.where(last, cc, -1e9)))
    yp, yc_ = A.Y(pp[kp_]), max(A.Y(cc[kc_]), A.Y(pp[kp_]) + 16)
    o.append(H.line(s, A.X(tt[kp_]) + 3, A.Y(pp[kp_]), 350, yp, I["rule"], "leader"))
    o.append(H.line(s, A.X(tt[kc_]) + 3, A.Y(cc[kc_]), 350, yc_, I["rule"], "leader"))
    o.append(label(s, 353, yp + 4, "COP", "label2", I["primary"]))
    o.append(label(s, 353, yc_ + 4, "COM", "label2", I["primary"]))
    o.append(legend(s, 66, 22, [(SER[1], "centre of pressure", None), (I["primary"], "centre of mass", None)]))
    # bars
    bx, by, sc = 120, 360, 12.0
    for i, (v, col, name) in enumerate(((rp, SER[1], "COP"), (rc, I["primary"], "COM"))):
        x = bx + i * 90
        o.append(f'<rect x="{x:.2f}" y="{by - sc*v:.2f}" width="56" height="{sc*v:.2f}" fill="{col}" opacity="0.85"/>')
        o.append(label(s, x + 28, by - sc * v - 6, f"{v:.1f} mm", "label2", I["primary"], "middle"))
        o.append(label(s, x + 28, by + 17, f"{name} RMS", "label2", I["secondary"], "middle"))
    o.append(H.line(s, bx - 10, by, bx + 156, by, I["axis"], "axis"))
    o.append(label(s, 290, 300, f"ratio {rp/rc:.2f}", "label", I["primary"]))
    o.append(label(s, 290, 318, f"= 1 + (2πf)²/ω₀²", "label2", I["secondary"]))
    o.append(label(s, 290, 335, f"at f = {fpk:.2f} Hz", "label2", I["secondary"]))
    o.append(label(s, 30, 404, f"600 s run, K{sub('p', s, 'label2')} = 900, K{sub('d', s, 'label2')} = 120, Δ = 0.12 s, noise 0.35 N·m·s½", "label2", I["secondary"]))
    o.append(label(s, 30, 421, f"Prop 3.3: COP = COM − (COM acceleration)/ω₀²", "label2", I["secondary"]))
    aria = (f"Problem K7, two panels from one 600 s simulation of the delayed closed loop with a random ankle torque. Top: "
            f"20 s of the anterior-posterior centre of pressure (blue) and centre of mass (black); the COP swings wider and "
            f"moves faster. Bottom: RMS excursions, COP {rp:.1f} mm and COM {rc:.1f} mm, a ratio of {rp/rc:.2f}, equal to "
            f"1 + (2 pi f) squared over omega-zero squared at the sway peak f = {fpk:.2f} Hz.")
    h = slice(0, 20000, 100)
    th_, hc, hp = t[h], 1e3 * com[h], 1e3 * cop[h]
    pa = hov(A, th_, [hp, hc], lambda i: f"t = {th_[i]:.1f} s: COP {hp[i]:.1f} mm, COM {hc[i]:.1f} mm")
    return svg(VB, aria, s, "".join(o), (A.box, pa))


# ================================================================ #53 K8: the price of recovery speed
def fig53():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    kpo, _, smax = k5_opt()
    k1, k2 = cheapest_kp(1.0), cheapest_kp(2.0)
    d1, d2 = sigma_best(round(k1, 6))[1], sigma_best(round(k2, 6))[1]
    assert (round(k1), round(k2), round(k1 / MGL, 2), round(k2 / MGL, 2), round(d1), round(d2)) == (660, 732, 1.07, 1.18, 185, 235), \
        (k1, k2, d1, d2)                                                                       # line 878
    P = Plot(s, (66, 44, 388, 226), (0, 3.6), (1.0, 1.3))
    ks = np.linspace(MGL + 0.5, kpo - 1, 50)
    sg = [sigma_best(round(float(k), 6))[0] for k in ks] + [smax]
    yk = [k / MGL for k in ks] + [kpo / MGL]
    o = [P.axes(tk((0, 1, 2, 3)), tk((1.0, 1.1, 1.2, 1.3), "{:.1f}"), "required decay rate σ (s⁻¹)",
                f"cheapest K{sub('p', s)} / Mgℓ", grid=(1.1, 1.2))]
    o.append(H.line(s, P.X(smax), P.y1, P.X(smax), P.y0, I["secondary"], "ref", H.DASH_REF))
    o.append(P.curve(sg, yk, SER[0]))
    for sv, kv in ((1.0, k1), (2.0, k2)):
        o.append(dot(P, sv, kv / MGL, O["flag"]))
    o.append(label(s, P.X(1.0) + 8, P.Y(k1 / MGL) + 18, f"{k1/MGL:.2f} Mgℓ ({k1:.0f})", "label2", I["primary"]))
    o.append(label(s, P.X(2.0) - 8, P.Y(k2 / MGL) - 10, f"{k2/MGL:.2f} Mgℓ ({k2:.0f})", "label2", I["primary"], "end"))
    o.append(label(s, P.X(smax) - 6, P.y0 - 26, f"σ{sub('max', s, 'label2')} = {smax:.2f} s⁻¹:", "label2", I["primary"], "end"))
    o.append(label(s, P.X(smax) - 6, P.y0 - 10, "no gain goes faster", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(0.2), P.Y(1.27), f"active part K{sub('p', s, 'label2')} − Mgℓ:", "label2", I["secondary"]))
    o.append(label(s, P.X(0.2), P.Y(1.27) + 16, f"{k1-MGL:.0f} → {k2-MGL:.0f} N·m/rad (×{(k2-MGL)/(k1-MGL):.1f})", "label2",
                   I["secondary"]))
    o.append(label(s, 66, 22, "Δ = 0.15 s, K_d optimised at each point".replace("K_d", f"K{sub('d', s, 'label2')}"), "label2",
                   I["secondary"]))
    aria = (f"Problem K8 plot at delay 0.15 s: the cheapest proportional gain, as a multiple of Mgl, that achieves each "
            f"required decay rate sigma with Kd optimised. It rises from 1 at sigma = 0 to {k1/MGL:.2f} Mgl ({k1:.0f}) at "
            f"sigma = 1 and {k2/MGL:.2f} Mgl ({k2:.0f}) at sigma = 2, then turns vertical at the dashed line sigma = "
            f"{smax:.2f} per second, where Kp = {kpo/MGL:.2f} Mgl: no gain goes faster.")
    order = np.argsort(sg)
    pts = [[P.X(sg[i]), P.Y(yk[i]), f"σ = {sg[i]:.2f} s⁻¹: Kp = {yk[i]*MGL:.0f} = {yk[i]:.3f} Mgℓ"] for i in order]
    return svg(VB, aria, s, "".join(o), (P.box, pts))


# ================================================================ #54 K9: heaviest load at 0.35 m
def fig54():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    m35, m15 = safe_load(0.35), safe_load(0.15)
    assert (round(m35, 1), round(m15, 1)) == (18.9, 42.6) and peak_compression(m35 - 1e-6, 0.35) < 3400  # line 882
    P = Plot(s, (66, 44, 388, 226), (0.10, 0.55), (0, 65))
    rs = np.linspace(0.10, 0.55, 91)
    ms = [safe_load(r) for r in rs]
    o = [f'<polygon points="{" ".join(f"{P.X(r):.1f},{P.Y(m):.1f}" for r, m in zip(rs, ms))} {P.X(0.55):.1f},{P.y0} '
         f'{P.X(0.10):.1f},{P.y0}" fill="{O["neural"]}" opacity="0.12"/>']
    o.append(P.axes(tk((0.1, 0.2, 0.3, 0.4, 0.5), "{:.1f}"), tk((0, 20, 40, 60)), f"reach r{sub('L', s)} (m)",
                    "maximum safe load (kg)", grid=(20, 40, 60)))
    o.append(H.line(s, P.X(0.35), P.Y(m35), P.X(0.35), P.y0, I["rule"], "leader", H.DASH_REF))
    o.append(P.curve(rs, ms, SER[0]))
    o.append(dot(P, 0.35, m35, O["flag"], r=5))
    o.append(dot(P, 0.15, m15, I["secondary"], hollow=True))
    o.append(label(s, P.X(0.35) + 8, P.Y(m35) - 12, f"0.35 m → {m35:.1f} kg", "label2", I["primary"]))
    o.append(label(s, P.X(0.15) + 9, P.Y(m15) - 4, f"0.15 m → {m15:.1f} kg", "label2", I["primary"]))
    o.append(label(s, P.X(0.115), P.Y(14), "safe: worst-case L5/S1", "label2", I["primary"]))
    o.append(label(s, P.X(0.115), P.Y(14) + 16, "compression below 3.4 kN", "label2", I["primary"]))
    o.append(label(s, 66, 22, "bisection on load, peak over flexion (Prop 8.2)", "label2", I["secondary"]))
    aria = (f"Problem K9 plot: the heaviest load whose worst-case L5/S1 compression stays below 3.4 kN, against reach "
            f"from 0.10 to 0.55 m, a red curve over a green safe region. It gives {m15:.1f} kg at 0.15 m (open dot) and "
            f"{m35:.1f} kg at 0.35 m (orange dot).")
    pts = hov(P, rs, [ms], lambda i: f"rL = {rs[i]:.3f} m: max safe load {ms[i]:.1f} kg")
    return svg(VB, aria, s, "".join(o), (P.box, pts))


FIGS = {
    46: ("K1: Using the method-of-steps DDE integrator of (computed pl", fig46),
    47: ("K2: Map the stability island in $(K_p,K_d)$ by grid simulati", fig47),
    48: ("Two computed inverse Hopf plots for K3. Left panel maps obse", fig48),
    49: ("K4: By how much does the tolerable neural delay change betwe", fig49),
    50: ("K5: For a fixed delay $\\Delta=0.15$ s, search the gain plane", fig50),
    51: ("Two-panel K6 capturability figure. Left panel plots extrapol", fig51),
    52: ("K7: Simulate a quiet-standing sway signal and compute the RM", fig52),
    53: ("K8: Co-contraction is how the nervous system buys the propor", fig53),
    54: ("K9: Compute the heaviest load that may be lifted at a reach ", fig54),
}
