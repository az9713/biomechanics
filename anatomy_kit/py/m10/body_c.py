"""Module 10, group `body_c`: conceptual problems C1-C10 (svg #18-#27), house style, 400 px.

Whole bodies and the head come from the posable Lynch skeleton (lynch_body.py); m10/body_main.py puts its defs on
the page, this group only <use>s them.  The page states no stature: 1.75 m (the m07/m08 problem groups' choice),
so a body is drawn at HF px for 1.75 m.  Where the text states a COM position it is used: 1.0 m above the ankle
(l, module10.html lines 106, 850) and 0.02 m ahead of the ankle in quiet standing (module07.html line 176, the
foot base of Module 7: usable base 0.05 m behind to 0.12 m ahead of the ankle, so b = 0.12 - 0.02 = 0.10 m, line 106).
Every plotted number is computed here from the formula, constant or lab code the text states (line numbers beside
each constant).  Positions, velocities and poses the text does not fix are design values and are marked so.
"""
import math

import numpy as np

import house as H
import lynch_body as LB
from m05.body import finish, it
from m05.plots_prob import Plot, label as plabel, legend

O, I, SER = H.OVERLAY, H.INK, H.SERIES
BOX = "#f7f4ef"
GRID = "#e6e6e6"

# ---------------------------------------------------------------- numbers module10.html states
M, ELL, W0 = 70.0, 1.0, 3.1             # kg, m, rad/s (lines 106, 850, 851)
KP, KD = 20.0, 3.0                      # design gains (lines 136, 852, 853)
D_TOE, D_HEEL, X_Q = 0.12, 0.05, 0.02   # m: usable base and quiet COM (module07.html line 176)
B_FOOT = D_TOE - X_Q                    # 0.10 m (module10.html lines 106, 860)
Q_NOISE = 2.2e-3                        # rad^2 s^-3 (lines 234, 864)
TAU_C, OM_C = 0.137, 3.6                # critical delay (line 208) and marginal frequency (line 210)
V_WALK = 1.4                            # m/s walking speed (line 106)


def close(v, ref, tol):
    assert abs(v - ref) <= tol * 1.0001, (v, ref)


def island(kd=KD, w0=W0):
    """Prop 4.2 (lines 198-200): first-crossing boundary (tau, kp) traced by Omega; arrays sorted by tau."""
    om = np.linspace(1e-3, 40.0, 400000)
    sn = kd * om / (om ** 2 + w0 ** 2)
    ok = sn <= 1.0
    u = np.arcsin(sn[ok])
    return u / om[ok], (om[ok] ** 2 + w0 ** 2) * np.cos(u), om[ok]


_TAU, _KPB, _OM = island()
_i = int(np.argmin(abs(_KPB - KP)))
close(_TAU[_i], TAU_C, 0.0005)          # line 208: tau_c = 137 ms
close(_OM[_i], OM_C, 0.05)              # line 210: Omega = 3.6 rad/s
close(float(_KPB[int(np.argmin(abs(_TAU - 0.10)))]), 27.8, 0.05)   # K6 solution, line 697: ceiling 27.8 at 100 ms
close(W0 ** 2, 9.6, 0.02)               # line 852


def ceiling(tau):
    """k_p ceiling of the stability island at delay tau (kd = 3)."""
    return float(np.interp(tau, _TAU[::-1] if _TAU[0] > _TAU[-1] else _TAU, _KPB[::-1] if _TAU[0] > _TAU[-1] else _KPB))


# ---------------------------------------------------------------- drawing helpers (idiom of m07/m08 body_c.py)
def lab(s, x, y, text, size="label", fill=I["primary"], anchor="start", extra=""):
    return H.label(s, x, y, text, size, fill, anchor, extra)


def lines(s, x, y, rows, size="label2", anchor="start", lead=1.35):
    return "".join(lab(s, x, y + i * s(H.PX[size]) * lead, t, size, anchor=anchor) for i, t in enumerate(rows))


def floor(s, x0, x1, y, hatch=True):
    o = [H.line(s, x0, y, x1, y, I["axis"], "axis")]
    if hatch:
        n = int((x1 - x0) / s(10))
        o += [H.line(s, x0 + s(10) * i + s(8), y + s(1), x0 + s(10) * i, y + s(7), I["rule"], "leader")
              for i in range(n)]
    return "".join(o)


def ext(s, x0, y0, x1, y1):
    """Dashed construction line (reference grey)."""
    return H.line(s, x0, y0, x1, y1, O["dim"], "ref", H.DASH_REF)


def dot(s, x, y, col, r=4.5):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{s(r):.2f}" fill="{col}" stroke="#fff" '
            f'stroke-width="{s(1.5):.2f}"/>')


def diamond(s, x, y, col, r=6.0):
    q = s(r)
    return (f'<path d="M{x:.2f},{y - q:.2f} L{x + q:.2f},{y:.2f} L{x:.2f},{y + q:.2f} L{x - q:.2f},{y:.2f} Z" '
            f'fill="{col}" stroke="#fff" stroke-width="{s(1.5):.2f}" stroke-linejoin="round"/>')


def rect(s, x, y, w, h, fill=BOX, stroke=I["secondary"], rx=0):
    r = f' rx="{rx:.2f}"' if rx else ""
    return (f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}"{r} fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{s(1.2):.2f}"/>')


def arc(s, p, cx, cy, r, a0, a1, meaning="force", head=True):
    """Arc about (cx, cy) from screen angle a0 to a1 (deg, + = clockwise), arrowhead at a1."""
    q = lambda a: (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))  # noqa: E731
    (x0, y0), (x1, y1) = q(a0), q(a1)
    sweep = 1 if a1 > a0 else 0
    big = 1 if abs(a1 - a0) > 180 else 0
    mk = f' marker-end="url(#{p}a_{meaning})"' if head else ""
    w = "geom" if meaning in ("geometry", "dim") else "force"
    return (f'<path d="M{x0:.2f},{y0:.2f} A{r:.2f},{r:.2f} 0 {big} {sweep} {x1:.2f},{y1:.2f}" fill="none" '
            f'stroke="{O[meaning]}" stroke-width="{s(H.PX[w]):.2f}"{mk}/>')


def credit(s, vb):
    """Lynch credit at the bottom of the viewBox, wrapped to its width."""
    w = vb[2] - s(12)
    t = H.ATTRIBUTION["by"].format(
        author="Patrick J. Lynch, medical illustrator",
        title="Skeleton lateral.svg” and “Skeleton whole body ant lat views.svg", licence="CC BY 2.5",
        changes="Recoloured, split into segments and reposed; arms from the anterior view.")
    n = max(20, int(w / (s(H.PX["credit"]) * 0.47)))
    nl, cur = 0, ""
    for wd in t.split():
        if cur and len(cur) + 1 + len(wd) > n:
            nl, cur = nl + 1, wd
        else:
            cur = (cur + " " + wd).strip()
    y = vb[1] + vb[3] - s(6) - nl * s(H.PX["credit"]) * 1.25
    return LB.credit(s, vb[0] + s(6), y, width=w)


def VBs(h):
    return (0, 0, 400, h), H.Scale(400, h, display_w=400, max_h=H.MAX_DISPLAY_H_BODY)


def bisect(f, lo, hi, n=50):
    flo = f(lo)
    for _ in range(n):
        mid = (lo + hi) / 2
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def xdot(t="x"):
    return f'{it(t)}̇'


def head_only(p, s, x, y, height):
    """Lateral skull + cervical spine only (the m08 fig20 idiom: filter the segments of a standing pose)."""
    Pf = LB.pose()
    Q = LB.Pose("lat")
    Q.__dict__.update(Pf.__dict__)
    Q.segs = [g for g in Pf.segs if g[0] == "lat_head"]
    return LB.draw(p, s, Q, x, y, height)


def lean_pose(a, arms=0.0):
    """Rigid body leaning a degrees forward about the ankles, feet flat (the kit's lean_forward)."""
    return LB.pose(pelvis=a, near=dict(hip=0, shoulder=arms), far=dict(hip=0, shoulder=arms))


