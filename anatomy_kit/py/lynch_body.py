"""Posable whole human body from Patrick J. Lynch's skeleton art (CC BY 2.5), in the house style.

Art and licence
  Lateral view:  "Skeleton lateral.svg" (no arms).  Arms and the anterior view:
  "Skeleton whole body ant lat views.svg".  Both Patrick J. Lynch, medical illustrator, CC BY 2.5, via Wikimedia
  Commons.  The kit stores the cropped segment art in three files (see ATTRIBUTIONS.md):
    svg_paths/lynch_lat_body.svg   lateral segments + lateral body silhouette (skin)
    svg_paths/lynch_arm.svg        Lynch's anterior-view LEFT arm (humerus; radius + ulna; hand), each bone turned so
                                   its joint-to-joint axis is vertical and scaled to Winter (2009) lengths
    svg_paths/lynch_ant_body.svg   anterior segments (left limbs, left halves of trunk and pelvis) + anterior silhouette
  The files are made once by `python -I -X utf8 lynch_body.py --build ART_DIR` (ART_DIR holds the two Lynch folders
  of the workspace art_sources/; it needs Chrome).  At import the kit only reads the three files.
  Segments are split by ELEMENT (the paths of that bone), never by a rectangle: Chrome samples 24 points along each
  light detail path and gives the path to the topmost big bone fill that contains a sample (isPointInFill, then the
  same test with an 8-direction 1.2-unit dilation for outline rings that sit on a fill edge).  `*_FORCE` lists the
  few overrides found by looking.  Paths inside no bone are body-outline details: they go to the skin group.
  Size: each path is flattened, simplified (Ramer-Douglas-Peucker, EPS = 0.45 U = 0.41 px at 900 px tall) and
  written with 0.1-unit relative steps; consecutive paths of one style in one segment are merged into one path
  (each turned to positive winding first, so the nonzero union looks the same as the separate paths).
  SHARED_DEFS() = 84,375 bytes (limit 90 KB); `python -I -X utf8 lynch_body.py` prints the bytes per segment.

Units and frames
  All art is in body units U: stature H = H_U (993.6 U, the lateral art after the Winter fix below), floor at y = 0,
  +y down, anterior = +x (facing right).  Each segment is one <g id="hbody_..."> in segment-local coordinates:
  proximal joint centre at the origin, axes as in the standing art (the long axis is vertical at standing; for
  trunk and head the distal end is at -y, for limbs at +y).
  Lateral segments: hbody_lat_head (skull, cervical spine), hbody_lat_trunk (ribcage, thoracic + lumbar spine,
  scapula), hbody_lat_pelvis (with sacrum), hbody_lat_thigh (femur, patella), hbody_lat_shank (tibia, fibula),
  hbody_lat_foot, hbody_lat_skin (silhouette, standing only).  Arms (shared by both views): hbody_arm_upper,
  hbody_arm_fore, hbody_arm_hand.  Anterior: hbody_ant_head, hbody_ant_trunk (= hbody_ant_trunkhalf + its mirror),
  hbody_ant_pelvis (= hbody_ant_pelvishalf + mirror), hbody_ant_thigh, hbody_ant_shank, hbody_ant_foot (left side;
  the right side is the same art mirrored, as Lynch drew it: the anterior figure is mirror-symmetric about x 52.0),
  hbody_ant_skin.  hbody_far = the darkening filter for far limbs.
  Joint centres (measured on the art, constants LAT / ANT below): hip = femoral-head centre (circle fit), knee =
  joint-line midpoint, ankle = tip of the lateral malleolus (Winter's ankle landmark, 0.039 H), shoulder = glenoid
  centre (lateral) / humeral-head centre (anterior), elbow = midpoint of the trochlea and capitulum lowest points,
  wrist = midpoint of the ulnar head and radial styloid tips, L5/S1 = mid L5 inferior endplate, neck = C7/T1.
  Winter fix: Lynch's lateral knee sits at 0.257 H.  The thigh art is scaled x0.937 and the shank art x1.149 along
  their long axis only (widths kept) so that hip = 0.530 H and knee = 0.285 H exactly; head, trunk, pelvis and foot
  are unscaled.  The silhouette gets the same piecewise vertical map.  Arms: upper arm 0.188 H, forearm 0.145 H,
  hand (wrist to middle fingertip) 0.108 H, each bone scaled uniformly.  The anterior view keeps Lynch's own
  proportions (hip 0.5375 H, knee 0.280 H: within 3 % of Winter) and Lynch's own arm lengths.

Arms and hand in the side view
  The lateral art has no arms, so the arm is Lynch's anterior-view left arm.  Hanging in neutral (palm toward the
  thigh) the forearm turns 90 deg from the anatomical position: the radius (lateral in the anterior view) comes to
  the front and the thumb points forward, so the anterior-view outline maps to the side view with x kept.  A side
  viewer sees the back of the hand, whose outline is the anterior-view palm outline.  The humeral head of the
  anterior view points medially; in the side view it sits on the glenoid and reads as a round head.

API (all angles in degrees)
  SHARED_DEFS() -> str             every hbody_ group once (recoloured with house.recolour(..., "lynch")) + filter.
  pose(...) -> Pose                lateral view.  Joint angles, zero = the standing art (arms: zero = hanging
      pelvis   anterior tilt of the pelvis about the hip (+ = top forward); the trunk and head go with it
      trunk    trunk flexion about L5/S1 relative to the pelvis (+ = forward).  The trunk is RIGID: the lumbar curve
               does not bend; total trunk inclination = pelvis + trunk.
      neck     head flexion about C7/T1 relative to the trunk (+ = chin down)
      near, far  dicts (near = the side the viewer sees, drawn in front): hip (+ = flexion), knee (+ = flexion),
               ankle (+ = dorsiflexion) or contact="flat" (default: foot flat, ankle solved) / "toe" / "heel"
               (foot turned so that point touches the floor) / None (use ankle), shoulder (+ = flexion, relative to
               the trunk), elbow (+ = flexion), wrist (+ = hand turned forward; radial deviation in neutral)
      anchor   (point, side): point in heel, toe, hip, ankle, knee, l5s1, shoulder; side "near"/"far".  draw()'s
               x, y is where that point lands; heel/toe also set the floor line.
  pose_ant(...) -> Pose            anterior view (subject faces the viewer; subject's right = image left).
      pelvis   pelvic obliquity, + = clockwise on screen (subject's LEFT hip lower).  With the stance foot as anchor
               this tilts the pelvis about the stance hip.
      trunk    lateral lean of trunk + head + arms about L5/S1 relative to the pelvis, + = toward the subject's left
               (clockwise on screen); neck, same sense, relative to the trunk
      r, l     dicts: hip (abduction from VERTICAL, global, + = foot away from the midline), knee (valgus, + = ankle
               away from the midline relative to the thigh), contact="flat" (foot sole level) or ankle (frontal
               angle), hip_flex / knee_flex (sagittal flexion shown as foreshortening: the segment is drawn scaled
               by cos(angle) along its axis, an orthographic first-order view of a limb tilted toward the viewer),
               shoulder (abduction relative to the trunk), elbow, wrist (frontal angles, + = away from the midline)
      anchor   (point, side): sole, ankle, knee, hip with side "r"/"l", or ("pelvis", None) = mid-hip point.
  draw(p, s, P, x, y, height, facing="right", skin=False, shade_far=True, gap_fill="none") -> (svg, J)
      svg: <use href="#hbody_..."> elements in one <g>; height = rendered stature in figure user units.  Far limbs
      are drawn first (behind) through the hbody_far filter (colours x 0.86).  gap_fill fills the one small gap
      shape of the trunk (none = see-through; standing_full uses skin).  facing="left" mirrors the figure.
      J: figure-unit points: vertex, neck, l5s1, hip, knee, ankle, heel, toe, shoulder, elbow, wrist, fingertip
      (lateral: near side; the far side has the suffix _far; anterior: suffixes _r / _l, sole_r / sole_l, hip_mid),
      com (whole body, Winter mass fractions from data/segments_winter.json), com_<segment>[_far|_r|_l],
      floor_y, bbox (conservative (x0, y0, x1, y1) of the drawn art), scale (figure units per U).
      p = the figure's id prefix (unused by the <use> markup; kept for the house call pattern).
  standing_full(p, s, x, y, height, view="lat", facing="right") -> (svg, J)
      the approved fig30 look: complete art with the skin silhouette (lateral: plus the added arm; the arm has no
      skin of its own: the silhouette is one path and cannot be cut).  Posed figures are skeleton-only.
  credit(s, x, y) -> svg text lines (house.ATTRIBUTION["by"]).
  POSES, POSES_ANT: named presets used by the gallery and the self-check.

Run  python -I -X utf8 lynch_body.py           self-check (asserts + Winter table + bytes per segment)
     python -I -X utf8 lynch_body.py --build ART_DIR    rebuild the three svg_paths files (Chrome)
"""
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))      # run as a script with python -I
import house as H  # noqa: E402

