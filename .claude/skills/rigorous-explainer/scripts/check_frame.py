#!/usr/bin/env python3
"""Flag figures whose content does not fit their viewBox — clipped past an edge
(HARD, exit 1) or floating in a much larger box (wasted margin, advisory).

Two bugs, one measurement (rendered getBBox vs the declared viewBox):

* CLIPPING (hard) — content extends *past* a viewBox edge, so the browser crops it.
  The one that shipped: 13 Module-10 problem figures placed an x-axis title at
  y0+30 = 182 inside a viewBox="0 0 300 180", so the bottom line of text ("gain kₚ",
  "placement error e (m)", "delay τ (s)") rendered below the box and was cut off on
  every browser. Every other check passed — check_svg only validates viewBox *arity*,
  check_overlap only tests label-vs-curve hits *inside* the render, verify_dom only
  checks MathJax/links, and this script previously only looked at *wasted* margin, so
  content spilling *out* of the box was invisible to the whole loop until a human
  spotted it. Clipping is never intentional, so it now fails the build.

* WASTED MARGIN (advisory) — the viewBox is a round number bigger than the drawing,
  so content sits in one corner with an empty band (a real one: a pennation diagram
  in the lower third of a 0 0 460 250 box, ~56% blank above it). A judgement call to
  retighten, so advisory as before.

How: load the page in headless Chrome and, per <svg class="setupfig">, compare
svg.getBBox() (the tight user-space box of all rendered content — it accounts for
transforms, unlike a static coordinate scrape) against the viewBox. If any single
side's empty margin exceeds THRESH of that dimension, report it. getBBox ignores
stroke width / markers / filters, so a few px of halo or arrowhead near an edge do
not trip it; the threshold is set well above that noise.

Advisory by design (exit 0): some figures are legitimately asymmetric, and the fix
(retighten the viewBox min-y / height) is a judgement call, not a hard gate. Run it
in the hardening loop and retighten any figure it names.

Usage:  python check_frame.py FILE [--chrome PATH] [--thresh 0.20]
"""
import subprocess, sys, re, os, shutil, tempfile, base64, json
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

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


# THRESH (wasted-margin) and CLIP_TOL (clip tolerance, px) are templated in.
INJECT = r"""<script>
(function(){
  var THRESH=__THRESH__, CLIP=__CLIP__;
  var out=[];
  document.querySelectorAll('svg.setupfig').forEach(function(svg,fi){
    var raw=(svg.getAttribute('viewBox')||'').trim().split(/[\s,]+/).map(Number);
    if(raw.length!==4 || raw.some(function(v){return isNaN(v);})) return;  // arity is check_svg's job
    var bb; try{ bb=svg.getBBox(); }catch(e){ return; }
    if(!bb || bb.width<1 || bb.height<1) return;                          // empty / defs-only
    var mnx=raw[0],mny=raw[1],w=raw[2],h=raw[3];
    // signed margin per side: >0 empty band, <0 content spills past the edge.
    var L=(bb.x-mnx), R=((mnx+w)-(bb.x+bb.width)), T=(bb.y-mny), B=((mny+h)-(bb.y+bb.height));
    var rec={fig:(svg.getAttribute('aria-label')||('figure '+fi)).slice(0,58),
      vb:[mnx,mny,w,h].map(Math.round),
      content:[Math.round(bb.x),Math.round(bb.y),Math.round(bb.width),Math.round(bb.height)],
      pct:{L:Math.round(L/w*100),R:Math.round(R/w*100),T:Math.round(T/h*100),B:Math.round(B/h*100)}};
    // CLIP (hard): any side where content spills past the viewBox by > CLIP px.
    // getBBox excludes stroke/markers, so CLIP tolerates a few px of halo/arrowhead.
    var over=Math.max(-L,-R,-T,-B);          // px past the worst edge (>0 = clipped)
    if(over>CLIP){ rec.clip=Math.round(over); out.push(rec); return; }
    // WASTED MARGIN (advisory): worst single empty side exceeds THRESH.
    var worst=Math.max(L/w,R/w,T/h,B/h);
    if(worst>THRESH){ rec.margin=Math.round(worst*100); out.push(rec); }
  });
  var d=document.createElement('div');d.id='__frame__';d.textContent=btoa(unescape(encodeURIComponent(JSON.stringify(out))));document.body.appendChild(d);
})();
</script>"""


