"""
Phase 2: insert anatomy heroes into M2, M3, M11 (and light M7 lumbar).

Run from repo root:
  python anatomy_kit/py/phase2_apply.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from anatomy_kit.py.bone_outline import BONE_DEFS, hero
from anatomy_kit.py.wave_a_apply import ensure_b_foot


def ensure_b_bone(html: str) -> str:
    if 'id="b_bone"' in html or "id='b_bone'" in html:
        return html
    # Prefer insert after first linearGradient if present
    if "</defs>" in html:
        return html.replace("</defs>", BONE_DEFS + "</defs>", 1)
    return html


def ensure_b_sh(html: str) -> str:
    if 'id="b_sh"' in html or 'id="sh_b"' in html:
        # map filter url(#b_sh) may need alias — heroes use b_sh
        if 'id="b_sh"' not in html and 'id="sh_b"' in html:
            html = html.replace('id="sh_b"', 'id="sh_b"')  # keep
            # add alias filter
            html = html.replace(
                "</defs>",
                '<filter id="b_sh" x="-25%" y="-25%" width="150%" height="160%">'
                '<feDropShadow dx="1.5" dy="2.5" stdDeviation="2" flood-color="#000" flood-opacity="0.18"/>'
                "</filter></defs>",
                1,
            )
        return html
    return html.replace(
        "</defs>",
        '<filter id="b_sh" x="-25%" y="-25%" width="150%" height="160%">'
        '<feDropShadow dx="1.5" dy="2.5" stdDeviation="2" flood-color="#000" flood-opacity="0.18"/>'
        "</filter></defs>",
        1,
    )


def ensure_b_sph(html: str) -> str:
    if 'id="b_sph"' in html:
        return html
    if 'id="sph_b"' in html:
        html = html.replace(
            "</defs>",
            '<radialGradient id="b_sph" cx="38%" cy="34%" r="70%">'
            '<stop offset="0" stop-color="#fcf8ef"/><stop offset="0.6" stop-color="#e8dabb"/>'
            '<stop offset="1" stop-color="#c2ae84"/></radialGradient></defs>',
            1,
        )
        return html
    return html.replace(
        "</defs>",
        '<radialGradient id="b_sph" cx="38%" cy="34%" r="70%">'
        '<stop offset="0" stop-color="#fcf8ef"/><stop offset="0.6" stop-color="#e8dabb"/>'
        '<stop offset="1" stop-color="#c2ae84"/></radialGradient></defs>',
        1,
    )


def replace_first_figure(html: str, aria_substr: str, new_figure: str) -> tuple[str, bool]:
    for m in re.finditer(r"<figure>.*?</figure>", html, re.S):
        if aria_substr in m.group(0):
            return html[: m.start()] + new_figure + html[m.end() :], True
    return html, False


def insert_after_paragraph(html: str, marker_substr: str, block: str) -> tuple[str, bool]:
    """Insert HTML block after the first </p> following marker_substr."""
    idx = html.find(marker_substr)
    if idx < 0:
        return html, False
    # find next </p> after marker
    end = html.find("</p>", idx)
    if end < 0:
        return html, False
    end += len("</p>")
    return html[:end] + "\n\n" + block + html[end:], True


ATTR_NOTE_M2 = (
    '<p class="small">Bone outlines: NIH BioArt upper-leg illustration is public domain '
    '(NIAID/NIH; Ryan Kissinger). Geometry heroes use typical adult dimensions '
    '(neck-shaft angle ≈125°, head diameter ≈46&nbsp;mm scaled). '
    'See <code>anatomy_kit/ATTRIBUTIONS.md</code>.</p>'
)


def fig_m2_femur_hero() -> str:
    # NIH real + geometry lateral side by side
    left = hero("nih_upper_leg", max_width=150, x=20, y=15)
    right = hero("femur_lateral", x=280, y_head=25, scale=0.95, show_labels=True)
    return (
        f'<figure><svg class="setupfig" viewBox="0 0 460 400" width="100%" role="img" '
        f'aria-label="Left: NIH BioArt upper leg bones (public domain). Right: lateral femur '
        f'with neck-shaft angle about 125 degrees, head, greater trochanter, and condyles.">'
        f"{left}{right}"
        f'<text x="95" y="390" font-size="12" fill="#555" text-anchor="middle">NIH BioArt (PD)</text>'
        f'<text x="320" y="390" font-size="12" fill="#555" text-anchor="middle">geometry: neck-shaft ≈125°</text>'
        f"</svg>"
        f"<figcaption>A real femur is not a capsule. Left: public-domain NIH BioArt upper-leg bones. "
        f"Right: teaching lateral outline with anatomic neck-shaft angle, head, greater trochanter (GT), "
        f"and distal condyles — the landmarks that matter for bending, torsion, and fall fracture.</figcaption>"
        f"</figure>"
    )


def fig_m2_torsion_replace() -> str:
    """Replace sausage torsion figure with geometry femur + helix."""
    bone = hero("femur_lateral", x=100, y_head=20, scale=0.85, show_labels=False)
    # helix crack overlay approximate
    helix = (
        '<polyline fill="none" stroke="#7a1f1f" stroke-width="2.8" stroke-linecap="round" '
        'points="115,90 125,110 132,135 128,160 118,185 122,210 135,235 145,255"/>'
        '<text x="155" y="160" font-size="12" fill="#7a1f1f">45° spiral</text>'
        '<path d="M95,55 A18 8 0 1 1 140,55" fill="none" stroke="#1f5f7a" stroke-width="2" marker-end="url(#a_blu)"/>'
        '<text x="145" y="48" font-size="12" fill="#1f5f7a">T</text>'
    )
    # Mohr-ish panel right
    right = (
        '<rect x="230" y="80" width="70" height="70" fill="none" stroke="#333" stroke-width="1.5"/>'
        '<line x1="230" y1="115" x2="300" y2="115" stroke="#999" stroke-dasharray="3 2"/>'
        '<line x1="265" y1="80" x2="265" y2="150" stroke="#999" stroke-dasharray="3 2"/>'
        '<text x="265" y="175" font-size="11" fill="#555" text-anchor="middle">pure shear</text>'
        '<text x="310" y="100" font-size="12" fill="#7a1f1f">σ₁ = +τ</text>'
        '<text x="310" y="140" font-size="12" fill="#2a7d2a">σ₂ = −τ</text>'
        '<line x1="250" y1="95" x2="280" y2="125" stroke="#7a1f1f" stroke-width="2"/>'
        '<line x1="280" y1="95" x2="250" y2="125" stroke="#2a7d2a" stroke-width="2"/>'
    )
    return (
        f'<figure><svg class="setupfig" viewBox="0 0 400 300" width="100%" role="img" '
        f'aria-label="Left: lateral femur under torque T with 45-degree helical crack. '
        f'Right: pure shear element and principal tension opening the crack.">'
        f"{bone}{helix}{right}"
        f"</svg>"
        f"<figcaption>Torsion on a real femoral shaft: the surface is pure shear; principal tension "
        f"at 45° opens the classic spiral fracture. Geometry uses an anatomic lateral outline "
        f"(neck-shaft ≈125°), not a featureless capsule.</figcaption></figure>"
    )


def fig_m3_hip_knee() -> str:
    hip = hero("hip_joint", cx=120, cy=100, scale=0.95)
    knee = hero("knee", cx=320, cy=90, scale=0.95, flexion_deg=10)
    return (
        f'<figure><svg class="setupfig" viewBox="0 0 440 240" width="100%" role="img" '
        f'aria-label="Left: hip ball-and-socket with deep acetabulum. Right: sagittal knee with femoral '
        f'condyles, tibial plateau, patella, and contact line.">'
        f"{hip}{knee}"
        f'<text x="120" y="225" font-size="12" fill="#555" text-anchor="middle">hip: deep socket</text>'
        f'<text x="320" y="225" font-size="12" fill="#555" text-anchor="middle">knee: condyles + plateau</text>'
        f"</svg>"
        f"<figcaption>Joint shape is the constraint. The hip's deep acetabulum buys stability; "
        f"the knee's condyle–plateau geometry guides flexion with a clear contact region "
        f"(pressure follows from reaction force / contact area in later sections).</figcaption></figure>"
    )


def fig_m11_shoulder_arm() -> str:
    sh = hero("shoulder", cx=110, cy=100, scale=1.0)
    try:
        arm = hero("nih_arm_bones", max_width=130, x=280, y=20)
    except FileNotFoundError:
        arm = ""
    return (
        f'<figure><svg class="setupfig" viewBox="0 0 440 310" width="100%" role="img" '
        f'aria-label="Left: shoulder complex with shallow glenoid, humeral head, scapula, clavicle. '
        f'Right: NIH BioArt arm bones public domain.">'
        f"{sh}{arm}"
        f'<text x="110" y="265" font-size="12" fill="#555" text-anchor="middle">glenoid is shallow</text>'
        f'<text x="340" y="265" font-size="12" fill="#555" text-anchor="middle">NIH arm bones (PD)</text>'
        f"</svg>"
        f"<figcaption>Shoulder mobility is bought with a shallow glenoid (contrast the deep hip socket). "
        f"Right: NIH BioArt arm bones (public domain) for the serial chain that forward kinematics "
        f"abstracts as links.</figcaption></figure>"
    )


def fig_m7_lumbar() -> str:
    lum = hero("lumbar", cx=180, cy=40, scale=1.3, n=4)
    return (
        f'<figure><svg class="setupfig" viewBox="40 20 280 240" width="100%" role="img" '
        f'aria-label="Lumbar vertebral bodies stacked with intervertebral discs.">'
        f"{lum}"
        f"</svg>"
        f"<figcaption>Low-back load paths pass through vertebral bodies and discs. "
        f"Disc height is small relative to the bodies — a short lever stack that still "
        f"carries large moments when the trunk leans (stoop lift).</figcaption></figure>"
    )


def patch_m2(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    log = []
    html = ensure_b_bone(html)
    html = ensure_b_sh(html)
    html = ensure_b_sph(html)

    if "NIH BioArt upper-leg" in html or "neck-shaft ≈125" in html:
        log.append("M2 femur hero already present")
    else:
        # Insert after motivation first paragraph block — after keyresult or first motivation paras
        html, ok = insert_after_paragraph(
            html,
            "why does the fracture appear in",
            fig_m2_femur_hero() + "\n" + ATTR_NOTE_M2,
        )
        log.append(f"femur hero inserted: {ok}")

    # Replace torsion sausage if present
    html, ok = replace_first_figure(
        html,
        "femur shaft under a torque",
        fig_m2_torsion_replace(),
    )
    log.append(f"torsion femur replaced: {ok}")

    # Trabecular figure — enhance caption only if needed; optional replace capsule head
    html, ok = replace_first_figure(
        html,
        "Trabecular struts inside the femoral head",
        # keep structure but use geometry hip for left part — simpler: new combined figure
        f'<figure><svg class="setupfig" viewBox="0 0 360 220" width="100%" role="img" '
        f'aria-label="Femoral head with trabecular struts along load lines and hip joint context.">'
        f'{hero("hip_joint", cx=100, cy=100, scale=0.85, show_labels=False)}'
        f'{hero("femur_lateral", x=240, y_head=20, scale=0.55, show_labels=False)}'
        # trabecular lines in head
        f'<g stroke="#b59a68" stroke-width="1.5" opacity="0.85">'
        f'<line x1="100" y1="110" x2="70" y2="50"/>'
        f'<line x1="100" y1="110" x2="85" y2="42"/>'
        f'<line x1="100" y1="110" x2="100" y2="38"/>'
        f'<line x1="100" y1="110" x2="115" y2="42"/>'
        f'<line x1="100" y1="110" x2="130" y2="50"/>'
        f"</g>"
        f'<text x="100" y="200" font-size="11" fill="#555" text-anchor="middle">trabeculae follow load</text>'
        f"</svg>"
        f"<figcaption>Trabecular struts inside the femoral head fan along principal load lines "
        f"(Wolff). Drawing the head as a sphere without the neck and acetabulum hides why "
        f"orientation matters for fall fracture.</figcaption></figure>",
    )
    log.append(f"trabecular/hip figure replaced: {ok}")

    path.write_text(html, encoding="utf-8")
    return log


def patch_m3(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    log = []
    html = ensure_b_bone(html)
    html = ensure_b_sh(html)
    html = ensure_b_sph(html)
    html = ensure_b_foot(html)

    if "hip: deep socket" in html:
        log.append("M3 hip/knee hero already present")
    else:
        # After motivation / taxonomy — look for early figure about joint types
        html, ok = insert_after_paragraph(
            html,
            "why the knee bends one way",
            fig_m3_hip_knee(),
        )
        if not ok:
            html, ok = insert_after_paragraph(
                html,
                "Motivation",
                fig_m3_hip_knee(),
            )
        log.append(f"hip/knee hero inserted: {ok}")

    path.write_text(html, encoding="utf-8")
    return log


def patch_m11(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    log = []
    html = ensure_b_bone(html)
    html = ensure_b_sh(html)
    html = ensure_b_sph(html)

    if "glenoid is shallow" in html:
        log.append("M11 shoulder hero already present")
    else:
        html, ok = insert_after_paragraph(
            html,
            "arm as a machine",
            fig_m11_shoulder_arm()
            + '\n<p class="small">Arm-bone plate: NIH BioArt (NIAID/NIH), public domain. '
            "Shoulder geometry is a teaching reconstruction (shallow glenoid vs deep hip socket).</p>",
        )
        if not ok:
            html, ok = insert_after_paragraph(
                html,
                "positions and pushes",
                fig_m11_shoulder_arm(),
            )
        log.append(f"shoulder/arm hero inserted: {ok}")

    path.write_text(html, encoding="utf-8")
    return log


def patch_m7(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    log = []
    html = ensure_b_bone(html)
    html = ensure_b_sh(html)
    html = ensure_b_sph(html)

    if "vertebral bodies and discs" in html or "Lumbar vertebral bodies stacked" in html:
        log.append("M7 lumbar already present")
    else:
        # only if low-back content exists
        if "low back" in html.lower() or "L5" in html or "trunk" in html.lower():
            html, ok = insert_after_paragraph(
                html,
                "Hip strategy",
                fig_m7_lumbar(),
            )
            if not ok:
                html, ok = insert_after_paragraph(
                    html,
                    "co-contraction",
                    fig_m7_lumbar(),
                )
            log.append(f"lumbar hero inserted: {ok}")
        else:
            log.append("M7: no clear low-back insert point")

    path.write_text(html, encoding="utf-8")
    return log


def main():
    for name, fn in (
        ("module02.html", patch_m2),
        ("module03.html", patch_m3),
        ("module11.html", patch_m11),
        ("module07.html", patch_m7),
    ):
        p = ROOT / name
        print("===", name, "===")
        if not p.exists():
            print(" missing")
            continue
        for line in fn(p):
            print(" ", line)


if __name__ == "__main__":
    main()