KIT = Path(__file__).resolve().parents[1]
SVG_DIR = KIT / "svg_paths"
FILES = ("lynch_lat_body.svg", "lynch_arm.svg", "lynch_ant_body.svg")
WINTER = json.loads((KIT / "data" / "segments_winter.json").read_text(encoding="utf-8"))["segments"]
EPS = 0.45                # RDP tolerance, body units (H = 993.6 U; 0.41 px at 900 px tall)
SKIN_FILL = H.TISSUE["skin"][0]

# ================================================================ measurements on the art (ROOT user space)
# Skeleton_lateral.svg: every path is in g3143, matrix(1.4023142,0,0,1.4023142,-73.755405,-141.20135); the values
# include it.  "samples" = getPointAtLength in Chrome, 4000 per path.  Path numbers = 0-based index in document order.
LAT_SRC = "C_skeleton-lateral-lynch/Skeleton_lateral.svg"
LAT = dict(
    vertex=(92.93, -140.90),    # silhouette path 0, highest sample
    floor=837.34,               # silhouette path 0, lowest sample (sole)
    heel_x=25.87, toe_x=181.61,  # silhouette path 0, rear- and front-most samples with y > 810
    hip=(97.87, 326.05),        # femur fill path 16: Kasa circle fit to its 346 samples with x > 83, y < 335
                                # (femoral-head arc): r 13.5, max residual 1.5
    knee=(72.64, 585.85),       # y: mid of femur fill 16 lowest sample (584.73) and tibial-plateau outline path 25
                                # top (586.9); x: mid of the femur-fill samples within 3 units of its lowest point
                                # (58.16 .. 87.11)
    ankle=(50.49, 799.05),      # lowest sample of the tibia+fibula fill path 18 = lateral malleolus tip
    l5s1=(94.25, 239.9),        # mid L5 inferior endplate: lumbar fill path 14 bottom outline, posterior corner
                                # (83.0, 237.2) to anterior corner (105.5, 242.6)
    neck=(68.5, 8.5),           # C7/T1: mid C7 inferior endplate, cervical fill path 11 bottom outline,
                                # (62, 6.0) to (75, 11.0)
    glenoid=(38.45, 30.24),     # glenoid-fossa ring path 213: circle fit to its samples, r 9.7, max residual 2.7
)
LAT_FILLS = {9: "head", 10: "head", 11: "head", 12: "trunk", 13: "trunk", 14: "trunk", 15: "pelvis",
             16: "thigh", 17: "thigh", 18: "shank", 19: "foot"}
# overrides found by looking at colour-coded renders: 309 = femoral-head outline (split vote with the acetabulum);
# 1 = a small dark gap in the ribcage (drawn with the <use> fill: none on a skeleton, skin in standing_full);
# skin group: 0 = the silhouette itself, 82 + 345 = skin line over the patellar ligament, 339 (dark) + 340, 7, 8 =
# the shin soft tissue in front of the tibia and its skin line
LAT_FORCE = {0: "skin", 309: "thigh", 1: "trunk", 82: "skin", 345: "skin", 339: "skin", 340: "skin", 7: "skin", 8: "skin"}

# Skeleton_whole_body_ant_lat_views.svg: every path is in g12, matrix(12.340883,0,0,12.355564,-9112.0735,-48854.848).
# Anterior figure = x < 2040 (the lateral figure of this file is not used).  1500 samples per path.
ANT_SRC = "C_skeleton-ant-lat-lynch/Skeleton_whole_body_ant_lat_views.svg"
ANT = dict(
    mid_x=52.0,                 # mirror axis: left femur fill 584 leftmost sample 140.00, right femur fill 765
                                # rightmost sample -36.02 -> (140.00 - 36.02) / 2
    vertex_y=17.06,             # anterior silhouette path 0, highest sample (x 51.1)
    floor=8673.04,              # anterior silhouette path 0, lowest sample
    sole_x=396.4,               # silhouette samples with y > 8600 under the left foot: x 159.1 .. 633.7, middle
    hip=(565.0, 4020.7),        # left femur fill 584: circle fit to 72 samples with 440 < x < 640, y < 4030 (head
                                # arc): r 112.4, max residual 1.5
    knee=(368.0, 6249.0),       # midpoint of the femoral-condyle lowest samples of fill 584: medial (212, 6242),
                                # lateral (~524, 6256)
    ankle=(267.5, 8094.7),      # midpoint of the malleolus tips: tibia fill 586 lowest sample (170.2, 8105.5),
                                # fibula fill 587 lowest sample (364.8, 8083.9)
    l5s1=(52.0, 3443.0),        # lumbar fill 56: lowest samples near the midline (y 3442-3443)
    neck=(52.0, 1458.0),        # C7/T1: disc line above the vertebra that carries the first rib, read off a
                                # 0.87 px/unit render of the cervical fill 55
    shoulder=(914.3, 1681.2),   # left humerus fill 274: circle fit to 149 samples with x < 980, y < 1780 (head
                                # arc): r 112.0, max residual 2.8
    elbow=(1130.0, 3166.0),     # humerus fill 274: midpoint of trochlea lowest (1024, 3175) and capitulum lowest
                                # (1236, 3157) samples
    wrist=(1545.3, 4308.4),     # midpoint of ulna fill 480 lowest sample (1441.5, 4314.7) and radial styloid tip
                                # of radius fill 479 (1649, 4302)
    fingertip=(1657.0, 5147.0),  # hand group lowest point: fill 417 lowest sample (1665.6, 5144.9) / outline path
                                # 465 bbox bottom 5147 (middle finger)
)
ANT_FILLS = {55: "head", 68: "head", 56: "trunk", 272: "trunkhalf", 273: "trunkhalf", 583: "pelvishalf",
             584: "thigh", 585: "thigh", 586: "shank", 587: "shank", 588: "foot",
             274: "upper", 479: "fore", 480: "fore", 417: "hand",
             # right side (mirror of the left; its paths are dropped) - listed so its outlines are not given away
             1039: "drop", 1040: "drop", 1041: "drop", 500: "drop", 562: "drop", 563: "drop",
             764: "drop", 765: "drop", 766: "drop", 767: "drop", 768: "drop", 769: "drop"}
ANT_FORCE = {0: "skin", 644: "skin"}     # 0 = the anterior silhouette; 644 = genital outline (voted into the pelvis)
# 56 (lumbar spine + the lowest ribs) is drawn whole; the ribcage half 272 (with the clavicle and half the sternum)
# and the scapula 273 are drawn as the left half and its mirror.

