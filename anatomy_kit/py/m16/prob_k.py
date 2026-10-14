"""Module 16 problem plots in the house style (group `prob_k`; svg #21 25 27 30 33 34 38 39 40 47), 400 px each.

Every plotted number is computed here from the formulas and code of module16.html:
  #21 C3  (line 552-554): rigid rotation F = R(theta): F changes, E = 1/2 (F^T F - I) = 0
  #25 C7  (line 568-570, Section 7, Fig. 10 data): linear 3 mu (lam - 1), neo-Hookean nominal mu (lam - lam^-2), fibre 0.6 (e^{48 e} - 1)
  #27 C9  (line 576-578, Prop. 8.1 line 355): sigma/sigma(0+) = g_inf + (1 - g_inf) F(T), Terzaghi series F(T), tau_0 = 4 L^2/(pi^2 c_v)
  #30 D2  (line 590-592): E = H + H^2/2 for a uniaxial gradient H, eps = H
  #33 D5  (line 602-604): sigma = E eps; mu = E/(2(1+nu)), lambda = E nu/((1+nu)(1-2 nu)), K = lambda + 2 mu/3 (E 17 GPa, nu 0.3)
  #34 D6  (line 606-608): W = 1/2 sigma eps = 1/2 E eps^2 and sigma = dW/d eps
  #38 D10 (line 622-624): neo-Hookean nominal stress against the linear law, ratio -> 1 as lambda -> 1
  #39 K1  (line 629-631, Lab A): FE error of the tapered bar, 1.1e-2 -> 1.1e-5, slope -2
  #40 K2  (line 633-635 and its code, 64 elements): tip displacement against E; 17.00 GPa, 0.99 % and 4.76 %, 0.816 um
  #47 K7  (line 710-713): d sigma/d lam = mu (2 lam + 1/lam^2), 0.0, 0.2, 0.9, 3.1, 14.8 % above 3 mu
This file does NOT expose SHARED_DEFS (the Lynch body kit is exposed by m16/body_main.py; nothing here draws a body).
"""
import math

import numpy as np

import house as H
from m05.plots_prob import Plot, hov, label, legend, sub, svg

O, I, SER, T = H.OVERLAY, H.INK, H.SERIES, H.TISSUE
RED, BLUE, ORANGE = SER[0], SER[1], SER[2]
W = 400
BOX = "#f7f4ef"
GRID = "#e6e6e6"


def sup(t, s, size="tick"):
    return f'<tspan baseline-shift="super" font-size="{s(H.PX[size] * 0.7):.2f}">{t}</tspan>'


def dot(P, x, y, col, hollow=False):
    s = P.s
    r = s(H.PX["dot"])
    if hollow:
        return f'<circle cx="{P.X(x):.2f}" cy="{P.Y(y):.2f}" r="{r:.2f}" fill="#fff" stroke="{col}" stroke-width="{s(1.8):.2f}"/>'
    return f'<circle cx="{P.X(x):.2f}" cy="{P.Y(y):.2f}" r="{r:.2f}" fill="{col}" stroke="#fff" stroke-width="{s(1.5):.2f}"/>'


def href(s, P, y, col=None):
    return H.line(s, P.x0, P.Y(y), P.x1, P.Y(y), col or I["secondary"], "ref", H.DASH_REF)


def vref(s, P, x, y_to, col=None):
    return H.line(s, P.X(x), P.Y(y_to), P.X(x), P.y0, col or I["secondary"], "ref", H.DASH_REF)


def tk(vals, f="{:g}"):
    return [(v, f.format(v).replace("-", "−")) for v in vals]


def band(P, x0, y0, x1, y1, col, op=1.0):
    return (f'<rect x="{P.X(x0):.2f}" y="{P.Y(y1):.2f}" width="{P.X(x1) - P.X(x0):.2f}" '
            f'height="{P.Y(y0) - P.Y(y1):.2f}" fill="{col}" opacity="{op}"/>')


def tag(s, x, y, col, text, dashed=False):
    """Direct label: a short coloured mark, then ink text."""
    return [H.line(s, x, y - 4.5, x + 20, y - 4.5, col, "curve_multi", H.DASH_REF if dashed else None),
            label(s, x + 25, y, text, "label2", I["primary"])]