# ================================================================ svg #18  C1 static versus dynamic margin
def fig18():
    p = "m10f18_"
    VB, s = VBs(440)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 200.0, 318.0
    pm = HF / 1.75                                            # px per metre
    # --- numbers (design values: x, xdot, beam width; omega0 and the usable base from the text)
    x_g, v_g, half = X_Q, 0.30, 0.05                          # gymnast: COM 0.02 m ahead of the ankle, beam top 0.10 m
    xi_g = x_g + v_g / W0
    x_d, v_d = D_TOE + 0.05, -0.40                            # dancer: COM 0.05 m past the usable toe edge, moving back
    xi_d = x_d + v_d / W0
    assert xi_g > x_g + half and -D_HEEL < xi_d < D_TOE       # gymnast's xi past the edge; dancer's xi inside the base
    close(v_g / W0, 0.0968, 0.00005)
    close(xi_d, 0.0410, 0.0005)
    bh = 0.12 * pm                                            # beam height (design)
    Pg = LB.pose(near=dict(shoulder=75, elbow=15), far=dict(shoulder=75, elbow=15))
    _, J0 = LB.draw(p, s, Pg, 0, 0, HF)
    xh = 100.0 - (J0["ankle"][0] - J0["heel"][0])
    a_d = math.degrees(math.asin(x_d / ELL))                  # lean so the COM line (l = 1.0 m) is x_d ahead of the ankle
    Pd = lean_pose(a_d, arms=10)
    _, K0 = LB.draw(p, s, Pd, 0, 0, HF)
    xh2 = 300.0 - (K0["ankle"][0] - K0["heel"][0])
    for k, (P, xheel, yfloor, xc, vv, xi_, lean) in enumerate((
            (Pg, xh, fy - bh, x_g, v_g, xi_g, 0.0), (Pd, xh2, fy, x_d, v_d, xi_d, a_d))):
        body, J = LB.draw(p, s, P, xheel, yfloor, HF)
        ax, ay = J["ankle"]
        X = lambda m, ax=ax: ax + m * pm  # noqa: E731
        if k == 0:
            o.append(rect(s, X(xc - half), yfloor, 2 * half * pm, bh))
            o.append(floor(s, 8, 196, fy))
            band = (xc - half, xc + half)
        else:
            o.append(floor(s, 204, 392, fy))
            band = (-D_HEEL, D_TOE)
        o.append(body)
        cx, cy = X(xc), ay - ELL * math.cos(math.radians(lean)) * pm
        o.append(ext(s, cx, cy + s(8), cx, yfloor))
        o.append(H.com_mark(s, cx, cy))
        x0a = cx + (s(10) if vv > 0 else -s(10))
        o.append(H.arrow(s, p, x0a, cy, x0a + vv * s(110), cy, "dim"))
        o.append(lab(s, cx + (s(14) if vv > 0 else -s(14)), cy - s(8),
                     f'{xdot()} = {vv:+.2f} m/s'.replace("-", "−"), "label2", anchor="start" if vv > 0 else "end"))
        o.append(H.line(s, X(band[0]), fy, X(band[1]), fy, O["geometry"], "force"))
        o.append(dot(s, cx, fy, I["primary"], 4))
        o.append(diamond(s, X(xi_), fy, O["flag"]))
        yd = fy + s(17)
        o.append(H.arrow(s, p, cx, yd, X(xi_), yd, "geometry"))
        o.append(lab(s, cx - s(4), fy + s(33), it("x"), "label2", anchor="end"))
        o.append(lab(s, X(xi_) + s(4), fy + s(33), "ξ", "label2"))
        o.append(lab(s, (X(band[0]) + X(band[1])) / 2, fy + s(50), "beam top" if k == 0 else "usable base", "label2",
                     anchor="middle"))
    o.append(lab(s, 10, 22, "gymnast, COM over the beam"))
    o.append(lines(s, 10, 22 + s(18), [f"{it('x')} = {x_g:.2f} m,  {xdot()} = +{v_g:.2f} m/s",
                                       f"ξ = {it('x')} + {xdot()}/ω₀ = {xi_g:.3f} m", f"beam edge at +{x_g + half:.2f} m:",
                                       "ξ is past it, so she topples"]))
    o.append(lab(s, 392, 22, "dancer, COM past the toes", anchor="end"))
    o.append(lines(s, 392, 22 + s(18), [f"{it('x')} = {x_d:.2f} m,  {xdot()} = {v_d:+.2f} m/s".replace("-", "−"),
                                        f"ξ = {it('x')} + {xdot()}/ω₀ = {xi_d:.3f} m", f"toe edge at +{D_TOE:.2f} m:",
                                        "ξ is inside it, so he recovers"], anchor="end"))
    o.append(lab(s, 200, fy + s(68), f"x from the ankle; ω₀ = {W0} rad/s; blue arrow = {xdot()}/ω₀", "tick",
                 I["secondary"], anchor="middle"))
    o.append(credit(s, VB))
    aria = ("Two side views (Lynch skeleton art) on the dynamic stability condition. Left, a gymnast stands on a "
            "beam with her centre of mass over the beam: it is 0.02 m from the ankle on a beam top 0.10 m wide, "
            "but it moves forward at 0.30 m/s, so the extrapolated centre of mass xi = x + x-dot/omega0, with "
            "omega0 = 3.1 rad/s, is 0.117 m, past the beam edge at 0.07 m, and she topples although the static "
            "margin is positive. Right, a dancer leans with his centre of mass 0.17 m from the ankle, 0.05 m "
            "past the usable toe edge at 0.12 m, but moves backward at 0.40 m/s, so xi = 0.041 m is inside the "
            "base and he recovers. The base of support is the blue bar on the floor, the centre of mass x the "
            "black dot and xi the orange diamond; the blue arrow is the lead x-dot over omega0.")
    return finish(VB, aria, s, o)


# ================================================================ svg #19  C2 delay + noise: the body never settles
def noisy_sway(tau, seed=3, T=12.0, warm=20.0, dt=0.002, q=Q_NOISE):
    """Delayed closed loop of Section 4 (line 185) driven by white noise of intensity q (Definition 5, line 219),
    Euler-Maruyama as in Fig. 7's simulation.  tau = 0 is the delay-free loop; the same kicks drive both."""
    rng = np.random.default_rng(seed)
    n, d = int((warm + T) / dt), int(round(tau / dt))
    kick = math.sqrt(q * dt) * rng.standard_normal(n)
    th, om = np.zeros(n + 1), np.zeros(n + 1)
    for i in range(n):
        if d == 0:
            thd, omd = th[i], om[i]
        else:
            thd, omd = (th[i - d], om[i - d]) if i >= d else (0.0, 0.0)
        om[i + 1] = om[i] + dt * (W0 ** 2 * th[i] - KP * thd - KD * omd) + kick[i]
        th[i + 1] = th[i] + dt * om[i + 1]
    k0 = int(warm / dt)
    return np.degrees(th[k0:]), dt


def dde_root(tau, kp=KP, kd=KD):
    """Dominant root of s^2 - w0^2 + (kp + kd s) exp(-s tau) = 0 (Prop 4.1, line 191), Newton from the ringing pair."""
    s_ = complex(-0.4, 3.4)
    for _ in range(60):
        e = np.exp(-s_ * tau)
        f = s_ ** 2 - W0 ** 2 + (kp + kd * s_) * e
        df = 2 * s_ + kd * e - tau * (kp + kd * s_) * e
        s_ -= f / df
    return s_