# ================================================================ derived body frame (pure arithmetic)
HIP_F, KNEE_F = 0.530, 0.285          # Winter (2009) fractions of stature
_h = lambda y: LAT["floor"] - y       # height above the floor in the lateral art  # noqa: E731
_D = _h(LAT["vertex"][1]) - _h(LAT["hip"][1])        # vertex to hip, kept
H_U = _D / (1 - HIP_F)                                # stature after the fix: 993.6
_HIP, _KNEE, _ANK = HIP_F * H_U, KNEE_F * H_U, _h(LAT["ankle"][1])
_TH = (_HIP - _KNEE) / (_h(LAT["hip"][1]) - _h(LAT["knee"][1]))      # thigh axial scale
_SH = (_KNEE - _ANK) / (_h(LAT["knee"][1]) - _ANK)                   # shank axial scale


def lat_height(h, seg):
    """Art height above the floor -> body height (the Winter fix), for one segment's art."""
    hh, hk = _h(LAT["hip"][1]), _h(LAT["knee"][1])
    if seg == "skin":
        seg = "foot" if h <= _ANK else "shank" if h <= hk else "thigh" if h <= hh else "head"
    if seg == "thigh":
        return _HIP + (h - hh) * _TH
    if seg == "shank":
        return _KNEE + (h - hk) * _SH
    if seg == "foot":
        return h
    return h - hh + _HIP


def lat_body(pt, seg):
    """Lateral art root point -> body point (U, floor y = 0)."""
    return (pt[0], -lat_height(_h(pt[1]), seg))


LJ = {k: lat_body(LAT[k], s) for k, s in
      [("hip", "pelvis"), ("knee", "thigh"), ("ankle", "foot"), ("l5s1", "pelvis"), ("neck", "trunk"),
       ("glenoid", "trunk"), ("vertex", "head")]}
LJ["heel"], LJ["toe"] = (LAT["heel_x"], 0.0), (LAT["toe_x"], 0.0)
L_UPPER, L_FORE, L_HAND = 0.188 * H_U, 0.145 * H_U, 0.108 * H_U     # Winter: 0.818-0.630, 0.630-0.485, hand

K_ANT = H_U / (ANT["floor"] - ANT["vertex_y"])        # anterior art units -> U (same stature)


def ant_body(pt):
    return ((pt[0] - ANT["mid_x"]) * K_ANT, (pt[1] - ANT["floor"]) * K_ANT)


AJ = {k: ant_body(ANT[k]) for k in ("hip", "knee", "ankle", "l5s1", "neck", "shoulder", "elbow", "wrist",
                                    "fingertip")}
AJ["sole"] = ant_body((ANT["sole_x"], ANT["floor"]))
AJ["vertex"] = (0.0, -H_U)
AJ["hip_mid"] = (0.0, AJ["hip"][1])


def _arm_art(a, b):
    """Length (U) and angle from vertical (deg, + = distal end to +x) of an anterior arm segment, art a -> b."""
    (x0, y0), (x1, y1) = ant_body(ANT[a]), ant_body(ANT[b])
    return math.hypot(x1 - x0, y1 - y0), math.degrees(math.atan2(x1 - x0, y1 - y0))


ARM_ART = {"upper": _arm_art("shoulder", "elbow"), "fore": _arm_art("elbow", "wrist"),
           "hand": _arm_art("wrist", "fingertip")}
ARM_LEN = {"upper": L_UPPER, "fore": L_FORE, "hand": L_HAND}


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


# segment-local offsets (U): proximal joint at the origin
OFF = {
    "lat_pelvis": {"l5s1": _sub(LJ["l5s1"], LJ["hip"]), "hip": (0.0, 0.0)},
    "lat_trunk": {"neck": _sub(LJ["neck"], LJ["l5s1"]), "shoulder": _sub(LJ["glenoid"], LJ["l5s1"])},
    "lat_head": {"vertex": _sub(LJ["vertex"], LJ["neck"])},
    "lat_thigh": {"knee": _sub(LJ["knee"], LJ["hip"])},
    "lat_shank": {"ankle": _sub(LJ["ankle"], LJ["knee"])},
    "lat_foot": {"heel": _sub(LJ["heel"], LJ["ankle"]), "toe": _sub(LJ["toe"], LJ["ankle"])},
    "arm_upper": {"elbow": (0.0, L_UPPER)}, "arm_fore": {"wrist": (0.0, L_FORE)},
    "arm_hand": {"fingertip": (0.0, L_HAND)},
    "ant_pelvis": {"hip": _sub(AJ["hip"], AJ["hip_mid"]), "l5s1": _sub(AJ["l5s1"], AJ["hip_mid"])},
    "ant_trunk": {"neck": _sub(AJ["neck"], AJ["l5s1"]), "shoulder": _sub(AJ["shoulder"], AJ["l5s1"])},
    "ant_head": {"vertex": _sub(AJ["vertex"], AJ["neck"])},
    "ant_thigh": {"knee": _sub(AJ["knee"], AJ["hip"])},
    "ant_shank": {"ankle": _sub(AJ["ankle"], AJ["knee"])},
    "ant_foot": {"sole": _sub(AJ["sole"], AJ["ankle"])},
}


# ================================================================ geometry helpers
def rot(v, deg):
    """SVG rotate(deg) of a vector (y down: + = clockwise on screen)."""
    a = math.radians(deg)
    return (v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a))


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _contact_angle(ankle, off, floor_y):
    """Foot angle that puts the foot point `off` (from the ankle) on the floor; the solution nearest 0 deg."""
    r, phi = math.hypot(*off), math.atan2(off[1], off[0])
    d = floor_y - ankle[1]
    assert abs(d) <= r, f"foot cannot reach the floor (ankle {d:.1f} U above it, reach {r:.1f})"
    a = math.asin(d / r)
    c = [math.degrees(t - phi) for t in (a, math.pi - a)]
    c = [(v + 180) % 360 - 180 for v in c]
    return min(c, key=abs)


class Pose:
    """Segment placements in body units: segs = [(def id, origin, angle, scale_y, mirror, far)], joints, masses."""

    def __init__(self, view):
        self.view, self.segs, self.j, self.com = view, [], {}, {}
        self.anchor = None


def _limb_sides(d):
    out = dict(hip=0.0, knee=0.0, ankle=0.0, contact="flat", shoulder=0.0, elbow=0.0, wrist=0.0)
    out.update(d or {})
    return out


