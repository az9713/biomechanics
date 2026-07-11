#!/usr/bin/env python3
"""Escape literal < and > inside $...$ / $$...$$ math to \\lt and \\gt.

Fixes the phantom-tag bug found by checklt.py. Only touches characters inside
math delimiters; HTML markup and prose are untouched. Writes FILE.html.bak.

Usage:  python escape_math_lt.py FILE.html
"""
import sys, shutil


def main(path):
    s = open(path, encoding="utf-8").read()
    out = []; state = "text"; i = 0; n = 0
    while i < len(s):
        if s[i:i + 2] == "$$":
            out.append("$$")
            state = "d" if state == "text" else ("text" if state == "d" else state)
            i += 2; continue
        ch = s[i]
        if ch == "$":
            out.append("$")
            state = "i" if state == "text" else ("text" if state == "i" else state)
            i += 1; continue
        if state in ("i", "d") and ch == "<":
            out.append(r"\lt "); n += 1; i += 1; continue
        if state in ("i", "d") and ch == ">":
            out.append(r"\gt "); n += 1; i += 1; continue
        out.append(ch); i += 1
    if state != "text":
        print("[escape_math_lt] WARNING: delimiter imbalance detected; run checktex.py "
              "first. No changes written.")
        return 1
    shutil.copy(path, path + ".bak")
    open(path, "w", encoding="utf-8").write("".join(out))
    print(f"[escape_math_lt] {path}: replaced {n} char(s) inside math; backup at {path}.bak")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python escape_math_lt.py FILE.html"); sys.exit(2)
    sys.exit(main(sys.argv[1]))