# ================================================================ #21 C3: rotation is not strain
def fig21():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 66, 388, 226), (0, 90), (0, 2.2))
    th = np.linspace(0, 90, 91)
    dF, nE = [], []
    for a in th:
        r = math.radians(a)
        F = np.array([[math.cos(r), -math.sin(r)], [math.sin(r), math.cos(r)]])
        dF.append(float(np.linalg.norm(F - np.eye(2))))                           # Frobenius norm of F - I
        nE.append(float(np.linalg.norm(0.5 * (F.T @ F - np.eye(2)))))              # Frobenius norm of E
    dF, nE = np.array(dF), np.array(nE)
    assert nE.max() < 1e-12 and abs(dF[-1] - 2.0) < 1e-12 and abs(dF[45] - 2 * math.sqrt(1 - math.cos(math.pi / 4))) < 1e-12
    o = [P.axes(tk((0, 30, 60, 90), "{:g}°"), tk((0, 0.5, 1.0, 1.5, 2.0), "{:g}"),
                "rigid rotation angle", "size of the change (Frobenius norm)", grid=(0.5, 1.0, 1.5, 2.0))]
    o.append(P.curve(th, dF, RED))
    o.append(P.curve(th, nE, BLUE))
    o += tag(s, 58, 18, RED, "F − I  (the gradient changes)")
    o += tag(s, 58, 38, BLUE, "E = ½(F" + sup("T", s, "label2") + "F − I)  (stays zero)")
    o.append(label(s, P.X(12), P.Y(1.15), f"F − I = {dF[-1]:.2f} at 90°", "label2", I["primary"]))
    o.append(label(s, P.X(45), P.Y(0) - 10, "E = 0 for every rotation", "label2", I["primary"], "middle"))
    o.append(dot(P, 90, dF[-1], I["primary"]))
    o.append(dot(P, 90, 0, I["primary"]))
    aria = ("Problem C3 plot. A body is rotated rigidly from 0 to 90 degrees. The red curve, the size of F minus the identity, "
            "rises from 0 to 2 because the deformation gradient F becomes a rotation matrix. The blue Green-Lagrange strain "
            "E, one half of F transpose F minus the identity, stays exactly zero for every angle, so it measures strain and F does not.")
    hv = hov(P, th, [dF, nE], lambda i: f"rotation {th[i]:.0f}°: size of F − I = {dF[i]:.3f}, size of E = {nE[i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #25 C7: linear against finite-strain laws
MU, K_FIB, A_FIB = 200.0, 48.0, 0.6


def lin(l):
    return 3 * MU * (l - 1)


def neo_nom(l):
    return MU * (l - l ** -2.0)


def fib(l):
    return A_FIB * (np.exp(K_FIB * (l - 1)) - 1)


def fig25():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 80, 340, 240), (1.0, 1.10), (0, 80))
    lam = np.linspace(1.0, 1.10, 201)
    assert abs(lin(1.1) - 60) < 1e-9 and abs(fib(1.1) - 72.3) < 0.1 and abs(neo_nom(1.1) - 54.71) < 0.01
    o = [P.axes(tk((1.0, 1.05, 1.10), "{:.2f}"), tk((0, 20, 40, 60, 80)), "stretch λ", "nominal stress P (MPa)", grid=(20, 40, 60, 80))]
    o.append(P.curve(lam, lin(lam), BLUE, multi=True, dash=(7, 4)))
    o.append(P.curve(lam, neo_nom(lam), ORANGE, multi=True))
    o.append(P.curve(lam, fib(lam), RED))
    o += tag(s, 58, 16, BLUE, "linear law, slope 3μ = 600 MPa", True)
    o += tag(s, 58, 34, ORANGE, "neo-Hookean, μ = 200 MPa")
    o += tag(s, 58, 52, RED, "fibre-reinforced (exponential)")
    for v, y, dy in ((fib(1.1), P.Y(fib(1.1)), 4), (lin(1.1), P.Y(lin(1.1)), 0), (neo_nom(1.1), P.Y(neo_nom(1.1)), 12)):
        o.append(label(s, P.x1 + 7, y + dy + 1, f"{v:.0f}", "label2", I["primary"]))
    aria = ("Problem C7 plot. Nominal stress against stretch from 1.00 to 1.10 for three laws. The blue dashed straight line, the linear law "
            "with slope 3 mu equal to 600 megapascals, reaches 60. The orange neo-Hookean curve, from an energy of the full deformation "
            "gradient, bends slightly below it, to 55. The red fibre-reinforced exponential law is nearly flat at first, then rises "
            "steeply to 72 megapascals, so the linear law fails to follow it at large stretch.")
    hv = hov(P, lam, [lin(lam), neo_nom(lam), fib(lam)],
             lambda i: f"λ = {lam[i]:.3f}: linear {lin(lam[i]):.1f}, neo-Hookean {neo_nom(lam[i]):.1f}, fibre {fib(lam[i]):.1f} MPa")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #27 C9: a draining solid relaxes
