"""Plantar foot outline + COP path (never use b_head fill)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .style import arrow, kit_root


def _load_cop() -> dict[str, Any]:
    return json.loads((kit_root() / "data" / "cop_plantar_path.json").read_text(encoding="utf-8"))


def plantar_outline_path(
    x0: float,
    y0: float,
    length: float,
    *,
    mirror: bool = False,
) -> str:
    """Return SVG path d= for a plantigrade right foot (heel left, toes right).

    Anatomically simplified: heel pad, lateral flare, medial arch indentation,
    forefoot width, toe region — not a kidney bean.
    """
    L = length
    # Control points in unit foot coords (x heel→toe, y lateral positive down in SVG)
    # y=0 is medial edge-ish centerline offset
    pts = [
        (0.00, 0.08),  # heel medial
        (0.02, -0.10),
        (0.08, -0.16),  # heel lateral
        (0.18, -0.14),
        (0.32, -0.12),  # mid lateral
        (0.50, -0.14),
        (0.68, -0.16),  # fore lateral
        (0.82, -0.12),
        (0.94, -0.04),  # 5th toe
        (0.98, 0.04),
        (0.96, 0.12),  # hallux region
        (0.88, 0.16),
        (0.72, 0.14),
        (0.55, 0.10),  # medial arch (indent)
        (0.40, 0.06),
        (0.25, 0.04),
        (0.12, 0.06),
        (0.04, 0.10),
    ]
    sign = -1.0 if mirror else 1.0
    cmds = []
    for i, (u, v) in enumerate(pts):
        x = x0 + u * L
        y = y0 + sign * v * L
        cmds.append(("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}")
    cmds.append("Z")
    # Smooth via cubic-ish by using path with C - for simplicity use polyline path
    # Better: build smooth cubic. Use quadratic smoothing.
    d_parts = []
    coords = [(x0 + u * L, y0 + sign * v * L) for u, v in pts]
    d_parts.append(f"M{coords[0][0]:.1f},{coords[0][1]:.1f}")
    for i in range(1, len(coords)):
        d_parts.append(f"L{coords[i][0]:.1f},{coords[i][1]:.1f}")
    d_parts.append("Z")
    return "".join(d_parts)


def cop_points(
    x0: float,
    y0: float,
    length: float,
    *,
    mirror: bool = False,
) -> list[tuple[float, float, str | None]]:
    data = _load_cop()
    sign = -1.0 if mirror else 1.0
    # Map normalized: x heel→toe, y medial(0)→lateral(1) to our outline coords
    # Our outline y: negative = lateral, positive = medial (right foot, top=medial)
    out = []
    for p in data["cop_path"]:
        x = x0 + p["x"] * length
        # y: 0.5 centerline; >0.5 lateral -> negative y
        y = y0 + sign * (0.5 - p["y"]) * 0.28 * length
        out.append((x, y, p.get("label")))
    return out


def cop_polyline(x0: float, y0: float, length: float, **kw) -> str:
    pts = cop_points(x0, y0, length, **kw)
    pl = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in pts)
    return (
        f'<polyline points="{pl}" fill="none" stroke="#2a7d2a" '
        f'stroke-width="3" stroke-linecap="round"/>'
    )


def foot_plantar_svg(
    x0: float = 80.0,
    y0: float = 120.0,
    length: float = 280.0,
    *,
    show_cop: bool = True,
    show_grf: bool = True,
    show_labels: bool = True,
) -> str:
    """Full plantar figure content (paths + COP + optional GRF)."""
    d = plantar_outline_path(x0, y0, length)
    # Prefer solid plantar fill (works even if b_foot defs missing); optional gradient overlay.
    parts = [
        f'<path d="{d}" fill="#f3ece0" stroke="#b7a98c" stroke-width="1.7"/>',
    ]
    # Medial arch annotation tick
    arch_x = x0 + 0.45 * length
    if show_labels:
        parts.append(
            f'<text x="{arch_x:.1f}" y="{y0 - 0.12 * length:.1f}" font-size="10" '
            f'fill="#888" text-anchor="middle">medial arch</text>'
        )
        parts.append(
            f'<text x="{x0 + 0.06 * length:.1f}" y="{y0 + 0.22 * length:.1f}" '
            f'font-size="10" fill="#888">heel</text>'
        )
        parts.append(
            f'<text x="{x0 + 0.92 * length:.1f}" y="{y0 + 0.22 * length:.1f}" '
            f'font-size="10" fill="#888" text-anchor="end">toes</text>'
        )

    if show_cop:
        parts.append(cop_polyline(x0, y0, length))
        for x, y, lab in cop_points(x0, y0, length):
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#2a7d2a"/>')
            if lab and show_labels:
                parts.append(
                    f'<text x="{x:.1f}" y="{y - 12:.1f}" font-size="11" '
                    f'fill="#2a7d2a" text-anchor="middle">{lab}</text>'
                )
            if show_grf:
                # GRF up (negative y) with slight A-P tilt
                parts.append(arrow(x, y, x - 8, y - 70, color="#2a6ca8", marker="a_blu", sw=2.4))

    if show_grf and show_labels:
        parts.append(
            f'<text x="{x0 + 0.95 * length:.1f}" y="{y0 - 0.35 * length:.1f}" '
            f'font-size="12" fill="#2a6ca8">GRF rotates as COP advances</text>'
        )
    return "".join(parts)
