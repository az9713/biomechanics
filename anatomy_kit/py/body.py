"""Posable whole-body SVG from Winter segment lengths + joint angles."""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from .style import capsule, head, kit_root, sphere


def _load_segments() -> dict[str, Any]:
    path = kit_root() / "data" / "segments_winter.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _load_gait() -> dict[str, Any]:
    path = kit_root() / "data" / "gait_angles_deg.json"
    return json.loads(path.read_text(encoding="utf-8"))


def segment_lengths_m(stature_m: float | None = None) -> dict[str, float]:
    data = _load_segments()
    H = stature_m if stature_m is not None else data["stature_m_default"]
    segs = data["segments"]
    return {k: segs[k]["length_frac_stature"] * H for k in segs}


def thickness_px(length_px: float, name: str, data: dict[str, Any] | None = None) -> float:
    data = data or _load_segments()
    frac = data["segments"][name]["thickness_frac_length"]
    # Enforce check_bodyprop band: thickness/length >= 0.18
    frac = max(frac, 0.20)
    return length_px * frac


def _rot(px: float, py: float, ang_deg: float) -> tuple[float, float]:
    a = math.radians(ang_deg)
    c, s = math.cos(a), math.sin(a)
    return px * c - py * s, px * s + py * c


def standing_joints(
    *,
    origin: tuple[float, float] = (150.0, 200.0),
    scale_px_per_m: float = 180.0,
    stature_m: float | None = None,
) -> dict[str, tuple[float, float]]:
    """Upright sagittal pose: origin at stance ankle on ground line."""
    L = segment_lengths_m(stature_m)
    ox, oy = origin
    # SVG y increases downward. Ground at oy. Up is negative y.
    ankle = (ox, oy)
    knee = (ox, oy - L["shank"] * scale_px_per_m)
    hip = (ox, knee[1] - L["thigh"] * scale_px_per_m)
    shoulder = (ox, hip[1] - L["pelvis_trunk"] * scale_px_per_m)
    head_c = (ox, shoulder[1] - L["head_neck"] * scale_px_per_m * 0.55)
    # Slight natural elbow flex; arms hang with mild flex
    elbow = (ox + 8, shoulder[1] + L["upper_arm"] * scale_px_per_m * 0.95)
    wrist = (ox + 10, elbow[1] + L["forearm"] * scale_px_per_m * 0.95)
    # Swing/contralateral limb slightly offset in x for visibility in sagittal
    ankle_L = (ox - 12, oy)
    knee_L = (ox - 10, oy - L["shank"] * scale_px_per_m)
    hip_L = hip  # same hip in sagittal schematic
    toe = (ox + L["foot"] * scale_px_per_m * 0.55, oy)
    heel = (ox - L["foot"] * scale_px_per_m * 0.25, oy)
    return {
        "ankle_R": ankle,
        "knee_R": knee,
        "hip": hip,
        "shoulder": shoulder,
        "head": head_c,
        "elbow_R": elbow,
        "wrist_R": wrist,
        "ankle_L": ankle_L,
        "knee_L": knee_L,
        "hip_L": hip_L,
        "toe_R": toe,
        "heel_R": heel,
        "scale": (scale_px_per_m, stature_m or _load_segments()["stature_m_default"]),
    }


