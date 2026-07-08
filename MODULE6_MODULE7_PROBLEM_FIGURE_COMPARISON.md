# Module 6 vs Module 7 Problem-Figure Comparison

Date: 2026-07-05

## Scope

This report compares the problem-set figures in `module06.html` and `module07.html`:

- Conceptual problems: C1-C10
- Derivational problems: D1-D10
- Computational problems: K1-K10

The comparison is about figure density and pedagogical treatment, not about whether the two modules cover the same biomechanics topic. Module 6 is about muscle-tendon / ligament mechanics; Module 7 is about balance, posture, and feedback control, so the figures should not be expected to be anatomically identical.

## Method

I parsed the 30 problem figures in each module and compared:

- SVG character count
- Number of visible shape tags (`path`, `line`, `rect`, `circle`, `ellipse`, `polyline`, `polygon`)
- Number of text labels
- Number of plotted polyline points
- Whether the figure used body/anatomy-like Tier-2 elements
- Direct inspection of the most extreme pairs, especially K3 and K6

No module HTML was edited.

## Bottom Line

There are clear differences.

The user's observation is supported most strongly for the computational figures. Module 6 K1-K10 are usually full computed plots with axes, numeric ticks, units, multiple curves or bars, legends, and marked limits/optima. Module 7 K1-K10 are mostly small thumbnails, formula callouts, or sparse schematics. K3 and K6 are the clearest examples.

The derivational figures in Module 7 are also generally sparser than Module 6, though a few Module 7 derivation figures use body sketches. The conceptual figures are mixed: several Module 7 C figures are comparable or richer because they include body context, but some individual conceptual figures, especially C8, are much thinner than their Module 6 counterparts.

I did not find that every Module 7 problem figure is sparse. The strongest difference is concentrated in K1-K10 and parts of D1-D10.

## Group Summary

| Group | Module 6 avg SVG chars | Module 7 avg SVG chars | Module 6 avg shapes | Module 7 avg shapes | Module 6 avg text labels | Module 7 avg text labels | Module 6 avg polyline points | Module 7 avg polyline points |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C1-C10 | 1500 | 1256 | 7.4 | 6.2 | 4.1 | 2.5 | 35.6 | 40.0 |
| D1-D10 | 1305 | 733 | 4.4 | 4.9 | 3.1 | 2.0 | 54.3 | 0.0 |
| K1-K10 | 3376 | 663 | 21.2 | 2.9 | 9.7 | 2.1 | 102.9 | 8.5 |

Interpretation:

- Conceptual figures are mixed. Module 7 has fewer labels on average but includes more body-context figures.
- Derivational figures in Module 7 have no plotted polyline data across D1-D10, while Module 6 often uses curves or process diagrams.
- Computational figures show the largest gap. Module 7 K figures are about one fifth the SVG size of Module 6 K figures by character count, with far fewer shapes, labels, and plotted points.

## Pair Metrics