def pose(pelvis=0.0, trunk=0.0, neck=0.0, near=None, far=None, anchor=("heel", "near")):
    """Lateral pose (see the module docstring).  Returns a Pose for draw()."""
    P, J = Pose("lat"), {}
    hip = (0.0, 0.0)
    th_p = pelvis
    th_t = th_p + trunk
    th_h = th_t + neck
    J["hip"] = J["hip_far"] = hip
    J["l5s1"] = add(hip, rot(OFF["lat_pelvis"]["l5s1"], th_p))
    J["neck"] = add(J["l5s1"], rot(OFF["lat_trunk"]["neck"], th_t))
    J["shoulder"] = J["shoulder_far"] = add(J["l5s1"], rot(OFF["lat_trunk"]["shoulder"], th_t))
    J["vertex"] = add(J["neck"], rot(OFF["lat_head"]["vertex"], th_h))
    legs, arms = [], []
    sides = {"near": _limb_sides(near), "far": _limb_sides(far)}
    for side, L in sides.items():
        sfx = "" if side == "near" else "_far"
        th_th = th_p - L["hip"]
        th_s = th_th + L["knee"]
        J["knee" + sfx] = add(hip, rot(OFF["lat_thigh"]["knee"], th_th))
        J["ankle" + sfx] = add(J["knee" + sfx], rot(OFF["lat_shank"]["ankle"], th_s))
        legs.append((side, sfx, th_th, th_s))
        th_u = th_t - L["shoulder"]
        th_f = th_u - L["elbow"]
        th_w = th_f - L["wrist"]
        J["elbow" + sfx] = add(J["shoulder"], rot(OFF["arm_upper"]["elbow"], th_u))
        J["wrist" + sfx] = add(J["elbow" + sfx], rot(OFF["arm_fore"]["wrist"], th_f))
        J["fingertip" + sfx] = add(J["wrist" + sfx], rot(OFF["arm_hand"]["fingertip"], th_w))
        arms.append((side, sfx, th_u, th_f, th_w))
    # feet: the anchor leg first (it sets the floor), then the other leg
    pt, aside = anchor
    order = sorted(legs, key=lambda q: q[0] != aside)
    floor = None                                 # set by the anchor foot (heel / toe anchor)
    foot_th = {}
    for side, sfx, th_th, th_s in order:
        L = sides[side]
        ank = J["ankle" + sfx]
        if L["contact"] == "flat":
            th_f = 0.0
        elif L["contact"] in ("toe", "heel") and floor is not None:
            th_f = _contact_angle(ank, OFF["lat_foot"][L["contact"]], floor)
        else:
            th_f = th_s - L["ankle"]
        foot_th[side] = th_f
        J["heel" + sfx] = add(ank, rot(OFF["lat_foot"]["heel"], th_f))
        J["toe" + sfx] = add(ank, rot(OFF["lat_foot"]["toe"], th_f))
        if floor is None and pt in ("heel", "toe"):
            floor = J[pt + sfx][1]
    if floor is None:
        floor = max(J[k][1] for k in ("heel", "toe", "heel_far", "toe_far"))
    P.floor_y = floor
    # draw order: far arm, far leg, head, trunk, pelvis, near leg, near arm (source order inside a limb)
    S = P.segs
    for side, sfx, th_u, th_f, th_w in arms:
        if side == "far":
            S += [("arm_upper", J["shoulder"], th_u, 1, False, True), ("arm_hand", J["wrist_far"], th_w, 1, False, True),
                  ("arm_fore", J["elbow_far"], th_f, 1, False, True)]
    for side, sfx, th_th, th_s in legs:
        if side == "far":
            S += [("lat_thigh", hip, th_th, 1, False, True), ("lat_shank", J["knee_far"], th_s, 1, False, True),
                  ("lat_foot", J["ankle_far"], foot_th["far"], 1, False, True)]
    S += [("lat_head", J["neck"], th_h, 1, False, False), ("lat_trunk", J["l5s1"], th_t, 1, False, False),
          ("lat_pelvis", hip, th_p, 1, False, False)]
    for side, sfx, th_th, th_s in legs:
        if side == "near":
            S += [("lat_thigh", hip, th_th, 1, False, False), ("lat_shank", J["knee"], th_s, 1, False, False),
                  ("lat_foot", J["ankle"], foot_th["near"], 1, False, False)]
    for side, sfx, th_u, th_f, th_w in arms:
        if side == "near":
            S += [("arm_upper", J["shoulder"], th_u, 1, False, False), ("arm_hand", J["wrist"], th_w, 1, False, False),
                  ("arm_fore", J["elbow"], th_f, 1, False, False)]
    # Winter centres of mass
    W = lambda k: WINTER[k]["com_frac_from_proximal"]  # noqa: E731
    C = {"head": (lerp(J["neck"], J["vertex"], W("head_neck")), WINTER["head_neck"]["mass_frac"]),
         "trunk": (lerp(J["hip"], J["shoulder"], W("pelvis_trunk")), WINTER["pelvis_trunk"]["mass_frac"])}
    for sfx in ("", "_far"):
        for name, a, b, k in [("upper_arm", "shoulder", "elbow", "upper_arm"), ("forearm", "elbow", "wrist", "forearm"),
                              ("hand", "wrist", "fingertip", "hand"), ("thigh", "hip", "knee", "thigh"),
                              ("shank", "knee", "ankle", "shank"), ("foot", "ankle", "toe", "foot")]:
            C[name + sfx] = (lerp(J[a + sfx] if a + sfx in J else J[a], J[b + sfx], W(k)), WINTER[k]["mass_frac"])
    P.j, P.com, P.anchor = J, C, J[pt + ("" if aside == "near" else "_far")]
    if pt in ("heel", "toe"):
        P.anchor = (P.anchor[0], floor)
    return P


def pose_ant(pelvis=0.0, trunk=0.0, neck=0.0, r=None, l=None, anchor=("pelvis", None), arm_len="art"):  # noqa: E741
    """Anterior pose (see the module docstring).  arm_len "art" = Lynch's arm lengths, "winter" = Winter's."""
    P, J = Pose("ant"), {}
    mid = (0.0, 0.0)
    th_p, th_t = pelvis, pelvis + trunk
    th_h = th_t + neck
    J["hip_mid"] = mid
    J["l5s1"] = add(mid, rot(OFF["ant_pelvis"]["l5s1"], th_p))
    J["neck"] = add(J["l5s1"], rot(OFF["ant_trunk"]["neck"], th_t))
    J["vertex"] = add(J["neck"], rot(OFF["ant_head"]["vertex"], th_h))
    S = P.segs
    S += [("ant_head", J["neck"], th_h, 1, False, False), ("ant_trunk", J["l5s1"], th_t, 1, False, False)]
    sides = {"r": _limb_sides(r), "l": _limb_sides(l)}
    arm_k = {k: (ARM_ART[k][0] / ARM_LEN[k] if arm_len == "art" else 1.0) for k in ARM_LEN}
    feet = []
    for side, L in sides.items():
        m = -1 if side == "r" else 1          # subject's right = image left = mirrored art
        sfx = "_" + side
        mir = lambda v: (m * v[0], v[1])  # noqa: E731
        J["hip" + sfx] = add(mid, rot(mir(OFF["ant_pelvis"]["hip"]), th_p))
        J["shoulder" + sfx] = add(J["l5s1"], rot(mir(OFF["ant_trunk"]["shoulder"]), th_t))
        th_th = -m * L["hip"]                   # global: + abduction = foot away from the midline
        th_s = th_th - m * L["knee"]
        cf_t, cf_s = math.cos(math.radians(L.get("hip_flex", 0))), math.cos(math.radians(L.get("knee_flex", 0)))
        kn = OFF["ant_thigh"]["knee"]
        J["knee" + sfx] = add(J["hip" + sfx], rot(mir((kn[0], kn[1] * cf_t)), th_th))
        an = OFF["ant_shank"]["ankle"]
        J["ankle" + sfx] = add(J["knee" + sfx], rot(mir((an[0], an[1] * cf_s)), th_s))
        th_f = 0.0 if L["contact"] == "flat" else th_s - m * L["ankle"]
        J["sole" + sfx] = add(J["ankle" + sfx], rot(mir(OFF["ant_foot"]["sole"]), th_f))
        feet.append((side, th_th, th_s, th_f, cf_t, cf_s, m))
        th_u = th_t - m * L["shoulder"]
        th_fo = th_u - m * L["elbow"]
        th_w = th_fo - m * L["wrist"]
        J["elbow" + sfx] = add(J["shoulder" + sfx], rot((0.0, L_UPPER * arm_k["upper"]), th_u))
        J["wrist" + sfx] = add(J["elbow" + sfx], rot((0.0, L_FORE * arm_k["fore"]), th_fo))
        J["fingertip" + sfx] = add(J["wrist" + sfx], rot((0.0, L_HAND * arm_k["hand"]), th_w))
        S += [("arm_upper", J["shoulder" + sfx], th_u, arm_k["upper"], m < 0, False),
              ("arm_hand", J["wrist" + sfx], th_w, arm_k["hand"], m < 0, False),
              ("arm_fore", J["elbow" + sfx], th_fo, arm_k["fore"], m < 0, False)]
    S.append(("ant_pelvis", mid, th_p, 1, False, False))
    for side, th_th, th_s, th_f, cf_t, cf_s, m in feet:
        sfx = "_" + side
        S += [("ant_thigh", J["hip" + sfx], th_th, (1, cf_t), m < 0, False),
              ("ant_shank", J["knee" + sfx], th_s, (1, cf_s), m < 0, False),
              ("ant_foot", J["ankle" + sfx], th_f, 1, m < 0, False)]
    W = lambda k: WINTER[k]["com_frac_from_proximal"]  # noqa: E731
    sh_mid = lerp(J["shoulder_r"], J["shoulder_l"], 0.5)
    C = {"head": (lerp(J["neck"], J["vertex"], W("head_neck")), WINTER["head_neck"]["mass_frac"]),
         "trunk": (lerp(mid, sh_mid, W("pelvis_trunk")), WINTER["pelvis_trunk"]["mass_frac"])}
    for sfx in ("_r", "_l"):
        for name, a, b, k in [("upper_arm", "shoulder", "elbow", "upper_arm"), ("forearm", "elbow", "wrist", "forearm"),
                              ("hand", "wrist", "fingertip", "hand"), ("thigh", "hip", "knee", "thigh"),
                              ("shank", "knee", "ankle", "shank"), ("foot", "ankle", "sole", "foot")]:
            C[name + sfx] = (lerp(J[a + sfx], J[b + sfx], W(k)), WINTER[k]["mass_frac"])
    pt, aside = anchor
    P.floor_y = max(J["sole_r"][1], J["sole_l"][1])
    P.j, P.com = J, C
    P.anchor = J["hip_mid"] if pt == "pelvis" else J[pt + "_" + aside]
    return P


