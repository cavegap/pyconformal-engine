"""Core abstractions: the :class:`ConformalMap` hierarchy (Chapter 2 of the thesis).

The thesis shows (Theorem 7) that a continuously differentiable map f : G → C
preserves angles in G iff f is holomorphic with ∂f/∂z̄ = 0, or antiholomorphic
with ∂f/∂z = 0. Theorem 8 strengthens this: f preserves both angles and
orientation iff f is holomorphic with f'(c) ≠ 0.

This module will expose:

* :class:`ConformalMap` — abstract base with ``__call__``, ``inverse``,
  ``derivative``, ``compose``, and the ``preserves_orientation`` attribute.
* :class:`HolomorphicMap` — concrete subclass for orientation-preserving maps.
* :class:`AntiholomorphicMap` — concrete subclass for orientation-reversing
  maps.
* Numerical Cauchy-Riemann verification (Type A and Type B of §1.3.1).
* Critical-point detection and angle-magnification factor *k* (Theorem 10).

References
----------
Vega Penagos & Olivero Zapata (2015), Chapter 2, Theorems 7–8, Lemma 1; and
§1.3 for the Type A / Type B Jacobian characterization.
"""

from __future__ import annotations

__all__: list[str] = []
