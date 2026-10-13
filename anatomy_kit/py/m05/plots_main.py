"""Module 5 main-text plots in the house style (group `plots_main`).

Every plotted number is computed here from the formula or the code the module states:
  f_L (Prop. 2.1 and Lab 1), GHK (Lemma 3.1), Hill a_inf (Prop. 3.1), the twitch and
  train model (Modelling assumption 3.2, K2's code), tau(Ca) (Prop. 5.1), the activation
  ODE (Def. 5.1), f_V (sec. 6 box), F_PE (sec. 7 box), d_m(theta) (Lab 1), the redundancy
  optimum (sec. 8), Lab 1 and Lab 2 (their code, unchanged).
All figures use a 760-unit-wide viewBox, so one user unit is one rendered px.
"""
import html
import math
from functools import lru_cache

import numpy as np

import house as H

T, O, I, SER = H.TISSUE, H.OVERLAY, H.INK, H.SERIES
GRID = "#e6e6e6"
BOXFILL = "#f7f4ef"


# ---------------------------------------------------------------- local plot scaffold
class Ax:
    """Plot box (x0, top, x1, bottom) in user units and one scale function per axis."""

    def __init__(self, box, xr, yr, xlog=False, ylog=False):
        self.x0, self.top, self.x1, self.y0 = box
        self.xr, self.yr, self.xlog, self.ylog = xr, yr, xlog, ylog

    def _f(self, v, r, log):
        if log:
            return (math.log10(v) - math.log10(r[0])) / (math.log10(r[1]) - math.log10(r[0]))
        return (v - r[0]) / (r[1] - r[0])

    def X(self, v):
        return self.x0 + self._f(v, self.xr, self.xlog) * (self.x1 - self.x0)

    def Y(self, v):
        return self.y0 - self._f(v, self.yr, self.ylog) * (self.y0 - self.top)

    @property
    def box(self):
        return [self.x0, self.top, self.x1, self.y0]


def axes(s, ax, xt, yt, xlab, ylab, grid=True, ylab_x=None, xlab_dy=46, right=None):
    """Grid, axis lines, ticks, tick labels and axis titles. xt / yt: [(value, text), ...]."""
    o = []
    if grid:
        for v, _ in yt:
            if abs(ax.Y(v) - ax.y0) > 1:
                o.append(H.line(s, ax.x0, ax.Y(v), ax.x1, ax.Y(v), GRID, "leader"))
    o.append(H.line(s, ax.x0, ax.y0, ax.x1, ax.y0, I["axis"], "axis"))
    o.append(H.line(s, ax.x0, ax.y0, ax.x0, ax.top, I["axis"], "axis"))
    for v, txt in yt:
        o.append(H.line(s, ax.x0 - 5, ax.Y(v), ax.x0, ax.Y(v), I["axis"], "leader"))
        o.append(H.label(s, ax.x0 - 9, ax.Y(v) + 4.5, txt, "tick", I["secondary"], "end"))
    for v, txt in xt:
        o.append(H.line(s, ax.X(v), ax.y0, ax.X(v), ax.y0 + 5, I["axis"], "leader"))
        o.append(H.label(s, ax.X(v), ax.y0 + 20, txt, "tick", I["secondary"], "middle"))
    if xlab:
        o.append(H.label(s, (ax.x0 + ax.x1) / 2, ax.y0 + xlab_dy, xlab, "label", I["primary"], "middle"))
    if ylab:
        yx = ylab_x if ylab_x is not None else ax.x0 - 56
        ym = (ax.y0 + ax.top) / 2
        o.append(H.label(s, yx, ym, ylab, "label", I["primary"], "middle", f'transform="rotate(-90 {yx:.2f} {ym:.2f})"'))
    return o


def pts_str(xy):
    return " ".join(f"{a:.2f},{b:.2f}" for a, b in xy)


def poly(s, xy, col, w="curve", dash=None, extra=""):
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    return (f'<polyline points="{pts_str(xy)}" fill="none" stroke="{col}" stroke-width="{s(H.PX[w]):.2f}" '
            f'stroke-linejoin="round"{da} {extra}/>')


def curve(s, ax, xs, ys, col, w="curve", dash=None, extra=""):
    return poly(s, [(ax.X(x), ax.Y(y)) for x, y in zip(xs, ys)], col, w, dash, extra)


def dot(s, x, y, col, hollow=False, r=None):
    r = s(r or H.PX["dot"])
    if hollow:
        return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="#fff" stroke="{col}" stroke-width="{s(1.8):.2f}"/>'
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{col}" stroke="#fff" stroke-width="{s(1.5):.2f}"/>'


DASH_SER = (7, 4)        # dashed series (px)


def legend(s, x, y, items, gap=26):
    """One row: [(colour, dash or None, text, kind)], kind 'line' (default), 'band' or 'dot'.
    Swatches are 26 units long (shorter than the 50-unit dashed-line overlap test)."""
    o = []
    for it in items:
        col, dash, txt = it[:3]
        kind = it[3] if len(it) > 3 else "line"
        if kind == "band":
            o.append(f'<rect x="{x:.2f}" y="{y-9:.2f}" width="22" height="10" fill="{col}" opacity="0.22"/>')
        elif kind == "dot":
            o.append(dot(s, x + 11, y - 4, col))
        elif kind == "hdot":
            o.append(dot(s, x + 11, y - 4, col, hollow=True))
        else:
            da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
            o.append(f'<line x1="{x:.2f}" y1="{y-4:.2f}" x2="{x+24:.2f}" y2="{y-4:.2f}" stroke="{col}" '
                     f'stroke-width="{s(H.PX["curve_multi"]):.2f}"{da}/>')
        o.append(H.label(s, x + 31, y, txt, "label2", I["primary"]))
        x += 31 + tw(txt) + gap
    return o


def tw(txt, px=13):
    """Rough width of plain text in Georgia at px (tags stripped)."""
    import re
    t = re.sub(r"<[^>]+>", "", txt)
    return 0.53 * px * len(t)


def hover(ax, xs, ys, texts):
    """[[x, y or [y...], text], ...] in user units, sorted by x."""
    pts = []
    for x, y, t in zip(xs, ys, texts):
        yy = [round(v, 2) for v in y] if isinstance(y, (list, tuple)) else round(y, 2)
        pts.append([round(x, 2), yy, t])
    pts.sort(key=lambda p: p[0])
    return H.hover_attr([round(v, 2) for v in ax.box], pts)


def svg(vb, aria, s, body, extra=""):
    return H.svg_open(vb, html.escape(aria), s, extra=extra) + "".join(body) + "</svg>"


def it(t):
    """Italic symbol."""
    return f'<tspan font-style="italic">{t}</tspan>'


# ---------------------------------------------------------------- shared models
def f_L_sarc(l):
    """Prop. 2.1, single sarcomere (µm): 1.27 -> 1.6 (0.8) -> 2.6 (1) -> 2.7 (1) -> 4.2 (0)."""
    p = [(1.27, 0.0), (1.60, 0.8), (2.60, 1.0), (2.70, 1.0), (4.20, 0.0)]
    if l <= p[0][0] or l >= p[-1][0]:
        return 0.0
    for (x0, y0), (x1, y1) in zip(p, p[1:]):
        if x0 <= l <= x1:
            return y0 + (y1 - y0) * (l - x0) / (x1 - x0)


def f_L_fib(L):
    """Lab 1 fibre-level length factor, L = l / l0."""
    if L <= 0.47 or L >= 1.556:
        return 0.0
    if L < 0.963:
        return (L - 0.47) / 0.493
    if L <= 1.0:
        return 1.0
    return (1.556 - L) / 0.556


C_HILL, K_ECC, F_ECC = 0.25, 20.0, 1.5


def f_V(v):
    """Sec. 6 box, v = v / v_max (positive = shortening)."""
    if v >= 0:
        return (1 - v) / (1 + v / C_HILL)
    return 1 + (F_ECC - 1) * K_ECC * (-v) / (1 + K_ECC * (-v))


# K2's twitch / train model, verbatim constants (ms, µM)
TR, TD, TAU_A = 3.6, 18.0, 41.0
T_PK = TR * np.log(1 + TD / TR)
NORM = (1 - np.exp(-T_PK / TR)) * np.exp(-T_PK / TD)


def pulse(t, s=1.0):
    tt = np.clip(t, 0.0, None)
    y = (1 - np.exp(-tt / (TR * s))) * np.exp(-tt / (TD * s))
    return np.where(t > 0, y / NORM, 0.0)


def a_inf(ca):
    return ca ** 3 / (1 + ca ** 3)


def run_train(times, T_end, dt=0.1):
    """Saturating calcium gate + activation ODE (K2), Euler as in K2. Returns t, ca, a."""
    t = np.arange(0.0, T_end, dt)
    prod = np.ones_like(t)
    for ti in times:
        prod *= 1 - pulse(t - ti)
    ca = 0.1 + 1.3 * (1 - prod)
    tgt = a_inf(ca)
    a = np.zeros_like(t)
    for i in range(1, len(t)):
        a[i] = a[i - 1] + dt * (tgt[i - 1] - a[i - 1]) / TAU_A
    return t, ca, a


@lru_cache(maxsize=None)
def train_stats(f, T_end=1200.0, dt=0.1):
    """K2's train(): mean, min, max of a over t > 0.6 T."""
    t, _, a = run_train(tuple(np.arange(0.0, T_end, 1000.0 / f)), T_end, dt)
    w = t > 0.6 * T_end
    return float(a[w].mean()), float(a[w].min()), float(a[w].max())


@lru_cache(maxsize=None)
def train_cycle(f, T_end=1200.0, dt=0.1):
    """Same run as K2's train(), averaged over whole firing periods inside t > 0.6 T. K2's fixed window
    holds a fractional number of periods, which makes its mean wobble below ~8 Hz; at 10, 25 and 60 Hz the
    two agree to 3 decimals (0.147, 0.380, 0.688)."""
    per = 1000.0 / f
    t, _, a = run_train(tuple(np.arange(0.0, T_end, per)), T_end, dt)
    k0 = math.ceil(0.6 * T_end / per) * per
    k1 = k0 + math.floor((T_end - k0) / per) * per
    w = (t >= k0) & (t < k1)
    return float(a[w].mean()), float(a[w].min()), float(a[w].max())


@lru_cache(maxsize=None)
def fusion_freq():
    """K2's sweep, fast fibre: first rate (0.5 Hz grid from 5 Hz) with ripple < 5 %."""
    for f in np.arange(5.0, 90.01, 0.5):
        m, lo, hi = train_stats(float(f))
        if (hi - lo) / m < 0.05:
            return float(f)