# ================================================================ art (read once)
_CACHE = {}


def _groups():
    """{def id: (markup, bbox)} from the three svg_paths files (source colours)."""
    if "g" not in _CACHE:
        g = {}
        for f in FILES:
            t = (SVG_DIR / f).read_text(encoding="utf-8")
            for m in re.finditer(r'<g id="hbody_(\w+)" data-bbox="([^"]+)">(.*?)</g><!--/\1-->', t, re.S):
                g[m.group(1)] = (m.group(0), tuple(float(v) for v in m.group(2).split()))
        _CACHE["g"] = g
    return _CACHE["g"]


FAR_FILTER = ('<filter id="hbody_far" color-interpolation-filters="sRGB"><feComponentTransfer>'
              '<feFuncR type="linear" slope="0.86"/><feFuncG type="linear" slope="0.86"/>'
              '<feFuncB type="linear" slope="0.86"/></feComponentTransfer></filter>')


def SHARED_DEFS():  # noqa: N802 (apply_figs calls this name)
    """All hbody_ groups once per page (recoloured to the house palette) + the far-limb filter."""
    return FAR_FILTER + H.recolour("".join(m for m, _ in _groups().values()), "lynch")


def _fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def draw(p, s, P, x, y, height, facing="right", skin=False, shade_far=True, gap_fill="none"):
    """<use> markup for pose P with its anchor at (x, y) and stature `height` (figure user units)."""
    k = height / H_U
    sx = -1 if facing == "left" else 1
    ax, ay = P.anchor
    F = lambda q: (x + sx * k * (q[0] - ax), y + k * (q[1] - ay))  # noqa: E731
    G = _groups()
    out = [f'<g transform="translate({_fmt(x)} {_fmt(y)}) scale({_fmt(sx * k)} {_fmt(k)}) '
           f'translate({_fmt(-ax)} {_fmt(-ay)})" fill="{SKIN_FILL if skin else gap_fill}">']
    if skin:
        out.append(f'<use href="#hbody_{P.view}_skin" transform="translate({_fmt(P.j["hip_mid" if P.view == "ant" else "hip"][0])} '
                   f'{_fmt(P.j["hip_mid" if P.view == "ant" else "hip"][1])})"/>')
    xs, ys = [], []
    for name, o, th, sc, mirror, far in P.segs:
        sxx, syy = (sc, sc) if not isinstance(sc, tuple) else sc
        tr = f"translate({_fmt(o[0])} {_fmt(o[1])})"
        if th:
            tr += f" rotate({_fmt(th)})"
        if mirror or (sxx, syy) != (1, 1):
            tr += f" scale({_fmt(-sxx if mirror else sxx)} {_fmt(syy)})"
        flt = ' filter="url(#hbody_far)"' if far and shade_far else ""
        out.append(f'<use href="#hbody_{name}" transform="{tr}"{flt}/>')
        x0, y0, x1, y1 = G[name][1]
        for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
            q = F(add(o, rot(((-sxx if mirror else sxx) * cx, syy * cy), th)))
            xs.append(q[0])
            ys.append(q[1])
    out.append("</g>")
    J = {key: F(v) for key, v in P.j.items()}
    tot = sum(m for _, m in P.com.values())
    J["com"] = F((sum(c[0] * m for c, m in P.com.values()) / tot, sum(c[1] * m for c, m in P.com.values()) / tot))
    for key, (c, _) in P.com.items():
        J["com_" + key] = F(c)
    J["floor_y"] = F((0, P.floor_y))[1]
    J["bbox"] = (min(xs), min(ys), max(xs), max(ys))
    J["scale"] = k
    J["_uses"] = out[1:-1]
    return "".join(out), J


def standing_full(p, s, x, y, height, view="lat", facing="right"):
    """Quiet standing with the skin silhouette (the approved fig30 look) plus the arm; (x, y) = the floor point under
    the heel (lateral) or under the mid-hip point (anterior)."""
    if view == "lat":
        P = pose(anchor=("heel", "near"))
    else:
        P = pose_ant(**POSES_ANT["standing"])
        P.anchor = (P.j["hip_mid"][0], P.floor_y)
    return draw(p, s, P, x, y, height, facing=facing, skin=True)


def credit(s, x, y, width=None, extra=""):
    """Credit lines (house.ATTRIBUTION["by"]), word-wrapped to `width` user units (default: 2 lines)."""
    t = H.ATTRIBUTION["by"].format(
        author="Patrick J. Lynch, medical illustrator", title="Skeleton lateral.svg” and “Skeleton whole body ant lat views.svg",
        licence="CC BY 2.5", changes="Recoloured, split into segments and reposed; arms from the anterior view." + extra)
    if width is None:
        cut = t.index(" via Wikimedia") + 1
        return H.credit(s, x, y, [t[:cut].strip(), t[cut:].strip()])
    n = max(20, int(width / (s(H.PX["credit"]) * 0.47)))      # Georgia: ~0.47 em per character
    lines, cur = [], ""
    for w in t.split():
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return H.credit(s, x, y, lines + [cur])


