# Math-in-HTML gotchas (read before debugging "why won't this render")

These six traps cost real time on the project this skill came from. Each has a
detector and/or a fix in `scripts/`.

## 1. `$…$$` delimiter mismatch silently scrambles everything downstream
A region opened with a single `$` but closed with `$$` (or vice-versa) flips
MathJax's inline/display state for the **rest of the file**: following prose gets
eaten into "math", equations render as garbage. It is invisible in the source.
**Detect:** `python scripts/checktex.py FILE.html` (also checks `{}`,
`\left/\right`, `\begin/\end`, `\boxed{`).

## 2. A literal `<` inside `$…$` becomes a phantom HTML tag
The HTML parser runs *before* MathJax. `$0<s<L$` is read as text `0` then a
start-tag `<s …>` (strikethrough!) that swallows everything up to the next `>`
— producing **blank regions, unrendered equations, and broken layout**. Same for
`<x`, `</`, etc.
**Detect:** `python scripts/checklt.py FILE.html`
**Fix:** `python scripts/escape_math_lt.py FILE.html` (turns `<`→`\lt`, `>`→`\gt`
inside math only; MathJax renders these identically).

## 3. GitHub README `$…$` math is unreliable
GitHub does support `$…$` in Markdown, but it fails quietly inside `**bold**` /
`*italic*` spans and other contexts — showing raw LaTeX. **For README/Markdown,
write math in Unicode** (Δ, π, θ, ℓ_eg, ½, ·, ², ∼, ≪, →, ∫). Save real MathJax
for the HTML and link to the live page. (HTML files are fine with `$…$`.)

## 4. MathJax renders asynchronously → screenshots lie
A screenshot taken before MathJax finishes shows blank/half-rendered math, and
the browser-extension capture often returns an all-white frame mid-typeset.
**Never verify rendering by eyeballing a screenshot.** Verify the DOM:
`python scripts/verify_dom.py URL_OR_FILE` (asserts 0 `mjx-merror` nodes, 0 stray
`$`, all `#id` links resolve), using headless Chrome with a virtual-time budget.
For preview images use `scripts/shoot.py` (also virtual-time-budgeted).

## 5. Two smaller traps
- **Fragment-only navigation doesn't reload.** Going from `page.html#a` to
  `page.html#b` (or re-opening the same `?`-less URL) may serve a cached DOM.
  Append a cache-buster `?v=2`, `?v=3`, … when re-checking after edits.
- **SVG `<marker>`/`id`s are GLOBAL across the page.** Two figures that both
  define `<marker id="ah">` collide — arrows vanish or point wrong. Give every
  marker/gradient/clip a figure-unique id (`t1ah`, `p2ah`, `eg1g`, …).

## 6. MathJax does not reach inside `<svg><text>` (but does inside `<details>`)
MathJax scans HTML text nodes; it does **not** typeset `$…$` inside an SVG
`<text>` element — the delimited string renders literally (`$L_1$`, or a mangled
fragment). **In SVG labels, write math in Unicode**: subscripts `₁ ₂ ₃ ₛ ₑ ₗ ₕ`
(`&#8321;…`, `&#8347;` s, `&#8337;` e, `&#8343;` l, `&#8341;` h), Greek `λ β θ`,
operators `≤ ≥ ⟂ →`. Keep real `$…$` for the surrounding HTML and the
**figcaption** (which is ordinary HTML and renders normally).
Conversely MathJax **does** typeset inside a *collapsed* `<details>` — the content
is in the DOM, only visually hidden — so a reveal-on-click answer/solution renders
fine. Two ready-made widgets ship in `assets/template.html`: the `.codewrap` +
`copyCode()` copy-button on code blocks, and `<details>` (style `.sol`) for
hide-until-clicked solutions.

