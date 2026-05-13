"""Elementary and trigonometric conformal maps (§3.3 of the thesis).

This module will expose the standard conformal building blocks:

* :class:`Exponential` — w = e^z.
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

__all__: list[str] = []
