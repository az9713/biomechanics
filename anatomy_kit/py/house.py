"""House figure style for the 2026-10 redraw (one style for all 18 modules).

Single source of truth: the style guide page and every figure generator read these
tokens. `style.py` is the OLD Tier-2 capsule style; it stays only for old generators.

Tissue colours are sampled from the approved fig21 (InjuryMap "Lower leg muscles.svg",
rendered at 900 px, most common pixel per region) or taken from its CSS where a flat
value exists. Overlay colours are the ones the approved sample already uses.
"""
import html
import json
import re

FONT = "Georgia, 'Times New Roman', serif"   # same as the course body text

# ---------------------------------------------------------------- tissue (fill, line)
TISSUE = {
    "skin":       ("#fde0d1", "#f0bfa6"),   # fig21 soft-tissue silhouette
    "bone":       ("#f2debf", "#c79f84"),   # fig21 tibia shaft / InjuryMap bone stroke
    "bone_shade": ("#e1c0a4", "#c79f84"),   # InjuryMap gradient dark stop (bone in shadow)
    "marrow":     ("#e6cfa9", "#c79f84"),   # cancellous / medullary region in sections
    "cartilage":  ("#e8f5fc", "#c79f84"),   # InjuryMap articular cartilage (cls-63)
    "fibrocart":  ("#a0cfdc", "#6f9fb0"),   # fig21 meniscus
    "muscle":     ("#c87272", "#8e3b3f"),   # fig21 gastrocnemius belly
    "muscle_dk":  ("#a9474d", "#8e3b3f"),   # fibre lines, deep muscle
    "tendon":     ("#eee2da", "#c79f84"),   # fig21 Achilles tendon
    "fat":        ("#f6dc8a", "#c9a95a"),   # fat pads (DBCLS yellow, toned down)
    "fluid":      ("#b9d3ee", "#4a6f99"),   # synovial fluid / joint cavity
    "nerve":      ("#f2d16b", "#9c7d1e"),   # anatomical nerve trunk (drawn tissue)
    "actin":      ("#6fa3d0", "#3f73a0"),   # thin filament (module05 caption: "thin (blue)")
    "myosin":     ("#a9474d", "#7a2a30"),   # thick filament (module05 caption: "thick (red)")
    "zdisc":      ("#555555", "#333333"),
}

# ---------------------------------------------------------------- overlays (meaning -> colour)
INK = {"primary": "#1a1a1a", "secondary": "#555555", "muted": "#777777", "rule": "#999999",
       "axis": "#333333", "halo": "#ffffff", "credit": "#666666"}
OVERLAY = {
    "force":    "#b03a2e",   # muscle / tendon force, line of action
    "geometry": "#2a6ca8",   # moment arm, length, angle, any dimension that is the subject
    "load":     "#5b3a1a",   # weight, external load, dimension of the load
    "reaction": "#1a1a1a",   # joint reaction force
    "neural":   "#2a7d2a",   # neural drive, motor nerve signal, "productive" region
    "flag":     "#e67e22",   # breakpoint, special point, "double overlap" (always labelled)
    "dim":      "#555555",   # reference dimension, joint line, construction line
}
# Plot series, fixed order, never cycled. Validated with the dataviz validator (light,
# adjacent pairs): all PASS; #e67e22 has contrast 2.77:1, so it is always direct-labelled.
SERIES = ["#b03a2e", "#2a6ca8", "#e67e22", "#2a7d2a"]

# ---------------------------------------------------------------- sizes, in RENDERED px
DISPLAY_W = 760          # default rendered width of a full-column figure (body max 52rem)
MAX_DISPLAY_H = 640      # tall figures shrink their width so the height stays <= this
MAX_DISPLAY_H_BODY = 900  # whole-body figures may be taller (the author, 2026-10-12)
PX = {
    "label": 15, "label2": 13, "tick": 13, "credit": 11,
    "force": 2.5, "geom": 2.0, "load": 2.5, "leader": 1.0, "ref": 1.4, "axis": 1.4,
    "curve": 2.5, "curve_multi": 2.0, "art_line": 1.2,
    "head_force": 11, "head_geom": 8, "dot": 4,
}
DASH_REF = (6, 4)        # px, reference / construction lines
DASH_LOA = (4, 3)        # px, line of action extension


