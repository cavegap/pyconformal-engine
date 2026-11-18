# Read the thesis with PyConformal

This companion follows Vega Penagos & Olivero Zapata (2015),
*Implementación en software de aplicaciones conformes*. Keep the
[original thesis](../thesis/IMPLEMENTACION_EN_SOFTWARE_DE_APLICACIONES_CONFORMES.pdf)
beside the [offline gallery](../examples/index.html). Page references below
are the printed page numbers, which also match the pages in this PDF.
The thesis remains the historical source; this repository supplies
reconstructions, numerical checks and explicitly identified extensions.

## Start here

Clone or download the complete repository, then open `examples/index.html`
in a browser. Downloading an individual HTML file is insufficient for
pages that load local numerical scripts, data or image tiles. Keep the
directory structure intact. The supplied gallery needs no network access.

For Python, run these commands from the repository root:

```bash
python -m pip install -e ".[dev]"
python examples/reader_checks.py
python -m pytest
```

The first command installs the local checkout. `reader_checks.py` runs
deterministic numerical checkpoints for the exercises and exits with a
nonzero status if a check fails. The test suite covers mathematical
properties beyond those short checkpoints. Run `python -m mypy` and
`ruff check .` when contributing code.

## Reading sequence

| Thesis passage | Read or manipulate | What to establish | Exercise |
| --- | --- | --- | --- |
| §1.1, Figs. 1.1–1.3, pp. 10–12 | [Group P](../examples/group-p.html), figure presets | A matrix acts on both directions. Distinguish rotation angle from reflection-axis angle. | [E1](exercises.md#e1-vector-angles-and-orientation) |
| §1.2, Definition 1, p. 12; §1.3, pp. 18–19 | Group P and the [curves demo](../examples/conformal-angle.html) | Unsigned angle preservation and orientation are separate statements. At a point, the derivative acts on tangent vectors. | [E2](exercises.md#e2-curves-tangents-and-a-critical-point) |
| §3.1, Figs. 3.1–3.2, pp. 29–31; Theorems 9–10, pp. 30–32 | [Curves and tangents](../examples/conformal-angle.html) and [square map](../examples/square-map.html) | Both tangent arguments receive the same rotation when f′ is nonzero. At a critical point the mapped parameter derivatives vanish. | E2 |
| §3.2, Fig. 3.6, p. 37 | [Disk to half-plane](../examples/disk-to-halfplane.html) | Track an interior point, boundary point and pole separately. | [E3](exercises.md#e3-the-cayley-map-and-its-pole) |
| §3.3, pp. 43–48; §4.2, p. 56 | [Exponential](../examples/exponential-map.html), [object reveal](../examples/object-reveal.html) | Local conformality does not imply global injectivity. An inverse branch needs a domain. | [E4](exercises.md#e4-recovering-an-object-with-a-logarithm) |
| §3.4, Fig. 3.17, p. 53 | [SC square](../examples/schwarz-christoffel-square.html) | Check normalization, vertex order and the point at infinity. | [E5](exercises.md#e5-normalizing-the-sc-square) |
| New boundary problem built on §3.4 | [SC heat problem](../examples/schwarz-christoffel-heat.html) | Pull back a harmonic temperature with varying Dirichlet data on all edges. | [E6](exercises.md#e6-a-second-sc-boundary-problem) |
| New electronics extensions | [CPW](../examples/coplanar-waveguide.html), [sensor](../examples/coplanar-sensor.html) | Translate elliptic-integral ratios into impedance or capacitance under stated assumptions. | [E7](exercises.md#e7-electronics-and-model-assumptions) |
| §4.2, Figs. 4.4–4.5, p. 57 | [Lunar crop](../examples/lunar_mercator.png), [tracing sequence](../examples/lunar-thesis-interactive.html) | Separate source coordinates, geographic registration and the additional planar map. | [E8](exercises.md#e8-what-does-local-scale-measure), [E10](exercises.md#e10-audit-the-historical-figure) |
| Recommendations, p. 59 | [Unified Peirce atlas](../examples/peirce-atlas.html) | Connect the SC square to both hemispheres, repeated poles, cuts and local scale. | [E9](exercises.md#e9-poles-cuts-and-tile-joins) |

## How the reconstructions relate to the original figures

The Group P presets reconstruct the coordinate-direction diagrams in
Figures 1.1–1.3 with specified sample vectors. The thesis supplies no
numerical coordinates for those drawings. The oblique-angle preset
implements Definition 1 with x = A − O and y = B − O. Moving O changes
the base point of those vectors; the linear maps still act about the
fixed coordinate origin.

The Python API follows the thesis matrix convention:
`Reflection(theta)` has axis angle `theta/2`. The browser slider labels
the geometric axis angle α and therefore evaluates the matrix at `2α`.
For example, an axis at 30° corresponds to `Reflection(pi/3)`. A negative
dilation has determinant λ² > 0; it preserves orientation.

The [curves demo](../examples/conformal-angle.html) reconstructs the
argument of Figure 3.2 with explicit quadratic paths. It uses the chain
rule to compute exact tangents, rather than measuring chords in a
picture. It also distinguishes a vanishing mapped parameter derivative
from the limiting outgoing directions at a critical point. It is not a
digitization of the figure's curve coordinates.

The [lunar tracing](lunar-thesis-outlines.md) is different: its vertices
were recovered from the PDF vectors. The written Figure 4.5 formula is
z³, while the plotted contour agrees with z². Both are retained and
identified. Registration of this archival tracing to modern lunar
imagery is approximate and lacks independent ground-control errors.

## Conventions and limits

- Browser angle controls use degrees. Python rotations and reflections
  use radians. Geographic APIs accept degrees, with east-positive
  longitude and north-positive latitude.
- The SC square uses dimensionless coordinates `[-1,1] × [-1,1]`.
  The whole-sphere Peirce square adds a rotation and scaling to the
  hemisphere prototype. Do not compare their numeric coordinates without
  accounting for that normalization.
- Conformal maps preserve local angles at ordinary points. They do not
  generally preserve lengths, areas, shapes over finite distances, or
  global one-to-one behavior. Reflection is anti-conformal.
- The orthographic lunar sphere is a context view. It is not a conformal
  step in the Mercator-to-planar transformation chain.
- Electronics examples use ideal quasi-static, uniform dielectric models.
  The thermal example assumes steady isotropic conduction with constant
  conductivity. The examples do not establish fabrication tolerances or
  experimental accuracy.

## Reproduce and extend

Follow [the exercises](exercises.md) before opening the
[worked checkpoints](exercise-solutions.md). The [reproduction guide](reproducibility.md)
lists assets and commands. Use the [future-work questions](future-work.md)
to turn an extension into a project with a reference calculation and a
clear acceptance criterion. Record changes in the [development log](development-log.md)
and update the relevant guide, exercise and validation together.
