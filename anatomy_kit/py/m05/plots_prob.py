"""Module 5 problem-set plots (C6-C10, D3-D10, K1-K11): house-style redraws at 400 px.

Every plotted number is computed here from the formula or the script the module states
(the K-problem scripts are ported line for line; their printed numbers are asserted).
"""
import html
import math
from functools import lru_cache

import numpy as np

import house as H

O, I, SER = H.OVERLAY, H.INK, H.SERIES
GRID = "#e6e6e6"
BOX = "#f7f4ef"
W = 400                     # viewBox width = rendered width, so 1 user unit = 1 px


# ---------------------------------------------------------------- plot helpers
class Plot:
    """One plot box with linear scales. X, Y map data -> user units (one scale for ticks AND curves)."""

    def __init__(self, s, box, xr, yr):
        self.s, (self.x0, self.y1, self.x1, self.y0), self.xr, self.yr = s, box, xr, yr

    def X(self, v):
        return self.x0 + (v - self.xr[0]) / (self.xr[1] - self.xr[0]) * (self.x1 - self.x0)

    def Y(self, v):
        return self.y0 - (v - self.yr[0]) / (self.yr[1] - self.yr[0]) * (self.y0 - self.y1)

    @property
    def box(self):
        return [self.x0, self.y1, self.x1, self.y0]

    def axes(self, xt, yt, xtitle, ytitle, grid=(), ytx=None):
        s, o = self.s, []
        for g in grid:
            o.append(H.line(s, self.x0, self.Y(g), self.x1, self.Y(g), GRID, "leader"))
        o.append(H.line(s, self.x0, self.y0, self.x1, self.y0, I["axis"], "axis"))
        o.append(H.line(s, self.x0, self.y0, self.x0, self.y1, I["axis"], "axis"))
        for v, t in yt:
            o.append(H.line(s, self.x0 - 5, self.Y(v), self.x0, self.Y(v), I["axis"], "leader"))
            o.append(label(s, self.x0 - 8, self.Y(v) + 4.5, t, "tick", I["secondary"], "end"))
        for v, t in xt:
            o.append(H.line(s, self.X(v), self.y0, self.X(v), self.y0 + 5, I["axis"], "leader"))
            o.append(label(s, self.X(v), self.y0 + 19, t, "tick", I["secondary"], "middle"))
        o.append(label(s, (self.x0 + self.x1) / 2, self.y0 + 40, xtitle, "label", I["primary"], "middle"))
        yx = ytx if ytx is not None else 15
        yc = (self.y0 + self.y1) / 2
        o.append(label(s, yx, yc, ytitle, "label", I["primary"], "middle", f'transform="rotate(-90 {yx} {yc:.2f})"'))
        return "".join(o)

    def curve(self, xs, ys, col, multi=False, dash=None, nmax=120):
        xs, ys = list(xs), list(ys)
        k = -(-len(xs) // nmax)                      # stride that keeps <= nmax points, last point kept
        keep = list(range(0, len(xs), k)) + ([len(xs) - 1] if (len(xs) - 1) % k else [])
        pts = " ".join(f"{self.X(xs[i]):.1f},{self.Y(ys[i]):.1f}" for i in keep)
        da = f' stroke-dasharray="{self.s(dash[0]):.1f} {self.s(dash[1]):.1f}"' if dash else ""
        return (f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="'
                f'{self.s(H.PX["curve_multi" if multi else "curve"]):.2f}" stroke-linejoin="round"{da}/>')

    def dot(self, x, y, col):
        s = self.s
        return (f'<circle cx="{self.X(x):.2f}" cy="{self.Y(y):.2f}" r="{s(H.PX["dot"]):.2f}" fill="{col}" '
                f'stroke="#fff" stroke-width="{s(1.5):.2f}"/>')


def label(s, x, y, text, size="label", fill=I["primary"], anchor="start", extra=""):
    """H.label with the plot-text rule: text is always an INK colour (identity comes from swatch and placement)."""
    if fill not in I.values():
        fill = I["primary"]
    return H.label(s, x, y, text, size, fill, anchor, extra)


def legend(s, x, y, items, gap=16):
    """One row: short line swatch + name per series (identity never by colour alone)."""
    o = []
    for col, txt, dash in items:
        o.append(H.line(s, x, y - 4.5, x + 20, y - 4.5, col, "curve_multi", dash))
        o.append(label(s, x + 25, y, txt, "label2", I["secondary"]))
        x += 25 + text_w(txt, 13) + gap
    return "".join(o)


def text_w(txt, fs):
    """Rough rendered width of Georgia text (tags stripped), for layout only."""
    import re
    return len(re.sub(r"<[^>]+>", "", txt)) * fs * 0.5


def hov(P, xs, ys_list, fmt):
    """Hover points: x in user units, y (or list of y) in user units, text."""
    out = []
    for i, x in enumerate(xs):
        ys = [round(P.Y(y[i]), 2) for y in ys_list]
        out.append([round(P.X(x), 2), ys[0] if len(ys) == 1 else ys, fmt(i)])
    return out


def svg(vb, aria, s, body, hover=None):
    extra = H.hover_attr(*hover) if hover else ""
    return H.svg_open(vb, html.escape(aria), s, extra=extra) + body + "</svg>"


def sub(t, s, size="label"):
    return H.sub(t, s, size)


def vmax(s, size="label"):
    return f"v{sub('max', s, size)}"


# ---------------------------------------------------------------- module models
TAU_ACT, TAU_DEACT = 10.0, 40.0                    # ms, section 5 boxed activation law
C_HILL, K_ECC, F_ECC = 0.25, 20.0, 1.5             # section 6 f_V constants
FF, FR = 0.018, 0.020                              # 1/s, section 9 fatigue / recovery rates


def fV(v, c=C_HILL):
    """Section 6 boxed f_V, v = shortening velocity / vmax (negative = eccentric)."""
    if v >= 0:
        return (1 - v) / (1 + v / c)
    return 1 + (F_ECC - 1) * K_ECC * (-v) / (1 + K_ECC * (-v))


# K2 / K10 / K11 calcium pulse (section 3) and twitch-summation model (section 4)
TR, TD, TAU_A = 3.6, 18.0, 41.0
T_PK = TR * np.log(1 + TD / TR)
NORM = (1 - np.exp(-T_PK / TR)) * np.exp(-T_PK / TD)


def pulse(t, s=1.0):
    tt = np.clip(t, 0.0, None)
    y = (1 - np.exp(-tt / (TR * s))) * np.exp(-tt / (TD * s))
    return np.where(t > 0, y / NORM, 0.0)


def train_trace(f, s=1.0, T=1200.0, dt=0.1):
    """K2 train(): activation a(t) for an f Hz impulse train (first impulse at t = 0)."""
    t = np.arange(0.0, T, dt)
    prod = np.ones_like(t)
    for ti in np.arange(0.0, T, 1000.0 / f):
        prod *= 1 - pulse(t - ti, s)
    ca = 0.1 + 1.3 * (1 - prod)
    tgt = ca**3 / (1 + ca**3)
    a = np.zeros_like(t)
    for i in range(1, len(t)):
        a[i] = a[i - 1] + dt * (tgt[i - 1] - a[i - 1]) / (TAU_A * s)
    return t, a


def train(f, s=1.0, T=1200.0, dt=0.1):
    t, a = train_trace(f, s, T, dt)
    w = t > 0.6 * T
    return a[w].mean(), (a[w].max() - a[w].min()) / a[w].mean()


# ---------------------------------------------------------------- #47 C6: command and activation
def fig47():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 62, 388, 226), (0, 320), (0, 1.12))
    t = np.arange(0.0, 320.01, 1.0)
    u = np.where((t >= 20) & (t < 140), 1.0, 0.0)
    a140 = 1 - math.exp(-120 / TAU_ACT)
    a = np.where(t < 20, 0.0, np.where(t < 140, 1 - np.exp(-(t - 20) / TAU_ACT), a140 * np.exp(-(t - 140) / TAU_DEACT)))
    ut = [0, 20, 20, 140, 140, 320]
    uy = [0, 0, 1, 1, 0, 0]
    o = [P.axes([(v, f"{v}") for v in (0, 100, 200, 300)], [(0, "0"), (0.5, "0.5"), (1, "1")],
                "time (ms)", "u, a", grid=(0.5, 1.0))]
    o.append(P.curve(ut, uy, SER[1], multi=True))
    o.append(P.curve(t, a, SER[0], multi=True))
    o.append(legend(s, 58, 20, [(SER[0], "activation a", None), (SER[1], "neural command u", None)]))
    o.append(label(s, P.X(80), P.Y(1.0) - 8, "u", "label", SER[1], "middle", 'font-style="italic"'))
    o.append(label(s, P.X(200), P.Y(0.55), "a", "label", SER[0], "middle", 'font-style="italic"'))
    o.append(label(s, P.X(36), P.Y(0.42), f"rise τ{sub('act', s, 'label2')} = 10 ms", "label2", I["secondary"]))
    o.append(label(s, P.X(196), P.Y(0.92), f"fall τ{sub('deact', s, 'label2')} = 40 ms", "label2", I["secondary"]))
    aria = ("Problem C6 plot. A rectangular neural command u, on (value 1) from 20 to 140 milliseconds, and the "
            "activation a it produces: a rises with a 10 millisecond time constant, so it lags the command at onset, "
            "and falls with a 40 millisecond time constant after release at 140 milliseconds, so it is still 0.37 at 180 milliseconds.")
    hv = hov(P, t[::2], [u[::2], a[::2]], lambda i: f"t = {t[::2][i]:.0f} ms: u = {u[::2][i]:.0f}, a = {a[::2][i]:.2f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #48 C7: the eccentric branch
def fig48():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 30, 388, 202), (-1, 1), (0, 1.7))
    v = np.linspace(-1, 1, 201)
    f = np.array([fV(x) for x in v])
    o = [P.axes([(x, t) for x, t in ((-1, "−1"), (-0.5, "−0.5"), (0, "0"), (0.5, "0.5"), (1, "1"))],
                [(0, "0"), (1, "1")], f"shortening velocity v/{vmax(s)}", f"force f{sub('V', s)} = F/F₀", grid=(1.0,))]
    o.append(H.line(s, P.X(0), P.y0, P.X(0), P.y1 + 18, I["rule"], "leader", H.DASH_REF))
    o.append(P.curve(v, f, SER[0]))
    o.append(label(s, P.X(0) + 5, P.y1 + 13, "isometric", "label2", I["muted"], "start"))
    o.append(label(s, P.X(-0.55), P.Y(1.22), "eccentric", "label", SER[0], "middle"))
    o.append(label(s, P.X(-0.55), P.Y(1.22) + 16, "(lengthening)", "label2", I["secondary"], "middle"))
    o.append(label(s, P.X(0.5), P.Y(0.62), "concentric", "label", SER[0], "middle"))
    o.append(label(s, P.X(0.5), P.Y(0.62) + 16, "(shortening)", "label2", I["secondary"], "middle"))
    o.append(label(s, P.X(0.97), P.Y(1.0) - 6, "F₀", "label2", I["secondary"], "end"))
    aria = ("Problem C7 plot: the force-velocity factor fV against shortening velocity over maximum velocity, from "
            "minus 1 to 1. Right of zero (concentric, shortening) force falls from the isometric value 1 to zero at "
            "maximum velocity; left of zero (eccentric, lengthening) force rises above the isometric value.")
    hv = hov(P, v, [f], lambda i: f"v = {v[i]:.2f} vmax, fV = {f[i]:.2f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #51 C10 and #58 D7: the fatigue model
def fatigue(t_end, hold, u=0.9, dt=0.05):
    """Lab 2 (section 9): C' = -Ff a C + Fr (1 - C), a quasi-static = u while held, force = a C."""
    t = np.arange(0, t_end + dt / 2, dt)
    a = np.where(t < hold, u, 0.0)
    C = np.ones_like(t)
    for i in range(1, len(t)):
        C[i] = C[i - 1] + dt * (-FF * a[i - 1] * C[i - 1] + FR * (1 - C[i - 1]))
    return t, a, C, a * C


def fig51():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 62, 388, 226), (0, 120), (0, 1.08))
    t, a, C, F = fatigue(120, 60)
    f60 = F[t < 60][-1]
    assert round(f60, 2) == 0.54 and round(C.min(), 2) == 0.60, (f60, C.min())     # module05 line 1541
    k = np.searchsorted(t, 60)
    o = [f'<rect x="{P.X(0):.2f}" y="{P.y1}" width="{P.X(60) - P.X(0):.2f}" height="{P.y0 - P.y1}" fill="{BOX}"/>']
    o.append(P.axes([(v, f"{v}") for v in (0, 30, 60, 90, 120)], [(0, "0"), (0.5, "0.5"), (1, "1")],
                    "time (s)", "a, C, force", grid=(0.5, 1.0)))
    o.append(P.curve(t[k:], C[k:], SER[2], multi=True))
    o.append(P.curve(t[:k + 1], C[:k + 1], SER[2], multi=True))
    o.append(P.curve(list(t[:k:10]) + [60, 60, 120], list(a[:k:10]) + [0.9, 0, 0], SER[1], multi=True, nmax=400))
    o.append(P.curve(list(t[:k:10]) + [60, 60, 120], list(F[:k:10]) + [F[k - 1], 0, 0], SER[0], multi=True,
                     nmax=400))
    o.append(legend(s, 58, 20, [(SER[0], "force a·C", None), (SER[1], "activation a", None),
                                (SER[2], "capacity C", None)], gap=12))
    o.append(label(s, P.X(30), P.Y(0.9) - 8, "a", "label", SER[1], "middle", 'font-style="italic"'))
    o.append(label(s, P.X(100), P.Y(0.82) - 12, "C", "label", I["primary"], "middle", 'font-style="italic"'))
    o.append(label(s, P.X(36), P.Y(0.52) + 4, "a·C", "label", SER[0], "middle", 'font-style="italic"'))
    o.append(label(s, P.X(30), P.Y(0.1), "hold, u = 0.9", "label2", I["secondary"], "middle"))
    o.append(label(s, P.X(90), P.Y(0.1), "released", "label2", I["secondary"], "middle"))
    aria = ("Problem C10 plot, Lab 2 of section 9: a command of 0.9 held for 60 seconds, then released. Activation a "
            "stays flat at 0.9 during the hold; the capacity C falls from 1 to 0.60; the force a times C therefore falls "
            "from 0.90 to 0.54. After release a and the force are zero and C recovers over tens of seconds.")
    idx = list(range(0, len(t), 10))
    tt = t[idx]
    aa, cc, ff = a[idx], C[idx], F[idx]
    hv = hov(P, tt, [ff, aa, cc], lambda i: f"t = {tt[i]:.0f} s: a = {aa[i]:.2f}, C = {cc[i]:.2f}, a·C = {ff[i]:.2f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


def fig58():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 62, 388, 226), (0, 200), (0, 1.08))
    t, a, C, F = fatigue(200, 1e9)
    o = [P.axes([(v, f"{v}") for v in (0, 50, 100, 150, 200)], [(0, "0"), (0.5, "0.5"), (1, "1")],
                "time (s)", "a, C, force", grid=(0.5, 1.0))]
    o.append(P.curve(t, C, SER[2], multi=True))
    o.append(P.curve(t, a, SER[1], multi=True))
    o.append(P.curve(t, F, SER[0], multi=True))
    o.append(legend(s, 58, 20, [(SER[0], "force a·C", None), (SER[1], "activation a", None),
                                (SER[2], "capacity C", None)], gap=12))
    o.append(label(s, P.X(160), P.Y(0.9) - 8, "a  (held constant)", "label2", SER[1], "middle"))
    o.append(label(s, P.X(160), P.Y(0.553) - 9, "C  → steady value?", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(160), P.Y(0.497) + 19, "a·C  → steady force?", "label2", SER[0], "middle"))
    aria = ("Problem D7 plot: the fatigue model under a command of 0.9 sustained for 200 seconds. Activation a stays "
            "at 0.9; capacity C falls from 1 and levels off at a steady value; the force a times C falls from 0.9 and "
            "levels off at a steady force below a. The levels are what the problem asks you to derive.")
    idx = list(range(0, len(t), 20))
    tt = t[idx]
    aa, cc, ff = a[idx], C[idx], F[idx]
    hv = hov(P, tt, [ff, aa, cc], lambda i: f"t = {tt[i]:.0f} s: a = {aa[i]:.2f}, C = {cc[i]:.3f}, a·C = {ff[i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #54 D3: Hill's hyperbola and its asymptotes
def fig54():
    VB = (0, 0, W, 246)
    s = H.Scale(W, VB[3], display_w=400)
    c = C_HILL                                                   # a_H = c F0, b_H = c vmax
    P = Plot(s, (40, 34, 388, 214), (-0.34, 1.12), (-0.34, 1.12))
    v = np.linspace(0, 1, 101)
    F = (1 + c) * c / (v + c) - c                                # (F + aH)(v + bH) = (F0 + aH) bH, in F0 and vmax units
    o = []
    # coordinate axes through the origin, plot frame light
    o.append(H.line(s, P.x0, P.Y(0), P.x1, P.Y(0), I["axis"], "axis"))
    o.append(H.line(s, P.X(0), P.y0, P.X(0), P.y1, I["axis"], "axis"))
    for x, t in ((1, vmax(s, "tick")),):
        o.append(H.line(s, P.X(x), P.Y(0), P.X(x), P.Y(0) + 5, I["axis"], "leader"))
        o.append(label(s, P.X(x), P.Y(0) + 19, t, "tick", I["secondary"], "middle"))
    for y, t in ((1, "F₀"),):
        o.append(H.line(s, P.X(0) - 5, P.Y(y), P.X(0), P.Y(y), I["axis"], "leader"))
        o.append(label(s, P.X(0) - 8, P.Y(y) + 4.5, t, "tick", I["secondary"], "end"))
    # asymptotes of the rectangular hyperbola
    o.append(H.line(s, P.X(-c), P.y0, P.X(-c), P.y1, O["dim"], "ref", H.DASH_REF))
    o.append(H.line(s, P.x0, P.Y(-c), P.x1, P.Y(-c), O["dim"], "ref", H.DASH_REF))
    o.append(label(s, P.X(-c) + 6, P.y1 + 4, "v = −b" + sub("H", s, "label2"), "label2", I["secondary"]))
    o.append(label(s, P.X(0.5), P.Y(-c) - 10, "F = −a" + sub("H", s, "label2"), "label2", I["secondary"], "middle"))
    o.append(P.curve(v, F, SER[0]))
    o.append(P.dot(0, 1, SER[0]))
    o.append(P.dot(1, 0, O["flag"]))
    o.append(label(s, P.X(0.05), P.Y(1.0) + 4, "isometric: v = 0, F = F₀", "label2", I["secondary"]))
    o.append(label(s, P.X(1.0), P.Y(0) - 26, "F = 0 at", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(1.0), P.Y(0) - 11, f"v = {vmax(s, 'label2')}", "label2", I["primary"], "middle"))
    o.append(label(s, P.X(0.42), P.Y(0.5), "(F + a" + sub("H", s) + ")(v + b" + sub("H", s)
                     + ") = const", "label", SER[0], "start"))
    o.append(label(s, P.X(0.45), P.y0 + 26, "shortening velocity v", "label", I["primary"], "middle"))
    o.append(label(s, 15, (P.y0 + P.y1) / 2, "force F", "label", I["primary"], "middle",
                     f'transform="rotate(-90 15 {(P.y0 + P.y1) / 2:.2f})"'))
    aria = ("Problem D3 plot: Hill's force-velocity hyperbola for shortening, drawn with curvature a_H/F0 = 0.25. "
            "Force starts at F0 at zero velocity and falls to zero at the maximum shortening velocity. Dashed lines "
            "mark the two asymptotes of the rectangular hyperbola, v = minus b_H and F = minus a_H.").replace("_", "")
    hv = hov(P, v, [F], lambda i: f"v = {v[i]:.2f} vmax, F = {F[i]:.2f} F₀")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #55 D4: the normalised concentric factor
def fig55():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 20, 388, 202), (0, 1.0), (0, 1.08))
    v = np.linspace(0, 1, 201)
    f = np.array([fV(x) for x in v])
    o = [P.axes([(x, f"{x:g}") for x in (0, 0.25, 0.5, 0.75, 1)], [(0, "0"), (0.5, "0.5"), (1, "1")],
                f"v/{vmax(s)}", f"f{sub('V', s)} = F/F₀", grid=(0.5, 1.0))]
    o.append(P.curve(v, f, SER[0]))
    o.append(P.dot(0, 1, SER[0]))
    o.append(P.dot(1, 0, SER[0]))
    o.append(label(s, P.X(0.04), P.Y(1.0) - 9, "isometric, f" + sub("V", s, "label2") + " = 1", "label2", I["secondary"]))
    o.append(label(s, P.X(1.0), P.Y(0.17), "f" + sub("V", s, "label2") + " = 0 at " + vmax(s, "label2"),
                     "label2", I["secondary"], "end"))
    o.append(label(s, P.X(0.38), P.Y(0.62), f"c = a{sub('H', s)}/F₀ = 0.25", "label", SER[0]))
    aria = ("Problem D4 plot: the normalised concentric force-velocity factor fV = F/F0 against v/vmax for curvature "
            "c = a_H/F0 = 0.25. It falls from 1 at zero velocity along a hyperbola, steeply at first, to 0 at "
            "vmax.").replace("_", "")
    hv = hov(P, v[::2], [f[::2]], lambda i: f"v = {v[::2][i]:.2f} vmax, fV = {f[::2][i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #56 D5: power peaks at an intermediate velocity
def fig56():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (72, 26, 388, 202), (0, 1.0), (0, 0.11))
    v = np.linspace(0, 1, 201)
    p = np.array([fV(x) * x for x in v])
    i = int(p.argmax())
    o = [P.axes([(x, f"{x:g}") for x in (0, 0.25, 0.5, 0.75, 1)], [(0, "0"), (0.05, "0.05"), (0.1, "0.10")],
                f"v/{vmax(s)}", f"power P/(F₀{vmax(s)})", grid=(0.05, 0.1))]
    o.append(H.line(s, P.X(v[i]), P.y0, P.X(v[i]), P.Y(p[i]), O["dim"], "leader", H.DASH_REF))
    o.append(P.curve(v, p, SER[0]))
    o.append(P.dot(v[i], p[i], SER[0]))
    o.append(label(s, P.X(v[i]) + 8, P.Y(p[i]) - 8, "peak", "label", SER[0]))
    o.append(label(s, P.X(0.62), P.Y(0.085), f"P = F·v,  c = 0.25", "label2", I["secondary"]))
    aria = ("Problem D5 plot: concentric power P = F v, in units of F0 vmax, against v/vmax for curvature c = 0.25. "
            "Power is zero at zero velocity and at vmax and peaks at an intermediate velocity, marked by a dot and a "
            "dashed drop line.")
    hv = hov(P, v[::2], [p[::2]], lambda k: f"v = {v[::2][k]:.2f} vmax, P = {p[::2][k]:.3f} F₀vmax")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #57 D6: exponential relaxation to a constant command
