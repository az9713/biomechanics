#!/usr/bin/env python3
"""Provenance gate: no borrowed constitutive parameter may enter a boxed result
without saying where it came from.

The contract this implements is written in the course repo at
`chemistry-audit-and-plan.md` §2.2c (decisions of 2026-09-09). Read that first;
this file is only its implementation. In one paragraph:

A textbook is allowed to borrow a number from a laboratory. It is not allowed to
borrow one silently, because then the reader cannot tell which parts of the book
are earned and which are quoted. So every *gated* parameter must carry, once per
module, a marker declaring one of three states:

    derived   -- this course derives it from chemistry or cell biology
    module0   -- Module 0 derives it; the marker links there
    measured  -- nobody derives it here, and the marker says why

    <span class="prov" data-sym="E" data-state="measured">measured, not derived:
    the composite modulus of cortical bone is reported from mechanical test.</span>

WHAT IS GATED, and why it is split in two.  "A units-bearing property of a tissue
or material, not a geometry, a body mass, a universal constant, or a computed
output" is a human judgement; no regular expression decides it. So:

  * the MECHANICAL half (this script) finds every `symbol REL number UNIT`
    assignment inside a boxed result, where UNIT is a \\mathrm{} or \\text{} group;
  * the JUDGEMENT half is GATED below -- an explicit INCLUSION list of canonical
    symbols, written by reading `--inventory` output, never guessed.

Inclusion and not exclusion, because this course's symbol namespace collides: `T`
is torque in Module 2 and temperature in chemistry, `a` is acceleration and Hill's
constant, `F` is force and Faraday, `mu` is friction and chemical potential, `k`
is the remodeling gain and a rate constant. An exclusion list silently un-gates
the interesting cases; an inclusion list fails visibly instead.

WHAT THIS DOES NOT DO. It never checks that a declaration is *true*. A section can
mark E as data-state="derived" and derive nothing. That is the "green gates, wrong
book" class, and it stays with the rigor-reviewer pass.

Usage:
    python check_provenance.py FILE.html [FILE.html ...]   # gate; exit 1 on fail
    python check_provenance.py --inventory FILE.html ...   # dump the worklist
    python check_provenance.py --self-test                 # fixtures
"""
import re
import sys
from collections import defaultdict

