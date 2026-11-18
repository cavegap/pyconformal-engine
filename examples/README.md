# Examples

## Group P

The [thesis companion](../docs/thesis-guide.md) gives a reading sequence
and [ten exercises](../docs/exercises.md). Run `python examples/reader_checks.py`
for numerical checkpoints after installing the local package.

Open [the gallery](index.html) to browse the complete set. In the new
[interactive Group P](group-p.html), drag O, A and B, then adjust the
rotation, reflection axis and dilation. All four views share the same
axis scale and report the angle at O and the two ray lengths.
Use the thesis presets for Figs. 1.1–1.3, then continue to
[curves and tangents](conformal-angle.html), a schematic reconstruction
of Fig. 3.2 with exact derivative vectors and a critical-point case.

From the repository root, install the package and regenerate the figure.

```bash
python -m pip install -e .
python examples/group_p.py
```

The script saves `examples/group_p.png`. It applies the Chapter 1
transformations in `pyconformal.linear` to a common grid and a marked
triangle. The labeled vertices, right-angle marker, and common axis scale
make angles, orientation, and lengths directly comparable across panels.

## The square map

Open `examples/square-map.html` in a browser. Drag P in the source plot or use
the coordinate sliders. The **Move P to the origin** button lets you compare
the mapped ray angles at the critical point. The demo uses the polygon
coordinates from the original `logo_UT.py` and the square-map example in
§3.1 of the thesis.

## From disk to half-plane

The [logarithmic object example](object-reveal.html) adds a new transformation:
a house is deformed by exp and recovered by the principal Log. The source
lies in the right half-plane. It is an inverse-designed teaching example.

Open `examples/disk-to-halfplane.html` in a browser. Use **Move to boundary**
to follow the image along the real axis. Use **Move to pole** to see the
image of `z = -1` at infinity. The matching Python function is
`pyconformal.mobius.disk_to_upper_half_plane`. The example follows §3.2,
Example 1, Figure 3.6 of the thesis and `disco.mw`.

## The exponential map

Open `examples/exponential-map.html` in a browser. Drag P to follow the two
grid lines through it and their images. Use **Compare −180° and +180°**
to see that the opposite edges map to the same ray. The Python function
is `pyconformal.elementary.exponential`.

## Schwarz–Christoffel square

Open `examples/schwarz-christoffel-square.html` in a browser. Drag P or use
the coordinate sliders to follow the mapped grid lines. Select −1, 0, 1,
or ∞ to see which corner each prevertex maps to.

From the repository root, run `python examples/schwarz_christoffel_square.py`
to regenerate `examples/schwarz_christoffel_square.png`. See the
[normalization and validation](../docs/schwarz-christoffel-square.md).

## Steady heat through the SC square

The [second SC boundary problem](schwarz-christoffel-heat.html) uses
`T = 60 + 40 Re(w) Im(w)` on a normalized square plate, with varying
Dirichlet temperatures on all four edges. It shares `sc-square.js` with
the geometric example. See [derivation and checks](../docs/square-heat.md).

## Lunar cubic grid

From the repository root, run `python examples/lunar_cubic_grid.py`
to regenerate `examples/lunar_cubic_grid.png`. See the
[coordinate conventions](../docs/lunar-cubic-grid.md) before applying the
map to a georeferenced image.

## Lunar Mercator raster

Run `python examples/lunar_mercator.py` to warp the supplied LROC crop and
regenerate `examples/lunar_mercator.png`. The
[lunar Mercator example](../docs/lunar-mercator.md) documents the raster
source, coordinate conversion, and landmark positions.

## 50 Ω coplanar waveguide

Open `examples/coplanar-waveguide.html` in a browser. Set the trace width and
relative permittivity, then select **Find 50 Ω gap**. The matching Python
functions and comparison are in the [CPW notes](../docs/coplanar-waveguide.md).

## Coplanar capacitive sensor

Open `examples/coplanar-sensor.html` to adjust the geometry and compare
the capacitance before and after doubling the gap. Run
`python examples/verify_coplanar_sensor.py` to reproduce the independent
boundary-element comparison. See the [sensor notes](../docs/coplanar-sensor.md).

## Peirce hemisphere square

Run `python examples/peirce_hemisphere.py` to reproduce the graticule
and crater markers. Add `--compare-proj` with pyproj installed to repeat
the numerical comparison. See the [projection notes](../docs/peirce-hemisphere.md).

## Global Peirce graticule

Run `python examples/peirce_global.py` to regenerate the global lunar
graticule. Add `--compare-proj` with pyproj installed to compare both
hemispheres. See the [global projection notes](../docs/peirce-global.md).

## Global Peirce lunar mosaic

Open the [unified Peirce atlas](peirce-atlas.html) to alternate between
hemisphere structure, imagery, scale and joined tiles. Longitude,
latitude and P remain synchronized. Run `python examples/peirce_atlas.py`
to regenerate its graticule and scale assets. See the
[asset list and verification](../docs/peirce-atlas.md).

Run `python examples/peirce_mosaic.py` to reproduce the global LROC
mosaic and scale panel offline. See the
[raster provenance and inverse method](../docs/peirce-mosaic.md).

## Recovered lunar outlines from Figure 4.5

Run `python examples/lunar_thesis_outlines.py` to regenerate the
comparison of the square and cube maps and the Peirce overlay.
Open `examples/lunar-thesis-interactive.html` to follow the same
boundary point from sphere to Mercator and through z², z³, Log(1 + z),
or Peirce. The sphere is an orthographic context view, not an additional
conformal step. Keep `lunar-thesis-data.js`, `lunar-thesis-tile.jpg` and
`lunar-thesis-globe.jpg` and `lunar-thesis-mercator.jpg` beside the HTML file.
Pass `--interactive` to the
Python script to regenerate the browser data.
See the [vector recovery and registration notes](../docs/lunar-thesis-outlines.md).

See the [applications roadmap](../docs/applications-roadmap.md) for the next examples.

## Mercator, global Peirce and repeated tiles

Run `python examples/peirce_tessellation.py` to generate
`peirce_tessellation.png`. Mercator is truncated at ±80°; the Peirce tile
includes the poles. Adjacent tiles use alternating 180° rotations. Their
edges represent the same geographic curves; the four corners are copies
of the south pole, not four separate poles.

The [global graticule](peirce_global.png) explains the hemisphere layout;
the [mosaic](peirce_mosaic.png) adds the imagery and relative scale;
the [tiling](peirce_tessellation.png) explains how the pieces join.