def fig19():
    p = "m10f19_"
    VB, s = VBs(388)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    TAU, SEED = 0.10, 6      # tau: design value inside the 100-200 ms range (line 176); seed: the 12 s window whose RMS
    th0, dt = noisy_sway(0.0, SEED)                           # matches the 300 s runs (0.35 and 0.63 degrees)
    th1, _ = noisy_sway(TAU, SEED)
    sig = math.degrees(math.sqrt(Q_NOISE / (2 * (KP - W0 ** 2) * KD)))        # Prop 5.1 (line 225), delay-free
    close(sig, 0.34, 0.005)                                   # line 232
    r, rc = dde_root(TAU), dde_root(TAU_C)
    close(rc.real, 0.0, 0.01)                                 # the pair is on the imaginary axis at tau_c
    close(rc.imag, OM_C, 0.05)                                # line 210: 3.6 rad/s
    close(2 * math.pi / rc.imag, 1.7, 0.05)                   # line 210: period near 1.7 s
    per = 2 * math.pi / r.imag
    assert r.real < 0 and 1.5 < per < 2.2, r
    rms0, rms1 = float(th0.std()), float(th1.std())
    close(rms0, 0.35, 0.02)
    close(rms1, 0.63, 0.03)
    pl = Plot(s, (132, 58, 294, 212), (0, 12), (-2.0, 2.0))
    o.append(pl.axes([(v, f"{v}") for v in (0, 4, 8, 12)], [(v, f"{v:g}".replace("-", "−")) for v in (-2, 0, 2)],
                     "time (s)", "sway angle θ (degrees)", grid=(-1, 1), ytx=88))
    ts = np.arange(len(th0)) * dt
    sel = slice(0, None, 25)
    for v in (sig, -sig):
        o.append(H.line(s, pl.X(0), pl.Y(v), pl.X(12), pl.Y(v), I["rule"], "ref", H.DASH_REF))
    o.append(pl.curve(ts[sel], th1[sel], SER[0], multi=True))
    o.append(pl.curve(ts[sel], th0[sel], SER[1], multi=True))
    o.append(legend(s, 112, 40, [(SER[0], f"delay {TAU * 1000:.0f} ms", None), (SER[1], "no delay", None),
                                 (I["rule"], f"±{sig:.2f}°", (6, 4))], gap=8))
    y1, y0_ = pl.Y(th1[sel][-1]), pl.Y(th0[sel][-1])
    if abs(y1 - y0_) < s(17):
        y1, y0_ = ((y1 + y0_) / 2 - s(9), (y1 + y0_) / 2 + s(9)) if y1 < y0_ else ((y1 + y0_) / 2 + s(9), (y1 + y0_) / 2 - s(9))
    o.append(plabel(s, 300, y1 + s(4), "delayed", "label2"))
    o.append(plabel(s, 300, y0_ + s(4), "no delay", "label2"))
    o.append(lines(s, 132, 270, [f"{TAU * 1000:.0f} ms delay against τ{H.sub('c', s, 'label2')} = {TAU_C * 1000:.0f} ms",
                                 f"dominant root {r.real:.2f} ± {r.imag:.2f}i, period {per:.1f} s".replace("-", "−"),
                                 f"RMS sway {rms1:.2f}° delayed, {rms0:.2f}° with no delay"], "tick", lead=1.25))
    o.append(lines(s, 10, 22, ["same noise,", "two loops"], "label"))
    # the body: quiet standing, with the ankle torque that acts on a delayed signal
    fy = 284.0
    body, J = LB.standing_full(p, s, 40.0, fy, 205.0)
    o.append(body)
    ax, ay = J["ankle"]
    o.append(floor(s, 8, 96, fy))
    o.append(arc(s, p, ax, ay, s(14), -50, 50, "force"))
    o.append(lines(s, 10, fy + s(20), ["ankle torque", "acts on a signal", f"{TAU * 1000:.0f} ms old"], "tick", lead=1.25))
    o.append(credit(s, VB))
    aria = ("Left, a standing skeleton (Lynch art) with the ankle torque that corrects its sway (red arc). Right, a "
            "simulated sway angle against time for the same random kicks (intensity 2.2e-3 rad squared per second "
            "cubed) acting on two loops with position gain 20 and rate gain 3. The loop with a 100 ms feedback delay "
            f"(red) rings with a period near {per:.1f} s and wanders about {rms1 / rms0:.1f} times as far as the loop with no "
            "delay (blue, RMS 0.35 degrees), which stays near the dashed plus and minus 0.34 degree band of the "
            "delay-free theory. The delay of 100 ms is close to the critical delay of 137 ms, so the loop is only "
            "lightly damped and the noise keeps it ringing: the body cannot be still.")
    pts = [[pl.X(ts[i]), [pl.Y(th1[i]), pl.Y(th0[i])],
            f"t = {ts[i]:.1f} s: delayed {th1[i]:+.2f}°, no delay {th0[i]:+.2f}°".replace("-", "−")]
           for i in range(0, len(ts), 25)]
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ svg #20  C3 eyes closed on foam
def fig20():
    p = "m10f20_"
    VB, s = VBs(430)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 262.0, 340.0
    pm = HF / 1.75
    foam_h = 0.07 * pm                                       # foam pad 7 cm thick (design)
    foam_w = 0.55 * pm
    body, J = LB.standing_full(p, s, 62.0, fy - foam_h, HF)
    hx, hy = J["heel"]
    o.append(floor(s, 8, 176, fy, hatch=True))
    o.append(rect(s, hx - 0.18 * pm, fy - foam_h, foam_w, foam_h, rx=s(4)))
    o.append(body)
    vx, vy = J["vertex"]
    eye = (vx + 0.034 * HF, vy + 0.074 * HF)                 # orbit position read on the standing_full art
    ear = (vx - 0.012 * HF, vy + 0.095 * HF)                 # inner-ear region (temporal bone)
    ank = J["ankle"]
    rr = s(6)
    o.append(f'<circle cx="{eye[0]:.2f}" cy="{eye[1]:.2f}" r="{rr:.2f}" fill="#fff" fill-opacity="0.85" stroke="{I["primary"]}" '
             f'stroke-width="{s(1.2):.2f}"/>')
    o.append(H.line(s, eye[0] - rr * 0.7, eye[1] + rr * 0.7, eye[0] + rr * 0.7, eye[1] - rr * 0.7, I["primary"], "leader"))
    o.append(dot(s, ear[0], ear[1], I["primary"], 3.5))
    o.append(dot(s, ank[0], ank[1], I["primary"], 3.5))
    o.append(lab(s, hx - 0.18 * pm + foam_w / 2, fy + s(17), "foam", "label2", anchor="middle"))
    rows = [("Vision", "optic flow, ≈150 ms", "eyes closed: removed", eye, "removed"),
            ("Vestibular", "canals + otoliths, ≈15 ms", "the only channel left", ear, "ok"),
            ("Ankle proprioception", "muscle spindles, ≈35 ms", "foam: corrupted", ank, "corrupt")]
    bx, bw, bh = 196.0, 196.0, s(66)
    y0 = 56.0
    ys = [y0, y0 + bh + s(14), y0 + 2 * (bh + s(14))]
    for (name, sub_, status, pt, kind), y in zip(rows, ys):
        o.append(rect(s, bx, y, bw, bh))
        cx, cy = bx + s(16), y + bh / 2
        o.append(H.line(s, pt[0] + s(5), pt[1], bx, cy, I["rule"], "leader"))
        if kind == "ok":
            o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{s(7):.2f}" fill="{I["primary"]}"/>')
        elif kind == "removed":
            o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{s(7):.2f}" fill="#fff" stroke="{I["primary"]}" stroke-width="{s(1.5):.2f}"/>')
            o.append(H.line(s, cx - s(5), cy + s(5), cx + s(5), cy - s(5), I["primary"], "axis"))
        else:
            o.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{s(7):.2f}" fill="#fff" stroke="{I["primary"]}" '
                     f'stroke-width="{s(1.5):.2f}" stroke-dasharray="{s(3):.2f} {s(2.5):.2f}"/>')
        o.append(lab(s, bx + s(32), y + s(19), name, "label"))
        o.append(lab(s, bx + s(32), y + s(36), sub_, "label2", I["secondary"]))
        o.append(lab(s, bx + s(32), y + s(53), status, "label2"))
    o.append(lab(s, 10, 22, "eyes closed on foam"))
    o.append(lab(s, 10, 22 + s(18), "two of three channels gone", "label2"))
    ylast = ys[-1] + bh + s(22)
    o.append(lines(s, bx, ylast, ["one channel carries the whole", "estimate, so its noise passes", "straight through; eyes open",
                                  "on firm ground leaves three"], "label2"))
    o.append(credit(s, VB))
    aria = ("A standing skeleton (Lynch art) on a foam pad, eyes closed, with the three sensory channels of Section 3 "
            "listed at the right. Vision (optic flow, latency about 150 ms) is removed by closing the eyes: "
            "crossed-out circle. Ankle proprioception (muscle spindles, about 35 ms) is corrupted by the foam, which "
            "deforms under the foot and no longer maps spindle length to sway: dashed circle. The vestibular channel "
            "(canals and otoliths, about 15 ms) is the only one left, filled circle, so two of three independent "
            "channels are gone and the state estimate inherits far more noise: the classic worst case for standing.")
    return finish(VB, aria, s, o)