def gait_pose_joints(
    event: str,
    *,
    origin: tuple[float, float] = (150.0, 200.0),
    scale_px_per_m: float = 160.0,
    stature_m: float | None = None,
    stance: str = "R",
) -> dict[str, tuple[float, float]]:
    """Sagittal gait pose from named event (ic, midstance, toe_off, midswing).

    Angles: hip +flex (thigh forward of vertical), knee +flex, ankle +dorsiflex.
    Stance foot fixed at origin. Swing leg uses mirrored/complementary angles.
    """
    gait = _load_gait()
    if event not in gait["events"]:
        raise KeyError(f"unknown gait event {event!r}; choose {list(gait['events'])}")
    e = gait["events"][event]
    L = segment_lengths_m(stature_m)
    ox, oy = origin
    s = scale_px_per_m

    def chain_from_hip(hip_xy, hip_deg, knee_deg, ankle_deg, foot_sign: float):
        # Vertical down is +90° in screen if 0 is +x; we use 0 = vertical down for leg
        # hip_deg flexion: thigh rotates forward (to +x when facing right)
        # From hip, knee direction: angle from downward vertical toward +x by hip_deg
        thigh_dir = 90.0 - hip_deg  # 90 = straight down in SVG? 
        # SVG: 0° along +x, 90° along +y (down). Downward vertical = 90°.
        # Hip flexion moves thigh forward (+x): angle becomes 90 - hip_deg
        th = math.radians(90.0 - hip_deg)
        knee = (
            hip_xy[0] + L["thigh"] * s * math.cos(th),
            hip_xy[1] + L["thigh"] * s * math.sin(th),
        )
        # Knee flexion bends shank back relative to thigh
        shank_heading = (90.0 - hip_deg) + knee_deg
        sk = math.radians(shank_heading)
        ankle = (
            knee[0] + L["shank"] * s * math.cos(sk),
            knee[1] + L["shank"] * s * math.sin(sk),
        )
        # Foot: roughly along ground; ankle PF negative -> toe down/back
        foot_heading = shank_heading - 90.0 - ankle_deg
        fk = math.radians(foot_heading)
        toe = (
            ankle[0] + L["foot"] * s * 0.7 * math.cos(fk) * foot_sign,
            ankle[1] + L["foot"] * s * 0.15 * abs(math.sin(fk)),
        )
        heel = (
            ankle[0] - L["foot"] * s * 0.25 * math.cos(fk) * foot_sign,
            ankle[1],
        )
        return knee, ankle, toe, heel

    # Place stance foot on ground; solve hip so stance ankle lands at origin
    # Build stance leg from temporary hip, then shift so ankle = origin
    hip0 = (ox, oy - (L["thigh"] + L["shank"]) * s)
    hip_a, knee_a, ankle_a = e["hip"], e["knee"], e["ankle"]
    if stance == "R":
        kR, aR, tR, hR = chain_from_hip(hip0, hip_a, knee_a, ankle_a, 1.0)
        # shift so aR -> origin
        dx, dy = ox - aR[0], oy - aR[1]
    else:
        kR, aR, tR, hR = chain_from_hip(hip0, hip_a, knee_a, ankle_a, 1.0)
        dx, dy = ox - aR[0], oy - aR[1]

    def sh(p):
        return (p[0] + dx, p[1] + dy)

    hip = sh(hip0)
    knee_R, ankle_R, toe_R, heel_R = sh(kR), sh(aR), sh(tR), sh(hR)

    # Swing leg: complementary angles (approximate opposite phase)
    # Simple teaching complement: swing hip more flexed at IC, etc.
    swing_map = {
        "ic": {"hip": -5, "knee": 5, "ankle": -5},
        "midstance": {"hip": 20, "knee": 50, "ankle": 0},
        "toe_off": {"hip": 25, "knee": 10, "ankle": 0},
        "midswing": {"hip": -5, "knee": 10, "ankle": 0},
    }
    sw = swing_map[event]
    kL, aL, tL, hL = chain_from_hip(hip, sw["hip"], sw["knee"], sw["ankle"], 1.0)
    # Keep swing foot above ground if needed
    if aL[1] > oy:
        lift = aL[1] - oy + 4
        kL = (kL[0], kL[1] - lift)
        aL = (aL[0], aL[1] - lift)
        tL = (tL[0], tL[1] - lift)
        hL = (hL[0], hL[1] - lift)

    shoulder = (hip[0], hip[1] - L["pelvis_trunk"] * s)
    head_c = (shoulder[0], shoulder[1] - L["head_neck"] * s * 0.55)

    # Reciprocal arms: right leg forward (hip flex) → left arm forward
    arm_flex = gait["contralateral_arm"]["shoulder_flex_with_contralateral_leg_flex_deg"]
    # Right arm: opposite to right hip flex
    r_shoulder_flex = -0.6 * hip_a  # degrees
    l_shoulder_flex = 0.6 * hip_a + arm_flex * 0.3
    # Upper arm: 0 = hanging down
    def arm(shoulder_xy, flex_deg, side: float):
        # flex positive = forward (+x)
        ang = math.radians(90.0 - flex_deg)
        elbow = (
            shoulder_xy[0] + L["upper_arm"] * s * 0.95 * math.cos(ang) * side,
            shoulder_xy[1] + L["upper_arm"] * s * 0.95 * math.sin(ang),
        )
        ang2 = math.radians(90.0 - flex_deg + 15)
        wrist = (
            elbow[0] + L["forearm"] * s * 0.9 * math.cos(ang2) * side,
            elbow[1] + L["forearm"] * s * 0.9 * math.sin(ang2),
        )
        return elbow, wrist

    elbow_R, wrist_R = arm(shoulder, r_shoulder_flex, 1.0)
    elbow_L, wrist_L = arm(shoulder, l_shoulder_flex, 1.0)
    # Offset left arm slightly for sagittal readability
    elbow_L = (elbow_L[0] - 6, elbow_L[1])
    wrist_L = (wrist_L[0] - 6, wrist_L[1])

    return {
        "ankle_R": ankle_R,
        "knee_R": knee_R,
        "hip": hip,
        "shoulder": shoulder,
        "head": head_c,
        "elbow_R": elbow_R,
        "wrist_R": wrist_R,
        "elbow_L": elbow_L,
        "wrist_L": wrist_L,
        "ankle_L": aL,
        "knee_L": kL,
        "toe_R": toe_R,
        "heel_R": heel_R,
        "toe_L": tL,
        "heel_L": hL,
        "scale": (s, stature_m or _load_segments()["stature_m_default"]),
    }


