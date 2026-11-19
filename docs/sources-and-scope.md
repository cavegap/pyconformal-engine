# Sources and scope

PyConformal Engine connects a historical thesis with reproducible software
and interactive reading. Use this page to distinguish the source material,
the present implementations and the questions that still need investigation.

## Mathematical and historical sources

- **Vega Penagos, C. A., and Olivero Zapata, H. A. (2015).**
  *Implementación en software de aplicaciones conformes*, Universidad del
  Tolima. The [original thesis](../thesis/IMPLEMENTACION_EN_SOFTWARE_DE_APLICACIONES_CONFORMES.pdf)
  is the source for the historical figures and applications. The
  [reading companion](thesis-guide.md) connects its passages to demonstrations
  and exercises; reconstructed figures are identified there.
- **Solanilla, L., Oostra, A., and Yáñez, J. P. (2016).**
  *Peirce quincuncial projection*, Revista Integración, 34(1), 23–38.
  [DOI: 10.18273/revint.v34n1-2016002](https://doi.org/10.18273/revint.v34n1-2016002).
  This is a mathematical and computational reference for the Peirce route.
  Peirce's projection, its conformal construction and its tiling properties
  are antecedents; their implementation here does not establish a new projection.
- **NIST Digital Library of Mathematical Functions.**
  [Conformal maps, §19.32](https://dlmf.nist.gov/19.32) and
  [numerical computation, §19.36](https://dlmf.nist.gov/19.36) provide references
  for the elliptic-integral constructions used in the square examples.
- **PROJ documentation.** The
  [Peirce quincuncial projection](https://proj.org/en/stable/operations/projections/peirce_q.html)
  supplies an independent implementation reference. Comparisons must state
  coordinate orientation, normalization and cut conventions.

## What the demonstrations support

| Route | Present implementation | Limit that matters |
| --- | --- | --- |
| Learn | Reconstructed thesis figures, interactive extensions and deterministic exercise checkpoints | Software checks do not measure learning outcomes. Local conformality requires the stated domain and a nonzero derivative. |
| Schwarz–Christoffel | A fixed half-plane-to-square construction and harmonic boundary examples | This is not a general solver for arbitrary polygons or their parameter problem. See the [square construction](schwarz-christoffel-square.md). |
| Electronics | Ideal quasi-static coplanar waveguide and capacitive-sensor examples | Material geometry, losses and physical measurements require further validation. Read the [waveguide](coplanar-waveguide.md) and [sensor assumptions](coplanar-sensor.md). |
| Map the Moon | Spherical lunar views, historical contour reconstruction and a Peirce atlas | Historical registration is approximate. The images support visualization rather than navigation or terrain measurement. See the [registration notes](lunar-thesis-outlines.md). |

Reconstructions recover an earlier example. Software extensions add controls,
comparisons or applications to that example. A claim of scientific novelty
requires a separate research question, comparison with prior work and evidence;
the existence of an interactive page or passing tests is not that evidence.

## Lunar data and attribution

The global imagery is derived from the
[LROC WAC global mosaic](https://data.lroc.im-ldi.com/lroc/view_rdr/WAC_GLOBAL),
credited to **NASA / GSFC / Arizona State University**. The bundled global
image has five pixels per degree and is used on a spherical Moon. It is
imagery, not an elevation model. The [mosaic documentation](peirce-mosaic.md)
records the request, resampling and coordinate conventions.

## Reproduce and continue

Start with the [reproduction commands](reproducibility.md), then follow the
[gallery's figure recipes](../examples/README.md). Each application page
describes its model and numerical checks. The [notation guide](notation.md)
records conventions shared by the demonstrations.

Keep unresolved questions separate from established results:
[future work](future-work.md) and the [applications roadmap](applications-roadmap.md)
describe the next investigations. Candidate research directions remain
proposals until their assumptions and validation have been reviewed.


## Animated opening and citation downloads

The opening follows one geographic location from an orthographic globe to
Peirce's square. Its grid and projection use the same conventions as the
atlas. Globe illumination and brightness are presentation choices, not a
lunar lighting prediction. Motion can be paused; a reduced-motion preference
starts the view paused. The animation suspends when hidden or out of view.

The [home page](../web/index.html#cite) supplies separate thesis and software
references, including BibTeX, RIS and CFF downloads. Thesis authorship and
supervision are credited separately. Downloads are local files and the copy
buttons require an explicit reader action.

The portraits are resized copies of the exact Wikimedia Commons files
listed below. Their file records identify them as public domain; credit
and provenance are retained independently of the software's MIT license.

| Portrait | Source record and credit |
| --- | --- |
| Hermann Schwarz | [ETH-Bibliothek, Ludwig Zipfel, circa 1890](https://commons.wikimedia.org/wiki/File:ETH-BIB-Schwarz,_Hermann_Amand_(1843-1921)-Portrait-Portr_11921.jpg) |
| Elwin Christoffel | [Wikimedia Commons, photographer unspecified](https://commons.wikimedia.org/wiki/File:Elwin_Bruno_Christoffel.JPG) |
| Charles S. Peirce | [Napoleon Sarony, 1891, New York Public Library / Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Charles_Sanders_Peirce.jpg) |

The [portrait provenance manifest](../web/landing/portraits/sources.json)
records download URLs, source and published SHA-256 hashes and resizing.