class Scale:
    """Convert rendered px to user units for one figure: u = viewBox width / rendered width."""

    def __init__(self, vb_w, vb_h, display_w=DISPLAY_W, max_h=MAX_DISPLAY_H):
        self.display_w = min(display_w, max_h * vb_w / vb_h)
        self.u = vb_w / self.display_w

    def __call__(self, px):
        return px * self.u


# ---------------------------------------------------------------- recolour maps (source hex -> house hex)
RECOLOUR = {
    "lynch": {                       # Patrick J. Lynch, Skeleton lateral.svg
        "#414142": TISSUE["skin"][0],      # body silhouette (dark grey)
        "#828487": TISSUE["bone"][0],      # the 28 large bone fills (mid grey)
        "#d1d3d4": TISSUE["bone_shade"][0],  # 329 detail shapes and edge strokes (light grey)
    },
    "nih": {                         # NIH BioArt 208 / 244 (kit copies)
        "#f8f2e5": TISSUE["bone"][0],
        "#d4c4a0": TISSUE["bone_shade"][1],
    },
    "dbcls": {                       # DBCLS sagittal sections (elbow, knee)
        "#e2dacf": TISSUE["bone"][0],      # cortical bone
        "#aaa59f": TISSUE["marrow"][0],    # medullary / cancellous interior
        "#c6baa8": TISSUE["bone_shade"][0],
        "#a59983": TISSUE["bone_shade"][1],
        "#84755d": TISSUE["bone"][1],      # all outlines
        "#f28b8b": TISSUE["muscle"][0],
        "#e56a70": TISSUE["muscle_dk"][0],
        "#adbcf2": TISSUE["fluid"][0],     # joint cavity
        "#29426d": TISSUE["fluid"][1],
        "#6079b2": TISSUE["fluid"][1],
        "#ffd664": TISSUE["fat"][0],
        "#ffe1e3": TISSUE["skin"][0],
        "#fff3f3": TISSUE["skin"][0],
        "#fdd6d8": TISSUE["skin"][0],
    },
    "injurymap": {},                 # target look: unchanged
}


def recolour(svg_text, source):
    """Replace every source hex (any case, 3- or 6-digit as written) by its house value."""
    m = RECOLOUR[source]
    if not m:
        return svg_text
    pat = re.compile("|".join(re.escape(k) for k in m), re.I)
    return pat.sub(lambda h: m[h.group(0).lower()], svg_text)


# ---------------------------------------------------------------- drawing helpers
def markers(p, s):
    """Slim arrowheads, userSpaceOnUse, one per overlay meaning. Ids: {p}a_<meaning>."""
    out = []
    for name, col in OVERLAY.items():
        sz = s(PX["head_geom"] if name in ("geometry", "dim") else PX["head_force"])
        out.append(
            f'<marker id="{p}a_{name}" markerUnits="userSpaceOnUse" markerWidth="{sz*1.2:.2f}" '
            f'markerHeight="{sz*0.8:.2f}" refX="{sz*0.95:.2f}" refY="{sz*0.4:.2f}" orient="auto-start-reverse">'
            f'<path d="M0,0 L{sz:.2f},{sz*0.4:.2f} L0,{sz*0.8:.2f} Z" fill="{col}"/></marker>')
    return "".join(out)


def label(s, x, y, text, size="label", fill=INK["primary"], anchor="start", extra=""):
    """Figure text: Georgia, white halo (paint-order stroke) so it reads over art and lines."""
    fs = s(PX[size])
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-size="{fs:.2f}" fill="{fill}" text-anchor="{anchor}" '
            f'stroke="{INK["halo"]}" stroke-width="{fs*0.28:.2f}" stroke-linejoin="round" '
            f'paint-order="stroke" {extra}>{text}</text>')


def line(s, x1, y1, x2, y2, col, w="leader", dash=None, extra=""):
    da = f' stroke-dasharray="{s(dash[0]):.2f} {s(dash[1]):.2f}"' if dash else ""
    return (f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{col}" '
            f'stroke-width="{s(PX[w]):.2f}"{da} {extra}/>')


