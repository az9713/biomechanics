"""Upper-limb chain for reach/wave figures (Winter proportions)."""
from __future__ import annotations

import math

from .body import segment_lengths_m, _load_segments
from .style import capsule, head, sphere


def upper_limb_reach(
    *,
    origin_hip: tuple[float, float] = (120.0, 200.0),
    shoulder_flex_deg: float = 40.0,
    elbow_flex_deg: float = 30.0,
    scale_px_per_m: float = 170.0,
    stature_m: float | None = None,
    show_torso: bool = True,
) -> str:
    """Side-view torso + one arm reaching forward (+x)."""
    L = segment_lengths_m(stature_m)
    data = _load_segments()
    s = scale_px_per_m
    H = stature_m or data["stature_m_default"]

    def th(name, p1, p2):
        length = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        return max(length * data["segments"][name]["thickness_frac_length"], length * 0.20)

    hip = origin_hip
    shoulder = (hip[0], hip[1] - L["pelvis_trunk"] * s)
    head_c = (shoulder[0], shoulder[1] - 0.065 * H * s)
    # Arm: flex from hanging
    ang = math.radians(90.0 - shoulder_flex_deg)
    elbow = (
        shoulder[0] + L["upper_arm"] * s * math.cos(ang),
        shoulder[1] + L["upper_arm"] * s * math.sin(ang),
    )
    ang2 = math.radians(90.0 - shoulder_flex_deg + elbow_flex_deg)
    wrist = (
        elbow[0] + L["forearm"] * s * math.cos(ang2),
        elbow[1] + L["forearm"] * s * math.sin(ang2),
    )
    hand = (
        wrist[0] + L["hand"] * s * 0.5 * math.cos(ang2),
        wrist[1] + L["hand"] * s * 0.5 * math.sin(ang2),
    )
    # Simple stance legs for context
    knee = (hip[0] + 5, hip[1] + L["thigh"] * s * 0.98)
    ankle = (knee[0] + 3, knee[1] + L["shank"] * s * 0.98)

    parts = []
    if show_torso:
        parts.append(capsule(hip[0], hip[1], knee[0], knee[1], th("thigh", hip, knee)))
        parts.append(capsule(knee[0], knee[1], ankle[0], ankle[1], th("shank", knee, ankle)))
        parts.append(capsule(hip[0], hip[1], shoulder[0], shoulder[1], th("pelvis_trunk", hip, shoulder)))
        parts.append(head(head_c[0], head_c[1], 0.065 * H * s))
        parts.append(sphere(hip[0], hip[1], max(5, 0.04 * s)))
    parts += [
        capsule(shoulder[0], shoulder[1], elbow[0], elbow[1], th("upper_arm", shoulder, elbow)),
        capsule(elbow[0], elbow[1], wrist[0], wrist[1], th("forearm", elbow, wrist)),
        capsule(wrist[0], wrist[1], hand[0], hand[1], th("hand", wrist, hand) * 0.9),
        sphere(shoulder[0], shoulder[1], max(5, 0.038 * s)),
        sphere(elbow[0], elbow[1], max(4.5, 0.032 * s)),
        sphere(wrist[0], wrist[1], max(4, 0.026 * s)),
    ]
    return f"<g>{''.join(parts)}</g>"
