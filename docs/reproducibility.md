# Reproduce the examples

Run commands from the repository root after installing the local checkout:

```bash
python -m pip install -e ".[dev]"
python examples/reader_checks.py
python -m pytest
ruff check .
ruff format --check .
python -m mypy
```

The Python package targets Python 3.10 or later. Core dependencies are
NumPy, SciPy and Matplotlib as declared in `pyproject.toml`. Figure and
JPEG-tile generators using Pillow need that package available as well;
Matplotlib installs it as a dependency. The browser-math verifier below
additionally needs Node.js. The reader exercises themselves do not.

## Regenerate assets

| Command | Output or purpose |
| --- | --- |
| `python examples/group_p.py` | Static Group P figure |
| `python examples/schwarz_christoffel_square.py` | Fixed SC square figure |
| `python examples/lunar_mercator.py` | Lunar crop, cubic image, scale and reference markers |
| `python examples/peirce_hemisphere.py` | Hemisphere disk/square figure |
| `python examples/peirce_global.py` | Global structural graticule |
| `python examples/peirce_mosaic.py` | Global imagery and relative-scale figure |
| `python examples/peirce_tessellation.py` | Mercator, one tile and joined tiles |
| `python examples/lunar_thesis_outlines.py` | Archived planar comparison and registered Peirce overlay |
| `python examples/lunar_thesis_outlines.py --interactive` | Browser tracing data and globe, Mercator and Peirce JPEG tiles |
| `python examples/peirce_atlas.py` | Atlas graticule data and scale PNG |
| `python examples/reader_checks.py --exercise E6` | One exercise's numerical checkpoints |
| `python examples/reader_checks.py --json` | All exercise checkpoints as JSON on stdout |
| `python scripts/verify_browser_math.py` | JavaScript/Python map comparison and a derivative-based scale check |

For unattended figure generation, set `MPLBACKEND=Agg` in the environment.
The supplied lunar source rasters make these commands usable offline.
Recovering the archival vectors again with
`python scripts/recover_lunar_outlines.py` additionally needs Poppler tools
on the path and uses the supplied thesis PDF.

## Keep the HTML dependencies together

Open [the gallery](../examples/index.html) from a complete checkout.

| Page | Local dependencies beyond its HTML |
| --- | --- |
| Group P, square, Cayley, exponential, object reveal | None for the interactive drawing |
| Curves and tangents | `plot-panel.js` |
| SC square | `sc-square.js` |
| SC heat problem | `sc-square.js`, `plot-panel.js` |
| Lunar thesis tracing | `lunar-thesis-data.js`, `lunar-thesis-globe.jpg`, `lunar-thesis-mercator.jpg`, `lunar-thesis-tile.jpg` |
| Unified Peirce atlas | `sc-square.js`, `peirce-map.js`, `plot-panel.js`, `peirce-atlas-data.js`, `peirce-scale-tile.png`, `lunar-thesis-tile.jpg` |

The heat and atlas pages use shared numerical scripts so their SC formula
has one browser implementation. Their plots are sampled displays; the
Python tests and browser-math comparison assess mathematical behavior.
The atlas uses a fixed central meridian of zero. Its markers are global
geographic references; the separate thesis-tracing registration remains
approximate.

## Report a result

For the public site and offline HTML companion, install `.[site]` and run
`python scripts/build_pages.py`. The [publishing guide](publishing.md)
documents the output, link validation and GitHub Pages workflow.

State the command, Python and dependency versions, selected inputs,
coordinate units and observed error. A numerical checkpoint tolerance is
not a measurement uncertainty. Record new results in the relevant model
notes and summarize completed changes in [the development log](development-log.md).
Future proposals belong in [future work](future-work.md), with an explicit
reference calculation and acceptance criterion.
