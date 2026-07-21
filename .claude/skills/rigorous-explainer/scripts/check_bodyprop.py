#!/usr/bin/env python3
"""Flag human figures whose LIMBS are far thinner than their HEAD implies —
"a template-size head bolted onto hairline stick legs" (HARD, exit 1).

The bug this exists to catch (it shipped in Module 8): a chunky-pictogram body
(big head, thick torso) was added on top of pre-existing schematic stick legs,
and the legs were deliberately left as 15px hairlines. The result is a figure
that matches NEITHER the old style nor the template — a chunky bust on sticks.
Every other gate passed it: checktex/checklt see no math, check_svg sees valid
markup, check_overlap sees no label on a curve, check_frame sees no clipping,
and check_probfig only asks "is SOME recognizable entity drawn?" — which a
thin-legged body answers yes to. Nothing in the loop measured PROPORTION, so
the only net was a human eye, and a sampled review missed ~20 problem figures.

How: load the page in headless Chrome; per <svg class="setupfig">, take the
head radius R (largest circle filled with a head gradient — note small joint
spheres also use it, so max wins) and every real limb segment (a rect filled
with a limb gradient, or a thick limb-coloured <line>). A segment counts as a
limb only if its LENGTH > R, which excludes fingers/knuckles/short details.
For each, thickness = the segment's short dimension (or the line's
stroke-width). Flag the figure when the THINNEST real limb is under
RATIO * R.

Calibration: in the approved template the thinnest limb (forearm, 0.34U) sits
against a head radius of 0.55U -> ratio 0.62; thighs are 0.52/0.55 = 0.95. The
shipped defect measured 15/49.5 = 0.30. Default RATIO 0.45 sits between them.

Also reports (advisory) a figure that has a template-size head but NO limb
segment at all — a floating bust.

Usage:  python check_bodyprop.py FILE [--chrome PATH] [--ratio 0.45]
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
  var RATIO=__RATIO__, ASPECT=__ASPECT__;
  // gradients that mean "this is flesh": head vs limb
  var HEAD=/b_head|sph[A-Za-z0-9_]*|head/i, LIMB=/b_limb|cyl[A-Za-z0-9_]*|limb/i;
  // warm limb stroke colours used for schematic legs drawn as <line>
  var LIMBSTROKE=/^#(c98a5e|b5744b|e6bd99|f3d7bd|a08b63|c9a227|bf8040)$/i;
  var out=[];
  document.querySelectorAll('svg.setupfig').forEach(function(svg,fi){
    // --- head radius: largest circle painted with a head gradient
    var R=0;
    svg.querySelectorAll('circle').forEach(function(c){
      var f=c.getAttribute('fill')||'';
      if(HEAD.test(f)){ var r=parseFloat(c.getAttribute('r')||0); if(r>R) R=r; }
    });
    if(R<12) return;                    // no real head -> not a body figure
    // --- real limb segments
    var segs=[];
    svg.querySelectorAll('rect').forEach(function(el){
      var f=el.getAttribute('fill')||'';
      if(!LIMB.test(f)) return;
      var bb; try{ bb=el.getBBox(); }catch(e){ return; }
      var len=Math.max(bb.width,bb.height), th=Math.min(bb.width,bb.height);
      if(len>R) segs.push({len:len,th:th,kind:'rect'});
    });
    svg.querySelectorAll('line').forEach(function(el){
      var st=(el.getAttribute('stroke')||'').trim();
      var w=parseFloat(el.getAttribute('stroke-width')||0);
      if(!LIMBSTROKE.test(st) || w<3) return;
      var x1=parseFloat(el.getAttribute('x1')||0),y1=parseFloat(el.getAttribute('y1')||0);
      var x2=parseFloat(el.getAttribute('x2')||0),y2=parseFloat(el.getAttribute('y2')||0);
      var len=Math.hypot(x2-x1,y2-y1);
      if(len>R) segs.push({len:len,th:w,kind:'line'});
    });
    var lab=(svg.getAttribute('aria-label')||('figure '+(fi+1))).slice(0,54);
    if(!segs.length){ out.push({fig:lab,R:Math.round(R),none:true}); return; }
    // Two independent defects, each on its own scale-free rule:
    //  (a) ASPECT  - a limb far thinner than its own length (a hairline stick).
    //      Template limbs run thickness/length 0.23 (forearm) .. 0.43 (thigh);
    //      the Module-8 compass legs measured 15/164 = 0.09.
    //  (b) RATIO   - a limb too thin for THIS body's head (mis-scaled part).
    var worst=null, rule=null;
    segs.forEach(function(s){
      var asp=s.th/s.len;
      if(asp < ASPECT && (!worst || asp < worst.th/worst.len)){ worst=s; rule='aspect'; }
    });
    if(!worst){
      segs.forEach(function(s){
        if(s.th < RATIO*R && (!worst || s.th < worst.th)){ worst=s; rule='head'; }
      });
    }
    if(worst){
      out.push({fig:lab,R:Math.round(R),th:Math.round(worst.th*10)/10,
                len:Math.round(worst.len),kind:worst.kind,rule:rule,
                asp:Math.round(worst.th/worst.len*100)/100,
                ratio:Math.round(worst.th/R*100)/100});
    }
  });
  var d=document.createElement('div');d.id='__bodyprop__';
  d.textContent=btoa(unescape(encodeURIComponent(JSON.stringify(out))));
  document.body.appendChild(d);
})();
</script>"""