def terzaghi(Tv, n=80):
    Tv = np.asarray(Tv, dtype=float)
    return sum(8 / ((2 * k + 1) ** 2 * math.pi ** 2) * np.exp(-((2 * k + 1) * math.pi / 2) ** 2 * Tv) for k in range(n))


G_INF = 0.2                      # illustrative equilibrium share; the module states no value


def fig27():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 62, 388, 226), (0, 1.0), (0, 1.0))
    Tt = np.linspace(0, 1, 201)
    F = terzaghi(Tt)
    sig = G_INF + (1 - G_INF) * F
    assert abs(F[0] - 1.0) < 0.02 and abs(float(terzaghi(0.5)) - 0.2360) < 0.0005          # line 355 / Lab C
    T0 = 4 / math.pi ** 2                                                                  # tau_0 = 4 L^2/(pi^2 c_v)
    s0 = G_INF + (1 - G_INF) * float(terzaghi(T0))
    o = [P.axes(tk((0, 0.25, 0.5, 0.75, 1.0), "{:g}"), tk((0, 0.5, 1.0)), "time T = c" + sub("v", s) + "t / L²",
                "stress σ(t) / σ(0⁺)", grid=(0.5, 1.0))]
    o.append(href(s, P, G_INF))
    o.append(vref(s, P, T0, s0))
    o.append(P.curve(Tt[::2], sig[::2], RED))
    o.append(dot(P, 0, 1.0, I["primary"]))
    o.append(dot(P, T0, s0, I["primary"], hollow=True))
    o.append(label(s, P.X(0.04), P.Y(1.0) + 2, "σ(0⁺): the fluid has not moved yet", "label2", I["primary"], "start"))
    o.append(label(s, P.x1 - 4, P.Y(G_INF) + 17, f"σ∞ = {G_INF} σ(0⁺) (illustrative)", "label2", I["primary"], "end"))
    o.append(label(s, P.X(T0) + 8, P.Y(0.80), "slowest mode τ" + sub("0", s, "label2"), "label2", I["primary"]))
    o.append(label(s, P.X(T0) + 8, P.Y(0.80) + 16, f"T = 4/π² = {T0:.3f}", "label2", I["primary"]))
    o.append(label(s, 58, 30, "elastic matrix + seeping fluid, no viscous element", "label2", I["secondary"]))
    aria = ("Problem C9 plot. Stress after a step strain of an elastic solid soaked in fluid, against dimensionless time T equal to "
            "c v t over L squared. The red curve starts at the instantaneous value, when the fluid has not moved, and falls to a dashed "
            "equilibrium level of 0.2 of it, the equilibrium value being illustrative. The fall follows the Terzaghi series, a sum of "
            "decaying exponentials, so the poroelastic tissue relaxes like a viscoelastic one; the slowest decay time 4 L squared over "
            "pi squared c v is marked at T equal to 0.405.")
    hv = hov(P, Tt, [sig], lambda i: f"T = {Tt[i]:.3f}: σ/σ(0⁺) = {sig[i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #30 D2: E reduces to epsilon for small H
def fig30():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 66, 388, 226), (0, 0.5), (0, 0.8))
    h = np.linspace(0, 0.5, 201)
    eps = h
    E = h + 0.5 * h ** 2                      # 1/2 (H + H^T) + 1/2 H^T H for H = h e1 x e1
    assert abs(E[-1] - 0.625) < 1e-12 and abs(0.5 * 0.1 ** 2 / 0.1 - 0.05) < 1e-12
    o = [band(P, 0, 0, 0.1, 0.8, BOX)]
    o.append(P.axes(tk((0, 0.1, 0.2, 0.3, 0.4, 0.5), "{:g}"), tk((0, 0.2, 0.4, 0.6, 0.8), "{:g}"),
                    "displacement gradient H", "strain", grid=(0.2, 0.4, 0.6, 0.8)))
    o.append(P.curve(h, eps, BLUE, multi=True, dash=(7, 4)))
    o.append(P.curve(h, E, RED))
    o += tag(s, 58, 18, BLUE, "ε = ½(H + H" + sup("T", s, "label2") + ")  (small strain)")
    o += tag(s, 58, 38, RED, "E = ε + ½H" + sup("T", s, "label2") + "H  (Green–Lagrange)")
    xg = 0.5
    o.append(H.line(s, P.X(xg), P.Y(xg), P.X(xg), P.Y(xg + 0.5 * xg ** 2), I["primary"], "geom"))
    o.append(label(s, P.X(xg) - 8, P.Y(0.14), "dropped term ½H²", "label2", I["primary"], "end"))
    o.append(label(s, P.X(xg) - 8, P.Y(0.14) + 16, f"= {0.5 * xg ** 2:.3f} at H = {xg}", "label2", I["primary"], "end"))
    o.append(label(s, P.X(0.0) + 4, P.Y(0.8) + 16, "H ≪ 1", "label2", I["primary"]))
    o.append(label(s, P.X(0.0) + 4, P.Y(0.8) + 32, "gap < 5% of ε", "label2", I["secondary"]))
    aria = ("Problem D2 plot, one dimension. Strain against the displacement gradient H from 0 to 0.5. The blue dashed line is the "
            "small strain epsilon equal to H. The red curve is the Green-Lagrange strain E equal to H plus one half H squared. The two "
            "coincide for small H, where the dropped quadratic term is under 5 percent of epsilon below H equal to 0.1, and separate by "
            "one half H squared, 0.125, at H equal to 0.5.")
    hv = hov(P, h, [eps, E], lambda i: f"H = {h[i]:.3f}: ε = {eps[i]:.3f}, E = {E[i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #33 D5: the isotropic law
E_BONE, NU = 17.0, 0.3                     # GPa, cortical bone (Section 5 listing, table)


def fig33():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 40, 372, 226), (0, 0.4), (0, 80))
    mu = E_BONE / (2 * (1 + NU))
    lam_ = E_BONE * NU / ((1 + NU) * (1 - 2 * NU))
    K = lam_ + 2 * mu / 3
    assert abs(mu - 6.538) < 1e-3 and abs(lam_ - 9.808) < 1e-3 and abs(K - E_BONE / (3 * (1 - 2 * NU))) < 1e-12
    e = np.linspace(0, 0.4, 81)                 # percent
    sg = E_BONE * 1e3 * e / 100                 # MPa
    o = [P.axes(tk((0, 0.1, 0.2, 0.3, 0.4), "{:g}%"), tk((0, 20, 40, 60, 80)), "axial strain ε", "axial stress σ (MPa)",
                grid=(20, 40, 60, 80))]
    o.append(P.curve(e, sg, RED))
    a, b = 0.1, 0.3
    o.append(H.line(s, P.X(a), P.Y(E_BONE * 10 * a), P.X(b), P.Y(E_BONE * 10 * a), O["geometry"], "geom"))
    o.append(H.line(s, P.X(b), P.Y(E_BONE * 10 * a), P.X(b), P.Y(E_BONE * 10 * b), O["geometry"], "geom"))
    o.append(label(s, P.X(0.22), P.Y(E_BONE * 10 * a) - 7, "Δε", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(b) + 8, P.Y(E_BONE * 10 * (a + b) / 2) + 4, "Δσ", "label2", I["primary"]))
    o.append(label(s, P.x1 - 4, P.Y(5), f"slope E = Δσ/Δε = {E_BONE:g} GPa", "label2", I["primary"], "end"))
    x0 = P.x0 + 8
    o.append(label(s, x0, P.y1 + 18, "σ = λ(tr ε)I + 2με", "label2", I["secondary"]))
    o.append(label(s, x0, P.y1 + 35, f"E = {E_BONE:g} GPa, ν = {NU} (cortical bone)", "label2", I["secondary"]))
    o.append(label(s, x0, P.y1 + 52, f"μ = E / 2(1+ν) = {mu:.2f} GPa", "label2", I["primary"]))
    o.append(label(s, x0, P.y1 + 69, f"λ = Eν / ((1+ν)(1−2ν)) = {lam_:.2f} GPa", "label2", I["primary"]))
    o.append(label(s, x0, P.y1 + 86, f"K = λ + 2μ/3 = {K:.2f} GPa", "label2", I["primary"]))
    aria = ("Problem D5 plot. Uniaxial stress against axial strain for the isotropic law with Young's modulus 17 gigapascals and "
            "Poisson's ratio 0.3, cortical bone: a straight red line of slope E, with a slope triangle of run delta epsilon and rise "
            "delta sigma. Printed values from the Lame relations: shear modulus 6.54 gigapascals, lambda 9.81, bulk modulus 14.17.")
    hv = hov(P, e, [sg], lambda i: f"ε = {e[i]:.2f}%: σ = Eε = {sg[i]:.1f} MPa")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #34 D6: strain energy