def fig57():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    a0, u = 0.2, 0.8                                       # illustrative; the problem is symbolic
    P = Plot(s, (58, 20, 388, 202), (0, 5.2), (0, 1.0))
    x = np.linspace(0, 5.2, 209)                          # time in units of tau
    a = u + (a0 - u) * np.exp(-x)
    o = [P.axes([(k, "0" if k == 0 else ("τ" if k == 1 else f"{k}τ")) for k in range(6)],
                [(0, "0"), (a0, "a₀"), (u, "u"), (1, "1")], "time t", "activation a", grid=())]
    o.append(H.line(s, P.x0, P.Y(u), P.x1, P.Y(u), O["dim"], "ref", H.DASH_REF))
    o.append(P.curve(x, a, SER[0]))
    o.append(P.dot(0, a0, SER[0]))
    o.append(label(s, P.X(4.0), P.Y(u) - 9, "constant command u", "label2", I["secondary"], "middle"))
    o.append(label(s, P.X(0.18), P.Y(a0) + 4, "a(0) = a₀", "label2", I["secondary"]))
    o.append(label(s, P.X(1.6), P.Y(0.52), "a(t)", "label", SER[0], "start", 'font-style="italic"'))
    aria = ("Problem D6 plot: activation a(t) under a constant command u, starting from a(0) = a0 below u. The "
            "curve climbs toward the dashed level u, fast at first and ever more slowly; the time axis is marked in "
            "multiples of the time constant tau.")
    hv = hov(P, x[::2], [a[::2]], lambda k: f"t = {x[::2][k]:.1f} τ, a = {a[::2][k]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #60 D9: redundancy optimum (Fig. 30 inputs)
def fig60():
    VB = (0, 0, W, 300)
    s = H.Scale(W, VB[3], display_w=400)
    F1M, F2M, D1, D2, TAU = 135.0, 210.0, 0.040, 0.025, 5.89     # module05 line 1434 caption
    lam2 = TAU / (D1 * D1 * F1M**2 + D2 * D2 * F2M**2)
    o1, o2 = lam2 * D1 * F1M**2, lam2 * D2 * F2M**2
    assert round(o1) == 76 and round(o2) == 114, (o1, o2)        # caption: 76 N and 114 N
    kopt = (o1 / F1M)**2 + (o2 / F2M)**2
    P = Plot(s, (58, 50, 388, 238), (0, 200), (0, 260))
    o = [P.axes([(v, f"{v}") for v in (0, 50, 100, 150, 200)], [(0, "0"), (100, "100"), (200, "200")],
                f"F{sub('1', s)} (N)", f"F{sub('2', s)} (N)", grid=())]
    th = np.linspace(0, math.pi / 2, 61)
    for k in (0.45 * kopt, kopt, 1.7 * kopt):
        r = math.sqrt(k)
        xs, ys = r * F1M * np.cos(th), r * F2M * np.sin(th)
        keep = (xs <= 200) & (ys <= 260)
        o.append(P.curve(xs[keep], ys[keep], SER[2], multi=True, dash=(5, 3)))
    f1 = np.linspace(0, TAU / D1, 149)
    f2 = (TAU - D1 * f1) / D2
    o.append(P.curve(f1, f2, SER[1]))
    o.append(P.dot(o1, o2, SER[0]))
    o.append(legend(s, 58, 16, [(SER[1], f"torque constraint: F{sub('1', s, 'label2')}d{sub('1', s, 'label2')} + "
                                         f"F{sub('2', s, 'label2')}d{sub('2', s, 'label2')} = τ", None)]))
    o.append(legend(s, 58, 36, [(SER[2], "equal cost: Σ(F" + sub("i", s, "label2") + "/F" + sub("i,max", s, "label2")
                                 + ")² = const", (5, 3))]))
    o.append(H.line(s, P.X(o1) + 4, P.Y(o2) - 4, P.X(122), P.Y(190), I["secondary"], "leader"))
    o.append(label(s, P.X(123), P.Y(196), "optimum", "label", SER[0]))
    o.append(label(s, P.X(20), P.Y(240), "torque constraint", "label2", SER[1]))
    o.append(label(s, P.X(150), P.Y(22), "equal cost", "label2", I["primary"]))
    aria = ("Problem D9 plot in the plane of two muscle forces F1 and F2, with the inputs of Fig. 30: capacities 135 "
            "and 210 newtons, moment arms 4.0 and 2.5 centimetres, torque 5.89 newton metres. A straight blue torque "
            "constraint line, dashed orange equal-cost ellipses of the summed squared relative stress, and the optimum "
            "where the smallest ellipse touches the line.")
    cost = (f1 / F1M)**2 + (f2 / F2M)**2
    hv = hov(P, f1, [f2], lambda i: f"F₁ = {f1[i]:.0f} N, F₂ = {f2[i]:.0f} N, cost {cost[i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #61 D10: fused tetanus approaches the ceiling
@lru_cache(None)
def d10_traces():
    out = {}
    for f in (25.0, 60.0, 200.0):
        t, a = train_trace(f, T=300.0, dt=0.1)
        out[f] = (t[::20], a[::20])
    return out


def fig61():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 62, 388, 226), (0, 300), (0, 0.85))
    ca = 1.4
    ainf = ca**3 / (1 + ca**3)                                 # gate at the single-pulse calcium peak
    tr = d10_traces()
    o = [P.axes([(v, f"{v}") for v in (0, 100, 200, 300)], [(0, "0"), (0.25, "0.25"), (0.5, "0.5"), (0.75, "0.75")],
                "time (ms)", "activation a", grid=(0.25, 0.5, 0.75))]
    o.append(H.line(s, P.x0, P.Y(ainf), P.x1, P.Y(ainf), I["primary"], "ref", H.DASH_REF))
    cols = {200.0: SER[0], 60.0: SER[1], 25.0: SER[2]}
    for f in (25.0, 60.0, 200.0):
        t, a = tr[f]
        o.append(P.curve(t, a, cols[f], multi=True, nmax=160))
    o.append(legend(s, 58, 20, [(SER[0], "200 Hz", None), (SER[1], "60 Hz", None), (SER[2], "25 Hz", None)]))
    o.append(label(s, P.X(296), P.Y(ainf) - 7, "ceiling a∞", "label2", I["primary"], "end"))
    o.append(label(s, P.X(10), P.Y(0.64), "200 Hz", "label2", SER[0]))
    o.append(label(s, P.X(98), P.Y(0.54), "60 Hz", "label2", SER[1], "start"))
    o.append(label(s, P.X(200), P.Y(0.17), "25 Hz", "label2", I["primary"], "middle"))
    aria = ("Problem D10 plot: activation from the twitch-summation model of section 4 for impulse trains at 25, 60 "
            "and 200 hertz over 300 milliseconds. The 25 hertz trace ripples well below the dashed calcium ceiling "
            "a-infinity; the 60 hertz trace ripples just under it; the 200 hertz trace rises smoothly onto it.")
    t = tr[25.0][0]
    idx = list(range(0, len(t), 1))
    ys = [tr[200.0][1], tr[60.0][1], tr[25.0][1]]
    hv = hov(P, t[idx], [y[idx] for y in ys],
             lambda i: f"t = {t[i]:.0f} ms: 200 Hz {ys[0][i]:.2f}, 60 Hz {ys[1][i]:.2f}, 25 Hz {ys[2][i]:.2f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #62 K1: force against pennation angle
def fig62():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    SIG, VOL, THK = 0.3e6, 2.0e-4, 0.02                       # K1 script constants

    def force(th):
        return SIG * (VOL / (THK / np.sin(th))) * np.cos(th)

    P = Plot(s, (66, 30, 388, 202), (0, 90), (0, 1700))
    d = np.linspace(0.5, 89.5, 179)
    F = force(np.radians(d))
    o = [P.axes([(v, f"{v}°") for v in (0, 15, 30, 45, 60, 75, 90)], [(0, "0"), (500, "500"), (1000, "1000"), (1500, "1500")],
                f"pennation angle θ{sub('p', s)}", f"F{sub('max', s)} (N)", grid=(500, 1000, 1500), ytx=13)]
    o.append(P.curve(d, F, SER[0]))
    o.append(P.dot(45, force(math.radians(45)), O["flag"]))
    o.append(P.dot(20, force(math.radians(20)), I["secondary"]))
    o.append(label(s, P.X(45), P.Y(force(math.radians(45))) - 10, "45° optimum", "label", I["primary"], "middle"))
    o.append(label(s, P.X(20) + 9, P.Y(force(math.radians(20))) + 18, "typical 20°", "label2", I["secondary"]))
    aria = ("Problem K1 plot: tendon force Fmax against pennation angle for a muscle of fixed volume 0.2 litres and "
            "belly thickness 2 centimetres at specific tension 0.3 megapascals. Force rises from zero, peaks at 45 "
            "degrees, and falls back to zero at 90 degrees; a grey dot marks a typical 20 degree muscle.")
    hv = hov(P, d, [F], lambda i: f"θp = {d[i]:.1f}°, Fmax = {F[i]:.0f} N")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #64 K2: ripple against firing rate
@lru_cache(None)
def k2_sweep():
    rates = np.arange(5.0, 80.01, 0.5)
    out = {}
    for sc in (1.0, 2.5):
        rip = np.array([train(f, sc)[1] for f in rates])
        fus = rates[np.argmax(rip < 0.05)]
        out[sc] = (rip, fus)
    return rates, out


def fig64():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    rates, res = k2_sweep()
    (rf, ff), (rs, fs) = res[1.0], res[2.5]
    assert (ff, fs) == (42.5, 17.0), (ff, fs)                     # K2 solution, boxed
    lo, hi = math.log10(0.001), math.log10(5.0)
    P = Plot(s, (66, 62, 388, 226), (5, 80), (lo, hi))
    o = [P.axes([(v, f"{v}") for v in (5, 20, 40, 60, 80)],
                [(math.log10(v), t) for v, t in ((0.001, "0.1%"), (0.01, "1%"), (0.05, "5%"), (1, "100%"))],
                "firing rate (Hz)", "ripple / mean (log)", grid=(math.log10(0.01), math.log10(1.0)), ytx=12)]
    o.append(H.line(s, P.x0, P.Y(math.log10(0.05)), P.x1, P.Y(math.log10(0.05)), I["primary"], "ref", H.DASH_REF))
    clip = lambda r: np.log10(np.clip(r, 0.001, 5.0))          # noqa: E731

    def to_floor(r):
        """Points down to the 0.1 % floor; the last one interpolated (in log) onto it."""
        lr = np.log10(r)
        n = int(np.argmax(lr < lo)) if (lr < lo).any() else len(r)
        xs, ys = list(rates[:n]), list(lr[:n])
        if n < len(r):
            f = (ys[-1] - lo) / (ys[-1] - lr[n])
            xs.append(rates[n - 1] + f * (rates[n] - rates[n - 1]))
            ys.append(lo)
        return xs, ys

    o.append(P.curve(*to_floor(rs), SER[1], multi=True))
    o.append(P.curve(*to_floor(rf), SER[0], multi=True))
    o.append(P.dot(ff, math.log10(0.05), SER[0]))
    o.append(P.dot(fs, math.log10(0.05), SER[1]))
    o.append(legend(s, 66, 20, [(SER[0], "fast fibre", None), (SER[1], "slow fibre (2.5× twitch)", None)]))
    o.append(label(s, P.X(80), P.Y(math.log10(2.5)), "ripple below 5% from", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(80), P.Y(math.log10(2.5)) + 16, f"fast fibre: {ff:.1f} Hz", "label2", SER[0], "end"))
    o.append(label(s, P.X(80), P.Y(math.log10(2.5)) + 32, f"slow fibre: {fs:.1f} Hz", "label2", SER[1], "end"))
    o.append(label(s, P.X(46), P.Y(math.log10(0.1)), "fast", "label2", SER[0]))
    o.append(label(s, P.X(18), P.Y(math.log10(0.1)), "slow", "label2", SER[1]))
    o.append(label(s, P.X(80), P.Y(math.log10(0.05)) - 7, "5% fusion threshold", "label2", I["primary"], "end"))
    aria = ("Problem K2 plot: steady peak-to-trough ripple relative to the mean activation, on a log axis, against "
            "impulse rate from 5 to 80 hertz, for the fast fibre and for a slow fibre with a 2.5 times longer twitch. "
            f"Ripple falls below the dashed 5 percent line at {ff:.1f} hertz for the fast fibre and {fs:.1f} hertz for "
            "the slow one.")
    hv = hov(P, rates, [clip(rf), clip(rs)],
             lambda i: f"{rates[i]:.1f} Hz: fast {100 * rf[i]:.1f}%, slow {100 * rs[i]:.1f}%")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #66 K3: power for three Hill curvatures
def fig66():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (72, 62, 388, 226), (0, 1.0), (0, 0.15))
    v = np.linspace(0, 1, 201)
    cs = (0.10, 0.25, 0.50)
    o = [P.axes([(x, f"{x:g}") for x in (0, 0.25, 0.5, 0.75, 1)], [(0, "0"), (0.05, "0.05"), (0.1, "0.10"), (0.15, "0.15")],
                f"v/{vmax(s)}", f"power P/(F₀{vmax(s)})", grid=(0.05, 0.1, 0.15))]
    curves = []
    for k, c in enumerate(cs):
        p = np.array([fV(x, c) * x for x in v])
        curves.append(p)
        o.append(P.curve(v, p, SER[k], multi=True))
    for k, p in enumerate(curves):
        i = int(p.argmax())
        o.append(P.dot(v[i], p[i], SER[k]))
    o.append(legend(s, 66, 20, [(SER[k], f"c = {c:g}", None) for k, c in enumerate(cs)]))
    for k, (c, xv, yv) in enumerate(((0.10, 0.45, 0.056), (0.25, 0.45, 0.096), (0.50, 0.36, 0.142))):
        o.append(label(s, P.X(xv), P.Y(yv), f"c = {c:g}", "label2"))
        if k < 2:                                           # 1 px leader in the series colour
            xl = xv + 0.02
            o.append(H.line(s, P.X(xl), P.Y(yv) + 3, P.X(xl), P.Y(fV(xl, c) * xl) - 2, SER[k], "leader"))
    aria = ("Problem K3 plot: normalised concentric power against v/vmax for Hill curvature c = 0.1, 0.25 and 0.5, "
            "each with its peak marked by a dot. As c rises the curve straightens, and the power peak moves to a "
            "higher velocity and grows taller.")
    hv = hov(P, v[::2], [p[::2] for p in curves],
             lambda i: f"v = {v[::2][i]:.2f} vmax: P = {curves[0][::2][i]:.3f}, {curves[1][::2][i]:.3f}, "
                       f"{curves[2][::2][i]:.3f} (c = 0.1, 0.25, 0.5)")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #68 K4: both branches against speed