def arrow(s, p, x1, y1, x2, y2, meaning, w=None, both=False):
    """A vector: thin shaft + slim head at (x2, y2). both=True for a dimension."""
    col = OVERLAY[meaning]
    w = w or {"geometry": "geom", "dim": "ref"}.get(meaning, "force")
    ms = f' marker-start="url(#{p}a_{meaning})"' if both else ""
    return line(s, x1, y1, x2, y2, col, w, extra=f'marker-end="url(#{p}a_{meaning})"{ms}')


def joint_centre(s, x, y):
    """Cross-hair circle: a mark, not anatomy."""
    r = s(5)
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="none" stroke="#fff" stroke-width="{s(3):.2f}"/>'
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="none" stroke="{INK["primary"]}" stroke-width="{s(1.2):.2f}"/>'
            f'<path d="M{x-r*1.6:.2f},{y:.2f}h{r*3.2:.2f}M{x:.2f},{y-r*1.6:.2f}v{r*3.2:.2f}" '
            f'stroke="{INK["primary"]}" stroke-width="{s(1.0):.2f}"/>')


def com_mark(s, x, y):
    """Centre of mass: circle with two filled quadrants."""
    r = s(6)
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r+s(1.5):.2f}" fill="#fff"/>'
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="#fff" stroke="#111" stroke-width="{s(1.1):.2f}"/>'
            f'<path d="M{x:.2f},{y:.2f} L{x+r:.2f},{y:.2f} A{r:.2f},{r:.2f} 0 0 0 {x:.2f},{y-r:.2f} Z '
            f'M{x:.2f},{y:.2f} L{x-r:.2f},{y:.2f} A{r:.2f},{r:.2f} 0 0 0 {x:.2f},{y+r:.2f} Z" fill="#111"/>')


def sub(t, s, size="label"):
    """Subscript tspan (MathJax does not run inside <svg><text>)."""
    return f'<tspan baseline-shift="sub" font-size="{s(PX[size]*0.7):.2f}">{t}</tspan>'


def credit(s, x, y, lines):
    fs = s(PX["credit"])
    return "".join(f'<text x="{x:.2f}" y="{y + i*fs*1.25:.2f}" font-size="{fs:.2f}" fill="{INK["credit"]}">{t}</text>'
                   for i, t in enumerate(lines))


ATTRIBUTION = {
    "by": "Art: {author}, “{title}”, {licence}, via Wikimedia Commons. {changes}",
    "by-sa": "Art: {author}, “{title}”, CC BY-SA 4.0, via Wikimedia Commons. {changes} This figure: CC BY-SA 4.0.",
    "pd": "Art: {author}, “{title}”, public domain (U.S. Government work). {changes}",
}


def svg_open(vb, aria, s, extra=""):
    x, y, w, h = vb
    return (f'<svg xmlns="http://www.w3.org/2000/svg" class="setupfig" viewBox="{x} {y} {w} {h}" width="100%" '
            f'style="max-width:{s.display_w:.0f}px;overflow:hidden;background:#fff" role="img" aria-label="{aria}" {extra} '
            f'font-family="{FONT}">')


# ---------------------------------------------------------------- plot hover (the author, 2026-10-12)
HOVER_MAX = 120          # points per panel. ponytail: uniform decimation can skip a ripple peak in the read-out


def hover_attr(box, pts=None):
    """data-hover for HOVER_JS. box = plot area (x0, y_top, x1, y_bottom) in user units;
    pts = [[x, y or [y1, y2, ...], "tooltip text"], ...] in user units, sorted by x.
    Several panels: hover_attr([(box1, pts1), (box2, pts2), ...]); the panel under the pointer is used.
    Bars: one point per bar (x = bar centre); the nearest point by x wins.
    Coordinates are rounded to 0.1 unit and each panel keeps at most HOVER_MAX points (uniform by index,
    first and last kept), so the page stays small (the author, 2026-10-12)."""
    def slim(q):
        if len(q) > HOVER_MAX:
            q = [q[round(i * (len(q) - 1) / (HOVER_MAX - 1))] for i in range(HOVER_MAX)]
        r = lambda v: [r(w) for w in v] if isinstance(v, (list, tuple)) else round(v, 1)  # noqa: E731
        return [[r(x), r(y), t] for x, y, t in q]
    panels = [{"box": b, "pts": q} for b, q in box] if pts is None else [{"box": box, "pts": pts}]
    panels = [{"box": [round(v, 1) for v in d["box"]], "pts": slim(d["pts"])} for d in panels]
    d = json.dumps({"panels": panels}, ensure_ascii=False, separators=(",", ":"))
    return "data-hover='" + html.escape(d, quote=False).replace("'", "&#39;") + "'"