def body_group(
    joints: dict[str, tuple[float, float]],
    *,
    show_arms: bool = True,
    show_com: bool = False,
    show_feet: bool = True,
    id_prefix: str = "",
) -> str:
    """Return SVG group markup for a posable body (no outer <svg>)."""
    data = _load_segments()
    parts: list[str] = [f'<g id="{id_prefix}body">' if id_prefix else "<g>"]

    def th(name: str, p1, p2) -> float:
        length = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        # Enforce check_bodyprop band (thickness/length >= 0.18); short segments
        # (feet, hands) get a floor so they don't read as hairlines next to the head.
        frac = max(data["segments"][name]["thickness_frac_length"], 0.22)
        return max(length * frac, 8.0)

    hip = joints["hip"]
    shoulder = joints["shoulder"]
    head_c = joints["head"]
    knee_R = joints["knee_R"]
    ankle_R = joints["ankle_R"]
    knee_L = joints.get("knee_L", knee_R)
    ankle_L = joints.get("ankle_L", ankle_R)

    # Draw order: far limbs first (left), then right, trunk, head
    parts.append(capsule(hip[0], hip[1], knee_L[0], knee_L[1], th("thigh", hip, knee_L)))
    parts.append(capsule(knee_L[0], knee_L[1], ankle_L[0], ankle_L[1], th("shank", knee_L, ankle_L)))
    if show_feet and "toe_L" in joints:
        tL, hL = joints["toe_L"], joints.get("heel_L", ankle_L)
        parts.append(capsule(hL[0], hL[1], tL[0], tL[1], th("foot", hL, tL) * 0.7, grad="b_limb"))

    parts.append(capsule(hip[0], hip[1], knee_R[0], knee_R[1], th("thigh", hip, knee_R)))
    parts.append(capsule(knee_R[0], knee_R[1], ankle_R[0], ankle_R[1], th("shank", knee_R, ankle_R)))
    if show_feet and "toe_R" in joints:
        tR, hR = joints["toe_R"], joints.get("heel_R", ankle_R)
        parts.append(capsule(hR[0], hR[1], tR[0], tR[1], th("foot", hR, tR) * 0.7))

    parts.append(capsule(hip[0], hip[1], shoulder[0], shoulder[1], th("pelvis_trunk", hip, shoulder)))

    if show_arms:
        if "elbow_R" in joints and "wrist_R" in joints:
            eR, wR = joints["elbow_R"], joints["wrist_R"]
            parts.append(capsule(shoulder[0], shoulder[1], eR[0], eR[1], th("upper_arm", shoulder, eR)))
            parts.append(capsule(eR[0], eR[1], wR[0], wR[1], th("forearm", eR, wR)))
        if "elbow_L" in joints and "wrist_L" in joints:
            eL, wL = joints["elbow_L"], joints["wrist_L"]
            parts.append(capsule(shoulder[0], shoulder[1], eL[0], eL[1], th("upper_arm", shoulder, eL)))
            parts.append(capsule(eL[0], eL[1], wL[0], wL[1], th("forearm", eL, wL)))

    # Joint spheres
    for key, rscale in (
        ("hip", 0.045),
        ("knee_R", 0.035),
        ("knee_L", 0.035),
        ("ankle_R", 0.028),
        ("ankle_L", 0.028),
        ("shoulder", 0.038),
    ):
        if key not in joints:
            continue
        x, y = joints[key]
        # r relative to stature in px
        scale = joints.get("scale", (160, 1.75))
        s_px, H = scale if isinstance(scale, tuple) else (160, 1.75)
        r = max(4.0, rscale * H * s_px)
        parts.append(sphere(x, y, r))

    # Head radius from Winter head_neck length fraction
    scale = joints.get("scale", (160, 1.75))
    s_px, H = scale if isinstance(scale, tuple) else (160, 1.75)
    head_r = 0.5 * data["segments"]["head_neck"]["length_frac_stature"] * H * s_px
    # Ensure head/stature ~ 0.13: head height 2r ≈ 0.13 * H * s_px
    head_r = 0.065 * H * s_px
    parts.append(head(head_c[0], head_c[1], head_r))

    if show_com:
        # Approximate COM ~ mid trunk
        com = ((hip[0] + shoulder[0]) / 2, (hip[1] + shoulder[1]) / 2 + 8)
        parts.append(f'<circle cx="{com[0]:.1f}" cy="{com[1]:.1f}" r="4" fill="#1a1a1a"/>')
        parts.append(
            f'<text x="{com[0] + 8:.1f}" y="{com[1] + 4:.1f}" font-size="11" fill="#1a1a1a">COM</text>'
        )

    parts.append("</g>")
    return "".join(parts)


def proportion_report(
    joints: dict[str, tuple[float, float]], stature_m: float | None = None
) -> dict[str, float]:
    """Compute head/stature and leg ratios for QA."""
    data = _load_segments()
    H = stature_m or data["stature_m_default"]
    scale = joints.get("scale", (160, H))
    s_px = scale[0] if isinstance(scale, tuple) else 160
    stature_px = H * s_px
    head_r = 0.065 * H * s_px
    head_h = 2 * head_r
    hip = joints["hip"]
    ankle = joints["ankle_R"]
    knee = joints["knee_R"]
    leg = math.hypot(hip[0] - ankle[0], hip[1] - ankle[1])
    thigh = math.hypot(hip[0] - knee[0], hip[1] - knee[1])
    shank = math.hypot(knee[0] - ankle[0], knee[1] - ankle[1])
    return {
        "head_over_stature": head_h / stature_px,
        "leg_over_stature": leg / stature_px,
        "thigh_over_shank": thigh / max(shank, 1e-6),
        "stature_px": stature_px,
        "head_r": head_r,
    }