| Problem | M6 chars | M7 chars | M7/M6 | M6 shapes | M7 shapes | M6 labels | M7 labels | M6 points | M7 points | Finding |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| C1 | 1155 | 1315 | 1.14 | 3 | 11 | 4 | 2 | 40 | 0 | M7 is not sparse here; it has more shape elements and body context, but fewer labels. |
| C2 | 2070 | 1697 | 0.82 | 13 | 14 | 6 | 2 | 0 | 0 | Comparable shape count; M7 has fewer labels. |
| C3 | 1319 | 808 | 0.61 | 6 | 5 | 4 | 3 | 40 | 0 | M7 is simpler and lacks the plotted polyline element present in M6. |
| C4 | 1991 | 2447 | 1.23 | 2 | 2 | 3 | 2 | 124 | 240 | M7 is not sparse by plotted-point count. |
| C5 | 1412 | 811 | 0.57 | 7 | 4 | 4 | 5 | 14 | 0 | M7 is smaller and has fewer shapes, though label count is similar/higher. |
| C6 | 745 | 1811 | 2.43 | 2 | 3 | 4 | 1 | 14 | 160 | M7 is richer by size and plotted points, but has fewer labels. |
| C7 | 1754 | 1054 | 0.60 | 8 | 8 | 4 | 1 | 68 | 0 | Similar shape count, but M7 has much less annotation and no plotted polyline. |
| C8 | 2815 | 787 | 0.28 | 26 | 4 | 3 | 4 | 56 | 0 | M7 is much sparser. Module 6 uses a richer mechanical-model schematic; Module 7 is a small relation/callout. |
| C9 | 801 | 999 | 1.25 | 2 | 6 | 4 | 2 | 0 | 0 | M7 is not sparse by shape count, but uses fewer labels. |
| C10 | 934 | 835 | 0.89 | 5 | 5 | 5 | 3 | 0 | 0 | Similar density; M7 has fewer labels. |
| D1 | 1694 | 746 | 0.44 | 6 | 7 | 2 | 1 | 90 | 0 | M7 has body context but is smaller and has no plotted curve. |
| D2 | 1394 | 792 | 0.57 | 6 | 5 | 3 | 3 | 60 | 0 | M7 is simpler and lacks the plotted curve. |
| D3 | 833 | 707 | 0.85 | 5 | 7 | 4 | 2 | 3 | 0 | Similar shape density; M7 has fewer labels. |
| D4 | 1364 | 613 | 0.45 | 3 | 4 | 4 | 2 | 62 | 0 | M7 is smaller and has no plotted curve. |
| D5 | 1012 | 522 | 0.52 | 4 | 1 | 3 | 2 | 28 | 0 | M7 is sparse; mostly a formula/result callout. |
| D6 | 938 | 652 | 0.70 | 3 | 5 | 2 | 2 | 40 | 0 | M7 is smaller and schematic, not plot-like. |
| D7 | 1085 | 620 | 0.57 | 4 | 0 | 3 | 3 | 40 | 0 | M7 is text/equation only; Module 6 includes a plotted curve. |
| D8 | 1356 | 608 | 0.45 | 4 | 4 | 3 | 2 | 60 | 0 | Similar shape count, but M7 is smaller and not curve-based. |
| D9 | 2301 | 1257 | 0.55 | 3 | 10 | 3 | 1 | 160 | 0 | M7 has more body-like shapes but much less plotted data and annotation. |
| D10 | 1074 | 810 | 0.75 | 6 | 6 | 4 | 2 | 0 | 0 | Similar shape count; M7 has fewer labels. |
| K1 | 4344 | 638 | 0.15 | 51 | 3 | 11 | 2 | 40 | 9 | M7 is much sparser. |
| K2 | 3642 | 504 | 0.14 | 14 | 2 | 11 | 3 | 146 | 0 | M7 is much sparser. |
| K3 | 5711 | 435 | 0.08 | 18 | 0 | 13 | 2 | 300 | 0 | M7 is text-only; this is the strongest difference. |
| K4 | 1903 | 605 | 0.32 | 9 | 3 | 8 | 2 | 40 | 6 | M7 is much sparser. |
| K5 | 5495 | 897 | 0.16 | 71 | 3 | 10 | 2 | 60 | 30 | M7 is much sparser. |
| K6 | 4389 | 593 | 0.14 | 14 | 4 | 12 | 1 | 210 | 0 | M7 is a sparse symbolic schematic; Module 6 is a full comparison plot. |
| K7 | 2421 | 509 | 0.21 | 11 | 3 | 10 | 2 | 60 | 0 | M7 is much sparser. |
| K8 | 2501 | 792 | 0.32 | 11 | 3 | 9 | 2 | 80 | 20 | M7 is sparser. |
| K9 | 949 | 832 | 0.88 | 4 | 4 | 4 | 2 | 12 | 20 | Similar size/shape density, though M7 has fewer labels. |
| K10 | 2402 | 821 | 0.34 | 9 | 4 | 9 | 3 | 81 | 0 | M7 is sparser. |

