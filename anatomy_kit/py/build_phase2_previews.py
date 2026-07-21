"""Build Phase 2 hero preview page."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from anatomy_kit.py.bone_outline import hero
from anatomy_kit.py.style import SHARED_DEFS

OUT = Path(__file__).resolve().parents[1] / "previews"
OUT.mkdir(parents=True, exist_ok=True)

# SHARED_DEFS may lack b_bone in the string - style.py has it
from anatomy_kit.py.bone_outline import BONE_DEFS

html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<title>Phase 2 anatomy heroes</title>
<style>
body{{font:16px/1.5 Georgia,serif;max-width:56rem;margin:2rem auto;padding:0 1rem;color:#1a1a1a}}
h1{{font-size:1.4rem}} h2{{font-size:1.1rem;color:#7a1f1f;margin-top:1.8rem}}
.setupfig text{{paint-order:stroke;stroke:#fff;stroke-width:2.5px;stroke-linejoin:round}}
figcaption{{color:#555;font-style:italic;font-size:.92rem}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem}}
@media(max-width:700px){{.grid{{grid-template-columns:1fr}}}}
</style></head><body>
{SHARED_DEFS.replace('</defs>', BONE_DEFS + '</defs>')}
<h1>Phase 2 — Anatomy heroes</h1>
<p>Real (NIH BioArt, public domain) + geometry-driven outlines from adult dimensions.
Grok Build / Grok 4.5 (high). Plan: BIOLOGICAL_FIGURE_REALISM_PLAN.md</p>

<div class="grid">
<figure>
<svg class="setupfig" viewBox="0 0 240 420" width="100%" role="img" aria-label="NIH upper leg bones">
{hero('nih_upper_leg', max_width=180, x=30, y=10)}
</svg>
<figcaption><b>Real.</b> NIH BioArt upper leg bones (PD). Use for M2/M14 femur context.</figcaption>
</figure>

<figure>
<svg class="setupfig" viewBox="0 0 240 360" width="100%" role="img" aria-label="Geometry femur lateral">
{hero('femur_lateral', x=90, y_head=30, scale=1.1)}
</svg>
<figcaption><b>Geometry.</b> Lateral femur with neck-shaft ≈125°, head, GT, condyles (M2 torsion/fall).</figcaption>
</figure>

<figure>
<svg class="setupfig" viewBox="0 0 320 240" width="100%" role="img" aria-label="Hip joint">
{hero('hip_joint', cx=150, cy=110, scale=1.1)}
</svg>
<figcaption><b>Geometry.</b> Acetabulum + femoral head (M2–M4 hip congruence).</figcaption>
</figure>

<figure>
<svg class="setupfig" viewBox="0 0 280 280" width="100%" role="img" aria-label="Knee joint">
{hero('knee', cx=130, cy=100, scale=1.15, flexion_deg=15)}
</svg>
<figcaption><b>Geometry.</b> Sagittal knee contact (M3–M4).</figcaption>
</figure>

<figure>
<svg class="setupfig" viewBox="0 0 280 220" width="100%" role="img" aria-label="Shoulder complex">
{hero('shoulder', cx=130, cy=100, scale=1.05)}
</svg>
<figcaption><b>Geometry.</b> Shallow glenoid vs humeral head (M11 mobility/stability).</figcaption>
</figure>

<figure>
<svg class="setupfig" viewBox="0 0 240 360" width="100%" role="img" aria-label="NIH arm bones">
{hero('nih_arm_bones', max_width=160, x=40, y=10)}
</svg>
<figcaption><b>Real.</b> NIH BioArt arm bones (PD). Use for M11 chain context.</figcaption>
</figure>

<figure>
<svg class="setupfig" viewBox="0 0 280 200" width="100%" role="img" aria-label="Lumbar unit">
{hero('lumbar', cx=140, cy=30, scale=1.2, n=3)}
</svg>
<figcaption><b>Geometry.</b> Lumbar bodies + discs (M1/M7/M13 low back).</figcaption>
</figure>

<figure>
<svg class="setupfig" viewBox="0 0 280 160" width="100%" role="img" aria-label="Foot lateral">
{hero('foot_lateral', x=50, y=100, scale=1.2)}
</svg>
<figcaption><b>Geometry.</b> Lateral foot + medial arch (M6–M9).</figcaption>
</figure>
</div>
</body></html>
"""
(OUT / "04_phase2_heroes.html").write_text(html, encoding="utf-8")
print("wrote", OUT / "04_phase2_heroes.html")