# ================================================================ svg #21  C4 ankle versus step
def fig21():
    p = "m10f21_"
    VB, s = VBs(476)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 210.0, 338.0
    pm = HF / 1.75
    JJ = 40.0                                                 # push impulse, N s (design; J_max = 21.7 N s, lines 106, 861)
    v0 = JJ / M
    xi = X_Q + v0 / W0                                        # Prop 1.2: xi jumps by J/(m w0) (line 104)
    DELTA = 0.03                                              # chosen capture margin (design value; < d_heel = 0.05 m)
    x_foot = xi + DELTA                                       # Prop 7.2 (line 285)
    close(JJ / (M * W0), 0.1843, 0.0005)
    close(M * W0 * B_FOOT, 21.7, 0.05)                        # lines 106, 395
    assert xi > D_TOE > X_Q                                   # xi has left the usable base: a step is mandatory
    Pa = LB.pose(pelvis=3, near=dict(hip=0), far=dict(hip=0))
    _, J0 = LB.draw(p, s, Pa, 0, 0, HF)
    xh = 90.0 - (J0["ankle"][0] - J0["heel"][0])
    body, J = LB.draw(p, s, Pa, xh, fy, HF)
    ax, ay = J["ankle"]
    X = lambda m: ax + m * pm  # noqa: E731
    o.append(floor(s, 8, 196, fy))
    o.append(body)
    cx, cy = X(X_Q), ay - ELL * pm
    o.append(ext(s, cx, cy + s(8), cx, fy))
    o.append(H.com_mark(s, cx, cy))
    o.append(H.arrow(s, p, cx - s(52), cy, cx - s(12), cy, "force"))
    o.append(lab(s, cx - s(34), cy - s(8), f"J = {JJ:.0f} N s", "label2", anchor="middle"))
    o.append(H.arrow(s, p, cx + s(12), cy, cx + s(12) + v0 * s(60), cy, "dim"))
    o.append(lab(s, cx + s(14), cy - s(8), f"{xdot()} = {v0:.2f} m/s", "label2"))
    o.append(H.line(s, X(-D_HEEL), fy, X(D_TOE), fy, O["geometry"], "force"))
    o.append(H.arrow(s, p, X(D_TOE), fy - s(52), X(D_TOE), fy - s(2), "reaction"))
    o.append(dot(s, X(X_Q), fy, I["primary"], 4))
    o.append(diamond(s, X(xi), fy, O["flag"]))
    o.append(lab(s, X(D_TOE) + s(6), fy - s(34), "COP", "label2"))
    o.append(lab(s, X(xi) + s(5), fy + s(17), "ξ", "label2"))
    o.append(arc(s, p, ax, ay, s(15), -60, 30, "force"))

    def mk(a):
        return LB.pose(pelvis=3, near=dict(hip=0), far=dict(hip=a, knee=6, contact="heel", shoulder=0),
                       anchor=("heel", "near"))

    def err(a):
        _, K = LB.draw(p, s, mk(a), 0, 0, HF)
        return (K["ankle_far"][0] - K["ankle"][0]) / pm - x_foot
    a2 = bisect(err, 2.0, 40.0)
    close(err(a2), 0.0, 0.0005)
    _, K0 = LB.draw(p, s, mk(a2), 0, 0, HF)
    xh2 = 262.0 - (K0["ankle"][0] - K0["heel"][0])
    body2, K = LB.draw(p, s, mk(a2), xh2, fy, HF)
    bx, by = K["ankle"]
    X2 = lambda m: bx + m * pm  # noqa: E731
    o.append(floor(s, 204, 392, fy))
    o.append(body2)
    c2x, c2y = X2(X_Q), by - ELL * pm
    o.append(ext(s, c2x, c2y + s(8), c2x, fy))
    o.append(H.com_mark(s, c2x, c2y))
    o.append(H.arrow(s, p, c2x + s(12), c2y, c2x + s(12) + v0 * s(60), c2y, "dim"))
    o.append(H.line(s, X2(-D_HEEL), fy, X2(D_TOE), fy, O["geometry"], "force"))
    o.append(dot(s, X2(X_Q), fy, I["primary"], 4))
    o.append(H.line(s, X2(x_foot - D_HEEL), fy, X2(x_foot + D_TOE), fy, O["geometry"], "force"))
    o.append(diamond(s, X2(xi), fy + s(12), O["flag"]))
    o.append(lab(s, X2(xi) - s(5), fy + s(30), "ξ", "label2", anchor="end"))
    o.append(dot(s, X2(x_foot), fy, I["primary"], 4))
    o.append(lab(s, X2(x_foot) + s(5), fy + s(30), f"x{H.sub('foot', s, 'label2')}", "label2"))
    o.append(lab(s, X2(x_foot + 0.035), fy - s(10), "new base", "label2"))
    o.append(lab(s, 10, 22, "ankle: COP saturates"))
    o.append(lines(s, 10, 22 + s(18), [f"ξ = {X_Q:.2f} + {JJ:.0f}/({M:.0f}×{W0})", f"= {xi:.3f} m, past +{D_TOE:.2f} m",
                                       "COP already at the toe:", "more torque shifts nothing"]))
    o.append(lab(s, 392, 22, "step: a new base", anchor="end"))
    o.append(lines(s, 392, 22 + s(18), [f"{it('x')}{H.sub('foot', s, 'label2')} = ξ + Δ", f"= {xi:.3f} + {DELTA:.2f} = {x_foot:.3f} m",
                                        "the pivot moves; ξ lands", "Δ inside the new base"], anchor="end"))
    o.append(lines(s, 10, fy + s(58), [f"x from the stance ankle; the blue bar is the usable base ({D_TOE + D_HEEL:.2f} m);",
                                       "red arc: ankle torque; black arrow: ground reaction at the COP"], "tick", lead=1.25))
    o.append(credit(s, VB))
    aria = ("Two side views (Lynch skeleton art) of a forward push of 40 N s on a 70 kg standing adult with omega0 = "
            "3.1 rad/s. The push raises the extrapolated centre of mass to xi = 0.02 + 40/(70 x 3.1) = 0.204 m "
            "from the ankle, past the usable toe edge at 0.12 m. Left, the ankle response: the centre of pressure "
            "(black arrow, the ground reaction) is already at the toe, so the ankle torque (red arc) saturates and a "
            "stronger muscle shifts nothing. Right, the step: the swing foot lands at the capture point x-foot = xi + "
            "delta = 0.234 m with a chosen margin delta of 0.03 m, which moves the base of support itself so that xi "
            "lands inside the new base. The usable base is the blue bar, xi the orange diamond.")
    return finish(VB, aria, s, o)