# ================================================================ svg #10 (ported ex_plot)
def fig10():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    x0, x1, y0, y1 = 80, 730, 330, 50
    L0, L1 = 1.0, 4.4
    X = lambda l: x0 + (l - L0) / (L1 - L0) * (x1 - x0)   # noqa: E731  one scale for ticks AND curve
    Y = lambda f: y0 - f / 1.1 * (y0 - y1)                # noqa: E731
    brk = [(1.27, 0.0), (1.60, 0.8), (2.60, 1.0), (2.70, 1.0), (4.20, 0.0)]
    o = [f'<rect x="{X(2.6):.2f}" y="{y1}" width="{X(2.7)-X(2.6):.2f}" height="{y0-y1}" fill="{O["neural"]}" opacity="0.12"/>']
    for f in (0.5, 1.0):
        o.append(H.line(s, x0, Y(f), x1, Y(f), GRID, "leader"))
    o.append(H.line(s, x0, y0, x1, y0, I["axis"], "axis"))
    o.append(H.line(s, x0, y0, x0, y1, I["axis"], "axis"))
    for f in (0.0, 0.5, 1.0):
        o.append(H.line(s, x0 - 5, Y(f), x0, Y(f), I["axis"], "leader"))
        o.append(H.label(s, x0 - 9, Y(f) + 4.5, f"{f:.1f}", "tick", I["secondary"], "end"))
    for l, txt in ((1.27, "1.27"), (1.6, "1.6"), (2.0, "2"), (3.0, "3"), (4.0, "4"), (4.2, "4.2")):
        o.append(H.line(s, X(l), y0, X(l), y0 + 5, I["axis"], "leader"))
        o.append(H.label(s, X(l), y0 + 20, txt, "tick", I["secondary"], "middle"))
    o.append(H.line(s, X(2.6), y0 + 8, X(2.7), y0 + 8, O["neural"], "ref"))
    o.append(H.label(s, X(2.65), y0 + 34, "2.60–2.70", "tick", I["secondary"], "middle"))
    pts = [(X(L0), Y(0))] + [(X(l), Y(f)) for l, f in brk] + [(X(L1), Y(0))]
    o.append(poly(s, pts, SER[0]))
    # four geometric breakpoints (orange); the 1.27 zero is an empirical extrapolation (hollow)
    for l, f in brk:
        o.append(dot(s, X(l), Y(f), O["flag"]) if l != 1.27 else dot(s, X(l), Y(f), I["secondary"], hollow=True))
    o.append(dot(s, 476, 62, O["flag"]))
    o.append(H.label(s, 488, 67, "geometric breakpoint (1.6, 2.6, 2.7, 4.2)", "label2", I["secondary"]))
    o.append(dot(s, 476, 84, I["secondary"], hollow=True))
    o.append(H.label(s, 488, 89, "zero near 1.27: empirical extrapolation", "label2", I["secondary"]))
    o.append(H.label(s, X(2.15), Y(0.62), "ascending limb", "label2", I["secondary"], "middle", 'font-style="italic"'))
    o.append(H.label(s, X(2.15), Y(0.62) + 16, "(double overlap, then", "label2", I["muted"], "middle"))
    o.append(H.label(s, X(2.15), Y(0.62) + 32, "thick-filament compression)", "label2", I["muted"], "middle"))
    o.append(H.label(s, X(2.65), Y(1.0) - 26, "plateau", "label", I["primary"], "middle"))
    o.append(H.label(s, X(2.65), Y(1.0) - 10, "ℓ₀ ≈ 2.7 µm", "label2", I["secondary"], "middle"))
    o.append(H.label(s, X(3.55), Y(0.62), "descending limb", "label2", I["secondary"], "start", 'font-style="italic"'))
    o.append(H.label(s, (x0 + x1) / 2, 390, "sarcomere length ℓ (µm)", "label", I["primary"], "middle"))
    o.append(H.label(s, 24, (y0 + y1) / 2, f'active force f{H.sub("L", s)}(ℓ), normalised', "label", I["primary"], "middle",
                     f'transform="rotate(-90 24 {(y0 + y1) / 2})"'))
    aria = ("Active length-tension curve: normalised force against sarcomere length. Zero below 1.27 micrometres, rising "
            "to 0.8 at 1.6 and 1.0 at 2.6, flat to 2.7, then falling linearly to zero at 4.2 micrometres. Orange dots mark "
            "the four geometric breakpoints 1.6, 2.6, 2.7 and 4.2; a hollow dot marks the empirical zero near 1.27.")
    hv = [[round(X(l), 2), round(Y(f_L_sarc(l)), 2), f"ℓ = {l:.2f} µm, f = {f_L_sarc(l):.2f}"]
          for l in (L0 + i * 0.02 for i in range(int(round((L1 - L0) / 0.02)) + 1))]
    return H.svg_open(VB, html.escape(aria), s, extra=H.hover_attr([x0, y1, x1, y0], hv)) + "".join(o) + "</svg>"


def mn(v, f="{:.1f}", plus=False):
    """Number with a Unicode minus (and an optional plus sign)."""
    t = f.format(v)
    if t.startswith("-"):
        return "−" + t[1:]
    return ("+" + t) if plus and v > 0 else t


def legend_col(s, x, y, items, dy=20):
    o = []
    for k, item in enumerate(items):
        o += legend(s, x, y + k * dy, [item])
    return o


def lead(s, x1, y1, x2, y2, col):
    """1 px leader in the series colour, from a label to its curve."""
    return H.line(s, x1, y1, x2, y2, col, "leader")


CA_LINE = T["fluid"][1]                       # ions are drawn in the fluid blue (the author, 2026-10-12)


def sub(t, s):
    return H.sub(t, s, "label2")


# ================================================================ svg #8: the ATP ledger
def fig8():
    VB = (0, 0, 760, 412)
    s = H.Scale(VB[2], VB[3])
    NA, KBT, D = 6.02214076e23, 4.28e-21, 10e-9          # 1/mol, J at 37 °C (text), m (stroke)
    g_rest, g_fat = 62.5, 52.7                           # |ΔG|, kJ/mol (text)
    e_rest, e_fat = g_rest * 1e3 / NA / KBT, g_fat * 1e3 / NA / KBT
    e_st = {f: f * 1e-12 * D / KBT for f in (6, 5, 3)}
    ceil_rest, ceil_fat = g_rest * 1e3 / NA / D * 1e12, g_fat * 1e3 / NA / D * 1e12
    eta_rest, eta_fat = e_st[5] / e_rest, e_st[5] / e_fat
    bars = [("one ATP", "resting muscle", "ΔG = −62.5 kJ/mol", e_rest, O["neural"]),
            ("one ATP", "end of a hard bout", "ΔG = −52.7 kJ/mol", e_fat, O["neural"]),
            ("one stroke", "6 pN × 10 nm", "", e_st[6], O["force"]),
            ("one stroke", "5 pN × 10 nm", "", e_st[5], O["force"]),
            ("one stroke", "3 pN × 10 nm", "", e_st[3], O["force"])]
    ax = Ax((90, 40, 740, 290), (0, 5), (0, 27))
    kbt = f'k{sub("B", s)}T'
    o = axes(s, ax, [], [(v, f"{v}") for v in (0, 5, 10, 15, 20, 25)], None,
             f'energy per event (k{H.sub("B", s)}T at 37 °C)', ylab_x=30)
    # the fatigued ATP budget: every stroke bar stays below it
    o.append(H.line(s, ax.X(2.0), ax.Y(e_fat), ax.X(5.0), ax.Y(e_fat), O["neural"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(5.0), ax.Y(e_fat) - 8, f"fatigued ATP, {e_fat:.1f} {kbt}: no stroke reaches it",
                     "label2", I["primary"], "end"))
    hv = []
    for i, (a, b, c, e, col) in enumerate(bars):
        xc = ax.X(i + 0.5)
        o.append(f'<rect x="{xc-32:.2f}" y="{ax.Y(e):.2f}" width="64" height="{ax.y0-ax.Y(e):.2f}" fill="{col}"/>')
        o.append(H.label(s, xc, ax.Y(e) - 7, f"{e:.1f} {kbt}", "label2", I["primary"], "middle"))
        for k, t in enumerate((a, b, c)):
            if t:
                o.append(H.label(s, xc, ax.y0 + 20 + 16 * k, t, "label2", I["primary"] if k == 0 else I["secondary"], "middle"))
        hv.append([xc, ax.Y(e), f"{a}, {b}: {e:.1f} kBT"])
    o.append(H.label(s, 20, 368, f"At 5 pN one stroke spends {100*eta_rest:.0f} % of a resting ATP and {100*eta_fat:.0f} % "
                     f"of a fatigued one (efficiency η{sub('xb', s)} = {eta_rest:.2f}, {eta_fat:.2f}).", "label2", I["primary"]))
    o.append(H.label(s, 20, 390, f"Force ceiling |ΔG|/(N{sub('A', s)}d): {ceil_rest:.2f} pN resting, {ceil_fat:.2f} pN "
                     f"fatigued; measured head force 3–6 pN.", "label2", I["primary"]))
    aria = (f"Vertical bar chart in units of thermal energy kBT at 37 degrees C. One ATP is worth {e_rest:.1f} units in "
            f"resting muscle and {e_fat:.1f} at the end of a hard bout (green); one 10 nanometre power stroke costs "
            f"{e_st[6]:.1f} units at 6 piconewtons, {e_st[5]:.1f} at 5 and {e_st[3]:.1f} at 3 (red). A dashed line at the "
            f"fatigued ATP value lies above every stroke bar. At 5 pN a stroke spends {100*eta_rest:.0f} and "
            f"{100*eta_fat:.0f} percent of an ATP; the force ceiling is {ceil_rest:.2f} and {ceil_fat:.2f} piconewtons.")
    return svg(VB, aria, s, o, hover(ax, *zip(*hv)))


# ================================================================ svg #13: Goldman-Hodgkin-Katz
RTF = 26.73                                                   # mV at 37 °C (text)
K_OI, NA_OI, CL_OI = (4, 140), (145, 12), (116, 4)            # mM outside / inside (text)


def ghk(r, pcl):
    num = K_OI[0] + r * NA_OI[0] + pcl * CL_OI[1]
    den = K_OI[1] + r * NA_OI[1] + pcl * CL_OI[0]
    return RTF * math.log(num / den)


def fig13():
    VB = (0, 0, 760, 400)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 30, 735, 320), (1e-3, 100), (-110, 80), xlog=True)
    EK, ENA = RTF * math.log(K_OI[0] / K_OI[1]), RTF * math.log(NA_OI[0] / NA_OI[1])
    rs = [10 ** (-3 + 5 * i / 110) for i in range(111)]
    o = axes(s, ax, [(v, t) for v, t in ((1e-3, "0.001"), (1e-2, "0.01"), (0.1, "0.1"), (1, "1"), (10, "10"), (100, "100"))],
             [(v, mn(v, "{:.0f}")) for v in (-100, -50, 0, 50)],
             f'permeability ratio P{H.sub("Na", s)}/P{H.sub("K", s)} (log scale)', "membrane potential V (mV)")
    for E, lab, yy, anc, xx in ((ENA, f'E{sub("Na", s)} = {mn(ENA, plus=True)} mV (Nernst, Module 0)', -11, "start", ax.x0 + 8),
                                (EK, f'E{sub("K", s)} = {mn(EK)} mV (Nernst, Module 0)', 17, "end", ax.x1 - 4)):
        o.append(H.line(s, ax.x0, ax.Y(E), ax.x1, ax.Y(E), O["flag"], "ref", H.DASH_REF))
        o.append(H.label(s, xx, ax.Y(E) + yy, lab, "label2", I["secondary"], anc))
    o.append(curve(s, ax, rs, [ghk(r, 0) for r in rs], SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, ax, rs, [ghk(r, 2) for r in rs], SER[0], "curve_multi"))
    vr, vs = ghk(0.02, 2), ghk(20, 2)
    # 128 mV swing between the two states, same equation
    o.append(H.line(s, ax.X(0.02), ax.Y(vr), ax.X(20), ax.Y(vr), I["secondary"], "leader", (3, 3)))
    o.append(H.line(s, ax.X(20), ax.Y(vr) - 6, ax.X(20), ax.Y(vs) + 6, O["geometry"], "geom",
                    extra='marker-start="url(#m5f13_a_geometry)" marker-end="url(#m5f13_a_geometry)"'))
    o.append(H.label(s, ax.X(20) - 9, ax.Y(-22), f"{vs - vr:.0f} mV swing", "label2", I["primary"], "end"))
    o.append(dot(s, ax.X(0.02), ax.Y(ghk(0.02, 0)), SER[1], hollow=True))
    o.append(dot(s, ax.X(20), ax.Y(ghk(20, 0)), SER[1], hollow=True))
    o.append(dot(s, ax.X(0.02), ax.Y(vr), SER[0]))
    o.append(dot(s, ax.X(20), ax.Y(vs), SER[0]))
    o.append(H.line(s, ax.X(0.0045), ax.Y(-58), ax.X(0.02) - 3, ax.Y(vr) - 5, I["rule"], "leader"))
    o.append(H.label(s, ax.X(0.0011), ax.Y(-48), "rest: ratio 0.02", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.0011), ax.Y(-48) + 16, f"V = {mn(vr, '{:.0f}')} mV", "label2", I["primary"]))
    o.append(H.label(s, ax.X(20) + 10, ax.Y(25), "spike: ratio 20", "label2", I["primary"]))
    o.append(H.label(s, ax.X(20) + 10, ax.Y(25) + 16, f"V = {mn(vs, '{:.0f}', True)} mV", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.03), ax.Y(-38), "K⁺, Na⁺ only", "label2", I["primary"]))
    o.append(lead(s, ax.X(0.08), ax.Y(-38) + 4, ax.X(0.08), ax.Y(ghk(0.08, 0)) - 3, SER[1]))
    o.append(H.label(s, ax.X(1.05), ax.Y(-42), "with Cl⁻", "label2", I["primary"]))
    o.append(lead(s, ax.X(1.4), ax.Y(-42) - 13, ax.X(1.4), ax.Y(ghk(1.4, 2)) + 3, SER[0]))
    o += legend_col(s, ax.x0 + 12, ax.Y(42), [
        (SER[0], None, f'with Cl⁻, P{sub("Cl", s)}/P{sub("K", s)} = 2'),
        (SER[1], DASH_SER, f"K⁺ and Na⁺ only: {mn(ghk(0.02, 0))} and {mn(ghk(20, 0), '{:.0f}', True)} mV at the same ratios")])
    aria = (f"Goldman-Hodgkin-Katz membrane potential against the sodium-to-potassium permeability ratio on a log axis from "
            f"0.001 to 100. With chloride at twice the potassium permeability (red) the potential is {mn(vr)} mV at the "
            f"resting ratio 0.02 and {mn(vs, plus=True)} mV at the spike ratio 20, a {vs - vr:.0f} mV swing; without "
            f"chloride (blue dashed) the same ratios give {mn(ghk(0.02, 0))} and {mn(ghk(20, 0), plus=True)} mV. Dashed "
            f"orange lines mark the Nernst potentials {mn(ENA, plus=True)} mV for sodium and {mn(EK)} mV for potassium.")
    hr = [10 ** (-3 + 5 * i / 160) for i in range(161)]
    hv = hover(ax, [ax.X(r) for r in hr], [[ax.Y(ghk(r, 2)), ax.Y(ghk(r, 0))] for r in hr],
               [f"PNa/PK = {r:.3g}: {mn(ghk(r, 2))} mV with Cl⁻, {mn(ghk(r, 0))} mV without" for r in hr])
    return svg(VB, aria, s, [f"<defs>{H.markers('m5f13_', s)}</defs>"] + o, hv)