# One copy per page, after the figures. No library. The tooltip nodes are created on the first
# pointer move, so the static SVG (and the repo gates) never contain them.
HOVER_JS = """<script>
document.querySelectorAll('svg[data-hover]').forEach(function (svg) {
  var P = JSON.parse(svg.getAttribute('data-hover')).panels, NS = 'http://www.w3.org/2000/svg', g, vl, txt, bg, dots = [];
  function el(n, a) { var e = document.createElementNS(NS, n); for (var k in a) e.setAttribute(k, a[k]); return e; }
  function make() {
    g = el('g', {'pointer-events': 'none'});
    vl = el('line', {stroke: '#999', 'stroke-dasharray': '4 3'});
    bg = el('rect', {fill: '#fff', stroke: '#999', rx: 3});
    txt = el('text', {fill: '#1a1a1a', 'font-family': 'Georgia, serif'});
    g.append(vl, bg, txt); svg.appendChild(g);
  }
  function show(e) {
    var p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY;
    p = p.matrixTransform(svg.getScreenCTM().inverse());
    var D = null;
    P.forEach(function (q) { var c = q.box; if (p.x >= c[0] && p.x <= c[2] && p.y >= c[1] && p.y <= c[3]) D = q; });
    if (!D) { if (g) g.style.display = 'none'; return; }
    var b = D.box;
    if (!g) make();
    var best = D.pts[0];
    D.pts.forEach(function (q) { if (Math.abs(q[0] - p.x) < Math.abs(best[0] - p.x)) best = q; });
    var u = svg.viewBox.baseVal.width / svg.getBoundingClientRect().width, ys = [].concat(best[1]);
    g.style.display = '';
    vl.setAttribute('x1', best[0]); vl.setAttribute('x2', best[0]);
    vl.setAttribute('y1', b[1]); vl.setAttribute('y2', b[3]); vl.setAttribute('stroke-width', u);
    while (dots.length < ys.length) { var c = el('circle', {fill: '#fff', stroke: '#1a1a1a'}); g.insertBefore(c, bg); dots.push(c); }
    dots.forEach(function (c, i) {
      c.style.display = i < ys.length ? '' : 'none';
      if (i < ys.length) { c.setAttribute('cx', best[0]); c.setAttribute('cy', ys[i]); c.setAttribute('r', 4 * u); c.setAttribute('stroke-width', 1.5 * u); }
    });
    txt.textContent = best[2]; txt.setAttribute('font-size', 13 * u);
    var w = txt.getComputedTextLength(), pad = 5 * u, h = 13 * u, V = svg.viewBox.baseVal, right = best[0] + 10 * u + w + 2 * pad < V.x + V.width;
    var tx = right ? best[0] + 10 * u + pad : Math.max(V.x + 2 * pad, best[0] - 10 * u - pad - w), ty = Math.max(b[1] + h + pad, Math.min.apply(null, ys) - 8 * u);
    txt.setAttribute('x', tx); txt.setAttribute('y', ty);
    bg.setAttribute('x', tx - pad); bg.setAttribute('y', ty - h); bg.setAttribute('width', w + 2 * pad); bg.setAttribute('height', h + pad);
    bg.setAttribute('stroke-width', u);
  }
  svg.addEventListener('pointermove', show);
  svg.addEventListener('pointerdown', show);
  svg.addEventListener('pointerleave', function () { if (g) g.style.display = 'none'; });
});
</script>"""


