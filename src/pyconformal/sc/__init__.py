"""Schwarz-Christoffel transformations (§3.4 of the thesis, Theorem 12).

The Schwarz-Christoffel formula expresses a conformal map from the upper
half-plane Im(z) > 0 onto the interior of a polygon P with vertices
w₁, …, wₙ and exterior angles α₁, …, αₙ as

    f(z) = B + A ∫ (z − x₁)^(−α₁/π) ⋯ (z − xₙ₋₁)^(−αₙ₋₁/π) dz,

where x₁ < x₂ < ⋯ < xₙ₋₁ are the pre-vertices on the real axis.

This module will expose:

* :class:`SchwarzChristoffel` — the SC map class (Phase 5a).
* Routines for numerical evaluation of the SC integral with Gauss-Jacobi
  handling of the (z − xₖ)^(−αₖ/π) singularities.
* A Newton-with-scaling solver for the *parameter problem*: finding the
  pre-vertices automatically for arbitrary polygons (Phase 5b).

The thesis explicitly leaves the numerical determination of A and B for the
square-map case (page 53, Figure 3.17) as an open problem; resolving it is a
concrete milestone of this library.

References
----------
Vega Penagos & Olivero Zapata (2015), §3.4, Theorem 12, Figures 3.15–3.17.
Driscoll, T. A. & Trefethen, L. N. (2002). *Schwarz-Christoffel Mapping*.
Cambridge University Press.
Maple source files: ``algo.mw``, ``proceso.mw``.
"""

from __future__ import annotations

__all__: list[str] = []
