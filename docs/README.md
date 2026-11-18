# Documentation

Start with [the thesis companion](thesis-guide.md) and open the
[offline visual gallery](../examples/index.html). The guide pairs thesis
pages with runnable examples and distinguishes historical reconstructions
from new extensions.

## Reader route

1. [Read with the thesis](thesis-guide.md): concepts, notation and figure references.
2. [Try ten exercises](exercises.md): predictions, calculations and visual checks.
3. [Compare worked checkpoints](exercise-solutions.md): answers kept separate.
4. [Reproduce the results](reproducibility.md): installation, assets and commands.
5. [Choose future work](future-work.md): questions and independent validation.

Run `python examples/reader_checks.py` after installing the local package.
These files can be read directly on GitHub or in a Markdown viewer.

## Mapping and application notes

| Topic | Notes |
| --- | --- |
| Fixed SC square | [Map and normalization](schwarz-christoffel-square.md) |
| Boundary problems | [Electrostatics](square-electrostatics.md), [steady heat](square-heat.md) |
| Electronics | [Coplanar waveguide](coplanar-waveguide.md), [capacitive sensor](coplanar-sensor.md) |
| Lunar objects | [Cubic grid](lunar-cubic-grid.md), [Mercator raster](lunar-mercator.md), [archival tracing](lunar-thesis-outlines.md) |
| Peirce | [Hemisphere](peirce-hemisphere.md), [global graticule](peirce-global.md), [mosaic and scale](peirce-mosaic.md), [unified atlas](peirce-atlas.md) |
| Planning | [Applications roadmap](applications-roadmap.md), [full roadmap](../ROADMAP.md), [development log](development-log.md) |

The [original thesis](../thesis/) supplies academic attribution. The
[root README](../README.md) documents installation and project status.
The [public gallery and companion](https://cavegap.github.io/pyconformal-engine/)
are built from these sources with a lightweight static renderer. See
[publication and preview instructions](publishing.md). A larger Sphinx
API reference remains future work.
