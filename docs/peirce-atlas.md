# Unified Peirce lunar atlas

Open [the offline atlas](../examples/peirce-atlas.html). It combines
the [graticule](peirce-global.md), [mosaic and scale](peirce-mosaic.md)
and [joined tiles](../examples/peirce_tessellation.png) in one canvas.
Switching views preserves longitude, latitude and P. Graticule, crater
markers and poles can be shown independently.

The atlas continues the thesis recommendation on p. 59. It uses the
same whole-sphere normalization as `pyconformal.cartography`, with the
northern hemisphere inside the equatorial diamond and four southern
triangles in the corners. A selected south pole is one of four equivalent
boundary copies. The exceptional equatorial points are at edge midpoints.
These are different roles and are labeled separately.

## Four views

| View | What it shows | What its colors mean |
| --- | --- | --- |
| Hemisphere structure | Hemisphere layout, equator and graticule | Green: north; peach: south; grid colors distinguish meridians and parallels |
| Lunar mosaic | The complete LROC surface in one tile | Grayscale lunar imagery, not an elevation model |
| Local scale | Linear scale relative to a pole | Viridis colors on a logarithmic 1×–5× range, clipped above 5× |
| Joined tiles | A checkerboard of half-turn neighbors | The same surface and P repeated; no new geographic coverage |

For stereographic disk coordinate ζ constructed from absolute latitude,
the pole-relative length scale is `(1+|ζ|²)/sqrt(|1−ζ⁴|)`. Its value is
one at either pole and diverges at the four exceptional equatorial points.
Area ratios are the squares of length ratios. Geographic controls use
degrees; formulas in the page use radians.

## Offline assets and validation

Keep `sc-square.js`, `peirce-map.js`, `plot-panel.js`,
`peirce-atlas-data.js`, `peirce-scale-tile.png` and
`lunar-thesis-tile.jpg` beside the page. The latter is the undecorated
global tile, reused from the lunar tracing demo; the atlas itself does
not use the archival tracing's approximate registration.

Generate graticule data and the scale tile with
`python examples/peirce_atlas.py`. Regenerate the shared mosaic tile with
`python examples/lunar_thesis_outlines.py --interactive`. Both run offline
from the supplied LROC mosaic after installation. The generator splits
southern parallels at cuts so it does not draw artificial connecting lines.

The [browser-math verifier](../scripts/verify_browser_math.py) compares
the JavaScript forward map and scale with Python values, including cut
points and pole copies. The existing inverse tests check geographic
agreement along each joined edge. The [reader checkpoints](../examples/reader_checks.py)
and [Exercise E9](exercises.md#e9-poles-cuts-and-tile-joins) give a shorter
route for classroom use.

LROC WAC imagery credit: NASA / GSFC / Arizona State University.
The [mosaic notes](peirce-mosaic.md) preserve its source and attribution.