def fig68():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    P = Plot(s, (58, 62, 388, 226), (0, 1.0), (0, 1.65))
    v = np.linspace(0, 1, 201)
    con = np.array([fV(x) for x in v])
    ecc = np.array([fV(-x) for x in v])
    c3, e3 = fV(0.3), fV(-0.3)
    assert (round(c3, 3), round(e3, 3)) == (0.318, 1.429), (c3, e3)       # K4 solution
    o = [P.axes([(x, f"{x:g}") for x in (0, 0.25, 0.5, 0.75, 1)], [(0, "0"), (0.5, "0.5"), (1, "1"), (1.5, "1.5")],
                f"speed |v|/{vmax(s)}", f"f{sub('V', s)} = F/F₀", grid=(0.5, 1.0, 1.5))]
    o.append(H.line(s, P.X(0.3), P.y0, P.X(0.3), P.y1, O["dim"], "leader", H.DASH_REF))
    o.append(P.curve(v, ecc, SER[1], multi=True))
    o.append(P.curve(v, con, SER[0], multi=True))
    o.append(P.dot(0.3, c3, SER[0]))
    o.append(P.dot(0.3, e3, SER[1]))
    o.append(legend(s, 58, 20, [(SER[1], "eccentric f" + sub("V", s, "label2") + "(−v)", None),
                                (SER[0], "concentric f" + sub("V", s, "label2") + "(v)", None)]))
    o.append(label(s, P.X(0.3) + 7, P.Y(e3) + 20, f"{e3:.2f}", "label2", SER[1]))
    o.append(label(s, P.X(0.3) + 7, P.Y(c3) - 7, f"{c3:.2f}", "label2", SER[0]))
    o.append(label(s, P.X(0.3) - 5, P.Y(0.1), "|v| = 0.3", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(0.98), P.Y(e3) + 20, "eccentric (lowering)", "label2", SER[1], "end"))
    o.append(label(s, P.X(0.98), P.Y(0.2), "concentric (lifting)", "label2", SER[0], "end"))
    aria = ("Problem K4 plot: the two branches of the force-velocity factor against speed |v|/vmax from 0 to 1. The "
            "concentric branch fV(v) falls from 1 to 0; the eccentric branch fV(-v) rises from 1 toward its 1.5 plateau. "
            "At |v| = 0.3 they are 0.32 and 1.43.")
    hv = hov(P, v[::2], [ecc[::2], con[::2]],
             lambda i: f"|v| = {v[::2][i]:.2f} vmax: eccentric {ecc[::2][i]:.3f}, concentric {con[::2][i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #70 K5: the command a 20 ms ramp needs
def fig70():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    TA, AEND, TR_ = 10.0, 0.9, 20.0                           # ms, K5
    upk = AEND + TA * AEND / TR_
    assert round(upk, 2) == 1.35
    P = Plot(s, (58, 62, 388, 226), (-5, 60), (0, 1.5))
    at = [-5, 0, TR_, 60]
    ay = [0, 0, AEND, AEND]
    ut = [-5, 0, 0, TR_, TR_, 60]
    uy = [0, 0, TA * AEND / TR_, upk, AEND, AEND]
    o = [f'<rect x="{P.X(-5):.2f}" y="{P.Y(1.5):.2f}" width="{P.x1 - P.x0:.2f}" height="{P.Y(1) - P.Y(1.5):.2f}" fill="{BOX}"/>']
    o.append(P.axes([(v, f"{v}") for v in (0, 20, 40, 60)], [(0, "0"), (0.5, "0.5"), (1, "1"), (1.5, "1.5")],
                    "time (ms)", "u, a", grid=(0.5,)))
    o.append(H.line(s, P.x0, P.Y(1), P.x1, P.Y(1), I["primary"], "ref", H.DASH_REF))
    o.append(P.curve(ut, uy, SER[1], multi=True))
    o.append(P.curve(at, ay, SER[0], multi=True))
    o.append(P.dot(TR_, upk, SER[1]))
    o.append(legend(s, 58, 20, [(SER[0], "activation a (ramp)", None), (SER[1], "required command u", None)]))
    o.append(label(s, P.X(TR_) + 8, P.Y(upk) + 5, f"u = {upk:.2f}", "label2", SER[1]))
    o.append(label(s, P.X(58), P.Y(1) - 7, "u = 1, the maximum", "label2", I["primary"], "end"))
    o.append(label(s, P.X(58), P.Y(1.3), "unreachable", "label2", I["secondary"], "end"))
    o.append(label(s, P.X(40), P.Y(AEND) + 18, "a = 0.9", "label2", SER[0], "middle"))
    o.append(label(s, P.X(13), P.Y(0.22), "20 ms ramp", "label2", SER[0], "start"))
    aria = ("Problem K5 plot: a linear activation ramp from 0 to 0.9 in 20 milliseconds, then held, and the command "
            "u = a + tau_act times da/dt it requires with tau_act = 10 milliseconds. The command jumps to 0.45, climbs "
            "to 1.35 at the end of the ramp, above the dashed maximum u = 1, then drops to 0.9.").replace("_", " ")
    tt = np.linspace(-5, 60, 131)
    aa = np.interp(tt, at, ay)
    uu = np.where(tt < 0, 0.0, np.where(tt <= TR_, aa + TA * AEND / TR_, AEND))
    hv = hov(P, tt, [uu, aa], lambda i: f"t = {tt[i]:.1f} ms: u = {uu[i]:.2f}, a = {aa[i]:.2f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #74 K7: forward dynamics, Hill model against constant torque
FMAX7, CP7, VMAX7 = 500.0, math.cos(math.radians(15.0)), 8.0
KJ, BJ, IJ, TMAX, U7 = 9.6, 0.76, 0.06, 14.0, 0.6


def _fL7(x):
    if x <= 0.47 or x >= 1.556:
        return 0.0
    if x < 0.963:
        return (x - 0.47) / 0.493
    if x <= 1.0:
        return 1.0
    return (1.556 - x) / 0.556


def _fV7(v):
    if v >= 0:
        return (1 - v) / (1 + v / 0.25)
    return 1 + 0.5 * 20 * (-v) / (1 + 20 * (-v))


def _fPE7(x):
    return (math.exp(3 * max(x - 1.0, 0.0) / 0.6) - 1) / (math.e**3 - 1)


def _torque7(a, th, om):
    x = 1.0 - 0.003 * (math.degrees(th) - 70.0)
    v = 0.003 * math.degrees(om) / VMAX7
    force = (a * FMAX7 * _fL7(x) * _fV7(v) + FMAX7 * _fPE7(x)) * CP7
    return force * (1.8 + 2.2 * math.sin(th)) / 100.0


@lru_cache(None)
def k7_run(kind, dt=2e-5, t_end=3.0):
    """K7 run(), ported (math instead of numpy scalars): angle history in degrees, every 5 ms."""
    n = int(t_end / dt)
    a = th = om = 0.0
    keep = int(round(0.005 / dt))
    ts, hs, full = [0.0], [0.0], np.empty(n)
    for i in range(n):
        a += dt * (U7 - a) / (0.010 if U7 > a else 0.040)
        tq = a * TMAX if kind == "const" else _torque7(a, th, om)
        om += dt * (tq - KJ * th - BJ * om) / IJ
        th += dt * om
        full[i] = math.degrees(th)
        if (i + 1) % keep == 0:
            ts.append((i + 1) * dt)
            hs.append(full[i])
    eq = full[-1]
    ov = 100 * max(full.max() - eq, 0.0) / eq
    return tuple(ts), tuple(hs), eq, ov


def fig74():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    th, hh, eqh, ovh = k7_run("hill")
    tc, hc, eqc, ovc = k7_run("const")
    assert (round(eqh, 1), round(eqc, 1), round(ovc, 1), round(ovh, 1)) == (63.4, 50.1, 16.1, 0.0), (eqh, eqc, ovc, ovh)
    P = Plot(s, (58, 62, 388, 226), (0, 3.0), (0, 80))
    o = [P.axes([(v, f"{v:g}") for v in (0, 1, 2, 3)], [(0, "0"), (25, "25"), (50, "50"), (75, "75")],
                "time (s)", "elbow angle θ (°)", grid=(25, 50, 75))]
    o.append(P.curve(tc, hc, SER[1], multi=True))
    o.append(P.curve(th, hh, SER[0], multi=True))
    o.append(legend(s, 58, 20, [(SER[0], "assembled Hill model", None), (SER[1], "constant torque", None)]))
    o.append(label(s, P.X(2.95), P.Y(eqh) - 9, f"settles at {eqh:.0f}°, no overshoot", "label2", SER[0], "end"))
    o.append(label(s, P.X(2.95), P.Y(eqc) + 19, f"settles at {eqc:.0f}°, {ovc:.0f}% overshoot", "label2", SER[1], "end"))
    aria = ("Problem K7 plot: elbow angle against time over 3 seconds after a step command u = 0.6, for the assembled "
            f"Hill model and for the constant-torque shortcut. The Hill model rises without overshoot to {eqh:.0f} "
            f"degrees; the constant-torque model overshoots by {ovc:.0f} percent and settles at {eqc:.0f} degrees.")
    hv = hov(P, th[::2], [hh[::2], hc[::2]],
             lambda i: f"t = {th[::2][i]:.2f} s: Hill {hh[::2][i]:.1f}°, constant torque {hc[::2][i]:.1f}°")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #78 K9: endurance against force target
def endurance(f):
    """K9 closed form (the solution shows it equals the simulation to the printed digit)."""
    cinf = 1 - FF * f / FR
    if cinf >= f:
        return math.inf
    return -math.log((f - cinf) / (1 - cinf)) / FR


def fig78():
    VB = (0, 0, W, 262)
    s = H.Scale(W, VB[3], display_w=400)
    YT = 150.0
    P = Plot(s, (58, 30, 388, 202), (0.5, 1.0), (0, YT))
    f = np.linspace(0.5, 1.0, 1001)
    t = np.array([endurance(x) for x in f])
    ok = t <= YT
    f0 = f[ok][0]
    e7, e9 = endurance(0.7), endurance(0.9)
    assert (round(e7, 1), round(e9, 1)) == (32.3, 6.6), (e7, e9)
    o = [P.axes([(v, f"{v:g}") for v in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)], [(0, "0"), (50, "50"), (100, "100"), (150, "150")],
                f"force target F{sub('hold', s)}/F{sub('max', s)}", "endurance (s)", grid=(50, 100, 150))]
    o.append(P.curve(f[ok], t[ok], SER[0]))
    o.append(P.dot(0.7, e7, SER[0]))
    o.append(P.dot(0.9, e9, SER[0]))
    o.append(label(s, P.X(0.7) + 9, P.Y(e7) - 9, f"0.7 → {e7:.1f} s", "label2", SER[0]))
    o.append(label(s, P.X(0.9), P.Y(e9) - 13, f"0.9 → {e9:.1f} s", "label2", SER[0], "middle"))
    aria = ("Problem K9 plot: endurance time of a held force target against the target as a fraction of maximum, from "
            f"the fatigue model of section 9. Endurance falls steeply as the target rises: {e7:.1f} seconds at 0.7, "
            f"{e9:.1f} seconds at 0.9, zero at 1; toward low targets it climbs off the top of the axis.")
    fs = np.linspace(f0, 1.0, 150)
    ts = np.array([endurance(x) for x in fs])
    hv = hov(P, fs, [ts], lambda i: f"Fhold = {fs[i]:.3f} Fmax: endurance {ts[i]:.1f} s")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


# ---------------------------------------------------------------- #80 K10 and #82 K11: the twitch fits
def _ca_pulse(t):
    return 0.1 + 1.3 * (1 - np.exp(-t / TR)) * np.exp(-t / TD) / NORM


def twitch_trace(tau_a, dt=0.02, T=400.0):
    """K10 twitch(): first-order activation driven by the Hill gate of the section 3 calcium pulse."""
    t = np.arange(0.0, T, dt)
    ca = _ca_pulse(t)
    tgt = ca**3 / (1 + ca**3)
    a = np.zeros_like(t)
    for i in range(1, len(t)):
        a[i] = a[i - 1] + dt * (tgt[i - 1] - a[i - 1]) / tau_a
    return t, a


def feats(t, a):
    i = a.argmax()
    j = i + int(np.argmax(a[i:] < 0.5 * a[i]))
    return a[i], t[i], t[j] - t[i]


@lru_cache(None)
def k10_fit():
    from scipy.optimize import minimize_scalar

    def cost(tau_a):
        _, tp, th = feats(*twitch_trace(tau_a))
        return (tp - 25.0)**2 + (th - 40.0)**2

    r = minimize_scalar(cost, bounds=(20.0, 80.0), method="bounded")
    return float(r.x)


def fig80():
    VB = (0, 0, W, 286)
    s = H.Scale(W, VB[3], display_w=400)
    p = "m5f80_"
    tau = k10_fit()
    t, a = twitch_trace(tau)
    pk, tp, th = feats(t, a)
    assert (round(tau, 1), round(pk, 3), round(tp, 1), round(th, 1)) == (43.7, 0.215, 25.2, 40.0), (tau, pk, tp, th)
    P = Plot(s, (58, 30, 388, 226), (0, 160), (0, 0.25))
    w = t <= 160
    tt, aa = t[w][::50], a[w][::50]
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o.append(P.axes([(v, f"{v}") for v in (0, 50, 100, 150)], [(0, "0"), (0.1, "0.1"), (0.2, "0.2")],
                    "time (ms)", "activation a", grid=(0.1, 0.2)))
    o.append(H.line(s, P.X(tp), P.y0, P.X(tp), P.Y(pk), O["dim"], "leader", H.DASH_REF))
    o.append(P.curve(tt, aa, SER[0]))
    o.append(P.dot(tp, pk, SER[0]))
    yb = P.Y(0.02)
    o.append(H.arrow(s, p, P.X(0), yb, P.X(tp), yb, "geometry", both=True))
    o.append(label(s, P.X(tp) + 6, yb + 5, "time to peak 25 ms", "label2", O["geometry"]))
    yh = P.Y(pk / 2)
    o.append(H.arrow(s, p, P.X(tp), yh, P.X(tp + th), yh, "geometry", both=True))
    o.append(label(s, P.X(tp + th) + 4, yh - 8, "half-relaxation 40 ms", "label2", O["geometry"]))
    o.append(label(s, P.X(tp) + 8, P.Y(pk) - 8, f"peak {pk:.3f}", "label2", SER[0]))
    o.append(label(s, P.X(158), P.Y(0.215), f"least-squares fit: τ{sub('a', s, 'label2')} = {tau:.1f} ms",
                     "label2", I["primary"], "end"))
    aria = (f"Problem K10 plot: the twitch of the fitted model. Activation peaks at {pk:.3f} after {tp:.0f} "
            f"milliseconds and falls to half that peak {th:.0f} milliseconds later, the two features the least-squares "
            f"fit matches, which recovers an activation time constant of {tau:.1f} milliseconds.")
    hv = hov(P, tt, [aa], lambda i: f"t = {tt[i]:.0f} ms, a = {aa[i]:.3f}")
    return svg(VB, aria, s, "".join(o), (P.box, hv))


def chain(k_off, tau_x=None, dt=0.02, T=400.0):
    """K11 chain(): Ca pulse -> mass-action binding s(t) -> optional first-order lag -> a(t)."""
    t = np.arange(0.0, T, dt)
    ca = _ca_pulse(t)
    r_on = k_off * ca**3 * 1e-3                                # Ca50 = 1, n = 3, per ms
    r_off = k_off * 1e-3
    s_ = np.zeros_like(t)
    a = np.zeros_like(t)
    for i in range(1, len(t)):
        s_[i] = s_[i - 1] + dt * (r_on[i - 1] * (1 - s_[i - 1]) - r_off * s_[i - 1])
        if tau_x:
            a[i] = a[i - 1] + dt * (s_[i - 1] - a[i - 1]) / tau_x
    return t, (a if tau_x else s_)


@lru_cache(None)
def k11_data():
    from scipy.optimize import minimize

    def cost(p):
        if min(p) <= 0:
            return 1e6
        _, tp, th = feats(*chain(*p))
        return (tp - 25.0)**2 + (th - 40.0)**2

    r = minimize(cost, [25.0, 10.0], method="Nelder-Mead", options=dict(xatol=1e-4, fatol=1e-8))
    assert (round(r.x[0], 1), round(r.x[1], 1)) == (22.3, 4.6), r.x       # K11 solution (b), branch A
    tA, aA = chain(*r.x)
    tB, aB = chain(3531.6, 43.6)                               # branch B, as printed by the K11 listing
    ks = np.geomspace(6.0, 80.0, 40)
    pairs = [feats(*chain(k))[1:] for k in ks]
    return (tA, aA), (tB, aB), ks, pairs


def fig82():
    VB = (0, 0, W, 530)
    s = H.Scale(W, VB[3], display_w=400)
    (tA, aA), (tB, aB), ks, pairs = k11_data()
    fA, fB = feats(tA, aA), feats(tB, aB)
    assert round(fA[0], 3) == 0.391 and round(fB[0], 3) == 0.215, (fA, fB)
    assert abs(fA[1] - 25) < 0.5 and abs(fA[2] - 40) < 0.5 and abs(fB[1] - 25) < 0.5 and abs(fB[2] - 40) < 0.5
    # top panel: the two fitted twitches
    P = Plot(s, (58, 66, 388, 222), (0, 160), (0, 0.45))
    w = tA <= 160
    tt, ya, yb = tA[w][::50], aA[w][::50], aB[w][::50]
    o = [P.axes([(v, f"{v}") for v in (0, 50, 100, 150)], [(0, "0"), (0.2, "0.2"), (0.4, "0.4")],
                "time (ms)", "activation a", grid=(0.2, 0.4))]
    o.append(H.line(s, P.X(25), P.y0, P.X(25), P.Y(0.43), O["dim"], "leader", H.DASH_REF))
    o.append(P.curve(tt, yb, SER[1], multi=True))
    o.append(P.curve(tt, ya, SER[0], multi=True))
    o.append(P.dot(fA[1], fA[0], SER[0]))
    o.append(P.dot(fB[1], fB[0], SER[1]))
    o.append(legend(s, 58, 20, [(SER[0], "branch A", None), (SER[1], "branch B", None)]))
    o.append(label(s, 58, 40, "both peak at 25 ms and fall to half 40 ms later", "label2", I["secondary"]))
    koff = f"k{sub('off', s, 'label2')}"
    tx = f"τ{sub('x', s, 'label2')}"
    o.append(label(s, P.X(32), P.Y(0.41), f"A: {koff} = 22.3/s, {tx} = 4.6 ms, peak {fA[0]:.2f}", "label2", SER[0]))
    o.append(label(s, P.X(70), P.Y(0.30), "B: binding instant,", "label2", SER[1]))
    o.append(label(s, P.X(70), P.Y(0.30) + 15, f"{tx} = 43.6 ms, peak {fB[0]:.3f}", "label2", SER[1]))
    # bottom panel: what pure binding kinetics can reach
    Q = Plot(s, (58, 312, 388, 488), (10, 30), (0, 130))
    tp = np.array([q[0] for q in pairs])
    th = np.array([q[1] for q in pairs])
    o.append(Q.axes([(v, f"{v}") for v in (10, 15, 20, 25, 30)], [(0, "0"), (40, "40"), (80, "80"), (120, "120")],
                    "time to peak (ms)", "half-relaxation (ms)", grid=(40, 80, 120)))
    o.append(Q.curve(tp, th, SER[2], multi=True))
    o.append(Q.dot(25, 40, I["primary"]))
    o.append(label(s, Q.X(25), Q.Y(40) + 19, "measured (25, 40)", "label2", I["primary"], "middle"))
    o.append(label(s, Q.X(tp[0]), Q.Y(th[0]) - 9, f"{koff} = 6/s", "label2", I["secondary"], "middle"))
    o.append(label(s, Q.X(tp[-1]) - 2, Q.Y(th[-1]) + 18, f"{koff} = 80/s", "label2", I["secondary"], "start"))
    o.append(label(s, Q.X(10.4), Q.Y(118), "pure binding kinetics, every", "label2", I["primary"]))
    o.append(label(s, Q.X(10.4), Q.Y(118) + 15, f"{koff} from 6 to 80/s: misses the point", "label2", I["primary"]))
    aria = ("Problem K11 plot in two stacked panels. Top: two fitted twitches that both peak at 25 milliseconds and "
            "fall to half 40 milliseconds later; branch A, with slow calcium unbinding at 22.3 per second and a 4.6 "
            f"millisecond downstream lag, peaks at {fA[0]:.2f}; branch B, with instantaneous binding and a 43.6 "
            f"millisecond lag, peaks at {fB[0]:.3f}. Bottom: time to peak against half-relaxation that pure binding "
            "kinetics reaches as the off-rate runs from 6 to 80 per second; the measured point 25, 40 lies off "
            "the curve.")
    xb = 112.0
    o.append(H.line(s, P.X(xb), P.Y(0.30) + 19, P.X(xb), P.Y(float(np.interp(xb, tt, yb))) - 2, SER[1], "leader"))
    hv = hov(P, tt, [ya, yb], lambda i: f"t = {tt[i]:.0f} ms: A {ya[i]:.3f}, B {yb[i]:.3f}")
    hq = hov(Q, tp, [th], lambda i: f"koff = {ks[i]:.1f}/s: time to peak {tp[i]:.1f} ms, half-relaxation {th[i]:.1f} ms")
    hq.sort(key=lambda q: q[0])
    return H.svg_open(VB, html.escape(aria), s, extra=H.hover_attr([(P.box, hv), (Q.box, hq)])) + "".join(o) + "</svg>"


FIGS = {
    47: ("A rectangular neural command on from 20 to 140 milliseconds,", fig47),
    48: ("eccentric branch above F0", fig48),
    51: ("force sags as capacity drains", fig51),
    54: ("Hill hyperbola zero at vmax", fig54),
    55: ("normalized fV", fig55),
    56: ("power peaks mid velocity", fig56),
    57: ("exponential activation step", fig57),
    58: ("fatigue steady state", fig58),
    60: ("redundancy Lagrange optimum", fig60),
    61: ("fused tetanus reaches ceiling", fig61),
    62: ("Fmax proportional to sin(2 theta_p), peaking at 45 degrees", fig62),
    64: ("ripple versus firing rate for fast and slow fibres, fusion a", fig64),
    66: ("power curves for three Hill curvatures; peak shifts right an", fig66),
    68: ("bar chart: eccentric force 1.43 versus concentric 0.32, a 4.", fig68),
    70: ("the command u required for a 20 ms activation ramp exceeds 1", fig70),
    74: ("Two forward-dynamics angle trajectories: the assembled Hill ", fig74),
    78: ("endurance time falls steeply with force target; 32 seconds a", fig78),
    80: ("The twitch the fitted model produces: activation peaks at 0.", fig80),
    82: ("Two panels. Left: two fitted twitches that both peak at 25 m", fig82),
}
