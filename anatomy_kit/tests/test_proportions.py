"""Proportion gates for anatomy_kit bodies (Winter bands)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent))

from anatomy_kit.py.body import (  # noqa: E402
    gait_pose_joints,
    proportion_report,
    standing_joints,
    segment_lengths_m,
)
from anatomy_kit.py import body as body_mod  # noqa: E402


def test_segment_length_fractions():
    L = segment_lengths_m(1.75)
    assert abs(L["thigh"] - 0.245 * 1.75) < 1e-9
    assert abs(L["shank"] - 0.246 * 1.75) < 1e-9
    data = json.loads((ROOT / "data" / "segments_winter.json").read_text(encoding="utf-8"))
    gates = data["proportion_gates"]
    leg = L["thigh"] + L["shank"] + L["foot"] * 0.3  # approximate hip-floor
    # hip-floor ≈ thigh+shank
    hip_floor = L["thigh"] + L["shank"]
    r = hip_floor / 1.75
    lo, hi = gates["leg_length_hip_to_floor_over_stature"]
    assert lo <= r <= hi, f"leg/stature {r}"
    ts = L["thigh"] / L["shank"]
    lo, hi = gates["thigh_over_shank"]
    assert lo <= ts <= hi, f"thigh/shank {ts}"


def test_standing_head_ratio():
    j = standing_joints(scale_px_per_m=180)
    rep = proportion_report(j)
    assert 0.12 <= rep["head_over_stature"] <= 0.15, rep
    assert 0.48 <= rep["leg_over_stature"] <= 0.55, rep
    assert 0.95 <= rep["thigh_over_shank"] <= 1.20, rep


def test_gait_poses_build():
    for ev in ("ic", "midstance", "toe_off", "midswing"):
        j = gait_pose_joints(ev, scale_px_per_m=160)
        rep = proportion_report(j)
        assert 0.11 <= rep["head_over_stature"] <= 0.16, (ev, rep)
        # SVG y increases downward: hip must be above ankle → hip.y < ankle.y
        assert j["hip"][1] < j["ankle_R"][1], (ev, j["hip"], j["ankle_R"])


def test_body_group_nonempty():
    j = standing_joints()
    svg = body_mod.body_group(j, show_com=True)
    assert "url(#b_limb)" in svg
    assert "url(#b_head)" in svg
    assert "COM" in svg


if __name__ == "__main__":
    test_segment_length_fractions()
    test_standing_head_ratio()
    test_gait_poses_build()
    test_body_group_nonempty()
    print("OK all proportion tests passed")