# ================================================================ svg #15: Hill activation switch
def fig15():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 30, 735, 300), (0.03, 10), (0, 1.05), xlog=True)
    cs = [10 ** (math.log10(0.03) + (1 + math.log10(1 / 0.03)) * i / 110) for i in range(111)]
    o = axes(s, ax, [(v, f"{v:g}") for v in (0.03, 0.1, 0.3, 1, 3, 10)], [(v, f"{v:.1f}") for v in (0, 0.5, 1.0)],
             "free Ca²⁺ concentration (µM, log scale)", f'steady-state activation a{sub("∞", s)}')
    o.append(H.line(s, ax.X(1), ax.Y(0.5), ax.X(1), ax.y0, I["rule"], "leader", H.DASH_REF))
    o.append(curve(s, ax, cs, [a_inf(c) for c in cs], SER[0]))
    for c, txt, dx, dy, anc in ((0.1, f"rest 0.1 µM: a{sub('∞', s)} = {a_inf(0.1):.3f}", 0, -12, "middle"),
                                (1.0, f"Ca{sub('50', s)} = 1 µM: a{sub('∞', s)} = 0.50 (half-maximal)", 12, 20, "start"),
                                (1.4, f"twitch calcium peak 1.4 µM: a{sub('∞', s)} = {a_inf(1.4):.2f} if held", -12, -4, "end")):
        o.append(dot(s, ax.X(c), ax.Y(a_inf(c)), O["flag"]))
        o.append(H.label(s, ax.X(c) + dx, ax.Y(a_inf(c)) + dy, txt, "label2", I["primary"], anc))
    o.append(H.label(s, ax.X(0.04), ax.Y(0.45), "cooperative Hill curve", "label", I["primary"], extra='font-style="italic"'))
    o.append(H.label(s, ax.X(0.04), ax.Y(0.45) + 18, f"n = 3, Ca{sub('50', s)} = 1 µM: an on/off switch", "label2", I["secondary"]))
    aria = ("Steady-state activation a-infinity versus free calcium on a log axis from 0.03 to 10 micromolar, from "
            "Proposition 3.1 with n = 3 and Ca50 = 1 micromolar. Activation is 0.001 at resting calcium 0.1, 0.50 at Ca50, "
            f"and {a_inf(1.4):.2f} at the twitch calcium peak of 1.4 micromolar if that level were held.")
    hc = [10 ** (math.log10(0.03) + (1 + math.log10(1 / 0.03)) * i / 200) for i in range(201)]
    hv = hover(ax, [ax.X(c) for c in hc], [ax.Y(a_inf(c)) for c in hc],
               [f"Ca²⁺ = {c:.3g} µM: a∞ = {a_inf(c):.3f}" for c in hc])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #16: the single twitch
@lru_cache(maxsize=None)
def twitch_fine():
    t, ca, a = run_train((0.0,), 140.005, dt=0.01)
    i = int(a.argmax())
    j = int(np.where((t > t[i]) & (a < a[i] / 2))[0][0])
    return t, ca, a, i, j


def fig16():
    VB = (0, 0, 760, 410)
    s = H.Scale(VB[2], VB[3])
    t, ca, a, ip, jh = twitch_fine()
    ax = Ax((80, 50, 735, 300), (-10, 140), (0, 1.0))
    shape = 0.9 * (ca - 0.1) / 1.3                       # p(t), drawn to 0.9 of the axis: shape only
    o = axes(s, ax, [(v, f"{v}") for v in range(0, 141, 20)], [(v, f"{v:.1f}") for v in (0, 0.5, 1.0)],
             None, "activation a", xlab_dy=0)
    o.append(H.label(s, (ax.x0 + ax.x1) / 2, ax.y0 + 76, "time after the action potential (ms)", "label", I["primary"], "middle"))
    ceil = a_inf(1.4)
    o.append(H.line(s, ax.x0, ax.Y(ceil), ax.x1, ax.Y(ceil), O["flag"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.x1 - 4, ax.Y(ceil) - 11, f"tetanic ceiling a{sub('∞', s)} ≈ {ceil:.2f} (calcium held at 1.4 µM, §4)",
                     "label2", I["secondary"], "end"))
    sel = [k for k in range(0, len(t), 150)] + [len(t) - 1]
    o.append(curve(s, ax, [-10, 0] + [t[k] for k in sel], [0, 0] + [shape[k] for k in sel], CA_LINE, "curve_multi", DASH_SER))
    o.append(curve(s, ax, [-10, 0] + [t[k] for k in sel], [0, 0] + [a[k] for k in sel], SER[0], "curve_multi"))
    # action potential at t = 0: an impulse tick under the axis (green, as in Figs. 15-16)
    o.append(H.line(s, ax.X(0), ax.y0 + 28, ax.X(0), ax.y0 + 44, O["neural"], "curve"))
    o.append(H.label(s, ax.X(0) + 8, ax.y0 + 42, "one action potential at t = 0", "label2", I["primary"]))
    o.append(H.label(s, ax.X(11), ax.Y(0.93), "Ca²⁺ peak 1.4 µM at 6.4 ms", "label2", I["primary"]))
    tp, ap, th, ah = t[ip], a[ip], t[jh], a[jh]
    o.append(dot(s, ax.X(tp), ax.Y(ap), O["flag"]))
    o.append(dot(s, ax.X(th), ax.Y(ah), O["flag"]))
    o.append(H.line(s, ax.X(tp) + 2, ax.Y(ap) - 4, ax.X(44) - 2, ax.Y(0.47) + 4, I["rule"], "leader"))
    o.append(H.label(s, ax.X(44), ax.Y(0.47), f"peak a = {ap:.2f} at {tp:.1f} ms", "label2", I["primary"]))
    o.append(H.line(s, ax.X(th) + 3, ax.Y(ah) - 4, ax.X(72) - 2, ax.Y(0.33) + 4, I["rule"], "leader"))
    o.append(H.label(s, ax.X(72), ax.Y(0.33), f"half-relaxed at {th:.1f} ms ({th - tp:.1f} ms after the peak)", "label2", I["primary"]))
    o += legend(s, ax.x0, 26, [(SER[0], None, "activation a (force ∝ a)"), (CA_LINE, DASH_SER, "free Ca²⁺, shape only"),
                               (O["neural"], None, "action potential")])
    aria = (f"Single-twitch time course after one action potential at time zero (green tick). The free calcium transient "
            f"(blue dashed, shape only) peaks at 1.4 micromolar 6.4 ms after the impulse and is gone within tens of ms. "
            f"Activation a (red) peaks at {ap:.2f} at {tp:.1f} ms and is half-relaxed at {th:.1f} ms, {th - tp:.1f} ms after "
            f"the peak, far below the dashed tetanic ceiling {ceil:.2f}.")
    hk = list(range(0, len(t), 100))
    hv = hover(ax, [ax.X(-10)] + [ax.X(t[k]) for k in hk], [[ax.Y(0), ax.Y(0)]] + [[ax.Y(a[k]), ax.Y(shape[k])] for k in hk],
               ["before the impulse: a = 0"] + [f"t = {t[k]:.0f} ms: a = {a[k]:.3f}, Ca²⁺ = {ca[k]:.2f} µM" for k in hk])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #18: recruitment staircase
N_MU = 9
U_THR = [0.04 + 0.095 * k for k in range(N_MU)]                 # recruitment thresholds in u
R_MU = 100 ** (1 / (N_MU - 1))                                  # largest unit = 100 x smallest (line 1051)
F_MU = [R_MU ** k / sum(R_MU ** j for j in range(N_MU)) for k in range(N_MU)]
CLS = [(0, 3, O["neural"], "S"), (3, 6, SER[2], "FR"), (6, 9, SER[0], "FF")]   # caption colours: green, orange, red


def stair(u):
    n = sum(1 for th in U_THR if u >= th)
    return n, sum(F_MU[:n])


def fig18():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    p = "m5f18_"
    ax = Ax((370, 40, 740, 300), (0, 1), (0, 1))
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, ax, [(v, f"{v:.2f}") for v in (0, 0.25, 0.5, 0.75, 1.0)], [(v, f"{v:.2f}") for v in (0, 0.25, 0.5, 0.75, 1.0)],
              "neural drive u", "cumulative force (fraction of maximum)", ylab_x=ax.x0 - 54)
    cum = [sum(F_MU[:k]) for k in range(N_MU + 1)]
    for k0, k1, col, _ in CLS:
        xy = [(ax.X(0 if k0 == 0 else U_THR[k0]), ax.Y(cum[k0]))]
        for k in range(k0, k1):
            xy += [(ax.X(U_THR[k]), ax.Y(cum[k])), (ax.X(U_THR[k]), ax.Y(cum[k + 1]))]
            nxt = U_THR[k + 1] if k + 1 < N_MU else 1.0
            xy.append((ax.X(nxt), ax.Y(cum[k + 1])))
        o.append(poly(s, xy, col))
    for k in range(N_MU):
        col = next(c for a0, a1, c, _ in CLS if a0 <= k < a1)
        o.append(dot(s, ax.X(U_THR[k]), ax.Y(cum[k + 1]), col, r=3 + 5 * math.sqrt(F_MU[k] / F_MU[-1])))
    o.append(H.label(s, ax.X(0.03), ax.Y(0.13), f"small (S): steps of {100*F_MU[0]:.1f}–{100*F_MU[2]:.1f} %", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.22), ax.Y(0.27), f"medium (FR): {100*F_MU[3]:.1f}–{100*F_MU[5]:.0f} %", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.02), ax.Y(0.80), f"large (FF): steps of {100*F_MU[6]:.0f}–{100*F_MU[8]:.0f} %", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.02), ax.Y(0.80) + 17, "largest step = 100 × smallest", "label2", I["secondary"]))
    o.append(lead(s, ax.X(0.02) + tw(f"large (FF): steps of {100*F_MU[6]:.0f}–{100*F_MU[8]:.0f} %") + 6, ax.Y(0.80) - 4,
                  ax.X(U_THR[7]) - 4, ax.Y(0.45), SER[0]))
    o += legend(s, ax.x0, 24, [(O["neural"], None, "S"), (SER[2], None, "FR"), (SER[0], None, "FF")], gap=18)
    # inset: Ohm's law sets the order
    bx0, by0, bx1, by1 = 10, 40, 284, 330
    o.append(f'<rect x="{bx0}" y="{by0}" width="{bx1-bx0}" height="{by1-by0}" rx="6" fill="{BOXFILL}" stroke="{I["rule"]}" stroke-width="1"/>')
    o.append(H.label(s, (bx0 + bx1) / 2, by0 + 22, "same drive current I to both cells", "label2", I["primary"], "middle"))
    thr = 215
    o.append(H.label(s, thr, by0 + 48, "threshold", "label2", I["primary"], "middle"))
    for (yy, r, col, name, w, note) in ((by0 + 88, 9, O["neural"], "small cell, high R", 122, "ΔV crosses threshold: fires first"),
                                        (by0 + 182, 22, SER[0], "large cell, low R", 45, "ΔV stays below threshold")):
        o.append(H.label(s, bx0 + 12, yy - r - 10, name, "label2", I["primary"]))
        o.append(H.arrow(s, p, bx0 + 12, yy, 92 - r - 4, yy, "dim"))
        o.append(f'<circle cx="92" cy="{yy}" r="{r}" fill="#fff" stroke="{col}" stroke-width="{s(2):.2f}"/>')
        o.append(f'<rect x="128" y="{yy-7}" width="{w}" height="14" fill="{col}" opacity="0.75"/>')
        o.append(H.line(s, thr, yy - 15, thr, yy + 15, O["force"], "ref", (4, 3)))
        o.append(H.label(s, bx0 + 12, yy + r + 20, note, "label2", I["primary"]))
    o.append(H.label(s, (bx0 + bx1) / 2, by1 - 34, "ΔV = I R", "label", I["primary"], "middle"))
    o.append(H.label(s, (bx0 + bx1) / 2, by1 - 14, "high R reaches threshold first", "label2", I["secondary"], "middle"))
    aria = ("Recruitment staircase: cumulative force versus neural drive u for nine motor units recruited at thresholds "
            "from u = 0.04 to 0.80, coloured small S green, medium FR orange and large FF red. The steps grow geometrically, "
            f"from {100*F_MU[0]:.1f} percent of maximum force for the smallest unit to {100*F_MU[8]:.0f} percent for the "
            "largest, a 100-fold range. An inset shows the same current I into a small high-resistance cell and a large "
            "low-resistance cell: by Delta V = I R the small cell crosses threshold first.")
    hu = [i / 200 for i in range(201)]
    hv = hover(ax, [ax.X(u) for u in hu], [ax.Y(stair(u)[1]) for u in hu],
               [f"u = {u:.3f}: {stair(u)[0]} of {N_MU} units on, force {stair(u)[1]:.3f}" for u in hu])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #19: twitch summation