def fig22():
    p = "m10f22_"
    VB, s = VBs(452)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 205.0, 318.0
    pm = HF / 1.75
    MU_REQ, MU_AV = 0.20, 0.05                                # mu_req in 0.17-0.22 (line 862); mu_avail on ice: design value
    assert 0.17 <= MU_REQ <= 0.22
    # ---- slip: heel strike, stance foot sliding forward, body falling backward
    Ps = LB.pose(pelvis=-4, trunk=-8, neck=4, near=dict(hip=25, knee=5, contact=None, ankle=0, shoulder=-20, elbow=10),
                 far=dict(hip=-10, knee=35, contact="toe", shoulder=25, elbow=25), anchor=("heel", "near"))
    _, J0 = LB.draw(p, s, Ps, 0, 0, HF)
    xs = 112.0 - J0["heel"][0]
    body, J = LB.draw(p, s, Ps, xs, fy, HF)
    o.append(floor(s, 8, 196, fy))
    o.append(body)
    hx = J["heel"][0]
    cx = J["hip"][0]
    cy = J["floor_y"] - 0.98 * pm                           # COM mark ~ l above the contact (design: l = 1.0 m, line 106)
    o.append(H.com_mark(s, cx, cy))
    # foot slides forward
    o.append(H.arrow(s, p, hx + s(14), fy - s(6), hx + s(42), fy - s(6), "dim"))
    o.append(lab(s, hx + s(16), fy - s(12), "slides", "label2"))
    # body falls back: arrow behind the centre of mass
    o.append(H.arrow(s, p, cx - s(12), cy, cx - s(46), cy, "dim"))
    o.append(lab(s, cx - s(30), cy - s(8), "falls back", "label2", anchor="middle"))
    # force triangle at the heel (to scale): R = (-Fh, -Fv) on the foot; friction cone of mu_avail
    ox, oy, L = 170.0, fy - s(2), s(86)
    o.append(H.arrow(s, p, ox, oy, ox, oy - L, "reaction"))
    o.append(H.arrow(s, p, ox, oy - L, ox - MU_REQ * L, oy - L, "force"))
    o.append(H.line(s, ox, oy, ox - MU_REQ * L, oy - L, I["primary"], "ref"))
    for sg in (-1, 1):
        o.append(H.line(s, ox, oy, ox + sg * MU_AV * L * 1.3, oy - L * 1.3, I["rule"], "ref", H.DASH_REF))
    o.append(lab(s, ox + s(6), oy - L * 0.5, f"F{H.sub('v', s, 'label2')}", "label2"))
    o.append(lab(s, ox - MU_REQ * L - s(5), oy - L + s(5), f"F{H.sub('h', s, 'label2')}", "label2", anchor="end"))
    o.append(lab(s, ox + s(8), oy - L * 1.3 - s(2), f"μ{H.sub('avail', s, 'label2')}", "label2"))
    # ---- trip: swing foot caught on a block, body pitching forward
    def mkt(h):
        return LB.pose(pelvis=8, trunk=14, neck=-6, near=dict(hip=h, knee=10, contact=None, ankle=-5, shoulder=40, elbow=20),
                       far=dict(hip=-6, knee=4, shoulder=-30, elbow=15), anchor=("heel", "far"))

    def terr(h):
        _, Q = LB.draw(p, s, mkt(h), 0, 0, HF)
        return (Q["floor_y"] - Q["toe"][1]) / pm - 0.06           # the caught toe is 6 cm above the floor (design)
    Pt = mkt(bisect(terr, 5.0, 60.0))
    _, K0 = LB.draw(p, s, Pt, 0, 0, HF)
    xt = 262.0 - K0["heel_far"][0]
    body2, K = LB.draw(p, s, Pt, xt, fy, HF)
    o.append(floor(s, 204, 392, fy))
    bx0 = K["toe"][0] + s(1)
    o.append(rect(s, bx0, fy - 0.10 * pm, s(18), 0.10 * pm))
    o.append(body2)
    ax2, ay2 = K["ankle_far"]
    c2x = ax2 + 0.10 * pm
    c2y = ay2 - ELL * pm
    o.append(H.com_mark(s, c2x, c2y))
    o.append(H.arrow(s, p, c2x + s(10), c2y, c2x + s(10) + V_WALK * s(30), c2y, "dim"))
    o.append(lab(s, c2x + s(12), c2y + s(17), f"v = {V_WALK} m/s", "label2"))
    # pitch about the block
    px_, py_ = bx0, fy - 0.10 * pm
    r2 = math.hypot(c2x - px_, c2y - py_)
    b0 = math.degrees(math.atan2(c2y - py_, c2x - px_))
    o.append(arc(s, p, px_, py_, r2 * 0.92, b0, b0 + 26, "force"))
    o.append(lab(s, c2x - s(8), c2y - s(30), f"H = m{it('v')}ℓ", "label2", anchor="end"))
    xi_t = c2x + V_WALK / W0 * pm
    close(V_WALK / W0, 0.4516, 0.0005)
    o.append(H.line(s, c2x, fy, xi_t, fy, O["geometry"], "force"))
    o.append(diamond(s, xi_t, fy, O["flag"]))
    o.append(dot(s, c2x, fy, I["primary"], 4))
    o.append(lab(s, xi_t, fy + s(18), "ξ", "label2", anchor="middle"))
    o.append(lab(s, bx0 + s(9), fy + s(18), "block", "label2", anchor="middle"))
    o.append(lab(s, 10, 22, "slip: friction fails"))
    o.append(lines(s, 10, 22 + s(18), [f"μ{H.sub('req', s, 'label2')} = F{H.sub('h', s, 'label2')}/F{H.sub('v', s, 'label2')} ≈ {MU_REQ:.2f}"
                                       f" > μ{H.sub('avail', s, 'label2')}", "foot shoots forward, base leaves,", "body falls backward"]))
    o.append(lab(s, 392, 22, "trip: clearance fails", anchor="end"))
    o.append(lines(s, 392, 22 + s(18), ["swing foot stopped at the block:", f"Δξ = v/ω₀ = {V_WALK}/{W0} = {V_WALK / W0:.2f} m,",
                                        "body pitches forward"], anchor="end"))
    o.append(lines(s, 10, fy + s(40), [f"design values: μ{H.sub('avail', s, 'tick')} = {MU_AV} (ice); μ{H.sub('req', s, 'tick')} = {MU_REQ:.2f},",
                                       "inside the 0.17–0.22 of normal gait (Module 8);",
                                       "red: friction demanded (slip), pitch about the block (trip)"], "tick", lead=1.25))
    o.append(credit(s, VB))
    aria = ("Two side views (Lynch skeleton art) of falls on ice. Left, a slip: at heel strike the floor must supply a "
            "horizontal force F-h against the vertical force F-v; the force triangle at the right shows the required "
            "coefficient mu-req = F-h/F-v = 0.20 (black line, typical of normal gait, 0.17 to 0.22) lying outside the "
            "friction cone of the available coefficient (dashed lines, 0.05 on ice), so the foot slides forward, the "
            "base leaves from under the centre of mass and the body falls backward. Right, a trip: the swing foot is "
            "stopped by a block while the body moves forward at 1.4 m/s; angular momentum H = m v l about the block "
            "is conserved, so the body pitches forward (red arc) and the extrapolated centre of mass is thrown "
            "forward by v/omega0 = 0.45 m (blue bar, orange diamond), far past the stopped foot, so a capture step "
            "is mandatory. A slip falls backward and a trip falls forward.")
    return finish(VB, aria, s, o)


# ================================================================ svg #23  C6 sensory reweighting
def fig23():
    p = "m10f23_"
    VB, s = VBs(392)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    HF, fy = 176.0, 268.0
    body, J = LB.standing_full(p, s, 54.0, fy, HF)
    o.append(floor(s, 8, 110, fy))
    o.append(body)
    vx, vy = J["vertex"]
    eye = (vx + 0.034 * HF, vy + 0.074 * HF)
    rr = s(6)
    o.append(f'<circle cx="{eye[0]:.2f}" cy="{eye[1]:.2f}" r="{rr:.2f}" fill="#fff" fill-opacity="0.85" stroke="{I["primary"]}" '
             f'stroke-width="{s(1.2):.2f}"/>')
    o.append(H.line(s, eye[0] - rr * 0.7, eye[1] + rr * 0.7, eye[0] + rr * 0.7, eye[1] - rr * 0.7, I["primary"], "leader"))
    o.append(lab(s, 10, fy + s(20), "eyes closed", "label2"))
    # K_f = sp2/(sp2 + sm2) against sm2/sp2 (Prop 6.1, line 247); the prediction keeps 1 - K_f
    pl = Plot(s, (186, 92, 384, 226), (-1, 2), (0, 1))
    xs = np.linspace(-1, 2, 301)
    r = 10 ** xs
    kf = 1 / (1 + r)
    close(float(1 / (1 + 1.0)), 0.5, 1e-12)
    close(float(1 - 1 / (1 + 100.0)), 0.9901, 0.0001)
    # the identity behind reweighting: K_f is the inverse-variance weight (Prop 6.1)
    sp2, sm2 = 2.0, 5.0
    close(sp2 / (sp2 + sm2), (1 / sm2) / (1 / sp2 + 1 / sm2), 1e-12)
    sub = lambda t: H.sub(t, s)  # noqa: E731
    o.append(pl.axes([(-1, "0.1"), (0, "1"), (1, "10"), (2, "100")], [(0, "0"), (0.5, "0.5"), (1, "1")],
                     f"noise ratio σ{sub('m')}²/σ{sub('p')}² (log)", "weight", grid=(0.5,), ytx=156))
    o.append(pl.curve(xs, kf, SER[0], multi=True))
    o.append(pl.curve(xs, 1 - kf, SER[1], multi=True))
    o.append(pl.dot(0, 0.5, I["primary"]))
    o.append(pl.dot(2, 1 / 101, SER[0]))
    o.append(legend(s, 186, 80, [(SER[0], f"channel K{sub('f')}", None), (SER[1], "prediction", None)], gap=10))
    o.append(H.line(s, pl.X(0) + s(4), pl.Y(0.5) + s(3), pl.X(0.5) - s(4), pl.Y(0.34), I["rule"], "leader"))
    o.append(plabel(s, pl.X(0.5), pl.Y(0.33), "equal trust: 0.50", "label2"))
    o.append(plabel(s, pl.X(2) - s(8), pl.Y(1 / 101) - s(22), "eyes closed:", "label2", anchor="end"))
    o.append(plabel(s, pl.X(2) - s(8), pl.Y(1 / 101) - s(8), "K → 0", "label2", anchor="end"))
    o.append(lab(s, 10, 22, "close your eyes and you do not fall:"))
    o.append(lines(s, 10, 22 + s(18), ["vision's weight drops toward zero,", "the other channels take over."]))
    o.append(lines(s, 186, 290, [f"K{H.sub('f', s, 'tick')} = σ{sub('p')}²/(σ{sub('p')}² + σ{sub('m')}²), Prop 6.1:",
                                 "a noisier channel gets a smaller", "weight. Optimal fusion is the",
                                 "reweighting, no separate rule"], "tick", lead=1.25))
    o.append(credit(s, VB))
    aria = ("Left, a standing skeleton (Lynch art) with the eyes closed. Right, the Kalman weight of Proposition 6.1 "
            "against the ratio of the channel's noise variance to the prediction's, on a log scale from 0.1 to 100. "
            "The weight on the channel, K-f = sigma-p squared over (sigma-p squared plus sigma-m squared) (red), falls "
            "from 0.91 at a ratio of 0.1 through 0.50 at equal trust to 0.01 at a ratio of 100, while the weight on the "
            "prediction (blue) rises: as a channel becomes unreliable, as vision does when the eyes close, its weight "
            "goes to zero and the estimate leans on the others. Fixed weights would leave a persistent error; "
            "reweighting is what optimal fusion does.")
    pts = [[pl.X(xs[i]), [pl.Y(kf[i]), pl.Y(1 - kf[i])],
            f"ratio {r[i]:.3g}: channel {kf[i]:.2f}, prediction {1 - kf[i]:.2f}"] for i in range(len(xs))]
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


