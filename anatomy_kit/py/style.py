"""Shared Tier-2 SVG defs and primitive drawers."""
from __future__ import annotations

import math
from pathlib import Path

# Course palette (matches modules 7–11 shared defs)
SHARED_DEFS = """\
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="b_limb" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#c98a5e"/><stop offset="0.42" stop-color="#f3d7bd"/>
  <stop offset="0.62" stop-color="#e6bd99"/><stop offset="1" stop-color="#b5744b"/>
</linearGradient>
<linearGradient id="b_bone" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#a08b63"/><stop offset="0.42" stop-color="#f8f2e5"/>
  <stop offset="0.62" stop-color="#e6d9bc"/><stop offset="1" stop-color="#9c8760"/>
</linearGradient>
<linearGradient id="b_foot" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#f7f0e4"/><stop offset="0.5" stop-color="#e8ded0"/>
  <stop offset="1" stop-color="#d4c4a8"/>
</linearGradient>
<radialGradient id="b_sph" cx="38%" cy="34%" r="70%">
  <stop offset="0" stop-color="#fbe7d6"/><stop offset="0.6" stop-color="#e7bd99"/>
  <stop offset="1" stop-color="#c07f52"/>
</radialGradient>
<radialGradient id="b_head" cx="40%" cy="32%" r="72%">
  <stop offset="0" stop-color="#fbe7d6"/><stop offset="0.65" stop-color="#e4b891"/>
  <stop offset="1" stop-color="#b7784e"/>
</radialGradient>
<filter id="b_sh" x="-25%" y="-25%" width="150%" height="160%">
  <feDropShadow dx="1.5" dy="2.5" stdDeviation="2" flood-color="#000" flood-opacity="0.18"/>
</filter>
<marker id="a_red" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="9" refX="7" refY="3.5" orient="auto">
  <path d="M0,0 L8,3.5 L0,7 Z" fill="#b0361f"/>
</marker>
<marker id="a_blu" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="9" refX="7" refY="3.5" orient="auto">
  <path d="M0,0 L8,3.5 L0,7 Z" fill="#2a6ca8"/>
</marker>
<marker id="a_grn" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="9" refX="7" refY="3.5" orient="auto">
  <path d="M0,0 L8,3.5 L0,7 Z" fill="#2a7d2a"/>
</marker>
<marker id="a_gry" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="9" refX="7" refY="3.5" orient="auto">
  <path d="M0,0 L8,3.5 L0,7 Z" fill="#666"/>
</marker>
</defs></svg>"""


def capsule(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    w: float,
    *,
    grad: str = "b_limb",
    shadow: bool = True,
) -> str:
    """Shaded capsule bone/limb along segment (x1,y1)→(x2,y2)."""
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    L = math.hypot(x2 - x1, y2 - y1) + w * 0.12
    a = math.degrees(math.atan2(y2 - y1, x2 - x1))
    filt = ' filter="url(#b_sh)"' if shadow else ""
    return (
        f'<rect x="{cx - L / 2:.1f}" y="{cy - w / 2:.1f}" width="{L:.1f}" '
        f'height="{w:.1f}" rx="{w / 2:.1f}" fill="url(#{grad})"{filt} '
        f'transform="rotate({a:.1f} {cx:.1f} {cy:.1f})"/>'
    )


def sphere(cx: float, cy: float, r: float, *, grad: str = "b_sph", shadow: bool = True) -> str:
    filt = ' filter="url(#b_sh)"' if shadow else ""
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="url(#{grad})"{filt}/>'


def head(cx: float, cy: float, r: float) -> str:
    return sphere(cx, cy, r, grad="b_head", shadow=True)


def arrow(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    color: str = "#2a6ca8",
    marker: str = "a_blu",
    sw: float = 2.5,
) -> str:
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{sw}" marker-end="url(#{marker})"/>'
    )


def kit_root() -> Path:
    return Path(__file__).resolve().parents[1]
