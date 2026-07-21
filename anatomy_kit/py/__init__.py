"""Anatomy kit: data-driven Tier-2 SVG for the biomechanics course."""
from .body import body_group, gait_pose_joints, standing_joints
from .foot_plantar import foot_plantar_svg, cop_polyline
from .style import SHARED_DEFS, capsule, sphere, head

__all__ = [
    "SHARED_DEFS",
    "body_group",
    "gait_pose_joints",
    "standing_joints",
    "foot_plantar_svg",
    "cop_polyline",
    "capsule",
    "sphere",
    "head",
]