RATES = [(None, SER[3], "1 impulse (twitch)"), (10, SER[1], "10 Hz"), (25, SER[2], "25 Hz"), (60, SER[0], "60 Hz")]


@lru_cache(maxsize=None)
def trace(rate, T_end=300.0):
    times = (0.0,) if rate is None else tuple(np.arange(0.0, T_end, 1000.0 / rate))
    return run_train(times, T_end + 0.1, 0.1)


def fig19():
    VB = (0, 0, 760, 420)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 46, 612, 300), (0, 300), (0, 0.8))
    o = axes(s, ax, [(v, f"{v}") for v in range(0, 301, 50)], [(v, f"{v:.1f}") for v in (0, 0.2, 0.4, 0.6, 0.8)],
             None, "activation a (force ∝ a)")
    o.append(H.label(s, (ax.x0 + ax.x1) / 2, ax.y0 + 104, "time (ms)", "label", I["primary"], "middle"))
    ceil = a_inf(1.4)
    o.append(H.line(s, ax.x0, ax.Y(ceil), ax.x1, ax.Y(ceil), O["flag"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.x0 + 8, ax.Y(ceil) - 11, f"tetanic ceiling a{sub('∞', s)} ≈ {ceil:.2f}", "label2", I["secondary"]))
    ts = np.linspace(0, 300, 118)
    ends = []
    for rate, col, name in RATES:
        t, _, a = trace(rate)
        ys = np.interp(ts, t, a)
        o.append(curve(s, ax, ts, ys, col, "curve_multi"))
        ends.append(ys[-1])
    # impulse combs under the axis
    for k, (rate, col, name) in enumerate(RATES[1:]):
        yy = ax.y0 + 32 + 16 * k
        o.append(H.label(s, ax.x0 - 9, yy + 4, f"{rate} Hz", "label2", I["primary"], "end"))
        for ti in np.arange(0.0, 300.0, 1000.0 / rate):
            o.append(H.line(s, ax.X(ti), yy - 6, ax.X(ti), yy + 6, col, "ref"))
    # direct labels at the right end, with the steady means from K2
    lab = {10: "10 Hz, unfused", 25: "25 Hz", 60: "60 Hz, fused"}
    ypos = {10: ax.Y(0.21), 25: ax.Y(0.40) - 2, 60: ax.Y(0.69) + 4}
    for (rate, col, name), e in zip(RATES, ends):
        yl = ypos.get(rate, ax.Y(0.0) - 6) - 4
        o.append(lead(s, ax.x1 + 2, ax.Y(e), ax.x1 + 8, yl, col))
    for rate, col, name in RATES[1:]:
        o.append(H.label(s, ax.x1 + 10, ypos[rate], lab[rate], "label2", I["primary"]))
        o.append(H.label(s, ax.x1 + 10, ypos[rate] + 16, f"mean ā = {train_stats(float(rate))[0]:.2f}", "label2", I["secondary"]))
    o.append(H.label(s, ax.x1 + 10, ax.Y(0.0) - 6, "1 impulse (twitch)", "label2", I["primary"]))
    o += legend(s, ax.x0, 26, [(c, None, n) for _, c, n in RATES])
    m10, m25, m60 = (train_stats(float(r))[0] for r in (10, 25, 60))
    aria = ("Activation versus time for one fibre at four firing rates, from the saturating calcium model of section 4. "
            f"A single impulse gives a twitch peaking near 0.22. At 10 Hz the twitches barely sum (unfused, mean {m10:.2f}); "
            f"at 25 Hz the ripple shrinks and the mean climbs to {m25:.2f}; at 60 Hz the ripple is gone and activation sits "
            f"on a fused plateau, mean {m60:.2f}, just under the dashed ceiling {ceil:.2f}. Impulse ticks for each rate run "
            "under the time axis.")
    hts = np.arange(0, 300.01, 2.5)
    cols = [np.interp(hts, *trace(r)[0::2]) for r, _, _ in RATES]
    hv = hover(ax, [ax.X(x) for x in hts], [[ax.Y(c[i]) for c in cols] for i in range(len(hts))],
               [f"t = {x:.1f} ms: twitch {cols[0][i]:.2f}, 10 Hz {cols[1][i]:.2f}, 25 Hz {cols[2][i]:.2f}, 60 Hz {cols[3][i]:.2f}"
                for i, x in enumerate(hts)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #20: fused tetanus build-up (animated)
def fig20():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 40, 735, 290), (0, 300), (0, 0.8))
    t, _, a = trace(60)
    per = 1000.0 / 60
    imp = list(np.arange(0.0, 300.0, per))
    tk = [k * per for k in range(19)]                         # one frame per impulse, 0 .. 300 ms
    tk[-1] = 300.0
    ts = np.linspace(0, 300, 118)
    ys = np.interp(ts, t, a)
    o = axes(s, ax, [(v, f"{v}") for v in range(0, 301, 50)], [(v, f"{v:.1f}") for v in (0, 0.2, 0.4, 0.6, 0.8)],
             None, "activation a")
    o.append(H.label(s, (ax.x0 + ax.x1) / 2, ax.y0 + 66, "time (ms)", "label", I["primary"], "middle"))
    ceil = a_inf(1.4)
    o.append(H.line(s, ax.x0, ax.Y(ceil), ax.x1, ax.Y(ceil), O["flag"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.x1 - 4, ax.Y(ceil) - 11, f"fused ceiling a{sub('∞', s)} ≈ {ceil:.2f}", "label2", I["secondary"], "end"))
    o.append(curve(s, ax, ts, ys, SER[0], "curve_multi", extra='opacity="0.3"'))
    yy = ax.y0 + 30
    o.append(H.label(s, ax.x0 - 9, yy + 4, "60 Hz", "label2", I["primary"], "end"))
    for ti in imp:
        o.append(H.line(s, ax.X(ti), yy - 7, ax.X(ti), yy + 7, O["neural"], "ref", extra='opacity="0.3"'))
    frames = []
    last = len(tk) - 1
    for k, tt in enumerate(tk):
        sel = [(x, y) for x, y in zip(ts, ys) if x < tt] + [(tt, float(np.interp(tt, t, a)))]
        at = sel[-1][1]
        body = [curve(s, ax, [p[0] for p in sel], [p[1] for p in sel], SER[0], "curve") if len(sel) > 1 else ""]
        body += [H.line(s, ax.X(ti), yy - 7, ax.X(ti), yy + 7, O["neural"], "ref") for ti in imp if ti <= tt + 1e-6]
        body.append(dot(s, ax.X(tt), ax.Y(at), SER[0], r=5.5))
        n_imp = sum(1 for ti in imp if ti <= tt + 1e-6)
        body.append(H.label(s, ax.x0 + 12, ax.Y(0.665), f"t = {tt:.0f} ms, a = {at:.2f}", "label", I["primary"]))
        body.append(H.label(s, ax.x0 + 12, ax.Y(0.665) + 18, f"{n_imp} impulse{'s' if n_imp != 1 else ''} so far", "label2",
                            I["secondary"]))
        frames.append(H.frame(k, last, "".join(body)))
    o += frames
    aria = ("Build-up of a 60 Hz fused tetanus, drawn frame by frame. Green ticks under the time axis are the impulses, "
            "one every 16.7 ms; the red curve and dot are the activation a from the same integration as the 60 Hz trace "
            f"of the summation figure. Each impulse lands before a can relax, so it ratchets up toward the fused ceiling "
            f"{ceil:.2f}, reaching {float(np.interp(300, t, a)):.2f} at 300 ms. The still frame shows the whole build-up.")
    fa = H.frames_attr("time", [f"{x:.0f} ms" for x in tk], last)
    return svg(VB, aria, s, o, fa)


# ================================================================ svg #21: force-frequency curve
def fig21():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 40, 735, 300), (0, 90), (0, 0.8))
    fs = [float(f) for f in np.arange(4.0, 90.01, 0.5)]
    st = [train_cycle(f) for f in fs]
    ff = fusion_freq()
    o = axes(s, ax, [(v, f"{v}") for v in range(0, 91, 10)], [(v, f"{v:.1f}") for v in (0, 0.2, 0.4, 0.6, 0.8)],
             "firing rate (Hz)", "mean activation ā")
    band = [(ax.X(f), ax.Y(x[2])) for f, x in zip(fs, st)] + [(ax.X(f), ax.Y(x[1])) for f, x in reversed(list(zip(fs, st)))]
    o.append(f'<polygon points="{pts_str(band)}" fill="{SER[0]}" opacity="0.14"/>')
    ceil = a_inf(1.4)
    o.append(H.line(s, ax.x0, ax.Y(ceil), ax.x1, ax.Y(ceil), O["flag"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.x0 + 8, ax.Y(ceil) - 11, f"ceiling a{sub('∞', s)} ≈ {ceil:.2f}", "label2", I["secondary"]))
    o.append(H.line(s, ax.X(ff), ax.y0, ax.X(ff), ax.Y(0.76), O["neural"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(ff) + 8, ax.Y(0.30), f"fusion frequency {ff:.1f} Hz:", "label2", I["primary"]))
    o.append(H.label(s, ax.X(ff) + 8, ax.Y(0.30) + 16, "ripple under 5 % of the mean", "label2", I["primary"]))
    o.append(H.label(s, ax.X(ff) + 8, ax.Y(0.30) + 32, "≈ 1/(25 ms contraction time) = 40 Hz", "label2", I["secondary"]))
    sel = list(range(0, len(fs), 2)) + [len(fs) - 1]
    o.append(curve(s, ax, [fs[k] for k in sel], [st[k][0] for k in sel], SER[0]))
    for f, col, dx, dy, anc in ((10, SER[1], 10, 20, "start"), (25, SER[2], 10, 20, "start"), (60, SER[0], 8, 22, "start")):
        m = train_cycle(float(f))[0]
        o.append(dot(s, ax.X(f), ax.Y(m), col, r=5))
        o.append(H.label(s, ax.X(f) + dx, ax.Y(m) + dy, f"{f} Hz: ā = {m:.2f}", "label2", I["primary"], anc))
    o += legend(s, ax.x0 + 300, 26, [(SER[0], None, "mean ā"), (SER[0], None, "ripple, peak to trough", "band")])
    aria = ("Mean activation versus firing rate from 4 to 90 Hz, from the same integrator as the summation figure. The "
            f"mean rises steeply and saturates toward the ceiling {ceil:.2f}. A shaded band shows the peak-to-trough ripple, "
            f"which narrows as the rate climbs; a green dashed line at the fusion frequency {ff:.1f} Hz marks where the "
            "ripple falls under 5 percent. Dots mark the 10, 25 and 60 Hz traces: mean "
            + ", ".join(f"{train_cycle(float(f))[0]:.2f}" for f in (10, 25, 60)) + ".")
    hv = hover(ax, [ax.X(f) for f in fs], [ax.Y(x[0]) for x in st],
               [f"{f:.1f} Hz: mean ā = {x[0]:.3f}, ripple {x[1]:.2f}–{x[2]:.2f}" for f, x in zip(fs, st)])
    return svg(VB, aria, s, o, hv)


# ================================================================ activation ODE (Def. 5.1)
TAU_ACT, TAU_DEACT = 10.0, 40.0


def act_ode(u_fn, T_end, dt=0.01):
    t = np.arange(0.0, T_end + dt / 2, dt)
    u = np.array([u_fn(x) for x in t])
    a = np.zeros_like(t)
    for i in range(1, len(t)):
        tau = TAU_ACT if u[i - 1] > a[i - 1] else TAU_DEACT
        a[i] = a[i - 1] + dt * (u[i - 1] - a[i - 1]) / tau
    return t, u, a


def fig23():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    p = "m5f23_"
    ax = Ax((80, 50, 735, 300), (0, 320), (0, 1.1))
    u_fn = lambda x: 1.0 if 20 <= x < 140 else 0.0      # noqa: E731

    def a_fn(x):                                         # exact solution of the ODE for this step
        if x < 20:
            return 0.0
        if x < 140:
            return 1 - math.exp(-(x - 20) / TAU_ACT)
        return (1 - math.exp(-120 / TAU_ACT)) * math.exp(-(x - 140) / TAU_DEACT)
    o = [f"<defs>{H.markers(p, s)}</defs>"]
    o += axes(s, ax, [(v, f"{v}") for v in range(0, 301, 50)], [(v, f"{v:.1f}") for v in (0, 0.5, 1.0)],
              "time (ms)", "command u, activation a")
    ta = [20 + 60 * i / 60 for i in range(61)]
    o.append(f'<polygon points="{pts_str([(ax.X(x), ax.Y(1)) for x in ta] + [(ax.X(x), ax.Y(a_fn(x))) for x in reversed(ta)])}" '
             f'fill="{SER[0]}" opacity="0.10"/>')
    tb = [140 + 180 * i / 90 for i in range(91)]
    o.append(f'<polygon points="{pts_str([(ax.X(x), ax.Y(a_fn(x))) for x in tb] + [(ax.X(320), ax.Y(0)), (ax.X(140), ax.Y(0))])}" '
             f'fill="{SER[0]}" opacity="0.10"/>')
    ts = sorted(set([0, 20, 140, 320] + [20 + 2 * i for i in range(61)] + [140 + 3.6 * i for i in range(51)]))
    o.append(curve(s, ax, [0, 20, 20, 140, 140, 320], [0, 0, 1, 1, 0, 0], SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, ax, ts, [a_fn(x) for x in ts], SER[0], "curve_multi"))
    a30, a180 = a_fn(30), a_fn(180)
    o.append(H.arrow(s, p, ax.X(20), ax.Y(a30), ax.X(30) - 5, ax.Y(a30), "geometry", both=True))
    o.append(H.arrow(s, p, ax.X(140), ax.Y(a180), ax.X(180) - 5, ax.Y(a180), "geometry", both=True))
    o.append(dot(s, ax.X(30), ax.Y(a30), O["flag"]))
    o.append(dot(s, ax.X(180), ax.Y(a180), O["flag"]))
    o.append(H.label(s, ax.X(34), ax.Y(a30) + 5, f"{100*a30:.0f} % at 30 ms:", "label2", I["primary"]))
    o.append(H.label(s, ax.X(34), ax.Y(a30) + 21, f"one τ{sub('act', s)} = 10 ms after onset", "label2", I["primary"]))
    o.append(H.label(s, ax.X(186), ax.Y(a180) - 9, f"{100*a180:.0f} % at 180 ms: one τ{sub('deact', s)} = 40 ms after offset",
                     "label2", I["primary"]))
    o.append(H.label(s, ax.X(178), ax.Y(0.60), "activation outlasts the command (shaded)", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(80), ax.Y(1.0) - 9, "command u = 1 from 20 to 140 ms", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(222), ax.Y(0.21), "activation a", "label2", I["primary"]))
    o += legend(s, ax.x0, 26, [(SER[1], DASH_SER, "neural command u"), (SER[0], None, "activation a")])
    aria = ("Activation step response. A blue dashed rectangular command u is on from 20 to 140 ms; the red activation "
            "rises with time constant 10 ms, reaching 63 percent at 30 ms (dot), and after the command ends decays with "
            "time constant 40 ms, still at 37 percent at 180 ms (dot). Shading marks the lag on the way up and the "
            "activation that outlasts the command on the way down.")
    hts = [2 * i for i in range(161)]
    hv = hover(ax, [ax.X(x) for x in hts], [[ax.Y(u_fn(x)), ax.Y(a_fn(x))] for x in hts],
               [f"t = {x} ms: u = {u_fn(x):.0f}, a = {a_fn(x):.3f}" for x in hts])
    return svg(VB, aria, s, o, hv)


def u_trap(x):
    """Graded command of svg #26 (the old figure's schedule): ramp 20-70 ms to 0.8, hold, ramp 150-190 ms to 0."""
    if x < 20 or x >= 190:
        return 0.0
    if x < 70:
        return 0.8 * (x - 20) / 50
    if x < 150:
        return 0.8
    return 0.8 * (190 - x) / 40


def fig26():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 50, 735, 300), (0, 320), (0, 1.0))
    t, u, a = act_ode(u_trap, 320.0)
    k190 = int(round(190 / 0.01))
    o = axes(s, ax, [(v, f"{v}") for v in range(0, 301, 50)], [(v, f"{v:.1f}") for v in (0, 0.5, 1.0)],
             "time (ms)", "command u, activation a")
    sel = list(range(0, len(t), 300)) + [len(t) - 1]
    tb = [k for k in sel if t[k] >= 190]
    o.append(f'<polygon points="{pts_str([(ax.X(190), ax.Y(a[k190]))] + [(ax.X(t[k]), ax.Y(a[k])) for k in tb] + [(ax.X(320), ax.Y(0)), (ax.X(190), ax.Y(0))])}" '
             f'fill="{SER[0]}" opacity="0.10"/>')
    o.append(curve(s, ax, [0, 20, 70, 150, 190, 320], [0, 0, 0.8, 0.8, 0, 0], SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, ax, [t[k] for k in sel], [a[k] for k in sel], SER[0], "curve_multi"))
    o.append(dot(s, ax.X(190), ax.Y(a[k190]), O["flag"]))
    o.append(H.label(s, ax.X(197), ax.Y(a[k190]) + 2, f"a = {a[k190]:.2f} when u reaches 0 at 190 ms", "label2", I["primary"]))
    o.append(H.label(s, ax.x1 - 4, ax.Y(0.24), "activation outlasts", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.x1 - 4, ax.Y(0.24) + 16, "the command (shaded)", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(110), ax.Y(0.8) - 10, "command u: ramp up, hold 0.8, ramp down", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(62), ax.Y(0.30), "activation a lags a little on the rise", "label2", I["primary"]))
    k48 = int(round(48 / 0.01))
    o.append(lead(s, ax.X(62) - 3, ax.Y(0.30) - 4, ax.X(48) + 3, ax.Y(a[k48]) + 2, SER[0]))
    o += legend(s, ax.x0, 26, [(SER[1], DASH_SER, "graded command u"), (SER[0], None, "activation a")])
    aria = ("Activation response to a graded trapezoidal command: u (blue dashed) ramps from 0 at 20 ms to 0.8 at 70 ms, "
            "holds, and ramps back to 0 between 150 and 190 ms. The red activation follows with a small lag on the rise "
            f"(time constant 10 ms) and trails far past the fall (40 ms): when u reaches zero at 190 ms, a is still "
            f"{a[k190]:.2f} (shaded tail).")
    hk = list(range(0, len(t), 200))
    hv = hover(ax, [ax.X(t[k]) for k in hk], [[ax.Y(u[k]), ax.Y(a[k])] for k in hk],
               [f"t = {t[k]:.0f} ms: u = {u[k]:.2f}, a = {a[k]:.3f}" for k in hk])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #25: tau(Ca) (Prop. 5.1)