def fig34():
    VB = (0, 0, W, 312)
    s = H.Scale(W, VB[3], display_w=400)
    A = Plot(s, (60, 62, 176, 226), (0, 0.4), (0, 80))
    B = Plot(s, (262, 62, 380, 226), (0, 0.4), (0, 140))
    e = np.linspace(0, 0.4, 81)                          # percent
    sg = E_BONE * 1e3 * e / 100                          # MPa
    Wd = 0.5 * E_BONE * 1e9 * (e / 100) ** 2 / 1e3       # kJ/m^3
    es = 0.30
    ss = E_BONE * 1e3 * es / 100
    Ws = 0.5 * E_BONE * 1e9 * (es / 100) ** 2 / 1e3
    assert abs(ss - 51.0) < 1e-9 and abs(Ws - 0.5 * ss * 1e6 * (es / 100) / 1e3) < 1e-9 and abs(Ws - 76.5) < 1e-9
    slope = ss * 10                                      # dW/d eps in kJ/m^3 per percent = sigma(MPa) * 10
    o = [A.axes(tk((0, 0.2, 0.4), "{:g}%"), tk((0, 20, 40, 60, 80)), "strain ε", "stress σ (MPa)", grid=(20, 40, 60, 80), ytx=15)]
    o.append(B.axes(tk((0, 0.2, 0.4), "{:g}%"), tk((0, 50, 100)), "strain ε", "W (kJ/m³)", grid=(50, 100), ytx=214))
    tri = [(A.X(0), A.Y(0)), (A.X(es), A.Y(ss)), (A.X(es), A.Y(0))]
    o.append('<polygon points="' + " ".join(f"{x:.2f},{y:.2f}" for x, y in tri) + f'" fill="{RED}" opacity="0.14"/>')
    o.append(A.curve(e, sg, RED))
    o.append(H.line(s, A.X(es), A.Y(0), A.X(es), A.Y(ss), I["secondary"], "ref", H.DASH_REF))
    o.append(dot(A, es, ss, I["primary"]))
    o.append(label(s, A.X(0.19), A.Y(7), "W = ½σε", "label2", I["primary"], "middle"))
    o.append(label(s, A.x0, 36, "stress line: W is the area", "label2", I["primary"]))
    o.append(B.curve(e, Wd, RED))
    t0, t1 = 0.17, 0.40
    o.append(B.curve([t0, t1], [Ws + slope * (t0 - es), Ws + slope * (t1 - es)], O["dim"], multi=True, dash=(6, 4)))
    o.append(dot(B, es, Ws, I["primary"]))
    o.append(label(s, B.x0, 36, "W(ε) = ½Eε²: slope is σ", "label2", I["primary"]))
    o.append(label(s, B.X(es) - 8, B.Y(Ws) - 14, f"at {es:.2f}%:", "label2", I["secondary"], "end"))
    o.append(label(s, B.X(es) - 8, B.Y(Ws) + 2, f"W = {Ws:.1f}", "label2", I["primary"], "end"))
    o.append(label(s, 200, 294, f"E = {E_BONE:g} GPa; marked strain {es:.2f}%: σ = {ss:.0f} MPa, W = {Ws:.1f} kJ/m³", "label2",
                   I["secondary"], "middle"))
    aria = ("Problem D6, two panels with Young's modulus 17 gigapascals. Left: the straight stress-strain line with the triangle under "
            "it up to a marked strain of 0.30 percent shaded as the strain energy W equal to one half sigma epsilon, 76.5 kilojoules "
            "per cubic metre at stress 51 megapascals. Right: W as the parabola one half E epsilon squared, with the dashed tangent at "
            "the marked strain whose slope is the stress, sigma equal to dW over d epsilon.")
    pa = hov(A, e, [sg], lambda i: f"ε = {e[i]:.2f}%: σ = {sg[i]:.1f} MPa, W = ½σε = {Wd[i]:.1f} kJ/m³")
    pb = hov(B, e, [Wd], lambda i: f"ε = {e[i]:.2f}%: W = {Wd[i]:.1f} kJ/m³, slope σ = {sg[i]:.1f} MPa")
    return svg(VB, aria, s, "".join(o), ([(A.box, pa), (B.box, pb)],))