# ---------------------------------------------------------------- motion: slider + Play (decision 5)
def frames_attr(label, values, default):
    """data-frames for FRAMES_JS. The svg holds one <g data-frame="k"> per value; every frame but
    `default` carries style="display:none", so without JS the figure is the still default frame."""
    d = json.dumps({"label": label, "values": values, "def": default}, ensure_ascii=False, separators=(",", ":"))
    return "data-frames='" + html.escape(d, quote=False).replace("'", "&#39;") + "'"


def frame(k, default, body):
    hide = "" if k == default else ' style="display:none"'
    return f'<g data-frame="{k}"{hide}>{body}</g>'


# One copy per page, after the figures. Adds a slider (and a Play button unless the reader asked
# for reduced motion) under each svg[data-frames]. Play is never automatic.
FRAMES_JS = """<script>
document.querySelectorAll('svg[data-frames]').forEach(function (svg) {
  var C = JSON.parse(svg.getAttribute('data-frames')), fr = svg.querySelectorAll('g[data-frame]'), n = fr.length, timer = null;
  var still = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var box = document.createElement('div');
  box.style.cssText = 'display:flex;gap:.6rem;align-items:center;justify-content:center;margin:.3rem 0;font-size:.9rem';
  var btn = document.createElement('button'); btn.type = 'button'; btn.textContent = '\u25B6 Play';
  var rng = document.createElement('input'); rng.type = 'range'; rng.min = 0; rng.max = n - 1; rng.step = 1;
  rng.setAttribute('aria-label', C.label); rng.style.width = '14rem';
  var out = document.createElement('output'); out.style.minWidth = '9rem';
  function show(k) {
    fr.forEach(function (g, i) { g.style.display = i === k ? '' : 'none'; });
    rng.value = k; out.textContent = C.label + ' = ' + C.values[k];
  }
  function stop() { clearInterval(timer); timer = null; btn.textContent = '\u25B6 Play'; }
  btn.onclick = function () {
    if (timer) return stop();
    var k = +rng.value >= n - 1 ? 0 : +rng.value; btn.textContent = '\u275A\u275A Pause';
    timer = setInterval(function () { k += 1; if (k >= n) { stop(); return; } show(k); }, 120);
  };
  rng.oninput = function () { stop(); show(+rng.value); };
  if (!still) box.appendChild(btn);
  box.append(rng, out); svg.after(box); show(C.def);
});
</script>"""


if __name__ == "__main__":
    s = Scale(380, 1080)
    assert abs(s.display_w - 640 * 380 / 1080) < 1e-9 and abs(s(15) - 15 * 1080 / 640) < 1e-9
    assert abs(Scale(550, 1110, max_h=MAX_DISPLAY_H_BODY).display_w - 900 * 550 / 1110) < 1e-9
    assert recolour('fill:#828487;x', "lynch") == f'fill:{TISSUE["bone"][0]};x'
    assert recolour('fill:#D1D3D4', "lynch") == f'fill:{TISSUE["bone_shade"][0]}'
    assert recolour("#abc", "injurymap") == "#abc"
    a = hover_attr([0, 0, 10, 10], [[1, 2, "it's <1>"]])
    assert a.startswith("data-hover='") and "'" not in a[12:-1] and "<" not in a
    assert json.loads(html.unescape(a[12:-1]))["panels"][0]["pts"][0][2] == "it's <1>"
    two = json.loads(html.unescape(hover_attr([([0, 0, 5, 5], [[1, 1, "a"]]), ([6, 0, 9, 5], [[7, 1, "b"]])])[12:-1]))
    assert [q["pts"][0][2] for q in two["panels"]] == ["a", "b"]
    big = json.loads(html.unescape(hover_attr([0, 0, 9, 9], [[i / 3, [i * 1.234, 2.0], str(i)] for i in range(301)])[12:-1]))
    q = big["panels"][0]["pts"]
    assert len(q) == HOVER_MAX and q[0][2] == "0" and q[-1][2] == "300" and q[1] == [1.0, [3.7, 2.0], "3"]
    assert frame(1, 0, "x") == '<g data-frame="1" style="display:none">x</g>' and frame(0, 0, "x") == '<g data-frame="0">x</g>'
    assert "<rect" not in svg_open((0, 0, 10, 10), "a", Scale(10, 10))
    print("house.py self-check OK")
