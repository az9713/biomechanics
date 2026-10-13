"""One-time crop of a source art SVG to the window a figure shows (keeps page size down).

Run:  python -I crop_art.py SRC.svg NAME X0 Y0 X1 Y1 [--drop "CSS selector"] [--png SCALE] [--rot DEG CX CY]
(--rot: the box is given in the frame rotated by DEG about CX, CY, as SVG rotate() turns it.)
Loads SRC in Chrome, removes the --drop elements, then every drawn element whose rendered box
(getBBox through getCTM, in root user units) misses the box X0..X1 x Y0..Y1. Empty groups and
unreferenced defs go too. Path points are rounded to 0.1 unit (written as relative steps).
Writes svg_paths/<SRC stem>_crop_<NAME>.svg next to SRC.
"""
import re
import sys
from pathlib import Path

JS = """([x0, y0, x1, y1, drop, rot, rcx, rcy]) => {
  const ca = Math.cos(rot * Math.PI / 180), sa = Math.sin(rot * Math.PI / 180);
  const root = document.documentElement, inv = root.getCTM().inverse();
  if (drop) document.querySelectorAll(drop).forEach(e => e.remove());
  const skip = 'defs,mask,clipPath,pattern,marker,symbol,filter,linearGradient,radialGradient';
  let n = 0;
  document.querySelectorAll('path,rect,circle,ellipse,line,polyline,polygon,image,use,text').forEach(e => {
    if (e.closest(skip)) return;
    const b = e.getBBox(), m = inv.multiply(e.getCTM());
    const xs = [], ys = [];
    for (const [px, py] of [[b.x, b.y], [b.x + b.width, b.y], [b.x, b.y + b.height], [b.x + b.width, b.y + b.height]]) {
      const qx = m.a * px + m.c * py + m.e - rcx, qy = m.b * px + m.d * py + m.f - rcy;   // into the rotated frame
      xs.push(qx * ca - qy * sa + rcx); ys.push(qx * sa + qy * ca + rcy);
    }
    if (Math.max(...xs) < x0 || Math.min(...xs) > x1 || Math.max(...ys) < y0 || Math.min(...ys) > y1) { e.remove(); n++; }
  });
  let again = true;
  while (again) { again = false;
    document.querySelectorAll('g').forEach(g => { if (!g.closest(skip) && !g.firstElementChild) { g.remove(); again = true; } }); }
  return [n, new XMLSerializer().serializeToString(root)];
}"""

NUM = re.compile(r'[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?')
LEVELS = 8                             # grey levels kept in a mask PNG
ARGS = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}


def fmt(v):
    s = f"{round(v, 1):.1f}".rstrip("0").rstrip(".")
    s = "0" if s in ("-0", "") else s
    return s.replace("0.", ".", 1) if s.startswith("0.") else s.replace("-0.", "-.", 1)


def absolute(d):
    """Path data -> relative commands whose deltas run between points rounded to 0.1 unit, so rounding
    error never accumulates (arc flags are parsed one digit each)."""
    i, out, cmd, first = 0, [], None, True
    cx = cy = sx = sy = 0.0            # exact current point and subpath start
    rx = ry = rsx = rsy = 0.0          # the same, rounded
    while i < len(d):
        ch = d[i]
        if ch in " ,\t\r\n":
            i += 1
            continue
        if ch.isalpha():
            cmd, i = ch, i + 1
            if cmd in "Zz":
                out.append("z")
                cx, cy, rx, ry = sx, sy, rsx, rsy
                continue
        args = []
        for k in range(ARGS[cmd.upper()]):
            while d[i] in " ,\t\r\n":
                i += 1
            if cmd in "Aa" and k in (3, 4):
                args.append(float(d[i]))
                i += 1
            else:
                m = NUM.match(d, i)
                args.append(float(m.group()))
                i = m.end()
        C, rel = cmd.upper(), cmd.islower()
        if C == "H":
            cx = args[0] + (cx if rel else 0)
            X = round(cx, 1)
            out.append("h" + fmt(X - rx))
            rx = X
        elif C == "V":
            cy = args[0] + (cy if rel else 0)
            Y = round(cy, 1)
            out.append("v" + fmt(Y - ry))
            ry = Y
        elif C == "A":
            cx, cy = args[5] + (cx if rel else 0), args[6] + (cy if rel else 0)
            X, Y = round(cx, 1), round(cy, 1)
            out.append("a" + " ".join(fmt(v) for v in args[:3]) + f" {int(args[3])} {int(args[4])} "
                       + fmt(X - rx) + " " + fmt(Y - ry))
            rx, ry = X, Y
        else:
            pts = [(args[j] + (cx if rel else 0), args[j + 1] + (cy if rel else 0)) for j in range(0, len(args), 2)]
            rp = [(round(x, 1), round(y, 1)) for x, y in pts]
            if C == "M" and first:
                out.append("M" + fmt(rp[0][0]) + " " + fmt(rp[0][1]))
                first = False
            else:
                out.append(C.lower() + " ".join(fmt(x - rx) + " " + fmt(y - ry) for x, y in rp))
            cx, cy = pts[-1]
            rx, ry = rp[-1]
            if C == "M":
                sx, sy, rsx, rsy = cx, cy, rx, ry
                cmd = "l" if rel else "L"            # implicit lineto after moveto
    return re.sub(r"(\.\d+) (?=\.)", r"\1", "".join(out).replace(" -", "-"))


DEFS = r'<(?:mask|clipPath|linearGradient|radialGradient|filter|pattern)\b[^>]*\bid="([^"]+)"'


