"""Preview one generator group: standalone page + one PNG per figure + the repo figure gates.

Run:  python -I preview_figs.py 05 plots OUTDIR
Writes OUTDIR/<group>.html (figures in a 52rem light column, like the course page) and
OUTDIR/m05_svg<idx>.png, then runs check_svg, check_overlap and check_frame on the page.
A passing gate is not proof: open every PNG and look at it.
"""
import importlib
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
REPO = KIT.parents[1]
GATES = REPO / ".claude" / "skills" / "rigorous-explainer" / "scripts"
sys.path.insert(0, str(KIT))
sys.stdout.reconfigure(encoding="utf-8")     # gates print τ, θ; the cp1252 console cannot
import house as H  # noqa: E402
from apply_figs import shared_defs  # noqa: E402


def main(mod, group, out):
    out.mkdir(parents=True, exist_ok=True)
    figs = importlib.import_module(f"m{mod}.{group}").FIGS
    body = "".join(f'<h3>svg #{i}</h3><figure id="f{i}" style="margin:0 0 2rem">{b()}</figure>' for i, (_, b) in figs.items())
    page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>m{mod} {group}</title>'
            f'<style>body{{max-width:52rem;margin:2rem auto;padding:0 1.25rem;font-family:Georgia,serif;'
            f'background:#fff;color:#1a1a1a}}figure{{text-align:center}}</style></head><body>{shared_defs(mod)}{body}'
            f'{H.HOVER_JS}{H.FRAMES_JS}</body></html>')
    f = out / f"{group}.html"
    f.write_text(page, encoding="utf-8")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1000, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(f.as_uri())
        pg.wait_for_timeout(300)
        for i in figs:
            pg.locator(f"#f{i}").screenshot(path=str(out / f"m{mod}_svg{i}.png"))
        b.close()
    print("page errors:", errs or "none")
    for g in ("check_svg", "check_overlap", "check_frame"):
        r = subprocess.run([sys.executable, str(GATES / f"{g}.py"), str(f)], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        print(f"== {g} (exit {r.returncode})\n{r.stdout[-3000:]}{r.stderr[-1000:]}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], Path(sys.argv[3]))