## 7. Generating math-bearing HTML from a script? Use raw strings
When you assemble the HTML programmatically (a figure generator, a problem-set
assembler), LaTeX collides with Python's own string escapes and the math mangles
*before* it ever reaches MathJax. `"\tau"` is a **tab**; `"\nu"` a newline;
`"\rho"` a carriage return; `"\varepsilon"` a vertical tab; `"\frac"`, `"\beta"`,
`"\alpha"`, `"\boxed"` (`\b` = backspace) each begin with an escape.
- **Author every math-bearing string as a raw string** — `r"""…"""`. Raw strings
  keep backslashes literal, which is exactly what LaTeX needs.
- **The single-line raw-string quote trap.** `r"...\"secref\"..."` *keeps* the
  backslash, emitting invalid `class=\"secref\"` HTML. Inside a `"`-delimited raw
  string use `'`-quoted HTML attributes, or de-escape at build time
  (`s.replace('\\"','"')` with an `assert '\\"' not in s` after). Triple-quoted
  `r"""…"""` with plain `"` attributes sidesteps it entirely.
- **The shell layer bites the same way — one level up.** Splicing math text through a
  **double-quoted shell command** (`python -c "…$W$…$F_{\text{GRF}}$…"`) is unsafe
  *even with a raw Python string*, because the shell processes `$` and `\` before
  Python runs. `$W`/`$F_…` expand as unset shell vars (→ empty), **deleting the `$…$`
  delimiters and their contents**, and `\t`/`\n`/`\v`/`\f`/`\b` become literal control
  chars (`\text`→`<TAB>ext`). The wreckage is still *valid* TeX — `checktex`'s global
  `$` parity holds (two delimiters destroyed → count stays even) and `verify_dom` sees
  no `mjx-merror` — so both pass while MathJax typesets a swallowed sentence as one
  giant italic math run. (Real case: Module 6 §0 Fig. 1 caption
  `Body weight $W$ … the ground reaction $F_{\text{GRF}}$ launches the body.` rendered
  as a 50-ex-wide run reading `drivesthecompression;thegroundreactionextGRF`.)
  **Rule:** author/patch math-bearing HTML with Write/Edit, or splice from a file/JSON
  using a raw string — never inline it into a `"…"`-quoted shell arg. `checktex.py`
  now **hard-fails** on the leftover control char (TAB/VT/FF/BS/BEL/CR), making this
  and the Python-escape trap above mechanically enforceable rather than advisory.

## 8. Windows Python + Unicode: write and print in UTF-8
Figure generators emit Unicode constantly (`σ ε τ Φ ≈ → ↑ ×`, sub/superscripts). On
Windows the default text encoding is **cp1252**, which crashes on these two operations:
- **Writing a file** — `open(path, "w").write(html_with_unicode)` raises
  `UnicodeEncodeError`. Always pass the encoding: **`open(path, "w", encoding="utf-8")`**
  (and `open(path, encoding="utf-8")` to read). `json.dump` to a file is safe only
  because it escapes non-ASCII by default; don't rely on that for HTML.
- **Printing** — `print("peak ≈ 1.4")` raises the same error on a cp1252 console. Run
  the generator with **`PYTHONIOENCODING=utf-8 python gen.py`**, or keep `print`
  diagnostics ASCII-only. (This does *not* affect the emitted file, only stdout.)
Neither is a rendering bug — the HTML is fine once written; the script just dies before
writing it. Two lines of friction that cost real time across a figure-heavy build.

## Subresource Integrity (the security hook)
Tools may warn that the MathJax `<script>` lacks `integrity="sha384-…"`. Do not
fabricate a hash (a wrong one blocks the script and nothing renders). Either
leave it off for a local/teaching doc, or fetch the real SRI hash for a pinned
MathJax version, or vendor `tex-mml-svg.js` locally to drop the CDN entirely.

## The MathJax config that works (in `assets/template.html`)
```html
<script>
window.MathJax = {
  tex: { inlineMath: [['$','$'],['\\(','\\)']], displayMath: [['$$','$$'],['\\[','\\]']], tags: 'ams' },
  svg: { fontCache: 'global' }
};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-svg.js" async></script>
```
SVG output (not CHTML) keeps the doc self-contained and prints/exports cleanly.
