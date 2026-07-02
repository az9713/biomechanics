# `check_svg.py` fix list — Modules 1–4

Output of `scripts/check_svg.py` run across `module01`–`module04`, with the **exact
replacement** for every hard issue. **No files were changed** — this is the
worklist for a later edit pass.

| Module | Hard issues | Advisories |
|---|---|---|
| module01 | 9 | 1 |
| module02 | 2 | 1 |
| module03 | 9 | 3 |
| module04 | 31 | 3 |

Hard issues block the hardening loop (`check_svg.py` exits 1). Advisories don't
fail; address at will.

---

## How to fix each class

**Literal `_` in an SVG `<text>` label → a real subscript.**
- **Single lowercase letter that has a Unicode subscript** → use the glyph directly.
  Available: `ₐ ₑ ₕ ᵢ ⱼ ₖ ₗ ₘ ₙ ₒ ₚ ᵣ ₛ ₜ ᵤ ᵥ ₓ` (a e h i j k l m n o p r s t u v x).
  So `F_m → Fₘ`, `W_s → Wₛ`, `r_s → rₛ`, `d_m → dₘ`, `F_t → Fₜ`, `ε_lo → εₗₒ`,
  `ε_hi → εₕᵢ`.
- **Capital letter, or a letter with no subscript glyph (b, c, d, f, g, q, …), or a
  multi-letter word** → use a `<tspan>` (matches the `r_L` fix already in module05):
  `X<tspan baseline-shift="sub" font-size="8">L</tspan>`. So `W_L`, `m_L`, `H_A`,
  `c_F`, `u_N`, `σ_E`, `F_ab`, `F_abd`, `E_tens`, `μ_eq`, `μ_eff`, `R_g` all take a
  tspan.

**Literal `^` in a label → a real superscript.**
`<tspan baseline-shift="super" font-size="8">…</tspan>`. So `R^(1/3) → R`+super`1/3`,
`R^(−2/3) → R`+super`−2/3`.

**Malformed `viewBox="0 0 0 0 W H"` → `viewBox="0 0 W H"`** (drop the leading `0 0`).

After editing, re-run `check_svg.py` (→ 0 hard) and `check_overlap.py` (tspans shift
label widths).

---

## module01 — 9 hard (all literal `_`)

| Current label | Exact fix |
|---|---|
| `W_s = m_s g` | `Wₛ = mₛg` |
| `W_L = m_L g` | `W`‹sub`L`› `= m`‹sub`L`›` g` |
| `F_m (muscle)` | `Fₘ (muscle)` |
| `r_s` | `rₛ` |
| `r_L` | `r`‹sub`L`› |
| `F_m (large)` | `Fₘ (large)` |
| `d_m ≈ 3 cm` | `dₘ ≈ 3 cm` |
| `W_L (small)` | `W`‹sub`L`›` (small)` |
| `r_L ≈ 35 cm` | `r`‹sub`L`›` ≈ 35 cm` |

‹sub`X`› = `<tspan baseline-shift="sub" font-size="8">X</tspan>`.

**Advisory:** 5 figures, no "Fig. N" reference in prose — cite them by number.

## module02 — 2 hard (all literal `_`)

| Current label | Exact fix |
|---|---|
| `ε_lo` | `εₗₒ` |
| `ε_hi` | `εₕᵢ` |

**Advisory:** 6 figures, no "Fig. N" reference in prose.

## module03 — 9 hard (all literal `_`)

| Current label | Exact fix |
|---|---|
| `W_s` | `Wₛ` |
| `F_ab` | `F`‹sub`ab`› |
| `W_s ≈ 0.84 BW (supported weight)` | `Wₛ ≈ 0.84 BW (supported weight)` |
| `abductor F_ab` | `abductor F`‹sub`ab`› |
| `F_abd` | `F`‹sub`abd`› |
| `F_t` | `Fₜ` |
| `dislocate when F_t = N tan β` | `dislocate when Fₜ = N tan β` |
| `m_L` (×2) | `m`‹sub`L`› |

**Advisories:** 54 figures, no "Fig. N" reference · mixed `<summary>` labels
("Answer" vs "solution") — unify · 4 polylines >120 points — decimate to ~40–60.

