#!/usr/bin/env python3
"""Flag figure labels that overlap plotted curves or dashed reference lines.

The chronic figure bug: curves/lines come from computed coords but <text> labels
are hand-placed, so a label lands on a curve, or a dashed reference line strikes
through it. The white halo makes that *legible* but does not remove the overlap.
This enforces the "labels must clear the curves" rule mechanically instead of by
eye.

How: load the page in headless Chrome, inject a probe that (in-page) measures
every <text> in each <svg class="setupfig"> against every <polyline> (a plotted
curve) and every DASHED <line> (mean / sigma_inf / tau reference lines). It uses
getBoundingClientRect + getScreenCTM, so rotated axis titles and %-width scaling
are handled correctly. SOLID lines (axes, gridlines, ticks, arrows, leader lines)
are intentionally skipped, so a tick label beside an axis and a label's own leader
are not false-flagged. The probe base64-encodes its report into a <div> that
--dump-dom serializes; this script decodes it.

Usage:  python check_overlap.py FILE [--chrome PATH]
Exits 1 if any label overlaps a curve or a dashed reference line.
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


INJECT = r"""<script>
(function(){
  function ptsOf(el){return (el.getAttribute('points')||'').trim().split(/\s+/).filter(Boolean).map(function(p){var a=p.split(',');return [parseFloat(a[0]),parseFloat(a[1])];});}
  var out=[];
  document.querySelectorAll('svg.setupfig').forEach(function(svg,fi){
    var label=(svg.getAttribute('aria-label')||('figure '+fi)).slice(0,60);
    var ctm=svg.getScreenCTM(); if(!ctm) return;
    function toScreen(x,y){var p=svg.createSVGPoint();p.x=x;p.y=y;var s=p.matrixTransform(ctm);return [s.x,s.y];}
    var samples=[];
    function pushSeg(x1,y1,x2,y2,kind){var d=Math.hypot(x2-x1,y2-y1),n=Math.max(1,Math.ceil(d/1.5));for(var k=0;k<=n;k++){samples.push([x1+(x2-x1)*k/n,y1+(y2-y1)*k/n,kind]);}}
    svg.querySelectorAll('polyline').forEach(function(pl){var pts=ptsOf(pl).map(function(p){return toScreen(p[0],p[1]);});for(var i=0;i+1<pts.length;i++){pushSeg(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1],'curve');}});
    svg.querySelectorAll('line').forEach(function(l){var da=l.getAttribute('stroke-dasharray')||getComputedStyle(l).strokeDasharray;if(!da||da==='none')return;var ux1=+l.getAttribute('x1'),uy1=+l.getAttribute('y1'),ux2=+l.getAttribute('x2'),uy2=+l.getAttribute('y2');if(Math.hypot(ux2-ux1,uy2-uy1)<50)return;var s=toScreen(ux1,uy1),e=toScreen(ux2,uy2);pushSeg(s[0],s[1],e[0],e[1],'dashed');});
    if(!samples.length) return;
    var inv=ctm.inverse();
    svg.querySelectorAll('text').forEach(function(tx){var r=tx.getBoundingClientRect();if(r.width===0)return;var kinds={},hp=null;for(var i=0;i<samples.length;i++){var x=samples[i][0],y=samples[i][1];if(x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom){kinds[samples[i][2]]=1;if(!hp){var q=svg.createSVGPoint();q.x=x;q.y=y;var u=q.matrixTransform(inv);hp=[Math.round(u.x),Math.round(u.y)];}}}if(hp){var bb=tx.getBBox();out.push({fig:label,text:tx.textContent.trim().replace(/\s+/g,' ').slice(0,48),box:[Math.round(bb.x),Math.round(bb.y),Math.round(bb.width),Math.round(bb.height)],hit:hp,kinds:Object.keys(kinds)});}});
  });
  var d=document.createElement('div');d.id='__overlap__';d.textContent=btoa(unescape(encodeURIComponent(JSON.stringify(out))));document.body.appendChild(d);
})();
</script>"""


def main(argv):
    target = argv[0]
    if re.match(r'^https?://', target):
        print("[check_overlap] pass a LOCAL file (the probe is injected into it), not a URL"); return 2
    chrome = find_chrome(argv[argv.index("--chrome") + 1] if "--chrome" in argv else None)
    if not chrome:
        print("[check_overlap] no Chrome/Edge found; pass --chrome PATH"); return 2
    src = open(target, encoding="utf-8").read()
    html2 = src.replace("</body>", INJECT + "\n</body>", 1) if "</body>" in src else src + INJECT
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
        print("[check_overlap] chrome failed:", e); return 2
    dom = r.stdout or ""
    m = re.search(r'id="__overlap__"[^>]*>([A-Za-z0-9+/=]*)<', dom)
    if not m:
        print("[check_overlap] probe did not run (no report div; load failed?)"); return 2
    try:
        data = json.loads(base64.b64decode(m.group(1)).decode("utf-8")) if m.group(1) else []
    except Exception as e:
        print("[check_overlap] could not parse probe report:", e); return 2
    if not data:
        print("[check_overlap] 0 label/curve overlaps"); return 0
    print(f"[check_overlap] {len(data)} label(s) overlap a curve or dashed reference line:")
    for o in data:
        b = o.get("box"); h = o.get("hit"); k = ",".join(o.get("kinds", []))
        loc = f" box(x,y,w,h)={b} hits {k} at {h}" if b else ""
        print(f'  - "{o["text"]}"  [{o["fig"][:30]}...]{loc}')
    return 1


if __name__ == "__main__":
    if not sys.argv[1:]:
        print("usage: python check_overlap.py FILE [--chrome PATH]"); sys.exit(2)
    sys.exit(main(sys.argv[1:]))