# --- the judgement half: canonical name -> symbols as written in the source ----
# Written from the --inventory dump over all 17 modules, not from memory.
# key   = canonical data-sym value the marker must carry
# value = normalised symbols (as this script spells them) that map to it
#
# An entry is a symbol as this script normalises it, optionally narrowed to a
# unit with `sym@unit-substring`. The narrowing exists because `k` is leg
# stiffness in kN/m in Modules 8-9 and hydraulic permeability in m^4/(N s) in
# Module 4; one is a lumped whole-body fit, the other is the borrowed
# constitutive parameter the chemistry plan owes a trace.
#
# Provenance of the list itself: every entry marked [inv] was read off the
# `--inventory` dump of 2026-09-09 over all 17 modules (494 assignments, 156
# distinct symbols). Entries marked [pre] are pre-registered names the course
# does not use yet but the chemistry build will, so the first use is gated
# rather than the retrofit.
GATED = {
    # --- stiffness ----------------------------------------------------------
    "E":           ["E@Pa", "E_bone", "E_lin", "E_inst", "E_stiff",     # [inv]
                    "E_soft", "E_f", "E_tens", "E_cart", "E_b", "E_t"],
    "E_apatite":   ["E_m", "E_apatite", "E_min"],                    # [inv]
    "E_collagen":  ["E_c", "E_collagen", "E_col"],                   # [inv]
    "G":           ["G@Pa"],                                         # [inv]
    # E_V and E_R (Voigt/Reuss) are computed bounds, not borrowed: not gated.
    # --- strength -----------------------------------------------------------
    "sigma_c":     ["sigma_c", "sigma_comp"],                        # [inv]
    "sigma_f":     ["sigma_f", "sigma_uts", "sigma_max"],            # [inv]
    "sigma_0":     ["sigma_0"],                                      # [inv]
    "sigma_Y":     ["sigma_Y", "sigma_y", "sigma_yield"],            # [pre]
    # --- cartilage / poroelastic -------------------------------------------
    "H_A":         ["H_A", "H_a"],                                   # [inv]
    "c_F":         ["c_F", "c_f"],                                   # [inv]
    "k_perm":      ["k@m^4", "k_perm", "k_h"],                       # [inv]
    "mu_fric":     ["mu", "mu_eq", "mu_b", "mu_eff"],                # [inv]
    "nu":          ["nu", "nu_s"],                                   # [pre]
    # --- muscle -------------------------------------------------------------
    "F_max":       ["F_max", "F_0", "F_iso"],                        # [pre]
    "v_max":       ["v_max"],                                        # [pre]
    "a_hill":      ["a_hill"],                                       # [pre]
    "tau_act":     ["tau_act"],                                      # [inv]
    "tau_deact":   ["tau_deact"],                                    # [inv]
    "tau_relax":   ["tau_c", "tau_m", "tau_r", "tau_d",              # [inv]
                    "tau_relax", "tau_sigma", "tau_gel"],
    # --- chemistry (Module 0 section 3 onward) ------------------------------
    "dG0_ATP":     ["dG0_ATP", "dG0", "DeltaG0", "DeltaG0_ATP"],     # [pre]
    "c_metab":     ["c_ATP", "c_ADP", "c_Pi", "c_Ca", "c_metab"],    # [pre]
    # --- entropic elasticity (Module 0 section 4) ---------------------------
    "E_elastin":   ["E_elastin", "E_el"],                            # [pre]
    "lp_collagen": ["lp_collagen", "lp", "ell_p", "l_p"],            # [pre]
    # --- water and ions (Module 0 section 5) --------------------------------
    "eps_r_water": ["eps_r", "epsilon_r", "eps_r_water"],          # [pre]
    # --- kinetics (Module 0 section 6) --------------------------------------
    "k_on": ["k_on", "k_off", "K_d", "K_M", "k_1", "k_2"],        # [pre]
    "Q10": ["Q10", "Q_10", "E_a", "n_H"],                          # [pre]
    # --- macromolecular architecture (Module 0 section 7) -------------------
    "L_collagen": ["L_c", "L_helix", "L_collagen"],                # [pre]
    # --- bone remodeling ----------------------------------------------------
    "k_remodel":   ["k_remodel"],                                    # [pre]
    "rho_tissue":  ["rho_b", "rho_bone", "rho_t", "rho_m"],          # [pre]
    # --- locomotion energetics (Amendment 5, Modules 8/9) -------------------
    "VO2max":      ["VO2max"],                                       # [pre]
    "E_O2":        ["E_O2"],                                         # [pre]
    "PCr_conc":    ["PCr_conc"],                                     # [pre]
    "C_gly":       ["C_gly"],                                        # [pre]
    "CoT_run":     ["CoT_run"],                                      # [pre]
}
# reverse index, built once: {sym: [(unit_substring_or_None, canon), ...]}
_ALIAS = defaultdict(list)
for _canon, _ws in GATED.items():
    for _w in _ws:
        _sym, _, _unit = _w.partition("@")
        _ALIAS[_sym].append((_unit or None, _canon))


def canonical(sym, unit):
    """Which canonical parameter this assignment is, or None if not gated."""
    for want, canon in _ALIAS.get(sym, ()):
        if want is None or want in unit:
            return canon
    return None


STATES = ("derived", "module0", "measured")

# --- the mechanical half -------------------------------------------------------
BOX_OPEN = re.compile(r'<div class="(keyresult|prop|thm|lem)"')
ANY_BLOCK = re.compile(r'<div class="[a-z]+"')
BOXED_TEX = re.compile(r"\\boxed\{")

_INNER = r"(?:\\(?:mathrm|text|mathsf|rm)\s*\{[^{}]{1,20}\}|[^{}]){1,30}"
_SUB = (r"(?:\{" + _INNER + r"\}"
        r"|\\(?:mathrm|text|rm)\s*\{[^{}]{1,20}\}"
        r"|[A-Za-z0-9])")

# A TeX control word that is decoration, never a quantity. `60^\circ=0.300\
# \mathrm{m}` would otherwise report a symbol named "circ": the real symbol is
# the one before the `=`, and `\circ` is a superscript glyph on the number.
NOT_A_SYMBOL = {
    "circ", "ast", "star", "approx", "simeq", "times", "cdot", "pm", "mp",
    "le", "ge", "ll", "gg", "to", "quad", "qquad", "text", "mathrm", "rm",
    "left", "right", "frac", "tfrac", "dfrac", "sqrt", "sin", "cos", "tan",
    "log", "ln", "exp", "min", "max", "sum", "int", "prime", "degree",
}
SYM = rf"\\?[A-Za-z]{{1,12}}(?:_{_SUB})?"
REL = r"(?:=|\\approx|\\simeq|\\sim)"
NUM = r"-?[0-9]+(?:\.[0-9]+)?(?:\s*\\times\s*10\^\{?-?[0-9]+\}?)?"
GAP = r"(?:\\[,;:!]|\\ |~|\s)*"
UNIT = r"\\(?:mathrm|text)\{[^{}]{1,40}\}"
# The unit is OPTIONAL. It is the filter that keeps --inventory readable, but a
# constitutive parameter can be dimensionless -- friction mu in Module 4 §7 and
# Poisson's ratio nu carry no \mathrm{} group and would otherwise be invisible
# to this gate. So: an assignment WITH a unit enters the inventory; an
# assignment of a symbol already on GATED is gated with or without one.
ASSIGN = re.compile(
    rf"({SYM}){GAP}{REL}{GAP}(?:\\?sim{GAP})?{NUM}{GAP}({UNIT})?")