def main(argv):
    target = argv[0]
    if re.match(r'^https?://', target):
        print("[check_frame] pass a LOCAL file (the probe is injected into it), not a URL"); return 2
    thresh = float(argv[argv.index("--thresh") + 1]) if "--thresh" in argv else 0.20
    clip = float(argv[argv.index("--clip") + 1]) if "--clip" in argv else 2.0
    chrome = find_chrome(argv[argv.index("--chrome") + 1] if "--chrome" in argv else None)
    if not chrome:
        print("[check_frame] no Chrome/Edge found; pass --chrome PATH"); return 2
    src = open(target, encoding="utf-8").read()
    probe = INJECT.replace("__THRESH__", repr(thresh)).replace("__CLIP__", repr(clip))
    html2 = src.replace("</body>", probe + "\n</body>", 1) if "</body>" in src else src + probe
    tmpd = tempfile.mkdtemp()
    tmpf = os.path.join(tmpd, "__chk.html")
    open(tmpf, "w", encoding="utf-8").write(html2)
    try:
        r = subprocess.run(
            [chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
             f"--user-data-dir={os.path.join(tmpd,'ud')}", "--virtual-time-budget=6000",
             "--dump-dom", "file:///" + tmpf.replace("\\", "/")],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    except Exception as e:
        print("[check_frame] chrome failed:", e); return 2
    dom = r.stdout or ""
    m = re.search(r'id="__frame__"[^>]*>([A-Za-z0-9+/=]*)<', dom)
    if not m:
        print("[check_frame] probe did not run (no report div; load failed?)"); return 2
    try:
        data = json.loads(base64.b64decode(m.group(1)).decode("utf-8")) if m.group(1) else []
    except Exception as e:
        print("[check_frame] could not parse probe report:", e); return 2
    clips = [o for o in data if "clip" in o]
    wasted = [o for o in data if "margin" in o]
    if not data:
        print(f"[check_frame] 0 figures clipped or with wasted margin "
              f"(>{int(thresh*100)}%)"); return 0

    def suggest(o):
        # tightened viewBox = content + ~5% pad. For a CLIP we must GROW the box to
        # contain the content, so do not clamp to the original; for wasted margin we
        # only ever crop, so clamp to the original box.
        vb = o["vb"]; c = o["content"]
        padx = max(4, round(0.05 * c[2])); pady = max(4, round(0.05 * c[3]))
        if "clip" in o:
            x0, y0 = c[0] - padx, c[1] - pady
            x1, y1 = c[0] + c[2] + padx, c[1] + c[3] + pady
        else:
            x0 = max(vb[0], c[0] - padx); y0 = max(vb[1], c[1] - pady)
            x1 = min(vb[0] + vb[2], c[0] + c[2] + padx)
            y1 = min(vb[1] + vb[3], c[1] + c[3] + pady)
        return f'{x0} {y0} {x1 - x0} {y1 - y0}'

    if clips:
        print(f"[check_frame] {len(clips)} figure(s) CLIPPED — content spills past the "
              f"viewBox edge and is cut off (HARD):")
        for o in clips:
            p = o["pct"]; vb = o["vb"]; c = o["content"]
            side = min(("L", p["L"]), ("R", p["R"]), ("T", p["T"]), ("B", p["B"]),
                       key=lambda kv: kv[1])[0]
            print(f'  - "{o["fig"][:40]}..."  clipped ~{o["clip"]}px past the '
                  f'{side} edge')
            print(f'      viewBox={vb}  content={c}  margins L/R/T/B='
                  f'{p["L"]}%/{p["R"]}%/{p["T"]}%/{p["B"]}% (negative = spills out)')
            print(f'      fix: enlarge to viewBox="{suggest(o)}" (or move the '
                  f'element inward)')
    if wasted:
        print(f"[check_frame] {len(wasted)} figure(s) with a viewBox larger than their "
              f"content (margin >{int(thresh*100)}%; advisory):")
        for o in wasted:
            p = o["pct"]; vb = o["vb"]; c = o["content"]
            print(f'  - "{o["fig"][:40]}..."')
            print(f'      margins L/R/T/B = {p["L"]}%/{p["R"]}%/{p["T"]}%/{p["B"]}%   '
                  f'viewBox={vb}  content={c}')
            print(f'      suggest viewBox="{suggest(o)}"')
    return 1 if clips else 0   # clipping fails the build; wasted margin is advisory


if __name__ == "__main__":
    if not sys.argv[1:]:
        print("usage: python check_frame.py FILE [--chrome PATH] [--thresh 0.20]"); sys.exit(2)
    sys.exit(main(sys.argv[1:]))
