# anatomy_kit

Data-driven **Tier-2** SVG factories for the Quantitative Human Musculoskeletal
Science course. Geometry comes from Winter anthropometry and teaching-grade
gait/COP tables — not freehand.

**Plan:** `../BIOLOGICAL_FIGURE_REALISM_PLAN.md`  
**Authored with:** Grok Build powered by Grok 4.5 (high)

## Layout

```
anatomy_kit/
  data/           # Winter segments, gait angles, COP path, sources
  py/             # body, foot_plantar, lower/upper limb, style
  tests/          # proportion gates
  previews/       # standalone HTML previews
  svg_paths/      # optional Real open-license path snippets (Phase 2)
  ATTRIBUTIONS.md
```

## Quick use

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(".").resolve()))  # repo root

from anatomy_kit.py.body import gait_pose_joints, body_group, standing_joints
from anatomy_kit.py.foot_plantar import foot_plantar_svg
from anatomy_kit.py.style import SHARED_DEFS

j = gait_pose_joints("midstance", origin=(200, 220), scale_px_per_m=160)
svg_body = body_group(j, show_com=True, show_arms=True)
foot = foot_plantar_svg(80, 120, 280)
```

## Rules

1. Never use `url(#b_head)` for feet — use `#f3ece0` / `url(#b_foot)`.
2. Head height / stature must stay in ~0.12–0.15 (`tests/test_proportions.py`).
3. Physics models (compass gait, SLIP) stay schematic — do not force kit bodies.
4. Real open-license heroes go in `svg_paths/` with `ATTRIBUTIONS.md` entries.
5. Prose stays in `moduleNN.html`; this package emits SVG only.

## Previews

```bash
python anatomy_kit/py/build_previews.py          # body kit (Phase 1)
python anatomy_kit/py/build_phase2_previews.py   # heroes (Phase 2)
# open anatomy_kit/previews/*.html
```

## Phase 2 heroes

```bash
python anatomy_kit/py/fetch_nih_heroes.py   # re-download NIH BioArt PD SVGs
python anatomy_kit/py/phase2_apply.py       # splice heroes into M2/M3/M7/M11
```

- **Real (PD):** `svg_paths/nih_upper_leg.svg`, `nih_arm_bones.svg`
- **Geometry:** `py/geometry_heroes.py` via `py/bone_outline.py`
- **Credits:** `ATTRIBUTIONS.md`

## Tests

```bash
python anatomy_kit/tests/test_proportions.py
```
