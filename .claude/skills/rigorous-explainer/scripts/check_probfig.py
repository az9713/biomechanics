#!/usr/bin/env python3
"""check_probfig.py FILE.html  — problem-set (C/D/K) figures must lead with a
recognizable Tier-2 entity, not be a bare FBD / arrows / chart (Layer 3 / Layer 1).

WHY THIS EXISTS.  The hardening loop proves labels don't sit on curves
(check_overlap) and viewBoxes aren't wasteful (check_frame), but nothing in it
proves a figure is *interpretable*. Module 8's C/D/K figures regressed to flat
line/arrow/bar schematics with no recognizable body/foot/leg — geometry puzzles —
and every mechanical check still passed. This advisory rides in the loop as a
concrete prompt for the semantic audit the skill otherwise leaves as prose.

HEURISTIC (advisory — it cannot judge full interpretability, only narrow the
candidates for the manual audit). A problem figure is *suspect* only when it has
BOTH:
  - no recognizable Tier-2 entity  (no b_limb/b_sph/b_head gradient, no silhouette
    <path>), AND
  - no real plot  (no pair of long axis lines, and no data polyline / many bars).
That combination means the figure is neither a drawn body/foot/leg NOR a labelled
chart/portrait — it is probably floating arrows, a bare circle/glyph, or text
boxes (Module 8's C6 vectors-at-a-point, C7/D7 bare circle, D3 text boxes). A
correct flat plot (phase portrait, cost curve, convergence, sweep) has axes and a
curve, so it is NOT flagged — abstraction is fine there. Redraw the flagged ones to
lead with the recognizable entity and anchor every arrow to the structure it acts
on (Layer 1 / Layer 3).

NEVER fails the build (advisory). Prints one line per flagged problem figure.
"""
import re
import sys

TIER2 = ("url(#b_limb)", "url(#b_sph)", "url(#b_head)", "url(#b_bone)",
         "url(#cyl", "url(#sph")


def has_entity(fig):
    if any(g in fig for g in TIER2):
        return True
    # a hand-drawn silhouette: a <path> with several curve commands
    paths = re.findall(r"<path\b[^>]*\bd=\"([^\"]+)\"", fig)
    return any(p.count("C") + p.count("c") >= 3 for p in paths)


def has_plot(fig):
    # a data polyline (a computed curve) or several bars = a real chart
    polylines = re.findall(r"<polyline\b[^>]*\bpoints=\"([^\"]+)\"", fig)
    if any(pl.count(",") >= 6 for pl in polylines):
        return True
    if len(re.findall(r"<rect\b", fig)) >= 3:          # bar chart
        return True
    # a pair of axis lines: one near-horizontal + one near-vertical long <line>
    horiz = vert = False
    for m in re.finditer(r"<line\b[^>]*\bx1=\"([\d.]+)\"[^>]*\by1=\"([\d.]+)\""
                         r"[^>]*\bx2=\"([\d.]+)\"[^>]*\by2=\"([\d.]+)\"", fig):
        x1, y1, x2, y2 = map(float, m.groups())
        if abs(y2 - y1) < 4 and abs(x2 - x1) > 80:
            horiz = True
        if abs(x2 - x1) < 4 and abs(y2 - y1) > 60:
            vert = True
    return horiz and vert


def main(path):
    s = open(path, encoding="utf-8").read()
    probs = re.split(r'(?=<div class="prob">)', s)
    probs = [p for p in probs if p.startswith('<div class="prob">')]
    flagged = []
    total = 0
    for block in probs:
        if "<figure" not in block:
            continue
        total += 1
        pid = re.search(r"<b>\s*([CDK]?\d+)\.", block)
        pid = pid.group(1) if pid else "?"
        fig = re.search(r"<figure.*?</figure>", block, re.S)
        fig = fig.group(0) if fig else ""
        if not has_entity(fig) and not has_plot(fig):
            flagged.append(pid)
    if flagged:
        print(f"[check_probfig] {path}: {len(flagged)} of {total} problem "
              f"figure(s) are neither a drawn entity nor a labelled plot — likely "
              f"floating arrows / bare glyph / text (verify Layer 1 + Layer 3):")
        print("   " + ", ".join(flagged))
    else:
        print(f"[check_probfig] {path}: {total} problem figure(s); each is a "
              f"recognizable entity or a real plot.")
    return 0  # advisory


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: check_probfig.py FILE.html")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
