"""Quasi-static conformal mapping model of a symmetric coplanar waveguide."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite, sqrt

from scipy.constants import c, epsilon_0
from scipy.optimize import brentq
from scipy.special import ellipkm1

from ._coplanar import coplanar_geometry, root_product

__all__ = [
    "CoplanarWaveguideResult",
    "coplanar_electric_field",
    "coplanar_waveguide",
    "gap_for_impedance",
]

_VACUUM_IMPEDANCE = 1 / (float(epsilon_0) * float(c))


@dataclass(frozen=True)
class CoplanarWaveguideResult:
    """Impedance in ohms, capacitance in F/m, and wave velocity in m/s."""

    impedance_ohm: float
    capacitance_f_per_m: float
    velocity_m_per_s: float


def coplanar_waveguide(width: float, gap: float, eps_r: float = 1.0) -> CoplanarWaveguideResult:
    """Evaluate a lossless, zero-thickness symmetric CPW in one dielectric.

    Width and gap use the same length unit. The model assumes semi-infinite
    ground planes, equal slots, uniform relative permittivity on both sides,
    and unit relative permeability. Only the ratio of width to gap enters.

    References
    ----------
    Ghione & Naldi (1984), *Analytical formulas for coplanar lines in
    hybrid and monolithic MICs*, Electronics Letters, 20(4), 179–181.
    """
    if not isfinite(eps_r) or eps_r < 1:
        raise ValueError("Relative permittivity must be finite and at least one.")
    _, parameter, complement = coplanar_geometry(width, gap)
    # ellipkm1 takes the complementary parameter, preserving the small gap limit.
    ratio = float(ellipkm1(parameter) / ellipkm1(complement))
    velocity = float(c) / sqrt(eps_r)
    impedance = _VACUUM_IMPEDANCE * ratio / (4 * sqrt(eps_r))
    return CoplanarWaveguideResult(impedance, 1 / (impedance * velocity), velocity)


def gap_for_impedance(width: float, impedance_ohm: float, eps_r: float = 1.0) -> float:
    """Return the symmetric gap, in the same unit as width, for a target impedance."""
    if not isfinite(width) or width <= 0:
        raise ValueError("Width must be positive and finite.")
    if not isfinite(impedance_ohm) or impedance_ohm <= 0:
        raise ValueError("Target impedance must be positive and finite.")

    def residual(log_ratio: float) -> float:
        return coplanar_waveguide(1.0, exp(log_ratio), eps_r).impedance_ohm - impedance_ohm

    lower, upper = -300.0, 300.0
    if residual(lower) > 0 or residual(upper) < 0:
        raise ValueError("Target impedance is outside the supported width-to-gap ratios.")
    gap = width * exp(brentq(residual, lower, upper))
    if not isfinite(gap) or gap <= 0:
        raise ValueError("The resulting gap is outside floating-point range.")
    return gap


def coplanar_electric_field(point: complex, width: float, gap: float) -> complex:
    """Return Ex + i Ey above the conductors, in V/m for a 1 V signal.

    Supply coordinates, width and gap in meters. The center conductor is
    centered at zero, and the grounds extend outward from the slots.
    The normalized field is independent of uniform permittivity.
    """
    if not (isfinite(point.real) and isfinite(point.imag) and point.imag > 0):
        raise ValueError("The field point must be finite and above the conductors.")
    half_span, parameter, _ = coplanar_geometry(width, gap)
    k = sqrt(parameter)
    z = point / half_span
    roots = root_product(z, k)
    derivative = -1j / (float(ellipkm1(parameter)) * roots) / half_span
    return -derivative.conjugate()
