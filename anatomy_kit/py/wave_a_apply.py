"""
Wave A applicator: retrofit key figures in module07, module08, module11
with anatomy_kit bodies and plantar feet.

Run from repo root:
  python anatomy_kit/py/wave_a_apply.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from anatomy_kit.py.body import body_group, gait_pose_joints, standing_joints
from anatomy_kit.py.foot_plantar import foot_plantar_svg
from anatomy_kit.py.style import SHARED_DEFS, arrow
from anatomy_kit.py.upper_limb import upper_limb_reach

# Shared defs block body (inner <defs> only) for injection if missing b_foot
B_FOOT_GRAD = """<linearGradient id="b_foot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7f0e4"/><stop offset="0.5" stop-color="#e8ded0"/><stop offset="1" stop-color="#d4c4a8"/></linearGradient>"""


def ensure_b_foot(html: str) -> str:
    if 'id="b_foot"' in html or "id='b_foot'" in html:
        return html
    # Insert before closing </defs> of first defs block
    return html.replace("</defs>", B_FOOT_GRAD + "</defs>", 1)


def fig_m8_gait_cycle() -> str:
    """Motivation gait strip with Winter poses."""
    ground_y = 246
    parts = [
        f'<line x1="40" y1="{ground_y}" x2="680" y2="{ground_y}" stroke="#999" stroke-width="1.3"/>',
        '<path d="M110,154 C190,102 280,102 360,154 C440,206 530,206 610,154" fill="none" stroke="#2a6ca8" stroke-width="2.6"/>',
        '<text x="360" y="72" font-size="13" fill="#2a6ca8" text-anchor="middle">COM vaults, then redirects</text>',
    ]
    events = [
        ("ic", 100, "heel strike"),
        ("midstance", 260, "midstance"),
        ("toe_off", 420, "toe-off"),
        ("midswing", 560, "swing"),
    ]
    for ev, x, lab in events:
        j = gait_pose_joints(ev, origin=(x, ground_y), scale_px_per_m=115)
        parts.append(body_group(j, show_arms=True, show_com=(ev == "midstance"), show_feet=True))
        parts.append(
            f'<text x="{x}" y="{ground_y + 28}" font-size="11" fill="#555" text-anchor="middle">{lab}</text>'
        )
    # Next heel strike ghost
    j2 = gait_pose_joints("ic", origin=(620, ground_y), scale_px_per_m=115)
    parts.append(body_group(j2, show_arms=True, show_feet=True))
    parts.append(
        f'<text x="620" y="{ground_y + 28}" font-size="11" fill="#555" text-anchor="middle">next IC</text>'
    )
    inner = "".join(parts)
    return (
        f'<figure><svg class="setupfig" viewBox="0 20 720 290" width="100%" role="img" '
        f'aria-label="Gait cycle showing heel strike, midstance, toe off, swing, and next heel strike '
        f'with COM arc and Winter-proportion bodies.">{inner}</svg>'
        f"<figcaption>Walking is a controlled sequence of falls and catches. The COM rises over the "
        f"stance leg, drops toward the next foot, and must be redirected at the step-to-step transition. "
        f"Body proportions follow Winter segment ratios; poses use teaching-grade sagittal means.</figcaption></figure>"
    )


def fig_m8_cop() -> str:
    foot = foot_plantar_svg(90, 155, 300, show_cop=True, show_grf=True, show_labels=True)
    # COM annotation at right
    extra = (
        '<circle cx="520" cy="90" r="5" fill="#1a1a1a"/>'
        '<text x="532" y="94" font-size="11" fill="#1a1a1a">COM</text>'
        '<line x1="520" y1="100" x2="555" y2="135" stroke="#b0361f" stroke-width="2.5" marker-end="url(#a_red)"/>'
        '<text x="560" y="140" font-size="11" fill="#b0361f">COM acceleration</text>'
        '<line x1="40" y1="205" x2="640" y2="205" stroke="#999"/>'
    )
    return (
        f'<figure><svg class="setupfig" viewBox="10 40 660 200" width="100%" role="img" '
        f'aria-label="Plantar foot with COP path from heel to toe (lateral then medial), GRF vectors, '
        f'and COM acceleration labels.">{extra}{foot}</svg>'
        f"<figcaption>The COP is a moving anatomical point under the stance foot, not an abstract arrow "
        f"anchor. Typical progression runs heel → lateral midfoot → medial forefoot/toes; GRF orientation "
        f"rotates as the COP advances and changes moment arms about the ankle and knee.</figcaption></figure>"
    )


def fig_m8_arm_swing() -> str:
    j = gait_pose_joints("ic", origin=(150, 205), scale_px_per_m=140)
    # Force a clearer reciprocal pose: right leg forward already at IC
    body = body_group(j, show_arms=True, show_feet=True)
    extra = (
        '<line x1="40" y1="205" x2="300" y2="205" stroke="#999"/>'
        '<path d="M196,170 A20,20 0 0 1 196,204" fill="none" stroke="#2a7d2a" stroke-width="2" marker-end="url(#a_grn)"/>'
        '<text x="202" y="192" font-size="10" fill="#2a7d2a">L<tspan baseline-shift="sub" font-size="7">leg</tspan></text>'
        '<path d="M106,128 A18,18 0 0 0 106,92" fill="none" stroke="#b0361f" stroke-width="2" marker-end="url(#a_red)"/>'
        '<text x="100" y="112" font-size="10" fill="#b0361f" text-anchor="end">L<tspan baseline-shift="sub" font-size="7">arm</tspan></text>'
        '<text x="320" y="96" font-size="11" fill="#555">arm and leg</text>'
        '<text x="320" y="114" font-size="11" fill="#555">momenta oppose:</text>'
        '<text x="320" y="136" font-size="11" fill="#7a1f1f">L<tspan baseline-shift="sub" font-size="7">arm</tspan> + L<tspan baseline-shift="sub" font-size="7">leg</tspan> &#8776; 0</text>'
    )
    return (
        f'<figure><svg class="setupfig" viewBox="20 -25 400 260" width="100%" role="img" '
        f'aria-label="Side view of a Winter-proportion walker with reciprocal arm and leg swing; '
        f'angular momenta about the vertical axis oppose.">{extra}{body}</svg>'
        f"<figcaption>Arm swing is angular-momentum management. With the right leg forward and the "
        f"left arm forward, the arm's and leg's angular momenta about the vertical axis largely cancel, "
        f"reducing the yaw torque the trunk must supply.</figcaption></figure>"
    )


def fig_m8_inverted_pendulum_body() -> str:
    """Midstance body for inverted-pendulum panel (left side of combined fig if needed)."""
    j = gait_pose_joints("midstance", origin=(190, 238), scale_px_per_m=120)
    return body_group(j, show_arms=False, show_com=True, show_feet=True)


def fig_m7_standing() -> str:
    j = standing_joints(origin=(200, 250), scale_px_per_m=160)
    body = body_group(j, show_com=True, show_arms=True, show_feet=True)
    # BoS under feet
    extra = (
        '<line x1="40" y1="250" x2="380" y2="250" stroke="#999"/>'
        '<rect x="160" y="248" width="80" height="10" rx="3" fill="#e8ded0" stroke="#b7a98c"/>'
        '<text x="200" y="275" font-size="11" fill="#555" text-anchor="middle">base of support</text>'
        '<line x1="200" y1="200" x2="200" y2="248" stroke="#2a6ca8" stroke-width="1.5" stroke-dasharray="4 3"/>'
        '<text x="208" y="225" font-size="11" fill="#2a6ca8">vertical through COM</text>'
    )
    return (
        f'<g>{extra}{body}</g>'
    )


def fig_m11_reach() -> str:
    return upper_limb_reach(
        origin_hip=(130, 220),
        shoulder_flex_deg=55,
        elbow_flex_deg=20,
        scale_px_per_m=155,
    )


def replace_first_figure_matching(html: str, aria_substr: str, new_figure: str) -> tuple[str, bool]:
    """Replace first <figure>...</figure> whose content contains aria_substr."""
    pattern = re.compile(r"<figure>.*?</figure>", re.S)
    for m in pattern.finditer(html):
        block = m.group(0)
        if aria_substr in block:
            return html[: m.start()] + new_figure + html[m.end() :], True
    return html, False


def shrink_large_heads(html: str, max_r: float = 16.0) -> tuple[str, int]:
    """Cap head circle radii that use b_head fill (fixes cartoon heads)."""
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        tag = m.group(0)
        if "b_head" not in tag:
            return tag
        rm = re.search(r'\br="([\d.]+)"', tag)
        if not rm:
            return tag
        r = float(rm.group(1))
        if r <= max_r:
            return tag
        n += 1
        return tag.replace(f'r="{rm.group(1)}"', f'r="{max_r:.1f}"', 1)

    # Match circle tags (order of attributes varies)
    out = re.sub(r"<circle\b[^>]*>", repl, html)
    return out, n


def fix_head_fill_on_foot_paths(html: str) -> tuple[str, int]:
    """Replace b_head fill on paths that look like feet (aria or nearby COP)."""
    n = 0
    # Global safe fix used in M7/M8/M10 problem figs: path with b_head that is a foot blob
    # Only replace when path is immediately in a figure mentioning COP/foot/plantar in aria-label
    def fig_fix(m: re.Match) -> str:
        nonlocal n
        block = m.group(0)
        low = block.lower()
        if not any(k in low for k in ("cop", "foot", "plantar", "heel")):
            return block
        if "url(#b_head)" not in block:
            return block
        n_local = block.count('fill="url(#b_head)"')
        if n_local:
            n += n_local
            block = block.replace('fill="url(#b_head)"', 'fill="#f3ece0"')
        return block

    out = re.sub(r"<figure>.*?</figure>", fig_fix, html, flags=re.S)
    return out, n


def strip_decorative_mini_bodies_near_plots(html: str) -> tuple[str, int]:
    """Conservative: no automatic strip — return unchanged (manual per figure)."""
    return html, 0


def patch_module08(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    log = []
    html = ensure_b_foot(html)

    # Always refresh kit-owned section figures (idempotent content replace)
    html, ok = replace_first_figure_matching(
        html,
        "Gait cycle showing heel strike",
        fig_m8_gait_cycle(),
    )
    log.append(f"gait cycle replaced: {ok}")

    for key in (
        "Foot with COP path from heel to toe",
        "Plantar foot with COP path",
    ):
        html, ok = replace_first_figure_matching(html, key, fig_m8_cop())
        if ok:
            break
    log.append(f"COP foot replaced: {ok}")

    for key in (
        "Side view of a walker with the right leg swung forward",
        "Winter-proportion walker with reciprocal arm",
    ):
        html, ok = replace_first_figure_matching(html, key, fig_m8_arm_swing())
        if ok:
            break
    log.append(f"arm swing replaced: {ok}")

    # C4 foot figure
    c4 = (
        '<figure><svg class="setupfig" viewBox="20 0 370 160" width="100%" style="max-width:360px" '
        'role="img" aria-label="C4 figure: plantar foot with COP heel to toe and GRF arrows.">'
        + foot_plantar_svg(40, 90, 200, show_cop=True, show_grf=True, show_labels=True)
        + "</svg></figure>"
    )
    for key in ('aria-label="C4 figure"', "C4 figure: plantar"):
        html, ok = replace_first_figure_matching(html, key, c4)
        if ok:
            break
    log.append(f"C4 foot replaced: {ok}")

    html, n = shrink_large_heads(html, max_r=15.5)
    log.append(f"heads shrunk: {n}")
    html, n = fix_head_fill_on_foot_paths(html)
    log.append(f"foot head-fill fixed: {n}")

    path.write_text(html, encoding="utf-8")
    return log


def patch_module07(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    log = []
    html = ensure_b_foot(html)

    # Replace first body-ish standing figure if we can match a known aria
    # Build a standing BoS figure replacement for motivation-like figures
    standing_inner = fig_m7_standing()
    # Try common labels
    for key in (
        "Base of support",
        "base of support",
        "centre of mass",
        "center of mass",
        "inverted pendulum",
        "quiet standing",
        "Standing",
    ):
        # only replace if figure has tier2 body
        pattern = re.compile(r"<figure>.*?</figure>", re.S)
        replaced = False
        for m in pattern.finditer(html):
            block = m.group(0)
            if key.lower() in block.lower() and ("b_limb" in block or "b_head" in block):
                new_fig = (
                    f'<figure><svg class="setupfig" viewBox="40 10 360 300" width="100%" role="img" '
                    f'aria-label="Winter-proportion standing body with COM and base of support.">'
                    f"{standing_inner}</svg>"
                    f"<figcaption>Quiet standing on a finite base of support. Segment lengths follow "
                    f"Winter ratios; the COM projection must remain inside the BoS for static balance.</figcaption></figure>"
                )
                html = html[: m.start()] + new_fig + html[m.end() :]
                log.append(f"standing-like figure replaced (matched {key!r})")
                replaced = True
                break
        if replaced:
            break
    else:
        log.append("standing figure: no match (manual review)")

    html, n = shrink_large_heads(html, max_r=15.5)
    log.append(f"heads shrunk: {n}")
    html, n = fix_head_fill_on_foot_paths(html)
    log.append(f"foot head-fill fixed: {n}")

    path.write_text(html, encoding="utf-8")
    return log


def patch_module11(path: Path) -> list[str]:
    """Safe M11 patch: only replace the first early body figure, never mass-match 'arm'."""
    html = path.read_text(encoding="utf-8")
    log = []
    html = ensure_b_foot(html)

    # Idempotent: already kit-patched
    if "Winter-proportion arm reach" in html:
        log.append("reach figure already present (skip replace)")
    else:
        reach = fig_m11_reach()
        new_fig = (
            f'<figure><svg class="setupfig" viewBox="40 0 360 360" width="100%" role="img" '
            f'aria-label="Winter-proportion arm reach: shoulder, elbow, wrist chain with torso.">'
            f'<line x1="40" y1="250" x2="280" y2="250" stroke="#999"/>'
            f"{reach}"
            f'<text x="250" y="100" font-size="11" fill="#2a6ca8">hand</text>'
            f"</svg>"
            f"<figcaption>The arm as a serial chain with Winter segment lengths. Shoulder and elbow "
            f"angles place the hand; proportions match the anthropometric tables used for inverse dynamics."
            f"</figcaption></figure>"
        )
        pattern = re.compile(r"<figure>.*?</figure>", re.S)
        ok = False
        for m in pattern.finditer(html):
            block = m.group(0)
            if m.start() > len(html) * 0.25:
                break
            if "b_limb" in block or "b_head" in block:
                html = html[: m.start()] + new_fig + html[m.end() :]
                ok = True
                break
        log.append(f"reach figure replaced: {ok}")

    html, n = shrink_large_heads(html, max_r=15.0)
    log.append(f"heads shrunk: {n}")
    html, n = fix_head_fill_on_foot_paths(html)
    log.append(f"foot head-fill fixed: {n}")

    path.write_text(html, encoding="utf-8")
    return log


def main():
    reports = {}
    for name, fn in (
        ("module08.html", patch_module08),
        ("module07.html", patch_module07),
        ("module11.html", patch_module11),
    ):
        p = ROOT / name
        if not p.exists():
            reports[name] = ["MISSING"]
            continue
        reports[name] = fn(p)
    for k, v in reports.items():
        print(f"=== {k} ===")
        for line in v:
            print(" ", line)


if __name__ == "__main__":
    main()
