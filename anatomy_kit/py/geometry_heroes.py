"""
Parameter-driven anatomic hero outlines (Tier-3 from biological dimensions).

These are NOT freehand cartoons and NOT claimed as open-license traces.
They are constructed from published typical adult dimensions (mm), so
landmarks (neck-shaft angle, head diameter, condyles) sit at correct
relative positions for teaching. When a public-domain NIH path exists,
prefer that (see svg_paths/nih_*.svg).
"""
from __future__ import annotations

import math
from typing import Iterable


def _path(cmds: Iterable[str]) -> str:
    return "".join(cmds)


def femur_lateral(
    *,
    x: float = 120.0,
    y_head: float = 40.0,
    scale: float = 1.0,
    show_labels: bool = True,
    neck_shaft_deg: float = 125.0,
) -> str:
    """Lateral/oblique teaching femur with true-ish neck-shaft angle.

    Dimensions (adult typical, mm scaled to px by scale):
      head diameter ~46 mm, neck length ~30 mm, shaft length ~400 mm,
      shaft mid width ~27 mm, neck-shaft angle ~125° (anatomical).
    """
    # map mm → px (scale=1 → 0.55 px/mm so full femur ~250 px)
    k = 0.55 * scale
    head_r = 23 * k
    neck_L = 32 * k
    shaft_L = 380 * k
    shaft_w = 14 * k
    # Head center
    hx, hy = x, y_head + head_r
    # Neck axis: from head center downward-lateral at (180-neck_shaft) from vertical
    # Anatomical neck-shaft: shaft axis vs neck axis ≈ 125°.
    # Shaft vertical down; neck goes up-medial at (180-125)=55° from shaft...
    # From head, neck goes toward greater trochanter / shaft junction.
    ang = math.radians(90 + (180 - neck_shaft_deg) / 2)  # teaching lateral view
    # Simpler construction for lateral teaching view:
    # head at top-leftish, neck diagonal, shaft vertical
    neck_ang = math.radians(55)  # from horizontal down-right to shaft
    jx = hx + neck_L * math.cos(neck_ang)
    jy = hy + neck_L * math.sin(neck_ang)
    # Greater trochanter bump
    gt_x, gt_y = jx + 12 * k, jy - 6 * k
    # Shaft bottom (distal)
    sx, sy = jx + 4 * k, jy + shaft_L
    # Condyle bulb
    cond_r = 16 * k

    # Build outline as filled path approximating lateral silhouette
    # Left (posterior) and right (anterior) shaft edges
    half = shaft_w
    d = (
        f"M{hx - head_r * 0.2:.1f},{hy:.1f} "
        f"A{head_r:.1f},{head_r:.1f} 0 1 1 {hx + head_r * 0.6:.1f},{hy + head_r * 0.3:.1f} "
        f"L{jx + half:.1f},{jy:.1f} "
        f"L{sx + half * 1.1:.1f},{sy - cond_r:.1f} "
        f"A{cond_r:.1f},{cond_r * 0.85:.1f} 0 0 1 {sx - half * 1.3:.1f},{sy - cond_r:.1f} "
        f"L{jx - half:.1f},{jy + 8 * k:.1f} "
        f"L{gt_x - 8 * k:.1f},{gt_y + 10 * k:.1f} "
        f"L{gt_x - 4 * k:.1f},{gt_y - 4 * k:.1f} "
        f"L{hx - head_r * 0.3:.1f},{hy + head_r * 0.4:.1f} Z"
    )
    parts = [
        f'<path d="{d}" fill="url(#b_bone)" stroke="#8a7350" stroke-width="1.4" filter="url(#b_sh)"/>',
        f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{head_r * 0.35:.1f}" fill="url(#b_sph)" opacity="0.5"/>',
    ]
    # Neck-shaft angle annotation
    parts.append(
        f'<line x1="{hx:.1f}" y1="{hy:.1f}" x2="{jx:.1f}" y2="{jy:.1f}" '
        f'stroke="#2a6ca8" stroke-width="1.5" stroke-dasharray="3 2"/>'
    )
    parts.append(
        f'<line x1="{jx:.1f}" y1="{jy:.1f}" x2="{sx:.1f}" y2="{sy - cond_r:.1f}" '
        f'stroke="#2a6ca8" stroke-width="1.5" stroke-dasharray="3 2"/>'
    )
    if show_labels:
        parts.append(
            f'<text x="{hx - head_r - 4:.1f}" y="{hy:.1f}" font-size="11" fill="#555" text-anchor="end">head</text>'
        )
        parts.append(
            f'<text x="{jx + half + 10:.1f}" y="{jy - 4:.1f}" font-size="11" fill="#2a6ca8">neck-shaft ~{neck_shaft_deg:.0f}°</text>'
        )
        parts.append(
            f'<text x="{gt_x + 8:.1f}" y="{gt_y:.1f}" font-size="10" fill="#555">GT</text>'
        )
        parts.append(
            f'<text x="{sx + cond_r + 6:.1f}" y="{sy - cond_r:.1f}" font-size="11" fill="#555">condyles</text>'
        )
        parts.append(
            f'<text x="{jx + half + 8:.1f}" y="{(jy + sy) / 2:.1f}" font-size="11" fill="#555">shaft</text>'
        )
    return f"<g>{''.join(parts)}</g>"


def hip_joint_coronal(
    *,
    cx: float = 160.0,
    cy: float = 120.0,
    scale: float = 1.0,
    show_labels: bool = True,
) -> str:
    """Coronal hip: acetabulum (deep socket) + femoral head."""
    k = scale
    acet_r = 42 * k
    head_r = 28 * k
    # Acetabulum as thick arc (socket)
    # Femoral head as sphere inside
    hx, hy = cx + 6 * k, cy + 10 * k
    parts = [
        # ilium block simplified
        f'<path d="M{cx - 70 * k:.1f},{cy - 50 * k:.1f} Q{cx - 20 * k:.1f},{cy - 70 * k:.1f} {cx + 40 * k:.1f},{cy - 40 * k:.1f} '
        f'L{cx + 50 * k:.1f},{cy + 10 * k:.1f} L{cx - 10 * k:.1f},{cy + 20 * k:.1f} Z" '
        f'fill="url(#b_bone)" stroke="#8a7350" stroke-width="1.3" filter="url(#b_sh)"/>',
        # acetabulum cavity (darker)
        f'<path d="M{cx - acet_r * 0.9:.1f},{cy - 5 * k:.1f} '
        f'A{acet_r:.1f},{acet_r:.1f} 0 0 0 {cx + acet_r * 0.5:.1f},{cy + acet_r * 0.7:.1f}" '
        f'fill="none" stroke="#7a1f1f" stroke-width="4" stroke-linecap="round"/>',
        f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{head_r:.1f}" fill="url(#b_sph)" stroke="#8a7350" stroke-width="1.2" filter="url(#b_sh)"/>',
        # neck stump
        f'<rect x="{hx + head_r * 0.3:.1f}" y="{hy - 8 * k:.1f}" width="{50 * k:.1f}" height="{16 * k:.1f}" '
        f'rx="{8 * k:.1f}" fill="url(#b_bone)" transform="rotate(35 {hx + head_r * 0.3:.1f} {hy:.1f})"/>',
    ]
    if show_labels:
        parts.append(
            f'<text x="{cx - 60 * k:.1f}" y="{cy - 55 * k:.1f}" font-size="11" fill="#555">ilium</text>'
        )
        parts.append(
            f'<text x="{cx - acet_r - 8:.1f}" y="{cy + 30 * k:.1f}" font-size="11" fill="#7a1f1f" text-anchor="end">acetabulum</text>'
        )
        parts.append(
            f'<text x="{hx:.1f}" y="{hy + head_r + 16:.1f}" font-size="11" fill="#555" text-anchor="middle">femoral head</text>'
        )
    return f"<g>{''.join(parts)}</g>"


def knee_joint_sagittal(
    *,
    cx: float = 160.0,
    cy: float = 130.0,
    scale: float = 1.0,
    flexion_deg: float = 20.0,
    show_labels: bool = True,
) -> str:
    """Sagittal knee: femoral condyles, tibial plateau, patella optional."""
    k = scale
    # Femur shaft up
    f_ang = math.radians(-90 + flexion_deg * 0.15)
    t_ang = math.radians(90 + flexion_deg)
    parts = []
    # femoral condyle (ellipse)
    parts.append(
        f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{28 * k:.1f}" ry="{32 * k:.1f}" '
        f'fill="url(#b_sph)" stroke="#8a7350" stroke-width="1.3" filter="url(#b_sh)"/>'
    )
    # femur shaft
    fx2 = cx + 90 * k * math.cos(math.radians(-90))
    fy2 = cy + 90 * k * math.sin(math.radians(-90))
    parts.append(
        f'<rect x="{(cx + fx2) / 2 - 45 * k:.1f}" y="{(cy + fy2) / 2 - 10 * k:.1f}" '
        f'width="{90 * k:.1f}" height="{20 * k:.1f}" rx="{10 * k:.1f}" fill="url(#b_bone)" '
        f'transform="rotate(-90 {cx:.1f} {cy - 45 * k:.1f})" filter="url(#b_sh)"/>'
    )
    # tibial plateau
    tx = cx + 8 * k * math.sin(math.radians(flexion_deg))
    ty = cy + 34 * k
    parts.append(
        f'<rect x="{tx - 22 * k:.1f}" y="{ty:.1f}" width="{44 * k:.1f}" height="{14 * k:.1f}" '
        f'rx="4" fill="url(#b_bone)" stroke="#8a7350" stroke-width="1.1"/>'
    )
    # tibia shaft
    parts.append(
        f'<rect x="{tx - 11 * k:.1f}" y="{ty + 10 * k:.1f}" width="{22 * k:.1f}" height="{85 * k:.1f}" '
        f'rx="{11 * k:.1f}" fill="url(#b_bone)" filter="url(#b_sh)"/>'
    )
    # patella
    px, py = cx + 30 * k, cy - 5 * k
    parts.append(
        f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{9 * k:.1f}" ry="{12 * k:.1f}" '
        f'fill="url(#b_sph)" stroke="#8a7350" stroke-width="1"/>'
    )
    # contact highlight
    parts.append(
        f'<line x1="{cx - 18 * k:.1f}" y1="{cy + 28 * k:.1f}" x2="{cx + 18 * k:.1f}" y2="{cy + 28 * k:.1f}" '
        f'stroke="#7a1f1f" stroke-width="2.5"/>'
    )
    if show_labels:
        parts.append(
            f'<text x="{cx - 40 * k:.1f}" y="{cy - 50 * k:.1f}" font-size="11" fill="#555">femur</text>'
        )
        parts.append(
            f'<text x="{tx + 28 * k:.1f}" y="{ty + 60 * k:.1f}" font-size="11" fill="#555">tibia</text>'
        )
        parts.append(
            f'<text x="{px + 14 * k:.1f}" y="{py:.1f}" font-size="10" fill="#555">patella</text>'
        )
        parts.append(
            f'<text x="{cx:.1f}" y="{cy + 48 * k:.1f}" font-size="10" fill="#7a1f1f" text-anchor="middle">contact</text>'
        )
    return f"<g>{''.join(parts)}</g>"


def shoulder_complex(
    *,
    cx: float = 140.0,
    cy: float = 120.0,
    scale: float = 1.0,
    show_labels: bool = True,
) -> str:
    """Glenoid (shallow) + humeral head + scapula blade + clavicle stub."""
    k = scale
    parts = []
    # scapula blade
    parts.append(
        f'<path d="M{cx - 10 * k:.1f},{cy - 10 * k:.1f} L{cx - 90 * k:.1f},{cy + 20 * k:.1f} '
        f'L{cx - 70 * k:.1f},{cy + 70 * k:.1f} L{cx + 5 * k:.1f},{cy + 30 * k:.1f} Z" '
        f'fill="url(#b_bone)" stroke="#8a7350" stroke-width="1.2" filter="url(#b_sh)"/>'
    )
    # glenoid (shallow arc)
    parts.append(
        f'<path d="M{cx - 8 * k:.1f},{cy - 22 * k:.1f} '
        f'A{24 * k:.1f},{28 * k:.1f} 0 0 1 {cx - 8 * k:.1f},{cy + 28 * k:.1f}" '
        f'fill="none" stroke="#7a1f1f" stroke-width="3.5" stroke-linecap="round"/>'
    )
    # humeral head
    hx, hy = cx + 22 * k, cy + 2 * k
    parts.append(
        f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{26 * k:.1f}" fill="url(#b_sph)" '
        f'stroke="#8a7350" stroke-width="1.2" filter="url(#b_sh)"/>'
    )
    # humerus shaft
    parts.append(
        f'<rect x="{hx + 8 * k:.1f}" y="{hy - 9 * k:.1f}" width="{70 * k:.1f}" height="{18 * k:.1f}" '
        f'rx="9" fill="url(#b_bone)" transform="rotate(25 {hx:.1f} {hy:.1f})" filter="url(#b_sh)"/>'
    )
    # clavicle
    parts.append(
        f'<rect x="{cx - 20 * k:.1f}" y="{cy - 48 * k:.1f}" width="{85 * k:.1f}" height="{10 * k:.1f}" '
        f'rx="5" fill="url(#b_bone)" transform="rotate(-8 {cx:.1f} {cy - 43 * k:.1f})"/>'
    )
    if show_labels:
        parts.append(
            f'<text x="{cx - 85 * k:.1f}" y="{cy + 50 * k:.1f}" font-size="11" fill="#555">scapula</text>'
        )
        parts.append(
            f'<text x="{cx - 30 * k:.1f}" y="{cy - 28 * k:.1f}" font-size="11" fill="#7a1f1f">glenoid (shallow)</text>'
        )
        parts.append(
            f'<text x="{hx + 40 * k:.1f}" y="{hy + 40 * k:.1f}" font-size="11" fill="#555">humerus</text>'
        )
        parts.append(
            f'<text x="{cx + 30 * k:.1f}" y="{cy - 55 * k:.1f}" font-size="11" fill="#555">clavicle</text>'
        )
    return f"<g>{''.join(parts)}</g>"


def lumbar_unit(
    *,
    cx: float = 160.0,
    cy: float = 80.0,
    scale: float = 1.0,
    n: int = 3,
    show_labels: bool = True,
) -> str:
    """Stacked lumbar vertebrae + discs (simplified but proportional)."""
    k = scale
    parts = []
    body_h, body_w, disc_h = 28 * k, 48 * k, 8 * k
    y = cy
    for i in range(n):
        # vertebral body
        parts.append(
            f'<rect x="{cx - body_w / 2:.1f}" y="{y:.1f}" width="{body_w:.1f}" height="{body_h:.1f}" '
            f'rx="4" fill="url(#b_bone)" stroke="#8a7350" stroke-width="1.1" filter="url(#b_sh)"/>'
        )
        # spinous process stub
        parts.append(
            f'<rect x="{cx + body_w / 2 - 2 * k:.1f}" y="{y + 8 * k:.1f}" width="{18 * k:.1f}" height="{10 * k:.1f}" '
            f'rx="3" fill="url(#b_bone)" stroke="#8a7350" stroke-width="0.8"/>'
        )
        y += body_h
        if i < n - 1:
            parts.append(
                f'<rect x="{cx - body_w / 2 + 4 * k:.1f}" y="{y:.1f}" width="{body_w - 8 * k:.1f}" height="{disc_h:.1f}" '
                f'rx="2" fill="#c9b89a" stroke="#a89070" stroke-width="0.8"/>'
            )
            y += disc_h
    if show_labels:
        parts.append(
            f'<text x="{cx - body_w / 2 - 8:.1f}" y="{cy + body_h:.1f}" font-size="11" fill="#555" text-anchor="end">vertebral body</text>'
        )
        parts.append(
            f'<text x="{cx - body_w / 2 - 8:.1f}" y="{cy + body_h + disc_h + 4:.1f}" font-size="11" fill="#8a7350" text-anchor="end">disc</text>'
        )
    return f"<g>{''.join(parts)}</g>"


def foot_lateral(
    *,
    x: float = 80.0,
    y: float = 140.0,
    scale: float = 1.0,
    show_labels: bool = True,
) -> str:
    """Lateral foot: calcaneus, midfoot arch, metatarsals, toes."""
    k = scale
    # outline path
    d = (
        f"M{x:.1f},{y:.1f} "
        f"C{x - 10 * k:.1f},{y - 25 * k:.1f} {x + 15 * k:.1f},{y - 45 * k:.1f} {x + 45 * k:.1f},{y - 40 * k:.1f} "
        f"C{x + 80 * k:.1f},{y - 35 * k:.1f} {x + 120 * k:.1f},{y - 20 * k:.1f} {x + 150 * k:.1f},{y - 8 * k:.1f} "
        f"C{x + 165 * k:.1f},{y - 4 * k:.1f} {x + 175 * k:.1f},{y + 2 * k:.1f} {x + 170 * k:.1f},{y + 12 * k:.1f} "
        f"L{x + 40 * k:.1f},{y + 18 * k:.1f} "
        f"C{x + 20 * k:.1f},{y + 20 * k:.1f} {x + 5 * k:.1f},{y + 12 * k:.1f} {x:.1f},{y:.1f} Z"
    )
    parts = [
        f'<path d="{d}" fill="url(#b_bone)" stroke="#8a7350" stroke-width="1.3" filter="url(#b_sh)"/>',
        # arch indicator
        f'<path d="M{x + 50 * k:.1f},{y + 8 * k:.1f} Q{x + 90 * k:.1f},{y - 18 * k:.1f} {x + 130 * k:.1f},{y + 4 * k:.1f}" '
        f'fill="none" stroke="#2a6ca8" stroke-width="1.5" stroke-dasharray="3 2"/>',
    ]
    if show_labels:
        parts.append(
            f'<text x="{x + 15 * k:.1f}" y="{y - 30 * k:.1f}" font-size="11" fill="#555">calcaneus</text>'
        )
        parts.append(
            f'<text x="{x + 85 * k:.1f}" y="{y - 28 * k:.1f}" font-size="11" fill="#2a6ca8">medial arch</text>'
        )
        parts.append(
            f'<text x="{x + 145 * k:.1f}" y="{y - 18 * k:.1f}" font-size="11" fill="#555">toes</text>'
        )
    return f"<g>{''.join(parts)}</g>"