## Direct Examples

### K3

Module 6 K3 is a full computed plot. It has axes, numerical ticks, a rigid reference line, four colored tendon-stiffness curves, legend labels, and about 300 plotted polyline points.

Module 7 K3 is a text-only SVG:

```html
<text x="24" y="54">0.40 Hz, Kd=100</text>
<text x="24" y="88">→ Kp≈1004, Δ≈98 ms</text>
```

This is not just a stylistic difference. Module 6 gives the reader a visual computation to inspect; Module 7 gives the final parameter translation as two text lines.

### K6

Module 6 K6 is a full comparison plot with axes/ticks, three stress-time curves, a legend, and about 210 plotted points.

Module 7 K6 is a compact XcoM schematic: baseline, COM dot, one arrow, one XcoM circle, and one text label:

```html
<text x="132" y="32">Jmax≈21 N·s</text>
```

The Module 7 figure communicates the idea of an impulse/XcoM limit, but it does not show the computational sweep, numerical curve, or comparison structure that Module 6's K6 figure provides.

## Pattern Differences

### 1. Computational problem figures are the main gap

Module 6 computational figures mostly behave like miniature lab outputs. They show enough of the calculation that the figure itself contains scientific evidence: axes, units, curves, legends, optima, thresholds, or comparative regimes.

Module 7 computational figures mostly behave like visual reminders or result labels. Several are closer to icon-sized summaries than computed figures. K3 is text only, and K6 is a sparse schematic despite the problem asking for a numerical impulse/XcoM computation.

### 2. Module 7 derivation figures often replace curves with formulas or pictograms

Module 6 D figures frequently include plotted curves or mechanical diagrams. Module 7 D figures include some body sketches, but many are compact formula diagrams. D7 is the clearest case: Module 6 has a curve; Module 7 has no shape tags and only text/equation content.

### 3. Conceptual figures are mixed, not uniformly worse

Module 7 C1, C2, C4, C6, and C9 are not obviously sparse by raw size or shape count. Some use Tier-2 body context that Module 6 does not. But several conceptual figures still have fewer annotations, and C8 is a large drop in visual richness.

### 4. Module 7 uses a smaller thumbnail style

A recurring production difference is canvas/style scale:

- Module 6 K figures commonly use larger plot-style SVGs, often with `viewBox="0 0 340 150"` and `max-width:340px`.
- Module 7 problem figures commonly use smaller SVGs around `viewBox="0 0 240 130"` or `0 0 240 140` and `max-width:300px`.

That smaller format is not automatically wrong, but it contributes to the sparse feeling because it leaves less room for axes, ticks, legends, annotations, and anatomical context.

### 5. Module 7 has fewer labels in most pairings

Even where Module 7 has a comparable number of shapes, it often has fewer labels. This is visible in all three groups:

- C group: 2.5 labels on average in Module 7 vs 4.1 in Module 6
- D group: 2.0 vs 3.1
- K group: 2.1 vs 9.7

The K-group label drop is especially large because the Module 6 K figures include legends, tick labels, units, curve labels, and marked values.

## Things I Did Not Find

- I did not find missing problem figures. Both modules have 30 problem figures.
- I did not find that every Module 7 conceptual figure is sparse. Several are comparable or richer than Module 6 in body/context elements.
- I did not audit the main section figures outside the problem sets.
- I did not verify whether the numerical values inside the figures are correct; this report only compares the visible figure treatment and structure.

## Conclusion

The difference is real. Module 7's problem-set figures, especially K1-K10 and specifically K3/K6, are much sparser than Module 6's corresponding problem figures. The main distinction is that Module 6 computational figures usually visualize the computation, while Module 7 computational figures often summarize the result or idea with a small schematic or text callout.

If Module 7 is revised, the highest-impact target would be K1-K8, with K3 and K6 first. The next target would be D5-D8, where several derivation figures are formula-heavy and visually thin compared with Module 6.
