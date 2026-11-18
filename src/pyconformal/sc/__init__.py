"""Schwarz-Christoffel transformations (§3.4 of the thesis, Theorem 12).

The Schwarz-Christoffel formula expresses a conformal map from the upper
half-plane Im(z) > 0 onto the interior of a polygon P with vertices
w₁, …, wₙ and exterior angles α₁, …, αₙ as

    f(z) = B + A ∫ (z − x₁)^(−α₁/π) ⋯ (z − xₙ₋₁)^(−αₙ₋₁/π) dz,

where x₁ < x₂ < ⋯ < xₙ₋₁ are the pre-vertices on the real axis.

The square with known prevertices is available as :func:`upper_half_plane_to_square`.
Planned general-purpose features include:

* :class:`SchwarzChristoffel` — the SC map class (Phase 5a).
* Routines for numerical evaluation of the SC integral with Gauss-Jacobi
  handling of the (z − xₖ)^(−αₖ/π) singularities.
* A Newton-with-scaling solver for the *parameter problem*: finding the
  pre-vertices automatically for arbitrary polygons (Phase 5b).

References
----------
Vega Penagos & Olivero Zapata (2015), §3.4, Theorem 12, Figures 3.15–3.17.
Driscoll, T. A. & Trefethen, L. N. (2002). *Schwarz-Christoffel Mapping*.
Cambridge University Press.
Maple source files: ``algo.mw``, ``proceso.mw``.
"""

from __future__ import annotations

from math import isfinite, sqrt

from scipy.special import elliprf

from .coplanar_sensor import coplanar_sensor_capacitance, coplanar_sensor_field
from .cpw import (
    CoplanarWaveguideResult,
    coplanar_electric_field,
    coplanar_waveguide,
    gap_for_impedance,
)

__all__ = [
    "CoplanarWaveguideResult",
    "coplanar_electric_field",
    "coplanar_sensor_capacitance",
    "coplanar_sensor_field",
    "coplanar_waveguide",
    "gap_for_impedance",
    "square_electrostatic_potential",
    "square_heat_temperature",
    "upper_half_plane_to_square",
]

_CORNER = 1 + 1j
_SIDE_INTEGRAL = float(elliprf(0.0, 1.0, 2.0))


def upper_half_plane_to_square(z: complex) -> complex:
    r"""Map the closed upper half-plane to the square ``[-1, 1] × [-1, 1]``.

    The prevertices ``-1, 0, 1, ∞`` map to ``-1+i, -1-i, 1-i, 1+i``
    respectively. Supply ``complex(float("inf"), 0)`` for the point at
    infinity. The open upper half-plane maps bijectively onto the interior.

    The normalized formula is
    ``1+i - (2i/K) R_F(z+1, z, z-1)`` with ``K = R_F(0, 1, 2)``.
    Real arguments on the branch cut are evaluated via square symmetries.

    Raises
    ------
    ValueError
        If the argument is below the real axis or is nonfinite other than
        the positive real infinity sentinel.

    References
    ----------
    Vega Penagos & Olivero Zapata (2015), §3.4, Figure 3.17, p. 53.
    NIST DLMF §19.32, https://dlmf.nist.gov/19.32.
    """
    if z == float("inf"):
        return _CORNER
    if not (isfinite(z.real) and isfinite(z.imag)) or z.imag < 0:
        raise ValueError("Expected a point in the closed upper half-plane or +infinity.")

    if z.imag == 0:
        x = abs(z.real)
        if x < 1:
            # The automorphism (x + 1)/(1 - x) rotates the square by π/2.
            integral = sqrt(1 - x) * float(elliprf(2.0, 1 + x, 2 * x))
            value = complex(1 - 2 * integral / _SIDE_INTEGRAL, -1)
        else:
            # Homogeneity avoids excessively large Carlson arguments.
            inverse_x = 1 / x
            integral = float(elliprf(1 + inverse_x, 1.0, 1 - inverse_x)) / sqrt(x)
            value = complex(1, 1 - 2 * integral / _SIDE_INTEGRAL)
        return 1j * value.conjugate() if z.real < 0 else value

    scale = max(1.0, abs(z.real), z.imag)
    normalized = z / scale
    offset = 1 / scale
    integral_complex = complex(elliprf(normalized + offset, normalized, normalized - offset))
    return _CORNER - 2j * (integral_complex / sqrt(scale)) / _SIDE_INTEGRAL


def square_electrostatic_potential(z: complex) -> float:
    """Return the half-plane potential for the square's 0 V and 1 V electrodes.

    In square coordinates the bottom side is grounded, the top is at 1 V,
    and the left and right sides are insulating. The potential is pulled
    back to the closed upper half-plane through the fixed-prevertex map.

    References
    ----------
    Vega Penagos & Olivero Zapata (2015), §3.4, Figure 3.17 for the map.
    Driscoll & Trefethen (2002), *Schwarz-Christoffel Mapping*, Chapter 4.
    """
    return (upper_half_plane_to_square(z).imag + 1) / 2


def square_heat_temperature(z: complex, *, cold: float = 20, hot: float = 100) -> float:
    """Pull back a harmonic square-plate temperature to the upper half-plane.

    For ``w = u + iv`` in the normalized square, prescribe
    ``T = (cold + hot)/2 + (hot - cold)*u*v/2`` on all four edges.
    The same expression solves steady isotropic conduction throughout
    the plate. These are varying Dirichlet data, with no internal source.
    This example extends the map of thesis section 3.4, Figure 3.17.

    The result is a temperature, not heat flux. A flux in physical units
    requires conductivity and a physical length scale.
    """
    if not (isfinite(cold) and isfinite(hot)) or cold >= hot:
        raise ValueError("Expected finite temperatures with cold < hot.")
    w = upper_half_plane_to_square(z)
    return (cold + hot) / 2 + (hot - cold) * w.real * w.imag / 2
