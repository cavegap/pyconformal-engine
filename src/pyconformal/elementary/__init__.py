"""Elementary and trigonometric conformal maps (§3.3 of the thesis).

The exponential map is available as :func:`exponential`. Planned building
blocks include:

* :class:`Logarithm` — w = log z (principal branch).
* :class:`Power` — w = z^n.
* :class:`Sine`, :class:`Cosine`, :class:`Tangent`.
* :class:`Arcsine` — inverse trigonometric mapping.

These primitives compose with :class:`pyconformal.mobius.Mobius` to reproduce
the canonical examples of §3.3, e.g.

    w = (e^z − i) / (e^z + i)   (Figure 3.10)
    w = log((1 + z) / (1 − z))  (Figure 3.11)
    w = tan(z)                  (Figure 3.12)

References
----------
Vega Penagos & Olivero Zapata (2015), §3.3, Figures 3.10–3.14.
Maple source files: ``exponencial.mw``, ``logaritmo.mw``, ``composicion.mw``,
``trigonometricas.mw``, ``w_tan_z_.mw``.
"""

from __future__ import annotations

from cmath import exp

__all__ = ["exponential"]


def exponential(z: complex) -> complex:
    """Map horizontal lines to rays and vertical lines to circles by ``exp(z)``.

    The image has radius ``exp(z.real)`` and direction ``z.imag`` modulo
    a full turn. The map is injective on any open horizontal strip of
    height at most ``2π``.

    References
    ----------
    Vega Penagos & Olivero Zapata (2015), §3.3 (``exponencial.mw``).
    """
    return exp(z)