# ================================================================ svg #24  C7 more gain is not better
def fig24():
    p = "m10f24_"
    VB, s = VBs(350)
    o = []
    sub = lambda t, z="label2": H.sub(t, s, z)  # noqa: E731
    # ---- left: the stability island at kd = 3 (Prop 4.2, lines 198-200)
    KMAX = 36.0
    L = Plot(s, (50, 74, 178, 210), (0, 0.30), (4, KMAX))
    tau_, kp_ = _TAU, _KPB
    order = np.argsort(tau_)
    t_s, k_s = tau_[order], kp_[order]
    assert np.all(np.diff(t_s) >= 0)
    keep = (t_s <= 0.30) & (k_s <= KMAX) & (k_s >= W0 ** 2)
    t_c, k_c = t_s[keep], k_s[keep]
    t_c = np.concatenate([[float(np.interp(KMAX, k_s[::-1], t_s[::-1]))], t_c])
    k_c = np.concatenate([[KMAX], k_c])
    t_c, k_c = t_c[::max(1, len(t_c) // 140)], k_c[::max(1, len(k_c) // 140)]
    o.append(L.axes([(0, "0"), (0.1, "0.1"), (0.2, "0.2"), (0.3, "0.3")], [(10, "10"), (20, "20"), (30, "30")],
                    "delay τ (s)", f"gain k{sub('p', 'label')} (s⁻²)", grid=(20, 30), ytx=15))
    fl = W0 ** 2
    poly_pts = [(L.X(0), L.Y(fl)), (L.X(0), L.Y(KMAX))] + [(L.X(a), L.Y(b)) for a, b in zip(t_c, k_c)] + \
               [(L.X(0.30), L.Y(fl))]
    o.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in poly_pts)}" fill="{GRID}" stroke="none"/>')
    o.append(H.line(s, L.X(0), L.Y(fl), L.X(0.30), L.Y(fl), I["rule"], "ref", H.DASH_REF))
    o.append(L.curve(t_c, k_c, I["primary"], multi=True))
    ceil01 = ceiling(0.10)
    close(ceil01, 27.8, 0.05)                                 # K6 solution, line 697
    o.append(H.line(s, L.X(0), L.Y(KP), L.X(TAU_C), L.Y(KP), I["rule"], "ref", H.DASH_REF))
    o.append(H.line(s, L.X(TAU_C), L.Y(KP), L.X(TAU_C), L.Y(4), I["rule"], "ref", H.DASH_REF))
    o.append(L.dot(0.10, KP, SER[1]))
    o.append(L.dot(0.10, 30.0, SER[0]))
    o.append(L.dot(0.10, ceil01, I["primary"]))
    o.append(plabel(s, L.X(0.015), L.Y(15.0), "stable", "label2"))
    o.append(plabel(s, L.X(TAU_C) + s(4), L.Y(fl) + s(15), f"τ{sub('c', 'tick')} = {TAU_C * 1000:.0f} ms", "tick", I["secondary"]))
    o.append(plabel(s, L.X(0.10) - s(7), L.Y(ceil01) + s(14), f"{ceil01:.1f}", "label2", anchor="end"))
    o.append(dot(s, 17, 55, SER[1], 4.5))
    o.append(plabel(s, 26, 59, "20 stable", "label2"))
    o.append(dot(s, 98, 55, SER[0], 4.5))
    o.append(plabel(s, 107, 59, "30 unstable", "label2"))
    # ---- right: RMS sway against k_p with signal-dependent motor noise (K6, lines 695-716)
    Q0, KREF = Q_NOISE, 8.0

    def rms_deg(kp):
        q = Q0 * (1.0 + (kp / KREF) ** 2)
        return np.degrees(np.sqrt(q / (2.0 * (kp - W0 ** 2) * KD)))
    kg = np.linspace(9.7, 45.0, 200000)
    k_opt_num = float(kg[np.argmin(rms_deg(kg))])
    k_opt = W0 ** 2 + math.sqrt(W0 ** 4 + KREF ** 2)
    close(k_opt, 22.11, 0.005)
    close(k_opt_num, k_opt, 0.01)
    close(float(rms_deg(k_opt)), 0.912, 0.0005)
    R = Plot(s, (248, 74, 388, 210), (10, 40), (0.5, 3.0))
    o.append(R.axes([(10, "10"), (20, "20"), (30, "30"), (40, "40")], [(1, "1"), (2, "2"), (3, "3")],
                    f"gain k{sub('p')} (s⁻²)", "RMS sway (degrees)", grid=(1, 2), ytx=222))
    k1 = np.linspace(10.0, ceil01, 120)
    k2 = np.linspace(ceil01, 40.0, 80)
    o.append(H.line(s, R.X(ceil01), R.Y(3.0), R.X(ceil01), R.Y(0.5), SER[0], "ref", H.DASH_REF))
    o.append(R.curve(k1, rms_deg(k1), I["primary"], multi=True))
    o.append(R.curve(k2, rms_deg(k2), I["rule"], multi=True, dash=(5, 3)))
    o.append(R.dot(k_opt, float(rms_deg(k_opt)), SER[1]))
    o.append(H.line(s, R.X(k_opt) + s(5), R.Y(float(rms_deg(k_opt))) - s(3), R.X(29.0) - s(3), R.Y(1.85) + s(3), I["rule"], "leader"))
    o.append(plabel(s, R.X(29.0), R.Y(1.85), f"best {k_opt:.1f}", "label2"))
    o.append(plabel(s, R.X(29.0), R.Y(1.85) + s(16), f"RMS {float(rms_deg(k_opt)):.2f}°", "label2"))
    o.append(plabel(s, R.X(ceil01) + s(5), R.Y(2.75), "island edge", "tick", I["secondary"]))
    o.append(plabel(s, R.X(ceil01) + s(5), R.Y(2.75) + s(14), "at 100 ms", "tick", I["secondary"]))
    o.append(lab(s, 10, 24, "1  delay caps the gain"))
    o.append(lab(s, 10, 24 + s(17), "the ceiling falls as τ grows", "label2", I["secondary"]))
    o.append(lab(s, 206, 24, "2  motor noise: a U-shape"))
    o.append(lab(s, 206, 24 + s(17), "sway rises again at high gain", "label2", I["secondary"]))
    o.append(lines(s, 10, 276, [f"island: k{sub('d', 'tick')} = {KD:g} s⁻¹, ω₀ = {W0} rad/s; at k{sub('p', 'tick')} = {KP:g}",
                                f"the critical delay is τ{sub('c', 'tick')} = {TAU_C * 1000:.0f} ms",
                                f"sway: q = q₀(1 + (k{sub('p', 'tick')}/{KREF:g})²), q₀ = 2.2×10⁻³ rad² s⁻³ (K6)",
                                f"best k{sub('p', 'tick')} = {k_opt:.1f} s⁻² (RMS {float(rms_deg(k_opt)):.2f}°); dashed: unstable"],
                   "tick", lead=1.25))
    aria = ("Two reasons that more proportional gain does not stabilise standing better. Left, the stability island in the "
            "delay and gain plane at damping gain 3 per second and omega0 = 3.1 rad/s (Proposition 4.2): the island "
            "(grey) lies between the floor k-p = omega0 squared = 9.61 and a ceiling that falls as the delay grows, 27.8 "
            "at 100 ms; at gain 20 the critical delay is 137 ms. The point at 100 ms and gain 20 (blue) is inside it, the point "
            "at gain 30 (red) is outside, where the delayed correction pumps the sway. Right, the RMS sway with "
            "signal-dependent motor noise q = q0 (1 + (k-p/8) squared): it falls, reaches a minimum of 0.91 degrees "
            "at gain 22.1, then rises again; the vertical red dashed line is the island edge at 100 ms and the grey "
            "dashed continuation is the same formula past it, where the loop is unstable. Both effects make sway a "
            "U-shaped function of gain.")
    pts_l = [[L.X(a), L.Y(b), f"τ = {a:.3f} s: ceiling k{chr(8346)} = {b:.1f}"] for a, b in zip(t_c, k_c)]
    kk = np.linspace(10.0, 40.0, 120)
    pts_r = [[R.X(a), R.Y(float(rms_deg(a))), f"k{chr(8346)} = {a:.1f}: RMS {float(rms_deg(a)):.2f}°"] for a in kk]
    return finish(VB, aria, s, o, extra=H.hover_attr([(L.box, pts_l), (R.box, pts_r)]))