def tau_ca(c):
    return TAU_DEACT / (1 + c ** 3)


def fig25():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 40, 735, 300), (0.05, 10), (0, 45), xlog=True)
    lo, hi = math.log10(0.05), 1.0
    cs = [10 ** (lo + (hi - lo) * i / 110) for i in range(111)]
    o = axes(s, ax, [(v, f"{v:g}") for v in (0.1, 0.3, 1, 3, 10)], [(v, f"{v}") for v in (0, 10, 20, 30, 40)],
             "free Ca²⁺ concentration (µM, log scale)", "relaxation time constant τ (ms)")
    o.append(H.line(s, ax.x0, ax.Y(40), ax.x1, ax.Y(40), O["flag"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.x1 - 4, ax.Y(40) - 11, f"τ{sub('deact', s)} = 1/k{sub('off', s)} = 40 ms", "label2", I["secondary"], "end"))
    o.append(curve(s, ax, cs, [tau_ca(c) for c in cs], SER[0]))
    pts = ((0.1, f"rest 0.1 µM: τ = {tau_ca(0.1):.1f} ms", 0, 22, "middle", False),
           (1.0, f"Ca{sub('50', s)} = 1 µM: τ = {tau_ca(1):.0f} ms", -12, 4, "end", False),
           (1.4, f"twitch peak 1.4 µM: τ = {tau_ca(1.4):.1f} ms = τ{sub('act', s)}", 12, -10, "start", False),
           (2.0, f"a 2 µM peak would give {tau_ca(2):.1f} ms", 12, -9, "start", True))
    for c, txt, dx, dy, anc, hol in pts:
        o.append(dot(s, ax.X(c), ax.Y(tau_ca(c)), O["flag"], hollow=hol))
        o.append(H.label(s, ax.X(c) + dx, ax.Y(tau_ca(c)) + dy, txt, "label2", I["primary"], anc))
    o.append(H.label(s, ax.X(0.055), ax.Y(14), f"τ(Ca) = τ{sub('deact', s)} / (1 + (Ca/Ca₅₀)³)", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.055), ax.Y(14) + 18, f"k{sub('off', s)} = 25 s⁻¹, Ca{sub('50', s)} = 1 µM, n = 3", "label2", I["secondary"]))
    aria = ("Relaxation time constant of thin-filament activation against free calcium on a log axis, from Proposition "
            "5.1 with k_off 25 per second, Ca50 1 micromolar and n = 3. It equals the deactivation constant, 40 ms, at "
            f"resting calcium 0.1 micromolar, falls to 20 ms at Ca50 and to {tau_ca(1.4):.1f} ms at the twitch calcium peak "
            f"of 1.4 micromolar, the activation constant; a 2 micromolar peak would give {tau_ca(2):.1f} ms.").replace("_", " ")
    hc = [10 ** (lo + (hi - lo) * i / 200) for i in range(201)]
    hv = hover(ax, [ax.X(c) for c in hc], [ax.Y(tau_ca(c)) for c in hc], [f"Ca²⁺ = {c:.3g} µM: τ = {tau_ca(c):.1f} ms" for c in hc])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #27: force-velocity
