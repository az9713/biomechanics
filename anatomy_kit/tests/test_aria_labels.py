"""Fail if problem figures still use placeholder aria-labels (§10.1)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PLACEHOLDER = re.compile(
    r"^(?:"
    r"problem figure(?:\s|$|:)"
    r"|upgraded problem figure"
    r"|(?:C|D|K)\d+\s+figure\b"
    r")",
    re.I,
)


def test_no_placeholder_problem_aria_labels():
    bad = []
    for p in sorted(ROOT.glob("module*.html")):
        html = p.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'aria-label="([^"]*)"', html):
            lab = m.group(1).strip()
            if "clipboard" in lab.lower():
                continue
            if PLACEHOLDER.match(lab):
                # allow only if already upgraded with long descriptive content after "figure X:"
                if re.match(r"^(?:C|D|K)\d+\s+figure\b", lab, re.I) and len(lab) > 100:
                    continue
                if lab.lower().startswith("problem figure:") and len(lab) > 80:
                    # "Problem figure: body pose" is bad; long recovered description might be ok
                    if lab.lower() in (
                        "problem figure: body pose",
                        "problem figure: body pose, force vectors",
                        "problem figure: computed plot",
                        "problem figure: problem schematic",
                        "problem figure: force vectors",
                        "problem figure: bone structure, computed plot",
                        "problem figure: bone structure, force vectors",
                        "problem figure: bone structure",
                        "problem figure: balance geometry",
                    ) or re.match(r"^problem figure: (body|plot|schematic|force|bone)", lab, re.I):
                        bad.append(f"{p.name}: {lab[:100]}")
                        continue
                    continue
                bad.append(f"{p.name}: {lab[:100]}")
    assert not bad, "placeholder aria-labels remain:\n" + "\n".join(bad[:30])


if __name__ == "__main__":
    test_no_placeholder_problem_aria_labels()
    print("OK no placeholder problem aria-labels")
