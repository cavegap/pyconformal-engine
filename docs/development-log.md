# Development log

This log records local development, not published package releases.
Version-control commits remain the authoritative file history.

## 2026-11-19: figure interaction, reading guides and source navigation

- Added a shared sources-and-scope page and navigation to learning,
  reproduction and attribution. Distinguished historical reconstructions,
  software extensions and research proposals without asserting new results.
- Improved Group P handle selection, dragging, keyboard controls, diagram
  framing and the separation of the vertex O from the angle label.
- Clarified the curved-tangent view with dashed supports, directed arrows,
  signed source/image openings and a controllable local neighborhood.
- Reviewed all twelve interactive demonstrations. Added practical reading
  steps, source/result labels, visible slider values and routes to the
  model, reproduction commands and sources. Kept labels within plot bounds.
- Local validation passed: 329 Python tests, 38 reader checkpoints, Ruff,
  MyPy and the browser/Python numerical comparisons. The site built 45 pages
  with 742 valid local links and fragments. All 34 browser viewport cases
  and the inline-execution/outbound-connection policy probes passed.
- The separate animated landing-page prototype remains an integration
  proposal. Physical validation, learning outcomes and the research
  stability study are outside this presentation update.

## 2026-11-18: scientific notation and static-site hardening

- Added a notation guide and native MathML generated from TeX at build
  time. Main formulas in twelve interactive examples now use fractions,
  integrals, matrices and explicit domains rather than code-like text.
  Distinguished the SC constant from the elliptic integral, trace width
  from the complex image coordinate, and per-length capacitance from a
  derivative. Long formulas scroll within their panel on mobile.
- Added a reviewed public-asset manifest, a restrictive resource policy,
  local script/style extraction, unsafe-markup checks and limited secret
  signature detection. No visitor-side typesetter or remote math font
  is needed. Added a security policy with explicit hosting boundaries.
- Unified validation and Pages publication: the deployment requires all
  Python/OS jobs, lint, types and browser/policy checks to pass. Pinned
  action commits, isolated deployment privileges and hashed the two
  site-build dependencies. Added weekly dependency-update proposals.
- Local validation: 329 Python tests, 38 reader checkpoints, numerical
  browser/Python comparisons, Ruff and MyPy passed. Fifteen page routes
  passed browser checks at 1440 px and 430 px; policy probes blocked
  inline execution and outbound connections. The generated companion
  contains 44 HTML pages. This review is not an independent security audit.
- Enabled and verified dependency alerts, security-update proposals and
  private vulnerability reporting. Account authentication and hosting
  response headers remain separate owner/hosting responsibilities.

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
- Remote CI additionally checks Python code fences in Markdown with Ruff
  0.17.5. Aligned those snippets and pinned the formatter version so a
  fresh development installation uses the same formatting rules.

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
