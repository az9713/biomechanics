"""Build three sign-off preview HTML pages (standing, gait, reach)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from anatomy_kit.py.body import body_group, gait_pose_joints, standing_joints
from anatomy_kit.py.foot_plantar import foot_plantar_svg
from anatomy_kit.py.style import SHARED_DEFS
from anatomy_kit.py.upper_limb import upper_limb_reach

OUT = Path(__file__).resolve().parents[1] / "previews"
OUT.mkdir(parents=True, exist_ok=True)

CSS = """
body{font:16px/1.5 Georgia,serif;max-width:52rem;margin:2rem auto;padding:0 1rem;color:#1a1a1a}
h1{font-size:1.4rem} .setupfig text{paint-order:stroke;stroke:#fff;stroke-width:2.5px;stroke-linejoin:round}
.setupfig text[fill="#fff"]{stroke:none} figcaption{color:#555;font-style:italic}
"""


def page(title: str, svg_inner: str, vb: str, caption: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/><title>{title}</title>
<style>{CSS}</style></head><body>
{SHARED_DEFS}
<h1>{title}</h1>
<figure>
<svg class="setupfig" viewBox="{vb}" width="100%" role="img" aria-label="{title}">
{svg_inner}
</svg>
<figcaption>{caption}</figcaption>
</figure>
<p class="small">anatomy_kit preview — Winter proportions. Grok Build / Grok 4.5 (high).</p>
</body></html>
"""


def main():
    # 1 standing
    j = standing_joints(origin=(160, 240), scale_px_per_m=170)
    inner = (
        '<line x1="40" y1="240" x2="300" y2="240" stroke="#999"/>'
        + body_group(j, show_com=True, show_arms=True)
    )
    (OUT / "01_standing.html").write_text(
        page(
            "Preview 1 — Standing (M7 style)",
            inner,
            "0 0 340 280",
            "Upright adult with Winter segment ratios; COM marked. Head ≈ 13% stature.",
        ),
        encoding="utf-8",
    )

    # 2 gait strip
    parts = ['<line x1="30" y1="230" x2="700" y2="230" stroke="#999"/>']
    labels = [("ic", 90, "heel strike"), ("midstance", 260, "midstance"),
              ("toe_off", 430, "toe-off"), ("midswing", 600, "mid-swing")]
    for ev, x, lab in labels:
        jj = gait_pose_joints(ev, origin=(x, 230), scale_px_per_m=130)
        parts.append(body_group(jj, show_arms=True, show_com=(ev == "midstance")))
        parts.append(
            f'<text x="{x}" y="260" font-size="12" fill="#555" text-anchor="middle">{lab}</text>'
        )
    (OUT / "02_gait.html").write_text(
        page(
            "Preview 2 — Gait keyframes (M8 style)",
            "".join(parts),
            "0 0 720 290",
            "IC, midstance, toe-off, mid-swing from gait_angles_deg.json; reciprocal arm swing.",
        ),
        encoding="utf-8",
    )

    # 3 reach + foot
    reach = upper_limb_reach(origin_hip=(100, 210), shoulder_flex_deg=50, elbow_flex_deg=25)
    foot = foot_plantar_svg(320, 140, 220, show_cop=True, show_grf=True)
    inner3 = (
        '<line x1="40" y1="250" x2="280" y2="250" stroke="#999"/>'
        + reach
        + foot
    )
    (OUT / "03_reach_foot.html").write_text(
        page(
            "Preview 3 — Reach + plantar COP (M11 / M8 foot)",
            inner3,
            "0 40 560 280",
            "Upper limb Winter chain; plantar foot with heel→toe COP (not a bean; not b_head fill).",
        ),
        encoding="utf-8",
    )
    print("Wrote previews to", OUT)


if __name__ == "__main__":
    main()