# ================================================================ svg #25  C8 four drifts, not "age"
def fig25():
    p = "m10f25_"
    VB, s = VBs(448)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    sub = lambda t, z="label2": H.sub(t, s, z)  # noqa: E731

    def jc(tau, t_move, l_step, w0=3.1, m=70.0):             # Definition 6 / Lab D (lines 336-337, 492-494)
        return m * w0 * l_step * math.exp(-w0 * (tau + t_move))
    young = dict(tau=0.10, t_move=0.20, l_step=0.60)         # lines 497-498, 866-868
    aged = dict(tau=0.18, t_move=0.32, l_step=0.42)
    j_y, j_a = jc(**young), jc(**aged)
    close(j_y, 51.4, 0.05)                                    # lines 343, 869
    close(j_a, 19.3, 0.05)
    alone = {k: jc(**dict(young, **{k: aged[k]})) for k in aged}
    assert all(35.0 <= v <= 40.2 for v in alone.values())    # line 506: each drift alone cuts it to about 35-40 N s
    HF, fy = 248.0, 318.0
    body, J = LB.standing_full(p, s, 54.0, fy, HF)
    o.append(floor(s, 8, 112, fy))
    o.append(body)
    vx, vy = J["vertex"]
    eye = (vx + 0.034 * HF, vy + 0.074 * HF)
    calf = ((J["knee"][0] + J["ankle"][0]) / 2, J["knee"][1] + 0.55 * (J["ankle"][1] - J["knee"][1]))
    spine = ((J["l5s1"][0] + J["neck"][0]) / 2, (J["l5s1"][1] + J["neck"][1]) / 2)
    ank = J["ankle"]
    rows = [
        ("Sensor-noise variance σ²", "sway variance ∝ σ² (Prop 5.1)", "widens sway, blurs the estimate", eye, "up"),
        ("Reflex delay τ", "0.10 → 0.18 s (Lab D)", f"J{sub('crit', 'tick')} alone: {j_y:.1f} → {alone['tau']:.1f} N s", spine, "up"),
        ("Torque rate", f"foot-travel t{sub('move')} 0.20 → 0.32 s", f"J{sub('crit', 'tick')} alone: {j_y:.1f} → {alone['t_move']:.1f} N s", calf, "down"),
        ("Peak ankle torque", f"step reach L{sub('step')} 0.60 → 0.42 m", f"J{sub('crit', 'tick')} alone: {j_y:.1f} → {alone['l_step']:.1f} N s", ank, "down"),
    ]
    bx, bw, bh, gap = 150.0, 242.0, s(60), s(8)
    y0 = 44.0
    for i, (name, l2, l3, pt, d) in enumerate(rows):
        y = y0 + i * (bh + gap)
        o.append(rect(s, bx, y, bw, bh))
        cy = y + bh / 2
        o.append(H.line(s, pt[0] + s(4), pt[1], bx, cy, I["rule"], "leader"))
        o.append(dot(s, pt[0], pt[1], I["primary"], 3.2))
        a, b = (cy + s(11), cy - s(11)) if d == "up" else (cy - s(11), cy + s(11))
        o.append(H.arrow(s, p, bx + s(14), a, bx + s(14), b, "dim"))
        o.append(lab(s, bx + s(28), y + s(19), name, "label"))
        o.append(lab(s, bx + s(28), y + s(36), l2, "label2", I["secondary"]))
        o.append(lab(s, bx + s(28), y + s(52), l3, "tick"))
    yb = fy + s(34)
    o.append(lines(s, 10, yb, [f"J{sub('crit', 'tick')} = mω₀L{sub('step', 'tick')}·exp[−ω₀(τ + t{sub('move', 'tick')})]  (Definition 6)",
                               f"all three together: {j_y:.1f} → {j_a:.1f} N s;", "the drifts multiply rather than add"],
                   "tick", lead=1.25))
    o.append(lab(s, 10, 22, "not “age”: four drifts"))
    o.append(credit(s, VB))
    aria = ("A standing skeleton (Lynch art) with four control parameters of Section 9 that drift with age, each tied to "
            "where it acts. Sensor-noise variance up (at the eye): sway variance is proportional to it (Proposition "
            "5.1). Reflex delay up (spine), 0.10 to 0.18 s. Torque rate down (calf), which lengthens the foot-travel "
            "time from 0.20 to 0.32 s. Peak ankle torque down (ankle), which shortens the reachable step from 0.60 to "
            "0.42 m. By the capture-step model J-crit = m omega0 L-step exp(-omega0 (tau + t-move)), the largest "
            "recoverable impulse falls from 51.4 to 19.3 N s when the three change together; each alone cuts it only "
            "to 40.1, 35.4 and 36.0 N s, so the effects multiply rather than add.")
    return finish(VB, aria, s, o)


# ================================================================ svg #26  C9 observability: the angle from the rate alone
def observer_run(T=3.0, dt=0.001, seed=4, sd=0.05, th0=0.05):
    """Rate-only observer (Prop 3.1, line 170): the canals give y = theta-dot + noise.  Plant x' = A x + B u with
    A = [[0, 1], [w0^2, 0]], B = [0, 1] (line 115), control u = -K xhat with K = [kp, kd] (design gains), observer
    xhat' = A xhat + B u + L (y - C xhat), C = [0, 1], observer poles at -6, -6 (design value)."""
    rng = np.random.default_rng(seed)
    l2 = 12.0                                                 # s^2 + l2 s + (l1 - 1) w0^2 with both roots at -6
    l1 = 1.0 + 36.0 / W0 ** 2
    n = int(T / dt)
    x = np.array([th0, 0.0])
    xh = np.zeros(2)
    out = np.zeros((n, 5))
    for i in range(n):
        y = x[1] + sd * rng.standard_normal()
        u = -(KP * xh[0] + KD * xh[1])
        out[i] = (i * dt, x[0], xh[0], y, x[1])
        e = y - xh[1]
        x = x + dt * np.array([x[1], W0 ** 2 * x[0] + u])
        xh = xh + dt * np.array([xh[1] + l1 * e, W0 ** 2 * xh[0] + u + l2 * e])
    return out


def fig26():
    p = "m10f26_"
    VB, s = VBs(414)
    o = [f'<defs>{H.markers(p, s)}</defs>']
    sub = lambda t, z="label2": H.sub(t, s, z)  # noqa: E731
    # observability of the canal channel: O = [C; CA] = [[0, 1], [w0^2, 0]], det = -w0^2 (lines 170-172)
    A = np.array([[0.0, 1.0], [W0 ** 2, 0.0]])
    Cm = np.array([[0.0, 1.0]])
    Ob = np.vstack([Cm, Cm @ A])
    assert np.linalg.matrix_rank(Ob) == 2
    close(float(np.linalg.det(Ob)), -W0 ** 2, 1e-9)
    close(W0 ** 2, 9.61, 0.0001)
    R = observer_run()
    t, th, thh, yy, om = R[:, 0], np.degrees(R[:, 1]), np.degrees(R[:, 2]), np.degrees(R[:, 3]), np.degrees(R[:, 4])
    err0 = abs(th[0] - thh[0])
    t1 = float(t[np.argmax(np.abs(th - thh) < 0.1 * err0)])   # first time the angle error is under 10 %
    assert t1 < 1.0 and abs(th[-1] - thh[-1]) < 0.15
    # head art (Lynch skull), canals report theta-dot only
    _, J0 = head_only(p, s, 0, 0, 470.0)
    x0b, y0b, x1b, y1b = J0["bbox"]
    hd, JH = head_only(p, s, 62 - (x0b + x1b) / 2, 96 - (y0b + y1b) / 2, 470.0)
    o.append(hd)
    o.append(lab(s, 62, 150, f"canals: {it('θ')}̇ only", "label", anchor="middle"))
    o.append(lines(s, 10, 178, ["Prop 3.1: C = [0 1]", "O = [C; CA]", "  = [0 1; ω₀² 0]", "det O = −ω₀²", f"  = {-W0 ** 2:.2f}: rank 2"],
                   "label2"))
    # top plot: what the canals measure; bottom: truth vs reconstruction
    sel = slice(0, None, 20)
    Pm = Plot(s, (200, 56, 388, 130), (0, 3), (-8, 8))
    o.append(H.line(s, Pm.x0, Pm.y0, Pm.x1, Pm.y0, I["axis"], "axis"))
    o.append(H.line(s, Pm.x0, Pm.y0, Pm.x0, Pm.y1, I["axis"], "axis"))
    for v in (-5, 0, 5):
        o.append(H.line(s, Pm.x0 - 5, Pm.Y(v), Pm.x0, Pm.Y(v), I["axis"], "leader"))
        o.append(plabel(s, Pm.x0 - 8, Pm.Y(v) + 4.5, f"{v}".replace("-", "−"), "tick", I["secondary"], "end"))
    o.append(Pm.curve(t[sel], yy[sel], SER[2], multi=True, nmax=150))
    o.append(plabel(s, 200, 42, "canals: rate + noise (°/s)", "label2"))
    Pb = Plot(s, (200, 172, 388, 262), (0, 3), (-4, 4))
    o.append(Pb.axes([(0, "0"), (1, "1"), (2, "2"), (3, "3")], [(-3, "−3"), (0, "0"), (3, "3")], "time (s)", "angle θ (°)",
                     grid=(-3, 3), ytx=162))
    o.append(Pb.curve(t[sel], th[sel], SER[1], multi=True, nmax=120))
    o.append(Pb.curve(t[sel], thh[sel], SER[0], multi=True, nmax=120, dash=(5, 3)))
    o.append(legend(s, 200, 154, [(SER[1], "true θ", None), (SER[0], "rebuilt θ̂", (5, 3))], gap=8))
    o.append(plabel(s, Pb.X(0.06), Pb.Y(0.2) + s(16), "starts at 0", "tick", I["secondary"]))
    o.append(plabel(s, 388 - s(2), Pb.Y(-2.9), f"error < 10 % from {t1:.2f} s", "tick", I["secondary"], "end"))
    o.append(lines(s, 10, 322, ["the model links angle and rate, so the angle the sensor", "never reports is rebuilt from the rate (observer poles", "at −6 s⁻¹, design value; noise 0.05 rad/s per sample)"],
                   "tick", lead=1.25))
    o.append(credit(s, VB))
    aria = ("Left, a skull from Lynch's skeleton art with the note that the semicircular canals report head angular "
            "velocity only. Right, a simulation of the closed loop at the design gains with a rate-only observer. Top: "
            "the canal measurement, the sway rate plus noise (orange). Bottom: the true sway angle (blue) and the angle "
            "the observer reconstructs from the rate alone (red, dashed), starting from zero while the true angle is "
            "2.9 degrees: the reconstruction is within 10 percent of the starting error in about "
            f"{t1:.1f} s and then follows the truth. This works because the pair (A, C) is observable: the observability "
            "matrix [0 1; omega0 squared 0] has determinant minus omega0 squared = -9.61, rank 2.")
    pts = [[Pb.X(t[i]), [Pb.Y(th[i]), Pb.Y(thh[i])], f"t = {t[i]:.2f} s: true {th[i]:+.2f}°, reconstructed {thh[i]:+.2f}°".replace("-", "−")]
           for i in range(0, len(t), 25)]
    ptm = [[Pm.X(t[i]), Pm.Y(yy[i]), f"t = {t[i]:.2f} s: measured rate {yy[i]:+.2f} °/s".replace("-", "−")]
           for i in range(0, len(t), 25)]
    return finish(VB, aria, s, o, extra=H.hover_attr([(Pm.box, ptm), (Pb.box, pts)]))