def tidy(svg):
    svg = re.sub(r'\sd="([^"]+)"', lambda m: f' d="{absolute(m.group(1))}"', svg)

    def rule(m, used):
        sel = [x.strip() for x in m.group(1).split(",") if x.strip().lstrip(".") in used]
        return f"{','.join(sel)}{{{m.group(2)}}}" if sel else ""
    while True:                    # unused CSS rules, then unreferenced defs (masks, gradients, filters, clips)
        n0 = len(svg)
        used = set(c for a in re.findall(r'class="([^"]+)"', svg) for c in a.split())
        svg = re.sub(r'<style[^>]*>(.*?)</style>', lambda m: "<style>" + re.sub(
            r'([^{}]+)\{([^{}]*)\}', lambda r: rule(r, used), m.group(1)) + "</style>", svg, flags=re.S)
        for idv in re.findall(DEFS, svg):
            if not re.search(rf'url\(#{re.escape(idv)}\)|href="#{re.escape(idv)}"', svg):
                svg = re.sub(rf'<(\w+)\b[^>]*\bid="{re.escape(idv)}"[^>]*?(?:/>|>.*?</\1>)', '', svg, count=1, flags=re.S)
        if len(svg) == n0:
            break
    return re.sub(r'>\s+<', '><', svg)


def minify(svg, png_scale):
    """Size only, same look: one shared copy of filters that differ only in their userSpaceOnUse region
    (valid when each region equals its element's box, as in InjuryMap's mask filters), short ids and
    class names, numbers to 0.1 (not inside transforms: matrix terms need the digits), and grey mask PNGs re-encoded as LEVELS-level greyscale at png_scale."""
    groups = {}
    for m in re.finditer(r'<filter\b([^>]*)>(.*?)</filter>', svg, re.S):
        attrs = re.sub(r'\s(?:id|x|y|width|height|filterUnits)="[^"]*"', '', m.group(1))
        groups.setdefault((attrs, m.group(2)), []).append(re.search(r'\bid="([^"]+)"', m.group(1)).group(1))
    for (attrs, body), ids in groups.items():
        if len(ids) > 1:
            keep = ids[0]
            svg = re.sub(rf'<filter\b[^>]*\bid="{re.escape(keep)}"[^>]*>',
                         f'<filter id="{keep}" x="0" y="0" width="1" height="1"{attrs}>', svg, count=1)
            for i in ids[1:]:
                svg = re.sub(rf'<filter\b[^>]*\bid="{re.escape(i)}"[^>]*>.*?</filter>', '', svg, count=1, flags=re.S)
                svg = svg.replace(f"url(#{i})", f"url(#{keep})")
    svg = re.sub(r'\sdata-name="[^"]*"', '', svg).replace('xlink:href="', 'href="')
    refs = set(re.findall(r'url\(#([^)]+)\)', svg)) | set(re.findall(r'href="#([^"]+)"', svg))
    svg = re.sub(r'\sid="([^"]+)"', lambda m: m.group(0) if m.group(1) in refs else "", svg)
    ids = re.findall(r'\bid="([^"]+)"', svg)
    short = {v: f"i{k:x}" for k, v in enumerate(ids)}
    svg = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{short[m.group(1)]}"', svg)
    svg = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{short.get(m.group(1), m.group(1))})', svg)
    svg = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{short.get(m.group(1), m.group(1))}"', svg)
    svg = re.sub(r'\bcls-(\d+)', r'c\1', svg)
    num = re.compile(r'-?\d+\.\d{2,}')
    svg = re.sub(r'\s(x|y|x1|y1|x2|y2|cx|cy|fx|fy|r|width|height)="([^"]*)"',
                 lambda m: f' {m.group(1)}="{num.sub(lambda n: fmt(float(n.group())), m.group(2))}"', svg)
    if png_scale:
        import base64
        import io
        from PIL import Image

        def png(m):
            im = Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert("RGB")
            r, g, b = im.split()
            if r.tobytes() != g.tobytes() or g.tobytes() != b.tobytes():
                return m.group(0)                        # colour image: leave it alone
            im = im.convert("L").resize((max(1, round(im.width * png_scale)), max(1, round(im.height * png_scale))),
                                        Image.LANCZOS).quantize(LEVELS).convert("L")
            bio = io.BytesIO()
            im.save(bio, "PNG", optimize=True)
            return "data:image/png;base64," + base64.b64encode(bio.getvalue()).decode("ascii")
        svg = re.sub(r'data:image/png;base64,([A-Za-z0-9+/=]+)', png, svg)
    return svg


def main(src, name, box, drop, png_scale, rot=(0.0, 0.0, 0.0)):
    from playwright.sync_api import sync_playwright
    src = Path(src).resolve()
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page()
        pg.goto(src.as_uri())
        n, svg = pg.evaluate(JS, [*box, drop, *rot])
        b.close()
    out = src.with_name(f"{src.stem}_crop_{name}.svg")
    out.write_text(minify(tidy(svg), png_scale), encoding="utf-8")
    print(f"{out.name}: removed {n} elements, {src.stat().st_size} -> {out.stat().st_size} bytes")


if __name__ == "__main__":
    a = sys.argv
    main(a[1], a[2], [float(v) for v in a[3:7]], a[a.index("--drop") + 1] if "--drop" in a else "",
         float(a[a.index("--png") + 1]) if "--png" in a else 0,
         [float(v) for v in a[a.index("--rot") + 1:a.index("--rot") + 4]] if "--rot" in a else (0.0, 0.0, 0.0))