# ================================================================ presets (degrees)
_A = ARM_ART
_ANT_ARMS = dict(shoulder=_A["upper"][1], elbow=_A["fore"][1] - _A["upper"][1], wrist=_A["hand"][1] - _A["fore"][1])
POSES = {
    "standing": dict(),
    "stoop_lift": dict(pelvis=40, trunk=30, near=dict(hip=50, shoulder=70), far=dict(hip=50, shoulder=70)),
    "squat_lift": dict(pelvis=25, trunk=15, near=dict(hip=125, knee=125, shoulder=50, elbow=10),
                       far=dict(hip=125, knee=125, shoulder=50, elbow=10)),
    "sitting": dict(near=dict(hip=90, knee=90), far=dict(hip=90, knee=90)),
    "sit_to_stand": dict(pelvis=25, trunk=20, near=dict(hip=110, knee=100, shoulder=45),
                         far=dict(hip=110, knee=100, shoulder=45)),
    "step_up": dict(pelvis=5, trunk=5, near=dict(hip=60, knee=70, shoulder=-15, elbow=15),
                    far=dict(hip=-5, knee=5, shoulder=20, elbow=20), anchor=("heel", "far")),
    # gait: data/gait_angles_deg.json (hip = thigh angle from vertical; pelvis 0 so it equals the joint angle)
    "gait_heel_strike": dict(near=dict(hip=25, knee=5, contact=None, ankle=0, shoulder=-25, elbow=10),
                             far=dict(hip=-10, knee=35, contact="toe", shoulder=25, elbow=25), anchor=("heel", "near")),
    "gait_midstance": dict(near=dict(hip=0, knee=8, shoulder=0, elbow=10),
                           far=dict(hip=30, knee=60, contact=None, ankle=15, shoulder=5, elbow=15), anchor=("heel", "near")),
    "gait_toe_off": dict(near=dict(hip=-10, knee=40, contact="toe", shoulder=25, elbow=25),
                         far=dict(hip=25, knee=5, shoulder=-25, elbow=10), anchor=("heel", "far")),
    "cmj_crouch": dict(pelvis=30, trunk=20, near=dict(hip=120, knee=120, shoulder=-60, elbow=10),
                       far=dict(hip=120, knee=120, shoulder=-60, elbow=10)),
    "lean_forward": dict(pelvis=8, near=dict(hip=0), far=dict(hip=0)),
}
# lean_forward: the whole body rigid, turned 8 deg forward about the ankles (pelvis 8, thigh 8 -> foot flat = 8 deg
# dorsiflexion); stoop_lift: trunk 70 deg from vertical = pelvis 40 + lumbar 30, knees straight, thighs 10 deg back
# (hips behind the heels, ankles 10 deg plantarflexed) so the COM stays over the feet, arms hanging.
# sit_to_stand (seat-off): trunk 45 deg forward, thigh 5 deg above horizontal, shank 15 deg forward (data/sts_angles.json
# "lift_off" gives hip 70 / knee 75 / trunk 30; those put the hip 0.08 H above the seat, so the kit uses a thigh
# near horizontal, as at the instant the buttocks leave the seat).  single_leg_lean: stance (left) hip 5 deg adducted
# and trunk 10 deg over it put the COM over the stance foot; the right pelvis drops 4 deg; the lifted right leg is
# drawn foreshortened (hip 30, knee 60 deg of flexion).
POSES_ANT = {
    "standing": dict(r=dict(_ANT_ARMS), l=dict(_ANT_ARMS)),
    "feet_apart": dict(r=dict(hip=8, **_ANT_ARMS), l=dict(hip=8, **_ANT_ARMS)),
    "single_leg_lean": dict(pelvis=-4, trunk=10, l=dict(hip=-5, shoulder=12, elbow=8),
                            r=dict(hip=4, hip_flex=30, knee_flex=60, shoulder=25, elbow=10), anchor=("sole", "l")),
}


# ================================================================ build (one time, needs Chrome + the source art)
_NUM = r'[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?'


def _parse(d):
    """Path data -> [(closed, [segment])]; segment = absolute points: 2 = line, 4 = cubic (quadratics raised)."""
    toks = re.findall(_NUM + r'|[A-Za-z]', d)
    n = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "Z": 0}
    subs, cur, k, cmd = [], None, 0, None
    cx = cy = sx = sy = 0.0
    lc = lq = None
    while k < len(toks):
        if toks[k].isalpha():
            cmd, k = toks[k], k + 1
            if cmd in "Zz":
                if cur:
                    if (cx, cy) != (sx, sy):
                        cur.append([(cx, cy), (sx, sy)])
                    subs.append((True, cur))
                cur, cx, cy, lc, lq = None, sx, sy, None, None
                continue
        C, rel = cmd.upper(), cmd.islower()
        a = [float(v) for v in toks[k:k + n[C]]]
        k += n[C]
        ox, oy = (cx, cy) if rel else (0.0, 0.0)
        if C == "M":
            if cur:
                subs.append((False, cur))
            cx, cy = a[0] + ox, a[1] + oy
            sx, sy, cur, lc, lq = cx, cy, [], None, None
            cmd = "l" if rel else "L"
            continue
        if cur is None:
            cur, sx, sy = [], cx, cy
        if C in "LHV":
            p = ((a[0] + ox, a[1] + oy) if C == "L" else (a[0] + (cx if rel else 0), cy) if C == "H"
                 else (cx, a[0] + (cy if rel else 0)))
            cur.append([(cx, cy), p])
            lc = lq = None
        elif C in "CS":
            if C == "C":
                c1, c2, p = (a[0] + ox, a[1] + oy), (a[2] + ox, a[3] + oy), (a[4] + ox, a[5] + oy)
            else:
                c1 = (2 * cx - lc[0], 2 * cy - lc[1]) if lc else (cx, cy)
                c2, p = (a[0] + ox, a[1] + oy), (a[2] + ox, a[3] + oy)
            cur.append([(cx, cy), c1, c2, p])
            lc, lq = c2, None
        else:
            q = (a[0] + ox, a[1] + oy) if C == "Q" else ((2 * cx - lq[0], 2 * cy - lq[1]) if lq else (cx, cy))
            p = (a[2] + ox, a[3] + oy) if C == "Q" else (a[0] + ox, a[1] + oy)
            cur.append([(cx, cy), lerp((cx, cy), q, 2 / 3), lerp(p, q, 2 / 3), p])
            lq, lc = q, None
        cx, cy = p
    if cur:
        subs.append((False, cur))
    return subs


def _flatten(subs, f, step):
    """Subpaths -> point lists in body units: f maps an art point; curves are sampled every `step` art units."""
    out = []
    for closed, segs in subs:
        pts = [f(segs[0][0])]
        for g in segs:
            if len(g) == 2:
                pts.append(f(g[1]))
                continue
            p0, c1, c2, p1 = g
            L = math.dist(p0, c1) + math.dist(c1, c2) + math.dist(c2, p1)
            m = max(1, math.ceil(L / step))
            for i in range(1, m + 1):
                t = i / m
                u = 1 - t
                pts.append(f((u ** 3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t ** 3 * p1[0],
                              u ** 3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t ** 3 * p1[1])))
        out.append((closed, pts))
    return out


def _rdp(pts, eps):
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy)
    if L < 1e-9:
        i = max(range(len(pts)), key=lambda q: math.dist(pts[q], a))
    else:
        i = max(range(1, len(pts) - 1), key=lambda q: abs(dy * (pts[q][0] - a[0]) - dx * (pts[q][1] - a[1])))
        if abs(dy * (pts[i][0] - a[0]) - dx * (pts[i][1] - a[1])) / L <= eps:
            return [a, b]
    if i in (0, len(pts) - 1):
        return [a, b]
    return _rdp(pts[:i + 1], eps)[:-1] + _rdp(pts[i:], eps)


def _area(pts):
    return sum(pts[i][0] * pts[i - 1][1] - pts[i - 1][0] * pts[i][1] for i in range(len(pts))) / 2


def _f1(v):
    t = f"{round(v, 1):.1f}".rstrip("0").rstrip(".")
    t = "0" if t in ("-0", "") else t
    return t.replace("0.", ".", 1) if t.startswith("0.") else t.replace("-0.", "-.", 1)