# ================================================================ svg #27  C10 the predictor beats the delay (Lab C)
def lab_c(tau=0.10, w0=3.1, kp=20.0, kd=3.0, dt=0.005, T=8.0, qp=0.6, rm=0.07, seed=11):
    """Lab C of module10.html (lines 441-481), ported line for line: true sway, delayed noisy measurement, Kalman
    filter, and the tau-ahead predictor.  Returns the time axis, truth theta, measurement z, predicted estimate."""
    def expm(Mx, terms=25):                                   # matrix exponential by series
        S, term = np.eye(len(Mx)), np.eye(len(Mx))
        for k in range(1, terms):
            term = term @ Mx / k
            S = S + term
        return S
    rng = np.random.default_rng(seed)
    A = np.array([[0, 1.0], [-(kp - w0 * w0), -kd]])
    F, Fp = expm(A * dt), expm(A * tau)
    n, d = int(T / dt), int(round(tau / dt))
    xt = np.zeros((n, 2))
    xt[0] = [0.08, 0.0]
    for i in range(n - 1):
        kick = np.sqrt(qp * dt) * rng.standard_normal()
        xt[i + 1] = F @ xt[i] + [0, kick]
    z = np.full(n, np.nan)
    for i in range(d, n):
        z[i] = xt[i - d, 0] + rm * rng.standard_normal()
    Hm = np.array([[1.0, 0.0]])
    Q = np.array([[0, 0], [0, qp * dt]])
    P, xc = np.eye(2) * 0.05, np.array([0.08, 0.0])
    pred = np.full(n, np.nan)
    for i in range(1, n):
        xc, P = F @ xc, F @ P @ F.T + Q
        if not np.isnan(z[i]):
            S = (Hm @ P @ Hm.T)[0, 0] + rm * rm
            Kk = (P @ Hm.T)[:, 0] / S
            xc = xc + Kk * (z[i] - (Hm @ xc)[0])
            P = (np.eye(2) - np.outer(Kk, Hm[0])) @ P
        pred[i] = (Fp @ xc)[0]
    mm = ~np.isnan(z)
    raw = np.sqrt(np.nanmean((z[mm] - xt[mm, 0]) ** 2))
    prd = np.sqrt(np.nanmean((pred[mm] - xt[mm, 0]) ** 2))
    return np.arange(n) * dt, xt[:, 0], z, pred, raw, prd


def fig27():
    p = "m10f27_"
    VB, s = VBs(368)
    o = []
    TAU = 0.10
    t, xt, z, pred, raw, prd = lab_c(TAU)
    close(raw, 0.075, 0.0005)                                 # line 484
    close(prd, 0.033, 0.0005)
    close(prd / raw, 0.44, 0.02)                              # "less than half"
    ok = ~np.isnan(z)
    pl = Plot(s, (62, 96, 330, 250), (0, 8), (-0.3, 0.3))
    o.append(pl.axes([(0, "0"), (2, "2"), (4, "4"), (6, "6"), (8, "8")], [(-0.2, "−0.2"), (0, "0"), (0.2, "0.2")],
                     "time (s)", "sway angle θ (rad)", grid=(-0.2, 0.2), ytx=15))
    o.append(pl.curve(t[ok], z[ok], SER[1], multi=True, nmax=200))
    o.append(pl.curve(t[ok], pred[ok], SER[0], multi=True, nmax=120))
    o.append(pl.curve(t, xt, I["primary"], nmax=120))
    o.append(legend(s, 62, 24, [(I["primary"], "true θ(t)", None)]))
    o.append(legend(s, 62, 41, [(SER[1], f"raw delayed measurement: RMS {raw:.3f} rad", None)]))
    o.append(legend(s, 62, 58, [(SER[0], f"predicted estimate: RMS {prd:.3f} rad", None)]))
    ends = sorted([(float(pl.Y(xt[-1])), "true"), (float(pl.Y(float(pred[-1]))), "predicted"), (float(pl.Y(float(z[-1]))), "raw")])
    ys_ = [q[0] for q in ends]
    for i in range(1, 3):
        ys_[i] = max(ys_[i], ys_[i - 1] + s(17))
    for (_, nm), yy in zip(ends, ys_):
        o.append(plabel(s, 336, yy + s(4), nm, "label2"))
    o.append(lines(s, 10, 318, ["Lab C: qp = 0.6 (16 times quiet standing), rm = 0.07 rad;",
                                f"the filter estimates the state {TAU * 1000:.0f} ms ago;",
                                "the predictor exp(Aτ) pushes the estimate to the present"], "tick", lead=1.25))
    aria = ("A simulated sway angle against time, 0 to 8 s, from Lab C at a delay of 100 ms and sixteen times the "
            "quiet-standing noise. The true angle (black) rings down from 0.08 rad. The raw delayed measurement (blue) "
            "is noisy and lags it, with an RMS error of 0.075 rad. The estimate that the Kalman filter and the delay "
            "predictor produce (red) tracks the true present angle with an RMS error of 0.033 rad, less than half. "
            "The forward model pushes the estimate across the delay, so feeding the controller the predicted "
            "present state restores the stability island that the raw delayed signal destroys.")
    pts = [[pl.X(t[i]), [pl.Y(xt[i]), pl.Y(float(pred[i])), pl.Y(float(z[i]))],
            f"t = {t[i]:.2f} s: true {xt[i]:+.3f}, predicted {pred[i]:+.3f}, raw {z[i]:+.3f} rad".replace("-", "−")]
           for i in range(int(round(TAU / 0.005)), len(t), 4)]
    return finish(VB, aria, s, o, extra=H.hover_attr(pl.box, pts))


FIGS = {
    18: ("C1: A gymnast stands motionless with her centre of mass over", fig18),
    19: ("C2: Why can a person never stand perfectly still, even with ", fig19),
    20: ("C3: A patient stands well with eyes open on firm ground but ", fig20),
    21: ("C4: A coach says a good stumble-recovery is 'just a much str", fig21),
    22: ("C5: Two people fall on ice: one lands on their back, one on ", fig22),
    23: ("C6: An engineer models the nervous system as trusting each b", fig23),
    24: ("C7: 'If proportional gain stabilises standing, more gain mus", fig24),
    25: ("C8: A clinician writes 'falls due to age.' Rewrite the cause", fig25),
    26: ("C9: The semicircular canals report only head angular velocit", fig26),
    27: ("C10: The feedback delay is fixed by biology and cannot be sh", fig27),
}
