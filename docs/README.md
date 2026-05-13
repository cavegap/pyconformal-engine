# Documentation

Documentation will be built with Sphinx + MyST + `pydata-sphinx-theme` and
deployed to GitHub Pages as part of Phase 7 of the roadmap.

Until then, the primary references are:

- [`../README.md`](../README.md) — installation and quickstart
- [`../ROADMAP.md`](../ROADMAP.md) — full project plan
- [`../thesis/`](../thesis/) — the underlying thesis PDF
- [`../notebooks/`](../notebooks/) — chapter-by-chapter tutorials

## Building locally (future)

```bash
uv pip install -e ".[docs]"
cd docs/
sphinx-build -b html . _build/html
```
