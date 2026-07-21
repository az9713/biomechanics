"""Download selected NIH BioArt / Wikimedia public-domain anatomy SVGs."""
from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "svg_paths"
OUT.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "anatomy_kit/1.0 (biomechanics course; educational)"}

# title on Commons → local stem
FILES = {
    "File:Human Upper Leg Bones (NIH BioArt 244 - 631095).svg": "nih_upper_leg",
    "File:Human Arm Bones (NIH BioArt 208 - 630553).svg": "nih_arm_bones",
}


def image_url(title: str) -> str:
    api = (
        "https://commons.wikimedia.org/w/api.php?action=query&titles="
        + urllib.parse.quote(title)
        + "&prop=imageinfo&iiprop=url|mime|size&format=json"
    )
    req = urllib.request.Request(api, headers=UA)
    data = json.loads(urllib.request.urlopen(req, timeout=60).read())
    pages = data["query"]["pages"]
    page = next(iter(pages.values()))
    return page["imageinfo"][0]["url"]


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


def clean_svg(raw: str) -> str:
    """Normalize NIH BioArt SVG for embedding (strip ns0, simplify)."""
    s = raw
    s = s.replace("ns0:", "").replace(":ns0", "")
    s = re.sub(r'xmlns:ns0="[^"]*"', "", s)
    # Drop external metadata bloat optionally keep short
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    # Recolor bone fills toward course bone palette
    s = s.replace("#c7aaa5", "#d4c4a0")  # cortical-ish
    s = s.replace("#fff3da", "#f8f2e5")  # highlight
    s = s.replace('fill: #fff;', "fill: #f8f2e5;")
    s = s.replace('fill="#fff"', 'fill="#f8f2e5"')
    # Unique-id safety: leave as-is; callers wrap in group with prefix transform
    return s


def main():
    for title, stem in FILES.items():
        try:
            url = image_url(title)
            print(title, "->", url)
            raw_path = OUT / f"{stem}_raw.svg"
            download(url, raw_path)
            cleaned = clean_svg(raw_path.read_text(encoding="utf-8", errors="replace"))
            (OUT / f"{stem}.svg").write_text(cleaned, encoding="utf-8")
            print("cleaned", stem)
        except Exception as e:
            print("FAIL", title, e)


if __name__ == "__main__":
    main()