def _d(polys):
    """[(closed, pts)] -> path data, relative steps between points rounded to 0.1 unit."""
    out, rx, ry, first = [], 0.0, 0.0, True
    for closed, pts in polys:
        q = []
        for x, y in pts:
            r = (round(x, 1), round(y, 1))
            if not q or r != q[-1]:
                q.append(r)
        if closed and len(q) > 1 and q[-1] == q[0]:
            q.pop()
        if len(q) < 2:
            continue
        out.append(("M" + _f1(q[0][0]) + " " + _f1(q[0][1])) if first else
                   ("m" + _f1(q[0][0] - rx) + " " + _f1(q[0][1] - ry)))
        first = False
        out.append("l" + " ".join(_f1(x - a) + " " + _f1(y - b) for (a, b), (x, y) in zip(q, q[1:])))
        rx, ry = q[-1]
        if closed:
            out.append("z")
            rx, ry = q[0]
    return re.sub(r"(\.\d+) (?=\.)", r"\1", "".join(out).replace(" -", "-"))


def _style(tag):
    st = dict(kv.split(":", 1) for kv in re.search(r'style="([^"]*)"', tag).group(1).split(";") if ":" in kv)
    return st.get("fill", "#000"), st.get("stroke", "none"), float(st.get("stroke-width", "1"))


_CLASSIFY_JS = """([fills, R]) => {
  const all = [...document.querySelectorAll('path')], svg = document.documentElement, F = fills.map(i => all[i]), res = {};
  all.forEach((e, i) => {
    if (fills.includes(i) || !e.getAttribute('d')) return;
    const L = e.getTotalLength(), sh = e.getCTM(), votes = new Array(F.length).fill(0);
    for (let k = 0; k < 24; k++) {
      const q = e.getPointAtLength(L * (k + 0.5) / 24);
      let won = -1;
      for (const pass of [[[0, 0]], [[R, 0], [-R, 0], [0, R], [0, -R], [R, R], [-R, -R], [R, -R], [-R, R]]]) {
        for (let j = F.length - 1; j >= 0 && won < 0; j--) {        // topmost fill first (later = drawn above)
          const m = F[j].getCTM().inverse().multiply(sh);
          for (const [dx, dy] of pass) {
            const p = svg.createSVGPoint(); p.x = q.x + dx; p.y = q.y + dy;
            if (F[j].isPointInFill(p.matrixTransform(m))) { won = j; break; }
          }
        }
        if (won >= 0) break;
      }
      if (won >= 0) votes[won] += 1;
    }
    res[i] = votes;
  });
  return res;
}"""


def _classify(src, fills, R):
    """{path index: segment} by the topmost-fill vote (Chrome); unassigned paths are absent."""
    from playwright.sync_api import sync_playwright
    idx = sorted(fills)
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome")
        pg = b.new_page()
        pg.goto(src.resolve().as_uri())
        r = pg.evaluate(_CLASSIFY_JS, [idx, R])
        b.close()
    out = {i: fills[i] for i in idx}
    for i, v in r.items():
        if max(v) > 0:
            out[int(i)] = fills[idx[max(range(len(v)), key=lambda j: v[j])]]
    return out


def _emit(seg, elems, f, step, sc):
    """One <g> from source elements [(index, tag)] in source order: runs of one style are merged."""
    runs = []
    for i, tag in elems:
        dm = re.search(r'\sd="([^"]*)"', tag)
        if not dm or not dm.group(1).strip():
            continue
        fill, stroke, sw = _style(tag)
        if fill == "#414142" and seg not in ("lat_skin", "ant_skin"):
            fill = "inherit"                    # a gap between bones: the <use> fill shows (white / skin)
        key = (fill, stroke, round(sw * sc, 2) if stroke != "none" else 0)
        polys = [(c, _rdp(p, EPS)) for c, p in _flatten(_parse(dm.group(1)), f, step)]
        if fill not in ("none",):
            big = max(polys, key=lambda q: abs(_area(q[1])))
            if _area(big[1]) < 0:
                polys = [(c, p[::-1]) for c, p in polys]
        if runs and runs[-1][0] == key:
            runs[-1][1].extend(polys)
        else:
            runs.append((key, polys))
    body, xs, ys = [], [], []
    for (fill, stroke, sw), polys in runs:
        d = _d(polys)
        if not d:
            continue
        for _, p in polys:
            xs += [q[0] for q in p]
            ys += [q[1] for q in p]
        a = "" if fill == "inherit" else f' fill="{fill}"'
        if stroke != "none":
            a += f' stroke="{stroke}" stroke-width="{_fmt(sw)}"'
        body.append(f'<path d="{d}"{a}/>')
    bb = f"{min(xs):.1f} {min(ys):.1f} {max(xs):.1f} {max(ys):.1f}"
    return f'<g id="hbody_{seg}" data-bbox="{bb}">{"".join(body)}</g><!--/{seg}-->'


def build(art_dir):
    art_dir = Path(art_dir)
    # ---------------- lateral
    src = art_dir / LAT_SRC
    t = src.read_text(encoding="utf-8")
    tags = re.findall(r'<path\b[^>]*>', t)
    assert len(tags) == 377, len(tags)
    M = (1.4023142, -73.755405, -141.20135)
    cls = _classify(src, LAT_FILLS, 1.2)
    cls.update(LAT_FORCE)
    by = {}
    for i, tag in enumerate(tags):
        by.setdefault(cls.get(i, "skin"), []).append((i, tag))
    origin = {"head": LJ["neck"], "trunk": LJ["l5s1"], "pelvis": LJ["hip"], "thigh": LJ["hip"], "shank": LJ["knee"],
              "foot": LJ["ankle"], "skin": LJ["hip"]}
    out = []
    for seg in ("head", "trunk", "pelvis", "thigh", "shank", "foot", "skin"):
        o = origin[seg]
        f = lambda q, seg=seg, o=o: _sub(lat_body((M[0] * q[0] + M[1], M[0] * q[1] + M[2]), seg), o)  # noqa: E731
        out.append(_emit("lat_" + seg, by[seg], f, 0.25 / M[0], M[0]))
    _write(FILES[0], LAT_SRC, out)
    # ---------------- anterior (arms + body)
    src = art_dir / ANT_SRC
    t = src.read_text(encoding="utf-8")
    tags = re.findall(r'<path\b[^>]*>', t)
    assert len(tags) == 1488, len(tags)
    A = (12.340883, -9112.0735, 12.355564, -48854.848)
    cls = _classify(src, ANT_FILLS, 1.0)
    cls.update(ANT_FORCE)
    root = lambda q: (A[0] * q[0] + A[1], A[2] * q[1] + A[3])  # noqa: E731
    by = {}
    for i, tag in enumerate(tags):
        seg = cls.get(i)
        if seg is None:                             # inside no bone: outline detail of the anterior silhouette
            xy = [float(v) for v in re.findall(_NUM, re.search(r'\sd="([^"]*)"', tag).group(1))[:2]]
            seg = "skin" if len(xy) == 2 and root(xy)[0] < 2040 else "drop"   # x >= 2040: this file's lateral figure
        by.setdefault(seg, []).append((i, tag))
    sc = A[0] * K_ANT
    arms = []
    for seg, (a, b) in {"upper": ("shoulder", "elbow"), "fore": ("elbow", "wrist"), "hand": ("wrist", "fingertip")}.items():
        o = ant_body(ANT[a])
        L, ang = ARM_ART[seg]
        k = ARM_LEN[seg] / L
        f = lambda q, o=o, ang=ang, k=k: tuple(v * k for v in rot(_sub(ant_body(root(q)), o), ang))  # noqa: E731
        arms.append(_emit("arm_" + seg, by[seg], f, 0.25 / sc, sc * k))
    _write(FILES[1], ANT_SRC, arms)
    origin = {"head": AJ["neck"], "trunkhalf": AJ["l5s1"], "trunk": AJ["l5s1"], "pelvishalf": AJ["hip_mid"],
              "thigh": AJ["hip"], "shank": AJ["knee"], "foot": AJ["ankle"], "skin": AJ["hip_mid"]}
    body = []
    for seg in ("head", "trunkhalf", "trunk", "pelvishalf", "thigh", "shank", "foot", "skin"):
        o = origin[seg]
        f = lambda q, o=o: _sub(ant_body(root(q)), o)  # noqa: E731
        g = _emit("ant_" + seg, by[seg], f, 0.25 / sc, sc)
        if seg == "trunk":                  # lumbar spine, then the left half and its mirror
            g = g.replace('</g><!--/ant_trunk-->', '<use href="#hbody_ant_trunkhalf"/>'
                          '<use href="#hbody_ant_trunkhalf" transform="scale(-1 1)"/></g><!--/ant_trunk-->')
            g = _widen(g, "trunkhalf", body)
        body.append(g)
        if seg == "pelvishalf":
            bb = re.search(r'data-bbox="([^"]+)"', g).group(1).split()
            w = max(abs(float(bb[0])), abs(float(bb[2])))
            body.append(f'<g id="hbody_ant_pelvis" data-bbox="{-w:.1f} {bb[1]} {w:.1f} {bb[3]}">'
                        '<use href="#hbody_ant_pelvishalf"/><use href="#hbody_ant_pelvishalf" transform="scale(-1 1)"/>'
                        '</g><!--/ant_pelvis-->')
    _write(FILES[2], ANT_SRC, body)


