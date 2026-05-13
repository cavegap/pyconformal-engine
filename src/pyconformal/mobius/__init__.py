"""Möbius (bilinear) transformations (§3.2 of the thesis).

A Möbius transformation has the form

    w = S(z) = (a z + b) / (c z + d),   with  ad ≠ bc.

The thesis (Theorem 11) gives an explicit *implicit formula* for the unique
Möbius transformation sending three distinct points to three distinct points,
and (Corollary 2) two important variants when one of the source or target
points is the point at infinity.

This module will expose:

* :class:`Mobius` — the basic class, with ``inverse``, ``compose``,
  ``derivative``, and extension to the extended complex plane.
* :meth:`Mobius.from_three_points` — implicit formula (Theorem 11).
* :meth:`Mobius.from_three_points_z_inf` — Corollary 2, Case 1.
* :meth:`Mobius.from_three_points_w_inf` — Corollary 2, Case 2.

References
----------
Vega Penagos & Olivero Zapata (2015), §3.2, Theorem 11 and Corollary 2.
Maple source files: ``bili.mw``, ``bili2.mw``, ``bilineal.mw``,
``funcion_implicita.mw``, ``corolario.mw``.
"""

from __future__ import annotations

__all__: list[str] = []