## module04 — 31 hard (11 `viewBox`, 18 `_`, 2 `^`)

### 11 malformed `viewBox` → drop the leading `0 0`
Mechanical: `viewBox="0 0 0 0 A B"` → `viewBox="0 0 A B"`. Resulting values, in
document order:

`0 0 440 240` · `0 0 440 240` · `0 0 450 240` · `0 0 440 230` · `0 0 460 250` ·
`0 0 440 240` · `0 0 460 230` · `0 0 450 230` · `0 0 450 230` · `0 0 450 220` ·
`0 0 460 230`

(These are the C2/C3/C4/C6/C8/C9/C10 and D2/D3/D8/D10 problem figures flagged in the
audit as **B1**.)

### 18 literal `_` → subscript

| Current label | Exact fix |
|---|---|
| `u_N = U(t)` | `u`‹sub`N`›` = U(t)` |
| `stiff: E_tens ≈ 12 MPa` | `stiff: E`‹sub`tens`›` ≈ 12 MPa` |
| `soft: H_A ≈ 0.6 MPa` | `soft: H`‹sub`A`›` ≈ 0.6 MPa` |
| `μ = μ_eq(1−F)` | `μ = μ`‹sub`eq`›`(1−F)` |
| `c_F⁻ (fixed)` | `c`‹sub`F`›`⁻ (fixed)` |
| `c₊ = c₋ + c_F` | `c₊ = c₋ + c`‹sub`F`› |
| `π = R_gT·Δc_ion` | `π = R`‹sub`g`›`T·Δc`‹sub`ion`› |
| `elastic: σ_E = H_A ε` | `elastic: σ`‹sub`E`›` = H`‹sub`A`›` ε` |
| `⇒ ∂u/∂t = H_A k ∂²u/∂z²` | `⇒ ∂u/∂t = H`‹sub`A`›` k ∂²u/∂z²` |
| `f = μ_eq · (1−F) · N   ⇒   μ_eff = μ_eq (1−F)` | subscript all three: `μ`‹sub`eq`›, `μ`‹sub`eff`› |
| `F ≈ 1 (fresh load) → μ_eff ≈ 0; F → 0 (drained) → ` | `μ`‹sub`eff`› |
| `ε∞ = σ / H_A` (×2) | `ε∞ = σ / H`‹sub`A`› |
| `fixed-charge density  c_F  (mol/L)` | `… c`‹sub`F`›` (mol/L)` |
| `equilibrium σ∞ = H_A ε₀` | `equilibrium σ∞ = H`‹sub`A`›` ε₀` |
| `friction  μ_eff` | `friction  μ`‹sub`eff`› |
| `cartilage: μ=μ_eq(1−F) stays low` | `cartilage: μ=μ`‹sub`eq`›`(1−F) stays low` |
| `(aggregate H_A)` | `(aggregate H`‹sub`A`›`)` |

Note: `Δc_ion` also carries a `_` — subscript `ion`. Several labels repeat
(`ε∞ = σ / H_A`, `μ_eq`) — fix **all occurrences**.

### 2 literal `^` → superscript

| Current label | Exact fix |
|---|---|
| `a ∝ R^(1/3)` | `a ∝ R`‹sup`1/3`› |
| `p₀ ∝ R^(−2/3)` | `p₀ ∝ R`‹sup`−2/3`› |

‹sup`X`› = `<tspan baseline-shift="super" font-size="8">X</tspan>`.

**Advisories:** 52 figures, no "Fig. N" reference · mixed `<summary>` labels · 19
polylines >120 points — decimate.

---

## Priorities

1. **module04 `viewBox` (11)** — the only *rendering* bug; mechanical one-liner each.
2. **All literal `_`/`^` (40 across M1–M4)** — cosmetic-but-visible; the sweep that
   brings the figures up to the module05 standard. Re-run `check_overlap.py` after,
   since tspans change label widths.
3. **Advisories** — cite figures by number; unify `<summary>` labels (M3, M4);
   optionally decimate the heavy polylines (M3, M4).

None of these are content/derivation changes — they are label-encoding and markup
fixes. The substance items live in `audit-modules.md`.