def fig27():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 40, 735, 300), (-1, 1), (0, 1.6))
    vs = sorted(set([-1 + 2 * i / 90 for i in range(91)] + [x / 200 for x in range(-12, 13)]))
    o = axes(s, ax, [(v, mn(v, "{:.1f}")) for v in (-1, -0.5, 0, 0.5, 1)], [(v, f"{v:.1f}") for v in (0, 0.5, 1.0, 1.5)],
             f"shortening velocity v/v{H.sub('max', s)}   (← lengthening | shortening →)", f"force F/F{H.sub('0', s)} = f{H.sub('V', s)}")
    o.append(H.line(s, ax.X(-1), ax.Y(1.5), ax.X(0), ax.Y(1.5), I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(-0.98), ax.Y(1.5) - 8, f"eccentric plateau f{sub('ecc', s)} = 1.5", "label2", I["secondary"]))
    o.append(curve(s, ax, vs, [f_V(v) for v in vs], SER[0]))
    # slopes at the kink: concentric -(1 + 1/c) = -5, eccentric -(f_ecc - 1) k = -10 (twice as steep)
    o.append(H.line(s, ax.X(0), ax.Y(1), ax.X(0.09), ax.Y(1 - 5 * 0.09), I["secondary"], "leader", (4, 3)))
    o.append(H.line(s, ax.X(0), ax.Y(1), ax.X(-0.045), ax.Y(1 + 10 * 0.045), I["secondary"], "leader", (4, 3)))
    o.append(H.label(s, ax.X(0.075), ax.Y(0.40), "concentric slope −5", "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(0.015), ax.Y(1.33), "eccentric slope −10: twice as steep", "label2", I["secondary"]))
    o.append(dot(s, ax.X(0), ax.Y(1), O["flag"]))
    o.append(H.label(s, ax.X(0.03), ax.Y(1) - 6, f"isometric: F = F{sub('0', s)}", "label2", I["primary"]))
    o.append(dot(s, ax.X(1), ax.Y(0), O["flag"]))
    o.append(H.label(s, ax.X(0.97), ax.Y(0.12), f"v{sub('max', s)}: F = 0", "label2", I["primary"], "end"))
    o.append(H.label(s, ax.X(-0.62), ax.Y(1.18), "eccentric (v < 0):", "label2", I["primary"], extra='font-style="italic"'))
    o.append(H.label(s, ax.X(-0.62), ax.Y(1.18) + 16, f"lengthened, force rises above F{sub('0', s)}", "label2", I["secondary"]))
    o.append(H.label(s, ax.X(0.38), ax.Y(0.62), "concentric (v > 0):", "label2", I["primary"], extra='font-style="italic"'))
    o.append(H.label(s, ax.X(0.38), ax.Y(0.62) + 16, "Hill’s hyperbola, c = 0.25", "label2", I["secondary"]))
    aria = ("Force-velocity curve from the boxed f_V with c = 0.25, k = 20 and an eccentric plateau of 1.5. Force equals "
            "F0 at zero velocity, falls along Hill's hyperbola to zero at maximum shortening velocity on the right "
            "(concentric), and rises above F0 toward 1.5 F0 on the left (eccentric). Dashed tangents at the isometric "
            "kink have slopes -5 and -10: the eccentric branch climbs twice as steeply.").replace("_", " ")
    hv_ = [-1 + i / 100 for i in range(201)]
    hv = hover(ax, [ax.X(v) for v in hv_], [ax.Y(f_V(v)) for v in hv_], [f"v/vmax = {mn(v, '{:.2f}')}: F/F0 = {f_V(v):.3f}" for v in hv_])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #29: warm vs cold muscle (two panels)
def fig29():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    EA, RG = 70.0e3, 8.314
    fac = math.exp(-EA / RG * (1 / 298.15 - 1 / 310.15))
    vw, vc = 8.0, 8.0 * fac
    L = Ax((80, 50, 350, 300), (0, 8.5), (0, 1.05))
    R = Ax((460, 50, 735, 300), (0, 8.5), (0, 0.12))
    xt = [(v, f"{v}") for v in (0, 2, 4, 6, 8)]
    o = axes(s, L, xt, [(v, f"{v:.1f}") for v in (0, 0.5, 1.0)], "shortening velocity v (ℓ₀/s)", f"force F/F{H.sub('0', s)}")
    o += axes(s, R, xt, [(v, f"{v:.2f}") for v in (0, 0.05, 0.10)], "shortening velocity v (ℓ₀/s)",
              f"power P/(F{H.sub('0', s)}v{H.sub('max', s)} at 37 °C)", ylab_x=R.x0 - 58)
    fv = lambda v, vm: f_V(v / vm)                  # noqa: E731
    pw = lambda v, vm: v * fv(v, vm) / vw           # noqa: E731
    for vm, col in ((vw, SER[0]), (vc, SER[1])):
        xs = [vm * i / 100 for i in range(101)]
        o.append(curve(s, L, xs, [fv(x, vm) for x in xs], col, "curve_multi"))
        o.append(curve(s, R, xs, [pw(x, vm) for x in xs], col, "curve_multi"))
    o.append(H.line(s, L.X(0.8), L.y0, L.X(0.8), L.Y(0.70), I["rule"], "leader", H.DASH_REF))
    o.append(H.line(s, L.X(0.8), L.y0, L.X(0.8), L.y0 + 5, I["axis"], "leader"))
    o.append(H.label(s, L.X(0.8) + 2, L.y0 + 20, "0.8", "tick", I["secondary"], "start"))
    fwm, fcm = fv(0.8, vw), fv(0.8, vc)
    o.append(dot(s, L.X(0.8), L.Y(fwm), SER[0]))
    o.append(dot(s, L.X(0.8), L.Y(fcm), SER[1]))
    o.append(H.label(s, L.X(3.4), L.Y(0.96), "at v = 0.8 ℓ₀/s (dashed):", "label2", I["primary"]))
    o.append(H.label(s, L.X(3.4), L.Y(0.96) + 17, f"{fwm:.2f} F₀ at 37 °C", "label2", I["primary"]))
    o.append(H.label(s, L.X(3.4), L.Y(0.96) + 34, f"{fcm:.2f} F₀ at 25 °C", "label2", I["primary"]))
    o.append(H.label(s, L.X(3.4), L.Y(0.96) + 51, f"cold/warm = {fcm/fwm:.2f}", "label2", I["secondary"]))
    o.append(H.label(s, L.X(8.0), L.Y(0.13), f"v{sub('max', s)} = 8", "label2", I["primary"], "end"))
    o.append(H.label(s, L.X(vc) + 6, L.Y(0.04), f"{vc:.2f}", "label2", I["primary"]))
    for vm, col, txt in ((vw, SER[0], "peak {:.3f} at 37 °C"), (vc, SER[1], "peak {:.3f} at 25 °C")):
        xs = np.linspace(0, vm, 4001)
        k = int(np.argmax([pw(x, vm) for x in xs]))
        xp, yp = xs[k], pw(xs[k], vm)
        o.append(dot(s, R.X(xp), R.Y(yp), col))
        if vm == vw:
            o.append(H.label(s, R.X(xp), R.Y(yp) - 10, txt.format(yp), "label2", I["primary"], "middle"))
            pw_w = yp
        else:
            o.append(H.label(s, R.X(xp) + 10, R.Y(yp) - 7, txt.format(yp), "label2", I["primary"]))
            o.append(H.label(s, R.X(xp) + 10, R.Y(yp) - 24, f"{yp / pw_w:.3f} × the warm peak", "label2", I["secondary"]))
    o += legend(s, L.x0, 26, [(SER[0], None, f"37 °C: v{sub('max', s)} = 8 ℓ₀/s"),
                              (SER[1], None, f"25 °C: v{sub('max', s)} = {vc:.2f} ℓ₀/s (Arrhenius factor {fac:.3f})")])
    aria = ("Two panels. Left: Hill force-velocity curves for a muscle at 37 and at 25 degrees Celsius; the cold curve "
            f"reaches zero force at {vc:.2f} optimal lengths per second instead of 8, and at 0.8 lengths per second it gives "
            f"{fcm:.2f} F0 against {fwm:.2f} F0 warm. Right: the power curves, peaking at {pw_w:.3f} and {pw_w*fac:.3f} "
            f"F0 vmax, in the same ratio {fac:.3f}.")
    hl = [8.5 * i / 85 for i in range(86)]

    def pnl(ax, fn, txt):
        pts = []
        for x in hl:
            ys = [round(ax.Y(fn(x, vm)), 2) for vm in (vw, vc) if x <= vm] or [round(ax.Y(0), 2)]
            pts.append([round(ax.X(x), 2), ys, txt.format(x, max(fn(x, vw), 0), max(fn(x, vc), 0))])
        return ([round(v, 2) for v in ax.box], pts)
    hv = H.hover_attr([pnl(L, fv, "v = {:.1f} ℓ0/s: F = {:.2f} F0 at 37 °C, {:.2f} F0 at 25 °C"),
                       pnl(R, pw, "v = {:.1f} ℓ0/s: P = {:.3f} at 37 °C, {:.3f} at 25 °C")])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #30: power
def fig30():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 40, 735, 300), (0, 1), (0, 0.12))
    P = lambda v: v * f_V(v)                        # noqa: E731
    vs = [i / 110 for i in range(111)]
    xs = np.linspace(0, 1, 100001)
    k = int(np.argmax(xs * (1 - xs) / (1 + xs / C_HILL)))
    vp, pp = xs[k], P(xs[k])
    o = axes(s, ax, [(v, f"{v:.2f}") for v in (0, 0.25, 0.5, 0.75, 1)], [(v, f"{v:.2f}") for v in (0, 0.05, 0.10)],
             f"shortening velocity v/v{H.sub('max', s)}", f"power P/(F{H.sub('0', s)}v{H.sub('max', s)})")
    o.append(H.line(s, ax.X(vp), ax.Y(pp), ax.X(vp), ax.y0, I["rule"], "leader", H.DASH_REF))
    o.append(curve(s, ax, vs, [P(v) for v in vs], SER[0]))
    o.append(dot(s, ax.X(vp), ax.Y(pp), O["flag"]))
    o.append(H.label(s, ax.X(vp), ax.Y(pp) - 12, f"peak power {pp:.3f} F₀v{sub('max', s)}", "label2", I["primary"], "middle"))
    o.append(H.label(s, ax.X(vp) + 8, ax.Y(0.014), f"v = {vp:.2f} v{sub('max', s)}, where F = {f_V(vp):.2f} F₀ (about ⅓)",
                     "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.02), ax.Y(0.112), f"P = F v = F₀ v{sub('max', s)} · (v/v{sub('max', s)}) · f{sub('V', s)}, c = 0.25",
                     "label2", I["secondary"]))
    aria = ("Concentric power P = F v against shortening velocity, from Hill's curve with c = 0.25. Power is zero in an "
            f"isometric hold and at v_max, and peaks at {pp:.3f} F0 vmax at v = {vp:.2f} vmax, where force is "
            f"{f_V(vp):.2f} F0: about one third of each.").replace("_", " ")
    hv_ = [i / 200 for i in range(201)]
    hv = hover(ax, [ax.X(v) for v in hv_], [ax.Y(P(v)) for v in hv_],
               [f"v/vmax = {v:.3f}: P = {P(v):.4f} F0 vmax, F = {f_V(v):.3f} F0" for v in hv_])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #32: active + passive