def _widen(g, half, done):
    """The trunk bbox must include the mirrored half."""
    hb = next(re.search(r'data-bbox="([^"]+)"', x).group(1) for x in done if f'id="hbody_ant_{half}"' in x).split()
    w = max(abs(float(hb[0])), abs(float(hb[2])))
    b = re.search(r'data-bbox="([^"]+)"', g).group(1).split()
    nb = f"{min(float(b[0]), -w):.1f} {min(float(b[1]), float(hb[1])):.1f} {max(float(b[2]), w):.1f} {max(float(b[3]), float(hb[3])):.1f}"
    return g.replace(f'data-bbox="{" ".join(b)}"', f'data-bbox="{nb}"', 1)


def _write(name, src, groups):
    head = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="-200 -1100 400 1150">'
            f'<!-- Patrick J. Lynch, medical illustrator, "{Path(src).name}", CC BY 2.5, via Wikimedia Commons. '
            'Split into segments by element, simplified (RDP) and moved to segment-local body units by '
            'anatomy_kit/py/lynch_body.py build(); source colours (recoloured at use). -->')
    (SVG_DIR / name).write_text(head + "<defs>" + "".join(groups) + "</defs></svg>", encoding="utf-8")
    print(f"{name}: {(SVG_DIR / name).stat().st_size} bytes")


# ================================================================ self-check
def _uses_transform(tr):
    """SVG transform list (translate/rotate/scale) -> 2x3 matrix (a, b, c, d, e, f)."""
    m = (1, 0, 0, 1, 0, 0)
    for op, args in re.findall(r'(\w+)\(([^)]*)\)', tr):
        v = [float(a) for a in args.replace(",", " ").split()]
        if op == "translate":
            n = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif op == "rotate":
            c, s_ = math.cos(math.radians(v[0])), math.sin(math.radians(v[0]))
            n = (c, s_, -s_, c, 0, 0)
        else:
            n = (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0)
        a, b, c, d, e, f = m
        m = (a * n[0] + c * n[1], b * n[0] + d * n[1], a * n[2] + c * n[3], b * n[2] + d * n[3],
             a * n[4] + c * n[5] + e, b * n[4] + d * n[5] + f)
    return m


def _apply(m, pt):
    return (m[0] * pt[0] + m[2] * pt[1] + m[4], m[1] * pt[0] + m[3] * pt[1] + m[5])


# parent's distal joint (local offset key) for every child def: the child's origin must land there
_PARENT = {"lat_trunk": ("lat_pelvis", "l5s1"), "lat_thigh": ("lat_pelvis", "hip"), "ant_thigh": ("ant_pelvis", "hip"),
           "lat_head": ("lat_trunk", "neck"), "lat_shank": ("lat_thigh", "knee"), "arm_upper": (None, "shoulder"),
           "lat_foot": ("lat_shank", "ankle"), "arm_fore": ("arm_upper", "elbow"), "arm_hand": ("arm_fore", "wrist"),
           "ant_trunk": ("ant_pelvis", "l5s1"), "ant_head": ("ant_trunk", "neck"), "ant_shank": ("ant_thigh", "knee"),
           "ant_foot": ("ant_shank", "ankle")}


def check_joints(svg, height):
    """Every child's origin (from its emitted <use> transform) coincides with its parent's distal joint, both computed
    through the emitted transforms; returns the worst miss in figure user units."""
    outer = _uses_transform(re.search(r'<g transform="([^"]+)"', svg).group(1))
    uses = [(n, _uses_transform(tr)) for n, tr in re.findall(r'<use href="#hbody_(\w+)" transform="([^"]+)"', svg)]
    worst = 0.0
    for i, (n, m) in enumerate(uses):
        if n not in _PARENT:
            continue
        par, key = _PARENT[n]
        if par is None:                         # the arm hangs from the trunk of either view
            par = "lat_trunk" if any(u[0] == "lat_trunk" for u in uses) else "ant_trunk"
        child_o = _apply(outer, _apply(m, (0, 0)))
        o = OFF[par][key]
        best = min((math.dist(_apply(outer, _apply(pm, (sg * o[0], o[1]))), child_o)
                    for pn, pm in uses if pn == par for sg in (1, -1)), default=1e9)
        worst = max(worst, best)
    return worst * 900 / height


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--build" in sys.argv:
        build(sys.argv[sys.argv.index("--build") + 1])
        sys.exit()
    s = H.Scale(400, 1000, max_h=H.MAX_DISPLAY_H_BODY)
    hgt = 900.0
    for name, kw in POSES.items():
        svg, J = draw("t_", s, pose(**kw), 200, 950, hgt)
        miss = check_joints(svg, hgt)
        assert miss < 1.0, (name, miss)
        for side in ("", "_far"):              # the arm and the trunk share the shoulder
            assert math.dist(J["shoulder" + side], J["shoulder"]) < 1e-6
    for name, kw in POSES_ANT.items():
        svg, J = draw("t_", s, pose_ant(**kw), 200, 950, hgt)
        assert check_joints(svg, hgt) < 1.0, name
    svg, J = draw("t_", s, pose(), 0, 0, hgt)
    print("Standing (lateral), heights / H vs Winter (2009):")
    print(f"{'joint':10s} {'kit':>7s} {'Winter':>7s} {'diff':>7s}")
    for k, w in [("shoulder", 0.818), ("elbow", 0.630), ("wrist", 0.485), ("hip", 0.530), ("knee", 0.285), ("ankle", 0.039)]:
        f = (J["floor_y"] - J[k][1]) / hgt
        print(f"{k:10s} {f:7.3f} {w:7.3f} {100 * (f - w) / w:+6.1f}%")
        assert abs(f - w) / w < 0.03, (k, f, w)
    com = (J["floor_y"] - J["com"][1]) / hgt
    print(f"whole-body COM {com:.3f} H")
    # Winter's table puts the trunk COM midway hip-shoulder; with Winter's own joint heights the sum is 0.577 H.
    # The art's shoulder (+1.2 %) adds ~0.003.  The module texts state 0.55 H (see the report).
    assert 0.55 <= com <= 0.585, com
    print("bytes per segment (source colours):")
    for g, (m, _) in _groups().items():
        print(f"  hbody_{g:12s} {len(m.encode()):7d}")
    n = len(SHARED_DEFS().encode())
    print(f"SHARED_DEFS total {n} bytes")
    assert n <= 90 * 1024, n
    print("lynch_body self-check OK")