MARKER = re.compile(
    r'<span class="prov"([^>]*)>(.*?)</span>', re.S)
ATTR = re.compile(r'data-(sym|state)="([^"]*)"')

STRIP = re.compile(r"<svg\b.*?</svg>|<pre\b.*?</pre>", re.S | re.I)


def normalise(sym):
    """`\\sigma_c` -> `sigma_c`; `W_{\\rm tr}` -> `W_tr`; `E_{b}` -> `E_b`."""
    s = sym
    for w in ("\\text", "\\mathrm", "\\mathsf", "\\rm"):
        s = s.replace(w, "")
    s = s.replace("{", "").replace("}", "").replace("\\", "")
    return re.sub(r"_+", "_", "_".join(s.split())).strip("_")


def blank(s, spans):
    """Replace each span with spaces, so every line number stays correct."""
    out = list(s)
    for a, b in spans:
        for i in range(a, b):
            if out[i] != "\n":
                out[i] = " "
    return "".join(out)


def boxes(s):
    """Yield (start, end) of every boxed region: the four box divs plus \\boxed{}.

    A div block runs to the next block opener, the same approximation
    check_proofs.py uses; nested divs are rare here and only widen a box.
    """
    opens = [m.start() for m in ANY_BLOCK.finditer(s)]
    for m in BOX_OPEN.finditer(s):
        nxt = [p for p in opens if p > m.start()]
        yield (m.start(), nxt[0] if nxt else len(s))
    for m in BOXED_TEX.finditer(s):
        yield (m.start(), min(m.start() + 400, len(s)))


def scan(path):
    """-> (hits, markers, errors, tried).

    hits: [(line, written, canon, unit, in_box)] over the whole prose body.
    The box flag is a priority hint for --inventory, not a filter: the
    inventory run of 2026-09-09 showed the course states its constitutive
    parameters in prose, definitions and tables, and consumes them in boxes.
    Only 91 of the course's units-bearing assignments were inside a box, and
    `E = 17 GPa` (module02.html:171) was not one of them. See §2.2c.
    """
    raw = open(path, encoding="utf-8").read()
    s = blank(raw, [(m.start(), m.end()) for m in STRIP.finditer(raw)])

    boxed = list(boxes(s))
    hits = []
    for m in ASSIGN.finditer(s):
        if m.start() and s[m.start() - 1] in "^_":
            continue          # a superscript/subscript glyph, not a quantity
        written = normalise(m.group(1))
        if written.split("_")[0] in NOT_A_SYMBOL:
            continue
        unit = m.group(2) or ""
        canon = canonical(written, unit)
        if not unit and not canon:
            continue          # bare number, not a gated symbol: not our business
        hits.append((s.count("\n", 0, m.start()) + 1, written, canon, unit,
                     any(a <= m.start() < b for a, b in boxed)))

    markers, errors, tried = {}, [], set()
    for m in MARKER.finditer(raw):
        attrs = dict(ATTR.findall(m.group(1)))
        line = raw.count("\n", 0, m.start()) + 1
        sym, state, body = attrs.get("sym"), attrs.get("state"), m.group(2)
        if sym:
            tried.add(sym)
        if not sym or not state:
            errors.append((line, "prov marker missing data-sym or data-state"))
            continue
        if state not in STATES:
            errors.append((line, f'data-state="{state}" is not one of '
                                 f'{"/".join(STATES)}'))
            continue
        if state == "module0" and not re.search(r'<a\s[^>]*href\s*=', body):
            errors.append((line, f'{sym}: data-state="module0" with no <a href> '
                                 f'— a pointer with no link is not a pointer'))
            continue
        if state == "measured":
            tail = body.split(":", 1)[1] if ":" in body else ""
            if "because" not in body and len(tail.strip()) < 40:
                errors.append((line, f'{sym}: data-state="measured" with no '
                                     f'reason — say "because …" or give 40+ '
                                     f'characters after a colon'))
                continue
        if sym not in GATED:
            errors.append((line, f'data-sym="{sym}" is not a canonical name '
                                 f'(chemistry-audit-and-plan.md §2.2c)'))
            continue
        markers.setdefault(sym, line)
    return hits, markers, errors, tried


