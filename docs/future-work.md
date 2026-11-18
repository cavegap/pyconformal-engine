# Future work with a reference calculation

The thesis Recommendations (p. 59) leave numerical SC integration and
its connection to Peirce open for further work. The fixed square and
global Peirce prototype now provide starting cases. The following work
is proposed; none of these rows describes a completed general solver or
a validated physical device.

| Priority | Question | First implementation | Evidence needed before completion |
| --- | --- | --- | --- |
| 1 | How reliably can prescribed polygons be mapped? | Fixed prevertices for unequal rectangles, then the accessory-parameter problem for a small convex polygon | Check boundary correspondence, corner angles, interior residuals, inverse round trips and comparison against an independent SC implementation |
| 2 | How does sampling affect curves near SC corners and critical points? | Adaptive contour subdivision driven by mapped midpoint error | Record convergence versus an oversampled reference; keep branch cuts separate from continuous curves and report failure cases |
| 3 | How much do PCB substrate interfaces change the CPW result? | Add a finite-substrate quasi-static model with explicit geometry and effective permittivity | Compare air, thick-substrate and finite-substrate limits with scikit-rf or another documented reference; then study thickness, dispersion and losses separately |
| 4 | Can the sensor predict a partially inserted material sample? | Solve a two-material dielectric cross-section before adding interdigitated electrodes | Verify interface conditions, charge balance and mesh convergence against a separate FEM/BEM calculation; use experimental calibration before inferring a material property |
| 5 | Can the historical lunar tracing support geographic measurement? | Register independent named landmarks and reserve held-out controls | Publish coordinate conventions, fitting method and held-out residuals in physical units; propagate registration uncertainty into any measured length or area |
| 6 | How should a Peirce tile be oriented for a chosen region? | Add a central-meridian control to the unified atlas | Compare coordinates with PROJ for each orientation; verify all joins, both poles and scale away from branch points |
| 7 | Can another harmonic boundary problem be solved from the square? | Implement prescribed smooth boundary data through a numerical Dirichlet solve | Demonstrate grid convergence, boundary residuals and agreement with a manufactured harmonic solution such as the heat example |

## A reproducible student project

Choose one row and state a narrow question. Include a known case, an
independent reference, an error measure, the domain of validity and a
failure case. Preserve source data and record dependency versions.
Separate measured error from visual appearance: a smoother plot alone
does not demonstrate better numerical accuracy.

For a numerical contribution, provide code, one runnable example,
appropriate tests, updated documentation and a reader exercise. For a
physical application, add units and boundary conditions before presenting
an engineering conclusion. Use the [reading guide](thesis-guide.md) to
identify the mathematical result being extended and the
[development log](development-log.md) to record what actually changed.

## Reference starting points

The rectangle formulation is documented by
[NIST DLMF §19.32](https://dlmf.nist.gov/19.32); duplication methods for
the symmetric integrals appear in
[NIST DLMF §19.36](https://dlmf.nist.gov/19.36). General polygon mapping
needs an accessory-parameter solve beyond that fixed rectangle.

Use the existing [SC Toolbox](https://github.com/tobydriscoll/sc-toolbox)
comparison target for general polygons. The [PROJ Peirce documentation](https://proj.org/en/stable/operations/projections/peirce_q.html)
provides a spherical forward projection and alternative arrangements;
the repository's own inverse has separate regression checks. The
[CPW model notes](coplanar-waveguide.md) and
[sensor verification](coplanar-sensor.md) preserve their engineering
sources and the assumptions behind the current ideal models.
