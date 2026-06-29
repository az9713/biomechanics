# SVG figure fidelity — tiers & tradeoffs

Reference for how anatomical (and other "real-entity") figures are drawn in this
course. **Default: Tier 2.**

## Guiding principle

Split figures into two kinds:

- **Physics / abstract** — free-body diagrams, force vectors, governing-equation
  sketches, charts, and **all animations**. These should stay **schematic** (flat
  SVG). A force vector or a `τ = r×F` diagram *must* be an abstraction; realism
  there hurts clarity, and raster/borrowed art can't be animated.
- **Anatomical / real-entity** — bones, joints, organs, devices. Here realism
  helps the reader connect a term to a thing. These are the figures the tiers
  below are about.

## The tiers

| Tier | Shape source | Look | Effort/figure | Accuracy | Licensing | Animatable |
|------|--------------|------|---------------|----------|-----------|------------|
| **1** | primitives (lines/rects/circles), flat fill | clean schematic | low | controlled, crude | none | yes |
| **2 (DEFAULT)** | shaded primitives (capsules + spheres) | stylized 3-D | medium | controlled, approximate shape | none | yes |
| **3** | hand-traced Bézier silhouettes + multi-layer shading | near-textbook | **high** | only as good as the freehand outline | none | yes |
| **Real** | adapt an open-license vector illustration | textbook | low–med | expert-correct | **attribution** | no |
| ~~AI~~ | image model (Higgsfield / "nano banana") | glossy raster | low | **hallucination risk** | model terms | no |

### Tier 1 — flat schematic
Primitives with flat fills (rounded-capsule lines, circles). What "stick diagrams"
are. Correct and fast; the right choice for physics diagrams. Reads as "crude" for
anatomy.

### Tier 2 — shaded primitives  *(default for anatomy)*
Same simple primitives, but shaded for volume:
- **cylinder gradient** across each capsule bone (a `<rect rx>` rotated to the
  bone's axis, filled with an object-bounding-box gradient → tube shading),
- **sphere (radial) gradients** on heads/knobs/condyles,
- a soft **`feDropShadow`** under the whole part (lifts it off the page),
- a blurred **specular highlight** on the lit side.

Reads convincingly 3-D, stays **self-contained, crisp, editable, license-free**,
and keeps anatomy under our control. Best realism-per-effort that carries no
external dependency. **This is the course default.**

### Tier 3 — hand-traced silhouettes + layered shading
The bone *outline* itself is hand-authored as cubic Bézier curves (real head,
neck, trochanters, condyles), then lit with a painter's layer stack (base
gradient → form shadow → ambient occlusion → core highlight → rim light →
specular → `feTurbulence` texture → cast shadow), each clipped to the silhouette;
optionally driven by SVG lighting filters (`feDiffuseLighting`/`feSpecularLighting`).
Near-textbook and still self-contained/animatable, **but**: ~60–100 lines of SVG
per bone, heavy iteration, and — the real catch — a freehand outline can be
*subtly wrong while looking authoritative*. Reserve for one or two "hero" figures.
Note: done *accurately* (by tracing a reference) it converges on "Real".

### Real — adapt open-license vector art
Reuse a professional medical illustration that already exists as licensed SVG
(Wikimedia / OpenStax CC-BY / Servier CC-BY / BodyParts3D / public-domain Gray's).
The expert already did the accurate outline; we recolor to our palette and overlay
our own markers/labels. Highest *correct* realism for the least drawing effort —
priced in **attribution** (CC-BY) or share-alike (CC-BY-SA), a possibly mismatched
style, heavier files, and no animation. The efficient route when true realism is
required.

### AI generation — avoid for anatomy
Image models produce glossy raster output but **hallucinate anatomy** (wrong
counts, invented structures, garbled labels). In a rigorous course, pretty-but-wrong
is worse than clean schematic. Acceptable only for purely decorative art, never for
load-bearing scientific anatomy.

## Decision

- **Default to Tier 2** for anatomical figures.
- Keep **physics diagrams and all animations at Tier 1** (schematic) — by design.
- Escalate to **Real** (with attribution) only when a figure genuinely needs
  textbook realism/accuracy beyond Tier 2.
- Use **Tier 3** only for a deliberate "hero" figure, and prefer tracing a
  reference (i.e. lean toward "Real") to avoid freehand-outline errors.
- **Never** AI-generate anatomy.
