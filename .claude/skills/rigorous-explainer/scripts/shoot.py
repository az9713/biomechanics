#!/usr/bin/env python3
"""Reliable screenshot of a rendered page via headless Chrome.

Far more dependable than browser-extension capture (which returns blank frames
while MathJax is still typesetting). Uses --virtual-time-budget so async JS /
MathJax finish before the shot. Good for a README preview image.

Usage:  python shoot.py URL_OR_FILE OUTPUT.png [--size WxH] [--wait MS] [--chrome PATH]
Defaults: --size 1280x820  --wait 9000
"""
import subprocess, sys, re, os, shutil, tempfile

CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "google-chrome", "chromium", "chromium-browser", "chrome",
]


def find_chrome(override=None):
    if override:
        return override
    for c in CANDIDATES:
        if c.endswith(".exe") or os.sep in c:
            if os.path.exists(c):
                return c
        elif shutil.which(c):
            return shutil.which(c)
    return None


def to_url(t):
    if re.match(r'^https?://', t):
        return t
    return "file:///" + os.path.abspath(t).replace("\\", "/")


def opt(argv, flag, default):
    return argv[argv.index(flag) + 1] if flag in argv else default


def main(argv):
    if len(argv) < 2:
        print("usage: python shoot.py URL_OR_FILE OUTPUT.png [--size WxH] [--wait MS] [--chrome PATH]")
        return 2
    target, out = argv[0], argv[1]
    size = opt(argv, "--size", "1280x820").replace("x", ",")
    wait = opt(argv, "--wait", "9000")
    chrome = find_chrome(opt(argv, "--chrome", None))
    if not chrome:
        print("[shoot] no Chrome/Edge found; pass --chrome PATH"); return 2
    tmp = tempfile.mkdtemp()
    try:
        subprocess.run(
            [chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
             "--force-color-profile=srgb", f"--user-data-dir={tmp}",
             f"--window-size={size}", f"--virtual-time-budget={wait}",
             f"--screenshot={os.path.abspath(out)}", to_url(target)],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    except Exception as e:
        print("[shoot] chrome failed:", e); return 2
    if os.path.exists(out) and os.path.getsize(out) > 1000:
        print(f"[shoot] wrote {out} ({os.path.getsize(out)} bytes)")
        return 0
    print("[shoot] screenshot missing or too small (load failed?)")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