# ================================================================ #38 D10: neo-Hookean -> linear
def fig38():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    A = Plot(s, (60, 62, 176, 226), (1.0, 1.10), (0, 70))
    B = Plot(s, (262, 62, 380, 226), (1.0, 1.10), (0.88, 1.0))
    lam = np.linspace(1.0, 1.10, 201)
    lam_r = lam[1:]
    ratio = neo_nom(lam_r) / lin(lam_r)
    assert abs(neo_nom(1.0)) < 1e-12 and abs(MU * (1 + 2) - 3 * MU) < 1e-12 and 0.99 < ratio[0] < 1.0 and abs(ratio[-1] - 54.71 / 60) < 1e-3
    xt = tk((1.0, 1.05, 1.10), "{:.2f}")
    o = [A.axes(xt, tk((0, 20, 40, 60)), "stretch λ", "nominal stress P (MPa)", grid=(20, 40, 60), ytx=15)]
    o.append(B.axes(xt, tk((0.90, 0.95, 1.00), "{:.2f}"), "stretch λ", "P(neo-Hookean) / P(linear)", grid=(0.95, 1.0), ytx=212))
    o.append(A.curve(lam, lin(lam), BLUE, multi=True, dash=(7, 4)))
    o.append(A.curve(lam, neo_nom(lam), ORANGE, multi=True))
    o += tag(s, 58, 16, BLUE, "linear: 2με + λ(tr ε)I")
    o += tag(s, 58, 34, ORANGE, "neo-Hookean, μ = 200 MPa")
    o.append(label(s, 60, 54, "uniaxial, incompressible", "label2", I["secondary"]))
    o.append(label(s, A.X(1.0) + 6, A.Y(63), "same slope 3μ at λ = 1", "label2", I["primary"]))
    o.append(href(s, B, 1.0))
    o.append(B.curve(lam_r, ratio, ORANGE))
    o.append(dot(B, 1.0, 1.0, I["primary"], ))
    o.append(label(s, B.X(1.0) + 10, 54, "ratio → 1 as λ → 1", "label2", I["primary"]))
    o.append(label(s, B.X(1.10) - 4, B.Y(ratio[-1]) + 22, f"{ratio[-1]:.3f} at 1.10", "label2", I["primary"], "end"))
    aria = ("Problem D10, two panels with the stretch from 1.00 to 1.10 for a uniaxial incompressible solid of shear modulus 200 "
            "megapascals. Left: nominal stress of the neo-Hookean law, orange, and of the isotropic linear law, blue dashed; both start at "
            "the origin with the same slope 3 mu and the neo-Hookean curve bends below. Right: their ratio, which tends to 1 as the "
            "stretch tends to 1 and is 0.912 at 1.10.")
    pa = hov(A, lam, [lin(lam), neo_nom(lam)], lambda i: f"λ = {lam[i]:.3f}: linear {lin(lam[i]):.1f}, neo-Hookean {neo_nom(lam[i]):.1f} MPa")
    pb = hov(B, lam_r, [ratio], lambda i: f"λ = {lam_r[i]:.3f}: ratio {ratio[i]:.4f}")
    return svg(VB, aria, s, "".join(o), ([(A.box, pa), (B.box, pb)],))


