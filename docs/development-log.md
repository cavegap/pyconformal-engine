# Development log

This log records local development, not published package releases.
Version-control commits remain the authoritative file history.

## 2026-11-18: v0.1.0a1 publication preparation

- Added a public landing page with learning, application and lunar
  cartography routes, preserving the offline interactive examples.
- Added a static Markdown renderer that checks every local file and
  HTML fragment, excludes private workspace material, and refuses to
  replace an unmarked output directory.
- Added the GitHub Pages build/deployment workflow, a reader-feedback
  issue form and prerelease notes. Package and citation metadata use
  version 0.1.0a1.
- Local validation: 308 Python tests, 38 reader checkpoints, Ruff and
  MyPy passed. The site and representative interactive examples were
  checked over HTTP at desktop and mobile viewport sizes. Publication
  status is established by the matching GitHub workflow and release,
  rather than by this local record alone.

## 2026-11-18: thesis companion and completed teaching views

- Checked the thesis's vector diagrams, Definition 1 and curved-tangent
  argument against the PDF pages. Added Group P figure presets, the
  reflection parameter convention and negative dilation. Added an
  explicit-curve reconstruction of Figure 3.2 with derivative readouts
  and a critical-point case.
- Added a second SC boundary problem: steady temperature with linearly
  varying Dirichlet data on all four square edges. Exposed
  `square_heat_temperature` and shared the browser SC kernel between
  the geometry, heat and Peirce pages.
- Combined hemisphere structure, imagery, scale and joined tiles in the
  Peirce atlas. Switching views preserves the selected geographic point.
  Added an offline data/scale generator and JavaScript/Python checks.
- Added the thesis reading guide, ten reader exercises, separate worked
  checkpoints, a runnable numerical exercise checker, reproduction
  instructions and proposed future projects with validation criteria.
- Added thermal boundary-value and harmonic mean-value tests. Updated
  gallery, documentation navigation and the applications roadmap.
  The CI workflow now includes the reader checkpoints after the tests.

Local validation for this batch: 303 Python tests passed; all 38 reader
checkpoints passed; Ruff and MyPy passed. The shared browser kernel
matched Python on 36 SC and 216 Peirce samples with maximum coordinate
differences of 1.11e-15 and 3.54e-13. Pole-relative scale agreed with
four meridian-derivative references within 8.54e-11 relative error.
Browser interaction checks covered the five new or changed teaching
pages at 1440 px and 430 px viewport widths. These results describe
the local checkout, not a completed hosted CI run.

## 2026-11-18: preceding gallery and lunar sequence work

- Added movable Group P vectors and an inverse-designed logarithmic
  object example. Added visible formulas and application explanations
  to existing mapping and electronics pages.
- Strengthened lunar contour and landmark contrast. Explained the cubic
  scale and the pole-relative Peirce scale with their different metrics.
- Added sphere → Mercator → selected-map tracing and Log(1+z).
- Added the Mercator/Peirce/repeated-tile figure and edge-join regression
  checks. Retained the difference between the written z³ formula and
  the plotted z² contour in the thesis.

For each later change, record the concrete behavior, source passage or
new assumptions, reproduction command, validation result and any remaining
limitation. Do not mark a future-work item complete from a screenshot alone.
