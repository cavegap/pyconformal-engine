"""Möbius (bilinear) transformations (§3.2 of the thesis).

A Möbius transformation has the form

    w = S(z) = (a z + b) / (c z + d),   with  ad ≠ bc.

The thesis (Theorem 11) gives an explicit *implicit formula* for the unique
Möbius transformation sending three distinct points to three distinct points,
and (Corollary 2) two important variants when one of the source or target
points is the point at infinity.

The disk-to-half-plane example from §3.2 is available as
:func:`disk_to_upper_half_plane`. Planned general-purpose operations include:

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

from math import isfinite

__all__ = ["disk_to_upper_half_plane"]


def disk_to_upper_half_plane(z: complex) -> complex:
    """Evaluate the Cayley map ``i(1 - z) / (1 + z)`` at a finite point.

    The open unit disk maps to the upper half-plane. Its boundary maps to
    the real axis, with ``-1`` sent to the point at infinity, represented
    here by ``complex(float("inf"), 0)``.

    References
    ----------
    Vega Penagos & Olivero Zapata (2015), §3.2, Example 1, Figure 3.6
    (Maple worksheet ``disco.mw``).
    """
    if not (isfinite(z.real) and isfinite(z.imag)):
        raise ValueError("The source point must be finite.")
    if z == -1:
        return complex(float("inf"), 0)
    if max(abs(z.real), abs(z.imag)) > 2:
        # Keep the sum of the denominator's components within float range.
        scaled = z * 0.5
        return 1j * (0.5 - scaled) / (0.5 + scaled)
    return 1j * (1 - z) / (1 + z)