# ================================================================ #39 K1 and #40 K2: the tapered bar (Lab A, K2 code)
E_, L_, P_, A0_ = 17e9, 0.10, 2000.0, 2e-4


def tip(nel, E=E_):
    xn = np.linspace(0, L_, nel + 1)
    Ael = A0_ * (1 - 0.5 * (xn[:-1] + xn[1:]) / 2 / L_)
    K = np.zeros((nel + 1, nel + 1))
    for e in range(nel):
        k = E * Ael[e] / (xn[e + 1] - xn[e])
        K[e:e + 2, e:e + 2] += k * np.array([[1, -1], [-1, 1]])
    fr = np.arange(1, nel + 1)
    u = np.zeros(nel + 1)
    u[fr] = np.linalg.solve(K[np.ix_(fr, fr)], np.eye(nel)[-1] * P_)
    return u[-1]


def sci(v):
    m, e = f"{v:.1e}".split("e")
    return f"{m}×10{str(int(e)).translate(str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹'))}"


def fig39():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    ns = [2, 4, 8, 16, 32, 64]
    u_exact = 2 * P_ * L_ / (E_ * A0_) * math.log(2)
    err = [abs(tip(n) - u_exact) / u_exact for n in ns]
    x = np.log2(ns)
    y = np.log10(err)
    slope = float(np.polyfit(np.log10(ns), y, 1)[0])
    assert abs(err[0] - 1.1e-2) < 0.05e-2 and abs(err[-1] - 1.1e-5) < 0.05e-5 and -2.1 < slope < -1.9, (err, slope)   # line 631
    assert 900 < err[0] / err[-1] < 1100                                                                            # "about 1000 = 4^5"
    P = Plot(s, (58, 66, 388, 226), (1, 6), (-6, -1))
    yt = [(float(e), "10" + sup(f"−{-e}", s)) for e in range(-6, 0)]
    o = [P.axes([(float(math.log2(n)), str(n)) for n in ns], yt, "elements N", "relative tip error", grid=[e for e in range(-5, 0)])]
    ref = [y[0] + 0.55 - 2 * (xx - 1) * math.log10(2) for xx in (1, 6)]
    o.append(P.curve([1, 6], ref, O["dim"], multi=True, dash=(7, 4)))
    o.append(P.curve(x, y, RED))
    for xx, yy in zip(x, y):
        o.append(dot(P, xx, yy, RED))
    o += tag(s, 58, 18, RED, f"computed error, fitted slope {slope:.2f}".replace("-", "−"))
    o += tag(s, 58, 38, O["dim"], "slope −2 reference, shifted up", True)
    o.append(label(s, P.X(1) + 4, P.Y(-3.8), f"{sci(err[0])} at N = 2", "label2", I["primary"]))
    o.append(label(s, P.X(6) - 4, P.Y(y[-1]) + 22, f"{sci(err[-1])} at N = 64", "label2", I["primary"], "end"))
    o.append(label(s, P.X(2.2), P.Y(-5.2) - 2, "each doubling of N:", "label2", I["secondary"]))
    o.append(label(s, P.X(2.2), P.Y(-5.2) + 14, "error falls fourfold", "label2", I["secondary"]))
    aria = ("Problem K1 plot. Relative error of the finite-element tip displacement of the tapered bar against the number of elements, "
            "2 to 64, on log-log axes: six red points on a straight line of slope about minus 2, from 1.1 times ten to the minus 2 at "
            "2 elements to 1.1 times ten to the minus 5 at 64, a factor of about 1000, with a dashed slope minus 2 reference line above.")
    hv = hov(P, x, [y], lambda i: f"N = {ns[i]}: error {err[i]:.2e}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


def fig40():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    u1 = tip(64, 1.0)                                   # K is proportional to E, so u(E) = u(1)/E exactly
    assert abs(tip(64, 17e9) - u1 / 17e9) < 1e-15
    uf = lambda Eg: u1 / (Eg * 1e9) * 1e6               # noqa: E731  micrometres, E in GPa
    meas = 81.55                                        # um, K2 statement (code: 8.155e-5 m)
    E_hat = u1 / (meas * 1e-6) / 1e9
    assert abs(E_hat - 17.00) < 0.005, E_hat                                            # "E = 17.00 GPa"
    e1 = 100 * abs(u1 / (meas * 1.01e-6) / 1e9 - E_hat) / E_hat
    e5 = 100 * abs(u1 / (meas * 1.05e-6) / 1e9 - E_hat) / E_hat
    assert round(e1, 2) == 0.99 and round(e5, 2) == 4.76 and abs(meas * 0.01 - 0.8155) < 1e-9     # lines 635 and code comments
    lo, hi = u1 / (meas * 1.05e-6) / 1e9, u1 / (meas * 0.95e-6) / 1e9
    P = Plot(s, (58, 40, 388, 226), (5, 30), (0, 300))
    Eg = np.linspace(5, 30, 126)
    uu = uf(Eg)
    o = [band(P, 5, meas * 0.95, 30, meas * 1.05, BLUE, 0.3)]
    o.append(P.axes(tk((5, 10, 17, 20, 25, 30)), tk((0, 100, 200, 300)), "Young's modulus E (GPa)", "tip displacement (µm)",
                    grid=(100, 200, 300)))
    o.append(P.curve(Eg, uu, RED))
    o.append(vref(s, P, E_hat, meas, I["secondary"]))
    o.append(href(s, P, meas, I["secondary"]))
    o.append(dot(P, E_hat, meas, I["primary"]))
    o.append(label(s, P.x1 - 4, P.Y(meas) - 30, f"measured {meas} µm", "label2", I["primary"], "end"))
    o.append(label(s, P.x1 - 4, P.Y(meas) - 14, f"E = {E_hat:.2f} GPa", "label2", I["primary"], "end"))
    x0 = P.x1 - 4
    o.append(label(s, x0, P.y1 + 18, "tinted band: ±5% in the reading", "label2", I["secondary"], "end"))
    o.append(label(s, x0, P.y1 + 35, f"+5% in u gives E {lo:.2f} GPa ({e5:.2f}% low)", "label2", I["primary"], "end"))
    o.append(label(s, x0, P.y1 + 52, f"−5% in u gives E {hi:.2f} GPa (+{100 * (hi - E_hat) / E_hat:.2f}%)", "label2", I["primary"], "end"))
    o.append(label(s, x0, P.y1 + 69, f"1% of u = {meas * 0.01:.3f} µm gives {e1:.2f}% in E", "label2", I["primary"], "end"))
    aria = ("Problem K2 plot. Tip displacement of the tapered bar under a 2 kilonewton load, from the 64-element finite-element model, "
            "against Young's modulus from 5 to 30 gigapascals: a red curve falling as one over E. The measured 81.55 micrometres "
            "marks E equal to 17.00 gigapascals. A tinted band of plus or minus 5 percent in the reading maps to E from 16.19 to "
            "17.89 gigapascals. A 1 percent reading error gives 0.99 percent in E, which is 0.816 micrometres of the reading.")
    hv = hov(P, Eg, [uu], lambda i: f"E = {Eg[i]:.1f} GPa: tip displacement {uu[i]:.1f} µm")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ================================================================ #47 K7: how much does neo-Hookean stiffen
def tangent(l):
    return 2 * l + 1 / l ** 2          # d sigma / d lambda in units of mu, Cauchy stress mu (l^2 - 1/l)


def fig47():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 62, 388, 226), (1.0, 1.5), (0, 4))
    lam = np.linspace(1.0, 1.5, 201)
    tg = tangent(lam)
    marks = (1.02, 1.05, 1.10, 1.20, 1.50)
    pct = [100 * (tangent(m) / 3 - 1) for m in marks]
    assert [round(v, 1) for v in pct] == [0.0, 0.2, 0.9, 3.1, 14.8] and abs(tangent(1.0) - 3.0) < 1e-12      # line 712
    o = [P.axes(tk((1.0, 1.1, 1.2, 1.3, 1.4, 1.5), "{:.1f}"), tk((0, 1, 2, 3, 4)), "stretch λ", "Cauchy tangent dσ/dλ (units of μ)", grid=(1, 2, 3, 4))]
    o.append(href(s, P, 3.0))
    o.append(P.curve(lam, tg, RED))
    for m in marks:
        o.append(dot(P, m, tangent(m), RED))
    for m, p in zip(marks[2:], pct[2:]):
        if m == 1.5:
            o.append(label(s, P.X(m) - 2, P.Y(tangent(m)) - 12, f"+{p:.1f}%  ({tangent(m):.2f}μ)", "label2", I["primary"], "end"))
        else:
            o.append(label(s, P.X(m), P.Y(tangent(m)) - 12, f"+{p:.1f}%", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(1.0) + 6, P.Y(3.0) + 18, "small-strain value 3μ", "label2", I["primary"]))
    o.append(label(s, 58, 30, "percent above 3μ at λ = 1.02 and 1.05: " + f"+{pct[0]:.1f}%, +{pct[1]:.1f}%", "label2", I["secondary"]))
    aria = ("Problem K7 plot. Tangent modulus of the Cauchy stress, d sigma over d lambda, of an incompressible neo-Hookean solid, in units of the shear modulus "
            "mu, against stretch from 1.0 to 1.5. The red curve starts at 3 mu, the small-strain value marked by a dashed line, and rises "
            "only slightly: 0.0, 0.2, 0.9, 3.1 and 14.8 percent above 3 mu at stretches 1.02, 1.05, 1.10, 1.20 and 1.50.")
    hv = hov(P, lam, [tg], lambda i: f"λ = {lam[i]:.3f}: tangent {tg[i]:.3f}μ, {100 * (tg[i] / 3 - 1):.1f}% above 3μ")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


FIGS = {
    21: ("C3: rotation is not strain. Why is the deformation gradient ", fig21),
    25: ("C7: when linear fails. Why does linear elasticity break at l", fig25),
    27: ("C9: biphasic is viscoelastic. Why does a purely elastic soli", fig27),
    30: ("D2: small strain from finite strain. Show the Green-Lagrange", fig30),
    33: ("D5: the isotropic law. Write the isotropic stress-strain law", fig33),
    34: ("D6: strain energy. Derive $W=\\tfrac12\\boldsymbol\\sigma:\\bold", fig34),
    38: ("D10: neo-Hookean to linear. Show the neo-Hookean stress redu", fig38),
    39: ("K1: convergence rate (regime + sensitivity). Fit the slope o", fig39),
    40: ("K2: recover the modulus, an inverse problem. A tapered bar o", fig40),
    47: ("K7: how much does a neo-Hookean solid actually stiffen? Comp", fig47),
}
