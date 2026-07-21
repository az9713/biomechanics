"""Durable tests: heroes and kit exports used by modules (real shipped functions)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from anatomy_kit.py.bone_outline import hero  # noqa: E402
from anatomy_kit.py.body import body_group, gait_pose_joints, proportion_report, standing_joints  # noqa: E402
from anatomy_kit.py.foot_plantar import foot_plantar_svg  # noqa: E402
from anatomy_kit.py.geometry_heroes import femur_lateral, hip_joint_coronal, knee_joint_sagittal  # noqa: E402


def test_nih_heroes_load():
    leg = hero("nih_upper_leg", max_width=100, x=0, y=0)
    arm = hero("nih_arm_bones", max_width=100, x=0, y=0)
    assert "<g" in leg and "scale(" in leg
    assert "<g" in arm and "scale(" in arm
    # files exist
    assert (ROOT / "anatomy_kit/svg_paths/nih_upper_leg.svg").is_file()
    assert (ROOT / "anatomy_kit/svg_paths/nih_arm_bones.svg").is_file()


def test_geometry_heroes_emit_landmarks():
    f = femur_lateral(show_labels=True)
    assert "neck-shaft" in f or "125" in f
    assert "url(#b_bone)" in f
    h = hip_joint_coronal(show_labels=True)
    assert "acetabulum" in h
    k = knee_joint_sagittal(show_labels=True)
    assert "contact" in k or "tibia" in k


def test_foot_never_uses_head_gradient():
    svg = foot_plantar_svg(40, 90, 200)
    assert "b_head" not in svg
    assert "#f3ece0" in svg or "b_foot" in svg


def test_body_proportions_within_gates():
    j = standing_joints(scale_px_per_m=180)
    rep = proportion_report(j)
    assert 0.12 <= rep["head_over_stature"] <= 0.15
    assert 0.48 <= rep["leg_over_stature"] <= 0.55
    svg = body_group(j)
    assert "url(#b_limb)" in svg
    g = gait_pose_joints("midstance")
    assert g["hip"][1] < g["ankle_R"][1]


def test_attributions_file_lists_nih():
    text = (ROOT / "anatomy_kit/ATTRIBUTIONS.md").read_text(encoding="utf-8")
    assert "nih_upper_leg" in text
    assert "Public domain" in text or "public domain" in text
    assert "nih_arm_bones" in text


if __name__ == "__main__":
    test_nih_heroes_load()
    test_geometry_heroes_emit_landmarks()
    test_foot_never_uses_head_gradient()
    test_body_proportions_within_gates()
    test_attributions_file_lists_nih()
    print("OK hero/export tests passed")
