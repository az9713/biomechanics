"""Load cleaned Real (NIH) SVGs and geometry heroes for embedding in modules."""
from __future__ import annotations

import re
from pathlib import Path

from . import geometry_heroes as gh
from .style import kit_root

SVG_DIR = kit_root() / "svg_paths"


def load_nih_svg(stem: str, *, max_width: float = 200.0, x: float = 0.0, y: float = 0.0) -> str:
    """Return a <g transform=...> wrapping a cleaned NIH SVG's inner content."""
    path = SVG_DIR / f"{stem}.svg"
    if not path.exists():
        path = SVG_DIR / f"{stem}_raw.svg"
    if not path.exists():
        raise FileNotFoundError(path)
    raw = path.read_text(encoding="utf-8", errors="replace")
    # Extract viewBox
    vb = re.search(r'viewBox=["\']([^"\']+)["\']', raw)
    if vb:
        parts = [float(x) for x in vb.group(1).replace(",", " ").split()]
        _, _, w, h = parts if len(parts) == 4 else (0, 0, 200, 400)
    else:
        w, h = 200.0, 400.0
    scale = max_width / w
    # Inner content between > of root svg and </svg>
    inner = re.sub(r"^.*?<svg[^>]*>", "", raw, count=1, flags=re.S)
    inner = re.sub(r"</svg>\s*$", "", inner, flags=re.S)
    # Strip nested style that may conflict? keep it
    # Prefix ids to avoid collisions
    prefix = stem.replace("-", "_") + "_"
    inner = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{prefix}{m.group(1)}"', inner)
    inner = re.sub(r"url\(#([^)]+)\)", lambda m: f"url(#{prefix}{m.group(1)})", inner)
    return (
        f'<g transform="translate({x:.1f},{y:.1f}) scale({scale:.4f})">{inner}</g>'
    )


def hero(
    name: str,
    **kwargs,
) -> str:
    """Dispatch named heroes.

    Real (NIH PD): nih_upper_leg, nih_arm_bones
    Geometry: femur_lateral, hip_joint, knee, shoulder, lumbar, foot_lateral
    """
    if name == "nih_upper_leg":
        return load_nih_svg(
            "nih_upper_leg",
            max_width=kwargs.get("max_width", 160.0),
            x=kwargs.get("x", 40.0),
            y=kwargs.get("y", 20.0),
        )
    if name == "nih_arm_bones":
        return load_nih_svg(
            "nih_arm_bones",
            max_width=kwargs.get("max_width", 140.0),
            x=kwargs.get("x", 40.0),
            y=kwargs.get("y", 20.0),
        )
    if name == "femur_lateral":
        return gh.femur_lateral(**{k: v for k, v in kwargs.items() if k in (
            "x", "y_head", "scale", "show_labels", "neck_shaft_deg"
        )})
    if name == "hip_joint":
        return gh.hip_joint_coronal(**{k: v for k, v in kwargs.items() if k in (
            "cx", "cy", "scale", "show_labels"
        )})
    if name == "knee":
        return gh.knee_joint_sagittal(**{k: v for k, v in kwargs.items() if k in (
            "cx", "cy", "scale", "flexion_deg", "show_labels"
        )})
    if name == "shoulder":
        return gh.shoulder_complex(**{k: v for k, v in kwargs.items() if k in (
            "cx", "cy", "scale", "show_labels"
        )})
    if name == "lumbar":
        return gh.lumbar_unit(**{k: v for k, v in kwargs.items() if k in (
            "cx", "cy", "scale", "n", "show_labels"
        )})
    if name == "foot_lateral":
        return gh.foot_lateral(**{k: v for k, v in kwargs.items() if k in (
            "x", "y", "scale", "show_labels"
        )})
    raise KeyError(name)


# Shared defs fragment for pages that only have b_limb (add bone)
BONE_DEFS = """
<linearGradient id="b_bone" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#a08b63"/><stop offset="0.42" stop-color="#f8f2e5"/>
  <stop offset="0.62" stop-color="#e6d9bc"/><stop offset="1" stop-color="#9c8760"/>
</linearGradient>
"""