K_PE, EPS0 = 3.0, 0.6


def f_pe(L):
    return 0.0 if L <= 1 else (math.exp(K_PE * (L - 1) / EPS0) - 1) / (math.exp(K_PE) - 1)


def fig32():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 50, 735, 300), (0.4, 1.6), (0, 1.25))
    Ls = sorted(set([0.4 + 1.2 * i / 110 for i in range(111)] + [0.47, 0.963, 1.0, 1.556]))
    Lt = [x for x in Ls if x >= 1.0]
    o = axes(s, ax, [(v, f"{v:.1f}") for v in (0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6)], [(v, f"{v:.1f}") for v in (0, 0.5, 1.0)],
             "normalised fibre length ℓ/ℓ₀", f"force / F{H.sub('max', s)}")
    o.append(curve(s, ax, Ls, [f_L_fib(x) for x in Ls], SER[0]))
    o.append(curve(s, ax, Ls, [f_pe(x) for x in Ls], SER[1]))
    tot = [f_L_fib(x) + f_pe(x) for x in Lt]
    o.append(curve(s, ax, Lt, tot, I["primary"], "curve_multi", DASH_SER))
    km = int(np.argmin(tot))
    for L_ in (1.2, 1.4, 1.6):
        o.append(dot(s, ax.X(L_), ax.Y(f_pe(L_)), SER[1]))
    for k, txt in enumerate((f"passive F{sub('PE', s)}:", f"{f_pe(1.2):.3f} at 1.2 ℓ₀", f"{f_pe(1.4):.3f} at 1.4 ℓ₀",
                             f"{f_pe(1.6):.1f} at 1.6 ℓ₀ (ε{sub('0', s)} = 0.6)")):
        o.append(H.label(s, ax.X(1.01), ax.Y(0.50) + 16 * k, txt, "label2", I["primary"]))
    o.append(lead(s, ax.X(1.08), ax.Y(0.50) + 54, ax.X(1.15), ax.Y(f_pe(1.15)) - 3, SER[1]))
    o.append(dot(s, ax.X(Lt[km]), ax.Y(tot[km]), I["primary"]))
    o.append(H.line(s, ax.X(Lt[km]) - 3, ax.Y(tot[km]) - 4, ax.X(1.2) + 30, ax.Y(1.12) + 5, I["rule"], "leader"))
    o.append(H.label(s, ax.X(1.2), ax.Y(1.12), f"total never below {tot[km]:.2f} (at {Lt[km]:.2f} ℓ₀)", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.56), ax.Y(0.72), f"active a·f{sub('L', s)}(ℓ), a = 1", "label2", I["primary"]))
    o += legend(s, ax.x0, 26, [(SER[0], None, "active"), (SER[1], None, f"passive F{sub('PE', s)} (k{sub('PE', s)} = 3)"),
                               (I["primary"], DASH_SER, "total = active + passive")])
    aria = ("Force versus normalised fibre length. The red active curve (Lab 1 length factor, full activation) peaks at "
            "1 on the plateau 0.963 to 1.0 optimal lengths and falls to zero at 1.556. The blue passive curve, from the "
            "exponential law with k_PE = 3 and reference strain 0.6, is zero up to optimal length and rises steeply: 0.090 "
            "at 1.2, 0.335 at 1.4 and 1.0 at 1.6. Their black dashed total stays at or above "
            f"{tot[km]:.2f} on the descending limb.").replace("_", " ")
    hl = [0.4 + 1.2 * i / 120 for i in range(121)]
    hv = hover(ax, [ax.X(x) for x in hl], [[ax.Y(f_L_fib(x)), ax.Y(f_pe(x)), ax.Y(f_L_fib(x) + f_pe(x))] for x in hl],
               [f"ℓ/ℓ0 = {x:.2f}: active {f_L_fib(x):.3f}, passive {f_pe(x):.3f}, total {f_L_fib(x) + f_pe(x):.3f}" for x in hl])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #33: f_L x f_V
def fig33():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 50, 735, 300), (-1, 1), (0, 1.6))
    vs = sorted(set([-1 + 2 * i / 90 for i in range(91)] + [x / 200 for x in range(-12, 13)]))
    sets = [(1.0, SER[0], "ℓ = ℓ₀"), (1.3, SER[1], "ℓ = 1.3 ℓ₀ (long)"), (0.8, SER[2], "ℓ = 0.8 ℓ₀ (short)")]
    o = axes(s, ax, [(v, mn(v, "{:.1f}")) for v in (-1, -0.5, 0, 0.5, 1)], [(v, f"{v:.1f}") for v in (0, 0.5, 1.0, 1.5)],
             f"shortening velocity v/v{H.sub('max', s)}", f"force / F{H.sub('max', s)} = f{H.sub('L', s)} f{H.sub('V', s)}")
    for L_, col, name in sets:
        fl = f_L_fib(L_)
        o.append(curve(s, ax, vs, [fl * f_V(v) for v in vs], col, "curve_multi"))
        o.append(H.label(s, ax.X(-0.97), ax.Y(fl * f_V(-0.97)) - 9, f"{name}: f{sub('L', s)} = {fl:.2f}", "label2", I["primary"]))
    o.append(H.label(s, ax.X(0.98), ax.Y(1.45), "each curve is the same f_V scaled by f_L;".replace("f_V", "f" + sub("V", s)).replace("f_L", "f" + sub("L", s)),
                     "label2", I["secondary"], "end"))
    o.append(H.label(s, ax.X(0.98), ax.Y(1.45) + 16, "activation a scales all three together", "label2", I["secondary"], "end"))
    o += legend(s, ax.x0, 26, [(c, None, n) for _, c, n in sets])
    fls = [f_L_fib(x) for x, _, _ in sets]
    aria = ("Three force-velocity curves at three fibre lengths, force equal to the length factor times the velocity "
            f"factor. At optimal length (red, f_L = 1) the curve reaches 1 at isometric and about 1.5 eccentric; at 1.3 "
            f"optimal lengths (blue, f_L = {fls[1]:.2f}) and 0.8 optimal lengths (orange, f_L = {fls[2]:.2f}) the whole "
            "curve is scaled down by the same factor, showing that length and velocity multiply.").replace("_", " ")
    hv_ = [-1 + i / 100 for i in range(201)]
    hv = hover(ax, [ax.X(v) for v in hv_], [[ax.Y(fl * f_V(v)) for fl in fls] for v in hv_],
               [f"v/vmax = {mn(v, '{:.2f}')}: " + ", ".join(f"{fl * f_V(v):.3f}" for fl in fls) + " (ℓ0, 1.3 ℓ0, 0.8 ℓ0)" for v in hv_])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #35: moment arm
def d_m(th):
    return 1.8 + 2.2 * math.sin(math.radians(th))


def fig35():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    ax = Ax((80, 40, 735, 300), (0, 150), (0, 4.5))
    th = [1.5 * i for i in range(101)]
    o = axes(s, ax, [(v, f"{v}") for v in range(0, 151, 30)], [(v, f"{v}") for v in range(0, 5)],
             "elbow flexion angle θ (degrees)", f"moment arm d{H.sub('m', s)}(θ) (cm)")
    o.append(H.line(s, ax.x0, ax.Y(3), ax.x1, ax.Y(3), I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(90), ax.Y(3) + 18, f"Module 1’s single value d{sub('m', s)} ≈ 3 cm", "label2", I["secondary"], "middle"))
    o.append(curve(s, ax, th, [d_m(x) for x in th], SER[0]))
    for x, txt, dx, dy, anc in ((0, f"{d_m(0):.1f} cm at full extension", 8, 22, "start"),
                                (90, f"peak {d_m(90):.1f} cm at 90°", 0, -12, "middle"),
                                (150, f"{d_m(150):.1f} cm at 150°", -6, 22, "end")):
        o.append(dot(s, ax.X(x), ax.Y(d_m(x)), O["flag"]))
        o.append(H.label(s, ax.X(x) + dx, ax.Y(d_m(x)) + dy, txt, "label2", I["primary"], anc))
    o.append(H.label(s, ax.X(75), ax.Y(1.05), f"same force, torque ratio: {d_m(90)/d_m(0):.1f}× at 90° vs full extension, "
                     f"{d_m(90)/d_m(150):.1f}× vs 150°", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.X(2), ax.Y(0.25), "extended", "label2", I["muted"]))
    o.append(H.label(s, ax.X(148), ax.Y(0.25), "flexed", "label2", I["muted"], "end"))
    aria = ("Moment arm of the elbow flexors versus flexion angle, d_m = 1.8 + 2.2 sin theta cm (Lab 1). It rises from "
            f"1.8 cm at full extension to a peak of 4.0 cm at 90 degrees and falls to {d_m(150):.1f} cm at 150 degrees. A "
            "dashed line marks the single 3 cm value of Module 1.").replace("_", " ")
    hv_ = list(range(151))
    hv = hover(ax, [ax.X(x) for x in hv_], [ax.Y(d_m(x)) for x in hv_], [f"θ = {x}°: dm = {d_m(x):.2f} cm" for x in hv_])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #36: redundancy optimum
def fig36():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    FB, FR, DB, DR, TAU = 135.0, 210.0, 0.040, 0.025, 5.89        # N, m, N m (sec. 1 and sec. 8)
    k = TAU / (DB * DB * FB ** 2 + DR * DR * FR ** 2)
    fb, fr = k * DB * FB ** 2, k * DR * FR ** 2
    copt = (fb / FB) ** 2 + (fr / FR) ** 2
    ax = Ax((80, 40, 735, 300), (0, 160), (0, 250))
    o = axes(s, ax, [(v, f"{v}") for v in range(0, 161, 20)], [(v, f"{v}") for v in range(0, 251, 50)],
             f"biceps force F{H.sub('bi', s)} (N)", f"brachialis force F{H.sub('br', s)} (N)")
    for c, dash, lab in ((0.15, DASH_SER, "0.15"), (copt, None, f"{copt:.2f}"), (1.0, DASH_SER, "1.00")):
        ph = [math.pi / 2 * i / 60 for i in range(61)]
        o.append(curve(s, ax, [FB * math.sqrt(c) * math.cos(p) for p in ph], [FR * math.sqrt(c) * math.sin(p) for p in ph],
                       O["flag"], "curve_multi", dash))
        yl = 4 if c < 0.9 else 24
        xl = FB * math.sqrt(c) * math.sqrt(max(0.0, 1 - (yl / (FR * math.sqrt(c))) ** 2))
        o.append(H.label(s, ax.X(xl) + 5, ax.Y(yl) - 4, lab, "label2", I["primary"]))
    o.append(H.label(s, ax.X(104), ax.Y(205), f"cost contours Σ(F/F{sub('max', s)})²", "label2", I["primary"]))
    o.append(H.label(s, ax.X(104), ax.Y(205) + 16, "smallest one touching the line wins", "label2", I["secondary"]))
    o.append(curve(s, ax, [0, TAU / DB], [TAU / DR, 0], O["geometry"]))
    o.append(H.label(s, ax.X(14), ax.Y(240), f"torque constraint 0.040 F{sub('bi', s)} + 0.025 F{sub('br', s)} = 5.89 N m",
                     "label2", I["primary"]))
    o.append(dot(s, ax.X(fb), ax.Y(fr), O["force"], r=5.5))
    o.append(H.line(s, ax.X(fb) + 5, ax.Y(fr) - 4, ax.X(102) - 3, ax.Y(158) + 4, I["rule"], "leader"))
    o.append(H.label(s, ax.X(102), ax.Y(158), f"optimum F{sub('bi', s)} = {fb:.0f} N, F{sub('br', s)} = {fr:.0f} N", "label2", I["primary"]))
    o.append(H.label(s, ax.X(102), ax.Y(158) + 16, f"relative stress {fb/FB:.2f} and {fr/FR:.2f}", "label2", I["secondary"]))
    aria = ("Optimization plot: biceps force against brachialis force. A blue torque-constraint line 0.040 F_bi + 0.025 "
            "F_br = 5.89 N m, orange contour ellipses of the cost sum of (F/F_max) squared at 0.15, "
            f"{copt:.2f} and 1.00, with F_max 135 and 210 N, and a red optimum where the {copt:.2f} ellipse touches the "
            f"line: biceps {fb:.0f} N, brachialis {fr:.0f} N, relative stresses {fb/FB:.2f} and {fr/FR:.2f}.").replace("_", " ")
    hb = [TAU / DB * i / 150 for i in range(151)]
    hr = [(TAU - DB * x) / DR for x in hb]
    hv = hover(ax, [ax.X(x) for x in hb], [ax.Y(y) for y in hr],
               [f"on the line: Fbi = {x:.1f} N, Fbr = {y:.1f} N, cost {(x/FB)**2 + (y/FR)**2:.3f}" for x, y in zip(hb, hr)])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #38: Lab 1 (its code, unchanged)
