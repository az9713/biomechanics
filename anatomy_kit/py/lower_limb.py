"""Lower-limb chain (hip–knee–ankle–foot) from Winter lengths."""
from __future__ import annotations

import math
from typing import Any

from .body import segment_lengths_m, _load_segments
from .style import capsule, sphere


def lower_limb_group(
    hip: tuple[float, float],
    *,
    hip_flex_deg: float = 0.0,
    knee_flex_deg: float = 0.0,
    ankle_df_deg: float = 0.0,
    scale_px_per_m: float = 180.0,
    stature_m: float | None = None,
    side: str = "R",
) -> str:
    """Draw one lower limb. hip_flex + = thigh forward; knee +flex; ankle +DF."""
    L = segment_lengths_m(stature_m)
    data = _load_segments()
    s = scale_px_per_m
    th = lambda name, p1, p2: max(
        math.hypot(p2[0] - p1[0], p2[1] - p1[1]) * data["segments"][name]["thickness_frac_length"],
        math.hypot(p2[0] - p1[0], p2[1] - p1[1]) * 0.20,
    )
    # SVG angles: 90 = down
    th_a = math.radians(90.0 - hip_flex_deg)
    knee = (hip[0] + L["thigh"] * s * math.cos(th_a), hip[1] + L["thigh"] * s * math.sin(th_a))
    sk = math.radians(90.0 - hip_flex_deg + knee_flex_deg)
    ankle = (knee[0] + L["shank"] * s * math.cos(sk), knee[1] + L["shank"] * s * math.sin(sk))
    fk = math.radians(90.0 - hip_flex_deg + knee_flex_deg - 90.0 - ankle_df_deg)
    toe = (ankle[0] + L["foot"] * s * 0.7 * math.cos(fk), ankle[1] + L["foot"] * s * 0.12 * abs(math.sin(fk)))
    heel = (ankle[0] - L["foot"] * s * 0.25 * math.cos(fk), ankle[1])
    parts = [
        capsule(hip[0], hip[1], knee[0], knee[1], th("thigh", hip, knee)),
        capsule(knee[0], knee[1], ankle[0], ankle[1], th("shank", knee, ankle)),
        capsule(heel[0], heel[1], toe[0], toe[1], th("foot", heel, toe) * 0.75),
        sphere(hip[0], hip[1], max(5, 0.04 * s)),
        sphere(knee[0], knee[1], max(4.5, 0.035 * s)),
        sphere(ankle[0], ankle[1], max(4, 0.028 * s)),
    ]
    return f"<g>{''.join(parts)}</g>"