def gate(paths):
    bad = 0
    for path in paths:
        hits, markers, errors, tried = scan(path)
        need = {}
        for line, written, canon, _, _ in hits:
            if canon and canon not in markers and canon not in tried:
                need.setdefault(canon, (line, written))
        n = len(need) + len(errors)
        bad += n
        print(f"[check_provenance] {path}: {len(hits)} parameter "
              f"assignment(s), {len(markers)} declaration(s), {n} issue(s)")
        for line, msg in sorted(errors):
            print(f"  - line {line}: {msg}")
        for canon, (line, written) in sorted(need.items()):
            print(f"  - line {line}: ${written}$ is gated as '{canon}' but the "
                  f"module declares no provenance. Add "
                  f'<span class="prov" data-sym="{canon}" '
                  f'data-state="derived|module0|measured">…</span>')
        if not n:
            print("  every gated parameter declares its provenance. "
                  "(This does not check that the declaration is TRUE — "
                  "that stays with rigor-reviewer.)")
    return 1 if bad else 0


def inventory(paths):
    """The worklist: every units-bearing assignment, grouped by symbol.

    Sorted by how often the course commits to the symbol. Read this before
    writing GATED — the inclusion list is meant to be measured, not recalled.
    """
    by = defaultdict(list)
    for path in paths:
        for line, written, canon, unit, in_box in scan(path)[0]:
            by[written].append((path, line, canon, unit, in_box))
    print(f"[check_provenance --inventory] {len(paths)} file(s), "
          f"{sum(len(v) for v in by.values())} assignment(s), "
          f"{len(by)} distinct symbol(s)\n")
    for written in sorted(by, key=lambda w: (-len(by[w]), w)):
        rows = by[written]
        canon = rows[0][2]
        tag = f"GATED as {canon}" if canon else "not gated"
        units = sorted({u for _, _, _, u, _ in rows})
        nbox = sum(1 for r in rows if r[4])
        print(f"{written:<16} {len(rows):>4} ({nbox} boxed)  [{tag}]  "
              f"{' '.join(units[:4])}")
        for path, line, _, _, _ in rows[:40]:
            print(f"                       {path}:{line}")
    return 0


FIXTURES = [
    ('<div class="keyresult">$E\\approx 17\\ \\mathrm{GPa}$</div>', 1,
     "gated symbol in a box with no marker"),
    ('<div class="keyresult">$E\\approx 17\\ \\mathrm{GPa}$</div>'
     '<span class="prov" data-sym="E" data-state="measured">measured, not '
     'derived, because no chemistry in this course reaches a whole tissue.'
     '</span>', 0, "same box, declared"),
    ('<p>$E\\approx 17\\ \\mathrm{GPa}$</p>', 1,
     "plain prose is gated too — the course states E outside any box"),
    ('<p>$F_{\\mathrm{comp}}=1717\\ \\mathrm{N}$</p>', 0,
     "a nested-\\mathrm subscript parses, and F_comp is not on the list"),
    ('<div class="keyresult">$M=70\\ \\mathrm{kg}$, $R=14\\ \\mathrm{mm}$</div>',
     0, "ungated symbols are ignored"),
    ('<div class="keyresult">$E\\approx 17\\ \\mathrm{GPa}$</div>'
     '<span class="prov" data-sym="E" data-state="measured">measured.</span>',
     1, "state 3 with no reason"),
    ('<div class="keyresult">$E\\approx 17\\ \\mathrm{GPa}$</div>'
     '<span class="prov" data-sym="E" data-state="module0">Module 0 §2.</span>',
     1, "state 2 with no link"),
    ('<div class="keyresult">$E\\approx 17\\ \\mathrm{GPa}$</div>'
     '<span class="prov" data-sym="E" data-state="assumed">why not.</span>',
     1, "invalid state"),
    ('<svg><text>$E\\approx 17\\ \\mathrm{GPa}$</text></svg>'
     '<div class="keyresult">nothing here</div>', 0, "svg is skipped"),
]


def self_test():
    import tempfile
    import os
    bad = 0
    for html, want, why in FIXTURES:
        fd, p = tempfile.mkstemp(suffix=".html")
        os.write(fd, html.encode("utf-8"))
        os.close(fd)
        hits, markers, errors, tried = scan(p)
        need = {c for _, _, c, _, _ in hits
                if c and c not in markers and c not in tried}
        got = len(need) + len(errors)
        os.unlink(p)
        ok = got == want
        bad += not ok
        print(f"  {'ok  ' if ok else 'FAIL'} {why}: want {want}, got {got}")
    print(f"[check_provenance --self-test] {len(FIXTURES) - bad}/"
          f"{len(FIXTURES)} passed")
    return 1 if bad else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--self-test"]:
        sys.exit(self_test())
    if args and args[0] == "--inventory":
        sys.exit(inventory(args[1:]))
    if not args:
        print(__doc__.rsplit("Usage:", 1)[-1])
        sys.exit(2)
    sys.exit(gate(args))
