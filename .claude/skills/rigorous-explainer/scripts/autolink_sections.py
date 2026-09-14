#!/usr/bin/env python3
"""Wrap bare section references (§N, §N.M, ranges like §§3-5, §§4.1-4.2) in links.

The number -> anchor-id map is DERIVED FROM THE DOCUMENT ITSELF: headings of the
form  <h2 id="setup">1. Title</h2>  or  <h3 id="onset">4.1 ...</h3>  contribute
"1" -> "#setup", "4.1" -> "#onset", etc. A range/list links to its FIRST number.
Existing <a>...</a> spans are left untouched (so re-running is safe). A .secref
CSS rule is injected if missing. Writes FILE.html.bak.

Usage:  python autolink_sections.py FILE.html
"""
import re, sys, shutil


def main(path):
    s = open(path, encoding="utf-8").read()

    # derive number -> id from id'd headings ("<hN id=..>NUM[. ]Title")
    M = {}
    for m in re.finditer(r'<h[1-6]\s+id="([^"]+)"[^>]*>\s*([A-Za-z]*\d+(?:\.\d+)?)', s):
        hid, num = m.group(1), m.group(2)
        M.setdefault(num, hid)
    if not M:
        print("[autolink_sections] no headings of form '<hN id=..>NUM. Title'; nothing to do.")
        return 0

    if ".secref" not in s and "</style>" in s:
        s = s.replace(
            "</style>",
            "  .secref{ color:var(--accent,#7a1f1f); text-decoration:none; "
            "border-bottom:1px dotted #b98; }\n"
            "  .secref:hover{ border-bottom:1px solid var(--accent,#7a1f1f); }\n</style>",
            1,
        )

    ref = re.compile(r'(§§?|Sections?\s)\s*(\d+(?:\.\d+)?(?:\s*[–,\-]\s*\d+(?:\.\d+)?)*)')
    count = [0]; miss = set()

    # A bare "§N" that is preceded by "Module <k>" belongs to THAT module,
    # not to this page. Linking it to a local anchor produces the worst
    # defect this repo can make: check_links passes because the anchor
    # resolves, and the reference silently points at the wrong book.
    # (Found 2026-09-09 in module00.html: "Module 4 §2" pointed at Module 0's
    # own §2, and "Module 5 §3" at Module 0's §3.)
    foreign = re.compile(r'Module(?:&nbsp;|\s)+\d+\s*[(;,]?\s*$')
    skipped = [0]

    def repl(m):
        if foreign.search(m.string[max(0, m.start() - 40):m.start()]):
            skipped[0] += 1; return m.group(0)
        nums = m.group(2)
        first = re.match(r'\d+(?:\.\d+)?', nums).group(0)
        if first not in M:
            miss.add(first); return m.group(0)
        count[0] += 1
        return f'<a class="secref" href="#{M[first]}">{m.group(0)}</a>'

    # split on existing anchors; only edit text OUTSIDE them (even indices)
    # <svg> is excluded too (added 2026-09-10, found by rev5):
    # eight SVG <text> elements had acquired an <a> element,
    # which MathJax cannot typeset and no generator wrote.
    # <pre> blocks are excluded as well as existing anchors. Added
    # 2026-09-10: without it this script rewrote "Section 6" inside
    # a Python docstring into an <a class="secref"> link, which
    # corrupts the code a reader is told to run and breaks
    # check_code's tokenizer.
    parts = re.split(r'(<a\b[^>]*>.*?</a>|<pre\b[^>]*>.*?</pre>|<svg\b[^>]*>.*?</svg>)',
                     s, flags=re.S)
    for k in range(0, len(parts), 2):
        parts[k] = ref.sub(repl, parts[k])
    s = "".join(parts)

    shutil.copy(path, path + ".bak")
    open(path, "w", encoding="utf-8").write(s)
    print(f"[autolink_sections] {path}: wrapped {count[0]} ref(s); "
          f"{len(M)} sections in map; unmapped firsts: {sorted(miss)}")
    if skipped[0]:
        print(f"  left {skipped[0]} cross-module ref(s) unlinked "
              f"(preceded by 'Module N' — they belong to that module)")
    print(f"  backup at {path}.bak")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python autolink_sections.py FILE.html"); sys.exit(2)
    sys.exit(main(sys.argv[1]))
