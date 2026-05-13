"""PyConformal Engine — Conformal mapping for Python.

This package is a numerical, open-source reimplementation of the mathematical
content of the undergraduate thesis:

    Vega Penagos, C. A. & Olivero Zapata, H. A. (2015).
    Implementación en software de aplicaciones conformes.
    Universidad del Tolima, Ibagué, Colombia.
    Director: Mg. Juan Pablo Yáñez Puentes.

Module structure mirrors the chapter structure of the thesis:

* :mod:`pyconformal.linear` — Group P of angle-preserving linear maps
  (rotations, reflections, dilations). Chapter 1.
* :mod:`pyconformal.core` — Abstract :class:`ConformalMap` and the
  holomorphic / antiholomorphic distinction. Chapter 2.
* :mod:`pyconformal.mobius` — Möbius (bilinear) transformations. §3.2.
* :mod:`pyconformal.elementary` — Exponential, logarithmic, and trigonometric
  maps. §3.3.
* :mod:`pyconformal.sc` — Schwarz-Christoffel transformations. §3.4.
* :mod:`pyconformal.viz` — Visualization helpers and orthogonal grids.
  Chapter 4.
* :mod:`pyconformal.examples` — Reproductions of the thesis figures.
"""

from __future__ import annotations

__version__ = "0.0.1"

__all__ = ["__version__"]