def main(argv):
    target = argv[0]
    if re.match(r'^https?://', target):
        print("[check_bodyprop] pass a LOCAL file, not a URL"); return 2
    ratio = float(argv[argv.index("--ratio") + 1]) if "--ratio" in argv else 0.55
    aspect = float(argv[argv.index("--aspect") + 1]) if "--aspect" in argv else 0.18
    chrome = find_chrome(argv[argv.index("--chrome") + 1] if "--chrome" in argv else None)
    if not chrome:
        print("[check_bodyprop] no Chrome/Edge found; pass --chrome PATH"); return 2
    src = open(target, encoding="utf-8").read()
    probe = INJECT.replace("__RATIO__", repr(ratio)).replace("__ASPECT__", repr(aspect))
    html2 = src.replace("</body>", probe + "\n</body>", 1) if "</body>" in src else src + probe
    tmpd = tempfile.mkdtemp()
    tmpf = os.path.join(tmpd, "__chk.html")
    open(tmpf, "w", encoding="utf-8").write(html2)
    try:
        r = subprocess.run(
            [chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
             f"--user-data-dir={os.path.join(tmpd,'ud')}", "--virtual-time-budget=6000",
             "--dump-dom", "file:///" + tmpf.replace("\\", "/")],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=120)
    except Exception as e:
        print("[check_bodyprop] chrome failed:", e); return 2
    m = re.search(r'id="__bodyprop__"[^>]*>([A-Za-z0-9+/=]*)<', r.stdout or "")
    if not m:
        print("[check_bodyprop] probe did not run (load failed?)"); return 2
    try:
        data = json.loads(base64.b64decode(m.group(1)).decode("utf-8")) if m.group(1) else []
    except Exception as e:
        print("[check_bodyprop] could not parse probe report:", e); return 2
    bust = [o for o in data if o.get("none")]
    # aspect = HARD (scale-free, needs no head, cannot mistake anatomy for a head).
    # head-ratio = ADVISORY: a circle painted with a head gradient is not always a
    # person's head — e.g. the humeral-head BALL in Module 11's glenohumeral detail
    # panel (r=60) made a legitimate forearm look "too thin". Judgement call, so it
    # must never block the build.
    thin = [o for o in data if o.get("rule") == "aspect"]
    adv = [o for o in data if o.get("rule") == "head"]
    if not data:
        print(f"[check_bodyprop] {os.path.basename(target)}: every body figure's "
              f"limbs are template-thick (aspect >= {aspect}, >= {ratio} x head r)")
        return 0
    if thin:
        print(f"[check_bodyprop] {len(thin)} figure(s) with a HAIRLINE LIMB "
              f"(thickness/length < {aspect}) — HARD:")
        for o in thin:
            print(f'  - "{o["fig"]}..."')
            print(f'      {o["th"]}px thick x {o["len"]}px long (<{o["kind"]}>) '
                  f'-> thickness/length={o["asp"]} (template 0.23-0.43)')
            print(f'      fix: derive U from the limb (a full hip->foot leg of '
                  f'length L => U=L/2.35) and thicken to 0.52*U '
                  f'(~{round(0.22*o["len"])}px here); size the head/torso from '
                  f'the same U so the body matches its own limbs')
    if adv:
        print(f"[check_bodyprop] {len(adv)} figure(s) with a limb thin relative to "
              f"a head-gradient circle (< {ratio} x its radius; ADVISORY — that "
              f"circle may be anatomy, not a head. Eyeball it):")
        for o in adv:
            print(f'  - "{o["fig"]}..."  {o["th"]}px thick ({o["len"]}px long) vs '
                  f'r={o["R"]} -> ratio={o["ratio"]}')
    if bust:
        print(f"[check_bodyprop] {len(bust)} figure(s) with a head but NO limb "
              f"segment (floating bust; advisory):")
        for o in bust:
            print(f'  - "{o["fig"]}..."  head r={o["R"]}')
    return 1 if thin else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    sys.exit(main(sys.argv[1:]))
