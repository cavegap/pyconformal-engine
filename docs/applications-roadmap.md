# PyConformal applications roadmap

PyConformal connects the examples in Vega Penagos & Olivero Zapata (2015)
to runnable Python and interactive explanations. Each example should name
the source worksheet or script, cite the relevant thesis section, and
include a way to verify the result.

The [thesis reading guide](thesis-guide.md), [reader exercises](exercises.md)
and [future-work questions](future-work.md) connect this status table to
a reproducible learning and research route. Update their references and
the [development log](development-log.md) when an example changes.

| Order | Deliverable | Acceptance criteria |
| --- | --- | --- |
| Available | [Group P presets and curved-tangent reconstruction](thesis-guide.md) | Matrix diagrams are linked to Figs. 1.1–1.3; the curved-path demo computes f′T and handles a critical point without assigning an angle to zero vectors. |
| Available | [Second SC problem: steady heat](square-heat.md) | Varying Dirichlet edge data, exact harmonic solution, temperature readouts and mean-value checks independent of the plotted grid. |
| Available | [Unified Peirce atlas](peirce-atlas.md) | Structure, imagery, scale and joined tiles preserve the selected coordinates. JavaScript maps are checked against Python and scale against a meridian derivative. |
| Available | [Ten reader exercises](exercises.md) | Source passages, expected written work, separate worked checkpoints and a Python numerical checker. |
| Available | [The square map](../examples/square-map.html), based on §3.1 and the polygons in `logo_UT.py` | Two synchronized planes follow P and P′. At ordinary points the opening is preserved. At the origin the opening doubles. The example runs offline with pointer and keyboard controls. |
| Available | [Disk to half-plane](../examples/disk-to-halfplane.html), based on `disco.mw` (§3.2) | The disk interior maps to the upper half-plane and the unit circle maps to the real axis except at the pole. The Python tests check reference points, the approach to the pole, and the inverse relation. |
| Available | [The exponential map](../examples/exponential-map.html), based on `exponencial.mw` (§3.3) | The labeled grid follows rays, circles and the periodic seam. Tests check magnitudes, arguments and periodicity. |
| Available | [Schwarz–Christoffel square](schwarz-christoffel-square.md) (§3.4, Fig. 3.17, p. 53) | The fixed-prevertex implementation checks vertex ordering, side constraints and interior values against a second formulation. Direct comparison with [SC Toolbox](https://github.com/tobydriscoll/sc-toolbox) remains open. |
| Available | [Lunar cubic coordinate grid](lunar-cubic-grid.md) (§4.2, Fig. 4.5) | Reproduce the source rectangle and its image under the cubic map. Verify the four corner images and document the inverse branch for resampling. |
| Available | [Georeferenced lunar demonstration](lunar-mercator.md) (§4.2, Figs. 4.4–4.5) | The LROC crop has three labeled craters and a local scale plot. Tests verify the inverse branch, landmark round trips and masking outside the source rectangle. |
| Available | [Square electrostatics](square-electrostatics.md) | The demo shows voltage and field lines. Tests check electrode values, insulating segments and an independent finite-difference solution inside the half-plane. |
| Available | [50 Ω coplanar waveguide](coplanar-waveguide.md) | Calculate a gap, trace the electric field and compare the ideal quasi-static impedance with scikit-rf. |
| Available | [Coplanar capacitive sensor](coplanar-sensor.md) | Vary the spacing between two strips and verify the coupling capacitance against a mesh-refined boundary-element solution. |
| Available | [Peirce hemisphere-to-square prototype](peirce-hemisphere.md) | The northern graticule and three lunar landmarks fit the normalized square. Tests verify the equator, corners and local orthogonality. A 192-point comparison checks agreement with PROJ. |
| Available | [Global Peirce quincuncial graticule](peirce-global.md) | The hemispheres join along the equator. Tests verify paired cut edges and the four south-pole copies. A 432-point comparison checks agreement with PROJ. |
| Available | [Global Peirce lunar mosaic](peirce-mosaic.md) | Inverse-sampled LROC imagery with four crater markers and a local-scale panel. Tests cover both hemispheres, poles, cut pairs and raster wrapping. |
| Available | [Recovered lunar outlines](lunar-thesis-outlines.md) | Follow the same boundary point from sphere to Mercator and through square, cube, Log(1+z) or Peirce, with the archival registration limits stated. |

## Peirce quincuncial projection

1. **Explore the [completed northern hemisphere prototype](peirce-hemisphere.md).**
   It composes stereographic projection, Cayley and the fixed-prevertex
   Schwarz–Christoffel square.
2. **Explore the [completed global graticule](peirce-global.md).**
   It adds the southern triangles and verifies the equator, cuts and
   antipodal pole under the same normalization as PROJ.
3. **Explore the [completed global lunar mosaic](peirce-mosaic.md).**
   It applies inverse sampling, tracks lunar control points and plots
   local linear scale.
   [Peirce's original paper](https://www.jstor.org/stable/10.2307/2369491) ·
   [PROJ peirce_q](https://proj.org/en/stable/operations/projections/peirce_q.html)

## Electrostatics and electronics

1. **Explore the [completed square electrostatics demo](square-electrostatics.md).**
   It uses 0 V and 1 V electrodes and two insulating sides.
2. **Explore the [completed 50 Ω coplanar waveguide example](coplanar-waveguide.md).**
   The ideal model has been checked against scikit-rf in the air-filled limit.
3. **Explore the [completed capacitive sensor example](coplanar-sensor.md).**
   Its two-strip, single-dielectric model establishes a benchmark for
   future multilayer or interdigitated geometries.