@lru_cache(maxsize=None)
def lab1():
    tau_act, tau_deact = 0.010, 0.040
    Fmax, theta_p, vmax = 500.0, np.radians(15), 8.0
    t = np.arange(0, 1.5, 0.001)
    u = np.clip((t - 0.1) / 0.2, 0, 0.85)
    u[t > 0.35] = 0.85
    a = np.zeros_like(t)
    for i in range(1, len(t)):
        dt = t[i] - t[i - 1]
        tau = tau_act if u[i - 1] > a[i - 1] else tau_deact
        a[i] = a[i - 1] + dt * (u[i - 1] - a[i - 1]) / tau
    theta = 30 + 80 * np.clip((t - 0.3) / 0.7, 0, 1)
    L = 1.0 - 0.003 * (theta - 70)
    vshort = -np.gradient(L, t) / vmax
    F = a * Fmax * np.array([f_L_fib(x) for x in L]) * np.array([f_V(x) for x in vshort]) * np.cos(theta_p)
    tq = F * np.array([1.8 + 2.2 * np.sin(np.radians(x)) for x in theta]) / 100.0
    return t, u, a, tq


def fig38():
    VB = (0, 0, 760, 420)
    s = H.Scale(VB[2], VB[3])
    t, u, a, tq = lab1()
    A = Ax((80, 50, 735, 170), (0, 1.5), (0, 1.0))
    B = Ax((80, 210, 735, 350), (0, 1.5), (0, 15))
    xt = [(v, f"{v:g}") for v in (0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5)]
    o = [f'<rect x="{A.X(0.3):.2f}" y="{A.top}" width="{A.X(1.0)-A.X(0.3):.2f}" height="{B.y0-A.top}" fill="{BOXFILL}"/>']
    o += axes(s, A, [(v, "") for v, _ in xt], [(v, f"{v:.1f}") for v in (0, 0.5, 1.0)], None, "u, a", ylab_x=30)
    o += axes(s, B, xt, [(v, f"{v}") for v in (0, 5, 10, 15)], "time (s)", "torque τ (N m)", ylab_x=30)
    o.append(H.label(s, A.X(0.65), A.Y(0.22), "curl 30° → 110°", "label2", I["secondary"], "middle"))
    sel = list(range(0, len(t), 20)) + [len(t) - 1]
    sel = sorted(set(sel + list(range(90, 300, 8)) + [299, 300, 301, 999, 1000, 1001, 1002]))
    o.append(curve(s, A, [t[k] for k in sel], [u[k] for k in sel], SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, A, [t[k] for k in sel], [a[k] for k in sel], SER[0], "curve_multi"))
    o.append(curve(s, B, [t[k] for k in sel], [tq[k] for k in sel], SER[2], "curve_multi"))
    kp = int(np.argmax(tq))
    o.append(dot(s, B.X(t[kp]), B.Y(tq[kp]), O["flag"]))
    o.append(H.label(s, B.X(t[kp]), B.Y(tq[kp]) - 10, f"τ peaks at {tq[kp]:.1f} N m, {t[kp]:.2f} s", "label2", I["primary"], "middle"))
    k3 = int(np.argmin(np.abs(t - 0.31)))
    o.append(H.line(s, B.X(0.31) + 3, B.Y(tq[k3]) + 4, B.X(0.42), B.Y(4.2) - 10, I["rule"], "leader"))
    o.append(H.label(s, B.X(0.42), B.Y(4.2), f"dip: f{sub('V', s)} bites as the fibres start shortening", "label2", I["secondary"]))
    o.append(H.label(s, B.X(1.03), B.Y(9.0), f"curl ends, v = 0: f{sub('V', s)} = 1", "label2", I["secondary"]))
    o.append(H.label(s, A.X(0.40), A.Y(0.55), "u ramps to 0.85; a follows about 10 ms behind", "label2", I["secondary"]))
    o += legend(s, A.x0, 26, [(SER[1], DASH_SER, "drive u"), (SER[0], None, "activation a"), (SER[2], None, "joint torque τ")])
    aria = ("Two stacked time series for the Lab 1 biceps curl, computed with the lab's code. Top: drive u (blue dashed) "
            "ramps from 0 at 0.1 s to 0.85 at 0.27 s and the activation a (red) follows it about 10 ms behind. Bottom: the "
            f"joint torque (orange) rises with a, dips as the curl from 30 to 110 degrees starts at 0.3 s, peaks at "
            f"{tq[kp]:.1f} N m at {t[kp]:.2f} s, and steps up when the curl ends at 1.0 s.")
    hk = list(range(0, len(t), 10))
    hv = H.hover_attr([
        ([round(v, 2) for v in A.box], [[round(A.X(t[k]), 2), [round(A.Y(u[k]), 2), round(A.Y(a[k]), 2)],
                                         f"t = {t[k]:.2f} s: u = {u[k]:.2f}, a = {a[k]:.3f}"] for k in hk]),
        ([round(v, 2) for v in B.box], [[round(B.X(t[k]), 2), round(B.Y(tq[k]), 2),
                                         f"t = {t[k]:.2f} s: τ = {tq[k]:.1f} N m"] for k in hk])])
    return svg(VB, aria, s, o, hv)


# ================================================================ svg #40: Lab 2 (its code, unchanged)
@lru_cache(maxsize=None)
def lab2():
    Ff, Fr = 0.018, 0.020
    t = np.arange(0, 120, 0.05)
    u = np.where(t < 60, 0.9, 0.0)
    a = u.copy()
    C = np.ones_like(t)
    for i in range(1, len(t)):
        dt = t[i] - t[i - 1]
        C[i] = C[i - 1] + dt * (-Ff * a[i - 1] * C[i - 1] + Fr * (1 - C[i - 1]))
    return t, a, C, a * C, Ff, Fr


def fig40():
    VB = (0, 0, 760, 380)
    s = H.Scale(VB[2], VB[3])
    t, a, C, F, Ff, Fr = lab2()
    ax = Ax((80, 50, 735, 300), (0, 120), (0, 1.05))
    k60 = int(np.where(t < 60)[0][-1])
    cinf = Fr / (Fr + Ff * 0.9)
    o = [f'<rect x="{ax.X(0):.2f}" y="{ax.top}" width="{ax.X(60)-ax.X(0):.2f}" height="{ax.y0-ax.top}" fill="{BOXFILL}"/>']
    o += axes(s, ax, [(v, f"{v}") for v in range(0, 121, 20)], [(v, f"{v:.1f}") for v in (0, 0.5, 1.0)],
              "time (s)", "a, C, force a·C")
    o.append(H.label(s, ax.X(30), ax.Y(0.08), "sustained effort, u = 0.9 (shaded)", "label2", I["secondary"], "middle"))
    o.append(H.label(s, ax.X(90), ax.Y(0.08), "release, u = 0: a and force drop to 0", "label2", I["secondary"], "middle"))
    o.append(H.line(s, ax.X(0), ax.Y(0.9 * cinf), ax.X(60), ax.Y(0.9 * cinf), I["secondary"], "ref", H.DASH_REF))
    o.append(H.label(s, ax.X(2), ax.Y(0.9 * cinf) + 18, f"steady a·C∞ = {0.9*cinf:.2f}, not reached in 60 s", "label2", I["secondary"]))
    sel = list(range(0, len(t), 24)) + [k60, k60 + 1, len(t) - 1]
    sel = sorted(set(sel))
    o.append(curve(s, ax, [t[k] for k in sel], [a[k] for k in sel], SER[1], "curve_multi", DASH_SER))
    o.append(curve(s, ax, [t[k] for k in sel], [C[k] for k in sel], SER[2], "curve_multi"))
    o.append(curve(s, ax, [t[k] for k in sel], [F[k] for k in sel], SER[0], "curve_multi"))
    o.append(dot(s, ax.X(t[k60]), ax.Y(F[k60]), SER[0]))
    o.append(dot(s, ax.X(t[k60]), ax.Y(C[k60]), SER[2]))
    o.append(H.label(s, ax.X(62), ax.Y(0.47), f"force a·C: {F[0]:.2f} → {F[k60]:.2f} at 60 s (−{100*(1-F[k60]/F[0]):.0f} %)",
                     "label2", I["primary"]))
    o.append(H.label(s, ax.X(62), ax.Y(0.47) + 18, f"capacity C: minimum {C.min():.2f} at 60 s", "label2", I["primary"]))
    o.append(H.label(s, ax.X(62), ax.Y(0.47) + 36, "then C recovers toward 1", "label2", I["primary"]))
    o.append(H.label(s, ax.X(16), ax.Y(0.9) - 9, "activation a = 0.9, held", "label2", I["primary"]))
    o += legend(s, ax.x0, 26, [(SER[0], None, "force a·C"), (SER[1], DASH_SER, "activation a"), (SER[2], None, "capacity C")])
    aria = ("Fatigue time series over 120 seconds from the Lab 2 code. During a 60-second effort at u = 0.9 (shaded) the "
            f"activation stays at 0.9 while the capacity C falls to {C.min():.2f}, so force a times C droops from 0.90 to "
            f"{F[k60]:.2f}, a {100*(1-F[k60]/F[0]):.0f} percent loss, still above the steady value {0.9*cinf:.2f}. After "
            "release the force and activation are zero and C recovers toward 1 over tens of seconds.")
    hk = list(range(0, len(t), 10))
    hv = hover(ax, [ax.X(t[k]) for k in hk], [[ax.Y(a[k]), ax.Y(C[k]), ax.Y(F[k])] for k in hk],
               [f"t = {t[k]:.1f} s: a = {a[k]:.2f}, C = {C[k]:.3f}, force = {F[k]:.3f}" for k in hk])
    return svg(VB, aria, s, o, hv)


FIGS = {
    8: ("Horizontal bar chart in units of thermal energy: one ATP is ", fig8),
    10: ("The active length-tension curve: normalized sarcomere force ", fig10),
    13: ("Goldman-Hodgkin-Katz membrane potential against the sodium-t", fig13),
    15: ("Steady-state activation a-infinity versus free calcium on a ", fig15),
    16: ("Single-twitch time course after one action potential. The fr", fig16),
    18: ("Recruitment staircase: cumulative force versus neural drive ", fig18),
    19: ("Activation versus time for one fibre at four firing rates. A", fig19),
    20: ("Animated build-up of a 60 Hz fused tetanus. A green impulse ", fig20),
    21: ("Mean activation versus stimulation rate. A steeply rising cu", fig21),
    23: ("Activation step response. A blue rectangular command on from", fig23),
    25: ("Relaxation time constant of thin-filament activation against", fig25),
    26: ("Activation response to a graded trapezoidal command. The red", fig26),
    27: ("Force-velocity curve. Force equals F0 at zero velocity, fall", fig27),
    29: ("Two panels. Left: Hill force-velocity curves for a muscle at", fig29),
    30: ("Power versus shortening velocity. Power is zero at v=0 and a", fig30),
    32: ("Force versus normalised fibre length. A red active hump peak", fig32),
    33: ("Three force-velocity curves at three fibre lengths. The opti", fig33),
    35: ("Moment arm versus elbow flexion angle. The curve rises from ", fig35),
    36: ("Optimization plot: biceps force versus brachialis force. A b", fig36),
    38: ("Two stacked time series for a biceps curl. Top: drive u and ", fig38),
    40: ("Fatigue time series over 120 seconds. During a 60-second sus", fig40),
}
