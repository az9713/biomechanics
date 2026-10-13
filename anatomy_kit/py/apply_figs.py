"""Put house-style redraws into a module page, matched by aria-label (never by number alone).

Each generator file anatomy_kit/py/mNN/<group>.py exposes
    FIGS = {svg_idx: (old_aria_prefix, build)}      build() -> "<svg ...>...</svg>" (house.svg_open)
svg_idx is the 1-based order of <svg> in the raw page (inventory/svg_inventory.csv `idx`); it is
only a label. The page svg is found by its old aria-label prefix, or, once applied, by its
data-fig="mNN-idx" stamp, so the script can be re-run after a generator changes.
HOVER_JS / FRAMES_JS go in once, before </body>, only if a figure needs them. A group may also expose
SHARED_DEFS() -> "<g id=...>...</g>" (art several figures <use>); it goes in once, after <body>.

Run:  python -I apply_figs.py 05            (writes moduleNN.html)
      python -I apply_figs.py 05 --check    (match only, write nothing)
"""
import html
import importlib
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
REPO = KIT.parents[1]
sys.path.insert(0, str(KIT))
import house as H  # noqa: E402

JS_A, JS_B = "<!--house-js-->", "<!--/house-js-->"
DEFS_A, DEFS_B = "<!--house-defs-->", "<!--/house-defs-->"


def shared_defs(mod):
    """One hidden svg with every group's SHARED_DEFS(), or "" if none."""
    mods = [importlib.import_module(f"m{mod}.{f.stem}") for f in sorted((KIT / f"m{mod}").glob("*.py"))
            if not f.stem.startswith("_")]
    d = "".join(m.SHARED_DEFS() for m in mods if hasattr(m, "SHARED_DEFS"))
    return (f'{DEFS_A}<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">'
            f'<defs>{d}</defs></svg>{DEFS_B}') if d else ""


def load(mod):
    figs = {}
    for f in sorted((KIT / f"m{mod}").glob("*.py")):
        if f.stem.startswith("_"):
            continue
        for idx, (aria, build) in importlib.import_module(f"m{mod}.{f.stem}").FIGS.items():
            assert idx not in figs, f"svg #{idx} built twice ({f.stem})"
            figs[idx] = (aria, build)
    return figs


def find(page, mod, idx, aria):
    hits = []
    for m in re.finditer(r"<svg\b.*?</svg>", page, re.S):
        tag = page[m.start():page.index(">", m.start())]
        a = re.search(r'aria-label="([^"]*)"', tag)
        if f'data-fig="m{mod}-{idx}"' in tag or (a and html.unescape(a.group(1)).startswith(aria)):
            hits.append(m)
    assert len(hits) == 1, f"svg #{idx}: {len(hits)} matches for {aria[:50]!r}"
    return hits[0]


def main(mod, write=True):
    path = REPO / f"module{mod}.html"
    page = path.read_bytes().decode("utf-8")      # keep the CRLF line ends of the working tree
    nl = "\r\n" if "\r\n" in page else "\n"
    figs = load(mod)
    spans = []
    for idx, (aria, build) in figs.items():
        m = find(page, mod, idx, aria)
        svg = build()
        assert svg.startswith("<svg ") and svg.endswith("</svg>") and 'class="setupfig"' in svg, idx
        svg = svg.replace("\r\n", "\n").replace("\n", nl)
        spans.append((m.start(), m.end(), svg.replace("<svg ", f'<svg data-fig="m{mod}-{idx}" ', 1)))
    for a, b, svg in sorted(spans, reverse=True):
        page = page[:a] + svg + page[b:]
    page = re.sub(re.escape(JS_A) + r".*?" + re.escape(JS_B) + r"\n?", "", page, flags=re.S)
    page = re.sub(re.escape(DEFS_A) + r".*?" + re.escape(DEFS_B), "", page, flags=re.S)
    page = re.sub(r"<body\b[^>]*>", lambda b: b.group(0) + shared_defs(mod), page, count=1)
    js = (H.HOVER_JS if "data-hover=" in page else "") + (H.FRAMES_JS if "data-frames=" in page else "")
    if js:
        page = page.replace("</body>", f"{JS_A}{js}{JS_B}\n</body>".replace("\n", nl), 1)
    print(f"module{mod}: {len(figs)} figures matched" + ("" if write else " (check only)"))
    if write:
        path.write_bytes(page.encode("utf-8"))


if __name__ == "__main__":
    main(sys.argv[1], write="--check" not in sys.argv)
