"""
Finish Waves A residual + B–E figure realism across module01–17.

Idempotent-ish: safe to re-run. Prose not authored here.
Run from repo root: python anatomy_kit/py/finish_all_waves.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from anatomy_kit.py.body import body_group, gait_pose_joints, standing_joints
from anatomy_kit.py.bone_outline import BONE_DEFS, hero
from anatomy_kit.py.foot_plantar import foot_plantar_svg
from anatomy_kit.py.wave_a_apply import (
    ensure_b_foot,
    fix_head_fill_on_foot_paths,
    shrink_large_heads,
)
from anatomy_kit.py.phase2_apply import ensure_b_bone, ensure_b_sh, ensure_b_sph

SCRATCH = Path(r"C:\Users\simon\AppData\Local\Temp\grok-goal-92ae88c38da1\implementer")
SCRATCH.mkdir(parents=True, exist_ok=True)


def ensure_defs(html: str) -> str:
    html = ensure_b_foot(html)
    html = ensure_b_bone(html)
    html = ensure_b_sh(html)
    html = ensure_b_sph(html)
    return html


def replace_first_figure(html: str, aria_substr: str, new_figure: str) -> tuple[str, bool]:
    for m in re.finditer(r"<figure\b.*?</figure>", html, re.S | re.I):
        if aria_substr in m.group(0):
            return html[: m.start()] + new_figure + html[m.end() :], True
    return html, False


def insert_after_marker(html: str, marker: str, block: str) -> tuple[str, bool]:
    if marker not in html:
        return html, False
    # avoid double insert
    if block[:80] in html or (len(block) > 100 and block[50:120] in html):
        return html, True
    idx = html.find(marker)
    end = html.find("</p>", idx)
    if end < 0:
        end = html.find(">", idx) + 1
    else:
        end += len("</p>")
    return html[:end] + "\n\n" + block + html[end:], True


def strip_deco_bodies_from_plot_figures(html: str) -> tuple[str, int]:
    n = 0

    def fig_fix(m: re.Match) -> str:
        nonlocal n
        block = m.group(0)
        low = block.lower()
        is_plot = "<polyline" in block and (
            "beside the plot" in low
            or "small walking" in low
            or ("stroke=\"#333\"" in block and block.count("polyline") >= 1 and "b_limb" in block)
        )
        if not is_plot or "b_limb" not in block:
            return block
        # Only strip if clearly a chart (axes)
        if block.count('stroke="#333"') < 1 and "percent" not in low and "cost" not in low:
            if "power" not in low and "beside" not in low:
                return block
        out = re.sub(r'<rect[^>]*fill="url\(#b_limb\)"[^>]*/>', "", block)
        out = re.sub(r'<circle[^>]*fill="url\(#b_head\)"[^>]*/>', "", out)
        out = re.sub(r'<circle[^>]*fill="url\(#b_sph\)"[^>]*/>', "", out)
        out = out.replace("; a small walking figure beside the plot", "")
        out = out.replace("a small walking figure beside the plot", "")
        if out != block:
            n += 1
        return out

    return re.sub(r"<figure\b.*?</figure>", fig_fix, html, flags=re.S | re.I), n


def thicken_hairline_limbs(html: str, min_ratio: float = 0.20) -> tuple[str, int]:
    """Bump stroke-width / rect height on very thin limbs in body-ish figures."""
    n = 0

    def fix_rect(m: re.Match) -> str:
        nonlocal n
        tag = m.group(0)
        if "b_limb" not in tag and "b_bone" not in tag and "b_lim" not in tag:
            return tag
        wh = re.search(r'\bwidth="([\d.]+)"', tag)
        ht = re.search(r'\bheight="([\d.]+)"', tag)
        if not wh or not ht:
            return tag
        w, h = float(wh.group(1)), float(ht.group(1))
        # limb capsules: length is max, thickness is min
        length, thick = max(w, h), min(w, h)
        if length < 20:
            return tag
        if thick / length >= min_ratio:
            return tag
        new_thick = max(min_ratio * length, 8.0)
        n += 1
        if w >= h:
            # horizontal-ish before rotate: height is thickness
            return tag.replace(f'height="{ht.group(1)}"', f'height="{new_thick:.1f}"', 1).replace(
                f'rx="{re.search(r"rx=\"([\d.]+)\"", tag).group(1)}"' if re.search(r'rx="([\d.]+)"', tag) else "NOPE",
                f'rx="{new_thick/2:.1f}"' if re.search(r'rx="([\d.]+)"', tag) else "NOPE",
                1,
            ) if re.search(r'rx="([\d.]+)"', tag) else tag.replace(
                f'height="{ht.group(1)}"', f'height="{new_thick:.1f}"', 1
            )
        else:
            return tag.replace(f'width="{wh.group(1)}"', f'width="{new_thick:.1f}"', 1)

    # Simpler robust approach: increase height of b_limb rects when height/width < 0.18
    def fix_rect2(m: re.Match) -> str:
        nonlocal n
        tag = m.group(0)
        if "url(#b_limb)" not in tag and "url(#b_bone)" not in tag and "url(#b_lim)" not in tag:
            return tag
        wh = re.search(r'\bwidth="([\d.]+)"', tag)
        ht = re.search(r'\bheight="([\d.]+)"', tag)
        if not wh or not ht:
            return tag
        w, h = float(wh.group(1)), float(ht.group(1))
        length, thick = max(w, h), min(w, h)
        if length < 25 or thick / length >= 0.18:
            return tag
        new_t = max(0.22 * length, 8.0)
        n += 1
        if h <= w:
            tag2 = tag.replace(f'height="{ht.group(1)}"', f'height="{new_t:.1f}"', 1)
            rm = re.search(r'\brx="([\d.]+)"', tag2)
            if rm:
                tag2 = tag2.replace(f'rx="{rm.group(1)}"', f'rx="{new_t/2:.1f}"', 1)
            return tag2
        else:
            tag2 = tag.replace(f'width="{wh.group(1)}"', f'width="{new_t:.1f}"', 1)
            rm = re.search(r'\brx="([\d.]+)"', tag2)
            if rm:
                tag2 = tag2.replace(f'rx="{rm.group(1)}"', f'rx="{new_t/2:.1f}"', 1)
            return tag2

    out = re.sub(r"<rect\b[^>]*>", fix_rect2, html)
    # thin stroke lines used as limbs (stroke-width small relative to nothing — bump < 2.5 used as body)
    def fix_line(m: re.Match) -> str:
        nonlocal n
        tag = m.group(0)
        if "stroke-linecap" not in tag and 'stroke="#c98a5e"' not in tag:
            return tag
        sw = re.search(r'stroke-width="([\d.]+)"', tag)
        if not sw:
            return tag
        w = float(sw.group(1))
        if w >= 8:
            return tag
        # length
        xs = re.findall(r'x[12]="([\d.]+)"', tag)
        ys = re.findall(r'y[12]="([\d.]+)"', tag)
        if len(xs) >= 2 and len(ys) >= 2:
            import math
            L = math.hypot(float(xs[1]) - float(xs[0]), float(ys[1]) - float(ys[0]))
            if L > 40 and w / L < 0.18:
                new_w = max(0.22 * L, 8.0)
                n += 1
                return tag.replace(f'stroke-width="{sw.group(1)}"', f'stroke-width="{new_w:.1f}"', 1)
        return tag

    out = re.sub(r"<line\b[^>]*>", fix_line, out)
    return out, n


def mini_body_svg(origin=(80, 140), scale=90.0, event: str | None = None) -> str:
    if event:
        j = gait_pose_joints(event, origin=origin, scale_px_per_m=scale)
    else:
        j = standing_joints(origin=origin, scale_px_per_m=scale)
    return body_group(j, show_arms=True, show_feet=True, show_com=False)


# --- Hero figure builders ---

def osteochondral_hero() -> str:
    return (
        '<figure><svg class="setupfig" viewBox="0 0 420 200" width="100%" role="img" '
        'aria-label="Osteochondral unit: subchondral bone, calcified cartilage, hyaline cartilage, synovial fluid.">'
        '<rect x="40" y="140" width="340" height="40" fill="url(#b_bone)" stroke="#8a7350"/>'
        '<text x="210" y="165" font-size="12" fill="#555" text-anchor="middle">subchondral bone</text>'
        '<rect x="40" y="120" width="340" height="20" fill="#c2ae84" stroke="#8a7350"/>'
        '<text x="210" y="134" font-size="11" fill="#555" text-anchor="middle">calcified cartilage</text>'
        '<rect x="40" y="70" width="340" height="50" fill="#e8f0f8" stroke="#5a86a8"/>'
        '<text x="210" y="100" font-size="12" fill="#2a6ca8" text-anchor="middle">hyaline cartilage (porous, charged)</text>'
        '<rect x="40" y="40" width="340" height="30" fill="#d6eaf8" fill-opacity="0.5" stroke="#2a6ca8" stroke-dasharray="4 2"/>'
        '<text x="210" y="60" font-size="12" fill="#2a6ca8" text-anchor="middle">synovial fluid</text>'
        '<line x1="40" y1="40" x2="40" y2="180" stroke="#333" stroke-width="1"/>'
        '</svg><figcaption>Osteochondral unit in load-bearing order: fluid, hyaline cartilage, '
        'calcified cartilage, subchondral bone. Biphasic and Donnan physics live in the cartilage layer; '
        'the sequence is anatomy, not decoration.</figcaption></figure>'
    )


def pennation_hero() -> str:
    fibers = "".join(
        f'<line x1="{120+i*28}" y1="50" x2="{150+i*28}" y2="170" stroke="#b0361f" stroke-width="2.5"/>'
        for i in range(7)
    )
    return (
        '<figure><svg class="setupfig" viewBox="0 0 440 220" width="100%" role="img" '
        'aria-label="Pennate muscle: fibers at pennation angle alpha to the tendon line of action; '
        'PCSA is physiological cross-sectional area perpendicular to fibers.">'
        '<line x1="60" y1="110" x2="380" y2="110" stroke="#8a7350" stroke-width="6" stroke-linecap="round"/>'
        '<text x="220" y="130" font-size="12" fill="#8a7350" text-anchor="middle">tendon line of action</text>'
        f"{fibers}"
        '<path d="M200,70 A40,40 0 0 1 230,95" fill="none" stroke="#2a6ca8" stroke-width="2"/>'
        '<text x="245" y="80" font-size="14" fill="#2a6ca8">α</text>'
        '<line x1="320" y1="60" x2="350" y2="160" stroke="#2a7d2a" stroke-width="2" stroke-dasharray="4 2"/>'
        '<text x="355" y="110" font-size="11" fill="#2a7d2a">PCSA (perp. to fibers)</text>'
        '<text x="80" y="40" font-size="12" fill="#b0361f">muscle fibers</text>'
        "</svg><figcaption>Pennation angle α is between fiber direction and the tendon's line of action. "
        "Force along the tendon is F_fiber cos α; physiological CSA is measured perpendicular to the fibers, "
        "not perpendicular to the tendon.</figcaption></figure>"
    )


def muscle_limb_hero() -> str:
    return (
        '<figure><svg class="setupfig" viewBox="0 0 360 240" width="100%" role="img" '
        'aria-label="Triceps surae on a lower limb: muscle belly, Achilles tendon to calcaneus, moment arm about ankle.">'
        '<rect x="155" y="40" width="20" height="100" rx="10" fill="url(#b_bone)" filter="url(#b_sh)"/>'
        '<ellipse cx="200" cy="185" rx="55" ry="18" fill="url(#b_bone)" stroke="#8a7350"/>'
        '<ellipse cx="145" cy="120" rx="22" ry="40" fill="#c45c4a" fill-opacity="0.85" stroke="#7a1f1f"/>'
        '<path d="M145,155 Q150,175 175,185" fill="none" stroke="#8a7350" stroke-width="4"/>'
        '<line x1="200" y1="185" x2="200" y2="160" stroke="#2a6ca8" stroke-width="2" marker-end="url(#a_blu)"/>'
        '<text x="210" y="155" font-size="11" fill="#2a6ca8">moment arm</text>'
        '<text x="100" y="115" font-size="11" fill="#7a1f1f">triceps surae</text>'
        '<text x="130" y="210" font-size="11" fill="#8a7350">Achilles to calcaneus</text>'
        "</svg><figcaption>Muscle force becomes joint torque through a geometric moment arm. "
        "The Achilles inserts on the calcaneus distal to the ankle axis; F_muscle times d_m supplies "
        "plantarflexion torque.</figcaption></figure>"
    )


def achilles_acl_heroes() -> str:
    return (
        '<figure><svg class="setupfig" viewBox="0 0 440 240" width="100%" role="img" '
        'aria-label="Left: Achilles path from calf to calcaneus. Right: ACL path on knee outline.">'
        '<rect x="70" y="40" width="20" height="100" rx="10" fill="url(#b_bone)"/>'
        '<ellipse cx="100" cy="160" rx="50" ry="16" fill="url(#b_bone)" stroke="#8a7350"/>'
        '<ellipse cx="60" cy="90" rx="18" ry="35" fill="#c45c4a" fill-opacity="0.8"/>'
        '<path d="M65,120 Q75,145 95,158" fill="none" stroke="#8a7350" stroke-width="4"/>'
        '<text x="50" y="200" font-size="12" fill="#555">Achilles path</text>'
        f'{hero("knee", cx=300, cy=90, scale=0.9, flexion_deg=25, show_labels=False)}'
        '<line x1="285" y1="70" x2="310" y2="115" stroke="#b0361f" stroke-width="3"/>'
        '<text x="320" y="95" font-size="12" fill="#b0361f">ACL</text>'
        '<text x="300" y="210" font-size="12" fill="#555" text-anchor="middle">ACL on knee outline</text>'
        "</svg><figcaption>Elastic tissues have anatomic paths: the Achilles stores energy between "
        "calf and calcaneus; the ACL runs from femur to tibia inside the knee and constrains anterior "
        "tibial translation.</figcaption></figure>"
    )


def fracture_oa_heroes() -> str:
    return (
        '<figure><svg class="setupfig" viewBox="0 0 440 280" width="100%" role="img" '
        'aria-label="Left: femoral neck fracture site on lateral femur. Right: osteoarthritic joint with thinned cartilage.">'
        f'{hero("femur_lateral", x=100, y_head=25, scale=0.75, show_labels=False)}'
        '<circle cx="108" cy="55" r="8" fill="none" stroke="#b0361f" stroke-width="2.5"/>'
        '<text x="125" y="50" font-size="12" fill="#b0361f">neck fracture site</text>'
        f'{hero("hip_joint", cx=320, cy=120, scale=0.85, show_labels=False)}'
        '<path d="M300,100 Q320,115 340,100" fill="none" stroke="#7a1f1f" stroke-width="3" stroke-dasharray="3 2"/>'
        '<text x="300" y="200" font-size="11" fill="#7a1f1f">cartilage loss / OA</text>'
        '</svg><figcaption>Aging and injury map onto anatomy: osteoporotic fracture concentrates at the '
        'femoral neck; osteoarthritis is progressive loss of the bearing surface and its fluid-load support.</figcaption></figure>'
    )


def marker_set_hero() -> str:
    j = standing_joints(origin=(160, 230), scale_px_per_m=150)
    body = body_group(j, show_arms=True, show_feet=True, show_com=True)
    # markers
    markers = ""
    for key, lab in (
        ("ankle_R", "ANK"),
        ("knee_R", "KNE"),
        ("hip", "HIP"),
        ("shoulder", "SHO"),
        ("wrist_R", "WRI"),
    ):
        if key not in j:
            continue
        x, y = j[key]
        markers += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#2a6ca8" stroke="#fff" stroke-width="1"/>'
        markers += f'<text x="{x+8:.1f}" y="{y+4:.1f}" font-size="9" fill="#2a6ca8">{lab}</text>'
    foot = foot_plantar_svg(280, 180, 120, show_cop=False, show_grf=False, show_labels=False)
    return (
        f'<figure><svg class="setupfig" viewBox="20 0 420 280" width="100%" role="img" '
        f'aria-label="Winter-proportion body with motion-capture markers and force-plate foot outline.">'
        f'<line x1="40" y1="230" x2="260" y2="230" stroke="#999"/>'
        f'<rect x="100" y="232" width="120" height="12" fill="#ddd" stroke="#999"/>'
        f'<text x="160" y="258" font-size="10" fill="#555" text-anchor="middle">force plate</text>'
        f"{body}{markers}{foot}"
        f"</svg><figcaption>Measurement chain: markers on a Winter-proportioned skeleton estimate joint "
        f"centers; the force plate supplies GRF and COP under a real foot outline — inverse dynamics "
        f"connects the two.</figcaption></figure>"
    )


def run_body_hero() -> str:
    j = gait_pose_joints("midstance", origin=(180, 220), scale_px_per_m=140)
    # exaggerate flight-like: use midswing as "flight" companion
    j2 = gait_pose_joints("midswing", origin=(320, 200), scale_px_per_m=120)
    return (
        f'<figure><svg class="setupfig" viewBox="40 0 400 270" width="100%" role="img" '
        f'aria-label="Running: stance vault and flight pose with Winter proportions.">'
        f'<line x1="50" y1="220" x2="250" y2="220" stroke="#999"/>'
        f"{body_group(j, show_arms=True, show_feet=True)}"
        f"{body_group(j2, show_arms=True, show_feet=True)}"
        f'<text x="180" y="250" font-size="12" fill="#555" text-anchor="middle">stance</text>'
        f'<text x="320" y="250" font-size="12" fill="#555" text-anchor="middle">flight</text>'
        f"</svg><figcaption>Running replaces double support with flight. Bodies use Winter segment ratios; "
        f"the spring-mass model is still the correct abstraction for the GRF, drawn beside not instead of the body.</figcaption></figure>"
    )


def balance_body_hero() -> str:
    j = standing_joints(origin=(160, 220), scale_px_per_m=150)
    body = body_group(j, show_com=True, show_arms=True, show_feet=True)
    return (
        f'<figure><svg class="setupfig" viewBox="40 0 360 280" width="100%" role="img" '
        f'aria-label="Standing balance: Winter body, COM, base of support, and capture region sketch.">'
        f'<line x1="50" y1="220" x2="300" y2="220" stroke="#999"/>'
        f'<rect x="130" y="218" width="60" height="10" rx="3" fill="#e8ded0" stroke="#b7a98c"/>'
        f'<text x="160" y="250" font-size="11" fill="#555" text-anchor="middle">BoS</text>'
        f'<rect x="100" y="215" width="120" height="4" fill="#2a6ca8" fill-opacity="0.3"/>'
        f'<text x="220" y="210" font-size="10" fill="#2a6ca8">capture region (schematic)</text>'
        f"{body}"
        f"</svg><figcaption>Balance is active control of the COM relative to a finite base of support. "
        f"Body proportions are Winter; sensorimotor block diagrams stay schematic.</figcaption></figure>"
    )


def sts_pose_hero() -> str:
    # simple sit and stand
    stand = standing_joints(origin=(280, 220), scale_px_per_m=120)
    # seated: hip flexed
    sit_j = standing_joints(origin=(120, 220), scale_px_per_m=120)
    # manually flex - use gait midstance-ish as stand and a crouched pose
    sit = gait_pose_joints("toe_off", origin=(120, 220), scale_px_per_m=110)
    return (
        f'<figure><svg class="setupfig" viewBox="20 0 400 270" width="100%" role="img" '
        f'aria-label="Sit-to-stand: seated and standing poses with Winter proportions.">'
        f'<line x1="40" y1="220" x2="380" y2="220" stroke="#999"/>'
        f'<rect x="70" y="160" width="50" height="60" fill="#ddd" stroke="#999"/>'
        f"{body_group(sit, show_arms=True, show_feet=True)}"
        f"{body_group(stand, show_arms=True, show_feet=True)}"
        f'<text x="120" y="250" font-size="12" fill="#555" text-anchor="middle">sit / lift-off</text>'
        f'<text x="280" y="250" font-size="12" fill="#555" text-anchor="middle">stand</text>'
        f"</svg><figcaption>Daily-life tasks are multi-joint. Sit-to-stand demands hip and knee extension "
        f"torque while the COM moves from the chair into the BoS — poses use the course body kit.</figcaption></figure>"
    )


def process_module(n: int) -> list[str]:
    path = ROOT / f"module{n:02d}.html"
    log: list[str] = []
    if not path.exists():
        return [f"MISSING {path.name}"]
    html = path.read_text(encoding="utf-8")
    html = ensure_defs(html)

    # Global hygiene
    html, n_head = shrink_large_heads(html, max_r=15.5)
    html, n_foot = fix_head_fill_on_foot_paths(html)
    html, n_deco = strip_deco_bodies_from_plot_figures(html)
    html, n_thick = thicken_hairline_limbs(html)
    log.append(f"heads={n_head} feet={n_foot} deco_plots={n_deco} thicken={n_thick}")

    # Wave-specific inserts
    if n == 4 and "Osteochondral unit in load-bearing order" not in html:
        html, ok = insert_after_marker(html, "impossible bearing", osteochondral_hero())
        if not ok:
            html, ok = insert_after_marker(html, "Motivation", osteochondral_hero())
        log.append(f"M4 osteochondral: {ok}")

    if n == 5:
        if "Pennation angle α" not in html and "pennation angle" not in html.lower()[:5000]:
            pass
        if "physiological CSA is measured perpendicular" not in html:
            html, ok = insert_after_marker(html, "force that has to be built", pennation_hero())
            if not ok:
                html, ok = insert_after_marker(html, "Muscle architecture", pennation_hero())
            log.append(f"M5 pennation: {ok}")
        if "Achilles inserts on the calcaneus" not in html and "triceps surae" not in html:
            html, ok = insert_after_marker(html, "Hill-type", muscle_limb_hero())
            if not ok:
                html, ok = insert_after_marker(html, "force–velocity", muscle_limb_hero())
            log.append(f"M5 muscle-limb: {ok}")

    if n == 6 and "Achilles path" not in html:
        html, ok = insert_after_marker(html, "running is bouncing", achilles_acl_heroes())
        if not ok:
            html, ok = insert_after_marker(html, "Motivation", achilles_acl_heroes())
        log.append(f"M6 Achilles/ACL: {ok}")

    if n == 9 and "stance</text>" not in html and "Running replaces double support" not in html:
        html, ok = insert_after_marker(html, "why running is bouncing", run_body_hero())
        if not ok:
            html, ok = insert_after_marker(html, "Motivation", run_body_hero())
        log.append(f"M9 run body: {ok}")

    if n == 10 and "capture region (schematic)" not in html:
        html, ok = insert_after_marker(html, "balance is active control", balance_body_hero())
        if not ok:
            html, ok = insert_after_marker(html, "Motivation", balance_body_hero())
        log.append(f"M10 balance body: {ok}")

    if n == 13 and "Sit-to-stand" not in html and "sit / lift-off" not in html:
        html, ok = insert_after_marker(html, "day as applied mechanics", sts_pose_hero())
        if not ok:
            html, ok = insert_after_marker(html, "case-study", sts_pose_hero())
        log.append(f"M13 STS: {ok}")
        # lumbar lift
        if "vertebral bodies and discs" not in html and "Lumbar vertebral" not in html:
            lum = (
                f'<figure><svg class="setupfig" viewBox="40 20 300 240" width="100%" role="img" '
                f'aria-label="Lumbar stack for lifting loads.">'
                f'{hero("lumbar", cx=160, cy=40, scale=1.2, n=4)}'
                f"</svg><figcaption>Lifting loads the lumbar stack: short disc height, long trunk moment arm.</figcaption></figure>"
            )
            html, ok2 = insert_after_marker(html, "Lifting", lum)
            log.append(f"M13 lumbar: {ok2}")

    if n == 14 and "neck fracture site" not in html:
        html, ok = insert_after_marker(html, "aging as parameter drift", fracture_oa_heroes())
        if not ok:
            html, ok = insert_after_marker(html, "Motivation", fracture_oa_heroes())
        log.append(f"M14 fracture/OA: {ok}")

    if n == 15 and "Helen Hayes" not in html and "force plate" not in html[:3000]:
        # may already have measurement figs
        if "Winter-proportion body with motion-capture markers" not in html:
            html, ok = insert_after_marker(html, "number you never measured", marker_set_hero())
            if not ok:
                html, ok = insert_after_marker(html, "measurement chain", marker_set_hero())
            log.append(f"M15 markers: {ok}")

    if n == 1:
        # optional lumbar if low-back torque discussed and no lumbar yet
        if "low back" in html.lower() and "vertebral body" not in html:
            lum = (
                f'<figure><svg class="setupfig" viewBox="40 20 280 220" width="100%" role="img" '
                f'aria-label="Lumbar vertebrae for low-back moment discussion.">'
                f'{hero("lumbar", cx=150, cy=30, scale=1.15, n=3)}'
                f"</svg><figcaption>Low-back moments act through the lumbar stack (bodies + discs).</figcaption></figure>"
            )
            html, ok = insert_after_marker(html, "low back", lum)
            log.append(f"M1 lumbar: {ok}")

    if n in (12, 16, 17):
        # light: only hygiene already applied; optional one body if coordination text
        if n == 12 and "Winter-proportion" not in html and "b_limb" in html:
            log.append("M12: hygiene only (control plots Class S)")
        if n == 17 and "capstone" in html.lower():
            log.append("M17: hygiene only")

    # M2: remove decorative bodies on bone plots if any
    if n == 2:
        html, n_deco2 = strip_deco_bodies_from_plot_figures(html)
        log.append(f"M2 extra deco strip: {n_deco2}")

    # M7/M8/M11 problem figures: re-shrink heads aggressively
    if n in (7, 8, 11):
        html, n_head2 = shrink_large_heads(html, max_r=14.5)
        log.append(f"re-shrink heads: {n_head2}")

    path.write_text(html, encoding="utf-8")
    return log


def main():
    all_log = []
    for n in range(1, 18):
        lines = process_module(n)
        msg = f"M{n:02d}: " + "; ".join(lines)
        print(msg)
        all_log.append(msg)
    (SCRATCH / "finish_waves_log.txt").write_text("\n".join(all_log), encoding="utf-8")
    print("wrote", SCRATCH / "finish_waves_log.txt")


if __name__ == "__main__":
    main()
