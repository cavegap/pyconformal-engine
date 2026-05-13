"""Visualization helpers and orthogonal grids (Chapter 4 of the thesis).

This module will expose:

* :func:`orthogonal_grid` — generate horizontal/vertical grids in a rectangular
  domain and map them through a :class:`pyconformal.core.ConformalMap`.
* :func:`apply_conformal_to_rectangle` — literal implementation of the
  flow diagram in Figure 4.1 of the thesis.
* Plotting helpers for reproducing the publication-quality figures of the
  thesis with ``matplotlib``.

References
----------
Vega Penagos & Olivero Zapata (2015), Chapter 4, Figures 4.1–4.5.
Maple source files: ``algo.mw``, ``proceso.mw``, ``mapeo_luna.mw``.
"""

from __future__ import annotations

__all__: list[str] = []
